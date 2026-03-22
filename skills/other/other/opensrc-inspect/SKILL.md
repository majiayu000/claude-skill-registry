---
name: opensrc-inspect
description: Fetch, inspect, and manage local opensrc source snapshots for packages and GitHub repositories. Use when you need dependency or upstream repo source code locally for deeper implementation review, API edge-case analysis, or version-aligned source inspection. Do not use as a general web-research skill.
---

# Opensrc Inspect

Use this skill when source-level dependency inspection is materially useful and API docs alone are not enough.

## Workflow

1. Read the repo `AGENTS.md`.
2. Check existing snapshots first:
   - `opensrc list`
   - `cat opensrc/sources.json` when present
3. Prefer safe fetches that avoid repo mutation:
   - `opensrc <package> --modify=false`
   - `opensrc pypi:<package> --modify=false`
   - `opensrc crates:<package> --modify=false`
   - `opensrc <owner>/<repo> --modify=false`
4. Inspect the fetched source path and cite exact files and versions when using it in analysis.
5. Refresh snapshots after meaningful dependency upgrades if internals changed.

## Use When

- You need to inspect a package implementation, not just its docs or types.
- You need source-level evidence for a migration, bug, or compatibility question.

## Do Not Use When

- Official docs, types, or direct code inspection already answer the question.
- The task is broad web research or release-note discovery.

## Guardrails

- Default to `--modify=false`.
- Treat `opensrc/` as read-only source context.
- Use Context7, Exa, or `web.run` for official/latest docs and changelogs; use opensrc only for implementation internals.

## Outputs

- fetched source target and version summary
- exact local paths used for analysis
- concise recommendation on whether deeper source inspection changed the conclusion
