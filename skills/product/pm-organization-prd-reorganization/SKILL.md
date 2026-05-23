---
name: pm-organization-prd-reorganization
description: Extract and reorganize PRD tasks from GDD updates and retrospective findings
category: organization
---

# PRD Reorganization

The PM must translate Game Design Document updates and retrospective findings into actionable PRD tasks. This skill defines the systematic process for PRD reorganization.

## When to Use

Use this skill during the `prd_analysis` phase, which occurs after the retrospective synthesis but before skill research:

```
passed → in_retrospective → prd_analysis → skill_research → completed
```

## Trigger Conditions

PRD reorganization is triggered by:

1. **GDD Update** - Game Designer sends `gdd_ready` or `gdd_update` message
2. **Retrospective Findings** - Implementation gaps or deviations discovered
3. **Technical Debt** - Debt items identified that need dedicated tasks
4. **Process Improvements** - Workflow changes requiring new tasks

## PRD Backlog Architecture (v3.1.0+)

Since v3.1.0, tasks are split between two files:

| File | Contains | Size |
|------|----------|------|
| `prd.json` | Top 5 active queue | ~5 tasks |
| `prd_backlog.json` | Remaining backlog | ~70 tasks |

**When reorganizing:**
- Read both files for complete PRD picture
- High-priority tasks (TIER_0, TIER_1) go to `prd.json` items array
- Lower priority tasks go to `prd_backlog.json` backlogItems array
- Maintain max 5 tasks in `prd.json.items` (move lower priority to backlog if needed)

## GDD-to-PRD Task Extraction

### Step 1: Read the GDD

```powershell
# Always read the latest GDD
READ docs/design/gdd.md

# Note the gddVersion for tracking
```

### Step 2: Parse GDD Sections

For each GDD section, extract implementation requirements:

```markdown
| GDD Section | What to Extract                          | Task Category           |
|-------------|------------------------------------------|-------------------------|
| Gameplay    | Core mechanics, player actions           | architectural           |
| UI/UX       | Interface elements, interactions         | feature                 |
| Multiplayer | Networking, synchronization              | architectural           |
| Audio       | Sound effects, music, spatial audio      | feature                 |
| Visuals     | Shaders, effects, post-processing        | feature                 |
| Performance | FPS targets, optimization requirements   | technical_debt          |
```

### Step 3: Check Existing PRD Coverage

For each extracted requirement, check if PRD already covers it:

```powershell
# Load both PRD files (v3.1.0+)
READ prd.json
READ prd.backlogFile (or "prd_backlog.json")

# Combine items from both files
$allItems = @($prd.items) + @($backlog.backlogItems)

# For each GDD requirement:
1. Search for related existing task by keyword in $allItems
2. Check if existing task's acceptanceCriteria covers requirement
3. Mark requirement as: COVERED / PARTIALLY_COVERED / NOT_COVERED
```

### Step 4: Create Missing Tasks

For each NOT_COVERED or PARTIALLY_COVERED requirement, create a new task:

```json
{
  "id": "design-001",
  "title": "Implement core gameplay loop from GDD",
  "description": "Implement the core gameplay loop as specified in GDD section 2, including player movement, jumping, and physics interaction.",
  "category": "architectural",
  "priority": "high",
  "status": "pending",
  "passes": false,
  "agent": "developer",
  "dependencies": [],
  "gddReference": "docs/design/gdd.md#2",
  "gddVersion": "1.2.0",
  "acceptanceCriteria": [
    "Player can move with WASD keys",
    "Player can jump with Space key",
    "Gravity physics matches GDD specification (-9.8 m/s²)",
    "Collision detection works with terrain",
    "Frame rate maintains 60fps during gameplay"
  ]
}
```

**Task ID Pattern**: Use `design-NNN` format for GDD-derived tasks to distinguish from user-created tasks.

### Step 5: Update Task Priorities

Re-evaluate priorities based on GDD vision:

```markdown
| Priority | Criteria                                      |
|----------|-----------------------------------------------|
| high     | Core gameplay, blockers, architectural        |
| medium   | Features, polish, UI                          |
| low      | Nice-to-have, optimizations, extras           |
```

## Retrospective-to-PRD Task Creation

### Step 1: Analyze Retrospective Findings

Extract actionable items from retrospective.txt:

```markdown
| Finding Type              | Action Required                          |
|---------------------------|------------------------------------------|
| Implementation gap        | Create task to complete missing work     |
| Design deviation          | Create task to align with GDD            |
| Technical debt identified | Create task with category: technical_debt |
| Process issue             | Update AGENT.md, no PRD task needed       |
| Bug found                 | Create task with category: bug_fix       |
```

### Step 2: Create Tasks for Findings

For each actionable finding, create a PRD task:

```json
{
  "id": "retro-001",
  "title": "Fix physics integration issues identified in retrospective",
  "description": "Address physics inconsistencies reported by Developer during retrospective. Rapier integration not working as expected.",
  "category": "bug_fix",
  "priority": "high",
  "status": "pending",
  "passes": false,
  "agent": "developer",
  "dependencies": [],
  "retrospectiveReference": ".claude/session/retrospective.txt#L15-L25",
  "acceptanceCriteria": [
    "Physics bodies spawn at correct positions",
    "Collision events fire consistently",
    "No physics-related console errors"
  ]
}
```

**Task ID Pattern**: Use `retro-NNN` format for retrospective-derived tasks.

### Step 3: Reorganize Existing Tasks

Based on retrospective findings, you may need to:

```powershell
# Update existing tasks
1. Mark validated tasks: status = "completed"
2. Update blocked tasks: add dependencies
3. Reprioritize based on new information
4. Combine related tasks for efficiency
5. Split oversized tasks into smaller chunks
```

## PRD Reorganization Workflow

```powershell
# During prd_analysis phase:

1. READ docs/design/gdd.md (if GDD updated)
2. READ .claude/session/retrospective.txt
3. READ prd.json
4. READ prd.backlogFile (or "prd_backlog.json")

5. EXTRACT requirements from GDD
6. EXTRACT action items from retrospective

7. FOR each requirement/action item:
   a. Check if covered by existing PRD task (check both files)
   b. If NOT covered: CREATE new task
   c. If partially covered: UPDATE existing task

8. REORGANIZE task priorities and dependencies

9. DETERMINE task placement:
   a. TIER_0_BLOCKER, TIER_1_FOUNDATION → prd.json.items
   b. TIER_2_ECONOMY and below → prd_backlog.json.backlogItems
   c. If prd.json.items.length > 5, move lowest priority to backlog

10. WRITE both updated files:
    WRITE prd.json
    WRITE prd_backlog.json

11. COMMIT with message:
    "Retrospective [N]: Reorganized PRD with [X] new tasks from GDD/retrospective"

12. SEND prd_reorganized message to workers:
    {
      "type": "prd_reorganized",
      "from": "pm",
      "timestamp": "<ISO timestamp>",
      "summary": {
        "newTasks": 3,
        "updatedTasks": 2,
        "gddVersion": "1.2.0"
      }
    }
```

## Message Types

### prd_reorganized

Sent after PRD reorganization to notify workers of changes:

```json
{
  "type": "prd_reorganized",
  "from": "pm",
  "timestamp": "2025-01-21T10:30:00Z",
  "summary": {
    "newTasks": 3,
    "updatedTasks": 2,
    "gddVersion": "1.2.0",
    "newTaskIds": ["design-001", "design-002", "retro-001"]
  }
}
```

## PRD Reorganization Checklist

Before completing `prd_analysis` phase:

- [ ] All GDD requirements have corresponding PRD tasks
- [ ] All retrospective findings have been addressed
- [ ] Task dependencies are accurate and acyclic (checked across both files)
- [ ] Priorities reflect current project priorities
- [ ] No duplicate tasks exist (check across both files)
- [ ] All new tasks have acceptance criteria
- [ ] prd.json is valid JSON
- [ ] prd_backlog.json is valid JSON
- [ ] Task placement correct: TIER_0/1 in prd.json, others in backlog
- [ ] prd.json.items.length <= 5
- [ ] Changes are committed to git
- [ ] Workers notified via prd_reorganized message

## Task Creation Guidelines

### Task Decomposition

When creating tasks from GDD or retrospectives:

```markdown
# DO: Break down large features
✓ "Implement player movement system" →
  - design-001: "Implement WASD movement"
  - design-002: "Implement jump mechanics"
  - design-003: "Implement sprint mechanics"

# DON'T: Create monolithic tasks
✗ "Implement all player movement and combat"
```

### Acceptance Criteria

Each task must have specific, testable acceptance criteria:

```markdown
# GOOD: Specific and testable
✓ "Player velocity matches input direction within 0.1s"
✓ "Jump height reaches 2 meters when space pressed"

# BAD: Vague and untestable
✗ "Movement feels good"
✗ "Make jumping work better"
```

### Agent Assignment

Assign tasks to the appropriate agent:

```markdown
| Task Type                    | Agent         |
|------------------------------|---------------|
| Gameplay implementation      | developer     |
| Tests and validation         | qa            |
| Design specs, GDD updates    | gamedesigner  |
| Architecture, coordination   | pm            |
```

## Reference

- [pm-retrospective-facilitation](../pm-retrospective-facilitation/SKILL.md) — Provides findings for task creation
- [pm-organization-task-selection](../pm-organization-task-selection/SKILL.md) — Assigns newly created tasks
- [pm-organization-scale-adaptive](../pm-organization-scale-adaptive/SKILL.md) — Adjusts approach based on task count
- [pm-improvement-self-improvement](../pm-improvement-self-improvement/SKILL.md) — PM improves this skill

---

## Playtest-Driven Task Creation (Added: ui-001 Playtest)

**Learned from ui-001:** Playtest may reveal visual inadequacy even when functional requirements pass. PM must create follow-up tasks for visual polish.

### CONDITIONAL_PASS Handling

When Game Designer issues CONDITIONAL_PASS:

1. **Assess functional status** - If all mechanics work, mark functional requirements as PASS
2. **Identify visual gaps** - Document specific visual deficiencies
3. **Create redesign task** - New task for visual design system implementation
4. **Set dependency** - Original task blocked on redesign completion
5. **Update PRD** - Move redesign to TIER_0_BLOCKER if UI is primary feature

### Visual Redesign Task Template

```json
{
  "id": "{original-id}-002",
  "title": "Professional UI/UX Redesign - {Feature Name}",
  "description": "Complete UI/UX redesign based on playtest findings. Current implementation is functionally complete but visually inadequate. Implement a professional design system inspired by {reference titles}. Full specification in {spec-file}.",
  "category": "visual",
  "priority": "high",
  "tier": "TIER_0_BLOCKER",
  "status": "pending",
  "passes": false,
  "agent": "techartist",
  "dependencies": [],
  "gddReference": "{spec-file}",
  "gddVersion": "1.0",
  "specificationFile": "{spec-file}",
  "acceptanceCriteria": [
    "All UI screens enforce 16:9 aspect ratio",
    "UI scales proportionally at any window size",
    "Design system tokens implemented",
    "{Specific visual requirements from spec}"
  ]
}
```

### Common Visual Gaps to Address

| Gap Found                     | Task Category        | Agent         |
| ------------------------------ | --------------------- | ------------- |
| No aspect ratio enforcement   | visual                | techartist    |
| Basic styling (Tailwind only) | visual                | techartist    |
| Generic fonts                 | visual                | techartist    |
| Default easing curves         | visual                | techartist    |
| No hover/active feedback      | visual                | techartist    |
| Inconsistent spacing          | visual                | techartist    |
| Poor contrast/accessibility   | visual                | techartist    |

### Specification Document Creation

When creating visual redesign tasks:

1. **Game Designer** creates detailed specification document
2. **Save to** `docs/design/{feature-name}-specification.md`
3. **Include**:
   - Aspect ratio and scaling requirements
   - Color palette with hex values
   - Typography (font families, sizes, weights)
   - Button/component designs
   - Animation timing and easing curves
   - Screenshot references where applicable

**Sources:**
- **Learned from ui-001 playtest (2026-01-28)**
- Specification document: `docs/design/ui-redesign-specification.md`
