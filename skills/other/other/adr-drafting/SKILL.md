---
name: adr-drafting
description: Creates new Architecture Decision Record (ADR) documents for significant architectural changes using a consistent template and repository-aware naming and storage guidance. Use when a user or agent decides on an architectural change, needs to document technical rationale, or wants to add a new ADR to the project history.
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
---

# ADR Drafting

Creates new Architecture Decision Record (ADR) documents for major architectural choices so teams can keep a clear history of why important technical decisions were made.

## Overview

This skill helps create a new ADR from discovery to final markdown file. It confirms the decision details, inspects the repository for any existing ADR conventions, and drafts a new ADR with the standard sections `Title`, `Status`, `Context`, `Decision`, and `Consequences`.

When the repository does not already have an ADR convention, default to storing ADRs in `docs/architecture/adr` and use a zero-padded filename such as `0001-use-postgresql-for-primary-database.md`.

See `references/template.md` for the default ADR template and `references/examples.md` for example ADRs and naming patterns.

## When to Use

Use this skill when a user or agent has decided on a meaningful architectural change and needs to document the rationale, chosen direction, and trade-offs in a new Architecture Decision Record. It fits requests such as creating an ADR, documenting an architecture decision, writing a decision record, or preserving the project history behind an important technical choice.

## Instructions

### Phase 1: Confirm the ADR inputs

Ask the user for the minimum information needed to draft a new ADR:

1. Decision title
2. Decision status (`Proposed` by default if not yet finalized)
3. Context: the problem, constraints, or forces driving the decision
4. Decision: the chosen approach
5. Consequences: what becomes easier, harder, riskier, or more expensive
6. Confirm that this request is for a **new ADR**, not for editing an existing ADR
7. Confirm the desired repository language if documentation language is unclear
8. Confirm whether any existing ADR naming convention must be preserved

If the user actually wants to update an existing ADR, change statuses in older ADRs, or manage supersession links, explain that this skill only drafts **new ADR documents** and ask whether they want to proceed with a new record instead.

### Phase 2: Discover ADR conventions in the repository

Inspect the repository before drafting:

1. Search for likely ADR locations such as:
   - `docs/architecture/adr`
   - `docs/adr`
   - `adr`
   - `architecture/adr`
2. If ADR files already exist, read one to three examples to infer:
   - numbering format
   - filename pattern
   - title format
   - language and tone
3. If no ADR directory exists, recommend `docs/architecture/adr`
4. Determine the next ADR number from existing files when possible
5. If no prior ADR exists, start with `0001`

Preferred default naming when no convention exists:

- Directory: `docs/architecture/adr`
- Filename: `NNNN-short-kebab-title.md`
- Title: `# ADR-NNNN: <Decision Title>`

### Phase 3: Draft the ADR

Create a draft using the standard structure:

```markdown
# ADR-NNNN: Decision Title

## Status
Proposed

## Context
What problem, constraints, or trade-offs led to this decision?

## Decision
What architectural choice was made?

## Consequences
What becomes easier, harder, riskier, or more expensive because of this decision?
```

Drafting rules:

- Keep the title specific and decision-oriented
- Capture enough context to explain *why* the decision was needed
- Record the chosen direction clearly and directly
- Include both positive and negative consequences when known
- Do not invent rationale, constraints, or outcomes that the user did not provide
- If critical information is missing, insert concise placeholders or ask follow-up questions before finalizing

### Phase 4: Review the draft with the user

Before writing files, present:

- proposed file path
- proposed title
- ADR status
- a concise preview of the drafted sections

Ask for approval before creating the file. If the user wants adjustments, revise the draft first.

### Phase 5: Create the ADR file

After approval:

1. Create the ADR directory if it does not exist
2. Write the ADR markdown file using the repository's established pattern when available
3. Preserve the user's wording for decision rationale as much as possible while keeping the document concise
4. Report the final file path and summarize what was created
5. Stop after creating the new ADR file so the skill remains focused on a single new decision record

## Examples

### Example 1: New database decision

**User request:** "Create an ADR for moving from SQLite to PostgreSQL"

**Expected flow:**

1. Confirm the title, status, reasons for the change, and expected consequences
2. Check whether the repository already has ADR files
3. Draft a new ADR in the existing convention or default to `docs/architecture/adr/0001-move-to-postgresql.md`
4. Ask for approval before writing the file

### Example 2: New service boundary

**User request:** "Document the decision to split billing into a dedicated service"

**Expected flow:**

1. Ask for the architectural context and why the current design is insufficient
2. Confirm the chosen boundary and the operational consequences
3. Draft a new ADR with the standard sections
4. Create the file only after user approval

See `references/examples.md` for longer ADR examples.

## Best Practices

- Keep each ADR focused on one architectural decision
- Match existing repository naming, numbering, and writing style when ADRs already exist
- Prefer concise explanations over long narratives
- Capture trade-offs honestly, including downsides and new risks
- Default the status to `Proposed` unless the user confirms another state
- Use the repository's preferred documentation language when it is clear

## Constraints and Warnings

- This skill is for **new ADR creation only**
- Do not update existing ADR files, status histories, or supersession chains
- Do not fabricate missing rationale or consequences
- Do not force `docs/architecture/adr` if the repository already uses another ADR location
- Ask clarifying questions whenever the decision, context, or consequences are too vague to document responsibly
