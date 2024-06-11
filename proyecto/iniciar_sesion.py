import tkinter as tk
import json
from entorno_usuario import EntornoUsuario
from reconocimiento_facial import ReconocimientoFacial
import threading as thread
import speech_recognition as sr
import queue
from PIL import Image, ImageTk

class IniciarSesion():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000")
        self.ventana.title("Your Anime realm")
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

        titulo = tk.Label(self.ventana, text="Inicio de sesión:", font=("Arial", 40, "bold"), bg="#FFB6C1", fg="#000000", border=0)
        titulo.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        nombre_usuario_label = tk.Label(self.ventana, text="Nombre de usuario:", font=("Arial", 20, "bold"), bg="#FFB6C1", fg="#000000", border=0)
        nombre_usuario_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        self.nombre_usuario = tk.Entry(self.ventana)
        self.nombre_usuario.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        contraseña_label = tk.Label(self.ventana, text="Contraseña:", font=("Arial", 20, "bold"), bg="#FFB6C1", fg="#000000", border=0)
        contraseña_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.contraseña = tk.Entry(self.ventana, show="*")
        self.contraseña.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        button_style = {"fg": "#000000", "bg": "#FFB6C1", "border": 0, "font": ("Script MT Bold", 25, "bold")}

        boton_enviar = tk.Button(self.ventana, text="Iniciar Sesión", command=lambda: self.comprobar_credenciales(self.nombre_usuario, self.contraseña), **button_style)
        boton_enviar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        boton_reconocimiento_facial = tk.Button(self.ventana, text="Reconocimiento facial", command=lambda: self.reconocimiento_facial(), **button_style)
        boton_reconocimiento_facial.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
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
                if command.startswith("iniciar sesión"):
                    self.command_queue.put(lambda: self.inicio_sesion_command(self.nombre_usuario, self.contraseña))
                elif command.startswith("reconocimiento facial"):
                    self.command_queue.put(self.reconocimiento_facial_command)
             
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
        
    def inicio_sesion_command(self, nombre_usuario, contraseña):
        self.ventana.after(0, lambda: self.comprobar_credenciales(nombre_usuario, contraseña))
        
    def reconocimiento_facial_command(self):
        self.ventana.after(0, self.reconocimiento_facial)
        
    def comprobar_credenciales(self, nombre_usuario, contraseña):
        nombre_usuario = nombre_usuario.get()
        contraseña = contraseña.get()
        
        with open('data.json', 'r') as f:
            data = json.load(f)

        try:
            usuario = next(user for user in data['usuarios'] if user['nombre_usuario'] == nombre_usuario and user['contrasena'] == contraseña)
            print("Inicio de sesión correcto")
            self.ventana.destroy()
            EntornoUsuario(nombre_usuario)
        except StopIteration:
            print("Inicio de sesión incorrecto")
        
    def reconocimiento_facial(self):
        self.stop_voice_thread()
        reconocimiento = ReconocimientoFacial()
        reconocimiento.cargar_imagenes_referencia("carasUsuarios/")
    
        reconocimiento.cargar_configuracion("data.json")
        
        nombre = reconocimiento.reconocer_caras()
        
        if nombre is not None:
            self.ventana.destroy()
            EntornoUsuario(nombre)
        else:
            print("No se ha detectado al usuario, introduce manualmente las credenciales")
            
    def stop_voice_thread(self):
        self.threading = False
        if self.voice_thread:
            self.voice_thread.join()


