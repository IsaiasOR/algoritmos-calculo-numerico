"""
Búsqueda de intervalos que contienen raíces por cambio de signo.
Basado en el Teorema de Bolzano: si f es continua en [a, b] y f(a)·f(b) < 0,
entonces existe al menos una raíz (nº impar) en (a, b).
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

def buscar_intervalos(
    f:    Callable[[float], float],
    a:    float,
    b:    float,
    paso: float = 1.0,
) -> list[tuple[float, float]]:
    """
    Recorre [a, b] con el paso dado y detecta sub-intervalos con cambio de signo.

    Parámetros
    ----------
    f    : función a analizar
    a    : extremo izquierdo del intervalo de búsqueda
    b    : extremo derecho del intervalo de búsqueda
    paso : tamaño del sub-intervalo (default 1.0)

    Retorna
    -------
    Lista de tuplas (xᵢ, xᵢ₊₁) donde f cambia de signo.
    """

    W: int = 75

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" BÚSQUEDA DE INTERVALOS CON RAÍCES (BOLZANO)".center(W))
    print("=" * W)
    print(f"  Intervalo de búsqueda : [{a}, {b}]")
    print(f"  Paso                  : {paso}")
    n_pasos = int(round((b - a) / paso))
    print(f"  Sub-intervalos a evaluar : {n_pasos}")
    print("=" * W)

    # ── Encabezado de tabla ────────────────────────────────────────────────
    col = f"{'x':>10} | {'f(x)':>18} | {'Signo':^7} | {'Observación'}"
    print(col)
    print("-" * W)

    # ── Evaluación y tabulación ────────────────────────────────────────────
    xs:     list[float] = []
    fs:     list[float] = []
    x = a
    while round(x, 10) <= round(b, 10):
        fx = f(x)
        signo = "(+)" if fx > 0 else ("(-)" if fx < 0 else "( 0)")
        xs.append(x)
        fs.append(fx)
        print(f"{x:>10.2f} | {fx:>18.6f} | {signo:^7} |")
        x = round(x + paso, 10)

    # ── Detección de cambios de signo ─────────────────────────────────────
    print("-" * W)
    intervalos: list[tuple[float, float]] = []

    for i in range(len(xs) - 1):
        x_izq, x_der = xs[i], xs[i + 1]
        f_izq, f_der = fs[i], fs[i + 1]

        if f_izq == 0.0:
            # Raíz exacta en el extremo izquierdo
            intervalos.append((x_izq, x_izq))
        elif f_der == 0.0:
            pass   # se detectará como extremo izquierdo del siguiente par
        elif f_izq * f_der < 0:
            intervalos.append((x_izq, x_der))

    # ── Resumen ────────────────────────────────────────────────────────────
    if intervalos:
        print(f"\n  ✅ Se encontraron {len(intervalos)} intervalo/s con raíz/ces:\n")
        for i, (xi, xd) in enumerate(intervalos, 1):
            if xi == xd:
                print(f"     {i}) Raíz exacta en x = {xi:.2f}  →  f({xi:.2f}) = 0")
            else:
                fi, fd = f(xi), f(xd)
                si = "(+)" if fi > 0 else "(-)"
                sd = "(+)" if fd > 0 else "(-)"
                print(
                    f"     {i}) [{xi:.2f}, {xd:.2f}]  "
                    f"f({xi:.2f}) = {fi:>12.4f} {si}   "
                    f"f({xd:.2f}) = {fd:>12.4f} {sd}   → cambio de signo"
                )
    else:
        print("\n  ⚠️  No se detectaron cambios de signo en el intervalo dado.")
        print("  ℹ️  Podría no haber raíces reales, o el paso es demasiado grande")
        print("      (raíces muy cercanas entre sí pueden quedar sin detectar).")

    print()
    print("=" * W)

    return intervalos


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 75
    print("\n" + "*" * W)
    print(" BÚSQUEDA DE INTERVALOS CON RAÍCES".center(W))
    print("*" * W)
    print()
    print("  Ingresá f(x) como expresión Python.")
    print("  Ejemplos:")
    print("    -19*(x-0.5)*(x-1) + math.exp(x) + math.exp(-2*x)")
    print("    x**3 - x - 1")

    expr_f: str = input("\n  f(x) = ")
    f: Callable[[float], float] = lambda x, _e=expr_f: eval(_e, {"x": x, **_ENV})

    a:    float = float(input("\n  Extremo izquierdo  a = "))
    b:    float = float(input("  Extremo derecho    b = "))
    paso: float = float(input("  Paso               h = "))

    intervalos = buscar_intervalos(f, a, b, paso)

    if intervalos:
        print(f"\n  Intervalos encontrados: {[list(iv) for iv in intervalos]}\n")
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    # main()

    W: int = 75

    # Y = -19(x - 0.5)(x - 1) + e^x + e^(-2x)   en [-10, 10], paso = 1.0
    # Respuesta esperada: [-3, -2]  [0, 1]  [1, 2]  [6, 7]
    print("\n" + "─" * W)
    print("  f(x) = -19(x - 0.5)(x - 1) + eˣ + e^(-2x)   en [-10, 10], paso = 1.0")
    print("─" * W)

    f_ej: Callable[[float], float] = (
        lambda x: -19 * (x - 0.5) * (x - 1) + math.exp(x) + math.exp(-2 * x)
    )
    intervalos_ej = buscar_intervalos(f_ej, a=-10.0, b=10.0, paso=1.0)

    # ── Ejemplo adicional: refinamiento sobre un intervalo detectado ───────
    print("\n" + "─" * W)
    print("  Refinamiento: sub-intervalo [0, 1] con paso = 0.1")
    print("─" * W)
    buscar_intervalos(f_ej, a=0.0, b=1.0, paso=0.1)