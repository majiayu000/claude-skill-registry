---
name: pm-audit
description: System-wide structural audit of the entire PM knowledge system. Checks orphans, broken links, register coverage, schema violations across all decisions, and vault health metrics. Slower and deeper than /pm-review. Triggers on "/pm-audit", "system audit", "vault health", "find orphans", "check broken links".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary mapping.
Read `ops/config.yaml` for all maintenance thresholds.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: run full audit (all checks)
- If "orphans": find orphan decisions only
- If "links": check broken wiki-links only
- If "schema": validate schema compliance across all decisions
- If "registers": audit decision register coverage and completeness

**START NOW.**

---

## Philosophy

**A knowledge system that cannot audit itself will rot.**

Individual /pm-review checks decisions for quality. /pm-audit checks the system for structural integrity. These are different problems. A system can contain individually high-quality decisions that are nevertheless disconnected, uncategorized, and inaccessible — effectively invisible to future coordination.

/pm-audit is the health scan. It finds the issues that individual review misses: decisions no register points to, wiki-links to files that were deleted or renamed, registers that grew too large to navigate, schema drift where fields added in new templates haven't been backfilled into old decisions.

Run /pm-audit when the vault feels slow or when coordination starts feeling inefficient — that inefficiency often has a structural cause.

---

## Audit Checks

### Check 1: Orphan Decisions

A decision not referenced by any decision register is an orphan. Orphans exist in the vault but cannot be discovered through normal navigation.

```bash
# Get all decision filenames
ls decisions/*.md | grep -v "index.md" | grep -v "-register.md"

# For each decision, check if it appears in any register
for f in decisions/*.md; do
  basename=$(basename "$f" .md)
  count=$(rg "$basename" decisions/*-register.md decisions/index.md --count 2>/dev/null | grep -v ":0" | wc -l)
  if [ "$count" -eq 0 ]; then
    echo "ORPHAN: $basename"
  fi
done
```

### Check 2: Broken Wiki-Links

Wiki-links pointing to non-existent files.

```bash
# Extract all [[links]] from decisions/
rg "\[\[([^\]]+)\]\]" decisions/ --include="*.md" -o --no-filename | sort -u

# Cross-reference against actual files
# Flag any [[link]] where the target file doesn't exist
```

### Check 3: Schema Violations

```bash
# Missing required fields
rg "^description: \"\"" decisions/ --include="*.md" -l
rg "last_reviewed: YYYY-MM-DD" decisions/ --include="*.md" -l
rg "^type: $" decisions/ --include="*.md" -l

# Invalid enum values
rg "^type:" decisions/ --include="*.md" -h | sort | uniq -c | sort -rn
rg "^status:" decisions/ --include="*.md" -h | sort | uniq -c | sort -rn
rg "^meta_state:" decisions/ --include="*.md" -h | sort | uniq -c | sort -rn
```

### Check 4: Register Size and Coverage

```bash
# Count decisions in each register
for f in decisions/*-register.md; do
  count=$(rg "\[\[" "$f" | wc -l)
  echo "$f: $count references"
done

# Check for registers approaching the split threshold (35 decisions)
```

Registers approaching 35 decisions should be flagged for split consideration.

### Check 5: Stale Decisions

```bash
# Find decisions by last_reviewed date
# Flag any older than stale_issue_days from config.yaml
rg "^last_reviewed:" decisions/ --include="*.md" -h | sort | head -20
```

### Check 6: Pending Observations and Tensions Backlog

```bash
# Count pending observations
rg "^status: pending" ops/observations/ --include="*.md" -l | wc -l

# Count pending tensions
rg "^status: pending" ops/tensions/ --include="*.md" -l | wc -l
```

If pending observations > threshold (from config.yaml), flag for /pm-retrospect.
If pending tensions > threshold, flag for /pm-retrospect.

### Check 7: Inbox Pressure

```bash
ls inbox/ | wc -l
```

If inbox has items, flag for /pm-document processing.

---

## Output Format

```
## Audit Complete — YYYY-MM-DD

### System Metrics
- Total decisions: N
- Total decision registers: N
- Total observations (pending/total): N/N
- Total tensions (pending/total): N/N
- Inbox items awaiting processing: N

### Check 1: Orphan Decisions
- Orphans found: N
- [[decision-a]], [[decision-b]] — not referenced by any register

### Check 2: Broken Wiki-Links
- Broken links found: N
- In [[decision-x]]: [[nonexistent-decision]] — target file missing

### Check 3: Schema Violations
- Violations found: N
- [[decision-y]] — missing last_reviewed date
- [[decision-z]] — description is empty

### Check 4: Register Coverage
- [[qftest-register]]: 12 decisions (healthy)
- [[architecture-register]]: 28 decisions (approaching split threshold — flag)
- [[sprint-register]]: 5 decisions (healthy)

### Check 5: Stale Decisions
- Stale decisions (>14 days): N
- [[decision-a]] — last reviewed 21 days ago

### Check 6: Pending Backlog
- Pending observations: N [TRIGGER: /pm-retrospect] if > threshold
- Pending tensions: N [TRIGGER: /pm-retrospect] if > threshold

### Check 7: Inbox
- Inbox items: N [TRIGGER: /pm-document] if > 0

---

### Priority Actions
1. [CRITICAL] Fix N orphan decisions — assign to registers
2. [HIGH] Process N pending observations — run /pm-retrospect
3. [MEDIUM] Update N stale decisions
4. [LOW] Review N schema violations

### Vault Health Score: N/100
[Breakdown: orphans -Xpts, schema violations -Xpts, stale decisions -Xpts, broken links -Xpts]
```

---

## Vault Health Scoring

| Issue | Penalty per instance |
|-------|---------------------|
| Orphan decision | -3 pts |
| Broken wiki-link | -2 pts |
| Schema violation | -2 pts |
| Stale decision (>14 days) | -1 pt |
| Pending observation >threshold | -5 pts flat |
| Pending tension >threshold | -5 pts flat |

Starting from 100. Report final score.
