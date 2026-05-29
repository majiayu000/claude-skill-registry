---
name: kirby-upgrade-and-maintenance
description: Upgrades Kirby and maintains dependencies safely using composer audit, plugin compatibility checks, and official docs. Use when updating Kirby versions or making maintenance changes that affect runtime.
---

# Kirby Upgrade and Maintenance

## Quick start

- Follow the workflow below for safe, incremental upgrades.

## KB entry points

- `kirby://kb/panel/compat-k5-k6-migration`
- `kirby://kb/panel/tooling-kirbyup`
- `kirby://kb/glossary/kirbyup`
- `kirby://kb/glossary/plugin`

## Required inputs

- Current and target Kirby versions.
- Environment constraints and downtime tolerance.
- Plugin compatibility risks and rollback expectations.

## Default upgrade checklist

- Read the target version guide and note breaking changes.
- Update `composer.json` constraints, then review the lockfile diff.
- Run project scripts and render representative pages.
- Verify runtime commands and CLI version match.

## Rollback note

- Keep a copy of the previous `composer.lock` and `vendor/` state.

## Rollback checklist

- Restore the previous `composer.lock`.
- Reinstall dependencies and re-run smoke tests.
- Re-render representative pages to confirm behavior.

## Staged upgrade pattern

- Upgrade a single environment/site first, then roll out to others.
- Validate plugins and custom code before multi-site rollout.

## Common pitfalls

- Skipping plugin compatibility checks.
- Upgrading multiple major versions in one jump.

## Workflow

1. Call `kirby:kirby_init` or gather baseline data with `kirby:kirby_info` and `kirby:kirby_composer_audit`.
2. Inventory plugins for compatibility risks: `kirby:kirby_plugins_index`.
3. Use `kirby:kirby_online` to find official upgrade guides and breaking changes for the target version (prefer `kirby:kirby_search` first).
4. Build a project-specific checklist of required code/config changes.
5. Ask for confirmation before dependency updates that change the lockfile.
6. Verify:
   - run project scripts discovered in the composer audit
   - call `kirby:kirby_cli_version` to confirm the installed version
   - ensure runtime commands are in sync: `kirby:kirby_runtime_status` and `kirby:kirby_runtime_install` if needed
   - render representative pages with `kirby:kirby_render_page(noCache=true)`
7. Summarize changes, remaining risks, and a short manual QA checklist.
