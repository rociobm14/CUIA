import tkinter as tk
from PIL import Image, ImageTk
import json

class AnimesFavoritos():
    def __init__(self, n, entorno):
        self.entorno_principal = entorno
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x1000")  # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime Realm")  # título de mi app
        
        self.nombre_usuario = n
        self.imagenes_animes = []  # Lista para mantener referencias a las imágenes
        self.threading = True

        # Prueba para mostrar que se ha metido en el usuario correctamente
        nombre_usuario_label = tk.Label(self.ventana, text=f"Animes favoritos de : {self.nombre_usuario}", font=("Arial", 20, "bold"))
        nombre_usuario_label.pack(side=tk.TOP, pady=10)
        
        # Crear el frame del menú a la izquierda
        menu_frame = tk.Frame(self.ventana, width=300, bg='grey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Crear los botones del menú
        
        boton_pagina_principal = tk.Button(menu_frame, text="Coleccion de animes", command=lambda:self.animes_favoritos())
        boton_pagina_principal.pack(pady=10)
        
        boton_personajes_favoritos = tk.Button(menu_frame, text="Personajes favoritos", bg="blue")
        boton_personajes_favoritos.pack(pady=10)

        boton_series_favoritas = tk.Button(menu_frame, text="Series favoritas")
        boton_series_favoritas.pack(pady=10)

        boton_series_vistas = tk.Button(menu_frame, text="Series vistas")
        boton_series_vistas.pack(pady=10)

        # Crear un frame principal que contendrá el canvas y el scrollbar
        main_frame = tk.Frame(self.ventana)
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear el canvas
        canvas = tk.Canvas(main_frame, bg='white')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un scrollbar vertical
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el canvas para usar el scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Crear un frame interno dentro del canvas
        animes_frame = tk.Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=animes_frame, anchor='nw')
        
        # Leer datos de animes desde el archivo JSON
        with open('data.json', 'r') as f:
            data = json.load(f)
            
        for i, anime in enumerate(data[self.nombre_usuario]['animes_favoritos']):
            # Cargar y redimensionar la imagen del anime
            imagen_anime = Image.open(anime['imagen'])
            imagen_anime = imagen_anime.resize((300, 400), Image.LANCZOS)
            imagen_anime = ImageTk.PhotoImage(imagen_anime)
            self.imagenes_animes.append(imagen_anime)  # Mantener referencia a la imagen

            # Crear un frame para cada anime
            anime_frame = tk.Frame(animes_frame, bg='white')
            anime_frame.grid(row=i//5, column=i%5, padx=10, pady=10, sticky="nsew")

            # Crear un label para la imagen
            label_imagen = tk.Label(anime_frame, image=imagen_anime)
            label_imagen.pack(padx=10, pady=10)

            # Crear un label para el nombre del anime
            label_nombre = tk.Label(anime_frame, text=anime['nombre'], font=("Arial", 16))
            label_nombre.pack()

        self.ventana.mainloop()
        
    def pagina_principal(self):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        self.entorno_principal
      
        