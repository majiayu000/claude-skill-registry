---
name: logging-config
description: MANDATORY - All logging code must use slog with structured fields. Load before writing any logging.
---

# Structured Logging Standards

## Requirements

- Use `log/slog` exclusively
- Never use `log.Printf()`, `fmt.Print()`, or visual formatting (`===`, empty lines)
- Use structured fields, not string interpolation
- Single format: JSON to stdout

```go
// Wrong
logger.Printf("WARNING: Failed to fetch %s", url)

// Right
slog.Warn("upstream fetch failed", "upstream", url, "error", err)
```

---

## Setup

cooked uses a single JSON handler writing to stdout:

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
slog.SetDefault(logger)
```

No log streams, no OTel/ECS formats, no object storage — just structured JSON to stdout.

---

## Request Log Example

Every request is logged with structured fields:

```json
{
  "time": "2026-02-06T12:00:00Z",
  "level": "INFO",
  "msg": "request",
  "method": "GET",
  "path": "/https://cgit.internal/repo/plain/README.md",
  "upstream": "https://cgit.internal/repo/plain/README.md",
  "status": 200,
  "cache": "hit",
  "upstream_ms": 0,
  "render_ms": 12,
  "total_ms": 14,
  "content_type": "markdown",
  "bytes": 14832
}
```

Cache field values: `hit`, `miss`, `revalidated`, `expired`.

---

## Log Message Style Guide

| Rule | Guideline | Example |
|------|-----------|---------|
| Tense | Past for events, present for conditions | `upstream fetched`, `cache full` |
| Case | lowercase start (no capital unless proper noun) | `config loaded`, `mermaid block found` |
| Punctuation | No trailing period (fragments, not sentences) | `request completed` not `Request completed.` |
| Redundancy | No severity prefix (level conveys this) | `upstream unreachable` not `Error: upstream unreachable` |
| Specificity | State what failed, not generic failure | `upstream fetch failed` not `operation failed` |
| Brevity | Omit articles and filler words | `file too large` not `The file was too large` |
| Action | Use verb-noun or noun-verb pattern | `config loaded`, `invalid upstream url` |

## Severity Levels

| Level | When to use | Examples |
|-------|-------------|----------|
| ERROR | Unrecoverable failures requiring attention | `template parse failed`, `listen failed` |
| WARN | Degraded but recoverable situations | `upstream returned 5xx`, `cache eviction failed` |
| INFO | Normal business events | `request`, `server started`, `config loaded` |
| DEBUG | Internal details for troubleshooting | `cache hit`, `rewriting relative url`, `mdx import stripped` |

## Structured Fields

- Use snake_case for field names: `upstream_ms`, `content_type`, `cache_status`
- Suffix units: `_ms`, `_bytes`, `_count`
- Boolean fields: `has_mermaid`, `has_toc`
- Avoid embedding data in message string; use fields instead

```go
// Bad
slog.Info(fmt.Sprintf("fetched %s in %dms", url, dur))

// Good
slog.Info("upstream fetched", "upstream", url, "duration_ms", dur)
```
