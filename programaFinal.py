import random
import string




class LongitudInvalidaError(Exception):

    def __init__(self, longitud):
        super().__init__(
            f"Longitud inválida: {longitud}. "
            "La longitud mínima permitida es 8 caracteres."
        )

class EntradaNoNumericaError(Exception):
    def __init__(self, valor):
        super().__init__(
            f"Entrada no numérica: '{valor}'. "
            "Debes ingresar un número entero."
        )

class ContrasenaInvalidaError(Exception):
    def __init__(self, razones: list):
        detalle = "\n   • ".join(razones)
        super().__init__(
            f"Contraseña inválida por las siguientes razones:\n   • {detalle}"
        )



#  CLASE CONTRASEÑA

class Contrasena:

    ESPECIALES = list("¿¡?=)(/¨*+-%&$#!")

    def __init__(self, longitud: int):
        self.longitud = longitud
        self.valor: str = ""

    def generar(self) -> str:

        universo = (
            list(string.ascii_uppercase) +
            list(string.ascii_lowercase) +
            list(string.digits) +
            self.ESPECIALES
        )


        universo = list(dict.fromkeys(universo))


        obligatorios = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(self.ESPECIALES),
        ]


        restantes = [c for c in universo if c not in obligatorios]
        extra_cantidad = self.longitud - len(obligatorios)

        if extra_cantidad < 0:
            extra_cantidad = 0

        extras = random.sample(restantes, min(extra_cantidad, len(restantes)))

        todos = obligatorios + extras
        random.shuffle(todos)

        self.valor = "".join(todos[: self.longitud])
        return self.valor

    def validar(self) -> bool:

        razones = []

        if len(self.valor) < 8:
            razones.append(f"Longitud {len(self.valor)} < 8")

        if not any(c.isupper() for c in self.valor):
            razones.append("No contiene letra mayúscula")

        if not any(c.islower() for c in self.valor):
            razones.append("No contiene letra minúscula")

        if not any(c.isdigit() for c in self.valor):
            razones.append("No contiene un número")

        if not any(c in self.ESPECIALES for c in self.valor):
            razones.append(f"No contiene carácter especial de: {''.join(self.ESPECIALES)}")

        if len(self.valor) != len(set(self.valor)):
            duplicados = {c for c in self.valor if self.valor.count(c) > 1}
            razones.append(f"Tiene caracteres repetidos: {duplicados}")

        if razones:
            raise ContrasenaInvalidaError(razones)

        return True



#  CLASE COFRE


class Cofre:

    TIPOS = {
        "Común":      {"puntos": +10, "emoji": "📦", "color": "gris"},
        "Raro":       {"puntos": +25, "emoji": "💠", "color": "azul"},
        "Legendario": {"puntos": +50, "emoji": "🏆", "color": "dorado"},
        "Maldito":    {"puntos": -20, "emoji": "💀", "color": "negro"},
    }

    # Probabilidades para cofres positivos (Común 60%, Raro 30%, Legendario 10%)
    _POSITIVOS = ["Común"] * 6 + ["Raro"] * 3 + ["Legendario"] * 1

    def __init__(self, tipo: str = None):
        if tipo:
            self.tipo = tipo
        else:
            self.tipo = random.choice(self._POSITIVOS)

        info = self.TIPOS[self.tipo]
        self.puntos: int = info["puntos"]
        self.emoji: str = info["emoji"]

    def __str__(self) -> str:
        signo = "+" if self.puntos >= 0 else ""
        return (
            f"{self.emoji} Cofre {self.tipo:10s} "
            f"→ {signo}{self.puntos} puntos"
        )


#  CLASE JUEGO CAZADOR

class JuegoCazador:

    BANNER = """

          CAZADOR DE CONTRASEÑAS                    
  Genera contraseñas válidas, abre cofres y acumula puntos!   

"""
    SEPARADOR = "─" * 62

    def __init__(self):
        self.puntos_totales: int = 0
        self.ronda: int = 0
        self.historial: list[dict] = []

    # ── helpers de UI ──────────────────────────────────────────

    def _imprimir_banner(self):
        print(self.BANNER)

    def _solicitar_longitud(self) -> int:

        raw = input(" Ingresa la longitud de la contraseña (mínimo 8): ").strip()

        # Validar que sea numérico
        if not raw.lstrip("-").isdigit():
            raise EntradaNoNumericaError(raw)

        longitud = int(raw)

        # Validar longitud mínima
        if longitud < 8:
            raise LongitudInvalidaError(longitud)

        return longitud

    def _mostrar_resultado(self, contrasena: Contrasena, cofre: Cofre):
        signo = "+" if cofre.puntos >= 0 else ""
        print(f"\n  Contraseña generada : {contrasena.valor}")
        print(f"  Longitud            : {len(contrasena.valor)}")
        print(f"  {cofre}")
        print(f" Puntos esta ronda   : {signo}{cofre.puntos}")
        print(f" Puntos acumulados   : {self.puntos_totales}")

    def _mostrar_historial(self):
        """Muestra el resumen de todas las rondas jugadas."""
        print(f"\n{self.SEPARADOR}")
        print("HISTORIAL DE RONDAS")
        print(self.SEPARADOR)
        for r in self.historial:
            estado = "V" if r["valida"] else "X"
            print(
                f"  Ronda {r['ronda']:2d} {estado}  "
                f"Contraseña: {r['contrasena']:>{r['longitud']}}  "
                f"Cofre: {r['cofre']:<10}  "
                f"Puntos: {r['puntos_ronda']:+3d}  "
                f"Total: {r['puntos_acum']:4d}"
            )

    # ── lógica principal de una ronda ──────────────────────────

    def jugar_ronda(self):
        self.ronda += 1
        print(f"\n{self.SEPARADOR}")
        print(f" RONDA {self.ronda}")
        print(self.SEPARADOR)

        # ── Paso 1: obtener longitud ───────────────────────────
        try:
            longitud = self._solicitar_longitud()
        except EntradaNoNumericaError as e:
            print(f"\n  {e}")
            print("¡Entrada inválida! Se abre el Cofre Maldito automáticamente.")
            cofre = Cofre("Maldito")
            self.puntos_totales += cofre.puntos
            self.historial.append({
                "ronda": self.ronda, "valida": False,
                "contrasena": "N/A", "longitud": 3,
                "cofre": cofre.tipo,
                "puntos_ronda": cofre.puntos,
                "puntos_acum": self.puntos_totales,
            })
            print(f"  {cofre}")
            print(f"Puntos acumulados: {self.puntos_totales}")
            return
        except LongitudInvalidaError as e:
            print(f"\n  {e}")
            print(" ¡Longitud inválida! Se abre el Cofre Maldito automáticamente.")
            cofre = Cofre("Maldito")
            self.puntos_totales += cofre.puntos
            self.historial.append({
                "ronda": self.ronda, "valida": False,
                "contrasena": "N/A", "longitud": 3,
                "cofre": cofre.tipo,
                "puntos_ronda": cofre.puntos,
                "puntos_acum": self.puntos_totales,
            })
            print(f"  {cofre}")
            print(f" Puntos acumulados: {self.puntos_totales}")
            return

        # ── Paso 2: generar contraseña ─────────────────────────
        contrasena = Contrasena(longitud)
        contrasena.generar()

        # ── Paso 3: validar contraseña ─────────────────────────
        try:
            contrasena.validar()

            # Contraseña válida → cofre aleatorio positivo
            cofre = Cofre()
            self.puntos_totales += cofre.puntos

            print("\n¡Contraseña VÁLIDA! El cofre se abre...")
            self._mostrar_resultado(contrasena, cofre)

            self.historial.append({
                "ronda": self.ronda, "valida": True,
                "contrasena": contrasena.valor,
                "longitud": longitud,
                "cofre": cofre.tipo,
                "puntos_ronda": cofre.puntos,
                "puntos_acum": self.puntos_totales,
            })

        except ContrasenaInvalidaError as e:
            # Contraseña inválida → cofre maldito
            cofre = Cofre("Maldito")
            self.puntos_totales += cofre.puntos

            print(f"\n  {e}")
            print("\n Contraseña INVÁLIDA. Se abre el Cofre Maldito...")
            self._mostrar_resultado(contrasena, cofre)

            self.historial.append({
                "ronda": self.ronda, "valida": False,
                "contrasena": contrasena.valor,
                "longitud": longitud,
                "cofre": cofre.tipo,
                "puntos_ronda": cofre.puntos,
                "puntos_acum": self.puntos_totales,
            })

    # ── bucle principal ────────────────────────────────────────

    def iniciar(self):
        """Punto de entrada del juego. Gestiona el bucle de rondas."""
        self._imprimir_banner()
        print("  Reglas:")
        print("  • Ingresa la longitud deseada (≥ 8) y se generará una contraseña.")
        print("  • Contraseña válida  → cofre con puntos positivos ")
        print("  • Contraseña inválida → cofre maldito (–20 pts)")
        print(f"  • Caracteres especiales permitidos: {''.join(Contrasena.ESPECIALES)}")

        while True:
            self.jugar_ronda()

            print(f"\n{self.SEPARADOR}")
            continuar = input("  ¿Deseas continuar jugando? (s/n): ").strip().lower()

            if continuar not in ("s", "si", "sí", "y", "yes"):
                break

        # ── Pantalla final ─────────────────────────────────────
        print(f"\n{self.SEPARADOR}")
        print("  JUEGO TERMINADO")
        print(self.SEPARADOR)
        print(f"  Rondas jugadas    : {self.ronda}")
        print(f"  Puntos finales    : {self.puntos_totales}")

        validas = sum(1 for r in self.historial if r["valida"])
        print(f"  Contraseñas válidas  : {validas}/{self.ronda}")
        print(f"  Contraseñas inválidas: {self.ronda - validas}/{self.ronda}")

        if self.ronda > 0:
            self._mostrar_historial()

        if self.puntos_totales >= 100:
            print("\n¡MAESTRO CAZADOR! Puntuación magistral.")
        elif self.puntos_totales >= 50:
            print("\n ¡Buen trabajo, Cazador!")
        elif self.puntos_totales > 0:
            print("\n Sigue practicando, ¡puedes mejorar!")
        else:
            print("\n Los cofres malditos te vencieron... ¡inténtalo de nuevo!")

        print(f"\n{self.SEPARADOR}\n")




if __name__ == "__main__":
    juego = JuegoCazador()
    juego.iniciar()