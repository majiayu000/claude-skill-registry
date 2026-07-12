---
name: vitaecontext-wiki-maintenance
description: Maintainer-only skill for refreshing VitaeContext wiki knowledge from official sources. Use only from a local repository clone when a maintainer asks to refresh one module, audit all module wiki entries, or audit module source lists.
license: MIT
metadata:
  homepage: https://vitaecontext.github.io/
  repository: https://github.com/vitaecontext/vitaecontext
---

# VitaeContext Wiki Maintenance

## Overview

Use this maintainer-only skill to keep VitaeContext `wiki/knowledge.md`, `hub/<module>/sources.md`, human-facing hub playbooks, runtime skill guidance, and internal runtime contracts aligned with their sources of truth.

This skill is for repository maintainers working from a local clone. It is never exported to user installs. End users receive static, pre-authored wiki entries through the package install flow.

## Wiki context

- Always read [.skills/agent-skill/vitaecontext/wiki/vitaecontext.md](../vitaecontext/wiki/vitaecontext.md) before running any maintenance task so the agent understands the full project architecture before touching any file.
- If the root wiki entry is unavailable, read [.skills/agent-skill/vitaecontext/SKILL.md](../vitaecontext/SKILL.md), [.skills/architecture.md](../../architecture.md), and [MAINTAINING.md](../../../MAINTAINING.md) before proceeding. State that the root wiki entry was unavailable.

## Allowed modules

Use only these module ids:

- `context-builder`
- `cv-ats`
- `github`
- `linkedin`
- `web-portfolio`
- `x-twitter`

Map each module id to its runtime skill folder:

| Module id | Runtime skill folder |
|---|---|
| `context-builder` | `.skills/agent-skill/vitaecontext-build/` |
| `cv-ats` | `.skills/agent-skill/vitaecontext-cv/` |
| `github` | `.skills/agent-skill/vitaecontext-github/` |
| `linkedin` | `.skills/agent-skill/vitaecontext-linkedin/` |
| `web-portfolio` | `.skills/agent-skill/vitaecontext-portfolio/` |
| `x-twitter` | `.skills/agent-skill/vitaecontext-x/` |

## Source handling rules

Apply the source quality rules from [MAINTAINING.md](../../../MAINTAINING.md) exactly:

- `stable`: Official platform documentation, official help-center pages describing system behavior, official engineering or product blogs, published specs, RFC-style documents, or official maintainer-published repositories.
- `likely`: Official sources that describe current behavior but depend on product tiers, UI state, geography, rollout status, undocumented implementation details, or provider-specific support.
- `inferred`: Official source code snapshots, architecture writeups, discontinued or historical official material, or repo-owned methodology where no external platform source exists.
- `disputed`: Conflicting official sources, unsupported public narratives, secondary commentary, or behavior where no clean official source exists.

When tools allow network access, search for newer or missing official sources before treating the current `sources.md` list as complete. Accept only official platform documentation, official help-center pages, official engineering or product blogs, published specs, RFC-style documents, or official maintainer-published repositories. Do not add secondary commentary, influencer posts, SEO agency articles, community speculation, Reddit threads, or login-gated material as source evidence.

Never introduce a source that does not meet the inclusion bar. Never upgrade `inferred` to `stable` without an explicit official source. Record every fetch and discovery check with URL, fetch date, determinable source changes, and affected wiki claims.

## Patch output rules

Before writing any file, present a proposed patch and ask for explicit maintainer confirmation.

Every proposed change must include:

- Exact current text in `knowledge.md` or `sources.md`.
- Proposed replacement text.
- Source URL that justifies the change.
- Confidence label before and after the change.
- Reason: `new evidence`, `source updated`, `source removed`, `conflicting sources`, or `confidence correction`.

Never propose a change without source justification. If no official source supports a proposed wiki change, flag the claim for downgrade or further review instead of writing it as stable guidance.

## File boundaries

On confirmation only, this skill may touch:

- `.skills/agent-skill/vitaecontext-<module>/wiki/knowledge.md`
- `.skills/agent-skill/vitaecontext-<module>/wiki/index.md` when source changes require a different conditional load map
- `.skills/agent-skill/vitaecontext-<module>/SKILL.md` when source changes require different routing, load, or high-level operating rules
- `.skills/agent-skill/vitaecontext-<module>/references/*.md`
- `hub/<module>/sources.md`
- `hub/<module>/*.md`
- `llms-full.txt`

This skill must never touch:

- `llms.txt`
- `README.md`
- Provider mirrors under `skills/` or `commands/`
- Files outside the confirmed list above

Every downstream edit must be source-backed and module-scoped. Do not change hub playbooks, runtime references, module `SKILL.md`, or `wiki/index.md` only because the wording could be cleaner. Change them only when official evidence invalidates, narrows, expands, or clarifies the methodology that agents or humans should apply.

If a source change implies that a forbidden file should change, do not edit that file. Flag it in a follow-up section with the exact file, affected section when known, reason, and source URL. This applies to project-level README content, CHANGELOG entries, provider mirrors, provider wrappers, install behavior, and files outside the target module.

## Mode 1: Single module refresh

Use this mode when the maintainer asks:

```text
Use vitaecontext-wiki-maintenance to refresh the <module> module
```

Workflow:

1. Read `hub/<module>/sources.md` to identify official sources for the surface.
2. Read `.skills/agent-skill/vitaecontext-<module>/wiki/knowledge.md` to understand current claims, confidence labels, `last_reviewed`, and `review_by`.
3. Search for newer or missing official sources for the same surface. Use source discovery queries that target official domains, specs, help centers, engineering blogs, or maintainer-published repositories. Reject secondary or speculative material.
4. Fetch every official source in `sources.md` that is newer than `last_reviewed`, plus any newly discovered official source that meets the inclusion bar. If `last_reviewed` is more than 30 days ago, fetch all official sources regardless of the stated review interval.
5. Extract source-backed claims relevant to the module surface.
6. Diff extracted claims against current `knowledge.md`:
   - New claims supported by official sources that are absent from the wiki.
   - Existing claims whose confidence should change based on current source text.
   - Claims the source no longer supports, flagged for removal or downgrade.
   - Claims contradicted by a conflicting official source, marked `disputed`.
7. Inspect downstream module files that may need aligned updates: `hub/<module>/*.md`, `.skills/agent-skill/vitaecontext-<module>/references/*.md`, `.skills/agent-skill/vitaecontext-<module>/SKILL.md`, and `.skills/agent-skill/vitaecontext-<module>/wiki/index.md`.
8. Diff extracted claims against downstream module guidance:
   - Hub playbook claims that should change because official evidence changed.
   - Runtime reference instructions that should change because agents would otherwise apply stale methodology.
   - Module `SKILL.md` routing, source hierarchy, or load rules that should change because the module's operating model changed.
   - `wiki/index.md` load rules that should change because new wiki knowledge should be loaded for different tasks.
9. Identify forbidden files that still need separate follow-up outside this skill's write permissions, including README, CHANGELOG, provider wrappers, generated provider mirrors, install behavior, or files outside the target module.
10. Produce a proposed patch with exact line-level edits to every touched allowed file and source URL justification for every change.
11. Present the full proposed patch and the forbidden-file follow-up list before writing anything. Ask for explicit confirmation.
12. On confirmation only, apply the patch, update `last_reviewed` to today, set `review_by` from the dominant confidence level, regenerate `llms-full.txt`, and run `npm run validate`.
13. Report what changed, which source justified it, which confidence labels moved up, down, or to `disputed`, which hub or runtime guidance changed, and which forbidden follow-up files still need separate updates if any.

Use these review intervals:

- `stable`: 6 months after `last_reviewed`
- `likely`: 3 months after `last_reviewed`
- `inferred`: 1 month after `last_reviewed`
- `disputed`: 1 month after `last_reviewed`

## Mode 2: Full audit

Use this mode when the maintainer asks:

```text
Use vitaecontext-wiki-maintenance to audit all modules
```

Workflow:

1. Spawn parallel subagent tasks for the six module ids: `context-builder`, `cv-ats`, `github`, `linkedin`, `web-portfolio`, and `x-twitter`.
2. Each subagent runs Mode 1 through step 10 only. It produces a proposed patch and forbidden-file follow-up list, but performs no writes.
3. Collect the proposed patches into one unified audit report:
   - Per module: sources fetched, claims changed, confidence movements, new claims, and flagged removals.
   - Cross-module: consistency issues, including the same claim labeled differently across modules or shared taxonomy drift.
   - Downstream guidance: hub playbooks, runtime references, module `SKILL.md`, or `wiki/index.md` edits proposed for each module.
   - Follow-ups: forbidden files that should be updated separately, with file path, reason, and source URL.
4. Present the full unified report to the maintainer.
5. Ask which modules to apply, which to skip, and which require further review.
6. Apply only confirmed module patches. Regenerate `llms-full.txt` once after all confirmed writes. Run `npm run validate` once after all confirmed writes.

If subagent tooling is unavailable, run the six module audits sequentially and state that parallel subagents were unavailable.

## Mode 4: Internal contract audit

Use this mode when the maintainer asks to audit routing, installed-skill workflow behavior, or VitaeGraph consistency. This mode is source-tree based and does not require external platform research.

Audit these contracts:

1. Every skill configured in `.skills/export/export-config.json` is represented in root routing and provider-capable command maps.
2. Every configured runtime skill defines trigger frontmatter, task or depth selection appropriate to its operations, mutation boundaries, verification behavior, self-review, and a bounded response or completion shape.
3. Relative runtime links resolve inside the portable skill bundle. Repository-only playbooks, source inventories, maintainer docs, and package maps use durable public links when installed providers do not ship them.
4. VitaeGraph record vocabulary matches `vitaegraph/schema/record-schema.json`; graph-level direction and claims to avoid are not described as record types.
5. VitaeGraph templates, schema, runtime skill, CLI validation, generated graph model, downstream retrieval rules, and public specification agree on paths, IDs, relationships, visibility, privacy, and lifecycle operations.
6. Audit-only modes do not silently authorize writes, and destructive or many-record operations require a preview and confirmation.
7. Generated mirrors match canonical skill sources after intentional provider exclusions.

Workflow:

1. Read the architecture map, style guide, skill architecture, root runtime skill, export configuration, and VitaeGraph specification when applicable.
2. Trace representative agent runs for audit, draft, apply, validate, retrieve, maintain, and degraded-tool scenarios.
3. Run `npm test`, `npm run validate`, and a provider export smoke test.
4. Produce a prioritized contract-drift report with exact files, observed behavior, proposed behavior, and the runtime consequence.
5. Present proposed patches before writing. Apply only changes confirmed by the maintainer under the repository's normal file ownership rules.
6. Regenerate stored mirrors and `llms-full.txt` when their canonical sources change, then rerun validation.

Do not force external-source confidence labels onto repo-owned architecture claims in this mode. Validate those claims against code, schemas, templates, tests, generated output, and repository docs.

## Mode 3: Source audit only

Use this mode when the maintainer asks:

```text
Use vitaecontext-wiki-maintenance to audit sources for <module>
```

or:

```text
Use vitaecontext-wiki-maintenance to audit all sources
```

Workflow:

1. Read `hub/<module>/sources.md`.
2. Search for newer or missing official sources for the module surface. Prefer official platform documentation, help centers, engineering or product blogs, published specs, RFC-style documents, and official maintainer-published repositories.
3. Fetch each listed and newly discovered candidate source and check:
   - Whether it is still live and accessible.
   - Whether it is still official, not moved to a third party, and not deprecated.
   - Whether it still covers what the `sources.md` entry claims it covers.
   - Whether a newer or more authoritative official source should replace or supplement it.
4. Propose updates to `sources.md` only. Do not propose wiki changes in this mode.
5. Present rejected candidate sources separately, with the reason they did not meet the inclusion bar.
6. Present the full proposed patch and ask for explicit confirmation.
7. On confirmation only, apply the `sources.md` patch and run `npm run validate`.

## Response shape

For proposed patches, return:

1. Module and mode.
2. Sources fetched, with URL and fetch date.
3. Proposed line-level changes across wiki, source, hub, and runtime skill files.
4. Source justification for every change.
5. Confidence movements.
6. Claims flagged for removal, downgrade, dispute, or further review.
7. Forbidden follow-up files that should be updated outside this skill, if any.
8. Explicit confirmation request before writing.

For completed writes, return:

1. Files changed.
2. Sources used.
3. Confidence movements.
4. `llms-full.txt` regeneration status when applicable.
5. Hub or runtime guidance changed, if applicable.
6. Forbidden follow-up files that still need separate updates, if any.
7. Validation result.
