---
name: project-status
description: Quick "where are we? what's next?" dashboard with handoffs, sessions, imports, and git activity
---

# Project Status

## Overview

Get instant project status visibility: active handoffs, recent work, import queue, and git activity.

**Use when:** Starting a session, returning after time away, checking project state.

**Announce at start:** "I'm using the project-status skill to show current project status."

## What This Skill Does

Aggregates status from multiple sources:
1. **Active Handoffs** - Work requiring attention (from `/docs/handoffs/current/`)
2. **Recent Sessions** - Last 5 work summaries (from `/docs/sessions/`)
3. **Current TODOs** - Action items (from `/docs/status/TODO-*.md`)
4. **Import Queue** - Files awaiting import (from `/imports/`)
5. **Recent Activity** - Last 10 git commits

## Operation

### Display Project Status

**Process:**

1. **Collect Active Handoffs**
   ```bash
   find /Users/anthonybyrnes/PycharmProjects/Python419/docs/handoffs/current -name "*.md" -type f | sort -r
   ```

   For each handoff:
   - Extract filename
   - Read YAML frontmatter to get creation date
   - Calculate age (days since creation)
   - Extract title from filename

2. **List Recent Sessions**
   ```bash
   find /Users/anthonybyrnes/PycharmProjects/Python419/docs/sessions -name "SESSION-*.md" -type f | sort -r | head -5
   ```

   Show last 5 session files

3. **Check TODO Files**
   ```bash
   ls /Users/anthonybyrnes/PycharmProjects/Python419/docs/status/TODO-*.md 2>/dev/null
   ```

   Read and display content of TODO files

4. **Count Import Queue**
   ```bash
   # Inbox
   find /Users/anthonybyrnes/PycharmProjects/Python419/imports/inbox -type f 2>/dev/null | wc -l

   # Staged by type
   for type in lbhra ps-lb lbsr08e 419f program-list cota-persistence; do
     find /Users/anthonybyrnes/PycharmProjects/Python419/imports/staged/$type -type f 2>/dev/null | wc -l
   done

   # Processing
   find /Users/anthonybyrnes/PycharmProjects/Python419/imports/processing -type f 2>/dev/null | wc -l
   ```

5. **Show Recent Git Activity**
   ```bash
   cd /Users/anthonybyrnes/PycharmProjects/Python419
   git log --oneline -10
   ```

6. **Display NEXT_STEPS if exists**
   ```bash
   cat /Users/anthonybyrnes/PycharmProjects/Python419/docs/status/NEXT_STEPS.md
   ```

## Output Format

```markdown
## Project Status - 2025-11-14

### Active Handoffs (2)
- import-coverage-completion
  Created: 2025-11-13 (1 day ago)
  File: docs/handoffs/current/2025-11-13-import-coverage-completion-handoff.md

- formula-correction-audit
  Created: 2025-11-13 (1 day ago)
  File: docs/handoffs/current/2025-11-13-formula-correction-audit-handoff.md

### Recent Sessions (last 5)
- SESSION-2025-11-13-import-coverage-matrix-handoff.md
- SESSION-2025-11-12-import-status-dashboard-mvp.md
- SESSION-2025-11-12-delta-cost-dashboard-mvp.md
- SESSION-2025-11-12-COMPLETE-SUMMARY.md
- SESSION-2025-11-12-autonomous-development.md

### Import Queue
Inbox: 0 files
Staged: 12 files
  - LBHRA: 5
  - PS_LB: 4
  - 419F: 3
Processing: 0 files

### Next Steps
[Content from /docs/status/NEXT_STEPS.md]

### Recent Activity (last 10 commits)
[git log --oneline -10]
```

## Implementation Details

**Date Calculation:**
```python
from datetime import datetime

def calculate_age(created_date_str: str) -> str:
    """Calculate age in days from YYYY-MM-DD string."""
    created = datetime.strptime(created_date_str, '%Y-%m-%d')
    today = datetime.now()
    delta = today - created
    days = delta.days

    if days == 0:
        return "today"
    elif days == 1:
        return "1 day ago"
    else:
        return f"{days} days ago"
```

**Parse Handoff Filename:**
```python
import re

def parse_handoff_filename(filename: str) -> tuple:
    """Extract date and title from handoff filename."""
    # Pattern: YYYY-MM-DD-{title}-handoff.md
    match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)-handoff\.md', filename)
    if match:
        date_str = match.group(1)
        title = match.group(2).replace('-', ' ').title()
        return (date_str, title)
    return (None, filename)
```

**Extract YAML Frontmatter:**
```python
import re

def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        import yaml
        return yaml.safe_load(match.group(1))
    return {}
```

## Usage Example

**User:** "What's the current project status?"

**Assistant:** "I'm using the project-status skill to show current project status."

[Runs all collection steps]

**Output:**
```
## Project Status - 2025-11-14

### Active Handoffs (2)
- Import Coverage Completion
  Created: 2025-11-13 (1 day ago)
  File: docs/handoffs/current/2025-11-13-import-coverage-completion-handoff.md

- Formula Correction Audit
  Created: 2025-11-13 (1 day ago)
  File: docs/handoffs/current/2025-11-13-formula-correction-audit-handoff.md

### Recent Sessions (last 5)
- SESSION-2025-11-13-import-coverage-matrix-handoff.md
- SESSION-2025-11-12-import-status-dashboard-mvp.md
- SESSION-2025-11-12-delta-cost-dashboard-mvp.md
- SESSION-2025-11-12-COMPLETE-SUMMARY.md
- SESSION-2025-11-12-autonomous-development.md

### Import Queue
Inbox: 0 files
Staged: 12 files
  - LBHRA: 5 files
  - PS_LB: 4 files
  - 419F: 3 files
Processing: 0 files

### Next Steps
[Displays content from NEXT_STEPS.md]

### Recent Activity (last 10 commits)
d5c98fc docs: add comprehensive quick start guide for web UI features
dd025d4 docs: add remaining web UI session summaries and implementation plans
5943b09 docs: add comprehensive session summary for Import Status Dashboard MVP
685f61c feat: complete Task 8 - Import Status Dashboard integration
da09d53 feat: add sortable ImportHistoryTable component
...
```

## Integration

**Used by:**
- Session startup workflow
- Project handoff preparation
- Status check during development

**Depends on:**
- `/docs/handoffs/current/` - Active handoffs
- `/docs/sessions/` - Session summaries
- `/docs/status/` - TODO and NEXT_STEPS files
- `/imports/` - Import workflow directories
- Git repository - Recent commits

## Common Mistakes

**Reading deleted files:**
- **Problem:** Try to read files that have been archived
- **Fix:** Only scan current/ directory, not resolved/ or archive/

**Not handling empty directories:**
- **Problem:** Errors when directories are empty
- **Fix:** Use `2>/dev/null` to suppress errors, show "0 files" for empty

**Stale git log:**
- **Problem:** Not running from correct directory
- **Fix:** Always cd to project root before git log

## Red Flags

**Never:**
- Modify any files (read-only operation)
- Run without announcing skill usage
- Skip sections if data is missing (show "0" or "None")
- Cache results (always run fresh)

**Always:**
- Calculate ages dynamically (not from cache)
- Show absolute file paths
- Handle missing directories gracefully
- Display all sections even if empty
