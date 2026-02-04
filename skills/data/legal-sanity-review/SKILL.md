---
name: legal-sanity-review
version: "1.0.0"
category: _internal
description: "Legal Sanity Review Workflow — mandatory pre-gate in the cross-review cycle"
---

# Legal Sanity Review Workflow

> Version: 1.0.0
> Category: Workflows
> Triggers: Before cross-review (Codex/Gemini), PR creation, code porting

## Purpose

Ensures no client project names, proprietary tool references, or legally sensitive content reaches the cross-review stage or a pull request. This is a **mandatory pre-gate** — if the legal scan fails, the review cycle does not proceed.

## Review Flow

```
Claude/Gemini performs task
         ↓
    Commit changes
         ↓
    Legal Sanity Scan ◄── MANDATORY PRE-GATE
    ├── BLOCK → Fix violations → Re-scan
    └── PASS  → Proceed to Codex review
                    ↓
               Cross-Review Cycle
```

## Integration Points

### Cross-Review Pre-Gate
The legal scan runs **before** the first Codex/Gemini iteration:

| Step | Gate | Action |
|------|------|--------|
| 1 | Legal Scan | Run `legal-sanity-scan.sh --diff-only` |
| 2 | Pass? | If no → fix and re-scan |
| 3 | Codex Review | First cross-review iteration |
| 4 | Gemini Review | Parallel cross-review |

### PR Pre-Hook
Integrated into `pr-manager.md` hooks:
```bash
./scripts/legal/legal-sanity-scan.sh --diff-only || (echo "Legal sanity FAILED" && exit 1)
```

### Manual Invocation
```bash
# Full repo scan
./scripts/legal/legal-sanity-scan.sh --repo=worldenergydata

# All submodules
./scripts/legal/legal-sanity-scan.sh --all
```

## Exit Conditions

| Condition | Code | Action |
|-----------|------|--------|
| PASS | 0 | Proceed to cross-review |
| BLOCK | 1 | Fix violations, re-scan |
| SCAN_ERROR | 2 | Check script/config, retry |

## Violation Response

When the scan finds block-severity violations:

1. **Stop** — do not proceed to cross-review or PR creation
2. **Report** — list each violation with file:line and pattern
3. **Fix** — replace client references with generic equivalents
4. **Re-scan** — confirm all violations are resolved
5. **Continue** — proceed to the cross-review cycle

## Configuration

Deny lists control what patterns are scanned:

- **Global**: `.legal-deny-list.yaml` (workspace root)
- **Per-project**: `<submodule>/.legal-deny-list.yaml`

See `.claude/rules/legal-compliance.md` for the full policy.

---

*Use this workflow whenever committing AI-generated or ported code to ensure legal compliance before review.*
