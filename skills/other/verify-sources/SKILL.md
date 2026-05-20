---
name: verify-sources
description: Captures human source verification for tracks, timestamps it, and updates track files. Use when sources need human review before generation.
argument-hint: <album-name>
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Bash
  - bitwize-music-mcp
---

## Your Task

**Input**: $ARGUMENTS (album name)

Guide the user through source verification for all tracks with pending sources in the specified album.

---

# Source Verification Skill

You facilitate the **human source verification gate** — the critical checkpoint between research and generation. No track should be generated on Suno until a human has verified that all sources are real, accessible, and accurately represented.

---

## Step 1: Find the Album

1. Call `find_album(name)` — fuzzy match by name, slug, or partial
2. If not found, MCP returns available albums

## Step 2: Identify Pending Tracks

1. Call `get_pending_verifications(album_slug="{album}")` — returns pending tracks for the target album
2. If no album specified, call `get_pending_verifications()` for all albums

If no pending tracks:
```
All tracks in [album] have been verified. No action needed.
```

If pending tracks exist, list them:
```
SOURCE VERIFICATION: [Album Title]
===================================

Tracks needing verification:
  1. [track-slug] — [track-title]
  2. [track-slug] — [track-title]
  ...

Total: X tracks pending verification
```

## Step 3: Walk Through Each Track

For each pending track:

1. Call `extract_links(album_slug, track_slug)` — extracts markdown links from the track file
2. Call `extract_links(album_slug, "SOURCES.md")` — get the full citation list
3. **Read RESEARCH.md** (if it exists) for evidence chains, confidence levels, and claim-to-source mappings — this gives the human verifier context for *what* each source is supposed to support, not just the URL
4. **Present sources to the user**:

```
TRACK: [track-title]
--------------------
Sources referenced in this track:

  1. [Source Name](URL) — [brief description of what it supports]
  2. [Source Name](URL) — [brief description]
  ...

Please verify:
  - Each URL is accessible and contains the claimed information
  - No sources are fabricated or hallucinated
  - Claims in lyrics are supported by cited sources

Type "verified" to confirm, or describe any issues.
```

4. **Wait for user response**:
   - If "verified" (or equivalent affirmative) → update the track
   - If issues reported → note them, ask user how to proceed

## Step 4: Update Track Files

When user confirms verification for a track:

1. Call `update_track_field(album_slug, track_slug, "sources-verified", "✅ Verified (YYYY-MM-DD)")` — updates the field and auto-rebuilds state cache
   - Use today's date

2. **Confirm the update**:
```
✅ [track-title] — Sources verified (2025-02-06)
```

3. Move to next pending track

## Step 5: Update Album Status (Auto-Advance)

After processing all tracks, check if the album status should advance:

1. Call `get_album_progress(album_slug)` — check how many tracks are now verified
2. **If ALL tracks are verified** (no more pending):
   - Read the album README to check current album status
   - If album status is `Research Complete`:
     - Update album README: change `| **Status** | Research Complete |` → `| **Status** | Sources Verified |`
     - Report: "Album status advanced: Research Complete → Sources Verified"
   - If album status is `In Progress`:
     - Report: "All track sources verified. Album status stays In Progress (already past research phase)."
3. **If some tracks still pending**:
   - Report how many remain and which ones
4. **Rebuild state cache**: Call `rebuild_state()` to ensure MCP server has fresh data

5. **Summary report**:
```
VERIFICATION COMPLETE
=====================
Album: [title]
Tracks verified: X/Y
Album status: [previous] → [new status]
Date: YYYY-MM-DD

All sources verified. This album is cleared for lyric writing.
Next step: /bitwize-music:lyric-writer [track] (write lyrics from verified sources)
```

**Partial verification report** (if some tracks still pending):
```
VERIFICATION PROGRESS
=====================
Album: [title]
Tracks verified this session: X
Tracks still pending: Y
  - [track-slug] — [reason if known]

Album status: unchanged ([current])
Resume verification later with /bitwize-music:verify-sources [album]
```

---

## Handling Issues

If the user reports a problem with a source:

1. **Document the issue** in the track file as a comment or note
2. **Do NOT mark as verified** — keep status as Pending
3. **Suggest resolution**:
   - Source URL broken → "Can you find an updated URL?"
   - Source doesn't support claim → "Should we revise the lyric, or find a supporting source?"
   - Source is fabricated → "I'll remove this source. Do we need to revise the track?"
4. After resolution, re-present for verification

---

## Remember

- **Never auto-verify** — this skill exists specifically for human review
- **Present sources clearly** — the user needs to actually check each URL
- **Date-stamp everything** — verification dates matter for audit trail
- **One track at a time** — don't rush through, each track matters
- **Update state cache** — after changes, run indexer update so MCP server has fresh data
