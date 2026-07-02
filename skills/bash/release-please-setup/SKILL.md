---
name: release-please-setup
description: Scaffold or migrate a repository onto release-please. Generates release-please-config.json, .release-please-manifest.json, and a release-please.yml workflow, plus an opt-in menu of tag-keyed deploy/publish templates (Docker/ECR matrix, frontend host deploy, npm OIDC publish, GitHub Release asset, Fly.io deploy, generic). Supports monorepo (mutual exclude-paths matrix), single-package, and mixed-language (node/simple/python) repos. Use when user runs /release-please-setup, mentions "release please", "set up release please", "automate releases", "conventional-commit releases", "monorepo release automation", or "migrate to release-please".
---

# Release-Please Setup

Scaffold or migrate a repository onto [release-please](https://github.com/googleapis/release-please). The skill generates `release-please-config.json` and `.release-please-manifest.json` from a monorepo package scan, then guides you through wiring the `release-please.yml` workflow and optionally an opt-in deploy/publish template from the six provided in `templates/`.

## Two modes

| Mode | When to use |
|---|---|
| **Greenfield** (default) | New repo with no prior tags. All packages start at `0.0.0` (or `--initial <ver>`). |
| **`--migrate`** | Existing repo with hand-maintained `<component>-v*` tags. Manifest is seeded from detected file versions; existing deploy workflows keep working unchanged. |

## Quick start

```bash
# SCRIPTS = absolute path to this skill's scripts/ directory
# Always dry-run first — no files are written
python3 SCRIPTS/release_please_setup.py --root . --dry-run            # greenfield
python3 SCRIPTS/release_please_setup.py --root . --migrate --dry-run  # migrate
python3 SCRIPTS/release_please_setup.py --root . --migrate            # write files
```

**CLI flags:** `--root` (repo root), `--globs` (comma-separated package globs; default `packages/*,backend/*,frontend/*`), `--migrate` (migration mode), `--single` (force single-package config), `--initial` (starting version; default `0.0.0`), `--dry-run` (print output, no writes), `--out-dir` (write location; default `--root`).

**Then:**

1. Copy `templates/release-please.yml` into `.github/workflows/`.
2. Set the `REPO_TOKEN` secret — see CONTRACT.md. ⚠️ GITHUB_TOKEN-created tags do **not** trigger other workflows; a PAT is required for deploy templates to fire.
3. Pick a deploy template (optional).

## Deploy template menu

| Template | Use for |
|---|---|
| `deploy-fly.yml` | Fly.io app deploy |
| `publish-npm-oidc.yml` | npm Trusted Publishing (OIDC, no token) |
| `release-asset.yml` | Build artifact → GitHub Release (e.g. `.vsix`, `.zip`) |
| `deploy-docker-matrix.yml` | Docker image → Amazon ECR / any registry |
| `deploy-frontend-host.yml` | Gated frontend deploy (Amplify, Vercel, Netlify) |
| `deploy-generic.yml` | Any build + deploy command |
| None | Release-please only — add deploy later |

Fill all `__TOKEN__` placeholders before committing; see WORKFLOW.md for the complete placeholder reference table.

## Output structure

```
<repo-root>/
├── release-please-config.json       ← written by the script
├── .release-please-manifest.json    ← written by the script
└── .github/workflows/
    ├── release-please.yml            ← copy from templates/
    └── deploy-<component>.yml        ← copy from templates/ (optional)
```

Monorepo: each package gets `include-component-in-tag: true`, `tag-separator: "-"`, and a mutual `exclude-paths` matrix (tags like `user-service-v1.2.0`). Single-package: minimal config, tags are `v<semver>`.

## Common issues

- **Release PR not created** — check commits follow [Conventional Commits](https://conventionalcommits.org), you are on the default branch, and the workflow has `contents: write` + `pull-requests: write` permissions.
- **Deploy didn't fire** — the REPO_TOKEN gotcha; see CONTRACT.md and TROUBLESHOOTING.md.
- **Wrong version after migration** — discovery missed the version; edit `.release-please-manifest.json` manually.

## References

- [WORKFLOW.md](WORKFLOW.md) — Greenfield and migration runbooks + placeholder reference table
- [EXAMPLES.md](EXAMPLES.md) — Three worked examples (acme monorepo, papia-studio migration, single-package)
- [CONTRACT.md](CONTRACT.md) — Tag format, REPO_TOKEN gotcha, job outputs, trigger variants
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Error reference
