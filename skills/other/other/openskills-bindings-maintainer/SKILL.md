---
name: openskills-bindings-maintainer
description: Maintain compatibility between openskills-runtime and language bindings (TypeScript, Python), including feature flags, build configuration, and smoke verification.
---

# OpenSkills Bindings Maintainer

Use this skill when runtime APIs, features, or dependency topology changes may affect bindings.

## Scope

- `bindings/ts/**`
- `bindings/python/**`
- runtime crate feature interactions affecting bindings

## Workflow

1. Identify runtime change surface (API, features, dependencies).
2. Check both bindings for feature/compile assumptions.
3. Verify build and smoke tests for each binding.
4. Confirm lockfile and manifest consistency where applicable.

## TS Binding Checks

```bash
cd bindings/ts
npm install
npm run build
```

## Python Binding Checks

Use project-standard build/test commands for Python bindings and confirm import/runtime behavior.

## Guardrails

- Avoid introducing plugin/build-tool dependencies into default binding paths unless intentional.
- Keep generated files and lockfiles aligned with project policy.

## Output Format

- Compatibility matrix (runtime vs TS/Python)
- Breaking changes
- Required migration steps
- Verification evidence
