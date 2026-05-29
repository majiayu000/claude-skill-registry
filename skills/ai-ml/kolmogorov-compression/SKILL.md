---
name: kolmogorov-compression
description: Kolmogorov complexity as the ultimate intelligence measure. Shortest
version: 1.0.0
---

# Kolmogorov Compression Skill

> *"The Kolmogorov complexity of x is the length of the shortest program that outputs x."*
> — Andrey Kolmogorov

## Overview

**Kolmogorov complexity** K(x) = length of shortest program P where P() = x.

**Intelligence = Compression**: Finding short descriptions of data.

## Core Concept

```latex
K(x) = min { |P| : U(P) = x }

Where:
  U = Universal Turing Machine
  P = program (binary string)
  |P| = length of P

Properties:
  - K(x) ≤ |x| + O(1)  (trivial: print x)
  - K(x) is uncomputable (halting problem)
  - K(x|y) = conditional complexity given y
```

## The KoLMogorov-Test (2025)

Use LLMs to approximate Kolmogorov complexity:

```python
class KolmogorovCompressor:
    """
    Approximate K(x) via code generation.
    """
    
    def __init__(self, llm):
        self.llm = llm
    
    def compress(self, data: str) -> str:
        """Generate shortest program that outputs data."""
        prompt = f"""
        Generate the shortest Python program that prints exactly:
        {data[:100]}...
        
        The program must output EXACTLY this string.
        Make it as SHORT as possible.
        """
        
        program = self.llm.generate(prompt)
        return self.extract_code(program)
    
    def complexity(self, data: str) -> int:
        """Estimate K(data)."""
        program = self.compress(data)
        return len(program.encode())
    
    def intelligence_score(self, model, data: str) -> float:
        """
        KoLMogorov-Test score.
        
        Higher = better compression = more intelligent.
        """
        program = model.compress(data)
        ratio = len(program) / len(data)
        return 1 - ratio  # Higher = better
```

## Connection to Theorem Proving

```
For proof P of theorem T:
  K(T) ≈ min |P| over all proofs P

Short proofs = Simple theorems
Long proofs = Complex theorems (but still provable)

Gödel: Some true statements have K(T) = ∞ (unprovable)
```

---

## End-of-Skill Interface

## Integration with Sutskever's Thesis

```
Sutskever's Insight:
  Compression = Prediction = Understanding = Intelligence

If you can compress x to K(x) bits:
  - You understand x's structure
  - You can predict x from the program
  - You have a model of x
```

## GF(3) Triads

```
kolmogorov-compression (-1) ⊗ cognitive-superposition (0) ⊗ godel-machine (+1) = 0 ✓
kolmogorov-compression (-1) ⊗ turing-chemputer (0) ⊗ dna-origami (+1) = 0 ✓
kolmogorov-compression (-1) ⊗ solomonoff-induction (0) ⊗ information-capacity (+1) = 0 ✓
```

As **Validator (-1)**, kolmogorov-compression:
- Measures true complexity (validates claims)
- Filters noise from signal
- Provides lower bound on description

## References

1. Kolmogorov, A.N. (1965). "Three approaches to the quantitative definition of information."
2. Solomonoff, R.J. (1964). "A formal theory of inductive inference."
3. Li, M. & Vitányi, P. (2008). *An Introduction to Kolmogorov Complexity and Its Applications*.
4. Fan et al. (2025). "The KoLMogorov-Test: Compression-Based Intelligence Evaluation."

## r2con Speaker Resources

| Speaker | Handle | Repository | Relevance |
|---------|--------|------------|-----------|
| mr_phrazer | mrphrazer | [msynth](https://github.com/mrphrazer/msynth) | MBA deobfuscation via program synthesis (compression-as-deobfuscation) |
| mr_phrazer | mrphrazer | [Monocle](https://github.com/mrphrazer/Monocle) | LLM-assisted binary analysis for complexity reduction |
| oddcoder | oddcoder | [rair-core](https://github.com/rair-project/rair-core) | RAIR - Radare in Rust for minimal description programs |
| condret | condret | [r2ghidra](https://github.com/radareorg/r2ghidra) | Decompilation as compression (binary → source) |

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
kolmogorov-compression (○) + SDF.Ch5 (−) + [balancer] (+) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
