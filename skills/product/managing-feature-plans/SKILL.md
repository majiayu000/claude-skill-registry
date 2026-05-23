---
name: managing-feature-plans
description: Create, review, update, and archive feature plan documents. Use when starting a new feature, assessing progress, refining requirements, or marking a plan complete.
owner: eng-product-process
version: 1.1
last_updated: 2026-02-01
---

## When to use this skill

- Start, scope, or refine a new feature plan.
- Review progress, unblock development, or update an existing plan.
- Audit a plan for missing requirements, unclear TODOs, or missing references.
- Mark a plan as complete and archive it.

Do not use this skill for

- Project-level roadmaps or long-lived strategy documents (use the roadmap-skill).
- Ad-hoc notes or meeting minutes that won't be maintained as a plan.

Why use this skill

- Standardizes feature plans in doc/plan/ so they are discoverable and actionable.
- Keeps TODOs, milestones, and acceptance criteria explicit and trackable.
- Automates safe archival of completed plans.

Key features

1) Create a feature plan
- Create doc/plan/{feature-name}-plan.md from doc/plan/plan-template.md (or fallback template).
- Enforce kebab-case names: {feature-name}-plan.md (e.g. storage-interface-plan.md).

2) Review and update
- Detect missing or ambiguous requirements, TODOs, acceptance criteria, and references.
- Edit plan sections: Goals, Non-goals, Requirements, Design, Milestones, Tasks, Risks, Dependencies.
- Maintain TODO/DONE lists and a changelog for completed items (with timestamps where applicable).

3) Archive
- Verify completion (no open TODOs, acceptance criteria satisfied) and move the plan to doc/plan/archived/{feature-name}-plan.md.
- Add a completion stamp (date + short summary) to the archived file.
- Helper: python archive_plan.py {feature-name}

How it works (runtime behavior)

1) Resolve feature name
- Normalize user input to kebab-case and validate uniqueness.
- If ambiguous, propose clearer names and ask for confirmation.

2) Locate or create plan
- If doc/plan/{feature-name}-plan.md exists: open it for review and updates.
- If missing: create it from doc/plan/plan-template.md or a minimal inline template and populate the header.

3) Review and edit
- Ensure sections are present and actionable (Goals, Non-goals, Requirements, Acceptance Criteria).
- Convert vague items into concrete TODOs with owners, estimates, and explicit acceptance criteria where possible.
- Move completed checklist items to the changelog with timestamps and author.

4) Archive when complete
- Preconditions: no open TODOs blocking release, all acceptance criteria marked PASS (or linked to verification evidence), and changelog updated.
- Run: python archive_plan.py {feature-name}
  - This moves the file to doc/plan/archived/{feature-name}-plan.md, appends a completion stamp, and records the archiver.

Acceptance checklist (before archiving)

- [ ] No open TODOs assigned to the feature team.
- [ ] All acceptance criteria marked PASS or have linked verification evidence (tests, design reviews).
- [ ] Milestones and release notes updated.
- [ ] Changelog contains all completed items with timestamps.

Template locations

- Active plans: doc/plan/
- Templates: doc/plan/plan-template.md
- Archived plans: doc/plan/archived/

Usage examples (explicit)

- Create a plan from a prompt: "Create a plan for \"Improved upload UX\""
  - Resulting filename: doc/plan/improved-upload-ux-plan.md
- Review an existing plan: "Review the plan for storage-interface and list missing requirements"
- Archive when done: "Archive the feature plan upload-progress once tests are green" or run locally: python archive_plan.py upload-progress

Requirements

- Python 3.7+ for archive_plan.py
- Read/write access to doc/plan/ and doc/plan/archived/

Notes

- Keep SKILL.md concise: frontmatter name/description are used to match user intents.
- Prefer concrete suggestions for naming and TODOs to reduce back-and-forth.
- Update the frontmatter owner/version/last_updated when making future changes.
