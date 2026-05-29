---
name: in2-validate-schema
description: Validate schemas and structured inputs before downstream execution.
version: 0.1.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/in2/validate-schema.v0.1.0","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN2 Validate Schema

Validate schemas and structured inputs before downstream execution.

## When to Use

- Verifying JSON/YAML schema compliance
- Preflight validation of structured payloads

## Usage

```bash
/apply-transformation IN2 "Validate the schema for this payload"
```
