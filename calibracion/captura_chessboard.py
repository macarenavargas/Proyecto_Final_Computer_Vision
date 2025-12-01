import cv2
import numpy as np

# Parámetros del tablero
CHESSBOARD_SIZE = (9,6)  # número de esquinas internas (ajusta según tu patrón)

cap = cv2.VideoCapture(0)
imagenes = []
print("Pulsa la tecla ESPACIO para capturar una imagen del patrón, 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

    cv2.imshow('Captura patrón', frame)
    if found:
        cv2.drawChessboardCorners(frame, CHESSBOARD_SIZE,    corners, found)
        cv2.imshow('Detectado', frame)

    key = cv2.waitKey(1)
    if key == ord(' '):
        if found:
            imagenes.append(gray)
            print("Imagen capturada.")
        else:
            print("No se detectó el patrón.")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Guarda imágenes en disco
for i, im in enumerate(imagenes):
    cv2.imwrite(f'calibracion/img_chess_{i:02d}.png', im)
print(f"{len(imagenes)} imágenes capturadas.")