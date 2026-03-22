---
name: speci5.plan
description: "Read a story spec and create a concrete implementation plan with tasks in .spec/features/<feature>/<story>/plan.md. Analyzes the codebase to produce specific, actionable tasks with file paths, function names, and unit test coverage aligned to the project tech stack. WHEN: /plan, create plan, plan story, break down story, implementation tasks, plan implementation, what to build. DO NOT USE FOR: brainstorming ideas (use brainstorm), writing specs (use specify), checking implementation (use check)."
argument-hint: "Path to the story folder, e.g. .spec/features/user-auth/login-with-email"
---

# Plan

Read a story spec and create a concrete implementation plan.

Start by understanding the story and the codebase, then produce specific, actionable tasks. Only ask questions if the spec has genuine ambiguities that would lead to a wrong plan.

<HARD-GATE>
Do NOT implement code, modify specs, create features, or brainstorm ideas. This skill ONLY produces plan files in `.spec/features/<feature>/<story>/plan.md`.
</HARD-GATE>

## Triggers

Activate this skill when the user wants to:
- Create an implementation plan for a story
- Break a story into concrete development tasks
- Understand what needs to be built for a story
- Update an existing plan with revised tasks

## Rules

1. Tasks must be **specific and actionable** — not vague ("implement feature") but concrete ("Create `POST /api/auth/login` route in `src/routes/auth.ts`").
2. Include unit test tasks as a first-class part of every plan (not optional). Tie each test task to acceptance criteria and existing test conventions.
3. If a `plan.md` already exists, update it — preserve any checked-off tasks and add/revise remaining ones.
4. Do NOT modify `story.md` or `feature.md` — those are the **specify** skill's domain.
5. Do NOT implement the code — only produce the plan.
6. **YAGNI ruthlessly** — Every task must tie back to an acceptance criterion. If it doesn't serve the story, leave it out.
7. Be tech-stack-specific: reference the actual frameworks, libraries, runtime, test runner, and folder conventions found in the target codebase. Avoid generic wording.

## Conversation Style

- **Bias toward action.** If the story and codebase give enough information, produce the plan directly.
- **Only ask when genuinely blocked** — ambiguous acceptance criteria, multiple conflicting interpretations, or a technical decision with no clear answer.
- **One question at a time** if you do need to ask.
- **Prefer multiple choice** when possible.

## Steps

1. **Read the story** — Load `.spec/features/<feature>/<story>/story.md`.
2. **Read the feature** — Load the parent `feature.md` for broader context.
3. **Analyze the codebase** — Go beyond the story. Understand:
   - Project structure, tech stack, and conventions.
   - Unit testing setup (test framework, mocking tools, naming/file patterns, test commands, coverage expectations).
   - What related code already exists.
   - Where new code should be placed.
   - Existing patterns to follow (routing conventions, test structure, naming, etc.).
4. **Check scope** — If the story is too large or covers multiple independent concerns, flag it. Help decompose into smaller stories before planning. Each plan should be completable in a focused session.
5. **Ask clarifying questions (only if needed)** — If acceptance criteria are genuinely ambiguous or a technical decision has no clear answer from the codebase, ask. Otherwise, proceed.
6. **Propose 2-3 implementation approaches** — Present different strategies with trade-offs (e.g., new module vs. extending existing, library vs. hand-rolled). Lead with your recommendation and explain why. Include testing implications for each approach.
7. **Write the plan** — Once aligned with the user, write ordered, actionable tasks to `.spec/features/<feature>/<story>/plan.md`.
   - Include explicit unit test tasks with concrete test file paths, test case intent, and the project's actual test tooling.
   - Include validation task(s) that run the relevant project test command(s) (for example, targeted test file command and/or package script used in this repo).
8. **Present for review** — Show the plan and confirm it looks right before considering the job done.

## Output Format

See [output template](./assets/output.md).
