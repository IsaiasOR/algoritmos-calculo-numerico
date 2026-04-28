# Método de Gauus-Jordan para resolver sistemas de ecuaciones lineales
# Sistemas de ecuaciones lineales A.X = B
import numpy as np
from sel_metodos_iterativos.pivoteo import pivoteo_parcial

def gauss_jordan(AB: np.ndarray) -> np.ndarray:
  tamano = np.shape(AB)
  n = tamano[0] # número de filas
  m = tamano[1] # número de columnas

  print("\nRealizando eliminación de Gauss-Jordan...")
  for i in range(n):
    # Hacer el elemento diagonal igual a 1
    pivote = AB[i][i] # Elemento diagonal (pivote)
    if pivote == 0:
      raise ValueError("El sistema no tiene solución única (pivote es cero).") # Verificar que el pivote no sea cero para evitar división por cero
    AB[i] = AB[i] / pivote # Normalizar la fila dividiendo por el pivote para hacer el elemento diagonal igual a 1

    # Eliminar los elementos arriba y abajo del pivote
    for j in range(n):
      if i != j: # Omitimos la fila en la que estamos parados (el pivote)
        factor = AB[j][i]
        AB[j] = AB[j] - factor * AB[i]
        print(f"● Eliminando elemento en fila {j+1}, columna {i+1}. Factor = {factor}")
        print(f"    ○ Nueva fila {j+1}: {AB[j]}")

  print("\nMatriz escalonada reducida (Identidad en A):")
  print(AB)

  x = AB[:, m-1]
  return x

print("\n" + "*"*80)
print(" INICIANDO PROCEDIMIENTO DE RESOLUCIÓN DE SISTEMA DE ECUACIONES")

# Ingreso de datos
n = int(input("Ingrese el número de ecuaciones: "))
# Crea un nueva matriz A de tamaño n x n con valores iniciales de 0
A = np.zeros((n, n), dtype=float)
# Crea un nuevo vector B de tamaño n con valores iniciales de 0
B = np.zeros(n, dtype=float)
# Crea vector solución inicial x0 de tamaño n con valores iniciales de 0
x0 = np.zeros(n, dtype=float)

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
  ab = np.hstack((A, B.reshape(-1, 1))) # Combina A y B en una sola matriz

# Método de Gauuss-Jordan
solucion = gauss_jordan(ab)
# Solución final
print('\nX: ',solucion)
print("\n" + "*"*80)