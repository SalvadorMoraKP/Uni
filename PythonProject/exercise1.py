import tkinter as tk
from tkinter import messagebox
from clase import BicicletaTaller
#Salvador Garavito Mora
#Programacion UNAD



bicicletas = []

# User y contraseña para la entrada.
usuario_correcto = "admin"
contrasena_correcta = "1234"

# Se valida el login, osea el user y password
def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if usuario == usuario_correcto and contrasena == contrasena_correcta:
        messagebox.showinfo("Login", "Welcome!")
        ventana_login.destroy()
        ventanaPrograma()


    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos, intente nuevamente")


#el programa principal, aquí se trabaja despues del login successful
def ventanaPrograma():
        def agregar_bicicleta():
            serial = entry_serial.get()
            hora = entry_hora.get()
            valor = float(entry_valor.get())

            bici = BicicletaTaller(serial, valor)
            bici.registrar_ingreso(hora)

            bicicletas.append(bici)
            entry_serial.delete(0, tk.END)
            entry_hora.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
            messagebox.showinfo(title="Success", message="Bicicleta registrado correctamente!")

        def calcular_costo():
            serial_buscar = entry_buscar.get()
            hora_salida = entry_salida.get()

            for bici in bicicletas:
                if bici.obtener_serial() == serial_buscar:
                    bici.registrar_salida(hora_salida)
                    total = bici.calcular_total(hora_salida)

                    messagebox.showinfo("Total", f"El valor total a pagar es de: ${total}")
                    return

            messagebox.showinfo(title="Error", message="Bicicleta no encontrada!")


        ventana_programa = tk.Tk()
        ventana_programa.title("Bikes maintenance")
        ventana_programa.geometry("400x400")
        ventana_programa.configure(bg="lightblue")

        tk.Label(ventana_programa, text="Serial:",  bg="lightblue").grid(row=0, column=0, sticky="w")
        tk.Label(ventana_programa, text="Hora llegada (HH:MM):",  bg="lightblue").grid(row=1, column=0, sticky="w")
        tk.Label(ventana_programa, text="Valor por hora:",  bg="lightblue").grid(row=2, column=0, sticky="w")

        entry_serial = tk.Entry(ventana_programa)
        entry_serial.grid(row=0, column=1)

        entry_hora = tk.Entry(ventana_programa)
        entry_hora.grid(row=1, column=1)

        entry_valor = tk.Entry(ventana_programa)
        entry_valor.grid(row=2, column=1)

        tk.Button(ventana_programa, text="Agregar", command=agregar_bicicleta).grid(row=3, column=0, columnspan=2)

        # Buscar + salida
        tk.Label(ventana_programa, text="Buscar por serial:",  bg="lightblue").grid(row=4, column=0, sticky="w")
        entry_buscar = tk.Entry(ventana_programa)
        entry_buscar.grid(row=4, column=1)

        tk.Label(ventana_programa, text="Hora salida (HH:MM):",  bg="lightblue").grid(row=5, column=0, sticky="w")
        entry_salida = tk.Entry(ventana_programa)
        entry_salida.grid(row=5, column=1)

        tk.Button(ventana_programa, text="cobrar", command=calcular_costo).grid(row=6, column=0, columnspan=2)

        ventana_programa.mainloop()








# Ventana del login
ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("300x200")
ventana_login.config(bg="lightblue")

# labels
label_usuario = tk.Label(ventana_login, text="User", bg="lightblue")
label_usuario.pack(pady=5)

entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack(pady=5)

label_contrasena = tk.Label(ventana_login, text="Password", bg="lightblue")
label_contrasena.pack(pady=5)

entry_contrasena = tk.Entry(ventana_login, show="*")
entry_contrasena.pack(pady=5)

# Botón de login
boton_login = tk.Button(ventana_login, text="Login", command=verificar_login)
boton_login.pack(pady=15)

label_credenciales = tk.Label(ventana_login, text="User/pass: admin/1234", bg="lightblue")
label_credenciales.pack(pady=5)







# Ejecutar ventana
ventana_login.mainloop()