---
name: aget-check-sessions
description: Monitor sessions/ directory health. Detects date subdirectories (anomaly), counts files, validates naming conventions, and tracks disk usage. Returns health status.
version: 1.0.0
---

# /aget-check-sessions

Monitor the health of the `sessions/` directory by checking file organization, naming conventions, and disk usage.

## Purpose

Provide self-diagnostic capability for AGET agents to assess their sessions directory health. Detects organizational anomalies like date-based subdirectories which indicate non-standard structure.

## Execution

When invoked, perform these checks:

### 1. Structure Check

```bash
# Check for date subdirectories (anomaly indicator)
find sessions -type d -name "20[0-9][0-9]-*" 2>/dev/null | wc -l

# Check for checkpoints subdirectory (expected)
test -d sessions/checkpoints && echo "yes" || echo "no"
```

### 2. File Inventory

```bash
# Count session files (excluding checkpoints)
find sessions -maxdepth 1 -type f -name "*.md" | wc -l

# Count checkpoint files
find sessions/checkpoints -type f -name "*.yaml" 2>/dev/null | wc -l
```

### 3. Naming Convention Check

Valid session pattern: `session_YYYY-MM-DD_*.md`

```bash
# Count valid session names
find sessions -maxdepth 1 -type f -name "session_20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.md" | wc -l

# Find non-conforming files
find sessions -maxdepth 1 -type f -name "*.md" ! -name "session_20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.md"
```

### 4. Disk Usage

```bash
du -sh sessions
```

## Thresholds

| Metric | OK | WARN | CRITICAL |
|--------|-----|------|----------|
| Total files | <200 | 200-500 | >500 |
| Date subdirectories | 0 | 1+ (anomaly) | - |
| Disk size | <50MB | 50-100MB | >100MB |

**Note**: Thresholds inherited from supervisor defaults. Research AGET baseline (2026-02-08): 77 files, 544K.

## Output Format

```
=== /aget-check-sessions ===

Directory: sessions/

Structure:
  Date subdirectories: [count] (0 = OK, >0 = anomaly)
  Checkpoints dir:     [yes/no]

File Counts:
  Session files: [count]
  Checkpoints:   [count]
  Non-conforming: [count]

Disk Usage: [size]

Non-Conforming Files:
  [list any files not matching expected patterns]

Health Status: [OK | WARN | CRITICAL]
Alerts:
  [list any threshold violations or anomalies]
```

## Health Status Logic

```
IF total_files > 500 OR disk > 100MB:
  CRITICAL
ELIF total_files > 200 OR disk > 50MB OR date_subdirs > 0:
  WARN
ELSE:
  OK
```

## Constraints

- **C1**: Read-only operation. Never modify files.
- **C2**: Date subdirectories are anomaly indicators, not errors.
- **C3**: Checkpoints subdirectory is expected and excluded from anomaly detection.

## Related Skills

- `/aget-check-evolution` - Evolution directory health
- `/aget-check-kb` - Knowledge base health
- `/aget-save-state` - Create checkpoints

## Traceability

| Link | Reference |
|------|-----------|
| POC | POC-017 |
| Project | PROJECT_PLAN_AGET_UNIVERSAL_SKILLS.md |
| Source | Fleet Skill Deployment Report (supervisor) |
| Baseline | 77 files, 544K (2026-02-08) |

---

*aget-check-sessions v1.0.0*
*Category: Monitoring*
*POC-017 Phase 1*
