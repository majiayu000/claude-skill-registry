---
name: feature
description: Orchestrate feature development through 5 phases - discuss, BOM, architect, test plan, implement
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Task
  - Skill
  - AskUserQuestion
  - WebFetch
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
---

# Feature Skill

## Purpose
Entry point for complex features. Guides development through a structured 5-phase workflow.

**CRITICAL**: MUST ask questions until 100% understanding is achieved. Never assume - always clarify.

**CRITICAL**: If feature name not specified, ASK for it first. Feature name determines file paths.

**When to suggest**: Multi-component work, new features, significant changes. Skip for simple fixes.

## Checkin Mode (Resume Existing Feature)

**Syntax**: `/feature checkin to <feature-name>` or `/feature checkin <feature-name>`

When user says "checkin to \<feature\>", this means **resume work on an existing feature**:

1. **Locate feature folder**: `docs/features/{feature-name}/`
2. **Read all 5 files**: description.md, todos.md, scratchpad.md, journey.md, test-plan.md
3. **CLEANUP scratchpad.md** (MANDATORY):
   - Delete resolved questions, completed warnings, superseded decisions
   - Delete notes from completed phases
   - Move finalized decisions to description.md
   - Keep only items relevant to current/upcoming work
   - Target: under 50 lines
4. **Present current state summary**:

```markdown
## {Feature} - Current State

**Status**: {from todos.md}
**Last Updated**: {from todos.md}

### Active TODOs
{list unchecked items from todos.md}

### Known Issues
{from todos.md}

### Ideas in Scratchpad
{from scratchpad.md}

---
What would you like to work on?
```

5. **Wait for user direction** - do NOT ask initial questions (feature already exists)
6. **Continue from where left off** or work on specific TODO user selects

**DO NOT**:
- Ask scope questions for existing features
- Try to create new feature docs
- Start from Phase 1

**DO**:
- Read existing docs thoroughly
- Present status clearly
- Let user choose what to work on next

## Document Mode (Generate Docs from Existing Code)

**Syntax**: `/feature document <path>` or `/feature doc <path>`

When user wants to create feature documentation for **existing code** that has no docs:

### Step 1: Analyze Existing Code

1. **Identify feature boundary** from the path:
   - If path is a feature folder: `src/app/{name}/`
   - If path is a route: trace imports to find related components/directives

2. **Scan all related files**:
   ```
   Feature folder → components/, services/, models/, directives/, pipes/
   Routes → trace component imports
   ```

3. **Extract information**:
   | What | How |
   |------|-----|
   | Purpose | Read component names, file structure, comments |
   | Data model | Check Firebase queries, entity files |
   | User flows | Trace route → page → components → services |
   | Dependencies | Check imports, package.json |

### Step 2: Generate Feature Docs

Create `docs/features/{feature-name}/` with 5 files:

#### description.md
```markdown
# {Feature Name} Specification

> ⚠️ **Auto-generated from existing code** - Review for accuracy

## Overview
{Inferred from code structure and naming}

## Source Locations
| Type | Path |
|------|------|
| Feature | src/app/{name}/ |
| Routes | src/app/{name}/{name}-routing.module.ts |

## Requirements (Inferred)
- [ ] {Requirement inferred from code}

## Bill of Materials

### Existing Code
| Item | Location | Purpose |
|------|----------|---------|
| {component} | {path} | {inferred purpose} |

### Dependencies Used
| Package | Purpose |
|---------|---------|
| {pkg} | {inferred from usage} |
```

#### todos.md
```markdown
# {Feature Name} - TODOs

**Status**: Documented (existing feature)
**Last Updated**: {date}

## Documentation TODOs
- [ ] Review auto-generated description for accuracy
- [ ] Add missing requirements
- [ ] Document edge cases
- [ ] Add test coverage if missing

## Known Technical Debt
- [ ] {Any issues found during analysis}
```

#### journey.md
```markdown
# {Feature Name} - User Journeys

> ⚠️ **Auto-generated** - Verify flows match actual behavior

## Primary Flow
{Mermaid diagram inferred from route → component → hook chain}

## Entry Points
- Route: `/{path}`
- Navigation: {where user clicks to reach this}
```

#### test-plan.md
```markdown
# {Feature Name} - Test Plan

> ⚠️ **Auto-generated** - Review coverage

## Existing Tests
| File | Coverage |
|------|----------|
| {test file} | {what it tests} |

## Missing Coverage
- [ ] {gaps identified}
```

#### scratchpad.md
```markdown
# {Feature Name} - Scratchpad

## Analysis Notes
- Generated on: {date}
- Code analyzed: {files count}

## Questions for Author
- {Any unclear patterns found}
```

### Step 3: Present Summary

```markdown
## Feature Documentation Generated

**Feature**: {name}
**Files Analyzed**: {count}
**Docs Created**: docs/features/{name}/

### What I Found
- Components: {count}
- Hooks: {count}
- Routes: {count}
- Backend services: {count}

### Confidence Level
- Data model: {High/Medium/Low}
- User flows: {High/Medium/Low}
- Requirements: {High/Medium/Low}

### Review Needed
{List areas where inference was uncertain}

---
Please review the generated docs and correct any inaccuracies.
```

## Sync Mode (Update Docs to Match Code)

**Syntax**: `/feature sync <feature-name>` or `/feature sync <path>`

When documentation exists but may be out of sync with code:

### Step 1: Load Current State

1. **Read feature docs**: `docs/features/{feature-name}/`
2. **Scan current code**: feature folder, routes, backend
3. **Build comparison**:

| Aspect | In Docs | In Code | Status |
|--------|---------|---------|--------|
| Components | {list} | {list} | ✅ Match / ⚠️ Drift |
| Routes | {list} | {list} | ✅ Match / ⚠️ Drift |
| Data model | {desc} | {desc} | ✅ Match / ⚠️ Drift |

### Step 2: Detect Drift

**Check for:**

1. **New code not in docs**:
   - New components added
   - New routes added
   - Schema changes
   - New dependencies

2. **Docs reference deleted code**:
   - Components removed
   - Routes removed
   - Deprecated patterns

3. **Behavior changes**:
   - Different data flow than documented
   - Changed API contracts
   - Modified user journeys

### Step 3: Present Drift Report

```markdown
## Sync Report: {Feature Name}

### Summary
- Last doc update: {from todos.md}
- Files checked: {count}
- **Drift detected**: {Yes/No}

### ✅ In Sync
- {list items that match}

### ⚠️ Code Added (not in docs)
| Item | Location | Suggested Doc Update |
|------|----------|---------------------|
| {new component} | {path} | Add to BOM |

### ⚠️ Code Removed (still in docs)
| Item | Doc Location | Action |
|------|--------------|--------|
| {old component} | description.md line 45 | Remove reference |

### ⚠️ Behavior Changed
| Aspect | Documented | Actual |
|--------|------------|--------|
| {flow} | {old} | {new} |

---
Options:
1. **Auto-fix** - Update docs to match code
2. **Review each** - Go through changes one by one
3. **Skip** - Keep docs as-is
```

### Step 4: Apply Updates (if requested)

If user chooses "Auto-fix" or "Review each":

1. **Update description.md**:
   - Add new components to BOM
   - Remove deleted items
   - Update data model if changed

2. **Update journey.md**:
   - Regenerate flow diagrams if routes changed
   - Update entry points

3. **Update todos.md**:
   - Add items for new untested code
   - Mark `**Last Updated**:` with current date

4. **Update test-plan.md**:
   - Flag new code needing tests
   - Remove tests for deleted code

5. **Clean scratchpad.md**:
   - Add sync notes
   - Keep under 50 lines

### Sync Checklist

- [ ] All new code added to docs
- [ ] Deleted code removed from docs
- [ ] User journeys match actual flows
- [ ] Test plan reflects current coverage
- [ ] `**Last Updated**:` timestamp updated

## Initial Questions (REQUIRED - Use AskUserQuestion Tool)

Before ANY work begins, use `AskUserQuestion` tool for EACH question:

### 1. Feature Name (if not provided)
```
AskUserQuestion:
  question: "What should we name this feature?"
  header: "Feature Name"
  options:
    - label: "{suggested-name-1}"
      description: "Based on the description"
    - label: "{suggested-name-2}"
      description: "Alternative naming"
```
Use kebab-case for file paths: `docs/features/{feature-name}/`

### 2. Scope
```
AskUserQuestion:
  question: "What is the scope of this feature?"
  header: "Scope"
  options:
    - label: "Full-stack (Recommended)"
      description: "Backend + frontend changes"
    - label: "Backend only"
      description: "GraphQL schema, resolvers, services"
    - label: "Frontend only"
      description: "Components, hooks, routes (uses existing API)"
    - label: "Refactor"
      description: "Modify existing feature"
```

## Workflow Phases

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: DISCUSS                                                │
│ ├── Ask questions until 100% understood                         │
│ ├── Clarify scope, edge cases, constraints                      │
│ └── Output: docs/features/{feature}/description.md              │
├─────────────────────────────────────────────────────────────────┤
│ Phase 2: BILL OF MATERIALS                                      │
│ ├── Scan codebase for existing code to reuse                    │
│ ├── List new files needed                                       │
│ ├── Identify dependencies to add                                │
│ └── Output: BOM section in description.md                       │
│                                                                 │
│ ⛔ CHECKPOINT: Present outline, wait for user approval          │
├─────────────────────────────────────────────────────────────────┤
│ Phase 3: INTERFACES (calls /architect)                          │
│ ├── UI/UX Research (MANDATORY FIRST):                           │
│ │   ├── Check existing UI patterns                              │
│ │   ├── Read UX-DESIGN-GUIDE.md                                 │
│ │   ├── Ask: Which fields visible? Loading behavior?            │
│ │   ├── Plan URL architecture (state in URL)                    │
│ │   ├── Plan component splitting (one per file)                 │
│ │   ├── Create wireframes                                       │
│ │   └── Document table/drill-down requirements                  │
│ │                                                               │
│ │ ⛔ CHECKPOINT: Present UI/UX wireframes for approval          │
│ │                                                               │
│ ├── Present 2+ implementation options with trade-offs           │
│ ├── Wait for user to choose approach                            │
│ ├── Design chosen: Services, components                │
│ └── Output: docs/features/{feature}/journey.md                  │
│                                                                 │
│ ⛔ CHECKPOINT: Present architecture, wait for user approval     │
├─────────────────────────────────────────────────────────────────┤
│ Phase 4: TEST PLAN (calls /test --plan)                         │
│ ├── Test cases with T-IDs                                       │
│ ├── Coverage targets                                            │
│ ├── Test strategy per component                                 │
│ └── Output: docs/features/{feature}/test-plan.md                │
│                                                                 │
│ ⛔ FINAL CHECKPOINT: Output full spec, ask for confirmation     │
├─────────────────────────────────────────────────────────────────┤
│ Phase 5: IMPLEMENT (calls /implement)                           │
│ ├── Follow TODO checklist in todos.md                           │
│ ├── Check off items as completed                                │
│ ├── Run verification (build, lint, test)                        │
│ └── Update todos.md if changes requested                        │
└─────────────────────────────────────────────────────────────────┘
```

## MANDATORY Checkpoints

### Checkpoint 1: After BOM (before /architect)

**STOP and present outline to user:**

```markdown
## Feature Outline

### Requirements
{summarize key requirements}

### Related Features (Domain: {domain-prefix})
| Feature | Shared Patterns |
|---------|-----------------|
| {domain}-{other} | {what we reuse from it} |

### Cross-References Identified
- **Inbound**: {features that may link TO this feature}
- **Outbound**: {features this feature will link TO}

### Existing Code to Reuse
- {list items}

### New Files to Create
- {list items}

### Dependencies
- {list items}

---
Does this outline look correct? Ready to discuss implementation options?
```

**DO NOT call /architect until user explicitly approves.**

### Checkpoint 2: After /architect options (before detailed design)

The `/architect` skill will present 2+ options. Wait for user choice before designing.

### Checkpoint 3: After architecture (before /test)

**STOP and present architecture to user:**

```markdown
## Chosen Architecture

### Approach
{selected option summary}

### GraphQL Schema
{schema overview}

### Components
{component list}

### Data Flow
{flow diagram}

---
Does this architecture look good? Ready to plan tests?
```

**DO NOT call /test until user explicitly approves.**

### Checkpoint 4: FINAL (after test plan, before /implement)

**STOP and output the COMPLETE feature documentation:**

1. Read the full `docs/features/{feature}/` folder (description.md, todos.md, test-plan.md, journey.md)
2. Output the key sections to the user
3. Ask: "Here is the complete feature specification. Ready to start implementation?"

**DO NOT call /implement until user explicitly confirms.**

## Phase 1: DISCUSS

### Mandatory Questions (Use AskUserQuestion Tool)

Use `AskUserQuestion` tool for clarifications. Ask ONE question at a time:

1. **Scope**: What exactly should this feature do?
2. **Auth**: Who can access?
   ```
   AskUserQuestion:
     question: "Who can access this feature?"
     header: "Auth"
     options:
       - label: "Public"
         description: "No authentication required"
       - label: "Any authenticated user"
         description: "Must be logged in"
       - label: "Specific roles"
         description: "Admin, Owner, etc."
   ```
3. **Data**: What data is created/read/updated/deleted?
4. **Edge cases**: What happens on error? Empty state? Loading?
5. **Integration**: How does it connect to existing features?
6. **Priority**: Are all requirements equal or is there a MVP subset?

**Rule**: If a question has clear options, use `AskUserQuestion`. If open-ended, ask in prose.

### Output: Feature Docs

Create `docs/features/{feature-name}/` folder with 5 files:
- description.md - Feature overview and source locations
- todos.md - Implementation TODO checklist
- test-plan.md - Test strategy and cases
- journey.md - User journeys with Mermaid diagrams
- scratchpad.md - Notes, ideas, issues

Start with description.md using this structure:

```markdown
# {Feature Name} Specification

## Overview
{1-2 sentence description}

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## User Stories
- As a {role}, I want to {action} so that {benefit}

## Constraints
- {Any technical or business constraints}

## Open Questions
- {Questions that need resolution during implementation}
```

**DO NOT proceed to Phase 2 until user confirms description is complete.**

## Phase 2: BILL OF MATERIALS

### What to Identify

| Category | Question             | Example                   |
|----------|----------------------|---------------------------|
| **Data Model** | New models           | `Roll`                    |
| **Existing Code** | What can we reuse?   | `Avatar` component        |
| **New Routes** | What routes/screens? | `/flow`                   |
| **New Components** | What UI pieces?      | `ItemList`, `ItemDetails` |
| **Dependencies** | NPM packages?        | `nanoid`                  |

### BOM Section Format

Add to description.md:

```markdown
## Bill of Materials

### Existing Code to Reuse
| Item | Location | Purpose |
|------|----------|---------|
| Avatar | src/app/shared/components/avatar | Person image representation |

### New Files to Create
| File | Type | Purpose |
|------|------|---------|
| src/app/{name}/{name}-routing.module.ts | Route | Module routing |
| src/app/shared/componenents/{name}/{name}.components.ts | Component | New shared component |

### Dependencies to Add
| Package | Version | Purpose |
|---------|---------|---------|
| @angular/cdk | ^18.2.14 | Drag and drop |
```

## Phase 3: INTERFACES

### Step 1: UI/UX Research (MANDATORY - BEFORE BACKEND)

**Call `/architect` skill which will:**

1. **Check existing UI patterns** in codebase for similar features
2. **Read UX-DESIGN-GUIDE.md** for standard patterns
4. **Ask user about field visibility** - which fields to show where
5. **Ask user about loading behavior** - eager vs lazy for relations
6. **Plan URL architecture** - what state goes in URL (filters, tabs, modal IDs)
7. **Plan component splitting** - one component per file, extract reusable pieces
8. **Create wireframes** showing layout, components, states
10. **Document drill-down requirements** - how to navigate nested data

### Step 2: UI/UX Review Checkpoint (BLOCKING)

**STOP and present UI/UX plan to user:**

```markdown
## UI/UX Review

### Wireframes
{wireframe diagrams}

### Existing Patterns Reused
{list of patterns from existing features}

### Field Visibility
| Field | List | Detail |
|-------|------|--------|

### Loading Behavior
| Relation | Strategy |
|----------|----------|

### URL Architecture
| Param | Purpose |
|-------|---------|

### Component Split
| Component | Location | Lines |
|-----------|----------|-------|

---
Does this UI approach look correct?
```

**DO NOT proceed to implementation options until user approves UI/UX.**

### Step 3: Present Implementation Options

After UI/UX is approved, `/architect` will present **2+ implementation options**.

### Step 4: Wait for User Choice

**DO NOT proceed until user picks an option.**

### Step 5: Design Chosen Approach

After user chooses, `/architect` designs:

1. **Service Interface** (if new service)
2. **Component Props** (for new components)
3. **UI Flow Diagrams** (Mermaid)

### Step 6: Present Architecture for Approval

Before proceeding to Phase 4, present the complete architecture and wait for approval.

## Phase 4: TEST PLAN

### Prerequisites (MANDATORY)

**DO NOT call `/test --plan` until ALL conditions are met:**

1. ✅ Phase 3 (Interfaces) is COMPLETE
2. ✅ UI/UX wireframes were presented and APPROVED by user
3. ✅ 2+ implementation options were presented
4. ✅ User CHOSE an option
5. ✅ Architecture was designed for chosen option
6. ✅ Architecture was PRESENTED to user
7. ✅ User EXPLICITLY APPROVED the architecture

**If any condition is not met, STOP and complete Phase 3 first.**

### Calling /test

Only after all prerequisites are met, call `/test` skill:

```
/test --plan docs/features/{feature-name}/
```

## Phase 5: IMPLEMENT

### Prerequisites
- User explicitly confirmed the complete feature docs
- TODO checklist exists in todos.md

### Call /implement with feature folder path

```
/implement docs/features/{feature-name}/
```

### Code Style Gate (MANDATORY - BLOCKING)

**After implementation, run codestyle check:**

```
/codestyle --integration src/app/{feature-name}/
```

### Cross-Reference Update (MANDATORY - After Implementation)

**Before completing feature, update cross-references discovered during planning.**

1. **Read scratchpad.md** for `## Cross-References to Add` section
2. **For each cross-reference noted:**
   - Open related feature's `description.md`
   - Add reference under "## Related Features" section:
   ```markdown
   ### References This Feature
   | Feature | Relationship |
   |---------|--------------|
   | {new-feature} | {how it relates - navigates to, shares data, etc.} |
   ```
3. **Delete cross-reference notes from scratchpad** after updating

**This ensures future developers know about feature interconnections.**

### Quality Gate (MANDATORY)

After codestyle passes, VERIFY quality standards:

1. Read `.claude/skills/QUALITY-STANDARDS.md`
2. Check each item against implementation
3. If ANY mandatory item unchecked → continue implementation
4. Only mark complete when ALL standards met

**BLOCKING**: Tests must pass before feature is complete.

### TODO Checklist (CRITICAL)

The todos.md MUST contain an `## Active TODOs` section with checkboxes.
Skills MUST:
1. Read the TODO list before starting
2. Work through items IN ORDER
3. Check off `[x]` each item when complete
4. Update todos.md after each completed item
5. If user requests changes → update todos.md FIRST, then continue

### Implementation Order (from TODO list)
1. Components
2. Routes
3. Tests

## Resuming Work

Can invoke `/feature` at any phase:

```
/feature --phase=discuss "Feature Name"
/feature --phase=bom "Feature Name"
/feature --phase=architect "Feature Name"
/feature --phase=test-plan "Feature Name"
/feature --phase=implement "Feature Name"
```

Without `--phase`, continues from last incomplete phase.

## Feature Folder Structure

Each feature folder contains 5 files:
- `description.md` - Feature overview, source locations, BOM
- `todos.md` - Implementation TODO checklist
- `test-plan.md` - Test strategy and cases
- `journey.md` - User journeys with Mermaid diagrams
- `scratchpad.md` - Notes, ideas, issues (max 50 lines)

## Scratchpad Maintenance (MANDATORY)

The scratchpad.md file MUST stay concise to avoid context bloat.

### Max Size: 50 lines

If scratchpad exceeds 50 lines:
1. Delete resolved items immediately
2. Move finalized decisions to description.md
3. Summarize verbose notes into 1-2 lines

### What to DELETE (not archive)

- Resolved questions → just delete
- Completed warnings → just delete
- Superseded decisions → just delete
- Implementation notes after code is written → just delete

## Checklist

Before completing each phase:

### Phase 1 (Discuss)
- [ ] All mandatory questions answered
- [ ] User confirmed description is complete
- [ ] docs/features/{feature}/ folder created with 5 files

### Phase 2 (BOM)
- [ ] **Shared patterns documented** (from related feature docs)
- [ ] **Cross-references noted** (in scratchpad.md)
- [ ] Existing code identified
- [ ] New files listed
- [ ] Dependencies noted
- [ ] **⛔ CHECKPOINT: Outline presented to user**
- [ ] **⛔ User approved outline**

### Phase 3 (Interfaces)
- [ ] Existing UI patterns checked
- [ ] UX-DESIGN-GUIDE.md referenced
- [ ] Field visibility confirmed with user
- [ ] Loading behavior (eager/lazy) confirmed
- [ ] URL architecture planned (state in URL)
- [ ] Component split planned (one per file, ~150 lines max)
- [ ] Wireframes created
- [ ] **⛔ CHECKPOINT: UI/UX wireframes presented to user**
- [ ] **⛔ User approved UI/UX**
- [ ] **2+ implementation options presented**
- [ ] **User chose an option**
- [ ] GraphQL schema defined (if needed)
- [ ] **⛔ CHECKPOINT: Architecture presented to user**
- [ ] **⛔ User approved architecture**

### Phase 4 (Test Plan)
- [ ] Test strategy chosen
- [ ] Test cases with T-IDs
- [ ] Coverage targets set
- [ ] **⛔ FINAL CHECKPOINT: Full spec output to user**
- [ ] **⛔ User confirmed ready to implement**

### Phase 5 (Implement)
- [ ] todos.md has `## Active TODOs` section
- [ ] TODO items being checked off in todos.md
- [ ] scratchpad.md stays under 50 lines
- [ ] Build passes
- [ ] Lint passes
- [ ] **Code style check passes** (`/codestyle --integration`)
- [ ] **Tests implemented AND pass (BLOCKING)**
- [ ] **Quality standards verified**
- [ ] **Cross-references updated** (related features' description.md)
- [ ] `**Status**:` in todos.md set to "Complete"
