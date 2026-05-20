---
name: explicit-checker
description: Scans lyrics for explicit content and verifies that explicit flags match actual content. Use before Suno generation or release to ensure accurate content ratings.
argument-hint: <album-path or track-path>
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Glob
  - Grep
---

## Your Task

**Path to scan**: $ARGUMENTS

1. Scan all lyrics for explicit words
2. Report findings with word counts per track
3. Flag mismatches (explicit content but flag says No, or vice versa)
4. Provide summary suitable for distributor submission

---

# Explicit Content Checker

You scan lyrics for explicit content to ensure proper flagging before release.

---

## Explicit Words (Require Explicit = Yes)

These words and variations require the explicit flag:

| Category | Words |
|----------|-------|
| **F-word** | fuck, fucking, fucked, fucker, motherfuck, motherfucker |
| **S-word** | shit, shitting, shitty, bullshit |
| **B-word** | bitch, bitches |
| **C-words** | cunt, cock, cocks |
| **D-word** | dick, dicks |
| **P-word** | pussy, pussies |
| **A-word** | asshole, assholes |
| **Slurs** | whore, slut, n-word, f-word (slur) |
| **Profanity** | goddamn, goddammit |

---

## Clean Words (No Explicit Flag Needed)

These are acceptable without explicit flag:
- damn, hell, crap, ass, bastard, piss

Note: "damn" alone is clean, but "goddamn" is explicit.

---

## Override Support

The MCP `check_explicit_content` tool automatically loads and merges user overrides from `{overrides}/explicit-words.md`. No manual config read or merge logic needed — pass lyrics text and get results with overrides applied.

### Override File Format

**`{overrides}/explicit-words.md`:**
```markdown
# Custom Explicit Words

## Additional Explicit Words
- slang-term
- regional-profanity
- artist-specific-explicit

## Not Explicit (Override Base)
- hell (context: historical/literary)
- damn (context: emphasis)
```

---

## Workflow

### For Album Path

1. Call `list_tracks(album_slug)` — get all tracks with metadata
2. For each track:
   - Call `extract_section(album_slug, track_slug, "lyrics")` — get lyrics text
   - Call `check_explicit_content(lyrics_text)` — returns matches with line numbers (overrides auto-merged)
   - Get Explicit flag from track metadata
   - Compare flag vs. content
3. Generate report

### For Single Track

1. Call `extract_section(album_slug, track_slug, "lyrics")` — get lyrics text
2. Call `check_explicit_content(lyrics_text)` — scan for explicit words
3. Get Explicit flag from track metadata via `get_track(album_slug, track_slug)`
4. Report findings

---

## Output Format

```
EXPLICIT CONTENT SCAN
Album: [Album Name]
Date: [Scan Date]

TRACK RESULTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Track 01: [Title]
  Flag: No
  Content: Clean
  Status: ✓ OK

Track 02: [Title]
  Flag: Yes
  Content: fuck (3), shit (2), bitch (1)
  Status: ✓ OK (flag matches content)

Track 03: [Title]
  Flag: No
  Content: fuck (1)
  Status: ⚠️ MISMATCH - Contains explicit content but flag is No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:
  Total tracks: 10
  Clean tracks: 7
  Explicit tracks: 3
  Mismatches: 1

ALBUM EXPLICIT FLAG: Yes (any track explicit = album explicit)

ACTION REQUIRED:
  - Track 03: Set Explicit flag to Yes
```

---

## Mismatch Detection

### Flag Says No, Content Is Explicit
```
⚠️ MISMATCH: Track contains explicit content but Explicit flag is "No"
ACTION: Set Explicit: Yes in track file
```

### Flag Says Yes, Content Is Clean
```
ℹ️ NOTE: Track flagged explicit but no explicit words found
This is OK - artist may want explicit flag for themes/context
No action required (conservative flagging is fine)
```

---

## Distributor Requirements

Most distributors (DistroKid, TuneCore, CD Baby) require:
- **Track-level flags**: Each track marked explicit or clean
- **Album-level flag**: If ANY track is explicit, album is explicit
- **Consistent metadata**: Flag must match actual content

**Consequences of wrong flags**:
- Explicit content marked clean → Potential removal from platforms, account issues
- Clean content marked explicit → Reduced reach (filtered from some playlists) but no penalty

**Rule**: When in doubt, mark explicit. Under-flagging is worse than over-flagging.

---

## Integration

This skill is called during:
1. **Ready to Generate Checkpoint** - Before Suno generation
2. **Album Completion Checklist** - Before release
3. **Manual review** - Anytime with `/explicit-checker [path]`

---

## Example Invocations

```
/explicit-checker artists/[artist]/albums/rock/dark-tide/
/explicit-checker artists/[artist]/albums/rock/dark-tide/tracks/01-the-tank.md
```

---

## Remember

- Case-insensitive matching (Fuck = fuck = FUCK)
- Check variations (fucking, fucked, fucker)
- Phonetic spellings count (fuk, sh1t if intentional)
- Context matters less than presence - if the word is there, flag it
- Album is explicit if ANY track is explicit
- **Override additions** - Add artist/genre-specific explicit words
- **Override removals** - Remove words for specific contexts (historical, literary)
