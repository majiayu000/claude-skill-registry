---
name: context-doctor
description: Audit CLAUDE.md/AGENTS.md for context bloat, duplication, and misplaced guidance. Use when agent docs feel too long, redundant, or slow the agent at startup.
---

# Context Doctor

Audit a project's documentation structure for context engineering best practices.
Finds waste, duplication, and misplaced content so agents spend tokens on work,
not re-reading redundant docs.

## Trigger cues (examples)

Use this skill when the user asks to:

- Audit/optimize `CLAUDE.md`, `AGENTS.md`, or `.claude/rules/`
- Reduce “agent reads too much at startup” / “context wasted on docs”
- Remove duplication across multiple `AGENTS.md` files
- Set up agent documentation for a new repo/monorepo

**Why this matters**: Every line in CLAUDE.md, AGENTS.md, and `.claude/rules/`
is loaded into the agent's context window. Bloated or duplicated docs mean agents
start every session with less room for actual work. This skill finds the waste
and tells you exactly what to move, merge, or delete.

## Audit Process

### Step 1: Run the Mechanical Checks

Run the audit script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/audit.sh"
```

If `CLAUDE_PLUGIN_ROOT` is not set, locate the skill directory from context and
run `scripts/audit.sh` from there. If the script isn't available, do these
checks manually with grep/wc.

This checks:
- CLAUDE.md line count (warn if >50 lines)
- `@import` validation (broken references)
- `.context/` gitignore check
- AGENTS.md file count
- Duplicated keywords across AGENTS.md files

### Step 2: Semantic Analysis

Read each AGENTS.md and CLAUDE.md file. Look for:

#### Duplication

Facts repeated across multiple files. Common offenders:
- "X is a stub/scaffold" appearing in both root and workspace AGENTS.md
- Read order / navigation instructions in multiple places
- Template surface lists duplicated across docs
- Command references (dev, build, test) in multiple files

For each duplicate, identify the **single source of truth** — the one file
where this fact naturally belongs. The others should reference it, not repeat it.

#### Misplaced Content

Content that's in the wrong file:
- **Workspace-specific guidance in root CLAUDE.md** — should be in
  `.claude/rules/` with `paths:` frontmatter so it only loads when relevant
- **Behavioral rules in AGENTS.md** — should be in `.claude/rules/`
- **Commands and env vars in docs/** — should be in root AGENTS.md

#### Bloat

Content that shouldn't be in always-loaded context at all:
- Long explanations derivable from reading the code
- Historical context that's in git history
- Verbose examples when a one-liner would do
- README content that serves human readers, not agents

### Subagent Strategy

For repos with >5 AGENTS.md files, delegate the semantic duplication analysis
to a read-only subagent (Haiku model, read-only tools):

1. Spawn subagent with: Read, Grep, Glob tools
2. Task: "Read all AGENTS.md files and identify duplicated facts, concepts
   repeated verbatim or paraphrased across multiple files"
3. Subagent returns a deduplication report
4. Use the report to generate findings in the main conversation

This keeps verbose file contents out of the main context window.

### Step 3: Generate Report

Output a structured report:

```markdown
# Context Doctor Report

## Summary
- X AGENTS.md files found
- CLAUDE.md is Y lines (target: <50)
- Z duplicated facts found
- N broken @imports

## Findings

### Critical (fix now)
- [finding with specific file:line references]

### Recommended (improve quality)
- [finding with specific suggestions]

### Optional (nice to have)
- [finding]

## Suggested Actions

1. [Specific action with before/after]
2. [Specific action]
```

### Step 4: Offer to Fix

After presenting the report, ask if the user wants you to apply the
recommendations. If yes, make the changes.

### Step 5: Verify Fixes

After applying changes, re-run the audit script to confirm improvements.
Report before/after metrics (e.g., "CLAUDE.md: 120 lines → 42 lines").
If new issues are found, iterate until the report is clean.

## What Good Looks Like

For project-type-specific patterns, see [references/doc-patterns.md](references/doc-patterns.md).

**CLAUDE.md** (~20-50 lines):
- Navigation pointers (read AGENTS.md first, then docs/)
- Project-specific rules the agent can't derive from code
- `@import` references for lazy-loaded context

**Root AGENTS.md** (topology + routing):
- Workspace map (what lives where)
- Commands (dev, build, test, lint)
- Env vars and secrets
- Commit conventions

**Workspace AGENTS.md** (per-package):
- What this package does (one paragraph)
- Key files and their roles
- Package-specific patterns or gotchas

**.claude/rules/** (conditional context):
- Path-scoped rules that only load when working in specific directories
- Example: tRPC patterns only load when touching `packages/trpc/**`

## Anti-patterns

- **CLAUDE.md as a novel**: If it's over 50 lines, most of it should move
- **Copy-paste AGENTS.md**: If two files say the same thing, one should reference the other
- **Everything in root**: Use workspace-level AGENTS.md for package-specific context
- **Rules without paths**: `.claude/rules/` files without `paths:` frontmatter load globally
