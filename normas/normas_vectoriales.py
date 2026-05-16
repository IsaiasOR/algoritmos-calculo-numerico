"""
Normas vectoriales
La norma es una medida que asigna un valor real positivo a un vector o matriz,
indicando su "tamaño" o "longitud".
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Normas
# ─────────────────────────────────────────────────────────────────────────────

# Norma-1 / Norma suma: suma de los valores absolutos de los componentes.
def norma_suma(v: list[float]) -> float:
    return sum(abs(x) for x in v)


# Norma-2 / Norma euclidiana: raíz cuadrada de la suma de los cuadrados.
def norma_euclidiana(v: list[float]) -> float:
    return sum(x**2 for x in v) ** 0.5


# Norma-∞ / Norma infinito: máximo valor absoluto entre los componentes.
def norma_infinito(v: list[float]) -> float:
    return max(abs(x) for x in v)


# ─────────────────────────────────────────────────────────────────────────────
#  Presentación
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_normas(v: list[float]) -> None:
    """Calcula y muestra las tres normas de un vector con formato de tabla."""

    W: int = 75

    n1  = norma_suma(v)
    n2  = norma_euclidiana(v)
    ninf = norma_infinito(v)

    # ── Encabezado ─────────────────────────────────────────────────────────
    print("\n" + "=" * W)
    print(" NORMAS VECTORIALES".center(W))
    print("=" * W)

    # ── Vector ─────────────────────────────────────────────────────────────
    componentes = "  ".join(f"{x:>10.4f}" for x in v)
    print(f"  Vector ({len(v)} componentes)")
    print(f"  [ {componentes} ]")
    print("-" * W)

    # ── Tabla de resultados ────────────────────────────────────────────────
    print(f"  {'Norma':<30} {'Símbolo':^10} {'Valor':>14}  {'Fórmula'}")
    print("-" * W)
    print(f"  {'Suma  (L¹)':<30} {'‖v‖₁':^10} {n1:>14.6f}  Σ |vᵢ|")
    print(f"  {'Euclidiana  (L²)':<30} {'‖v‖₂':^10} {n2:>14.6f}  √(Σ vᵢ²)")
    print(f"  {'Infinito  (L∞)':<30} {'‖v‖∞':^10} {ninf:>14.6f}  max |vᵢ|")
    print("=" * W)

# ─────────────────────────────────────────────────────────────────────────────
#  Punto de entrada con ingreso de datos por consola
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    W: int = 75
    print("\n" + "*" * W)
    print(" CÁLCULO DE NORMAS VECTORIALES".center(W))
    print("*" * W)

    raw = input("\nIngresá los componentes del vector separados por espacios:\n  v = ")
    v: list[float] = [float(x) for x in raw.split()]

    mostrar_normas(v)
    print("*" * W)


# ─────────────────────────────────────────────────────────────────────────────
#  Ejemplos de uso directo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Descomentar main() para ingresar datos por consola, o usar los ejemplos:

    main()

    # W: int = 75
    # print("\n" + "─" * W)
    # print("  Ejemplo: v = [3, -4, 5]")
    # print("─" * W)
    # mostrar_normas([3, -4, 5])