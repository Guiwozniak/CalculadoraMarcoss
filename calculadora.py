import tkinter as tk
import math
from fractions import Fraction  # NOVO

COR_FUNDO = "#212121"

def cor_botao(texto):
    if texto in ["DEL", "AC", "On", "Alpha"]:
        return {"bg": "#E53935", "fg": "#FFFFFF"}
    elif texto == "Shift":
        return {"bg": "#424242", "fg": "#FFFFFF"}
    elif texto == "Replay":
        return {"bg": "#BDBDBD", "fg": "#000000"}
    elif texto in ["=", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "Ans", "EXP", "+", "-", "X", "÷"]:
        return {"bg": "#E0E0E0", "fg": "#000000"}
    else:
        return {"bg": "#424242", "fg": "#FFFFFF"}

calc = tk.Tk()
calc.title("Calculadora Científica")
calc.configure(bg=COR_FUNDO)
calc.geometry("529x900")
calc.resizable(False, False)

var = tk.StringVar(value="0")
expressao = ""
resultado_mostrado = False

display = tk.Entry(calc, textvariable=var, font=("Arial", 34), bd=10, insertwidth=2, width=14,
                   borderwidth=4, relief="ridge", justify="right", bg="white")
display.grid(row=0, column=0, columnspan=6, pady=10, padx=10)

def formatar_numero(valor):
    try:
        if "Erro" in valor:
            return valor
        valor = valor.replace(".", "#").replace(",", ".").replace("#", ",")
        if "." in valor:
            inteiro, decimal = valor.split(".")
        else:
            inteiro, decimal = valor, ""
        inteiro_formatado = "{:,}".format(int(inteiro)).replace(",", ".")
        if decimal:
            return f"{inteiro_formatado},{decimal}"
        return inteiro_formatado
    except:
        return valor

def limpar():
    global expressao, resultado_mostrado
    expressao = ""
    var.set("0")
    resultado_mostrado = False

def limpar_entrada():
    global resultado_mostrado
    var.set("0")
    resultado_mostrado = False

def calcular():
    global expressao, resultado_mostrado
    try:
        resultado = eval(expressao.replace("÷", "/").replace("X", "*"))
        if resultado == float('inf') or resultado == float('-inf'):
            raise ZeroDivisionError
        resultado_str = str(round(resultado, 10)).replace(".", ",")
        var.set(formatar_numero(resultado_str))
        expressao = ""
        resultado_mostrado = True
    except ZeroDivisionError:
        var.set("Erro")
        expressao = ""
        resultado_mostrado = False
    except Exception:
        var.set("Erro")
        expressao = ""
        resultado_mostrado = False

def clique(valor):
    global expressao, resultado_mostrado

    if valor in "0123456789":
        if resultado_mostrado:
            atual = ""
            resultado_mostrado = False
        else:
            atual = var.get().replace(".", "")
        if atual == "0":
            novo = valor
        else:
            novo = atual + valor
        var.set(formatar_numero(novo))

    elif valor == ",":
        if resultado_mostrado:
            var.set("0,")
            resultado_mostrado = False
            return
        atual = var.get().replace(".", "")
        if "," in atual:
            return
        if atual == "" or atual == "0":
            var.set("0,")
        else:
            var.set(formatar_numero(atual + ","))

    elif valor in ["+", "-", "X", "÷"]:
        resultado_mostrado = False
        if expressao and expressao[-1] in "+-*/":
            expressao = expressao[:-1]
        entrada = var.get().replace(".", "").replace(",", ".")
        expressao += entrada + valor.replace("X", "*").replace("÷", "/")
        var.set("")

    elif valor == "=":
        entrada = var.get().replace(".", "").replace(",", ".")
        expressao += entrada
        calcular()

    elif valor == "C":
        limpar()

    elif valor == "AC":
        limpar_entrada()

    elif valor == "DEL":
        resultado_mostrado = False
        atual = var.get().replace(".", "")
        if len(atual) > 1:
            var.set(formatar_numero(atual[:-1]))
        else:
            var.set("0")

    elif valor == "x²":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            resultado = num ** 2
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "√":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            resultado = math.sqrt(num)
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "log":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            resultado = math.log10(num)
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "ln":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            if num <= 0:
                raise ValueError
            resultado = math.log(num)
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "^":
        resultado_mostrado = False
        entrada = var.get().replace(".", "").replace(",", ".")
        expressao = entrada + "**"
        var.set("")

    elif valor == "²√x":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            if num < 0:
                raise ValueError
            resultado = num ** 0.5
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "1/x":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            if num == 0:
                raise ZeroDivisionError
            resultado = 1 / num
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "%":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            resultado = num / 100
            var.set(formatar_numero(str(round(resultado, 10)).replace(".", ",")))
            resultado_mostrado = True
        except:
            var.set("Erro")

    elif valor == "ab/c":
        try:
            num = float(var.get().replace(".", "").replace(",", "."))
            fracao = Fraction(num).limit_denominator()
            var.set(f"{fracao.numerator}/{fracao.denominator}")
            resultado_mostrado = True
        except:
            var.set("Erro")

def criar_botao(texto, linha, coluna, span, largura):
    cores = cor_botao(texto)
    tk.Button(calc, text=texto, padx=20, pady=20, width=largura, font=("Arial", 12),
              bg=cores["bg"], fg=cores["fg"], relief="raised", bd=3,
              command=lambda t=texto: clique(t)) \
        .grid(row=linha, column=coluna, columnspan=span, padx=5, pady=5)

def criar_botao_redondo(canvas, x, y, raio, texto, comando):
    cores = cor_botao(texto)
    oval = canvas.create_oval(
        x - raio, y - raio, x + raio, y + raio,
        fill=cores["bg"], outline=""
    )
    text_id = canvas.create_text(
        x, y, text=texto, fill=cores["fg"], font=("Arial", 10, "bold")
    )
    def clique_evento(event):
        comando()
    canvas.tag_bind(oval, "<Button-1>", clique_evento)
    canvas.tag_bind(text_id, "<Button-1>", clique_evento)

botoes_retangulares = [
    ("Shift", 1, 0, 1, 3), ("Alpha", 1, 1, 1, 3),
    ("Modeclr", 1, 4, 1, 3), ("On", 1, 5, 1, 3),
    ("x⁻¹", 2, 0, 1, 3), ("nCr", 2, 1, 1, 3), ("Pol( )", 2, 4, 1, 3), ("x³", 2, 5, 1, 3),
    ("ab/c", 3, 0, 1, 3), ("√", 3, 1, 1, 3), ("x²", 3, 2, 1, 3), ("^", 3, 3, 1, 3), ("log", 3, 4, 1, 3), ("ln", 3, 5, 1, 3),
    ("(-)", 4, 0, 1, 3), ("., ,,", 4, 1, 1, 3), ("hyp", 4, 2, 1, 3), ("sin", 4, 3, 1, 3), ("cos", 4, 4, 1, 3), ("tan", 4, 5, 1, 3),
    ("RCL", 5, 0, 1, 3), ("ENG", 5, 1, 1, 3), ("(", 5, 2, 1, 3), (")", 5, 3, 1, 3), (",", 5, 4, 1, 3), ("m+", 5, 5, 1, 3),
]

for (texto, linha, coluna, span, largura) in botoes_retangulares:
    criar_botao(texto, linha, coluna, span, largura)

calc.grid_rowconfigure(6, weight=0)
teclado = tk.Frame(calc, bg=COR_FUNDO, height=300)
teclado.grid(row=6, column=0, columnspan=6, sticky="nsew", padx=5, pady=(5, 5))

for r in range(4):
    teclado.grid_rowconfigure(r, weight=1, uniform="linhas")
for c in range(5):
    teclado.grid_columnconfigure(c, weight=1, uniform="colunas")

def criar_botao_teclado(texto, r, c, rs=1, cs=1):
    cores = cor_botao(texto)
    tk.Button(teclado, text=texto, font=("Arial", 12, "bold"), width=9, height=3,
              bg=cores["bg"], fg=cores["fg"], relief="raised", bd=2,
              command=lambda t=texto: clique(t)) \
        .grid(row=r, column=c, rowspan=rs, columnspan=cs, padx=2, pady=2)

criar_botao_teclado("7", 0, 0)
criar_botao_teclado("8", 0, 1)
criar_botao_teclado("9", 0, 2)
criar_botao_teclado("DEL", 0, 3)
criar_botao_teclado("AC", 0, 4)

criar_botao_teclado("4", 1, 0)
criar_botao_teclado("5", 1, 1)
criar_botao_teclado("6", 1, 2)
criar_botao_teclado("X", 1, 3)
criar_botao_teclado("÷", 1, 4)

criar_botao_teclado("1", 2, 0)
criar_botao_teclado("2", 2, 1)
criar_botao_teclado("3", 2, 2)
criar_botao_teclado("+", 2, 3)
criar_botao_teclado("-", 2, 4)

criar_botao_teclado("0", 3, 0)
criar_botao_teclado(".", 3, 1)
criar_botao_teclado("EXP", 3, 2)
criar_botao_teclado("Ans", 3, 3)
criar_botao_teclado("=", 3, 4)

# Botão redondo Replay
tamanho_largura = 140
tamanho_altura = 160
raio_replay = 70
canvas_replay = tk.Canvas(calc, width=tamanho_largura, height=tamanho_altura, bg=COR_FUNDO, highlightthickness=0)
canvas_replay.place(x=190, y=80)
criar_botao_redondo(canvas_replay, tamanho_largura//2, tamanho_altura//2, raio_replay, "Replay", lambda: clique("Replay"))

calc.mainloop()
