---
name: album-dashboard
description: Shows a structured progress dashboard for an album with percentage complete per phase, blocking items, and status breakdown. Use for a quick visual overview of album progress.
argument-hint: <album-name>
model: claude-haiku-4-5-20251001
prerequisites:
  - resume
allowed-tools:
  - Read
  - Glob
  - Grep
---

## Your Task

**Input**: $ARGUMENTS (album name)

Generate a structured progress dashboard for the specified album.

---

# Album Dashboard

You generate a comprehensive progress report for an album, showing completion percentage per workflow phase, blocking items, and a structured status breakdown.

---

## Workflow Phases

Track completion across these phases:

| Phase | Complete When |
|-------|-------------|
| 1. Concept | Album README has title, genre, tracklist defined |
| 2. Research | RESEARCH.md and SOURCES.md exist (if source-based) |
| 3. Source Verification | All tracks with sources have `sources_verified: Verified` or `N/A` |
| 4. Lyrics | All tracks have lyrics in their Lyrics Box |
| 5. Pronunciation | All pronunciation table entries applied in lyrics |
| 6. Review | Lyrics reviewed (no critical issues remain) |
| 7. Generation | All tracks have `has_suno_link: true` |
| 8. Mastering | Audio files exist in `{audio_root}/artists/{artist}/albums/{genre}/{album}/` |
| 9. Release | Album status is "Released" |

---

## Data Collection

### From MCP Server

1. Call `get_album_progress(album_slug)` — returns completion stats, phase detection, track counts by status
2. Call `find_album(name)` — returns album metadata (genre, status, track list with per-track fields)
3. Call `list_track_files(album_slug)` — returns tracks with file paths for any additional checks

These three calls replace all manual state.json reads and file globbing.

---

## Dashboard Format

```
ALBUM DASHBOARD
===============

[Album Title] ([genre])
Status: [status]

PROGRESS BY PHASE
─────────────────
[============================  ] 90%  Concept
[============================  ] 90%  Research
[========================      ] 75%  Source Verification
[====================          ] 63%  Lyrics Written
[================              ] 50%  Pronunciation
[============                  ] 38%  Reviewed
[========                      ] 25%  Generated
[                              ]  0%  Mastered
[                              ]  0%  Released

OVERALL: ████████░░░░░░░░ 47% complete

TRACK STATUS BREAKDOWN
──────────────────────
| # | Track | Status | Suno | Sources |
|---|-------|--------|------|---------|
| 01 | Track One | Final | link | Verified |
| 02 | Track Two | In Progress | — | Pending |
| 03 | Track Three | Not Started | — | N/A |
...

BLOCKING ITEMS
──────────────
! Track 02: Sources pending verification — blocks generation
! Track 05: No style prompt — blocks generation
! Track 07: Pronunciation table not applied — blocks generation

SUMMARY
───────
Tracks: [X complete / Y total]
Blocking: [N items]
Next action: [recommendation]
```

---

## Phase Completion Calculation

### Concept Phase
- 100% if: Album README has title AND tracklist with actual track names (not template)
- 50% if: README exists but tracklist is template placeholder
- 0% if: No README

### Research Phase (source-based albums only)
- 100% if: RESEARCH.md AND SOURCES.md both exist with content
- 50% if: Only one exists
- N/A if: Album is not source-based (no tracks have sources_verified field or all are N/A)

### Source Verification Phase
- % = (tracks with Verified or N/A) / total tracks * 100
- Skip tracks where sources_verified is N/A for the denominator

### Lyrics Phase
- % = (tracks with lyrics content) / total tracks * 100

### Generation Phase
- % = (tracks with has_suno_link=true) / total tracks * 100

### Mastering Phase
- Check `{audio_root}/artists/{artist}/albums/{genre}/{album}/` for WAV/FLAC files
- % = (audio files found) / total tracks * 100

### Release Phase
- 100% if album status is "Released", 0% otherwise

---

## Remember

1. **Visual progress bars** — Use ASCII progress bars for quick scanning
2. **Highlight blockers** — Blocking items are the most important info
3. **Include next action** — End with a clear recommendation
4. **Be accurate** — Count carefully, don't estimate
5. **Handle missing data gracefully** — If audio_root doesn't exist, mastering is 0%
