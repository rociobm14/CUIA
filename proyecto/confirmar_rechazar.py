import tkinter as tk
import json
from PIL import Image
import registro_facial
import pagina_inicio
import os

class ConfirmarRechazarRegistro:
    def __init__(self, n, c):
        self.nombre_usuario = n
        self.contraseña = c
        
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000") # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime realm") # título de mi app
        
        #cargamos la imagen del usuario
        ruta_imagen = "carasUsuarios/" + self.nombre_usuario + ".jpg"
        
        # abrimos imagen
        Image.open(ruta_imagen)
        
        
         # Crear un widget Label para la confirmación
        titulo_label = tk.Label(self.ventana, text="Do you wan to use this photo?", font=("Arial", 20, "bold"), bg="gray", fg="white", border=0)
        titulo_label.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

        # Estilo para los botones sin bordes
        button_style = {"fg": "white", "bg": "gray", "border": 0, "font": ("Arial", 20, "bold")}

        # Crear un widget Button para aceptar la foto
        boton_aceptar = tk.Button(self.ventana, text="Yes", command=lambda:self.aceptar(self.nombre_usuario, self.contraseña), **button_style)
        boton_aceptar.place(relx = 0.3, rely = 0.75, anchor = tk.CENTER)

        # Crear un widget Button para rechazar la foto
        boton_rechazar = tk.Button(self.ventana, text="No", command=lambda:self.rechazar(self.nombre_usuario, self.contraseña), **button_style)
        boton_rechazar.place(relx = 0.7, rely = 0.75, anchor = tk.CENTER)

        self.ventana.mainloop()

    def rechazar(self, nombre, contraseña):
        # Eliminar la foto
        self.ventana.destroy()
        os.remove("faces/" + nombre + ".jpg")
        registro_facial.RegistroFacial(nombre, contraseña)
    
    def aceptar(self, nombre, contraseña):
        # Cerrar la ventana
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

        # Escribir el contenido actualizado en el archivo JSON
        with open('data.json', 'w') as archivo:
            json.dump(contenido_json, archivo, indent=4)

        print("Nuevo contenido agregado a 'personas' correctamente.")

        pagina_inicio.VentanaPrincipal()
        
        
        
    