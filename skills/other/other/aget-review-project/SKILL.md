---
name: aget-review-project
description: Mid-flight review of active project plans. Assesses gate progress, V-test completion, blockers, and recommendations. Use to evaluate project health.
version: 1.0.0
---

# /aget-review-project

Perform mid-flight review of an active project plan. Evaluates progress, identifies blockers, and generates recommendations.

## Purpose

Enable AGETs to self-assess project health. Provides structured evaluation against success criteria and V-tests, supporting proactive course correction.

## Input

$ARGUMENTS - Path to PROJECT_PLAN file (optional, defaults to current project context)

## Execution

### Step 1: Locate Project Plan

```bash
# If path provided
test -f "$ARGUMENTS" && echo "found"

# If no path, search for active projects
ls planning/PROJECT_PLAN_*.md 2>/dev/null
```

If multiple projects found, prompt user to select.

### Step 2: Parse Project Structure

Extract from project plan:
1. **Metadata**: Version, Status, Created, Author, POC
2. **Gates**: All G-X sections with their V-tests
3. **Success Criteria**: Target metrics
4. **Risk Assessment**: Identified risks

### Step 3: Evaluate V-Tests

For each gate, check V-test status:

```
Status indicators in plan:
- "✅" or "PASS" or "Complete" → Passed
- "❌" or "FAIL" → Failed
- "Pending" or unmarked → Not started
- "IN_PROGRESS" → Active
```

Calculate:
- Total V-tests
- Passed V-tests
- Completion percentage

### Step 4: Identify Blockers

Scan for:
- Failed V-tests
- Dependencies on pending gates
- Risk items marked as materialized
- Items marked BLOCKED

### Step 5: Generate Recommendations

Based on evaluation:
1. **Next Actions**: Immediate steps for current gate
2. **Risk Alerts**: Risks close to materializing
3. **Scope Adjustments**: If behind schedule or blocked

### Step 6: Output Report

## Output Format

```
=== /aget-review-project ===

Project: <project name>
POC: <POC-XXX if applicable>
Status: <overall status>

Gate Progress:
  G-0: [x] Complete (X/X V-tests)
  G-1: [~] In Progress (X/Y V-tests)
  G-2: [ ] Pending
  ...
  G-F: [ ] Pending

Summary:
  Total V-tests: <count>
  Passed: <count> (<percentage>%)
  Failed: <count>
  Pending: <count>

Blockers:
  [list or "None identified"]

Recommendations:
  1. <specific action>
  2. <specific action>
  ...

Overall Assessment:
  <brief assessment of project health>

Health Status: [OK | WARN | CRITICAL]
```

## Health Status Logic

```
IF failed_vtests > 0 AND no_progress:
  CRITICAL
ELIF completion < 25% AND started > 7_days_ago:
  WARN
ELIF blockers_count > 3:
  WARN
ELSE:
  OK
```

## Constraints

- **C1**: Read-only operation. Never modify project files.
- **C2**: Must report all gates, even if empty.
- **C3**: Recommendations must be actionable.
- **C4**: Never assess projects outside write scope.

## Related Skills

- `/aget-create-project` - Create new project plans
- `/aget-healthcheck-evolution` - Check L-doc health
- `/aget-record-lesson` - Capture lessons during review

## Traceability

| Link | Reference |
|------|-----------|
| POC | POC-017 |
| Project | PROJECT_PLAN_AGET_UNIVERSAL_SKILLS.md |
| Proposal | PROPOSAL_aget-review-project.md |
| Source | Fleet Skill Deployment Report (supervisor) |

---

*aget-review-project v1.0.0*
*Category: Planning*
*POC-017 Phase 6*
