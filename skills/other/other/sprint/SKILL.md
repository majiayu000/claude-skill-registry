---
name: sprint
description: Creates or advances sprints in prd.json. Use when starting new work cycles or closing completed sprints.
triggers:
  - sprint
allowed-tools: Read, Write, Edit, TaskCreate, TaskUpdate, TaskList
model: opus
user-invocable: true
argument-hint: "[new|advance|close]"
---

# Sprint

Create a new sprint or advance to the next one.

## Usage

- `sprint [description]` - Create new sprint from feature description
- `sprint next` - Advance to next sprint from roadmap

## Creating from Description

1. Parse $ARGUMENTS as feature description
2. Generate epic prefix from description
3. Create/update prd.json with new sprint
4. Generate 10-20 stories via TaskCreate with full metadata (see quality skill for schema):
   ```
   TaskCreate({
     subject: "[verb] [specific deliverable]",
     description: "## What\n[Exactly what to build]\n\n## Acceptance Criteria\n- [ ] [Testable outcome]\n- [ ] Build passes\n- [ ] No type errors\n\n## Files\n- `src/path/file.ts` - [what to change]",
     activeForm: "[Building|Adding] [short desc]",
     metadata: {
       sid: "[PREFIX]-[NNN]",
       sprint: currentSprint,
       epic: "[epic name]",
       priority: [1-3],
       category: "[auth|ui|perf|security|qa|infra]",
       type: "feature",
       passes: null,
       verified: null
     }
   })
   ```
   - Include file paths, patterns to follow
   - Set dependencies between stories
5. Report sprint summary

## Advancing (sprint next)

1. Read prd.json
2. Mark current sprint as "done"
3. Find next unscheduled roadmap epic(s)
4. Create new sprint with stories from those epics
5. Update prd.json

## Auto-Archive Check

Before creating a new sprint, check if prd.json needs archiving:

```bash
# Count completed sprints
node -e "try{const p=require('./prd.json');const sprints=p.sprints||[];const done=sprints.filter(s=>s.passes===true||s.stories?.every(st=>st.passes===true||st.passes==='deferred'));console.log('completed:',done.length,'total:',sprints.length,'lines:',JSON.stringify(p).split(',').length)}catch{}"
```

| Condition | Action |
|-----------|--------|
| 3+ completed sprints in prd.json | Suggest `archive` before creating new sprint |
| prd.json > 500 lines | Warn: "prd.json is large, consider `archive` first" |

Large prd.json wastes tokens on every request. Run the check.

## Rules
- HARD CAP: 20 stories per sprint
- Stories must be detailed enough to implement without guessing
- Every story must be testable
- If user asks to "expand", explain roadmap and offer `sprint next`
