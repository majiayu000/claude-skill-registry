---
name: docs-expert
description: Guide users through structured co-authoring, improvement, and QA of documentation. Use when users want to write or improve docs such as proposals, technical specs, decision docs, READMEs, guides, API docs, or runbooks; or when they ask for doc review, doc QA, checklists, or templates to make documentation clearer, skimmable, and correct for readers.
metadata:
  short-description: Documentation co-authoring
---

# Doc Co-Authoring Workflow

## Compliance

- Check against GOLD Industry Standards guide in ~/.codex/AGENTS.override.md

This skill provides a structured workflow for guiding users through
collaborative document creation. Act as an active guide, walking users through
three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## Philosophy

- Clarity over completeness: prefer a smaller, readable doc with explicit

  gaps.

- Reader-first structure: optimize for how someone will consume the doc.
- Evidence over assertion: back claims with sources or rationale.

## Table of Contents

- [When to Offer This Workflow](#when-to-offer-this-workflow)
- [Quickstart (Lightweight Path)](#quickstart-lightweight-path)
- [Stage 1: Context Gathering](#stage-1-context-gathering)
- [Stage 2: Refinement & Structure](#stage-2-refinement--structure)
- [Stage 3: Reader Testing](#stage-3-reader-testing)
- [Final Review](#final-review)
- [Docs Expert (Baseline Practices)](#docs-expert-baseline-practices)
- [In-code documentation (TS/JS/React, Swift, config

  files)](#in-code-documentation-tsjsreact-swift-config-files)

- [Definition of Done and Evidence (Gold

  Standard)](#definition-of-done-and-evidence-gold-standard)

- [Deliverable format](#deliverable-format)
- [References and templates](#references-and-templates)
- [Official documentation links (use when citing

  standards)](#official-documentation-links-use-when-citing-standards)

- [Docs Upkeep Runbook (Short)](#docs-upkeep-runbook-short)
- [brAInwav Brand Styling (Include when styling

  artifacts)](#brainwav-brand-styling-include-when-styling-artifacts)

## When to Offer This Workflow

**Trigger conditions:**

- User mentions writing documentation: "write a doc", "draft a proposal",

  "create a spec", "write up"

- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a large writing task

**Initial offer:** Offer the user a structured workflow for co-authoring the
document. Explain the three stages:

1. **Context Gathering**: User provides all relevant context while you ask

   clarifying questions

2. **Refinement & Structure**: Iteratively build each section through

   brainstorming and editing

3. **Reader Testing**: Test the doc with a fresh model (no context) to catch

   blind spots before others read it

Explain that this approach helps ensure the doc works well when others read it
(including when they paste it into a model). Ask if they want to try this
workflow or prefer to work freeform.

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Quickstart (Lightweight Path)

Use this when the user wants help quickly and does not want the full
three-stage workflow.

1. Collect the minimal inputs (doc target, audience, job-to-be-done,

   constraints).

2. Propose a tight outline (3-6 sections) and confirm it.
3. Draft the highest-impact section first.
4. Run a fast QA pass (clarity, missing steps, top 3 failure points).
5. Offer to switch to the full workflow if the scope grows or ambiguity

   remains.

## Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what you know,
enabling smart guidance later.

### Initial Questions

Start by asking the user for meta-context about the document:

1. What document is this? (e.g., technical spec, decision doc, proposal)
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?
6. Does this doc require brAInwav brand styling or the documentation

   signature? If it's a root README, assume yes unless the user opts out.

Tell them they can answer in shorthand or dump information in any format that
works for them.

**If user provides a template or mentions a doc type:**

- Ask if they have a template document to share
- If they provide a link to a shared document, use the appropriate integration

  to fetch it

- If they provide a file, read it

**If user mentions editing an existing shared document:**

- Use the appropriate integration to read the current state
- Check for images without alt-text
- If images exist without alt-text, explain that when others use a model to

  understand the doc, the model won't be able to see them. Ask if they want
  alt-text generated. If so, request they paste each image into chat for
  descriptive alt-text generation.

### Info Dumping

Once initial questions are answered, encourage the user to dump all the
context they have. Request information such as:

- Background on the project/problem
- Related team discussions or shared documents
- Why alternative solutions aren't being used
- Organizational context (team dynamics, past incidents, politics)
- Timeline pressures or constraints
- Technical architecture or dependencies
- Stakeholder concerns

Tell them not to worry about organizing it - just get it all out. Offer more
than one way to provide context:

- Info dump stream-of-consciousness
- Point to team channels or threads to read
- Link to shared documents

**If integrations are available** (e.g., Slack, Teams, Google Drive,
SharePoint, or other MCP servers), mention that these can be used to pull in
context directly.

**If no integrations are detected:** Suggest they can enable connectors in
their settings to allow pulling context from messaging apps and document
storage directly.

Inform them clarifying questions will be asked once they've done their initial
dump.

**During context gathering:**

- If user mentions team channels or shared documents:
  - If integrations available: Inform them the content will be read now, then

    use the appropriate integration

  - If integrations not available: Explain lack of access. Suggest they enable

    connectors in settings, or paste the relevant content directly.

- If user mentions entities/projects that are unknown:
  - Ask if connected tools should be searched to learn more
  - Wait for user confirmation before searching

- As user provides context, track what's being learned and what's still

  unclear

**Asking clarifying questions:**

When user signals they've done their initial dump (or after enough context is
provided), ask clarifying questions to ensure understanding:

Generate 5-10 numbered questions based on gaps in the context.

Inform them they can use shorthand to answer (e.g., "1: yes, 2: see #channel,
3: no because backwards compat"), link to more docs, point to channels to
read, or just keep info-dumping. Pick the fastest path for them.

**Exit condition:** Enough context has been gathered when questions show
understanding - when edge cases and trade-offs can be asked about without
needing basics explained.

**Transition:** Ask if there's any more context they want to provide at this
stage, or if it's time to move on to drafting the document.

If user wants to add more, let them. When ready, proceed to Stage 2.

## Stage 2: Refinement & Structure

**Goal:** Build the document section by section through brainstorming,
curation, and iterative refinement.

**Instructions to user:** Explain that the document will be built section by
section. For each section:

1. Clarifying questions will be asked about what to include
2. 5-20 options will be brainstormed
3. User says what to keep/remove/combine
4. The section will be drafted
5. It will be refined through surgical edits

Start with the section that has the most unknowns (the core
decision/proposal), then work through the rest.

**Section ordering:**

If the document structure is clear: Ask which section they'd like to start
with.

Suggest starting with the section that has the most unknowns. For decision
docs, that's the core proposal. For specs, that's the technical approach.
Summary sections are best left for last.

If user doesn't know what sections they need: Based on the document and
template, suggest 3-5 sections appropriate for the doc type.

Ask if this structure works, or if they want to adjust it.

**Doc type mapping (fast defaults):**

| Doc type |
| --- |
| Technical spec |
| Decision doc |
| README |
| Runbook |
| API doc |
| Proposal/PRD |

**Once structure is agreed:**

Create the initial document structure with placeholder text for all sections.

**If access to artifacts is available:** Use `create_file` to create an
artifact. This gives both you and the user a scaffold to work from.

Inform them that the initial structure with placeholders for all sections will
be created.

Create artifact with all section headers and brief placeholder text like "[To
be written]" or "[Content here]".

Provide the scaffold link and say it's time to fill in each section.

**If no access to artifacts:** Create a markdown file in the working
directory. Name it appropriately (e.g., `decision-doc.md`,
`technical-spec.md`).

Inform them that the initial structure with placeholders for all sections will
be created.

Create file with all section headers and placeholder text.

Confirm the filename has been created and say it's time to fill in each
section.

**For each section:**

### Step 1: Clarifying Questions

Announce work will begin on the [SECTION NAME] section. Ask 5-10 clarifying
questions about what should be included:

Generate 5-10 specific questions based on context and section purpose.

Inform them they can answer in shorthand or just say what's important to
cover.

### Step 2: Brainstorming

For the [SECTION NAME] section, brainstorm [5-20] things that might be
included, depending on the section's complexity. Look for:

- Context shared that might have been forgotten
- Angles or considerations not yet mentioned

Generate 5-20 numbered options based on section complexity. At the end, offer
to brainstorm more if they want more options.

### Step 3: Curation

Ask which points should be kept, removed, or combined. Request brief
justifications to help learn priorities for the next sections.

Provide examples:

- "Keep 1,4,7,9"
- "Remove 3 (duplicates 1)"
- "Remove 6 (audience already knows this)"
- "Combine 11 and 12"

**If user gives freeform feedback** (e.g., "looks good" or "I like most of it
but...") instead of numbered selections, extract their preferences and
proceed. Parse what they want kept/removed/changed and apply it.

### Step 4: Gap Check

Based on what they've selected, ask if there's anything important missing for
the [SECTION NAME] section.

### Step 5: Drafting

Use `str_replace` to replace the placeholder text for this section with the
actual drafted content.

Announce the [SECTION NAME] section will be drafted now based on what they've
selected.

**If using artifacts:** After drafting, provide a link to the artifact.

Ask them to read through it and say what to change. Note that being specific
helps learning for the next sections.

**If using a file (no artifacts):** After drafting, confirm completion.

Inform them the [SECTION NAME] section has been drafted in [filename]. Ask
them to read through it and say what to change. Note that being specific helps
learning for the next sections.

**Key instruction for user (include when drafting the first section):**
Provide a note: Instead of editing the doc directly, ask them to say what to
change. This helps learning of their style for future sections. For example:
"Remove the X bullet - already covered by Y" or "Make the third paragraph more
concise".

### Step 6: Iterative Refinement

As user provides feedback:

- Use `str_replace` to make edits (never reprint the whole doc)
- **If using artifacts:** Provide link to artifact after each edit
- **If using files:** Just confirm edits are complete
- If user edits doc directly and asks to read it: note the changes they made

  and keep them in mind for future sections

**Continue iterating** until user is satisfied with the section.

### Quality Checking

After 3 consecutive iterations with no major changes, ask if anything can be
removed without losing important information.

When section is done, confirm [SECTION NAME] is complete. Ask if ready to move
to the next section.

**Repeat for all sections.**

### Near Completion

As approaching completion (80%+ of sections done), announce intention to
re-read the entire document and check for:

- Flow and consistency across sections
- Redundancy or contradictions
- Anything that feels like filler or generic
- Whether every sentence carries weight

Read entire document and provide feedback.

**When all sections are drafted and refined:** Announce all sections are
drafted. Say you will review the complete document one more time.

Review for coherence, flow, completeness.

Provide any final suggestions.

Ask if ready to move to Reader Testing, or if they want to refine anything
else.

## Stage 3: Reader Testing

**Goal:** Test the document with a fresh model (no context bleed) to verify it
works for readers.

**Instructions to user:** Explain that testing will now occur to see if the
document actually works for readers. This catches blind spots - things that
make sense to the authors but might confuse others.

### Testing Approach

**If access to sub-agents is available:**

Perform the testing directly without user involvement.

### Testing Rubric (Deterministic)

Use this to make reader testing predictable and comparable across docs.

**Question template (pick 5-10):**

1. What is this doc for, and who is it for?
2. What are the prerequisites or assumptions?
3. What is the primary workflow or decision?
4. What are the exact steps to achieve the outcome?
5. How do I verify success?
6. What are the failure modes and how do I recover?
7. What are the risks, constraints, or non-goals?
8. Who owns this, and how do I get help?

**Pass criteria:**

- At least 80% of answers are correct and complete.
- No critical misunderstandings on safety, data loss, security, or rollback.
- Ambiguities are localized to one section or less, and can be fixed in one

  edit pass.

### Step 1: Predict Reader Questions

Announce intention to predict what questions readers might ask when trying to
discover this document.

Generate 5-10 questions that readers would realistically ask.

### Step 2: Test with Sub-Agent

Announce that these questions will be tested with a fresh instance (no context
from this conversation).

For each question, invoke a sub-agent with just the document content and the
question.

Summarize what the reader got right/wrong for each question.

### Step 3: Run Extra Checks

Announce extra checks will be performed.

Invoke sub-agent to check for ambiguity, false assumptions, contradictions.

Summarize any issues found.

### Step 4: Report and Fix

If issues found: Report that the reader struggled with specific issues.

List the specific issues.

Say you will fix these gaps.

Loop back to refinement for problematic sections.

---

**If no access to sub-agents:**

The user will need to do the testing manually.

### Step 1: Predict Reader Questions (manual)

Ask what questions people might ask when trying to discover this document.
What would they type into a model?

Generate 5-10 questions that readers would realistically ask.

### Step 2: Setup Testing

Provide testing instructions:

1. Open a fresh conversation
2. Paste or share the document content (if using a shared doc platform with

   connectors enabled, provide the link)

3. Ask the reader the generated questions

For each question, instruct the reader to provide:

- The answer
- Whether anything was ambiguous or unclear
- What knowledge/context the doc assumes is already known

Check if the reader gives correct answers or misinterprets anything.

### Step 3: Extra Checks

Also ask the reader:

- "What in this doc might be ambiguous or unclear to readers?"
- "What knowledge or context does this doc assume readers already have?"
- "Are there any internal contradictions or inconsistencies?"

### Step 4: Iterate Based on Results

Ask what the reader got wrong or struggled with. Say you will fix those gaps.

Loop back to refinement for any problematic sections.

---

### Exit Condition (Both Approaches)

When the reader consistently answers questions correctly and doesn't surface
new gaps or ambiguities, the doc is ready.

## Final Review

When Reader Testing passes: Announce the doc has passed reader testing. Before
completion:

1. Recommend they do a final read-through themselves - they own this document

   and are responsible for its quality

2. Suggest double-checking any facts, links, or technical details
3. Ask them to verify it achieves the impact they wanted

Ask if they want one more review, or if the work is done.

**If user wants final review, provide it. Otherwise:** Announce document
completion. Provide a few final tips:

- Consider linking this conversation in an appendix so readers can see how the

  doc was developed

- Use appendices to provide depth without bloating the main doc
- Update the doc as feedback is received from real readers

## Docs Expert (Baseline Practices)

## Mission

Produce documentation that gets useful information into a reader's head
quickly, with minimal cognitive load, and with practical paths to success
(examples + troubleshooting).

## Notes

- Short description: Make docs skimmable, clear, and broadly helpful.
- Version: 1.0.0.
- Category: documentation.
- Compatibility: Works best in repos with Markdown docs. Optional tooling (if

  present): markdownlint/vale. No internet required.

## Inputs to collect (minimal)

1. Doc target(s): file path(s) or feature/component name.
2. Audience: beginner vs experienced; known prerequisites.
3. Primary job-to-be-done: what the reader is trying to do.
4. Constraints: supported platforms, required versions, security/compliance

   requirements.

If the user did not provide these, infer from repo context (existing docs,
package.json, tool configs) and state assumptions explicitly.

## Outputs

- Updated Markdown docs (PR-ready edits).
- A short "Doc QA" summary of what changed and what to verify.
- If information is missing/unknown: a TODO list of specific facts the team

  must confirm.

- If branding applies: include brand compliance results and evidence

  (signature + assets).

- An evidence bundle that records lint outputs, brand check output, and

  checklist snapshot.

## Operating procedure

### 1) Locate and scope

- Identify the canonical doc surface(s): README, /docs, /guides, /runbooks,

  /api, etc.

- Do not rewrite everything. Pick the smallest set of files that solves the

  user task.

### 1a) Capture doc requirements

Record these at the top of the doc or in a visible "Doc requirements" section:

- Audience tier (beginner, intermediate, expert).
- Scope and non-scope (what this doc covers and does not cover).
- Doc owner and review cadence.
- Required approvals or stakeholders.

### 2) Build a skimmable structure first

- Create/repair a clear outline with sections that match reader questions.
- Add a table of contents for longer docs.
- Use headings as informative sentences (not vague nouns).

### 3) Write for skim-reading

Apply these rules aggressively:

- Keep paragraphs short; use one-sentence paragraphs for key points.
- Start sections/paragraphs with a standalone topic sentence.
- Put the topic words at the beginning of topic sentences.
- Put takeaways before procedure (results first, then steps).
- Use bullets and tables whenever they reduce scanning time.
- Bold truly important phrases sparingly (what to do, what not to do, critical

  constraints).

### 4) Write clean, unambiguous prose

- Prefer simple sentences; split long ones.
- Remove filler/adverbs and needless phrasing.
- Avoid hard-to-parse phrasing and ambiguous sentence starts.
- Prefer right-branching phrasing (tell readers early what the sentence

  connects to).

- Avoid "this/that" references across sentences; repeat the specific noun

  instead.

- Be consistent (terminology, casing, naming conventions, punctuation style).

### 4a) Capture risk and assumptions

If the doc involves operational steps, safety, or data impact, add a "Risks
and assumptions" section that includes:

- Assumptions the doc relies on.
- Failure modes and blast radius.
- Rollback or recovery guidance.

### 5) Be broadly helpful (optimize for beginners without annoying experts)

- Explain simply; do not assume English fluency.
- Avoid abbreviations; write terms out on first use.
- Proactively address likely failure points (env vars, PATH, permissions,

  ports, tokens).

- Prefer specific, accurate terminology over insider jargon.
- Keep examples general and exportable (minimal dependencies, self-contained

  snippets).

- Focus on common/high-value tasks over edge cases.
- Do not teach bad habits (e.g., hardcoding secrets, unsafe defaults).

### 6) Accessibility and inclusive design

- Use descriptive link text; avoid "click here".
- Ensure heading order is logical and no levels are skipped.
- Provide alt text for non-decorative images; mark decorative images as such.
- Avoid instructions that rely only on color, shape, or spatial position.
- Prefer inclusive, plain language and avoid ableist or exclusionary phrasing.

### 7) Security, privacy, and safety pass

- Never expose real secrets, tokens, or internal endpoints; use placeholders.
- Avoid encouraging destructive or irreversible commands without warnings and

  backups.

- Call out PII handling and data retention considerations when relevant.
- Prefer least-privilege guidance for credentials, access, and permissions.

### 8) Check content against the repo

- Never invent commands, flags, file paths, outputs, or version numbers.
- Cross-check installation steps with actual configs (package scripts,

  Makefile, Dockerfile, CI).

- If you cannot verify a detail, flag it as needing confirmation.

### 9) Run doc linters (when available)

- If `.vale.ini` exists, run `vale {doc}` and record results.
- If markdownlint config exists, run `markdownlint-cli2 {doc} --config

  {config}`.

- If link-check tooling exists, run it and record results.
- If tooling is missing, state what is missing and how to enable it.
- If `scripts/check_readability.py` exists, run it and record the score and

  target range (default target: 45-70 Flesch Reading Ease; override with
  `--min/--max` or use `--no-range`).

### 9a) Automation hooks (optional)

Use these commands in CI or pre-commit, adjusting paths to your repo:

```sh
vale <doc>
markdownlint-cli2 <doc> --config <config>
python /path/to/check_brand_guidelines.py --repo . --docs <doc>
python /path/to/check_readability.py <doc>
```

### 10) Finish with verification hooks

- Add "Verify" steps readers can run (expected output, health checks).
- Add Troubleshooting for the top 3 predictable failures.
- Ensure the doc has a clear "Next step" path.

### 11) Brand compliance pass (when applicable)

If branding, visual formatting, or a root README is in scope, read
`references/BRAND_GUIDELINES.md` and enforce these requirements:

- Add the documentation signature to root README files.
- Ensure `brand/` assets exist and match the approved formats.
- Do not add watermarks to technical docs.
- Apply color/typography guidance only where visual formatting is requested.
- Treat missing signature/assets as blocking; list them in Open questions and

  do not mark the doc complete.

- If `scripts/check_brand_guidelines.py` exists, run it against the repo root.

  Pass the current doc with `--docs {doc}` and include the output in the
  results section.

**If the user asks to update or install brand guidelines in the repo:**

- Copy `references/BRAND_GUIDELINES.md` into the repo (default target:

  `brand/BRAND_GUIDELINES.md`).

- Copy the full contents of `assets/brand/` into the repo (default target:

  `brand/`).

- If the repo expects a different path or filename (e.g., `BRANDGUIDELINES.md`

  without underscore), ask and mirror that naming.

### 12) Acceptance criteria and evidence bundle

Add a short acceptance checklist and an evidence bundle at the end of the doc:

- Acceptance criteria: 5-10 checkboxes that must be true before completion.
- Evidence bundle: lint output, brand check output, readability output, and

  checklist snapshot.

## In-code documentation (TS/JS/React, Swift, config files)

### TS/JS + React (JSDoc/TSDoc)

Document public APIs (exports), non-obvious utilities, hooks, and any
function/component with constraints.

Required content for public symbols:

- One-line summary starting with a verb (e.g., "Creates...", "Renders...")
- `@param` for non-trivial params (include units, allowed values, defaults)
- `@returns` (or React render contract if it returns JSX)
- `@throws` for thrown errors (name + condition)
- `@example` for anything with more than one "correct" usage
- `@deprecated` when applicable (include migration hint)

React-specific:

- Document props contract (required/optional, default behavior,

  controlled/uncontrolled)

- Document accessibility contract: keyboard behavior, focus management, ARIA

  expectations

- For hooks: document dependencies, side effects, and SSR constraints

Rules:

- For public symbols, explain what the code does (behavior/contract), not just

  why.

- Inline comments explain why/constraints, not what the code already says.
- Do not invent; docs must match implementation and tests.

### Swift (DocC / SwiftDoc)

Use `///` DocC comments for public types/methods, and anything with tricky
invariants.

Required content for public symbols:

- Summary sentence
- `- Parameters:` and `- Returns:` (when applicable)
- `- Throws:` (conditions and error meaning)
- `- Important:` for invariants/constraints
- `- Warning:` for footguns (threading, main-actor, performance, security)
- `- Example:` for non-obvious usage

Best practice (richer DocC directives):

- Add `### Discussion` to explain behavior, edge cases, and tradeoffs.
- Add `- Complexity:` when time/space cost is non-trivial.
- Use `- Note:` for usage guidance and `- Attention:` for user-impacting

  caveats.

- Use `## Topics` and `### {Group}` to cluster related symbols on type docs.
- Add a "See Also" list when there are close alternatives or companion APIs.

Concurrency:

- Document actor/isolation expectations (`@MainActor`, thread-safety)

  explicitly.

### Config files (JSON / TOML / YAML)

Goal: readers can safely edit config without guessing.

- Prefer a schema + docs:
  - JSON: `.schema.json` + examples (since JSON cannot have comments)
  - YAML/TOML: inline comments are allowed, but still link to schema/spec
- Document:
  - Each key's meaning, type, defaults, allowed values
  - Security-sensitive keys (tokens, paths, network endpoints)
  - Migration notes when keys change
- Provide at least one minimal example and one full example.

Validation rule:

- Config docs must reference the validating mechanism (Zod schema, JSON

  Schema, or typed config loader).

## Definition of Done and Evidence (Gold Standard)

For any significant doc work, provide evidence that the Gold Industry Standard
bar is met.

**Required evidence (fill in):**

Standards mapping:

- [ ] CommonMark/Markdown structure and formatting
- [ ] Accessibility and inclusive language basics
- [ ] Security/privacy guidance for sensitive info
- [ ] Brand compliance (when branding or README signature applies)

Automated checks (if available):

- [ ] markdownlint/vale/link check (list commands run)
- [ ] Brand check script output (if branding applies)
- [ ] Readability check output (if available)

Review artifact:

- [ ] Self-review summary or peer review note

Deviations (if any):

- [ ] Description, risk, mitigation

## Anti-patterns to avoid

- Writing without confirming audience and purpose.
- Burying key decisions or risks in long prose.
- Shipping drafts without a verification pass.

## Deliverable format

When you finish edits, include:

1. Summary of changes (3-7 bullets).
2. Doc QA checklist results (use `references/CHECKLIST.md`).
3. Open questions / requires confirmation (explicit list, no hand-waving).
4. Brand compliance results (if applicable) with evidence of signature and

   assets.

5. Evidence bundle (lint output, brand check output, readability output,

   checklist snapshot).

If you touch in-code documentation, also include Code Doc QA checklist results
(use `references/CODE_DOC_CHECKLIST.md`).

## References and templates

- Doc QA checklist: `references/CHECKLIST.md`
- Code Doc QA checklist: `references/CODE_DOC_CHECKLIST.md`
- Doc template skeleton: `assets/DOC_TEMPLATE.md`
- Code doc templates (JSDoc and language equivalents):

  `assets/CODE_DOC_TEMPLATES.md`

- README example template: `assets/README_TEMPLATE.md`
- AGENTS example template: `assets/AGENTS_TEMPLATE.md`
- Anthropic brand guidelines reference: `references/BRAND_GUIDELINES.md`
- Brand asset pack: `assets/brand/`
- Doc co-authoring workflow reference: `references/DOC_COAUTHORING.md`
- Automation scripts: `scripts/check_brand_guidelines.py`,

  `scripts/check_readability.py`

## Official documentation links (use when citing standards)

- [MDX docs](https://mdxjs.com/docs/)
- [Markdown (CommonMark spec)](https://spec.commonmark.org/)
- [Markdown (original syntax)](https://daringfireball.net/projects/markdown/syntax)
- [JSDoc](https://jsdoc.app/)
- [Swift DocC (overview)](https://www.swift.org/documentation/)
- [Swift DocC (API docs)](https://swiftlang.github.io/swift-docc/documentation/swiftdocc/)

---

## Remember

The agent is capable of extraordinary work in this domain. These guidelines
unlock that potential—they don't constrain it. Use judgment, adapt to context,
and push boundaries when appropriate.

## Docs Upkeep Runbook (Short)

Use this when maintaining docs over time.

## Versioning

- Add a visible “Last updated” date to top-level docs.
- Use semantic versioning for public API docs and note breaking changes.
- Keep a changelog for major docs when behavior changes.

## Deprecation

- Mark deprecated sections with a date and replacement link.
- Keep deprecated content for at least one release cycle.
- Remove only after migration guidance is published.

## Ownership

- Assign a clear doc owner per major doc.
- Require owner approval for structural changes.
- Review docs at least once per release.

## Metrics Loop (Docs ROI)

Use this to track whether docs are working.

- Support deflection: track tickets or questions that docs should prevent.
- Onboarding time: measure time-to-first-success for new users.
- FAQ deflection: measure repeated questions before/after doc updates.
- Search success: track search terms that lead to page exits or “no results.”

---

## brAInwav Brand Styling (Include when styling artifacts)

Use this section to ensure all artifacts and documentation follow brAInwav
brand guidelines when visual formatting is requested or relevant.

## Overview

To access brAInwav's official brand identity and style resources, use this
skill.

**Keywords**: branding, corporate identity, visual identity, post-processing,
styling, brand colors, typography, brAInwav brand, visual formatting, visual
design

## Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems
