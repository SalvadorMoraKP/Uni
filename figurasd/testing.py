import tkinter as tk
from clasesfiguras import *


def calcular_figura(figura):
    resultado.set(
        f"{figura.dibujar()}\n"
        f"Volumen: {figura.calcular_volumen():.2f}\n"
        f"Área: {figura.calcular_area_superficial():.2f}"
    )


def calcular():
    try:
        figura = opcion.get()

        if figura == "Cubo":
            lado = float(entry1.get())
            obj = Cubo(lado)

        elif figura == "Esfera":
            radio = float(entry1.get())
            obj = Esfera(radio)

        elif figura == "Cilindro":
            radio = float(entry1.get())
            altura = float(entry2.get())
            obj = Cilindro(radio, altura)

        calcular_figura(obj)

    except ValueError:
        resultado.set("Ingresa valores numéricos válidos")

#labellssss
def actualizar_campos(*args):
    figura = opcion.get()

    if figura == "Cubo":
        label1.config(text="Lado:")
        label2.config(text="")
        entry2.pack_forget()

    elif figura == "Esfera":
        label1.config(text="Radio:")
        label2.config(text="")
        entry2.pack_forget()

    elif figura == "Cilindro":
        label1.config(text="Radio:")
        label2.config(text="Altura:")
        label2.pack()
        entry2.pack()

# --- INTERFAZ ---
root = tk.Tk()

opcion = tk.StringVar(value="Cubo")
opcion.trace("w", actualizar_campos)

menu = tk.OptionMenu(root, opcion, "Cubo", "Esfera", "Cilindro")
menu.pack()

label1 = tk.Label(root, text="Lado:")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="")
entry2 = tk.Entry(root)

btn = tk.Button(root, text="Calcular", command=calcular)
btn.pack()

resultado = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado)
label_resultado.pack()

root.mainloop()