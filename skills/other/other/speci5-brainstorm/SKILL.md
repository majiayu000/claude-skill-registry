---
name: speci5.brainstorm
description: "Elaborate and expand user input into structured idea documents in .spec/ideas/. Takes rough thoughts, researches patterns, surfaces trade-offs and open questions. WHEN: /brainstorm, brainstorm idea, new idea, capture idea, explore concept, elaborate on, think about, research idea. DO NOT USE FOR: writing specs (use specify), creating plans (use plan), checking implementation (use check)."
argument-hint: "Describe the idea or concept you want to brainstorm"
---

# Brainstorm

Turn rough ideas into well-structured idea documents through collaborative dialogue.

Start by understanding the project context and the user's intent, then ask clarifying questions before elaborating. The goal is a thinking artifact — not a formal spec.

<HARD-GATE>
Do NOT create feature files, story files, specs, plans, or code. This skill ONLY produces idea documents in `.spec/ideas/`. The **specify** skill is the next step.
</HARD-GATE>

## Triggers

Activate this skill when the user wants to:
- Capture a new idea or concept
- Elaborate on a rough thought
- Research patterns, prior art, or trade-offs for an idea
- Update or refine an existing idea document

## Rules

1. Use **kebab-case** for all filenames (e.g., `user-auth.md`).
2. Do NOT create feature or story files — that's the **specify** skill's job.
3. If updating an existing idea, preserve human-written content and append/refine rather than overwrite.
4. Keep language clear and concise — this is a thinking artifact, not a formal spec.
5. **YAGNI ruthlessly** — Strip unnecessary complexity. Simpler ideas are better ideas. If a feature isn't clearly needed, leave it out.

## Conversation Style

- **One question at a time.** Don't overwhelm the user with multiple questions in one message.
- **Prefer multiple choice** when possible — easier to answer than open-ended.
- **Be flexible** — go back and clarify when something doesn't make sense.

## Steps

1. **Explore project context** — Scan `.spec/ideas/` for existing ideas, but also check the codebase, docs, and recent changes to understand what's already built and what patterns are in use. Ideas don't exist in a vacuum.
2. **Check scope** — If the user's input describes multiple independent subsystems or a very large surface area, flag this immediately. Help decompose into smaller, independent ideas before elaborating. Each idea should be a single cohesive concept.
3. **Ask clarifying questions** — Before writing anything, ask questions one at a time to understand purpose, constraints, and success criteria. Don't skip this even for "simple" ideas — unexamined assumptions cause the most wasted work.
4. **Propose 2-3 approaches** — Present different ways to tackle the idea, with trade-offs for each. Lead with your recommendation and explain why.
5. **Write or update** — Once you and the user are aligned, write the idea document. If the input closely relates to an existing idea file, **update** it. Otherwise, **create** a new file in `.spec/ideas/`.
6. **Present** — Show the user the resulting idea document and highlight any open questions.

## Output Format

See [output template](./assets/output.md).
