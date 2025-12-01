import cv2
import numpy as np

def detectar_patron(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    # Para círculos
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=60, param2=30, minRadius=20, maxRadius=150)
    if circles is not None:
        return "circulo"

    # Para líneas (ejemplo muy básico)
    edges = cv2.Canny(blur, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 120)
    if lines is not None:
        # Podrías analizar theta para diferenciar horizontal/vertical
        theta = lines[0][0][1]
        if np.abs(theta - np.pi/2) < 0.2:  # vertical
            return "linea_vertical"
        else:
            return "linea_horizontal"

    # Para triángulos/cuadrados
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            return "triangulo"
        elif len(approx) == 4:
            return "cuadrado"
    return "ninguno"