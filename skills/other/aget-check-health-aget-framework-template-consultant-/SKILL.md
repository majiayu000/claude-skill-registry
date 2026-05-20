---
name: aget-check-health
description: Run AGET health inspection and housekeeping checks
allowed-tools:
  - Bash
  - Read
  - Glob
---

# aget-check-health

Run health inspection on an AGET agent. This skill performs sanity checks, validates structure, and reports agent health status.

## Instructions

When this skill is invoked:

1. Run the housekeeping script:
   ```bash
   python3 scripts/aget_housekeeping_protocol.py
   ```

2. The script checks:
   - `.aget/` directory structure
   - `version.json` validity
   - `identity.json` validity (if exists)
   - `governance/` directory contents
   - 5D directory structure
   - L-doc count and format

3. Report the health status:
   - **Healthy** (exit 0): All checks passed
   - **Warnings** (exit 1): Non-blocking issues found
   - **Errors** (exit 2): Blocking issues require attention

## Output Format

Present the health report:
```
Sanity Check: [HEALTHY/WARNINGS/ERRORS]

Checks:
- Structure: [PASS/WARN/FAIL]
- Version: [PASS/WARN/FAIL]
- Identity: [PASS/WARN/FAIL]
- Governance: [PASS/WARN/FAIL]

[If warnings/errors, list specific issues]

Recommendations:
- [Action items if any]
```

## Options

- `--json`: Machine-readable output
- `--fix`: Attempt auto-fixes for known issues
- `--dir /path`: Run on specific agent directory

## Error Handling

- Exit code 0: All checks passed
- Exit code 1: Warnings found (list them)
- Exit code 2: Errors found (list them, recommend fixes)
- Exit code 3: Script configuration error

## Related

- L532: Skills vs Learnings Distinction
- CAP-SESSION-002: Sanity Check Protocol
