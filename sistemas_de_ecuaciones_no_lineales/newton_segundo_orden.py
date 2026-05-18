"""
Método de Newton de Segundo Orden para encontrar raíces de ecuaciones no lineales.

Toma los tres primeros términos de la serie de Taylor (incluye f''):
    f(x_i) + Δxᵢ · [f'(xᵢ) - f(xᵢ)·f''(xᵢ) / (2·f'(xᵢ))] = 0

Despejando Δxᵢ:
    Δxᵢ = -f(xᵢ) / [f'(xᵢ) - f(xᵢ)·f''(xᵢ) / (2·f'(xᵢ))]

Fórmula de recurrencia:
    x_{i+1} = xᵢ - f(xᵢ) / [f'(xᵢ) - f(xᵢ)·f''(xᵢ) / (2·f'(xᵢ))]

Converge más rápidamente que Newton-Raphson al considerar más términos de la serie.
"""

import math
from collections.abc import Callable
from typing import Any


# ─────────────────────────────────────────────────────────────────────────────
#  Derivadas numéricas (respaldo cuando el usuario no las provee)
# ─────────────────────────────────────────────────────────────────────────────

def _primera_derivada(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    """Diferencia centrada de orden 2: f'(x) ≈ [f(x+h) - f(x-h)] / (2h)."""
    return (f(x + h) - f(x - h)) / (2 * h)


def _segunda_derivada(f: Callable[[float], float], x: float, h: float = 1e-4) -> float:
    """Diferencia centrada de orden 2: f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h²."""
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def newton_segundo_orden(
    f:   Callable[[float], float],
    x0:  float,
    df:  Callable[[float], float] | None = None,
    d2f: Callable[[float], float] | None = None,
    tolerancia: float = 1e-6,
    max_iter:   int   = 50,
) -> float:
    """
    Método de Newton de Segundo Orden.

    Parámetros
    ----------
    f          : función objetivo f(x)
    x0         : aproximación inicial
    df         : primera derivada f'(x).  None → derivada numérica.
    d2f        : segunda derivada f''(x). None → derivada numérica.
    tolerancia : criterio de parada (error relativo |xᵢ₊₁ - xᵢ| / |xᵢ₊₁|)
    max_iter   : número máximo de iteraciones

    Retorna
    -------
    x_nuevo : aproximación de la raíz
    """

    # ── Derivadas numéricas como respaldo ──────────────────────────────────
    modo_df  = "analítica" if df  is not None else "numérica"
    modo_d2f = "analítica" if d2f is not None else "numérica"
    if df  is None: df  = lambda x: _primera_derivada(f, x)
    if d2f is None: d2f = lambda x: _segunda_derivada(f, x)

    W: int = 95

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" MÉTODO DE NEWTON DE SEGUNDO ORDEN".center(W))
    print("=" * W)
    print(f"  Aproximación inicial : x₀ = {x0}")
    print(f"  Tolerancia           : {tolerancia}")
    print(f"  Iteraciones máx.     : {max_iter}")
    print(f"  f'(x)                : {modo_df}")
    print(f"  f''(x)               : {modo_d2f}")
    print("=" * W)

    col = (
        f"{'Iter':>5} | {'xᵢ':>12} | {'f(xᵢ)':>12} | "
        f"{'f\'(xᵢ)':>12} | {'f\'\'(xᵢ)':>12} | {'Δxᵢ':>12} | {'xᵢ₊₁':>12}"
    )
    print(col)
    print("-" * W)

    x_actual:  float = x0
    x_nuevo:   float = x0
    error_abs: float = float("inf")
    error_rel: float = float("inf")
    convergio: bool  = False
    it:        int   = 0

    while True:
        it += 1
        fx   = f(x_actual)
        dfx  = df(x_actual)
        d2fx = d2f(x_actual)

        # ── Guardia: f'(xᵢ) = 0 ──────────────────────────────────────────
        if abs(dfx) < 1e-15:
            print(f"\n  ❌  f'(xᵢ) ≈ 0 en la iteración {it}  →  denominador singular.")
            print("      Probá con un x₀ distinto o verificá si la raíz es múltiple.")
            print("=" * W)
            return x_actual

        # ── Paso de Newton de 2° orden ────────────────────────────────────
        #   denominador = f'(xᵢ) - [f(xᵢ) / f'(xᵢ)] · f''(xᵢ) / 2
        denominador = dfx - (fx / dfx) * d2fx / 2.0

        # ── Guardia: denominador ≈ 0 ──────────────────────────────────────
        if abs(denominador) < 1e-15:
            print(f"\n  ❌  Denominador ≈ 0 en la iteración {it}.")
            print("      f'(xᵢ)² ≈ f(xᵢ)·f''(xᵢ)/2  →  el método no puede continuar.")
            print("=" * W)
            return x_actual

        delta_x = -fx / denominador
        x_nuevo = x_actual + delta_x

        error_abs = abs(delta_x)
        error_rel = error_abs / abs(x_nuevo) if abs(x_nuevo) > 1e-15 else float("inf")

        print(
            f"{it:>5} | {x_actual:>12.7f} | {fx:>12.4e} | "
            f"{dfx:>12.4e} | {d2fx:>12.4e} | {delta_x:>12.4e} | {x_nuevo:>12.7f}"
        )

        # ── Criterio de parada ─────────────────────────────────────────────
        if error_rel <= tolerancia:
            convergio = True
            break

        if it >= max_iter:
            break

        if abs(x_nuevo) > 1e12:
            print("\n  ⚠️  Divergencia detectada: |xᵢ₊₁| creció demasiado.")
            break

        x_actual = x_nuevo

    # ── Resumen final ──────────────────────────────────────────────────────
    print("-" * W)
    if convergio:
        print(f"  ✅ Convergencia alcanzada en {it} iteración/es.")
        print(f"  ➤  Raíz aproximada : x    = {x_nuevo:.10f}")
        print(f"  ➤  f(x)            = {f(x_nuevo):.6e}")
        print(f"  ➤  |Δxᵢ|           = {error_abs:.6e}  (error absoluto del último paso)")
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

_ENV: dict[str, Any] = {"math": math, **{k: getattr(math, k) for k in dir(math)}}


def main() -> None:
    W: int = 95
    print("\n" + "*" * W)
    print(" RESOLUCIÓN POR EL MÉTODO DE NEWTON DE SEGUNDO ORDEN".center(W))
    print("*" * W)
    print()
    print("  Ejemplo: f(x) = x**3 - x - 1  |  f'(x) = 3*x**2 - 1  |  f''(x) = 6*x")

    expr_f: str = input("\n  f(x)   = ")
    f: Callable[[float], float] = lambda x, _e=expr_f: eval(_e, {"x": x, **_ENV})

    print("  (Dejá en blanco para usar derivadas numéricas automáticas)")
    expr_df: str  = input("  f'(x)  = ").strip()
    expr_d2f: str = input("  f''(x) = ").strip()

    df:  Callable[[float], float] | None = (lambda x, _e=expr_df:  eval(_e, {"x": x, **_ENV})) if expr_df  else None
    d2f: Callable[[float], float] | None = (lambda x, _e=expr_d2f: eval(_e, {"x": x, **_ENV})) if expr_d2f else None

    x0:         float = float(input("\n  Aproximación inicial x₀ = "))
    tolerancia: float = float(input("  Tolerancia               = "))
    max_iter:   int   = int(input("  Iteraciones máximas      = "))

    raiz = newton_segundo_orden(f, x0, df=df, d2f=d2f,
                                tolerancia=tolerancia, max_iter=max_iter)
    print(f"\n  Raíz encontrada: x = {raiz}\n")
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    # main()

    W: int = 95

    # ── Ejemplo 1: f(x) = x² - 4x + 2, x₀ = 1
    print("\n" + "─" * W)
    print("  Ejemplo 1 — f(x) = x² - 4x + 2,  f'(x) = 2x - 4,  f''(x) = 2,  x₀ = 1")
    print("─" * W)
    newton_segundo_orden(
        f   = lambda x: x**2 - 4*x + 2,
        df  = lambda x: 2*x - 4,
        d2f = lambda x: 2.0,
        x0  = 1.0,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 2: f(x) = x³ - x - 1, x₀ = 1.5
    print("\n" + "─" * W)
    print("  Ejemplo 2 — f(x) = x³ - x - 1,  f'(x) = 3x² - 1,  f''(x) = 6x,  x₀ = 1.5")
    print("─" * W)
    newton_segundo_orden(
        f   = lambda x: x**3 - x - 1,
        df  = lambda x: 3*x**2 - 1,
        d2f = lambda x: 6*x,
        x0  = 1.5,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 3: derivadas numéricas automáticas
    print("\n" + "─" * W)
    print("  Ejemplo 3 — f(x) = e^(-x²) - x  (derivadas numéricas)")
    print("─" * W)
    newton_segundo_orden(
        f  = lambda x: math.exp(-x**2) - x,
        x0 = 0.5,
        tolerancia = 1e-8,
    )