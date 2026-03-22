---
name: auto-improvement
description: (ePost) Use when reviewing session performance, analyzing improvement trends, or understanding the metrics-capture-detection pipeline
user-invocable: false

metadata:
  agent-affinity: [epost-project-manager, epost-code-reviewer, epost-debugger]
  keywords: [metrics, improvement, lessons, trends, detection, rework, session]
  platforms: [all]
  triggers: ["improvement report", "session metrics", "detect patterns", "rework analysis"]
---

# Auto-Improvement Skill

## Purpose

Documents the automated feedback loop: metrics collection, lesson capture, and pattern detection across sessions.

## Architecture

```
SessionStart hook          Stop hooks (sequential)
      │                          │
  write marker ──→   session-metrics.cjs ──→ lesson-capture.cjs
  current-session.json       │                      │
                        append JSONL           evaluate thresholds
                        sessions.jsonl              │
                                             significant? ──→ prompt knowledge-capture
                                                  │
                                               /review-improvements
                                             (on-demand detection)
```

## Data Flow

### Storage Tiers

| Tier | Location | Tracked | Retention |
|------|----------|---------|-----------|
| Raw metrics | `.epost-data/improvements/sessions.jsonl` | No (gitignored) | Auto-rotate at 1000 lines |
| Session marker | `.epost-data/improvements/current-session.json` | No | Deleted on Stop |
| Detection report | `.epost-data/improvements/latest-report.json` | No | Overwritten per run |
| Significant learnings | `docs/` | Yes (git tracked) | Permanent |

### JSONL Schema

Each line in `sessions.jsonl` is a JSON object:

```json
{
  "sessionId": "string",
  "timestamp": "ISO-8601",
  "duration_ms": "number|null",
  "branch": "string",
  "git": { "filesChanged": 0, "insertions": 0, "deletions": 0 },
  "tasks": { "total": 0, "completed": 0, "failed": 0 },
  "errors": { "count": 0, "types": ["build|test|lint|runtime"] },
  "rework": { "fixIterations": 0, "verificationFailures": 0 },
  "skills": { "discovered": [], "loaded": [], "unused": [] },
  "knowledge": { "retrieved": 0, "captured": 0, "staleHits": 0 },
  "routing": { "intent": "string", "command": "string", "platform": "string" }
}
```

Full schema: `packages/core/assets/improvements-schema.json`

## Significance Thresholds

Lesson capture triggers automatically when:

| Trigger | Threshold | Capture Type |
|---------|-----------|--------------|
| Errors fixed | `errors.count > 0` | FINDING |
| Rework detected | `fixIterations >= 2` | PATTERN |
| Verification failure | `verificationFailures >= 1` | CONV |
| New skill first-seen | Not in previous 5 sessions | NOTE |

## Detection Engine

Analyzes accumulated metrics from `.epost-data/improvements/sessions.jsonl`:

| Detection | Method | Recommendation |
|-----------|--------|----------------|
| Repeat errors | Same error type 3+ times in 7 days | Create FINDING or fix root cause |
| Skill gaps | Platform detected but no platform-skill loaded | Check skill wiring |
| Stale knowledge | `docs/` entries >90 days with no references | Review or archive |
| Rework patterns | Avg fixIterations >2 over recent sessions | Review verification process |
| Unused skills | Loaded but unreferenced 10+ sessions | Optimize or remove |

Run via command: `/review --improvements`

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `session-init.cjs` | SessionStart | Writes `current-session.json` marker |
| `session-metrics.cjs` | Stop | Collects metrics, appends to JSONL |
| `lesson-capture.cjs` | Stop (prompt) | Evaluates significance, prompts capture |

## Related Skills

- `data-store` — `.epost-data/` convention for persistent agent data
- `knowledge-capture` — Post-task capture workflow (triggered by lesson-capture hook)
- `knowledge-retrieval` — Search existing knowledge before acting
- `knowledge-retrieval` — Knowledge system structure and conventions
- `verification-before-completion` — Verification failures tracked for rework detection
- `debug` — Error metrics auto-captured by session-metrics hook
- `code-review` — Convention violations auto-detected across sessions
