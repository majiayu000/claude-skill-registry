---
name: no-runtime-code
description: 'Guardrails to keep the pipeline pure: specs + SEA + generators only.'
---

---
name: no-runtime-code
description: Guardrails to keep the pipeline pure: specs + SEA™ + generators only.
---

# No handwritten runtime code


## Allowed edits
- `specs/**`, `.github/**`, `tools/**`, `tools/nx/**`, `.vscode/**`, `.githooks/**`, `.github/workflows/**`
- generated `**/src/gen/**`

## If you need behavior
- Model it in SDS/SEA™ (entities, flows, tags)
- Extend schemas if needed
- Update AST→IR→manifest mapping
- Update code generator templates

## Anti-patterns
- Patching generated code
- Adding runtime “helpers” by hand
- Hiding logic in adapters instead of modeling it
