import tkinter as tk
from registro_facial import RegistroFacial
from PIL import Image, ImageTk
import queue
import threading as thread
import speech_recognition as sr


class NuevoUsuario():
    def __init__(self):
        
        # ventana de registro de nuevo usuario
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000") # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime realm") # título de mi app
        self.threading = True
        self.voice_thread = None
        self.command_queue = queue.Queue()
        
        # Cargar la imagen de fondo
        image = Image.open("imagenes/fondo2.jpg")
        image = image.resize((1700, 800), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        
        # Crear un Label con la imagen de fondo y agregarlo a la ventana
        background_label = tk.Label(self.ventana, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Título del formulario de registro
        titulo = tk.Label(self.ventana, text="Registro de Usuario:", font=("Arial", 40, "bold"), bg="#FFB6C1", fg="#000000", border=0)
        titulo.place(relx = 0.5, rely = 0.15, anchor = tk.CENTER)
        
        # Label nombre de usuario 
        nombre_usuario_label = tk.Label(self.ventana, text="Nombre de usuario:", font=("Arial", 20, "bold"), bg="#FFB6C1", fg="#000000", border=0)
        nombre_usuario_label.place(relx = 0.5, rely = 0.25, anchor = tk.CENTER)

        self.nombre_usuario = tk.Entry(self.ventana)
        self.nombre_usuario.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER)
        
        # Label contraseña
        contraseña_label = tk.Label(self.ventana, text="Contraseña:", font=("Arial", 20, "bold"), bg="#FFB6C1", fg="#000000", border=0)
        contraseña_label.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)

        self.contraseña = tk.Entry(self.ventana, show="*") # ocultamos la contraseña
        self.contraseña.place(relx = 0.5, rely = 0.45, anchor = tk.CENTER)
        
        # estilo del botón de envío
        button_style = {"fg": "#FFB6C1", "bg": "#000000", "border": 0, "font": ("Script MT Bold", 25, "bold")}
        
        #Botón de envío
        boton_enviar = tk.Button(self.ventana, text="Registrar Usuario", command=lambda:self.registro(self.nombre_usuario, self.contraseña), **button_style)
        boton_enviar.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)
        
        self.voice_thread = thread.Thread(target=self.voice_recognition, daemon=True)
        self.voice_thread.start()
        
        self.process_queue()
        
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
                if command.startswith("registro"):
                    self.command_queue.put(lambda: self.registro_command(self.nombre_usuario, self.contraseña))
             
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
        
    def registro_command(self, nombre_usuario, contraseña):
        self.ventana.after(0, lambda: self.registro(nombre_usuario, contraseña))
    
    def registro(self, nombre_usuario, contraseña):
        nombre_usuario = nombre_usuario.get()
        print(nombre_usuario)
        
        contraseña = contraseña.get()
        print(contraseña)
        self.stop_voice_thread()
        self.ventana.destroy()
        RegistroFacial(nombre_usuario, contraseña)
        
    def stop_voice_thread(self):
        self.threading = False
        if self.voice_thread:
            self.voice_thread.join()
        
        
        
        
        
        
        
    