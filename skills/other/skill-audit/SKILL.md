---
name: skill-audit
description: "Audit, design, categorize, distribute, and measure agent skills using lessons from Anthropic's Lessons from building Claude Code: How we use skills. Use when reviewing an existing skill, deciding whether a workflow deserves a skill, planning a skill library, turning team knowledge into skills, choosing skill categories, writing trigger descriptions, designing progressive disclosure, or planning skill marketplace and usage measurement."
---

# Skill Audit

Use this skill to audit existing skills, turn workflow knowledge into useful
agent skills, and review skill libraries at the strategy level. It complements
`skill-creator`: use this skill to decide what a skill should be, how it should
fit a library, and what needs improvement; use `skill-creator` when the user
wants the concrete SKILL.md implementation and eval loop.

This workflow is based on Anthropic's June 3, 2026 blog post, "Lessons from
building Claude Code: How we use skills":
https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills

## Core Principle

A good skill is not "some markdown about a topic." It is a compact extension
point that gives the agent non-obvious domain knowledge, reusable files,
deterministic helpers, setup rules, verification habits, and guardrails at the
moment they matter.

## Workflow

### 1. Decide Whether This Should Be A Skill

Create or improve a skill only when at least one of these is true:

- The workflow repeats often enough that users should not re-explain it.
- The agent regularly makes the same domain-specific mistake.
- The work needs local scripts, templates, examples, assets, hooks, or setup.
- The output must follow a stable structure or verification path.
- The knowledge is team-specific, product-specific, infrastructure-specific, or
  otherwise not inferable from general model knowledge.

Do not make a skill when the content only restates obvious coding behavior,
generic best practices, or one-off instructions.

### 2. Classify The Skill

Read `references/skill-taxonomy.md` and classify the candidate into exactly one
primary category. If it appears to span several categories, tighten the scope or
split it.

Report:
- Primary category
- Secondary category, if truly needed
- Why this category is the cleanest fit
- What would make the skill too broad

### 3. Draft A Skill Brief

Use `assets/skill-brief-template.md` for the output. Fill it with:

- Trigger description written for the model, not as a human-facing summary
- High-signal knowledge the model would not otherwise know
- Gotchas and failure modes
- Progressive disclosure map: SKILL.md vs references vs scripts vs assets
- Setup requirements or config questions
- Verification strategy
- Distribution path
- Measurement plan

### 4. Design Progressive Disclosure

Keep `SKILL.md` focused on activation, decisions, and the main workflow. Move
details into support files:

- `references/` for tables, API conventions, taxonomy, playbooks, and long docs
- `scripts/` for deterministic actions or repetitive checks
- `assets/` for templates, report formats, starter files, or examples
- `agents/` for specialized subagent prompts when the repo supports them
- `evals/` for realistic prompts and objective assertions

Tell the agent exactly when to read each support file.

### 5. Add Operational Design

Read `references/writing-and-operations.md` when deciding:

- Whether a setup step or config file is needed
- Whether the skill should remember past runs
- Whether scripts or hooks would improve reliability
- Whether the skill belongs in a repo, a shared plugin, or a marketplace
- What usage signals indicate undertriggering, overtriggering, or decay

### 6. Hand Off To Implementation

When the user wants the skill built, pass the brief into `skill-creator` and ask
it to implement the files, generate realistic test prompts, and run validation.

If editing an existing skill, include the exact file paths and the smallest
content changes needed. Do not rewrite unrelated skill behavior.

## Output Format

For advisory requests, answer with:

1. Decision: create, improve, split, merge, or do not create
2. Category: one primary taxonomy category
3. Skill brief: filled from the template
4. Implementation notes: files to create/edit and validation commands
5. Risks: overbreadth, obviousness, missing setup, missing verification, or weak
   trigger description

For repository work, actually create or update the files, then run the repo's
skill validation command.

## Gotchas

- Do not make a knowledge dump. Convert article or team knowledge into decisions,
  checklists, templates, and verification.
- Do not put all details in SKILL.md. Long reference material belongs in support
  files.
- Do not write a description as a marketing summary. It must name concrete user
  phrases and contexts that should trigger the skill.
- Do not railroad the agent with brittle instructions. Provide defaults,
  decision criteria, and escape hatches.
- Do not ship a skill without at least a lightweight way to tell if it worked:
  validation commands, example prompts, expected artifacts, or usage metrics.
