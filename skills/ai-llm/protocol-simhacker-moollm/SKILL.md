---
name: protocol
description: "K-lines as semantic activation — the name activates the tradition."
license: MIT
tier: 0
allowed-tools:
  - read_file
related: [k-lines, naming, skill, bootstrap, yaml-jazz]
tags: [moollm, meta, naming, k-line, minsky, semantic]
credits:
  - "Marvin Minsky — K-lines, Society of Mind (1986)"
---

# PROTOCOL

> **"The name activates the tradition."**

K-lines as semantic activation. When you invoke a protocol by name, you activate an entire constellation of knowledge and behavior.

---

## Core Concept

A **protocol** is a named pattern that the LLM already knows. Invoking it by name activates that knowledge without needing to repeat it.

### Why This Works

```yaml
# Traditional approach: Explain everything
"When writing YAML, use natural keys, add comments for humans and LLMs,
keep structure flexible, use semantic naming, allow improvisation..."
# [500 tokens of explanation]

# K-line approach: Name activates pattern
> Apply YAML-JAZZ

# The LLM already knows. One name = 500 tokens compressed.
```

### Minsky's Insight

> "A K-line is a wirelike structure that attaches itself to whichever mental agents are active when you solve a problem. When activated later, those agents are partially activated, creating a similar mental state."
> — Marvin Minsky, *Society of Mind* (1986)

**MOOLLM protocols ARE K-lines.** The name IS the activation vector.

---

## Methods

### INVOKE

Activate a protocol by name.

```yaml
> INVOKE POSTEL
# Activates: "Be liberal in what you accept, conservative in what you emit"
# Plus: ASK when uncertain, robustness principles, defensive parsing
```

### DEFINE

Create a new protocol.

```yaml
> DEFINE WAFFLE-PARTY AS "Celebratory gathering requiring Form WP-7"
# Now WAFFLE-PARTY is a K-line that activates this context
```

### LIST

Show available protocols.

```yaml
> LIST PROTOCOLS
ADVENTURE, BOOTSTRAP, INCARNATION, POSTEL, PSIBER,
SPEED-OF-LIGHT, YAML-JAZZ, ...
```

### K-REF

Emit a file pointer with metadata.

```yaml
Format: PATH[:LINE[-END]][#anchor][?search] # TYPE - DESC

Examples:
/path/file.txt:42 # secret 🔴
/path/screenshot.png # image - Cursor can read!
/path/schema.yml#field.name # k-line
@central/apps/insights/brain/Schema.py:142-200 # code - Schema class
```

---

## K-REF Format

Full syntax:
```
PATH[:LINE[-END]][#anchor][?search] # TYPE - DESC
```

| Component | Purpose | Example |
|-----------|---------|---------|
| `PATH` | File location | `/path/file.yml` |
| `:LINE` | Specific line | `:42` |
| `[-END]` | Line range | `:42-67` |
| `#anchor` | YAML path / section | `#field.name` |
| `?search` | Search term | `?error` |
| `# TYPE` | Content type | `# secret`, `# image` |
| `- DESC` | Description | `- The Schema class` |

**Special types:**
- `# secret 🔴` — Sensitive content
- `# image` — Cursor can read images from absolute paths!
- `# k-line` — Semantic activation point
- `# code` — Source code reference

---

## SISTER-SCRIPT Pattern

Tools emit K-REFs, LLM reads selectively.

### The Pattern

```python
# Tool (Python/shell) runs and emits:
print("/logs/2026-01-28.log:147 # error - Database timeout")
print("/logs/2026-01-28.log:892 # error - Memory exhausted")
print("/logs/2026-01-28.log:1203 # warning - Slow query")
print("/config/db.yml # config - Database settings")
```

### LLM Behavior

1. Scans the K-REF list
2. Decides which to read based on task
3. Reads only relevant files/sections
4. Avoids loading everything

**Key insight:** Scan and point, not dump.

---

## Core Protocols

| Protocol | Activates |
|----------|-----------|
| `ADVENTURE` | Text adventure patterns, room navigation |
| `YAML-JAZZ` | Flexible YAML with semantic comments |
| `BOOTSTRAP` | Session startup, context assembly |
| `PSIBER` | Data as navigable room (HyperCard heritage) |
| `POSTEL` | Liberal accept, conservative emit, ASK |
| `INCARNATION` | Gold-standard character creation |
| `SPEED-OF-LIGHT` | Many turns in one LLM call |
| `HERO-STORY` | Safe real-person references |
| `TREKIFICATION` | Privacy masking protocol |

---

## Protocol Activation Cascade

When you invoke a protocol, related concepts activate:

```yaml
> INVOKE YAML-JAZZ

# Activates:
- yaml-jazz/SKILL.md content
- Related: POSTEL (be liberal), plain-text (forever accessible)
- Patterns: Semantic comments, natural keys, improvisational structure
- Anti-patterns: Cryptic keys, missing comments, rigid schemas
- Emotional tone: Jazzy, playful, improvisational
```

This is why K-lines are so powerful — one name activates a **network** of knowledge.

---

## Why Tier 0

This skill is **tier 0** because:
- It's foundational to all other skills
- Every skill name IS a protocol
- Understanding K-lines is essential to understanding MOOLLM

---

## Dovetails With

- [../k-lines/](../k-lines/) — Naming conventions and K-line formatting
- [../naming/](../naming/) — Big-endian semantic file naming
- [../skill/](../skill/) — Skills are invokable protocols
- [../bootstrap/](../bootstrap/) — Session startup protocol
- [../yaml-jazz/](../yaml-jazz/) — The YAML-JAZZ protocol

---

*"Speak the name. Become the pattern."*
