import cv2
import numpy as np
import os

import camara


class aruco():
    def __init__(self, image_paths):
        # Comprobamos si existe el fichero de calibración de la cámara
        if os.path.exists('camara.py'):
            import camara
        else:
            print("Es necesario realizar la calibración de la cámara")
            exit()

        # Cargamos las imágenes para los marcadores
        self.images = [cv2.imread(image_path) for image_path in image_paths]

        # Cargamos el diccionario de marcadores
        DIC = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        parametros = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(DIC, parametros)

        # Abrimos la cámara
        self.cap = cv2.VideoCapture(0)

        # Comprobamos si la cámara está abierta
        if self.cap.isOpened():
            # Obtenemos el tamaño del frame
            hframe = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            wframe = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            print("Tamaño del frame de la cámara: ", wframe, "x", hframe)

            # Obtenemos la matriz de la cámara
            self.matrix, self.roi = cv2.getOptimalNewCameraMatrix(camara.cameraMatrix, camara.distCoeffs, (wframe, hframe), 1, (wframe, hframe))
            self.roi_x, self.roi_y, self.roi_w, self.roi_h = self.roi

            # Creamos el bucle para capturar frames
            self.run()
        else:
            print("No se pudo acceder a la cámara.")

    def run(self):
        final = False
        while not final:
            # Capturamos un frame
            ret, framebgr = self.cap.read()
            if ret:
                # Aquí procesamos el frame
                framerectificado = cv2.undistort(framebgr, camara.cameraMatrix, camara.distCoeffs, None, self.matrix)
                framerecortado = framerectificado[self.roi_y:self.roi_y + self.roi_h, self.roi_x:self.roi_x + self.roi_w]

                # Buscamos los marcadores
                corners, ids, rejected = self.detector.detectMarkers(framerecortado)

                if len(corners) > 0:
                    for i in range(min(len(corners), 6)):  # Procesamos hasta 6 marcadores
                        c1 = (corners[i][0][0][0], corners[i][0][0][1])
                        c2 = (corners[i][0][1][0], corners[i][0][1][1])
                        c3 = (corners[i][0][2][0], corners[i][0][2][1])
                        c4 = (corners[i][0][3][0], corners[i][0][3][1])

                        # Dibujamos los contornos
                        tamaño = self.images[i].shape

                        # Calculamos la homografía
                        puntos_aruco = np.array([c1, c2, c3, c4], dtype=np.float32)

                        # Puntos de la imagen
                        puntos_imagen = np.array([[0, 0], [tamaño[1], 0], [tamaño[1], tamaño[0]], [0, tamaño[0]]], dtype=np.float32)

                        # Calculamos la homografía
                        h, estado = cv2.findHomography(puntos_imagen, puntos_aruco)

                        # Aplicamos la homografía
                       # Aplicamos la homografía
                        perspectiva = cv2.warpPerspective(self.images[ids[i][0] % len(self.images)], h, (self.roi_w, self.roi_h))  # Corregido

                        cv2.fillConvexPoly(framerecortado, puntos_aruco.astype(int), 0, 16)
                        framerecortado = framerecortado + perspectiva

                    cv2.imshow("Monumento", framerecortado)
                else:
                    cv2.imshow("Monumento", framebgr)

                # Esperamos 1ms y verificamos si se ha presionado la barra espaciadora o la tecla 'q'
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' ') or key == ord('q'):
                    final = True
            else:
                final = True

        # Liberamos la cámara y cerramos las ventanas
        self.cap.release()
        cv2.destroyAllWindows()


