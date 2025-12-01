import cv2
import numpy as np
import time
def detectar_pua_roja(frame):

    # convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # definir rangos para rojo en HSV
    # necesitamos hacer dos mascaras porque en hsv el rojo esta de 0 - 10º y de 170-180º
    lower_red1 = (0, 140, 50)
    upper_red1 = (10, 255, 255)
    lower_red2 = (165, 140, 50)
    upper_red2 = (180, 255, 255)

    # crear máscaras
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # combinamos ambas mascaras para tener la mascara completa
    mask = cv2.bitwise_or(mask1, mask2)


    # quitar ruido, los puntitos pequeños
    mask = cv2.medianBlur(mask, 7)
    # cambiar a opening, ver diferencia
    
    return mask


def obtener_centro_pua(mask):

    # detecta el controno de la pua, devuelve una lista donde cada elemento es un conjunto deputnos que son partes de cada objeto rojo detectado
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        # cv2.contourArea() te calcula el area que encierra cada contorno
        # con max hacemos que nos devuelva el contorno del elemento rojo con mayor area
        c = max(contours, key=cv2.contourArea)
        
        # calcular el circulo mas pequeño que contenga el conjunto de puntos
        (x, y), radius = cv2.minEnclosingCircle(c)

        centro = (int(x), int(y))
        radio = int(radius)

        return centro, radio
    

    return None, None



def dibujar_pua(frame, centro, radio):
    if centro and radio:  # Solo si hay detección
        cv2.circle(frame, centro, radio, (0,0,255), 2)  # Rojo brillante




def definir_zonas(frame_shape, n_cuerdas=6):
    # segun el tamaño que coordenadas y tiene las zonas
    alto = frame_shape[0]
    zonas = []
    for i in range(n_cuerdas):
        y1 = int(i * alto / n_cuerdas)
        y2 = int((i+1) * alto / n_cuerdas)

        # para cada zona limite superior e inferior
        zonas.append((y1, y2))
    return zonas

def zona_actual(centro, zonas):
    # dado el centro de la pua en que zona esta
    y = centro[1]

    for i, (y1, y2) in enumerate(zonas):
        if y1 <= y < y2:
            return i
    return None



            

            
      


# ------ LOGICA DE EJECUCIÓN ----------





if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    n_zonas = 7
    zonas = None
    patron = [(2,4),(5,4),(3,4),(6,4)]
    paso = 0
    seguridad_superada = False
    tiempo_inicio = None
    dentro_objetivo = False
    sonidos = []
    for i in range(n_zonas): 
        sonidos.append('s') # aqui iria el arhivo de sonido
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if zonas is None:
            zonas = definir_zonas(frame.shape, n_zonas)
        
        mask = detectar_pua_roja(frame)
        centro, radio = obtener_centro_pua(mask)
        dibujar_pua(frame, centro, radio)

        if centro:
            zona_actual_val = zona_actual(centro, zonas)
            
            # LÓGICA DE SEGURIDAD
            if not seguridad_superada:
                zona_objetivo, tiempo_objetivo = patron[paso]
                ahora = time.time()

                if zona_actual_val == zona_objetivo:
                    if not dentro_objetivo:
                        # primer frame que entra en zona objetivo
                        tiempo_inicio = ahora
                        dentro_objetivo = True
                        print(f"Entraste en la zona {zona_objetivo}")
                    # ¿Lleva suficiente tiempo?
                    elif ahora - tiempo_inicio >= tiempo_objetivo:
                        paso += 1
                        dentro_objetivo = False
                        tiempo_inicio = None
                        print(f"Superado paso {paso} (zona {zona_objetivo})")
                        if paso == len(patron):
                            seguridad_superada = True
                            print("¡Acceso permitido!")
                else:
                    # sale de zona objetivo antes de tiempo: reset ese paso pero NO todo el patrón
                    if dentro_objetivo:
                        print("Saliste de la zona demasiado pronto, reiniciando paso actual")
                        tiempo_inicio = None
                        dentro_objetivo = False

            else:
                # Lógica de guitarra virtual aquí
                print(f"Púa en la zona {zona_actual_val}")
                if zona_guitarra_prev is not None and zona_actual_val is not None and zona_actual_val != zona_guitarra_prev:
                    print(f"¡Cruzaste de zona {zona_guitarra_prev} a {zona_actual_val}, suena nota {zona_actual_val}!")
                    # sonidos[zona_actual_val].play() que suene el sondio
                zona_guitarra_prev = zona_actual_val
                
            

        for y1, y2 in zonas:
            cv2.line(frame, (0, y1), (frame.shape[1], y1), (255,255,255), 1)
            cv2.line(frame, (0, y2), (frame.shape[1], y2), (255,255,255), 1)
        cv2.imshow("Guitarra Virtual", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()