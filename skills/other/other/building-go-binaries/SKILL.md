---
name: building-go-binaries
description: Build Go binaries for local development or release. Use when you need to compile the project, troubleshoot build failures, or understand the build pipeline.
---

# Building Go Binaries

All commands run from the Go module root (`installer/`).

## Local Development Build

```bash
task build
```

Builds a snapshot binary for the current platform via GoReleaser. Output goes to `./bin/`. This is the only command you need for local builds.

## How It Works

- Task wraps GoReleaser in snapshot mode (no git tag required, single target)
- GoReleaser config: `.goreleaser.yaml`
- Task runner config: `Taskfile.yml`
- Version info is injected via ldflags at build time (see `main.go` for the variables)

## When Builds Fail

1. Check that `go mod tidy` has been run (GoReleaser runs it as a pre-hook in release mode)
2. Check for compilation errors in the `go build` output
3. For GoReleaser-specific issues, read `.goreleaser.yaml` for the current configuration
