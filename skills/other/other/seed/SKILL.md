---
name: seed
description: Generate a project-level CLAUDE.md from stack detection and user-selected rule categories. Use when starting a new project, onboarding a repo, or when the user says "seed claude.md", "create project rules", "set up CLAUDE.md", "configure this project for me", or wants to establish coding conventions.
---

Concrete rules enforce. Abstract principles don't. Every rule in a CLAUDE.md must be a situation→action pair that Claude either follows or visibly violates — no interpretation required.

This was empirically validated: situation-keyed rules score 10.2% higher on compliance than named principles.

## Principles

- Every rule starts with "When [situation]:" followed by a concrete action. No principle names, no abstract descriptions.
- Anti-examples enforce better than positive instructions. "Do NOT suggest X, Y, Z" beats "Keep it focused."
- Explicit ordering words make sequencing stick. "BEFORE any code" and "Then and only then" are enforcement language.
- Concrete output formats enforce themselves. "Write three sections: 1. What I know 2. What I assume 3. What I need" — Claude either follows the format or visibly doesn't.
- The output is a CLAUDE.md file, not a conversation. No explanations, no rationale — just rules.

## Presentation

- One AskUserQuestion per step. Label = the choice. Description = what it means for the generated rules.
- No preamble between questions. One bold sentence framing the decision, then the question.
- Final output is the raw CLAUDE.md content — no wrapping, no commentary.

## Workflow

### Step 1: Detect project context

Read the project to understand what rules apply. No text output — go straight to Step 2.

1. Read package.json / Cargo.toml / pyproject.toml / go.mod — detect stack
2. Read existing CLAUDE.md if present — note what to preserve
3. Scan src/ for patterns: test runner, linter config, framework
4. Check .claude/settings.json for hooks, permissions
5. Read git log --oneline -10 for commit conventions

### Step 2: Select applicable rule categories

**Present categories based on detected stack.**

Use AskUserQuestion (multiSelect). Label = category name. Description = what it means for the generated rules, tuned to detected stack (e.g., mention npm if Node project, pip if Python).

Categories:
- **Response format** — Approach + Risks before every response
- **Library preference** — Name a package before writing custom code
- **Code review stance** — Default to deletion over addition when improving code
- **Uncertainty protocol** — Three-section format (know/assume/need) when choosing between approaches
- **Atomic changes** — Change everything at once, no deprecation, no v2
- **Output sizing** — Response length rules per task type
- **Stack-specific** — Rules for the detected framework: component patterns, data fetching, state management

### Step 3: Gather project-specific constraints

For each selected category, ask ONE focused question to tune the rules to this project. Use AskUserQuestion with project-specific options derived from Step 1 analysis.

Examples:
- Response format → "Should approach/risks apply to commit messages too, or just code responses?"
- Library preference → "Any packages you always want recommended?"
- Stack-specific → "Any architectural patterns to enforce?"

### Step 4: Generate CLAUDE.md

Assemble the file using these construction rules:

**Section: Response format** (if selected)
```markdown
## Response format

Every response MUST start with approach and risks BEFORE any code, analysis, or recommendations:

**Approach:** [one sentence — what you will do and why]
**Risks:** [2-3 things that could go wrong or must not happen]

Then and only then, provide the content (code, analysis, recommendation).

Exception: trivially simple tasks (single typo, yes/no) — compress to one line, skip risks.
```

**Section: Decision rules** (assembled from selections)
Each rule follows the pattern:
```
When [situation]:
- [concrete action with anti-example if applicable]
```

**Section: Output rules** (if output sizing selected)
Include task-type → length mapping with project-specific examples.

**Section: Style** (always included, from detected stack)
One line: language, paradigm preference, key conventions.

**Construction constraints:**
- Total file MUST be under 50 lines
- Every rule must be verifiable — if you can't tell whether Claude followed it by reading the output, rewrite it
- No named principles (no "Musashi's razor", no "Library over custom") — only situation→action rules
- No explanations of why a rule exists — the CLAUDE.md is for Claude, not for humans
- Anti-examples are mandatory for any rule about restraint ("do not also suggest X, Y, Z")

### Step 5: Present and refine

Show the generated CLAUDE.md in a code block. Use AskUserQuestion to confirm:
- **Looks good — write it** — Save to ./CLAUDE.md in the project root
- **Too strict** — User tells you which rules to relax
- **Missing something** — User tells you what to add
- **Start over** — Different category selection

If "Looks good" → write the file. Done. Otherwise → apply feedback, re-present.

## Boundaries

- Seed generates CLAUDE.md files. It does not modify settings.json, hooks, or system prompts.
- Seed does not explain its choices to the user. The generated file speaks for itself.
- Seed does not generate rules for things Claude already does well by default.
- Seed does not generate rules that can only be enforced by hooks — it notes these as "enforce via hooks" comments.
