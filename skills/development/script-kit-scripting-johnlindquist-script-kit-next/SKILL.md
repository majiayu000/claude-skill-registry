---
name: script-kit-scripting
description: Script metadata and scriptlet bundle patterns for Script Kit. Use when writing scripts, test files, or scriptlet bundles. Covers global metadata, legacy comment-based metadata, and YAML frontmatter for bundles.
---

# Script Kit Scripting

Patterns for writing scripts and scriptlet bundles.

## Script Metadata (Preferred: Global Export)

Use for all new scripts/tests:
```ts
import '../../scripts/kit-sdk';

export const metadata = {
  name: "My Script",
  description: "Does something useful",
  shortcut: "cmd+shift+m",
  author: "Your Name",
  // more typed fields available
};
```

Why prefer global metadata:
- Type safety (TS types)
- IDE autocomplete + validation
- More fields + easier extensibility
- Compile-time feedback (vs runtime parsing)

## Legacy Comment-Based Metadata

Supported for backwards compatibility:
```ts
// Name: My Script
// Description: Does something useful
// Shortcut: cmd+shift+m
import '../../scripts/kit-sdk';
```

## SDK Import in Tests

Tests import from repo path:
```ts
import '../../scripts/kit-sdk'; // globals: arg(), div(), editor(), fields(), captureScreenshot(), getLayoutInfo(), ...
```

Production scripts use runtime-extracted SDK at `~/.scriptkit/sdk/kit-sdk.ts`.

## Scriptlet Bundles (`~/.scriptkit/snippets/*.md`)

Optional YAML frontmatter (line 1 must be `---`, closed by `---` on its own line):
```md
---
name: My API Tools
description: Collection of useful API utilities
author: John Doe
icon: api
---
```

Fields: `name`, `description`, `author`, `icon` (all optional). Unknown fields ignored.

### Backwards Compatibility

- Frontmatter optional; bundles without it still work
- Filename fallback: missing `name` uses filename (sans `.md`)
- Invalid frontmatter logs warnings but does not break parsing

### Validation Behavior

- Missing closing `---` → warn (line #), skip frontmatter
- Invalid YAML → warn (error + line #), skip frontmatter
- Errors surface to users via HUD notifications with line #

### Default Icon Mapping

When no explicit `icon:`:
- `template` → `text-cursor-input`
- `tool` → `wrench`
- `snippet` → `code`
- `script` → `terminal`
- `prompt` → `message-circle`
- `action` → `zap`
- fallback → `file-text`

Icon resolution priority:
1. explicit frontmatter icon
2. tool-type default
3. bundle fallback `file-text`

### Troubleshooting

- Frontmatter not parsed → must start on line 1 with `---` and have closing `---` on its own line
- Icon not showing → verify icon name exists; check `[CACHE]` logs
- HUD validation error → use the reported line number; quote special chars
- Metadata not updating → touch file to refresh cache; check logs
