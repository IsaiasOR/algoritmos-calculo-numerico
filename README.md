# Cálculo Numérico

Este proyecto reúne implementaciones en Python de métodos para resolver sistemas de ecuaciones lineales.

## Algoritmos implementados

Hasta el momento, el proyecto incluye los siguientes algoritmos:

- Método de Gauss.
- Método de Gauss-Jordan.
- Descomposición LU.
- Método de Jacobi.
- Método de Gauss-Seidel.
- Pivoteo parcial.

## Cómo ejecutar los algoritmos

Cada algoritmo se ejecuta desde la raíz del proyecto con Python, por ejemplo:

```bash
python -m sel_metodos_directos/gauss.py
python -m sel_metodos_directos/gauss_jordan.py
python -m sel_metodos_directos/lu.py
python -m sel_metodos_iterativos/jacobi.py
python -m sel_metodos_iterativos/gauss_seidel.py
```

Al ejecutarlos, el programa solicitará los datos de entrada por consola.

## Algoritmos previstos

En una siguiente etapa se implementarán los siguientes métodos de búsqueda de raíces:

- Normas.
- Bisección.
- Regula falsi.
- Iteración de punto fijo.
- Newton-Raphson.
- Newton de segundo orden.
- Método de la secante de Newton-Lagrange.
- Método de Müller.

## Estructura del proyecto

- `sel_metodos_directos/`: métodos directos para sistemas lineales.
- `sel_metodos_iterativos/`: métodos iterativos y utilidades asociadas.
- `normas/`: distintos métodos para calcular las normas.

## Estado actual

El repositorio está orientado a prácticas de cálculo numérico y se ampliará con nuevos métodos de resolución de ecuaciones no lineales.
