# PCD-Sexcom

> **SEMILLA: 1**

Repositorio destinado para la asignatura de programación para ciencia de datos

EQUIPO: Los cazadores de bandides

TEMA: Ventas online

SEED: 1

Integrantes: 
1- Perez Davila Ulises Alberto

2- Fuentes Rosales Isis Jeanell

Practica 1:

Se hizo un analisis breve y concreto de los datos proporcionados (ventas_online-ruido_100000.csv), usando manejo de archivos y las funciones sum(), min() y max(), dejando los resultados en
un archivo con nombre 'resumen.txt'

Practica 2:

Se observo que al no tener estandarizada la columna de categoria se obtuvieron mas de una categoria con el mismo nombre pero escrita distinta, por esa razon cuando sacamos el promedio por categoria donde CAMARA y camara tienen distintos valores.

📦 **Aviso:** ya está disponible su dataset en `datos/` — `ventas_online-ruido_100.csv` (para pruebas rápidas) y `ventas_online-ruido_100000.csv` (el dataset real para sus prácticas). ¡Ya pueden empezar!

---

## Observaciones del profesor

### 13-oct-2026 — Correcciones de la Práctica 1

**Calificación de P1: 83 → 90 / 100.**

**Corrigieron sus dos observaciones** (commit del 9-oct):

1. El conteo de filas ya es correcto: 103000. El bug era que quitaban la cabecera dos veces
   (con `lineas[1:]` y otra vez con `len(filas) - 1`).
2. La columna numérica ya es **`monto_venta`**: 98866 válidos, mínimo -14634.3 y máximo
   200325.6.

Los dos coinciden exacto con la solución de referencia.

Un detalle menor que no afecta la calificación: en `Pareja:` sigue el nombre del equipo en
vez de los nombres de los integrantes.

**Cómo se aplicó el reconocimiento.** Nueve de los diez equipos que tenían observaciones las atendieron entre el 8 y el 12 de octubre. A quien corrigió y tenía 90 o más, su práctica queda en **99**; a quien tenía menos de 90, en **90**. El 100 se reserva para quien entregó bien desde la primera vez. En la tabla de calificaciones del curso su celda aparece como `anterior/vigente`: el primer número es la entrega original y **el segundo es el que cuenta**.

### Práctica 1 — evaluación (8-oct-2026, 00:51 h)

**Calificación: 83 / 100**

Entregada el **6-oct-2026 a las 17:34**, dentro del plazo (la entrega cerraba el mar 6-oct), así que no lleva penalización por retraso.

**Criterios cubiertos al 100%:** Estructura del monorepo (6/6); Nombres exactos de los entregables; Requisitos de Git (3+ commits, rama mergeada); Python puro (sin `csv` ni `pandas`, lectura con `open`); Formato del `resumen.txt` (encabezado y secciones); Encabezado: Archivo, Pareja, Seed; Primeras 5 filas (separadas con barra y espacios); Columna categórica (nombre, únicos, más frecuente); Calidad de datos (celdas vacías).

**Observaciones:**

1. El conteo de filas es incorrecto: reportan 102999 y son 103000.
2. La columna numérica que pide P1 es la `numerica_1` de su tema, **`monto_venta`**, no `minutos_en_sitio`.

**Desglose:**

| Criterio | Obtenido | Máximo |
|---|:---:|:---:|
| Estructura del monorepo (6/6) | 8 | 8 |
| Nombres exactos de los entregables | 10 | 10 |
| Requisitos de Git (3+ commits, rama mergeada) | 10 | 10 |
| Python puro (sin `csv` ni `pandas`, lectura con `open`) | 8 | 8 |
| Formato del `resumen.txt` (encabezado y secciones) | 9 | 9 |
| Encabezado: Archivo, Pareja, Seed | 10 | 10 |
| Dimensiones: filas, columnas, nombres | 6 | 10 |
| Primeras 5 filas (separadas con barra y espacios) | 5 | 5 |
| Columna categórica (nombre, únicos, más frecuente) | 12 | 12 |
| Columna numérica_1 (nombre, válidos, mín, máx) | 0 | 13 |
| Calidad de datos (celdas vacías) | 5 | 5 |
| **Total** | **83** | **100** |
### 22-sep-2026

**Estatus:** 6/6 de la estructura esperada.

Siguen con la estructura completa, sin pendientes.

### 23-sep-2026

**Estatus:** 6/6 de la estructura esperada.

Siguen con la estructura completa, sin pendientes.

📖 **Práctica 1 ya está disponible.** La encontrarán en `labs/P1/P1_setup_reconocimiento.md`, dentro del repositorio del profesor: https://github.com/ESCOMLCD/pcd202701/blob/main/labs/P1/P1_setup_reconocimiento.md — léanla completa antes de empezar a programar, ahí está todo lo que deben hacer, el formato exacto de `resumen.txt` y la fecha de entrega (mar 6-oct).

### 26-sep-2026

**Estatus:** 6/6 de la estructura esperada.

Siguen con la estructura completa, sin pendientes.
