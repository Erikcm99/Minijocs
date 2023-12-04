import tkinter as tk
import random
from tkinter import messagebox
import time


class Buscaminas:
    def __init__(self, root, on_cierre_juego=None):
        # Inicializa la ventana principal y los elementos del juego
        self.root = root
        self.on_cierre_juego = on_cierre_juego
        self.root.title("Buscaminas")
        self.botones = []  # Matriz que almacena los botones del tablero
        self.minas = set()  # Almacena las posiciones de las minas
        # Almacena las posiciones marcadas por el usuario como posibles minas
        self.marcadas = set()
        self.time = time.time()
        self.clicks = 0
        self.casillas_reveladas = set()  # Almacena las casillas reveladas por el usuario
        self.crear_tablero()  # Crea la interfaz gráfica del tablero
        self.colocar_minas()  # Coloca las minas en posiciones aleatorias
        root.mainloop()

    def crear_tablero(self):
        # Crea los botones del tablero y los asocia con eventos
        for i in range(8):
            row = []
            for j in range(8):
                # Crea un botón en la interfaz gráfica y asigna eventos a cada botón
                boton = tk.Button(self.root, width=3, height=1,
                                  command=lambda i=i, j=j: self.clic_boton(i, j))
                boton.bind("<Button-3>", lambda event, i=i,
                           j=j: self.marcar_mina(event, i, j))
                boton.grid(row=i, column=j)
                row.append(boton)
            self.botones.append(row)
        frameReinicio = tk.Frame(self.root)
        frameSalir = tk.Frame(self.root)
        boton1 = tk.Button(frameReinicio,  width=20, height=1,
                           text="Reiniciar", command=lambda self=self: self.reinicio())
        boton2 = tk.Button(frameSalir,  width=20, height=1,
                           text="Salir", command=lambda self=self: self.salir())
        frameReinicio.grid(row=0, column=12)
        frameSalir.grid(row=7, column=12)
        boton1.pack()
        boton2.pack()

    def salir(self):
        self.root.destroy()
        self.on_cierre_juego()

    def reinicio(self):
        self.root.destroy()
        Buscaminas(tk.Tk())

    def colocar_minas(self):
        # Coloca aleatoriamente 15 minas en el tablero
        minas_colocadas = 0
        while minas_colocadas < 15:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if (x, y) not in self.minas:
                self.minas.add((x, y))
                minas_colocadas += 1

    def clic_boton(self, x, y):
        # Acción al hacer clic en un botón del tablero
        # Primero se comprueba si la casilla tiene F(Flag)
        if self.botones[x][y]["text"] == "F":
            pass  # Ignora el clic si la casilla está marcada como posible mina
        elif (x, y) in self.minas:
            self.mostrar_mina()  # Muestra todas las minas si el usuario hace clic en una mina
        else:
            # Si no hay mina en la casilla, muestra el número de minas adyacentes o revela casillas vacías
            minas_adyacentes = self.contar_minas_adyacentes(x, y)
            if minas_adyacentes > 0:
                # Muestra el número de minas adyacentes
                self.botones[x][y].config(text=str(minas_adyacentes))
                # Añade la casilla revelada al conjunto
                self.casillas_reveladas.add((x, y))
            else:
                # Revela las casillas vacías adyacentes
                self.revelar_casillas_vacias(x, y)
        self.clicks += 1
        self.root.title("Jugador 1")
        if (len(self.casillas_reveladas) == 8*8 - 1):
            messagebox.showinfo(
                "Fin del juego", "¡Victoria! Juego terminado.\n Clicks: " + str(self.clicks) + "\nTiempo de juego: " + str(round(self.time)))
            self.root.destroy()

    def contar_minas_adyacentes(self, x, y):
        # Cuenta el número de minas adyacentes a una casilla dada
        count = 0
        for i in range(max(0, x - 1), min(8, x + 2)):
            for j in range(max(0, y - 1), min(8, y + 2)):
                if (i, j) in self.minas:
                    count += 1
        return count

    # Aquí no tenia ni idea de como hacer la busqueda de casillas vacías,
    def revelar_casillas_vacias(self, x, y):
        # Así que he preguntado al señor gpt
        # Revela las casillas vacías y sus adyacentes recursivamente
        if self.botones[x][y]["text"] == "":
            # Marca la casilla como vacía en la interfaz
            self.botones[x][y].config(text=".")
            # Añade la casilla revelada al conjunto
            self.casillas_reveladas.add((x, y))
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Revela las casillas adyacentes vacías
                    self.clicks -= 1
                    self.clic_boton(new_x, new_y)
        else:
            return  # Termina la recursión si la casilla ya está revelada o tiene minas adyacentes

    def mostrar_mina(self):
        # Muestra todas las minas al finalizar el juego y cierra la ventana
        for x in range(8):
            for y in range(8):
                if (x, y) in self.minas:
                    # Muestra la mina en la interfaz
                    self.botones[x][y].config(text="M")
                    # Añade la casilla revelada al conjunto
                    self.casillas_reveladas.add((x, y))
                else:
                    minas_adyacentes = self.contar_minas_adyacentes(x, y)
                    if minas_adyacentes > 0:
                        # Muestra el número de minas adyacentes
                        self.botones[x][y].config(text=str(minas_adyacentes))
                        # Añade la casilla revelada al conjunto
                        self.casillas_reveladas.add((x, y))
                    else:
                        # Marca la casilla como vacía en la interfaz
                        self.botones[x][y].config(text=".")
                        # Añade la casilla revelada al conjunto
                        self.casillas_reveladas.add((x, y))
        messagebox.showinfo(
            "Fin del juego", "¡Has encontrado una mina! Juego terminado.\n Clicks: " + str(self.clicks) + "\nTiempo de juego: " + str(round(time.time() - self.time))+"s")

    def marcar_mina(self, event, x, y):
        # Marca o desmarca una casilla como posible mina al hacer clic derecho
        if (x, y) in self.marcadas:
            # Desmarca la casilla si ya estaba marcada
            self.botones[x][y].config(text="")
            # Elimina la casilla del conjunto de marcadas
            self.marcadas.remove((x, y))
        else:
            # Marca la casilla como posible mina
            self.botones[x][y].config(text="F")
            # Agrega la casilla al conjunto de marcadas
            self.marcadas.add((x, y))



