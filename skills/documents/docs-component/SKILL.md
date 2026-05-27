---
name: docs-component
description: "(ePost) Document a klara-theme component (Figma data + prop mapping)"
user-invokable: true
context: fork
agent: epost-documenter
metadata:
  argument-hint: "<componentKey> [nodeId]"
  connections:
    requires: [web-ui-lib, web-figma]
---

# /docs-component

Document a klara-theme component by extracting Figma data and creating prop mappings.

## Usage

```
/docs-component <componentKey> [nodeId]
```

## Arguments

- `componentKey` (required): Component identifier (e.g., `button`, `select`, `dialog`)
- `nodeId` (optional): Figma node ID. If not provided, will be looked up from manifest or user will be prompted.

## Examples

```bash
# Document a component (nodeId from manifest)
/docs-component button

# Document with explicit Figma node ID
/docs-component select 207:134939

# Batch document all pending components
/docs-component --batch

# Batch document components in a category
/docs-component --batch forms
```

## Process

1. **Route**: Command routes to `epost-documenter`
2. **Detect**: Documenter detects klara-theme context
3. **Delegate**: Delegates to `epost-implementer` with:
   - `componentKey`: The component to document
   - `workflow`: `document-component`
4. **Execute**: Implementer follows `web-ui-lib-dev/references/document-component.md` skill aspect:
   - Extract Figma data via `web-figma/references/extraction-procedure.md`
   - Cross-reference with codebase
   - Write `<componentKey>.figma.json`
   - Write `<componentKey>.mapping.json`
   - Update manifest status
   - Validate against schemas

## Output

- `libs/klara-theme/figma-data/components/<componentKey>.figma.json` — Figma component data
- `libs/klara-theme/figma-data/mappings/<componentKey>.mapping.json` — Prop mappings
- `libs/klara-theme/figma-data/manifest.json` — Updated status

## Related

- Skill: `.github/skills/web-ui-lib-dev/references/document-component.md`
- Extraction: `.github/skills/web-figma/references/extraction-procedure.md`
- Manifest: `libs/klara-theme/figma-data/manifest.json`
- Schemas: `libs/klara-theme/figma-data/schema/`
