---
name: pijul
description: Pijul patch-based VCS with categorical patch theory for skill versioning
version: 1.0.0
trit: -1
role: MINUS
color: "#4393DE"
source: flox install pijul
---

# pijul

Patch-based version control with mathematically sound commutative patch theory.

**Trit**: -1 (MINUS) - Validator role for patch verification and merge correctness

---

## Overview

Pijul is a distributed VCS where patches are first-class citizens that commute when independent. This maps directly to:
- **GF(3) skill derivation chains**: patches as morphisms between skill states
- **Pushouts = merges**: categorical semantics for conflict resolution
- **Sparsity preservation**: changes stored as morphisms, not materialized states

---

## Installation via flox-mcp

```bash
# Using flox CLI
flox install pijul

# Via MCP (flox_install tool)
{"name": "flox_install", "arguments": {"package": "pijul"}}
```

---

## Core Commands

### Repository Operations

```bash
# Initialize
pijul init

# Clone (partial clone supported!)
pijul clone https://nest.pijul.com/user/repo
pijul clone --partial https://nest.pijul.com/user/repo  # sparse clone

# Record changes (creates patch)
pijul record -m "Add feature"

# Push/Pull
pijul push
pijul pull
```

### Patch Operations

```bash
# List patches (changes)
pijul log

# Show patch contents
pijul diff

# Apply specific patch
pijul apply <hash>

# Unapply (revert) patch
pijul unrecord <hash>

# Fork (branch)
pijul fork <name>

# Switch channel (branch)
pijul channel switch <name>
```

### Sparse Operations

```bash
# Partial clone - only fetch needed patches
pijul clone --partial <url>

# Fetch specific patches
pijul pull --from-channel <channel>

# Lazy evaluation - patches fetched on demand
pijul reset --lazy
```

---

## Categorical Patch Theory

### Patches as Morphisms

```
State_A --patch_1--> State_B --patch_2--> State_C
                                    
If patch_1 ⊥ patch_2 (independent):
  patch_1 ; patch_2 = patch_2 ; patch_1
```

### Pushout for Merges

```
     State_A
      /   \
   p_1     p_2
    /       \
State_B    State_C
    \       /
     p_2'  p_1'
      \   /
     State_D (pushout)
```

When patches are independent, their pushout is unique and well-defined.

---

## GF(3) Integration

### Sparse Mode (Default)

```
trit == -1 or +1: Store as morphism (patch)
  - No materialization
  - Lazy evaluation
  - Minimal storage
```

### Projection Mode (ERGODIC Gate)

```
trit == 0: Force materialization
  - Coordination point
  - Full state snapshot
  - Archive checkpoint
```

### Projection Triggers

1. `--materialize` flag explicit
2. `trit == 0` (ERGODIC coordination)
3. Explicit archive command
4. Conflict resolution requiring full state

---

## Skill Versioning Pattern

### Record Skill Change

```bash
cd .agents/skills/my-skill
pijul record -m "Add GF(3) frontmatter"
```

### Sync with Upstream

```bash
# Sparse pull - only new patches
pijul pull --partial

# Check for conflicts
pijul log --pending
```

### Fork for Experimentation

```bash
pijul fork experiment
pijul channel switch experiment
# ... make changes ...
pijul record -m "Experimental patch"

# Merge back if successful
pijul channel switch main
pijul pull --from-channel experiment
```

---

## Integration with flox

### Install via flox Environment

```toml
# manifest.toml
[install]
pijul.pkg-path = "pijul"
```

### Activate and Use

```bash
flox activate
pijul --version
```

### MCP Tool Call

```json
{
  "name": "flox_install",
  "arguments": {"package": "pijul"}
}
```

---

## References

- [Pijul Manual](https://pijul.org/manual/)
- [Nest (Pijul Forge)](https://nest.pijul.com)
- Mimram/Di Giusto: Categorical Patch Theory
- Delta-State CRDTs / Merkle Search Trees
- [flox-mcp skill](../flox-mcp/SKILL.md)
- [structured-decomp skill](../structured-decomp/SKILL.md)

---

## Triadic Composition

```
pijul (-1)  + flox-mcp (0)  + skill-creator (+1) = 0 ✓
Validator     Coordinator     Generator
```

Pijul validates patch correctness, flox-mcp coordinates environment, skill-creator generates new skills.

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
pijul (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch5: Evaluation
- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
