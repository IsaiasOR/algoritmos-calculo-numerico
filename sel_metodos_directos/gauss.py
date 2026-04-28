# Método de Gauus
# Sistemas de ecuaciones lineales A.X = B
import numpy as np
from pivoteo import pivoteo_parcial

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
  ab = np.hstack((A, B.reshape(-1, 1))) # Matriz aumentada sin pivoteo
  print("\nMatriz aumentada:")
  print(ab)

tamano = np.shape(ab)
n = tamano[0]
m = tamano[1]

# Eliminación hacia adelante
print('\nEliminación hacia adelante:')
for i in range(0, n-1, 1): # Para cada fila en ab, excepto la última
  pivote = ab[i][i] # El pivote es el elemento en la posición (i, i) de ab
  adelante = i + 1 # La fila siguiente a la fila actual
  # Para cada fila debajo de la fila actual, calcula el factor de eliminación y actualiza la fila restando el factor multiplicado por la fila actual
  for j in range(adelante, n, 1):
    factor = ab[j][i] / pivote
    ab[j] = ab[j] - factor * ab[i]
    print(f"Fila {j+1} actualizada: {ab[j]}, factor: {factor}")
    print(ab)

print("\nMatriz aumentada después de eliminar hacia adelante")
print(ab)

# Sustitución hacia atrás
print('\nSustitución hacia atrás:')
ultima_fila = n - 1
ultima_columna = m - 1
# Inicializa el vector de soluciones X con ceros
X = np.zeros(n, dtype=float)

# Para cada fila desde la última hacia la primera
for i in range(ultima_fila, 0-1, -1):
  # ab[i][i+1:ultima_columna] → coeficientes de las variables ya calculadas (a la derecha de la diagonal en esa fila)
  # X[i+1:ultima_columna] → valores de las variables (ya conocidos por iteraciones anteriores)
  # np.dot multiplica cada coeficiente por su variable y los suma
  suma = np.dot(ab[i][i+1:ultima_columna], X[i+1:ultima_columna])
  # Calcula la solución para la variable correspondiente a la fila actual restando la suma de los productos de los coeficientes y las soluciones ya encontradas del término independiente (ab[i][ultima_columna]) y dividiendo por el coeficiente de la variable en la fila actual (ab[i][i])
  X[i] = (ab[i][ultima_columna] - suma) / ab[i][i]
  print(f"X[{i+1}] = {X[i]}")

print("\nSolución del sistema de ecuaciones con el método de Gauss:")
print("Solución X:")
print(X)