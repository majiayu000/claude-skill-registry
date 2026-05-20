---
name: Logging
description: Standards for structured logging and observability in Golang.
metadata:
  labels: [golang, logging, slog, zap, observability]
  triggers:
    files: ['go.mod', 'pkg/logger/**']
    keywords: [logging, slog, structured logging, zap]
---

# Golang Logging Standards

## **Priority: P1 (STANDARD)**

## Principles

- **Structured Logging**: Use JSON or structured text. Readable by machines and humans.
- **Leveled Logging**: Debug, Info, Warn, Error.
- **Contextual**: Include correlation IDs (TraceID, RequestID) in logs.
- **No `log.Fatal`**: Avoid terminating app inside libraries. Return error instead. Only `main` should exit.

## Libraries

- **`log/slog` (Recommended)**: Stdlib since Go 1.21. Fast, structured, zero-dep.
- **Zap (`uber-go/zap`)**: High performance, good if pre-1.21 or extreme throughput needed.
- **Zerolog**: Zero allocation, fast JSON logger.

## Guidelines

- Initialize logger at startup.
- Inject logger or use a global singleton configured at startup (pragmatic choice).
- Use `slog.Attr` for structured data.

## References

- [Slog Patterns](references/slog-patterns.md)
