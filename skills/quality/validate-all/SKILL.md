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

### 5. Log Results

Append results to `obsidian/workflow/changelog.md` with:
- Timestamp
- Status (Success/Warnings/Errors)
- Count of files validated
- Any errors or warnings found
- List of orphaned content (if any)
- List of stale drafts (if any)

## Output Format

```markdown
### HH:MM - validate-all
- **Status**: Success/Warnings/Errors
- **Files validated**: N
- **Errors**: List or "None"
- **Warnings**: List or "None"
- **Orphaned content**: List or "None"
- **Stale drafts**: List or "None"
```

## Important

- This skill is READ-ONLY for content files
- Only writes to `changelog.md`
- Does not modify any content
- Reports issues for human review
