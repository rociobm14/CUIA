import tkinter as tk
import json
from PIL import Image, ImageTk
import registro_facial
import pagina_inicio
import os

class ConfirmarRechazarRegistro:
    def __init__(self, n, c):
        self.nombre_usuario = n
        self.contraseña = c
        
        self.ventana = tk.Tk()
        self.ventana.geometry("800x600")  # Establecemos dimensiones más razonables para la pantalla
        self.ventana.title("Your Anime Realm")  # Título de la app
        
        # Cargamos la imagen del usuario
        ruta_imagen = "carasUsuarios/" + self.nombre_usuario + ".jpg"
        
        # Abrimos imagen
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((600, 400), Image.LANCZOS)  # Redimensionar la imagen si es necesario
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Crear un widget Label para la imagen
        label_imagen = tk.Label(self.ventana, image=imagen_tk)
        label_imagen.image = imagen_tk  # Necesario para evitar que la imagen sea recogida por el recolector de basura
        label_imagen.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        # Crear un widget Label para la confirmación
        titulo_label = tk.Label(self.ventana, text="Do you want to use this photo?", font=("Arial", 20, "bold"), bg="gray", fg="white", border=0)
        titulo_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Estilo para los botones sin bordes
        button_style = {"fg": "white", "bg": "gray", "border": 0, "font": ("Arial", 20, "bold")}

        # Crear un widget Button para aceptar la foto
        boton_aceptar = tk.Button(self.ventana, text="Yes", command=lambda:self.aceptar(self.nombre_usuario, self.contraseña), **button_style)
        boton_aceptar.place(relx = 0.3, rely = 0.9, anchor = tk.CENTER)

        # Crear un widget Button para rechazar la foto
        boton_rechazar = tk.Button(self.ventana, text="No", command=lambda:self.rechazar(self.nombre_usuario, self.contraseña), **button_style)
        boton_rechazar.place(relx = 0.7, rely = 0.9, anchor = tk.CENTER)

        self.ventana.mainloop()

    def rechazar(self, nombre, contraseña):
        # Eliminar la foto
        self.ventana.destroy()
        os.remove("carasUsuarios/" + nombre + ".jpg")
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
        contenido_json[nombre] = {}

        # Escribir el contenido actualizado en el archivo JSON
        with open('data.json', 'w') as archivo:
            json.dump(contenido_json, archivo, indent=4)

        print("Nuevo contenido agregado a 'personas' correctamente.")

        pagina_inicio.VentanaPrincipal()
        
        
        
    