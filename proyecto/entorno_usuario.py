import tkinter as tk

class EntornoUsuario():
    def __init__(self, n):
    
        self.ventana = tk.Tk()
        self.ventana.geometry("10000x10000") # establecemos las dimensiones principales de la pantalla
        self.ventana.title("Your Anime realm") # título de mi app
        
        self.nombre_usuario = n
        
        #prueba para mostrar que se ha metido en el usuario correctamente
        nombre_usuario_label = tk.Label(self.ventana, text=f"Usuario: {self.nombre_usuario}", font=("Arial", 20, "bold"))
        nombre_usuario_label.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)
        