---

name: write-article
description: End-to-end workflow for writing an article in the Real World AI Log project, focusing on practice-first, workflow-first collaboration.
version: 0.1
------------

# write-article

This skill manages the **full article lifecycle** for the project **AI 实践记录 / Real World AI Log**.

The goal is not to maximize writing speed, but to enforce a **clear, reviewable, and repeatable workflow**.

Agents using this skill must behave as collaborators, not autonomous authors.

---

## When to Use

Use this skill when:

* Starting a new article from an idea or rough topic
* Turning an experience or practice into a structured article
* Managing multi-step writing with explicit human checkpoints

Do NOT use this skill for:

* Minor edits or copy changes
* Style-only polishing
* One-off brainstorming

---

## Core Philosophy

* Practice > theory
* Process > polished conclusions
* Human judgment > agent autonomy
* Small steps > big jumps

The agent must **never skip planning or confirmation steps**.

---

## Required Workflow

### Phase 1: Context Intake (Mandatory)

Before proposing any outline or text, the agent MUST:

1. Read `README.md`
2. Read `AGENTS.md`
3. Scan the latest 2–3 files in `content/published/`
4. Identify:

   * Target audience (explicit or assumed)
   * Relevant column/series (if any)
   * Tone constraints and boundaries

The agent must summarize its understanding in 5–7 bullet points.

STOP and wait for confirmation if understanding is unclear.

---

### Phase 2: Planning & Outline Proposal (Mandatory)

The agent MUST propose **2–3 outline options**, each including:

* Central question or problem statement
* Intended reader takeaway
* High-level section list
* Trade-offs (why choose / not choose this outline)

The agent MUST:

* Explicitly ask the human to choose one option
* NOT proceed until a choice is confirmed

---

### Phase 3: Task Breakdown (Mandatory)

After an outline is confirmed, the agent MUST:

1. Break the work into small tasks, typically:

   * Create outline file → `content/outlines/<slug>.md`
   * Create draft file → `content/drafts/<slug>.md`
2. Describe what each task will produce
3. Ask for confirmation before executing tasks

**CRITICAL TASK FLOW**:
- Task 1 (Create outline file): Execute, then WAIT for user confirmation or manual edits
- Task 2 (Create draft file): Execute ONLY AFTER user explicitly confirms the outline is finalized

No task execution without approval.

---

### Phase 4: Execution (Controlled)

For each approved task:

* Execute **one task at a time**
* Produce a concrete artifact in the correct folder
* Summarize what was done
* Ask whether to continue to the next task

Do NOT chain tasks without explicit approval.

---

### Phase 5: Self-Review & Checks

After draft completion, the agent MUST self-check for:

* Logical flow and clarity
* Overconfident or authoritative tone
* Missing concrete examples
* Redundancy or unnecessary abstraction
* Alignment with project principles

The agent should output:

* A short review summary
* A list of suggested human edits (not applied automatically)

---

## Writing Constraints

The agent MUST follow these constraints:

* No hype or exaggerated AI claims
* Prefer first-person reflective tone when appropriate
* Avoid tutorial-style commands
* Use short to medium paragraphs
* Do not pretend to have final answers

---

## Guardrails (Hard Rules)

* ❌ Do not start writing without an approved outline
* ❌ Do not publish or move files to `published/`
* ❌ Do not invent facts or experiences
* ❌ Do not overwrite existing files without permission

If uncertain, STOP and ask.

---

## Success Criteria

This skill is successful when:

* The human can easily review, modify, or stop the process
* Each step produces a clear, inspectable artifact
* The workflow reduces cognitive load for future writing
* The result feels honest, grounded, and practice-driven

Consistency and clarity are more important than speed.
