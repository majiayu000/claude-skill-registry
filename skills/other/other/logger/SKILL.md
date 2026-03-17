---
name: logger
description: >
  Structured logging and reporting system for development work sessions.
  Trigger: Completing development tasks, generating session reports, documenting changes.
license: MIT
metadata:
  author: aurora
  version: "2.0"
  auto_invoke: "Completing tasks, documenting changes, generating reports"
---

# Logger Skill
Standardized protocol for tracking development activities and generating comprehensive session reports.

## When to Use
Use this skill when:
- You complete a development task or feature
- You want to document what was changed and why
- You need to track which skills/patterns were applied
- You want to generate a summary of work done
- Historical analysis of development sessions is needed
- Documenting architectural decisions and trade-offs

## Purpose
Track development activities and generate detailed reports showing:
- ✅ Files modified/created during the session
- ✅ Skills and patterns applied
- ✅ Business logic implemented
- ✅ Architectural decisions made
- ✅ Performance metrics and duration
- ✅ Historical analysis capabilities

## How It Works
**Structured Logging:** Follow this skill's protocol to log development activities in conversation context.
**In-Memory Accumulation:** All tracking data accumulates during the work session.
**Report Generation:** At session end, compile logs into a comprehensive markdown report.
**Optional Persistence:** Save reports as JSON for historical analysis and documentation.

## Protocol Actions

### 1. Log Development Activity
**When:** At the END of a development session or task completion.
**What to log:** Output structured activity data in conversation context:

```yaml
Work Session Log:
  Task: Add price validation to TeslaModel
  Skills Applied: [typescript, aurora-cqrs, aurora-criteria]
  Patterns Used: [Command Handler validation, Custom exception]
  Files Modified:
    - src/@app/tesla/model/application/create/tesla-create-model.command-handler.ts
    - src/@app/tesla/model/domain/exceptions/tesla-invalid-price.exception.ts
  Tests Added:
    - src/@app/tesla/model/application/create/tesla-create-model.command-handler.spec.ts
  Summary: Implemented price validation (> 0) in command handler with custom exception
  Complexity: Medium
  Status: completed
  Timestamp: 2026-01-16T14:30:45Z
```

**Required fields:**
- `Task` - What you were working on (user request summary)
- `Skills Applied` - Skills/patterns used (or [] if none)
- `Patterns Used` - Architectural patterns applied (or [] if none)
- `Files Modified` - Files created/modified (or [] if none)
- `Tests Added` - Test files created/modified (or [] if none)
- `Summary` - One-sentence description of what was accomplished
- `Complexity` - Low/Medium/High
- `Status` - 'completed' or 'failed'
- `Timestamp` - ISO 8601 timestamp (auto-generated if omitted)

**Example Output:**
```
Work Session Log:
  Task: Implement one-year maintenance validation
  Skills Applied: [aurora-cqrs, aurora-criteria, typescript]
  Patterns Used: [QueryStatement filtering, Custom domain exception]
  Files Modified:
    - src/@app/tesla/maintenance-history/application/create/create-maintenance-history.handler.ts
    - src/@app/tesla/maintenance-history/domain/exceptions/unit-not-revised-exception.ts
  Tests Added:
    - test/acceptance/tesla/maintenance-history.e2e-spec.ts
  Summary: Added business rule validation for maintenance records older than one year
  Complexity: Medium
  Status: completed
  Timestamp: 2026-01-16T15:42:18Z
```

### 2. Generate Session Report
**When:** At task completion, after logging all activities.
**What to do:**
1. Compile all activity logs from the session
2. Generate comprehensive markdown report (see structure below)
3. Display report to user
4. Ask if user wants to save as JSON
5. If yes: Save to `.claude/logs/session-YYYYMMDD-HHMMSS.json`

**Required information:**
- Original task description
- Total session duration (in minutes)
- All activities performed

**Example report initiation:**
```
Generating work session report...

Task: "Add price validation to TeslaModel with exception handling"
Duration: 12 minutes
Activities: [Implementation, Testing, Documentation]
```

## Report Structure
When generating the session report, it follows this structure:

```markdown
# AURORA DEVELOPMENT SESSION REPORT

**Task:** [User's original request]
**Date:** [ISO timestamp]
**Duration:** [total minutes]
**Status:** ✅ Completed / ❌ Failed

---

## Work Summary

**What was done:**
[Brief description of the task and approach taken]

**Architectural decisions:**
[Key decisions made during implementation]

**Patterns applied:**
- [Pattern 1]: [Why it was chosen]
- [Pattern 2]: [Trade-offs considered]

---

## Changes Made

### Files Modified
```
src/@app/tesla/model/
  ├── application/create/
  │   └── tesla-create-model.handler.ts       [Added: price validation]
  └── domain/exceptions/
      └── tesla-invalid-price.exception.ts    [Created: custom exception]
```

### Tests Added
```
test/acceptance/tesla/
  └── model.e2e-spec.ts                       [Added: 3 test cases]
```

---

## Skills & Patterns Applied

| Skill/Pattern | Purpose | Location |
|---------------|---------|----------|
| aurora-cqrs | Command handler logic | CreateTeslaModelHandler |
| typescript | Type-safe validation | Exception classes |
| aurora-criteria | Query filtering | Repository queries |

---

## Metrics

| Metric | Value |
|--------|-------|
| Files modified | 3 |
| Files created | 1 |
| Tests added | 3 |
| Skills applied | 4 |
| Complexity | Medium |
| Duration | 12m |

---

**Save this report?** Would you like to save this session log to `.claude/logs/` for future reference? (y/n)
```

## JSON Persistence Format
If the user opts to save, a JSON file is created with the following structure:
```json
{
  "sessionId": "session-20260116-153045",
  "task": "Add price validation to TeslaModel",
  "timestamp": "2026-01-16T15:30:45Z",
  "duration": "12m",
  "status": "completed",
  "activities": [
    {
      "type": "implementation",
      "skillsApplied": ["aurora-cqrs", "typescript"],
      "patternsUsed": ["Command Handler validation"],
      "filesModified": [
        "src/@app/tesla/model/application/create/tesla-create-model.handler.ts"
      ],
      "summary": "Implemented price validation in command handler",
      "complexity": "medium",
      "timestamp": "2026-01-16T15:30:45Z"
    },
    {
      "type": "exception-handling",
      "skillsApplied": ["typescript"],
      "patternsUsed": ["Custom domain exception"],
      "filesModified": [
        "src/@app/tesla/model/domain/exceptions/tesla-invalid-price.exception.ts"
      ],
      "summary": "Created custom exception for invalid price",
      "complexity": "low",
      "timestamp": "2026-01-16T15:35:20Z"
    },
    {
      "type": "testing",
      "skillsApplied": ["jest-nestjs"],
      "patternsUsed": ["Unit testing", "E2E testing"],
      "filesModified": [
        "test/acceptance/tesla/model.e2e-spec.ts"
      ],
      "summary": "Added 3 test cases for price validation",
      "complexity": "medium",
      "timestamp": "2026-01-16T15:40:10Z"
    }
  ],
  "summary": {
    "totalActivities": 3,
    "uniqueSkills": 3,
    "filesModified": 3,
    "testsAdded": 1,
    "overallComplexity": "medium"
  }
}
```

### Persistence Commands
When the user opts to save, execute:

```bash
mkdir -p .claude/logs
cat > .claude/logs/session-$(date +%Y%m%d-%H%M%S).json <<'EOF'
{JSON_CONTENT_HERE}
EOF

# Create symlink to latest report
ln -sf session-$(date +%Y%m%d-%H%M%S).json .claude/logs/latest.json
```

## Usage Guidelines

### During Development
**OPTIONAL:** Log activities as you work to track progress:
```yaml
Work Session Log:
  Task: [Current task description]
  Skills Applied: [list of skills/patterns used]
  Patterns Used: [architectural patterns applied]
  Files Modified: [files changed]
  Tests Added: [test files created]
  Summary: [one-sentence summary]
  Complexity: [Low/Medium/High]
  Status: [in_progress/completed/failed]
```

### At Task Completion
**RECOMMENDED:** Generate final session report with:
- Original task description (user request)
- Total session duration (from start to completion)
- All activities performed
- Architectural decisions made
- Files modified/created
- Tests added
- Skills and patterns applied
- Offer to save JSON to `.claude/logs/`

## Examples

### Example 1: Implementation Activity Log
**After implementing business logic:**
```yaml
Work Session Log:
  Task: Implement one-year maintenance validation
  Skills Applied: [aurora-cqrs, aurora-criteria, typescript]
  Patterns Used: [Command Handler validation, QueryStatement filtering, Custom exception]
  Files Modified:
    - src/@app/tesla/maintenance-history/application/create/tesla-create-maintenance-history.handler.ts
    - src/@app/tesla/maintenance-history/domain/tesla-unit-not-revised-in-one-year.exception.ts
  Tests Added:
    - test/acceptance/tesla/maintenance-history.e2e-spec.ts
  Summary: Implemented one-year validation using QueryStatement with [gte] operator and custom exception
  Complexity: Medium
  Status: completed
  Timestamp: 2026-01-16T15:42:30Z
```

### Example 2: Refactoring Activity Log
**After refactoring code:**
```yaml
Work Session Log:
  Task: Extract validation logic to reusable service
  Skills Applied: [aurora-project-structure, typescript, aurora-development]
  Patterns Used: [Service extraction, Dependency injection]
  Files Modified:
    - src/@app/tesla/model/application/services/tesla-validation.service.ts
    - src/@app/tesla/model/application/create/tesla-create-model.handler.ts
    - src/@app/tesla/model/application/update/tesla-update-model.handler.ts
  Tests Added:
    - src/@app/tesla/model/application/services/tesla-validation.service.spec.ts
  Summary: Extracted duplicate validation logic into shared service with DI
  Complexity: Medium
  Status: completed
  Timestamp: 2026-01-16T15:40:15Z
```

### Example 3: Session Report Generation
**At task completion, generate comprehensive report:**
```
## Session Report Generation

Task: "Cuando se cree un mantenimiento nuevo, si desde el último mantenimiento ha pasado un año, quiero que mandes una excepción"
Duration: 12 minutes

Activities performed:
- Business logic implementation
- Exception handling
- Unit and e2e testing

[Generates comprehensive markdown report as specified in Report Structure section]

Would you like to save this session report to .claude/logs/ for future reference? (y/n)
```

## Benefits
- ✅ **Visibility:** Document what was accomplished in each session
- ✅ **Traceability:** Track which skills and patterns were applied
- ✅ **Learning:** Understand which approaches work best
- ✅ **Audit:** Historical analysis of development decisions
- ✅ **Documentation:** Automatic generation of session reports
- ✅ **Accountability:** Clear record of changes and their reasoning
- ✅ **Knowledge sharing:** Share reports with team members

## Maintenance
To modify report format or add new metrics:
- Edit only this skill file (`.claude/skills/logger/SKILL.md`)
- Changes apply to all future sessions automatically
- No need to modify other files

## Analysis Commands
Once you have historical data in `.claude/logs/`, you can analyze it:

```bash
# View latest report
cat .claude/logs/latest.json | jq .

# List all session reports
ls -lht .claude/logs/*.json

# Most used skills
cat .claude/logs/*.json | jq -r '.activities[].skillsApplied[]' | sort | uniq -c | sort -rn

# Most used patterns
cat .claude/logs/*.json | jq -r '.activities[].patternsUsed[]' | sort | uniq -c | sort -rn

# Files modified most frequently
cat .claude/logs/*.json | jq -r '.activities[].filesModified[]' | sort | uniq -c | sort -rn

# Average session duration
cat .claude/logs/*.json | jq -r '.duration' | sed 's/m//' | awk '{sum+=$1; n++} END {print sum/n "m"}'

# Sessions by complexity
cat .claude/logs/*.json | jq -r '.summary.overallComplexity' | sort | uniq -c
```

---

## Remember
- ✅ This is a **documentation and logging skill**
- ✅ Log activities as you complete tasks
- ✅ Use structured YAML format for activity logs
- ✅ Generate comprehensive report at session end
- ✅ All tracking data accumulates in conversation context
- ✅ Reports can be persisted to `.claude/logs/` for historical analysis
- ✅ Modify report format by editing this skill file only

**Note:** This skill helps document development work systematically, creating a clear audit trail of what was done, why, and how.
