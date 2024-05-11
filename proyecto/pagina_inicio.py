import tkinter as tk # para la interfaz gráfica de la aplicación
from nuevo_usuario import NuevoUsuario
from iniciar_sesion import IniciarSesion

class VentanaPrincipal():
    def __init__(self):
        
        # ventana principal de la aplicación
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000") # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime realm") # título de mi app
        
        # estilo de los botones
        button_style = {"fg": "#ffffff", "bg": "#1a2b3c", "border": 0, "font": ("Script MT Bold", 25, "bold")}

        # Botón "Sign in"
        btn_sign_in = tk.Button(self.ventana, text="Iniciar sesión", command=self.inicio_sesion, **button_style)
        btn_sign_in.place(relx=0.5, rely=0.62, anchor=tk.CENTER)

        # Botón "Sign up"
        btn_sign_up = tk.Button(self.ventana, text="Darse de alta", command=self.darse_alta, **button_style)
        btn_sign_up.place(relx=0.5, rely=0.69, anchor=tk.CENTER)

        self.ventana.mainloop()
        
    def inicio_sesion(self):
        print("El usuario quiere iniciar sesión")
        #cerramos esta ventana
        self.ventana.destroy()
        IniciarSesion()
        
    
    def darse_alta(self):
        print("el usuario quiere darse de alta")
        self.ventana.destroy() 
        NuevoUsuario()
