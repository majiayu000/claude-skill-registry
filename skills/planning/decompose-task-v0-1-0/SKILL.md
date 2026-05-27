---
name: de3-decompose-task
description: Apply DE3 decomposition to split a task into smaller, independent units.
version: 0.1.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/de3/decompose-task.v0.1.0","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# DE3 Decompose Task

Apply DE3 decomposition to partition a task into modular units with clear boundaries.

## When to Use

- Breaking a large task into manageable parts
- Isolating responsibilities or work streams

## Usage

```bash
/apply-transformation DE3 "Decompose this task into modular units"
```
