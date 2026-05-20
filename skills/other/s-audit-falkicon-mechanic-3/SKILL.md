---
name: s-audit
description: >
  Comprehensive quality analysis for WoW addons. Combines security, complexity,
  deprecation, and dead code analysis into a single audit workflow.
  Triggers: audit, quality, analysis, review, check, scan.
---

# Auditing WoW Addons

Expert guidance for comprehensive addon quality analysis.

## Related Commands

- [c-audit](../../commands/c-audit.md) - Full audit workflow
- [c-clean](../../commands/c-clean.md) - Dead code cleanup
- [c-lint](../../commands/c-lint.md) - Syntax and style
- [c-review](../../commands/c-review.md) - Full review (includes audit)

## MCP Tools

| Task | MCP Tool |
|------|----------|
| Security Analysis | `addon.security(addon="MyAddon")` |
| Complexity Analysis | `addon.complexity(addon="MyAddon")` |
| Deprecation Scan | `addon.deprecations(addon="MyAddon")` |
| Dead Code Detection | `addon.deadcode(addon="MyAddon")` |

## Capabilities

1. **Security Analysis** — Combat lockdown, secret values, taint, unsafe eval
2. **Complexity Analysis** — Deep nesting, long functions, magic numbers, duplicates
3. **Deprecation Scanning** — 100+ deprecated APIs with migration paths
4. **Dead Code Detection** — Unused functions, orphaned files, dead exports

## Analysis Categories

### Security (`addon.security`)

| Category | Description | Severity |
|----------|-------------|----------|
| `combat_violation` | Protected API without InCombatLockdown() guard | Error |
| `secret_leak` | Logging/storing secret values (12.0+) | Error |
| `taint_risk` | Unsafe global modifications | Warning |
| `unsafe_eval` | loadstring/RunScript with variable input | Warning |
| `addon_comm` | Unvalidated message parsing | Info |

### Complexity (`addon.complexity`)

| Category | Threshold | Description |
|----------|-----------|-------------|
| `deep_nesting` | > 5 levels | Excessive if/for/while nesting |
| `long_function` | > 100 lines | Functions too long to understand |
| `long_file` | > 500 lines | Files that should be split |
| `magic_number` | pattern-based | Unexplained numeric literals |
| `duplicate_code` | > 10 lines | Near-identical code blocks |

### Deprecations (`addon.deprecations`)

| Category | Example APIs | Since |
|----------|--------------|-------|
| `addons` | GetAddOnInfo → C_AddOns.GetAddOnInfo | 11.0 |
| `spells` | GetSpellInfo → C_Spell.GetSpellInfo | 11.0 |
| `items` | GetItemInfo → C_Item.GetItemInfo | 11.0 |
| `containers` | GetContainerItemInfo → C_Container | 10.0 |
| `unit` | UnitHealth (returns secret for enemies) | 12.0 |

### Dead Code (`addon.deadcode`)

| Category | Description |
|----------|-------------|
| `unused_function` | Functions defined but never called |
| `orphaned_file` | Lua files not in TOC |
| `dead_export` | Exported values never used |
| `unused_library` | Libraries in Libs/ never used |

## Workflow

### Quick Audit

```
1. addon.security   → Critical issues (combat, secrets)
2. addon.deprecations (min_severity=error) → Breaking changes
3. Report critical findings
```

### Full Audit

```
1. addon.security   → All security issues
2. addon.complexity → All maintainability issues
3. addon.deprecations → All deprecated APIs
4. addon.deadcode   → All dead code
5. Comprehensive report with priority order
```

## Interpreting Results

### Priority Order

1. **Critical** (Fix immediately):
   - Combat lockdown violations (will cause bugs)
   - Secret value leaks (12.0+ breaking)
   - Deprecated APIs with `severity: error`

2. **High** (Fix before release):
   - Taint risks
   - Deprecated APIs with `severity: warning`
   - Orphaned files

3. **Medium** (Fix when convenient):
   - Deep nesting (maintainability)
   - Long functions
   - Magic numbers

4. **Low** (Consider fixing):
   - Code duplicates
   - Suspicious dead code

## Best Practices

1. **Run before release** — Catch breaking changes early
2. **Start with critical** — Security and deprecations first
3. **Filter by severity** — Use `include_suspicious=false` for focused results
4. **Check 12.0 readiness** — Secret value APIs are breaking changes
5. **Review complexity** — High complexity = high bug risk
