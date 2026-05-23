---
name: skill-specification
description: Agent Skills formal specification for cross-platform compatibility. Ensures skills are evolutionarily robust across Claude, Codex, Cursor, Amp, and future agents.
version: 1.0.0
---


# Skill Specification

Formal specification for evolutionarily robust agent skills.

## Why This Matters

Skills that follow the spec work across:
- **Claude Code** (Anthropic)
- **Codex CLI** (OpenAI)
- **Cursor** (Anysphere)
- **Amp** (Sourcegraph)
- **Letta** (memGPT)
- Future agents

Non-compliant skills break silently or fail validation.

## SKILL.md Schema

```yaml
---
name: skill-name              # REQUIRED: lowercase, hyphens, 1-64 chars
description: What and when    # REQUIRED: max 1024 chars, no < or >
license: Apache-2.0           # optional
compatibility: Requires git   # optional, max 500 chars
metadata:                     # optional: custom key-value pairs
  trit: 0
  author: bmorphism
  version: "1.0"
allowed-tools: Bash Read      # optional, experimental
---

# Body content (Markdown)
```

## Field Constraints

| Field | Required | Rules |
|-------|----------|-------|
| `name` | ✓ | `[a-z0-9-]+`, no `--`, no leading/trailing `-`, max 64 |
| `description` | ✓ | 1-1024 chars, no `<` or `>`, includes WHEN to use |
| `license` | ✗ | Short name or file reference |
| `compatibility` | ✗ | Environment requirements, max 500 |
| `metadata` | ✗ | Arbitrary k:v for custom fields |
| `allowed-tools` | ✗ | Space-delimited tool names |

## Evolutionary Robustness Patterns

### 1. Progressive Disclosure

```
Level 1: name + description (~100 tokens) - loaded at startup
Level 2: SKILL.md body (<5000 tokens) - loaded on activation
Level 3: scripts/, references/, assets/ - loaded on demand
```

Keep SKILL.md under 500 lines. Move details to `references/`.

### 2. Cross-Platform Compatibility

```yaml
# BAD - platform-specific
allowed-tools: claude_desktop_mcp

# GOOD - generic capability
compatibility: Requires MCP server access
```

### 3. Self-Validation Hook

Include validation in your skill:

```bash
# scripts/validate.sh
skills-ref validate "$(dirname "$0")/.."
```

### 4. Semantic Versioning in Metadata

```yaml
metadata:
  version: "2.1.0"
  breaking-changes: "v2.0 changed API"
```

### 5. Triadic Classification (GF(3) Extension)

For plurigrid/asi skills:

```yaml
metadata:
  trit: -1   # MINUS: verification, constraint
  trit: 0    # ERGODIC: balance, mediation
  trit: +1   # PLUS: generation, exploration
```

Conservation: `Σ trits ≡ 0 (mod 3)` across compositions.

## Directory Structure

```
skill-name/
├── SKILL.md           # Required
├── scripts/           # Executable code
│   └── main.py
├── references/        # Additional docs
│   └── REFERENCE.md
└── assets/            # Static resources
    └── template.json
```

## Validation Commands

```bash
# Official validator
skills-ref validate ./my-skill

# Codex-rs validator
python3 codex-rs/core/src/skills/assets/samples/skill-creator/scripts/quick_validate.py ./my-skill

# Batch validate
for d in skills/*/; do skills-ref validate "$d"; done
```

## Common Failures

| Error | Fix |
|-------|-----|
| No YAML frontmatter | Add `---` delimiters |
| Unexpected keys | Move to `metadata:` |
| Angle brackets in description | Remove `<` and `>` |
| Name not hyphen-case | Lowercase, hyphens only |
| Description too long | Max 1024 chars |
| YAML colon in value | Quote the string |

## Evolution Strategy

1. **Start minimal** - name + description + one paragraph
2. **Add scripts/** when automation helps
3. **Add references/** when body exceeds 300 lines
4. **Add metadata** for custom classification
5. **Validate on every commit** via CI

## References

- [agentskills.io/specification](https://agentskills.io/specification)
- [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills/)
- [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.