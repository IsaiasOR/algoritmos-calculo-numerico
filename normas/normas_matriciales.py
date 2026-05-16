"""
Normas matriciales
La norma es una medida que asigna un valor real positivo a una matriz,
indicando su "tamaño" o "magnitud".
"""


# ─────────────────────────────────────────────────────────────────────────────
#  Normas
# ─────────────────────────────────────────────────────────────────────────────

# Norma-1 / columna-suma: máximo de las sumas de valores absolutos por columna.
def norma_columna_suma(A: list[list[float]]) -> float:
    cols = len(A[0])
    return max(sum(abs(A[i][j]) for i in range(len(A))) for j in range(cols))


# Norma-∞ / fila-suma: máximo de las sumas de valores absolutos por fila.
def norma_fila_suma(A: list[list[float]]) -> float:
    return max(sum(abs(x) for x in fila) for fila in A)


# Norma de Frobenius: raíz cuadrada de la suma de los cuadrados de todos los elementos.
def norma_frobenius(A: list[list[float]]) -> float:
    return sum(x**2 for fila in A for x in fila) ** 0.5


# ─────────────────────────────────────────────────────────────────────────────
#  Presentación
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_normas(A: list[list[float]]) -> None:
    """Calcula y muestra las tres normas de una matriz con formato de tabla."""

    W: int = 75
    filas, cols = len(A), len(A[0])

    n1  = norma_columna_suma(A)
    ninf = norma_fila_suma(A)
    nf  = norma_frobenius(A)

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" NORMAS MATRICIALES".center(W))
    print("=" * W)

    # ── Matriz (una fila por línea) ─────────────────────────────────────────
    print(f"  Matriz ({filas} × {cols})\n")
    for i, fila in enumerate(A):
        nums = "  ".join(f"{x:>8.4f}" for x in fila)
        bracket_izq = "⎡" if i == 0 else ("⎣" if i == filas - 1 else "⎢")
        bracket_der = "⎤" if i == 0 else ("⎦" if i == filas - 1 else "⎥")
        print(f"  {bracket_izq} {nums} {bracket_der}")
    print("-" * W)

    # ── Tabla de resultados ────────────────────────────────────────────────
    print(f"  {'Norma':<28} {'Símbolo':^8} {'Valor':>14}  {'Fórmula'}")
    print("-" * W)
    print(f"  {'Columna-suma  (L¹)':<28} {'‖A‖₁':^8} {n1:>14.6f}  max_j Σᵢ |aᵢⱼ|")
    print(f"  {'Fila-suma  (L∞)':<28} {'‖A‖∞':^8} {ninf:>14.6f}  max_i Σⱼ |aᵢⱼ|")
    print(f"  {'Frobenius':<28} {'‖A‖_F':^8} {nf:>14.6f}  √(Σᵢⱼ aᵢⱼ²)")
    print("=" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 75
    print("\n" + "*" * W)
    print(" CÁLCULO DE NORMAS MATRICIALES".center(W))
    print("*" * W)
    print("\nIngresá cada fila separada por ';' y los elementos por espacios.")
    print("  Ejemplo: 1 2 3 ; 4 5 6 ; 7 8 9")

    raw = input("\n  A = ")
    rows = raw.split(";")
    A: list[list[float]] = [[float(x) for x in row.split()] for row in rows]

    mostrar_normas(A)
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    main()

    # W: int = 75
    # print("\n" + "─" * W)
    # print("  Ejemplo: A = [[3, -4, 5], [1, 2, 3], [0, -1, 4]]")
    # print("─" * W)
    # mostrar_normas([[3, -4, 5], [1, 2, 3], [0, -1, 4]])