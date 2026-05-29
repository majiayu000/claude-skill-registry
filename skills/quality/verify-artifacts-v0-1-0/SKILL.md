---
name: in2-verify-artifacts
description: Verify required artifacts exist, are complete, and match expectations.
version: 0.1.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/in2/verify-artifacts.v0.1.0","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN2 Verify Artifacts

Verify required artifacts exist, are complete, and match expectations.

## When to Use

- Checking build outputs and generated files
- Confirming evidence or logs are present and valid

## Usage

```bash
/apply-transformation IN2 "Verify the required artifacts for this run"
```
