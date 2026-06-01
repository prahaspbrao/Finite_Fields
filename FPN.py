from itertools import product

def list_finite_field(p, n, irr_poly):
    """
    List all elements of the finite field F_p^n.
    
    p        : prime (e.g. 2, 3, 5)
    n        : degree >= 2
    irr_poly : coefficients of irreducible polynomial [a0, a1, ..., an]
               e.g. x^2+x+1 over Z2 -> [1, 1, 1]
    """
    elements = []
    for coeffs in product(range(p), repeat=n):
        poly_str = format_poly(coeffs)
        elements.append((list(coeffs), poly_str))
    return elements


def format_poly(coeffs):
    """Convert coefficient tuple to human-readable polynomial string."""
    terms = []
    for i, a in enumerate(coeffs):
        if a == 0:
            continue
        if i == 0:
            terms.append(str(a))
        elif i == 1:
            terms.append(f"{a}x" if a != 1 else "x")
        else:
            terms.append(f"{a}x^{i}" if a != 1 else f"x^{i}")
    return " + ".join(reversed(terms)) if terms else "0"


def poly_add(a, b, p):
    """Add two polynomials mod p."""
    n = max(len(a), len(b))
    result = [(0)] * n
    for i in range(len(a)):
        result[i] = (result[i] + a[i]) % p
    for i in range(len(b)):
        result[i] = (result[i] + b[i]) % p
    return result


def poly_mul_mod(a, b, irr_poly, p):
    """Multiply two polynomials mod (irr_poly, p)."""
    n = len(irr_poly) - 1  # degree of irreducible polynomial
    # Full multiplication
    product_poly = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            product_poly[i + j] = (product_poly[i + j] + ai * bj) % p
    # Reduce mod irr_poly
    for i in range(len(product_poly) - 1, n - 1, -1):
        if product_poly[i] == 0:
            continue
        coeff = product_poly[i]
        for j, c in enumerate(irr_poly):
            product_poly[i - n + j] = (product_poly[i - n + j] - coeff * c) % p
        product_poly[i] = 0
    return [x % p for x in product_poly[:n]]


def verify_irreducible(irr_poly, p):
    """Check that irr_poly has no roots in Zp (necessary condition)."""
    n = len(irr_poly) - 1
    for x in range(p):
        val = 0
        for i, c in enumerate(irr_poly):
            val = (val + c * (x ** i)) % p
        if val == 0:
            print(f"  WARNING: f({x}) = 0, polynomial may not be irreducible!")
            return False
    return True


def print_field(p, n, irr_poly):
    print("=" * 55)
    print(f"  Finite Field  F_{p}^{n}")
    poly_name = format_poly(irr_poly)
    print(f"  Modulus     : f(x) = {poly_name}")
    print(f"  Prime       : p = {p}")
    print(f"  Degree      : n = {n}")
    print(f"  Total elems : p^n = {p}^{n} = {p**n}")
    print("=" * 55)

    irred = verify_irreducible(irr_poly, p)
    status = "OK (no roots in Zp)" if irred else "Check failed"
    print(f"  Irreducibility check: {status}")
    print("-" * 55)

    elements = list_finite_field(p, n, irr_poly)
    print(f"  {'#':<5} {'Coefficients':<25} {'Polynomial'}")
    print(f"  {'-'*5} {'-'*25} {'-'*20}")
    for idx, (coeffs, poly_str) in enumerate(elements):
        print(f"  {idx:<5} {str(coeffs):<25} {poly_str}")

    print("=" * 55)
    print(f"  Total: {len(elements)} elements listed.")
    print()


# ── Run Examples ──────────────────────────────────────────
if __name__ == "__main__":

    # Example 1: F_2^2 using f(x) = x^2 + x + 1
    # irr_poly coefficients: [a0, a1, a2] for a0 + a1*x + a2*x^2
    print_field(p=2, n=2, irr_poly=[1, 1, 1])

    # Example 2: F_2^3 using f(x) = x^3 + x + 1
    print_field(p=2, n=3, irr_poly=[1, 1, 0, 1])

    # Example 3: F_3^2 using f(x) = x^2 + 1
    print_field(p=3, n=2, irr_poly=[1, 0, 1])

    # Example 4: F_2^4 using f(x) = x^4 + x + 1
    print_field(p=2, n=4, irr_poly=[1, 1, 0, 0, 1])