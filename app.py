import tkinter as tk
from tkinter import PhotoImage, font, messagebox, ttk

# Criando a janela
janela = tk.Tk()
janela.title("Agendador de Tarefas")
janela.configure(bg="#C0C0C0")
janela.geometry("530x600")


frame_em_edicao = None

# Função adcionar tarefa


def adcionar_tarefa():
    global frame_em_edicao

    tarefa = entrada_tarefa.get().strip()
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None
        else:
            adcionar_item_tarefa(tarefa)
            entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Atenção - Entrada inválida",
                               "Insira uma tarefa antes de adcionar")


def adcionar_item_tarefa(tarefa):
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=(
        "Comic Sans MS", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    botao_editar = tk.Button(frame_tarefa, image=icone_editar, command=lambda f=frame_tarefa,
                             l=label_tarefa: preparar_edicao(f, l), bg="white", relief=tk.FLAT)
    botao_editar.pack(side=tk.RIGHT, padx=5)

    botao_deletar = tk.Button(frame_tarefa, image=icone_deletar,
                              command=lambda f=frame_tarefa: deletar_tarefa(f), bg="white", relief=tk.FLAT)
    botao_deletar.pack(side=tk.RIGHT, padx=5)

    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

    check_buuton = ttk.Checkbutton(
        frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
    check_buuton.pack(side=tk.RIGHT, padx=5)

    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_em_edicao

    frame_em_edicao = frame_tarefa
    entrada_tarefa.delete(0, tk.END)
    entrada_tarefa.insert(0, label_tarefa.cget("text"))


def atualizar_tarefa(nova_tarefa):
    global frame_em_edicao

    for widget in frame_em_edicao.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=nova_tarefa)


def deletar_tarefa(frame_tarefa):
    frame_tarefa.destroy()
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def alternar_sublinhado(label):
    fonte_atual = label.cget("font")
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)


def ao_clicar_entrada(event):
    if entrada_tarefa.get() == "Escreva sua tarefa aqui":
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.configure(fg="black")


def ao_sair_foco(event):
    if not entrada_tarefa.get().strip():
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
        entrada_tarefa.configure(fg="grey")


icone_editar = PhotoImage(file="botao-editar.png").subsample(4, 4)
icone_deletar = PhotoImage(file="botao-excluir.png").subsample(4, 4)


cabecalho_fonte = font.Font(family="Comic Sans MS", size=20,
                            weight="bold")
cabecalho_rotulo = tk.Label(janela, text="Agenda de tarefas",
                            font=cabecalho_fonte, bg="#C0C0C0", fg="#333").pack(pady=20)

frame = tk.Frame(janela, bg="#F5F5F5")
frame.pack(pady=10)

# Informar as tarefas
entrada_tarefa = tk.Entry(frame, font=(
    "Comic Sans MS", 12), relief=tk.FLAT, bg="white", fg="black", width=30)
entrada_tarefa.pack(side=tk.LEFT, padx=10)

# Botão de adcionar as tarefas
botao_adcionar = tk.Button(frame, text="Adcionar Tarefa", command=adcionar_tarefa,
                           bg="#DCDCDC", fg="black", height=1, width=20, font=("Roboto", 12), relief=tk.FLAT)
botao_adcionar.pack(side=tk.LEFT, padx=10)

# Criar um frame para a lista de tarefas com rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

barra_rolagem = tk.Scrollbar(
    frame_lista_tarefas, orient="vertical", command=canvas.yview)
barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=barra_rolagem.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(
    scrollregion=canvas.bbox("all")))

janela.mainloop()
