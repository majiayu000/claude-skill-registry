---
name: map-codebase
description: Analyze codebase with parallel Explore agents to produce .planning/codebase/ documents. Use for brownfield project onboarding, refreshing codebase understanding after significant changes, before major refactoring, when onboarding to unfamiliar codebases, or when asked to understand codebase or analyze project structure. Creates structured documentation of stack, architecture, structure, conventions, testing, integrations, and concerns.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
# model: inherit
---

## Reference Files

**Workflow & Process:**

- [workflow.md](workflow.md) — Detailed orchestration and guidance

**Core Templates** (always use):

- [templates/stack.md](templates/stack.md) — STACK.md
- [templates/architecture.md](templates/architecture.md) — ARCHITECTURE.md
- [templates/structure.md](templates/structure.md) — STRUCTURE.md
- [templates/conventions.md](templates/conventions.md) — CONVENTIONS.md

**Optional Templates** (use as applicable):

- [templates/testing.md](templates/testing.md) — TESTING.md (if tests exist)
- [templates/integrations.md](templates/integrations.md) — INTEGRATIONS.md (if external services)
- [templates/concerns.md](templates/concerns.md) — CONCERNS.md (if complex project)

---

# Map Codebase

Analyzes existing codebases using parallel Explore agents to produce structured documentation in `.planning/codebase/`.

## Objective

Spawns multiple Explore agents to analyze different aspects of the codebase in parallel, each with fresh context. Results are structured documents in `.planning/` that provide a comprehensive map of the codebase state.

**Core Output** (always generated):

- `STACK.md` — Languages, frameworks, key dependencies
- `ARCHITECTURE.md` — System design, patterns, data flow
- `STRUCTURE.md` — Directory layout, module organization
- `CONVENTIONS.md` — Code style, naming, patterns

**Optional Output** (generate as applicable):

- `TESTING.md` — Test structure, coverage, practices (if tests exist)
- `INTEGRATIONS.md` — APIs, databases, external services (if external dependencies exist)
- `CONCERNS.md` — Technical debt, risks, issues (for complex/brownfield projects)

## When to Use

**Use map-codebase for:**

- **Brownfield projects** before initialization — understand existing code first
- **Refreshing codebase map** after significant changes
- **Onboarding** to an unfamiliar codebase
- **Before major refactoring** — understand current state thoroughly
- **When STATE.md references outdated codebase info** — refresh understanding

**Skip map-codebase for:**

- **Greenfield projects** with no code yet — nothing to map
- **Trivial codebases** (<5 files) — not worth the overhead

## Process

### Step 1: Check Existing Documents

Check if codebase documents already exist in `.planning/`:

- If yes: Offer to refresh (overwrite) or skip
- If no: Proceed with creation

### Step 2: Determine Template Set

Ask user which optional templates to generate (or use defaults):

- **Always**: STACK.md, ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md
- **Optional**: TESTING.md (if tests exist), INTEGRATIONS.md (if external services), CONCERNS.md (if complex project)

### Step 3: Load Project Context

Check for `.planning/STATE.md` to load existing project context if available. Helps agents understand project-specific terminology and patterns.

### Step 4: Process Focus Area Argument

If user provided a focus area (e.g., "api" or "auth"), instruct agents to pay special attention to that subsystem while still providing holistic analysis.

### Step 5: Spawn Parallel Explore Agents

Launch 4 Explore agents in parallel, each with "very thorough" exploration level:

**Agent 1: Technology Stack & Integrations**

- Focus: Languages, frameworks, dependencies, external services
- Outputs: Data for STACK.md and INTEGRATIONS.md

**Agent 2: Architecture & Structure**

- Focus: System design, patterns, directory organization
- Outputs: Data for ARCHITECTURE.md and STRUCTURE.md

**Agent 3: Conventions & Testing**

- Focus: Code style, naming patterns, test infrastructure
- Outputs: Data for CONVENTIONS.md and TESTING.md

**Agent 4: Concerns & Technical Debt**

- Focus: Issues, risks, technical debt, potential improvements
- Outputs: Data for CONCERNS.md

### Step 5: Collect Agent Findings

Wait for all agents to complete. Collect and organize findings by document type.

### Step 6: Write Core Documents

Write 4 core markdown documents in `.planning/`:

**STACK.md**: Languages, versions, frameworks, build tools, key dependencies  
**ARCHITECTURE.md**: System design, patterns, component relationships, data flow  
**STRUCTURE.md**: Directory layout, modules, naming patterns, organization  
**CONVENTIONS.md**: Code style, naming conventions, patterns, documentation

### Step 7: Write Optional Documents (if selected)

Generate only selected optional documents:

**TESTING.md** (if applicable): Test frameworks, structure, coverage, practices  
**INTEGRATIONS.md** (if applicable): External APIs, databases, third-party services, config  
**CONCERNS.md** (if applicable): Tech debt, issues, security, performance, improvements

### Step 8: Provide Next Steps

Inform user codebase mapping is complete:

- Review generated documents in `.planning/`
- Use findings to inform refactoring or development
- Update `STATE.md` with new insights if needed

## Success Criteria

- [ ] 4 core documents created in `.planning/` (STACK, ARCHITECTURE, STRUCTURE, CONVENTIONS)
- [ ] Optional documents created based on user selection
- [ ] All documents have substantive, actionable content
- [ ] Documents follow template structure
- [ ] Parallel agents completed without errors
- [ ] User informed of completion and next steps

## Integration Notes

**Command Integration:**

- Invoked via `/map-codebase [optional: focus-area]` command
- Focus area argument is passed to agents for targeted analysis

**Project Lifecycle:**

- Can run **before** initial project setup on brownfield codebases
- Can run **after** initial project setup to refresh as code evolves
- Can run **anytime** to refresh codebase understanding
