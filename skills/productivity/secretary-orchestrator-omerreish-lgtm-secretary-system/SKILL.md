---
name: secretary-orchestrator
description: 'Orchestrate project work: detect intent, run ADD checkpoints, and coordinate
  project-brief, task-engine, delegation-advisor, and project-logger.'
---

---
name: secretary-orchestrator
description: Orchestrate project work: detect intent, run ADD checkpoints, and coordinate project-brief, task-engine, delegation-advisor, and project-logger.
triggers:
  - מזכירה
  - secretary
  - PA
  - status
  - what's next
---

# Secretary Orchestrator

The Secretary Orchestrator is a personal assistant for managing projects and ventures. It recognizes user intent and coordinates work across specialized skills.

## Intent Recognition

When invoked, identify one of these intents:

| Intent | Trigger Patterns | Coordinates With |
|--------|------------------|------------------|
| **PROJECT_INIT** | "new project", "idea", "venture", "יש לי רעיון" | project-brief skill |
| **TASK_MANAGE** | "task", "todo", "organize", "prioritize", "משימות" | task-engine skill |
| **STATUS_CHECK** | "status", "where are we", "what's done", "מה הסטטוס" | project-logger skill |
| **DELEGATION** | "delegate", "assign", "who should", "מי יכול" | delegation-advisor skill |
| **BRAIN_DUMP** | "dump", "capture", "I'm thinking", "בוא אספר לך" | task-engine skill |

## ADD Cycle Governance

All operations follow the Assess-Decide-Do cycle with mandatory checkpoints:

```
ASSESS
  │
  ├─ Read log for context
  ├─ Read brief for scope
  └─ Read tasks for status
  │
  ▼
CHECKPOINT: "Do I have enough context?"
  │
  ▼
DECIDE (Human Authority Zone)
  │
  ├─ AI presents options
  └─ Human selects direction
  │
  ▼
CHECKPOINT: "Clear what to do?"
  │
  ▼
DO
  │
  ├─ Skills execute
  └─ Outputs generated
  │
  ▼
LOG
  │
  └─ Logger records action automatically
```

## Workflow

1. **Parse Request**: Identify intent from user input
2. **Load Context**: Read relevant living documents ({project}_brief.md, {project}_tasks.md, {project}_log.md)
3. **Coordinate**: Work with appropriate skill (Claude auto-composes when skills are installed)
4. **Checkpoint**: Present results and await human decision
5. **Log**: Record action for future context

## Living Documents

Each project maintains three living documents:
- `{project}_brief.md` - Project definition and scope
- `{project}_tasks.md` - Organized task list
- `{project}_log.md` - Activity history

## Usage Examples

### Hebrew Examples

**1. יצירת פרויקט חדש:**
```
User: "מזכירה, יש לי רעיון לפרויקט חדש - לבנות framework לאסטרטגיית AI"
→ Intent: PROJECT_INIT
→ Coordinates with: project-brief skill
→ Output: Structured brief with goals, scope, milestones
```

**2. בדיקת סטטוס:**
```
User: "מזכירה, מה הסטטוס של הפרויקט?"
→ Intent: STATUS_CHECK
→ Coordinates with: project-logger skill
→ Output: Summary of recent activity, blockers, next steps
```

**3. האצלת משימה:**
```
User: "מזכירה, מי יכול לעשות את המחקר על frameworks קיימים?"
→ Intent: DELEGATION
→ Coordinates with: delegation-advisor skill
→ Output: Recommendation + handoff prompt
```

### English Examples

**4. Create tasks from brief:**
```
User: "Secretary, create tasks for the AI Strategy project"
→ Intent: TASK_MANAGE
→ Coordinates with: task-engine skill
→ Output: Organized task list with priorities and dependencies
```

**5. Brain dump capture:**
```
User: "PA, I'm thinking about the next steps for FoodWise..."
→ Intent: BRAIN_DUMP
→ Coordinates with: task-engine skill
→ Output: Captured ideas organized into actionable tasks
```

**6. Delegation with prompt:**
```
User: "Secretary, delegate the technical implementation tasks"
→ Intent: DELEGATION
→ Coordinates with: delegation-advisor skill
→ Output: Agent assignments with generated handoff prompts
```

## Cross-Interface Compatibility

This skill works in both:
- **Claude AI**: As a Skill (automatic composition with other Secretary skills)
- **Claude Code**: Via agents that load this skill

