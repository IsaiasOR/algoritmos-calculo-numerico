"""
Método de Newton-Raphson (de la tangente) para encontrar raíces de ecuaciones no lineales.

Fórmula de recurrencia:
    x_{i+1} = x_i - f(x_i) / f'(x_i)

Convergencia cuadrática: |x_{i+1} - x*| ≤ C · |x_i - x*|²
"""

import math
from collections.abc import Callable
from typing import Any, Dict


# ─────────────────────────────────────────────────────────────────────────────
#  Derivada numérica (respaldo si el usuario no ingresa f')
# ─────────────────────────────────────────────────────────────────────────────

def _derivada_numerica(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-7,
) -> float:
    """Diferencia centrada de orden 2: f'(x) ≈ [f(x+h) - f(x-h)] / (2h)."""
    return (f(x + h) - f(x - h)) / (2 * h)


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def newton_raphson(
    f: Callable[[float], float],
    x0: float,
    df: Callable[[float], float] | None = None,
    tolerancia: float = 1e-6,
    max_iter: int = 50,
) -> float:
    """
    Método de Newton-Raphson para encontrar una raíz de f.

    Parámetros
    ----------
    f          : función objetivo f(x)
    x0         : aproximación inicial
    df         : derivada f'(x). Si es None, se usa diferenciación numérica.
    tolerancia : criterio de parada para el error relativo |x_{i+1} - x_i| / |x_{i+1}|
    max_iter   : número máximo de iteraciones

    Retorna
    -------
    x_nuevo : aproximación de la raíz encontrada
    """

    usa_derivada_numerica = df is None
    if usa_derivada_numerica:
        df = lambda x: _derivada_numerica(f, x)

    W: int = 85

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" MÉTODO DE NEWTON-RAPHSON".center(W))
    print("=" * W)
    print(f"  Aproximación inicial : x₀ = {x0}")
    print(f"  Tolerancia           : {tolerancia}")
    print(f"  Iteraciones máx.     : {max_iter}")
    if usa_derivada_numerica:
        print("  Derivada             : numérica (diferencia centrada)")
    else:
        print("  Derivada             : analítica (provista por el usuario)")
    print("=" * W)

    col = (
        f"{'Iter':>5} | {'xᵢ':>13} | {'f(xᵢ)':>13} | "
        f"{'f\'(xᵢ)':>13} | {'xᵢ₊₁':>13} | {'|xᵢ₊₁ - xᵢ|':>13}"
    )
    print(col)
    print("-" * W)

    x_actual: float = x0
    x_nuevo: float  = x0
    error_abs: float = float("inf")
    convergio: bool  = False
    it: int          = 0

    while True:
        it += 1
        fx  = f(x_actual)
        dfx = df(x_actual)

        # ── Derivada nula: singularidad ────────────────────────────────────
        if abs(dfx) < 1e-15:
            print(f"\n  ❌  f'(xᵢ) ≈ 0 en la iteración {it}  →  división imposible.")
            print("      El método diverge o la raíz es múltiple.")
            print("=" * W)
            return x_actual

        x_nuevo   = x_actual - fx / dfx
        error_abs = abs(x_nuevo - x_actual)
        error_rel = error_abs / abs(x_nuevo) if abs(x_nuevo) > 1e-15 else float("inf")

        print(
            f"{it:>5} | {x_actual:>13.7f} | {fx:>13.6e} | "
            f"{dfx:>13.6e} | {x_nuevo:>13.7f} | {error_abs:>13.2e}"
        )

        # ── Criterio de parada ─────────────────────────────────────────────
        if error_rel <= tolerancia:
            convergio = True
            break

        if it >= max_iter:
            break

        # ── Detección de divergencia ───────────────────────────────────────
        if abs(x_nuevo) > 1e12:
            print("\n  ⚠️  Divergencia detectada: |xᵢ₊₁| creció demasiado.")
            break

        x_actual = x_nuevo

    # ── Resumen final ──────────────────────────────────────────────────────
    print("-" * W)
    if convergio:
        print(f"  ✅ Convergencia cuadrática en {it} iteración/es.")
        print(f"  ➤  Raíz aproximada : x   = {x_nuevo:.10f}")
        print(f"  ➤  f(x)            = {f(x_nuevo):.6e}")
        print(f"  ➤  Error relativo  = {error_rel:.6e}  ≤  tolerancia")
    else:
        print(f"  ⚠️  Límite de iteraciones ({max_iter}) alcanzado sin convergencia.")
        print(f"  ➤  Mejor aproximación: x = {x_nuevo:.10f}")
        print(f"  ➤  f(x)              = {f(x_nuevo):.6e}")
        print("  ℹ️  Probá con un x₀ más cercano a la raíz.")
    print("=" * W)

    return x_nuevo


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

_ENV: Dict[str, Any] = {"math": math, **{k: getattr(math, k) for k in dir(math)}}

def main() -> None:
    W: int = 85
    print("\n" + "*" * W)
    print(" RESOLUCIÓN POR EL MÉTODO DE NEWTON-RAPHSON".center(W))
    print("*" * W)
    print()
    print("  Ejemplos de f(x): x**3 - x - 1  |  x**2 - 4*x + 2  |  math.exp(-x) - x")

    expr_f: str = input("\n  f(x)  = ")
    f: Callable[[float], float] = lambda x, _e=expr_f: eval(_e, {"x": x, **_ENV})

    print("  (Dejá en blanco para usar derivada numérica automática)")
    expr_df: str = input("  f\'(x) = ").strip()

    if expr_df:
        df: Callable[[float], float] | None = (
            lambda x, _e=expr_df: eval(_e, {"x": x, **_ENV})
        )
    else:
        df = None

    x0: float         = float(input("\n  Aproximación inicial x₀ = "))
    tolerancia: float = float(input("  Tolerancia               = "))
    max_iter: int     = int(input("  Iteraciones máximas      = "))

    raiz = newton_raphson(f, x0, df=df, tolerancia=tolerancia, max_iter=max_iter)
    print(f"\n  Raíz encontrada: x = {raiz}\n")
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    # main()

    W: int = 85

    # ── Ejemplo 1: f(x) = x² - 4x + 2, x₀ = 1
    #    f'(x) = 2x - 4     Raíz exacta: x* ≈ 0.5857864...
    print("\n" + "─" * W)
    print("  Ejemplo 1 — f(x) = x² - 4x + 2,  f'(x) = 2x - 4,  x₀ = 1")
    print("─" * W)
    newton_raphson(
        f  = lambda x: x**2 - 4*x + 2,
        df = lambda x: 2*x - 4,
        x0 = 1.0,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 2: f(x) = x³ - x - 1
    #    f'(x) = 3x² - 1     Raíz exacta: x* ≈ 1.3247179...
    print("\n" + "─" * W)
    print("  Ejemplo 2 — f(x) = x³ - x - 1,  f'(x) = 3x² - 1,  x₀ = 1.5")
    print("─" * W)
    newton_raphson(
        f  = lambda x: x**3 - x - 1,
        df = lambda x: 3*x**2 - 1,
        x0 = 1.5,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 3: derivada numérica automática
    print("\n" + "─" * W)
    print("  Ejemplo 3 — f(x) = e^(-x²) - x  (derivada numérica)")
    print("─" * W)
    newton_raphson(
        f  = lambda x: math.exp(-x**2) - x,
        x0 = 0.5,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 4: raíz múltiple → convergencia lineal
    #    f(x) = (x - 1)²,  raíz doble en x* = 1
    print("\n" + "─" * W)
    print("  Ejemplo 4 — f(x) = (x-1)²  (raíz doble: convergencia lineal)")
    print("─" * W)
    newton_raphson(
        f  = lambda x: (x - 1)**2,
        df = lambda x: 2*(x - 1),
        x0 = 2.0,
        tolerancia = 1e-8,
    )