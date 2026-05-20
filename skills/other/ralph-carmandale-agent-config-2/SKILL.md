---
name: ralph
description: Create and run Ralph loops for structured AI-driven development. Triggered by "create a ralph loop for X" or "ralph plan for X". Uses interview to clarify requirements, expert review via Ralph wrappers, creates phased task plans, and executes in YOLO mode.
---

# Ralph Loop Skill

Create bulletproof development plans that execute reliably in YOLO mode.

## Trigger Phrases

- "create a ralph loop for..."
- "ralph plan for..."
- "make a ralph loop and start with an interview"
- "yolo this feature..."

## The Bulletproof Process

```
1. RESEARCH      - Understand the codebase
       ↓
2. INTERVIEW     - Gather requirements from user
       ↓
3. DESIGN        - Create architecture document
       ↓
4. EXPERT REVIEW - ralph review design (wrapper)
       ↓
5. ORACLE        - (if complex) Deep architecture review
       ↓
6. CREATE PLAN   - Write atomic, complete tasks
       ↓
7. PLAN REVIEW   - ralph review plan (wrapper)
       ↓
8. FINALIZE      - User approval
       ↓
9. EXECUTE       - ralph yolo
       ↓
10. POST-REVIEW  - ralph review post (wrapper)
```

---

## Phase 1: RESEARCH (Required)

**Before creating ANY interview, understand the codebase.**

Start with a canonical template:
```bash
ralph scaffold research
```

### What to Research

1. **Find existing patterns** - How does similar functionality work?
2. **Identify files to modify** - What will change?
3. **Understand the architecture** - Where does this fit?
4. **Note naming conventions** - Match existing style

### Research Commands

```bash
# Find relevant files
rg -l "keyword" --type swift
find . -name "*.swift" -path "*/Views/*" | head -20

# Understand existing patterns  
rg -A5 "struct.*View.*:" --type swift | head -50

# Check file structure
tree -L 3 path/to/relevant/code/

# Read key files
cat path/to/existing/similar/feature.swift | head -100
```

### Research Output

Document findings:
```markdown
## Research Findings

**Existing patterns:**
- Views are in Features/*/Views/
- State is in Features/*/State/
- Uses @Observable pattern

**Files that will change:**
- MainSplitView.swift (add new component)
- SomeState.swift (add new property)

**Files to create:**
- NewFeatureView.swift
- NewFeatureState.swift

**Naming conventions:**
- Views: SomethingView.swift
- State: SomethingState.swift
```

Complete Phase 1 by running:
```bash
ralph advance phase1
```

---

## Phase 2: INTERVIEW (Required)

**Use the interview tool to gather requirements. Never guess.**

Start with a canonical template:
```bash
ralph scaffold interview
```

### Interview Question Categories

Every interview MUST cover:

1. **Scope** - What exactly are we building?
2. **Location** - Where does it appear/integrate?
3. **Behavior** - How does it work?
4. **Edge Cases** - What could go wrong?
5. **Acceptance** - How do we know it's done?

### Interview Template

```json
{
  "title": "Ralph Plan: [Feature Name]",
  "description": "I've researched the codebase. Help me understand the requirements.\n\n**What I found:**\n[Brief research summary]",
  "questions": [
    {
      "id": "scope",
      "type": "single",
      "question": "What exactly should this feature do?",
      "options": ["Option A (describe)", "Option B (describe)", "Both", "Something else (explain below)"],
      "context": "Based on my research, [context]"
    },
    {
      "id": "scope_details",
      "type": "text",
      "question": "Any additional scope details?",
      "required": false
    },
    {
      "id": "location",
      "type": "single",
      "question": "Where should [feature] appear?",
      "options": ["Location A", "Location B", "New location"],
      "context": "Currently, similar features are in [location]"
    },
    {
      "id": "behavior_primary",
      "type": "single",
      "question": "When [trigger], what should happen?",
      "options": ["Behavior A", "Behavior B", "Configurable"]
    },
    {
      "id": "behavior_secondary",
      "type": "single",
      "question": "[Follow-up behavior question]?",
      "options": ["Option A", "Option B", "Option C"]
    },
    {
      "id": "edge_cases",
      "type": "multi",
      "question": "Which edge cases should I handle?",
      "options": ["Error state", "Empty state", "Loading state", "Offline mode", "Other (specify)"]
    },
    {
      "id": "edge_case_details",
      "type": "text",
      "question": "Any specific edge case handling?",
      "required": false
    },
    {
      "id": "acceptance",
      "type": "text",
      "question": "How will you verify this works correctly?",
      "context": "Describe what you'll test or look for"
    },
    {
      "id": "constraints",
      "type": "text",
      "question": "Any constraints or requirements I should know?",
      "required": false
    }
  ]
}
```

Complete Phase 2 by running:
```bash
ralph advance phase2
```

---

## Phase 3: DESIGN (Required)

**After interview, design the solution before writing tasks.**

Start with a canonical template:
```bash
ralph scaffold design
```

### Design Document Template

```markdown
## Design: [Feature Name]

### Interview Summary
- Scope: [answer]
- Location: [answer]  
- Behavior: [answer]
- Edge cases: [answer]
- Acceptance: [answer]

### Architecture

**New files to create:**
| File | Purpose |
|------|---------|
| NewView.swift | Main UI component |
| NewState.swift | State management |

**Files to modify:**
| File | Changes |
|------|---------|
| MainSplitView.swift | Add NewView to layout |
| AppState.swift | Add newState property |

**Integration points:**
- NewView will be added to MainSplitView in the detail area
- NewState will be owned by AppState
- NewView observes NewState via @Environment

### UI Mockup (if applicable)
```
┌─────────────────────────────────────┐
│  [Existing UI]                      │
├─────────────────────────────────────┤
│  [New Feature Here]                 │
│  - Element A                        │
│  - Element B                        │
└─────────────────────────────────────┘
```

### Verification Checklist
- [ ] Feature appears in correct location
- [ ] Primary behavior works
- [ ] Edge cases handled
- [ ] User acceptance criteria met
```

Complete Phase 3 by running:
```bash
ralph advance phase3
```

---

## Phase 4: EXPERT REVIEW (Required)

**Use Ralph wrapper commands (never call rp-cli directly).**

### Run Design Review

```bash
ralph review design
```

Ralph selects context automatically from `design.md`.

Optional one-shot finalize:
```bash
ralph review design --final
```

Do not summarize review results until `ralph review design --final` succeeds or `ralph show-proof phase4` renders the verified output.

### Process Review Feedback (re-review loop)

1. Run review on the current draft
2. Apply feedback to `design.md`
3. **Run `ralph review design` again** after edits
4. Complete Phase 4 with:
   ```bash
   ralph advance phase4
   ```

If major issues are found, return to Phase 3.

---

## Phase 5: ORACLE (Required Unless Waived)

**Phase 5 is required unless a TTY-confirmed waiver is granted.** Use these guidelines to decide whether a waiver is appropriate:

### When Oracle Is Definitely Required

- Multiple subsystems involved
- New architectural patterns needed
- Cross-cutting concerns (auth, sync, caching)
- Integration with external services
- Performance-critical paths

If none apply and you want to skip, request a waiver:
```bash
ralph waive phase5 --reason "..."
```

### Run Oracle Review

```bash
ralph oracle
```

Ralph bundles the README/spec/implementation and runs APR in robot mode. Do not call APR/Oracle directly.

Optional one-shot finalize:
```bash
ralph oracle --final
```

Do not summarize Oracle results until `ralph oracle --final` succeeds or `ralph show-proof phase5` renders the verified output.

### Process Oracle Response

- Update design with Oracle recommendations
- Document key decisions and rationale
- If significant changes, re-run Phase 4 review

**Re-review loop:** If you change `design.md` after Oracle output, you must re-run `ralph oracle` before advancing. For a one-shot finalize:

```bash
ralph oracle --final
```

Complete Phase 5 by running:
```bash
ralph advance phase5
```

---

## Phase 6: CREATE PLAN (Critical)

**Write tasks that are atomic, complete, and verifiable.**

Start with a canonical template:
```bash
ralph scaffold plan
```

### Task Anatomy

Every task MUST have:

1. **WHAT** - The specific change to make
2. **WHERE** - The exact file(s) to modify
3. **HOW** - Brief implementation approach (if not obvious)
4. **VERIFY** - How to confirm it worked

### Task Sizing (Critical)

**All tasks should be similar size** - the LLM struggles with inconsistent sizing.

| Task Size | Time Estimate | Example |
|-----------|---------------|---------|
| Too small | < 2 min | "Add import statement" |
| ✅ Right | 5-15 min | "Create SyncConsolePanel view with basic layout" |
| Too large | > 30 min | "Implement entire sync feature with all UI" |

**Why this matters:** Large tasks get "swallowed up" - the LLM runs out of context window before finishing, producing incomplete or buggy code. If a task would take a human > 30 minutes, split it.

### Task Writing Rules

#### Rule 1: Atomic = One Concern

❌ BAD: "Add sync panel with drag handle and animations"
✅ GOOD: Three separate tasks

#### Rule 2: Consistent Size

❌ BAD: Mix of tiny ("add import") and huge ("implement feature") tasks
✅ GOOD: All tasks take roughly 5-15 minutes of LLM work

#### Rule 3: Complete = Create + Integrate

❌ BAD: "Create SyncConsolePanel view"
✅ GOOD: "Create SyncConsolePanel view in SharedUI/Common/ AND replace SyncProgressView with it in MainSplitView.swift"

#### Rule 4: Specific Files Named

❌ BAD: "Add the button to the toolbar"
✅ GOOD: "Add refresh button to toolbar in MediaOrganizationView.swift toolbarContent"

#### Rule 5: Verification Included

❌ BAD: "Add drag handle"
✅ GOOD: "Add drag handle to panel. VERIFY: Dragging handle resizes panel height"

### Plan Structure

```markdown
# Plan: [Feature Name]

## Context
[What we're building and why]

## Interview Responses ([date])
- Scope: [answer]
- Location: [answer]
- Behavior: [answer]

## Design Review Notes
[Key feedback from ralph review design]
[Oracle recommendations if applicable]

## Tasks

### Phase 1: Foundation
- [ ] 1.1 [Task with WHAT, WHERE, VERIFY]
- [ ] 1.2 [Task with WHAT, WHERE, VERIFY]

### Phase 2: Core Implementation  
- [ ] 2.1 [Task with WHAT, WHERE, VERIFY]
- [ ] 2.2 [Task with WHAT, WHERE, VERIFY]

### Phase 3: Integration
- [ ] 3.1 [Task with WHAT, WHERE, VERIFY]

### Phase 4: Verification
- [ ] 4.1 VERIFY: [Acceptance criteria 1]
- [ ] 4.2 VERIFY: [Acceptance criteria 2]

## Success Criteria
- [ ] [Criterion 1 from interview]
- [ ] [Criterion 2 from interview]

## Files Changed
| File | Action |
|------|--------|
| path/to/new.swift | CREATE |
| path/to/existing.swift | MODIFY |
```

Complete Phase 6 by running:
```bash
ralph advance phase6
```

---

## Phase 7: PLAN REVIEW (Required)

**Use Ralph wrapper commands (never call rp-cli directly).**

### Run Plan Review

```bash
ralph review plan
```

Ralph selects context automatically from `plan.md`.

Optional one-shot finalize:
```bash
ralph review plan --final
```

Do not summarize review results until `ralph review plan --final` succeeds or `ralph show-proof phase7` renders the verified output.

### Process Review Feedback (re-review loop)

1. Run review on the current plan
2. Apply feedback to `plan.md`
3. **Run `ralph review plan` again** after edits
4. Complete Phase 7 with:
   ```bash
   ralph advance phase7
   ```

---

## Phase 8: FINALIZE (Required)

**Get user approval before execution.**

### Finalization Checklist

Before presenting to user, verify:

- [ ] Every "create" task has a corresponding "integrate" task
- [ ] Every task names specific files
- [ ] Every task has a VERIFY step
- [ ] Phase 4 has explicit verification tasks
- [ ] Success criteria match interview answers
- [ ] Files Changed table is complete
- [ ] Design review feedback incorporated
- [ ] Plan review feedback incorporated

### Present to User

```markdown
## Plan Ready: [Feature Name]

**Summary:**
- [N] tasks across [M] phases
- [X] files to create, [Y] files to modify

**Reviews completed:**
- ✅ Design review (`ralph review design`)
- ✅ Plan review (`ralph review plan`)
- [✅ Oracle review (`ralph oracle`, if applicable)]

**Key decisions:**
- [Decision 1 from interview/reviews]
- [Decision 2 from interview/reviews]

**How to proceed:**
1. **Review full plan** - See all tasks
2. **Edit plan** - Make changes before running
3. **Launch YOLO** - Execute all tasks automatically
4. **Interactive mode** - Work task by task

Ready to launch?
```

Complete Phase 8 by running:
```bash
ralph advance phase8
```

---

## Phase 9: EXECUTE

### Launch YOLO Mode

```bash
cd /path/to/project
ralph yolo
# Type 'yolo' to confirm
# Runs all tasks non-interactively
# Auto-commits each task
# Post-review runs automatically at end
```

Agent/CI contexts:
```bash
RALPH_YOLO_AUTO=1 ralph yolo
```

Note: Auto-YOLO requires a signed policy receipt (run `ralph allow-auto-yolo --reason "..."` in a TTY).

### Monitor Execution

- Watch for build failures
- Note any tasks that seem to struggle
- Be ready to intervene if needed

### On Failure

```bash
ralph status    # See where we stopped
ralph gates     # See exactly what's blocking
ralph ensure-reviews  # Run missing review wrappers
ralph next      # Fix the issue interactively
ralph yolo      # Continue from current task
```

Complete Phase 9 by running:
```bash
ralph advance phase9
```

---

## Phase 10: POST-REVIEW (Required)

**After YOLO completes, review the changes.**

### Automatic Post-Review

Ralph runs the post-review wrapper after YOLO completes. If it doesn't run automatically:

```bash
ralph review post
```

Optional one-shot finalize:
```bash
ralph review post --final
```

Do not summarize post-review results until `ralph review post --final` succeeds or `ralph show-proof phase10` renders the verified output.

### Manual Verification

For UI changes, verify visually:
```bash
gj run ms  # Or appropriate run command
# Check that feature works as expected
```

### Post-Implementation Review (Optional)

For complex changes, run an additional post-review via Ralph:

```bash
ralph review post
```

Complete Phase 10 by running:
```bash
ralph advance phase10
```

---

## Anti-Patterns (DO NOT DO)

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Skipping research | Questions are vague, plan is wrong |
| Skipping interview | Assumptions lead to rework |
| Skipping design review | Architecture issues caught too late |
| Skipping plan review | Missing tasks, broken YOLO |
| "Create X" without integration | Component built but never used |
| No file paths in tasks | Agent guesses wrong location |
| No verification tasks | Feature broken but marked done |
| Huge tasks | Too much scope, partial completion |
| Inconsistent task sizes | Large tasks "swallowed up", small tasks waste iterations |
| No success criteria | No way to know if done |
| Skipping post-review | Bugs ship to production |
| Direct tool calls | Bypasses Ralph receipts; gates won't pass |
| Not appending to progress.txt | Lost learnings, repeated mistakes |

---

## Ralph Wrapper Quick Reference

```bash
ralph review design    # Phase 4
ralph oracle           # Phase 5 (if required)
ralph review plan      # Phase 7
ralph review post      # Phase 10
ralph ensure-reviews   # Run missing review wrappers
ralph advance <phase>  # Complete a phase (required)
ralph yolo --auto      # Execute with auto-review compliance
```

---

## Example: Complete Flow

**User:** "Create a ralph loop for Xcode-style bottom console panel"

### 1. Research
```bash
rg -l "SyncProgress" --type swift
# Found: SyncProgressView.swift (current implementation)
# Found: MainSplitView.swift (where it's used)

cat "SharedUI/Common/SyncProgressView.swift" | head -50
# Current: floating card overlay

cat "Features/MediaOrganization/Views/MainSplitView.swift" | grep -A10 "SyncProgress"
# Integration point identified
```

### 2. Interview
```json
{
  "title": "Ralph Plan: Xcode-style Console Panel",
  "description": "Currently using floating card. You want Xcode-style bottom panel.",
  "questions": [
    {"id": "style", "question": "Confirm: Bottom slide-up panel like Xcode console?"},
    {"id": "resize", "question": "Should panel be resizable via drag?"},
    {"id": "collapse", "question": "Should panel collapse to header-only?"},
    {"id": "shortcut", "question": "Keyboard shortcut? (suggest ⌘⇧C)"},
    {"id": "acceptance", "question": "How will you verify it works?"}
  ]
}
```

### 3. Design
```markdown
## Design: Xcode-style Console Panel

### Architecture
- CREATE: SyncConsolePanel.swift (new component)
- MODIFY: MainSplitView.swift (replace SyncProgressView)
- MODIFY: AppState.swift (add showSyncConsole toggle)

### Integration
- SyncConsolePanel replaces SyncProgressView in StatusFooter
- Same callbacks (onCancel, onPause, etc.)
- AppState.showSyncConsole controls visibility
```

### 4. Expert Review (Ralph)
```bash
ralph review design
```

### 5. Create Plan
```markdown
## Tasks

### Phase 1: Create Component
- [ ] 1.1 Create SyncConsolePanel.swift in SharedUI/Common/
      VERIFY: File compiles, preview renders

### Phase 2: Integration  
- [ ] 2.1 Replace SyncProgressView with SyncConsolePanel in MainSplitView.swift StatusFooter
      VERIFY: New panel appears at bottom when sync starts

### Phase 3: Features
- [ ] 3.1 Add drag handle for resizing
      VERIFY: Dragging changes panel height
- [ ] 3.2 Add collapse/expand toggle
      VERIFY: Panel collapses to header only

### Phase 4: Verification
- [ ] 4.1 VERIFY: Panel slides up from bottom (not floating)
- [ ] 4.2 VERIFY: ⌘⇧C toggles visibility
- [ ] 4.3 VERIFY: Drag handle resizes panel
```

### 6. Plan Review (Ralph)
```bash
ralph review plan
```

### 7. Finalize & Execute
```bash
ralph yolo
# All tasks execute
# Codex review runs automatically
```

### 8. Post-Review
```bash
# Verify visually
gj run ms
# Check panel appears at bottom, drag works, etc.
```

---

## Key Principles

1. **Research first** - Understand before asking
2. **Interview always** - Never assume requirements  
3. **Design before tasks** - Architecture drives implementation
4. **Review twice** - Design review + Plan review via Ralph wrappers
5. **Atomic + Complete** - One thing, fully integrated
6. **Verify everything** - Build passing ≠ feature working
7. **Post-review always** - Ralph post-review + manual verification
8. **Anti-bloat** - Add only what closes a real failure mode; remove redundant layers
