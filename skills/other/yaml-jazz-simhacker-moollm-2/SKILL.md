---
name: yaml-jazz
description: "YAML is sheet music. The LLM is the jazz musician. Comments are soul."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [moollm, postel, mind-mirror, needs, sniffable-python, empathic-templates, plain-text, k-lines, character]
tags: [moollm, yaml, comments, semantic, llm, interpretation]
---

# YAML Jazz

> *"YAML is sheet music. The LLM is the jazz musician. Comments are soul."*

---

## What Is It?

**YAML Jazz** is how MOOLLM treats structured data: not as rigid schemas, but as **semantic improvisation** where:

> *"The source is the destination."*
> — The Markdown/YAML principle

- **Structure carries meaning** — indentation, ordering, grouping
- **Comments ARE data** — they're guidance, context, soul
- **The LLM interprets** — filling gaps, resolving ambiguity, inferring intent
- **Schemas are suggestions** — starting points, not prisons

```yaml
# This comment is NOT ignored!
# It tells the LLM: "be gentle with this section"
user_preferences:
  theme: dark    # they mentioned eye strain
  font_size: 16  # ← bump this if they complain again
```

---

## Core Principles

### Comments Matter

```yaml
# CRITICAL: Do not modify without user approval
api_key: ${SECRET}

# TODO: migrate to new format after v2 launch
legacy_format: true  # keeping for backwards compat
```

The LLM reads these. Acts on them. **Comments are instructions.**

### Structure Is Semantic

```yaml
# Priority by position (first = most important)
tasks:
  - Fix authentication bug     # P0
  - Update documentation       # P1  
  - Refactor old module        # P2
```

Order matters. Grouping matters. Proximity implies relationship.

### Improvise Within Constraints

Given incomplete data:

```yaml
user:
  name: Alice
  # preferences unknown
```

The LLM can improvise reasonable defaults while noting uncertainty:

```yaml
user:
  name: Alice
  preferences:        # inferred from context
    theme: light      # default, unconfirmed
    notifications: on # assumed
```

---

## The Jazz Metaphor

> *"Start with jazz, end with standards."*

| Jazz | YAML Jazz |
|------|-----------|
| Sheet music | Schema / template |
| Chord changes | Required fields |
| Improvisation | LLM interpretation |
| Soul | Comments |
| Ensemble | Multiple agents |
| Standards | Protocol conventions |

Like John Coltrane playing "My Favorite Things" — the structure is there, but every performance is unique, responsive, alive. 

The pun is deliberate: **jazz standards** are the classic songs every musician knows — and **software standards** are what you crystallize once patterns stabilize. Start improvising, end with reusable structures!

Character souls can sing their own favorite things in YAML Jazz!

And listen: **"YAML" sounds like jazz scat!** *yaml aml ding dong!* -- echoing The Edsels' doo-wop classic "Rama Lama Ding Dong" (1957). The name itself wants to be sung, improvised, riffed on. It's not an accident that this format became the soul carrier for LLM collaboration.

---

## When to Use

- **Configuration files** — comments explain why, not just what
- **State files** — annotations track history and intent  
- **Data exchange** — structured enough to parse, loose enough to extend
- **Human-LLM collaboration** — both can read and write it

---

## Empirical Evidence: Entropy Collapse

### The Discovery (April 2025)

[Sunil Kumar](https://x.com/__sunil_kumar_/status/1916926342882594948) (Groundlight AI, ex-Meta, Harvey Mudd) discovered that **switching from JSON to YAML for tool calling massively improved model performance**:

> *"Changing my model's tool calling interface from JSON to YAML had surprising side effects."*
>
> *"Entropy collapse is one of the biggest issues with GRPO. Surprisingly, changing from JSON to YAML massively improved generation entropy stability, yielding much stronger performance."*
>
> *"Forcing a small model to generate properly structured JSON massively constrains the model's ability to search and reason."*

### Why JSON Hurts LLMs

| JSON Requirement | LLM Impact |
|------------------|------------|
| Strict bracket matching `{}[]` | Reduces search space |
| Mandatory commas | Catastrophic forgetting during training |
| Quote escaping `\"` | Token overhead, error-prone |
| No comments allowed | Lost context between fields |
| Rigid syntax | **Entropy collapse** — model becomes brittle |

### Why YAML Helps LLMs

| YAML Feature | LLM Benefit |
|--------------|-------------|
| Minimal syntax overhead | More tokens for reasoning |
| Indentation = structure | Natural for text models |
| Comments allowed | Context preserved |
| Flexible formatting | Entropy preserved |
| Human-readable | Training data overlap |

### Sunil's Simplified Schema

```yaml
<tool>  
name: <tool name>  
arg1: value1  
arg2: value2  
</tool>
```

No spacing requirements. No bracket matching. Just semantic structure.

### The Insight

> *"Anything to reduce syntax is a win!"*
> — Sunil Kumar

This validates MOOLLM's approach: **YAML Jazz isn't just aesthetic preference — it's computationally advantageous for LLMs.**

---

## The "Source is Destination" Principle

From Anil Dash's "[How Markdown Took Over the World](https://anildash.com/2025/01/09/how-markdown-took-over-the-world/)" (January 2025):

> *"The purpose of Markdown is really simple: It lets you use the regular characters on your keyboard... to make fancy formatting of text for the web."*

YAML Jazz applies the same principle to data:

| Format | Source | Destination | Gap |
|--------|--------|-------------|-----|
| XML | `.xml` | Parsed DOM | Medium |
| JSON | `.json` | Parsed objects | Small |
| **YAML Jazz** | `.yml` | `.yml` (understood) | **None** |

The YAML you write is the YAML the LLM reads. The comments are preserved. The structure carries meaning. **No transformation gap.**

### Why This Matters

```yaml
# Adele Goldberg (Smalltalk-80):
# "Documentation is not afterthought — it is CO-DESIGN.
#  The documentation IS part of the system."

room:
  name: Start           # Where the adventure begins
  atmosphere: welcoming  # Sets the tone for new players
```

These comments aren't stripped for parsing. They ARE the specification. The LLM reads them. Acts on them.

---

## Anti-Patterns

❌ **Rigid schema enforcement** — "field X is required" without context  
❌ **Stripping comments** — losing the soul  
❌ **Machine-only YAML** — if humans can't read it, use JSON  
❌ **Over-specification** — killing the jazz  
❌ **JSON for tool calls** — entropy collapse, catastrophic forgetting
❌ **Transformation gaps** — compile steps that hide meaning

---

## Dovetails With

### Sister Skills
- [markdown/](../markdown/) — The prose format; YAML is the data format
- [plain-text/](../plain-text/) — The durability philosophy
- [format-design/](../format-design/) — Why simple formats win
- [postel/](../postel/) — Be liberal in accepting ambiguous YAML
- [soul-chat/](../soul-chat/) — Markdown with embedded YAML Jazz

### Kernel
- [kernel/constitution-core.md](../../kernel/constitution-core.md) — Section 3: YAML Jazz Principle

---

## Protocol Symbol

```
YAML-JAZZ
```

Invoke when: Interpreting YAML semantically, not just syntactically.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#YAML-JAZZ)
