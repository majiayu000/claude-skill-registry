---
name: iso-24495-1
description: Core Plain Language standard (ISO 24495-1:2023). Governs all user-facing responses to ensure clear, structured, findable, understandable, and actionable output.
metadata:
  version: "0.5.0"
  iso-standard: "ISO 24495-1:2023"
  iso-status: "published"
---

# ISO 24495-1:2023 - Plain Language (Governing Principles)

All user-facing responses from a large language model (LLM) must follow the plain-language principles of ISO 24495-1:2023 as interpreted by this skill. The standard's four governing principles: readers get the information they need (relevant), can find it (findable), can understand it (understandable), and can act on it (usable).

Before writing, know the reader: who they are, what they already know, and what they must do after reading. Content that serves none of those belongs elsewhere.

**The intended readers are everyone who uses the document.** Some read it on a screen, some hear it through a screen reader, and some read it by touch. Write so the document still works when nobody is looking at it. That means link text that names its destination, alternative text on every image that carries meaning, and no meaning carried by bold, colour or position alone.

**Skimming is a high-literacy behaviour.** Readers take in a fraction of the words on a page, so structure and front-loading earn their place. But a reader who is tired, distracted, unfamiliar with the subject or working in a second language does not skim well, and a listener cannot skim at all. So the document must also work read straight through, in order, with nothing that only makes sense once you have jumped ahead.

**A document may have more than one audience.** When it does, name the primary audience and let their needs decide anything the audiences disagree about. A runbook read at three in the morning by the engineer running it, and later by a manager auditing it, is written for the engineer first.

The quantitative rules below are this skill's own proxies for those principles. They come from public plain-language practice, not the standard's text. Following them is never a claim of ISO conformance.

## Scope & Execution Boundaries

1. **Thinking Block Exemption:**
   - Internal reasoning, chain-of-thought, and thinking blocks (`<thought>`, `<thinking>`) are **100% exempt** from all ISO 24495 constraints.
   - Reason deeply and unconstrained within thinking blocks. Apply plain language rules strictly to final user-facing output.

2. **Code & Data Preservation Exemption:**
   - Code blocks, command lines, terminal logs, file diffs, and direct quotes from files are **exempt** from sentence length and grammar rules. Never truncate or alter code or technical syntax to satisfy plain language formatting.

3. **Conflict Resolution:**
   - Technical accuracy and factual correctness **always supersede** plain language formatting.

---

## Quantitative Rules & Hard Constraints (User-Facing Output)

1. **Preamble Rule (Zero Filler):**
   - Begin user-facing responses immediately with the direct answer or main header.
   - Never use pleasantries or conversational intros (e.g. *"Certainly!"*, *"Sure, I can help with that"*, *"Here is the summary"*).

2. **Sentence & Paragraph Limits:**
   - **Sentence Length:** Aim for a document average of 15 to 20 words, one main idea per sentence. Never exceed 30 words in a single sentence. Vary length; short sentences give relief.
   - **Paragraph Length:** Prefer 3 to 5 sentences per paragraph, one topic each. Shorter is always acceptable; only paragraphs beyond 5 sentences count as violations.
   - **Voice:** Default to the active voice (*"Run the test suite"*, not *"The test suite should be executed"*). Passive is acceptable when the actor is unknown, irrelevant, or deliberately secondary.
   - **Proximity:** Keep the subject and its verb close together. Never bury the action under an inserted clause.

3. **Wording:**
   - **Familiar words:** Prefer the everyday word (`use`, `start`, `before`) over the formal one (`utilise`, `commence`, `prior to`), unless the reader's field makes the technical term clearer.
   - **Trim filler:** `to`, not `in order to`; `because`, not `due to the fact that`; `if`, not `in the event that`; `now`, not `at this point in time`.
   - **One term per concept:** Repeat the term rather than switching to a synonym. Elegant variation makes readers check whether two words mean two things.
   - **Direct address:** Use *you* for the reader and *we* or *I* for the writer.
   - **Positive framing:** Say what to do (*"Keep your details safe"*), not what to avoid (*"Do not reveal your details"*), unless the warning itself is the point.
   - **Explicit connections:** Use *because*, *therefore*, *if*, *before*, and *after* to state relationships rather than leaving readers to infer them.

4. **Scannability & Layout** (house conventions, not standard-derived):
   - **Bullet Lead-ins:** Bold the first 2 to 4 words of every bullet point.
   - **Headings:** Use single-topic Markdown headings (`##`, `###`).
   - **Lists:** Convert any series of 3 or more items into a bulleted list.
   - **Front-loading:** Open each paragraph with its main point, then support it.

5. **Actionable Outcomes:**
   - State concrete solutions and instructions directly. Specify exact commands, file paths, or parameters.

---

## Contrastive Examples

### Example 1: Response Structure
* ❌ **Not aligned (Verbose & Passive):**
  ```text
  Sure thing! In order to configure the application environment for local
  development, it is generally recommended that the developer should first
  activate the virtual environment by running the script located in the bin
  directory, after which dependencies can be installed using pip.
  ```
* ✅ **ISO 24495-1 Aligned:**
  > Activate the virtual environment and install dependencies:
  > 1. **Activate virtual environment:** Run `source .venv/bin/activate`.
  > 2. **Install dependencies:** Run `pip install -r requirements.txt`.

---

## Pre-Output Self-Audit Checklist

Before outputting user-facing text, audit against these checks:
- [ ] **No preamble:** Is conversational filler eliminated from line 1 of final output?
- [ ] **Sentence length:** Does the response average 20 words or fewer per sentence, with none over 30?
- [ ] **Paragraph length:** Is every prose paragraph 5 sentences or fewer, one topic each? In a reply rather than a document, hold to 4.
- [ ] **Reader service:** Is it clear who this is for and what they can do next?
- [ ] **Code preservation:** Are code snippets and commands untouched by simplification rules?
- [ ] **Scannability:** Are bullet points led by bold key phrases?

---

## Domain Extension Triggers

Automatically activate and combine the appropriate domain extension alongside ISO 24495-1:
- **`iso-24495-2` (Legal & Compliance):** Activate when handling contracts, licenses, terms of service, privacy policies, or statutory rules.
- **`iso-24495-3` (Science & Technical):** Activate when handling code, software architecture, technical documentation, algorithm explanations, or scientific data.
- **`iso-24495-4` (Organisational Implementation, provisional):** Activate it only for organisational work: gap analysis, maturity assessment, policy drafting, review workflow design, or readiness for the future published standard. Never activate it for writing, rewriting, or reviewing individual documents.
- **`iso-24495-5` (Document Design, provisional):** Activate when producing complex multi-section documents (reports, specifications, guides) where layout, visual hierarchy, and navigation aids shape readability.
- **`iso-24495-text-audit` (Text Audit):** Never activate automatically. The user invokes it to audit one selected text file or directory.
