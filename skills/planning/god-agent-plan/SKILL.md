---
name: god-agent-plan
description: >
  Interactive planning for god-agent. Research, interview, external review.
  Produces god-agent-compatible artifacts (_docs/specs/, _docs/plans/).
  Run before /god-agent for high-quality specs.
user-invocable: true
argument-hint: "Build a recipe sharing app. Preferences: Danish market, mobile-first"
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# God-Agent Plan: Interactive Planning Pipeline

**Version: 1.0.0** -- Interactive planning with research, interview, external review

> **ANNOUNCE AT STARTUP:** "Starting god-agent-plan v1.0.0 (interactive planning)"

Take any input (one-liner, rough spec, or product brief) and produce high-quality God-Agent-compatible planning artifacts through research, interactive interview, and external LLM review.

**Tech stack (always):** .NET 9, ASP.NET Core, EF Core 9, SQLite, SignalR, React 19, Vite, TypeScript, Tailwind CSS v4, Zustand.

**Output artifacts:** `_docs/specs/`, `_docs/plans/`, `.god-agent/` -- ready for `/god-agent` execution.

**Key difference from God-Agent's built-in Phases 0-2:** This skill involves the human (interview), researches unknowns (web + codebase), and gets external LLM review. God-Agent's built-in intake is self-dialogue only.

---

## Logging Format

Use this format for every step:

```
===============================================================
STEP {N}/12: {STEP_NAME}
===============================================================
[PLAN] {details}
Step {N} complete: {summary}
---------------------------------------------------------------
```

---

## Step 1: Print Intro + Validate Input

```
===============================================================
STEP 1/12: VALIDATE INPUT
===============================================================
```

Print banner:
```
  ___           _     _                  _     ___  _
 / __|___  __| |   /_\  __ _ ___ _ _ | |_  | _ \| |__ _ _ _
| (_ / _ \/ _` |  / _ \/ _` / -_) ' \|  _| |  _/| / _` | ' \
 \___\___/\__,_| /_/ \_\__, \___|_||_|\__| |_|  |_\__,_|_||_|
                        |___/
Interactive Planning Pipeline v1.0.0
```

**Input validation:**
- Input can be: (1) path to `.md` spec file, (2) raw idea string
- If path provided: read the file, use contents as input
- If raw string: use directly
- If neither provided (empty $ARGUMENTS): print usage and STOP:
  ```
  Usage: /god-agent-plan "Build a recipe sharing app. Preferences: Danish market, mobile-first"
     or: /god-agent-plan path/to/spec.md
  ```

Log: `Step 1 complete: Input validated ({word count} words)`

---

## Step 2: Setup Session

```
===============================================================
STEP 2/12: SETUP SESSION
===============================================================
```

1. **Derive project path:**
   - Extract `{project-name}` from input (kebab-case, e.g., "recipe sharing app" -> `recipe-app`)
   - Target path: `~/repos/playground/{project-name}/`

2. **Create directories** (if needed):
   ```
   {project}/
   ├── _docs/
   │   ├── specs/
   │   └── plans/
   └── .god-agent/
       └── reviews/
   ```

3. **Detect mode:**
   - Target folder exists with `CLAUDE.md` -> **Extension Mode**
   - Otherwise -> **Greenfield Mode**

4. **Scan for existing artifacts** and determine resume point (see Resume Logic below).

5. **Enter project directory** -- `cd` into it.

Log: `Step 2 complete: {Mode} mode, project at {path}, resuming from Step {N}`

### Resume Logic

File-existence based. Check in order:

| Artifacts Found | Resume From |
|-----------------|-------------|
| None | Step 3 (assess input) |
| `.god-agent/research-decision.md` with `skipped: true` | Step 6 (interview -- research was skipped) |
| `.god-agent/research.md` | Step 6 (interview) |
| + `.god-agent/brainstorm-qa.md` | Step 7 (spec synthesis) |
| + `_docs/specs/*-{feature}.md` but NO `design-system/MASTER.md` | Step 7b (style generation) |
| + `_docs/specs/*-{feature}.md` AND `design-system/MASTER.md` | Step 8 (architecture) |
| + `_docs/specs/*-architecture.md` | Step 9 (planning) |
| + `_docs/plans/MANIFEST.json` | Step 10 (external review) |
| + `.god-agent/reviews/` + `.god-agent/integration-notes.md` | Step 11 (user review) |
| + `.god-agent/integration-notes.md` but plans NOT updated | Step 10 (re-apply integration) |
| All artifacts present + user previously completed review | Step 12 (print summary) |

**Research skip detection:** If `.god-agent/research-decision.md` exists and contains `skipped: true`, resume skips directly to interview without re-asking.

If resuming, skip to the determined step. Otherwise continue to Step 3.

---

## Step 3: Assess Input Completeness

```
===============================================================
STEP 3/12: ASSESS INPUT COMPLETENESS
===============================================================
```

Score input against 7 dimensions. See `references/completeness-dimensions.md`.

For each dimension, ask: "Could an implementer make a specific decision from this detail without asking follow-ups?"

| # | Dimension | Covered? |
|---|-----------|----------|
| 1 | Problem | Yes/No |
| 2 | Target Users | Yes/No |
| 3 | Core Features | Yes/No |
| 4 | Entities | Yes/No |
| 5 | User Flows | Yes/No |
| 6 | Constraints | Yes/No |
| 7 | Visual/UX | Yes/No |

**Score -> Interview depth:**
- 0-2: FULL (5-8 rounds)
- 3-5: LIGHT (2-3 rounds)
- 6-7: VALIDATION (1 round)

Log which dimensions are covered and which need interview.

Log: `Step 3 complete: Score {N}/7, interview depth: {FULL|LIGHT|VALIDATION}`

---

## Step 4: Research Decision

```
===============================================================
STEP 4/12: RESEARCH DECISION
===============================================================
```

See `references/research-protocol.md` for full protocol.

1. Analyze input to extract 3-5 searchable research topics
2. Present to user via AskUserQuestion:

**Question 1** (extension mode only):
- "Should I research the existing codebase for patterns and conventions?"
- Options: Yes / No

**Question 2:**
- "Which technology topics should I research?" (multi-select)
- Options: extracted topics from input analysis
- User can also select "Other" for custom topics

3. Write `.god-agent/research-decision.md` with choices.

**If user selects NO codebase research AND no web topics:**
- Write `.god-agent/research-decision.md` with `skipped: true`
- Skip Step 5 entirely
- Proceed to Step 6

Log: `Step 4 complete: Research decision recorded ({N} topics selected | skipped)`

---

## Step 5: Execute Research

```
===============================================================
STEP 5/12: EXECUTE RESEARCH
===============================================================
```

**Skip if:** research-decision.md has `skipped: true`.

See `references/research-protocol.md` for full protocol.

Launch research subagents based on user choices from Step 4.

**CRITICAL:** Subagents return results as text. They do NOT write files. Main context combines and writes `.god-agent/research.md`.

**Codebase research** (if selected):
```
Task(subagent_type="Explore", prompt="""
Analyze this codebase for patterns and conventions:
- CLAUDE.md contents and conventions
- Backend: endpoint patterns, entity patterns, folder structure
- Frontend: component patterns, state management, routing
- Database: schema patterns, migration approach
- Testing: test patterns, coverage approach

Return findings as markdown text. Do NOT write any files.
""")
```

**Web research** (for each selected topic):
```
Task(subagent_type="Explore", prompt="""
Research: {topic}

Use WebSearch and ref_search_documentation to find:
- Current best practices and patterns
- Common pitfalls and gotchas
- Recommended libraries/approaches
- Code examples and patterns

Return findings as markdown text. Do NOT write any files.
""")
```

**Parallel execution:** If both codebase AND web research needed, launch ALL Tasks in a SINGLE message.

After all subagents return, combine results and write `.god-agent/research.md`.

**Failure handling:** See `references/research-protocol.md`.

Log: `Step 5 complete: Research written to .god-agent/research.md`

---

## Step 6: Interview

```
===============================================================
STEP 6/12: INTERVIEW
===============================================================
```

See `references/interview-protocol.md` for full protocol.

Adaptive AskUserQuestion sessions. Only ask about missing/vague dimensions from Step 3.

**Key rules:**
- One question per message
- Multiple choice via AskUserQuestion options
- Reference research findings (if any) when asking about technical decisions
- Don't ask the obvious -- skip what's already answered
- Dig deeper when answers reveal complexity

**Depth from Step 3:**
- FULL (0-2): 5-8 rounds, all missing dimensions + edge cases
- LIGHT (3-5): 2-3 rounds, fill specific gaps only
- VALIDATION (6-7): 1 round, "Here's my understanding -- anything wrong?"

**Stop criteria:**
- All 7 dimensions covered with actionable detail, OR
- User predominantly answers "I don't know" / "Up to you", OR
- Maximum rounds reached

After interview, write Q&A to `.god-agent/brainstorm-qa.md` using God-Agent's Q&A template.

Read the Q&A template from the god-agent skill's references: `god-agent/references/qa-template.md`

Log: `Step 6 complete: Interview done ({N} rounds), Q&A written`

---

## Step 7: Spec Synthesis + Style

```
===============================================================
STEP 7/12: SPEC SYNTHESIS + STYLE
===============================================================
```

### 7a: Spec Synthesis

Combine all inputs:
- Original user input/spec
- Research findings (`.god-agent/research.md`, if exists)
- Interview Q&A (`.god-agent/brainstorm-qa.md`)

Write product spec to `_docs/specs/{DATE}-{feature}.md` using God-Agent's spec template.

Read the spec template from the god-agent skill's references: `god-agent/references/spec-template.md`

**Spec must be self-contained** -- readable by an unfamiliar reader without other docs.

### 7b: Design System / Style

**Check:** If `design-system/MASTER.md` already exists (extension mode):
- Log: `[STYLE] Reusing existing design system`
- Skip style generation

**Otherwise:**
- Extract style keywords from Q&A (Q9: Visual Style answer)
- If Q9 is generic, combine: product type + industry + users -> style keywords
- Run `ui-ux-pro-max`:
  ```
  Invoke Skill tool: ui-ux-pro-max
  Run: python3 {skill_path}/scripts/search.py \
    "{style_keywords}" \
    --design-system --persist -p "{project_name}"
  ```
- Fallback if ui-ux-pro-max fails or produces empty result:
  - Write a minimal `design-system/MASTER.md` with style "Modern Minimal Clean" and sensible defaults (neutral palette, system fonts, clean spacing)
  - Log assumption to STATE.md equivalent (`.god-agent/` notes)

**Update CLAUDE.md** (create if needed):
```markdown
## Visual Style
Style: {style_name from MASTER.md}
Design System: design-system/MASTER.md
```

Log: `Step 7 complete: Spec written, style {generated|reused}`

---

## Step 8: Architecture

```
===============================================================
STEP 8/12: ARCHITECTURE
===============================================================
```

Dispatch architecture subagent with both pattern skills:

```
Task(subagent_type="general-purpose", prompt="""
You are creating a technical architecture document for a .NET 9 + React 19 application.

SKILLS TO LOAD (use Skill tool):
1. saurun:dotnet-tactical-ddd -- for backend architecture decisions
2. saurun:react-frontend-patterns -- for frontend architecture decisions

PRODUCT SPEC:
{contents of _docs/specs/{DATE}-{feature}.md}

ENTITY DESIGN DECISION FRAMEWORK:
For each entity in the spec, ask:
  Does it have business rules or behavior methods?
  YES -> Rich domain object (private setters, factory methods, invariants)
  NO  -> Anemic property bag (public getters/setters, no domain methods)

CONCISENESS RULES (this doc is for autonomous agents, not humans):
- NO redundancy: information appears ONCE in the most logical place
- NO full code: method signatures only, not implementations
- NO obvious patterns: don't describe standard TanStack Query or EF Core flows
- NO separate validation section: put validation inline in DTOs as comments
- Rich entities: list method signatures only
- Anemic entities: just name and properties, no behavior section
- Data Flow: ONLY describe non-standard flows or critical decisions
- Infrastructure: ONLY non-default choices

OUTPUT: Write architecture doc to _docs/specs/{DATE}-{feature}-architecture.md

ARCHITECTURE TEMPLATE:
{contents of god-agent/references/architecture-template.md}
""")
```

**Architecture doc must be self-contained** -- entity model, API contracts, component tree all inline. Plans reference it by section title.

**Gate 8 validation:**
- Architecture doc exists
- Has `## Entity Model` with rich/anemic classifications
- Has `## API Contract` with DTOs and endpoints
- Has `## Component Tree`
- Has `## Test Layer Map`
- No full code implementations

If gate fails, re-dispatch with specific issues (up to 2 retries).

Log: `Step 8 complete: Architecture doc written`

---

## Step 9: Planning

```
===============================================================
STEP 9/12: PLANNING
===============================================================
```

Dispatch parallel subagents per work unit. Select applicable units from:
- Backend domain + infra
- Backend API
- Backend real-time (if SignalR needed)
- Frontend state + API
- Frontend pages + components
- Integration

**Skill routing:**

| Work Unit | Skill |
|-----------|-------|
| Backend * | `saurun:dotnet-writing-plans` |
| Frontend * | `saurun:react-writing-plans` |
| Integration | Both |

**Per work unit subagent:**

```
Task(subagent_type="general-purpose", prompt="""
Generate an implementation plan for work unit: {unit_name}

SKILL TO LOAD: {saurun:dotnet-writing-plans | saurun:react-writing-plans}
Load via Skill tool.

ARCHITECTURE DOC:
{contents of architecture doc}

PRODUCT SPEC:
{contents of product spec}

CONTEXT FOR PLAN WRITER:
{relevant sections of architecture doc for this work unit}

OUTPUT: Write plan to _docs/plans/{DATE}-{unit_name}.md

Plans use "Implements:" to reference architecture doc sections by title
(e.g., Implements: ## API Contract > POST /recipes).

Plans are compact -- God-Agent's specialized implementer agents have
patterns pre-loaded, so plans only need contract references, file paths,
and behaviors.
""")
```

**Dispatch independent work units in parallel** (multiple Task calls in a single message).

**After all subagents complete**, write `_docs/plans/MANIFEST.json`:

```json
{
  "feature": "{feature-name}",
  "created": "{ISO timestamp}",
  "plans": [
    {"id": "{unit-id}", "path": "_docs/plans/{DATE}-{unit-name}.md"},
    ...
  ]
}
```

Array order = execution order (backend before frontend).

**Gate 9 validation:**
- MANIFEST.json exists with `plans` array >= 1 entry
- Each entry's `path` points to an existing `.md` file on disk
- Each plan has tasks with `**Implements:**`, `**Files:**`, `**Behaviors:**`
- Plans are in correct execution order

If any path is missing, the plan subagent failed -- log error and re-dispatch for that work unit (up to 1 retry).

Log: `Step 9 complete: {N} plans written, MANIFEST.json created`

---

## Step 10: External Review

```
===============================================================
STEP 10/12: EXTERNAL REVIEW
===============================================================
```

See `references/external-review-protocol.md` for full protocol.

### Pre-Check

```bash
which gemini && which codex
```

If either missing: STOP with install instructions (see protocol).

### Launch Reviews

Dispatch BOTH in a SINGLE message (two parallel Bash calls):

**Bash call 1 (Gemini):**
```bash
echo '{REVIEW_PROMPT}' | gemini -m gemini-3-pro-preview --approval-mode yolo
```

**Bash call 2 (Codex):**
```bash
echo '{REVIEW_PROMPT}' | codex exec -m gpt-5.3 --sandbox read-only --full-auto
```

Substitute `{ARCHITECTURE_CONTENT}` and `{ALL_PLAN_CONTENTS}` into the reviewer prompt (see protocol).

Set 5-minute timeout on both Bash calls.

### Process Results

Write `.god-agent/reviews/gemini-review.md` and `.god-agent/reviews/codex-review.md`.

Read both reviews. For each suggestion, apply integration criteria (see protocol):
- **ACCEPT** if it fixes bugs, gaps, security issues, or classification errors
- **REJECT** if it contradicts user decisions, over-engineers, or expands scope

### Integration Output

1. Write `.god-agent/integration-notes.md` with Integrated/Rejected lists
2. Update `_docs/specs/*-architecture.md` with accepted architectural changes
3. Update `_docs/plans/*.md` with accepted plan changes (only affected plans)

Log: `Step 10 complete: {N} accepted, {M} rejected from {K} total suggestions`

---

## Step 11: User Review

```
===============================================================
STEP 11/12: USER REVIEW
===============================================================
```

Use AskUserQuestion to pause for user review:

```
Plans have been reviewed by Gemini + Codex. I've integrated feedback.

Review the updated files:
- _docs/specs/*-architecture.md (architecture)
- _docs/plans/*.md (implementation plans)
- .god-agent/integration-notes.md (what was accepted/rejected)

When satisfied, select Done.
```

Options: ["Done reviewing"]

Wait for confirmation, then **immediately proceed to Step 12** (no re-invocation needed).

Log: `Step 11 complete: User approved plans`

---

## Step 12: Summary

```
===============================================================
STEP 12/12: SUMMARY
===============================================================
```

Print all generated artifacts:

```
Planning complete! Generated artifacts:

SPECS:
  _docs/specs/{DATE}-{feature}.md          (product spec)
  _docs/specs/{DATE}-{feature}-architecture.md  (architecture)

PLANS:
  _docs/plans/MANIFEST.json                (plan manifest)
  _docs/plans/{DATE}-{unit-1}.md           (plan 1)
  _docs/plans/{DATE}-{unit-2}.md           (plan 2)
  ...

SUPPORTING:
  .god-agent/brainstorm-qa.md              (interview Q&A)
  .god-agent/research.md                   (research findings)
  .god-agent/research-decision.md          (research choices)
  .god-agent/reviews/gemini-review.md      (Gemini review)
  .god-agent/reviews/codex-review.md       (Codex review)
  .god-agent/integration-notes.md          (review integration)
  design-system/MASTER.md                  (visual design system)

Next: Run /god-agent to execute these plans.
---------------------------------------------------------------
```

Only list files that actually exist (some may have been skipped).

**Done.**

---

## Gate Checks

Lightweight validation after each step. Check that expected files exist and have key sections. No retry loop -- if something fails, log the issue and let the user fix.

| Step | Gate Check |
|------|-----------|
| 1 | Input is non-empty (file readable or string has content) |
| 2 | Project directory exists, `_docs/` and `.god-agent/` created |
| 3 | Completeness score calculated |
| 4 | research-decision.md written |
| 5 | research.md written (or skipped) |
| 6 | brainstorm-qa.md has answers for uncovered dimensions |
| 7 | Spec exists with Problem, Solution, Scope, Entities, User Flows |
| 7b | MASTER.md exists (or reused) |
| 8 | Architecture doc has Entity Model, API Contract, Component Tree, Test Layer Map |
| 9 | MANIFEST.json exists, all plan paths valid, plans have Implements/Files/Behaviors |
| 10 | Review files exist (or noted as failed), integration-notes.md written |
| 11 | User confirmed |

---

## Error Handling

- **Subagent failure:** Log error, note which step failed. Do not retry automatically (user can re-invoke to resume).
- **Missing CLI:** STOP with install instructions (Step 10 only).
- **User aborts:** STATE.md-equivalent is the artifact files themselves. Re-invoke picks up from last completed step.
- **Context exhaustion:** All artifacts are on disk. Re-invoke and resume logic handles continuation.
