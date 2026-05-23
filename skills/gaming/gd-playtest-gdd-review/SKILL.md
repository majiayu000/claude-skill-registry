---
name: gd-playtest-gdd-review
description: GDD review and research during playtest phase. Use during playtest phase BEFORE sending playtest_session_report to PM, after completing gameplay testing, after reviewing retrospective pain points, or before finalizing the playtest report.
---

# Playtest GDD Review

## The 3-Phase GDD Review Process

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PLAYTEST GDD REVIEW WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1: RETROSPECTIVE ANALYSIS                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Read retrospective.txt for pain points                            │   │
│  │ 2. Identify worker struggles: unclear specs, missing references      │   │
│  │ 3. Note repeated questions about GDD content                         │   │
│  │ 4. Catalog implementation deviations from design                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Phase 2: GAME STATE REVIEW                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Review current implementation via Playwright MCP                   │   │
│  │ 2. Compare actual gameplay vs GDD specifications                      │   │
│  │ 3. Check docs/design/gdd/ for outdated sections                       │   │
│  │ 4. Verify acceptance criteria alignment                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Phase 3: GAP ANALYSIS & UPDATE PROPOSAL                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Identify GDD sections needing updates                              │   │
│  │ 2. Catalog missing specifications                                     │   │
│  │ 3. Identify skills workers need but don't have                        │   │
│  │ 4. Propose task priority adjustments                                  │   │
│  │ 5. Update GDD files if changes are clear                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│                         Include in playtest_report                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Phase 1: Retrospective Analysis

### Step 1: Read Retrospective

```bash
# Read the most recent retrospective using Read tool
Read(".claude/session/retrospective.txt")

# Extract pain points from each worker section
# Look for sections: Developer Perspective, Tech Artist Perspective, QA Perspective
```

### Step 2: Identify GDD-Related Pain Points

Look for patterns indicating GDD issues:

| Pain Point Pattern             | GDD Issue Type          | Action                   |
| ------------------------------ | ----------------------- | ------------------------ |
| "Unclear what X means"         | Ambiguous specification | Clarify in GDD           |
| "Not specified how Y works"    | Missing specification   | Add to GDD               |
| "Had to guess Z"               | Incomplete design       | Complete design          |
| "Reference images unclear"     | Visual reference gap    | Add/update references    |
| "Conflicting specs in X and Y" | Contradiction           | Resolve conflict         |
| "No examples for pattern"      | Missing examples        | Add code/visual examples |

### Step 3: Catalog Questions from Workers

**Use native Read/Write tools to check for messages:**

```bash
# Use Glob to find messages in your inbox
Glob(".claude/session/messages/gamedesigner/msg-*.json")

# Read each message file using Read tool
# Look for type "question" or "design_question"
# Track patterns of what workers are asking about
# Log question topics for GDD update analysis
```

**Question patterns to catalog:**

| Pattern           | What it means              | Action                |
| ----------------- | -------------------------- | --------------------- |
| design_question   | Asking about design intent | Clarify in GDD        |
| reference_request | Needs visual reference     | Add/update references |
| clarification     | Unclear specification      | Add details to GDD    |

## Phase 2: Game State Review

### Step 1: Compare Implementation vs GDD

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION vs GDD CHECKLIST                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  GDD Module                     │ Implementation │ Gap?                     │
│  ───────────────────────────────┼────────────────┼─────────────────────────│
│  2_paint_friction_system.md     │ [Review src/]  │ Values differ?           │
│  3_movement_system.md           │ [Review src/]  │ Controls different?      │
│  4_territory_control.md         │ [Review src/]  │ Grid size mismatch?      │
│  5_weapon_system.md             │ [Review src/]  │ Weapon behavior off?     │
│  8_ui_hud_system.md             │ [Review src/]  │ HUD elements missing?    │
│  13_multiplayer.md              │ [Review src/]  │ Network pattern wrong?   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step 2: Check GDD Currency

For each GDD module, verify:

```markdown
## GDD Currency Checklist

### [Module Name].md

- [ ] Version number updated
- [ ] Last updated date current
- [ ] Acceptance criteria match PRD
- [ ] Technical specs accurate
- [ ] Reference images still relevant
- [ ] No TODO comments unresolved
- [ ] No conflicting specifications
```

### Step 3: Vision MCP Analysis

Use Vision MCP to compare gameplay with GDD visual specifications:

```javascript
// Analyze gameplay screenshot against GDD visual specs
const gddVisualCheck = await visionAnalyze(screenshot, {
  prompt: `Compare this gameplay screenshot against GDD visual requirements:
  - Character: [GDD spec]
  - UI: [GDD spec]
  - Environment: [GDD spec]

  Report any deviations with severity (low/medium/high).`,
});
```

## Phase 3: Gap Analysis & Update Proposal

### Step 1: Identify GDD Updates Needed

```markdown
## GDD Update Proposals

| Task ID      | GDD Module                 | Issue                       | Proposed Update           | Priority |
| ------------ | -------------------------- | --------------------------- | ------------------------- | -------- |
| P1-001       | 2_paint_friction_system.md | Friction values unclear     | Add specific values table | HIGH     |
| P1-002       | 4_territory_control.md     | Grid cell size ambiguous    | Specify 2mx2m explicitly  | HIGH     |
| feat-tps-001 | TPS_CAMERA_SPEC.md         | No shoulder offset examples | Add code examples         | CRITICAL |
```

### Step 2: Identify Missing Skills

Analyze worker struggles to identify skill gaps:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SKILL GAP ANALYSIS                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Worker Struggle                      │ Missing Skill                   │
│  ─────────────────────────────────────┼───────────────────────────────────│
│  "Don't know X pattern"              │ dev-patterns-[X]                 │
│  "Unsure how to integrate Y"         │ dev-integration-[Y]              │
│  "Visual reference unclear for Z"    │ gd-visual-reference-[Z]          │
│  "Performance issues with W"         │ dev-performance-[W]              │
│  "Shader doesn't match spec V"       │ ta-shader-[V]-examples            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step 3: Propose Task Priority Adjustments

Based on playtest findings, recommend priority changes:

```json
{
  "priorityRecommendations": [
    {
      "taskId": "P1-00X",
      "currentTier": "TIER_3",
      "recommendedTier": "TIER_1",
      "reason": "Blocks multiple user-facing features, discovered during playtest"
    },
    {
      "taskId": "iter6-0XX",
      "currentTier": "TIER_2",
      "recommendedTier": "TIER_4",
      "reason": "Lower impact than expected, can defer"
    }
  ]
}
```

## GDD Update Process

### When to Update GDD Immediately

Update GDD files directly when:

- Specification is clearly wrong (e.g., typo in values)
- Acceptance criteria are ambiguous
- Missing examples that would prevent work
- Visual references are outdated

### When to Propose Updates

Propose updates (include in report) when:

- Design changes need team discussion
- New features affect multiple GDD sections
- Priority changes affect planning
- Scope changes need PM approval

### GDD Update Template

```markdown
## GDD Update: [Module Name]

**Date:** YYYY-MM-DD
**Updated By:** Game Designer
**Trigger:** Playtest [taskId] - Retrospective analysis

### Changes Made

| Section   | Before        | After         | Reason        |
| --------- | ------------- | ------------- | ------------- |
| [Section] | [Old content] | [New content] | [Why changed] |

### Impact on Tasks

| Task ID  | Impact        | Action Required         |
| -------- | ------------- | ----------------------- |
| [taskId] | [Description] | [What worker should do] |

### Version Update

- Previous: X.Y.Z
- New: X.Y.Z+1
```

## Playtest Report Additions

Include these sections in `playtest_session_report`:

```json
{
  "taskId": "{taskId}",
  "playtestResult": {
    "overall": "PASS|FAIL|PARTIAL",
    "criteriaTested": [...],
    "issuesFound": [...]
  },
  "gddReview": {
    "modulesReviewed": ["2_paint_friction_system.md", "4_territory_control.md"],
    "updatesNeeded": [
      {
        "task": "P1-001",
        "gddModule": "2_paint_friction_system.md",
        "issue": "Friction values ambiguous",
        "proposedChange": "Add explicit values table",
        "priority": "HIGH"
      }
    ],
    "gddUpdatesMade": [
      {
        "file": "docs/design/gdd/4_territory_control.md",
        "change": "Clarified grid cell size as 2mx2m",
        "version": "1.2.0"
      }
    ]
  },
  "skillGaps": [
    {
      "agent": "developer",
      "missingSkill": "dev-patterns-friction-transition",
      "description": "Workers struggled with smooth surface transitions",
      "proposedSkill": "Create skill for 100ms friction blend patterns"
    }
  ],
  "priorityRecommendations": [
    {
      "taskId": "P1-008",
      "currentTier": "TIER_3",
      "recommendedTier": "TIER_2",
      "reason": "Critical for UX, discovered friction testing difficult without it"
    }
  ]
}
```

## Sub-Agent Coordination

### Use skill-researcher for Skill Proposals

```
If skill gaps identified:
1. Document gap clearly
2. Use Task with skill-researcher sub-agent
3. Research existing similar skills
4. Propose new skill structure
5. Include in playtest report
```

### Update GDD Files

```
If clear GDD updates needed:
1. Read the GDD module
2. Edit with clarifications
3. Update version number
4. Document change in decision_log.md
5. List updated files in playtest report
```

## Quality Gates

Before sending playtest report:

- [ ] Retrospective pain points reviewed
- [ ] Worker questions analyzed
- [ ] Game state compared to GDD
- [ ] GDD modules checked for currency
- [ ] Skill gaps documented
- [ ] GDD updates made (if clear) or proposed
- [ ] Priority recommendations justified
- [ ] All findings included in playtest report

## Messages You Send

After GDD review, use Write tool to send the playtest report:

```javascript
// Use Write tool to send message to PM's inbox:
Write(".claude/session/messages/pm/msg-playtest-{timestamp}.json", JSON.stringify({
  "id": "msg-playtest-report-{timestamp}",
  "from": "gamedesigner",
  "to": "pm",
  "type": "playtest_session_report",
  "payload": {
    "taskId": "{taskId}",
    "playtestResult": {
      "overall": "PASS|FAIL|PARTIAL",
      "criteriaTested": [...],
      "issuesFound": [...]
    },
    "gddReview": {
      "modulesReviewed": ["2_paint_friction_system.md", "4_territory_control.md"],
      "updatesNeeded": [...],
      "gddUpdatesMade": [...]
    },
    "skillGaps": [...],
    "priorityRecommendations": [...]
  },
  "timestamp": "{ISO-8601-UTC}"
}))
```
