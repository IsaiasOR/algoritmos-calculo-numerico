# Método de Jacobi
import numpy as np
from pivoteo import pivoteo_parcial

# 1. Configuración global para que NumPy imprima bonito
np.set_printoptions(precision=5, suppress=True, linewidth=100)

def jacobi(A: np.ndarray, B: np.ndarray, x0: np.ndarray, tolerancia: float, max_iteraciones: int) -> np.ndarray:
  # Método de Jacobi para resolver Ax = B

  tamano = np.shape(A)
  n = tamano[0] # número de filas

  # Valores inciales
  diferencia = 2 * tolerancia * np.ones(n, dtype=float)
  errado = 2 * tolerancia
  tabla = [np.copy(x0)] # tabla de iteraciones, inicia con la aproximación inicial

  # 2. Encabezado tabular con f-strings y separadores
  print("\n" + "="*70)
  print(" INICIANDO MÉTODO DE JACOBI")
  print("="*70)
  print(f"{'Iteración':<10} | {'Aproximación [X]':<35} | {'Error Máx.':<12}")
  print("-" * 70)

  # Imprimir iteración 0 convirtiendo el array a un string limpio
  x0_str = np.array2string(x0, separator=', ')
  print(f"{0:<10} | {x0_str:<35} | {'-':<12}")

  iteracion = 0
  x = np.copy(x0)
  x_nuevo = np.copy(x0)

  while errado > tolerancia and iteracion < max_iteraciones:
    for i in range(n):
      suma = np.dot(A[i], x) - A[i][i] * x[i] # suma de los productos de los coeficientes y las aproximaciones actuales, excluyendo el término diagonal
      x_nuevo[i] = (B[i] - suma) / A[i][i] # nueva aproximación para la variable i

    diferencia = np.abs(x_nuevo - x) # diferencia entre la nueva aproximación y la anterior
    errado = np.linalg.norm(diferencia, ord=np.inf) # norma infinito de la diferencia como criterio de error
    tabla.append(np.copy(x_nuevo)) # agregar la nueva aproximación a la tabla de iteraciones

    # 3. Impresión formateada por cada fila
    x_nuevo_str = np.array2string(x_nuevo, separator=', ')
    print(f"{iteracion + 1:<10} | {x_nuevo_str:<35} | {errado:<12.5f}")

    x = np.copy(x_nuevo) # actualizar la aproximación actual para la siguiente iteración
    iteracion += 1

  print("-" * 70)
  if iteracion == max_iteraciones:
    print(f"⚠️ Se alcanzó el número máximo de iteraciones ({max_iteraciones}) sin converger.")
  else:
    print(f"✅ Convergencia alcanzada exitosamente en {iteracion} iteraciones.")
  print("="*70)
  return x_nuevo


print("\n" + "*"*80)
print(" INICIANDO PROCEDIMIENTO DE RESOLUCIÓN DE SISTEMA DE ECUACIONES")

# Ingreso de datos
n = int(input("\nIngrese el número de ecuaciones: "))
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
  AB = pivoteo_parcial(A, B)
  n, m = np.shape(AB)
  a_nuevo = AB[:,:n] # Separa en A y B
  b_nuevo = AB[:,n]
else:
  a_nuevo = A
  b_nuevo = B

print("\nIngrese la aproximación inicial:")
for i in range(n):
  x0[i] = float(input(f"x0[{i+1}]: "))

print("\nVector solución inicial:")
print(x0)

tolerancia = float(input("\nIngrese la tolerancia: "))
max_iteraciones = int(input("Ingrese el número máximo de iteraciones: "))

# Método de Jacobi
solucion = jacobi(a_nuevo, b_nuevo, x0, tolerancia, max_iteraciones)
# Solución final
print('X: ',solucion)
print("\n" + "*"*80)