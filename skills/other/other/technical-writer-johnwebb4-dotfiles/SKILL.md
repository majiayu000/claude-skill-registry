---
name: technical-writer
description: Document generator that produces polished markdown for any technical document - tickets, PR descriptions, spikes, plans, reports, architecture decisions, RFCs, and proposals. Use directly when the user asks to write, draft, or summarize a document or plan, or as the writing engine called by other skills (e.g. write-tickets for ticket markdown, dev-workflow-create-pr for PR body content).
---

# Technical Writer

**The document generator.** Given knowledge, context, and a document type, this skill produces polished markdown. It does not collect requirements or manage workflows — it writes.

Other skills feed into this one. For example, `write-tickets` gathers JIRA inputs, research, and ticket plans, then passes the collected data here to generate the markdown. Any skill or user can invoke this the same way: provide the type, the knowledge, and get back a well-structured document.

## Core Writing Principles

These apply to ALL document types:

1. **Research before writing.** Explore the codebase and/or search online BEFORE drafting. A "big project" is often a "5-line config change."
2. **No assumptions.** Only include verified findings. No "likely" or "probably."
3. **Point to the door, don't walk them through the house.** Give entry points and constraints, not exhaustive file lists or step-by-step instructions.
4. **Concise over comprehensive.** Every sentence should earn its place. Cut filler.
5. **Markdown always.** All output in Markdown.
6. **GitHub links for code.** Never local paths. Always `[file.ts#L45](https://github.com/org/repo/blob/main/path/file.ts#L45)`.
7. **No open questions in output.** Ask the user BEFORE writing. The document should be actionable.
8. **Preserve source links.** If the user provides URLs (docs, Slack, Confluence), include them automatically. Don't add vague references without actual URLs.
9. **Include code examples when needed.** Use short code blocks or snippets when they clarify: bug reproduction steps, config/schema examples, API usage, or "before/after" in ADRs or docs. In ticket Tech Specs prefer links and bullets; in documentation, spikes, reports, and ADRs use code freely when it helps the reader.

## How This Skill Is Used

### Called by another skill (e.g. `write-tickets`)

The calling skill provides:
1. **Document type** (ticket-story, ticket-bug, spike, report, adr, etc.)
2. **Collected knowledge** (requirements, research findings, context, links)

This skill then:
1. Reads the appropriate template
2. Generates the markdown
3. Returns it to the calling skill

### Called directly by the user

When a user asks to write/draft a document directly:

**Step 1: Determine document type.** Use AskQuestion if not clear from context:

```
AskQuestion({
  "title": "Document Type",
  "questions": [
    {
      "id": "type",
      "prompt": "What type of document should I write?",
      "options": [
        {"id": "ticket-story", "label": "Ticket - Story / Feature"},
        {"id": "ticket-bug", "label": "Ticket - Bug Report"},
        {"id": "ticket-tech-debt", "label": "Ticket - Tech Debt"},
        {"id": "ticket-spike", "label": "Ticket - Spike / Investigation"},
        {"id": "pr-description", "label": "PR Description"},
        {"id": "plan", "label": "Plan (Development / Migration / Project / Rollout)"},
        {"id": "docs", "label": "Documentation (Feature)"},
        {"id": "spike", "label": "Spike / Investigation"},
        {"id": "report", "label": "Technical Report / Summary"},
        {"id": "adr", "label": "Architecture Decision Record"},
        {"id": "rfc", "label": "RFC / Proposal"},
        {"id": "other", "label": "Something else"}
      ]
    }
  ]
})
```

**Step 2: Collect inputs.** Ask: "Provide your requirements, context, or raw input (meeting notes, Slack threads, rough ideas, etc.)"

**Step 3: Generate.** Read the template, draft the document, present to user.

**Step 4: Confirm.** Use AskQuestion:

```
AskQuestion({
  "title": "Review Draft",
  "questions": [{
    "id": "review",
    "prompt": "How does this look?",
    "options": [
      {"id": "approve", "label": "Looks good"},
      {"id": "feedback", "label": "I have feedback"},
      {"id": "redo", "label": "Start over"}
    ]
  }]
})
```

Refine until approved.

**Step 5: Deliver.** Use AskQuestion:

```
AskQuestion({
  "title": "Output",
  "questions": [{
    "id": "output",
    "prompt": "How would you like the output?",
    "options": [
      {"id": "clipboard", "label": "Copy to clipboard"},
      {"id": "file", "label": "Save to file"},
      {"id": "done", "label": "Already have it, thanks"}
    ]
  }]
})
```

## Templates

Read the appropriate template when writing each document type. All templates are in this skill's `templates/` directory.

### Ticket Templates (`ticket-*`)

Used when writing JIRA tickets or standalone ticket descriptions.

| Type | Template |
|------|----------|
| Feature / Story | [ticket-story-template.md](templates/ticket-story-template.md) |
| Bug Report | [ticket-bug-template.md](templates/ticket-bug-template.md) |
| Tech Debt | [ticket-tech-debt-template.md](templates/ticket-tech-debt-template.md) |
| Spike / Investigation (ticket) | [ticket-spike-template.md](templates/ticket-spike-template.md) |

### PR Description

Used when writing pull request descriptions (jira/what/why/who format). Can be called by `dev-workflow-create-pr` (which supplies diff + ticket and may wrap output in `[[[` / `]]]`) or directly.

**PR description rules:**
- Output only the **jira** / **what** / **why** / **who** block; no extra headers or preamble.
- Keep each field concise (1–2 sentences; use bullets for "what" only when there are multiple distinct changes).
- Use backticks for code references. Link format: RETIRE branches → `gustohq.atlassian.net`; others → `internal.guideline.tools/jira`.
- Do not add indentation inside the block.

| Type | Template |
|------|----------|
| PR Description | [pr-description-template.md](templates/pr-description-template.md) |

### Plan Templates (`plan-*`)

Used when summarizing brainstorming sessions, strategy discussions, or project scoping into a structured plan.

| Type | Template |
|------|----------|
| Development Plan | [plan-development-template.md](templates/plan-development-template.md) |
| Migration Plan | [plan-migration-template.md](templates/plan-migration-template.md) |
| Project Plan | [plan-project-template.md](templates/plan-project-template.md) |
| Rollout Plan | [plan-rollout-template.md](templates/plan-rollout-template.md) |

### Documentation Templates (`docs-*`)

Used when documenting existing or newly shipped features.

| Type | Template |
|------|----------|
| Feature Documentation | [docs-feature-template.md](templates/docs-feature-template.md) |

### Document Templates

Used when writing standalone documents, reports, or decision records.

| Type | Template |
|------|----------|
| Spike / Investigation | [spike-template.md](templates/spike-template.md) |
| Technical Report | [report-template.md](templates/report-template.md) |
| Architecture Decision Record | [adr-template.md](templates/adr-template.md) |
| RFC / Proposal | Use ADR template with expanded Proposal section |

### Template Routing

Match the ask to the template:

| Ask | Template |
|-----|----------|
| "Create a ticket" / "Write a story" / "Feature for X" | `templates/ticket-story-template.md` |
| "File a bug" / "Bug report for X" | `templates/ticket-bug-template.md` |
| "Tech debt item" / "Refactor X" | `templates/ticket-tech-debt-template.md` |
| "Spike ticket" / "Ticket for a spike" / "Investigation ticket" | `templates/ticket-spike-template.md` |
| "Write a PR description" / "PR body" / "Describe this PR" | `templates/pr-description-template.md` |
| "Write up a plan" / "How should we build X" | `templates/plan-development-template.md` |
| "Plan the migration" / "Move from X to Y" | `templates/plan-migration-template.md` |
| "Project plan for X" / "Scope the project" | `templates/plan-project-template.md` |
| "How do we roll this out" / "Rollout plan" | `templates/plan-rollout-template.md` |
| "Summarize our brainstorm into a plan" | Pick the `templates/plan-*` type that fits; ask if ambiguous |
| "Document this feature" / "Write docs for X" | `templates/docs-feature-template.md` |
| "Investigate X" / "Spike on Y" | `templates/spike-template.md` |
| "Write up findings" / "Summarize the incident" | `templates/report-template.md` |
| "Should we use A or B?" / "ADR" | `templates/adr-template.md` |
| "Propose X" / "RFC for Y" | `templates/adr-template.md` with expanded Proposal section |
| "Document spike findings as tickets" | `templates/spike-template.md` first, then extract into `ticket-*` |

## Ticket Writing Rules

These apply when writing any ticket (feature, bug, tech debt, spike):

**Scoping tickets:**
- UI work is often a separate ticket (different skillset, different reviewer)
- Risky migrations (column deletes, renames, type changes) always get their own ticket
- Model + API changes for the same feature stay as ONE ticket
- Simple migrations bundled with the feature they enable stay together
- Changes that must be deployed together stay together

**Ordering:**
- Dependencies/prerequisites come first in the list
- Present tickets in dependency order so each can reference the ones before it

**Tech Specs (all ticket types):**
- 3-5 bullet points max
- Entry points only - where to start looking, not every file that might change
- Name patterns to reuse: "follow the X pattern" with one link
- Constraints and gotchas that will bite the implementer
- No "Files to Create" or "Files to Modify" sections
- Prefer links and bullets over code blocks here; use a short code example only when it's the clearest way to show a gotcha (e.g. a required wrapper or config line)

**Example Tech Specs section:**

```markdown
## Tech Specs

- Entry point: [useUserAccounts.ts](https://github.com/guideline-app/mobile-app/blob/main/src/features/me/hooks/useUserAccounts.ts)
- Follow pattern from [usePortfolio.ts](https://github.com/guideline-app/mobile-app/blob/main/src/features/portfolio/hooks/usePortfolio.ts)
- Gotcha: Suspense queries require a Suspense boundary - wrap in `<Suspense fallback={<LoadingScreen />}>`
```

**What NOT to include in tickets:**
- "Dependencies", "Scope Boundaries", "In Scope", "Open Questions", "Data Model", "Implementation Steps", "Files to Create", "Success Metrics" sections
- Exhaustive lists of related files
- Step-by-step implementation instructions
- Long code examples or class structures in Tech Specs (short snippets for gotchas are fine when they clarify)

**Multiple tickets from one input:**
- Analyze input for natural ticket boundaries
- Confirm the ticket plan (list + order) before writing any tickets
- Write and confirm each ticket sequentially so JIRA keys are available for cross-references

## Writing Style Guide

**Tone:** Direct, professional, no fluff. Write like a senior engineer documenting for other senior engineers.

**Structure:**
- Lead with the conclusion/decision/recommendation
- Context comes second (reader already knows why they opened this doc)
- Use bullet points over paragraphs where possible
- Tables for comparisons, always

**Technical references:**
- 3-5 bullet points max for tech specs
- Entry points only, not every file
- Name patterns to reuse with one link
- Constraints and gotchas that will bite someone

**Code examples:**
- Include code when it helps: bug reproduction, config snippets, API usage, before/after in ADRs, or feature docs. Keep examples short and focused.
- In ticket Tech Specs prefer links; use a code snippet only when it's the clearest way to convey a constraint or gotcha.

**What to cut:**
- Background the reader already knows
- Obvious statements ("we need to test this")
- Hedging language ("it might be good to consider")
- Redundant sections across templates

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing before researching | Research first - scope often shrinks dramatically |
| Local file paths | Always GitHub links with line numbers |
| Open questions in the document | Ask BEFORE writing, not in the output |
| Exhaustive file lists | 3-5 entry points max, trust the reader |
| Avoiding code when it would help | Use short code examples for bug repro, config, ADRs, docs when they clarify; in ticket Tech Specs prefer links |
| Hedging language | Be direct: "We should" not "We might want to consider" |
| Missing confirmation loop | Always confirm with AskQuestion before finalizing |
| Adding sections not in template | Use ONLY the template sections |
| Verbose context sections | Reader is a senior engineer, skip the basics |
| One mega-ticket for multi-part work | Analyze input for natural boundaries; confirm plan first |
| Splitting too granularly (model vs API) | Model + API for same feature = ONE ticket; UI can be separate |
| Bundling risky migrations with features | Column deletes/renames/type changes always get own ticket |
| Wrong ticket order | Dependencies/prerequisites come first in the list |
| "Files to Create/Modify" sections | Give entry points and patterns, not file lists |
| Full tech spec in a ticket | Tech Specs are implementation hints, not a blueprint |
| Making assumptions about codebase | Only include verified findings - no "likely" or "probably" |
