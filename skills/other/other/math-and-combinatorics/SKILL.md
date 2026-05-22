---
name: math-and-combinatorics
description: >-
  Reference patterns for mathematical and combinatorial problem-solving.
  Covers modular arithmetic, prime sieves, GCD/LCM, binomial coefficients,
  fast exponentiation, counting techniques, inclusion-exclusion, and game
  theory. Load this skill when a problem involves number theory, combinatorics,
  modular operations, or strategic game analysis.
user-invocable: false
disable-model-invocation: false
---

# Math and Combinatorics Patterns

Mathematical and combinatorial problems appear frequently in competitive programming and algorithm design. They often hide behind constraints that look like brute-force problems but require algebraic shortcuts to meet time limits. This reference covers eight core pattern families with recognition signals, templates, and pitfalls.

## Pattern Recognition Table

| Trigger Signals | Technique | Typical Complexity |
|---|---|---|
| "answer modulo 10^9+7", large product/sum | Modular Arithmetic | O(1) per operation |
| "count primes up to N", "smallest factor" | Sieve of Eratosthenes | O(N log log N) |
| "greatest common divisor", "least common multiple" | GCD / LCM | O(log min(a,b)) |
| "how many ways to choose", "combinations mod p" | Binomial Coefficients | O(N) precompute, O(1) query |
| "compute a^b mod m", "matrix recurrence" | Fast Exponentiation | O(log b) |
| "count arrangements", "distribute items into groups" | Counting Techniques | Varies |
| "count elements satisfying at least one", "derangements" | Inclusion-Exclusion | O(2^k) for k constraints |
| "two players, optimal play", "who wins" | Game Theory (Sprague-Grundy) | Varies by state space |

---

## Constraint-to-Technique Mapping

- **N up to 10^7** and asks about primes: Sieve of Eratosthenes.
- **N up to 10^6** and asks "how many ways": Precomputed factorials + modular inverse for nCr.
- **"modulo 10^9+7"** anywhere in the problem: Modular arithmetic throughout; use modular inverse for division.
- **Two players, finite game, no randomness**: Sprague-Grundy theorem or direct DP on game states.
- **"count subsets satisfying property"** with small constraint count (k <= 20): Inclusion-exclusion over 2^k subsets.
- **Linear recurrence with large N (10^18)**: Matrix exponentiation to compute nth term in O(k^3 log N).
- **"distribute N items into K groups"**: Stars and bars, possibly combined with inclusion-exclusion for bounded constraints.

## Individual Patterns

### Modular Arithmetic

**Recognition Signals**
- Problem says "answer modulo 10^9+7" or any large prime
- Intermediate values overflow 64-bit integers
- Division is required under a modular context
- Counting problem with astronomically large answers

**Core Idea**

All arithmetic operations (add, subtract, multiply) distribute over modulo. Division under a prime modulus uses modular inverse: `a / b mod p = a * b^(p-2) mod p` via Fermat's little theorem. Always reduce intermediate results to prevent overflow.

**Python Template**

```python
MOD = 10**9 + 7

def mod_add(a: int, b: int) -> int:
    return (a + b) % MOD

def mod_mul(a: int, b: int) -> int:
    return (a * b) % MOD

def mod_pow(base: int, exp: int, mod: int = MOD) -> int:
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

def mod_inv(a: int, mod: int = MOD) -> int:
    """Modular inverse via Fermat's little theorem. Requires mod is prime."""
    return mod_pow(a, mod - 2, mod)

def mod_div(a: int, b: int) -> int:
    return mod_mul(a, mod_inv(b))
```

**Key Edge Cases**
- Subtraction can go negative: use `(a - b + MOD) % MOD`
- Zero divisor: `mod_inv(0)` is undefined; guard against it
- Non-prime modulus: Fermat's theorem does not apply; use extended GCD instead
- Chained multiplications: reduce after every multiply, not just at the end

**Common Mistakes**
- Forgetting to take mod after subtraction, producing negative values
- Using Fermat's inverse with a composite modulus
- Applying mod to intermediate index calculations where exact values are needed

### Sieve of Eratosthenes

**Recognition Signals**
- "Find all primes up to N" with N up to 10^7
- "Smallest prime factor of every number"
- Need to factorize many numbers efficiently
- "Count of prime factors" across a range

**Core Idea**

The classic sieve marks composites by iterating through multiples of each prime. The smallest-prime-factor (SPF) variant stores the smallest divisor at each index, enabling O(log N) factorization of any number after an O(N log log N) precompute. For ranges beyond memory, use a segmented sieve.

**Python Template**

```python
def sieve_primes(n: int) -> list[bool]:
    """Standard boolean sieve. is_prime[i] is True if i is prime."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

def smallest_prime_factor(n: int) -> list[int]:
    """SPF sieve for fast factorization."""
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize(x: int, spf: list[int]) -> list[int]:
    """Factorize x using precomputed SPF table."""
    factors: list[int] = []
    while x > 1:
        factors.append(spf[x])
        x //= spf[x]
    return factors
```

**Key Edge Cases**
- N = 0 or 1: no primes exist; handle boundary
- Memory limit: standard sieve needs O(N) space; switch to segmented sieve above ~10^8
- SPF of 1: not defined; skip or handle separately
- Even numbers: can optimize by treating 2 specially and only sieving odds

**Common Mistakes**
- Starting inner loop at `2*i` instead of `i*i` (correct but slower)
- Off-by-one on sieve size (allocate `n+1` slots)
- Forgetting that `sieve[0]` and `sieve[1]` are not prime

### GCD / LCM

**Recognition Signals**
- Problem explicitly mentions GCD or LCM
- "Find the largest number that divides all elements"
- "Smallest number divisible by all elements"
- Equations involving linear combinations of two integers (Bezout's identity)

**Core Idea**

Euclidean algorithm computes GCD in O(log min(a,b)). LCM derives from GCD: `lcm(a,b) = a * b // gcd(a,b)`. Extended Euclidean finds coefficients x, y such that `a*x + b*y = gcd(a,b)`, which is essential for modular inverse when the modulus is not prime.

**Python Template**

```python
from math import gcd
from functools import reduce

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)

def lcm_array(arr: list[int]) -> int:
    return reduce(lcm, arr)

def gcd_array(arr: list[int]) -> int:
    return reduce(gcd, arr)

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def mod_inv_ext(a: int, m: int) -> int:
    """Modular inverse via extended GCD. Works for any coprime a, m."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"Inverse does not exist: gcd({a}, {m}) = {g}")
    return x % m
```

**Key Edge Cases**
- `gcd(0, x) = x` and `gcd(0, 0) = 0` by convention
- LCM overflow: compute `a // gcd(a,b) * b` instead of `a * b // gcd(a,b)`
- Negative inputs: take absolute values before computing
- Extended GCD with `b = 0`: base case returns `(a, 1, 0)`

**Common Mistakes**
- LCM overflow from multiplying before dividing by GCD
- Assuming modular inverse exists when `gcd(a, m) != 1`
- Recursion depth for very large inputs (Python's default limit); use iterative version if needed

### Binomial Coefficients

**Recognition Signals**
- "How many ways to choose k items from n"
- "nCr mod p" with large n
- Pascal's triangle or binomial theorem mentioned
- Lattice path counting (grid movement problems)

**Core Idea**

For small n (up to ~10^6), precompute factorials and inverse factorials modulo a prime, then answer nCr queries in O(1). Pascal's triangle DP works for smaller n without modular arithmetic. Lucas' theorem handles nCr mod p when n is very large but p is small.

**Python Template**

```python
MOD = 10**9 + 7

def precompute_factorials(n: int) -> tuple[list[int], list[int]]:
    """Precompute factorial and inverse factorial arrays mod MOD."""
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD
    return fact, inv_fact

def nCr(n: int, r: int, fact: list[int], inv_fact: list[int]) -> int:
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

def lucas(n: int, r: int, p: int) -> int:
    """nCr mod p for small prime p, using Lucas' theorem."""
    if r == 0:
        return 1
    return lucas(n // p, r // p, p) * nCr_small(n % p, r % p, p) % p

def nCr_small(n: int, r: int, p: int) -> int:
    """Direct nCr mod p for n < p."""
    if r < 0 or r > n:
        return 0
    num = den = 1
    for i in range(r):
        num = num * (n - i) % p
        den = den * (i + 1) % p
    return num * pow(den, p - 2, p) % p
```

**Key Edge Cases**
- `nCr(n, 0) = 1` and `nCr(n, n) = 1` for all valid n
- `r > n` returns 0
- Negative r or n: return 0
- Lucas' theorem only works when p is prime

**Common Mistakes**
- Off-by-one in precompute size (need `n+1` slots)
- Using Lucas' theorem with composite modulus
- Forgetting the `r > n` guard, causing index-out-of-bounds

### Fast Exponentiation

**Recognition Signals**
- "Compute a^b mod m" with b up to 10^18
- Linear recurrence (Fibonacci-like) with very large n
- "Matrix power" or "transform applied k times"
- State transition repeated billions of times

**Core Idea**

Binary exponentiation computes `a^b mod m` in O(log b) by squaring the base and halving the exponent at each step. Matrix exponentiation extends this: represent a linear recurrence as a matrix multiplication, then raise the transition matrix to the nth power. This turns O(n) recurrence evaluation into O(k^3 log n) where k is the matrix dimension.

**Python Template**

```python
def power(base: int, exp: int, mod: int) -> int:
    """Binary exponentiation: base^exp mod mod."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        exp >>= 1
        base = base * base % mod
    return result

Matrix = list[list[int]]

def mat_mul(a: Matrix, b: Matrix, mod: int) -> Matrix:
    """Multiply two square matrices mod mod."""
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            for j in range(n):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % mod
    return result

def mat_pow(mat: Matrix, exp: int, mod: int) -> Matrix:
    """Raise a square matrix to exp-th power mod mod."""
    n = len(mat)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    while exp > 0:
        if exp & 1:
            result = mat_mul(result, mat, mod)
        exp >>= 1
        mat = mat_mul(mat, mat, mod)
    return result
```

**Key Edge Cases**
- `exp = 0`: result is 1 (scalar) or identity matrix
- `base = 0` with `exp = 0`: conventionally 1, but problem-dependent
- Overflow in matrix multiplication: reduce mod at every addition
- Recurrence with more than 2 terms: increase matrix dimension accordingly

**Common Mistakes**
- Forgetting to handle `exp = 0` as a special case
- Not reducing base modulo m before starting (causes unnecessary large intermediate values)
- Using the wrong matrix dimension for the recurrence

### Counting Techniques

**Recognition Signals**
- "How many ways to arrange/distribute/partition"
- "Count sequences satisfying constraints"
- "Stars and bars" or "multiset coefficient"
- Catalan-number patterns: balanced parentheses, binary trees, non-crossing partitions

**Core Idea**

Permutations count ordered arrangements; combinations count unordered selections. Stars and bars counts ways to distribute n identical items into k distinct bins: `C(n+k-1, k-1)`. Catalan numbers count structures with recursive nesting (nth Catalan = `C(2n, n) / (n+1)`). Recognize which formula applies by identifying whether order matters and whether items are identical or distinct.

**Python Template**

```python
MOD = 10**9 + 7

def permutations_mod(n: int, r: int, fact: list[int], inv_fact: list[int]) -> int:
    """P(n, r) = n! / (n-r)! mod MOD."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[n - r] % MOD

def stars_and_bars(n: int, k: int, fact: list[int], inv_fact: list[int]) -> int:
    """Distribute n identical items into k distinct bins (each >= 0)."""
    return nCr(n + k - 1, k - 1, fact, inv_fact)

def catalan(n: int, fact: list[int], inv_fact: list[int]) -> int:
    """Nth Catalan number mod MOD."""
    return nCr(2 * n, n, fact, inv_fact) * pow(n + 1, MOD - 2, MOD) % MOD

def multiset_coeff(n: int, k: int, fact: list[int], inv_fact: list[int]) -> int:
    """Choose k items from n types with repetition allowed. Uses nCr from above."""
    return nCr(n + k - 1, k, fact, inv_fact)
```

**Key Edge Cases**
- Stars and bars with lower bounds: shift variables (replace x_i with y_i = x_i - lower_i)
- Catalan(0) = 1 by convention
- Empty arrangements: 0 items chosen from n gives 1 way (the empty selection)
- Upper-bounded distributions: combine stars and bars with inclusion-exclusion

**Common Mistakes**
- Confusing "with repetition" vs "without repetition" in the problem statement
- Applying stars and bars when items are distinct (use multinomial instead)
- Forgetting the `n+1` denominator in the Catalan formula

### Inclusion-Exclusion

**Recognition Signals**
- "Count elements satisfying at least one of k properties"
- "Count permutations with no fixed points" (derangements)
- "Count integers in range divisible by at least one of given primes"
- Constraints that are easier to count by complementing

**Core Idea**

Inclusion-exclusion alternates between adding and subtracting intersection sizes: `|A1 union A2 union ... Ak| = sum|Ai| - sum|Ai intersect Aj| + ...`. This is powerful when direct counting is hard but counting elements with specific properties (or their complements) is easy. Derangements are a classic application: `D(n) = n! * sum_{i=0}^{n} (-1)^i / i!`.

**Python Template**

```python
MOD = 10**9 + 7

def inclusion_exclusion(sets_sizes: list[int], intersect_fn) -> int:
    """Generic IE over k sets. intersect_fn(mask) returns |intersection of sets in mask|."""
    k = len(sets_sizes)
    total = 0
    for mask in range(1, 1 << k):
        bits = bin(mask).count("1")
        size = intersect_fn(mask)
        if bits % 2 == 1:
            total = (total + size) % MOD
        else:
            total = (total - size + MOD) % MOD
    return total

def derangements(n: int) -> int:
    """Count permutations with no fixed points, mod MOD."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0
    for i in range(2, n + 1):
        dp[i] = (i - 1) * (dp[i - 1] + dp[i - 2]) % MOD
    return dp[n]

def euler_totient(n: int) -> int:
    """Euler's totient: count integers in [1, n] coprime to n."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result
```

**Key Edge Cases**
- `D(0) = 1` (the empty permutation is a derangement)
- Inclusion-exclusion with k > 20 is usually too slow (2^k subsets); look for algebraic shortcuts
- Totient of 1 is 1
- Overlapping constraints that are not independent require careful intersection counting

**Common Mistakes**
- Sign error: forgetting to alternate between addition and subtraction
- Double-counting when constraints are not mutually independent
- Not handling the complementary counting step (total minus IE result)

### Game Theory (Sprague-Grundy)

**Recognition Signals**
- "Two players take turns, optimal play, who wins"
- Game with positions that can be decomposed into independent sub-games
- Nim-like games with pile manipulation
- "First player wins or second player wins"

**Core Idea**

The Sprague-Grundy theorem states that every impartial game position has a Grundy number (nimber). A position with Grundy number 0 is a losing position for the player to move. For composite games (independent sub-games), the overall Grundy number is the XOR of individual Grundy numbers. Standard Nim: XOR all pile sizes; if nonzero, first player wins.

**Python Template**

```python
def compute_grundy(max_state: int, moves_fn) -> list[int]:
    """Compute Grundy numbers for states 0..max_state.

    moves_fn(state) returns an iterable of reachable states.
    """
    grundy = [0] * (max_state + 1)
    for state in range(max_state + 1):
        reachable: set[int] = set()
        for next_state in moves_fn(state):
            reachable.add(grundy[next_state])
        mex = 0
        while mex in reachable:
            mex += 1
        grundy[state] = mex
    return grundy

def game_winner(values: list[int]) -> str:
    """Winner via XOR. Works for Nim piles or composite Grundy values."""
    xor_sum = 0
    for v in values:
        xor_sum ^= v
    return "First" if xor_sum != 0 else "Second"
```

**Key Edge Cases**
- Terminal position (no moves available): Grundy number is 0 (losing for player to move)
- Single pile Nim: first player wins unless pile is 0
- Game with cycles: Sprague-Grundy applies only to acyclic (impartial) games
- Misere Nim: different endgame rule inverts the strategy for the last move

**Common Mistakes**
- Applying Sprague-Grundy to partisan games (different move sets per player)
- Forgetting that XOR-based composition requires sub-games to be independent
- Computing mex incorrectly by not collecting all reachable Grundy values first
