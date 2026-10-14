# Análisis — Tarea 1

**Integrantes:**
1. García Herrera Valeria
2. Grajeda Palacios Dulce Abril
3. Pérez Megchun Pablo de Jesús

**Fork:** https://github.com/valeriagh-star/tarea1-mini-interprete

**Rama:** tarea1-pruebas-refactorizacion

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` | Una cadena de texto (`str`) | Una lista de `Token` | Debe partir la entrada en tokens e identificar números, operadores y paréntesis, ignorando espacios. |
| `parser` | Una lista de `Token` | `Nodo` del AST | Debe construir la estructura jerárquica del árbol aplicando la gramática y la precedencia de operadores. |
| `ast` | No recibe nada, se limita a definir los tipos de datos que representan los nodos. | Nodos `Numero` y `OperacionBinaria`. | |
| `evaluator` | `Nodo` del AST | Un número de tipo `int` o `float` | Debe recorrer el AST de manera recursiva para realizar los cálculos y lanzar `ErrorDeEvaluacion` si falla.|

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens | `[Token(PAR_IZQ, '(', 0), Token(NUMERO, 3, 1), Token(MAS, '+', 3), Token(NUMERO, 4, 5), Token(PAR_DER, ')', 6), Token(POR, '*', 8), Token(NUMERO, 2, 10)]` |
| AST | `OperacionBinaria('*', OperacionBinaria('+', Numero(3), Numero(4)), Numero(2))` |
| resultado | `14` |

* Representación en forma de árbol de esta operación: 

```text
*
|-- +
|   |-- 3
|   `-- 4
`-- 2
```
---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| `test_lexer.py::test_tokeniza_un_numero_solo` | `lexer` | Reconoce y convierte un entero a un único token. | 0 | Normal |
| `test_lexer.py::test_tokeniza_una_suma` | `lexer` | Genera la secuencia correcta de tokens para una operación básica sin espacios. | 1 | Normal |
| `test_lexer.py::test_los_espacios_no_producen_tokens` | `lexer` | Ignora espacios en blanco múltiples alrededor de tokens. | 1 | Frontera |
| `test_lexer.py::test_tokeniza_parentesis` | `lexer` | Reconoce los símbolos de paréntesis de apertura y cierre. | 0 | Normal |
| `test_parser.py::test_construye_el_arbol_de_una_suma` | `parser` | Arma la estructura binaria para una suma simple. | 1 | Normal |
| `test_parser.py::test_la_multiplicacion_se_agrupa_antes_que_la_suma` | `parser` | Respeta la precedencia por defecto agrupando la multiplicación primero. | 2 | Normal |
| `test_parser.py::test_los_parentesis_cambian_la_agrupacion` | `parser` | Modifica el AST agrupando primero la suma al usar paréntesis. | 2 | Normal |
| `test_evaluator.py::test_suma` | `evaluator` | Calcula la suma de dos números enteros. | 1 | Normal |
| `test_evaluator.py::test_resta` | `evaluator` | Calcula la resta de dos números enteros. | 1 | Normal |
| `test_evaluator.py::test_multiplicacion` | `evaluator` | Calcula la multiplicaión de dos números enteros. | 1 | Normal |
| `test_evaluator.py::test_division` | `evaluator` | Calcula la división exacta de dos números enteros. | 1 | Normal |
| `test_evaluator.py::test_precedencia_sin_parentesis` | `evaluator` | Evalúa correctamente la suma y multiplicación sin paréntesis según precedencia. | 2 | Normal |
| `test_evaluator.py::test_precedencia_con_parentesis` | `evaluator` | Evalúa correctamente cuando los paréntesis alteran el orden natural. | 2 | Normal |

### 2.2 ¿Qué comportamientos **no** estaban probados?

Al revisar las 13 pruebas que venían en el proyecto, nos dimos cuenta de que faltaban probar los siguientes casos importantes:

1. **Entradas con errores:**
   * **Errores de Sintaxis:** No existe ninguna prueba que valide el comportamiento del sistema ante expresiones mal compuestas (ej. paréntesis sin cerrar `(3 + 4`, operadores consecutivos `3 ++ 4` o expresiones incompletas `3 +`).
   * **Errores Lexicográficos:** Tampoco se probó qué ocurre si metes letras o caracteres que el sistema no conoce, como `3 + a` o `3 $ 4`.

2. **Errores de Evaluación en Tiempo de Ejecución:**
   * **División entre cero:** Aunque el componente `evaluator` contiene una validación para lanzar `ErrorDeEvaluacion` cuando se divide entre cero, no existe ninguna prueba en `test_evaluator.py` que compruebe que esta excepción se dispare correctamente.

3. **Asociatividad de Operadores de Igual Precedencia (Casos Frontera):**
   * No se prueban cadenas de operadores de la misma prioridad seguidos sin paréntesis (ej. restas encadenadas `10 - 4 - 2` o divisiones encadenadas `12 / 3 / 2`). Esto no permite verificar si la gramática del `parser` asocia correctamente de **izquierda a derecha** o si cae en asociatividad a la derecha.

4. **Operaciones con Flotantes y Tipos de Datos:**
   * **Resultados Decimales:** Todas las pruebas de división existentes resultan en enteros exactos (`10 / 2 = 5`). No se evalúa el comportamiento cuando la división devuelve un número flotante (ej. `10 / 8 = 1.25`).

5. **Límites de Formato y Sintaxis en el Lexer:**
   * **Ceros a la Izquierda:** No se valida cómo interpreta el `lexer` números con formato inusual como `007` o `00`.
   * **Operador Unario Negativo:** No hay pruebas para verificar si el sistema soporta o rechaza números negativos directos como `-5` o `3 * -2`.

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| `tests/test_parser.py::test_resta_encadenada_asocia_a_la_izquierda` | `"10 - 4 - 2"` | `OperacionBinaria("-", OperacionBinaria("-", Numero(10), Numero(4)), Numero(2))` | Frontera | Evalúa la regla de asociatividad a la izquierda para operadores de igual precedencia. |
| `tests/test_parser.py::test_expresion_incompleta_lanza_error` | `"3 +"` | Lanza `ErrorDeSintaxis` | Inválido | Falta el operando derecho de la suma, violando la gramática del lenguaje. |
| `tests/test_parser.py::test_parentesis_sin_cerrar_lanza_error` | `"(3 + 4"` | Lanza `ErrorDeSintaxis` | Inválido | Falta el paréntesis de cierre `)`, dejando la estructura sintáctica incompleta. |
| `tests/test_parser.py::test_operadores_consecutivos_lanza_error` | `"3 ++ 4"` | Lanza `ErrorDeSintaxis` | Inválido | Dos operadores seguidos sin un operando entre ellos rompen la sintaxis esperada. |
| `tests/test_lexer.py::test_ceros_a_la_izquierda_se_convierten_a_entero` | `"007"` | `Token(NUMERO, 7, 0)` | Frontera | Verifica el caso límite en el que un entero viene precedido de ceros a la izquierda sin alterar su valor final. |
| `tests/test_lexer.py::test_caracter_invalido_lanza_error_de_sintaxis` | `"3 $ 4"` | Lanza `ErrorDeSintaxis` | Inválido | Símbolos fuera del alfabeto/tokens permitidos por el lexer deben rechazarse inmediatamente. |
| `tests/test_lexer.py::test_tokeniza_multiplicacion_y_division` | `"6 * 2 / 3"` | Lista de 5 tokens válidos | Normal | Verifica la tokenización estándar de expresiones con multiplicación y división secuencial. |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

El primer defecto revelado por la suite de pruebas fue un problema de asociatividad en el parser (`test_resta_encadenada_asocia_a_la_izquierda`). Al procesar la expresión `"10 - 4 - 2"`, el parser genera una agrupación a la derecha `10 - (4 - 2)` en lugar de asociar hacia la izquierda `(10 - 4) - 2`. 

Además, las pruebas de errores sintácticos revelaron que expresiones incompletas (`"3 +"`) o sin cerrar (`"(3 + 4"`) provocan un fallo no controlado del sistema (`IndexError: list index out of range` en `_avanzar()`) en lugar de lanzar la excepción esperada `ErrorDeSintaxis`.

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

El comportamiento fue incorrecto porque violó directamente tres reglas explícitas de la **Sección 7 (Semántica declarada)** del `README.md`:

1. **Resta encadenada (`"10 - 4 - 2"`):** Rompe la regla del renglón **Asociatividad**, el cual especifica textualmente: *"los operadores de la misma precedencia se asocian a la izquierda"*. El parser agrupaba hacia la derecha (`10 - (4 - 2)`), devolviendo `8` en lugar de `4`.
2. **Expresiones incompletas y paréntesis sin cerrar (`"3 +"`, `"(3 + 4"`):** Rompe la regla del renglón **Entrada inválida**, que indica: *"debe rechazarse con ErrorDeSintaxis, nunca con un error de Python"*. El parser dejó propagar un `IndexError: list index out of range` al intentar leer más allá del arreglo de tokens.
3. **Carácter no reconocido (`"3 $ 4"`):** También violó el renglón **Entrada inválida** (*"debe rechazarse con ErrorDeSintaxis"*), ya que el lexer no capturaba el símbolo ajeno a la gramática ni lanzaba la excepción correspondiente.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| Asociatividad a la derecha en restas encadenadas. | `"10 - 4 - 2"` | `OperacionBinaria("-", Numero(10), OperacionBinaria("-", Numero(4), Numero(2)))` | `OperacionBinaria("-", OperacionBinaria("-", Numero(10), Numero(4)), Numero(2))` | `37ffaf4` | `ec5a04d` |
| Desbordamiento de lista en expresiones incompletas o paréntesis sin cerrar. | `"3 +"` / `"(3 + 4"` | `IndexError: list index out of range` | Lanza `ErrorDeSintaxis` | `37ffaf4` | `ec5a04d` |
| Carácter no reconocido no es capturado como sintaxis inválida. | `"3 $ 4"` | No lanza excepción (`Failed: DID NOT RAISE ErrorDeSintaxis`) | Lanza `ErrorDeSintaxis` | `eb8d488` | `4204132` |

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

> Al menos dos. Usen el vocabulario de clase: duplicación, rigidez,
> acoplamiento alto, condicionales repetidos, amplificación del cambio.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

> "Las pruebas siguen pasando" es parte de la respuesta, pero no toda.
> ¿Por qué el cambio es equivalente?

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

> Justifiquen. **"Ninguno" puede ser la respuesta correcta.** Si dicen que sí,
> digan qué problema concreto resuelve y qué costo tiene. Si dicen que no,
> digan qué tendría que cambiar en el sistema para que empezara a convenir.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

> Por ejemplo `%`. ¿Cuántos archivos hay que tocar? ¿Por qué?

---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué *no* encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. *"No usamos"* es una declaración válida y completa; *"lo
descartamos porque..."* es de las mejores respuestas posibles.
