---
name: raycast
description: Raycast extension development framework. Use for creating extensions, API integration, UI components, command development, TypeScript patterns, React integration, and extension publishing.
---

# Raycast Skill

Comprehensive assistance with raycast development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with raycast
- Asking about raycast features or APIs
- Implementing raycast solutions
- Debugging raycast code
- Learning raycast best practices

## Quick Reference

### Common Patterns

*Quick reference patterns will be added as you use the skill.*

### Example Code Patterns

**Example 1** (bash):
```bash
npx @raycast/api@latest pull-contributions
```

**Example 2** (typescript):
```typescript
async function showHUD(
  title: string,
  options?: { clearRootSearch?: boolean; popToRootType?: PopToRootType }
): Promise<void>;
```

**Example 3** (typescript):
```typescript
import { showHUD } from "@raycast/api";

export default async function Command() {
  await showHUD("Hey there 👋");
}
```

**Example 4** (js):
```js
{
  macOS: { modifiers: ["cmd", "shift"], key: "c" },
  Windows: { modifiers: ["ctrl", "shift"], key: "c" },
}
```

**Example 5** (json):
```json
"default": {
  "macOS": "foo",
  "Windows": "bar"
}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **best_practices.md** - Best Practices documentation
- **examples.md** - Examples documentation
- **extension_development.md** - Extension Development documentation
- **getting_started.md** - Getting Started documentation
- **other.md** - Other documentation
- **teams.md** - Teams documentation
- **ui_components.md** - Ui Components documentation
- **utilities.md** - Utilities documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
