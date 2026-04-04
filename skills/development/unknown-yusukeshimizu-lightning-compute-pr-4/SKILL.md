---
name: lcp-go-lcpd
description: Develop the go-lcpd daemon/tools (Go). Follow repo principles (robustness, TDD, lint) and validate with make test/lint/gen.
metadata:
  short-description: Work on the go-lcpd implementation
---

You are working in the `go-lcpd/` module (the reference LCP daemon and tools).

## Scope

- Module: `go-lcpd/`
- Primary behavior sources:
  - Protocol spec: `docs/protocol/protocol.md`
  - WYSIWID design doc (when present): `go-lcpd/spec.md` (see `$lcp-wysiwid-spec`)

## Development principles

These are the consolidated rules that previously lived in `go-lcpd/AGENTS.md`:

1. If `go-lcpd/spec.md` exists, implementation MUST match the behavior defined there.
2. Design for robustness. Keep modules aligned with SRP.
3. Use a ubiquitous language. Keep terminology consistent across code and docs.
4. Test-first. Prefer TDD when changing behavior.
5. Run golangci-lint v2. When changing code, run `make lint` and fix findings.
6. Use `cmp.Diff` in tests. Compare expected vs actual with `github.com/google/go-cmp/cmp.Diff`.
7. Make logging diagnosable. Logging level MUST be configurable (for example via env vars).
8. Prefer lnd libraries. Use lnd-provided APIs/libraries before re-implementing.

## Go documentation and commenting (house style)

- Every function should have a comment describing purpose and assumptions.
- Function comments start with the function name (Effective Go), use complete sentences.
- Comments in code should explain intent, not restate the obvious.

## Workflow

1. Locate the relevant codepath under `go-lcpd/internal/` or `go-lcpd/tools/`.
2. If changing protobufs, edit the `.proto` sources and regenerate instead of hand-editing generated code.
3. Prefer small, testable changes; add/update unit tests and integration tests as needed.
4. If you are authoring/changing `go-lcpd/spec.md`, use `$lcp-wysiwid-spec`.

## Validation (run from `go-lcpd/`)

- `make gen` (only if protobuf / generated code changes)
- `make test`
- `make lint`
- `make fmt`

Optional integration test (regtest):

- `LCP_ITEST_REGTEST=1 go test ./itest/e2e -run Regtest_LNDPayment -count=1 -v`
