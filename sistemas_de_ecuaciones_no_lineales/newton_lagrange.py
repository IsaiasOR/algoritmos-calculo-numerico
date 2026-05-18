"""
Método de la Secante (Newton-Lagrange) para encontrar raíces de ecuaciones no lineales.

Variación de Newton-Raphson que reemplaza la derivada analítica por una diferencia dividida (secante entre dos puntos consecutivos):
    f'(xᵢ) ≈ [f(xᵢ₋₁) - f(xᵢ)] / (xᵢ₋₁ - xᵢ)

Fórmula de recurrencia:
    x_{i+1} = [xᵢ₋₁·f(xᵢ) - xᵢ·f(xᵢ₋₁)] / [f(xᵢ) - f(xᵢ₋₁)]

Requiere dos puntos iniciales x₀ y x₁ (no necesitan encerrar la raíz).
Orden de convergencia ≈ 1.618 (áureo): más lento que Newton pero no requiere f'.
"""

import math
from typing import Any
from collections.abc import Callable


# ─────────────────────────────────────────────────────────────────────────────
#  Entorno de evaluación compartido
# ─────────────────────────────────────────────────────────────────────────────

_ENV: dict[str, Any] = {"math": math, **{k: getattr(math, k) for k in dir(math)}}


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def secante(
    f:          Callable[[float], float],
    x0:         float,
    x1:         float,
    tolerancia: float = 1e-6,
    max_iter:   int   = 50,
) -> float:
    """
    Método de la Secante (Newton-Lagrange).

    Parámetros
    ----------
    f          : función objetivo f(x)
    x0         : primer punto inicial
    x1         : segundo punto inicial
    tolerancia : criterio de parada (error relativo |xᵢ₊₁ - xᵢ| / |xᵢ₊₁|)
    max_iter   : número máximo de iteraciones

    Retorna
    -------
    x_nuevo : aproximación de la raíz encontrada
    """

    W: int = 95

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" MÉTODO DE LA SECANTE (NEWTON-LAGRANGE)".center(W))
    print("=" * W)
    print(f"  Puntos iniciales : x₀ = {x0},  x₁ = {x1}")
    print(f"  Tolerancia       : {tolerancia}")
    print(f"  Iteraciones máx. : {max_iter}")
    print("=" * W)

    col = (
        f"{'Iter':>5} | {'xᵢ₋₁':>13} | {'xᵢ':>13} | "
        f"{'f(xᵢ₋₁)':>13} | {'f(xᵢ)':>13} | {'xᵢ₊₁':>13} | {'|xᵢ₊₁ - xᵢ|':>13}"
    )
    print(col)
    print("-" * W)

    x_prev:    float = x0
    x_actual:  float = x1
    x_nuevo:   float = x1
    error_abs: float = float("inf")
    error_rel: float = float("inf")
    convergio: bool  = False
    it:        int   = 0

    f_prev   = f(x_prev)
    f_actual = f(x_actual)

    while True:
        it += 1

        # ── Guardia: denominador nulo (f(xᵢ) = f(xᵢ₋₁)) ──────────────────
        denom = f_actual - f_prev
        if abs(denom) < 1e-15:
            print(f"\n  ❌  f(xᵢ) - f(xᵢ₋₁) ≈ 0 en la iteración {it}.")
            print("      La secante es horizontal: no se puede calcular xᵢ₊₁.")
            print("      Probá con puntos iniciales distintos.")
            print("=" * W)
            return x_actual

        # ── Fórmula de la secante ──────────────────────────────────────────
        x_nuevo = (x_prev * f_actual - x_actual * f_prev) / denom

        error_abs = abs(x_nuevo - x_actual)
        error_rel = error_abs / abs(x_nuevo) if abs(x_nuevo) > 1e-15 else float("inf")

        print(
            f"{it:>5} | {x_prev:>13.7f} | {x_actual:>13.7f} | "
            f"{f_prev:>13.5e} | {f_actual:>13.5e} | {x_nuevo:>13.7f} | {error_abs:>13.2e}"
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

        # ── Avanzar la ventana deslizante de dos puntos ────────────────────
        x_prev, f_prev     = x_actual, f_actual
        x_actual, f_actual = x_nuevo, f(x_nuevo)

    # ── Resumen final ──────────────────────────────────────────────────────
    print("-" * W)
    if convergio:
        print(f"  ✅ Convergencia alcanzada en {it} iteración/es.")
        print(f"  ➤  Raíz aproximada : x   = {x_nuevo:.10f}")
        print(f"  ➤  f(x)            = {f(x_nuevo):.6e}")
        print(f"  ➤  Error relativo  = {error_rel:.6e}  ≤  tolerancia")
    else:
        print(f"  ⚠️  Límite de iteraciones ({max_iter}) alcanzado sin convergencia.")
        print(f"  ➤  Mejor aproximación: x = {x_nuevo:.10f}")
        print(f"  ➤  f(x)              = {f(x_nuevo):.6e}")
        print("  ℹ️  Probá con puntos iniciales más cercanos a la raíz.")
    print("=" * W)

    return x_nuevo


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 95
    print("\n" + "*" * W)
    print(" RESOLUCIÓN POR EL MÉTODO DE LA SECANTE (NEWTON-LAGRANGE)".center(W))
    print("*" * W)
    print()
    print("  Ingresá f(x) como expresión Python.")
    print("  Ejemplos: x**3 - x - 1  |  math.exp(-x**2) - x  |  x**2 - 4*x + 2")

    expr_f: str = input("\n  f(x) = ")
    f: Callable[[float], float] = lambda x, _e=expr_f: eval(_e, {"x": x, **_ENV})

    print("\nIngresá los dos puntos iniciales x₀ y x₁ (no necesitan encerrar la raíz):")
    x0: float = float(input("  x₀ = "))
    x1: float = float(input("  x₁ = "))

    tolerancia: float = float(input("\n  Tolerancia          = "))
    max_iter:   int   = int(input("  Iteraciones máximas = "))

    raiz = secante(f, x0, x1, tolerancia=tolerancia, max_iter=max_iter)
    print(f"\n  Raíz encontrada: x = {raiz}\n")
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    # main()

    W: int = 95

    # ── Ejemplo 1: f(x) = e^(-x²) - x,  x₀=0, x₁=1
    print("\n" + "─" * W)
    print("  Ejemplo 1 — f(x) = e^(-x²) - x,  x₀ = 0,  x₁ = 1  (del PDF)")
    print("─" * W)
    secante(
        f  = lambda x: math.exp(-x**2) - x,
        x0 = 0.0,
        x1 = 1.0,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 2: f(x) = x² - 4x + 2
    print("\n" + "─" * W)
    print("  Ejemplo 2 — f(x) = x² - 4x + 2,  x₀ = 0,  x₁ = 1")
    print("─" * W)
    secante(
        f  = lambda x: x**2 - 4*x + 2,
        x0 = 0.0,
        x1 = 1.0,
        tolerancia = 1e-8,
    )

    # ── Ejemplo 3: f(x) = x³ - x - 1
    print("\n" + "─" * W)
    print("  Ejemplo 3 — f(x) = x³ - x - 1,  x₀ = 1,  x₁ = 1.5")
    print("─" * W)
    secante(
        f  = lambda x: x**3 - x - 1,
        x0 = 1.0,
        x1 = 1.5,
        tolerancia = 1e-8,
    )