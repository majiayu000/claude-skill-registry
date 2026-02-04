---
name: in2-check-invariants
description: Check critical invariants before applying changes or decisions.
version: 0.1.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/in2/check-invariants.v0.1.0","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN2 Check Invariants

Check critical invariants before applying changes or decisions.

## When to Use

- Validating safety or compliance gates
- Ensuring prerequisite conditions are satisfied

## Usage

```bash
/apply-transformation IN2 "Check invariants before proceeding"
```
