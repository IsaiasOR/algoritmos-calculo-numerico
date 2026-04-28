import numpy as np

def pivoteo_parcial(A: np.ndarray, B: np.ndarray) -> np.ndarray:
  # Pivoteo parcial por filas, entrega matriz aumentada AB
  # Si hay ceros en diagonal es matriz singular, se devuelve None
  # Revisa si la diagonal tiene ceros, si es así, busca una fila debajo que no tenga cero en esa columna y las intercambia

  print("\n" + "-"*70)
  print(" INICIANDO MÉTODO DE PIVOTEO PARCIAL")
  print("-"*70)

  # Matriz aumentada
  AB = np.hstack((A, B.reshape(-1, 1)))

  print("\nMatriz aumentada:")
  print(AB)

  # Pivoteo parcial por filas
  print("\nPivoteo parcial por filas:")
  tamano = np.shape(AB)
  n = tamano[0] # Número de filas
  pivoteado = 0

  for i in range(0, n-1, 1): # Para cada fila en AB, excepto la última
    max_index = np.argmax(np.abs(AB[i:, i])) + i # Encuentra el índice de la fila con el valor absoluto máximo en la columna i desde la fila i hacia abajo
    if AB[max_index][i] == 0: # Si el valor máximo es cero, la matriz es singular
      print(f"Matriz singular, no se puede pivotear en la columna {i+1}")
      return AB # Devuelve la matriz aumentada sin modificar
    if max_index != i: # Si el índice de la fila con el valor máximo no es la fila actual, intercambia las filas
      AB[[i, max_index]] = AB[[max_index, i]]
      pivoteado += 1
      print(f"Intercambio de filas {i+1} y {max_index+1}:")
      print(AB)

  if pivoteado == 0:
    print("No se realizaron intercambios, la matriz ya estaba en orden.")
  else:
    print(f"\nTotal de intercambios realizados: {pivoteado}")
    print("Matriz aumentada después del pivoteo parcial:")
    print(AB)
  return AB