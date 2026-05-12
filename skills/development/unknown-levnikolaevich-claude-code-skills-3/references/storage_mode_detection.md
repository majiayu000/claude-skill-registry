<!-- SOURCE-OF-TRUTH: shared/references/storage_mode_detection.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Storage Mode Operations

Provider routing table for Agile task storage. Provider selection comes from `.hex-skills/environment_state.json -> task_management.provider`; this file does not detect providers.

## Mode Selection

| Provider | Source of truth | ID format |
|---|---|---|
| `linear` | Linear API | `PROJ-123` / UUID |
| `file` | Markdown files + `kanban_board.md` | `Epic N`, `US001`, `T001` |
| `github` | GitHub Issues + Projects v2 | issue `#N` |

Rules:
- Missing environment state defaults to `file`.
- Unknown provider is a contract error unless the skill explicitly falls back to `file`.
- Load only the selected provider transport reference for operation details; do not preload all provider docs.

## Operation Map

| Operation | Linear | File | GitHub |
|---|---|---|---|
| list epics | list projects | glob `epics/*/epic.md` | issues labeled `epic` |
| create epic | save project | write `epic.md` | create issue labeled `epic` |
| list stories | list project issues | glob `stories/*/story.md` | sub-issues |
| create story | save issue | write `story.md` | create issue/sub-issue |
| list tasks | list child issues | glob `tasks/*.md` | sub-issues |
| create task | save child issue | write `T{NNN}.md` | create issue/sub-issue |
| update status | save issue state | edit `**Status:**` | edit Project v2 status |
| add comment | Linear comment | write `comments/{ts}.md` | issue comment |

## Status Map

| Abstract | Linear/File/GitHub value |
|---|---|
| new | `Backlog` |
| ready | `Todo` |
| working | `In Progress` |
| review | `To Review` |
| rework | `To Rework` |
| complete | `Done` |
| removed | `Canceled` |

## Fallback

On Linear/GitHub auth, rate limit, timeout, tool-missing, or server failure:
1. Preserve partial remote evidence when available.
2. Update environment state fallback metadata.
3. Continue in file mode.

**Version:** 4.0.0
**Last Updated:** 2026-04-05
