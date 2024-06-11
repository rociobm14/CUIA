import tkinter as tk
from tkinter import PhotoImage
from nuevo_usuario import NuevoUsuario
from iniciar_sesion import IniciarSesion
import threading as thread
import speech_recognition as sr
from PIL import Image, ImageTk

class VentanaPrincipal():
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000")
        self.ventana.title("Your Anime realm")
        self.threading = True
        self.voice_thread = None
        
        # Cargar la imagen de fondo
        image = Image.open("imagenes/fondo.jpg")
        image = image.resize((1700, 800), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        
        # Crear un Label con la imagen de fondo y agregarlo a la ventana
        background_label = tk.Label(self.ventana, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear un Label para el mensaje de bienvenida
        welcome_label = tk.Label(self.ventana, text="¡Bienvenido/a a Your Anime Realm!", font=("Comic Sans MS", 50, "bold"), bg="#FFB6C1", fg="#000000")
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        button_style = {"fg": "#000000", "bg": "#FFB6C1", "border": 0, "font": ("Comic Sans MS", 25, "bold")}
        
        btn_sign_in = tk.Button(self.ventana, text="Iniciar sesión", command=self.inicio_sesion, **button_style)
        btn_sign_in.place(relx=0.5, rely=0.62, anchor=tk.CENTER)

        btn_sign_up = tk.Button(self.ventana, text="Darse de alta", command=self.darse_alta, **button_style)
        btn_sign_up.place(relx=0.5, rely=0.69, anchor=tk.CENTER)
        
        self.voice_thread = thread.Thread(target=self.voice_recognition, daemon=True)
        self.voice_thread.start()

        self.ventana.mainloop()
    
        
        
    def voice_recognition(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        while self.threading:
            with mic as source:
                try:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Escuchando...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio, language='es-ES')
                    print(f"Comando escuchado: {command}")
                    command = command.lower()
                    if command.startswith("iniciar sesión"):
                        self.inicio_sesion_command()
                    elif command.startswith("dar de alta"):
                        self.darse_alta_command()
                except sr.UnknownValueError:
                    print("No se entendió el comando")
                except sr.RequestError as e:
                    print(f"Error con el servicio de reconocimiento de voz; {e}")
                except AssertionError:
                    print("El micrófono no está disponible.")
                    break
        
    def inicio_sesion_command(self):
        self.ventana.after(0, lambda: self.inicio_sesion())
        
    def darse_alta_command(self):
        self.ventana.after(0, lambda: self.darse_alta())
        
    def inicio_sesion(self):
        print("El usuario quiere iniciar sesión")
        self.stop_voice_thread()
        self.ventana.destroy()
        IniciarSesion()
        
    def darse_alta(self):
        print("El usuario quiere darse de alta")
        self.stop_voice_thread()
        self.ventana.destroy()
        NuevoUsuario()

    def stop_voice_thread(self):
        self.threading = False
        if self.voice_thread:
            self.voice_thread.join()


