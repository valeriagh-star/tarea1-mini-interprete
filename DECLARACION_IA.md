# Declaración de uso de Inteligencia Artificial

**Actividad:** Tarea 1

**Integrantes:**
1. García Herrera Valeria
2. Grajeda Palacios Dulce Abril
3. Pérez Megchun Pablo de Jesús

**Fecha:** 16 de octubre de 2026
---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.** Firmen la última sección y terminen. Con eso queda completa.
- [ ✔ ] **Sí.** Contesten los cinco puntos.

---

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
|---|---|
| Google Gemini | Flash (asistencia en chat) |
| GitHub Copilot | Extensión autocompletado en Visual Studio Code |

---

## 2. Objetivo del uso

| Para qué la usamos | En qué parte del entregable |
|---|---|
| Autocompletado rápido de sintaxis e impresiones durante la edición. | En el editor Visual Studio Code al modificar los archivos `.py` |
| Asesoría para la redacción técnica de los incisos. | Respuestas de la Sección 4.3 en `ANALISIS.md`, en la sección 4.3 porque no sabíamos cómo representar los commits o qué deberíamos poner en esos rubros, y en secciones como 4.4, 5.1 y 5.2  solo para redactar mejor las respuestas. |
| Asistencia técnica para el uso de Git (comandos para subir cambios, uso de `--amend` y resolución de conflictos). | Flujo de trabajo en la terminal local. |

---

## 3. Prompts principales

```
(prompt 1)
```
No entiendo qué debemos poner en los apartados de Commit rojo y Commit verde, explica: ### 4.3 ¿Qué cambio realizaron? 

 | Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde | 
 |---|---|---|---|---|---| 
 | | | | | | | 

```
(prompt 2)
```
Se está usando Windows, al cambiar a terminal bash en Visual Studio y querer subir los commits de las pruebas realizadas, nos dice que no reconoce los comandos, qué debemos hacer?

```
(prompt 3)
```
Subimos un commit pero lo describimos mal, cómo podemos cambiarle el nombre?

---

## 4. Cómo se incorporó o se descartó lo obtenido

**Éste es el punto que más pesa.**

| Qué produjo la herramienta | ¿Aceptado, modificado o descartado? | Por qué | Dónde quedó (archivo / commit) |
|---|---|---|---|
| Autocompletado inicial de Copilot usando `if` en `_expresion` | **Descartado** | Mantenía la asociatividad a la derecha y calculaba mal operaciones encadenadas como `10 - 4 - 2`. | `src/mini_interprete/parser.py` |
| Abstracción del método `_operacion_binaria` con un ciclo `while` | **Aceptado** | Se aceptó para eliminar código duplicado y fijar la asociatividad a la izquierda. | `src/mini_interprete/parser.py` |
| Estructura del mapa `OPERACIONES` con funciones lambda. | **Aceptado con modificaciones** | Nos sirvió para quitar los `if` repetidos del evaluador; le ajustamos el estilo para que quedara más limpio y legible. | `src/mini_interprete/evaluator.py` |
| Comandos para Git (`git commit --amend`, `git push --force-with-lease`) y solución de Path en Bash. | **Aceptado** | Nos permitió solucionar el problema con los comandos no reconocidos en la terminal de VS Code y mantener limpio el historial. | Flujo de trabajo en la terminal local |
| Explicación sobre qué poner en los incisos de Commit Rojo y Commit Verde | **Aceptado con modificaciones** | Nos ayudó a entender el concepto del flujo TDD para redactar las tablas del análisis con nuestras propias palabras. | `ANALISIS.md` |
---

### 4.1 Si la usaron para el análisis: el contraste

**NO APLICA**

Se les pidió intentarlo primero por su cuenta. Si lo hicieron así:

| | |
|---|---|
| ¿Qué encontró la herramienta que ustedes **no** habían notado? | |
| ¿Qué **no** encontró, que en este curso sí consideramos un problema? | |
---

### 4.2 ¿Cómo verificaron que lo que incorporaron era correcto?

Corrimos la suite de pruebas automáticas ejecutando el comando `pytest` y `pytest -v` en la terminal de VS Code después de cada cambio en el código. Verificamos que las 25 pruebas pasaran en verde, poniendo especial atención en las pruebas de asociatividad a la izquierda (como `10 - 4 - 2 = 4`) para asegurarnos de que la refactorización con el ciclo `while` en `parser.py` no hubiera cambiado la lógica del intérprete. De igual manera, confirmamos que la evaluación de los operadores (+, -, *, /) siguiera respondiendo correctamente tras reemplazar los `if` repetidos por el diccionario `OPERACIONES` en `evaluator.py`, garantizando que no se rompiera el comportamiento original.

---

## 5. Reflexión

### 5.1 ¿Qué limitación concreta observaron **en esta actividad**?

Observamos que la herramienta no identificó la duplicación de código entre `_expresion` y `_termino` en el parser; al generar o autocompletar el código, daba la solución por correcta porque sintácticamente funcionaba, pasando por alto que ambos métodos compartían exactamente el mismo comportamiento. Además, las sugerencias de Copilot en VS Code tendían a perpetuar el patrón con `if` recursivos sin advertir que esto rompía la asociatividad a la izquierda en operaciones encadenadas como `10 - 4 - 2`.

---

### 5.2 ¿Qué harían distinto la próxima vez?

Seríamos más minuciosos al revisar el código línea por línea antes de integrarlo, fijándonos tanto en la indentación de Python como en no mantener estructuras redundantes solo porque "ya funcionan". De hecho, consideramos que para refactorizaciones estructurales como la eliminación de duplicación o la aplicación de patrones, es mucho mejor analizar y realizar los cambios directamente nosotros mismos desde el principio, utilizando las herramientas solo para consultas puntuales o sintácticas.

---

## Firma

> Declaramos que entendemos y podemos explicar todo lo que entregamos,
> independientemente de las herramientas que hayamos utilizado.

| Nombre | Número de cuenta |
|---|---|
| García Herrera Valeria | 323284819 |
| Grajeda Palacios Dulce Abril | 323300120 |
| Pérez Megchun Pablo de Jesús | 426008701 |