---
name: swift-package-agents-maintainer
description: Create, update, and maintain a canonical AGENTS.md (agents file) across Swift Package repositories. Use when Codex needs to update AGENTS.md for Swift packages, sync agents files for one or many Swift package repos, enforce a shared repository policy baseline, detect AGENTS.md drift in automation, or apply the canonical AGENTS.md template during repository maintenance.
---

# Swift Package AGENTS Maintainer

Maintain one canonical `AGENTS.md` across Swift Package repositories.
Prefer the bundled script for deterministic automation runs.

## Workflow

1. Confirm scope and mode.
- Use `--repo <path>` for a single repository.
- Use `--root <path>` to scan recursively for repos containing `Package.swift`.
- If neither `--repo` nor `--root` is provided, scan `~/Workspace` by default.
- Use `--check` for read-only drift detection in recurring automation.
- Omit `--check` to apply updates.

2. Resolve the canonical file.
- Default canonical file: `assets/AGENTS.md` in this skill.
- If the user provides another canonical source, pass it with `--canonical <path>`.

3. Run synchronization.
- Command:
  `scripts/sync_agents_md.sh [--canonical <path>] (--repo <path> | --root <path>) [--check] [--verbose]`
- In apply mode, the script creates or updates `AGENTS.md` in each discovered Swift package repo.
- In check mode, the script reports drift and exits non-zero if any repo differs.

4. Validate and report.
- Summarize: scanned repos, unchanged repos, updated repos, and drift count.
- For automation runs, include whether exit status indicates drift.

## Defaults

- Prefer `--check` for scheduled automation runs that only detect drift.
- Prefer apply mode for user-invoked maintenance runs.
- Treat a directory as a Swift package repo only when `Package.swift` is present.
- Use `~/Workspace` as the default discovery root on machines where Swift packages are stored there.
- Use `--root` when your repositories live outside `~/Workspace`.
- Skip hidden/build dependency directories during scans (for example `.git`, any `.*` directory, `.build`, `.swiftpm`, `node_modules`).
- Skip Xcode-protected/generated directories during scans (for example `*.xcworkspace`, `*.xcodeproj`, `DerivedData`).

## Automation Prompting

- Codex App automation fit: Strong. Use for recurring drift detection or scheduled apply runs.
- Codex CLI automation fit: Strong. Use deterministic prompts that map directly to `--check` or apply mode.
- Use `references/automation-prompts.md` for Codex App and Codex CLI templates with placeholders.
- Keep mode, schedule, and workspace routing explicit to avoid accidental apply runs.

## Troubleshooting

- If the canonical file path is missing, stop and request or restore a valid canonical `AGENTS.md`.
- If no repositories are discovered under `--root`, report that no `Package.swift` files were found.
- If permissions block writes, rerun with an authorized workspace path or approved elevation.

## Resources

### scripts/

- `scripts/sync_agents_md.sh`: Detect and apply canonical `AGENTS.md` changes across Swift package repos.

### assets/

- `assets/AGENTS.md`: Canonical baseline template for Swift package repositories.

### references/

- `references/automation-usage.md`: Suggested recurring automation modes and output expectations.
- `references/automation-prompts.md`: Codex App and Codex CLI automation templates with placeholders and guardrails.
