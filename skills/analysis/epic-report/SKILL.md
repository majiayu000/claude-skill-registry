---
name: epic-report
description: Generate epic progress reports. Use for epic status, story tracking, blocker detection, and progress summaries.
---

# /epic-report - Epic Completion Report

Generate a completion report for an epic.

## Usage

```
/epic-report <epic-number>
```

**Example:**
```
/epic-report 441
```

## What This Skill Does

1. **Fetches Epic Data** - Uses `gh issue view` to get epic details
2. **Finds Related Issues** - Searches for issues mentioning the epic
3. **Analyzes Completion** - Checks status of each story/task
4. **Detects Blockers** - Finds TODOs in changed files
5. **Generates Report** - Creates structured markdown

## Report Sections

### 1. Epic Summary
- Title and objective
- Overall completion percentage
- Date range

### 2. Stories Status Table
| Story | Title | Status | Notes |
|-------|-------|--------|-------|
| #442 | Story title | Complete | |
| #443 | Story title | In Progress | Blocked by X |

### 3. Test Results Summary
- Total tests run
- Passed/Failed/Skipped
- Link to Allure report if available

### 4. Artifacts Created
- New files added
- Modified files
- Location and purpose

### 5. Blocking Issues
- TODOs found in code
- Failing tests
- Open dependencies

### 6. Next Steps
- Recommended follow-up actions
- Issues to create
- Documentation needed

## Implementation Notes

To generate the report, execute these steps:

1. **Get Epic Details:**
   ```bash
   gh issue view <epic-number> --repo krazyuniks/guitar-tone-shootout --json title,body,state
   ```

2. **Find Related Issues:**
   ```bash
   gh issue list --repo krazyuniks/guitar-tone-shootout --search "epic:<epic-number>" --json number,title,state
   ```

3. **Check for TODOs in Changed Files:**
   ```bash
   git diff main...HEAD --name-only | xargs grep -n "TODO:" 2>/dev/null || true
   ```

4. **Check for Allure Reports:**
   ```bash
   ls -la tests/allure-report/index.html 2>/dev/null
   ```

## Output Format

Generate the report as markdown and output it directly to the conversation.
The report should be structured, scannable, and include links to relevant issues.
