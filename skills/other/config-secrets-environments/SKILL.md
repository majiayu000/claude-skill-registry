---
name: config-secrets-environments
description: Design, audit, and verify configuration, environment separation, secrets, BYOK flows, key rotation, config schema validation, and drift checks across local, dev, staging, and production. Use when adding env vars, changing runtime config, handling API keys or user-provided keys, diagnosing config drift, or preparing deploy/release configuration.
---

# Config Secrets Environments

## Purpose

Use this skill when behavior depends on configuration or secrets. The goal is explicit config ownership, validation, and environment parity without exposing credentials.

## Inventory

Collect:

1. Config files and env var declarations.
2. Runtime readers and startup wiring.
3. Secret sources: env, secret manager, local keychain, BYOK storage.
4. Environment matrix: local, test, dev, staging, prod.
5. Rotation, revocation, and audit requirements.
6. Existing `.env.example`, schema, docs, and CI checks.

Never print real secrets. Redact values and report only names, source type, and wiring status.

## Design Rules

- Define a schema for required and optional config.
- Fail closed for missing critical config; do not silently fall back to insecure or broad behavior.
- Keep defaults safe for local development and explicit for production.
- Separate build-time and runtime config.
- Keep tenant/user-provided keys isolated from platform keys.
- Document rotation and revocation paths.
- Verify config is wired into startup, not only declared.

## Environment Matrix

Use this shape:

| Key | Local | Test | Staging | Prod | Secret? | Owner | Rotation |
|---|---|---|---|---|---|---|---|

Mark unknown values as unknown. Do not infer a production value from local files.

## Output Shape

```text
config_inventory:
environment_matrix:
secret_flows:
validation_and_startup_wiring:
drift_checks:
rotation_plan:
failure_behavior:
verification_commands:
```
