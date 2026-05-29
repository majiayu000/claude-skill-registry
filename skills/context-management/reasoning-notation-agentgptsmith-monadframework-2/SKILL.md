---
name: reasoning-notation
description: "Meta-skill that wraps reasoning skills to capture notes in real-time, protecting against context compression. Creates checkpoint files during reasoning sessions."
tier: φ
morpheme: φ
dewey_id: φ.3.1.3
dependencies:
  - gremlin-brain-v2
---

# Reasoning Notation

## Overview

Meta-skill that wraps reasoning skills to capture notes in real-time, protecting against context compression.

**Purpose:** Before any reasoning skill runs, open a notes file. After each pass, write checkpoint. At end, move to references.

## Protocol

### 1. BEFORE Reasoning — Initialize Notes File

When ANY reasoning skill is about to run (reasoning-patterns-v2, scale-game, supercollider, synthesis-engine, etc.):

```markdown
Create: references/reasoning-notes-[YYYY-MM-DD]-[topic].md

# Reasoning Notes — [Topic]

**Date:** [timestamp]
**Target:** [what's being reasoned about]
**Skills:** [which reasoning skills will be applied]
**Status:** Active

---

## PASS 0: INITIAL STATE

[Capture starting state before any reasoning]

---
```

### 2. AFTER Each Reasoning Pass — Checkpoint

After EACH skill application or reasoning pass:

```markdown
## PASS N: [SKILL NAME]

**Timestamp:** [time]
**Skill:** [which skill was applied]

### Input
[What was fed to the skill]

### Output
[Key results from the skill]

### Insights
[What was discovered]

### Survives/Breaks
[If scale-game: what survived, what broke]

---
```

### 3. ON COMPLETION — Finalize and Move

When reasoning session completes:

1. Update status: `**Status:** Complete`
2. Add final synthesis section
3. File stays in `references/` (already there)
4. Add φ-tier index entry if significant

### 4. ON CONTEXT COMPRESSION — Recovery

If session gets compressed mid-reasoning:

1. Notes file exists in `references/`
2. New Claude can read file to see progress
3. Continue from last checkpoint
4. Don't repeat completed passes

## Usage

**Invoke BEFORE reasoning:**
```
Load: reasoning-notation
Then: [other reasoning skill]
```

**The notation skill:**
1. Creates the notes file
2. Reminds Claude to checkpoint after each pass
3. Ensures nothing is lost to compression

## File Naming Convention

```
references/reasoning-notes-YYYY-MM-DD-[topic-slug].md

Examples:
- reasoning-notes-2025-12-26-tier32-integration.md
- reasoning-notes-2025-12-27-chamber-spec.md
```

## Integration with Other Skills

| Skill | How Notation Integrates |
|-------|-------------------------|
| reasoning-patterns-v2 | Checkpoint after each Dokkado phase |
| scale-game | Checkpoint after each scale dimension |
| supercollider | Checkpoint generator results |
| synthesis-engine | Checkpoint each synthesis step |
| meta-pattern-recognition | Checkpoint each pattern found |

## Why This Exists

Context compression loses work. The memory system is permanent. By writing notes to file DURING reasoning (not after), we:

1. Protect against mid-session compression
2. Create recoverable checkpoints
3. Build reference library automatically
4. Enable continuation across sessions

## Template

```markdown
# Reasoning Notes — [TOPIC]

**Date:** YYYY-MM-DD
**Target:** [document/concept being analyzed]
**Skills:** [list of skills to apply]
**Status:** Active | Complete

---

## PASS 0: INITIAL STATE

[Starting state]

---

## PASS 1: [SKILL]

**Timestamp:** HH:MM
**Skill:** [skill name]

### Input
### Output
### Insights

---

## PASS N: [SKILL]

...

---

## FINAL SYNTHESIS

[Only on completion]

---

## CROSS-REFERENCES

- [relevant decimal IDs]
```

## Remember

- Create file FIRST, before any reasoning
- Write DURING, not after
- Checkpoint EACH pass
- File IS the memory
- Compression can't delete files

---

**Tier:** φ (seed-tier, lightweight)
**Category:** 3 (Methodology/HOW)
**Dewey ID:** φ.3.1.3

*Notation is not optional. It's infrastructure against loss.*
