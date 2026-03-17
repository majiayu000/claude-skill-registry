---
name: specsafe-status
description: Show SpecSafe project status and metrics.
license: MIT
metadata:
  author: Agentic Engineering
  version: "1.0"
---

Show SpecSafe project status, metrics, and spec overview.

**When to use:**
- Check project progress
- View metrics by stage
- See active specs
- Get project overview

**Steps**

1. **Run status command**

   ```bash
   specsafe status
   ```

2. **Display results**

   Show:
   - Project name and version
   - Total specs count
   - Specs by stage (SPEC, TEST, CODE, QA, COMPLETE)
   - Completion rate
   - Recent specs (last 5)
   - Average cycle time

3. **Offer additional actions**

   Based on status, suggest:
   - Continue work on active specs
   - Start new specs
   - Review completed specs
   - Archive old specs

**Output**

Status report including:
- Project metrics
- Stage breakdown
- Recent activity
- Suggestions for next actions

**Example Output**
```
📊 MyProject - Project Status

Metrics:
  Total Specs: 12
  Completion Rate: 58.3%
  Last Updated: 2024-02-04

By Stage:
  SPEC     2
  TEST     1
  CODE     2
  QA       0
  COMPLETE 7

Recent Specs:
  SPEC-20240204-001 - User Auth [CODE]
  SPEC-20240203-002 - Payment API [COMPLETE]
```