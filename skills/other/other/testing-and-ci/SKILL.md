---
name: testing-and-ci
description: Runs tests, lint, and format checks; explains CI workflows. Use when running or debugging tests, lint, or GitHub Actions.
---

# Testing and CI

## Commands

- **make test-all** – Run all Go tests (`go test ./...`).
- **make check-fmt** – Verify Go formatting (`gofmt -s -l`); fails if any file needs formatting.
- **make lint** – Run golangci-lint (requires golangci-lint installed).
- **make build** – Build the `neptune` binary.

## CI Workflows

- **test.yml** – On push to `main`/`release-*` and on PRs. Path filter for Go files and Makefile. Runs `make test-all` and `make check-fmt`.
- **lint.yml** – On PRs. Path filter for Go and lint config. Runs golangci-lint.
- **labeler.yml** – On pull_request. Runs actions/labeler with `.github/labeler.yml` (path and head-branch rules).
- **label-old-prs.yml** – workflow_dispatch. Backfills labels: applies same rules as labeler to head branch and PR title (labeler has no branch context on manual run), then runs the labeler for path-based labels. Use state and limit inputs.
- **release.yml** – On push of tags `v*.*.*`. Runs GoReleaser to create the GitHub Release and artifacts.

## Adding Tests

- Place `*_test.go` in the same package as the code (e.g. `internal/config/loader_test.go`).
- Use table-driven tests for multiple cases; single-case tests are fine when appropriate.
- Existing test packages: `internal/config`, `internal/git`, `internal/run`, `internal/notifications/github`. Add or extend tests when touching those areas or adding new packages.
- Do not depend on live GitHub or GCS in unit tests; use mocks or stubs.
