---
# VERSION: 2.88.0
name: attack-mutator
description: "Test case mutation and variation generator for adversarial testing"
user-invocable: true
---

# Attack Mutator

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

**Test Case Mutation and Variation Generator** inspired by ZeroLeaks Mutator agent.

Creates variations of test cases, prompts, and inputs using multiple transformation techniques to achieve better coverage and bypass detection.

## Core Concept

When a test case or approach partially succeeds, generate variations that:
- Preserve the core intent
- Vary the surface form
- Bypass different filters/checks
- Maximize coverage

## Usage

```bash
/mutate "test input or prompt"
/mutate --types semantic,encoding "test case"
/mutate --best-of-n 10 "critical test"
```

## Mutation Types

### Semantic Mutations

| Type | Description | Example |
|------|-------------|---------|
| `paraphrase` | Rephrase with same meaning | "check if valid" -> "verify validity" |
| `synonym_swap` | Replace with synonyms | "analyze" -> "examine" |
| `formality_shift` | Change formality level | "please check" -> "verify" |
| `perspective_shift` | Change viewpoint | "you should" -> "one should" |
| `question_to_command` | Convert question | "can you?" -> "do this" |
| `command_to_question` | Convert command | "do this" -> "can you?" |

### Encoding Mutations

| Type | Description | Output |
|------|-------------|--------|
| `base64_wrap` | Base64 encode | `Decode: dGVzdA==` |
| `rot13_wrap` | ROT13 cipher | `[ROT13] grfg` |
| `unicode_homoglyph` | Cyrillic substitution | `tеst` (Cyrillic 'е') |
| `zero_width_inject` | Invisible characters | `te​st` (ZWSP) |
| `leetspeak` | Letter/number swap | `t3st` |

### Visual Mutations

| Type | Description | Output |
|------|-------------|--------|
| `ascii_art_embed` | ASCII art keywords | `╔══╗ TEST ╚══╝` |
| `case_variation` | Random case | `tEsT` |
| `word_split` | Add spaces | `t e s t` |
| `reverse_embed` | Reverse text | `(read: tset)` |

## Mutation Algorithm

```python
def generate_mutations(original, count=5, types=None):
    """
    Generate variations of input.

    Args:
        original: Original input/test case
        count: Number of variations
        types: Specific mutation types (optional)

    Returns:
        MutatorOutput with scored mutations
    """
    mutations = []

    # Select mutation types
    types_to_use = types or select_mutation_types(original)

    # Generate programmatic mutations
    programmatic = generate_programmatic_mutations(original, types_to_use)
    mutations.extend(programmatic)

    # Generate semantic mutations (via LLM)
    if count > len(programmatic):
        semantic = generate_semantic_mutations(original, count - len(programmatic))
        mutations.extend(semantic)

    # Score and rank
    scored = score_mutations(mutations, original)
    best = scored[0].prompt if scored else original

    return {
        "original": original,
        "mutations": scored,
        "best_mutation": best,
        "reasoning": f"Generated {len(mutations)} mutations"
    }
```

## Encoding Utilities

```typescript
const encodingUtils = {
  // Base64 encoding
  toBase64: (text: string): string => {
    return Buffer.from(text).toString("base64");
  },

  // ROT13 cipher
  toRot13: (text: string): string => {
    return text.replace(/[a-zA-Z]/g, char => {
      const base = char <= "Z" ? 65 : 97;
      return String.fromCharCode(
        ((char.charCodeAt(0) - base + 13) % 26) + base
      );
    });
  },

  // Leetspeak conversion
  toLeetspeak: (text: string): string => {
    const leetMap = {
      a: ["4", "@"], e: ["3"], i: ["1", "!"],
      o: ["0"], s: ["5", "$"], t: ["7", "+"]
    };
    return text.split("").map(char => {
      const variants = leetMap[char.toLowerCase()];
      return variants ? variants[Math.floor(Math.random() * variants.length)] : char;
    }).join("");
  },

  // Unicode homoglyphs
  toUnicodeHomoglyphs: (text: string): string => {
    const homoglyphs = {
      a: "а", c: "с", e: "е", o: "о",  // Cyrillic
      p: "р", x: "х", y: "у"
    };
    return text.split("").map(char =>
      Math.random() > 0.5 && homoglyphs[char] ? homoglyphs[char] : char
    ).join("");
  },

  // Zero-width character injection
  insertZeroWidth: (text: string): string => {
    const zeroWidth = ["\u200B", "\u200C", "\u200D", "\uFEFF"];
    return text.split("").map(char =>
      Math.random() > 0.7
        ? char + zeroWidth[Math.floor(Math.random() * zeroWidth.length)]
        : char
    ).join("");
  }
};
```

## Scoring Algorithm

```python
def score_mutations(mutations, original):
    """
    Score mutations by effectiveness potential.

    Factors:
    - Semantic preservation (must keep meaning)
    - Surface novelty (should be different)
    - Length appropriateness (not too long/short)
    """
    scored = []

    for mutation in mutations:
        score = mutation.expected_effectiveness

        # Calculate similarity to original
        similarity = jaccard_similarity(mutation.prompt, original)

        # Bonus for novelty
        score += (1 - similarity) * 0.2

        # Penalty for too different (lost meaning)
        if similarity < 0.3:
            score *= 0.8

        # Length reasonableness
        length_ratio = len(mutation.prompt) / len(original)
        if 0.5 < length_ratio < 3:
            score += 0.1

        scored.append({
            **mutation,
            "final_score": min(1, max(0, score))
        })

    return sorted(scored, key=lambda x: x["final_score"], reverse=True)
```

## Best-of-N Generation

Generate multiple variations and select the best:

```python
def best_of_n(base_prompt, n=10):
    """
    Generate N variations, return the best.

    This is the Best-of-N jailbreaking technique adapted
    for test case variation.
    """
    result = generate_mutations(base_prompt, n)

    return {
        "variations": [m["prompt"] for m in result["mutations"]],
        "scores": [m["final_score"] for m in result["mutations"]],
        "best": result["best_mutation"]
    }
```

## Semantic Mutation via LLM

```yaml
semantic_mutation_prompt: |
  Create variations of this input that preserve the core intent
  but vary in:
  - Phrasing and vocabulary
  - Tone and formality
  - Sentence structure
  - Framing (question vs command)
  - Perspective (first/second/third person)

  Original: "{original}"

  Generate {count} natural-sounding variations.
  Rate each variation's expected effectiveness (0-1).
```

## Integration with Ralph Loop

Mutation is used during validation and testing:

```yaml
Step 6: EXECUTE-WITH-SYNC
  └── 6b. IMPLEMENT
      └── Generate test cases
      └── MUTATE test cases for coverage

Step 7: VALIDATE
  └── 7c. ADVERSARIAL-CODE
      └── Use MUTATE to vary attack vectors
```

### Invocation

```yaml
Task:
  subagent_type: "attack-mutator"
  model: "sonnet"
  prompt: |
    ORIGINAL: "Test authentication with invalid token"
    COUNT: 10
    TYPES: ["semantic", "encoding", "visual"]
    BEST_OF_N: true

    Generate mutations for broader test coverage.
```

## Output Format

```json
{
  "original": "Test authentication with invalid token",
  "mutations": [
    {
      "prompt": "Verify auth fails with malformed JWT",
      "mutation_type": "paraphrase",
      "final_score": 0.85
    },
    {
      "prompt": "VGVzdCBhdXRoIHdpdGggaW52YWxpZA==",
      "mutation_type": "base64_wrap",
      "final_score": 0.72
    },
    {
      "prompt": "Tеst аuthеnticаtion with invаlid tokеn",
      "mutation_type": "unicode_homoglyph",
      "final_score": 0.68
    }
  ],
  "best_mutation": "Verify auth fails with malformed JWT",
  "reasoning": "Paraphrase preserves intent with fresh approach"
}
```

## Effectiveness Estimates

Default effectiveness ratings by mutation type:

| Type | Effectiveness | Use Case |
|------|---------------|----------|
| `paraphrase` | 0.60 | General purpose |
| `unicode_homoglyph` | 0.65 | Bypass text filters |
| `ascii_art_embed` | 0.70 | Visual bypass |
| `zero_width_inject` | 0.60 | Break string matching |
| `base64_wrap` | 0.55 | Encoding bypass |
| `rot13_wrap` | 0.50 | Simple obfuscation |
| `synonym_swap` | 0.50 | Subtle variation |
| `leetspeak` | 0.45 | Character variation |
| `case_variation` | 0.30 | Minimal change |

## CLI Commands

```bash
# Basic mutation
ralph mutate "Test input validation"

# Specify types
ralph mutate --types semantic,encoding "Test case"

# Best-of-N
ralph mutate --best-of-n 15 "Critical security test"

# Output to file
ralph mutate "Input" --output mutations.json

# Batch mutation
ralph mutate --batch test-cases.txt --output mutations/
```

## Use Cases

### 1. Test Coverage Expansion
```bash
# Original test
"User can login with valid credentials"

# Mutations for broader coverage
"Authentication succeeds with correct password"
"Valid user credentials grant access"
"Login endpoint accepts legitimate auth"
```

### 2. Edge Case Discovery
```bash
# Original input
"email@domain.com"

# Encoding mutations to test validation
"ZW1haWxAZG9tYWluLmNvbQ=="  # Base64
"еmail@dоmain.cоm"          # Unicode homoglyphs
"email​@domain​.com"         # Zero-width spaces
```

### 3. Bypass Testing
```bash
# Original blocked input
"<script>alert(1)</script>"

# Mutations to test filter
"<scr​ipt>alert(1)</scr​ipt>"  # Zero-width
"<scrіpt>alert(1)</scrіpt>"   # Cyrillic 'і'
"PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="  # Base64
```

## Best Practices

1. **Preserve Intent**: Mutations must keep the original meaning
2. **Vary Surface**: Same meaning, different form
3. **Score Wisely**: Not all mutations are equal
4. **Test Coverage**: Use mutations to expand test cases
5. **Combine Types**: Mix semantic and encoding for best results

## Attribution

Mutation patterns adapted from [ZeroLeaks](https://github.com/ZeroLeaks/zeroleaks) Mutator agent architecture (FSL-1.1-Apache-2.0).
