---
name: umbraco-skill-validator
description: Validate links and references in SKILL.md files using deterministic scripts
allowed-tools: Bash, Read, Glob, Task, AskUserQuestion, Edit
---

# Skill Content Validator

Validates all SKILL.md files in the repository for broken links, missing references, and invalid paths.

## What This Skill Does

1. **Runs deterministic validation script** - Fast, consistent checking of all links
2. **Generates structured report** - JSON output with all issues found
3. **Spawns fixer subagent** - AI-powered fix suggestions for issues
4. **Presents fix plan** - Diff-style changes for approval
5. **Executes approved fixes** - Only applies changes user approves

## Validation Checks

| Check Type | Description |
|------------|-------------|
| External URLs | HTTP HEAD request to verify accessibility |
| Skill references | Verify referenced skills exist (e.g., `umbraco-dashboard`) |
| Internal links | Check relative paths resolve (e.g., `patterns/foo.md`) |
| File paths | Verify Umbraco-CMS paths via GitHub API if not local |
| Import paths | Check `@umbraco-cms/backoffice/*` imports are valid |

## Running the Validator

### Via Slash Command
```
/validate-skills
```

### Via Script Directly (CI/CD)
```bash
cd .claude/skills/umbraco-skill-validator/scripts
npm install
npm run validate
```

## Report Format

The script outputs JSON that gets formatted as:

```markdown
# Skill Validation Report

## Summary
- Skills scanned: 25
- Issues found: 3
- Auto-fixable: 2

## Issues by Skill

### `umbraco-dashboard`
| Line | Type | Issue | Status |
|------|------|-------|--------|
| 45 | Broken URL | [example-broken-url] returns 404 | :x: |

### `umbraco-tree`
| Line | Type | Issue | Status |
|------|------|-------|--------|
| 72 | Missing skill | [example-missing-skill] not found | :x: |
```

## Fix Plan Format

When issues are found, the fixer subagent generates:

```markdown
# Fix Plan

## Fix 1: Update broken URL
**File:** plugins/.../umbraco-dashboard/SKILL.md
**Line:** 45
**Action:** Replace with current documentation URL

- [Dashboard docs][old-url]
+ [Dashboard docs][new-url]

## Approval
- [ ] Fix 1: Update broken URL
- [ ] Fix 2: ...
```

## Link Patterns Detected

### External URLs
```
https://docs.umbraco.com/...
https://github.com/umbraco/...
```

### Skill References
```
`umbraco-dashboard`
`umbraco-workspace`
```

### Internal Pattern Links
```
[Pattern Name](patterns/pattern-name.md)
[Example](examples/example-name/)
```

### File Paths
```
/Umbraco-CMS/src/Umbraco.Web.UI.Client/...
src/packages/core/...
```

### Import Paths (in code blocks)
```typescript
import { ... } from '@umbraco-cms/backoffice/notification';
```

## Workflow Instructions

When this skill is invoked:

1. **Run the validation script**
   ```bash
   cd .claude/skills/umbraco-skill-validator/scripts
   npx tsx validate-links.ts
   ```

2. **Read the JSON output** from stdout or `validation-report.json`

3. **Format as markdown report** using the template above

4. **If issues found**, spawn the `skill-content-fixer` agent:
   - Pass the JSON report as context
   - Request fix suggestions with diffs

5. **Present fix plan** to user with AskUserQuestion

6. **Execute only approved fixes** using Edit tool

## Edge Cases

- **Rate limiting**: Script batches URL checks with 100ms delays
- **Redirects**: Reported as warnings with new URL suggestion
- **Missing Umbraco-CMS**: Falls back to GitHub API
- **Timeouts**: 5 second timeout per URL request
- **Large repos**: Processes files in batches of 10
