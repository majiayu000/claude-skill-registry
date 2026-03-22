---
name: workflows
description: >
  Project-specific development workflows for the flight-path Go project: adding endpoints, benchmarking, releasing, Docker builds, and CI pipelines.
  Use when following a development process, preparing a release, running CI locally, or understanding the build pipeline.
  Do NOT use for environment setup, troubleshooting errors, or debugging specific failures.
---

# Development Workflows

## Adding a New Endpoint

1. Create handler method on `Handler` struct in `internal/handlers/` with Swagger annotations
2. Register route in `internal/routes/` (receives `*handlers.Handler`)
3. Wire route in `main.go`
4. Run `make api-docs`
5. Write table-driven tests
6. Add Postman test case to `test/FlightPath.postman_collection.json`
7. Run: `make test && make build`

## Performance Optimization

1. `make bench-save` (baseline — saved to `benchmarks/bench_YYYYMMDD_HHMMSS.txt`)
2. Implement optimization
3. `make bench-save` (after)
4. `make bench-compare` (auto-picks latest two files, or specify `OLD=file1 NEW=file2`)
5. `make test` (verify correctness)

Benchmarks run: `go test ./internal/handlers/ -bench=. -benchmem -benchtime=3s`

## Pre-commit Checklist

Quick way:
```bash
make check    # Runs: lint sec vulncheck secrets test api-docs build
```

Or individual steps:
```bash
make lint           # golangci-lint (60+ linters)
make sec            # gosec security scanner
make vulncheck      # govulncheck dependency check
make secrets        # gitleaks secrets detection
make test           # Unit tests
make api-docs       # Regenerate Swagger docs
make build          # Compile binary (depends on api-docs)
```

## Local CI

```bash
make ci             # static-check + build + test + fuzz
make ci-full        # ci + coverage-check (80% threshold)
```

## Release

1. Ensure clean main branch, all checks pass
2. Run full checks: `make check`
3. `make release` — validates semver tag (`vN.N.N`), updates `pkg/api/version.txt`, commits, tags, pushes
4. GitHub Actions release workflow triggers on tag push (uses GoReleaser)

`make release` depends on: `lint sec vulncheck test api-docs build`

## Docker

```bash
make docker-build                        # Build locally (single platform, buildx)
make docker-run                          # Build + run container (-e SERVER_PORT=8080)
make docker-test                         # Build + smoke test (health + API check)
make build-image                         # Multi-platform build + push to Docker Hub
```

- Image: multi-stage Alpine build (`golang:1.26-alpine` -> `alpine:3.23.3`)
- Non-root user: `srvuser:1000`, `CGO_ENABLED=0`
- Platforms: `linux/amd64`, `linux/arm64`, `linux/arm/v7`
- Registry: `andriykalashnykov/flight-path:latest` on Docker Hub
- `make build-image` runs checks first (`deps api-docs lint sec vulncheck secrets`) then calls `scripts/build-image.sh`

## CI Pipeline (GitHub Actions)

Pipeline in `.github/workflows/ci.yml`, runs on push and PRs:

| Job | Depends on | What it runs |
|---|---|---|
| `static-check` | — | `make static-check` (lint, sec, vulncheck, secrets, lint-ci) + Trivy FS scan |
| `builds` | static-check | `make build` + upload binary artifact |
| `tests` | static-check | `make test` + `make fuzz` |
| `integration` | builds, tests | Download artifact, start server, install Newman, `make e2e` |
| `dast` | integration | Start server, OWASP ZAP API scan against Swagger spec |
| `image-scan` | builds | Build Docker image, Trivy image scan |
| `container-test` | image-scan | Build image, run container, health + API smoke test |

- Go version read from `go.mod` via `actions/setup-go`
- Integration job sets up Node.js for Newman
- Server readiness: polls with curl for up to 30 seconds
- Release workflow (`.github/workflows/release.yml`) triggers on git tags via GoReleaser

## Dependency Updates

- **Automated**: Renovate auto-creates and auto-merges PRs (config: `renovate.json`)
- **Manual**: `make update` (runs `go get -u && go mod tidy`)

## Quick Test Commands

```bash
make test-case-one    # Single flight: [["SFO", "EWR"]]
make test-case-two    # Two flights: [["ATL", "EWR"], ["SFO", "ATL"]]
make test-case-three  # Four flights: [["IND", "EWR"], ["SFO", "ATL"], ["GSO", "IND"], ["ATL", "GSO"]]
make open-swagger     # Open Swagger UI in browser
```
