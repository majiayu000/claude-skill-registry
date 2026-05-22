---
name: optimus-prime
argument-hint: additional-context
description: "Generates a Claude Code configuration tailored to a specific project. Use whenever the user wants to prime a project, set up claude for a repo, bootstrap claude config, or re-prime/refresh an already-primed project (for example after `/prime-sync` pulled new starter content). Triggers on 'prime', 'prime this project', 'optimus-prime', 're-prime', 'refresh claude config', 'regenerate CLAUDE.md', 'set up claude for this repo'. Deeply analyzes the real codebase and builds project-specific skills, rules, and CLAUDE.md — not generic boilerplate. For ongoing config health checks and proposal review, use `self-evolve` instead."
disable-model-invocation: true
---

Ultrathink.

## Mission

Generate a Claude configuration that fits the specific project. Every skill, rule, and CLAUDE.md entry must exist because this project needs it — not because a template included it. Analyze the real codebase deeply, understand its conventions and patterns, and build a config that makes Claude work well here.

## Modes

- **Fresh prime** — no claude config yet. Build from scratch.
- **Re-prime** — claude config already exists. Preserve intentional project work, refresh what is stale or generic, fill gaps.

Default to re-prime whenever meaningful existing config is found. Never overwrite it wholesale without user approval.

## Flow

1. **Analyze** the repo deeply — stack, conventions, boundaries, docs, existing config. See [analysis-checklist.md](./references/analysis-checklist.md).
2. **Propose** findings using the Output Format below. Do not touch meaningful files before approval.
3. **Create skills** via `/skill-creator` — every skill must go through skill-creator to ensure quality and project fit. Starters in `.claude/starter-skills/` are reference input to accelerate creation, not templates to copy.
4. **Generate or refine CLAUDE.md** — lean, high-signal, always-on context only. Point to docs/READMEs for detail.
5. **Rules only if needed** — apply the rule test. Zero rules is valid.
6. **Offer CLAUDE.local.md** — personal preferences (role, sandbox URLs, preferred test data, workflow quirks), gitignored.
7. **Clean up** — delete `.claude/starter-skills/` after processing. Keep protected skills. Confirm all deletions.
8. **Verify** — references resolve, stack claims match evidence, config is project-specific not generic.
9. **Offer skill optimization** — after everything is set up, offer optimization paths sized to how many new skills were created. ≤3 skills: recommend full optimization for all. >3 skills: recommend full optimization for user-designated core skills only + description optimization for the rest (avoids long execution time and token burn). Always emphasize that full optimization takes meaningful time and tokens. **Run sequentially — never in parallel; concurrent runs overload the user's machine.**

Follow full step-by-step in [setup-project.md](./references/setup-project.md).

## Placement Decision Matrix

Every piece of knowledge must earn its place. Use this to decide where it belongs:

| Detected need | Where it belongs | Test |
|---|---|---|
| General framework/library knowledge | Skill (via `/skill-creator`) | Would a reusable skill teach this across projects? |
| Project-specific constraint that still produces wrong code with the right skill loaded | `.claude/rules/<name>.md` with `paths:` | With the relevant skill activated, will code still be wrong without this? |
| Identity, commands, stack, key architecture, reference pointers | `CLAUDE.md` | Should this be always-on for most tasks in this repo? |
| Detailed architecture or domain explanations | Existing `docs/`, READMEs — referenced from CLAUDE.md | Valuable but too detailed for always-on? |
| Dense agent-oriented reference material - referenced from CLAUDE.md | `.claude/project/` (optional) | Do agents need a tighter reference than the human docs provide? |

## Principles

- **Domain-scoped, project-fitted.** Skills target a capability, not the project itself — with this project's patterns baked in. Generic templates and project-named catch-alls both degrade context quality.
- **Repo evidence is the source of truth.** Verify conventions from actual source files, configs, and docs. Do not assert what you haven't confirmed.
- **Lean context, high signal.** Follow the context engineering philosophy — load only what's needed, when it's needed. CLAUDE.md carries always-on essentials. Skills load on demand. Rules auto-attach by path.
- **Rules are optional and path-scoped.** Only create a rule when the rule test passes. Do **not** modify `_apply-all.md` — it is a universal boilerplate rule from prime, not project config.
- **Reuse over duplication.** If the project has strong docs, point to them. Do not re-author parallel agent docs unless existing material is too noisy or incomplete.

## Output Format

Before making non-trivial changes, report findings in this shape:

### Current State
What Claude config already exists; what the repo evidence says about stack, tooling, and conventions.

### Proposed Changes
What to create, update, keep, or remove — including which skills to build and what each should cover.

### Files to Touch
Concrete file list with short purpose notes.

Include these only when non-empty:
- **Decisions Needing User Input** — overwrites, deletions, or major structural changes
- **Risks / Assumptions** — inferred facts that still need verification

After approval, implement and finish with a short summary of what changed and any follow-ups.

## References

| Reference | Content |
|---|---|
| [analysis-checklist.md](./references/analysis-checklist.md) | What to inspect during repo + existing-config review |
| [setup-project.md](./references/setup-project.md) | Fresh-prime / re-prime step-by-step workflow |

## Additional Context (Optional)

<user-context>$ARGUMENTS</user-context>
