"""
Método de Müller para encontrar raíces de funciones no lineales.
Basado en el algoritmo de Mathews & Fink (2004).
"""

import math
from collections.abc import Callable


# ─────────────────────────────────────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────────────────────────────────────

def muller(
    f: Callable[[float], float],
    p0: float,
    p1: float,
    p2: float,
    delta: float = 1e-6,
    epsilon: float = 1e-10,
    max_iter: int = 100,
) -> float | None:
    """
    Método de Müller para encontrar una raíz real de f.

    Parámetros
    ----------
    f        : función objetivo f(x)
    p0, p1, p2 : tres aprox iniciales distintas
    delta    : tolerancia para el cambio en p  (criterio de parada)
    epsilon  : tolerancia para |f(p)|           (criterio de parada)
    max_iter : número máximo de iteraciones

    Retorna
    -------
    p : aproximación de la raíz encontrada
    """

    # ── Encabezado ────────────────────────────────────────────────────────────
    W = 90
    print("\n" + "=" * W)
    print(" MÉTODO DE MÜLLER".center(W))
    print("=" * W)
    print(f"  Aproximaciones iniciales : p0 = {p0},  p1 = {p1},  p2 = {p2}")
    print(f"  Tolerancia (delta)       : {delta}")
    print(f"  Tolerancia (epsilon)     : {epsilon}")
    print(f"  Iteraciones máximas      : {max_iter}")
    print("=" * W)

    col = f"{'Iter':>5} | {'p0':>12} | {'p1':>12} | {'p2':>12} | {'p (nueva)':>15} | {'Error abs.':>12} | {'f(p)':>14}"
    print(col)
    print("-" * W)

    # ── Inicialización ────────────────────────────────────────────────────────
    aprox = [p0, p1, p2]
    vector_indep = [f(aprox[0]), f(aprox[1]), f(aprox[2])]

    # Imprimir fila inicial (iteración 0)
    print(
        f"{'0':>5} | {aprox[0]:>12.6f} | {aprox[1]:>12.6f} | {aprox[2]:>12.6f} | "
        f"{'—':>15} | {'—':>12} | {vector_indep[2]:>14.6e}"
    )

    p_final = None
    convergio = False
    k = 0
    p = aprox[2]

    for k in range(1, max_iter + 1):
        # ── Calcular coeficientes a, b, c del polinomio cuadrático ───────────
        h0 = aprox[0] - aprox[2]   # h_{i-2}
        h1 = aprox[1] - aprox[2]   # h_{i-1}
        e0 = vector_indep[0] - vector_indep[2]   # f(p0) - f(p2)
        e1 = vector_indep[1] - vector_indep[2]   # f(p1) - f(p2)
        c  = vector_indep[2]           # f(p2)  →  término independiente del polinomio

        denom = h1 * h0**2 - h0 * h1**2
        a = (e0 * h1 - e1 * h0) / denom
        b = (e1 * h0**2 - e0 * h1**2) / denom

        # ── Discriminante: suprimir raíces complejas ──────────────────────────
        disc_sq = b**2 - 4 * a * c
        disc = math.sqrt(disc_sq) if disc_sq > 0 else 0.0

        # Elegir el signo que maximiza |denominador| para mayor precisión
        if b < 0:
            disc = -disc

        # ── Nueva aproximación ────────────────────────────────────────────────
        z = -2 * c / (b + disc)   # corrección
        p = aprox[2] + z              # nueva raíz candidata

        # ── Error y valor de la función ───────────────────────────────────────
        err    = abs(z)
        relerr = err / (abs(p) + delta)
        y_p    = f(p)

        print(
            f"{k:>5} | {aprox[0]:>12.6f} | {aprox[1]:>12.6f} | {aprox[2]:>12.6f} | "
            f"{p:>15.8f} | {err:>12.2e} | {y_p:>14.6e}"
        )

        # ── Criterio de parada ────────────────────────────────────────────────
        if err < delta or relerr < delta or abs(y_p) < epsilon:
            p_final  = p
            convergio = True
            break

        # ── Reorganizar los tres puntos: conservar los dos más cercanos a p ──
        #    Ordenamos aprox por distancia a p y descartamos el más lejano
        indices = sorted([0, 1, 2], key=lambda i: abs(p - aprox[i]))
        # Los dos más cercanos quedan como p0 y p1; el tercer lugar lo ocupa p
        aprox_nueva = [aprox[indices[0]], aprox[indices[1]], p]
        vector_indep_nuevo = [f(aprox_nueva[0]), f(aprox_nueva[1]), f(aprox_nueva[2])]
        aprox, vector_indep = aprox_nueva, vector_indep_nuevo

    # ── Mensaje final ──────────────────────────────────────────────────────────
    print("-" * W)
    if convergio:
        print(f"  ✅ Convergencia alcanzada en {k} iteraciones.")
        print(f"  ➤  Raíz aproximada : p  = {p_final:.10f}")
        print(f"  ➤  f(p)            = {f(p_final):.6e}")
    else:
        print(f"  ⚠️  Se alcanzó el máximo de iteraciones ({max_iter}) sin converger.")
        p_final = p
    print("=" * W)

    return p_final


# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "*" * 90)
    print(" RESOLUCIÓN DE RAÍCES POR EL MÉTODO DE MÜLLER".center(90))
    print("*" * 90)

    # Función objetivo
    print("\nIngrese la función f(x) como expresión de Python.")
    print("  Ejemplos: x**3 - x - 1   |   math.sin(x) - x/2   |   x**3 - 3*x + 1")
    expr = input("  f(x) = ")

    # Se crea la función evaluando la expresión con math disponible
    f: Callable[[float], float] = lambda x, _e=expr: eval(_e, {"x": x, "math": math})

    # Aproximaciones iniciales
    print("\nIngrese las tres aprox iniciales:")
    p0 = float(input("  p0 = "))
    p1 = float(input("  p1 = "))
    p2 = float(input("  p2 = "))

    # Tolerancias
    delta    = float(input("\nIngrese la tolerancia para el cambio en p (delta): "))
    epsilon  = float(input("Ingrese la tolerancia para |f(p)|         (epsilon): "))
    max_iter = int(input("Ingrese el número máximo de iteraciones: "))

    # Ejecutar método
    raiz = muller(f, p0, p1, p2, delta=delta, epsilon=epsilon, max_iter=max_iter)
    print(f"\n  Raíz encontrada: {raiz}\n")
    print("*" * 90)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplo de uso directo (sin menú)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:
    # main()

    print("\n" + "─" * 50)
    print("  Ejemplo: f(x) = x³ - 3x + 1")
    print("─" * 50)
    f2: Callable[[float], float] = lambda x: x**3 - 3*x + 1
    muller(f2, p0=1.0, p1=1.5, p2=2.0, delta=1e-6, epsilon=1e-10)