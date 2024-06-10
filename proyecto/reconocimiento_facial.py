import os
import cv2
import face_recognition
import json
import camara as cam

class ReconocimientoFacial:
    # Constructor
    def __init__(self):
        self.encodings_referencia = []
        self.nombres_referencia = []
        self.persona_detectada = None

    # Método para cargar las imágenes de referencia
    def cargar_imagenes_referencia(self, ruta_directorio):
        # Recorremos el directorio
        for nombre_archivo in os.listdir(ruta_directorio):
            # Comprobamos que sea una imagen
            if nombre_archivo.endswith(".jpg") or nombre_archivo.endswith(".png"):
                # Cargamos la imagen
                nombre_persona = os.path.splitext(nombre_archivo)[0]
                ruta_imagen = os.path.join(ruta_directorio, nombre_archivo)

                # Cargamos la imagen de referencia
                imagen_referencia = face_recognition.load_image_file(ruta_imagen)
                encodings_referencia = face_recognition.face_encodings(imagen_referencia)

                # Verificamos si se encontraron encodings
                if len(encodings_referencia) > 0:
                    # Añadimos el encoding y el nombre a la lista
                    self.encodings_referencia.append(encodings_referencia[0])
                    self.nombres_referencia.append(nombre_persona)
                else:
                    print(f"Advertencia: No se encontraron rostros en la imagen {nombre_archivo}")

    # Método para cargar la configuración
    def cargar_configuracion(self, ruta_configuracion):
        # Cargamos el archivo JSON
        with open(ruta_configuracion) as archivo:
            datos = json.load(archivo)
            personas = datos["usuarios"]

            # Recorremos la lista de personas
            for persona in personas:
                # Obtenemos el nombre de la imagen y el idioma
                nombre_imagen = persona["nombre_usuario"]

    # Método para reconocer caras
    def reconocer_caras(self):
        camara = cv2.VideoCapture(0)

        # Creamos la ventana
        cv2.namedWindow("Reconocimiento Facial")

        # Creamos el bucle para capturar frames
        while True:
            ret, imagen_capturada = camara.read()
            imagen_rgb = cv2.cvtColor(imagen_capturada, cv2.COLOR_BGR2RGB)

            # Buscamos las caras en la imagen
            ubicaciones_caras = face_recognition.face_locations(imagen_rgb)
            encodings_caras = face_recognition.face_encodings(imagen_rgb, ubicaciones_caras)

            nombres = []

            # Recorremos los encodings de las caras
            for encoding in encodings_caras:
                coincidencias = face_recognition.compare_faces(self.encodings_referencia, encoding)
                nombre = "Desconocido"

                # Comprobamos si hay alguna coincidencia
                if True in coincidencias:
                    indice = coincidencias.index(True)
                    nombre = self.nombres_referencia[indice]
                    self.persona_detectada = nombre
                    print("Persona detectada:", nombre)
                    camara.release()
                    cv2.destroyWindow("Reconocimiento Facial")
                    return nombre

                nombres.append(nombre)

            # Dibujamos los recuadros
            for (top, right, bottom, left), nombre in zip(ubicaciones_caras, nombres):
                cv2.rectangle(imagen_capturada, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(imagen_capturada, nombre, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            cv2.imshow("Reconocimiento Facial", imagen_capturada)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        camara.release()
        cv2.destroyWindow("Reconocimiento Facial")
        return None

# Ejemplo de uso:
# reconocimiento = ReconocimientoFacial()
# reconocimiento.cargar_imagenes_referencia("carasUsuarios/")
# reconocimiento.reconocer_caras()
