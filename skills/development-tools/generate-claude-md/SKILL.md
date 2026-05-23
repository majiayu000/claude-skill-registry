---
name: generate-claude-md
description: Interactive wizard to generate a CLAUDE.md file for a project. Use when setting up a new project or when user asks to create/initialize CLAUDE.md or AGENTS.md.
invocation: /generate-claude-md
---

# Generate CLAUDE.md

Create a minimal, well-structured CLAUDE.md file through an interactive conversation.

## Important Guidelines

- **Always use AskUserQuestion tool** when asking the user anything
- **Keep it minimal** — CLAUDE.md loads on every request, so only include what's essential
- **One question at a time** — don't overwhelm with multiple questions
- **Use MUST/NEVER/ALWAYS keywords** — for unambiguous rules

## Core Principle

Models can reliably follow ~150-200 instructions. Every token in CLAUDE.md loads on every request. Only include:
- Project identity (1 sentence)
- Tech stack declaration
- Tooling with MUST/NEVER rules
- Critical guardrails
- Pointers to docs/skills

Everything else should be progressive disclosure (separate docs) or skills (loaded on-demand).

## Process

### Step 1: Check for Existing Configuration

Check if `CLAUDE.md` or `AGENTS.md` exists in the project root.

Also check if `package.json` exists to help infer tech stack.

**If CLAUDE.md or AGENTS.md exists**, use AskUserQuestion:

```
I found existing agent configuration:
- CLAUDE.md: [exists/missing]
- AGENTS.md: [exists/missing]

Would you like to:
1. Start fresh (replace)
2. Audit and improve existing file
3. Cancel

(Choose 1, 2, or 3)
```

If option 2, read the existing file and use the agents-md audit workflow.
If option 3, stop here.

**If no files exist**, proceed to Step 2.

### Step 2: Gather Project Identity

Use AskUserQuestion:

```
Let's set up your CLAUDE.md file.

**Describe your project in one sentence.**

What does it do and who is it for?

(Example: "A B2B SaaS platform for construction companies to manage projects and crews.")
```

### Step 3: Gather Tech Stack

If `package.json` exists, read it first to understand the dependencies.

Use AskUserQuestion:

```
**What's your tech stack?**

Based on your package.json, I see: [summarize what you found, or "no package.json found"]

Please confirm or describe:
- Frontend: (framework, meta-framework)
- Backend: (API approach)
- Database: (database + ORM)
- Styling: (CSS approach)
```

### Step 4: Gather Tooling

Use AskUserQuestion:

```
**What package manager does this project use?**

1. pnpm
2. npm
3. yarn
4. bun

(Choose 1-4)
```

After they respond, use AskUserQuestion:

```
**What do you use for formatting/linting?**

1. Biome
2. ESLint + Prettier
3. ESLint only
4. Other (please specify)

(Choose 1-4)
```

After they respond, use AskUserQuestion:

```
**What are your common dev commands?**

List commands you run frequently (dev server, build, test, database, etc.)

(Example: "pnpm dev, pnpm build, pnpm test, pnpm db:push")
```

### Step 5: Gather Guardrails

Use AskUserQuestion:

```
**Is this a multi-tenant application?**

(Where each customer/org has isolated data that must be filtered)

1. Yes - queries must filter by tenant/org ID
2. No - single tenant or public data

(Choose 1 or 2)
```

After they respond, use AskUserQuestion:

```
**Are there any other critical rules that must NEVER be violated?**

Security, compliance, or code quality rules that apply to every task.

(Examples: "Never use any type", "Always validate user input", or "None")
```

### Step 6: Gather Documentation Pointers

Use AskUserQuestion:

```
**Do you have existing documentation the agent should know about?**

List paths to architecture docs, API docs, or other important files.

(Example: "docs/architecture.md, docs/api.md" or "None yet")
```

### Step 7: Generate CLAUDE.md

Create the file based on gathered information.

#### Template

```markdown
# Project Context

## Identity
[Single sentence from Step 2]

## Tech Stack
- Frontend: [from Step 3]
- Backend: [from Step 3]
- Database: [from Step 3]
- Styling: [from Step 3]

## Tooling
- MUST use [package_manager] (NEVER [alternatives])
- MUST use [formatter] for formatting

## Commands
- `[cmd]` - [description]
- `[cmd]` - [description]

## Guardrails
[MUST/NEVER/ALWAYS rules from Step 5]

## More Information
[Documentation pointers from Step 6]
- Run `/skills` to see available patterns and workflows
```

#### Generation Rules

1. **Skip empty sections** — don't include sections with no content
2. **Use MUST/NEVER for tooling** — "MUST use pnpm (NEVER npm or yarn)"
3. **Use MUST/ALWAYS/NEVER for guardrails** — security and compliance rules
4. **Keep commands minimal** — only the most common daily commands
5. **Always add** — "NEVER commit `.env` files or secrets" to guardrails

### Step 8: Confirm and Write

Show the generated content to the user and use AskUserQuestion:

```
Here's your CLAUDE.md:

[Show the generated content]

Would you like to:
1. Write this to CLAUDE.md
2. Make changes first
3. Cancel

(Choose 1-3)
```

If option 1, write the file.
If option 2, ask what they'd like to change.

### Step 9: Post-Setup

After creating the file, use AskUserQuestion:

```
✓ Created CLAUDE.md

Would you like to create a symlink to AGENTS.md for compatibility with other tools?

1. Yes - create symlink
2. No - just CLAUDE.md is fine

(Choose 1 or 2)
```

If yes, run: `ln -s CLAUDE.md AGENTS.md`

Then output skill recommendations:

```
Based on your stack, consider installing these skill plugins:

[List relevant plugins based on their tech stack]

- core: Universal coding standards
- platform-frontend / tech-react: React patterns
- platform-backend / tech-trpc: tRPC patterns
- platform-database / tech-drizzle: Drizzle patterns
- platform-testing / tech-vitest: Testing patterns

Run: claude /plugin install github:ravnhq/ai-toolkit/plugins/[name]
```

## Tips

- If the user provides brief answers, that's fine — the CLAUDE.md can be expanded later
- If they want to skip a section, omit it rather than adding placeholders
- Encourage minimal over comprehensive — less is more for CLAUDE.md
- The agents-md skill can audit and improve the file later
