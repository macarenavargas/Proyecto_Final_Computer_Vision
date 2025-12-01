class DecodificadorSecuencia:
    def __init__(self, secuencia_correcta):
        self.secuencia_correcta = secuencia_correcta  # e.g. ["circulo", "linea_horizontal", "triangulo", "cuadrado"]
        self.secuencia_actual = []

    def actualiza(self, patron_detectado):
        if patron_detectado != "ninguno":
            self.secuencia_actual.append(patron_detectado)
            # Solo guarda los últimos N
            if len(self.secuencia_actual) > len(self.secuencia_correcta):
                self.secuencia_actual.pop(0)
        return self.verifica()

    def verifica(self):
        return self.secuencia_actual == self.secuencia_correcta

    def resetea(self):
        self.secuencia_actual = []