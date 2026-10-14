"""Pruebas del lexer: del texto a los tokens."""

import pytest
from mini_interprete.lexer import tokenizar
from mini_interprete.tokens import Token, TipoToken
from mini_interprete.errores import ErrorDeSintaxis


def test_tokeniza_un_numero_solo():
    assert tokenizar("42") == [Token(TipoToken.NUMERO, 42, 0)]


def test_tokeniza_una_suma():
    assert tokenizar("3+4") == [
        Token(TipoToken.NUMERO, 3, 0),
        Token(TipoToken.MAS, "+", 1),
        Token(TipoToken.NUMERO, 4, 2),
    ]


def test_los_espacios_no_producen_tokens():
    assert len(tokenizar("  3   +   4  ")) == 3


def test_tokeniza_parentesis():
    tipos = [token.tipo for token in tokenizar("(3)")]
    assert tipos == [TipoToken.PAR_IZQ, TipoToken.NUMERO, TipoToken.PAR_DER]


# PRUEBA DE FORMATO DE NÚMEROS (Caso Frontera)
def test_ceros_a_la_izquierda_se_convierten_a_entero():
    """Según la semántica declarada: '007' es el entero 7."""
    tokens = tokenizar("007")
    assert tokens[0].valor == 7


# PRUEBA DE CARACTERES INVÁLIDOS (Caso Inválido)
def test_caracter_invalido_lanza_error_de_sintaxis():
    """Un carácter no reconocido como '$' o letras debe ser rechazado con ErrorDeSintaxis."""
    with pytest.raises(ErrorDeSintaxis):
        tokenizar("3 $ 4")

# PRUEBA DE MULTIPLICACIÓN Y DIVISIÓN (Caso Normal)
def test_tokeniza_multiplicacion_y_division():
    """Verifica la tokenización estándar de operadores de multiplicación y división."""
    tokens = tokenizar("6 * 2 / 3")
    assert len(tokens) == 5
    assert tokens[1].tipo == TipoToken.POR
    assert tokens[3].tipo == TipoToken.ENTRE