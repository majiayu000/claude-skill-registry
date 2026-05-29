---
name: aget-check-kb
description: Validate Knowledge Base health by checking structure, frontmatter compliance, and content staleness. Returns conformance score and health status (OK/WARN/CRITICAL).
version: 1.0.0
---

# /aget-check-kb

Validate the health of the `knowledge/` directory by checking structure, file organization, and content freshness.

## Purpose

Provide self-diagnostic capability for AGET agents to assess their knowledge base health. Identifies structural issues, missing documentation, and stale content.

## Execution

When invoked, perform these checks:

### 1. Structure Check

```bash
# Check if knowledge/ exists
test -d knowledge && echo "exists" || echo "missing"

# List subdirectories
find knowledge -type d -mindepth 1 -maxdepth 1

# Check for README
test -f knowledge/README.md && echo "yes" || echo "no"
```

### 2. File Inventory

```bash
# Count markdown files
find knowledge -type f -name "*.md" | wc -l

# Count by subdirectory
for dir in knowledge/*/; do
  echo "$dir: $(find "$dir" -type f -name "*.md" | wc -l)"
done
```

### 3. Staleness Check

```bash
# Find files not modified in 90+ days
find knowledge -type f -name "*.md" -mtime +90 | wc -l

# Find files not modified in 180+ days
find knowledge -type f -name "*.md" -mtime +180 | wc -l
```

### 4. Disk Usage

```bash
du -sh knowledge
```

## Thresholds

| Metric | OK | WARN | CRITICAL |
|--------|-----|------|----------|
| KB exists | yes | - | no |
| README exists | yes | no | - |
| Staleness (90+ days) | <25% | 25-50% | >50% |
| Staleness (180+ days) | <10% | 10-25% | >25% |

**Note**: Research AGET baseline (2026-02-08): 14 files, 96K.

## Output Format

```
=== /aget-check-kb ===

Directory: knowledge/

Structure:
  KB exists:     [yes/no]
  README:        [yes/no]
  Subdirectories: [list]

File Counts:
  Total files:   [count]
  By directory:
    [dir]: [count]
    ...

Staleness:
  >90 days:  [count] ([%])
  >180 days: [count] ([%])

Disk Usage: [size]

Health Status: [OK | WARN | CRITICAL]
Alerts:
  [list any threshold violations]
```

## Health Status Logic

```
IF kb_missing:
  CRITICAL
ELIF stale_180 > 25% OR stale_90 > 50%:
  CRITICAL
ELIF readme_missing OR stale_180 > 10% OR stale_90 > 25%:
  WARN
ELSE:
  OK
```

## Constraints

- **C1**: Read-only operation. Never modify files.
- **C2**: Report staleness as both count and percentage.
- **C3**: If KB doesn't exist, report CRITICAL but don't fail.

## Related Skills

- `/aget-check-evolution` - Evolution directory health
- `/aget-check-sessions` - Sessions directory health

## Traceability

| Link | Reference |
|------|-----------|
| POC | POC-017 |
| Project | PROJECT_PLAN_AGET_UNIVERSAL_SKILLS.md |
| Source | Fleet Skill Deployment Report (supervisor) |
| Baseline | 14 files, 96K (2026-02-08) |

---

*aget-check-kb v1.0.0*
*Category: Monitoring*
*POC-017 Phase 1*
