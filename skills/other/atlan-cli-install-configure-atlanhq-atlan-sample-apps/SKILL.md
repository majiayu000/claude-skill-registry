---
name: atlan-cli-install-configure
description: Install Atlan CLI with OS-aware binaries (or Homebrew on macOS) only when missing, then configure baseline tenant auth/log settings.
---

# Atlan CLI Install Configure

Use this skill when CLI setup is the blocker. Keep it lightweight and safe.

## Trigger
1. Trigger when a workflow needs CLI and `command -v atlan` fails.
2. Trigger when the user explicitly asks to install, reinstall, or configure Atlan CLI.
3. Do not trigger for normal app tasks if `atlan` is already available and user did not request reinstall.

## Workflow
1. Pre-check:
   - run `command -v atlan`
   - if found and reinstall is not requested, skip install and move to config check.
2. Detect platform (`uname -s`, `uname -m`, or PowerShell OS/arch on Windows).
3. Use install guidance from `references/install-matrix.md`:
   - macOS: prefer Homebrew when available.
   - otherwise use pre-built binary for detected OS/arch.
   - never use `go get` or source-build as default install path.
4. Verify installation:
   - `atlan --version`
   - `atlan --help`
5. Configure CLI using `references/config-template.md`:
   - ensure `.atlan/config.yaml` has `atlan_base_url` and `log` settings.
   - auth via `ATLAN_API_KEY` env var (preferred) or `atlan_api_key` in config.
6. Configure `data_source` entries only if user has provided source details.
7. Summarize install method, binary path, CLI version, and config status.

## Security Rules
- Never print raw API keys in logs or summaries.
- Prefer `ATLAN_API_KEY` env var for automation and CI.
- Ask user for missing `atlan_base_url` or auth inputs before writing config.

## Failure Handling
1. If network/policy blocks download, stop and ask for either:
   - temporary network access, or
   - an existing local `atlan` binary path.
2. If extraction fails, retry once, then report exact failing command and output.
3. If install succeeded but `atlan` is still not in `PATH`, provide a shell-specific `PATH` update step.

## References
- Install matrix: `references/install-matrix.md`
- Config template: `references/config-template.md`
