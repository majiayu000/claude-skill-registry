---
name: repo-scaffold
description: Scaffold or standardize a production-ready repository structure with specs, source layout, tests, CI, agent context, config examples, release notes, and operational docs. Use when starting a new repo, turning a prototype into a maintainable project, adding missing repository foundations, or creating a repo skeleton before implementation. For AGENTS.md-only context scaffolding, use agentsmd-scaffold.
---

# Repo Scaffold

## Purpose

Use this skill to create the repo foundation that lets product, architecture, implementation, verification, and operations stay connected. It is broader than `agentsmd-scaffold`; it may include AGENTS.md, but also specs, tests, CI, config, release, and runbook structure.

## Search First

Before adding files, inspect the repo for existing equivalents:

```bash
rg --files -g 'AGENTS.md' -g 'CONTRIBUTING.md' -g 'README*' -g 'pyproject.toml' -g 'package.json' -g 'go.mod' -g 'Cargo.toml' -g '.github/workflows/*' -g 'docs/**' -g 'specs/**' -g 'tests/**'
```

Reuse existing conventions. Do not create parallel `docs/`, `spec/`, `planning/`, or `test/` trees when the repo already has a standard location.

## Scaffold Layers

Add only the layers needed for the repo:

| Layer | Typical Files |
|---|---|
| Product and specs | `specs/PRODUCT.md`, `specs/TECH.md`, `docs/adr/` |
| Agent context | `AGENTS.md`, scoped `AGENTS.md`, local skill notes |
| Source layout | language-specific `src/`, `pkg/`, `cmd/`, `app/`, `lib/` |
| Tests | `tests/`, fixtures, golden snapshots, e2e harness |
| CI | `.github/workflows/ci.yml`, lint/typecheck/test jobs |
| Config | `.env.example`, config schema, secret inventory |
| Release | `CHANGELOG.md`, release checklist, versioning notes |
| Operations | `docs/runbooks/`, SLO and incident templates |

## Decision Rules

- For a new repo, propose the tree first, then create files only after the user asks to apply.
- For an existing repo, make the smallest additive change that closes the foundation gap.
- Keep generated starter files short and executable. Prefer empty placeholders only when a tool requires them.
- Do not hardcode credentials, service names, ports, or cloud providers without repo evidence.
- Do not overwrite existing README, CI, or config files without showing the diff intent.

## Minimal Output

For planning:

```text
existing_foundation:
missing_layers:
proposed_tree:
files_to_create_or_update:
verification_commands:
```

For implementation, finish by running the repo's validation command and, when available, the scaffold-specific lint or generated-file check.
