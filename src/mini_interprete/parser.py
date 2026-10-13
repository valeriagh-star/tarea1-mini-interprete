"""De los tokens al AST.

La gramatica que reconoce este parser es:

    expresion := termino  (('+' | '-') termino)*
    termino   := factor   (('*' | '/') factor)*
    factor    := NUMERO | '(' expresion ')'

Los tres niveles son lo que hace que  3 + 4 * 2  se agrupe como  3 + (4 * 2)
y no como  (3 + 4) * 2 : la multiplicacion vive un nivel mas abajo, asi que
se arma primero.
"""

from .ast import Numero, OperacionBinaria
from .errores import ErrorDeSintaxis
from .tokens import TipoToken

OPERADORES_SUMA = (TipoToken.MAS, TipoToken.MENOS)
OPERADORES_PRODUCTO = (TipoToken.POR, TipoToken.ENTRE)


class Parser:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def parsear(self):
        """Construye el AST de la lista de tokens."""
        if not self.tokens:
            raise ErrorDeSintaxis("expresion vacia", 0)
        
        arbol = self._expresion()

        if self.pos < len(self.tokens):
            token_sobrante = self._actual()
            raise ErrorDeSintaxis(f"token inesperado {token_sobrante.valor!r}", token_sobrante.posicion)
            
        return arbol
        
    def _actual(self):
        """El token en la posicion actual, o None si ya no quedan."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _avanzar(self):
        """Consume el token actual y lo regresa. Lanza ErrorDeSintaxis si llega al final inesperadamente."""
        if self.pos >= len(self.tokens):
            # Usamos la posición del último token si existe para el mensaje de error
            pos_error = self.tokens[-1].posicion + 1 if self.tokens else 0
            raise ErrorDeSintaxis("fin de entrada inesperado", pos_error)
        
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _expresion(self):
        nodo = self._termino()
        # Se cambia 'if' por 'while' para asociar a la izquierda de forma iterativa
        while self._actual() is not None and self._actual().tipo in OPERADORES_SUMA:
            operador = self._avanzar()
            derecha = self._termino()
            nodo = OperacionBinaria(operador.valor, nodo, derecha)
        return nodo

    def _termino(self):
        nodo = self._factor()
        # Se cambia 'if' por 'while' para asociar a la izquierda de forma iterativa
        while self._actual() is not None and self._actual().tipo in OPERADORES_PRODUCTO:
            operador = self._avanzar()
            derecha = self._factor()
            nodo = OperacionBinaria(operador.valor, nodo, derecha)
        return nodo

    def _factor(self):
        token = self._avanzar()

        if token.tipo == TipoToken.NUMERO:
            return Numero(token.valor)

        if token.tipo == TipoToken.PAR_IZQ:
            nodo = self._expresion()
            
            # Verificar si se llegó al final antes de encontrar el ')'
            if self._actual() is None:
                raise ErrorDeSintaxis("se esperaba ')' al final de la expresion", token.posicion)
                
            cierre = self._avanzar()
            if cierre.tipo != TipoToken.PAR_DER:
                raise ErrorDeSintaxis("se esperaba ')'", cierre.posicion)
            return nodo

        raise ErrorDeSintaxis(f"token inesperado {token.valor!r}", token.posicion)
