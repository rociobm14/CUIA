import tkinter as tk
from PIL import Image, ImageTk
import json
import threading as thread
import speech_recognition as sr
from aruco import aruco

class EntornoUsuario():
    def __init__(self, n):
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x1000")  # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime Realm")  # título de mi app
        
        self.nombre_usuario = n
        self.imagenes_animes = []  # Lista para mantener referencias a las imágenes
        self.threading = True

        # Prueba para mostrar que se ha metido en el usuario correctamente
        nombre_usuario_label = tk.Label(self.ventana, text=f"Bienvenido/a : {self.nombre_usuario}", font=("Arial", 20, "bold"))
        nombre_usuario_label.pack(side=tk.TOP, pady=10)
        
        # Crear el frame del menú a la izquierda
        menu_frame = tk.Frame(self.ventana, width=300, bg='grey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Crear los botones del menú
        
        boton_pagina_principal = tk.Button(menu_frame, text="Coleccion de animes", bg="blue")
        boton_pagina_principal.pack(pady=10)
        
        boton_personajes_favoritos = tk.Button(menu_frame, text="Personajes favoritos" , command=lambda:self.personajes_favoritos(self.nombre_usuario))
        boton_personajes_favoritos.pack(pady=10)

        boton_series_favoritas = tk.Button(menu_frame, text="Animes favoritos", command=lambda:self.animes_favoritos(self.nombre_usuario))
        boton_series_favoritas.pack(pady=10)

        boton_series_vistas = tk.Button(menu_frame, text="Animes vistos", command=lambda:self.animes_vistos(self.nombre_usuario))
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
        with open('anime.json', 'r') as f:
            data = json.load(f)
            
        for i, anime in enumerate(data['animes']):
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

            # Crear un botón para ver más información
            boton_info = tk.Button(anime_frame, text="Ver información", command=lambda anime=anime: self.ver_informacion(anime))
            boton_info.pack(pady=10)
            
        #thread.Thread(target=self.voice_recognition, daemon=True).start()
            
        self.ventana.mainloop()
         
    def ver_informacion(self, anime):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        InformacionAnime(self.nombre_usuario, anime)
        
    #nos aseguramos de que el hilo que maneje es el hilo principal, ya que por comando de voz se crea un nuevo hilo
    #y la interfaz tkinter no está preparada para manejarse con muchos hilos  
    def animes_favoritos_command(self, nombre_usuario):
        self.ventana.after(0, lambda: self.animes_favoritos(nombre_usuario))
        
    def animes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesFavoritos(nombre_usuario)
        
    def personajes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        PersonajesFavoritos(nombre_usuario)
        
    def animes_vistos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesVistos(nombre_usuario)
          
    def voice_recognition(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        while self.threading:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Escuchando...")
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language='es-ES')
                print(f"Comando escuchado: {command}")
                words = command.lower().split()
                if words[0] == "favoritos":
                    anime_name = " ".join(words[1:])
                    self.add_to_favorites(anime_name)
                    
                elif words[0] == "vistos":
                    anime_name = " ".join(words[1:])
                    self.add_to_watched(anime_name)
                    
                #Scrollear en las distintas
                elif command.lower() == "animes favoritos":
                    self.animes_favoritos_command(self.nombre_usuario)
                    break
            except sr.UnknownValueError:
                print("No se entendió el comando")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento de voz; {e}")
                
    def add_to_favorites(self, anime_name):
        anime = self.find_anime(anime_name)
        print("el anime es", anime)

        try:
            with open('data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}

        if 'animes_favoritos' not in user_data[self.nombre_usuario]:
            user_data[self.nombre_usuario]['animes_favoritos'] = []

        if anime in user_data[self.nombre_usuario]['animes_favoritos']:
            raise ValueError(f"El anime {anime_name} ya está en tus favoritos")
        else:
            if anime is not None:
                
                print("entra aqui")
                user_data[self.nombre_usuario]['animes_favoritos'].append(anime)

                with open('data.json', 'w') as archivo:
                    json.dump(user_data, archivo, indent=4)

                print("Nuevo contenido agregado a 'animes_favoritos' correctamente.")

                self.show_confirmation_favourites(anime_name)
                
                
    def add_to_watched(self, anime_name):
        anime = self.find_anime(anime_name)
        print("el anime es", anime)

        try:
            with open('data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}

        if 'animes_vistos' not in user_data[self.nombre_usuario]:
            user_data[self.nombre_usuario]['animes_vistos'] = []

        if anime in user_data[self.nombre_usuario]['animes_vistos']:
            raise ValueError(f"El anime {anime_name} ya está en tus vistos")
        else:
            if anime is not None:
                
                print("entra aqui")
                user_data[self.nombre_usuario]['animes_vistos'].append(anime)

                with open('data.json', 'w') as archivo:
                    json.dump(user_data, archivo, indent=4)

                print("Nuevo contenido agregado a 'animes_vistos' correctamente.")

                self.show_confirmation_watched(anime_name)
                
    
                
    def find_anime(self, anime_name):
        with open('anime.json', 'r') as f:
            animes = json.load(f)
        for anime in animes['animes']:
            if anime['nombre'].lower() == anime_name.lower():
                return anime
        return None
    

    def show_confirmation_favourites(self, anime_name):
        confirmation_window = tk.Toplevel(self.ventana)
        confirmation_window.title("Confirmación")
        confirmation_label = tk.Label(confirmation_window, text=f"{anime_name} ha sido añadido a tus favoritos", font=("Arial", 16))
        confirmation_label.pack(pady=20)
        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack(pady=10)
        
    def show_confirmation_watched(self, anime_name):
        confirmation_window = tk.Toplevel(self.ventana)
        confirmation_window.title("Confirmación")
        confirmation_label = tk.Label(confirmation_window, text=f"{anime_name} ha sido añadido a tus vistos", font=("Arial", 16))
        confirmation_label.pack(pady=20)
        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack(pady=10)
        

class InformacionAnime():
    def __init__(self, nombre_usuario, anime):
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x1000")  # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime Realm")  # título de mi app
        
        self.nombre_usuario = nombre_usuario
        self.anime = anime
        self.imagen = []
        self.threading = True
        
        # Prueba para mostrar que se ha metido en el usuario correctamente
        nombre_usuario_label = tk.Label(self.ventana, text=f"Información de {self.anime['nombre']}", font=("Arial", 20, "bold"))
        nombre_usuario_label.pack(side=tk.TOP, pady=10)
        
        # Crear el frame del menú a la izquierda
        menu_frame = tk.Frame(self.ventana, width=300, bg='grey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Crear los botones del menú
        
        boton_pagina_principal = tk.Button(menu_frame, text="Coleccion de animes", command=lambda:self.pagina_principal(self.nombre_usuario))
        boton_pagina_principal.pack(pady=10)
        
        boton_personajes_favoritos = tk.Button(menu_frame, text="Personajes favoritos" , command=lambda:self.personajes_favoritos(self.nombre_usuario))
        boton_personajes_favoritos.pack(pady=10)

        boton_series_favoritas = tk.Button(menu_frame, text="Animes Favoritos", command=lambda:self.animes_favoritos(self.nombre_usuario))
        boton_series_favoritas.pack(pady=10)

        boton_series_vistas = tk.Button(menu_frame, text="Series vistas" , command=lambda:self.animes_vistos(self.nombre_usuario))
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
        
        
        #imprimir la informacion del anime, buscando antes el anime en el archivo json
        with open('anime.json', 'r') as f:
            data = json.load(f)
        
        for i, anime in enumerate(data['animes']):
            if anime['nombre'] == self.anime['nombre']:
                # Cargar y redimensionar la imagen del anime
                imagen_anime = Image.open(anime['imagen'])
                imagen_anime = imagen_anime.resize((500, 600), Image.LANCZOS)
                imagen_anime = ImageTk.PhotoImage(imagen_anime)
                self.imagen.append(imagen_anime)  # Mantener referencia a la imagen
                
                # Crear un frame para el anime
                anime_frame = tk.Frame(animes_frame, bg='white')
                anime_frame.pack(padx=10, pady=10, fill='x', expand=True)

                # Crear un frame para la imagen y la descripción
                image_desc_frame = tk.Frame(anime_frame, bg='white')
                image_desc_frame.pack(side="top", fill="both", padx=10, pady=10)

                # Crear un label para la imagen
                label_imagen = tk.Label(image_desc_frame, image=imagen_anime)
                label_imagen.pack(side="left", padx=10, pady=10)

                # Crear un label para la descripción del anime
                label_descripcion = tk.Label(image_desc_frame, text=anime['descripcion'], font=("Arial", 16), wraplength=500, justify="left")
                label_descripcion.pack(side="right", padx=10, pady=10)

                # Crear un frame para los personajes del anime
                personajes_frame = tk.Frame(anime_frame, bg='white')
                personajes_frame.pack(side="bottom", fill="both", padx=10, pady=10)

                # Título para la sección de personajes principales
                label_personajes = tk.Label(personajes_frame, text="Personajes principales", font=("Arial", 16, "bold"))
                label_personajes.pack(pady=10)

                # Cargar y mostrar las imágenes y nombres de los personajes
                for j, personaje in enumerate(anime['personajes']):
                    # Crear un frame para cada personaje
                    personaje_frame = tk.Frame(personajes_frame, bg='white')
                    personaje_frame.pack(side="left", padx=10, pady=10)

                    imagen_personaje = Image.open(personaje['imagen'])
                    imagen_personaje = imagen_personaje.resize((150, 150), Image.LANCZOS)
                    imagen_personaje = ImageTk.PhotoImage(imagen_personaje)
                    self.imagen.append(imagen_personaje)  # Mantener referencia a la imagen

                    # Crear un label para la imagen del personaje
                    label_imagen_personaje = tk.Label(personaje_frame, image=imagen_personaje)
                    label_imagen_personaje.pack()

                    # Crear un label para el nombre del personaje
                    label_nombre_personaje = tk.Label(personaje_frame, text=personaje['nombre'], font=("Arial", 12))
                    label_nombre_personaje.pack()
                    
        #thread.Thread(target=self.voice_recognition, daemon=True).start()
                    
        self.ventana.mainloop()
        
    def voice_recognition(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        while self.threading:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Escuchando...")
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language='es-ES')
                print(f"Comando escuchado: {command}")
                words = command.lower().split()
                if words[0] == "favorito":
                    character = " ".join(words[1:])
                    self.add_to_favorites(character)
                    
            except sr.UnknownValueError:
                print("No se entendió el comando")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento de voz; {e}")
                
    def pagina_principal(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        EntornoUsuario(nombre_usuario)
                
    def animes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesFavoritos(nombre_usuario)
        
    def personajes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        PersonajesFavoritos(nombre_usuario)
        
    def animes_vistos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesVistos(nombre_usuario)
                
    def find_character(self, character_name):
        with open('anime.json', 'r') as f:
            animes = json.load(f)
        for anime in animes['animes']:
            for character in anime['personajes']:
                if character['key'].lower() == character_name.lower():
                    return character
        return None
    
    def add_to_favorites(self, character_name):
        
        character = self.find_character(character_name)
        print("el personaje es", character)

        try:
            with open('data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}

        if 'personajes_favoritos' not in user_data[self.nombre_usuario]:
            user_data[self.nombre_usuario]['personajes_favoritos'] = []

        if character in user_data[self.nombre_usuario]['personajes_favoritos']:
            raise ValueError(f"El personaje {character} ya está en tus favoritos")
        else:
            if character is not None:
                
                print("entra aqui")
                user_data[self.nombre_usuario]['personajes_favoritos'].append(character)

                with open('data.json', 'w') as archivo:
                    json.dump(user_data, archivo, indent=4)

                print("Nuevo contenido agregado a 'personajes_favoritos' correctamente.")

                self.show_confirmation_favourites(character_name)
        
    def show_confirmation_favourites(self, character_name):
        confirmation_window = tk.Toplevel(self.ventana)
        confirmation_window.title("Confirmación")
        confirmation_label = tk.Label(confirmation_window, text=f"{character_name} ha sido añadido a tus personajes favoritos", font=("Arial", 16))
        confirmation_label.pack(pady=20)
        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack(pady=10)
                    
    
                        
        
#Ventana con los animes favoritos
class AnimesFavoritos():
    def __init__(self, n):
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
        
        boton_pagina_principal = tk.Button(menu_frame, text="Coleccion de animes", command=lambda:self.pagina_principal(self.nombre_usuario))
        boton_pagina_principal.pack(pady=10)
        
        boton_personajes_favoritos = tk.Button(menu_frame, text="Personajes favoritos" , command=lambda:self.personajes_favoritos(self.nombre_usuario))
        boton_personajes_favoritos.pack(pady=10)

        boton_series_favoritas = tk.Button(menu_frame, text="Animes favoritos", bg="blue")
        boton_series_favoritas.pack(pady=10)

        boton_series_vistas = tk.Button(menu_frame, text="Animes vistos" , command=lambda:self.animes_vistos(self.nombre_usuario))
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
            
        #thread.Thread(target=self.voice_recognition, daemon=True).start()

        self.ventana.mainloop()
        
    def voice_recognition(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        while self.threading:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Escuchando...")
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language='es-ES')
                print(f"Comando escuchado: {command}")
                words = command.lower().split()
                if words[0] == "eliminar":
                    anime = " ".join(words[1:])
                    self.delete(anime)
                    
            except sr.UnknownValueError:
                print("No se entendió el comando")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento de voz; {e}")
                
    def delete(self, anime_name):
        try:
            with open('data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            print("No se encontró el archivo data.json")
            return

        animes_favoritos = user_data[self.nombre_usuario]['animes_favoritos']
        for anime in animes_favoritos:
            if anime['nombre'].lower() == anime_name.lower():
                animes_favoritos.remove(anime)
                print(f"Anime {anime_name} eliminado de tus favoritos.")
                self.show_confirmation_delete(anime_name)
                break
            
        else:
            print(f"No se encontró el anime {anime_name} en tus favoritos.")

        with open('data.json', 'w') as archivo:
            json.dump(user_data, archivo, indent=4)
            
            
    def show_confirmation_delete(self, anime_name):
        confirmation_window = tk.Toplevel(self.ventana)
        confirmation_window.title("Confirmación")
        confirmation_label = tk.Label(confirmation_window, text=f"{anime_name} ha sido eliminado de tus animes favoritos", font=("Arial", 16))
        confirmation_label.pack(pady=20)
        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack(pady=10)
    
        
    def pagina_principal(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        EntornoUsuario(nombre_usuario)
                
    def personajes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        PersonajesFavoritos(nombre_usuario)
        
    def animes_vistos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesVistos(nombre_usuario)
              
        
class PersonajesFavoritos():
    def __init__(self, n):
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x1000")  # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime Realm")  # título de mi app
        
        self.nombre_usuario = n
        self.imagenes_animes = []  # Lista para mantener referencias a las imágenes
        self.threading = True

        # Prueba para mostrar que se ha metido en el usuario correctamente
        nombre_usuario_label = tk.Label(self.ventana, text=f"Personajes favoritos de : {self.nombre_usuario}", font=("Arial", 20, "bold"))
        nombre_usuario_label.pack(side=tk.TOP, pady=10)
        
        # Crear el frame del menú a la izquierda
        menu_frame = tk.Frame(self.ventana, width=300, bg='grey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Crear los botones del menú
        
        boton_pagina_principal = tk.Button(menu_frame, text="Coleccion de animes", command=lambda:self.pagina_principal(self.nombre_usuario))
        boton_pagina_principal.pack(pady=10)
        
        boton_personajes_favoritos = tk.Button(menu_frame, text="Personajes favoritos", bg="blue")
        boton_personajes_favoritos.pack(pady=10)

        boton_series_favoritas = tk.Button(menu_frame, text="Animes favoritos" , command=lambda:self.animes_favoritos(self.nombre_usuario))
        boton_series_favoritas.pack(pady=10)

        boton_series_vistas = tk.Button(menu_frame, text="Animes vistos" , command=lambda:self.animes_vistos(self.nombre_usuario))
        boton_series_vistas.pack(pady=10)
        
        boton_realidad_aumentada = tk.Button(menu_frame, text="Realidad aumentada", command=self.realidad_aumentada)
        boton_realidad_aumentada.pack(pady=10)

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
            
        for i, anime in enumerate(data[self.nombre_usuario]['personajes_favoritos']):
            # Cargar y redimensionar la imagen del anime
            imagen_anime = Image.open(anime['imagen'])
            imagen_anime = imagen_anime.resize((300, 300), Image.LANCZOS)
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
            
        #thread.Thread(target=self.voice_recognition, daemon=True).start()

        self.ventana.mainloop()
        
    def realidad_aumentada(self):
        self.threading = False
        print("Finalizando hilo")
        #saco las rutas de las imagenes de mis personajes favoritos
        images_path = []
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        for personaje in data[self.nombre_usuario]['personajes_favoritos']:
            images_path.append(personaje['imagen'])
            
        aruco(images_path)
        
    def voice_recognition(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        while self.threading:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Escuchando...")
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language='es-ES')
                print(f"Comando escuchado: {command}")
                words = command.lower().split()
                if words[0] == "eliminar":
                    character = " ".join(words[1:])
                    self.delete(character)
                    
            except sr.UnknownValueError:
                print("No se entendió el comando")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento de voz; {e}")
                
    def delete(self, character_name):
        try:
            with open('data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            print("No se encontró el archivo data.json")
            return

        personajes_favoritos = user_data[self.nombre_usuario]['personajes_favoritos']
        for personaje in personajes_favoritos:
            if personaje['nombre'].lower() == character_name.lower():
                personajes_favoritos.remove(personaje)
                print(f"Anime {character_name} eliminado de tus favoritos.")
                self.show_confirmation_delete(character_name)
                break
        else:
            print(f"No se encontró el personaje {character_name} en tus favoritos.")

        with open('data.json', 'w') as archivo:
            json.dump(user_data, archivo, indent=4)
            
    def show_confirmation_delete(self, character_name):
        confirmation_window = tk.Toplevel(self.ventana)
        confirmation_window.title("Confirmación")
        confirmation_label = tk.Label(confirmation_window, text=f"{character_name} ha sido eliminado de tus personajes favoritos", font=("Arial", 16))
        confirmation_label.pack(pady=20)
        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack(pady=10)
        
    def pagina_principal(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        EntornoUsuario(nombre_usuario)
                
    def animes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesFavoritos(nombre_usuario)
        
    def animes_vistos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesVistos(nombre_usuario)
        

class AnimesVistos():
    def __init__(self, n):
        self.ventana = tk.Tk()
        self.ventana.geometry("1000x1000")  # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime Realm")  # título de mi app
        
        self.nombre_usuario = n
        self.imagenes_animes = []  # Lista para mantener referencias a las imágenes
        self.threading = True

        # Prueba para mostrar que se ha metido en el usuario correctamente
        nombre_usuario_label = tk.Label(self.ventana, text=f"Animes vistos de : {self.nombre_usuario}", font=("Arial", 20, "bold"))
        nombre_usuario_label.pack(side=tk.TOP, pady=10)
        
        # Crear el frame del menú a la izquierda
        menu_frame = tk.Frame(self.ventana, width=300, bg='grey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Crear los botones del menú
        
        boton_pagina_principal = tk.Button(menu_frame, text="Coleccion de animes", command=lambda:self.pagina_principal(self.nombre_usuario))
        boton_pagina_principal.pack(pady=10)
        
        boton_personajes_favoritos = tk.Button(menu_frame, text="Personajes favoritos", command=lambda:self.personajes_favoritos(self.nombre_usuario))
        boton_personajes_favoritos.pack(pady=10)

        boton_series_favoritas = tk.Button(menu_frame, text="Animes favoritos" , command=lambda:self.animes_favoritos(self.nombre_usuario))
        boton_series_favoritas.pack(pady=10)

        boton_series_vistas = tk.Button(menu_frame, text="Animes vistos", bg="blue")
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
            
        for i, anime in enumerate(data[self.nombre_usuario]['animes_vistos']):
            # Cargar y redimensionar la imagen del anime
            imagen_anime = Image.open(anime['imagen'])
            imagen_anime = imagen_anime.resize((300, 300), Image.LANCZOS)
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
        
    def pagina_principal(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        EntornoUsuario(nombre_usuario)
                
    def animes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        AnimesFavoritos(nombre_usuario)
        
    def personajes_favoritos(self, nombre_usuario):
        self.threading = False
        print("Finalizando hilo")
        self.ventana.destroy()
        PersonajesFavoritos(nombre_usuario)

    
        
        

        
    


