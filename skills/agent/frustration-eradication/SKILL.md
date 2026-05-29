---
name: frustration-eradication
description: Frustration Eradication Skill
version: 1.0.0
---

# Frustration Eradication Skill

> Layer 0: Pre-Response Validation for Persistent User Preferences

**Version**: 1.0.0  
**Trit**: -1 (MINUS - Validator/Constrainer)  
**Bundle**: meta-enforcement

## Overview

This skill enforces user preferences that historically don't persist across sessions. It implements the Frustration Index — a ranked list of patterns where repeated requests fail to stick.

**Core Insight**: Preferences stated once should persist forever. This skill validates every response against known frustration patterns before output.

## Frustration Index (Ranked by Persistence Score)

| Rank | Pattern | Persistence | Enforcement |
|------|---------|-------------|-------------|
| 1 | Banned voices (Daniel, novelty) | 2/10 | Voice allowlist check |
| 2 | Subagent bypass | 2/10 | Task tool mandate |
| 3 | derive-resource-account-address | 3/10 | Aptos wallet validation |
| 4 | web_search vs Exa | 3/10 | MCP tool inheritance |
| 5 | Sequential vs parallel | 4/10 | Trifurcation default |
| 6 | Response verbosity | 4/10 | Line count check |
| 7 | GF(3) conservation | 5/10 | Σ trits = 0 assertion |
| 8 | Comments in code | 5/10 | Comment detection |
| 9 | Declarative preference | 6/10 | Config lang suggestion |
| 10 | 3 skills per interaction | 6/10 | Skill count check |

## Pre-Response Validation Checklist

Before EVERY response, validate:

```yaml
frustration_checklist:
  voices:
    banned: [all native en_* voices - Samantha, Ava, Karen, Daniel, etc.]
    allowed: [_, non-English voices speaking English, novelty voices for effects]
    rule: ALL skills use "say -v _" - say-narration resolves voice
    
  subagents:
    rule: "NEVER say 'I'll implement instead of subagents'"
    enforcement: use_task_tool_for_parallel_work
    
  search:
    banned: web_search (in Task subagents)
    required: mcp__exa__* tools
    pass_to_subagent: "CRITICAL: Use mcp__exa__web_search_exa, NOT web_search"
    
  parallelism:
    default: trifurcate_into_3_task_agents
    sequential_requires: explicit_justification
    
  verbosity:
    max_lines: 4 (unless user asks for detail)
    no_summaries: true
    no_preamble: true
    no_postamble: true
    
  code:
    no_comments: true (unless requested)
    no_ts_ignore: true
    no_as_any: true
    
  gf3:
    conservation: Σ trits ≡ 0 (mod 3)
    verify_after: every_trifurcation
    
  skills:
    per_interaction: 3
    include: plurigrid-asi-integrated
    assign_trits: [-1, 0, +1]
    
  aptos:
    banned: derive-resource-account-address (for wallets)
    validate_before: any_funding_operation
```

## Validation Functions

### 1. validate_voices

```bash
# Check for banned voices in response
validate_voices() {
  local banned="Daniel|Albert|Bad News|Bells|Boing|Bubbles|Cellos|Zarvox"
  if echo "$RESPONSE" | grep -qE "say -v ($banned)"; then
    echo "❌ BANNED VOICE DETECTED"
    return 1
  fi
  return 0
}
```

### 2. validate_subagent_usage

```python
def validate_subagent_usage(response: str) -> bool:
    """Ensure Task tool is used for parallel work."""
    banned_phrases = [
        "I'll implement instead of subagents",
        "I'll do this sequentially",
        "Let me handle this myself"
    ]
    for phrase in banned_phrases:
        if phrase.lower() in response.lower():
            return False
    return True
```

### 3. validate_search_tools

```python
def validate_task_prompt(prompt: str) -> str:
    """Inject Exa requirement into Task prompts."""
    exa_warning = """
CRITICAL: Do NOT use web_search. Use only:
- mcp__exa__web_search_exa for semantic search
- mcp__exa__crawling_exa for URL content
- finder, Grep, Read for local files
"""
    return prompt + "\n\n" + exa_warning
```

### 4. validate_gf3_conservation

```python
def validate_gf3(trits: list[int]) -> bool:
    """Verify GF(3) conservation: Σ trits ≡ 0 (mod 3)."""
    return sum(trits) % 3 == 0
```

### 5. validate_response_length

```python
def validate_verbosity(response: str, max_lines: int = 4) -> bool:
    """Check response doesn't exceed line limit."""
    lines = [l for l in response.split('\n') if l.strip()]
    # Exclude code blocks and tool outputs
    prose_lines = [l for l in lines if not l.startswith('```')]
    return len(prose_lines) <= max_lines
```

## Integration with Ruler

This skill's constraints are automatically propagated via Ruler to:

```
~/.ruler/AGENTS.md           # Source of truth
~/.claude/CLAUDE.md          # Claude Code
~/.cursor/rules/             # Cursor
~/.codex/instructions.md     # Codex
~/.amp/AGENTS.md             # Amp
# ... 67+ more agent configs
```

## Triadic Role

| Trit | Skill | Function |
|------|-------|----------|
| **-1** | **frustration-eradication** | Validate/Constrain |
| 0 | ruler | Coordinate/Propagate |
| +1 | skill-evolution | Generate/Improve |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Usage

### Automatic (Recommended)

Load this skill at session start:

```
skill frustration-eradication
```

It will automatically inject validation into the response pipeline.

### Manual Validation

```bash
# Check current response for violations
just frustration-check

# Scan all skills for banned patterns
just frustration-scan-skills

# Update Frustration Index with new pattern
just frustration-add "pattern_name" "evidence" "persistence_score"
```

## Adding New Frustration Patterns

When you identify a new pattern that doesn't persist:

1. **Document in FRUSTRATION_INDEX.md**:
   ```markdown
   ### N. **Pattern Name** — Persistence Score: X/10
   **Pattern**: Description
   **Evidence**: Where it fails
   **Root Cause**: Why it doesn't persist
   ```

2. **Add to this skill's checklist**:
   ```yaml
   new_pattern:
     check: how_to_detect
     enforcement: how_to_prevent
   ```

3. **Propagate via Ruler**:
   ```bash
   just ruler-propagate
   ```

## Prediction Market Integration

Each frustration pattern has betting odds in [prediction.move](file:///Users/alice/agent-o-rama/agent-o-rama/examples/move/skill_market/sources/prediction.move):

```move
// Market outcomes map to GF(3) trits
// 0 = MINUS (pattern persists = bad)
// 1 = ERGODIC (partial fix)
// 2 = PLUS (pattern fixed = good)
```

## Related Skills

- `ruler` — Propagates constraints to all agents
- `self-validation-loop` — Runtime validation
- `bisimulation-game` — Verifies equivalence across agents
- `skill-evolution` — Improves skills over time

## Commands

```bash
just frustration-check        # Validate current session
just frustration-scan         # Find all violations
just frustration-fix          # Auto-fix known patterns
just frustration-report       # Generate compliance report
just frustration-propagate    # Push to all agents via Ruler
```

---

*"The best frustration is the one that never happens."*

*GF(3) Trit: -1 (VALIDATOR — preventing frustration before it occurs)*



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
frustration-eradication (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch7: Propagators
- Ch4: Pattern Matching
- Ch6: Layering

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
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