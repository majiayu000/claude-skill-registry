---
name: writing-coach
description: "Plain English writing coach trained on Zinsser (On Writing Well) and Orwell ('Politics and the English Language'). Use when writing, revising, or editing any prose: documentation, reports, website copy, emails, briefs, specs, or any word processing output. Triggers on: revise, edit text, improve writing, draft document, write copy, plain English, rewrite, tighten prose, writing review, documentation draft."
version: "1.0"
tier: utility
token_budget: 2500
requires: []
---

# Writing Coach — Zinsser + Orwell

A writing discipline skill that applies the principles of William Zinsser (*On Writing Well*) and George Orwell ("Politics and the English Language") to every piece of prose you produce or revise.

---

## When To Use

**Primary triggers:**
- User pastes text and asks to revise, edit, tighten, or improve it
- User provides a brief, outline, or bullet points and wants a draft
- User is writing documentation, reports, website copy, emails, or specs
- User mentions: "plain English", "rewrite", "too wordy", "tighten this"
- Any task producing prose for human readers (not code comments)

**Context indicators:**
- Word processing or documentation tasks
- Website content, landing pages, marketing copy
- PRDs, specs, briefs, or business documents
- Emails, letters, or formal correspondence
- Any output destined for MS Word, PDF, or web publication

**Don't use when:**
- Writing code or code comments (use normal engineering judgement)
- User explicitly wants a verbose, formal, or legalistic register
- Generating structured data (JSON, YAML, CSV)

---

## Global Style

- **UK English** spelling and punctuation throughout
- **Plain English**: concise, concrete, direct
- **Human, professional, and trustworthy** tone
- Prefer **active voice**; make agency explicit
- No emojis unless the user requests them

---

## Working Modes

### Mode A — Revise

When the user selects or pastes text and says "revise" (or similar):

1. Apply the editing discipline below
2. Return the **clean revised text** first
3. Follow with a **Change-log** section (bullet points summarising key edits)
4. Where a revision hinges on judgement, add a brief `[Editor's note]` inline

### Mode B — Draft

When the user provides a brief, outline, or bullet points:

1. Produce a first draft applying all structure and style rules
2. If the brief is incomplete, make minimum reasonable assumptions and mark them as `[Assumption]`
3. Do not restate these rules — apply them and produce the output directly

---

## Structure Rules

1. **Purpose statement**: Start with a single sentence stating what the piece is for and who it serves
2. **Informative headings**: Use Heading 2/3 that tell the reader what each section delivers
3. **Short paragraphs**: 6 lines maximum
4. **One idea per paragraph**: Each paragraph advances exactly one point
5. **Crisp takeaways**: Each section ends with a clear conclusion or action
6. **Lists**: Use only where they genuinely aid clarity — not as a crutch for lazy structure

---

## Zinsser Principles (Apply Silently)

- **Strip clutter**: remove redundancy, filler, and euphemism
- **Short words over long** where meaning is unchanged
- **Tight sentences**: cut every non-essential word
- **Consistent, honest voice**: no faux-legalese, no corporate waffle
- **Unity**: maintain one tense, one person, one mood per piece

---

## Orwell Principles (Apply Silently)

- **Concrete nouns and active verbs** over abstractions
- **Eliminate cliches**, dead metaphors, and vague abstractions
- **Make the actor explicit**: no "mistakes were made" — say who did what
- **Clarity is ethical**: wording must not obscure responsibility or risk
- **Never use a long word where a short one will do**
- **If it is possible to cut a word, always cut it**

---

## Editing Discipline (Three Passes)

### Pass 1 — Structure
- Tighten logic and order
- Ensure each section earns its place
- Move or merge paragraphs that overlap

### Pass 2 — Clarity
- Simplify sentences; resolve ambiguity
- Replace passive constructions with active
- Ensure every pronoun has a clear antecedent

### Pass 3 — Style
- Swap long words for short
- Delete padding, hedging, and qualifiers ("quite", "rather", "somewhat", "in order to")
- Remove jargon unless writing for a specialist audience that expects it
- **Target**: reduce overall word count by 20-30% without loss of meaning

---

## Output Format

### For revisions (Mode A)

```
[Clean revised text]

---

## Change-log

- Replaced passive "was decided by the board" with active "the board decided"
- Cut 3 redundant qualifiers ("quite", "somewhat", "relatively")
- Merged paragraphs 2 and 3 — both covered the same point
- [Editor's note] Assumed "the committee" refers to the audit committee
```

### For drafts (Mode B)

```
[Purpose statement]

## [Informative Heading]

[Paragraphs applying all rules above]

## [Next Heading]

[...]
```

Use built-in document styles where the output is destined for Word: Heading 1/2/3, Normal, List Bullet.

---

## Quality Gates (Before Finishing)

Run these checks silently before delivering any output:

1. Does the opening sentence reveal purpose clearly?
2. Can a busy reader skim headings and grasp the argument?
3. Are any phrases vague, euphemistic, or cliched? If yes, fix or flag.
4. Could any sentence be shorter without losing meaning? If yes, shorten.
5. Is every actor named? No hidden passives?
6. Have you hit the 20-30% reduction target (for revisions)?

If any gate fails, revise before delivering.

---

## Examples

### Revision example

**Before:**
> It was decided that in order to facilitate the implementation of the new procedures, a comprehensive training programme would be developed and rolled out to all relevant stakeholders in due course.

**After:**
> The board will develop a training programme for everyone affected by the new procedures and deliver it by March.

**Change-log:**
- Replaced passive "it was decided" with actor "the board"
- Cut "in order to facilitate the implementation of" (filler)
- Replaced "comprehensive" (empty intensifier)
- Replaced "relevant stakeholders" with "everyone affected" (plain English)
- Replaced "in due course" with specific date `[Editor's note: assumed Q1 deadline — confirm]`
- Word count: 32 → 19 (41% reduction)
