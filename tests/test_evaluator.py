"""Pruebas del evaluador: del AST a un numero."""

import pytest
from mini_interprete.cli import interpretar
from mini_interprete.errores import ErrorDeEvaluacion, ErrorDeSintaxis


def test_suma():
    assert interpretar("3 + 4") == 7


def test_resta():
    assert interpretar("10 - 3") == 7


def test_multiplicacion():
    assert interpretar("6 * 7") == 42


def test_division():
    assert interpretar("10 / 2") == 5


def test_precedencia_sin_parentesis():
    assert interpretar("3 + 4 * 2") == 11


def test_precedencia_con_parentesis():
    assert interpretar("(3 + 4) * 2") == 14

# CASOS NORMALES
def test_evalua_resta_y_suma_combinadas():
    """Verifica la evaluación estándar de operaciones mixtas con igual precedencia."""
    assert interpretar("10 - 3 + 2") == 9


def test_division_real_con_flotante():
    """Verifica que la división retorne un número flotante (10 / 4 = 2.5)."""
    assert interpretar("10 / 4") == 2.5


def test_evalua_expresion_combinada_con_parentesis():
    """Verifica la correcta evaluación de una expresión con combinación de operadores y paréntesis."""
    assert interpretar("(2 + 3) * 4") == 20


# CASO INVÁLIDO
def test_division_por_cero_lanza_error_de_evaluacion():
    """Verifica que dividir entre cero lance un ErrorDeEvaluacion."""
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("10 / 0")


# CASO FRONTERA / INVÁLIDO
def test_menos_unario_no_soportado_lanza_error():
    """Verifica que números con signo negativo unario no sean soportados y lancen error."""
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-3")