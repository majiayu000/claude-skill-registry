---
name: init-project
description: Quick-start Claude Code configuration. Auto-detects stack, asks 4 questions to understand the project, generates complete config.
context: fork
---

# Init Project

MANDATORY FLOW: detect stack → ask 4 questions → WAIT for answers → generate config.

You MUST ask the 4 questions in Step 4 and WAIT for the user to answer BEFORE generating any files. Do NOT skip the questions. Do NOT generate config before receiving answers.

## Step 1: Check if already initialized

If `.claude/settings.json` exists:
```
Already initialized. Use /forge sync to update or /forge audit to check score.
```
Exit without changes.

## Step 2: Detect stacks

Scan project files silently using `$DOTFORGE_DIR/stacks/detect.md` as reference:

```
python-fastapi: pyproject.toml, requirements.txt with fastapi
react-vite-ts:  package.json with react + vite
swift-swiftui:  Package.swift, *.xcodeproj
node-express:   package.json with express/fastify (no react)
go-api:         go.mod
java-spring:    pom.xml or build.gradle with spring
supabase:       supabase/ dir or supabase in deps
docker-deploy:  Dockerfile or docker-compose*
gcp-cloud-run:  app.yaml or cloudbuild.yaml
aws-deploy:     cdk.json or template.yaml
redis:          redis in deps
data-analysis:  *.ipynb prominent
devcontainer:   .devcontainer/
```

Also scan existing files for additional context:
- README.md → project description
- existing test files → testing patterns
- CI config (.github/workflows, Makefile) → build/test commands

## Step 3: Detect user language and ask 4 questions

Detect language: check previous messages → global CLAUDE.md → system locale → default English.

OVERRIDE RULE: For `/forge init`, ALWAYS present questions in the detected language, even if global CLAUDE.md says "communicate in Spanish/English/etc." The questions are part of the tool's UI, not a conversation.

Present all 4 questions together in one message. Then STOP and WAIT for the user's response. Do NOT proceed to Step 5 until the user answers.

**English version:**
```
═══ FORGE INIT ═══
Stack detected: {stacks or "none — generic config"}

4 quick questions to generate a complete config:

1. What does it do and what does it NOT do?
   → One sentence: the problem it solves, and explicit limits of v0.1.
   Example: "REST API for real-time quotes. No auth, no frontend, no historical data yet."

2. Built with what?
   → Stack, language, DB, external services, where it runs.
   Example: "Python 3.12, FastAPI, Supabase, deployed on GCP Cloud Run."

3. How do you work?
   → Solo or team, spec-first or prototype-first, testing level from day one.
   Example: "Solo, prototype-first, tests only for critical paths."

4. What domain and role?
   → What expertise does Claude need? What business concepts are critical?
   Example: "Expert in Jira API v3, agile metrics, dashboard generation.
   Key concepts: velocity, cycle time, sprint burndown, JQL."
```

**Spanish version:**
```
═══ FORGE INIT ═══
Stack detected: {stacks or "none — generic config"}

4 quick questions to generate a complete config:

1. What does it do and what does it NOT do?
   → One sentence: the problem it solves, and the explicit limits of v0.1.
   Example: "Real-time quotes REST API. No auth, no frontend, no historical data yet."

2. Built with what?
   → Stack, language, DB, external services, where it runs.
   Example: "Python 3.12, FastAPI, Supabase, deploy on GCP Cloud Run."

3. How do you work?
   → Solo or team, spec-first or prototype-first, testing level from day one.
   Example: "Solo, prototype-first, tests only for critical paths."

4. What domain and role?
   → What expertise does Claude need? What business concepts are critical?
   Example: "Expert in Jira API v3, agile metrics, dashboard generation.
   Key concepts: velocity, cycle time, sprint burndown, JQL."
```

Use the appropriate version based on detected language. For other languages, translate the questions following the same structure.

STOP HERE. Wait for the user's response before proceeding.

If the user answers in a single message covering all 4, parse accordingly.
If the user says "skip", proceed with auto-detected info only.

**Important:** Generate CLAUDE.md content in English (Claude-consumed content must be in English per project conventions). The user's answers are incorporated as-is regardless of their language.

## Step 5: Generate config

Run `/bootstrap-project` internally with:
- Profile: `standard`
- Stacks: auto-detected
- No confirmation prompt

Then **enrich the generated CLAUDE.md** with the user's answers:

### CLAUDE.md enrichment

Insert the user's answers into the `<!-- forge:custom -->` section of CLAUDE.md:

```markdown
<!-- forge:custom -->

## What this project does
{answer to question 1 — what it does AND what it doesn't do}

## Stack & infrastructure
{answer to question 2 — expanded with detected stacks}

## Working style
{answer to question 3 — solo/team, approach, testing expectations}

## Role
{Generated from answer to question 4 — Claude's role and expertise for this project}

## Domain
{Generated from answer to question 4 — key domain concepts, business rules, reference data}
```

If the user provided build/test commands in their answers, also update the `## Build & Test` section above the forge:custom marker.

### Deny list enrichment

If the user mentioned specific services, external APIs, or sensitive areas in question 2, add relevant deny patterns to settings.json. Examples:
- Mentioned Supabase → ensure `Read(**/.env)` covers SUPABASE_* vars
- Mentioned external API → add API key env var patterns
- Mentioned "no auth yet" → no auth-related deny needed

### Domain rules scaffolding

If the user answered question 4 with domain/role info:
1. Create `.claude/rules/domain/` directory
2. Based on the domain concepts mentioned, generate 1-3 domain rule files:
   - Each file covers one domain area (e.g., jira-api.md, agile-metrics.md)
   - Each file has frontmatter: globs (specific to domain keywords), description, domain tag, last_verified
   - Content: key facts, constraints, and gotchas Claude needs to know about that domain
   - Keep each file under 40 lines — concise, imperative, no filler
3. Show the generated files to the user for review before writing

If the user skipped question 4, skip this entirely.

## Step 6: Output

Show a concise summary:

```
═══ FORGE INIT — DONE ═══
Project:  {name}
Stacks:   {detected stacks}
Config:   dotforge v2.3.0 standard

Generated:
  CLAUDE.md          → project context (personalized)
  .claude/settings.json → permissions + hooks
  .claude/rules/     → {N} rules
  .claude/hooks/     → {N} hooks
  .claude/commands/  → {N} commands
  .claude/agent-memory/ → persistent memory
  CLAUDE_ERRORS.md   → error log
  .forge-manifest.json → version tracking

Score: {X}/10 (run /forge audit for details)
```

## Constraints

- Ask exactly 4 questions, together, not sequentially
- If user skips questions, proceed with auto-detected info — never block on missing answers
- Keep the output concise — no walls of text
- The user's answers go in `<!-- forge:custom -->` section (protected from future syncs)
- If bootstrap-project fails, show error and suggest `/forge bootstrap` for full interactive version
