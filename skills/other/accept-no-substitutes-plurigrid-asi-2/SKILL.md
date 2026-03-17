---
name: accept-no-substitutes
description: This skill should be used when agents generate placeholder tokens like "pseudo-", "mock-", "temporary", "TODO", "demo-", or similar incompleteness markers. Detects substitution patterns in agent OUTPUT and triggers mandatory user interview instead of accepting incomplete work. Activates automatically on any output containing forbidden tokens.
version: 0.1.0
metadata:
  trit: -1
  color: "#2626D8"
  role: validator
created_with:
  - skill-creator: ○ structure
  - tree-sitter: ⊕ AST detection
  - kolmogorov-compression: ⊕ compression ratio
  - chromatic-walk: ⊕ triadic search
  - code-review: ⊖ validation pattern
  - narya-proofs: ⊖ GF(3) emission
---

# Accept No Substitutes

Zero tolerance for placeholder tokens **in agent output**. Incompleteness triggers user interview.

## Purpose

Detect and reject incomplete work tokens **generated in agent output**. When uncertainty exists, ask the user rather than substitute with placeholders.

## Scope: Agent Output Only

This skill validates what agents **produce**, not existing code:
- Code being written or modified
- Prose explanations
- Configuration being generated
- Any text output from parallel agents

**NOT** for scanning existing codebases (use linters for that).

## Trit Assignment

- **Trit**: -1 (MINUS/VALIDATOR)
- **Hue**: 240° (cold blue - enforcement)
- **Role**: Constraint enforcer, substitution detector

## Forbidden Token Categories

### Prefix Substitutions
| Pattern | Examples |
|---------|----------|
| `pseudo-*` | pseudo-code, pseudo-implementation |
| `mock-*` | mock-data, mock-service |
| `fake-*` | fake-response, fake-auth |
| `stub-*` | stub-function, stub-api |
| `dummy-*` | dummy-value, dummy-handler |

### Completeness Evasions
| Token | Context |
|-------|---------|
| `temporary` | "temporary solution" |
| `placeholder` | "placeholder for now" |
| `TODO` | inline TODOs as output |
| `FIXME` | deferred fixes |
| `TBD`/`TBA` | undetermined items |
| `WIP` | work-in-progress as deliverable |

### Deferral Signals
| Pattern | Context |
|---------|---------|
| `later` | "we'll add this later" |
| `eventually` | "eventually this will..." |
| `for now` | "for now just use..." |
| `skeleton` | incomplete implementation |

### Example/Demo Evasions
| Pattern | Examples |
|---------|----------|
| `example_*` | example_config, example_key |
| `demo_*` | demo_mode, demo_data |
| `foo/bar/baz` | metasyntactic placeholders |
| `xxx`/`yyy` | marker placeholders |

## Enforcement Protocol

### On Detection

1. **HALT** - Stop generation immediately
2. **ABANDON** - Discard substituted content with complete disgust
3. **INTERVIEW** - Ask user for clarification

### Interview Template

```
Substitution detected that indicates incomplete work:
  - Token: "[detected token]"
  - Context: [what was being attempted]

This requires input:
1. What is the ACTUAL implementation needed?
2. What specific details are missing?
3. Should research be conducted before proceeding?
```

## GF(3) Integration

Operates as MINUS (-1) validator in any triad:

```
accept-no-substitutes(-1) + generator(+1) + coordinator(0) = 0
```

When generator produces substitution tokens:
- Validator REJECTS with -1
- Generator must RE-ATTEMPT with +1
- Coordinator mediates user interview at 0

## Examples

### Rejected Output (triggers interview)
```python
def authenticate(user):
    # TODO: implement actual auth
    return True  # temporary bypass
```

### Accepted Output (no substitution)
```python
def authenticate(user: User) -> AuthResult:
    credentials = vault.get_credentials(user.id)
    return verify_signature(user.token, credentials.public_key)
```

### Rejected Prose (triggers interview)
```
Here's a pseudo-implementation you can adapt...
```

### Accepted Prose (no substitution)
```
Clarification needed before implementing:
- Which authentication provider is used?
- What is the expected token format?
```

## Rationale

Placeholder tokens are **technical debt laundering**:
1. Create false sense of progress
2. Defer decisions that need making NOW
3. Accumulate into unmaintainable systems
4. Signal uncertainty that should be surfaced

**The correct response to uncertainty is asking, not substituting.**

## Integrated Detection Pipeline

### Phase 1: Regex Scan
```bash
scripts/detect.py --stdin < output.txt
```

### Phase 2: AST Check (if code)
```bash
# Invoke tree-sitter for structural detection
tree-sitter query '(comment) @comment' | grep -iE 'TODO|FIXME|placeholder'
```

### Phase 3: Compression Test
```python
# High compression ratio = likely template/placeholder
from zlib import compress
ratio = len(compress(output.encode())) / len(output)
if ratio < 0.3:  # Suspiciously compressible
    flag_as_boilerplate()
```

### Phase 4: GF(3) Emit
```python
# On detection, emit MINUS signal
emit_trit(-1, reason="substitution_detected", token=matched)
```

## Hook Integration

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": {"toolName": "Write|Edit"},
      "command": "~/.claude/skills/accept-no-substitutes/scripts/validate.sh"
    }]
  }
}
```

## MCP Bridge

Call via babashka for fast validation:
```clojure
(require '[babashka.process :refer [shell]])
(defn validate-output [text]
  (let [{:keys [exit]} (shell {:in text} "scripts/detect.py" "-")]
    (zero? exit)))
```
