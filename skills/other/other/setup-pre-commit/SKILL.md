---
name: setup-pre-commit
description: Install git pre-commit hooks via the project's hook tool of choice — Husky+lint-staged (npm/yarn/pnpm/bun), pre-commit framework (Python), lefthook (Go), cargo-husky (Rust), pre-commit (OCaml). Use when user wants commit-time formatting, linting, type-checking, or test gates. Detects ecosystem first; recommends the right tool.
---

Detect the ecosystem, pick the right hook tool, install with formatter + type-check + test gates.

## Detection (run first)

Dispatch Explore agent — or for a single-language repo, probe directly via `fd` for lockfile / manifest signature. Map the first manifest hit to an ecosystem. Multi-language repos: ask the maintainer which surface to gate, or apply both.

## Ecosystem → hook tool

| Ecosystem            | Hook tool                  | Install command                                                  |
| -------------------- | -------------------------- | ---------------------------------------------------------------- |
| npm / yarn / pnpm / bun | husky + lint-staged     | `<pm> add -D husky lint-staged prettier && npx husky init`       |
| Python (poetry/pip)  | pre-commit (framework)     | `pipx install pre-commit && pre-commit install`                  |
| Go                   | lefthook (or pre-commit)   | `go install github.com/evilmartians/lefthook@latest && lefthook install` |
| Rust (cargo)         | cargo-husky (or pre-commit)| add `cargo-husky` as `[dev-dependencies]`; runs on `cargo test`  |
| OCaml (dune)         | pre-commit + dune hooks    | `pipx install pre-commit && pre-commit install`                  |

## Per-ecosystem hook contents

**Node ecosystems** — write `.husky/pre-commit`:

```
npx lint-staged
<pm> run typecheck
<pm> run test
```

Drop missing scripts and tell the user. Write `.lintstagedrc`:

```json
{ "*": "prettier --ignore-unknown --write" }
```

Formatter policy is **out of scope** for this skill. Do NOT auto-create `.prettierrc`. If no Prettier config exists, surface that fact and ask the user.

**Python** — write `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: pyright
        language: system
        pass_filenames: false
      - id: pytest
        name: pytest
        entry: pytest -q
        language: system
        pass_filenames: false
        stages: [pre-commit]
```

**Go** — write `lefthook.yml`:

```yaml
pre-commit:
  parallel: true
  commands:
    fmt:    { run: gofmt -l -w {staged_files} }
    vet:    { run: go vet ./... }
    test:   { run: go test -race ./... }
```

**Rust** — `Cargo.toml`:

```toml
[dev-dependencies]
cargo-husky = { version = "1", default-features = false, features = ["precommit-hook", "run-cargo-test", "run-cargo-clippy", "run-cargo-fmt"] }
```

**OCaml** — `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: dune-fmt
        name: dune fmt
        entry: dune fmt
        language: system
        pass_filenames: false
      - id: dune-build
        name: dune build
        entry: dune build
        language: system
        pass_filenames: false
      - id: dune-test
        name: dune runtest
        entry: dune runtest
        language: system
        pass_filenames: false
```

## Verify

- `fd -d 2 -t f '\.husky|\.pre-commit-config\.yaml|lefthook\.yml'` shows the expected file.
- The hook is executable.
- Run a no-op commit (`git commit --allow-empty -m "chore: verify hooks"`) — every gate must run and pass.

## Commit

`chore: install pre-commit hooks (<tool>)`. The commit itself trips the new hook — first-class smoke test.
