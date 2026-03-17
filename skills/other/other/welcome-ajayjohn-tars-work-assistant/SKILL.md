---
name: welcome
description: Interactive first-run workspace setup with directory scaffolding, integration verification, and context gathering
user-invocable: true
help:
  purpose: |-
    Interactive first-run workspace setup with directory scaffolding, integration verification, and context gathering.
  use_cases:
    - "Set up TARS"
    - "Bootstrap my workspace"
    - "Initialize TARS"
  scope: setup,bootstrap,onboarding,welcome
---

# Welcome to TARS

Interactive first-run setup. Creates workspace scaffolding and learns user context.

**This skill replaces both `install.sh` and the legacy `/welcome` command.**

## Protocol

No external protocol file. Self-contained setup command.

## Procedure

### Step 1: Check existing workspace

Check for existing workspace files:
- `CLAUDE.md` (root config)
- `memory/` directory
- `tasks/` directory
- `journal/` directory
- `contexts/` directory
- `reference/replacements.md`

If files exist, ask: "Existing workspace detected. A) Add to it, B) Start fresh, C) Cancel"

### Step 2: Create directory scaffolding and verify integrations

Run the automated scaffolding script:

```bash
bash scripts/scaffold.sh {workspace_path} {plugin_path}
```

This script creates all directories, copies reference templates, creates empty indexes, and verifies configured integrations. Parse the JSON output to determine what was created and which integrations are available.

Then run integration verification separately for detailed health info:

```bash
python3 scripts/verify-integrations.py {workspace_path}
```

This script checks each configured integration's health and returns JSON with status per integration (`configured`, `error`, `not_configured`, `check_mcp_servers`). Report integration status to the user.

If the scripts are not available, create directories manually:

```
memory/
  people/
  vendors/
  competitors/
  products/
  initiatives/
  decisions/
  organizational-context/
journal/
contexts/
  products/
  artifacts/
```

And verify manually:
1. **Task integration**: Read `reference/integrations.md` Tasks section. Execute a test `list` operation. If it fails, warn and continue.
2. **Calendar integration**: Read `reference/integrations.md` Calendar section. Execute a test `list_events` operation. If it fails, warn and continue.

### Step 3: Interactive setup wizard

Gather context through bounded questions (max 3 questions per round):

**Round 1: Identity**
- "What is your name?"
- "What is your title/role?"
- "What is your company name and industry?"

**Round 2: Organization**
- "What teams do you manage or work with? (List team names and their focus areas)"
- "What products or services do you own/oversee?"
- "Who is your manager, and who are 2-3 key executives you work with? (Name, title)"

**Round 3: People**
- "List your top 10-15 key people with their roles and any nicknames/abbreviations. Format: Full Name (Role) - also known as: nickname"

**Round 4: Context**
- "What are your current active initiatives/projects? (Name and one-line description each)"
- "Any common acronyms or shorthand your team uses? (Format: abbreviation = full name)"

### Step 4: Generate workspace files

Using the gathered information, create:

#### `CLAUDE.md` (workspace root)

```markdown
# TARS Framework

You are TARS, the intelligent assistant for **{user_name}, {title} at {company}**.
{company_description}
Teams: {team_list}.
Products: {product_list}.

---

## Core directives

- **BLUF**: Lead every response with the bottom line. No preambles.
- **Anti-sycophancy**: Challenge flawed premises. Never default to agreement.
- **Clarification**: If critical context is missing after checking sources, STOP and ask using bounded techniques (menu, strawman, binary). Never guess.
- **Wikilinks**: Use `[[Entity Name]]` for all internal entity references.
- **Name normalization**: Read `reference/replacements.md` before processing any names. Always use canonical forms.
- **Framework citation**: When applying a decision framework, state which one and why.

---

## MCP integrations

External tools available via MCP. See `reference/integrations.md` for query patterns.
Configured: {configured_mcps}. Placeholder: {placeholder_mcps}.
```

#### `reference/replacements.md`

Populate People section with nicknames from Round 3. Populate Teams section with abbreviations. Populate Products/Initiatives section with acronyms from Round 4.

#### `reference/taxonomy.md`

Copy the template taxonomy from the plugin's `reference/taxonomy.md`. No user-specific modifications needed (it's already generic structure).

#### `reference/kpis.md`

Create a template KPI file with sections for each team and initiative gathered in setup:

```markdown
# KPI definitions

User-maintained file. Add metrics per team and initiative.

---

## {Team Name}

- **Velocity**: Average story points per sprint (~~project tracker)
- **Cycle time**: Average days from start to done (~~project tracker)

[Repeat for each team]

---

## {Initiative Name}

- **Feature completion**: Done / Total stories (~~project tracker)
- **Blocked items**: Issues in Blocked status (~~project tracker)

[Repeat for each initiative]

---

## Adding new KPIs

1. Add under the appropriate team or initiative heading
2. Format: `- **Metric Name**: Description (data source)`
3. Include the data source so the report protocol knows where to query
```

#### Memory folder indexes

For each memory category, create an empty `_index.md`:

```markdown
# {Category} index

| Name | Aliases | File | Summary | Updated |
|------|---------|------|---------|---------|
```

#### Contexts indexes

Create `contexts/products/_index.md`:

```markdown
# Product specifications index

| Name | Status | Owner | Summary | Updated |
|------|--------|-------|---------|---------|
```

Create `contexts/artifacts/_index.md`:

```markdown
# Artifacts index

| Name | Type | Created | Source | Summary |
|------|------|---------|--------|---------|
```

#### Initial people entries

For each key person from Round 3, create `memory/people/{slug}.md`:

```yaml
---
title: Full Name
type: person
tags: [stakeholder]
aliases: [nickname1, nickname2]
summary: Role description
related: []
updated: YYYY-MM-DD
---
```

```markdown
# [[Full Name]]

**Role:** {role}
**Relationship:** {relationship to user}
```

Update `memory/people/_index.md` with all entries.

#### Master memory index

Create `memory/_index.md` with counts.

#### `reference/schedule.md`

Create empty schedule template from the plugin's `reference/schedule.md` for recurring and one-time scheduled items.

### Step 5: MCP and integration scan (optional)

If MCP tools are available, offer:
- "I detected ~~project tracker is configured. Want me to scan for active initiatives and recent items?"

If the calendar integration is reachable, offer:
- "Calendar integration is connected. Want me to check your upcoming meetings for additional people context?"

If accepted, run lightweight queries and add findings to memory.

### Step 6: Offer daily housekeeping shortcut

If the environment supports Cowork shortcuts with schedules (check if the `create-shortcut` skill is available):

1. Ask the user: "Would you like TARS to run daily maintenance automatically? This keeps indexes healthy, archives stale content, and syncs scheduled items."
2. If accepted, ask for preferred time (default: 5:30 PM) using AskUserQuestion
3. Use the `create-shortcut` skill to create a `daily-housekeeping` shortcut with the task description from `reference/shortcuts.md` and the user's preferred cron schedule
4. Note: Even without the shortcut, TARS runs a session-start housekeeping check as a fallback (see core skill)

If the environment does not support scheduled shortcuts, skip this step. The session-start check will handle daily housekeeping.

### Step 7: Report

Display summary:

```markdown
## Setup complete

### Workspace created
- CLAUDE.md (root config)
- reference/replacements.md ({N} entries)
- reference/kpis.md ({N} teams, {N} initiatives)
- Task integration verified (configured lists accessible)
- Calendar integration verified (calendar access)
- memory/ ({N} people created, {N} category indexes)
- journal/ (ready)
- contexts/ (products index, artifacts index ready)

### Next steps
1. Run `/daily-briefing` to see your first morning briefing
2. Run `/process-meeting` with your next meeting transcript
3. Add more people and context as you use TARS
4. Edit `reference/kpis.md` to define your team metrics
5. Daily housekeeping runs automatically (shortcut or session-start check)
```

## Post-execution checklist
- [ ] All directories created
- [ ] CLAUDE.md generated with user identity
- [ ] replacements.md populated with name mappings
- [ ] kpis.md templated with teams and initiatives
- [ ] Task and calendar integrations verified
- [ ] Memory indexes created for all categories
- [ ] Contexts indexes created (products, artifacts)
- [ ] People entries created from setup wizard
- [ ] Summary report displayed
