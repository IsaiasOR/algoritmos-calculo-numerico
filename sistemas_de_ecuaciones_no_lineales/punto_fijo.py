"""
Método de Iteración de Punto Fijo para encontrar raíces de ecuaciones no lineales.

Idea: transformar f(x) = 0  →  x = g(x) e iterar  x_{i+1} = g(x_i)  hasta convergencia.

Condición suficiente de convergencia: |g'(x)| ≤ k < 1  en el intervalo.
"""

import math
from collections.abc import Callable


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iter: int = 50,
) -> float:
    """
    Método de Iteración de Punto Fijo: x_{i+1} = g(x_i).

    Parámetros
    ----------
    g          : función de iteración  g(x)  tal que la raíz de f satisface  x = g(x)
    x0         : aproximación inicial
    tolerancia : criterio de parada  |x_{i+1} - x_i|
    max_iter   : número máximo de iteraciones

    Retorna
    -------
    x_nuevo : aproximación de la raíz (punto fijo de g)
    """

    W: int = 75

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" MÉTODO DE ITERACIÓN DE PUNTO FIJO".center(W))
    print("=" * W)
    print(f"  Aproximación inicial : x₀ = {x0}")
    print(f"  Tolerancia           : {tolerancia}")
    print(f"  Iteraciones máx.     : {max_iter}")
    print("=" * W)

    col = (
        f"{'Iter':>5} | {'xᵢ':>14} | {'xᵢ₊₁ = g(xᵢ)':>14} | "
        f"{'|xᵢ₊₁ - xᵢ|':>14} | {'Error rel.':>12}"
    )
    print(col)
    print("-" * W)

    x_actual: float = x0
    convergio: bool = False
    it: int = 0
    error_abs: float = float("inf")
    error_rel: float = float("inf")

    while True:
        it += 1
        x_nuevo = g(x_actual)

        error_abs = abs(x_nuevo - x_actual)
        # Error relativo: evitar división por cero
        error_rel = error_abs / abs(x_nuevo) if abs(x_nuevo) > 1e-15 else float("inf")

        print(
            f"{it:>5} | {x_actual:>14.8f} | {x_nuevo:>14.8f} | "
            f"{error_abs:>14.2e} | {error_rel:>12.2e}"
        )

        # ── Criterio de parada ─────────────────────────────────────────────
        if error_abs <= tolerancia:
            convergio = True
            break

        if it >= max_iter:
            break

        # ── Detección de divergencia ───────────────────────────────────────
        if abs(x_nuevo) > 1e10:
            print("\n  ⚠️  Divergencia detectada: |xᵢ₊₁| creció demasiado.")
            break

        x_actual = x_nuevo

    # ── Mensaje final ──────────────────────────────────────────────────────
    print("-" * W)
    if convergio:
        print(f"  ✅ Convergencia alcanzada en {it} iteración/es.")
        print(f"  ➤  Punto fijo (raíz) : x  = {x_nuevo:.10f}")
        print(f"  ➤  |xᵢ₊₁ - xᵢ|      = {error_abs:.6e}  ≤  tolerancia")
    else:
        print(f"  ⚠️  Límite de iteraciones ({max_iter}) alcanzado sin convergencia.")
        print(f"  ➤  Mejor aproximación: x  = {x_nuevo:.10f}")
        print(f"  ➤  |xᵢ₊₁ - xᵢ|      = {error_abs:.6e}")
        print("  ℹ️  Verificá que |g'(x)| < 1 en el intervalo (condición de convergencia).")
    print("=" * W)

    return x_nuevo


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 75
    print("\n" + "*" * W)
    print(" RESOLUCIÓN POR ITERACIÓN DE PUNTO FIJO".center(W))
    print("*" * W)
    print()
    print("  Reescribí f(x) = 0  como  x = g(x)  e ingresá g(x).")
    print("  Ejemplos:")
    print("    f(x) = x² - 4x + 2  →  g(x) = (x² + 2) / 4")
    print("    f(x) = x³ - x - 1   →  g(x) = (x + 1) ** (1/3)")
    print()
    expr: str = input("  g(x) = ")

    g: Callable[[float], float] = lambda x, _e=expr: eval(
        _e, {"x": x, "math": math, **{k: getattr(math, k) for k in dir(math)}}
    )

    x0: float         = float(input("\n  Aproximación inicial x₀ = "))
    tolerancia: float = float(input("  Tolerancia               = "))
    max_iter: int     = int(input("  Iteraciones máximas      = "))

    raiz = punto_fijo(g, x0, tolerancia=tolerancia, max_iter=max_iter)
    print(f"\n  Punto fijo encontrado: x = {raiz}\n")
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    main()

    # W: int = 75

    # # ── Ejemplo 1 (del PDF): f(x) = x² - 4x + 2  →  g(x) = (x² + 2) / 4
    # #    Raíz exacta: x* ≈ 0.5857864...
    # print("\n" + "─" * W)
    # print("  Ejemplo 1 — f(x) = x² - 4x + 2")
    # print("  Reescritura: g(x) = (x² + 2) / 4  (x₀ = 1)")
    # print("─" * W)
    # g1: Callable[[float], float] = lambda x: (x**2 + 2) / 4
    # punto_fijo(g1, x0=1.0, tolerancia=1e-6, max_iter=30)

    # # ── Ejemplo 2: f(x) = x³ - x - 1  →  g(x) = (x + 1)^(1/3)
    # #    Raíz exacta: x* ≈ 1.3247179...
    # print("\n" + "─" * W)
    # print("  Ejemplo 2 — f(x) = x³ - x - 1")
    # print("  Reescritura: g(x) = (x + 1)^(1/3)  (x₀ = 1.5)")
    # print("─" * W)
    # g2: Callable[[float], float] = lambda x: (x + 1) ** (1 / 3)
    # punto_fijo(g2, x0=1.5, tolerancia=1e-6, max_iter=30)

    # # ── Ejemplo 3 (divergencia intencional): g(x) = x² - x + 1
    # #    |g'(x)| > 1  →  diverge
    # print("\n" + "─" * W)
    # print("  Ejemplo 3 — g(x) = x² - x + 1  (diverge: |g'(x)| ≥ 1)")
    # print("─" * W)
    # g3: Callable[[float], float] = lambda x: x**2 - x + 1
    # punto_fijo(g3, x0=1.5, tolerancia=1e-6, max_iter=15)