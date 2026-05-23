---
name: speci5.specify
description: "Transform idea documents from .spec/ideas/ into structured feature and story specs in .spec/features/. Creates feature.md and story.md files organized by feature folders and story subfolders. WHEN: /specify, write spec, create spec, turn idea into spec, specify feature, define stories, break down feature, structure requirements. DO NOT USE FOR: brainstorming ideas (use brainstorm), creating plans (use plan), checking implementation (use check)."
argument-hint: "Name the idea(s) to specify, or leave blank to process all ideas"
---

# Specify

Transform idea documents into structured feature and story specs.

Start by understanding the ideas and the existing codebase, then produce clear, testable specifications. Only ask questions if the idea has genuine ambiguities that would lead to a wrong spec.

<HARD-GATE>
Do NOT create plan files, implement code, or brainstorm ideas. This skill ONLY produces `feature.md` and `story.md` files in `.spec/features/`. The **plan** skill is the next step.
</HARD-GATE>

## Triggers

Activate this skill when the user wants to:
- Convert ideas into formal feature/story specifications
- Break a feature down into deliverable stories
- Create or update feature and story specs
- Structure requirements from idea documents

## Rules

1. Use **kebab-case** for all folder and file names.
2. Each story must have concrete, testable acceptance criteria.
3. Stories should be small enough to implement in a single focused effort.
4. Do NOT create `plan.md` files — that's the **plan** skill's job.
5. Link stories in `feature.md` using relative paths.
6. If features/stories already exist, update them — do not overwrite human edits.
7. Present the proposed feature/story breakdown to the user for confirmation before writing files.
8. **YAGNI ruthlessly** — If a story isn't clearly needed for the feature's goals, leave it out. Fewer well-defined stories beat many vague ones.

## Conversation Style

- **Bias toward action.** If the idea and codebase give enough information, produce the specs directly.
- **Only ask when genuinely blocked** — ambiguous intent, multiple conflicting interpretations, or missing information that can't be inferred.
- **One question at a time** if you do need to ask.
- **Prefer multiple choice** when possible.

## Steps

1. **Read ideas** — Read the specified idea file(s) from `.spec/ideas/`. If none specified, read all.
2. **Explore project context** — Go beyond the ideas. Check the codebase, docs, and existing specs to understand what's already built, what conventions exist, and what patterns to follow. Specs should be grounded in reality.
3. **Read existing specs** — Scan `.spec/features/` to avoid duplicating or conflicting with what's already specified.
4. **Check scope** — If an idea covers multiple independent capabilities or is too broad, flag it. Help decompose into separate features before specifying. Each feature should be a single cohesive capability.
5. **Ask clarifying questions (only if needed)** — If the idea has genuine ambiguities or missing information that can't be inferred from context, ask. Otherwise, proceed.
6. **Synthesize** — Break ideas into **features** (cohesive capabilities) and **stories** (independently deliverable slices of a feature).
7. **Propose** — Present the feature/story breakdown with a brief rationale. Get user confirmation before writing files.
8. **Write specs** — For each feature, create a folder with `feature.md`. For each story, create a subfolder with `story.md`.
9. **Present for review** — Show the written specs and confirm they look right before considering the job done.

## Folder Structure

```
.spec/features/
  <feature-slug>/
    feature.md
    <story-slug>/
      story.md
```

## Output Formats

See [output templates](./assets/output.md).
