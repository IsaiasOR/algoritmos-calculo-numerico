"""
Interpolación de Lagrange para aproximación polinómica.
"""

import math
from typing import Any


# ─────────────────────────────────────────────────────────────────────────────
#  Entorno de evaluación compartido
# ─────────────────────────────────────────────────────────────────────────────

_ENV: dict[str, Any] = {"math": math, **{k: getattr(math, k) for k in dir(math)}}


# ─────────────────────────────────────────────────────────────────────────────
#  Álgebra de polinomios (coeficientes: índice = grado)
#  p = [a₀, a₁, a₂, ...]  →  p(x) = a₀ + a₁x + a₂x² + …
# ─────────────────────────────────────────────────────────────────────────────

def _poly_mul(p: list[float], q: list[float]) -> list[float]:
    """Multiplica dos polinomios representados como listas de coeficientes."""
    resultado = [0.0] * (len(p) + len(q) - 1)
    for i, ai in enumerate(p):
        for j, bj in enumerate(q):
            resultado[i + j] += ai * bj
    return resultado


def _poly_add(p: list[float], q: list[float]) -> list[float]:
    """Suma dos polinomios, rellenando con ceros si tienen distinto grado."""
    n = max(len(p), len(q))
    p = p + [0.0] * (n - len(p))
    q = q + [0.0] * (n - len(q))
    return [a + b for a, b in zip(p, q)]


def _poly_escalar(p: list[float], k: float) -> list[float]:
    """Multiplica un polinomio por un escalar."""
    return [k * c for c in p]


# ─────────────────────────────────────────────────────────────────────────────
#  Núcleo: cálculo de coeficientes del polinomio interpolante
# ─────────────────────────────────────────────────────────────────────────────

def _coeficientes_lagrange(xs: list[float], ys: list[float]) -> list[float]:
    """
    Devuelve los coeficientes [a₀, a₁, …, aₙ] del polinomio interpolante
    de Lagrange expandido, tal que Pₙ(x) = a₀ + a₁x + … + aₙxⁿ.
    """
    n   = len(xs)
    acc = [0.0]
    for j in range(n):
        # Numerador: Π_{i≠j} (x - xᵢ)  →  polinomio simbólico
        num: list[float] = [1.0]
        den: float       = 1.0
        for i in range(n):
            if i != j:
                num = _poly_mul(num, [-xs[i], 1.0])   # (x - xᵢ)
                den *= xs[j] - xs[i]
        # Término j: yⱼ · Lⱼ(x)
        term = _poly_escalar(num, ys[j] / den)
        acc  = _poly_add(acc, term)
    return acc


def _evaluar_poly(coefs: list[float], x: float) -> float:
    """Evalúa el polinomio en x usando el esquema de Horner."""
    resultado = 0.0
    for c in reversed(coefs):
        resultado = resultado * x + c
    return resultado


def _formatear_poly(coefs: list[float], decimales: int = 6) -> str:
    """Devuelve una cadena legible del polinomio, omitiendo términos nulos."""
    terminos: list[str] = []
    for grado, c in enumerate(coefs):
        if abs(c) < 1e-12:
            continue
        coef_str = f"{c:.{decimales}f}"
        if grado == 0:
            terminos.append(coef_str)
        elif grado == 1:
            terminos.append(f"{coef_str}·x")
        else:
            terminos.append(f"{coef_str}·x^{grado}")
    if not terminos:
        return "0"
    # El primer término va sin signo delante; los demás con " + " o " - "
    resultado = terminos[0]
    for t in terminos[1:]:
        if t.startswith("-"):
            resultado += f"  -  {t[1:]}"
        else:
            resultado += f"  +  {t}"
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
#  Presentación principal
# ─────────────────────────────────────────────────────────────────────────────

def lagrange(
    xs:     list[float],
    ys:     list[float],
    x_eval: float | None = None,
) -> float | None:
    """
    Calcula e imprime el polinomio interpolante de Lagrange.
    Opcionalmente lo evalúa en x_eval.

    Retorna Pₙ(x_eval) o None si no se pidió evaluación.
    """

    W: int = 75
    n  = len(xs) - 1
    coefs = _coeficientes_lagrange(xs, ys)

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" INTERPOLACIÓN DE LAGRANGE".center(W))
    print("=" * W)
    print(f"  {n + 1} nodos  →  polinomio de grado ≤ {n}")
    print("=" * W)

    # ── Tabla de nodos ─────────────────────────────────────────────────────
    print(f"\n  {'j':>4}  {'xⱼ':>12}  {'yⱼ':>12}")
    print("  " + "-" * 32)
    for j, (xj, yj) in enumerate(zip(xs, ys)):
        print(f"  {j:>4}  {xj:>12.4f}  {yj:>12.4f}")

    # ── Polinomio resultante ───────────────────────────────────────────────
    print("\n" + "-" * W)
    print("  Polinomio interpolante:")
    print()
    polinomio_str = _formatear_poly(coefs)
    # Partir en líneas si es muy largo
    if len(polinomio_str) > W - 6:
        partes = polinomio_str.split("  +  ")
        print(f"  P(x) = {partes[0]}")
        for p in partes[1:]:
            print(f"         +  {p}")
    else:
        print(f"  P(x) = {polinomio_str}")

    # ── Evaluación en x_eval ───────────────────────────────────────────────
    resultado: float | None = None
    if x_eval is not None:
        resultado = _evaluar_poly(coefs, x_eval)
        print()
        print("-" * W)
        print(f"  P({x_eval}) = {resultado:.8f}")

    print("=" * W)
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 75
    print("\n" + "*" * W)
    print(" INTERPOLACIÓN DE LAGRANGE".center(W))
    print("*" * W)
    print()
    print("  Ingresá los nodos (xⱼ yⱼ). Escribí 'fin' para terminar.")
    print("  Ejemplo:  0 -1   →  x=0, y=-1\n")

    xs: list[float] = []
    ys: list[float] = []

    while True:
        entrada = input(f"  Nodo {len(xs)}: ").strip()
        if entrada.lower() == "fin":
            break
        try:
            partes = entrada.split()
            xs.append(float(partes[0]))
            ys.append(float(partes[1]))
        except (ValueError, IndexError):
            print("  Formato inválido. Ingresá dos números separados por espacio.")

    if len(xs) < 2:
        print("  Se necesitan al menos 2 nodos.")
        return

    print()
    resp = input("  ¿Querés evaluar P(x) en un punto? (s/n): ").strip().lower()
    x_eval: float | None = None
    if resp == "s":
        x_eval = float(input("  x = "))

    lagrange(xs, ys, x_eval)
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    main()

    W: int = 75

    # print("\n" + "─" * W)
    # print("  Ejemplo — Puntos: (0,-1) (2,0) (3,2) (5,1)")
    # print("─" * W)
    # lagrange([0.0, 2.0, 3.0, 5.0], [-1.0, 0.0, 2.0, 1.0], x_eval=4.0)

    # print("\n" + "─" * W)
    # print("  Ejemplo — Puntos: (1,2) y (3,8), evaluar en x=2")
    # print("─" * W)
    # lagrange([1.0, 3.0], [2.0, 8.0], x_eval=2.0)