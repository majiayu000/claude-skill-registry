---
name: learn
version: 3.0.0
description: "[Utilities] Teach Claude lessons that persist across sessions. Triggers on 'remember this', 'always do', 'never do', 'learn this', 'from now on'. Smart routing to the most relevant reference doc."
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

## Quick Summary

**Goal:** Teach Claude lessons that persist across sessions by saving to the most relevant reference doc.

**Workflow:**

1. **Capture** -- Identify the lesson from user instruction or experience
2. **Route** -- Analyze lesson content and select the best target file (see routing table)
3. **Save** -- Append lesson to the selected file
4. **Confirm** -- Acknowledge what was saved and where

**Key Rules:**

- Triggers on "remember this", "always do X", "never do Y"
- Smart-route to the most relevant file, NOT always `docs/project-reference/lessons.md`
- Check for existing entries before creating duplicates
- Confirm target file with user before writing

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Lesson Learning Skill

Teach Claude lessons that persist across sessions. Lessons are smart-routed to the most relevant reference doc and automatically injected into prompts and before file edits.

## Usage

### Add a lesson

```
/learn always use the validation framework fluent API instead of throwing ValidationException
/learn never call external APIs in command handlers - use Entity Event Handlers
/learn prefer async/await over .then() chains
```

### List lessons

```
/learn list
```

### Remove a lesson

```
/learn remove 3
```

### Clear all lessons

```
/learn clear
```

## Smart File Routing (CRITICAL)

When saving a lesson, analyze its content and route to the **most relevant file**:

| If lesson is about...                                                                                                     | Route to                                                | Section hint                                                    |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| Code review rules, anti-patterns, review checklists, YAGNI/KISS/DRY, naming conventions, review process                   | `docs/project-reference/code-review-rules.md`           | Add to most relevant section (anti-patterns, rules, checklists) |
| Backend C# patterns: CQRS, repositories, entities, validation, message bus, background jobs, migrations, EF Core, MongoDB | `docs/project-reference/backend-patterns-reference.md`  | Add to relevant section or Anti-Patterns section                |
| Frontend Angular/TS patterns: components, stores, forms, API services, BEM, RxJS, directives, pipes                       | `docs/project-reference/frontend-patterns-reference.md` | Add to relevant section or Anti-Patterns section                |
| Integration tests: test base classes, fixtures, test helpers, test patterns, assertions                                   | `docs/project-reference/integration-test-reference.md`  | Add to relevant section                                         |
| General lessons, workflow tips, tooling, AI behavior, project conventions, anything not matching above                    | `docs/project-reference/lessons.md`                     | Append as dated list entry                                      |

### Prevention Depth Assessment (MANDATORY before saving)

Before saving any lesson, critically evaluate whether a doc update alone is sufficient or a deeper prevention mechanism is needed:

| Prevention Layer                            | When to use                                                        | Example                                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Doc update only**                         | One-off awareness, rare edge case, team convention                 | "Always use fluent validation API" → `docs/project-reference/backend-patterns-reference.md` |
| **Prompt rule** (`development-rules.md`)    | Rule that ALL agents must follow on every task                     | "Grep after bulk edits" → `.claude/workflows/development-rules.md`                          |
| **System Lesson** (`prompt-injections.cjs`) | Universal AI mistake, high recurrence, silent failure, any project | "Re-read files after context compaction" → `.claude/hooks/lib/prompt-injections.cjs`        |
| **Hook** (`.claude/hooks/`)                 | Automated enforcement, must never be forgotten                     | "Dedup markers must match" → `lib/dedup-constants.cjs` + consistency test                   |
| **Test** (`.claude/hooks/tests/`)           | Regression prevention, verifiable invariant                        | "All hooks import from shared module" → test in `test-all-hooks.cjs`                        |
| **Skill update** (`.claude/skills/`)        | Workflow step that should always include this check                | "Review changes must check doc staleness" → skill SKILL.md update                           |

**Decision flow:**

1. **Capture** the lesson
2. **Ask:** "Could this mistake recur if the AI forgets this lesson?" If yes → needs more than a doc update
3. **Ask:** "Can this be caught automatically by a test or hook?" If yes → recommend hook/test
4. **Evaluate System Lesson promotion** (see below)
5. **Present options to user** with `AskUserQuestion`:
    - "Doc update only" — save to the best-fit reference file (default for most lessons)
    - "Doc + prompt rule" — also add to `development-rules.md` so all agents see it
    - "Doc + System Lesson" — also add to `prompt-injections.cjs` System Lessons (see criteria below)
    - "Full prevention" — plan a hook, test, or shared module to enforce it automatically
6. **Execute** the chosen option. For "Full prevention", create a plan via `/plan` instead of just saving.

### System Lesson Promotion (MANDATORY evaluation)

After generalizing a lesson, evaluate whether it qualifies as a **System Lesson** in `.claude/hooks/lib/prompt-injections.cjs`. System Lessons are injected into EVERY prompt — they are the highest-visibility prevention layer.

**Qualification criteria (ALL must be true):**

1. **Universal** — Applies to ANY AI coding project, not just this codebase
2. **High recurrence** — AI agents make this mistake repeatedly across sessions without the reminder
3. **Silent failure** — The mistake produces no error/warning; it silently degrades output quality
4. **Not already covered** — No existing System Lesson addresses the same root cause

**Current System Lessons** (read `.claude/hooks/lib/prompt-injections.cjs` → `injectLessonReminder()` → "Common AI Mistake Prevention" section to check for duplicates).

**If qualified:** Recommend "Doc + System Lesson" option. On user approval, append the lesson as a new bullet to the System Lessons array in `prompt-injections.cjs` following the existing format: `` `- **Bold title.** Explanation sentence.` ``

**If NOT qualified:** Explain why (e.g., "Too project-specific", "Already covered by existing System Lesson about X", "Low recurrence — only happens in rare edge cases"). Proceed with doc-only or prompt-rule option.

### Lesson Quality Gate (MANDATORY before saving)

Every lesson MUST be **generic and reusable across any project**. Before saving:

1. **Analyze root cause** — Why did this mistake happen? What is the underlying pattern?
2. **Generalize** — Strip project-specific names, file paths, and tool names. Express the lesson as a universal principle.
3. **Verify universality** — Would this lesson help an AI working on a completely different codebase? If no → rewrite until yes.

**Anti-pattern examples:**

- BAD: "Always check `lib/dedup-constants.cjs` for marker strings" → project-specific path
- GOOD: "When consolidating modules, ensure shared constants are imported from a single source of truth — never define inline duplicates."
- BAD: "Update `.claude/docs/hooks/README.md` after deleting hooks" → project-specific file
- GOOD: "Deleting components causes documentation staleness cascades — map all referencing docs before removal."

### Routing Decision Process

1. **Read the lesson text** — identify keywords and domain
2. **Apply Lesson Quality Gate** — analyze root cause, generalize, verify universality
3. **Run Prevention Depth Assessment** — determine if doc-only or deeper prevention needed
4. **Match against routing table** — pick the best-fit file
5. **Tell the user:** "This lesson fits best in `docs/{file}`. Confirm? [Y/n]"
6. **On confirm** — read target file, find the right section, append the lesson
7. **On reject** — ask user which file to use instead

### Format by Target File

**For `docs/project-reference/lessons.md`** (general lessons):

```markdown
- [YYYY-MM-DD] <lesson text>
```

**For pattern/rules files** (code-review-rules, backend-patterns, frontend-patterns, integration-test):

- Find the most relevant existing section in the file
- Append the lesson as a rule, anti-pattern entry, or code example
- Use the file's existing format (tables, code blocks, bullet lists)
- If no section fits, append to the Anti-Patterns or general rules section

## Budget Enforcement (MANDATORY for `docs/project-reference/lessons.md`)

`docs/project-reference/lessons.md` is injected into EVERY prompt and EVERY file edit. Token budget must be controlled.

**Hard limit:** 3000 characters (~1000 tokens). Check BEFORE saving any new lesson.

**Workflow when adding to `docs/project-reference/lessons.md`:**

1. Read file, count characters (`wc -c docs/project-reference/lessons.md`)
2. If current + new lesson > 3000 chars → trigger **Budget Trim** before saving
3. If under budget → save normally

**Budget Trim process:**

1. Display all current lessons with char count each
2. Evaluate each lesson on two axes:
    - **Universality** — How often does this apply? (every session vs rare edge case)
    - **Recurrence risk** — How likely is the AI to repeat this mistake without the reminder?
3. Score each: **HIGH** (keep as-is), **MEDIUM** (candidate to condense), **LOW** (candidate to remove)
4. Present to user with `AskUserQuestion`: "Budget exceeded. Recommend removing/condensing these LOW/MEDIUM items: [list]. Approve?"
5. On approval: condense MEDIUM items (shorten wording), remove LOW items, then save new lesson
6. On rejection: ask user which to remove/condense

**Condensing rules:**

- Remove examples, keep the rule: `"Patterns like X break Y syntax"` → just state the rule
- Merge related lessons into one if they share the same root cause
- Target: each lesson ≤ 250 chars (one concise sentence + bold title)

**Does NOT apply to:** Other routing targets (`backend-patterns-reference.md`, `code-review-rules.md`, etc.) — those files have their own size and are injected contextually, not on every prompt.

## Behavior

1. **`/learn <text>`** — Route and append lesson to the best-fit file (check budget if target is `lessons.md`)
2. **`/learn list`** — Read and display lessons from ALL 5 target files (show file grouping + char count for `lessons.md`)
3. **`/learn remove <N>`** — Remove lesson from `docs/project-reference/lessons.md` by line number
4. **`/learn clear`** — Clear all lessons from `docs/project-reference/lessons.md` only (confirm first)
5. **`/learn trim`** — Manually trigger Budget Trim on `docs/project-reference/lessons.md`
6. **File creation** — If target file doesn't exist, create with header only

## Auto-Inferred Activation

When Claude detects correction phrases in conversation (e.g., "always use X", "remember this", "never do Y", "from now on"), this skill auto-activates via `infer: true`. When auto-inferred (not explicit `/learn`), **confirm with the user before saving**: "Save this as a lesson? [Y/n]"

## Storage

Lessons are distributed across 5 files:

| File                                                    | Content type                             |
| ------------------------------------------------------- | ---------------------------------------- |
| `docs/project-reference/code-review-rules.md`           | Review rules, anti-patterns, conventions |
| `docs/project-reference/backend-patterns-reference.md`  | Backend C# patterns and rules            |
| `docs/project-reference/frontend-patterns-reference.md` | Frontend Angular/TS patterns and rules   |
| `docs/project-reference/integration-test-reference.md`  | Test patterns and rules                  |
| `docs/project-reference/lessons.md`                     | General lessons (fallback)               |

## Injection

Lessons are injected by `lessons-injector.cjs` hook on:

- **UserPromptSubmit** — `docs/project-reference/lessons.md` content (with dedup)
- **PreToolUse(Edit|Write|MultiEdit)** — `docs/project-reference/lessons.md` content (always)
- Pattern reference files are injected by their respective hooks (`code-patterns-injector.cjs`, `code-review-rules-injector.cjs`, etc.)
