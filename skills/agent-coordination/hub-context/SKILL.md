---
name: hub-context
description: Use when routing user prompts to the right skill or agent. Senses git state, detects platform, classifies intent, and applies context boosts before dispatching.
user-invokable: false
tier: core

metadata:
  agent-affinity: [epost-orchestrator]
  keywords: [context, hub, routing, git-state, platform-detection, error-signals]
  platforms: [all]
  triggers: []
  connections:
    enhances: [skill-discovery]
---

# Hub Context Skill

## Purpose

Defines a context sensing protocol for the `/epost` smart hub. Before routing, the hub gathers a snapshot of the current working state to make informed routing decisions.

## Context Snapshot Protocol

On every `/epost` invocation, gather these signals **before** parsing intent:

### 1. Git State

Run these commands and capture output:

| Signal | Command | Purpose |
|--------|---------|---------|
| Branch | `git branch --show-current` | Detect feature branch vs main |
| Staged files | `git diff --cached --name-only` | Know what's ready to commit |
| Unstaged changes | `git diff --name-only` | Know what's being worked on |
| Untracked files | `git ls-files --others --exclude-standard \| head -20` | New files not yet tracked |
| Recent commits | `git log --oneline -3` | Understand recent activity |
| Merge conflicts | `git diff --name-only --diff-filter=U` | Detect blocked state |

### 2. Platform Detection

Determine the dominant platform from changed files:

| Extension Pattern | Platform | Confidence |
|-------------------|----------|------------|
| `.tsx`, `.ts`, `.jsx`, `.js`, `.scss`, `.css` | web | high |
| `.swift` | ios | high |
| `.kt`, `.kts` | android | high |
| `.java` | backend | high |
| `.md`, `.json`, `.yml` | unknown | low — check directory path |

**Rules:**
- If 80%+ of changed files share a platform → that platform is dominant
- If mixed → set platform to `multi` (triggers orchestrator delegation)
- If no changed files → check current working directory for platform signals
- Platform prefix in `$ARGUMENTS` always overrides auto-detection

### 3. Error Signals

Check for recent errors (only if platform detected):

| Platform | Check | Command |
|----------|-------|---------|
| web | TypeScript errors | `npx tsc --noEmit 2>&1 \| head -5` (only if `tsconfig.json` exists) |
| web | Lint errors | Check for recent lint output in terminal |
| ios | Build errors | Check for recent `xcodebuild` failure output |
| android | Build errors | Check for recent `gradle` failure output |
| any | Test failures | Check for recent test runner output with "FAIL" or "ERROR" |

**Important:** Error signal gathering should be **fast** (< 2 seconds). Skip checks that would be slow. TypeScript check is the most valuable — run it if web context is detected.

### 4. Session Hints

| Signal | How to Check | Purpose |
|--------|-------------|---------|
| Active plans | `ls ./plans/*.md 2>/dev/null` | Detect in-progress work |
| Data store | `ls .epost-data/ 2>/dev/null` | Detect persistent agent state |
| Branch pattern | Parse branch name for `feature/`, `fix/`, `hotfix/` | Infer work type |

## Context Summary Format

After gathering, produce a structured summary for the routing engine:

```
[Context] branch: {branch_name} | platform: {platform}
[Context] staged: {count} files ({extensions}) | unstaged: {count} files ({extensions})
[Context] errors: {error_summary} (or "none detected")
[Context] plan: {plan_file} ({status}) (or "no active plan")
[Context] hints: {branch_type}, {other_signals}
```

## Context Boost Table

The routing engine uses context to boost intent categories:

| Context Signal | Boosts Category | Example Routing Effect |
|---------------|----------------|----------------------|
| TypeScript/build errors detected | **Fix** | "what's wrong?" → `/fix` (auto-detects types) |
| Staged files present | **Git** or **Review** | "I'm done" → `/git-commit` |
| Active plan file exists | **Build** | "continue" → `/cook` with plan context |
| Test failures detected | **Fix** or **Test** | "help" → `/fix` (auto-detects test failures) |
| Feature branch, no changes | **Build** or **Plan** | "what's next?" → continue from plan |
| Clean main branch | **Plan** or **Explore** | show contextual menu |
| Merge conflicts detected | **Fix** | auto-suggest conflict resolution |

## Smart Routing

### Prompt Classification
- **Dev task** (action verbs: cook, fix, plan, test, debug, etc.) → route via intent map
- **Kit question** ("which agent", "list commands", "our conventions") → `epost-orchestrator`
- **External tech question** ("how does React...", "what is gRPC") → `epost-researcher`
- **Conversational** (greetings, opinions, clarifications) → respond directly, no routing

### Intent → Skill Map

| Intent | Signal Words | Routes To |
|--------|-------------|-----------|
| Build | cook, implement, build, create, add, make, continue | `/cook` skill |
| Fix | fix, broken, error, crash, failing, what's wrong | `/fix` skill |
| Plan | plan, design, architect, spec, roadmap | `/plan` skill |
| Test | test, coverage, validate, verify | `/test` skill |
| Debug | debug, trace, inspect, diagnose | `/debug` skill |
| Review | review, check code, audit | `/review-code` skill |
| Git | commit, push, pr, merge, done, ship | `/git-commit`, `/git-push`, `/git-pr` |
| Docs | docs, document, write docs | `/docs-init` or `/docs-update` |
| Scaffold | bootstrap, init, scaffold, new project, new module | `/bootstrap` skill |
| Convert | convert, prototype, migrate | `/convert` skill |
| A11y | a11y, accessibility, wcag | `/fix-a11y` or `/review-a11y` |
| Onboard | get started, begin, onboard, new to project, what is this | `/get-started` |

### Routing Rules
- If user types a slash command explicitly → execute it directly, skip routing
- If ambiguous → use context boost to break tie; if still ambiguous → ask user (max 1 question)
- If multi-intent ("plan and build X") → delegate to `epost-orchestrator`
- Platform detection delegates to `skill-discovery` — never hardcode platform logic here

## Rules

- Context gathering MUST complete before intent parsing
- If a git command fails (not a git repo), skip git state gracefully
- Never run destructive commands during context gathering
- TypeScript check should timeout after 5 seconds — skip if slow
- Context snapshot is read-only — never modify working state
