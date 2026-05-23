---
name: lean4-prove
description: >
  Retrieval-augmented Lean4 proof generation. Queries 94k+ exemplars from DeepSeek-Prover V1+V2,
  uses hybrid search (BM25 + semantic + graph), generates via Claude, compiles in Docker, retries on failure.
allowed-tools: Bash, Read, Docker
triggers:
  - prove this
  - lean4 proof
  - generate proof
  - verify lean4
  - lean4-prove
  - formalize this requirement
metadata:
  short-description: Retrieval-augmented Lean4 proof generation
---

# lean4-prove

Retrieval-augmented Lean4 proof generation for engineering requirements. Uses 94,000+ proven theorems from DeepSeek-Prover V1+V2 to guide proof synthesis via hybrid search (BM25 + semantic + graph traversal).

## Architecture

```
Requirement + Tactics + Persona
        │
        ▼
┌───────────────────────────┐
│ 1. RECALL similar proofs  │  ← Hybrid search on ArangoDB
│    from 94k+ exemplars    │     (BM25 + semantic + graph)
└───────────────────────────┘
        │
        ▼
┌───────────────────────────┐
│ 2. BUILD support pack     │
│    - Validated imports    │
│    - Tactic patterns      │
│    - Similar proofs       │
└───────────────────────────┘
        │
        ▼
┌───────────────────────────┐
│ 3. GENERATE N candidates  │  ← Claude with exemplar context
│    constrained by corpus  │
└───────────────────────────┘
        │
        ▼
┌───────────────────────────┐
│ 4. COMPILE each in        │  ← lean_runner Docker
│    lean_runner container  │
└───────────────────────────┘
        │
   ┌────┴────┐
   │         │
 Success   Failure
   │         │
   ▼         ▼
 Return   Retry with error feedback
          (up to max_retries)
```

## Why Retrieval-Augmented?

1. **Determinism** - Exact provenance: "used these 3 proofs as templates"
2. **Version alignment** - Exemplars use imports that actually work
3. **Fewer hallucinations** - Constrained to lemmas that exist
4. **Tactic idioms** - Transfers working `simp` sets and proof patterns

## Usage

```bash
# Basic proof
./run.sh --requirement "Prove n + 0 = n"

# With tactics preference
./run.sh -r "Prove commutativity of addition" -t "simp,ring,omega"

# With persona context
./run.sh -r "Prove message integrity" -p "cryptographer"

# Via stdin (JSON)
echo '{"requirement": "Prove n + 0 = n", "tactics": ["rfl"]}' | ./run.sh

# Custom settings
./run.sh -r "Prove theorem" --candidates 5 --retries 5 --model claude-sonnet-4-20250514
```

## Output

```json
{
  "success": true,
  "code": "import Mathlib\n\ntheorem list_append_length (xs ys : List α) :\n    (xs ++ ys).length = xs.length + ys.length := by\n  induction xs with\n  | nil => simp\n  | cons x xs ih => simp [List.cons_append, ih]",
  "attempts": 1,
  "candidate": 0,
  "errors": null,
  "retrieval": {
    "retrieved": 5,
    "tactics_added": ["simp", "aesop", "norm_num", "intro"],
    "imports_count": 3
  }
}
```

On failure:

```json
{
  "success": false,
  "code": null,
  "attempts": 9,
  "errors": [
    "Candidate 0 attempt 1: unknown identifier 'natAdd'",
    "Candidate 1 attempt 1: type mismatch..."
  ],
  "retrieval": {
    "retrieved": 5,
    "tactics_added": ["simp", "exact"],
    "imports_count": 3
  }
}
```

## Parameters

| Parameter           | Default                  | Description                       |
| ------------------- | ------------------------ | --------------------------------- |
| `--requirement, -r` | (required)               | Theorem to prove                  |
| `--tactics, -t`     | none                     | Comma-separated preferred tactics |
| `--persona, -p`     | none                     | Persona context for generation    |
| `--candidates, -n`  | 3                        | Parallel proof candidates         |
| `--retries`         | 3                        | Max retries per candidate         |
| `--model`           | claude-sonnet-4-20250514 | Claude model                      |
| `--container`       | lean_runner              | Docker container name             |
| `--timeout`         | 120                      | Compilation timeout (seconds)     |

## Environment Variables

```bash
# Proof generation
LEAN4_CONTAINER=lean_runner      # Docker container
LEAN4_TIMEOUT=120                # Compile timeout
LEAN4_MAX_RETRIES=3              # Retries per candidate
LEAN4_CANDIDATES=3               # Parallel candidates
LEAN4_PROVE_MODEL=opus           # Claude model (opus recommended for proofs)

# Retrieval (requires ArangoDB with ingested dataset)
LEAN4_RETRIEVAL=1                # Enable/disable retrieval (default: 1)
LEAN4_RETRIEVAL_K=5              # Number of exemplars to retrieve
ARANGO_URL=http://127.0.0.1:8529 # ArangoDB connection
ARANGO_DB=memory                 # Database name (same as memory skill)
```

## Dataset Setup

The skill uses 94,000+ theorems from DeepSeek-Prover V1+V2 for retrieval:
- **V1**: 27,503 theorems (`status: "proven"`)
- **V2**: 66,708 theorems (`status: "ok"` for 11,689 proven + others)

One-time ingest:

```bash
# Ingest full dataset (~5 min)
./ingest.sh

# Or limit for testing
./ingest.sh --limit 1000
```

This populates the `lean_theorems` collection in ArangoDB with:
- `formal_statement` - The theorem statement
- `formal_proof` - Working proof code
- `header` - Validated imports (Mathlib, Aesop, etc.)
- `tactics` - Extracted tactic names
- `source` - "deepseek-prover-v1" or "deepseek-prover-v2"
- `status` - "proven" (V1) or "ok"/"failed"/etc. (V2)

## Authentication

Uses Claude Code CLI (`claude -p`) in headless non-interactive mode.

The CLI is called with:
- `-p` flag for print/headless mode
- `--output-format text` for plain text output
- `--max-turns 1` for single-turn operation

Environment variables `CLAUDE_CODE` and `CLAUDECODE` are cleared to avoid recursion detection when called from within Claude Code.

No separate API key required - authentication is handled via your Claude subscription.

## Requirements

1. **Docker** with `lean_runner` container running (Lean4 + Mathlib installed)
2. **Claude Code CLI** (`claude`) in PATH with valid authentication
3. **ArangoDB** running locally (for retrieval - optional but recommended)
4. **Dataset ingested** via `./ingest.sh` (one-time setup)

## Tactics

Common Lean4/Mathlib tactics to suggest:

| Tactic      | Use For                 |
| ----------- | ----------------------- |
| `rfl`       | Reflexivity proofs      |
| `simp`      | Simplification          |
| `ring`      | Ring arithmetic         |
| `omega`     | Linear arithmetic       |
| `decide`    | Decidable propositions  |
| `exact`     | Exact term construction |
| `apply`     | Apply lemmas            |
| `induction` | Inductive proofs        |

## Examples

### Engineering: List operations

```bash
./run.sh -r "Prove length(xs ++ ys) = length(xs) + length(ys)" -t "simp,induction"
```

### Engineering: State machine property

```bash
./run.sh -r "When mux_enable is false, output shall equal default_value" \
  -p "embedded systems engineer" -t "simp,cases,decide"
```

### Engineering: Protocol correctness

```bash
./run.sh -r "Prove message append preserves checksum: checksum(msg ++ data) = update(checksum(msg), data)" \
  -t "simp,induction,ring"
```

### Cryptography

```bash
./run.sh -r "Prove that XOR is self-inverse: a ⊕ a = 0" -p "cryptographer" -t "simp,decide"
```

### Complex theorem

```bash
./run.sh -r "Prove the sum of first n natural numbers equals n*(n+1)/2" \
  -t "induction,simp,ring" \
  --candidates 5 \
  --retries 5
```

## Difference from lean4-verify

| Skill          | Purpose                                                          |
| -------------- | ---------------------------------------------------------------- |
| `lean4-verify` | Compile-only. Takes Lean4 code, returns pass/fail                |
| `lean4-prove`  | Full pipeline. Takes requirement, generates + compiles + retries |

Use `lean4-verify` when you already have Lean4 code to check.
Use `lean4-prove` when you need to generate the proof from a requirement.

## Advanced: Memory Integration

The skill integrates with the memory project for hybrid retrieval (BM25 + semantic + graph traversal):

```bash
# One-time setup: embed theorems and create edges
ARANGO_PASS=yourpass ARANGO_DB=memory python integrate_memory.py
```

This creates:
- **Embeddings**: 39k+ theorem embeddings in `lesson_embeddings` for semantic search
- **Tactic edges**: 10k+ edges between theorems sharing primary tactics
- **Similarity edges**: Edges between semantically similar theorems (cosine > 0.7)

This enables:
- **Semantic search**: Find theorems by meaning, not just keywords
- **Multi-hop traversal**: "What proofs use similar tactics?"
- **Impact analysis**: "If I change lemma X, what breaks?"

### Lemma Dependency Graph (Planned)

Extract lemma dependencies during compilation to build an impact graph:

```
Query: "What's affected if mux_default changes?"

Answer:
  mux_default
    └── system_safe_state (NEEDS RE-VERIFY)
          └── requirement_42 (NEEDS RE-VERIFY)
```

### Engineering Use Cases

1. **Ambiguity detection**: Formalization fails → requirement is vague
2. **Completeness check**: "Are all state transitions covered?"
3. **Regression impact**: "Change to X affects theorems Y, Z"
4. **Cross-reference**: "Which requirements share this lemma?"
