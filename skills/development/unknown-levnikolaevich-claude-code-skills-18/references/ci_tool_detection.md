<!-- SOURCE-OF-TRUTH: shared/references/ci_tool_detection.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# CI Tool Detection Contract

Small runtime contract for discovering lint, typecheck, test, build, and benchmark commands.

## Discovery Order

Use the first reliable source per category: project docs (`tech_stack`, `infrastructure`, `runbook`), tool config, package/build manifest, then skip with evidence. Explicit docs override auto-detection.

## Detection Map

| Category | Signals | Command shape |
|---|---|---|
| lint | eslint/biome/ruff/dotnet format | `npm run lint`, `npx eslint .`, `ruff check .`, `dotnet format --verify-no-changes` |
| typecheck | `tsconfig`, mypy/pyright, Go/Rust | `tsc --noEmit`, `mypy .`, `pyright`, `go vet ./...`, `cargo check` |
| test | Jest/Vitest/Pytest, test project refs | `npm test`, `npx vitest run`, `pytest`, `go test ./...`, `dotnet test`, `cargo test` |
| build | manifests, solutions, Maven, Cargo | `npm run build`, `python -m build`, `go build ./...`, `dotnet build`, `cargo build`, `mvn compile` |
| benchmark | benchmark files/framework markers | framework command with JSON/text artifact |

## Execution Rules

- Preserve real exit codes; piping/truncation must not mask failure.
- Prefer compact or JSON output when supported.
- Use CI-compatible non-interactive flags.
- Auto-fix flow is `fix -> rerun without fix -> verify`.
- On failure, keep compact context and preserve full logs under `.hex-skills/logs/error_recovery/` when the skill writes artifacts.

## Evidence

Record `{category, command, source, status, evidence}` where `source=docs|config|manifest|fallback` and `status=pass|fail|skipped`.

Skip with evidence when no config is found, command is missing, or project docs are absent. Timeout is a category failure with timeout evidence.

Long provider recipes are skill-local or conditional; this file is only detection and evidence SSOT.

**Version:** 1.0.0
**Last Updated:** 2026-02-15
