---
name: epost
description: (ePost) Use when user intent is ambiguous, spans multiple workflows, or is not matched by a specific skill — performs intent detection and routes to the correct specialist (plan, cook, fix, audit, git, docs)
user-invocable: true
context: fork
agent: epost-project-manager
metadata:
  argument-hint: "[what you want to do, or leave blank for contextual menu]"
---

# Smart Hub v2 — `/epost`

The intelligent entry point to the epost agent ecosystem. Senses your current work context, detects intent from natural language, chains multi-step workflows, and shows contextual suggestions.

## Execution Flow

On every invocation, follow these steps **in order**:

### Step 1: Gather Context Snapshot

**Before parsing arguments**, follow the `hub-context` Context Snapshot Protocol to gather git state, platform detection, error signals, and session hints. Produce the context summary format defined there.

### Step 2: Parse Intent from Arguments

If `$ARGUMENTS` is empty → skip to Step 4 (Contextual Discovery Menu).

Otherwise, classify the request using **semantic intent categories**:

#### Intent Categories

| Category | Signal Words | Context Boost | Routes To |
|----------|-------------|---------------|-----------|
| **Build** | cook, implement, build, create, add, scaffold, make, continue | Has plan file → boost | `/cook` or orchestrator |
| **Fix** | fix, debug, error, crash, broken, failing, wrong, what's wrong | Has error signals → boost | `/fix` (auto-detects error type) |
| **Plan** | plan, design, architect, think about, spec, roadmap | Complex request → boost | `/plan` (auto-detects complexity) |
| **Test** | test, coverage, validate, verify, check tests, run tests | Has test failures → boost | `/test` (auto-detects platform) |
| **Review** | review, check code, audit, look at, inspect | Has staged changes → boost | `/review` (auto-detects variant) |
| **Git** | commit, push, pr, merge, branch, release, done, ship | Has staged changes → boost | `/git` (auto-detects action) |
| **Docs** | docs, document, write docs, readme | — | `/docs` (auto-detects init vs update) |
| **Explore** | scout, search, find, explore, where is, show me | — | `/scout` skill |
| **Knowledge** | which agent, list agents/skills/commands, what's our, convention, kit, our agents, our skills, what rag | Internal ref | `epost-project-manager` |
| **Components** | what components, search components, find component, design tokens | RAG query | `epost-project-manager` |
| **Research** | research, what is [external tech], how does [external tech], best practice for [tech] | External tech ref | `epost-researcher` |
| **A11y** | a11y, accessibility, wcag, screen reader, voiceover | — | `/a11y` (auto-detects variant) |
| **Brainstorm** | brainstorm, evaluate, compare, think about options, weigh | — | `epost-brainstormer` |
| **Guide** | guide, help me, how do I, wizard | — | Show discovery menu or `epost-project-manager` |
| **Convert** | convert, prototype, migrate | — | `/convert` |
| **Bootstrap** | bootstrap, init, scaffold new | — | `/bootstrap` (auto-detects scope) |

#### Context Boost Rules

When context signals match a category, that category gets priority **even with weaker keyword matches**:

| Context Signal | Boosts Category | Example |
|---------------|----------------|---------|
| TypeScript/build errors detected | Fix | "what's wrong?" → `/fix` (auto-detects types) |
| Staged files present | Git or Review | "I'm done" → `/git --commit` |
| Active plan file exists | Build | "continue" → `/cook --fast` with plan |
| Test failures detected | Fix | "help" → `/fix` (auto-detects test failures) |
| Feature branch, no changes yet | Build or Plan | "what's next?" → resume from plan |
| Clean main branch, no work | Plan or Explore | show contextual menu |
| Merge conflicts | Fix | "help" → suggest conflict resolution |

#### Knowledge Question Routing

When the request is a question ("what is...", "how does...", "where is...", "show me...", "find..."):

**Answer directly** when asking about the kit itself (agents, skills, commands, hooks, conventions):
- Signals: "our agent", "which skill", "list commands", "what's our convention", "which agent handles X", "how does /cook work", "what skills exist"
- Action: Answer from context — no delegation needed

**Project overview questions** — check docs first, fall back gracefully:
- Signals: "what is this project", "what does this project do", "tell me about this project", "what is this repo", "what is this codebase", "give me an overview", "what are we building", "what does this do"
- Action (in order):
  1. Check if `docs/index.json` exists → if yes, read it + key ARCH/FEAT entries and synthesize a summary
  2. If no `docs/`, check README → summarize from README
  3. If no docs and no README → say: "No documentation found. Run `/get-started` to onboard — it will research the codebase, generate docs, and install dependencies."
- Example: "what is this project about?" → read docs/index.json or README, answer directly

**Route to `/scout`** when asking about project source code or codebase structure:
- Signals: "where is", "find the", "show me the code", "how is X implemented", "what does this file do", "search for", "which file", "where's the class/function/component", "how does the CLI work", "how does feature X work"
- Action: Delegate to `scout` skill — it explores files, traces patterns, searches across platforms
- Example: "where is authentication handled?" → `/scout`
- Example: "find the Button component" → `/scout`

**Route to `epost-researcher`** when asking about external tech:
- Signals: no project/kit reference + specific library, framework, or technology name
- Example: "how does JWT work?" → `epost-researcher`
- Example: "what is gRPC?" → `epost-researcher`

#### Fuzzy Matching

Don't require exact keyword matches. Use semantic understanding:
- "my tests are broken" → Fix (via "broken") + Test (via "tests"). Context boost breaks the tie.
- "I need to change the button" → Build (change ≈ modify ≈ implement)
- "what happened?" → context boost determines: if errors → Fix; if clean → Explore
- "I'm stuck" → if errors → Fix; if plan exists → Build; else → Guide

### Step 3: Detect Multi-Intent and Route

#### Multi-Intent Detection

Check for compound requests via conjunctions:

**Triggers**: "and", "then", "after that", "followed by", comma-separated action verbs, semicolons

| Pattern | Intent Chain | Delegation |
|---------|-------------|------------|
| "plan and build X" | [Plan, Build] | → orchestrator |
| "fix the bug then commit" | [Fix, Git] | → orchestrator |
| "test and review" | [Test, Review] | → orchestrator |
| "plan, implement, and test the feature" | [Plan, Build, Test] | → orchestrator |

**If multi-intent detected** → delegate to `epost-project-manager` with a structured handoff (see Orchestrator Delegation below).

#### Single Intent Routing

**If single intent detected:**

1. **Platform prefix check**: If `$ARGUMENTS` starts with `ios`, `android`, `web`, or `backend`, route to platform-specific command.
2. **Variant auto-selection** based on complexity:

| Complexity Signal | Variant |
|-------------------|---------|
| Single file + clear error | `:fast` |
| 2-5 files, one module | `:fast` |
| Multiple modules, some unknowns | `:deep` |
| Multi-platform or needs research | `:deep` or `:parallel` |
| Has existing plan with phases | `:parallel` (follow plan) |

3. **Route directly** to the matched command.

#### Routing Decision Report

**Always** show the user what you decided and why:

```
Routing to `/fix` — detected TypeScript errors on web platform (branch: feature/auth)
```

or

```
Delegating to orchestrator — multi-intent detected: [Plan, Build] for notification system (web)
```

### Step 4: Contextual Discovery Menu

When invoked with **no arguments**, show a context-aware menu instead of the static command list.

#### If active work detected (staged files, errors, plan):

```markdown
## Suggested Actions

You're on `{branch}` with {context_summary}.

| # | Action | Command | Why |
|---|--------|---------|-----|
| 1 | {most relevant action} | `{command}` | {reason from context} |
| 2 | {second action} | `{command}` | {reason} |
| 3 | {third action} | `{command}` | {reason} |
| 4 | {fourth action} | `{command}` | {reason} |

> Describe what you want to do, or type a number. Full command list: say "show all commands"
```

**Priority rules for suggestions:**
1. If merge conflicts → suggest fix/resolve first
2. If errors → suggest fix commands
3. If staged files → suggest commit or review
4. If active plan → suggest continuing implementation
5. If feature branch, no changes → suggest starting work or checking plan
6. Always include at least one "escape hatch" (explore, plan, help)

#### If clean state (main branch, no changes, no errors):

```markdown
## What do you want to do?

No active work detected on `{branch}`.

| Action | Command |
|--------|---------|
| Plan a feature | `/epost plan ...` |
| Build something | `/epost build ...` |
| Fix an issue | `/epost fix ...` |
| Explore codebase | `/epost scout ...` |
| Ask about the kit | `/epost which agent handles X?` |
| Research external tech | `/epost research ...` |

> Describe what you want to do in natural language.
```

#### Full command list (on "show all commands"):

```
### All Commands

| Category | Command | Flags |
|----------|---------|-------|
| Core Verbs | `/cook`, `/fix`, `/plan`, `/debug`, `/test`, `/bootstrap` | `--fast`, `--deep`, `--parallel`, `--ci`, `--ui`, `--validate` |
| Git | `/git` | `--commit`, `--push`, `--pr` |
| Docs | `/docs` | `--migrate`, `--scan`, `--verify`, `--batch` |
| Review | `/review` | `--code`, `--a11y`, `--improvements` |
| A11y | `/a11y` | `--audit`, `--fix`, `--review`, `--close` |
| Kit | `/kit` | `--add-agent`, `--add-skill`, `--add-hook`, `--optimize` |
| Onboarding | `/get-started`, `/epost` | — |
| Utilities | `/convert`, `/scout`, `/simulator` | — |
```

## Orchestrator Delegation

When delegating to `epost-project-manager`, provide a structured handoff:

```markdown
## Hub Handoff

**Original request**: "{user's exact words}"
**Intent chain**: [{Category1}, {Category2}, ...]
**Suggested commands**: [{/command1}, {/command2}, ...]
**Context**:
  - Branch: {branch_name}
  - Platform: {detected_platform}
  - Staged: {count} files
  - Errors: {summary}
  - Plan: {plan_file or "none"}
**Delegation reason**: {why hub can't handle directly — multi-intent / ambiguous platform / project-level}
```

**Delegation triggers:**
- Multi-intent chain detected (2+ intents)
- Ambiguous platform (files from multiple platforms changed)
- Project oversight request ("status", "progress", "what's left")
- Multi-platform task ("test everything", "review all platforms")

## Platform Hint Detection

If `$ARGUMENTS` starts with a platform name, pass it as a hint to the unified verb command:

| Prefix | Effect |
|--------|--------|
| `ios ...` | Forces `/cook`, `/test`, `/debug` to use iOS agent |
| `android ...` | Forces `/cook`, `/test`, `/debug` to use Android agent |
| `web ...` | Forces `/cook`, `/test`, `/debug` to use Web agent |
| `backend ...` | Forces `/cook`, `/test`, `/debug` to use Backend agent |

## Rules

- **ALWAYS** gather context before routing (Step 1 is mandatory)
- If no clear intent detected → show contextual discovery menu
- If ambiguous between two intents → use context boost to break tie; if still ambiguous → ask user (max 1 question)
- Always show the routing decision and reasoning before executing
- Prefer fast variants unless complexity clearly warrants deep
- Multi-intent requests → always delegate to orchestrator
- Context gathering should be fast (< 5 seconds total). Skip slow checks.
- If not in a git repo, skip git state gracefully and proceed with intent-only routing
