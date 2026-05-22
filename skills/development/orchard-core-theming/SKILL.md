---
name: orchard-core-theming
description: Evidence-first Orchard Core theming skill for shapes, alternates, placement, Razor/Liquid templates, content model access, assets/resources, and recipes. Use for theme adjustments, shape overrides, template discovery, content item/field access, placement.json rules, and recipe authoring in Orchard Core projects.
license: MIT
metadata:
  author: Lombiq Technologies
  version: "1.0"
---

# Orchard Core Theming

Use this skill for Orchard Core theming and content-definition/recipe work.

## How to use
- Path A (task match): scan the Tasks list; if the request matches, open `references/TASK-MAP.md` and go directly to the leaf files.
- Path B (exploration): use the section cues to pick a reference section, open that section's `INDEX.md`, then choose the leaf file it points to.
- Determine Razor vs Liquid early using the workflow in `references/TASK-MAP.md`. If it cannot be decided, fall back to Liquid and confirm with the user.
- Open only the necessary leaf files; use a section `INDEX.md` only for orientation and discovery.
- Prefer examples and ready-to-copy patterns.

## Evidence rules
- Prefer repo evidence over assumptions: active theme, base theme, `placement.json`, and existing templates.
- Trace the shape model first when it is unclear; use `references/TASK-MAP.md` to find shape tracing guidance and ask the user if needed.
- Confirm unknown part/field properties in `ContentDefinition.json` (or `OrchardCore.db`) and the relevant field references.
- Ask for missing identifiers (content type, part name, field name, display type) instead of inventing them.
- Do not invent recipe steps or feature IDs; use `references/TASK-MAP.md` to find the right recipe references.

## Scripts
Use these scripts instead of hand-building extracts.
- `scripts/extract-content-definitions.py` to extract content types/parts/fields from `ContentDefinition.json` or `OrchardCore.db`, with optional related-type expansion and Markdown/JSON output. See `references/50-content-model/CONTENT-DEFINITIONS-EXTRACTOR.md`.
- `scripts/extract-content-items.py` to get content items from `OrchardCore.db`, filter by type/IDs/text, and optionally emit a recipe `content` step or a Markdown/JSON extract. See `references/50-content-model/CONTENT-ITEMS-EXTRACTOR.md`.
- `scripts/generate-orchard-ids.py` to generate Orchard Core IDs that match the `DefaultIdGenerator` alphabet for stable `ContentItemId` values in recipes. See `references/70-recipes/ID-GENERATION.md`.
- `scripts/sync-skill.py` to refresh the entire skill folder from the Lombiq/Orchard-Core-Agent-Skills repo (references, scripts, SKILL.md, assets). The running script is not overwritten until the next sync.

Sync example:
```bash
python skills/orchard-core-theming/scripts/sync-skill.py
```

## Reference section cues
Use these cues to decide which reference section to open.
- Use `references/10-understand-structure/` to confirm solution and theme structure (manifests, base theme), create themes, and locate layouts/zones.
- Use `references/20-shapes-placement/` to find shape names, alternates, placement rules, and override workflow steps.
- Use `references/30-razor/` to implement Razor theme changes with tag helpers, shape rendering, and IOrchardHelper.
- Use `references/40-liquid/` to implement Liquid theme changes with tags, filters, and shape helpers.
- Use `references/50-content-model/` to inspect content definitions/items, parts/fields, settings/containers, and the extractors.
- Use `references/60-assets-resources/` to include scripts/styles and manage resources and static files.
- Use `references/70-recipes/` to author, validate, and reuse recipes for setup, definitions, and content import.
- Use `references/80-debugging-discovery/` to trace shapes, inspect logs, and find evidence in source.
- Use `references/90-glossary/` to resolve terms and acronyms in Orchard Core theming docs.

## Tasks
Use this list to decide whether to open `references/TASK-MAP.md` for the exact leaf files.
- Determine template language (Razor vs Liquid).
- Add or update a content type/part/field in ContentDefinition.json.
- Extract a focused content definition slice (large JSON).
- Create a setup recipe.
- Add content types and sample content to a recipe.
- Create or update workflows in a recipe.
- Create or override a content item shape template.
- Implement or override OrchardCore.Forms widgets and Form content.
- Inspect real content items (SQLite).
- Update a shape after adding fields.
- Render BagPart/FlowPart/ListPart items.
- Add scripts/styles and include them in the layout.
- Find shape alternates and placement rules.
- Find evidence in Orchard Core source.
- Work on theme structure or layout.
- Understand solution structure.
