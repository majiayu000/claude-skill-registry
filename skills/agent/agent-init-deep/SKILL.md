---
name: agent-init-deep
description: >
  Initialize or migrate to nested CLAUDE.md structure for progressive disclosure.
  Claude auto-loads CLAUDE.md from any directory it enters, so nested files get
  discovered automatically. Use when setting up a new project's agent config,
  refactoring a bloated CLAUDE.md, or adding progressive disclosure to an existing repo.
  Triggers on: '/agent-init-deep', 'setup progressive disclosure', 'refactor claude.md',
  'split claude.md', 'claude.md is too big'.
---

# Init Deep — Progressive Disclosure CLAUDE.md

Set up or migrate to a progressive disclosure CLAUDE.md structure using `docs/agents/` for topic-specific guidance.

## Context Model

```
Static (root CLAUDE.md)      — loaded every conversation, minimal, high-value
Semi-dynamic (docs/agents/)  — linked from root, loaded on-demand when relevant
Fully dynamic (skills)       — triggered by metadata match, loaded only when invoked
```

Root CLAUDE.md should be ~40-50 lines. Everything else belongs in docs/agents/ or skills.

## Target Structure

```
CLAUDE.md                        # Root: identity, tech stack, key rules, workflow, links
docs/agents/
├── tooling.md                   # e.g. package manager, linting, formatting, hooks
├── commands.md                  # e.g. script execution, build filters, passing args
├── guardrails.md                # e.g. data isolation, secrets, library docs
├── definition-of-done.md       # e.g. coverage, lint, type-check, format requirements
└── [topic].md                   # Additional topic-specific files as needed
```

## Workflow

### Step 1: Detect State

```
Check for:
- CLAUDE.md exists?
- docs/agents/ exists?
- How many lines is CLAUDE.md?
```

If no CLAUDE.md → **Greenfield path**
If CLAUDE.md exists → **Migration path**

### Step 2a: Greenfield Path

Ask the user:

1. Project name and one-line description
2. Tech stack (frontend, backend, database, etc.)
3. Package manager (pnpm, npm, yarn, bun)
4. Key guardrails (multi-tenancy, secrets, etc.)
5. Definition of done (test coverage, lint, types, format)

Then generate:

**Root CLAUDE.md** with:

- Project identity (1-2 lines)
- Tech stack list
- 3-5 key rules (only things the agent consistently gets wrong)
- 4-stage workflow: Plan → Execute → Validate → Commit
- Links to docs/agents/ files with routing signals

**docs/agents/ files** based on answers. Common files include:

- `tooling.md` — package manager rules, linting config, hooks
- `commands.md` — how to run scripts, filter by package, pass args
- `guardrails.md` — data isolation, secrets, library docs
- `definition-of-done.md` — specific thresholds and commands

Adjust filenames and topics to match the project's actual needs.

### Step 2b: Migration Path

1. Read existing CLAUDE.md
2. Classify each section:
   - **Root-worthy**: identity, tech stack, key rules (3-5 max), workflow
   - **docs/agents/**: detailed tooling, commands, guardrails, definition of done
   - **Skill-worthy**: complex workflows, procedures, domain expertise
3. Present proposed split to user:

   ```
   ROOT CLAUDE.md:
   - Project identity
   - Tech stack
   - Key rules: [list]
   - Workflow (Plan/Execute/Validate/Commit)
   - Links to docs/agents/

   docs/agents/tooling.md:
   - [extracted sections]

   docs/agents/commands.md:
   - [extracted sections]

   ... etc
   ```

4. Ask user to confirm or adjust
5. Create docs/agents/ files
6. Rewrite root CLAUDE.md

### Step 3: Post-Setup

After creating the structure:

1. List all created files
2. Show the root CLAUDE.md
3. Suggest additional improvements:
   - "Consider adding CLAUDE.md files in app subdirectories for app-specific rules"
   - "Run `/agent-add-rule` to add new rules to the right location"
   - "Run `/skills` to see available skills"

## Root CLAUDE.md Template

```markdown
# Project Context

[One-line project description]

## Tech Stack

- [list technologies]

## Key Rules

- [3-5 rules the agent consistently gets wrong without being told]

## Workflow

Every task follows four stages. Identify which stage you're in and follow its rules.

Plan → Execute → Validate → Commit
↑                               |
└── fix ────────────────────────┘

1. **Plan** — Understand the task, research code, design approach. Be concise; list unresolved questions.
2. **Execute** — Implement changes AND write tests together. No implementation is complete without tests.
3. **Validate** — ALL checks must pass with zero errors before moving on:
   - [list validation commands]
     If ANY check fails → return to Execute, fix, re-validate. Pre-existing errors are NOT exempt.
4. **Commit** — Only after Validate passes completely. Never commit with failing checks.

## Detailed Guidance

When working on tasks involving these topics, read the linked doc:

- [Topic](docs/agents/file.md) — brief routing signal describing when to read this
- Run `/skills` to see available patterns and workflows
```

## Classification Heuristic

When deciding what stays in root vs moves to docs/agents/:

| Criteria                     | Root                  | docs/agents/ |
| ---------------------------- | --------------------- | ------------ |
| Agent gets wrong without it? | YES                   | maybe        |
| Applies to every task?       | YES                   | no           |
| Under 2 lines?               | YES                   | any length   |
| Detailed reference?          | NO                    | YES          |
| Procedural/workflow?         | only the 4-stage loop | YES          |

## Principles

- **Minimal root**: Every line in root costs tokens on every conversation. Only include what the agent consistently gets wrong without being told.
- **Routing signals**: Each link description helps Claude decide whether to follow it. Be specific: "pnpm conventions, ESLint config" not just "tooling".
- **One level deep**: All docs link from root. No cross-references between docs/agents/ files.
- **docs/agents/ not docs/**: The `agents/` subdirectory separates agent instructions from human documentation.
