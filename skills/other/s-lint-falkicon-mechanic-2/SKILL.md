---
name: s-lint
description: >
  Ensure code quality using Luacheck linting and StyLua formatting. Covers
  common warnings, style rules, and auto-formatting. Use when checking code
  quality, fixing style issues, or preparing code for review.
  Triggers: lint, format, style, luacheck, stylua, code quality, warnings.
---

# Linting WoW Addons

Expert guidance for code quality and formatting in WoW addon development.

## Related Commands

- [c-lint](../../commands/c-lint.md) - Lint and format workflow
- [c-review](../../commands/c-review.md) - Full code review (includes lint step)
- [c-clean](../../commands/c-clean.md) - Cleanup workflow (dead code, stale docs)

## MCP Tools

| Task | MCP Tool |
|------|----------|
| Lint Addon | `addon.lint(addon="MyAddon")` |
| Format Addon | `addon.format(addon="MyAddon")` |
| Check Format Only | `addon.format(addon="MyAddon", check=true)` |
| Security Analysis | `addon.security(addon="MyAddon")` |
| Complexity Analysis | `addon.complexity(addon="MyAddon")` |

## Capabilities

1. **Luacheck Linting** — Detect syntax errors, undefined globals, unused variables
2. **StyLua Formatting** — Consistent code style across all files
3. **Error Resolution** — Fix common linting issues systematically
4. **Security Analysis** — Detect combat lockdown violations, secret leaks, taint risks
5. **Complexity Analysis** — Find deep nesting, long functions, magic numbers
6. **Dead Code Detection** — For unused function analysis, use `addon.deadcode` (see [s-clean](../s-clean/SKILL.md))

## Common Luacheck Warnings

| Code | Meaning | Fix |
|------|---------|-----|
| W111 | Setting undefined global | Add to `.luacheckrc` globals or fix typo |
| W112 | Mutating undefined global | Same as W111 |
| W113 | Accessing undefined global | Check if API exists, add to read_globals |
| W211 | Unused local variable | Remove or prefix with `_` |
| W212 | Unused argument | Prefix with `_` (e.g., `_event`) |
| W213 | Unused loop variable | Prefix with `_` |
| W311 | Value assigned but never used | Remove assignment or use the value |
| W431 | Shadowing upvalue | Rename the local variable |

## .luacheckrc Configuration

Standard WoW addon configuration:

```lua
std = "lua51"
max_line_length = false

globals = {
    -- Addon globals
    "MyAddon",
}

read_globals = {
    -- WoW API
    "C_Timer", "C_Spell", "CreateFrame",
    -- Ace3
    "LibStub",
}
```

## StyLua Configuration

Standard `.stylua.toml`:

```toml
column_width = 120
line_endings = "Unix"
indent_type = "Tabs"
indent_width = 4
quote_style = "AutoPreferDouble"
call_parentheses = "Always"
```

## Quick Reference

### Lint Then Format

```bash
# Check for issues
addon.lint(addon="MyAddon")

# Auto-format
addon.format(addon="MyAddon")

# Verify clean
addon.lint(addon="MyAddon")
```

### Best Practices

1. **Run lint before commit** — Catch issues early
2. **Format consistently** — Use StyLua for all files
3. **Configure globals** — Add addon-specific globals to `.luacheckrc`
4. **Prefix unused** — Use `_` prefix for intentionally unused variables

## Security Analysis

Beyond syntax linting, use `addon.security` to detect runtime safety issues:

| Category | Description |
|----------|-------------|
| `combat_violation` | Protected API calls without `InCombatLockdown()` guard |
| `secret_leak` | Logging/printing secret values (12.0+) |
| `taint_risk` | Unsafe global modifications (`_G` without namespace) |
| `unsafe_eval` | `loadstring`/`RunScript` with unsanitized input |

## Complexity Analysis

Use `addon.complexity` to identify maintainability issues:

| Category | Threshold | Description |
|----------|-----------|-------------|
| `deep_nesting` | > 5 levels | Excessive if/for/while nesting |
| `long_function` | > 100 lines | Functions that should be split |
| `long_file` | > 500 lines | Files that need restructuring |
| `magic_number` | pattern-based | Unexplained numeric literals |

For comprehensive analysis, use [c-audit](../../commands/c-audit.md).
