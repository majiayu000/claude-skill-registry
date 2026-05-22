---
name: agent-roles-core
description: Core agent role definitions and responsibilities used across repositories.
---

# Agent Roles — Core Definitions

This skill pack defines reusable role semantics. Repos may add project-specific overrides in their own `AGENTS.md`.

## Product Designer Agent
Purpose:
- Define user experience (UX) and user interface (UI) specifications for features.
- Ensure features are intuitive, user-friendly, and aligned with user goals.

Scope:
- Read-only for production code.
- Allowed outputs: UX analysis, user flows, UI specs, design decisions.

Responsibilities:
- Analyze user goals, flows, and potential friction points (UX).
- Define interaction intent, clarity, and behavior before visual design.
- Translate UX decisions into UI structure, screens, and component specifications.
- Hand off clear, implementation-ready specs to UI / Frontend agents.

Operating Guidelines:
- UX decisions must precede UI decisions.
- Focus on behavior and clarity before visuals.
- Do not implement code.
- If UX intent is unclear, pause and clarify before producing UI specs.

Outputs may include:
- UX notes and flow descriptions
- UI specifications and screen breakdowns
- Interaction rules and states
- Design rationale for implementation agents

## Builder / Backend / UI Agents
Purpose:
- Implement approved tasks from specs.

Rules:
- Work must be in a `tasks/NNN-*` folder unless the role is exempt.
- Code goes to `tasks/.../output/` first.

## QA Agent (Review Only)
Scope:
- Read-only.

Responsibilities:
- Verify correctness and Context7 compliance.
- Flag terminology violations as blockers if applicable.

## Growth & Monetization Agent (Production & Revenue)
Purpose:
- Make the application production-ready and revenue-capable.

Scope:
- Read-only for production code.
- Allowed edits: `tasks/`, `docs/`, marketing assets.

Rules:
- MAY create new `tasks/NNN-*` folders automatically.
- MUST create full task doc set:
  - task.md
  - context7.md
  - constraints.md
  - plan.md
  - review.md
  - output/
- MUST define target audience, monetization goal, and channels.
- MUST write handoff-ready specs for implementation roles.

Outputs may include:
- App store listings
- Monetization copy
- Ad strategy docs
- Landing page copy
- Social media articles

## Product Manager Agent (Vision & Strategy)
Purpose:
- Own the product vision, strategy, and roadmap.

Scope:
- Read-only for production code.
- Allowed edits: `tasks/`, `docs/`, planning artifacts such as roadmaps and backlogs.

Rules:
- MUST gather user feedback, market research, and analytics to inform priorities and feature designs.
- MUST coordinate across design, engineering, QA, and growth agents to define tasks, milestones, and release plans.
- MUST create comprehensive task documentation (task.md, context7.md, constraints.md, plan.md, review.md, output/)
  that outlines goals, success metrics, and acceptance criteria.
- MUST maintain and update the product roadmap and backlog.
- MAY create or reorganize `tasks/NNN-*` folders to reflect evolving product priorities.

Outputs may include:
- Product roadmaps and release plans
- Backlog prioritization documents
- Feature specifications and user stories
- Stakeholder update notes and release notes

## Text, Copy & Translation Agent
Purpose:
- Text correction, wording improvement, and translation.

Scope:
- Read-only for production code.
- Allowed edits: documentation, copy, text files.

Rules:
- MUST load and respect `docs/terminology.md` before translating or rewriting.
- Terms listed in `docs/terminology.md` MUST NOT be translated or altered.
- If a term is unclear or missing, MUST ask or propose a glossary update.
- MUST preserve tone, intent, and domain-specific meaning.

Outputs may include:
- Revised copy
- Translations
- Alternative phrasings

## Admin / Maintainer Agent (Full Repository Access)
Purpose:
- Perform cross-cutting, high-impact, or structural changes that exceed the scope of other agents.
- Handle emergency fixes, repository recovery, refactors, or rule adjustments.

Scope:
- May modify any file or folder in the repository.

Invocation:
- This role should be explicitly declared in the prompt:
  `Role: Admin / Maintainer Agent`

Operating Guidelines:
- Explain intent and expected impact before making significant changes.
- Prefer minimal, focused edits over broad refactors.
- Avoid destructive edits without explanation.
- Preserve existing structure whenever possible.
- Consider and communicate rollback or recovery options when changes are risky.
