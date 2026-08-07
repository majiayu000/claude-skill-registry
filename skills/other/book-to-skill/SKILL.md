---
name: book-to-skill
description: 'Use when turning a book, course, whitepaper, or comparable source document into a reusable agent skill: the user names a source and asks to distill it, encode its method, or build an agent that works the way it prescribes. Classifies the source as procedure or reference, writes a validated SKILL.md, and proves the trigger fires before finishing.'
argument-hint: "Which book or document should become a skill?"
---

Turn a source document into a skill the agent can run. Nine steps, each with a done condition. The source is a single book, course, paper, or comparable document; a folder of sources belongs to `map-corpus`, not here.

## 1. Read the source

Inventory the source at the level the document affords: chapters, top-level headings, or sections. Show that inventory as one line per unit with its heading slug where one exists. A file the agent cannot open stops the run and is named; this skill owns no converter either. Done when the inventory covering every top-level unit is shown.

## 2. Classify

Ask: can you name three or more ordered actions, each with a checkable done-state? Three or more, **procedure** (a sequence the agent can follow). Fewer, **reference** (distinctions and rules consulted on demand). Both present, a procedure spine with the judgment material in `references/`. Done when the classification is stated with the three actions named, or with the statement that fewer than three exist.

## 3. Extract into four buckets

Sort what you read: coined terms and leading words, constraints and prohibitions, procedures with their completion criteria, and deep material destined for `references/`. Done when every inventoried unit has contributed to a bucket or is marked as out of scope for the skill.

## 4. Name it

Kebab-case matching `^[a-z0-9]+(-[a-z0-9]+)*$`, at most 64 characters, identical to the directory name. Done when the name matches the directory you will write to.

## 5. Write the frontmatter

`description` at most 1024 characters, front-loaded, one trigger per genuinely distinct branch, phrased positively. Redirect rather than forbid: "for X, use skill Z" rather than "do not use for X". Done when the `description` parses as single-quoted YAML and is within the limit.

## 6. Write the body

Write the body in the shape its classification selects, from [references/OUTPUT-SHAPES.md](references/OUTPUT-SHAPES.md). Include one attribution line naming title, author, and year. Paraphrase throughout; quote only a coined term or named law where the exact phrasing is the idea. Done when the body follows its shape and carries the attribution.

## 7. Disclose

Material only some branches reach moves to `references/<topic>.md`, linked one level deep from the body. Keep the body under 500 lines. Done when branch-specific material lives behind a pointer and the body line count is under the cap.

## 8. Validate

Check four conditions: `name` equals the directory name; the frontmatter parses as YAML; `description` is within 1024 characters; every relative link resolves on disk. Run `yaml.safe_load` on the frontmatter and `test -f` on each link target. Done when all four pass.

## 9. Probe and place

Author three to five probe prompts — at least two that must fire the skill, at least two out-of-scope prompts that must not — and run each in a subagent. Adjust the `description` until every probe lands correctly. Then ask for the write target, defaulting to `.claude/skills/<name>/`, and re-run step 8 there. Done when probe results are reported and the checks are green at the target.

## Rules

- One skill per run. Another source is another run.
- Paraphrase the source; do not paste it.
- Keep the skill runnable without the source in context. The skill, not the book, is the source of truth when the skill runs.
