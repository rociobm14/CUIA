import cv2
from confirmar_rechazar import ConfirmarRechazarRegistro

class RegistroFacial:
    def __init__(self, n, c):
        self.nombre_usuario = n
        self.contraseña = c
        
        self.capturar_rostro()
        
    def capturar_rostro(self):
         # Crear un objeto de captura de video
        captura = cv2.VideoCapture(0)  # 0 para la cámara predeterminada

        # Configurar la fuente, tipo de letra y tamaño para el contador
        fuente = cv2.FONT_HERSHEY_SIMPLEX
        posicion_contador = (400, 50)
        tamaño_fuente = 1
        color_contador = (0, 255, 0)

        # Dar nombre a la ventana
        name_window = "Camara"
        cv2.namedWindow(name_window)

        # Inicializar el contador
        contador = 10

        while True:
            # Leer la imagen de la cámara
            ret, imagen = captura.read()

            # Mostrar el contador en la imagen
            if (contador > 0):
                cv2.putText(imagen, str(contador), posicion_contador, fuente, tamaño_fuente, color_contador, 2)

            # Mostrar la imagen
            cv2.imshow('Camara', imagen)

            # Esperar 1 segundo y restar 1 al contador
            if cv2.waitKey(1000) == ord('q') or contador == 0:
                break
            contador -= 1

        # Verificar si se alcanzó el contador cero
        if contador == 0:
            # Guardar la imagen en un archivo
            nombre_imagen = "carasUsuarios/" + self.nombre_usuario + ".jpg"
            cv2.imwrite(nombre_imagen, imagen)
            print("¡Foto guardada correctamente!")
            cv2.destroyWindow(name_window)
            ConfirmarRechazarRegistro(self.nombre_usuario, self.contraseña)

        else:
            print("Captura cancelada.")

        # Liberar la cámara y cerrar la ventana
        captura.release()
        cv2.destroyAllWindows()
        
        