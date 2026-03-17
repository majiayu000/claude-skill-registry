---
name: aget-check-evolution
description: Monitor .aget/evolution/ directory health. Validates file counts, naming conventions, disk usage, and returns health status with alerts on anomalies.
version: 1.0.0
---

# /aget-check-evolution

Monitor the health of the `.aget/evolution/` directory by checking file counts, types, naming conventions, and disk usage.

## Purpose

Provide self-diagnostic capability for AGET agents to assess their evolution directory health without supervisor intervention.

## Execution

When invoked, perform these checks:

### 1. File Inventory

```bash
# Count total files
find .aget/evolution -type f | wc -l

# Count by extension
find .aget/evolution -type f -name "*.md" | wc -l
find .aget/evolution -type f -name "*.json" | wc -l
find .aget/evolution -type f ! -name "*.md" ! -name "*.json" | wc -l
```

### 2. Naming Convention Check

Valid L-doc pattern: `L###_*.md` (e.g., `L588_skill_invocation_control_semantics.md`)

```bash
# Count valid L-doc names
find .aget/evolution -type f -name "L[0-9][0-9][0-9]_*.md" | wc -l

# Find non-conforming files (excluding index.json)
find .aget/evolution -type f ! -name "L[0-9][0-9][0-9]_*.md" ! -name "index.json" ! -name "README.md"
```

### 3. Disk Usage

```bash
du -sh .aget/evolution
```

### 4. Index Integrity

Check that `index.json` exists and is valid JSON:

```bash
test -f .aget/evolution/index.json && jq empty .aget/evolution/index.json 2>/dev/null && echo "valid" || echo "invalid"
```

## Thresholds

| Metric | OK | WARN | CRITICAL |
|--------|-----|------|----------|
| Total files | <500 | 500-750 | >750 |
| Non-standard files | 0-10 | 11-50 | >50 |
| Disk size | <10MB | 10-25MB | >25MB |
| Index integrity | valid | - | invalid |

**Note**: Thresholds inherited from supervisor defaults. Research AGET baseline (2026-02-08): 94 files, 800K - well within OK range.

## Output Format

Report the following:

```
=== /aget-check-evolution ===

Directory: .aget/evolution/

File Counts:
  Total:     [count]
  L-docs:    [count] (.md matching L###_*.md)
  Index:     [1 if exists, 0 otherwise]
  Other:     [count] (non-conforming)

Disk Usage: [size]

Index Status: [valid/invalid/missing]

Non-Conforming Files:
  [list any files not matching expected patterns]

Health Status: [OK | WARN | CRITICAL]
Alerts:
  [list any threshold violations]
```

## Health Status Logic

```
IF index invalid OR index missing:
  CRITICAL
ELIF total_files > 750 OR disk > 25MB OR non_standard > 50:
  CRITICAL
ELIF total_files > 500 OR disk > 10MB OR non_standard > 10:
  WARN
ELSE:
  OK
```

## Constraints

- **C1**: Read-only operation. Never modify files.
- **C2**: Report ALL findings, even if status is OK.
- **C3**: List non-conforming files by name for actionability.

## Related Skills

- `/aget-check-sessions` - Sessions directory health
- `/aget-check-kb` - Knowledge base health
- `/aget-record-lesson` - Capture findings as L-docs

## Traceability

| Link | Reference |
|------|-----------|
| POC | POC-017 |
| Project | PROJECT_PLAN_AGET_UNIVERSAL_SKILLS.md |
| Source | Fleet Skill Deployment Report (supervisor) |
| Baseline | 94 files, 800K (2026-02-08) |

---

*aget-check-evolution v1.0.0*
*Category: Monitoring*
*POC-017 Phase 1*
