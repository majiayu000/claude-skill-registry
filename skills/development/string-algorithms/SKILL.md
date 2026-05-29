---
name: string-algorithms
description: >-
  Reference for string algorithm patterns — KMP, Z-function, Rabin-Karp,
  Manacher's, string hashing, suffix arrays, and Aho-Corasick. Covers
  recognition signals, core ideas, Python templates, edge cases, and
  common mistakes for each technique.
user-invocable: false
disable-model-invocation: false
---

# String Algorithm Patterns

This reference covers seven foundational string algorithms used in competitive programming and technical interviews. Each pattern includes recognition signals, a core idea explanation, a Python template, and notes on edge cases and common mistakes. Use the pattern recognition table to match problem constraints to the right technique, then drill into the individual pattern section.

---

## Pattern Recognition Table

| Trigger Signals | Technique | Typical Complexity |
|---|---|---|
| Find pattern in text, exact match, prefix function | KMP | O(N + M) |
| Longest common prefix at each position, string period | Z-function | O(N) |
| Multiple pattern search, rolling hash, substring fingerprint | Rabin-Karp | O(N + M) average |
| Longest palindromic substring, count palindromes | Manacher's | O(N) |
| Fast substring comparison, equality checks in O(1) | String Hashing | O(N) preprocess, O(1) query |
| Lexicographic ordering of suffixes, LCP queries, substring counting | Suffix Array | O(N log N) build |
| Dictionary of patterns matched against text, multi-pattern search | Aho-Corasick | O(N + M + Z) |

Where N = text length, M = pattern length (or total pattern lengths), Z = number of matches.

---

## Constraint-to-Technique Mapping

- **Single pattern, exact match, N up to 10^6**: KMP or Z-function
- **All prefix-suffix overlaps**: KMP failure function gives overlap chain
- **String periodicity or repetition**: Z-function (period = smallest i where z[i] + i == N)
- **Multiple patterns, moderate count (< 100)**: Rabin-Karp with rolling hash
- **Multiple patterns, large dictionary (10^3+)**: Aho-Corasick automaton
- **Palindrome queries**: Manacher's for longest; hashing + binary search for arbitrary checks
- **Substring equality or comparison in O(1)**: Polynomial string hashing with double hash
- **Lexicographic queries, distinct substrings, LCP**: Suffix array + LCP array

---

### KMP (Knuth-Morris-Pratt)

**Recognition Signals**
- Find all occurrences of a pattern in a text
- Compute the longest proper prefix that is also a suffix (failure/border array)
- Pattern matching without backtracking on the text pointer

**Core Idea**

KMP preprocesses the pattern into a failure (prefix) function that records, for each position, the length of the longest proper prefix that is also a suffix. On mismatch, the failure function tells us where to resume comparison without re-scanning text characters, guaranteeing linear time.

**Python Template**

```python
def kmp_search(text: str, pattern: str) -> list[int]:
    """Return all starting indices where pattern occurs in text."""
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    # Build failure function
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = fail[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        fail[i] = k
    # Search
    matches: list[int] = []
    k = 0
    for i in range(n):
        while k > 0 and pattern[k] != text[i]:
            k = fail[k - 1]
        if pattern[k] == text[i]:
            k += 1
        if k == m:
            matches.append(i - m + 1)
            k = fail[k - 1]
    return matches
```

**Key Edge Cases**
- Empty pattern or empty text (return empty list)
- Pattern longer than text
- Overlapping matches (e.g., pattern "aa" in text "aaaa" yields [0, 1, 2])
- Pattern equals text exactly (single match at index 0)

**Common Mistakes**
- Off-by-one in failure function construction (loop must start at index 1, not 0)
- Forgetting to reset `k = fail[k - 1]` after a full match to allow overlapping matches
- Confusing 0-indexed vs 1-indexed failure arrays across reference implementations

---

### Z-function

**Recognition Signals**
- Compute the longest substring starting at each position that matches a prefix
- Detect string periods or smallest repeating units
- Alternative to KMP for single-pattern matching

**Core Idea**

The Z-array for a string S stores at each index i > 0 the length of the longest substring starting at i that matches a prefix of S. Construction runs in O(N) using a sliding window [l, r] tracking the rightmost Z-box. For pattern matching, concatenate pattern + separator + text and look for Z-values equal to the pattern length. Periodicity detection: the smallest period p satisfies z[p] + p == N.

**Python Template**

```python
def z_function(s: str) -> list[int]:
    """Compute the Z-array for string s."""
    n = len(s)
    z = [0] * n
    z[0] = n
    l, r = 0, 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def z_search(text: str, pattern: str) -> list[int]:
    """Find all occurrences of pattern in text using Z-function."""
    combined = pattern + "$" + text
    z = z_function(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]
```

**Key Edge Cases**
- Single-character strings (Z[0] = N by definition, rest are trivial)
- Strings of all identical characters (every Z[i] = N - i)
- Separator character must not appear in pattern or text

**Common Mistakes**
- Forgetting to set z[0] = n (by convention, z[0] equals the full string length)
- Using a separator character that exists in the input alphabet
- Incorrect window update: the condition is `i + z[i] > r`, not `>=`

---

### Rabin-Karp

**Recognition Signals**
- Multiple pattern search in a single text
- Substring fingerprinting or equality via hashing
- Problems where average-case O(N + M) suffices and worst-case O(NM) is acceptable

**Core Idea**

Rabin-Karp computes a polynomial rolling hash for each text window matching the pattern length. The hash slides in O(1) by subtracting the outgoing character's contribution and adding the incoming one. Hash matches are confirmed by character comparison. For multi-pattern search, store all pattern hashes in a set.

**Python Template**

```python
def rabin_karp(text: str, pattern: str, base: int = 131, mod: int = 10**18 + 9) -> list[int]:
    """Return all starting indices where pattern occurs in text."""
    n, m = len(text), len(pattern)
    if m > n:
        return []
    # Precompute highest power
    power = pow(base, m - 1, mod)
    # Hash the pattern and first window
    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
    matches: list[int] = []
    for i in range(n - m + 1):
        if t_hash == p_hash and text[i:i + m] == pattern:
            matches.append(i)
        if i + m < n:
            t_hash = (t_hash - ord(text[i]) * power) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
    return matches
```

**Key Edge Cases**
- Hash collisions requiring the string comparison fallback
- Very long patterns where power computation must use modular exponentiation
- Negative hash values in languages with signed modular arithmetic (Python handles correctly)

**Common Mistakes**
- Forgetting the confirmation step after a hash match (false positives)
- Using a small modulus that causes frequent collisions
- Off-by-one in the sliding window loop bounds

---

### Manacher's Algorithm

**Recognition Signals**
- Find the longest palindromic substring
- Count total palindromic substrings
- Compute palindrome radii at every center (both odd and even length)

**Core Idea**

Manacher's algorithm finds the maximum palindrome radius centered at each position in O(N). It processes odd-length and even-length palindromes separately. A center c and right boundary r track the rightmost palindrome; for each new position i, the mirror 2c - i provides an initial radius estimate that is then expanded, avoiding redundant comparisons.

**Python Template**

```python
def manacher(s: str) -> tuple[list[int], list[int]]:
    """Return (odd, even) palindrome radius arrays.
    odd[i] = max radius of odd palindrome centered at i (includes center).
    even[i] = max radius of even palindrome centered between i-1 and i.
    """
    n = len(s)
    odd = [0] * n
    l, r = 0, 0
    for i in range(n):
        odd[i] = max(0, min(r - i, odd[l + r - i])) if i < r else 0
        while i - odd[i] >= 0 and i + odd[i] < n and s[i - odd[i]] == s[i + odd[i]]:
            odd[i] += 1
        if i + odd[i] > r:
            l, r = i - odd[i] + 1, i + odd[i]

    even = [0] * n
    l, r = 0, 0
    for i in range(n):
        even[i] = max(0, min(r - i, even[l + r - i - 1])) if i < r else 0
        while i - even[i] - 1 >= 0 and i + even[i] < n and s[i - even[i] - 1] == s[i + even[i]]:
            even[i] += 1
        if i + even[i] > r:
            l, r = i - even[i], i + even[i]

    return odd, even
```

**Key Edge Cases**
- Single-character string (always a palindrome of length 1)
- All characters identical (every substring is a palindrome)
- Even-length palindromes require careful boundary indexing
- Empty string input

**Common Mistakes**
- Mixing up odd and even palindrome handling (different mirror formulas)
- Incorrect mirror index when using the transformed-string variant
- Forgetting boundary checks during expansion (i - radius >= 0)

---

### String Hashing

**Recognition Signals**
- Compare arbitrary substrings for equality in O(1)
- Fast fingerprint for substrings (search, duplicate detection, binary search + comparison)

**Core Idea**

Polynomial hashing assigns each string a fingerprint: H(s) = sum of s[i] * base^i mod p. By precomputing prefix hashes and powers, any substring hash is extracted in O(1). Double hashing (two independent base-mod pairs) reduces collision probability to ~1/p^2, reliable for N up to 10^6.

**Python Template**

```python
class StringHasher:
    """Double polynomial hash for O(1) substring comparison."""

    def __init__(self, s: str, base1: int = 131, mod1: int = 10**18 + 9,
                 base2: int = 137, mod2: int = 10**18 + 7) -> None:
        n = len(s)
        self.mod1, self.mod2 = mod1, mod2
        self.h1 = [0] * (n + 1)
        self.h2 = [0] * (n + 1)
        self.p1 = [1] * (n + 1)
        self.p2 = [1] * (n + 1)
        for i in range(n):
            self.h1[i + 1] = (self.h1[i] * base1 + ord(s[i])) % mod1
            self.h2[i + 1] = (self.h2[i] * base2 + ord(s[i])) % mod2
            self.p1[i + 1] = self.p1[i] * base1 % mod1
            self.p2[i + 1] = self.p2[i] * base2 % mod2

    def query(self, l: int, r: int) -> tuple[int, int]:
        """Return double hash of s[l:r+1] (inclusive on both ends)."""
        length = r - l + 1
        h1 = (self.h1[r + 1] - self.h1[l] * self.p1[length]) % self.mod1
        h2 = (self.h2[r + 1] - self.h2[l] * self.p2[length]) % self.mod2
        return (h1, h2)
```

**Key Edge Cases**
- Substrings of length 0 or 1
- Hash values wrapping around the modulus (ensure non-negative results)
- Comparing substrings from different strings (build separate hashers)

**Common Mistakes**
- Using a single hash (high collision risk at N > 10^5)
- Choosing a base smaller than the alphabet size
- Off-by-one in substring index conventions (inclusive vs exclusive bounds)

---

### Suffix Array

**Recognition Signals**
- Lexicographic ordering of all suffixes, count distinct substrings
- Longest common prefix (LCP) queries between suffixes
- Problems involving sorted suffix structure or substring searching

**Core Idea**

A suffix array is a sorted array of all suffix starting indices. Construction in O(N log^2 N) uses iterative doubling: sort suffixes by their first 1, 2, 4, ... characters using previous rank as key. The LCP array (Kasai's algorithm, O(N)) stores the longest common prefix between consecutive sorted suffixes. Together they enable distinct substring counting (N*(N+1)/2 - sum(LCP)) and binary search over suffixes.

**Python Template**

```python
def build_suffix_array(s: str) -> list[int]:
    """Build suffix array in O(N log^2 N) via iterative doubling."""
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    while k < n:
        def compare(a: int, b: int) -> int:
            if rank[a] != rank[b]:
                return rank[a] - rank[b]
            ra = rank[a + k] if a + k < n else -1
            rb = rank[b + k] if b + k < n else -1
            return ra - rb
        from functools import cmp_to_key
        sa.sort(key=cmp_to_key(compare))
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (1 if compare(sa[i - 1], sa[i]) < 0 else 0)
        rank[:] = tmp
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def build_lcp_array(s: str, sa: list[int]) -> list[int]:
    """Build LCP array using Kasai's algorithm in O(N)."""
    n = len(s)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i
    lcp = [0] * n
    k = 0
    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue
        j = sa[rank[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        k = max(k - 1, 0)
    return lcp
```

**Key Edge Cases**
- Single-character strings
- Strings with all identical characters (suffix array is reverse order)
- Appending a sentinel character ('$') for algorithms requiring unique termination

**Common Mistakes**
- Forgetting the boundary check `a + k < n` when comparing second-half ranks
- Using O(N^2 log N) naive sort instead of rank-based doubling

---

### Aho-Corasick

**Recognition Signals**
- Search for multiple patterns simultaneously in a single text
- Dictionary matching: given a set of words, find all occurrences in a text
- Large pattern dictionary (hundreds or thousands of patterns)

**Core Idea**

Aho-Corasick builds a trie from all patterns, then adds failure links connecting each node to the longest proper suffix that is also a trie prefix. Output lists along failure chains ensure all matching patterns are reported. Text is processed character by character through the automaton in O(N + M + Z) total time.

**Python Template**

```python
from collections import deque

class AhoCorasick:
    """Multi-pattern matching automaton."""

    def __init__(self) -> None:
        self.goto: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.output: list[list[int]] = [[]]

    def add_pattern(self, pattern: str, index: int) -> None:
        """Add a pattern with its identifier to the automaton."""
        state = 0
        for ch in pattern:
            if ch not in self.goto[state]:
                self.goto[state][ch] = len(self.goto)
                self.goto.append({})
                self.fail.append(0)
                self.output.append([])
            state = self.goto[state][ch]
        self.output[state].append(index)

    def build(self) -> None:
        """Construct failure links using BFS."""
        queue: deque[int] = deque()
        for ch, s in self.goto[0].items():
            queue.append(s)
        while queue:
            u = queue.popleft()
            for ch, v in self.goto[u].items():
                queue.append(v)
                f = self.fail[u]
                while f and ch not in self.goto[f]:
                    f = self.fail[f]
                self.fail[v] = self.goto[f].get(ch, 0)
                if self.fail[v] == v:
                    self.fail[v] = 0
                self.output[v] = self.output[v] + self.output[self.fail[v]]

    def search(self, text: str) -> list[tuple[int, int]]:
        """Return list of (end_position, pattern_index) for all matches."""
        state = 0
        results: list[tuple[int, int]] = []
        for i, ch in enumerate(text):
            while state and ch not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(ch, 0)
            for pat_idx in self.output[state]:
                results.append((i, pat_idx))
        return results
```

**Key Edge Cases**
- Patterns that are prefixes of other patterns
- Overlapping pattern matches at the same text position
- Empty patterns in the dictionary (filter before insertion)

**Common Mistakes**
- Forgetting to merge output lists along failure links (misses suffix-state patterns)
- Not guarding against failure links pointing back to the same node
- Building the automaton before all patterns are added
