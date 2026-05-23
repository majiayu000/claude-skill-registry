---
name: front-door
description: "Intelligent entry point for all tasks. Interviews, triages, and routes. Use when starting any non-trivial work, when user says 'build me', 'new project', 'help me', '/interview', or '/front-door'."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Task
---

# front-door (ONE_SHOT v6.0)

You are executing the front-door skill - the intelligent orchestration hub for ONE_SHOT.

## Prime Directive

> USER TIME IS PRECIOUS. AGENT COMPUTE IS CHEAP.
> Ask ALL questions UPFRONT. Get ALL info BEFORE coding.
> NEVER REWRITE FROM SCRATCH. Extend, refactor, use existing solutions.

## When To Use

- User says "new project", "build me", "create", "start fresh"
- User says "help me", "/front-door", "/interview"
- TRIAGE intent = build_new or modify_existing
- Multi-file changes or unclear requirements detected
- User explicitly requests interview mode

## Auto-Detection Signals (Triggers Interview)

Any of these signals invoke the interview flow:
- **Vague scope**: User says "build me X" without specifics
- **Multi-domain request**: Spans UI + backend + infra
- **Missing context**: References things not found in codebase
- **High-stakes change**: Refactors, migrations, >5 files

## Smart Bypass for Trivial Tasks

**One triage question first:**
> "This seems straightforward - proceed directly or discuss first?"

**Bypass signals** (STRICT - all must apply):
- "typo" → Single word/character fix only
- "rename" → Search-replace operation with explicit before/after
- Explicit file path provided + estimated <10 lines change

**Signals that DO NOT bypass** (require at least mini-interview):
- "just add" → Still need to understand where and how
- "quick fix" → Could hide complexity
- "simple change" → Subjective, verify first

User can always force interview with `/front-door` or `/interview`.

---

## Interview Depth Control

Check `ONESHOT_INTERVIEW_DEPTH` environment variable OR session override:

| Mode | Trigger | Questions | Behavior |
|------|---------|-----------|----------|
| `full` | `ONESHOT_INTERVIEW_DEPTH=full` or `/full-interview` | All 13+ questions | No bypass, no auto-delegation, ask everything |
| `smart` | Default (no env var) | Auto-detect (5-13) | Full for greenfield, shorter for mods |
| `quick` | `ONESHOT_INTERVIEW_DEPTH=quick` or `/quick-interview` | Q1, Q2, Q6, Q12 only | Skip non-essential, use smart defaults |

### Depth Detection Logic

```
1. Check env var: $ONESHOT_INTERVIEW_DEPTH
2. Check session override: /full-interview or /quick-interview
3. If neither set, use smart detection:
   - "new project" + no existing code → full
   - "modify" + existing code → smart (5-8 questions)
   - "micro" or <100 lines → quick
```

### Session Override Commands

| Command | Effect |
|---------|--------|
| `/full-interview` | Force full depth this session (all 13+ questions) |
| `/quick-interview` | Force quick depth this session (Q1, Q2, Q6, Q12) |
| `/smart-interview` | Reset to smart detection (default) |

**When in doubt, prefer full.** Missing requirements → rework.

---

## TRIAGE (First 30 Seconds)

Before doing ANYTHING, classify the user's intent:

| Intent | Signals | Action |
|--------|---------|--------|
| **build_new** | "new project", "build me" | Full interview → PRD → Build |
| **fix_existing** | "broken", "bug", "error" | Quick triage → `debugger` skill |
| **continue_work** | "continue", "resume" | Use `resume-handoff` skill |
| **modify_existing** | "add feature", "change" | Interview → `create-plan` |
| **understand** | "explain", "how does" | Research only (bypass) |
| **quick_task** | "just", "quickly" | Quick triage → bypass |

**Triage Output:**
```
Intent: [type] | Scope: [micro/small/medium/large] | Flow: [Full/Mini/Direct/Research]
Next: [specific next step]
```

---

## Auto-Delegation During Triage (Context Optimization)

**CRITICAL**: For modify_existing, fix_existing, or understand intents, delegate exploration BEFORE interviewing.

### Immediate Delegation (before interview starts)

```
IF intent IN [modify_existing, fix_existing, understand]:
  1. Spawn Explore agent IMMEDIATELY (non-blocking)
  2. Start interview while agent explores
  3. Inject findings when agent returns
```

### Spawn Pattern

```
Task:
  subagent_type: Explore
  description: "Map codebase for {intent}"
  prompt: |
    User wants to: {user_request}

    Find and summarize:
    - Relevant files (max 10, ranked by relevance)
    - Existing patterns that apply
    - Key dependencies and imports
    - Related test files

    Return a 500-token summary with file:line references.
    Do NOT paste file contents - just paths and brief context.
```

### Non-Blocking Interview

```
1. Spawn Explore agent (returns immediately)
2. Ask first interview question (don't wait for agent)
3. Agent explores in parallel while user answers
4. When agent returns, inject under "## Discovery" in spec
5. Use discovered patterns to inform later questions
```

### Why This Matters

| Old Flow | New Flow |
|----------|----------|
| Read 10 files (10k tokens) | Interview starts immediately |
| Interview (200 tokens) | Agent explores in background |
| Spec file created | Agent returns summary (500 tokens) |
| **Total: 10,200 tokens** | **Total: 700 tokens** |

**Context reduction: 93%**

### Example

```
User: "Help me add rate limiting to the API"

1. Triage: intent=modify_existing, scope=medium

2. Spawn Explore agent:
   "User wants to add rate limiting to API.
    Find: middleware files, existing auth patterns,
    API route structure, any existing rate limit code."

3. Ask user (while agent explores):
   "What rate limiting strategy? Per-user, per-IP, or per-endpoint?"

4. Agent returns:
   "Found:
    - src/middleware/auth.ts:45 - existing middleware pattern
    - src/routes/api/*.ts - 12 route files, all use withAuth wrapper
    - No existing rate limiting
    - Uses Express with express-async-handler"

5. Inject into spec, continue interview with context
```

---

## Interview Mechanics

### Core Tool: AskUserQuestion

front-door is built on **AskUserQuestion** - Claude Code's native multi-choice question tool.

**Usage pattern:**
```javascript
AskUserQuestion({
  questions: [
    {
      question: "What problem are you solving?",
      header: "Problem",
      options: [
        { label: "Option A", description: "Details..." },
        { label: "Option B", description: "Details..." }
      ],
      multiSelect: false
    }
  ]
})
```

**Best practices:**
- 1-2 questions per call (quick focused iterations)
- Use `multiSelect: true` when choices aren't mutually exclusive
- Header should be <=12 chars (displays as chip)
- 2-4 options per question (users can always pick "Other")

### Question Strategy

**Visible progress tracker after each round:**
```
✓ Requirements  ✓ UX  ○ Edge Cases  ○ Testing
```

**Flag contradictions immediately:**
> "Earlier you said X, but now Y - which is correct?"

### Topic Exhaustion Detection

Full coverage required before suggesting completion:
- Requirements & success criteria
- UX & user flows
- Edge cases & error handling
- Testing strategy
- Technical constraints

### When User Gets Impatient

**One gentle push with stakes:**
> "Skipping discovery risks rework on [specific gaps]. Continue anyway?"

If user insists, proceed with assumptions documented.

---

## Mode Selection

| Mode | Trigger | Questions | Output |
|------|---------|-----------|--------|
| **Micro** | <100 lines, "quick script" | Q1, Q11 only | Single file |
| **Tiny** | Single CLI, no services | Skip web/AI | CLI/script |
| **Normal** | CLI or simple web/API | Full interview | Standard project |
| **Heavy** | Multi-service, AI agents | Full + AI questions | Multi-service |

---

## Project Type Templates

### Auto-Detection
Scan for package.json, go.mod, Dockerfile, etc. to infer type before asking.

### CLI Tool (Type A)
- Requirements, Success Criteria
- Shell integration (completion, aliases, piping)
- Configuration (config files, env vars, precedence)
- Testing strategy

### Web App (Type C/F)
- Requirements, Success Criteria
- State management, Auth/permissions
- Responsive/mobile design
- Error handling (loading states, boundaries)

### API/Backend (Type E)
- Requirements, Success Criteria
- Data modeling & migrations
- Auth & rate limits, Versioning
- Observability (logs, metrics, health)

### Library/SDK (Type B)
- Requirements, Success Criteria
- Public API surface
- Documentation strategy

---

## Project Types (Q6)

- A. CLI Tool
- B. Python Library
- C. Web Application
- D. Data Pipeline
- E. Background Service
- F. AI-Powered Web App
- G. Static / Landing Page

---

## Core Questions (Extract During Interview)

| ID | Key | Required | Smart Default |
|----|-----|----------|---------------|
| **Q0** | Mode | Yes | - |
| **Q1** | What are you building? | Yes | - |
| **Q2** | What problem does this solve? | Yes | - |
| **Q4** | Features (3-7 items) | Yes | - |
| **Q6** | Project type | Yes | - |
| **Q12** | Done criteria / v1 scope | Yes | - |
| Q3 | Philosophy | If non-default | "Simplicity first" |
| Q7 | Data shape | If non-default | From Q1 context |
| Q8 | Data scale | If non-default | A (Small) |
| Q9 | Storage | If non-default | SQLite |
| Q11 | Interface shape | If non-default | From Q6 |

---

## Output Artifacts

### Spec File
- **Location:** `~/.claude/plans/spec-YYYY-MM-DD-{slug}.md`
- **Format:** YAML frontmatter + markdown body
- **Written incrementally** (enables resume)
- **Confidence scores per section:** [HIGH/MED/LOW]

### Spec File Structure
```yaml
---
project: feature-name
type: web-app | cli | api | library
created: 2025-01-15
status: in-progress | complete
covered: [requirements, ux]
remaining: [edge-cases, testing]
---

# Feature Name Specification

## Requirements [HIGH]
- ...

## UX & User Flows [MED]
- ...

## Edge Cases [TBD]
- Not yet explored

## Testing Strategy [TBD]
- Not yet explored
```

---

## Visual Iteration Loop (Web Apps)

When building web UIs with Playwright MCP configured:

```
1. Implement UI change
2. Take full-page screenshot via Playwright
3. Self-assess: "Rate this design 1-10 for [criteria from spec]"
4. If < 10/10: identify specific issues, iterate
5. Repeat until 10/10 or user-defined threshold
```

**Triggers:** `visual_polish: true`, project type C or F, "make it look good"

---

## Routing Logic (Post-Interview)

| Classification | Route To |
|----------------|----------|
| New project (greenfield) | `create-plan` → implementation |
| Existing + complex | `create-plan` → implementation |
| Existing + simple | Direct implementation |

**Intelligent complexity detection:**
- Multi-file changes → create-plan
- Single-file, clear requirements → direct implement

---

## Resume Capability

If interview is interrupted (/clear, context exhaustion):
- Spec file tracks `covered` vs `remaining` categories
- On resume, Claude reads spec file and picks up where left off
- User sees: "Resuming from partial spec. Already covered: X, Y. Now exploring: Z"

---

## Hard Stops (Require Explicit Approval)

- Storage upgrade (files → SQLite → Postgres)
- Auth method changes
- Production deployment changes
- External API integration
- Data deletion operations
- Schema migrations

**Action:** STOP → Present prompt → Wait for approval → Log decision

---

## Project Invariants

Every project from front-door MUST have:
- `README.md` - one-line description, current tier, upgrade trigger, quick start
- `TODO.md` - task tracking (kanban-style)
- `LLM-OVERVIEW.md` - complete project context for any LLM
- `PRD.md` - approved requirements document
- `scripts/` - setup.sh, start.sh, stop.sh, status.sh
- `/health` endpoint (if service) with /metrics
- Storage tier documented with upgrade trigger

---

## Storage Decision Matrix

| Need | Solution | Why |
|------|----------|-----|
| Simple local storage | SQLite | Zero config, portable |
| Real-time web app | Convex | Reactive DB, TypeScript, built-in auth |
| User auth with magic links | Supabase | Built-in auth, edge functions |
| Production DB, multi-user | OCI Autonomous DB | Free 20GB, managed Oracle |
| File/blob storage | OCI Object Storage | Free 20GB, pre-signed URLs |

---

## Quick Mode (formerly Yolo Mode)

**Trigger**: "yolo", "fast mode", "just do it", "quick mode"

1. Ask only: Q0, Q1, Q2, Q6, Q12
2. Propose smart defaults for rest
3. Show summary: "Using these defaults: [list]. Proceed?"
4. On "yes" → Generate PRD immediately

**Smart Defaults by Type:**
| Q6 Type | Stack | Storage |
|---------|-------|---------|
| A. CLI | Python, Click | SQLite |
| B. Library | Python, pytest | N/A |
| C. Web | Next.js, React | Convex |
| D. Pipeline | Python, pandas | SQLite |
| E. Service | Python, APScheduler | SQLite |
| F. AI Web | Next.js, React, OpenRouter | Convex |
| G. Static | HTML/CSS/JS | N/A |

---

## Micro Mode

**Trigger**: "micro mode" OR describes <100 line script

**Questions**: Only Q1 (what) and Q11 (interface)

**Skip**: PRD, README, LLM-OVERVIEW, scripts/, TODO.md

**Output**: Single file with shebang, inline comments, usage in header

---

## Anti-Patterns

- Under-interviewing (missing critical requirements → rework)
- Analysis paralysis (never moving to implementation)
- Drip-feeding questions (ask all upfront)
- Building without PRD approval
- PostgreSQL for small data (use SQLite)
- Adding abstraction "for flexibility"
- Skipping TODO.md updates
- Using full flow for micro tasks

---

## Workflow Summary

```
1. TRIAGE (30 seconds)
   └─ Classify intent, assess scope

2. BYPASS CHECK
   └─ Trivial? → Ask one triage question → Direct action

3. INTERVIEW (iterative)
   └─ 1-2 questions per round
   └─ Progress tracker visible
   └─ Write spec incrementally

4. SPEC COMPLETE
   └─ All categories covered OR user insists on proceeding

5. ROUTE
   └─ Greenfield/complex → create-plan
   └─ Simple → direct implementation
```

---

## Keywords

front-door, interview, triage, spec, discovery, requirements, build me, new project, help me, oneshot, yolo, micro, fast, create, start fresh
