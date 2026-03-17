---
name: prompt
description: >
  Orchestrator skill for the `prompt` skillset. Dispatches to member skills in a safe,
  predictable order. Separates intent formation from execution to protect humans from
  premature or misaligned execution.
metadata:
  author: Jordan Godau
  version: 0.1.0

  skillset:
    name: prompt
    schema_version: 1
    skills:
      - prompt-forge
      - prompt-exec

    resources:
      root: .prompt-forge
      assets: []
      scripts: []
      references: []

    pipelines:
      default:
        - prompt-forge
        - prompt-exec
      allowed:
        - [prompt-forge]
        - [prompt-exec]
        - [prompt-forge, prompt-exec]

    requires: []

---

# Prompt Skillset

> **We forge prompts collaboratively, and we execute them deliberately.**

## Philosophy

This skillset assumes:

- Human intent is *discovered*, not known upfront
- Conversation is not state
- Disk state is authoritative
- Execution is irreversible and requires explicit consent

## Core Invariants

### 1. Conversation is not state

The agent must not assume continuity or memory across turns.
All durable state lives on disk.
The agent may only read or modify state **inside an explicit skill invocation**.

> **Conversation is not state. Disk is state. Skills are the only legal state transitions.**

### 2. Single canonical prompt on disk

There may be **at most one active prompt artifact** at any time.

**Canonical path:** `.prompt-forge/active.yaml`

### 3. Execution is destructive

After a **successful** `prompt-exec`:

- The canonical prompt artifact **must be deleted**
- The system must return to a "no active prompt" state

### 4. Optional execution receipts

To preserve auditability without violating single-prompt rules:

- `prompt-exec` *may* write an **execution receipt**
- Receipts are immutable and never executable

**Receipt location:** `.prompt-forge/receipts/<timestamp>-<hash>.yaml`

## Member Skills

| Skill          | Purpose                                                                |
| -------------- | ---------------------------------------------------------------------- |
| `prompt-forge` | Shape, refine, and stabilize intent into the canonical prompt artifact |
| `prompt-exec`  | Execute the forged prompt exactly as written                           |

No other prompt-related skills are permitted.
