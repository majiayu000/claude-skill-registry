---
name: technical-documentation
description: 'Audit, write, and improve developer documentation using Google''s Developer Documentation Style Guide and Technical Writing courses. Use this skill for any documentation work, even when the user names no style guide: "audit our docs", "review this README", "write a README", "getting started guide", "how-to or tutorial", "API reference", "docstrings", "CLI help text", "changelog or release notes", "migration guide", or "our docs are confusing". Also use it when writing docs from code, rewriting a doc for clarity, fixing headings, procedures, or code samples, or enforcing consistent voice and terminology across a docs set — prefer it over editing documentation unaided. Covers reader and doc-type fit, second person and active voice, procedures, headings, lists and tables, code samples and placeholders, link text, notices, the word list, timeless docs, and accessibility. For code comments and naming, see clean-code. For marketing or landing-page copy, see storybrand-messaging.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Technical Documentation

Audit, write, and improve developer documentation the way Google's technical writers do: start from the reader's task, verify every fact against the code, then apply the style guide in severity order — structure before voice, voice before word choice.

## Core Principle

**Write for the reader's task, not the product's feature list.** Google's guide asks for prose that is conversational but not frivolous, precise, and consistent, because a developer reading docs is trying to get something done, not to admire the product. Two framing rules from the guide shape everything below:

- **Guidelines, not rules.** Depart from the guide when doing so improves the content — established domain terminology wins — but stay consistent within the document.
- **Precedence.** A project's own style guide comes first, then Google's guide, then Merriam-Webster (spelling), the Chicago Manual of Style (general style), and the Microsoft Writing Style Guide (technical style).

Rules come in two layers. Structural and content rules (headings, procedures, code samples, second person, active voice, timeless docs, accessibility) apply to documentation in any language. Rules tagged `[EN]` (spelling, serial comma, contractions, the word list) apply only to English text — skip them for other languages, and never translate a document unless asked.

## Scoring

**Goal: 10/10.** Score = number of Quick Diagnostic rows passed (10 rows, 1 point each; the `[EN]` row auto-passes for non-English docs). Bands: **9-10** = ships as is; **7-8** = word- and voice-level edits only; **5-6** = restructure sections, then re-edit; **≤4** = rewrite from the doc-type skeleton. Blocking findings — wrong or unverifiable facts, a procedure that can't be completed, information that exists only in an image or in an image without alt text — are a separate gate: the doc is **not shippable** at any score until they're fixed. Report the score, the failed rows, and the exact edits that reach 10/10.

## Framework

### 1. Know the Reader and the Document's Job

**Core concept:** Every page serves one reader with one task. Name both before writing a word — audience and level, what they'll be able to do afterwards — and pick the document type that fits: tutorial (learn by doing), how-to (accomplish a task), concept (understand), reference (look up), README (orient and start).

**Why it works:** Readers scan for their task; a page that mixes concept, procedure, and reference forces them to read everything to find anything.

**Key insights:**
- Google's Technical Writing course opens a doc with an audience statement and a scope plus non-scope statement — the non-scope rescues readers who are on the wrong page
- "Before you begin" lists prerequisites before step 1, not inside step 4 (convention)
- Key points first: the intro states what the reader gets, not the product's history
- Every procedural page ends with verification ("Confirm that…") and "What's next" (convention)

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| README | Orient: what it is, who it's for, three-step start, links out | Purpose → install → first run → docs map |
| Mixed page | Split concept from procedure into linked pages | "How OAuth works" + "Configure OAuth" |
| Tutorial vs how-to | Tutorial teaches one path end to end; how-to assumes context | "Build your first plugin" vs "Add a hook" |

See [references/document-types.md](references/document-types.md) when choosing or restructuring a doc type — skeletons for README, getting started, tutorial, how-to, and concept pages, the audience and scope statements, and the self-editing pass for large doc sets.

### 2. Voice: You, Active, Present, Timeless

**Core concept:** Address the reader as "you", make the actor of every sentence explicit, describe behavior in the present tense, and write as if the page will be read in five years.

**Key insights:**
- "We" hides who acts; "the user" turns the reader into a third party — both weaken an instruction
- Passive voice is allowed only when the actor is unknown or irrelevant ("The file is encrypted at rest")
- "Will" belongs only to genuinely later effects: "The server sends an ack", not "will send"
- Contractions are fine — Google prefers "isn't" over "is not" for negations `[EN]`
- Software doesn't want, see, or think: "The API detects", not "the API sees"
- No "please" (reserve it for asking permission), no "simply / easily / just", no superlatives — if a step is easy, the reader will notice
- Timeless: cut "currently", "new", and "soon"; never pre-announce unreleased features

**Before → after:**
- "Please note that the new dashboard will simply be shown once the user has logged in." → "After you sign in, the dashboard appears."
- "We recommend that the token is refreshed by the client." → "Refresh the token from the client."

See [references/voice-and-words.md](references/voice-and-words.md) when a doc's tone is off or inconsistent — the voice rules with the guide's exact exceptions, inclusive and global-audience language, and the full word list.

### 3. Sentences and Words

**Core concept:** Put the condition before the instruction, keep one idea per sentence, and choose the plain word the guide's word list prefers.

**Key insights:**
- "To delete the document, click **Delete**" — readers decide whether a step applies before they act, not after
- Spell out an abbreviation on first use with the short form in parentheses; skip only universally known ones (URL, HTML)
- Latin abbreviations translate and scan poorly: "for example", not "e.g."; "that is", not "i.e."; omit "etc." or finish the list `[EN]`
- "can" = ability, "may" = permission, "might" = possibility `[EN]`
- Word list samples `[EN]`: sign in (not log in) · set up as a verb · lets you (not allows you to) · through or by using (not via) · after (not once) · use (not leverage or utilize) · checkbox · email
- Jargon is fine for the stated reader and a defect for anyone else — define it or link it

**Before → after:**
- "Click Save in order to persist the settings once you are done, i.e. when all fields are filled." → "After you fill in all fields, click **Save**."
- "The CLI utilizes the GCP SDK (e.g. for auth)." → "The CLI uses the Google Cloud SDK, for example for authentication."

See [references/voice-and-words.md](references/voice-and-words.md) when auditing word choice — the word list table (avoid → use → why), abbreviation rules, and modal verbs.

### 4. Structure: Headings, Lists, Tables, Notices

**Core concept:** Structure is the reader's map. Headings in sentence case read as a table of contents; lists carry parallel items introduced by a full sentence; tables have header rows; notices are rare and mean something.

**Key insights:**
- Task headings are bare imperatives ("Create an instance"); concept headings are noun phrases ("Instance lifecycle"); no "-ing" headings
- A list needs an introductory sentence ending in a colon, and every item in the same grammatical form; numbered only when order matters
- Description lists (term → definition) beat two-column tables for paired data
- Tables: header row, an intro sentence, no merged or empty cells — screen readers depend on it
- Note = useful but optional; Caution = proceed carefully; Warning = harm or irreversible loss. Don't stack them; one per section is a practical ceiling (inferred)
- Cross-references say "see", never "above" or "below" — pages reflow and get translated
- Link text names the target ("see Configure a custom domain"), never "click here"
- Alt text states the image's purpose; information must never live only in a picture

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Wall-of-text page | Insert a task heading wherever the task changes | "Install", "Configure", "Verify" |
| Three stacked notes | Fold two into body text; keep the one that changes behavior | One **Caution** about data loss |
| Options table | Header row + intro sentence + parallel cell phrasing | "The following flags control output:" |

See [references/structure-and-formatting.md](references/structure-and-formatting.md) when fixing page structure — heading, list, table, notice, cross-reference, link-text, image, number, and date rules with before/after pairs.

### 5. Procedures and Code

**Core concept:** A procedure is a numbered list of single imperative actions, each stating where to act and what to expect. Code is set in code font, introduced by a sentence ending in a colon, and uses placeholders the reader can't mistake for literals.

**Key insights:**
- One action per step; "Optional:" prefix for optional steps; a single step is a bullet, not "1."
- Sub-steps run a, b, c; document the shortest path, not every alternative
- UI element names in bold, matching on-screen casing; click for a mouse, tap for touch, select when device-agnostic
- Code font for filenames, paths, commands, flags, parameters, and values — not for product names
- Placeholders are `ALL_CAPS_WITH_UNDERSCORES`, never `<your-key>` or `YOUR_API_KEY`, and are explained right after the sample ("Replace `PROJECT_ID` with…")
- Command syntax: `[optional]`, `{a|b}` for exclusive choices, `...` for repeatable arguments
- Samples are runnable, minimal, wrapped at 80 characters, and show the expected output

**Before → after:**
- "Run the command below with your key: `shipit deploy --key=<your-key>`" → "To deploy, run the following command:" → fenced `shipit deploy --key=API_KEY` → "Replace `API_KEY` with the key from the **Settings** page."
- "1. You should now click on the Deploy button to deploy." → "1. Click **Deploy**. The status changes to **Deploying**."

See [references/procedures-and-code.md](references/procedures-and-code.md) when writing steps or samples — the full procedure rules, UI-element and device verbs, code-in-text, placeholder, command-line syntax, and the sample-code quality checklist.

### 6. Reference Docs: API, Docstrings, CLI Help

**Core concept:** Reference text is descriptive, complete, and formulaic on purpose — readers look things up, so every entry must exist and read the same way.

**Key insights:**
- Document every public class, method, field, constant, and enum value; a missing entry reads as "unsupported"
- Open method descriptions with the category verb: "Gets the…", "Sets the…", "Checks whether…", "Creates a…", "Returns…" — never "This method…"
- Non-boolean parameters start "The…" or "A…"; booleans read "If true, … If false, …" (action) or "True if …; false otherwise" (state)
- Document return values and exceptions ("Thrown when…") for every method that has them
- A deprecated element names its replacement in the first sentence
- CLI `--help` (convention — Google has no `--help` page): usage line in `[optional]` syntax, one-line synopsis, every flag described with the same placeholder style

**Before → after:**
- "This method is used for getting the customer." → "Gets the customer for the given `customerId`. Throws `NotFoundError` when no customer exists."
- "@param force - force flag" → "@param force If true, deletes the bucket even if it contains objects. If false, fails when the bucket isn't empty."

See [references/api-reference.md](references/api-reference.md) when writing or auditing reference material — the verb-by-category table, parameter, return, and exception patterns, one complete JSDoc example, and CLI help conventions.

### 7. Release Notes, Changelogs, Migration Guides

**Core concept:** A changelog is documentation for the reader who is about to upgrade. Each entry states what changed, what it means for them, and what to do — in the structure of Keep a Changelog, in the voice of the rest of the docs.

**Key insights:**
- Newest version first, an `Unreleased` section on top, ISO dates in version headings, version headings linked to diffs (Keep a Changelog)
- Group entries under Added / Changed / Deprecated / Removed / Fixed / Security; never paste commit messages
- Breaking changes go first in the version, with a link to migration steps (convention)
- A deprecation entry names the replacement and the removal version or date
- A migration guide is a procedure: "Before you begin" (versions, backups), numbered steps with before/after snippets, "Verify the migration", rollback
- Apply the Google layer to every entry: second person for actions, no "currently/new", code font for flags and APIs, one tense used consistently

**Before → after:**
- "Various improvements to the auth module (#412)" → "Changed: `login()` now returns a `Session` instead of a token string. Update callers that read `.token` — see *Migrate to sessions*."

See [references/release-notes.md](references/release-notes.md) when writing release notes or a migration guide — the Keep a Changelog skeleton, entry patterns per category, deprecation wording, and the migration-guide procedure.

### 8. Running the Audit, Rewrite, or Write

**Core concept:** Three modes, one discipline: intake → local conventions → read as the reader → verify facts → apply rules by severity → output in a fixed shape.

**Protocol:**
1. **Intake.** Confirm the mode (audit, improve, or write), document type, reader and level, and language. For *write*, the reader's task and the fact sources (code paths, existing docs) are required — don't start without them.
2. **Local style guide.** Look for `CONTRIBUTING.md`, `STYLE.md`, `docs/style-guide.md`, `.vale.ini`, and the conventions existing docs already follow (for example, "log in" everywhere). They win over Google. Vale with the `Google` package automates the `[EN]` word and punctuation layer if the project wants a linter.
3. **Read `references/audit-checklist.md`** before any audit or improve pass — the rule IDs cited in findings live there; never cite an ID you haven't read.
4. **Read the doc cold** as the target reader, then check every command, flag, parameter, and behavior against the code before judging style. A stylish wrong doc is worse than an ugly right one.
5. **Apply rules in severity order:** Blocking → High (structure, accessibility, missing reference entries) → Medium (voice, notices, intro sentences) → Low (word list, punctuation `[EN]`).
6. **Output.** A finding's location is one the reader can find: the heading path, plus the line number when auditing a file. Improve = a one-line `Score before → after`, the full rewritten document, then a `## Change log` table (Change | Rule ID + name | Why). Facts stay untouched — a fact stated in the source document counts as received from the user, so keep it (with `TODO(verify): …` when no code confirms it) rather than deleting it. Write = the document, with `TODO(verify)` for every gap. Never include a command, flag, or parameter you didn't see in code or receive from the user.

ALWAYS output audits in this format:

```
# Documentation Audit: [path or title]
**Score:** X/10 — [band]   **Shippable:** yes | no (blocking findings below)
**Diagnostic:** N/10 — failed rows: [row numbers + one-line reason each]
**Doc type / reader:** [type] for [audience, level]   **Language:** [en | xx — [EN] rules skipped]
**Local style guide:** [file found and honored | none — Google applies]
**Blocking:** [wrong/unverifiable facts, unfollowable steps, image-only information — or "none"]
**Findings:**
| # | Location | Rule (ID + name) | Before | After | Severity |
**Rewrite plan:** [ordered: structure → voice → words; what to do first to reach 10/10]
```

See [references/audit-checklist.md](references/audit-checklist.md) when running any audit or rewrite — the full rule table with IDs and severities, the severity rubric, non-English handling, a Vale configuration, and a worked mini-audit.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Organizing by feature instead of reader task | Readers hunt across sections for one workflow | Name the reader's task; pick the doc type; one task per page |
| Fixing style before verifying facts | Polished wrong instructions are trusted longer | Check every command and parameter against code first |
| "Click here" and "see below" | Meaningless out of context, to screen readers, and after reflow | Link text names the target; cross-refs say "see" |
| Steps buried in paragraphs, passive and future tense | Reader can't tell who does what, or in what order | Numbered imperative steps, condition first, present tense |
| Stacked Note/Warning boxes | Everything shouted, nothing heard | One notice per section; the rest becomes body text |
| `<your-key>` or `YOUR_API_KEY` placeholders | Reader types the brackets or reads the prefix as a literal | `API_KEY` in caps, explained after the sample |
| Rewriting the meaning while "fixing style" | Reviewer approves prose, ships wrong behavior | Facts unchanged; unknowns become `TODO(verify)` |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Does the first paragraph say who the doc is for and what they'll be able to do? | Readers can't tell if they're on the right page | Add audience, outcome, and non-scope statements |
| Does the doc type match the reader's task (tutorial · how-to · concept · reference · README)? | Concept and steps interleave; nothing is findable | Split by type; link between pages |
| Is every command, flag, parameter, and behavior verified against code or the user? | The doc teaches something false | Verify or mark `TODO(verify)`; not shippable until fixed |
| Do headings read as a sentence-case table of contents (tasks imperative, concepts noun phrases)? | Scanning fails; "-ing" headings hide the action | Rewrite headings; add one where each new task starts |
| Are all sequences numbered steps, one imperative action each, condition first? | Readers miss steps or act before checking | Convert paragraphs to steps; move conditions forward |
| Is every code sample introduced by a colon sentence, with `ALL_CAPS` placeholders explained? | Readers paste literals or don't know what the sample does | Add intro sentences; fix and explain placeholders |
| Is the text in second person, active voice, present tense, with no please/simply/just and no anthropomorphism? | Instructions read as narration | Rewrite sentence by sentence; cut filler |
| Are links descriptive, cross-refs "see"-based, images alt-texted, tables headed? | Screen readers and reflow break the page | Fix each; move image-only information into text |
| Is it timeless — no "currently/new/soon", no pre-announced features? | The doc rots the day it ships | Remove time words; describe only shipped behavior |
| `[EN]` Does it follow the word list, serial comma, contractions, and American spelling — or the local guide? | Small inconsistencies erode trust | Apply the word list; run Vale if configured |

## About the Source

Google's Developer Documentation Style Guide is the public house style that Google's technical writers maintain for developers.google.com, Android, and Google Cloud documentation; the companion Technical Writing One and Two courses are Google's internal engineer training, released publicly. This skill adapts both under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (per [Google's site policies](https://developers.google.com/terms/site-policies)) and adds Keep a Changelog for release notes; it is an independent adaptation, not endorsed by Google.

## Further Reading

- [Google Developer Documentation Style Guide](https://developers.google.com/style) — start with [Highlights](https://developers.google.com/style/highlights) and the [Word list](https://developers.google.com/style/word-list)
- [Technical Writing One](https://developers.google.com/tech-writing/one) and [Technical Writing Two](https://developers.google.com/tech-writing/two) — Google's courses on words, sentences, documents, self-editing, and sample code
- [Keep a Changelog](https://keepachangelog.com/) — the changelog structure this skill uses for release notes
- [*"Docs for Developers: An Engineer's Field Guide to Technical Writing"*](https://www.amazon.com/Docs-Developers-Engineers-Technical-Writing/dp/1484272161?tag=wondelai00-20) by Jared Bhatti, Zachary Sarah Corleissen, Jen Lambourne, David Nunez, and Heidi Waterhouse
- [*"Every Page Is Page One: Topic-Based Writing for Technical Communication and the Web"*](https://www.amazon.com/Every-Page-One-Topic-Based-Technical/dp/1937434281?tag=wondelai00-20) by Mark Baker
