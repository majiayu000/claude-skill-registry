---
name: environment
description: >
  Development environment setup, tool locations, and dependency installation for the flight-path Go project.
  Use when setting up the project, installing tools, troubleshooting PATH issues, or asking about Go/Node versions.
  Do NOT use for runtime troubleshooting, workflow guidance, or CI pipeline questions.
---

# Development Environment

## Go (via gvm)

```bash
GOROOT=/home/andriy/.gvm/gos/go1.26.1
GOPATH=/home/andriy/.gvm/pkgsets/go1.26.1/global
```

Activated via `~/.zshrc`: `gvm use go1.26.1 --default`

## Node.js (via nvm)

Required for Newman E2E tests. Installed by `make deps` if not present.

## Tool Installation

`make deps` installs all tools idempotently (skips if already present):

| Tool | Version | Purpose |
|---|---|---|
| `swag` | v1.16.6 | Swagger doc generation |
| `gosec` | v2.24.0 | Security scanner |
| `govulncheck` | v1.1.4 | Dependency vulnerability check |
| `gitleaks` | v8.24.0 | Secrets detection |
| `actionlint` | v1.7.7 | GitHub Actions linter |
| `benchstat` | latest | Benchmark comparison |
| `golangci-lint` | v2.11.1 | Meta-linter (60+ linters) |
| `node` | LTS (via nvm) | Newman runtime |
| `newman` | latest (via npm) | E2E API testing |

Most build targets depend on `deps` and auto-install missing tools.

## Makefile Targets

| Target | Depends on | What it does |
|---|---|---|
| `deps` | — | Install all tools |
| `lint` | deps | golangci-lint |
| `sec` | deps | gosec security scan |
| `vulncheck` | deps | govulncheck |
| `secrets` | deps | gitleaks scan |
| `lint-ci` | deps | actionlint |
| `static-check` | deps, lint, sec, vulncheck, secrets, lint-ci | All static checks |
| `api-docs` | deps | Swagger generation |
| `test` | — | Unit tests (`go test -v ./...`) |
| `fuzz` | — | Fuzz tests (30s) |
| `bench` | — | Benchmarks |
| `bench-save` | deps | Save benchmark with timestamp |
| `bench-compare` | deps | Compare latest two benchmarks |
| `build` | api-docs | Compile binary |
| `run` | build | Build and start server |
| `check` | lint, sec, vulncheck, secrets, test, api-docs, build | Pre-commit checklist |
| `ci` | static-check, build, test, fuzz | Local CI pipeline |
| `ci-full` | ci, coverage-check | CI + coverage threshold |
| `coverage` | — | Test coverage report |
| `coverage-check` | coverage | Verify 80% threshold |
| `clean` | — | Remove build artifacts and test cache |
| `docker-build` | — | Build Docker image locally |
| `docker-run` | docker-build | Run container locally |
| `docker-test` | docker-build | Build + smoke test container |
| `build-image` | deps, api-docs, lint, sec, vulncheck, secrets | Multi-platform build + push |
| `release` | lint, sec, vulncheck, test, api-docs, build | Tag and push release |
| `e2e` | deps | Newman E2E tests |
| `update` | — | Update Go dependencies |

## If Tools Not Found

Ensure `$(go env GOPATH)/bin` is in PATH:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
```
