---
name: specify
description: Interactive specification workflow - design vision, clarify capabilities, extract behaviors. Produces spec packets, capability maps, and ADRs for /plan consumption.
---

# Specify Workflow

**IMPORTANT: All tasker working files go in `$TARGET_DIR/.tasker/`. Do NOT create any other directories like `project-planning/`, `planning/`, or `schemas/` at the target project root. The `.tasker/` directory is the ONLY location for tasker artifacts (including `.tasker/schemas/` for JSON schemas).**

An **agent-driven interactive workflow** that transforms ideas into actionable specifications with extracted capabilities, ready for `/plan` to decompose into tasks.

## Core Principles

1. **Workflows and invariants before architecture** - Never discuss implementation until behavior is clear
2. **Decision-dense, not prose-dense** - Bullet points over paragraphs
3. **No guessing** — Uncertainty becomes Open Questions
4. **Minimal facilitation** — Decide only when required
5. **Specs are living; ADRs are historical**
6. **Less is more** — Avoid ceremony

## Artifacts

### Required Outputs (in TARGET project)
- **README** — `{TARGET}/README.md` (project overview - what it is, how to use it)
- **Spec Packet** — `{TARGET}/docs/specs/<slug>.md` (human-readable)
- **Capability Map** — `{TARGET}/docs/specs/<slug>.capabilities.json` (machine-readable, for `/plan`)
- **Behavior Model (FSM)** — `{TARGET}/docs/state-machines/<slug>/` (state machine artifacts, for `/plan` and `/execute`)
- **ADR files** — `{TARGET}/docs/adrs/ADR-####-<slug>.md` (0..N)

### Working Files (in target project's .tasker/)
- **Session state** — `$TARGET_DIR/.tasker/state.json` (persistent, primary resume source)
- **Spec draft** — `$TARGET_DIR/.tasker/spec-draft.md` (working draft, written incrementally)
- **Discovery file** — `$TARGET_DIR/.tasker/clarify-session.md` (append-only log)
- **Stock-takes** — `$TARGET_DIR/.tasker/stock-takes.md` (append-only log of vision evolution)
- **Decision registry** — `$TARGET_DIR/.tasker/decisions.json` (index of decisions/ADRs)
- **Spec Review** — `$TARGET_DIR/.tasker/spec-review.json` (weakness analysis)

### Archive
After completion, artifacts can be archived using `tasker archive` for post-hoc analysis.

---

## MANDATORY: Phase Order

```
Initialization → Scope → Clarification Loop (Discovery) → Synthesis → Architecture Sketch → Decisions/ADRs → Gate → Spec Review → Export
```

**NEVER skip or reorder these phases.**

---

# Phase 0 — Initialization

## Goal
Establish project context and session state before specification work begins.

## STEP 1: Auto-Detect Session State (MANDATORY FIRST)

**Before asking the user anything**, check for existing session state files.

### 1a. Determine Target Directory

Check in order:
1. If user provided a path in their message, use that
2. If CWD contains `.tasker/state.json`, use CWD
3. Otherwise, ask:

```
What is the target project directory?
```

### 1b. Check for Existing Session

```bash
TARGET_DIR="<determined-path>"
STATE_FILE="$TARGET_DIR/.tasker/state.json"

if [ -f "$STATE_FILE" ]; then
    # Read state to determine if session is in progress
    PHASE=$(jq -r '.phase.current' "$STATE_FILE")
    if [ "$PHASE" != "complete" ] && [ "$PHASE" != "null" ]; then
        echo "RESUME: Found active session at phase '$PHASE'"
        # AUTO-RESUME - skip to Step 1c
    else
        echo "NEW: Previous session completed. Starting fresh."
        # Proceed to Step 2 (new session)
    fi
else
    echo "NEW: No existing session found."
    # Proceed to Step 2 (new session)
fi
```

### 1c. Auto-Resume Protocol (if active session found)

**If `.tasker/state.json` exists and `phase.current != "complete"`:**

1. **Read state.json** to get current phase and step
2. **Inform user** (no question needed):
   ```
   Resuming specification session for "{spec_session.spec_slug}"
   Current phase: {phase.current}, step: {phase.step}
   ```
3. **Read required working files** for the current phase (see Resume Protocol section)
4. **Jump directly to the current phase** - do NOT re-run earlier phases

**This is automatic. Do not ask the user whether to resume.**

---

## STEP 2: New Session Setup (only if no active session)

### 2a. No Guessing on Reference Materials

**You MUST NOT:**
- Scan directories to infer what files exist
- Guess spec locations from directory structure
- Read files to detect existing specs
- Make any assumptions about what the user has

**The user tells you everything. You ask, they answer.**

### 2b. Ask About Reference Materials

Ask using AskUserQuestion:
```
Do you have existing specification reference materials (PRDs, requirements docs, design docs, etc.)?
```
Options:
- **No reference materials** — Starting from scratch
- **Yes, I have reference materials** — I'll provide the location(s)

### If "Yes, I have reference materials":
Ask for the location(s):
```
Where are your reference materials located? (Provide path(s) - can be files or directories)
```
Free-form text input. User provides path(s) (e.g., `docs/specs/`, `requirements.md`, `PRD.pdf`).

**Validate path exists:**
```bash
EXISTING_SPEC_PATH="<user-provided-path>"
if [ ! -e "$TARGET_DIR/$EXISTING_SPEC_PATH" ] && [ ! -e "$EXISTING_SPEC_PATH" ]; then
    echo "Warning: Path not found. Please verify the path."
fi
```

### 2c. Initialize Session State

Create `.tasker/` directory structure in target project:

```bash
TASKER_DIR="$TARGET_DIR/.tasker"
mkdir -p "$TASKER_DIR"/{inputs,artifacts,tasks,bundles,reports,fsm-draft,adrs-draft}
```

Create `$TARGET_DIR/.tasker/state.json`:

```json
{
  "version": "3.0",
  "target_dir": "<absolute-path>",
  "phase": {
    "current": "initialization",
    "completed": [],
    "step": null
  },
  "created_at": "<timestamp>",
  "updated_at": "<timestamp>",
  "spec_session": {
    "project_type": "new|existing",
    "existing_spec_path": "<path-from-step-2-or-null>",
    "spec_slug": "<slug>",
    "spec_path": "<target>/docs/specs/<slug>.md",
    "started_at": "<timestamp>",
    "resumed_from": null
  },
  "scope": null,
  "clarify": null,
  "synthesis": null,
  "architecture": null,
  "decisions": null,
  "review": null
}
```

**CRITICAL: Update state.json after EVERY significant action.** This enables resume from any point.

The phase-specific state objects are populated as each phase progresses (see phase definitions below).

**If user provided existing spec path in Step 2b**, store it in `spec_session.existing_spec_path` for reference during Scope phase.

## Output (New Session Only)

For **new sessions** (Step 2 path):
- `.tasker/` directory structure created in target project
- Session state initialized in `$TARGET_DIR/.tasker/state.json`
- Existing spec path captured (if provided)
- Proceed to Phase 1 (Scope)

For **resumed sessions** (Step 1c path):
- State already exists - no initialization needed
- Jump directly to `phase.current` phase
- Read working files as specified in Resume Protocol

---

# Phase 1 — Scope

## Goal
Establish bounds before discovery.

## Pre-Scope: Load Existing Spec (if provided)

If `spec_session.existing_spec_path` was set during initialization:

1. **Read the existing spec file** to understand prior context
2. **Extract initial answers** for the scope questions below (Goal, Non-goals, Done means)
3. **Present extracted context** to user for confirmation/refinement rather than asking from scratch

```bash
if [ -n "$EXISTING_SPEC_PATH" ]; then
    echo "Loading existing spec from: $EXISTING_SPEC_PATH"
    # Read and analyze existing spec
    # Pre-fill scope questions with extracted information
fi
```

## Required Questions (AskUserQuestion)

Ask these questions using AskUserQuestion tool with structured options.
**If existing spec was loaded**, present extracted answers for confirmation rather than blank questions:

### Question 1: Goal
```
What are we building?
```
Free-form text input.

### Question 2: Non-goals
```
What is explicitly OUT of scope?
```
Free-form text input (allow multiple items).

### Question 3: Done Means
```
What are the acceptance bullets? (When is this "done"?)
```
Free-form text input (allow multiple items).

### Question 4: Tech Stack
```
What tech stack should be used?
```
Free-form text input. Examples:
- "Python 3.12+ with FastAPI, PostgreSQL, Redis"
- "TypeScript, Next.js, Prisma, Supabase"
- "Go with Chi router, SQLite"
- "Whatever fits best" (let /specify recommend based on requirements)

**If user says "whatever fits best" or similar:**
- Note this for Phase 2 (Clarify) to recommend based on gathered requirements
- Ask clarifying questions: "Any language preferences?", "Cloud provider constraints?", "Team expertise?"

### Question 5: Entry Point (CRITICAL for W8/I6 compliance)
```
How will users invoke this? What makes it available?
```

Options to present:
- **CLI command** — User runs a command (specify command name)
- **API endpoint** — User calls an HTTP endpoint (specify URL pattern)
- **Claude Code skill** — User invokes /skillname (specify trigger)
- **Library/module** — No direct invocation, imported by other code
- **Other** — Custom activation mechanism

**If user selects CLI/API/Skill:**
Follow up: "What specific steps are needed to make this available to users?"

**If user selects Library/module:**
Note in spec: "Installation & Activation: N/A - library/module only"

**Why this matters:** Specs that describe invocation without activation mechanism cause W8 weakness and I6 invariant failure. Capturing this early prevents dead entry points.

## Output

### 1. Update State (MANDATORY)

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "scope",
    "completed": ["initialization"],
    "step": "complete"
  },
  "updated_at": "<timestamp>",
  "scope": {
    "goal": "<user-provided-goal>",
    "non_goals": ["<item1>", "<item2>"],
    "done_means": ["<criterion1>", "<criterion2>"],
    "tech_stack": "<tech-stack-or-TBD>",
    "entry_point": {
      "type": "cli|api|skill|library|other",
      "trigger": "<command-name or /skillname or endpoint>",
      "activation_steps": ["<step1>", "<step2>"]
    },
    "completed_at": "<timestamp>"
  }
}
```

### 2. Write Spec Draft (MANDATORY)

Write initial spec sections to `$TARGET_DIR/.tasker/spec-draft.md`:

```markdown
# Spec: {Title}

## Goal
{goal from scope}

## Non-goals
{non_goals from scope}

## Done means
{done_means from scope}

## Tech Stack
{tech_stack from scope}

## Installation & Activation
**Entry Point:** {entry_point.trigger from scope}
**Type:** {entry_point.type from scope}

**Activation Steps:**
{entry_point.activation_steps from scope, numbered list}

**Verification:**
<!-- To be filled in during Clarify or Synthesis -->

<!-- Remaining sections will be added by subsequent phases -->
```

**IMPORTANT:** All spec content is built in this file, NOT in conversation context. Read from this file when you need prior spec content.

---

# Phase 2 — Clarify (Ralph Iterative Discovery Loop)

## Purpose
Exhaustively gather requirements via structured questioning.

## Setup

### 1. Initialize Clarify State in state.json (MANDATORY)

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "clarify",
    "completed": ["initialization", "scope"],
    "step": "starting"
  },
  "updated_at": "<timestamp>",
  "clarify": {
    "current_category": "core_requirements",
    "current_round": 1,
    "categories": {
      "core_requirements": { "status": "not_started", "rounds": 0 },
      "users_context": { "status": "not_started", "rounds": 0 },
      "integrations": { "status": "not_started", "rounds": 0 },
      "edge_cases": { "status": "not_started", "rounds": 0 },
      "quality_attributes": { "status": "not_started", "rounds": 0 },
      "existing_patterns": { "status": "not_started", "rounds": 0 },
      "preferences": { "status": "not_started", "rounds": 0 }
    },
    "pending_followups": [],
    "requirements_count": 0,
    "stock_takes_count": 0,
    "started_at": "<timestamp>"
  }
}
```

### 2. Create Discovery File

Create `$TARGET_DIR/.tasker/clarify-session.md`:

```markdown
# Discovery: {TOPIC}
Started: {timestamp}

## Category Status

| Category | Status | Rounds | Notes |
|----------|--------|--------|-------|
| Core requirements | ○ Not Started | 0 | — |
| Users & context | ○ Not Started | 0 | — |
| Integrations | ○ Not Started | 0 | — |
| Edge cases | ○ Not Started | 0 | — |
| Quality attributes | ○ Not Started | 0 | — |
| Existing patterns | ○ Not Started | 0 | — |
| Preferences | ○ Not Started | 0 | — |

## Discovery Rounds

```

### 3. Create Stock-Takes File

Create `$TARGET_DIR/.tasker/stock-takes.md`:

```markdown
# Stock-Takes: {TOPIC}
Started: {timestamp}

This file tracks how the vision evolves as discovery progresses.

---

```

## CRITICAL: Resume Capability

**On resume (after compaction or restart):**
1. Read `$TARGET_DIR/.tasker/state.json` to get `clarify` state
2. Read `$TARGET_DIR/.tasker/clarify-session.md` to get discovery history
3. Resume from `clarify.current_category` and `clarify.current_round`
4. If `clarify.pending_followups` is non-empty, continue follow-up loop first

**DO NOT rely on conversation context for clarify progress. Always read from files.**

## Loop Rules

- **No iteration cap** - Continue until goals are met
- **Category Focus Mode** - Work on ONE category at a time until it's complete or explicitly deferred
- Each iteration:
  1. Read discovery file
  2. Select ONE incomplete category to focus on (priority: Core requirements → Users & context → Integrations → Edge cases → Quality attributes → Existing patterns → Preferences)
  3. Ask **2–4 questions** within that focused category
  4. Get user answers
  5. **Run Follow-up Sub-loop** (see below) - validate and drill down on answers
  6. Only after follow-ups are complete: update discovery file, extract requirements, update category status
  7. Repeat within same category until goal is met OR user says "move on from this category"

- **Clarity Before Progress** - If user response is anything except a direct answer (counter-question, confusion, pushback, tangential), provide clarification FIRST. Do NOT present new questions until prior questions have direct answers.

- **Stop ONLY when:**
  - ALL category goals are met (see checklist), OR
  - User says "enough", "stop", "move on", or similar

## Follow-up Sub-loop (MANDATORY)

After receiving answers to a question round, **DO NOT immediately move to the next round**. First, validate each answer:

### Answer Validation Triggers

For each answer, check if follow-up is required:

| Trigger | Example | Required Follow-up |
|---------|---------|-------------------|
| **Vague quantifier** | "several users", "a few endpoints" | "How many specifically?" |
| **Undefined scope** | "and so on", "etc.", "things like that" | "Can you list all items explicitly?" |
| **Weak commitment** | "probably", "maybe", "I think" | "Is this confirmed or uncertain?" |
| **Missing specifics** | "fast response", "secure" | "What's the specific target? (e.g., <100ms)" |
| **Deferred knowledge** | "I'm not sure", "don't know yet" | "Should we make a default assumption, or is this blocking?" |
| **Contradicts earlier answer** | Conflicts with prior round | "Earlier you said X, now Y. Which is correct?" |

### Sub-loop Process

```
For each answer in current round:
  1. Check against validation triggers
  2. If trigger found:
     a. Add to pending_followups in state.json
     b. Ask ONE follow-up question (not batched)
     c. Wait for response
     d. Remove from pending_followups, re-validate the new response
     e. Repeat until answer is concrete OR user explicitly defers
  3. Only after ALL answers validated → proceed to next round
```

### MANDATORY: Persist Follow-up State

Before asking a follow-up question, update `state.json`:
```json
{
  "clarify": {
    "pending_followups": [
      {
        "question_id": "Q3.2",
        "original_answer": "<user's vague answer>",
        "trigger": "vague_quantifier",
        "followup_question": "<the follow-up question being asked>"
      }
    ]
  }
}
```

After receiving follow-up response, remove from `pending_followups` and update the round in `clarify-session.md`.

### Follow-up Question Format

Use AskUserQuestion with context from the original answer:

```json
{
  "question": "You mentioned '{user_quote}'. {specific_follow_up_question}",
  "header": "Clarify",
  "options": [
    {"label": "Specify", "description": "I'll provide a specific answer"},
    {"label": "Not critical", "description": "This detail isn't important for the spec"},
    {"label": "Defer", "description": "I don't know yet, note as open question"}
  ]
}
```

### Handling Non-Direct Responses (MANDATORY)

If the user's response is **anything other than a direct answer**, assume clarification is required. Do NOT present new questions until the original question is resolved.

| Response Type | Example | Required Action |
|---------------|---------|-----------------|
| **Counter-question** | "What do you mean by X?" | Answer their question, then re-ask yours |
| **Confusion** | "I'm not sure what you're asking" | Rephrase the question with more context |
| **Pushback** | "Why do you need to know that?" | Explain why this matters for the spec |
| **Tangential** | Talks about something else | Acknowledge, then redirect to the question |
| **Partial answer** | Answers part, ignores rest | Note the partial, ask about the unanswered part |
| **Meta-comment** | "This is getting detailed" | Acknowledge, offer to simplify or defer |

**Process:**
```
1. Detect non-direct response
2. Address the user's concern/question FIRST
3. Only after clarity achieved → re-present the original question (or confirm it's now answered)
4. Do NOT batch new questions until all prior questions have direct answers
```

**Example:**
```
Agent: "What authentication method should users use?"
User: "What options are there?"

[NON-DIRECT: User asked a counter-question]

Agent: "Common options are: (1) Email/password, (2) OAuth (Google, GitHub),
       (3) Magic link, (4) SSO/SAML. Which fits your use case?"
User: "Email/password for now, maybe OAuth later."

[NOW DIRECT: Can proceed]
```

### When NOT to Follow Up

- User explicitly says "that's all I know" or "let's move on"
- The answer is already concrete and specific
- The detail is genuinely non-blocking (implementation detail, not spec-level)
- You've already asked 2 follow-ups on the same answer (avoid interrogation)

### Example Interaction

```
Agent: "What integrations are required?"
User: "We need to connect to a few external services and maybe some APIs."

[FOLLOW-UP REQUIRED: "a few" is vague, "maybe" is weak commitment]

Agent: "You mentioned 'a few external services'. Can you list all the external systems this will integrate with?"
User: "Stripe for payments, SendGrid for email, and our internal user service."

[ANSWER NOW CONCRETE: specific services named]

Agent: "You said 'maybe some APIs'. Are there additional API integrations beyond Stripe, SendGrid, and the user service?"
User: "No, that's all."

[CATEGORY GOAL PROGRESS: Integrations now has concrete list]
```

## Category Checklist (Goal-Driven Coverage)

Each category has concrete "done" criteria. Track completion in the discovery file.

| Category | Goal (Done When) |
|----------|------------------|
| **Core requirements** | Primary workflows enumerated with inputs, outputs, and happy path steps |
| **Users & context** | User roles identified, expertise levels known, access patterns clear |
| **Integrations / boundaries** | All external systems named, data flows mapped, API contracts sketched |
| **Edge cases / failures** | Error handling defined for each workflow step, retry/fallback behavior specified |
| **Quality attributes** | Performance targets have numbers (or explicit "not critical"), security requirements stated |
| **Existing patterns** | Relevant prior art identified OR confirmed none exists, conventions to follow listed |
| **Preferences / constraints** | Tech stack decided, deployment target known, timeline/resource constraints stated |

### Tracking Format

Update discovery file with completion status:

```markdown
## Category Status

| Category | Status | Notes |
|----------|--------|-------|
| Core requirements | ✓ Complete | 3 workflows defined |
| Users & context | ✓ Complete | 2 roles: admin, user |
| Integrations | ⋯ In Progress | DB confirmed, auth TBD |
| Edge cases | ○ Not Started | — |
| Quality attributes | ○ Not Started | — |
| Existing patterns | ✓ Complete | Follow auth module pattern |
| Preferences | ⋯ In Progress | Python confirmed, framework TBD |
```

### Completion Criteria

A category is **complete** when:
1. The goal condition is satisfied (see table above)
2. User has confirmed or provided the information
3. **All answers have passed follow-up validation** (no vague quantifiers, no weak commitments, no undefined scope)
4. No obvious follow-up questions remain for that category
5. User has explicitly confirmed or the agent has verified understanding

**Do NOT mark complete** if:
- User said "I don't know" without a fallback decision
- Information is vague (e.g., "fast" instead of "<100ms")
- Dependencies on other categories are unresolved
- **Follow-up validation has not been run on all answers**
- **Any answer contains unresolved triggers** (vague quantifiers, weak commitments, etc.)

### Category Transition Rules

Before moving to a new category:
1. **Summarize** what was learned in the current category
2. **Confirm** with user: "I've captured X, Y, Z for [category]. Does that cover everything, or is there more?"
3. **Run Stock-Take** (see below)
4. **Only then** move to the next incomplete category

This prevents the feeling of being "rushed" through categories.

## Stock-Taking (Big Picture Synthesis)

### Purpose

As questions are answered and categories complete, periodically synthesize the "big picture" - what's emerging, the shape of the vision. This helps users see how their answers are building toward something coherent and provides calibration moments.

### Trigger

Stock-take is triggered **after each category completes** (before transitioning to the next category). This creates a natural rhythm of ~5-7 stock-takes during Phase 2.

### Content

A stock-take is NOT a list of answers. It's a **synthesis of meaning** - what's taking shape:

1. **What we're building** (1-2 sentences, evolving as understanding deepens)
2. **Key constraints/boundaries** that have emerged from answers
3. **The shape becoming visible** (patterns, tensions, tradeoffs surfacing)
4. **Direction check** - light confirmation the vision still feels right

### Format

```markdown
**Taking stock** (after {category_name}):

{1-3 sentence synthesis of what's emerging - not a summary of answers, but the picture forming}

{Any notable patterns, tensions, or tradeoffs becoming visible}

Does this still capture where we're heading?
```

### Example

After completing "Integrations" category:

> **Taking stock** (after Integrations):
>
> We're building a CLI skill system where specs drive task decomposition. The emphasis is on preventing incomplete handoffs - every behavior must trace back to stated requirements. The system is self-contained except for Git (for state persistence) and Claude Code (as the execution runtime).
>
> There's tension between thoroughness and workflow friction that keeps surfacing - users want comprehensive specs but not interrogation.
>
> Does this still capture where we're heading?

### Tone

- **Reflective**, not interrogative
- **Synthesizing**, not summarizing
- **Calibrating**, not gate-checking

The question at the end is light - "Does this still feel right?" not "Please confirm items 1-7."

### Process

After category completion:

1. **Read accumulated state** from `spec-draft.md` (scope), `clarify-session.md` (discovery so far)
2. **Synthesize** the emerging picture (not regurgitate answers)
3. **Present** the stock-take to user
4. **Listen** for any course correction or "that's not quite right"
5. **Append** to `$TARGET_DIR/.tasker/stock-takes.md`
6. **Update** `state.json` with `stock_takes_count`

### Stock-Takes File Format

Append each stock-take to `$TARGET_DIR/.tasker/stock-takes.md`:

```markdown
---

## Stock-Take {N} — After {Category Name}
*{timestamp}*

{The synthesis content}

**User response:** {confirmed | adjusted: brief note}

---
```

### State Update

After each stock-take, update `state.json`:
```json
{
  "clarify": {
    "stock_takes_count": N
  },
  "updated_at": "<timestamp>"
}
```

### When NOT to Stock-Take

- **Early exit**: If user says "move on" mid-category, skip stock-take for that category
- **Minor category**: If a category yielded very little new information, stock-take can be brief or combined with next
- **User impatience**: If user explicitly wants to skip calibration, respect that

## AskUserQuestion Format

### Primary Questions (Category-Focused)

Use AskUserQuestion with 2-4 questions per iteration, **all within the same category**:

```
questions:
  - question: "How should the system handle [specific scenario]?"
    header: "Edge case"  # Keep headers consistent within a round
    options:
      - label: "Option A"
        description: "Description of approach A"
      - label: "Option B"
        description: "Description of approach B"
    multiSelect: false
```

**IMPORTANT:** Do NOT mix categories in a single question batch. If you're asking about "Edge cases", all 2-4 questions should be about edge cases.

### Follow-up Questions (Single Question)

For follow-ups during the validation sub-loop, ask **ONE question at a time**:

```
questions:
  - question: "You mentioned '{user_quote}'. Can you be more specific about X?"
    header: "Clarify"
    options:
      - label: "Specify"
        description: "I'll provide details"
      - label: "Not critical"
        description: "This isn't spec-relevant"
      - label: "Defer"
        description: "Note as open question"
    multiSelect: false
```

### Open-ended Questions

For open-ended questions, use free-form with context:
```
questions:
  - question: "What integrations are required?"
    header: "Integrations"
    options:
      - label: "REST API"
        description: "Standard HTTP/JSON endpoints"
      - label: "Database direct"
        description: "Direct database access"
      - label: "Message queue"
        description: "Async via queue (Kafka, RabbitMQ, etc.)"
    multiSelect: true
```

## Updating Discovery File AND State (MANDATORY)

After each Q&A round AND its follow-ups are complete:

### 1. Append to Discovery File

Append to `$TARGET_DIR/.tasker/clarify-session.md`:

```markdown
### Round N — [Category Name]

**Questions:**
1. [Question text]
2. [Question text]

**Answers:**
1. [User's answer]
2. [User's answer]

**Follow-ups:**
- Q1 follow-up: "[follow-up question]" → "[user response]"
- Q2: No follow-up needed (answer was specific)

**Requirements Discovered:**
- REQ-NNN: [Req 1]
- REQ-NNN: [Req 2]

**Category Status:** [✓ Complete | ⋯ In Progress | User deferred]
```

### 2. Update State (MANDATORY after every round)

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "step": "round_N_complete"
  },
  "updated_at": "<timestamp>",
  "clarify": {
    "current_category": "<category>",
    "current_round": N+1,
    "categories": {
      "<category>": { "status": "in_progress|complete", "rounds": N }
    },
    "pending_followups": [],
    "requirements_count": <total REQ count>
  }
}
```

### 3. Update Category Status Table

Also update the Category Status table at the top of `clarify-session.md` to reflect current state.

**NOTE:** Do NOT proceed to next round until both files are updated. This ensures resumability.

## Completion Signal

When ALL category goals are met:

1. Verify all categories show "✓ Complete" in the status table
2. Confirm no blocking questions remain
3. Update state.json:
```json
{
  "phase": {
    "current": "clarify",
    "completed": ["initialization", "scope"],
    "step": "complete"
  },
  "updated_at": "<timestamp>",
  "clarify": {
    "status": "complete",
    "completed_at": "<timestamp>",
    "categories": { /* all marked complete */ },
    "requirements_count": <final count>
  }
}
```
4. Output:
```
<promise>CLARIFIED</promise>
```

**If user requests early exit:** Accept it, mark incomplete categories in state.json with `status: "deferred"`, and note in discovery file for Phase 3 to flag as assumptions.

---

# Phase 3 — Synthesis (Derived, Not Asked)

## Purpose
Derive structured requirements AND capabilities from discovery. **No new information introduced here.**

This phase produces TWO outputs:
1. **Spec sections** (human-readable) - Workflows, invariants, interfaces
2. **Capability map** (machine-readable) - For `/plan` to consume

## CRITICAL: State-Driven, Not Context-Driven

**On entry to Phase 3:**
1. Read `$TARGET_DIR/.tasker/state.json` to confirm `clarify.status == "complete"`
2. Read `$TARGET_DIR/.tasker/clarify-session.md` for ALL discovery content
3. Read `$TARGET_DIR/.tasker/spec-draft.md` for existing spec sections (Goal, Non-goals, etc.)

**DO NOT rely on conversation context for discovery content. Read from files.**

## Initialize Synthesis State

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "synthesis",
    "completed": ["initialization", "scope", "clarify"],
    "step": "starting"
  },
  "updated_at": "<timestamp>",
  "synthesis": {
    "status": "in_progress",
    "spec_sections": {
      "workflows": false,
      "invariants": false,
      "interfaces": false,
      "open_questions": false
    },
    "capability_map": {
      "domains_count": 0,
      "capabilities_count": 0,
      "behaviors_count": 0,
      "steel_thread_identified": false
    },
    "fsm": {
      "machines_count": 0,
      "states_count": 0,
      "transitions_count": 0,
      "invariants_validated": false
    }
  }
}
```

## Process

1. Read `$TARGET_DIR/.tasker/clarify-session.md` completely
2. Extract and organize into spec sections (update spec-draft.md after each)
3. Decompose into capabilities using I.P.S.O.A. taxonomy
4. Everything must trace to a specific discovery answer

---

## Part A: Spec Sections

### Workflows
Numbered steps with variants and failures:
```markdown
## Workflows

### 1. [Primary Workflow Name]
1. User initiates X
2. System validates Y
3. System performs Z
4. System returns result

**Variants:**
- If [condition], then [alternative flow]

**Failures:**
- If [error], then [error handling]

**Postconditions:**
- [State after completion]
```

### Invariants
Bulleted rules that must ALWAYS hold:
```markdown
## Invariants
- [Rule that must never be violated]
- [Another invariant]
```

### Interfaces
Only if a boundary exists:
```markdown
## Interfaces
- [Interface description]

(or "No new/changed interfaces" if none)
```

### Open Questions
Classified by blocking status:
```markdown
## Open Questions

### Blocking
- [Question that affects workflows/invariants/interfaces]

### Non-blocking
- [Question about internal preferences only]
```

### Part A Output: Update Files (MANDATORY)

After synthesizing each spec section:

**1. Append section to `$TARGET_DIR/.tasker/spec-draft.md`:**
```markdown
## Workflows
[Synthesized workflows content]

## Invariants
[Synthesized invariants content]

## Interfaces
[Synthesized interfaces content]

## Open Questions
[Synthesized open questions content]
```

**2. Update state.json after EACH section:**
```json
{
  "synthesis": {
    "spec_sections": {
      "workflows": true,
      "invariants": true,
      "interfaces": false,
      "open_questions": false
    }
  },
  "updated_at": "<timestamp>"
}
```

---

## Part A.5: Behavior Model Compilation (FSM)

After synthesizing Workflows, Invariants, and Interfaces, compile the Behavior Model (state machine).

### Purpose

The FSM serves two purposes:
1. **QA during implementation** - Shapes acceptance criteria, enables transition/guard coverage verification
2. **Documentation** - Human-readable diagrams for ongoing system understanding

### CRITICAL INVARIANT: Canonical Truth

> **FSM JSON is canonical; Mermaid is generated. `/plan` and `/execute` must fail if required transitions and invariants lack coverage evidence.**

- **Canonical artifacts**: `*.states.json`, `*.transitions.json`, `index.json`
- **Derived artifacts**: `*.mmd` (Mermaid diagrams) - generated ONLY from canonical JSON
- **NEVER** manually edit `.mmd` files - regenerate from JSON using `fsm-mermaid.py`
- If Mermaid is ever edited manually, the system loses machine trust

### Compilation Steps

1. **Identify Steel Thread Flow**: The primary end-to-end workflow
2. **Derive States**: Convert workflow steps to business states
   - Initial state from workflow trigger
   - Normal states from step postconditions
   - Success terminal from workflow completion
   - Failure terminals from failure clauses
3. **Derive Transitions**: Convert step sequences, variants, and failures
   - Happy path: step N → step N+1
   - Variants: conditional branches with guards
   - Failures: error transitions to failure states
4. **Link Guards to Invariants**: Map spec invariants to transition guards
5. **Validate Completeness**: Run I1-I6 checks (see below)
6. **Resolve Ambiguity**: Use AskUserQuestion for any gaps

### Completeness Invariants

The FSM MUST satisfy these invariants:

| ID | Invariant | Check |
|----|-----------|-------|
| I1 | Steel Thread FSM mandatory | At least one machine for primary workflow |
| I2 | Behavior-first | No architecture dependencies required |
| I3 | Completeness | Initial state, terminals, no dead ends |
| I4 | Guard-Invariant linkage | Every guard links to an invariant ID |
| I5 | No silent ambiguity | Vague terms resolved or flagged as Open Questions |
| I6 | Precondition reachability | If initial transition requires external trigger (e.g., "user invokes X"), the preconditions for that trigger must be specified in the spec |

**I6 Detailed Check:**
If the first transition's trigger describes user invocation (e.g., "user runs /command", "user invokes skill"):
1. Check if spec has "Installation & Activation" section
2. Verify the activation mechanism makes the trigger possible
3. If missing, flag as W8 weakness (missing activation requirements)

Example I6 failure:
- FSM starts: `Idle --[user invokes /kx]--> Running`
- Spec has NO section explaining how `/kx` becomes available
- **I6 FAILS**: "Precondition for initial transition 'user invokes /kx' not reachable - no activation mechanism specified"

### Complexity Triggers (Splitting Rules)

Create additional machines based on **structural heuristics**, not just state count:

**State Count Triggers:**
- Steel Thread exceeds 12 states → split into domain-level sub-machines
- Any machine exceeds 20 states → mandatory split

**Structural Triggers (split even with fewer states):**
- **Divergent user journeys**: Two or more distinct journeys that share only an initial prefix, then branch into unrelated flows → separate machines for each journey
- **Unrelated failure clusters**: Multiple failure states that handle different categories of errors (e.g., validation errors vs. system errors vs. business rule violations) → group related failures into their own machines
- **Mixed abstraction levels**: Machine combines business lifecycle states (e.g., Order: Created → Paid → Shipped) with UI microstates (e.g., Modal: Open → Editing → Validating) → separate business lifecycle from UI state machines
- **Cross-boundary workflows**: Workflow that spans multiple bounded contexts or domains → domain-level machine for each context

**Hierarchy Guidelines:**
- `steel_thread` level: Primary end-to-end flow
- `domain` level: Sub-flows within a bounded context
- `entity` level: Lifecycle states for a specific entity

### Ambiguity Resolution

If the compiler detects ambiguous workflow language, use AskUserQuestion:

```json
{
  "question": "The workflow step '{step}' has ambiguous outcome. What business state results?",
  "header": "FSM State",
  "options": [
    {"label": "Define state", "description": "I'll provide the state name"},
    {"label": "Same as previous", "description": "Remains in current state"},
    {"label": "Terminal success", "description": "Workflow completes successfully"},
    {"label": "Terminal failure", "description": "Workflow fails with error"}
  ]
}
```

### FSM Working Files (Written Incrementally)

During synthesis, write FSM drafts to `$TARGET_DIR/.tasker/fsm-draft/`:
- `index.json` - Machine list, hierarchy, primary machine
- `steel-thread.states.json` - State definitions (S1, S2, ...)
- `steel-thread.transitions.json` - Transition definitions (TR1, TR2, ...)
- `steel-thread.notes.md` - Ambiguity resolutions and rationale

**Update state.json after each FSM file:**
```json
{
  "synthesis": {
    "fsm": {
      "machines_count": 1,
      "states_count": 8,
      "transitions_count": 12,
      "files_written": ["index.json", "steel-thread.states.json"],
      "invariants_validated": false
    }
  },
  "updated_at": "<timestamp>"
}
```

### FSM Final Output Structure

Final FSM artifacts are exported to `{TARGET}/docs/state-machines/<slug>/` in Phase 8:
- `index.json` - Machine list, hierarchy, primary machine
- `steel-thread.states.json` - State definitions (S1, S2, ...)
- `steel-thread.transitions.json` - Transition definitions (TR1, TR2, ...)
- `steel-thread.mmd` - Mermaid stateDiagram-v2 for visualization (DERIVED from JSON)
- `steel-thread.notes.md` - Ambiguity resolutions and rationale

### ID Conventions (FSM-specific)

- Machines: `M1`, `M2`, `M3`...
- States: `S1`, `S2`, `S3`...
- Transitions: `TR1`, `TR2`, `TR3`...

### Traceability (Spec Provenance - MANDATORY)

Every state and transition MUST have a `spec_ref` pointing to the specific workflow step, variant, or failure that defined it. This prevents "FSM hallucination" where states/transitions are invented without spec basis.

**Required for each state:**
- `spec_ref.quote` - Verbatim text from the spec that defines this state
- `spec_ref.location` - Section reference (e.g., "Workflow 1, Step 3")

**Required for each transition:**
- `spec_ref.quote` - Verbatim text from the spec that defines this transition
- `spec_ref.location` - Section reference (e.g., "Workflow 1, Variant 2")

**If no spec text exists for an element:**
1. The element should NOT be created (likely FSM hallucination)
2. Or, use AskUserQuestion to get clarification and document the decision

---

## Part B: Capability Extraction

Extract capabilities from the synthesized workflows using **I.P.S.O.A. decomposition**.

### I.P.S.O.A. Behavior Taxonomy

For each capability, identify behaviors by type:

| Type | Description | Examples |
|------|-------------|----------|
| **Input** | Validation, parsing, authentication | Validate email format, parse JSON body |
| **Process** | Calculations, decisions, transformations | Calculate total, apply discount rules |
| **State** | Database reads/writes, cache operations | Save order, fetch user profile |
| **Output** | Responses, events, notifications | Return JSON, emit event, send email |
| **Activation** | Registration, installation, deployment | Register skill, deploy endpoint, write config |

### Activation Behaviors

If the spec describes user invocation (e.g., "user runs /command"), extract activation behaviors:
- **Registration**: Skill/plugin registration with runtime
- **Installation**: CLI or package installation steps
- **Deployment**: API endpoint or service deployment
- **Configuration**: Config files or environment setup

**Missing activation = coverage gap.** If spec says "user invokes X" but doesn't specify how X becomes available, add to `coverage.gaps`.

### Domain Grouping

Group related capabilities into domains:
- **Authentication** - Login, logout, session management
- **User Management** - Profile, preferences, settings
- **Core Feature** - The primary business capability
- etc.

### Steel Thread Identification

Identify the **steel thread** - the minimal end-to-end flow that proves the system works:
- Mark one flow as `is_steel_thread: true`
- This becomes the critical path for Phase 1 implementation

### Capability Map Working File

During synthesis, write capability map draft to `$TARGET_DIR/.tasker/capability-map-draft.json`.

**Update state.json as you build the map:**
```json
{
  "synthesis": {
    "capability_map": {
      "domains_count": 3,
      "capabilities_count": 8,
      "behaviors_count": 24,
      "steel_thread_identified": true,
      "draft_written": true
    }
  },
  "updated_at": "<timestamp>"
}
```

### Capability Map Final Output

In Phase 8, write final to `{TARGET}/docs/specs/<slug>.capabilities.json`:

```json
{
  "version": "1.0",
  "spec_checksum": "<first 16 chars of SHA256 of spec>",

  "domains": [
    {
      "id": "D1",
      "name": "Authentication",
      "description": "User identity and access",
      "capabilities": [
        {
          "id": "C1",
          "name": "User Login",
          "discovery_ref": "Round 3, Q2: User confirmed email/password auth",
          "behaviors": [
            {"id": "B1", "name": "ValidateCredentials", "type": "input", "description": "Check email/password format"},
            {"id": "B2", "name": "VerifyPassword", "type": "process", "description": "Compare hash"},
            {"id": "B3", "name": "CreateSession", "type": "state", "description": "Store session"},
            {"id": "B4", "name": "ReturnToken", "type": "output", "description": "JWT response"}
          ]
        }
      ]
    }
  ],

  "flows": [
    {
      "id": "F1",
      "name": "Login Flow",
      "is_steel_thread": true,
      "steps": [
        {"order": 1, "behavior_id": "B1", "description": "Validate input"},
        {"order": 2, "behavior_id": "B2", "description": "Check password"},
        {"order": 3, "behavior_id": "B3", "description": "Create session"},
        {"order": 4, "behavior_id": "B4", "description": "Return JWT"}
      ]
    }
  ],

  "invariants": [
    {"id": "I1", "description": "Passwords must never be logged", "discovery_ref": "Round 5, Q1"}
  ],

  "coverage": {
    "total_requirements": 15,
    "covered_requirements": 15,
    "gaps": []
  }
}
```

### ID Conventions

- Domains: `D1`, `D2`, `D3`...
- Capabilities: `C1`, `C2`, `C3`...
- Behaviors: `B1`, `B2`, `B3`...
- Flows: `F1`, `F2`, `F3`...
- Invariants: `I1`, `I2`, `I3`...

### Traceability

Every capability and invariant MUST have a `discovery_ref` pointing to the specific round and question in `$TARGET_DIR/.tasker/clarify-session.md` that established it.

## Synthesis Complete: Update State

After all synthesis outputs are complete, update state.json:
```json
{
  "phase": {
    "current": "synthesis",
    "completed": ["initialization", "scope", "clarify"],
    "step": "complete"
  },
  "updated_at": "<timestamp>",
  "synthesis": {
    "status": "complete",
    "completed_at": "<timestamp>",
    "spec_sections": { "workflows": true, "invariants": true, "interfaces": true, "open_questions": true },
    "capability_map": { "domains_count": N, "capabilities_count": N, "behaviors_count": N, "steel_thread_identified": true, "draft_written": true },
    "fsm": { "machines_count": N, "states_count": N, "transitions_count": N, "invariants_validated": true }
  }
}
```

## CRITICAL: Resume From Synthesis

**On resume (after compaction or restart):**
1. Read `$TARGET_DIR/.tasker/state.json` to get `synthesis` state
2. If `synthesis.spec_sections` shows incomplete sections, read `spec-draft.md` and continue
3. If `synthesis.capability_map.draft_written` is false, continue building from `capability-map-draft.json`
4. If `synthesis.fsm.invariants_validated` is false, continue FSM work from `fsm-draft/`

---

# Phase 4 — Architecture Sketch

## Rule
Architecture MUST come **AFTER** workflows, invariants, interfaces.

## Initialize Architecture State

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "architecture",
    "completed": ["initialization", "scope", "clarify", "synthesis"],
    "step": "starting"
  },
  "updated_at": "<timestamp>",
  "architecture": {
    "status": "in_progress",
    "user_provided": false,
    "agent_proposed": false
  }
}
```

## CRITICAL: Read Prior State

**On entry:**
1. Read `$TARGET_DIR/.tasker/spec-draft.md` to understand synthesized workflows
2. Architecture sketch should align with the workflows defined

## Process

Use AskUserQuestion to either:

**Option A: Ask for sketch**
```
questions:
  - question: "Can you provide a brief architecture sketch for this feature?"
    header: "Architecture"
    options:
      - label: "I'll describe it"
        description: "User provides architecture overview"
      - label: "Propose one"
        description: "Agent proposes architecture for review"
```

**Option B: Propose and confirm**
Present a brief sketch and ask for confirmation/edits.

## Output

### 1. Update spec-draft.md

Append **Architecture sketch** section to `$TARGET_DIR/.tasker/spec-draft.md`:
```markdown
## Architecture sketch
- **Components touched:** [list]
- **Responsibilities:** [brief description]
- **Failure handling:** [brief description]
```

**Keep this SHORT. No essays.**

### 2. Update State

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "step": "complete"
  },
  "updated_at": "<timestamp>",
  "architecture": {
    "status": "complete",
    "completed_at": "<timestamp>",
    "user_provided": true|false,
    "agent_proposed": true|false
  }
}
```

---

# Phase 5 — Decisions & ADRs

## Initialize Decisions State

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "decisions",
    "completed": ["initialization", "scope", "clarify", "synthesis", "architecture"],
    "step": "starting"
  },
  "updated_at": "<timestamp>",
  "decisions": {
    "status": "in_progress",
    "count": 0,
    "pending": 0
  }
}
```

## CRITICAL: Read Prior State

**On entry:**
1. Read `$TARGET_DIR/.tasker/spec-draft.md` to identify decision points from workflows/invariants
2. Read `$TARGET_DIR/.tasker/clarify-session.md` for context on requirements

## ADR Trigger

**Create ADR if ANY of these are true:**
- Hard to reverse
- Reusable standard
- Tradeoff-heavy
- Cross-cutting
- NFR-impacting

**If none apply → record decision in spec only.**

## Decision Facilitation Rules

### FACILITATE a decision ONLY IF ALL are true:
1. ADR-worthy (meets trigger above)
2. Not already decided (no existing ADR, no explicit user preference)
3. Blocking workflows, invariants, or interfaces

### DO NOT FACILITATE if ANY are true:
- Already decided
- Local / reversible / implementation detail
- Non-blocking
- User not ready to decide
- Too many options (>3)
- Premature (behavior not defined yet)

## Facilitation Format

If facilitation is allowed:

```
questions:
  - question: "How should we approach [decision topic]?"
    header: "Decision"
    options:
      - label: "Option A: [Name]"
        description: "Consequences: [1], [2]"
      - label: "Option B: [Name]"
        description: "Consequences: [1], [2]"
      - label: "Need more info"
        description: "Defer decision, add to Open Questions"
```

## Outcomes

- **User chooses option** → Write decision to spec-draft.md + create ADR (Accepted)
- **User says "need more info"** → Add as Blocking Open Question (no ADR yet)

**Update state.json after each decision:**
```json
{
  "decisions": {
    "count": 2,
    "pending": 1
  },
  "updated_at": "<timestamp>"
}
```

### Decision Registry

Write decision index to `$TARGET_DIR/.tasker/decisions.json`:
```json
{
  "decisions": [
    { "id": "DEC-001", "title": "Authentication method", "adr": "ADR-0001-auth-method.md" },
    { "id": "DEC-002", "title": "Database choice", "adr": "ADR-0002-database-choice.md" },
    { "id": "DEC-003", "title": "Error handling strategy", "adr": null }
  ]
}
```

- `adr` is the filename if ADR-worthy, `null` if inline decision only
- ADR files contain full decision context and rationale

**Usage pattern:** Always consult `decisions.json` first to find relevant decisions by title. Only read a specific ADR file when you need the full details. Never scan `adrs-draft/` directory to discover what decisions exist.

### ADR Working Files

Write ADR drafts to `$TARGET_DIR/.tasker/adrs-draft/`:
- `ADR-0001-auth-method.md`
- `ADR-0002-database-choice.md`

Final ADRs are exported to `{TARGET}/docs/adrs/` in Phase 8.

## ADR Template

Write ADRs to `{TARGET}/docs/adrs/ADR-####-<slug>.md`:

```markdown
# ADR-####: {Title}

**Status:** Accepted
**Date:** {YYYY-MM-DD}

## Applies To
- [Spec: Feature A](../specs/feature-a.md)
- [Spec: Feature B](../specs/feature-b.md)

## Context
[Why this decision was needed - reference specific discovery round if applicable]

## Decision
[What was decided]

## Alternatives Considered
| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| [Alt 1] | ... | ... | ... |
| [Alt 2] | ... | ... | ... |

## Consequences
- [Consequence 1]
- [Consequence 2]

## Related
- Supersedes: (none | ADR-XXXX)
- Related ADRs: (none | ADR-XXXX, ADR-YYYY)
```

**ADR Rules:**
- ADRs are **immutable** once Accepted
- Changes require a **new ADR** that supersedes the old
- ADRs can apply to multiple specs (many-to-many relationship)
- When creating a new spec that uses an existing ADR, update the ADR's "Applies To" section

## Decisions Complete: Update State

After all decisions are resolved, update state.json:
```json
{
  "phase": {
    "step": "complete"
  },
  "updated_at": "<timestamp>",
  "decisions": {
    "status": "complete",
    "completed_at": "<timestamp>",
    "count": 3,
    "pending": 0
  }
}
```

Also append Decisions section to `$TARGET_DIR/.tasker/spec-draft.md`.

---

# Phase 6 — Handoff-Ready Gate

## CRITICAL: State-Driven Gate Check

**On entry to Phase 6:**
1. Read `$TARGET_DIR/.tasker/state.json` to verify all prior phases complete
2. Read `$TARGET_DIR/.tasker/spec-draft.md` to verify all sections exist
3. Read `$TARGET_DIR/.tasker/fsm-draft/` to verify FSM compiled
4. Read `$TARGET_DIR/.tasker/capability-map-draft.json` to verify capability map exists

**DO NOT rely on conversation context. All gate checks use persisted files.**

Update state.json:
```json
{
  "phase": {
    "current": "gate",
    "completed": ["initialization", "scope", "clarify", "synthesis", "architecture", "decisions"],
    "step": "checking"
  },
  "updated_at": "<timestamp>"
}
```

## Preliminary Check (ALL must pass)

| Check | Requirement | Verify By |
|-------|-------------|-----------|
| Phases complete | All phases 1-5 completed in order | `state.json` phase.completed array |
| No blocking questions | Zero Blocking Open Questions | `spec-draft.md` Open Questions section |
| Interfaces present | Interfaces section exists (even if "none") | `spec-draft.md` |
| Decisions present | Decisions section exists | `spec-draft.md` |
| Workflows defined | At least one workflow with variants/failures | `spec-draft.md` |
| Invariants stated | At least one invariant | `spec-draft.md` |
| FSM compiled | Steel Thread FSM compiled with I1-I6 passing | `fsm-draft/index.json` |

## Spec Completeness Check (Checklist C1-C11)

Run the checklist verification against the current spec draft:

```bash
tasker spec checklist /tmp/claude/spec-draft.md
```

This verifies the spec contains all expected sections:

| Category | Critical Items (must pass) |
|----------|---------------------------|
| C2: Data Model | Tables defined, fields typed, constraints stated |
| C3: API | Endpoints listed, request/response schemas, auth requirements |
| C4: Behavior | Observable behaviors, business rules |
| C7: Security | Authentication mechanism, authorization rules |

### Handling Checklist Gaps

For **critical missing items** (marked with *):

1. If the spec SHOULD have this content → return to Phase 2 (Clarify) to gather requirements
2. If the spec legitimately doesn't need this → document as N/A with rationale

Example checklist failure:
```
## Gate FAILED - Incomplete Spec

Checklist verification found critical gaps:

- [✗] C2.4*: Constraints stated (UNIQUE, CHECK, FK)?
  → Data model section exists but no constraints defined

- [✗] C3.2*: Request schemas defined?
  → API endpoints listed but request bodies not specified

Action: Return to Phase 2 to clarify data constraints and API request formats.
```

## Gate Result: Update State

### If Gate PASSES:
```json
{
  "phase": {
    "current": "gate",
    "step": "passed"
  },
  "updated_at": "<timestamp>"
}
```

### If Gate FAILS:

Update state.json with blockers:
```json
{
  "phase": {
    "current": "gate",
    "step": "failed"
  },
  "updated_at": "<timestamp>",
  "gate_blockers": [
    { "type": "blocking_question", "detail": "Rate limiting across tenants" },
    { "type": "missing_section", "detail": "Interfaces" },
    { "type": "checklist_gap", "detail": "C2.4: No database constraints" }
  ]
}
```

1. List exact blockers
2. **STOP** - do not proceed to spec review
3. Tell user what must be resolved

Example:
```
## Gate FAILED

Cannot proceed. The following must be resolved:

1. **Blocking Open Questions:**
   - How should rate limiting work across tenants?
   - What is the retry policy for failed webhooks?

2. **Missing Sections:**
   - Interfaces section not present

3. **Checklist Gaps (Critical):**
   - C2.4: No database constraints defined
   - C3.2: API request schemas missing
```

---

# Phase 7 — Spec Review (MANDATORY)

## Purpose
Run automated weakness detection to catch issues before export. This is the final quality gate.

## Initialize Review State

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "review",
    "completed": ["initialization", "scope", "clarify", "synthesis", "architecture", "decisions", "gate"],
    "step": "starting"
  },
  "updated_at": "<timestamp>",
  "review": {
    "status": "in_progress",
    "weaknesses_found": 0,
    "weaknesses_resolved": 0,
    "critical_remaining": 0
  }
}
```

## CRITICAL: Read From Files

**On entry to Phase 7:**
1. The spec draft is already in `$TARGET_DIR/.tasker/spec-draft.md` - use this file
2. Do NOT build spec from conversation context

## Process

### Step 1: Copy Spec Draft for Analysis

The spec draft already exists at `$TARGET_DIR/.tasker/spec-draft.md`. Copy to temp for analysis:

```bash
cp "$TARGET_DIR/.tasker/spec-draft.md" /tmp/claude/spec-draft.md
```

### Step 2: Run Weakness Detection

```bash
tasker spec review /tmp/claude/spec-draft.md
```

This detects:
- **W1: Non-behavioral requirements** - DDL/schema not stated as behavior
- **W2: Implicit requirements** - Constraints assumed but not explicit
- **W3: Cross-cutting concerns** - Config, observability, lifecycle
- **W4: Missing acceptance criteria** - Qualitative terms without metrics
- **W5: Fragmented requirements** - Cross-references needing consolidation
- **W6: Contradictions** - Conflicting statements
- **W7: Ambiguity** - Vague quantifiers, undefined scope, weak requirements, passive voice
- **W8: Missing activation requirements** - Spec describes invocation without specifying how to make it invocable (e.g., "user runs /command" without defining how the command becomes available)
- **CK-*: Checklist gaps** - Critical missing content from C1-C11 categories

W7 Ambiguity patterns include:
- Vague quantifiers ("some", "many", "several")
- Undefined scope ("etc.", "and so on")
- Vague conditionals ("if applicable", "when appropriate")
- Weak requirements ("may", "might", "could")
- Passive voice hiding actor ("is handled", "will be processed")
- Vague timing ("quickly", "soon", "eventually")
- Subjective qualifiers ("reasonable", "appropriate")
- Unquantified limits ("large", "fast", "slow")

### Step 3: Handle Critical Weaknesses

For **CRITICAL** weaknesses (W1, W6, W7 with weak requirements), engage user:

#### W1: Non-Behavioral Requirements

```json
{
  "question": "The spec contains DDL/schema that isn't stated as behavioral requirement: '{spec_quote}'. How should this be treated?",
  "header": "DDL Mandate",
  "options": [
    {"label": "DB-level required", "description": "MUST be implemented as database-level constraint"},
    {"label": "App-layer OK", "description": "Application-layer validation is sufficient"},
    {"label": "Documentation only", "description": "This is reference documentation, not a requirement"}
  ]
}
```

#### W6: Contradictions

```json
{
  "question": "Conflicting statements found: {description}. Which is authoritative?",
  "header": "Conflict",
  "options": [
    {"label": "First statement", "description": "{first_quote}"},
    {"label": "Second statement", "description": "{second_quote}"},
    {"label": "Clarify", "description": "I'll provide clarification"}
  ]
}
```

#### W7: Ambiguity

Each W7 weakness includes a clarifying question. Use AskUserQuestion with the auto-generated question:

```json
{
  "question": "{weakness.question or weakness.suggested_resolution}",
  "header": "Clarify",
  "options": [
    {"label": "Specify value", "description": "I'll provide a specific value/definition"},
    {"label": "Not required", "description": "This is not a hard requirement"},
    {"label": "Use default", "description": "Use a sensible default"}
  ]
}
```

Example clarifying questions by ambiguity type:
- Vague quantifier: "How many specifically? Provide a number or range."
- Weak requirement: "Is this required or optional? If optional, under what conditions?"
- Vague timing: "What is the specific timing? (e.g., <100ms, every 5 minutes)"
- Passive voice: "What component/system performs this action?"

#### W8: Missing Activation Requirements

Detected when the spec describes invocation (e.g., "user runs /command", "user invokes the skill") without specifying how that invocation becomes possible.

```json
{
  "question": "The spec describes '{invocation_description}' but doesn't specify how this becomes invocable. What makes this available to users?",
  "header": "Activation",
  "options": [
    {"label": "Registration required", "description": "I'll specify what registration/installation is needed"},
    {"label": "Built-in", "description": "This is provided by the runtime environment (document which)"},
    {"label": "Documentation only", "description": "Activation is out of scope - add to Non-goals"}
  ]
}
```

W8 patterns to detect:
- "User invokes X" or "User runs X" without installation/registration steps
- Entry points described without activation mechanism
- Commands or APIs referenced without deployment/registration
- Skills or plugins described without installation instructions

If user selects "Registration required", follow up:
```json
{
  "question": "What specific steps or files are needed to make '{invocation}' available?",
  "header": "Activation Steps",
  "options": [
    {"label": "Config file", "description": "A configuration file registers this (specify format/location)"},
    {"label": "CLI install", "description": "A CLI command installs this (specify command)"},
    {"label": "Auto-discovery", "description": "The runtime auto-discovers this (specify convention)"},
    {"label": "Manual setup", "description": "Manual steps are required (I'll document them)"}
  ]
}
```

#### CK-*: Checklist Gaps

For critical checklist gaps that weren't caught in Phase 6 Gate:

```json
{
  "question": "The spec is missing {checklist_item}. Should this be added?",
  "header": "Missing Content",
  "options": [
    {"label": "Add it", "description": "I'll provide the missing information"},
    {"label": "N/A", "description": "This spec doesn't need this (document why)"},
    {"label": "Defer", "description": "Address in a follow-up spec"}
  ]
}
```

### Step 4: Record and Apply Resolutions

For each resolved weakness:

1. **Record the resolution** for downstream consumers (logic-architect):
```bash
tasker spec add-resolution {weakness_id} {resolution_type} \
    --response "{user_response}" \
    --notes "{context}"
```

Resolution types:
- `mandatory` - MUST be implemented as specified (W1 DDL requirements, W8 activation requirements)
- `clarified` - User provided specific value/definition (W7 ambiguity, W8 activation mechanism)
- `not_applicable` - Doesn't apply to this spec (checklist gaps)
- `defer` - Address in follow-up work

2. **Update the spec content** to address the issue:
   - If W1 resolved as "mandatory", add explicit behavioral statement
   - If W6 resolved, remove contradictory statement
   - If W7 resolved, replace ambiguous language with specific terms
   - If W8 resolved as "mandatory" or "clarified", add Installation & Activation section to spec
   - If CK-* resolved as "not_applicable", document rationale

### Step 5: Re-run Until Clean

```bash
# Re-run analysis
tasker spec review /tmp/claude/spec-draft.md
```

**Update state.json after each resolution:**
```json
{
  "review": {
    "weaknesses_found": 6,
    "weaknesses_resolved": 4,
    "critical_remaining": 2
  },
  "updated_at": "<timestamp>"
}
```

**Continue until:**
- Zero critical weaknesses remain, OR
- All critical weaknesses have been explicitly accepted by user

### Step 6: Save Review Results

Save the final review results:

```bash
tasker spec review /tmp/claude/spec-draft.md > $TARGET_DIR/.tasker/spec-review.json
```

Update state.json:
```json
{
  "phase": {
    "step": "complete"
  },
  "review": {
    "status": "complete",
    "completed_at": "<timestamp>",
    "weaknesses_found": 6,
    "weaknesses_resolved": 6,
    "critical_remaining": 0
  },
  "updated_at": "<timestamp>"
}
```

## Spec Review Gate

| Check | Requirement |
|-------|-------------|
| No critical weaknesses | All W1, W6, critical W7, CK-* resolved or accepted |
| Resolutions recorded | `spec-resolutions.json` contains all resolution decisions |
| Review file saved | `$TARGET_DIR/.tasker/spec-review.json` exists |

Check resolution status:
```bash
tasker spec unresolved
```

If critical weaknesses remain unresolved, **STOP** and ask user to resolve.

---

# Phase 8 — Export

## CRITICAL: Export From Working Files

**On entry to Phase 8:**
All content comes from working files, NOT conversation context:
- Spec content: `$TARGET_DIR/.tasker/spec-draft.md`
- Capability map: `$TARGET_DIR/.tasker/capability-map-draft.json`
- FSM artifacts: `$TARGET_DIR/.tasker/fsm-draft/`
- Decision registry: `$TARGET_DIR/.tasker/decisions.json`
- ADR drafts: `$TARGET_DIR/.tasker/adrs-draft/`

Update state.json:
```json
{
  "phase": {
    "current": "export",
    "completed": ["initialization", "scope", "clarify", "synthesis", "architecture", "decisions", "gate", "review"],
    "step": "starting"
  },
  "updated_at": "<timestamp>"
}
```

## Write Files

Only after spec review passes. All permanent artifacts go to the **TARGET project**.

### 1. Ensure Target Directory Structure

```bash
mkdir -p {TARGET}/docs/specs {TARGET}/docs/adrs {TARGET}/docs/state-machines/<slug>
```

### 2. Spec Packet
Copy and finalize `$TARGET_DIR/.tasker/spec-draft.md` to `{TARGET}/docs/specs/<slug>.md`:

```markdown
# Spec: {Title}

## Related ADRs
- [ADR-0001: Decision Title](../adrs/ADR-0001-decision-title.md)
- [ADR-0002: Another Decision](../adrs/ADR-0002-another-decision.md)

## Goal
[From Phase 1]

## Non-goals
[From Phase 1]

## Done means
[From Phase 1]

## Tech Stack
[From Phase 1 - summarized]

**Language & Runtime:**
- [e.g., Python 3.12+, Node.js 20+, Go 1.22+]

**Frameworks:**
- [e.g., FastAPI, Next.js, Chi]

**Data:**
- [e.g., PostgreSQL, Redis, SQLite]

**Infrastructure:**
- [e.g., Docker, AWS Lambda, Kubernetes]

**Testing:**
- [e.g., pytest, Jest, go test]

(Remove sections that don't apply)

## Installation & Activation
[If spec describes user invocation, this section is REQUIRED]

**Entry Point:** [e.g., `/myskill`, `mycommand`, `POST /api/start`]

**Activation Mechanism:**
- [e.g., "Skill registration in .claude/settings.local.json"]
- [e.g., "CLI installation via pip install"]
- [e.g., "API deployment to AWS Lambda"]

**Activation Steps:**
1. [Step to make the entry point available]
2. [Step to verify it works]

**Verification Command:**
```bash
[Command to verify the system is properly activated and invocable]
```

(If no user invocation is described, this section can be "N/A - library/module only")

## Workflows
[From Phase 3]

## Invariants
[From Phase 3]

## Interfaces
[From Phase 3]

## Architecture sketch
[From Phase 4]

## Decisions
Summary of key decisions made during specification:

| Decision | Rationale | ADR |
|----------|-----------|-----|
| [Decision 1] | [Why] | [ADR-0001](../adrs/ADR-0001-slug.md) |
| [Decision 2] | [Why] | (inline - not ADR-worthy) |

## Open Questions

### Blocking
(none - gate passed)

### Non-blocking
- [Any remaining non-blocking questions]

## Agent Handoff
- **What to build:** [Summary]
- **Must preserve:** [Key constraints]
- **Blocking conditions:** None

## Artifacts
- **Capability Map:** [<slug>.capabilities.json](./<slug>.capabilities.json)
- **Behavior Model (FSM):** [state-machines/<slug>/](../state-machines/<slug>/)
- **Discovery Log:** Archived in tasker project
```

### 3. Capability Map
Copy and validate `$TARGET_DIR/.tasker/capability-map-draft.json` to `{TARGET}/docs/specs/<slug>.capabilities.json`.

Validate against schema:
```bash
tasker state validate capability_map --file {TARGET}/docs/specs/<slug>.capabilities.json
```

### 4. Behavior Model (FSM)

Copy FSM drafts from `$TARGET_DIR/.tasker/fsm-draft/` to `{TARGET}/docs/state-machines/<slug>/`:

```bash
# Copy FSM drafts to final location
cp -r "$TARGET_DIR/.tasker/fsm-draft/"* "{TARGET}/docs/state-machines/<slug>/"

# Generate Mermaid diagrams from canonical JSON
tasker fsm mermaid {TARGET}/docs/state-machines/<slug>

# Validate FSM artifacts (I1-I6 invariants)
tasker fsm validate {TARGET}/docs/state-machines/<slug>
```

Validate against schemas:
```bash
tasker fsm validate {TARGET}/docs/state-machines/<slug>
```

### 6. ADR Files (0..N)
Copy ADR drafts from `$TARGET_DIR/.tasker/adrs-draft/` to `{TARGET}/docs/adrs/`:

```bash
cp "$TARGET_DIR/.tasker/adrs-draft/"*.md "{TARGET}/docs/adrs/"
```

### 7. Spec Review Results
Verify `$TARGET_DIR/.tasker/spec-review.json` is saved.

### 8. Generate README.md

**Purpose:** Ensure anyone encountering the project immediately understands what it is and how to use it.

Generate `{TARGET}/README.md` with:

```markdown
# {Project Title}

{One-sentence description of what this system does}

## What It Does

{2-3 bullet points explaining the core functionality}

## Installation

{From Installation & Activation section of spec}

## Usage

{Primary entry point and basic usage example}

## How It Works

{Brief explanation of the architecture/workflow - 3-5 bullet points}

## Project Structure

```
{key directories and files with one-line descriptions}
```

## License

{License from spec or "TBD"}
```

**Content Sources:**
- Title/description: From spec Goal section
- Installation: From spec Installation & Activation section
- Usage: From spec Entry Point and Workflows
- How It Works: From spec Architecture Sketch
- Project Structure: From capability map domains/files

**IMPORTANT:** The README is the first thing anyone sees. It must clearly answer:
1. What is this? (one sentence)
2. What problem does it solve?
3. How do I use it?

## Final State Update

Update `$TARGET_DIR/.tasker/state.json`:
```json
{
  "phase": {
    "current": "complete",
    "completed": ["initialization", "scope", "clarify", "synthesis", "architecture", "decisions", "gate", "review", "export"],
    "step": "done"
  },
  "updated_at": "<timestamp>",
  "completed_at": "<timestamp>"
}
```

## Completion Message

```markdown
## Specification Complete

### What Was Designed

**{Project Title}** — {One-sentence description}

{2-3 sentences explaining what this system does, who it's for, and the key value it provides}

**Entry Point:** {e.g., `/kx`, `mycommand`, `POST /api/start`}

---

**Exported to {TARGET}/:**
- `README.md` (project overview - start here)

**Exported to {TARGET}/docs/:**
- `specs/<slug>.md` (human-readable spec)
- `specs/<slug>.capabilities.json` (machine-readable for /plan)
- `state-machines/<slug>/` (behavior model - state machine)
  - `index.json`, `steel-thread.states.json`, `steel-thread.transitions.json`
  - `steel-thread.mmd` (Mermaid diagram)
- `adrs/ADR-####-*.md` (N ADRs)

**Working files (in $TARGET_DIR/.tasker/):**
- `clarify-session.md` (discovery log)
- `spec-review.json` (weakness analysis)
- `state.json` (session state)

**Capabilities Extracted:**
- Domains: N
- Capabilities: N
- Behaviors: N
- Steel Thread: F1 (name)

**Behavior Model (FSM) Summary:**
- Machines: N (primary: M1 Steel Thread)
- States: N
- Transitions: N
- Guards linked to invariants: N

**Spec Review Summary:**
- Total weaknesses detected: X
- Critical resolved: Y
- Warnings noted: Z

**Next steps:**
- Review exported spec, capability map, and FSM diagrams
- Run `/plan {TARGET}/docs/specs/<slug>.md` to begin task decomposition
```

---

# Non-Goals (Skill-Level)

- No Git automation (user commits manually)
- No project management (no Jira/Linear integration)
- No runtime ops/runbooks
- No over-facilitation (don't ask unnecessary questions)
- No architectural debates before behavior is defined
- No file/task mapping (that's `/plan`'s job)

---

# Commands

| Command | Action |
|---------|--------|
| `/specify` | Start or resume specification workflow (auto-detects from state files) |
| `/specify status` | Show current phase and progress |
| `/specify reset` | Discard current session and start fresh |

---

# Context Engineering: Persistence Over Memory

## Design Principle

This skill is designed to **survive context compaction**. All significant state is persisted to files, not held in conversation memory.

## Working Files Summary

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `state.json` | Phase progress, granular step tracking | Updated after every significant action |
| `spec-draft.md` | Accumulated spec sections | Appended after each phase |
| `clarify-session.md` | Discovery Q&A log | Append-only during Phase 2 |
| `stock-takes.md` | Vision evolution log | Append-only during Phase 2 (after each category) |
| `capability-map-draft.json` | Capability extraction working copy | Written during Phase 3 |
| `fsm-draft/` | FSM working files | Written during Phase 3 |
| `decisions.json` | Decision registry (index of ADRs) | Updated during Phase 5 |
| `adrs-draft/` | ADR working files (full decision details) | Written during Phase 5 |
| `spec-review.json` | Weakness analysis results | Written during Phase 7 |

## Resume Protocol

**On any `/specify` invocation (including after compaction):**

The skill automatically detects and resumes active sessions. This is NOT optional.

### Detection (Phase 0, Step 1)
1. Check for `$TARGET_DIR/.tasker/state.json`
2. If exists and `phase.current != "complete"` → **auto-resume**
3. If not exists or `phase.current == "complete"` → **new session**

### Resume Steps (when auto-resume triggered)
1. **Read `state.json`** to get current phase and step
2. **Inform user** of resume (no confirmation needed)
3. **Read the appropriate working files** for that phase's context:

| Phase | Files to Read |
|-------|---------------|
| scope | `state.json` only |
| clarify | `clarify-session.md`, `stock-takes.md`, `state.json` (category status, pending followups, stock_takes_count) |
| synthesis | `clarify-session.md`, `stock-takes.md`, `spec-draft.md`, `capability-map-draft.json`, `fsm-draft/` |
| architecture | `spec-draft.md` |
| decisions | `spec-draft.md`, `decisions.json` |
| gate | `spec-draft.md`, `capability-map-draft.json`, `fsm-draft/` |
| review | `spec-draft.md`, `spec-review.json` |
| export | All working files |

4. **Jump to the current phase** - do NOT re-run earlier phases
5. **Resume from `phase.step`** within that phase

## Anti-Patterns (AVOID)

- **DO NOT** accumulate requirements in conversation context during Phase 2 - write to `clarify-session.md`
- **DO NOT** build spec text in conversation - write sections to `spec-draft.md` immediately
- **DO NOT** assume prior phase content is in context - always read from files
- **DO NOT** batch state updates - update `state.json` after every significant action
- **DO NOT** scan `adrs-draft/` to find decisions - use `decisions.json` as the index, then read specific ADR files only when full details are needed

## State Update Frequency

Update `state.json` after:
- Completing any user question round
- Completing any follow-up sub-loop
- Changing categories in Phase 2
- Completing any stock-take in Phase 2
- Completing any spec section in Phase 3
- Each decision outcome in Phase 5
- Each weakness resolution in Phase 7
- Completing any phase

This ensures the skill can resume from any point with minimal context loss.

---

# Integration with /plan

After `/specify` completes, user runs:
```
/plan {TARGET}/docs/specs/<slug>.md
```

Because `/specify` already produced a capability map and FSM, `/plan` can **skip** these phases:
- Spec Review (already done)
- Capability Extraction (already done)

`/plan` starts directly at **Physical Mapping** (mapping capabilities to files).

Additionally, `/plan` will:
- Load FSM artifacts from `{TARGET}/docs/state-machines/<slug>/`
- Validate transition coverage (every FSM transition → ≥1 task)
- Generate FSM-aware acceptance criteria for tasks

# Integration with /execute

When executing tasks, `/execute` will:
- Load FSM artifacts for adherence verification
- For each task with FSM context:
  - Verify transitions are implemented
  - Verify guards are enforced
  - Verify states are reachable
- Include FSM verification results in task completion
