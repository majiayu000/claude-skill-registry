---
name: sync-paper
description: Synchronize paleoseismic research documents to ensure consistency. Use when checking if catalogs match paper, finding documentation drift, or updating summaries. Triggers on "sync paper", "check consistency", "document sync", "update catalog".
---

# /sync-paper - Cross-Document Synchronization Skill

## Purpose

Ensure consistency between the authoritative paper (`PAPER_2_DARK_EARTHQUAKES.md`) and summary documents (`ANOMALY_CATALOG.md`, `ANOMALY_TRACKING.md`, `GAPS_AND_PRIORITIES.md`). Prevents documentation drift.

## Usage

```
/sync-paper [--check | --update | --region REGION]
```

**Examples:**
```
/sync-paper --check                    # Find inconsistencies (read-only)
/sync-paper --update                   # Generate updates for approval
/sync-paper --region italy             # Check only Italy section
/sync-paper --check --verbose          # Detailed comparison
```

## Document Hierarchy

```
PAPER_2_DARK_EARTHQUAKES.md    ← AUTHORITATIVE SOURCE (57k+ tokens)
         │
         ├──→ ANOMALY_CATALOG.md       (Americas summaries)
         ├──→ ANOMALY_TRACKING.md      (Italy summaries)
         ├──→ GAPS_AND_PRIORITIES.md   (Task status only)
         └──→ CLAUDE.md                (Project Statistics)
```

**Rule**: Information flows DOWN from the paper. Catalogs are SUMMARIES.

## Synchronization Checks

### 1. Event Count Consistency

Check that event counts match across documents:

```markdown
| Region | Paper Count | Catalog Count | Match? |
|--------|-------------|---------------|--------|
| Motagua (Belize) | 7 seismic + 2 CVSE | 7 seismic + 2 CVSE | ✓ |
| Italy (Bàsura) | 1 confirmed + 1 candidate | 1 + 1 | ✓ |
| California | 3 prehistoric + 1 pre-Spanish | 3 + 1 | ✓ |
```

### 2. Classification Consistency

Check event classifications match:

```markdown
| Event | Paper Classification | Catalog Classification | Match? |
|-------|---------------------|------------------------|--------|
| ~1394 Italy | CANDIDATE DARK | CANDIDATE DARK | ✓ |
| ~1741 CA | PRE-SPANISH | ~~DARK~~ PRE-SPANISH | ✗ UPDATE |
| Brazil ~96 | TRUE DARK | TRUE DARK | ✓ |
```

### 3. Statistics Consistency

Check CLAUDE.md Project Statistics table:

```markdown
| Statistic | Paper Value | CLAUDE.md Value | Match? |
|-----------|-------------|-----------------|--------|
| Italy anomalies | 32 | 32 | ✓ |
| Motagua events | 7 + 2 CVSE | 7 + 2 CVSE | ✓ |
| Cascadia detection | 7/15 (46.7%) | 7/15 (46.7%) | ✓ |
```

### 4. Task Status (GAPS)

Check that completed work is marked in GAPS:

```markdown
| Task | Paper Status | GAPS Status | Match? |
|------|--------------|-------------|--------|
| MS5 (fault verification) | ✅ Complete | PENDING | ✗ MARK COMPLETE |
| IC1 (Pallett Creek) | ✅ Complete | ✅ DONE | ✓ |
```

## Workflow

### Step 1: Read Source Documents

Read the following files:
1. `publication/PAPER_2_DARK_EARTHQUAKES.md` (authoritative)
2. `catalogs/ANOMALY_CATALOG.md`
3. `catalogs/ANOMALY_TRACKING.md`
4. `GAPS_AND_PRIORITIES.md`
5. `CLAUDE.md` (Project Statistics section)

### Step 2: Extract Key Data

From PAPER_2:
- Event lists by region
- Classifications (DARK, PRE-HISTORICAL, etc.)
- Detection rates
- Evidence tiers

From Catalogs:
- Summary tables
- Event counts
- Classifications

### Step 3: Compare & Report

Generate comparison report:

```markdown
## Synchronization Report

**Generated**: [date]
**Paper version**: [last modified date]

### ✓ Consistent Items (N)
- [list of matching items]

### ✗ Inconsistencies Found (N)

#### 1. [Issue Title]
**Location**: `ANOMALY_CATALOG.md` Section X
**Paper says**: [value]
**Catalog says**: [different value]
**Action**: Update catalog to match paper

#### 2. [Issue Title]
...

### Recommended Updates

1. Edit `ANOMALY_CATALOG.md`:
   - Line X: Change "DARK" to "PRE-SPANISH"

2. Edit `GAPS_AND_PRIORITIES.md`:
   - Mark MS5 as ✅ COMPLETE

3. Edit `CLAUDE.md`:
   - Update Project Statistics table row X
```

### Step 4: Generate Updates (if --update)

Produce specific edits:

```markdown
## Proposed Updates

### 1. ANOMALY_CATALOG.md

Old:
| ~1741 CA | **DARK** | Rose Canyon | ... |

New:
| ~1741 CA | **PRE-SPANISH** | Rose Canyon (known fault) | ... |

### 2. GAPS_AND_PRIORITIES.md

Add to MS5 line:
| **~~MS5~~** | ~~Update papers with fault verification~~ | ✅ COMPLETE 2026-01-03 |

Apply these updates? [Y/n]
```

## Common Sync Issues

### Issue 1: Classification Drift
**Symptom**: Event called "dark" in catalog but reclassified in paper
**Fix**: Update catalog classification to match paper

### Issue 2: Missing Events
**Symptom**: New event in paper not in catalog
**Fix**: Add summary entry to catalog

### Issue 3: Outdated Statistics
**Symptom**: CLAUDE.md counts don't match paper
**Fix**: Update Project Statistics table

### Issue 4: Stale Tasks
**Symptom**: Task completed in paper but GAPS still shows pending
**Fix**: Mark task complete in GAPS

### Issue 5: Duplicate Content
**Symptom**: Full analysis in catalog that should only be in paper
**Fix**: Replace with summary + pointer to paper

## Output Format

### Check Mode (--check)

```
📊 SYNC CHECK REPORT

Documents checked:
- PAPER_2_DARK_EARTHQUAKES.md (last modified: 2026-01-03)
- ANOMALY_CATALOG.md
- ANOMALY_TRACKING.md
- GAPS_AND_PRIORITIES.md
- CLAUDE.md

Results:
✓ 23 items consistent
✗ 3 inconsistencies found

Issues:
1. [Issue 1 summary]
2. [Issue 2 summary]
3. [Issue 3 summary]

Run `/sync-paper --update` to generate fixes.
```

### Update Mode (--update)

```
📝 SYNC UPDATES

Generating fixes for 3 inconsistencies...

### Update 1: ANOMALY_CATALOG.md
[specific edit]

### Update 2: GAPS_AND_PRIORITIES.md
[specific edit]

### Update 3: CLAUDE.md
[specific edit]

Apply all updates? [Y/n]
```

## Best Practices

1. **Run weekly** - Prevents drift accumulation
2. **After major analysis** - Sync immediately after paper updates
3. **Before publication prep** - Ensure all docs consistent
4. **Check before citing** - Verify catalog matches paper

## Document Update Order

When updating, follow this order:
1. **PAPER_2_DARK_EARTHQUAKES.md** - Add/update analysis
2. **Regional files** - Update detailed analysis docs
3. **ANOMALY_CATALOG.md** - Update summary
4. **GAPS_AND_PRIORITIES.md** - Update task status
5. **CLAUDE.md** - Update statistics if changed

**Never update catalog without updating paper first.**

## Files Checked

| File | Purpose |
|------|---------|
| `publication/PAPER_2_DARK_EARTHQUAKES.md` | Authoritative source |
| `catalogs/ANOMALY_CATALOG.md` | Americas summaries |
| `catalogs/ANOMALY_TRACKING.md` | Italy summaries |
| `GAPS_AND_PRIORITIES.md` | Task tracking |
| `CLAUDE.md` | Project statistics |
