from datetime import datetime

class BicicletaTaller:
    def __init__(self, serial, costo_por_hora):
        self._serial = serial
        self._hora_ingreso = None
        self._hora_salida = None
        self._costo_por_hora = costo_por_hora

    def registrar_ingreso(self, hora):
        try:
            self._hora_ingreso = datetime.strptime(hora, "%H:%M")
        except:
            print("Formato de hora inválido (usa HH:MM)")

    def registrar_salida(self, hora):
        try:
            self._hora_salida = datetime.strptime(hora, "%H:%M")
        except:
            print("Formato de hora inválido (usa HH:MM)")

    def calcular_total(self, hora_salida):
        try:
            hora_salida = datetime.strptime(hora_salida, "%H:%M")

            if self._hora_ingreso is None:
                print("No se ha registrado la hora de ingreso")
                return 0

            diferencia = hora_salida - self._hora_ingreso
            horas = diferencia.total_seconds() / 3600

            if horas < 0:
                print("La hora de salida no puede ser menor a la de ingreso")
                return 0

            total = horas * self._costo_por_hora
            return total

        except:
            print("Error en el cálculo")
            return 0

    def obtener_serial(self):
        return self._serial
