---
name: agent-add-rule
description: >
  Add a new rule, convention, or instruction to the project's agent configuration.
  Analyzes the rule and helps decide placement: root CLAUDE.md (universal rules),
  docs/agents/ files (topic-specific guidance), or a new skill (complex workflows).
  Triggers on: '/agent-add-rule', 'add a rule', 'add convention', 'new coding standard',
  'add instruction for claude', 'update claude.md with'.
---

# Add Rule — Place Agent Instructions Correctly

Add a new rule or convention to the right location in the progressive disclosure structure.

## Context Spectrum

```
Static (root CLAUDE.md)      — loaded every conversation. Token cost always paid.
Semi-dynamic (docs/agents/)  — linked from root. Loaded when Claude follows a link.
Fully dynamic (skills)       — metadata only in context. Body loaded on trigger.
```

## Workflow

### Step 1: Ask

Ask the user: **"What rule or convention do you want to add?"**

Accept free text. If the user already provided it (e.g., `/agent-add-rule always use snake_case for database columns`), skip this step.

### Step 2: Analyze Current Structure

Read:

- Root CLAUDE.md
- List files in docs/agents/
- List available skills

Understand what already exists so you don't duplicate or contradict.

### Step 3: Classify

Apply this decision tree:

```
Does the agent consistently get this wrong WITHOUT being told?
├── NO → Challenge: "Does this justify its token cost?"
│        If user still wants it → treat as semi-dynamic
│
├── YES → Does it apply to EVERY task?
│   ├── YES → Root CLAUDE.md (static)
│   │         Examples: package manager, multi-tenancy, project scripts
│   │
│   └── NO → docs/agents/ file (semi-dynamic)
│             Examples: lint rules, test thresholds, API conventions
│
└── Is it a repeatable workflow or procedural knowledge?
    ├── YES → Skill (fully dynamic)
    │         Examples: deployment process, PR review checklist, migration procedure
    │
    └── NO → Probably not needed. Ask: "Does this justify its token cost?"
```

Key questions to ask the user:

1. **"Does the agent consistently get this wrong?"** — If no, consider skipping
2. **"Does this apply to every task or just some?"** — Static vs semi-dynamic
3. **"Is this a rule or a workflow?"** — docs/agents/ vs skill
4. **"Will this change frequently?"** — Skills are easier to evolve independently

### Step 4: Recommend

Present the recommended placement with reasoning:

```
Recommendation: Add to docs/agents/guardrails.md

Reasoning:
- This is a data handling rule, not a universal workflow rule
- It applies only when working with the database
- guardrails.md already covers data isolation patterns
- Adding to root would cost tokens on every conversation unnecessarily
```

### Step 5: Confirm

Ask the user to confirm or override. If they override, respect their choice but note the trade-off:

- Moving to root: "This adds ~X lines to every conversation's context"
- Moving to docs/agents/: "This won't be visible unless Claude follows the link"
- Moving to skill: "This will only load when triggered by matching keywords"

### Step 6: Write

Based on confirmed placement:

**If root CLAUDE.md:**

- Add the rule under the appropriate section (Key Rules, Workflow, etc.)
- Warn: "This adds to every conversation's token budget"
- Keep it concise — 1-2 lines max

**If existing docs/agents/ file:**

- Read the target file
- Add the rule under the appropriate section
- Keep consistent formatting with existing content

**If new docs/agents/ file:**

- Create the file with a clear heading and the rule
- Update root CLAUDE.md links section with a new entry including routing signal
- Example: `- [API Conventions](docs/agents/api-conventions.md) — REST patterns, error response format, pagination`

**If skill:**

- Tell the user to run `/agent-skill-creator` to scaffold it
- Provide the rule content as input for the skill body

## Examples

### Example 1: Universal Rule → Root

User: "Always use pnpm, never npm"

Classification: Agent gets this wrong without being told + applies to every task → **Root**

Action: Add to Key Rules section in CLAUDE.md

### Example 2: Topic-Specific Rule → docs/agents/

User: "API responses must always include a `requestId` field"

Classification: Agent might get wrong + only applies to API work → **Semi-dynamic**

Action: Add to docs/agents/guardrails.md or create docs/agents/api-conventions.md

### Example 3: Complex Workflow → Skill

User: "When deploying, always run migrations first, then build, then deploy to staging, verify, then production"

Classification: Repeatable multi-step procedure → **Fully dynamic (skill)**

Action: Suggest `/agent-skill-creator` to create a deployment skill

### Example 4: Unnecessary Rule → Challenge

User: "Always use `const` instead of `let`"

Classification: ESLint already enforces this → **Not needed**

Response: "ESLint already enforces this via the `prefer-const` rule. Adding it to agent instructions would cost tokens without benefit. Skip?"

## Principles

- **Challenge before adding**: Every rule costs tokens. Ask "does this justify its token cost?"
- **No duplication**: If ESLint, TypeScript, or another tool already enforces it, don't add it
- **Routing signals matter**: When adding to docs/agents/, update the root CLAUDE.md link description so Claude knows when to follow it
- **One level deep**: Never cross-reference between docs/agents/ files. All links go from root
