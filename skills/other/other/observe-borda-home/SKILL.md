---
name: observe
description: Analyzes ongoing work patterns and the existing agent/skill roster to suggest creating new agents or skills for specialized or repetitive tasks. Continuously monitors what tasks are being done repeatedly or where specialist knowledge would help. Avoids recommending duplicates.
argument-hint: '[review | prune | "<recurring task description>"]'
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

<objective>

Analyze how Claude Code is being used in this project and suggest new agents or skills that would reduce repetition, improve quality, or handle specialized domains — without duplicating what already exists.

</objective>

<inputs>

- **$ARGUMENTS**: optional. Four modes:
  - Omitted — analyze the project's existing patterns and agents to generate suggestions proactively.
  - `review` — review the existing agent/skill roster for quality and gaps without suggesting new additions.
  - `prune` — evaluate the project memory file for stale, redundant, or verbose entries and apply a trimmed version.
  - Description of a recurring task — use the description as context when generating suggestions (e.g. "I keep doing X manually").

</inputs>

<workflow>

## Step 1: Inventory existing agents and skills

Use the Glob tool to enumerate agents (pattern `agents/*.md`, path `.claude/`) and skills (pattern `skills/*/SKILL.md`, path `.claude/`).

For each agent/skill found, extract: name, description, tools, purpose.

## Step 2: Analyze work patterns

**If `$ARGUMENTS` is `prune`**: skip Steps 2–5 entirely and go to "Mode: Memory Pruning" below.

**If `$ARGUMENTS` is `review`**: skip the git analysis below and go directly to Step 3 (Gap analysis). Use the agent/skill descriptions from Step 1 as the sole input — the goal is to assess quality and coverage of the existing roster, not to look for new patterns in recent work. In Step 5, suppress all "Recommend: New Agent/Skill" sections and output only "Existing Coverage", "Recommend: Enhance Existing", and "No Action Needed" entries.

Otherwise, look for signals of repetitive or specialist work. The first three git commands are independent — run them in parallel:

```bash
# --- run these three in parallel ---

# Recent git history — what kinds of changes are common?
git log --oneline -50

# What file types are being worked on?
git log --name-only --pretty="" -30 | sort | uniq -c | sort -rn | head -20

# Commit message patterns — what verbs appear most?
git log --oneline -100 | awk '{print $2}' | sort | uniq -c | sort -rn | head -15
```

Then use the Read tool on `tasks/todo.md` and `tasks/lessons.md` (if they exist) for task history and conversation hints.

If `$ARGUMENTS` was provided, use it as additional context for the pattern analysis.

### Frequency Heuristics

- **3+ occurrences** of a pattern in recent history → candidate for automation
- **2+ different projects** using the same manual process → cross-project skill
- **> 10 minutes** of manual work per occurrence → high-value automation target
- **Domain-specific knowledge** required → candidate for a specialist agent (not just a skill)

## Step 3: Gap analysis

For each identified pattern, check:

1. **Is it already covered?** — search existing agent/skill descriptions for overlap
2. **Is it frequent enough?** — recurring ≥ 3 times or clearly domain-specialized
3. **Would a specialist add quality?** — does it require deep domain knowledge?
4. **Is it too narrow?** — a single-use task doesn't warrant a persistent agent

Thresholds for recommendation:

- **New agent**: recurring specialist role, complex decision-making, 5+ distinct capabilities
- **New skill**: workflow orchestration, multi-step process with fixed structure
- **No new file needed**: one-off or already covered by existing agent

## Step 4: Check for duplication

Before recommending anything, run through both the overlap check and the anti-pattern checklist:

```
For each candidate agent/skill:
- Does any existing agent cover >50% of its scope? → enhance existing instead
- Is the name/description confusingly similar to an existing one? → rename existing
```

Anti-pattern checklist — reject the candidate if any apply:

1. **Role vs task confusion**: agents are roles, not tasks. Do not create an agent for every different topic.
2. **Near-duplicate**: the candidate duplicates an existing agent with a slightly different name. Enhance the existing one instead.
3. **Thin wrapper**: the candidate skill just calls one agent with fixed args. That is not enough value to justify a new skill file. Exception: skills that add measure-first/measure-after bookends, multi-mode dispatch across 3+ agents, or safety breaks (retry limits, validation gates) justify the wrapper even if only one agent executes for a given invocation.

## Step 5: Report

```
## Agent/Skill Suggestions

### Existing Coverage (no gaps found)
- [agent/skill]: covers [pattern] well — no new file needed

### Recommend: New Agent — [name]
**Trigger**: [what recurring pattern or gap justifies this]
**Gap**: [what existing agents don't cover]
**Scope**: [what it would do — 3-5 bullet points]
**Suggested tools**: [Read, Write, Edit, Bash, etc.]
**Draft description**: "[one-line description for frontmatter]"

### Recommend: New Skill — [name]
**Trigger**: [what repetitive workflow justifies this]
**Gap**: [why existing skills don't cover it]
**Scope**: [what workflow steps it would orchestrate]
**Draft description**: "[one-line description for frontmatter]"

### Recommend: Enhance Existing — [agent/skill name]
**Add**: [specific capability missing from current version]
**Why**: [what recurring task would benefit]

### No Action Needed
[pattern]: already handled by [existing agent/skill]

## Confidence
**Score**: [0.N]
**Gaps**: [e.g., git history too shallow, task files not present, descriptions too generic to compare]
**Refinements**: N passes. [Pass 1: <what improved>. Pass 2: <what improved>.] — omit if 0 passes
```

## Mode: Memory Pruning (prune)

Locate, evaluate, and trim the project memory file.

**Find the memory file:**

```bash
PROJECT="$(git rev-parse --show-toplevel)"
MEMORY_FILE="$HOME/.claude/projects/$(echo "$PROJECT" | sed 's|/|-|g')/memory/MEMORY.md"
echo "$MEMORY_FILE"
```

Read the memory file with the Read tool. Also read `.claude/CLAUDE.md` to identify overlap — anything already covered in CLAUDE.md does not need to live in memory.

**Evaluate each section against these criteria:**

- **Drop**: content that is no longer accurate (removed features, resolved one-time issues, superseded decisions), or fully duplicated in CLAUDE.md
- **Trim**: sections still accurate but containing implementation history or rationale no longer needed day-to-day — keep operational facts (what/where), drop the why-it-was-built backstory
- **Keep**: rules actively applied every session; project-specific facts absent from CLAUDE.md; anything the model needs to act correctly

Apply changes with the Edit tool — targeted replacements for trimmed sections, full section removal for dropped ones.

Print a compact summary:

```
Pruned MEMORY.md — <date>
  Dropped: N sections — [names]
  Trimmed: N sections — [names]
  Kept:    N sections unchanged
  Saved:   ~N lines
```

End your response with a `## Confidence` block per CLAUDE.md output standards.

</workflow>

<notes>

- This skill is introspective: it looks at the tooling itself, not just the code

- Run periodically (e.g., monthly) or after noticing repetitive manual work

- Suggestions are proposals — always review before creating new files

- After creating a new agent/skill based on a suggestion, re-run this skill once to confirm the gap is resolved, then stop

- **Agent Teams signal tracking**: when reviewing patterns, also look for:

  - Skills using `--team` or team-mode heuristics more/less than expected → flag over/under-use relative to the decision matrix in `CLAUDE.md § Agent Teams`
  - Security findings appearing in reviews for non-auth code → suggests qa-specialist teammate scope is too broad; narrow it
  - Model tier mismatches (e.g., heavy analysis assigned to `sonnet` teammates) → flag for tier adjustment

- Follow-up chains:

  - Suggestion accepted for new agent/skill → `/manage create` to scaffold and register it
  - Suggestion to enhance existing → edit the agent/skill directly, then `/sync`

</notes>
