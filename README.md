# Cálculo Numérico

Este proyecto reúne implementaciones en Python de métodos para resolver sistemas de ecuaciones lineales y ecuaciones no lineales.

## Algoritmos implementados

Hasta el momento, el proyecto incluye los siguientes algoritmos:

### Normas

- Normas vectoriales
  - Norma suma
  - Norma euclidiana
  - Norma infinito (máximo)
- Normas matriciales
  - Norma infinito (fila-suma)
  - Norma columna-suma
  - Norma de Frobenius

### Sistemas de ecuaciones lineales - Métodos directos

- Método de Gauss.
- Método de Gauss-Jordan.
- Descomposición LU.

### Sistemas de ecuaciones lineales - Métodos iterativos

- Método de Jacobi.
- Método de Gauss-Seidel.

### Utilidades

- Pivoteo parcial.

### Métodos de búsqueda de raíces

- Bisección.
- Regula falsi.
- Método de Müller.
- Iteración de punto fijo.
- Newton-Raphson.
- Newton de segundo orden.
- Método de la secante de Newton-Lagrange.

## Cómo ejecutar los algoritmos

Cada algoritmo se ejecuta desde la raíz del proyecto con Python, por ejemplo:

```bash
python -m sistemas_de_ecuaciones_lineales.sel_metodos_directos.gauss
python -m sistemas_de_ecuaciones_lineales.sel_metodos_directos.gauss_jordan
python -m sistemas_de_ecuaciones_lineales.sel_metodos_directos.lu
python -m sistemas_de_ecuaciones_lineales.sel_metodos_iterativos.jacobi
python -m sistemas_de_ecuaciones_lineales.sel_metodos_iterativos.gauss_seidel
python -m sistemas_de_ecuaciones_no_lineales.biseccion
python -m sistemas_de_ecuaciones_no_lineales.regula_falsi
python -m sistemas_de_ecuaciones_no_lineales.muller
```

Al ejecutarlos, el programa solicitará los datos de entrada por consola.

## Estructura del proyecto

- `sistemas_de_ecuaciones_lineales/`: métodos para resolver sistemas lineales.
  - `sel_metodos_directos/`: métodos directos.
  - `sel_metodos_iterativos/`: métodos iterativos.
- `sistemas_de_ecuaciones_no_lineales/`: métodos de búsqueda de raíces.
- `normas/`: distintos métodos para calcular las normas.

## Estado actual

El repositorio incluye implementaciones de algoritmos para calcular normas vectoriales y matriciales, métodos para resolver sistemas de ecuaciones lineales (métodos directos e iterativos) y métodos de búsqueda de raíces.
