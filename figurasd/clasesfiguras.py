from __future__ import annotations

from abc import ABC, abstractmethod
from math import pi


class Figura3D(ABC):
    @abstractmethod
    def calcular_volumen(self) -> float:
        """Calcula y devuelve el volumen de la figura."""

    @abstractmethod
    def calcular_area_superficial(self) -> float:
        """Calcula y devuelve el area superficial de la figura."""

    @abstractmethod
    def dibujar(self) -> str:
        """Devuelve una representacion textual de la figura."""


class Cubo(Figura3D):
    def __init__(self, lado: float) -> None:
        self.lado = lado

    def calcular_volumen(self) -> float:
        return self.lado ** 3

    def calcular_area_superficial(self, factor_escala: float = 1) -> float:
        lado_escalado = self.lado * factor_escala
        return 6 * (lado_escalado ** 2)

    def dibujar(self) -> str:
        return (
            "   +-------+\n"
            "  /       /|\n"
            " +-------+ |\n"
            " |       | +\n"
            " |       |/\n"
            " +-------+\n"
            f" CUBO (lado={self.lado})"
        )


class Esfera(Figura3D):
    def __init__(self, radio: float) -> None:
        self.radio = radio

    def calcular_volumen(self) -> float:
        return (4 / 3) * pi * (self.radio ** 3)

    def calcular_area_superficial(self, factor_escala: float = 1) -> float:
        radio_escalado = self.radio * factor_escala
        return 4 * pi * (radio_escalado ** 2)

    def dibujar(self) -> str:
        return (
            "    .-'''-.\n"
            "  .'  .-.  '.\n"
            " /   (   )   \\\n"
            " |    `-'    |\n"
            " \\           /\n"
            "  '.       .'\n"
            "    '-...-'\n"
            f" ESFERA (radio={self.radio})"
        )


class Cilindro(Figura3D):
    def __init__(self, radio: float, altura: float) -> None:
        self.radio = radio
        self.altura = altura

    def calcular_volumen(self) -> float:
        return pi * (self.radio ** 2) * self.altura

    def calcular_area_superficial(self, factor_escala: float = 1) -> float:
        radio = self.radio * factor_escala
        altura = self.altura * factor_escala
        return 2 * pi * radio * (radio + altura)

    def dibujar(self) -> str:
        return (
            "    _______\n"
            "  /       \\\n"
            " |         |\n"
            " |         |\n"
            " |         |\n"
            "  \\_______/\n"
            f" CILINDRO (radio={self.radio}, altura={self.altura})"
        )



