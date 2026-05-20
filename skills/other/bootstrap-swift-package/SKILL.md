---
name: bootstrap-swift-package
description: Bootstrap new Swift Package Manager projects with consistent defaults and fast setup. Use when creating a new Swift package (library, executable, or tool), scaffolding package structure, applying standard platform/version defaults, always initializing git for a package, and running first-step safety checks plus build/test validation.
---

# Bootstrap Swift Package

## Overview

Create a new Swift package quickly with repeatable defaults.
Prefer the bundled script for deterministic setup.

## Workflow

1. Confirm package intent.
- Ask for package `name`, `type` (`library`, `executable`, or `tool`), destination path, platform preset (`mac`, `mobile`, `multiplatform`), and version profile (`latest-major`, `current-minus-one`, `current-minus-two`).
- Accept aliases: `macos` for `mac`, `ios` for `mobile`, `both` for `multiplatform`, and `latest`/`minus-one`/`minus-two` for version profiles.

2. Create the package.
- Preferred: run `scripts/bootstrap_swift_package.sh --name <Name> --type <library|executable|tool> --destination <dir> --platform <mac|macos|mobile|ios|multiplatform|both> --version-profile <latest-major|current-minus-one|current-minus-two|latest|minus-one|minus-two>`.
- Fallback: run `swift package init --name <Name> --type <library|executable|tool>` manually inside the target directory, patch `Package.swift` platforms, copy `assets/AGENTS.md` to repo root as `AGENTS.md`, then run `git init`.

3. Validate bootstrap output.
- Verify `Package.swift` exists.
- Verify `.git` exists.
- Verify `AGENTS.md` exists.
- Verify `Tests/` exists.
- Run `swift build` and `swift test` in the package root.

4. Report result.
- Summarize created path, package type, platform preset, version profile, build/test status, and immediate next steps.

## Defaults

- Use `library` unless the user clearly asks for `executable` or `tool`.
- Use `multiplatform` unless the user clearly wants only `mac` or `mobile`.
- Use `current-minus-one` as the default version profile.
- Keep generated structure minimal; do not add extra frameworks unless requested.
- Always initialize git.
- Always include `AGENTS.md` with repository expectations for working with Swift Package Manager and Swift packages.

## Automation Prompting

- Codex App automation fit: Guarded. Prefer event-driven or explicit scaffold requests over frequent recurring schedules.
- Codex CLI automation fit: Strong. Use deterministic `codex exec` prompts with explicit placeholders and strict scope.
- Use `references/automation-prompts.md` for ready-to-use Codex App and Codex CLI templates.
- Keep schedule and workspace configuration outside the prompt body for App automations.

## Troubleshooting

- If `swift` is missing, stop and ask the user to install Xcode command line tools or Swift toolchain.
- If `git` is missing, stop and ask the user to install git or Xcode command line tools.
- If `assets/AGENTS.md` is missing, stop and restore the template before bootstrapping packages.
- If destination exists and is non-empty (excluding ignorable macOS metadata like `.DS_Store`), do not overwrite; ask for a new destination or explicit cleanup instructions.
- If validation fails in constrained environments, rerun with `--skip-validation` and report that checks were skipped.

## Resources

### scripts/

- `scripts/bootstrap_swift_package.sh`: Create package directory, run `swift package init`, apply platforms defaults to `Package.swift`, initialize git, and run safety/validation checks.

### references/

- `references/package-types.md`: Quick selection guide for package types, platform presets, and version profiles.
- `references/automation-prompts.md`: Codex App and Codex CLI automation prompt templates with placeholders and guardrails.

### assets/

- `assets/AGENTS.md`: Template copied into each new package repository to set repository expectations for Swift Package Manager workflows.
