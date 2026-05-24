"""
Regresión polinomial por Mínimos Cuadrados.
"""

import math


# ─────────────────────────────────────────────────────────────────────────────
#  Álgebra matricial básica (sin dependencias externas)
# ─────────────────────────────────────────────────────────────────────────────

Matrix = list[list[float]]
Vector = list[float]


def _traspuesta(A: Matrix) -> Matrix:
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def _mat_mul(A: Matrix, B: Matrix) -> Matrix:
    n, m, p = len(A), len(A[0]), len(B[0])
    C = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(m))
    return C


def _mat_vec(A: Matrix, v: Vector) -> Vector:
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _gauss(A: Matrix, b: Vector) -> Vector:
    """Eliminación gaussiana con pivoteo parcial."""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        fila_max = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[fila_max] = M[fila_max], M[col]
        if abs(M[col][col]) < 1e-14:
            raise ValueError(f"Sistema singular en columna {col}.")
        for fila in range(col + 1, n):
            f = M[fila][col] / M[col][col]
            for j in range(col, n + 1):
                M[fila][j] -= f * M[col][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


# ─────────────────────────────────────────────────────────────────────────────
#  Polinomio
# ─────────────────────────────────────────────────────────────────────────────

def _evaluar(coefs: Vector, x: float) -> float:
    resultado = 0.0
    for c in reversed(coefs):
        resultado = resultado * x + c
    return resultado


def _formatear(coefs: Vector, dec: int = 6) -> str:
    terminos: list[str] = []
    for grado, c in enumerate(coefs):
        if abs(c) < 1e-12:
            continue
        cf = f"{c:.{dec}f}"
        terminos.append(cf if grado == 0 else (f"{cf}·x" if grado == 1 else f"{cf}·x^{grado}"))
    if not terminos:
        return "0"
    s = terminos[0]
    for t in terminos[1:]:
        s += f"  -  {t[1:]}" if t.startswith("-") else f"  +  {t}"
    return s


# ─────────────────────────────────────────────────────────────────────────────
#  Presentación de matrices
# ─────────────────────────────────────────────────────────────────────────────

def _mat_print(M: Matrix, etiqueta: str, dec: int = 4) -> None:
    ancho = max(len(f"{v:.{dec}f}") for fila in M for v in fila) + 2
    print(f"\n  {etiqueta}")
    for fila in M:
        print("  │ " + "  ".join(f"{v:>{ancho}.{dec}f}" for v in fila) + " │")


def _vec_print(v: Vector, etiqueta: str, dec: int = 4) -> None:
    ancho = max(len(f"{x:.{dec}f}") for x in v) + 2
    print(f"\n  {etiqueta}")
    for val in v:
        print(f"  │ {val:>{ancho}.{dec}f} │")


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def minimos_cuadrados(xs: Vector, ys: Vector, m: int) -> Vector:
    """
    Calcula el polinomio de mínimos cuadrados de grado m.

    Parámetros
    ----------
    xs : abscisas
    ys : ordenadas
    m  : grado del polinomio  (m ≤ n = len(xs) - 1)

    Retorna
    -------
    coefs : [a₀, a₁, …, aₘ]
    """

    n  = len(xs) - 1
    W: int = 72

    if m > n:
        raise ValueError(f"El grado m={m} no puede superar n={n}.")

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" REGRESIÓN POLINOMIAL — MÍNIMOS CUADRADOS".center(W))
    print("=" * W)
    print(f"  Puntos : {n + 1}")
    print(f"  Grado  : m = {m}  →  P(x) = a₀ + a₁x + … + a{m}x^{m}")
    if m == n:
        print("  ⚠️  m = n: el polinomio pasa exactamente por todos los puntos (ε = 0).")
    print("=" * W)

    # ── 1) Vandermonde y sistema normal ────────────────────────────────────
    A: Matrix = [[xi ** j for j in range(m + 1)] for xi in xs]
    At  = _traspuesta(A)
    AtA = _mat_mul(At, A)
    Aty = _mat_vec(At, ys)

    print("\n  ── MATRIZ  A  ({} × {}) ─────────────────────".format(n+1, m+1))
    _mat_print(A, f"A  ({n+1} × {m+1})")

    print("\n  ── SISTEMA NORMAL   (AᵀA)·a = Aᵀy ────────────────────────")
    _mat_print(AtA, f"AᵀA  ({m+1} × {m+1})")
    _vec_print(Aty, "Aᵀy")

    # ── 2) Resolución ──────────────────────────────────────────────────────
    coefs = _gauss([fila[:] for fila in AtA], Aty[:])

    print("\n  ── SOLUCIÓN ────────────────────────────────────────────────")
    _vec_print(coefs, "a  =  (AᵀA)⁻¹ · Aᵀy")

    # ── 3) Polinomio ───────────────────────────────────────────────────────
    print("\n" + "-" * W)
    print("  Polinomio de ajuste:\n")
    poly_str = _formatear(coefs)
    if len(poly_str) > W - 10:
        partes = poly_str.split("  +  ")
        print(f"  P(x) = {partes[0]}")
        for p in partes[1:]:
            print(f"         +  {p}")
    else:
        print(f"  P(x) = {poly_str}")

    # ── 4) Tabla de errores ────────────────────────────────────────────────
    print("\n  ── TABLA DE ERRORES ────────────────────────────────────────")
    print(f"\n  {'i':>4}  {'xᵢ':>8}  {'yᵢ':>10}  {'P(xᵢ)':>12}  {'yᵢ-P(xᵢ)':>12}  {'[yᵢ-P(xᵢ)]²':>14}")
    print("  " + "─" * 66)

    epsilon = 0.0
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        pxi  = _evaluar(coefs, xi)
        diff = yi - pxi
        sq   = diff ** 2
        epsilon += sq
        print(f"  {i:>4}  {xi:>8.4f}  {yi:>10.4f}  {pxi:>12.6f}  {diff:>12.6f}  {sq:>14.6f}")

    e_rms = math.sqrt(epsilon / (n + 1))
    print("  " + "─" * 66)
    print(f"  {'':>48}  ε  = {epsilon:.6f}")
    print()
    print(f"  ε     = {epsilon:.6f}")
    print(f"  E_RMS = √(ε / {n+1}) = {e_rms:.6f}")
    print("=" * W)

    return coefs


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 72
    print("\n" + "*" * W)
    print(" REGRESIÓN POLINOMIAL — MÍNIMOS CUADRADOS".center(W))
    print("*" * W)
    print("\n  Ingresá los puntos (xᵢ yᵢ). Escribí 'fin' para terminar.")

    xs: Vector = []
    ys: Vector = []
    while True:
        entrada = input(f"  Punto {len(xs)}: ").strip()
        if entrada.lower() == "fin":
            break
        try:
            partes = entrada.split()
            xs.append(float(partes[0]))
            ys.append(float(partes[1]))
        except (ValueError, IndexError):
            print("  Formato inválido. Ingresá dos números: x y")

    if len(xs) < 2:
        print("  Se necesitan al menos 2 puntos.")
        return

    m = int(input(f"\n  Grado del polinomio (1 a {len(xs)-1}): "))
    minimos_cuadrados(xs, ys, m)
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    main()

    W: int = 72
    xs_ej = [0.0, 2.0, 3.0, 5.0]
    ys_ej = [-1.0, 0.0, 2.0, 1.0]

    # print("\n" + "─" * W)
    # print("  Ejemplo — Recta de mínimos cuadrados  (m = 1)")
    # print("─" * W)
    # minimos_cuadrados(xs_ej, ys_ej, m=1)

    # print("\n" + "─" * W)
    # print("  Ejemplo — Parábola de mínimos cuadrados  (m = 2)")
    # print("─" * W)
    # minimos_cuadrados(xs_ej, ys_ej, m=2)