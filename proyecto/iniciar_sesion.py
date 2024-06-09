import tkinter as tk
import json
from entorno_usuario import EntornoUsuario
from reconocimiento_facial import ReconocimientoFacial

class IniciarSesion():
    def __init__(self):
        # ventana de registro de nuevo usuario
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000") # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime realm") # título de mi app
        
        # Título del formulario de registro
        titulo = tk.Label(self.ventana, text="Inicio de sesión:", font=("Arial", 20, "bold"), bg="gray", fg="white", border=0)
        titulo.place(relx = 0.5, rely = 0.15, anchor = tk.CENTER)
        
        # Label nombre de usuario 
        nombre_usuario_label = tk.Label(self.ventana, text="Nombre de usuario:", font=("Arial", 20, "bold"), bg="gray", fg="white", border=0)
        nombre_usuario_label.place(relx = 0.5, rely = 0.25, anchor = tk.CENTER)

        self.nombre_usuario = tk.Entry(self.ventana)
        self.nombre_usuario.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER)
        
        # Label contraseña
        contraseña_label = tk.Label(self.ventana, text="Contraseña:", font=("Arial", 20, "bold"), bg="gray", fg="white", border=0)
        contraseña_label.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)

        self.contraseña = tk.Entry(self.ventana, show="*") # ocultamos la contraseña
        self.contraseña.place(relx = 0.5, rely = 0.45, anchor = tk.CENTER)
        
        # estilo del botón de envío
        button_style = {"fg": "#ffffff", "bg": "#1a2b3c", "border": 0, "font": ("Script MT Bold", 25, "bold")}
        
        #Botón de envío
        boton_enviar = tk.Button(self.ventana, text="Iniciar Sesión", command=lambda:self.comprobar_credenciales(self.nombre_usuario, self.contraseña), **button_style)
        boton_enviar.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)
        
        #Reconocimiento facial
        boton_reconocimiento_facial = tk.Button(self.ventana, text="Reconocimiento facial", command=lambda:self.reconocimiento_facial(), **button_style)
        boton_reconocimiento_facial.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)
        
    def comprobar_credenciales(self, nombre_usuario, contraseña):
        nombre_usuario = nombre_usuario.get()
        contraseña = contraseña.get()
        
        with open('data.json', 'r') as f:
            data = json.load(f)

        try:
            usuario = next(user for user in data['usuarios'] if user['nombre_usuario'] == nombre_usuario and user['contrasena'] == contraseña)
            print("Inicio de sesión correcto")
        except StopIteration:
            print("Inicio de sesión incorrecto")
        self.ventana.destroy()
        EntornoUsuario(nombre_usuario)
        
    def reconocimiento_facial(self):
        self.ventana.destroy()
        reconocimiento = ReconocimientoFacial()
        reconocimiento.reconocer_caras("carasUsuarios/")
        
         # Cargar la configuración
        #reconocimiento.cargar_configuracion("data.json")

        
        
       
        
        
    
    