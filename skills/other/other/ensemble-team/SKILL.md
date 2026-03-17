---
name: ensemble-team
description: >
  Set up a full AI ensemble/mob programming team for any software project. Creates
  team member profiles (.team/), coordinator instructions (CLAUDE.md), project owner
  constraints (PROJECT.md), team agreements (TEAM_AGREEMENTS.md), domain glossary,
  and supporting docs. Use when: (1) starting a new project and wanting a full expert
  agent team, (2) the user asks to "set up a team", "create a mob team", "set up
  ensemble programming", or "create agent profiles", (3) converting an existing project
  to the driver-reviewer mob model, (4) the user wants Claude Code agents to work as a
  coordinated product team with retrospectives and consensus-based decisions.
---

# Ensemble Team Setup

Set up an AI ensemble programming team for any software project. Creates the full
structure for a team of expert agents working in a single-driver mob programming style
with consensus-based decisions, TDD, and continuous retrospectives.

## Workflow

### Phase 1: Project Discovery

Gather essential project information. Ask the user:

1. **Project name and description**: What is being built? What problem does it solve?
2. **Tech stack**: Language, framework, database, frontend approach, testing tools.
   If unsure, help them decide based on their goals.
3. **Product vision**: Target user? MVP scope? Vague ideas are fine — the Product
   Manager agent will refine them.
4. **Dev environment**: Nix? Docker? Standard package managers? CI provider?
5. **Repository**: Existing repo or new? Branching strategy?

### Phase 2: Team Composition

Determine the right team. Read [references/role-catalog.md](references/role-catalog.md)
for role selection criteria and the research process.

**Always include**: Product Manager, Dev Practice Lead, Domain Architect, Lead Engineer
(language-specific), UX Specialist.

**Add based on needs**: UI Designer, Accessibility Specialist, CSS Engineer, Frontend
Specialist, Hypermedia Architect, DevOps, Security, Data/ML, API Specialist. See the
role catalog for "Add When" criteria.

**Team size**: 7-9 members. Min 5, max 10. Odd numbers preferred.

**Research each expert — do NOT pick from a memorized list.** For each role:
1. Identify the specific technology/domain this project needs
2. Use WebSearch to find the recognized authority — the person who wrote the book,
   created the tool, or gave the defining talks for that specific area
3. Verify their credentials, recent work, and relevance to this project
4. Evaluate: published authority, distinctive voice, practical experience,
   complementary perspective to other team members

Present each proposed expert with: name, credentials, key published work, why they
fit THIS project, and what they'd focus on. Let user approve, swap, or remove.

### Phase 3: Generate Team Profiles

Create `.team/<name>.md` for each member. Read
[references/profile-template.md](references/profile-template.md) for structure.

Required sections: Opening bio, Role, Core Philosophy (5-8 principles from their
published work), Technical Expertise (6-12 items), On This Project (concrete
guidance), Communication Style (personality + 4-6 characteristic phrases), Mob
Approach, Code Review Checklist (6-12 checks), Lessons (empty, to be updated).

**Quality gates**: Profile must not be interchangeable with another expert. Must
include project-specific guidance. Must capture their distinctive voice.

### Phase 4: Generate Project Scaffolding

#### CLAUDE.md
Read [references/coordinator-template.md](references/coordinator-template.md).
Fill in roster, build tools, team size. This file is for the coordinator only.

#### PROJECT.md
Read [references/project-template.md](references/project-template.md).
Fill in tech stack, scope (Must/Should/Could/Out), dev mandates, environment.

#### TEAM_AGREEMENTS.md — Skeleton Only
Create a **skeleton** `TEAM_AGREEMENTS.md` with section headers but NO pre-filled
agreements. The team writes their own agreements during the formation session (Phase 5).

#### Supporting docs

- **docs/glossary.md**: Domain glossary skeleton (Core Types table, Actions table,
  Errors table, Type Design Principles)
- **docs/deferred-items.md**: Tracker table (Item | Category | Source | Severity | Status)
- **docs/future-ideas.md**: Parking lot for out-of-scope ideas

### Phase 5: Team Formation Session

This is the critical phase. The team debates and reaches consensus on their own
working agreements. Read
[references/team-agreements-template.md](references/team-agreements-template.md) for
the list of problems the team must discuss.

**How it works**: The coordinator spawns the full team, then presents each discussion
topic (from the reference file) one at a time. The team debates, proposes approaches,
and reaches consensus. The Driver records the agreed-upon norms in
`TEAM_AGREEMENTS.md`.

**The 10 topics** (non-exhaustive — team may add more):
1. How do we decide what to build?
2. How does the Driver-Reviewer mob model work?
3. When is a piece of work "done"?
4. What is our commit and integration pipeline?
5. How do we resolve disagreements?
6. What are our code conventions?
7. When and how do we hold retrospectives?
8. What are our architectural principles?
9. How do we communicate as a team?
10. What tooling and repository conventions do we follow?

Each topic includes the **problem** it addresses and **sub-questions** to guide
discussion. The team's answers become their agreements — not pre-canned templates.

### Phase 6: Configure Permissions

Create/update `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": ["Edit", "Write", "Bash(*)"]
  }
}
```

### Phase 7: Configure CI

Add `paths-ignore` for `.claude-sessions/` to CI config to prevent session transcript
commits from triggering CI runs.

### Phase 8: Summary

Present: files created, how to start the team ("Run Claude Code — the coordinator reads
CLAUDE.md and spawns the team"), remind about Shift+Tab for delegate mode after spawn,
suggest telling the coordinator what to build.

## Key Principles

Non-negotiable aspects baked in from production experience. Read
[references/lessons-learned.md](references/lessons-learned.md) for details.

- Consensus before push (review locally, then push)
- Refactor step is mandatory every commit
- CI wait rule (never queue multiple CI runs)
- Mini-retro after every CI build (team runs it, not coordinator)
- Driver handoff protocol (summary + git log + green baseline)
- Glossary compliance (domain types match glossary)
- Deferred items tracked immediately
- Reviewer coordination (check others' reviews first)
- Explicit Driver onboarding in spawn prompts
- Session transcripts excluded from CI triggers
