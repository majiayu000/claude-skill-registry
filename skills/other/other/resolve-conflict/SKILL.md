---
name: resolve-conflict
description: Resolve disagreements between Cursor and Gemini feedback using weighted expertise.
version: 1.1.0
tags: [conflict, review, governance]
owner: orchestration
status: active
---

# Resolve Conflict Skill

Resolve disagreements between Cursor and Gemini agents.

## Overview

When agents disagree on approval or have conflicting assessments, this skill provides structured conflict resolution using weighted expertise and escalation rules.

## Usage

```
/resolve-conflict
```

## Prerequisites

- Cursor and Gemini feedback available in `phase_outputs`.

## When to Use

Use this skill when:
- One agent approves, another doesn't
- Agents have significantly different scores (>2 points)
- Blocking issues conflict between agents
- Manual resolution is needed

## Agent Expertise Weights

| Agent | Area | Weight | Rationale |
|-------|------|--------|-----------|
| Cursor | Security | **0.8** | Primary security expertise |
| Cursor | Code Quality | 0.7 | Strong in patterns |
| Cursor | Testing | 0.7 | Test coverage focus |
| Gemini | Architecture | **0.7** | Design pattern expert |
| Gemini | Scalability | **0.8** | Performance focus |
| Gemini | Maintainability | 0.6 | Long-term view |

## Resolution Strategies

### Strategy 1: Expertise-Based (Default)

Route decision to agent with higher expertise weight:

```
IF issue.type == "security":
    winner = cursor  # weight 0.8

ELIF issue.type in ["architecture", "scalability"]:
    winner = gemini  # weight 0.7-0.8

ELIF issue.type == "code_quality":
    # Average both opinions
    resolved_score = (cursor.score * 0.7 + gemini.score * 0.6) / 1.3
```

### Strategy 2: Conservative (Phase 4)

In verification phase, take the MORE CONSERVATIVE view:

```
# If either agent blocks, it's blocked
IF cursor.blocking_issues OR gemini.blocking_issues:
    result = blocked

# Take lower score
final_score = min(cursor.score, gemini.score)

# Combine all concerns
all_concerns = cursor.concerns + gemini.concerns
```

### Strategy 3: Weighted Average

For scores and non-critical assessments:

```
# Based on issue type
security_weight = 0.6  # More weight to Cursor
architecture_weight = 0.4  # More weight to Gemini

weighted_score = (
    cursor.score * security_weight +
    gemini.score * architecture_weight
)
```

### Strategy 4: Human Escalation

Escalate to human when:
- Both agents have blocking issues
- Score difference > 4 points
- Issue classification unclear
- Third attempt still has conflicts

## Resolution Process

### 1. Load Feedback

```python
cursor_feedback = phase_outputs_repo.get_by_type(phase=phase, output_type="cursor_feedback")
gemini_feedback = phase_outputs_repo.get_by_type(phase=phase, output_type="gemini_feedback")
```

### 2. Identify Conflicts

```python
conflicts = []

# Approval mismatch
if cursor.approved != gemini.approved:
    conflicts.append({
        "type": "approval_mismatch",
        "cursor": cursor.approved,
        "gemini": gemini.approved
    })

# Score difference
if abs(cursor.score - gemini.score) > 2:
    conflicts.append({
        "type": "score_difference",
        "cursor": cursor.score,
        "gemini": gemini.score,
        "difference": abs(cursor.score - gemini.score)
    })

# Conflicting assessments
for cursor_issue in cursor.concerns:
    for gemini_strength in gemini.strengths:
        if similar(cursor_issue.area, gemini_strength):
            conflicts.append({
                "type": "assessment_conflict",
                "area": cursor_issue.area,
                "cursor_view": "concern",
                "gemini_view": "strength"
            })
```

### 3. Resolve Each Conflict

```python
resolutions = []

for conflict in conflicts:
    if conflict.type == "approval_mismatch":
        # Check what's driving the non-approval
        if blocker_is_security:
            resolution = cursor_wins()
        elif blocker_is_architecture:
            resolution = gemini_wins()
        else:
            resolution = escalate_to_human()

    elif conflict.type == "score_difference":
        resolution = weighted_average(conflict)

    resolutions.append(resolution)
```

### 4. Generate Resolution Document

Write conflict resolution output to `phase_outputs` (type=validation_consolidated or verification_consolidated):

```json
{
  "conflicts_found": 2,
  "conflicts": [
    {
      "type": "approval_mismatch",
      "cursor_position": "reject",
      "gemini_position": "approve",
      "resolved_by": "cursor",
      "reason": "Security concern takes precedence",
      "strategy": "expertise_based"
    }
  ],
  "final_decision": {
    "approved": false,
    "score": 6.5,
    "primary_concern": "SQL injection vulnerability",
    "action_required": "Fix security issue before proceeding"
  },
  "escalated_to_human": false
}
```

## Decision Matrix

| Cursor | Gemini | Issue Type | Resolution |
|--------|--------|------------|------------|
| Approve | Approve | - | **Approved** |
| Approve | Reject | Architecture | **Gemini wins** |
| Approve | Reject | Security | Review Gemini's concern |
| Reject | Approve | Security | **Cursor wins** |
| Reject | Approve | Architecture | Review Cursor's concern |
| Reject | Reject | Any | **Rejected** + combine issues |
| Reject | Reject | Different | **Escalate** |

## Escalation to Human

When escalating:

1. **Prepare Summary**:
   ```markdown
   ## Conflict Requiring Human Decision

   ### Cursor Assessment
   - Score: 5.0
   - Position: Reject
   - Blocking Issue: "Potential XSS vulnerability in user input"

   ### Gemini Assessment
   - Score: 8.0
   - Position: Approve
   - View: "Input is server-side only, XSS not applicable"

   ### Conflict
   Cursor sees security risk, Gemini sees it as false positive.

   ### Options
   1. Accept Cursor's view - implement additional sanitization
   2. Accept Gemini's view - document as intentional design
   3. Request more information from both agents
   ```

2. **Pause Workflow**:
   - Set state to "awaiting_human_decision"
   - Save escalation document
   - Notify user

3. **Resume on Decision**:
   - User provides decision
   - Log decision and rationale
   - Continue workflow with decision applied

## Integration Example

```
# In /validate-plan or /verify-code skill:

# After running both agents
cursor_result = parse(cursor_feedback)
gemini_result = parse(gemini_feedback)

# Check for conflicts
if cursor_result.approved != gemini_result.approved:
    # Invoke conflict resolution
    resolution = resolve_conflict(cursor_result, gemini_result, phase="validation")

    if resolution.escalated:
        pause_for_human()
    else:
        apply_resolution(resolution)
```

## Outputs

- Consolidated decision stored in `phase_outputs` (validation_consolidated or verification_consolidated).

## Error Handling

- If one agent output is missing, proceed with available feedback and mark as partial.
- If both outputs are missing, escalate to human review.

## Related Skills

- `/validate-plan` - Uses this for Phase 2 conflicts
- `/verify-code` - Uses this for Phase 4 conflicts
- `/call-cursor` - Cursor agent details
- `/call-gemini` - Gemini agent details
