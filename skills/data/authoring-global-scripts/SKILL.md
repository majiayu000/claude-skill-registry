---
name: authoring-global-scripts
description: 'Authors and manages global package scripts using the _: prefix convention.
  Scripts defined in root package.json are propagated to all packages with the prefix
  stripped.'
---

---
name: authoring-global-scripts
description: Authors and manages global package scripts using the _: prefix convention. Scripts defined in root package.json are propagated to all packages with the prefix stripped.
---

# Authoring Global Scripts

Manage package scripts that apply to all packages in the monorepo.

## Steps

### Adding a Global Script

1. Add script to root `package.json` with `_:` prefix:
   ```json
   {
     "scripts": {
       "_:build": "tsgo -p tsconfig.build.json",
       "_:check:types": "tsgo --noEmit"
     }
   }
   ```

2. Run the sync script at `.claude/skills/authoring-global-scripts/scripts/sync-package-scripts.ts`

### Auditing for Inconsistencies

Run with `--check` flag to verify all packages are in sync without modifying:
```
tsx .claude/skills/authoring-global-scripts/scripts/sync-package-scripts.ts --check
```

## Reference

### Convention

| Location | Format | Example |
|----------|--------|---------|
| Root package.json | `_:script-name` | `"_:build": "tsgo -p tsconfig.build.json"` |
| Package package.json | `script-name` | `"build": "tsgo -p tsconfig.build.json"` |

The `_:` prefix marks scripts as "global templates". The sync script:
- Strips the prefix when copying to packages
- Replaces all package scripts (packages should not have custom scripts)
- Warns about extra scripts in packages that aren't in the template

### Relative Paths

Relative paths like `../../oxlint.json` are preserved as-is. They're relative from each package directory, so `../../` correctly points to the monorepo root from `packages/*/`.

## Notes

- Packages should NOT have custom scripts - all scripts come from the global template
- If a package needs a unique script, reconsider whether it belongs as a global script
- Run audit (`--check`) to catch manual edits that broke the pattern
