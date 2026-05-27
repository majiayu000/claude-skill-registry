---
name: decompose
description: Decompose a phase plan into atomic beads and sub-beads. Use when breaking down a phase into tasks, when the user mentions "decompose" or "break down", when creating beads from a plan, or when structuring work for parallel execution.
---

# Decompose — Task Breakdown

Break a phase into atomic beads and sub-beads for agent execution.

> **Design rationale:** This skill uses the orchestrator-subagent pattern because decomposition involves substantial cognitive work: understanding the phase, creating a lossless manifest, generating beads, setting dependencies, and validation. The "Create Beads" phase is especially critical—when an agent reads a 1000-line phase doc directly, it summarizes. With subagents, the manifest captures everything first, preventing information loss.

## When This Applies

| Signal | Action |
|--------|--------|
| User says "decompose" or "break down" | Run full protocol |
| Have a phase plan ready | Decompose into beads |
| User says "/decompose" | Run full protocol |
| Need to structure work for agents | Create bead hierarchy |

---

## Tool Reference

### File Operations
| Tool | Purpose |
|------|---------|
| `Read(phase_doc_path)` | Read phase document |
| `Read(north_star_path)` | Read North Star for context |
| `Write(file_path, content)` | Write manifest, reports |

### Beads (Task Tracking)
| Command | Purpose |
|---------|---------|
| `bd create --title "..." --body "..."` | Create parent bead |
| `bd create --parent <id> --title "..."` | Create sub-bead |
| `bd dep add <child> <blocker>` | Set dependency |
| `bd list --json` | List all beads |

### BV (Graph Intelligence)
| Command | Purpose |
|---------|---------|
| `bv --robot-suggest` | Find missing dependencies |
| `bv --robot-plan` | Validate execution order |
| `bv --robot-alerts` | Check for risks/cycles |

### Sub-Bead Suffix Convention
| Suffix | Purpose |
|--------|---------|
| `.1` | Schema/types/models |
| `.2-.3` | Core implementation |
| `.4-.8` | Tests |
| `.9` | Integration/wiring |
| `.10` | Documentation |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECOMPOSE ORCHESTRATOR                        │
│  - Creates session: sessions/decompose-{timestamp}/              │
│  - Manages TodoWrite state                                       │
│  - Spawns subagents with minimal context                         │
│  - Passes manifest (not phase doc) to Create Beads phase         │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Understand     │  │    Manifest     │  │  Create Beads   │
│  agents/        │  │  agents/        │  │  agents/        │
│  understand.md  │  │  manifest.md    │  │  create-beads.md│
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
    01_understanding     02_manifest.md      03_beads_created
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  Dependencies   │  │    Validate     │ → Ready for execution
│  agents/        │  │  agents/        │
│  dependencies.md│  │  validate.md    │
└────────┬────────┘  └────────┬────────┘
         │                    │
    04_dependencies      05_validation
```

## Subagents

| Phase | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | `agents/understand.md` | phase_doc | goals, components, ambiguities |
| 2 | `agents/manifest.md` | understanding | lossless item list |
| 3 | `agents/create-beads.md` | manifest (NOT phase doc) | parent + sub-beads |
| 4 | `agents/dependencies.md` | beads created | dependency graph |
| 5 | `agents/validate.md` | dependencies | validation report |

---

## Why Subagents for Decomposition

**The "Create Beads" phase is the most lossy.** When an agent reads a 1000-line phase doc directly, it summarizes. With subagents:

| Monolithic | Subagent Pattern |
|------------|------------------|
| Agent reads phase doc, summarizes | Manifest captures everything first |
| Create Beads sees summarized version | Create Beads sees manifest (lossless) |
| "4 tests for X" | Actual test code in manifest |
| Context bombing | Fresh context per phase |

**Key insight:** The manifest becomes the source of truth. Create Beads never reads the original phase doc—it reads the manifest.

---

## Execution Flow

### 1. Setup (Orchestrator)

```markdown
1. Create session directory:
   mkdir -p sessions/decompose-{timestamp}

2. Initialize TodoWrite with phases:
   - [ ] Phase 1: Understand
   - [ ] Phase 2: Manifest
   - [ ] Phase 3: Create Beads
   - [ ] Phase 4: Dependencies
   - [ ] Phase 5: Validate

3. Gather inputs:
   - phase_doc_path: Path to phase document
   - north_star_path: Path to North Star Card
```

### 2. Phase 1: Understand

**Spawn:** `agents/understand.md`

**Input:**
```json
{
  "phase_doc_path": "PLAN/phase-2.md",
  "session_dir": "sessions/decompose-{timestamp}",
  "north_star_path": "PLAN/00_north_star.md"
}
```

**Output:** understanding_path + goals + ambiguities

### 3. Phase 2: Manifest

**Spawn:** `agents/manifest.md`

**Input:**
```json
{
  "session_dir": "sessions/decompose-{timestamp}",
  "understanding_path": "<from Phase 1>",
  "phase_doc_path": "PLAN/phase-2.md"
}
```

**Output:** manifest_path + item counts + gaps

### 4. Phase 3: Create Beads (CRITICAL)

**Spawn:** `agents/create-beads.md`

**Input:**
```json
{
  "session_dir": "sessions/decompose-{timestamp}",
  "manifest_path": "<from Phase 2>",
  "north_star_path": "PLAN/00_north_star.md",
  "phase_name": "Phase 2: User Auth"
}
```

**CRITICAL:** Input is `manifest_path`, NOT `phase_doc_path`. The manifest is the lossless source of truth.

**Output:** beads_created_path + bead IDs

### 5. Phase 4: Dependencies

**Spawn:** `agents/dependencies.md`

**Input:**
```json
{
  "session_dir": "sessions/decompose-{timestamp}",
  "beads_created_path": "<from Phase 3>"
}
```

**Output:** dependencies_path + execution order

### 6. Phase 5: Validate

**Spawn:** `agents/validate.md`

**Input:**
```json
{
  "session_dir": "sessions/decompose-{timestamp}",
  "dependencies_path": "<from Phase 4>",
  "manifest_path": "<from Phase 2>"
}
```

**Output:** validation_path + ready_for_execution

### 7. Finalize (Orchestrator)

1. Update TodoWrite (all phases complete)
2. If validation failed, report issues
3. Output summary to user

---

## Templates

Located in `.claude/templates/planning/`:
- `content-manifest.md` — Pre-decomposition checklist
- `sub-bead-structure.md` — Standard suffix pattern
- `decompose-output.md` — Output summary format

---

## 1. Understand

Read the phase. Identify:
- Goal
- Components/files
- Dependencies (what must exist first)
- Deliverables (how we know it's done)

**If vague → ask for clarification before decomposing.**

---

## 2. Manifest

Use content-manifest template. List everything:
- Components
- Files to create/modify
- Tests required
- Dependencies
- Acceptance criteria

---

## 3. Create Beads

### Terminology Clarification

| Term | When Created | Purpose |
|------|--------------|---------|
| **Phase/Epic bead** | Planning | Container for a phase's work |
| **Task beads** | Planning | Individual work items under a phase |
| **ADaPT sub-beads** | Execution (after 3 failures) | Decompose failing task |

**Phase/Epic bead (container for the phase):**
```bash
bd create "Phase N: <Title>" -t epic -p 1 -d '<description>'
```

**Task beads (the actual work items):**
```bash
bd create "<Task title>" --parent <phase-id> --priority 1 -d '<Full description>'
```

> **Note:** Task beads use suffixes `.1`, `.2`, etc. for organization. This is DIFFERENT from ADaPT sub-beads which are created when execution fails. See `templates/planning/sub-bead-structure.md` for ADaPT.

### Critical Rules — Bounded. Complete. Verified.

| Rule | Why |
|------|-----|
| **BOUNDED** | Scoped to what an agent can hold in working memory |
| **COMPLETE** | Every detail from phase survives (no summarization) |
| **VERIFIED** | A fresh agent could implement without clarifying questions |
| **FULL CODE** | Complete code with all imports, not snippets |
| **FULL TESTS** | Actual test code, not "4 tests for X" |
| **NO SUMMARIZING** | Reorganize, don't paraphrase |
| **STANDALONE** | Each sub-bead executable without referencing others |
| **NORTH STAR** | Copy North Star Card into every sub-bead |

---

## 4. Set Dependencies

```bash
bd dep add <child-id> <blocker-id> --type blocks
```

Common pattern:
- Schema (.1) → blocks → Implementation (.2, .3)
- Implementation → blocks → Tests (.4-.8)
- All sub-beads → block → Parent completion

---

## 5. Validate

```bash
bv --robot-suggest   # Duplicates, missing deps, cycle breaks
bv --robot-plan      # Can work proceed in order?
bv --robot-alerts    # Stale, cascades, drift signals
```

**Fix issues before agents start executing.**

---

## Sizing Guidelines

The goal is **semantic coherence**, not fixed line counts. Can an agent hold the full context without losing track?

| Heuristic | Question |
|-----------|----------|
| **Bounded** | Can an agent hold this in working memory without degradation? |
| **Complete** | Does every detail from the phase survive? |
| **Verified** | Could a fresh agent implement this without clarifying questions? |
| **Testable** | Is it independently verifiable? |

If you'd have to guess → the bead isn't ready. If an agent would ask "what should I do here?" → keep decomposing.

---

## When to STOP and Ask

1. **Phase too vague** — Can't identify concrete deliverables
2. **Phase too large** — Would result in 20+ sub-beads (split phase)
3. **Unclear dependencies** — Don't know what must exist first
4. **Multiple valid approaches** — Need architectural decision first

---

## Task Bead Suffix Convention (Planning-Time)

> **IMPORTANT DISTINCTION:**
> - **Planning-time task beads** (this section): Created upfront when decomposing phases
> - **ADaPT sub-beads**: Created ONLY when execution fails after 3 iterations
>
> Both use the same `.1`, `.2` naming, but serve different purposes. See `.claude/templates/planning/sub-bead-structure.md` for ADaPT sub-beads.

| Suffix | Purpose |
|--------|---------|
| `.1` | Schema/types/models |
| `.2-.3` | Core implementation |
| `.4-.8` | Tests |
| `.9` | Integration/wiring |
| `.10` | Documentation (if needed) |

**Example:** For epic `user-auth` (Phase bead):
- `user-auth.1` → User model schema (task bead)
- `user-auth.2` → JWT validation logic (task bead)
- `user-auth.3` → Session management (task bead)
- `user-auth.4` → Unit tests for JWT (task bead)
- `user-auth.5` → Integration tests (task bead)

**If `user-auth.2` fails after 3 iterations during execution:**
- `user-auth.2.1` → ADaPT sub-bead for specific failing component

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Summarize: "4 tests for validation" | Include full test code |
| Reference elsewhere: "See phase plan" | Copy verbatim |
| Skip imports: Partial code | Full runnable code |
| Huge beads: 2000+ lines | Split further |
| Forget tests: Implementation without .4-.8 | Always include |

---

## Output Format

Use decompose-output template. Include:
- Parent bead ID
- Sub-beads table with IDs, titles, estimates, dependencies
- Verification checklist
- Next steps

---

## See Also

- `docs/workflow/DISCOVERY.md` — Pre-pipeline discovery (where plans come from)
- `docs/workflow/DECOMPOSITION.md` — Full decomposition guide
- `advance/` — Bead lifecycle
- `.claude/templates/planning/` — Templates
