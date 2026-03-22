---
name: vp
description: >-
  Create interactive visual prototype playground for user approval before technical decomposition.
  Use when asked to 'create prototype', 'visual mockup', 'preview design', 'design playground',
  or 'show me the feature'. NOT for brainstorming (use /brainstorm), NOT for feature discovery
  (use /nf), NOT for implementation tasks (use /ct).
argument-hint: [task-directory or feature-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

# Visual Prototype Command

## PRIMARY OBJECTIVE
Create interactive HTML playground for visual approval of feature designs before technical decomposition. Works for both UI-facing tasks (mobile/web screens) and backend tasks (architecture diagrams with Mermaid.js).

## PREREQUISITES
- Discovery document exists (`/nf` completed)
- Task directory created at `tasks/task-YYYY-MM-DD-[feature-name]/`

## WORKFLOW STEPS

### GATE 0: Task Discovery

1. **Locate task directory:**
   - If argument provided: Use `tasks/task-YYYY-MM-DD-[argument]/` or match partial name
   - If no argument: List recent task directories, ask user to select

2. **Validate discovery document exists:**
   - Look for `discovery-[feature-name].md` in task directory
   - **STOP if missing:** "No discovery document found. Run `/nf` first to create feature specification."

3. **Read discovery document:**
   - Extract: Feature overview, requirements, UI/UX specifications, technical considerations
   - Identify key screens, flows, entities, and interactions

---

### GATE 1: Task Type Detection

**Analyze discovery document for keywords to determine playground type:**

**UI_FACING** (use design-playground template):
- Contains "Screen:", "Button", "Input", "Modal", "Navigation", "Card", "List"
- Has ASCII wireframes or user flow diagrams
- References mobile/web components
- Contains "UI/UX Specifications" section with detail

**BACKEND** (use code-map template):
- Contains "Service", "Repository", "Use Case", "API endpoint", "Entity"
- References database/schema changes
- Contains "Technical Considerations" without UI specs
- DDD layer references (Domain, Application, Infrastructure)

**Detection logic:**
```
IF UI keywords count > Backend keywords count AND has UI/UX section:
  → UI_FACING_TASK
ELSE IF Backend keywords count > UI keywords count OR no UI section:
  → BACKEND_TASK
ELSE:
  → ASK_USER with AskUserQuestion tool
```

**Confirm with user via AskUserQuestion:**
"Detected [UI-facing/backend] task. Creating [design playground/architecture diagram]. Proceed?"

---

### GATE 2: Playground Generation

**Invoke the `playground` skill** with context from discovery document.

#### For UI-Facing Tasks:

```
Use the playground skill to create a design playground for [FEATURE_NAME].

**Context from discovery:** [PASTE UI/UX SPECIFICATIONS SECTION]

**Requirements:**
- Use Wythm design system tokens (read `.claude/skills/design-tokens/SKILL.md` for current palette, fonts, spacing)
- Reference colors, fonts, and spacing from the project's design token definitions
- Phone frame: 375x780px with notch
- Three-column layout: Controls | Preview | Implementation Notes

**Scenarios to include:**
1. Happy Path: [Main flow from discovery]
2. Edge Cases: [From discovery edge cases section]
3. Error States: [From error handling section]
4. Empty State: [If applicable]

**Output file:** [TASK_DIRECTORY]/playground-[feature-name].html
```

#### For Backend Tasks:

```
Use the playground skill to create a code-map playground for [FEATURE_NAME].

**Context from discovery:** [PASTE TECHNICAL CONSIDERATIONS SECTION]

**Requirements:**
- SVG-based architecture diagram with Mermaid.js (prefer C4 diagram type for DDD layer visualization, flowcharts for processes)
- Show DDD layers: Domain, Application, Infrastructure
- Click-to-comment enabled on all components
- Connection types: data-flow (blue), dependency (gray), event (red)

**Components to visualize:**
- Entities: [From discovery]
- Use Cases: [From discovery]
- Repositories: [From discovery]
- API Endpoints: [From discovery]

**Presets:**
1. Full System - All layers visible
2. Domain Focus - Entities and domain services only
3. API Flow - Request path through layers

**Output file:** [TASK_DIRECTORY]/playground-[feature-name].html
```

**After playground created:**
```bash
open [TASK_DIRECTORY]/playground-[feature-name].html
```

---

### GATE 3: User Interaction and Approval

**Iterative approval loop** - allows refinement without restarting.

1. **Present to user:**
   ```
   Playground created and opened in browser.

   Please explore the prototype and provide your decision:
   ```

2. **Use AskUserQuestion with options:**
   - **Approve** - Ready for technical decomposition
   - **Request Changes** - Specify modifications (stays in /vp)
   - **Reject** - Needs significant discovery rework

3. **Handle each decision:**

   **If APPROVED:**
   - Capture any final notes from user
   - Proceed to GATE 4

   **If CHANGES_REQUESTED:**
   - Capture specific change requests
   - Re-invoke playground skill with modifications
   - Regenerate playground file
   - Return to step 1 of GATE 3 (loop until approved/rejected)

   **If REJECTED:**
   - Capture rejection reason
   - Update discovery doc with rejection status
   - Advise: "Discovery needs refinement. Consider running `/nf` again with additional context."
   - **STOP**

---

### GATE 4: Documentation Update

**Update discovery document with approval status:**

1. **Add Visual Prototype Approval section** at end of discovery doc:

```markdown
---

## Visual Prototype Approval

**Status**: APPROVED
**Date**: [TODAY]
**Prototype**: `playground-[feature-name].html`

### User Feedback
[Captured feedback from user interaction]

### Key Decisions Confirmed
- [Decisions validated during prototype review]

### Notes for Technical Decomposition
[Any clarifications discovered during prototype review]
```

2. **Notify user:**
   ```
   Visual prototype approved!

   - Playground: playground-[feature-name].html
   - Discovery updated with approval status
   - Ready for /ct (Create Task) to proceed with technical decomposition
   ```

---

## OUTPUT

**Files created/modified:**
- `tasks/task-YYYY-MM-DD-[feature-name]/playground-[feature-name].html` (new)
- `tasks/task-YYYY-MM-DD-[feature-name]/discovery-[feature-name].md` (updated)

**Next step:** Run `/ct` to create technical decomposition based on approved visual prototype.

---

## TIPS FOR EFFECTIVE PLAYGROUNDS

**UI Playgrounds:**
- Include realistic data (names, numbers, text) not lorem ipsum
- Show loading states and transitions
- Test with different content lengths
- Include accessibility indicators

**Backend Playgrounds:**
- Focus on data flow, not implementation details
- Use comments to capture architectural concerns
- Show error paths, not just happy path
- Indicate async vs sync operations

**Prompt Output:**
- The playground's "Copy Prompt" button generates implementation notes
- These notes can be pasted directly into `/ct` for technical decomposition
- Include in discovery doc under "Notes for Technical Decomposition"
