import cv2
from confirmar_rechazar import ConfirmarRechazarRegistro
import camara as cam

class RegistroFacial:
    def __init__(self, n, c):
        self.nombre_usuario = n
        self.contraseña = c
        self.capturar_rostro()

    def capturar_rostro(self):
        captura = cv2.VideoCapture(0)  # 0 para la cámara predeterminada

        if captura.isOpened():
            # Obtenemos el tamaño del frame
            hframe = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
            wframe = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
            print("Tamaño del frame de la cámara: ", wframe, "x", hframe)

            # Obtenemos la matriz de la cámara
            self.matrix, self.roi = cv2.getOptimalNewCameraMatrix(cam.cameraMatrix, cam.distCoeffs, (wframe, hframe), 1, (wframe, hframe))
            self.roi_x, self.roi_y, self.roi_w, self.roi_h = self.roi


            name_window = "Camara"
            cv2.namedWindow(name_window)

            while True:
                ret, imagen = captura.read()

                if ret:
                    # Rectificamos la imagen de la cámara
                    imagen_rectificada = cv2.undistort(imagen, cam.cameraMatrix, cam.distCoeffs, None, self.matrix)
                    imagen_recortada = imagen_rectificada[self.roi_y:self.roi_y + self.roi_h, self.roi_x:self.roi_x + self.roi_w]

                    cv2.imshow('Camara', imagen_recortada)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('c'):  # Presionar 'c' para capturar
                        nombre_imagen = "carasUsuarios/" + self.nombre_usuario + ".jpg"
                        cv2.imwrite(nombre_imagen, imagen_recortada)
                        print("¡Foto guardada correctamente!")
                        cv2.destroyWindow(name_window)
                        ConfirmarRechazarRegistro(self.nombre_usuario, self.contraseña)
                        break
                    elif key == ord('q'):  # Presionar 'q' para salir
                        print("Captura cancelada.")
                        break
                else:
                    break

            captura.release()
            cv2.destroyAllWindows()
        else:
            print("No se pudo acceder a la cámara.")
            cv2.destroyAllWindows()
