import cv2

def main():
    cap = cv2.VideoCapture(0)  # 0 es la cámara por defecto

    if not cap.isOpened():
        print("¡No se pudo abrir la cámara!")
        return

    print("Cámara conectada correctamente. Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo recibir el frame (fin de stream?). Saliendo...")
            break

        cv2.imshow('Vista de la Cámara - Prueba', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()