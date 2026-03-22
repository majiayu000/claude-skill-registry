---
name: meta-skill-generator
description: Use when users want to create, revise, or scaffold a Codex skill from a plain-language brief. Especially relevant when they ask for a new SKILL.md, want to convert workflow requirements into a reusable skill, or need help defining trigger conditions, structure, bundled resources, or UI metadata for a skill.
tags:
  - agent-skills
  - codex
  - claude-code
  - cursor
  - github-copilot
  - prompt-engineering
  - developer-tools
allowed-tools:
  - read
  - write
  - exec
license: MIT
---

# Meta Skill Generator

Turn a user's workflow brief into a concise, production-ready `SKILL.md`. Prefer shipping a minimal useful skill over an ornate one.

Default to English unless the user explicitly asks for another language.

## Goal

Create or update skills that:
- trigger on the right requests
- encode only task-specific knowledge Codex would not already know
- use the lightest structure that still keeps execution reliable

## Intake

Collect only the minimum inputs needed to design the skill:
- what job the skill should do
- what kinds of user requests should trigger it
- what output the skill should help produce
- whether the task needs `scripts/`, `references/`, or `assets/`
- any required tone, constraints, frameworks, or file formats

If the brief is incomplete, infer sensible defaults and note assumptions briefly after the draft instead of blocking.

## Workflow

1. Distill the request into a one-sentence mission.
2. Choose the simplest structure that fits:
   - workflow-based for stepwise procedures
   - task-based for multiple operations
   - reference-based for policies or specifications
   - capability-based for multi-feature systems
3. Write frontmatter:
   - `name`: short, stable, hyphen-case
   - `description`: explicit trigger conditions; start with `Use when...`
4. Draft the body with only the sections the skill actually needs. Common sections:
   - `# Title`
   - `## Goal` or `## Overview`
   - `## Intake`
   - `## Workflow` or `## Task Guide`
   - `## Resource Use`
   - `## Output Contract`
   - `## Quality Bar`
5. Add optional resources only when justified:
   - `scripts/` for deterministic or repeated automation
   - `references/` for large or variant-specific material
   - `assets/` for templates or files consumed by outputs
6. If the user asks for a full skill package, also add `agents/openai.yaml` with short UI text and a default prompt that explicitly mentions `$skill-name`.

## Authoring Rules

- Keep the skill lean. Do not explain basics Codex already knows.
- Optimize for progressive disclosure. Put bulky details in `references/` only if they are truly needed.
- Be concrete about triggers, inputs, outputs, and failure modes.
- Prefer direct instructions over theory.
- Do not create auxiliary docs such as `README.md`, `CHANGELOG.md`, or setup notes unless the user explicitly asks.
- Use examples only when they remove ambiguity.
- Match guidance strictness to task fragility:
  - high freedom for broad creative work
  - medium freedom for preferred patterns
  - low freedom for fragile operations

## Updating Existing Skills

- Preserve sections that already work well and only tighten what is vague, repetitive, or misleading.
- Improve the `description` first if the trigger conditions are weak.
- Remove generic filler before adding new sections.
- Do not expand scope unless the user clearly wants a broader skill.

## Description Pattern

The `description` should answer:
- what the skill does
- when to use it
- which user phrases, tasks, or scenarios should trigger it
- what deliverable it helps produce

Preferred pattern:

```yaml
description: Use when users ask to ...
```

## Output Modes

When the user asks for only a `SKILL.md`, produce a complete `SKILL.md` and keep everything else optional.

When the user asks for a full skill package, produce:
- `SKILL.md`
- `agents/openai.yaml` if UI metadata would help
- only the minimal extra directories required by the workflow

## Minimal Template

```markdown
---
name: skill-name
description: Use when users ask to ...
---

# Skill Title

## Goal

State the job in 1-2 sentences.

## Intake

List only the inputs needed to do the job well.

## Workflow

Give the execution steps or decision rules.

## Resource Use

Explain when to read or run bundled files.

## Quality Bar

State the constraints, failure modes, and expected output quality.
```

## Quality Check

Before finalizing, verify that:
- the `name` is short and stable
- the `description` would actually trigger the skill
- the body is concise and actionable
- optional resources are justified
- the draft matches the user's requested language and output scope
