---
name: create-rfc
description: >-
  Draft a populated RFC from conversation context, research artifacts, and codebase analysis.
  Use when a topic has been discussed or researched and needs to be captured as a formal technical proposal.
argument-hint: "<topic>"
---

# Create RFC

Draft a populated RFC for the given topic. This is NOT a blank template — gather context and write a real first draft.

## Instructions

### 1. Determine the Topic

- If `$0` is provided, use it as the RFC topic
- If `$0` is empty, ask the user what the RFC should be about

### 2. Gather Context

Search for existing information about the topic before writing:

1. **Conversation context** — review the current conversation for discussion, decisions, and research already conducted
2. **Research artifacts** — search for related research documents (check `docs/30-research/`, `docs/50-research/`, `docs/research/`)
3. **Memory files** — grep the memory directory for cached research on the topic
4. **Codebase** — scan relevant source files to understand the current state (the "before" picture)
5. **ADRs** — check for related architecture decisions (check `docs/20-architecture/22-adr/`, `docs/20-architecture/adr/`, `docs/adr/`)

### 3. Confirm Scope with User

Before drafting, present a brief summary of what you found and the proposed RFC scope. Ask the user to confirm or adjust. Use `AskUserQuestion` with key scoping choices if there are meaningful alternatives.

### 4. Read the Template

Read the template structure from the `review-rfc` skill's `templates/rfc-template.md` (sibling skill directory). Use this as the section structure for the RFC.

### 5. Draft the RFC

Write a populated RFC filling **every section** with substantive content based on the gathered context:

- **Summary**: 1-2 paragraph overview of the proposal
- **Motivation**: Real problems from the codebase/discussion, not placeholder text
- **Goals / Non-Goals**: Specific, actionable items
- **Architecture Overview**: Concrete technical approach with package names, file paths, patterns
- **Diagram**: Mermaid diagram showing the proposed architecture or data flow
- **Data Model**: Actual schema changes or "no changes required" with rationale
- **APIs**: Real endpoints or "no API changes" with rationale
- **Infrastructure**: Deployment impact assessment
- **Security Considerations**: Specific to this proposal
- **Scalability**: Realistic load assessment
- **Observability**: What to monitor
- **Risks and Mitigations**: Real risks with likelihood/impact assessment
- **Alternatives Considered**: At least 2 alternatives with clear rejection rationale
- **Migration Plan**: Step-by-step with rollback strategy
- **Open Questions**: Genuine unresolved decisions (not filler)

Set **Author** to the git user name, **Status** to `Draft`, **Date** to today.

### 6. Discover RFC Directory

Determine where to write the RFC:

1. **Detect jd-docs**: Check if `.jd-config.json` exists or `docs/20-architecture/` directory exists
2. **Resolve directory**:
   - If jd-docs detected → use `docs/20-architecture/rfcs/`
   - Else if `docs/rfcs/` exists → use `docs/rfcs/`
   - Else → create `docs/rfcs/` as default

### 7. Auto-Number and Write

1. Glob for existing RFCs in the resolved directory and all fallback paths (`docs/rfcs/*.md`, `docs/20-architecture/rfcs/*.md`, `.arkhe/rfcs/*.md`) to find the highest existing RFC number
2. Assign the next sequential number (zero-padded to 4 digits)
3. Ask the user to confirm the title — generate a kebab-case filename slug
4. Write to `<resolved-dir>/NNNN-[slug].md`

### 8. Suggest Next Steps

After writing the RFC, suggest:
- `/review-rfc <path-to-new-rfc>` — to get a design review
- Manual review by team members

## Quality Standards

- Every section must contain real content, not placeholder text like `[describe here]`
- Reference specific files, packages, and patterns from the codebase
- If a section genuinely doesn't apply (e.g., no data model changes), state that explicitly with a one-line rationale — don't leave it blank
- The draft should be good enough to review immediately, not a skeleton to fill in later
