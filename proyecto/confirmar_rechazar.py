import tkinter as tk
import json
from PIL import Image, ImageTk
import registro_facial
import pagina_inicio
import os
import queue
import threading as thread
import speech_recognition as sr

class ConfirmarRechazarRegistro:
    def __init__(self, n, c):
        self.nombre_usuario = n
        self.contraseña = c
        
        self.ventana = tk.Tk()
        self.ventana.geometry("800x600")  # Establecemos dimensiones más razonables para la pantalla
        self.ventana.title("Your Anime Realm")  # Título de la app
        self.threading = True
        self.voice_thread = None
        self.command_queue = queue.Queue()
        
        # Cargamos la imagen del usuario
        ruta_imagen = "carasUsuarios/" + self.nombre_usuario + ".jpg"
        
        # Abrimos imagen
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((600, 400), Image.LANCZOS)  # Redimensionar la imagen si es necesario
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Cargar la imagen de fondo
        image = Image.open("imagenes/fondo.jpg")
        image = image.resize((10000, 10000), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        
        # Crear un Label con la imagen de fondo y agregarlo a la ventana
        background_label = tk.Label(self.ventana, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear un widget Label para la imagen
        label_imagen = tk.Label(self.ventana, image=imagen_tk)
        label_imagen.image = imagen_tk  # Necesario para evitar que la imagen sea recogida por el recolector de basura
        label_imagen.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        # Crear un widget Label para la confirmación
        titulo_label = tk.Label(self.ventana, text="¿Quieres usar esta foto?", font=("Arial", 20, "bold"), bg="#FFB6C1", fg="white", border=0)
        titulo_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Estilo para los botones sin bordes
        button_style = {"fg": "white", "bg": "#FFB6C1", "border": 0, "font": ("Arial", 20, "bold")}

        # Crear un widget Button para aceptar la foto
        boton_aceptar = tk.Button(self.ventana, text="Usar foto", command=lambda:self.aceptar(self.nombre_usuario, self.contraseña), **button_style)
        boton_aceptar.place(relx = 0.3, rely = 0.9, anchor = tk.CENTER)

        # Crear un widget Button para rechazar la foto
        boton_rechazar = tk.Button(self.ventana, text="No usar foto", command=lambda:self.rechazar(self.nombre_usuario, self.contraseña), **button_style)
        boton_rechazar.place(relx = 0.7, rely = 0.9, anchor = tk.CENTER)

        self.voice_thread = thread.Thread(target=self.voice_recognition, daemon=True)
        self.voice_thread.start()
        
        self.process_queue()
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
                command = command.lower()
                if command.startswith("usar foto"):
                    self.command_queue.put(lambda: self.aceptar_command(self.nombre_usuario, self.contraseña))
                    
                elif command.startswith("no usar foto"):
                    self.command_queue.put(lambda: self.rechazar_command(self.nombre_usuario, self.contraseña))
             
            except sr.UnknownValueError:
                print("No se entendió el comando")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento de voz; {e}")
                
    def process_queue(self):
        try:
            while True:
                command = self.command_queue.get_nowait()
                command()
        except queue.Empty:
            pass
        self.ventana.after(100, self.process_queue)

    def aceptar_command(self, nombre, contraseña):
        self.ventana.after(0, lambda: self.aceptar(nombre, contraseña))
        
    def rechazar_command(self, nombre, contraseña):
        self.ventana.after(0, lambda: self.rechazar(nombre, contraseña))
        
    def rechazar(self, nombre, contraseña):
        # Eliminar la foto
        self.stop_voice_thread()
        self.ventana.destroy()
        os.remove("carasUsuarios/" + nombre + ".jpg")
        registro_facial.RegistroFacial(nombre, contraseña)
    
    def aceptar(self, nombre, contraseña):
        # Cerrar la ventana
        self.stop_voice_thread()
        self.ventana.destroy()

        # Leer el archivo JSON existente
        with open('data.json') as archivo:
            contenido_json = json.load(archivo)

        # Agregar nuevo contenido a la lista "personas"
        nuevo_contenido = {
            "nombre_usuario": nombre,
            "contrasena": contraseña
        }

        contenido_json["usuarios"].append(nuevo_contenido)
        contenido_json[nombre] = {}

        # Escribir el contenido actualizado en el archivo JSON
        with open('data.json', 'w') as archivo:
            json.dump(contenido_json, archivo, indent=4)

        print("Nuevo contenido agregado a 'personas' correctamente.")

        pagina_inicio.VentanaPrincipal()
        
    def stop_voice_thread(self):
        self.threading = False
        if self.voice_thread:
            self.voice_thread.join()
        
        
        
    