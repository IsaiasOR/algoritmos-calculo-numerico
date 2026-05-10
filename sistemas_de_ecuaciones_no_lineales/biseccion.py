"""
Método de Bisección para encontrar raíces de funciones no lineales.
Basado en bisec_n de S. Nakamura (1995).
"""

import math
from collections.abc import Callable


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def biseccion(
    f: Callable[[float], float],
    a: float,
    c: float,
    tolerancia: float = 1e-6,
    max_iter: int = 30,
) -> float:
    """
    Método de Bisección para encontrar una raíz de f en el intervalo [a, c].

    Parámetros
    ----------
    f          : función objetivo f(x)
    a          : extremo izquierdo del intervalo inicial
    c          : extremo derecho del intervalo inicial
    tolerancia : criterio de parada para |c - a|
    max_iter   : número máximo de iteraciones

    Retorna
    -------
    b : aproximación de la raíz encontrada
    """

    # ── Encabezado ─────────────────────────────────────────────────────────
    W: int = 95
    print("\n" + "=" * W)
    print(" MÉTODO DE BISECCIÓN".center(W))
    print("=" * W)
    print(f"  Intervalo inicial : [{a}, {c}]")
    print(f"  Tolerancia        : {tolerancia}")
    print(f"  Iteraciones máx.  : {max_iter}")
    print("=" * W)

    col: str = (
        f"{'Iter':>5} | {'a':>12} | {'b':>12} | {'c':>12} | "
        f"{'f(a)':>14} | {'f(b)':>14} | {'f(c)':>14}"
    )
    print(col)
    print("-" * W)

    # ── Evaluaciones iniciales ─────────────────────────────────────────────
    y_a: float = f(a)
    y_c: float = f(c)

    # ── Verificación de condición de Bolzano ───────────────────────────────
    if y_a * y_c > 0.0:
        print("\n  ❌ Error: f(a) y f(c) deben tener signos opuestos.")
        print("     Verificá que exista una raíz en el intervalo dado.")
        print("=" * W)
        raise ValueError("f(a) · f(c) > 0: no se garantiza una raíz en [a, c].")

    b: float = a                  # se inicializa; se asignará en la primera iteración
    y_b: float = 0.0
    convergio: bool = False
    it: int = 0

    while True:
        it += 1
        b   = (a + c) / 2.0
        y_b = f(b)

        print(
            f"{it:>5} | {a:>12.6f} | {b:>12.6f} | {c:>12.6f} | "
            f"{y_a:>14.6e} | {y_b:>14.6e} | {y_c:>14.6e}"
        )

        # ── Criterios de parada ────────────────────────────────────────────
        if abs(f(b)) <= tolerancia:
            convergio = True
            break

        if it >= max_iter:
            break

        # ── Actualizar intervalo ───────────────────────────────────────────
        if y_a * y_b <= 0.0:
            c   = b
            y_c = y_b
        else:
            a   = b
            y_a = y_b

    # ── Mensaje final ──────────────────────────────────────────────────────
    print("-" * W)
    if convergio:
        print(f"  ✅ Tolerancia satisfecha en {it} iteraciones.")
        print(f"  ➤  Raíz aproximada : b  = {b:.10f}")
        print(f"  ➤  f(b)            = {y_b:.6e}")
    else:
        print(f"  ⚠️  Se alcanzó el límite de iteraciones ({max_iter}) sin converger.")
        print(f"  ➤  Mejor aproximación : b = {b:.10f}")
        print(f"  ➤  f(b)               = {y_b:.6e}")
    print("=" * W)

    return b


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "*" * 95)
    print(" RESOLUCIÓN DE RAÍCES POR EL MÉTODO DE BISECCIÓN".center(95))
    print("*" * 95)

    print("\nIngrese la función f(x) como expresión de Python.")
    print("  Ejemplos: x**3 - x - 1   |   math.sin(x) - x/2   |   x**3 - 3*x + 1")
    expr: str = input("  f(x) = ")

    f: Callable[[float], float] = lambda x, _e=expr: eval(_e, {"x": x, "math": math})

    print("\nIngrese los extremos del intervalo [a, c]:")
    a: float = float(input("  a = "))
    c: float = float(input("  c = "))

    tolerancia: float = float(input("\nIngrese la tolerancia: "))
    max_iter: int     = int(input("Ingrese el número máximo de iteraciones: "))

    raiz: float = biseccion(f, a, c, tolerancia=tolerancia, max_iter=max_iter)
    print(f"\n  Raíz encontrada: {raiz}\n")
    print("*" * 95)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    # main()

    print("\n" + "─" * 50)
    print("  Ejemplo: f(x) = x³ - 17  en [2, 3]")
    print("─" * 50)
    f2: Callable[[float], float] = lambda x: x**3 - 17
    biseccion(f2, a=2.0, c=3.0, tolerancia=0.125, max_iter=10)