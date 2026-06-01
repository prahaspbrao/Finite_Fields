from math import gcd
import random


def pollards_rho(n):
    """
    Pollard's Rho algorithm to find a non-trivial factor of n.
    Uses Floyd's cycle detection (tortoise and hare).
    Returns a factor d where 1 < d < n, or None if failed.
    """
    if n % 2 == 0:
        return 2

    # Try several random starting values if needed
    for attempt in range(20):
        x = random.randint(2, n - 1)
        y = x
        c = random.randint(1, n - 1)
        d = 1

        iterations = 0
        while d == 1:
            x = (x * x + c) % n          # tortoise: one step
            y = (y * y + c) % n          # hare: two steps
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
            iterations += 1
            if iterations > 1_000_000:
                break

        if d != n:
            return d  # found a non-trivial factor

    return None  # all attempts failed


def factorize(n):
    """
    Fully factorize n into prime factors using Pollard's Rho.
    Returns a sorted list of prime factors (with repetition).
    """
    if n <= 1:
        return []
    if is_prime(n):
        return [n]

    factor = None
    while factor is None:
        factor = pollards_rho(n)

    return sorted(factorize(factor) + factorize(n // factor))


def is_prime(n):
    """Miller-Rabin primality test (deterministic for n < 3.3e24)."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def euler_phi(n, factors):
    """
    Compute Euler's phi(n) given the prime factorization.
    Uses: phi(n) = n * product of (1 - 1/p) for each distinct prime p.
    For n = p * q (distinct primes): phi(n) = (p-1)(q-1)
    """
    phi = n
    seen = set()
    for p in factors:
        if p not in seen:
            phi = phi * (p - 1) // p
            seen.add(p)
    return phi


def factor_n(n):
    print("=" * 55)
    print(f"  Integer Factorization of  n = {n}")
    print("=" * 55)

    if is_prime(n):
        print(f"  {n} is already prime!")
        print(f"  phi({n}) = {n - 1}")
        return

    print(f"  Applying Pollard's Rho Algorithm...")
    factors = factorize(n)
    print(f"\n  Prime Factorization:")

    # Group factors with exponents
    from collections import Counter
    factor_counts = Counter(factors)
    factored_str = " × ".join(
        f"{p}^{e}" if e > 1 else str(p)
        for p, e in sorted(factor_counts.items())
    )
    print(f"    {n} = {factored_str}")
    print(f"    Factors: {sorted(factor_counts.items())}")

    # Verify
    product = 1
    for f in factors:
        product *= f
    check = "✓ Correct" if product == n else "✗ MISMATCH"
    print(f"    Verification: {' × '.join(map(str, factors))} = {product}  {check}")

    # Euler's Phi
    phi = euler_phi(n, factors)
    print(f"\n  Euler's Phi Function:")
    if len(factor_counts) == 2 and all(e == 1 for e in factor_counts.values()):
        p, q = sorted(factor_counts.keys())
        print(f"    phi({n}) = (p-1)(q-1) = ({p}-1)({q}-1)")
        print(f"           = {p-1} × {q-1} = {phi}")
    else:
        print(f"    phi({n}) = {phi}")

    print(f"\n  RSA Relevance:")
    print(f"    Choose e coprime to phi({n}) = {phi}")
    print(f"    Private key d = e^(-1) mod {phi}")
    print("=" * 55)
    print()


# ── Run Examples ──────────────────────────────────────────
if __name__ == "__main__":

    # Example 1: n = 8051 = 83 × 97  (from the presentation)
    factor_n(8051)

    # Example 2: n = 15 = 3 × 5
    factor_n(15)

    # Example 3: n = 1649 = 17 × 97
    factor_n(1649)

    # Example 4: larger semiprime
    factor_n(104729 * 15013)