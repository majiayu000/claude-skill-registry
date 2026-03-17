---
name: sdd-skill-creator
description: |
  Generate project-specific SDD skills for a repository.
  Use when: setting up SDD for a new project, customizing SDD for a domain,
  creating repo-local skills that implement `docs/sdd-guidelines.md`.
  Triggers: "create sdd skills", "setup sdd for project", "customize sdd"
---

# SDD Skill Creator

Generate project-specific SDD skills that live in a repository.

## Prerequisites

**You (the generator) must first:**
1. Read `docs/sdd-guidelines.md` (especially §1 Artifacts, §9 Customization Points, §10 Multi-Agent)
2. Have project context available

Generated skills will be self-contained—their users won't need to read Guidelines.

## Output Structure

```
{project}/.sdd/skills/
├── sdd-foundation/SKILL.md
├── sdd-requirements/SKILL.md
├── sdd-design/SKILL.md
├── sdd-verify/SKILL.md
└── sdd-workflow/SKILL.md
```

## Instructions

### Step 1: Gather Project Context

| Question | Purpose | Default |
|----------|---------|---------|
| Project name? | Naming, examples | — |
| Domain? (game, API, CLI, etc.) | Terminology | — |
| Multi-agent? | Include §10 | No |
| Custom anchor prefixes? | Guidelines §9 | `SCOPE-`, `CONSTRAINT-` |
| REQ ID format? | Guidelines §9 | `REQ-{NNN}` |

Skip questions already answered in conversation.

### Step 2: Define Customizations

Fill out the customization record. See [templates/customization.yaml](templates/customization.yaml).

### Step 3: Generate Each Skill

For each skill, create SKILL.md with proper frontmatter and these sections:

| Section | Content |
|---------|---------|
| **Customizations** | From Step 2: prefixes, ID formats, terminology |
| **Instructions** | Guidelines steps rewritten with project terminology |
| **Examples** | One complete example using project's domain |
| **Verification** | Checklist to validate output |

#### Skill-to-Guidelines Mapping

| Skill | Guidelines Source | Key Customizations |
|-------|-------------------|-------------------|
| sdd-foundation | §1.1 Foundation | Anchor prefixes, domain framing |
| sdd-requirements | §1.2 Requirements | REQ ID format, alignment examples |
| sdd-design | §1.3 Design, §1.4 Decisions | Rationale patterns, domain design |
| sdd-verify | §3 Verification | Checklists, gap severity |
| sdd-workflow | §1-5 (full flow) | State file, handoff, phase transitions |

#### What "Project-Adapted" Means

| Guidelines says | You write |
|-----------------|-----------|
| "Identity Anchors" | "{Domain} Identity Anchors" with project prefixes |
| "REQ-{NNN}" | Project's REQ ID format with example |
| "Design item" | Domain-specific term (e.g., "endpoint", "mechanic") |

**If multi-agent:** Add §10 coordination to each skill.

### Step 4: Write Skills

Create files in `.sdd/skills/`. Each skill must be:

- **Self-contained** — User can follow without reading Guidelines
- **Project-specific** — Uses project terminology throughout
- **Guidelines-aligned** — Doesn't contradict §1-10
- **Concise** — Under 200 lines

### Step 5: Verify Generated Skills

For each skill:

1. Frontmatter has `name` and `description` with triggers?
2. All Step 2 customization values applied?
3. Complete workflow, no placeholders?
4. Concrete, domain-relevant example?
5. Actionable verification checklist?

### Step 6: Inform User

```
Created SDD skills in {project}/.sdd/skills/:

- sdd-foundation   → Foundation documents (§1.1)
- sdd-requirements → Requirements documents (§1.2)
- sdd-design       → Design documents (§1.3)
- sdd-verify       → Integrity verification (§3)
- sdd-workflow     → End-to-end orchestration

Customizations: {prefixes}, {req_format}, multi-agent={yes/no}
```

## Examples

See [examples/taskcli.md](examples/taskcli.md) for a complete walkthrough.

## Anti-patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Generic skills | No project value | Apply all customizations |
| Contradict Guidelines | Integrity violation | Re-read source section |
| Verbose skills | Context waste | Keep < 200 lines |
| Placeholders left | Incomplete | Fill all `{...}` before saving |
