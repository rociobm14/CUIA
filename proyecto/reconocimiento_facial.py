import os
import cv2
import face_recognition

class ReconocimientoFacial:
    def __init__(self):
        self.encodings_referencia = []
        self.nombres_referencia = []

    def cargar_imagenes_referencia(self, directorio):
        for filename in os.listdir(directorio):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                ruta_imagen = os.path.join(directorio, filename)
                imagen = face_recognition.load_image_file(ruta_imagen)
                encodings = face_recognition.face_encodings(imagen)

                if len(encodings) > 0:
                    self.encodings_referencia.append(encodings[0])
                    self.nombres_referencia.append(os.path.splitext(filename)[0])

    def reconocer_caras(self,directorio):
        self.cargar_imagenes_referencia(directorio)
        camara = cv2.VideoCapture(0)

        while True:
            ret, imagen_capturada = camara.read()
            imagen_rgb = cv2.cvtColor(imagen_capturada, cv2.COLOR_BGR2RGB)

            ubicaciones_caras = face_recognition.face_locations(imagen_rgb)
            encodings_caras = face_recognition.face_encodings(imagen_rgb, ubicaciones_caras)

            nombres = []

            for encoding in encodings_caras:
                coincidencias = face_recognition.compare_faces(self.encodings_referencia, encoding)
                nombre = "Desconocido"

                if True in coincidencias:
                    indice = coincidencias.index(True)
                    nombre = self.nombres_referencia[indice]
                    print("Persona detectada:", nombre)
                    camara.release()
                    cv2.destroyWindow("Reconocimiento Facial")
                    return

                nombres.append(nombre)

            for (top, right, bottom, left), nombre in zip(ubicaciones_caras, nombres):
                cv2.rectangle(imagen_capturada, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(imagen_capturada, nombre, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            cv2.imshow("Reconocimiento Facial", imagen_capturada)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        camara.release()
        cv2.destroyWindow("Reconocimiento Facial")