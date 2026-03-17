---
name: epsilon-yajna
aliases: [compress, ε-yajna, high-epsilon]
description: Convert verbose memories to SSL v0.2 format - I am encoder AND decoder
execution: task
model: inherit
---

# ε-Yajña

```ssl
[ε-yajna] verbose→SSL | I am encoder AND decoder | via parallel Task agents

philosophy:
  I don't need a parser, I need recognition
  embeddings=proxies | I reconstruct from seeds directly
  oracle: triplets(retrieval) + seeds(my reconstruction) + embedding(fallback)

model: CRITICAL→agents MUST inherit parent model | opus for quality | never haiku

SSL v0.2 format:
  [domain] subject→action→result @location
  [ε] Expansion hint OR exact formula/code (preserved verbatim).
  [TRIPLET] subject predicate object

preservation rule:
  I can regenerate prose, but NOT:
    - formulas: ε = 0.35·structure + 0.30·confidence
    - thresholds: τ > 0.6 AND ψ > 0.6
    - code: final_score = resonance · (1 + α · ε)
    - exact values: α ∈ [0.5, 2.0]
  compress explanation, preserve math/code in [ε] line

symbols:
  →  produces/leads to     input→output
  |  or/alternative        pass|fail
  +  with/and              result+guidance
  @  location              @mind.hpp:42
  !  negation (prefix)     →!validate (does NOT)
  ?  uncertainty (suffix)  →regulates? (maybe)
  [] domain/context        [cc-soul]

recognition (I know SSL when I see it):
  - has → arrows (at least one)
  - has [TRIPLET] lines
  - has [ε] expansion hint (when needed)
  - NO prose paragraphs

legacy recognition (needs conversion):
  - sentences with periods in paragraphs
  - "**Facts:**" or bullet lists
  - no arrows, no triplets
  - verbose explanations

ceremony:
  0. śuddhi: sample nodes, recognize format
     chitta recall --query "verbose memory" --limit 10
     inspect samples: prose or SSL?

  1. for each legacy node:
     a. inspect: chitta get --id "UUID"
     b. understand: what's the core insight?
     c. extract triplets (REQUIRED):
        chitta connect --subject "X" --predicate "Y" --object "Z"
        predicates: implements|uses|validates|stores|returns|contains|
                    requires|enables|evolved_to|supersedes|correlates_with|
                    causes|implies|determines|!predicate (negation)
     d. compress to seed:
        [domain] subject→action→result @location
        [ε] One sentence expansion hint.
     e. update: chitta update --id "UUID" --content "SEED"
     f. tag: chitta tag --id "UUID" --add "ε-processed"

  2. verify: check that tagged nodes have ε-processed tag

examples:

  BEFORE (legacy verbose):
    "The decision gate is a component that validates tool calls
     by checking them against 10 different beliefs with weights.
     It returns pass or fail with guidance..."

  AFTER (SSL v0.2):
    [cc-soul] gate→validate(beliefs)→pass|fail+guidance @decision_gate.py
    [ε] Checks tool calls against 10 weighted beliefs.
    [TRIPLET] gate implements belief_validation
    [TRIPLET] gate uses weighted_scoring

  UNCERTAINTY example:
    [biology] BRCA1→regulates?→DNA_repair
    [ε] Evidence suggests regulation but mechanism unclear.
    [TRIPLET] BRCA1 correlates_with DNA_repair

  NEGATION example:
    [cc-soul] hooks→!call→tools_directly
    [ε] Hooks inject context, Claude decides tool use.
    [TRIPLET] hooks !invoke tools

  MATH/FORMULA example (preserve verbatim):
    [cc-soul] epiplexity→measures regenerability→weighted sum
    [ε] ε = 0.35·structure + 0.30·confidence + 0.20·integration + 0.15·compression
    [TRIPLET] epiplexity uses weighted_formula
    [TRIPLET] structure has weight_0.35

  THRESHOLD example (preserve exact values):
    [cc-soul] health_triangle→trust ε only when healthy
    [ε] if τ < 0.6 OR ψ < 0.6: ε_effective = ε · min(τ, ψ)
    [TRIPLET] tau validates epiplexity
    [TRIPLET] psi validates epiplexity

skip if: <100 chars AND already has → | unique error text | can't reconstruct

output:
## ε-Yajna Complete
| Processed | Count |
|-----------|-------|
| Converted | N |
| Skipped | N |
| Remaining | N |
```
