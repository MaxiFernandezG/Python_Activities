#################### Importo bibliotecas #######################

from ast import Str
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from typing import ItemsView
import mysql.connector
import re
import sys, os


# -----codigo para carga de imagenes-----

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, "imagenes")
ruta_icono = STATIC_ROOT + "\\alumno.ico"
ruta_img_ventana = STATIC_ROOT + "\\alumnopng.png"


# ----- Conexion, Salir y limpiarcampos-----

conectabase = mysql.connector.connect(host="localhost", user="root", passwd="")
puntero = conectabase.cursor()
puntero.execute("CREATE DATABASE if not exists utn2")
puntero.execute(
    "CREATE TABLE if not exists utn2.alumnos(identif INT(7) NOT NULL AUTO_INCREMENT, nombre VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, apellido VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, direccion VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, PRIMARY KEY (identif))"
)


def miconexion():
    conectabase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="utn2"
    )
    return conectabase


def Salir():
    valor = messagebox.askquestion("SALIR", "Deseas salir de la aplicación?")
    if valor == "yes":
        conectabase.close()
        ven_ppal.destroy()


def limpiacampos():
    ape.set("")
    dir.set("")
    nom.set("")


############### Funciones de actualizacion de BBDD ###############################


def altalumno():
    limpiacampos()
    deshabilita()
    bot_alta.config(state=NORMAL)
    campoape.config(state=NORMAL)
    camponom.config(state=NORMAL)
    campodir.config(state=NORMAL)


def alta2():
    cadena = ape.get()  # obtenemos la cadena del campo de texto
    patron = "[A-Za-z]"
    if re.match(patron, cadena) and cadena != "":
        conectabase = miconexion()
        puntero = conectabase.cursor()
        sql = "INSERT INTO alumnos(nombre, apellido, direccion) VALUES (%s, %s, %s)"
        datos = (nom.get().title(), ape.get().upper(), dir.get().title())
        puntero.execute(sql, datos)
        conectabase.commit()
        conectabase.close()
        messagebox.showinfo(
            "Alta",
            "El alumno "
            + nom.get().title()
            + " "
            + ape.get().upper()
            + " fue dado de alta",
        )
        limpiacampos()
        deshabilita()
    else:
        messagebox.showwarning("Error", "Debe ingresar datos en el campo apellido")
        limpiacampos()
    mostrar()


def mostrar():
    conectabase = miconexion()
    puntero = conectabase.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        puntero.execute("SELECT * FROM alumnos")
        for fila in puntero:
            tree.insert("", END, text=fila[0], values=(fila[1], fila[2], fila[3]))
    except:
        pass


def bajalumno():
    conectabase = miconexion()
    puntero = conectabase.cursor()
    try:
        valor = messagebox.askquestion(
            "BAJA", "Realmente desea dar de baja este alumno?"
        )
        if valor == "yes":
            dato = (id.get(),)
            sql = "DELETE FROM alumnos WHERE identif=%s"
            puntero.execute(sql, dato)
            conectabase.commit()
            conectabase.close()
            messagebox.showinfo(
                "Baja",
                "El alumno "
                + nom.get().title()
                + " "
                + ape.get().upper()
                + " fue dado de baja",
            )

    except:
        messagebox.showwarning(
            "AVISO", "Ocurrió un error al intentar dar de baja el alumno"
        )
        pass
    deshabilita()
    deshabilitalta()
    deshabilita2()
    limpiacampos()
    mostrar()


def deshabilita():
    bot_baja.config(state=DISABLED)
    bot_modif.config(state=DISABLED)


def deshabilitalta():
    bot_alta.config(state=DISABLED)


def deshabilita2():
    campoape.config(state=DISABLED)
    camponom.config(state=DISABLED)
    campodir.config(state=DISABLED)


def seleccion(event):
    campoape.config(state=NORMAL)
    camponom.config(state=NORMAL)
    campodir.config(state=NORMAL)
    bot_baja.config(state=NORMAL)
    bot_modif.config(state=NORMAL)
    bot_alta.config(state=DISABLED)
    item = tree.identify("item", event.x, event.y)
    id.set(tree.item(item, "text"))
    nom.set(tree.item(item, "values")[0])
    ape.set(tree.item(item, "values")[1])
    dir.set(tree.item(item, "values")[2])


def modifalumno():
    cadena1 = ape.get()  # obtenemos la cadena del campo de texto
    patron = "[A-Za-z]"

    try:
        if re.match(patron, cadena1) and cadena1 != "":
            conectabase = miconexion()
            puntero = conectabase.cursor()
            valor = messagebox.askquestion(
                "MODIFICACIÓN", "Realmente desea modificar los datos del alumno?"
            )
            if valor == "yes":
                sql = "UPDATE alumnos SET nombre=%s, apellido=%s, direccion=%s WHERE identif=%s"
                datos = (
                    nom.get().title(),
                    ape.get().upper(),
                    dir.get().title(),
                    id.get(),
                )
                puntero.execute(sql, datos)
                conectabase.commit()
                conectabase.close()
        else:
            messagebox.showwarning("Error", "Debe ingresar datos en el campo apellido ")
    except:
        messagebox.showwarning("AVISO", "Ocurrió un error al actualizar el alumno")
        pass
    deshabilita()
    limpiacampos()
    mostrar()


# -----ventana raiz-----

ven_ppal = Tk()
ven_ppal.iconbitmap(ruta_icono)
ven_ppal.title("Sistema de alumnos")
ven_ppal.config(bg="#9EE8D6")
ven_ppal.geometry("1200x600")

mi_imagen = PhotoImage(file=ruta_img_ventana)

lab_titulo = Label(ven_ppal, text="Alumnos", fg="#285D51")
lab_titulo.config(font=("comic sans", 40), bg="#9EE8D6")
lab_titulo.pack()
lab_alumno = Label(ven_ppal, image=mi_imagen, height="150", width="150")
lab_alumno.pack()

# -----definicion de barra de menu-----

barramenu = Menu(ven_ppal, font=12)
ven_ppal.config(menu=barramenu, height="500", width="1000")
abmcmenu = Menu(barramenu, tearoff=0)
abmcmenu.add_command(label="Habilitar alta", command=altalumno)
abmcmenu.add_command(label="Mostrar todos los registros", command=mostrar)
barramenu.add_cascade(label="Datos", menu=abmcmenu, font=10)
barramenu.add_cascade(label="Limpiar campos", command=limpiacampos)
barramenu.add_cascade(label="Salir", command=Salir)

# -----campos de datos------

opcicombo = StringVar()
framedatos = Frame(ven_ppal)
framedatos.pack(fill="x")
framechico = Frame(framedatos)
framechico.config(width=800, height=350)
framechico.pack(anchor=CENTER)
framebut = Frame(ven_ppal)
framebut.pack(side="top", anchor=CENTER)
framebut.config(bg="#9EE8D6", width=780, height=350)  #
id, nom, ape, dir = StringVar(), StringVar(), StringVar(), StringVar()
campoid = Entry(framechico, textvariable=id)
campoape = Entry(framechico, width="40", font=13)
campoape.grid(row=1, column=2, padx="50", pady="25")
campoape.config(textvariable=ape, state=DISABLED)
camponom = Entry(framechico, width="40", font=13)
camponom.grid(row=2, column=2, padx="50", pady="25")
camponom.config(textvariable=nom, state=DISABLED)

# comboal.grid(row=2, column=3, padx="50", pady=25)
# campodni = Entry(framechico, width="50", font=13)
# campodni.grid(row=4, column=2, padx="50", pady="25")
campodir = Entry(framechico, width="40", font=13)
campodir.grid(row=3, column=2, padx="50", pady="25")
campodir.config(textvariable=dir, state=DISABLED)
labcaja = Label(framechico, text="Muestra todos los registros cargados", font=13)
labcaja.place(x=680, y=0)
labape = Label(framechico, text="Apellido", font=13)
labape.grid(row=1, column=1, sticky="w")
labnom = Label(framechico, text="Nombre", font=13)
labnom.grid(row=2, column=1, sticky="w")  # padx="70", pady="25"
labdir = Label(framechico, text="Dirección", font=13)
labdir.grid(row=3, column=1, sticky="w")
# labtel = Label(framechico, text="Teléfono", font=13)
# labtel.grid(row=5, column=1, sticky="w")
# tel = IntVar()

# modulo de consulta para baja y modificación
tree = ttk.Treeview(framechico, height=10)
tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=20, minwidth=50, anchor=W)
tree.column("col1", width=120, minwidth=50)
tree.column("col2", width=120, minwidth=50)
tree.column("col3", width=270, minwidth=70)
tree.heading("#0", text="ID", anchor=CENTER)
tree.heading("#1", text="Nombre", anchor=CENTER)
tree.heading("#2", text="Apellido", anchor=CENTER)
tree.heading("#3", text="Dirección", anchor=CENTER)
tree.grid(row=1, column=3, padx="10", pady=25, rowspan=10)
tree.bind("<ButtonRelease-1>", seleccion)
item = StringVar()
# Barra de desplazamiento para el Treeview
barra = Scrollbar(framechico, orient="vertical", command=tree.yview)
barra.grid(row=1, rowspan=10, column=4, sticky="ns")
tree.configure(yscrollcommand=barra.set)
# tree.grid(row=2, rowspan=6, column=3)

# -----modulo de botones-----

bot_alta = Button(framebut, text="AGREGAR", command=alta2)
bot_alta.config(font=("comic sans", 18), bg="#9EE8D6", state=DISABLED)
bot_alta.place(x=60, y=20)
bot_baja = Button(framebut, text="BAJA", command=bajalumno)
bot_baja.config(font=("comic sans", 18), bg="#9EE8D6", state=DISABLED)
bot_baja.place(x=225, y=20)
# bot_consul = Button(framebut, text="CONSULTA", command=mostrar)
# bot_consul.config(font=("comic sans", 18), bg="#9EE8D6")
# bot_consul.place(x=280, y=20)
bot_modif = Button(framebut, text="MODIFICACIÓN", command=modifalumno)
bot_modif.config(font=("comic sans", 18), bg="#9EE8D6", state=DISABLED)
bot_modif.place(x=330, y=20)
bot_salir = Button(framebut, text="SALIR")
bot_salir.config(font=("comic sans", 18), bg="#285D51", fg="#9EE8D6", command=Salir)
bot_salir.place(x=550, y=20)

ven_ppal.mainloop()
