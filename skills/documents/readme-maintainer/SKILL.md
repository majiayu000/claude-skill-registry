---
name: readme-maintainer
description: Create or update project README.md files by scanning the repository and keeping documentation in sync with the current setup. Use when a README is missing, outdated, or needs updates based on package configs, build/test scripts, env examples, licenses, or changelog files. Include install/usage/env vars/testing/contributing/license/changelog sections only when the repo contains evidence for them.
---

# README Maintainer

## Goal

Create or update `README.md` so it accurately reflects the current project setup. Only include information you can verify from the repository contents. Ask brief questions if critical information is missing.

## Workflow

1. Scan the repository for sources of truth.

- README: `README.md`
- Package managers: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`
- Python: `pyproject.toml`, `requirements.txt`, `Pipfile`
- Go: `go.mod`
- Rust: `Cargo.toml`
- Ruby: `Gemfile`
- PHP: `composer.json`
- Java/Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`
- Build/test tasks: `Makefile`, `justfile`, `Taskfile.yml`, CI workflows under `.github/workflows/`
- Containers: `Dockerfile`, `docker-compose.yml`
- Env samples: `.env.example`, `.env.sample`, `.env.template`, `config/*.example`, `*.env`
- Contribution: `CONTRIBUTING.md`
- License: `LICENSE`, `LICENSE.*`, `COPYING`
- Changelog: `CHANGELOG.md`, `CHANGELOG.*`, `RELEASES.md`

2. Decide what to include.

- If a section is not supported by evidence, omit it.
- If a section is required but the repo lacks details (e.g., no usage info), ask the user a focused question instead of guessing.
- Preserve existing sections, tone, and badges unless they are incorrect. Update in place when possible.

3. Build or update sections using verified data.

- **Install**: infer package manager from lockfiles. Example: `pnpm-lock.yaml` -> `pnpm install`; `yarn.lock` -> `yarn install`; `package-lock.json` -> `npm install`. For Python, use `poetry install` only if `pyproject.toml` specifies Poetry; otherwise use `pip install -r requirements.txt` if present.
- **Usage**: derive from `package.json` scripts (e.g., `dev`, `start`, `build`), CLI entry points, Makefile targets, or existing docs.
- **Env vars**: list keys from `.env.example` or similar files. Provide descriptions only if present in comments or docs; otherwise leave descriptions blank or say "Required".
- **Testing**: use `package.json` scripts (`test`, `lint`) or standard commands inferred from repo files (`pytest`, `go test`, `cargo test`) only if those tools are clearly used in the repo.
- **Contributing**: link to `CONTRIBUTING.md` if present; otherwise omit.
- **License**: link to the license file. Name the license only if the file explicitly states it.
- **Changelog**: link to `CHANGELOG.md` or equivalent if present.

4. Validate the README.

- Ensure commands match actual scripts and tooling in the repo.
- Remove outdated instructions.
- Keep it concise and skimmable.

## Output expectations

- Update or create `README.md` only.
- Do not add new policy files or templates.
- If questions are needed, ask them before writing or changing major sections.
