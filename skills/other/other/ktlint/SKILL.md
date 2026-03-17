---
name: ktlint
description: Format and lint Kotlin using ktlint; set up or update ktlint in Gradle/CLI/CI, configure .editorconfig, and troubleshoot ktlint failures or formatting changes in Kotlin projects.
---

# Ktlint

Use this skill to format and lint Kotlin code with ktlint, and to set up or maintain ktlint tooling in a project.

## Quick start

1. Detect how the project runs ktlint (Gradle tasks vs CLI).
2. Run ktlint check or format on the target paths.
3. Fix or configure rules via existing project config (usually `.editorconfig`).

## Determine the integration

- Prefer existing build tasks: look for `ktlintCheck` / `ktlintFormat` (or custom ktlint tasks) in Gradle.
- If there are no build tasks, fall back to the `ktlint` CLI if it is installed.
- Before changing setup, search for existing config and automation:
  - `.editorconfig` and any `ktlint` sections
  - `build.gradle` / `build.gradle.kts`
  - CI files (GitHub Actions, GitLab CI, etc.)
  - pre-commit hooks

## Common tasks

### Run ktlint check (no changes)

- Prefer Gradle: run the project’s ktlint check task.
- Otherwise use the CLI to lint specific files or directories.

### Run ktlint format (apply fixes)

- Prefer Gradle: run the project’s ktlint format task.
- Otherwise use the CLI formatter.

### Format only specific files

- Pass explicit paths to the task or CLI.
- If using Gradle, check whether the plugin supports path filters or separate source sets.

### Configure rules

- Modify the project’s existing `.editorconfig` rather than inventing a new location.
- Keep changes minimal and explain why a rule is enabled/disabled.
- If the project pins a ktlint version, follow its supported rule IDs and config keys.

### Add ktlint to a Gradle project

- Prefer the project’s existing Kotlin/Gradle conventions (versions catalog, buildSrc, convention plugins).
- Add the plugin and tasks in the standard place for that repository.
- Wire ktlint into CI the same way other quality checks are run.

### Troubleshoot failures

- Identify the ktlint version and whether it is coming from Gradle or CLI.
- Reproduce locally with the same task or command used in CI.
- If a rule suddenly fails, check recent ktlint or rule-set updates in the project.

## Scripts

- `scripts/ktlint.sh` provides a lightweight wrapper to run check/format using Gradle tasks if present, or fall back to the `ktlint` CLI.

## Notes

- Avoid changing rule configuration unless the user asks; prefer formatting fixes.
- When updating setup, keep changes minimal and aligned with existing project conventions.
