---
name: validate-all
description: Run comprehensive validation on all site content. Use for daily health checks or before deployment.
---

# Validate All Content

Run comprehensive validation checks on The Unfinishable Map site content.

## When to Use

- Daily automated health checks
- Before deploying to production
- After major content changes
- When `/validate-all` is invoked

## Instructions

Execute these validation steps in order:

### 1. Frontmatter Validation

Run the validation script:
```bash
uv run python scripts/validate.py hugo/content/ --strict
```

Report any validation errors or warnings.

### 2. Link Checking

Run the `/check-links` skill to verify all internal links are valid.

If the Hugo dev server is not running, note that link checking was skipped.

### 3. Orphan Detection

Find content files with no inbound links:
1. Read all markdown files in `hugo/content/`
2. Extract all internal links from each file
3. Identify files that are never linked to (except index files)
4. Report orphaned content for human review

### 4. Stale Draft Detection

Find draft content older than 30 days:
1. Find all files with `draft: true` in frontmatter
2. Check the `created` or `modified` date
3. If older than 30 days, flag as stale
4. Report stale drafts for human review

### 5. Length Analysis

Check article lengths against section-specific thresholds:

```bash
uv run python -c "
from pathlib import Path
from tools.curate.length import get_length_summary

summary = get_length_summary(Path('obsidian'))
print(f'Critical: {summary[\"critical_count\"]}')
print(f'Hard warnings: {summary[\"hard_warning_count\"]}')
print(f'Soft warnings: {summary[\"soft_warning_count\"]}')
for w in summary['worst_offenders'][:5]:
    print(f'  {w[\"path\"]}: {w[\"words\"]} words ({w[\"excess_percent\"]:.0f}%)')
"
```

**Thresholds by section:**
| Section | Target | Hard | Critical |
|---------|--------|------|----------|
| concepts/ | 2500 | 3500 | 5000 |
| topics/ | 3000 | 4000 | 6000 |
| apex/ | 4000 | 5000 | 6500 |
| voids/ | 2000 | 3000 | 4000 |

Report critical and hard warnings. Note soft warnings only if concerning trend.

### 6. Log Results

Prepend results to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries).

## Output Format

```markdown
## [current time from prompt] - validate-all
- **Status**: Success/Warnings/Errors
- **Files validated**: N
- **Errors**: List or "None"
- **Warnings**: List or "None"
- **Orphaned content**: List as wikilinks or "None"
- **Stale drafts**: List as wikilinks or "None"

**Length Warnings:**
| Status | Count | Worst |
|--------|-------|-------|
| Critical | N | [[filename]] (X%) |
| Hard | N | [[filename]] (X%) |
| Soft | N | (noted if >50% of articles) |
```

## Important

- This skill is READ-ONLY for content files
- Only writes to `changelog.md`
- Does not modify any content
- Reports issues for human review
