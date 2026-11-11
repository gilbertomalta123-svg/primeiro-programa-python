import tkinter as tk

expressao_atual = ""

# Atualiza o texto do visor
def atualizar_visor(texto):
    visor.config(text=texto if texto else "0")

# Adiciona números ou operadores ao visor
def clique_botao(valor):
    global expressao_atual
    if expressao_atual == "Erro":
        expressao_atual = ""
    expressao_atual += str(valor)
    atualizar_visor(expressao_atual)

# Limpa completamente o visor
def limpar():
    global expressao_atual
    expressao_atual = ""
    atualizar_visor("0")

# Apaga apenas o último caractere digitado
def apagar_ultimo():
    global expressao_atual
    if expressao_atual == "Erro":
        limpar()
    else:
        expressao_atual = expressao_atual[:-1]
        atualizar_visor(expressao_atual)

# Calcula o resultado
def calcular():
    global expressao_atual
    if not expressao_atual:
        return
    try:
        resultado = str(eval(expressao_atual))
        if resultado.endswith(".0"):
            resultado = resultado[:-2]
        atualizar_visor(resultado)
        expressao_atual = resultado
    except Exception:
        atualizar_visor("Erro")
        expressao_atual = "Erro"

# Captura as teclas do teclado físico
def pressionar_tecla(event):
    tecla = event.char
    keysym = event.keysym

    if tecla in '0123456789+-*/.':
        clique_botao(tecla)
    elif tecla == ',':
        clique_botao('.')
    elif keysym in ('Return', 'KP_Enter'):
        calcular()
    elif keysym == 'BackSpace':
        apagar_ultimo()
    elif keysym == 'Escape' or tecla.lower() == 'c':
        limpar()

# Configuração da janela compacta
janela = tk.Tk()
janela.title("Calculadora")
janela.geometry("240x310")
janela.resizable(False, False)
janela.configure(bg="#1e1e1e")

# --- VISOR PEQUENO (1 linha compacta) ---
visor = tk.Label(
    janela, text="0", font=("Consolas", 18, "bold"),
    bg="#2d2d2d", fg="#ffffff", anchor="e",
    padx=10, pady=6, relief=tk.SUNKEN, bd=2
)
visor.grid(row=0, column=0, columnspan=4, padx=6, pady=8, sticky="ew")

# --- BOTÕES ---
botoes = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

for (texto, linha, coluna) in botoes:
    if texto == '=':
        btn = tk.Button(janela, text=texto, font=("Arial", 13, "bold"), bg="#6C6E6C", fg="white", bd=0, command=calcular)
    elif texto in '/*-+':
        btn = tk.Button(janela, text=texto, font=("Arial", 13), bg="#3c3c3c", fg="#d1810a", bd=0, command=lambda t=texto: clique_botao(t))
    else:
        btn = tk.Button(janela, text=texto, font=("Arial", 13), bg="#333333", fg="white", bd=0, command=lambda t=texto: clique_botao(t))
    btn.grid(row=linha, column=coluna, sticky="nsew", padx=2, pady=2)

# Botões inferiores: Limpar (C) e Apagar (⌫)
btn_limpar = tk.Button(janela, text="C", font=("Arial", 12, "bold"), bg="#494848", fg="white", bd=0, command=limpar)
btn_limpar.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)

btn_apagar = tk.Button(janela, text="⌫", font=("Arial", 12), bg="#3965A7", fg="white", bd=0, command=apagar_ultimo)
btn_apagar.grid(row=5, column=2, columnspan=2, sticky="nsew", padx=2, pady=2)

# Proporção das linhas (linha 0 do visor com peso 0 para não esticar)
janela.rowconfigure(0, weight=0)
for i in range(1, 6):
    janela.rowconfigure(i, weight=1)
for i in range(4):
    janela.columnconfigure(i, weight=1)

# Foco automático no teclado
janela.focus_force()
janela.bind("<Key>", pressionar_tecla)

janela.mainloop()
