# Método LU
# Descomposición de una matriz A en el producto de una matriz triangular inferior L y una matriz triangular superior U

import numpy as np
from sel_metodos_iterativos.pivoteo import pivoteo_parcial

def lu_decomposicion(AB: np.ndarray) -> list[np.ndarray]:
  print("\n" + "="*70)
  print(" Iniciando descomposición LU (Método de Doolittle - Vía Eliminación Gaussiana)")
  print("="*70)

  tamano = np.shape(AB)
  n = tamano[0]
  m = tamano[1]
  L = np.identity(n, dtype=float)

  for i in range(0, n,1):
    pivote = AB[i, i]
    adelante = i + 1

    print(f"\n--- PASO {i+1} ---")
    print(f"Pivote actual en diagonal: {pivote:.4f}")

    for j in range(adelante, n, 1):
      if (np.abs(pivote) >= 1e-15):
        factor = AB[j, i] / pivote
        AB[j, :] = AB[j, :] - factor * AB[i, :]

        # Redondeo a cero para evitar errores numéricos
        for k in range(m):
          if np.abs(AB[j, k]) < 1e-15:
            AB[j, k] = 0.0

        L[j, i] = factor # Llena la matriz L con los factores de eliminación
        print(f"  ○ Fila {j+1} modificada. Factor usado: {factor:.4f}")

      else:
        print("\n" + "="*70)
        print(f" ERROR: Pivote nulo encontrado en la posición ({i+1}, {i+1})")
        print(" No se puede continuar con la descomposición LU.")
        print("="*70)
        raise ValueError("Pivote nulo.")

  # Extrae la matriz U de la parte superior de la matriz cuadrada de coeficientes
  U = np.triu(AB[:, :n])

  # Extraer el vector C de la última columna de la matriz AB modificada
  C = AB[:, n]

  print("\nVector intermedio C:")
  print(C)

  print("\nSustitución hacia atrás para resolver U * X = C")
  # Sustitución hacia atrás para resolver U * X = C
  X = np.zeros(n, dtype=float)

  for i in range(n-1, -1, -1): # Recorre de abajo hacia arriba
    print(f"\n--- Despejando X[{i+1}] ---")
    X[i] = C[i]
    print(f"Valor inicial (C[{i+1}]): {X[i]:.4f}")

    # Solo entra a este bucle si hay variables a la derecha ya calculadas
    if i < n - 1:
      print("Restando términos de variables ya conocidas:")

    for j in range(i+1, n):
      termino = U[i, j] * X[j]
      X[i] = X[i] - termino
      print(f"  ○ Acumulado parcial - (U[{i+1},{j+1}] * X[{j+1}]) = {X[i] + termino:.4f} - ({U[i,j]:.4f} * {X[j]:.4f}) = {X[i]:.4f}")

    X[i] = X[i] / U[i, i]
    print(f"Dividiendo por el pivote U[{i+1},{i+1}] ({U[i,i]:.4f}):")
    print(f"● X[{i+1}] = {X[i]:.4f}")

  print("\n" + "="*70)
  print(" DESCOMPOSICIÓN COMPLETADA")
  print("="*70)

  # Devuelve la matriz AB modificada, L y U
  return [L, U, X]


print("\n" + "*"*80)
print(" INICIANDO PROCEDIMIENTO DE RESOLUCIÓN DE SISTEMA DE ECUACIONES")

# Ingreso de datos
n = int(input("Ingrese el número de ecuaciones: "))
# Crea un nueva matriz A de tamaño n x n con valores iniciales de 0
A = np.zeros((n, n), dtype=float)
# Crea un nuevo vector B de tamaño n con valores iniciales de 0
B = np.zeros(n, dtype=float)

print("Ingrese los coeficientes de la matriz A:")
for i in range(n):
  for j in range(n):
    A[i][j] = float(input(f"A[{i+1}][{j+1}]: "))

print("\nIngrese los términos independientes:")
for i in range(n):
  B[i] = float(input(f"B[{i+1}]: "))

print("\nMatriz A:")
print(A)
print("\nVector B:")
print(B)

# Privoteo parcial
print("\nDesea realizar pivoteo parcial? (s/n): ")
opcion = input().lower()
if opcion == 's':
  ab = pivoteo_parcial(A, B)
else:
  ab = np.column_stack((A, B))

# Configuración visual para NumPy
np.set_printoptions(precision=4, suppress=True)

# Método de LU
ab_final = lu_decomposicion(ab)
L = ab_final[0] # Índice 0 corresponde a la matriz L
U = ab_final[1] # Índice 1 corresponde a la matriz U
X = ab_final[2] # Índice 2 corresponde al vector solución X

# Solución final
print("\nMatriz L: ")
print(L)
print("\nMatriz U: ")
print(U)
print("\nVector solución X: ")
print(X)
print("\n" + "*"*80)