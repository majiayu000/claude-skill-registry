---
name: clix-skill-creator
display-name: Skill Creator
short-description: Generate new Clix agent skills
description: Helps authors create new Clix agent skills by first researching the latest Clix
  SDK + docs via the Clix MCP Server, then generating a complete skill folder
  (SKILL.md, references, scripts, examples) aligned with the conventions in this
  repository. Use when the user asks to create/author a new Clix skill, extend
  the skills library, or when the user types `clix-skill-creator`.
user-invocable: true
---

# Clix Skill Creator

Use this skill to **create a new Clix skill** that matches a user's need, while
avoiding duplicated scope and **preventing hallucinated API usage** by relying
on the Clix MCP server as the source of truth.

This is a “meta-skill”: it does not integrate an SDK directly; it guides you to
produce **another skill folder** (docs + deterministic scripts) that does.

## When to use this skill

- User says: “Create a new skill for Clix that helps with X”
- Internal request: “We need a new skill for feature X in Clix”
- User provides a workflow that is not well-covered by existing skills
- User types: `clix-skill-creator`

## Non-goals (important)

- Do **not** create a new skill if the request can be satisfied by combining
  existing skills (integration + event tracking + personalization + user
  management + API-triggered campaigns).
- Do **not** invent SDK methods, endpoints, or constraints. If you can’t confirm
  via MCP, treat it as unknown and ask the user or add a TODO note.
- Do **not** embed secrets, project IDs, API keys, or customer data in the skill.

## MCP-first (mandatory source of truth)

Before writing any new “Clix API behavior” or “SDK signature” into a newly
generated skill:

- **MUST** use `clix-mcp-server:search_docs` to confirm conceptual behavior,
  limits, and console semantics.
- **MUST** use `clix-mcp-server:search_sdk` to confirm exact method signatures
  for each platform (iOS/Android/Flutter/React Native) that the new skill will
  mention.

If `clix-mcp-server` tools are not available:

- Ask the user whether to install the MCP server (prefer using the existing
  installer in `skills/integration/scripts/install-mcp.sh`).
- If the user declines, proceed with an explicit “static fallback may be
  outdated” warning and minimize hard claims.

## Workflow (copy + check off)

```
Clix skill creation progress:
- [ ] 1) Intake: user need → crisp problem statement + acceptance criteria
- [ ] 2) Scope check: confirm this isn’t already covered by existing skills
- [ ] 3) MCP research: gather evidence (docs + SDK signatures) for the target scope
- [ ] 4) Draft a Skill Brief (name, trigger phrases, inputs/outputs, guardrails)
- [ ] 5) Generate scaffold (SKILL.md + references/ + scripts/ + examples/)
- [ ] 6) Validate scaffold (structure + frontmatter + MCP-first section)
- [ ] 7) Wire-in (README + llms index + tests if needed)
```

## 1) Intake: minimum questions

Ask only what’s needed to define a stable skill boundary:

- **Goal**: what outcome should the skill reliably produce?
- **Audience**: app devs, backend devs, marketers/ops, or mixed?
- **Platform** (if SDK-related): iOS / Android / Flutter / React Native
- **Clix capability**: push / in-app / email / audiences / journeys / etc.
- **Constraints**: PII policy, compliance, performance limits, rate limits
- **Success criteria**: what does “done” look like?

## 2) Reference official skills (match repo style)

Before creating a new skill, use the existing **official Clix skills** in this
repo as your style guide so the generated skill matches the standards here
(format, tone, workflow, validators), while still being tailored to the user’s
need.

- Study how they are written:
  - YAML frontmatter conventions
  - MCP-first “source of truth” behavior
  - Progressive disclosure (`references/`, `scripts/`, `examples/`)
  - Plan artifacts + deterministic validators (bash scripts)
- Then generate the new skill based on the user’s need using the same patterns.
  If the need is clearly a tiny addition to an existing skill, prefer adding a
  `references/` doc or `examples/` file there instead of creating a new skill.

- `clix-integration`
- `clix-event-tracking`
- `clix-user-management`
- `clix-personalization`
- `clix-api-triggered-campaigns`

## 3) MCP research: build an “Evidence Pack”

Create a short evidence pack that you will cite while writing the new skill:

- **Docs evidence** (from `clix-mcp-server:search_docs`)
  - behavior guarantees
  - constraints/limits
  - console terminology
- **SDK evidence** (from `clix-mcp-server:search_sdk`)
  - exact signatures per platform
  - initialization / required params
  - error behavior (throws? returns promise?)

Store the evidence in your notes (or as a `references/` markdown file in the new
skill), with the search queries you used so future maintainers can refresh it.

## 4) Draft a Skill Brief (output format)

Produce this brief for approval _before_ generating files:

```yaml
skill:
  folder_name: "<kebab-case>" # e.g. "push-troubleshooting"
  name: "clix-<kebab-case>" # e.g. "clix-push-troubleshooting"
  display_name: "<Title Case>"
  short_description: "<short>"
  description: "<2-3 lines>"
  user_invocable: true

triggers:
  - "phrases the user might say"

inputs:
  - "minimal inputs the skill will ask for"

outputs:
  - "artifacts the skill produces (plan JSON, code changes, checklists)"

guardrails:
  - "MCP-first requirements"
  - "security / PII constraints"

files_to_generate:
  skill_md: true
  references:
    - "<doc>.md"
  scripts:
    - "<script>.sh"
  examples:
    - "<optional>"
```

## 5) Generate scaffold (repo conventions)

In this repository, a “complete” skill folder should include:

- `SKILL.md` (with YAML frontmatter; MCP-first; workflow; progressive disclosure)
- `LICENSE.txt`
- `references/` (markdown docs; not empty)
- `scripts/` (deterministic bash scripts; not empty)
- `examples/` (optional, but recommended when copy/paste code is useful)

## 6) Validate scaffold (fast feedback loop)

After generating a new skill folder, validate it:

```bash
bash <skill-dir>/scripts/validate-same-scope.sh path/to/installed/skill-creator path/to/new-skill-folder
bash <skill-dir>/scripts/validate-skill-location.sh path/to/new-skill-folder --mode repo
bash <skill-dir>/scripts/validate-skill-scaffold.sh path/to/new-skill-folder
```

This should check:

- the new skill is installed at the **same scope** as `skill-creator` (project-level
  vs user-level), i.e. the new skill folder lives next to the installed
  `skill-creator` under the same `.../skills/` directory
- the skill folder is in the correct `skills/<name>/` location (for this repo)
- required files exist
- `references/` and `scripts/` are present and non-empty
- `SKILL.md` has valid frontmatter keys
- the skill includes an MCP-first section referencing `clix-mcp-server`

## Progressive Disclosure

- **Level 1**: This `SKILL.md` (always loaded)
- **Level 2**: `references/` (load when authoring the new skill)
- **Level 3**: `examples/` (load when copy/pasting scaffolds)
- **Level 4**: `scripts/` (execute directly; do not load into context)

## References

- `references/skill-template.md`
- `references/mcp-research-playbook.md`
