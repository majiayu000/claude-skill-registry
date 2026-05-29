---
name: managing-sc-packages
description: List, install, or uninstall Synaptic Canvas packages. Use with the `/sc-manage` command.
version: 0.8.0
---

# Managing Synaptic Canvas Packages

Use this skill to manage Synaptic Canvas packages on this machine or in the current repo.

## Agent Delegation

This skill delegates to specialized agents via the Task tool:

| Operation | Agent | Returns |
|-----------|-------|---------|
| List      | `sc-packages-list`       | JSON: packages [{ name, description, installable_scopes, installed }] |
| Install   | `sc-package-install`     | JSON: success, scope, dest |
| Uninstall | `sc-package-uninstall`   | JSON: success, scope, dest |
| Docs      | `sc-package-docs`        | JSON: readme_path, size_bytes |

## Inputs / Flags

- `--list` → call `sc-packages-list`.
- `--install <package>` → require `--local`/`--project` or `--global`/`--user`; if missing, ask the user. If the package is local-only, force `--local`.
- `--uninstall <package>` → same scope logic as install.
- `--docs <package>` (alias `--doc`) → call `sc-package-docs` to load and present the package README.

## Conventions

- Local scope: current repository's `.claude` directory.
- Project scope: alias for local.
- User scope: `~/.claude` unless `USER_CLAUDE_DIR` is set.
- Global scope: `~/.claude` unless `GLOBAL_CLAUDE_DIR` is set.
- The agents will detect the repo toplevel via `git rev-parse --show-toplevel`.
- The agents call the Synaptic Canvas installer at `<SC_REPO_PATH>/tools/sc-install.py` (default resolved from `SC_REPO_PATH` or the repo root).

## Safety

- Respect package metadata: if a package manifest declares `install.scope: local-only`, block global installation.
- Return only fenced JSON from agents; present tables and prompts in this skill.
