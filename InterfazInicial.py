import sqlite3
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import shutil


if not os.path.exists("bbdd"):
    os.makedirs("bbdd")

var_BD = sqlite3.connect(os.path.join("bbdd", "users.db"))

var_path_BD = os.path.join("bbdd", "users.db")

dir = os.getcwd()

directori_fotos = os.path.join(dir,"profile_images")
if not os.path.exists(directori_fotos):
    os.makedirs(directori_fotos)

contador = 0

cur_BD = var_BD.cursor()

cur_BD.execute('''CREATE TABLE IF NOT EXISTS jugadors (
                  nick TEXT,
                  password TEXT,
                  avatar TEXT,
                  games INTEGER,
                  win INTEGER
                )''')

var_BD.commit()

def seleccionar_imatge(imagen):
    tipus_arxius = (
        ('Tots els arxius', '*.*'),
        ('Imatges tipus jpg', '*.jpg')
    )
    imagen = filedialog.askopenfilename(
        initialdir=directori_fotos,
        title='Selecciona una imatge',
        filetypes=tipus_arxius
    )
def seleccionar_imagen(entry_avatar):
    directori_fotos = "profile_images"

    if not os.path.exists(directori_fotos):
        os.makedirs(directori_fotos)
    
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif")])
    nombre_archivo = os.path.basename(ruta_imagen)

    ruta_destino = os.path.join(directori_fotos, nombre_archivo)

    try:
        if ruta_imagen != ruta_destino:
            shutil.copy2(ruta_imagen, ruta_destino)
    except Exception as e:
        print(f"Error al copiar la imagen: {e}")

    entry_avatar.delete(0, END)
    entry_avatar.insert(0, nombre_archivo)

def crea_usuari():
    global imatge_seleccionada
    imatge_seleccionada = None
    ventana_usuari = Toplevel()


    label_nick = Label(ventana_usuari, text="Nick:")
    label_nick.grid(row=0, column=0)
    entry_nick = Entry(ventana_usuari)
    entry_nick.grid(row=0, column=1)

    label_password = Label(ventana_usuari, text="Contrasenya:")
    label_password.grid(row=1, column=0)
    entry_password = Entry(ventana_usuari)
    entry_password.grid(row=1, column=1)

    label_avatar = Label(ventana_usuari, text="Avatar:")
    label_avatar.grid(row=2, column=0)
    entry_avatar = Entry(ventana_usuari)
    entry_avatar.grid(row=2, column=1)
    entry_avatar_button = Button(ventana_usuari, text='Seleccionar i Obrir Imatge', command=lambda:seleccionar_imagen(entry_avatar))
    entry_avatar_button.grid(row=2, column=2)

    label_games = Label(ventana_usuari, text="Partides jugades:")
    label_games.grid(row=3, column=0)
    entry_games = Entry(ventana_usuari)
    entry_games.grid(row=3, column=1)

    label_win = Label(ventana_usuari, text="Partides guanyades:")
    label_win.grid(row=4, column=0)
    entry_win = Entry(ventana_usuari)
    entry_win.grid(row=4, column=1)

    entries = [
        entry_nick,
        entry_password,
        entry_avatar,
        entry_games,
        entry_win]

    btn_afegir = Button(
        ventana_usuari, text="Afegir a la Base de Dades", command=lambda: afegir_a_bd(entries))
    btn_afegir.grid(row=7, column=0, columnspan=2)

    entry_nick.delete(0, END)
    entry_password.delete(0, END)
    entry_avatar.delete(0, END)
    entry_games.delete(0, END)
    entry_win.delete(0, END)


def afegir_a_bd(datos):
    
    var_BD = sqlite3.connect(var_path_BD)
    cur_BD = var_BD.cursor()

    nick = datos[0].get()
    password = datos[1].get()
    avatar = datos[2].get()
    games = datos[3].get()
    win = datos[4].get()

    cur_BD.execute("INSERT INTO jugadors VALUES (:z_nick, :z_password, :z_avatar, :z_games, :z_win)",
                   {'z_nick': nick, 'z_password': password, 'z_avatar': avatar, 'z_games': games, 'z_win': win})

    var_BD.commit()

    datos[0].delete(0, END)
    datos[1].delete(0, END)
    datos[2].delete(0, END)
    datos[2].delete(0, END)
    datos[3].delete(0, END)
    datos[4].delete(0, END)


def comprovar_dades():
    var_BD = sqlite3.connect(var_path_BD)
    cur_BD = var_BD.cursor()

    cur_BD.execute("SELECT * FROM jugadors")

    resultats = cur_BD.fetchall()

    for fila in resultats:
        print(fila)

    var_BD.close()


def comprovar_usuari(nick_entry, password_entry, frame: Frame, titulo_text):
    global contador

    var_BD = sqlite3.connect(var_path_BD)
    cur_BD = var_BD.cursor()

    cur_BD.execute("SELECT count(*) FROM jugadors where nick= '" +
                   nick_entry + "' and password= '" + password_entry + "' ;")

    resultats = cur_BD.fetchall()

    if resultats[0][0] == 0:
        print("ERROR: Nick o contraseña erronea!")
        contador += 1
        if (contador == 3):
            print("ALERTA: Ya lo has intentado el limite de veces permitida!")
            finestra.destroy()
    else:
        cur_BD.execute("SELECT nick, avatar FROM jugadors where nick= '" +
                   nick_entry + "' and password= '" + password_entry + "' ;")
        
        resultats = cur_BD.fetchall()
        for widget in frame.winfo_children():
            widget.destroy()
        tit_frame = Label(frame, anchor="center", text=titulo_text)
        tit_frame.grid(row=0, column=0)
        nick_frame = Label(frame, anchor="center", text=nick_entry)
        nick_frame.grid(row=1, column=0)
        ruta_destino = os.path.join(directori_fotos, resultats[0][1])
        imagen = Image.open(ruta_destino)
        imagenFinal = ImageTk.PhotoImage(imagen)
        avatar_frame = Label(frame, anchor="center", image=imagenFinal)
        avatar_frame.grid(row=2, column=0)
        avatar_frame.img = ImageTk.PhotoImage(imagen)
        avatar_frame.config(image=avatar_frame.img)
        contador = 0


    var_BD.close()



finestra = Tk()
finestra.title("Menú principal")
frame_j1 = Frame(finestra)
frame_j2 = Frame(finestra)

tit_frame1 = Label(frame_j1, anchor="center", name="jugador 1" ,text="Jugador 1:")
tit_frame1.grid(row=0, column=0)
label_nick1 = Label(frame_j1, anchor="center", text="Nick:")
label_nick1.grid(row=1, column=0)
entry_nick1 = Entry(frame_j1, justify="center")
entry_nick1.grid(row=2, column=0)

label_password1 = Label(frame_j1, anchor="center", text="Contrasenya:")
label_password1.grid(row=3, column=0)
entry_password1 = Entry(frame_j1, justify="center")
entry_password1.grid(row=4, column=0)

btn_entra_usuari1 = Button(
    frame_j1, text="Entrar", command=lambda: comprovar_usuari(entry_nick1.get(), entry_password1.get(),frame_j1, tit_frame1.cget("text")))
btn_entra_usuari1.grid(row=5, column=0, columnspan=2)

tit_frame2 = Label(frame_j2, anchor="center", name="jugador 2", text="Jugador 2:")
tit_frame2.grid(row=0, column=4)

label_nick2 = Label(frame_j2, text="Nick:")
label_nick2.grid(row=1, column=4)
entry_nick2 = Entry(frame_j2)
entry_nick2.grid(row=2, column=4)

label_password2 = Label(frame_j2, text="Contrasenya:")
label_password2.grid(row=3, column=4)
entry_password2 = Entry(frame_j2)
entry_password2.grid(row=4, column=4)

btn_entra_usuari2 = Button(
    frame_j2, text="Entrar", command=lambda: comprovar_usuari(entry_nick2.get(), entry_password2.get(),frame_j2, tit_frame2.cget("text")))
btn_entra_usuari2.grid(row=5, column=4, columnspan=2)

frame_j1.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
frame_j2.grid(row=1, column=25, columnspan=2, padx=20, pady=20)


btn_crea_usuari = Button(
    finestra, text="Crea usuari", command=crea_usuari)
btn_crea_usuari.grid(row=6, column=0, columnspan=2)

btn_comprovar = Button(
    finestra, text="Comprovar Dades", command=comprovar_dades)
btn_comprovar.grid(row=7, column=0, columnspan=2)

finestra.geometry("600x600")
finestra.mainloop()
