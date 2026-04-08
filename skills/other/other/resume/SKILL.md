---
name: resume
description: Finds an album by name and shows detailed status with next steps. Use when the user mentions an album name or wants to continue previous work.
argument-hint: <album-name>
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Glob
  - Bash
  - bitwize-music-mcp
---

# Resume Album Work

**Purpose**: Find an album and resume work where you left off.

**Usage**:
```
/bitwize-music:resume <album-name>
/bitwize-music:resume my-album
/bitwize-music:resume "demo album"
```

**When to use**: When user wants to continue working on an existing album.

---

## Instructions

When this skill is invoked with an album name:

### Step 1: Find the Album via MCP

1. Call `find_album(name)` — fuzzy match by name, slug, or partial (case-insensitive)
2. If not found: MCP returns available albums — suggest closest match or `/bitwize-music:new-album`
3. If multiple matches: list all with paths, ask user which one
4. If MCP returns stale/missing cache error: call `rebuild_state()` then retry

### Step 2: Get Album Progress

1. Call `get_album_progress(album_slug)` — returns track counts by status, completion percentage, and detected workflow phase
2. Call `list_tracks(album_slug)` — returns per-track details (status, has_suno_link, sources_verified)

### Step 3: Update Session Context

Call `update_session(album=album_slug, phase=detected_phase)` to set the active album and phase.

### Step 4: Determine Current Phase

Based on album and track statuses, identify the workflow phase:

| Album Status | Track Statuses | Current Phase |
|--------------|----------------|---------------|
| Concept | Most "Not Started" | Planning - Need to fill in album README and create tracks |
| Research Complete | Some "Sources Pending" | Verification - Need human verification of sources (documentary albums) |
| Sources Verified | All sources verified | Ready to Write - Sources cleared, begin lyrics (documentary albums) |
| In Progress | Mixed, some "Not Started" | Writing - Need to complete lyrics (or route instrumental tracks to suno-engineer) |
| In Progress | Some "Sources Pending" | Verification - Need human verification of sources |
| In Progress | All have lyrics | Ready to Generate - Run Ready to Generate checkpoint |
| In Progress | Some "Generated" | Generating - Continue generating on Suno. Check Generation Logs for rejected tracks needing regeneration |
| In Progress | All "Generated", none "Final" | Review & Approve - Listen to generated tracks, mark keepers with ✓, regenerate rejected ones |
| Complete | All "Final" | Mastering - Ready to master audio |
| Released | All "Final" | Released - Album is live |

**Note**: Non-documentary albums skip `Research Complete` and `Sources Verified` — they go directly from `Concept` → `In Progress`.

### Step 5: Report to User

Present a clear status report:

```
📁 Album: [Album Title]
   Location: {content_root}/artists/{artist}/albums/{genre}/{album}/
   Status: [Album Status]

📊 Progress:
   - Tracks: [X completed / Y total] ([N vocal, M instrumental])
   - Not Started: X
   - In Progress: Y
   - Generated: Z
   - Final: N

📍 Current Phase: [Phase Name]

✅ What's Done:
   - [List completed items]

⏭️ Next Steps:
   1. [Specific action 1]
   2. [Specific action 2]
   3. [Specific action 3]

Ready to continue? Tell me what you'd like to work on.
```

### Step 6: Recommend the Single Best Next Action

Pick ONE clear recommendation from the decision tree below. Don't list 5 options — pick the best one, include the skill name, and be specific about which track.

**Decision Tree** (evaluate top-to-bottom, first match wins):

**Instrumental detection**: Check each track's frontmatter for `instrumental: true` or Track Details table for `**Instrumental** | Yes`. Instrumental tracks skip the lyrics workflow entirely and go straight to `/bitwize-music:suno-engineer`.

```
Album Status = "Concept"
  → "Define the album concept. Run /bitwize-music:album-conceptualizer"

Album Status = "Research Complete"
  → Any tracks Sources Pending?
    YES → "Sources need verification. Run /bitwize-music:verify-sources [album]"
    NO  → Any "Not Started" tracks instrumental?
      YES → "Create Style Box for instrumental track [name]. Use /bitwize-music:suno-engineer"
      NO  → "Ready to write! Pick a track and use /bitwize-music:lyric-writer"

Album has tracks with "Not Started"
  → Is the first not-started track instrumental?
    YES → "Create Style Box for [track]. Use /bitwize-music:suno-engineer directly (instrumental track)"
    NO  → "Write lyrics for [first not-started track]. Use /bitwize-music:lyric-writer"

Album has tracks with "In Progress" (lyrics partially written)
  → "Finish lyrics for [first in-progress track]. Use /bitwize-music:lyric-writer"

Album has tracks with "Sources Pending"
  → "Verify sources for [track]. Run /bitwize-music:verify-sources [album]"

All tracks have lyrics (or Style Box for instrumentals), none generated
  → Mixed album (vocal + instrumental)?
    YES → "All tracks ready! Run /bitwize-music:pronunciation-specialist on vocal tracks, then /bitwize-music:lyric-reviewer, then /bitwize-music:pre-generation-check to validate all gates (instrumental tracks auto-skip lyrics gates)."
    NO  → "All lyrics complete! Style prompts should be ready. Run /bitwize-music:pronunciation-specialist to check for pronunciation risks, then /bitwize-music:lyric-reviewer for final QC, then /bitwize-music:pre-generation-check to validate all gates before generating on Suno."

Some tracks generated, some not
  → Any Generated tracks without ✓ in Generation Log Rating?
    YES → "Track [name] was generated but not approved. Listen and decide:
           - Happy? Mark ✓ in Generation Log and set Status: Final
           - Not happy? Log the reason, then:
             Style issue → /bitwize-music:suno-engineer to revise Style Box
             Lyrics issue → /bitwize-music:lyric-writer to fix, then regenerate
             Bad luck → Regenerate on Suno with same settings (it's non-deterministic)"
    NO  → "Generate [first un-generated track] on Suno. Use /bitwize-music:suno-engineer"

All tracks generated, none Final
  → "All tracks generated! Listen to each track and approve:
     - Mark keepers with ✓ in Generation Log Rating column
     - Reject and regenerate any that don't meet quality standards
     - Once all have ✓, batch-approve:
       Use update_track_field(album_slug, track_slug, 'status', 'Final') for each approved track.
       Once all Final, album advances to Complete automatically."

All tracks generated, some Final
  → Any Generated (non-Final) tracks without ✓?
    YES → "Review track [name] — listen and approve (✓) or regenerate"
    NO  → "All tracks approved! Batch-approve: update_track_field(album_slug, track_slug, 'status', 'Final') for each.
           Then import audio with /bitwize-music:import-audio, then master with /bitwize-music:mastering-engineer"

All tracks Final
  → "All tracks approved! Import audio with /bitwize-music:import-audio, then master with /bitwize-music:mastering-engineer"

Album Status = "Complete"
  → "Album is complete! Release with /bitwize-music:release-director"

Album Status = "Released"
  → "This album is released! Consider /bitwize-music:promo-director for promotional content"
  → Also suggest: "Start a new album? Check /bitwize-music:album-ideas list"
```

**Format the recommendation as:**
```
RECOMMENDED NEXT ACTION:
  [Clear, specific instruction with skill name and track name]

WHY:
  [One sentence explaining why this is the right next step]
```

### When No Album Specified (No Arguments)

If invoked without an album name:
1. Call `get_session()` — check `last_album` from session context, resume that album
2. If no session context, call `list_albums()` to find all in-progress albums
3. Prioritize: closest to completion > unblocked work > last worked on
4. If no albums exist, suggest `/bitwize-music:new-album`

Present a multi-album summary if multiple are in progress:
```
You have X albums. Here's the most actionable:

PRIORITY 1: [album-name] ([genre])
  Status: [status] | Progress: [X/Y tracks]
  → [Recommended action]

Also in progress:
  - [album-2] — [brief status]
```

---

## Examples

### Example 1: Album in Writing Phase

```
/bitwize-music:resume my-album

📁 Album: My Album
   Location: ~/bitwize-music/artists/bitwize/albums/rock/my-album/
   Status: In Progress

📊 Progress:
   - Tracks: 3 completed / 8 total
   - Not Started: 3
   - In Progress: 2
   - Final: 3

📍 Current Phase: Writing Lyrics

✅ What's Done:
   - Tracks 1-3 have final lyrics
   - Album concept and tracklist defined

⏭️ Next Steps:
   1. Complete lyrics for Track 4 (in progress)
   2. Complete lyrics for Track 5 (in progress)
   3. Write lyrics for Tracks 6-8

Ready to continue? Tell me which track you'd like to work on.
```

### Example 2: Album Ready for Generation

```
/bitwize-music:resume demo-album

📁 Album: Demo Album
   Location: ~/bitwize-music/artists/bitwize/albums/electronic/demo-album/
   Status: In Progress

📊 Progress:
   - Tracks: 8 / 8 total (all lyrics complete)
   - Final: 8

📍 Current Phase: Ready to Generate

✅ What's Done:
   - All 8 tracks have complete lyrics
   - All lyrics phonetically reviewed
   - Suno Style and Lyrics boxes filled

⏭️ Next Steps:
   1. Run Ready to Generate checkpoint (I'll verify everything)
   2. Start generating on Suno
   3. Log generation attempts

Shall I run the Ready to Generate checkpoint now?
```

### Example 3: Album Not Found

```
/bitwize-music:resume my-album

❌ Album 'my-album' not found.

Available albums:
- demo-album (electronic) - In Progress
- example-tracks (hip-hop) - Complete

Did you mean one of these? Or use /bitwize-music:new-album to create a new album.
```

---

## Implementation Notes

- **Use MCP tools** - `find_album`, `get_album_progress`, `list_tracks`, `update_session` instead of reading state.json directly
- **Case-insensitive matching** - "Sample-Album" should match "sample-album"
- **Handle missing albums gracefully** - List what exists, don't error
- **Be specific about next steps** - Don't just say "continue working", say exactly what to do
- **Include full paths** - User needs to know where files are located
- **Use emojis sparingly** - Only for section headers in the report

---

## Model

Use **Sonnet 4.5** - This is a coordination/reporting task, not creative work.
