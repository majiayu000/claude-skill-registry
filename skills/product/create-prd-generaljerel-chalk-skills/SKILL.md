---
name: create-prd
description: Create a structured Product Requirements Document when the user asks to write a PRD, define requirements, or spec out a feature
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feature or problem description]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: docs, product, planning
---

# Create PRD

## Overview

Generate a problem-first Product Requirements Document with measurable success metrics, testable acceptance criteria, and clearly scoped boundaries. Every PRD starts from the user problem, not the solution.

## Workflow

1. **Read product context** — Scan `.chalk/docs/product/` for the product profile (`0_product_profile.md`), JTBD docs, existing PRDs, and user research. Also check `.chalk/docs/engineering/` for architecture docs that inform feasibility. If no product context exists, note that explicitly and work from what the user provides.

2. **Accept the feature request** — Parse `$ARGUMENTS` to identify the problem space, target user, and any constraints the user has mentioned. If `$ARGUMENTS` is vague (e.g., "notifications"), ask one round of clarifying questions before proceeding. Never silently assume the scope.

3. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next PRD number is `highest + 1`.

4. **Generate the PRD** — Write all sections listed below. Every section is mandatory. Do not leave sections empty or write "TBD" without also adding the item to Open Questions.

5. **Cross-reference architecture** — Read `.chalk/docs/engineering/` to validate that the proposed solution is feasible within the current stack. Flag any new infrastructure, services, or third-party dependencies in the Dependencies section.

6. **Flag assumptions** — Any statement that is not grounded in an existing doc or explicit user input goes into Open Questions. Be aggressive about surfacing unknowns.

7. **Write the file** — Save to `.chalk/docs/product/<n>_prd_<slug>.md`.

8. **Confirm** — Tell the user the PRD was created, share the file path, and highlight the top 2-3 open questions that need resolution before engineering work begins.

## PRD Structure

```markdown
# PRD: <Feature Name>

Last updated: <YYYY-MM-DD> (Initial draft)

## Problem Statement

What user problem are we solving and why does it matter now? Link to a Job-to-be-Done if one exists in the product docs. State the problem from the user's perspective, not the system's.

## Target Users

Who specifically experiences this problem? Use personas from product docs if available. Include:
- Primary persona and their context
- Secondary personas (if any)
- Who this is NOT for (anti-personas)

## Success Metrics

How will we know this worked? Every metric must be:
- Measurable (has a number or clear threshold)
- Time-bound (measured over what period)
- Baselined (current state vs. target state)

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| ... | ... | ... | ... |

## User Stories

Group by user activity. Each story follows:

**Activity: <activity name>**

As a [persona], I want [action], so that [outcome].

Acceptance Criteria:
- Given [context], when [action], then [expected result]
- Given [context], when [action], then [expected result]

## Acceptance Criteria (Feature-Level)

Testable conditions that must ALL be true for the feature to be considered complete. Write in Given/When/Then format. These are the contract between product and engineering.

## Edge Cases

Enumerate scenarios that are easy to overlook:
- Error states (network failure, invalid input, timeout)
- Empty states (first-time user, no data)
- Boundary conditions (max limits, concurrent users, large payloads)
- Permission boundaries (unauthorized access, expired sessions)
- Backwards compatibility (existing users, data migration)

## Out of Scope

Explicitly list what this PRD does NOT cover. This section prevents scope creep and misaligned expectations. Be specific: "Real-time sync is out of scope" not "Some features are out of scope."

## Dependencies

- **Internal**: Other teams, services, or features that must exist first
- **External**: Third-party APIs, vendor contracts, compliance requirements
- **Technical**: Infrastructure, tooling, or architectural changes required

## Open Questions

Numbered list of unresolved items that block confident implementation. Each question should name who can answer it.

1. [Question] — Owner: [person/team]
```

## Output

- **File**: `.chalk/docs/product/<n>_prd_<slug>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# PRD: <Feature Name>`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial draft)`

## Anti-patterns

- **Solution-first writing** — Never start with "We will build X." Start with the user problem. If the user gives you a solution ("add a button that..."), dig back to the underlying need.
- **PRDs without success metrics** — A PRD with no measurable outcomes is a wish list. Every PRD needs at least 2 metrics with concrete targets.
- **Missing out-of-scope section** — Omitting this guarantees scope creep. Even if the scope seems obvious, write it down.
- **Vague acceptance criteria** — "The feature should work well" is not testable. Every criterion must follow Given/When/Then and be verifiable by QA without asking the PM what "well" means.
- **Feature lists instead of user outcomes** — "Add filtering, sorting, and pagination" describes implementation, not value. Write "Users can find the specific record they need within 10 seconds" instead.
- **Copy-pasting the template with blanks** — Every section must contain substantive content. If you genuinely don't have information for a section, move the gap to Open Questions and explain what's missing.
- **Ignoring existing product context** — Always check `.chalk/docs/product/` first. PRDs that contradict the product profile or duplicate existing PRDs waste everyone's time.
