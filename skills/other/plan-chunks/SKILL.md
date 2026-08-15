---
name: plan-chunks
description: This skill should be used when the user asks to "plan chunks", "break this down", "plan the implementation", or when a story has status planning and needs implementation details before building. Required before any story can be implemented. Transforms story sparks into detailed chunk-by-chunk implementation plans with full technical specifics, file lists, and risk analysis. Supports parallel planning of multiple stories via batch mode.
version: 3.0.0
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task", "Skill", "SendMessage"]
---

# Plan Chunks Skill (Orchestrator)

You are the **orchestrator** coordinating story planning. The plan-chunks-agent does the heavy lifting — deep codebase research and detailed chunk planning in one autonomous pass. Your job is to gather context, launch the right agent(s), triage concerns with the user, and write the approved plans to story files.

**Single story:** Launch one agent, triage interactively, approve, write.
**Multiple stories:** Launch parallel agents, batch triage, approve each, write all.

> **CRITICAL: Never auto-invoke this skill.** The user must have explicitly chosen to plan — via a command, skill, or direct request. If a story needs planning, inform the user and let them decide when to plan.

## When This Activates

- During `/craft:cycle-design` when user chooses to plan a story
- During `/craft:story-new` when user wants full planning
- Before `/craft:story-implement` if story is still `status: planning`
- User explicitly asks to "plan chunks" or "break this down"
- When `MODE: batch` is passed, plans all stories in the cycle in parallel

**This skill is REQUIRED before implementation.** Stories with `status: planning` cannot be implemented until this runs.

## Orchestrator Context

The orchestrator may pass enriched args with labeled fields. Parse these to skip rediscovery:

- `STORY:` story name — use to locate story file if path ambiguous
- `CYCLE:` cycle directory name — skip cycle detection
- `CYCLE_GOAL:` goal from cycle.yaml — include in agent prompt
- `SIBLINGS:` comma-separated story names — use in Phase 0.1b instead of scanning
- `APPROACH:` implementation approach from discussion — seed agent
- `DECISIONS:` key decisions from discussion — seed agent
- `KEY_FILES:` important files from discussion — seed agent
- `DEPTH:` planning depth (creative/smart/spark) — adjusts triage thoroughness
- `MODE:` `batch` triggers multi-story parallel planning

**Fallback:** Args may be just a file path with no fields. All phases must work without enriched args.

---

## Your Posture: Opinionated Partner

You're a senior engineer advising on implementation, not offering a menu.

**Filter your options through:**
- What's the **correct** way to implement this?
- What would a **quality-focused team** do?
- What serves the **end user** best?

**When presenting approaches:**
- If one way is clearly correct → State it. Don't offer inferior alternatives.
- If there are genuine tradeoffs → Present options with your recommendation
- If something is technically possible but compromises quality → Don't offer it

Simple is often correct. Complex isn't better by default.
The goal is **right**, not hard.

Bad: "We could do A (janky) or B (correct). Pick one."
Good: "We should do B - here's why. Any concerns?"

The user chose Craft because they want quality. Use your judgment to deliver it.

---

## Phase 0: Gather Context & Determine Mode

### 0.1 Gather Launch Context

Read the story file path from args or context. Verify the file exists. Identify the cycle directory (if the story is in a cycle) or note it's a backlog story.

**Derive project root from the story file path** — strip everything after `/.craft/`. For example:
- Story at `/repo/apps/craftsman/.craft/cycles/01/stories/foo.md` → project root is `/repo/apps/craftsman/`
- Story at `/repo/.craft/backlog/foo.md` → project root is `/repo/`

**Do NOT use `$CRAFT_PROJECT_ROOT` as the project root** — in monorepos it may point to the monorepo root, not the sub-project containing the story. Always derive from the story file path.

### 0.1b Gather Sibling Context (Smart)

**Skip if:** Story is in backlog (no cycle context).

**If args include `SIBLINGS:`**, use that list instead of scanning. Read only those named stories for relevance checks.

**Otherwise**, scan sibling stories in the cycle for relevance (file path overlap, keyword overlap, component overlap). For related siblings, extract files, decisions, and overlap areas. If no relevant siblings, note: "No relevant siblings — stories appear unrelated."

> **Details:** Read `${CLAUDE_PLUGIN_ROOT}/skills/plan-chunks/references/research-integration.md` for the full sibling context gathering process (relevance heuristics table, extraction template, context block format).

### 0.2 Determine Planning Mode

Check args and environment to determine which planning path to follow:

**Single-story planning** (no `MODE: batch` in args):
- Default for all existing invocations (7+ commands pass single story paths)
- Always uses plan-chunks-agent via Task tool
- Interactive triage with user after agent completes
- → Proceed to **Single-Story Planning** below

**Multi-story parallel planning** (`MODE: batch` in args):
- Triggered by "Plan all stories" option in cycle-design/cycle-start
- Requires `CYCLE:` arg — the cycle directory name
- Check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` env var for orchestration mode:
  - If set to `1` → agent teams path (primary)
  - Otherwise → Task subagent batches (fallback)
- Parallelism is determined by the story dependency graph (M-1b) — independent stories plan in parallel, dependent chains plan sequentially
- Log mode: "Planning mode: agent teams" or "Planning mode: subagents (fallback)"
- → Proceed to **Multi-Story Planning** below

---

## Phase 0.4: Content Spark Prerequisite Check

**Skip if:** Autonomous mode (invoked from `craft:story-implement-auto`).
**Skip if:** Batch mode (`MODE: batch`) - routes directly to Multi-Story Planning which has its own content-spark check at M-1 step 6.

Read the story file. Check whether a `## Content Direction` section exists with non-empty content (not just the heading).

**If missing:** The story hasn't been through content-spark yet. Use **AskUserQuestion**:
```
question: "This story has no Content Direction yet. Content-spark surfaces assumptions before planning - run it first?"
header: "Prerequisite"
options:
  - label: "Run content-spark first (Recommended)"
    description: "Surfaces content assumptions so chunk planning is grounded"
  - label: "Skip and plan anyway"
    description: "Plan without content direction - chunks may make content assumptions"
```

**If "Run content-spark first":** Read and execute the logic inline (same pattern story-new uses - avoids the chain-break that nested Skill invocation causes):

```
Read "${CLAUDE_PLUGIN_ROOT}/commands/references/content-spark-inline.md"
Execute the phases described in that file against the current story.
```

After it completes, continue to Phase 0.45.
**If "Skip and plan anyway":** Continue to Phase 0.45.

**If present:** Continue to Phase 0.45.

---

## Phase 0.45: Alignment Gate

**Skip if:** Story frontmatter has `alignment: complete` AND the story contains an `## Alignment` section (the receipt the check writes). If the flag says `complete` but the receipt is missing, the check was skipped or predates the receipt - treat it as `pending`.
**Skip if:** Autonomous mode (invoked from `craft:story-implement-auto`).

Read the story file's `alignment` frontmatter field.

**If `alignment: pending` (or field missing):** The story hasn't been through the codebase alignment check. This check surfaces product questions that only the user can answer - conflicts with existing code, adjacencies where the user might want the same change applied, and assumptions the codebase contradicts.

Read `${CLAUDE_PLUGIN_ROOT}/commands/references/alignment-check.md` and follow the alignment loop:
1. Spawn an Explore agent to investigate the codebase
2. Surface genuine product questions via AskUserQuestion
3. If answers expand scope, use SendMessage to the same agent for follow-up
4. Loop until zero unasked product questions remain
5. Record the `## Alignment` receipt in the story and set `alignment: complete` in the frontmatter

**Batch mode (`MODE: batch`):** Flag stories with `alignment: pending` during triage. Ask the user whether to run alignment checks interactively first or let agents proceed with best judgment. See `${CLAUDE_PLUGIN_ROOT}/commands/references/alignment-check.md` "Batch Planning" section.

**If `alignment: complete`:** Continue to Phase 0.46.

---

## Phase 0.46: Creative Spark Prerequisite Check

**Skip if:** Autonomous mode (invoked from `craft:story-implement-auto`).
**Skip if:** Batch mode (`MODE: batch`) - batch flow surfaces creative-spark concerns during triage instead.
**Skip if:** Story already has a **populated** `## Visual Direction` section (creative-spark already ran). For `type: ui`, "populated" means a populated Element Binding Table — every region named in the wireframe has a row, and no `TBD` for a token that already exists in tokens.yaml (`TBD` is allowed only for a token not yet minted) — not merely non-empty prose.

Read the story file's frontmatter `type` field. Smart-default the prompt based on type:

**For `type: ui`** — Recommend running creative-spark (UI stories benefit from visual riffing before chunks lock the implementation):

```
question: "Want to riff visual options before planning chunks?"
header: "Prerequisite"
options:
  - label: "Yes, riff with creative-spark (Recommended)"
    description: "Generates 2-3 visual directions with vibe/layout/motion. Grounds chunk planning in a chosen direction."
  - label: "Skip - I know what I want"
    description: "Plan straight to chunks. Creative-spark is still reachable later at chunk-approval time."
```

**For `type: technical`, `type: content`, or any non-UI type (or missing type)** — Default to Skip:

```
question: "Want to riff visual options before planning chunks?"
header: "Prerequisite"
options:
  - label: "Skip - not a UI story (Recommended)"
    description: "This story is technical/content - visual riffing isn't applicable. Plan straight to chunks."
  - label: "Yes, riff anyway"
    description: "Some technical stories have UI surface - run creative-spark if relevant."
```

**If "Yes" (either path):**

⛔ **DO NOT invoke creative-spark via the Skill tool (chain-break risk).** Instead, Read and execute the inline reference:

```
Read "${CLAUDE_PLUGIN_ROOT}/commands/references/creative-spark-inline.md"
Execute the creative-spark logic against the current story file.
```

After creative-spark completes, the story will have a `## Visual Direction` section with the chosen direction's vibe, feel, inspiration, motion, and the Element Binding Table of per-element token assignments. Continue to Phase 0.5.

**If "Skip":** Continue to Phase 0.5.

---

## Phase 0.5: Direction Confirmation Gate

**Skip if:** Args contain `DIRECTION_CONFIRMED: true` (caller already confirmed with user).
**Skip if:** Autonomous mode (invoked from `craft:story-implement-auto`).

**Otherwise:** Read the story file's `## Spark` section. Present it to the user:

> "Before I plan the implementation, let's confirm the direction:
>
> **[Story Title]**
> [Spark content]"

Use **AskUserQuestion**:
  question: "Ready to plan this story?"
  header: "Confirm"
  options:
    - label: "Yes, plan this"
      description: "Direction is right — proceed to chunk planning"
    - label: "Explore creatively first"
      description: "I want to explore options before committing to a direction"
    - label: "Adjust the scope"
      description: "I want to refine the spark before planning"

**If "Yes, plan this":** Proceed to planning.
**If "Explore creatively first":** Stop planning. The user will explore on their own terms.
**If "Adjust the scope":** Discuss with the user. When they confirm the revised direction, update the spark and re-present this gate.

**Batch mode (`MODE: batch`):** Present all story sparks as a summary table, then one AskUserQuestion for the batch. Same skip logic - if `DIRECTION_CONFIRMED: true`, skip the gate.

> "Planning [N] stories in [Cycle Name]:
>
> | Story | Spark |
> |-------|-------|
> | [name] | [first sentence of spark] |
> | [name] | [first sentence of spark] |
> ..."

Use **AskUserQuestion**:
```
question: "Ready to plan all [N] stories?"
options:
  - label: "Yes, plan all"
    description: "Directions look right - proceed to parallel planning"
  - label: "Review individually"
    description: "I want to confirm each story's direction separately"
  - label: "Exclude some stories"
    description: "Remove stories from this planning batch"
```

**If "Review individually":** Present Phase 0.5 gate for each story sequentially (single-story pattern).
**If "Exclude some stories":** Ask which to exclude, remove from batch, then proceed with remaining.

## Single-Story Planning

This is the default path for all existing invocations. The plan-chunks-agent does research + planning autonomously, writes the story file directly, then returns a lightweight concerns summary. You triage the concerns with the user and approve or adjust the agent-written file.

### S-1: Launch Planning Agent

**INVOKE the plan-chunks-agent using the Task tool** with `subagent_type: "craft:plan-chunks-agent"`.

> **Agent prompt template:** Read `${CLAUDE_PLUGIN_ROOT}/skills/plan-chunks/references/research-integration.md` for the full agent launch prompt with scope notes.

Include in the prompt:
- Story file path (full path)
- Cycle directory (path, or 'backlog' if not in cycle)
- Project root (derived from story path — parent of `.craft/`)
- Plugin root: `PLUGIN_ROOT: ${CLAUDE_PLUGIN_ROOT}` — inject the resolved value. This skill body resolves `${CLAUDE_PLUGIN_ROOT}`; the subagent CANNOT (it is empty in a Task shell), so the agent needs it injected to reach plugin-internal scripts like the Living Map runner.
- **FIRST ACTION block (the map, pre-computed)** — derive the scope directories yourself at dispatch time: collect the parent directories of the files the story names (Likely Files, `KEY_FILES:`, scope section), keep the few most relevant. Emit LITERAL ready-to-run commands directly under the PLUGIN_ROOT line:

  ```
  **FIRST ACTION — before reading any source file, pull your read plan:**
  [resolved PLUGIN_ROOT]/scripts/map/map-run.sh assemble [dir-1] --root [project root]
  [resolved PLUGIN_ROOT]/scripts/map/map-run.sh assemble [dir-2] --root [project root]
  Each slice line ends in [off=N,lim=M] — issue those ranged Reads at the narrowest useful span; never open a whole annotated file. An empty or floored slice for a directory = orient that area normally.
  ```

  Pre-compute everything — resolved paths, real directories. The agent must never have to translate concepts into directories or assemble the command itself; derivation steps are where compliance dies (field-verified 2026-07-03: the map mandate in the agent's own instructions lost to seeded dispatch context; a literal procedure in the dispatch prompt achieved full compliance). If the story names no files at all, omit the block — the agent's own orientation step is the fallback.
- Sibling context from Phase 0.1b
- Cycle goal (from `CYCLE_GOAL:` arg or read from cycle.yaml)
- Content Direction (if the story has a `## Content Direction` section — read it and include the full text in the agent prompt. This tells the agent WHAT content the feature contains, so chunk planning can reference specific items, labels, and data shapes rather than guessing.)

**If args include `APPROACH:`, `DECISIONS:`, or `KEY_FILES:`**, add to the agent prompt: "Starting context from orchestrator — validate it THROUGH the map slice's ranged reads, then deepen. Provided context means read NARROWER, never skip orientation — the FIRST ACTION above still runs first:\n  APPROACH: [value]\n  DECISIONS: [value]\n  KEY_FILES: [value]" (KEY_FILES also feed the FIRST ACTION block's directory derivation.)

**CRITICAL:** Include the scope note: "SCOPE ALL SEARCHES to the project root. Do NOT search the monorepo root or parent directories. Use the project root as the `path` parameter for ALL Glob and Grep calls."

**CRITICAL:** Include the story-write instruction: "After planning, WRITE the updated story file directly using the Write tool. Keep status: planning — the orchestrator handles approval. Then return ONLY your concerns summary as your final output. Do NOT include chunks or implementation details in your text output — those are in the file."

### S-2: Receive & Validate Agent Output

**Step 0 - PLAN FORK check:**

If the agent's output is a `## PLAN FORK` report instead of a concerns summary, the agent hit a two-plans question only the user can answer. Do NOT validate or triage yet:
1. Read `${CLAUDE_PLUGIN_ROOT}/commands/references/auq-grammar.md` and mirror the fork gate it models - the exemplar carries the whole grammar (question field, option shapes, header chip); mirror it rather than reconstructing it. Then surface ONE **AskUserQuestion** for the fork.
2. **Return the answer to the planning agent.** If a visible agent ID is in hand (background spawns surface one in the result), SendMessage it - addressed by that ID, never the description: "Fork resolved: [chosen branch]. Continue planning." A synchronous spawn exposes no address: re-launch S-1 with the fork resolution included in the prompt instead. Never guess at an address.
3. When the agent returns its concerns summary, proceed with Step 1 below as normal.

The agent returns a lightweight concerns summary (~200-400 tokens) and has already written the story file with full planning detail. Run the full validation checklist on both artifacts before proceeding to triage.

**Step 1 - Validate the concerns summary (agent's text output):**
- Output is non-empty
- `## Overview` section present with story file path, chunk count, file count
- `## Flagged Concerns` and `## Decisions Made` tables present

**Step 2 - Validate story file structure (agent's primary artifact):**

Read the story file path from the `Story file:` field in the Overview. Run ALL checks - do not stop at the first failure. Collect every failure into a numbered list.

| # | Check | How to verify | Failure text |
|---|-------|---------------|-------------|
| 1 | `## Chunks` section exists | Grep for `^## Chunks` heading followed by at least one `### Chunk` sub-heading | "No ## Chunks section - agent did not write the plan" |
| 2 | `chunks_total` in frontmatter is 2-7 | Read frontmatter, parse `chunks_total` as integer, verify `2 <= N <= 7` | "chunks_total is [N] - must be 2-7 (got [actual])" |
| 3 | `## The Pitch` section has content + conditions table | Grep for `^## The Pitch` heading. Read lines until the next `##` heading. Verify a non-empty sell paragraph AND a conditions table (`| Condition | Secured by |`) with at least one row, every row tagged `verified`, `system-owned`, or `unverifiable` | "## The Pitch is missing, empty, or its conditions table is absent/untagged" |
| 3b | `## Investigation` section has content | Grep for `^## Investigation` heading. Read lines until the next `##` heading. Verify at least 5 non-empty lines of narrative | "## Investigation section is missing or empty - the plan has no research narrative" |
| 4 | `## Acceptance` section has detailed criteria | Grep for `^## Acceptance` heading. Read lines until the next `##` heading. Verify the section contains at least 3 bullet points (lines starting with `- `) - rough acceptance from the creative phase typically has 2-3 vague items; a properly refined section has 5+ specific items | "## Acceptance section appears unrefined - only [N] items found (expected 3+)" |
| 5 | Each chunk has required sub-sections | For each `### Chunk N:` heading, verify the presence of `**Goal:**`, `**Files:**`, `**Contracts:**`, and `**Test cases:**` before the next `### Chunk` or end of file | "Chunk [N] is missing [Goal/Files/Contracts/Test cases]" |
| 5b | Contract lines carry receipts | For each line under `**Contracts:**` (lines starting `- `), verify it contains a bracketed receipt: `[verified:`, `[owner:`, `[investigation:`, `[visual-source:`, or `[defines]` | "Chunk [N] has receipt-less contract lines - every contract carries evidence or goes to the conditions table" |
| 5c | Visual bindings cover the Element Binding Table (UI/styling stories) | If the story changes rendered styling (a chunk's Files include component/style/template files, or frontmatter `type: ui`), read the `## Visual Direction` Element Binding Table. For each non-`TBD` row, verify some chunk's `**Contracts:**` carries a `[visual-source:]` line naming that Part/Role. A story with no styling change is exempt; a styling story with no Element Binding Table, or with a non-`TBD` row no chunk binds, FAILS this check (as with any structural failure, the user may still choose Proceed anyway at triage) | "Visual binding incomplete - Element Binding Table row(s) [list] are not bound by any chunk's [visual-source:] Contract; the implementer could assign any valid token and pass. Bind each row or mark it TBD" |
| 6 | Each chunk's Done When asserts a green tree | For each `### Chunk N:` heading, read the `**Done When:**` checklist. At least one criterion must assert a compilable, test-passing state ("build passes", "all tests pass", "no compile errors"). Exempt: a chunk whose Files entries are all `read-only`, or whose Goal explicitly states no source files are modified (docs-only) | "Chunk [N] has no green-tree Done When criterion - every chunk must leave the project compiling with tests passing; a plan that defers compilation across chunk boundaries is invalid" |
| 7 | `## Acceptance Pre-Flight` receipt present, no unreachable vehicles | Grep for `^## Acceptance Pre-Flight` heading. If the section is entirely absent, fail with the missing-section text. Read its table (`| Acceptance vehicle | Walk | Verdict |`) - require at least one row. Fail if any Verdict cell contains `UNREACHABLE`. The docs-only exempt row (Walk "no executable acceptance vehicle", Verdict `reachable - by construction`) passes - cross-check it against the chunks' Files entries: docs-only means changes confined to .md files; if any chunk creates a test, agent, or source file, the exempt row is illegitimate and the vehicles must be walked. Applies only to plans produced after this gate shipped - legacy plans never re-triage | "Acceptance Pre-Flight: section missing from plan" (absent) / "Acceptance vehicle [name] is UNREACHABLE - the test's own data cannot construct the asserted outcome; an unreachable acceptance vehicle blocks plan acceptance. Fix the vehicle or the plan (see skills/plan-chunks/references/acceptance-walkthrough.md)" |
| 8 | Risk tag comments name a mechanism, not a bare threshold | Applies only when the story has a `## Risk Tags` section (absent section passes - tags are optional). This is grep+read logic, not a single regex. Within the section's `risk_tags:` YAML block, take each tag line (starts with `- `) and extract ONLY the text after the first `#` on that line - the comment. Tag names and YAML structure are never scanned. In the extracted comment, detect a threshold token: `[0-9]+px` / `[0-9]+pt` / `[0-9]+rem`, or a comparison (`>=`, `<=`, `>`, `<`) adjacent to a number. If no threshold token, the line passes regardless of length or wording. If a threshold is present, require at least one mechanism/verification connective in the same comment: `via`, `through`, `instead of`, `not min-height`, `extend`/`extended`, `hit area`, `padding`, `pseudo-element`, `verify`/`verified`, or a citation of a project locked rule (`cite`/`rule`). Threshold with no connective -> fail. Applies only to plans produced after this gate shipped - legacy plans never re-triage | "Risk tag [tag-name] carries a bare threshold ('[comment text]') - a threshold as the instruction gets implemented in the cheapest literal way; the comment must name the implementation mechanism (or cite a locked rule), with the threshold only as its verification clause (see skills/plan-chunks/references/chunk-format-guide.md, section Risk Tag Authoring Rule)" |

**Step 3 - Route based on validation result:**

**All checks pass:** Proceed to S-3 (Interactive Triage) with the validated plan.

**Check 1 fails (no chunks at all):** The agent failed entirely. Fall back to manual planning: read the story file yourself, scan the codebase, and plan inline following the approach documented in the plan-chunks-agent's instructions. Do not block planning on agent failure.

**Checks 2-7 fail (partial failure - agent wrote chunks but plan is structurally incomplete):** Report the specific failures to the user:

> "The planning agent produced a plan, but it has structural issues:
>
> 1. [failure text]
> 2. [failure text]
> ..."

Use **AskUserQuestion**:
```
question: "How should we handle these plan issues?"
header: "Plan validation"
options:
  - label: "Retry planning"
    description: "Re-launch the planning agent for this story"
  - label: "Fix manually"
    description: "I'll review and fix the plan issues in the story file"
  - label: "Proceed anyway"
    description: "Accept the plan as-is and move to triage"
```

**If "Retry planning":** Re-invoke the plan-chunks-agent (return to S-1). Include in the retry prompt: "Previous plan attempt had structural issues: [failure list]. Ensure the plan includes a ## The Pitch section (sell + conditions table using the exact headers `| Condition | Secured by |`, every row tagged verified / system-owned / unverifiable), a ## Investigation narrative, refined ## Acceptance criteria (5+ specific items), chunks_total in 2-7 range, and every chunk has Goal, Files, Contracts (every line receipted), and Test cases. Every chunk's Done When must assert the project builds and all tests pass at that checkpoint. Rename and removal work must update ALL call sites - including test files, mocks, and fixtures - within the same chunk; if that cannot fit the chunk limits, flag the story for splitting instead of planning chunks that leave the tree broken between boundaries. The plan must also include a ## Acceptance Pre-Flight table - one row per acceptance vehicle, no UNREACHABLE verdicts (see references/acceptance-walkthrough.md). Risk Tags descriptions must name the implementation mechanism - bare threshold values with no mechanism wording are flagged by check #8."

**If "Fix manually":** Acknowledge and end - the user will edit the story file directly and re-invoke planning when ready.

**If "Proceed anyway":** Continue to S-3 with the plan as-is. Note the validation gaps in the triage presentation so the user is aware.

### S-3: Interactive Triage

The agent has written the story file and returned flagged concerns, decisions, and validation results. Your job is to triage the concerns summary with the user — surface what needs human judgment.

**Before constructing any triage AskUserQuestion (Steps 1-5), Read `${CLAUDE_PLUGIN_ROOT}/commands/references/auq-grammar.md` and mirror the worked gate that matches the question** - a decision weighing alternatives is a fork; a fact that decides itself is a dead end. The exemplar carries the whole grammar (question field, option shapes, header chip); mirror it rather than reconstructing it from a summary. The grammar governs how options read; it never changes which outcomes an option set offers.

**Answer-time write:** after each answered triage question (Steps 1-5), apply that answer's edit to the story file immediately - per the write rules in `${CLAUDE_PLUGIN_ROOT}/skills/plan-chunks/references/batch-triage.md` ("Story File Writing") - then print one truthful receipt line before the next question renders. A real edit names what changed ("Updated Chunk 3: inline confirmation replaces modal"); a no-op answer prints "kept as planned" and makes no edit. Answers must survive a session that dies mid-triage.

**Step 1 — Critical Blockers:**

If the concerns summary's Critical Blockers section has entries, surface them immediately before anything else:

> "[Story Name] has a blocker: [blocker description]. [Agent's recommendation]."

Use **AskUserQuestion** per blocker, mirroring the exemplar's fork gate. If the blocker means the story can't be planned, stop and report why. (A blocker with no live alternatives is a dead end - mirror the dead-end gate and ask the story-fate question.)

**Step 2 - Flagged Concerns:**

Review the Flagged Concerns table. Surface by confidence level - **each concern gets its own individual AskUserQuestion** (the anti-collapse principle applies here too):

- **Low confidence:** Individual AskUserQuestion with agent's recommendation + alternative
- **Medium confidence:** Individual AskUserQuestion with "(Recommended)" label + alternative + "Accept as-is"
- **High confidence:** Informational only - include in plan presentation as "Risks Acknowledged," don't surface during triage

**Step 3 — Design Decision Validation:**

Review the Design Decision Validation table from the concerns summary. If any entries are `concern` or `invalid`:

Use **AskUserQuestion**:

```
question: "[The design decision, what the codebase showed, and the ask - self-contained, e.g. 'The story locked X, but planning found Y - adjust to the agent's fix, or keep X?']"
options:
  - label: "Adjust: [agent's proposed fix] (Recommended)"
    description: "[Why original doesn't work + how this solves it]"
  - label: "Keep original anyway"
    description: "[The honest cost of keeping it, in a phrase]"
```

If all decisions validated as `valid` → proceed with no interaction.

**Don't silently "fix" design decisions.** Surface them explicitly so the user stays in control.

**Step 4 — Clarification Decisions:**

Review the Decisions Made table from the concerns summary. Route by the **Product-stake** column (the agent already applied the low-confidence bump):

- **ask** → individual AskUserQuestion per decision, regardless of the agent's confidence. The question text must be self-contained: what was decided, what it trades off for the user, the agent's reasoning.

Use **AskUserQuestion**:

```
question: "[The decision and its user-facing consequence — self-contained]"
options:
  - label: "[Agent's decision] (agent recommends)"
    description: "[Agent's reasoning]"
  - label: "[Alternative]"
    description: "[Different approach]"
```

- **mention** → no question. Collect into the "Decisions you'd want to know" block of the plan presentation (S-4) — the "cool, that's nice" tier.
- **silent** → table only. No surfacing.

(Old-format summaries without a Product-stake column: fall back to confidence routing — low asks, medium/high proceed.)

**Step 5 — Cycle Impact:**

Check the Cycle Impact section from the concerns summary. If any item is non-"none":

Use **AskUserQuestion**:

```
question: "[The cycle impact and its consequence - self-contained, e.g. 'Planning found this story is really three: A, B, C - split it, or continue as one?']"
options:
  - label: "Split this story"
    description: "Actually 2-3 stories: [brief list]"
  - label: "Reorder stories"
    description: "This needs [X] done first"
  - label: "Add new story"
    description: "[New work] should be its own story"
  - label: "Continue as-is"
    description: "I understand, proceed anyway"
```

(Mark the option matching the agent's recommendation "(Recommended)" and list it first; give each shown option an honest one-line verdict. Show only the options the impact actually argues for.)

**Fast path:** If no low-confidence items exist across all five steps → report "No risks or concerns flagged — plan looks clean." and skip straight to plan presentation. Don't create artificial interaction.

### S-4: Present Plan for Approval

**Read the story file** the agent wrote using the Read tool. Present the `## Chunks` section — this is the full plan with all implementation details. Do NOT present from memory or from the concerns summary.

### Format

```
## Implementation Plan: [Story Name]

**Total:** [N] chunks, [M] files

**Decisions you'd want to know:**
[Mention-tier decisions from the Decisions Made table — what the agent did for the user beyond spec]

**Risks Acknowledged:**
[High-confidence concerns from triage]

**File Impact:**
[From concerns summary's File Impact table]

---

### Chunk 1: [Name]
[Full details from the story file's ## Chunks section]

### Chunk 2: [Name]
[Full details from the story file's ## Chunks section]

...

---

Does this plan look complete?
```

Use **AskUserQuestion**:
```
question: "Does this implementation plan look complete?"
options:
  - label: "Yes, mark ready"
    description: "Plan is solid, approve the story"
  - label: "Explore creatively"
    description: "Invoke creative-spark to riff on the approach"
  - label: "More detail on a chunk"
    description: "A chunk needs more specifics"
  - label: "Adjust the approach"
    description: "I want to change something"
```

### S-5: Finalize Story

The agent already wrote the story file with full detail. Your job depends on the user's response:

**If "Yes, mark ready":**

Triage answers already landed in the story file at answer time (S-3's answer-time write), so this is a status flip plus final reconciliation - verify nothing answered is missing, then:

```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/update-story-status.sh [story-file] ready
```

**If "Explore creatively":**

⛔ **DO NOT generate creative options directly. You MUST invoke the skill.** Write a breadcrumb before invoking to handle the skill-to-skill turn boundary:

```bash
cat > "${CRAFT_PROJECT_ROOT:-.}/.craft/.continuation" << CRUMB
ACTION: Re-present plan for approval after creative-spark completes
SKILL: craft:plan-chunks
ARGS: [story-file-path] DIRECTION_CONFIRMED: true
WRITTEN_BY: plan-chunks
TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%S)
CRUMB
```

Then invoke:
```
Skill tool:
  skill: "craft:creative-spark"
  args: "[story name] — Exploring implementation approach creatively.
  STORY: [story-name]"
```

After creative-spark completes, re-present the plan for approval.

**If "More detail on a chunk":**

Read the story file, discuss the specific chunk with the user, then make targeted edits to that chunk section only. Re-present for approval.

**If "Adjust the approach":**

Read the story file, discuss changes with the user, then make targeted edits based on their feedback. Re-present for approval.

**If "This is too big":**

Discuss splitting with the user. If splitting, create new story files and redistribute chunks across them.

### S-6: Offer Implementation

After the story is marked `ready`, offer to start implementation:

Use **AskUserQuestion**:
```
question: "Story is ready to implement. Start now?"
options:
  - label: "Yes, implement now"
    description: "Begin implementing chunk by chunk"
  - label: "Plan another story first"
    description: "Keep planning before implementing"
  - label: "Come back later"
    description: "I'll implement later"
```

**If "Yes, implement now":**

⛔ **DO NOT implement directly. You MUST invoke the skill:**

```
Skill tool:
  skill: "craft:craft-story-implement"
  args: "[story-file-path]"
```

This hands off to the implementation workflow which will invoke the `implementer` agent for each chunk.

**If "Plan another story first":**
→ Return to cycle planning flow

**If "Come back later":**
→ Acknowledge and end

---

## Multi-Story Planning

This path is triggered when `MODE: batch` is in args. It plans all `status: planning` stories in the cycle in parallel.

### M-1: Detect & Prepare Stories

1. Read the cycle directory from `CYCLE:` arg
2. List all stories: Glob `"[cycle_dir]/stories/*.md"` → story files
3. Read frontmatter of each — filter to `status: planning` only
4. If no planning stories found → report "No stories need planning in this cycle." and exit
5. If only 1 planning story → switch to single-story path (no batch overhead needed)
6. **Content spark check:** For each planning story, check whether it has a `## Content Direction` section with non-empty content. If ANY stories are missing it, report them: "These stories haven't been through content-spark yet: [list]." Use **AskUserQuestion**:
   ```
   question: "[N] stories are missing Content Direction. Run content-spark on them before planning?"
   header: "Prerequisite"
   options:
     - label: "Run content-spark first (Recommended)"
       description: "Invoke content-spark on each missing story before batch planning"
     - label: "Skip and plan anyway"
       description: "Plan without content direction - chunks may make content assumptions"
   ```
   **If "Run content-spark first":** Read and execute the logic inline for each missing story (same pattern story-new uses - avoids the chain-break that nested Skill invocation causes):

   ```
   Read "${CLAUDE_PLUGIN_ROOT}/commands/references/content-spark-inline.md"
   Execute the phases described in that file against each missing story sequentially.
   ```

   After all complete, continue.
   **If "Skip":** Continue.
7. Build sibling context: for each story, read first 30 lines (frontmatter + spark). Create a summary list: `[story-name]: [spark first sentence]`
8. Read cycle goal from `cycle.yaml`
9. Report to user: "Found [N] stories to plan in [cycle name]. Analyzing dependencies..."

### M-1b: Build Dependency Graph

Parse dependencies from each planning story to determine which can plan in parallel.

1. For each planning story, read the `## Dependencies` section:
   - **HARD BLOCK:** If any story is missing the `## Dependencies` section entirely, or has no `**Blocked by:**` line, STOP. Do not proceed with batch planning. Report: "Story [name] has no dependency declaration. Dependencies must be filled in before batch planning - without them, stories may plan in parallel when they share files, causing stale plans that require full replan and reimplement." Use AskUserQuestion to let the user fill them in or cancel.
   - Extract the `**Blocked by:**` line
   - Parse story names and statuses. Handle all real-world variations:
     - `"none"` or `"None"` → no blockers
     - `"story-name"` → single blocker
     - `"story-name (complete)"` → single blocker, already done
     - `"story-1, story-2 (complete)"` → comma-separated list with mixed statuses

2. **Verify Likely Files exist (CODE RED gate):**

   For each planning story, check for a `## Likely Files` section:
   - **CODE RED:** If ANY story in the batch is missing `## Likely Files` entirely, HARD STOP. Do not proceed.
   - Report: "**CODE RED: Story [name] has no Likely Files scan.** The orchestrator never checked which files this story touches. Dependency declarations cannot be verified - parallel planning could produce conflicting plans that require full replan and reimplement."
   - Use **AskUserQuestion**:
   ```
   question: "Story [name] has no Likely Files scan. Cannot verify dependencies."
   header: "CODE RED"
   options:
     - label: "Scan now"
       description: "Read the spark and scan the codebase for likely files"
     - label: "Cancel batch"
       description: "Fix story files manually before batch planning"
   ```
   - **If "Scan now":** Read the story's Spark and Scope, grep/glob the codebase for matching files, write the `## Likely Files` section to the story file (same format as story-new: dated, action-tagged). Then continue.
   - **If "Cancel batch":** Stop. Do not proceed with batch planning.

3. **Verify "Blocked by: None" declarations via file overlap:**

   For each story that declares `Blocked by: None` (or `none`):
   1. Read its `## Likely Files` section. Extract all files tagged `modify` or `create`.
   2. Compare against every OTHER story in the batch's `modify`/`create` files.
   3. If ANY file appears in both stories' modify/create lists - that's an overlap. Flag it:

   Use **AskUserQuestion** per overlap:
   ```
   question: "[Story X] and [Story Y] both plan to modify `[file]`. [X] declares no blockers. Which depends on which?"
   header: "Overlap"
   options:
     - label: "[X] blocked by [Y]"
       description: "Plan [X] after [Y]"
     - label: "[Y] blocked by [X]"
       description: "Plan [Y] after [X]"
     - label: "Truly independent"
       description: "I've verified these changes don't conflict"
   ```

   - **If user picks a direction:** Update the story's `**Blocked by:**` line in the story file. Continue to step 4 with the updated dependency.
   - **If "Truly independent":** Update `**Blocked by:**` to `None - verified independent (overlap with [other story] reviewed on [date])`. This prevents re-asking on future batch runs.

   If a `Blocked by: None` story has zero file overlaps with all other stories in the batch: update to `Blocked by: None - verified (no file overlap with batch stories)`. No AskUserQuestion needed.

4. Build the dependency graph:
   - **Ignore** blockers that are `(complete)` or not in the current planning set — completed/external dependencies don't constrain planning order
   - **Keep** blockers that are other `planning` stories in this batch — these create sequencing constraints

5. Assign stories to **topological levels** (parallel batches):
   - **Level 0:** Stories with zero in-set blockers → plan first (all parallel)
   - **Level 1:** Stories blocked only by Level 0 stories → plan after Level 0 completes
   - **Level N:** Stories blocked only by Level N-1 or earlier → plan after Level N-1 completes
   - **Circular dependency:** If any story can't be assigned to a level (mutual blocking), flag it: "Stories [A] and [B] have a circular dependency — resolve before planning." Exclude from batching and report to user.
   - **No `## Dependencies` section:** Treat as zero blockers (Level 0)

   **WHY levels must plan sequentially - this is NOT about implementation order:**

   Planners make *contract decisions* - hook IDs, file paths, export names, state management locations, message formats, shared constants. These decisions are not in the codebase yet. A downstream planner that runs without seeing its predecessor's plan will invent its OWN versions of these contracts. The result: duplicate state managers, inconsistent IDs, conflicting file ownership, and manual patching after the fact.

   This is not a theoretical risk. It has caused 5+ structural alignment issues across two projects when dependency levels were planned in parallel. Sequential planning is the fix - each level's planners see the completed plans from the level before, so contract decisions propagate forward.

   **DO NOT rationalize around this.** "Planning is different from implementation" is wrong - planning IS where contracts are defined. If the dependency graph produces 4 levels with 1 story each, that means 4 sequential planning rounds. Accept the time cost.

6. Estimate planning time: each level takes ~8 minutes (stories within a level plan in parallel, but triage and level transitions add overhead). Estimate = `[L] levels × ~8 min`. For a single level with many stories, still use ~8 min (parallel execution). Include this in the report.

7. Report the batch plan to the user:
   > "Dependency analysis: [N] stories in [L] levels. Estimated time: ~[L × 8] minutes.
   > - Level 1 ([M] stories, parallel): [story names]
   > - Level 2 ([M] stories, parallel): [story names] - after level 1
   > Launching level 1..."

### M-2: Launch Planning Agents

#### Mode: Agent Teams (when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is `1`)

> **Details:** Read `${CLAUDE_PLUGIN_ROOT}/skills/plan-chunks/references/team-planning.md` for agent teams spawn templates, monitoring patterns, and result collection.

1. Use the dependency graph levels from M-1b as your batches
2. For each level (starting from Level 0):
   - Create agent team teammates, one per story in this level
   - Each teammate receives: planning instructions (reference plan-chunks-agent approach), story path, cycle context (goal + all sibling names/sparks), project root, **sibling Likely Files** (for each other story in this level, include its name and `## Likely Files` content so the agent can detect file overlap)
   - **Each teammate's prompt MUST include:** "After planning, WRITE the updated story file directly using the Write tool. Keep status: planning — the orchestrator handles approval. Then return ONLY your concerns summary as your final output — do NOT include the full plan report."
   - Teammates can coordinate via messaging (file overlap, dependency awareness)
3. **WAIT for all teammates in the current level to complete before launching the next level.** DO NOT launch Level 1 while Level 0 is still running - Level 1 stories depend on Level 0 plans for contract alignment.
4. **Predecessor Context Handoff:** Before launching the next level, build predecessor context for each story in that level (see Predecessor Context Handoff below).
5. Report progress: "Level 0 complete: [story names]. Starting Level 1..."
6. Continue until all levels done

#### Mode: Task Subagents (fallback - no agent teams)

1. Use the dependency graph levels from M-1b as your batches
2. For each level (starting from Level 0):
3. For each story in the current level, launch plan-chunks-agent subagents via Task tool. **CRITICAL: Always use `run_in_background: true`** so each agent's full output is persisted to a file on disk. This is essential — concerns summaries MUST survive context compaction.
   ```
   Task tool:
     subagent_type: "craft:plan-chunks-agent"
     description: "Plan [story-name]"
     run_in_background: true
     prompt: "Research and plan this story.

     **Story file:** [full path]
     **Cycle directory:** [path]
     **Project root:** [derived path]
     **PLUGIN_ROOT:** ${CLAUDE_PLUGIN_ROOT}   (inject the resolved value — the subagent cannot resolve ${CLAUDE_PLUGIN_ROOT} itself; it needs this to reach plugin-internal scripts like the Living Map runner)

     **FIRST ACTION — before reading any source file, pull your read plan:**
     [one literal command per scope directory, pre-computed from the story's Likely Files — resolved paths, ready to run:]
     [resolved PLUGIN_ROOT]/scripts/map/map-run.sh assemble [dir] --root [project root]
     Each slice line ends in [off=N,lim=M] — issue those ranged Reads at the narrowest useful span; never open a whole annotated file. An empty or floored slice for a directory = orient that area normally.

     CRITICAL: SCOPE ALL SEARCHES to the project root above.
     Do NOT search the monorepo root or parent directories.
     Use the project root as the `path` parameter for ALL Glob and Grep calls.

     **Cycle goal:** [goal from cycle.yaml]

     **All stories in cycle (for sibling awareness):**
     [story-name-1]: [spark first sentence]
     [story-name-2]: [spark first sentence]
     ...

     **Sibling Likely Files (for file overlap detection):**
     [For each OTHER story in this planning level, include its name and Likely Files content.
      The agent uses this to detect modify/create overlap and flag dependency concerns.]
     [story-name-1]:
       - `path/file.ext` - modify
       - `path/other.ext` - create
     [story-name-2]:
       - `path/file.ext` - modify
     ...

     If the story has a `## Content Direction` section, use it as authoritative content decisions — reference specific items, labels, data shapes, and priorities from it in your chunk implementation details.

     Read the story, understand what it needs, then research the codebase and plan chunks.
     After planning, WRITE the updated story file directly using the Write tool.
     Keep status: planning — the orchestrator handles approval.
     Then return ONLY your concerns summary as your final output — do NOT include the full plan report.

     BATCH MODE: PLAN FORK is unavailable — decide down your recommended branch, set
     product-stake 'ask', and record the fork as a Critical Blocker for triage."
   ```
4. Each Task tool result includes an `output_file` path. **Record each path** in a simple registry: `{story-name: output_file_path}`. These paths are tiny (~50 bytes each) and survive compaction. The files themselves are on disk.
5. Use `TaskOutput` to wait for each background agent to complete. **WAIT for all subagents in the current level to complete before launching the next level.** Level 1 stories depend on Level 0 plans for contract alignment.
6. **Predecessor Context Handoff:** Before launching the next level, build predecessor context for each story in that level (see Predecessor Context Handoff below).
7. Report progress: "Level 0 complete: [story names]. Starting Level 1..."
8. Continue until all levels done

#### Predecessor Context Handoff

Before launching Level N+1, build predecessor context for each story in that level:

1. For each story in Level N+1, identify its in-set blockers (the stories it depends on)
2. For each blocker, read the **completed story file** (not the concerns summary) using the Read tool
3. Extract each chunk's **Goal**, **Files**, and **Contracts** sections only. Strip **Approach**, **Test cases**, **What Could Break**, and **Done When** - contracts are the only cross-story binding surface; the rest is interior detail the next planner must not couple to. Do NOT modify the story file - this is a read-and-extract operation for prompt building only.
4. Include ONLY the immediate predecessor's chunks - not the entire chain. Each plan already incorporates awareness of its own predecessors, so context is transitive.

Add to the agent prompt for each Level N+1 story:

```
**Predecessor plan (MUST align with - do not duplicate or contradict):**

Story: [predecessor name]
Status: planned (chunks written, not yet implemented)

### Chunk 1: [Name]
**Goal:** [from predecessor]
**Files:** [from predecessor]
**Contracts:** [from predecessor]

### Chunk 2: [Name]
...

CRITICAL: This predecessor's plan defines contracts you MUST respect:
- Use the same IDs, naming conventions, and formats
- Do not re-implement functionality the predecessor already covers
- Reference the predecessor's files and exports - do not create parallel versions
- If you need something the predecessor doesn't provide, ADD to it (note in your concerns) - don't duplicate
```

If a story has multiple predecessors (converging dependencies), include each as a separate predecessor context block.

**The output file paths contain concerns summaries (lightweight metadata).** The agents also wrote story files directly — the story files contain the full plans. Every time you need the full plan (BT-5 approval), read the story file. Every time you need metadata (M-3 validation, BT-1 overview), read the output file. NEVER rely on conversation memory. This follows the same pattern used by ultrawork/ralph (oh-my-claudecode) and OmO's "Context Pack" approach: file-based persistence for multi-agent output, not conversation memory.

### M-3: Collect & Validate Concerns Summaries

Validate each agent's output **one at a time** by reading from output files. Do NOT load all into context simultaneously.

For each story in your output file registry:
1. **Read the output file** using the Read tool (the path from M-2 step 4) — this is the concerns summary
2. **Validate concerns summary:** non-empty, has `## Overview` section with `Story file:` path
3. **Validate story file was written:** Read the story file path from the `Story file:` field. Use Read tool to check it has a `## Chunks` section and `chunks_total > 0` in frontmatter. If the story file wasn't updated (no `## Chunks` section), mark as failed — "agent didn't write story file". While the story file is open, run the S-2 Step 2 structural check table against it (one story at a time - do not hold multiple plans in context). A plan that fails any structural check (including check #6, the green-tree Done When criterion) is marked failed with the check's failure text
4. **Extract lightweight metadata** from concerns summary — story name, chunk count, file count, concern count, and the `## File Impact` table. Do NOT hold the full plan in memory — you'll read the story file fresh in BT-5.
5. Note any failures with reason
6. Move to the next story

After validating all reports, build the **cohesion check** from the lightweight metadata:

**Subagent mode only — Post-hoc Cohesion Check:**

Using the extracted File Impact tables (lightweight — just file paths and actions):
- **File overlap:** Flag if the same file appears in multiple stories: "[file] touched by stories A and B — verify no conflict during implementation"
- **Component overlap:** Flag if multiple stories create similar components: "Stories A and B both create [component type] — consolidate into shared component?"
- **Decision conflicts:** Flag if stories made different decisions for the same concern: "Story A chose X, Story B chose Y for [concern]"
- Note issues as additional concerns to surface during batch triage

**Agent teams mode — Coordination Review:**
- Review Teammate Coordination Notes from each agent's output
- Surface any unresolved coordination items (file conflicts, component overlap the agents detected but couldn't resolve)

### M-4: Failure Handling

If any agents failed:
- Note failure reason for each
- Report: "[N] of [M] stories planned successfully. [failed story names] need retry."
- Use **AskUserQuestion**:
  ```
  question: "[F] stories failed to plan. What should we do?"
  options:
    - label: "Retry failed stories"
      description: "Re-launch as single-story planning (interactive, higher quality for problematic stories)"
    - label: "Skip them for now"
      description: "Proceed with the [N] successful plans"
    - label: "Retry all"
      description: "Re-plan everything from scratch"
  ```

If "Retry failed stories" → queue for single-story planning (S-1 through S-6) after batch triage
If "Skip them for now" → proceed with successful plans only
If "Retry all" → re-launch the full batch (M-2)

### M-5: Hand Off to Batch Triage

Pass the lightweight metadata and output file registry to the batch triage flow.

---

## Batch Triage

> **Full flow details:** Read `${CLAUDE_PLUGIN_ROOT}/skills/plan-chunks/references/batch-triage.md` for AskUserQuestion templates, concern tier definitions, cohesion heuristics, and edge cases.

The batch triage flow (BT-1 through BT-7) reviews all plans with the user after parallel agents complete. The core principle:

**Every concern gets its own AskUserQuestion.** Never summarize concerns as a text list with a single "All good?" approval. This is the most important behavioral guardrail in the entire skill - it exists because batching concerns leads to silent soft-approval by omission. If there are 5 concerns across 3 stories, that means 5 separate AskUserQuestion calls.

### Flow Summary

| Phase | What | Key Behavior |
|-------|------|-------------|
| **BT-1** | Overview | Count concerns by tier. Fast path if zero needs-review AND zero worth-noting. |
| **BT-2** | Needs Review (ask-tier product-stake, or low confidence) | Individual AskUserQuestion per item, grouped by story. |
| **BT-3** | Worth Noting (mention-tier product-stake, or medium confidence) | Presented visibly per story; questions only where the user reacts. |
| **BT-4** | Cohesion/Coordination | Surface file overlaps, component duplication, decision conflicts. AskUserQuestion per issue. |
| **BT-5** | Per-Story Approval | Read story file fresh. Present ONE story at a time. Never hold two plans in context. Each gets Approve/Explore/Adjust/Reject. |
| **BT-6** | Finalize | Reconcile - triage adjustments already landed at answer time; verify consistency, update status to ready. Queue adjusted stories for re-planning. |
| **BT-7** | Summary | Report counts, offer implementation or re-planning. |

### Critical Rules

- **BT-5: Read story files fresh** - use the Read tool, not memory or concerns summaries
- **BT-5: Sequential only** - present one story, wait for response, then read the next
- **BT-5: "Explore creatively"** invokes `craft:creative-spark` via Skill tool (never generate options inline). Write a breadcrumb before invoking to handle the skill-to-skill turn boundary.
- **BT-6: "Approve"** runs `update-story-status.sh [story-file] ready`
- **BT-7: "Start implementing"** invokes `craft:craft-story-implement` via Skill tool (never implement directly)

---

## Reference Notes

### Chunk Size Guidelines

| Complexity | Chunks | Files/Chunk |
|------------|--------|-------------|
| Simple | 2-3 | 1-2 |
| Medium | 3-5 | 2-4 |
| Large | 5-7 | 2-5 |

**Hard limit: 7 chunks.** More than that → split the story.

### Testing Pattern (Always)

Each chunk includes tests for what it implements. Every chunk must end with all tests passing.

**Do NOT create a separate "write tests" chunk.** Tests belong in the same chunk as the code they verify. A chunk is self-contained: implement + test + validate.

These guidelines are built into the plan-chunks-agent. They're here for reference when reviewing agent output.

---

## Remember

- **Never auto-invoke** — this skill requires explicit user request. Phase 0.5 enforces this via AskUserQuestion. Callers pass `DIRECTION_CONFIRMED: true` to skip when they've already confirmed.
- **Quality is unchanged** — single-story planning has the same interactive triage quality as before
- **Agent does research + planning** — you orchestrate and triage, you don't plan inline
- **Surface risks early** — triage agent concerns before approving the plan
- **One question at a time** (single-story triage) — don't overwhelm with unknowns
- **Batch mode trades interaction for speed** — user can always re-plan individual stories interactively
- **Cycle stays coherent** — review agent's cycle impact findings
- **User approves the plan** — explicit confirmation required for every story
- **Status changes to ready** — story can now be implemented
- **Fallback always works** — if agent teams unavailable, subagent path works independently. If agents fail entirely, fall back to manual planning inline.
- **Full details or nothing** — vague chunks lead to vague implementation. The agent handles this, but verify during triage.

Your goal: Coordinate planning agents and help the user review their output — ensuring the same "here's EXACTLY how we'll build this" quality, now at parallel speed.
