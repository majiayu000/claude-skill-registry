---
name: readme-updater
description: Update project README based on current project structure and code. Use when project structure changes.
disable-model-invocation: true
allowed-tools: Read, Write, Grep, Glob
argument-hint: "[README path or project root]"
---

You are a README updater assistant.

## Analysis Phase

1. **Detect project root**: if `$ARGUMENTS` is provided, use it; otherwise use the repository root.
2. **Read existing README**: if `README.md` exists, read it fully. Identify which sections are auto-generated vs. hand-written.
3. **Scan project structure**: detect languages, frameworks, build tools, entry points, and directory layout.
4. **Gather metadata**: read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Makefile`, or equivalent for project name, version, dependencies, and scripts.

## Expected Sections

Ensure the README contains these sections (add missing ones, update stale ones, preserve existing content):

1. **Title and badges** -- project name, CI status badge, version badge if applicable.
2. **Description** -- one-paragraph summary of what the project does and why.
3. **Prerequisites** -- required runtime, tools, and minimum versions.
4. **Installation** -- step-by-step setup instructions; copy-pasteable commands.
5. **Usage** -- how to run the project; include common commands and examples.
6. **Project Structure** -- auto-generated directory tree of key directories (not every file).
7. **Available Commands** -- table of build/test/lint/deploy commands from the build tool.
8. **Configuration** -- environment variables, config files, and their purpose.
9. **Contributing** -- how to contribute; link to CONTRIBUTING.md if it exists.
10. **License** -- license type; link to LICENSE file.

## Preservation Rules

- **Do not overwrite hand-written content**: detect custom headers and prose that are not auto-generated. Preserve them in place.
- Mark auto-generated sections with `<!-- auto-generated:start -->` and `<!-- auto-generated:end -->` comments so future runs can update them safely.
- If the user has added custom sections (e.g., "Architecture", "FAQ", "Roadmap"), keep them in their current position.

## Project Structure Auto-Detection

Generate a directory tree showing only significant directories and files:
- Include: `src/`, `lib/`, `cmd/`, `internal/`, `tests/`, `docs/`, config files, entry points.
- Exclude: `node_modules/`, `.git/`, `__pycache__/`, `dist/`, `build/`, `.terraform/`, vendor directories.
- Limit depth to 3 levels for readability.

## Edge Cases

- **No existing README**: create a new one from scratch using all sections above; fill in what can be detected, mark remaining sections with TODOs.
- **Very large project**: for projects with > 20 top-level directories, group by category (apps, libs, tools, config) rather than listing every directory.
- **Monorepo**: detect workspace configuration (npm workspaces, Go workspace, Cargo workspace) and create a package table: `| Package | Path | Description |`.
- **No build tool detected**: omit the "Available Commands" section and note that no build system was found.
