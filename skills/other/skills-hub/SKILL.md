---
name: skills-hub
description: Use this skill when the user wants to discover, inspect, install, or apply Skills Hub presets, kits, AGENTS.md policies, or skill packages for a project. It guides the agent to use the Skills Hub CLI to search presets, inspect their policy and selected skills, install them as kit artifacts, and apply them with optional temporary skill overrides after user confirmation.
allowed-tools: Bash(skills-hub:*), Read, Grep, Glob
---

# Skills Hub

Use this skill as the Skills Hub orchestration and preset-selection entrypoint.

## Use This Skill When

- The user wants help choosing a project setup from Skills Hub presets.
- The user asks which AGENTS.md and skills package fit a project.
- The user wants to browse or inspect presets before installing.
- The user wants to install a preset as a policy/package/kit.
- The user wants to apply a saved kit with temporary added or removed skills.

## Core Rule

Do not invent available presets or skills.

Always inspect the current Skills Hub catalog or local kit state first, then explain what you found.

## Workflow

### 1. Read Project Context

First understand the user goal and the project context:

- project path
- language / framework
- whether this is new feature work, backend work, research work, or release work
- whether the user wants a preset or a custom/manual kit

If the project context is ambiguous, inspect the repository before recommending a preset.

### 2. Search Presets First

For first-pass recommendations, use the preset catalog before falling back to manual kit assembly.

Start with:

```bash
skills-hub kit preset-list
```

If you need to narrow candidates:

```bash
skills-hub kit preset-search <query>
```

Examples:

```bash
skills-hub kit preset-search nextjs
skills-hub kit preset-search node api
skills-hub kit preset-search scientific literature
```

### 3. Inspect Candidate Presets

For any promising candidate, inspect it before recommending installation:

```bash
skills-hub kit preset-inspect --id <preset-id>
```

Use the inspect output to explain:

- which policy the preset uses
- which source repos it draws skills from
- which selected skills are included
- whether it matches the current project and user goal

### 4. Recommend Before Installing

Before installing anything, present a short recommendation to the user:

- recommended preset
- why it fits
- what policy it will create
- what skills it will include
- whether you suggest any temporary `--with` or `--without` adjustments at apply time

Do not install or apply until the user confirms.

### 5. Install the Preset

After confirmation:

```bash
skills-hub kit preset-install --id <preset-id>
```

This creates:

- a preset-backed policy
- a preset-backed package
- a kit

### 6. Review Installed Kits If Needed

After installation, you can inspect saved kit state with:

```bash
skills-hub kit list
skills-hub kit policy-list
skills-hub kit package-list
```

Use these when the user wants to confirm what was created, or when multiple kits already exist.

### 7. Apply the Kit

Apply the installed kit only after the user confirms the target project and agent:

```bash
skills-hub kit apply --id <kit-id> --project <path> --agent <name>
```

If the user wants temporary adjustments for this one apply only:

```bash
skills-hub kit apply --id <kit-id> --project <path> --agent <name> --with <skill> --without <skill>
```

Notes:

- `--with` adds a hub skill for this apply only
- `--without` removes a skill from the saved loadout for this apply only
- these flags do not mutate the saved kit

### 8. Fall Back to Manual Kit Workflows Only When Needed

If no preset fits, fall back to manual kit composition:

```bash
skills-hub kit policy-list
skills-hub kit package-list
skills-hub kit list
```

Then guide the user toward manual policy/package/kit creation or editing.

## Recommendation Output Format

When recommending a preset, keep the answer compact and explicit:

```text
Recommended preset: <preset-id>

Why:
- <reason 1>
- <reason 2>

Policy:
- <policy name>

Selected skills:
- <skill 1>
- <skill 2>

Suggested apply-time adjustments:
- add: <skill> (optional)
- remove: <skill> (optional)

If you want, I can install this preset and then apply it to <project> for <agent>.
```

## Produces

- an inspected preset recommendation
- optionally, a newly installed preset-backed policy/package/kit
- optionally, an applied kit for a selected project and agent

## Guardrails

- Do not claim a preset exists unless `skills-hub kit preset-list/search` shows it.
- Do not claim a skill is included unless `skills-hub kit preset-inspect` shows it.
- Do not apply a kit without user confirmation.
- If no official preset fits, say so directly and switch to manual kit guidance.
