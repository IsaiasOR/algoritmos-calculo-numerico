"""
Método de Regula Falsi (Falsa Posición) para encontrar raíces de funciones no lineales.
Basado en el algoritmo de Mathews & Fink (2004).
"""

import math
from collections.abc import Callable


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def regula_falsi(
    f: Callable[[float], float],
    a: float,
    b: float,
    delta: float = 1e-6,
    epsilon: float = 1e-10,
    max_iter: int = 100,
) -> tuple[float, float, float]:
    """
    Método de Regula Falsi para encontrar una raíz de f en el intervalo [a, b].

    Parámetros
    ----------
    f        : función objetivo f(x)
    a        : extremo izquierdo del intervalo inicial
    b        : extremo derecho del intervalo inicial
    delta    : tolerancia para el cambio en c  (criterio de parada)
    epsilon  : tolerancia para |f(c)|           (criterio de parada)
    max_iter : número máximo de iteraciones

    Retorna
    -------
    c   : aproximación de la raíz encontrada
    err : error estimado  |b - a| / 2
    y_c : f(c) en la última iteración
    """

    # ── Encabezado ─────────────────────────────────────────────────────────
    W: int = 105
    print("\n" + "=" * W)
    print(" MÉTODO DE REGULA FALSI".center(W))
    print("=" * W)
    print(f"  Intervalo inicial : [{a}, {b}]")
    print(f"  Tolerancia (delta)   : {delta}")
    print(f"  Tolerancia (epsilon) : {epsilon}")
    print(f"  Iteraciones máx.     : {max_iter}")
    print("=" * W)

    col: str = (
        f"{'Iter':>5} | {'a':>12} | {'b':>12} | {'c':>12} | "
        f"{'f(a)':>14} | {'f(b)':>14} | {'f(c)':>14} | {'Error':>12}"
    )
    print(col)
    print("-" * W)

    # ── Evaluaciones iniciales ─────────────────────────────────────────────
    y_a: float = f(a)
    y_b: float = f(b)

    # ── Verificación de condición de Bolzano ───────────────────────────────
    if y_a * y_b > 0.0:
        print("\n  ❌ Error: f(a) y f(b) deben tener signos opuestos.")
        print("     Verificá que exista una raíz en el intervalo dado.")
        print("=" * W)
        raise ValueError("f(a) · f(b) > 0: no se garantiza una raíz en [a, b].")

    # Variables de trabajo
    c: float   = a        # se asignará correctamente en la primera iteración
    y_c: float = 0.0
    dx: float  = 0.0
    err: float = 0.0
    convergio: bool = False
    k: int = 0

    for k in range(1, max_iter + 1):

        # ── Fórmula de falsa posición ──────────────────────────────────────
        dx  = y_b * (b - a) / (y_b - y_a)
        c   = b - dx
        ac: float = c - a          # distancia desde a hasta c
        y_c = f(c)

        # ── Error estimado ─────────────────────────────────────────────────
        dx  = min(abs(dx), abs(ac))
        err = abs(b - a) / 2.0

        print(
            f"{k:>5} | {a:>12.6f} | {b:>12.6f} | {c:>12.6f} | "
            f"{y_a:>14.6e} | {y_b:>14.6e} | {y_c:>14.6e} | {err:>12.2e}"
        )

        # ── Criterios de parada ────────────────────────────────────────────
        if y_c == 0.0:
            convergio = True
            break
        if dx < delta:
            convergio = True
            break
        if abs(y_c) < epsilon:
            convergio = True
            break

        # ── Actualizar intervalo ───────────────────────────────────────────
        if y_b * y_c > 0.0:
            b   = c
            y_b = y_c
        else:
            a   = c
            y_a = y_c

    # ── Error final y mensaje de estado ───────────────────────────────────
    err = abs(b - a) / 2.0
    y_c = f(c)

    print("-" * W)
    if convergio:
        print(f"  ✅ Convergencia alcanzada en {k} iteraciones.")
        print(f"  ➤  Raíz aproximada : c   = {c:.10f}")
        print(f"  ➤  Error estimado  : err = {err:.6e}")
        print(f"  ➤  f(c)            = {y_c:.6e}")
    else:
        print(f"  ⚠️  Se alcanzó el límite de iteraciones ({max_iter}) sin converger.")
        print(f"  ➤  Mejor aproximación : c   = {c:.10f}")
        print(f"  ➤  Error estimado     : err = {err:.6e}")
        print(f"  ➤  f(c)               = {y_c:.6e}")
    print("=" * W)

    return c, err, y_c


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "*" * 105)
    print(" RESOLUCIÓN DE RAÍCES POR EL MÉTODO DE REGULA FALSI".center(105))
    print("*" * 105)

    print("\nIngrese la función f(x) como expresión de Python.")
    print("  Ejemplos: x**3 - x - 1   |   math.sin(x) - x/2   |   x**3 - 3*x + 1")
    expr: str = input("  f(x) = ")

    f: Callable[[float], float] = lambda x, _e=expr: eval(_e, {"x": x, "math": math})

    print("\nIngrese los extremos del intervalo [a, b]:")
    a: float = float(input("  a = "))
    b: float = float(input("  b = "))

    delta: float   = float(input("\nIngrese la tolerancia para el cambio en c   (delta): "))
    epsilon: float = float(input("Ingrese la tolerancia para |f(c)|           (epsilon): "))
    max_iter: int  = int(input("Ingrese el número máximo de iteraciones: "))

    c, err, y_c = regula_falsi(f, a, b, delta=delta, epsilon=epsilon, max_iter=max_iter)
    print(f"\n  Raíz encontrada : {c}")
    print(f"  Error estimado  : {err:.6e}")
    print(f"  f(c)            : {y_c:.6e}")
    print("*" * 105)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    # main()

    print("\n" + "─" * 55)
    print("  Ejemplo: f(x) = sen(x) - e**(-x)  en [0.5, 1.0]")
    print("─" * 55)
    f2: Callable[[float], float] = lambda x: math.sin(x) - math.exp(-x)
    regula_falsi(f2, a=0.5, b=1.0, delta=1e-6, epsilon=0.00001, max_iter=10)