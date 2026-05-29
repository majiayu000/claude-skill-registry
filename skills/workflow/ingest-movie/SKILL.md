---
name: ingest-movie
description: >
  Locate NZBGeek releases with subtitle-rich movie files, auto-tag rage/anger/humor
  cues, and emit PersonaPlex-ready JSON for Horus Theory-of-Mind benchmarks.
triggers:
  - ingest movie
  - movie ingest
  - nzb search
  - movie subtitles
  - persona plex movie
allowed-tools:
  - Bash
  - Python
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      bins:
        - uv
        - ffmpeg
        - whisper
        - requests
---

Use this skill whenever we need cinematic emotional exemplars (respect, humor, regret, anger, rage, etc.) for PersonaPlex.

It enforces a **subtitle-first** workflow:

1. **Search** NZBGeek for scene releases that already include `.srt`/`.sup` files with stage directions.
2. **Map** rage/anger windows from the subtitle text or tags (no decoding needed yet).
3. **Clip + Transcribe** targeted scenes, marry them with the subtitle cues, and emit Persona-ready JSON.

## Commands

### `run.sh search "<title>"`

- Calls NZBGeek’s API (requires `NZBD_GEEK_API_KEY`) and prints size/date/link.
- Use this to locate releases that explicitly mention `subs`, `CC`, or `SDH`.

### `run.sh scenes find --subtitle <file.srt> (--query "text" | --tag laugh)`

- Quick TUI view of subtitle windows that match free text or cue tags (`rage`, `shout`, `laugh`, etc.).
- Pass `--video movie.mkv` to see ready-to-copy `ffmpeg -ss ... -to ...` snippets.
- Designed for “project agent wants a specific sequence” moments.

### `run.sh scenes quality --subtitle <file.srt> [--strict]`

- Validates subtitle quality for PersonaPlex ingestion before processing.
- Checks: encoding, entry count, emotion cue presence, timing consistency.
- Use `--strict` to fail on warnings (for CI pipelines).

### `run.sh scenes analyze --subtitle <file.srt> [--verbose] [--output-json report.json]`

- Scans a subtitle file and reports ALL emotion cues found, grouped by type.
- Shows count, tags found, and first occurrence for each emotion.
- Use this to assess a subtitle before extracting specific emotions.

### `run.sh scenes extract --subtitle <file.srt> --tag rage --video movie.mkv --clip-dir ./clips`

- Writes a PersonaPlex-ready manifest that lists each candidate scene, cue tags, inferred emotion, and clip timing.
- Optional `--clip-dir` automatically runs `ffmpeg` to produce numbered `.mkv` clips plus `.srt` subtitle snippets per match.
- Use this when we need every rage/anger sequence from a film—no guessing or manual scrubbing.

### `run.sh transcribe movie_clip.mkv --emotion rage --scene "..."`

- Extracts mono WAV via `ffmpeg`, runs Whisper (default `medium`), and joins the output with the matching `.srt`.
- Produces `*_persona.json` containing:
  - Stable `video_id`, movie title, scene notes, ISO timestamp.
  - Segment-by-segment tags (`laugh`, `rage`, `whisper_candidate`, etc.).
  - Rhythm metrics (WPM, pause count, duration).
- Pipe straight into `horus_lore_ingest.py emotion --input <dir> --emotion rage`.

> **Do we still need the movie if we have subtitles?**  
> Yes for PersonaPlex: subtitles help us *find* the right windows, but Whisper + rhythm features require the actual audio to model tone, pacing, and breath. Use `scenes extract --subtitle-only` when scouting, then transcribe once the clip is cut.

## Environment

| Variable | Purpose |
|----------|---------|
| `NZB_GEEK_API_KEY` (or `NZBD_GEEK_API_KEY`) | Auth for NZBGeek search |
| `NZB_GEEK_BASE_URL` (or `NZBD_GEEK_BASE_URL`) | Override for private Usenet proxies |
| `WHISPER_BIN` | Path to Whisper CLI (defaults to `~/.local/bin/whisper`) |
| `FFMPEG_BIN` | Path to ffmpeg (defaults to `/usr/bin/ffmpeg`) |
| `AUDIO_RMS_THRESHOLD` | Base RMS threshold for audio intensity tags (default `0.2`) |
| `AUDIO_RMS_WINDOW_SEC` | Window size in seconds for RMS scanning (default `0.5`) |

> Audio intensity tagging automatically installs `numpy` + `soundfile` via `uv`. If either import ever fails, the CLI logs a warning and continues without those tags so ingestion still works.

## Workflow Example

```bash
# 1. Find a release that ships with SDH subtitles
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/ingest-movie
./run.sh search "There Will Be Blood"

# 2. Extract rage windows from the downloaded subtitles
./run.sh scenes extract \
  --subtitle "/home/graham/Downloads/media/movies/There Will Be Blood (2007)/blood.en.srt" \
  --tag rage \
  --video "/home/graham/Downloads/media/movies/There Will Be Blood (2007)/There.Will.Be.Blood.2007.PROPER.1080p.BluRay.x264-ELBOWDOWN.mkv" \
  --clip-dir "./clips/there_will_be_blood_rage" \
  --output-json "./clips/there_will_be_blood_rage/scenes.json"

# 3. Transcribe one of the clips with subtitles + metadata baked in
./run.sh transcribe ./clips/there_will_be_blood_rage/clip_01.mkv \
  --subtitle ./clips/there_will_be_blood_rage/clip_01.srt \
  --emotion rage \
  --movie-title "There Will Be Blood" \
  --scene "Most explosive confrontation" \
  --characters "Daniel Plainview,Eli Sunday"
```

## Batch Processing (Automated Pipeline)

For automated Horus persona training, use the batch commands to process multiple movies at once.

### `run.sh batch discover [--subtitles]`

Scan media directories to create an inventory of available movies.

```bash
./run.sh batch discover --subtitles
# Shows: Title | Size | Subtitle availability (✓ SDH, ✓, ✗)
```

### `run.sh batch plan [--emotion rage,sorrow] [--include-unavailable]`

Create a processing manifest from built-in emotion-movie mappings (dogpile research).

```bash
./run.sh batch plan --emotion camaraderie
# Creates batch_manifest.json with ready/needs_subtitle/not_in_library status
```

### `run.sh batch run --manifest batch_manifest.json [--dry-run]`

Execute batch processing: extract → clip → transcribe → persona JSON.

```bash
./run.sh batch run --manifest batch_manifest.json --dry-run  # Preview
./run.sh batch run --manifest batch_manifest.json            # Execute
```

### `run.sh batch status`

Show status of processed emotion exemplars.

```bash
./run.sh batch status
# Shows: Emotion | Movies | Clips | Personas
```

## Built-in Emotion Mappings

The batch system includes curated movie-emotion mappings from dogpile research:

| Emotion | Actor Model | Movies |
|---------|-------------|--------|
| **rage** | Daniel Day-Lewis | There Will Be Blood, Sicario, No Country for Old Men |
| **anger** | Al Pacino / Marlon Brando | The Godfather, Heat, Apocalypse Now |
| **sorrow** | Russell Crowe / Ken Watanabe | Gladiator, The Last Samurai, Schindler's List |
| **regret** | George Carlin | YouTube standup, Full Metal Jacket |
| **camaraderie** | Javier Bardem / Tom Hanks | Dune, Dune Part Two, Band of Brothers, Saving Private Ryan, Fury |

## Agent-Friendly Commands

These commands are designed for easy use by project agents (like Horus) with integration into dogpile for research and agent-inbox for cross-project communication.

### `run.sh agent recommend <emotion> [--actor MODEL] [--library PATH]`

Research movies with emotional scenes for TTS training. Returns abstracts, balanced reviews, and scene recommendations for agent evaluation.

```bash
# Research rage movies with DDL intensity
./run.sh agent recommend rage --actor "DDL" --library /mnt/storage12tb/media/movies

# Output includes:
# - Actor model and voice tone for the emotion
# - BDI patterns (Belief/Desire/Intention) to match
# - Dogpile research results with movie abstracts and reviews
# - Local library availability check
# - Instructions for agent to respond with APPROVED/QUEUE/SKIP decisions
```

### `run.sh agent quick --movie PATH --emotion EMO --scene "desc" --timestamp "HH:MM:SS-HH:MM:SS"`

Single-step extraction that consolidates the 6-step manual workflow:
1. Download subtitles (if missing)
2. Extract video clip
3. Extract subtitle window
4. Run Whisper transcription
5. Create persona JSON
6. Update inventory

```bash
./run.sh agent quick \
  --movie "/mnt/storage12tb/media/movies/Troy (2004)" \
  --emotion rage \
  --scene "Achilles beach landing" \
  --timestamp "01:15:30-01:17:00" \
  --output /path/to/persona/exemplars/rage/
```

### `run.sh agent discover <library_path> [--emotion EMO] [--query TEXT]`

Discover emotion-matching scenes in local media library by scanning subtitles.

```bash
./run.sh agent discover /mnt/storage12tb/media/movies --emotion rage
# Outputs matching scenes with timestamps, ready for extraction
```

### `run.sh agent inventory [--emotion EMO] [--json]`

Show inventory of processed clips across all sessions.

```bash
./run.sh agent inventory
# Shows: Total clips, movies processed, clips per emotion, threshold status
```

### `run.sh agent request --to PROJECT --emotion EMO --desc "description"`

Send clip extraction request to another project via agent-inbox.

```bash
./run.sh agent request --to ingest-movie --emotion rage --desc "Need betrayal fury scenes" --count 5
```

### `run.sh agent recommend-book [--movie TITLE] [--emotion EMO] [--library PATH]`

Recommend books to read before processing a movie for emotion extraction.

```bash
# Find source material for a specific movie
./run.sh agent recommend-book --movie "Dune"

# Find thematically related books for an emotion
./run.sh agent recommend-book --emotion rage --library ~/library/books

# Combined: find books related to movie AND emotion
./run.sh agent recommend-book --movie "There Will Be Blood" --emotion rage
```

**Why read before watching?**
- Understand character motivations and internal monologue
- Note what was changed in the adaptation
- Provide richer context for emotion extraction
- Ground persona training in textual detail

See `/consume_common/WORKFLOW.md` for the complete book-before-movie pipeline.

## Radarr Integration (Automated Acquisition)

Automatically acquire movies from curated emotion mappings using Radarr.

### Horus TTS Preset

**All downloads enforce:**
- **1080p maximum** - No 4K (1080p sufficient for TTS voice extraction)
- **15GB maximum file size** - Prevents storage bloat
- **English audio required** - For TTS training
- **SDH subtitles preferred** - For emotion tagging

### Radarr Configuration

Configure in Radarr UI before using:

1. **Settings > Profiles > Quality Profiles** - Add "Horus TTS" profile:
   - Enable ONLY: Bluray-1080p, WEB 1080p, HDTV-1080p
   - Set Bluray-1080p Max Size: 15000 MB (15GB)
   - Disable all 4K qualities

2. **Settings > Custom Formats** - Add "SDH Subtitles":
   - Condition: Release Title contains "SDH" OR "CC" OR "Subs"
   - Score: +100

3. **Settings > Profiles > "Horus TTS"** - Set custom format scores:
   - SDH Subtitles = +100

### `run.sh acquire radarr [--preset horus_standard] [--emotion rage,sorrow]`

Add missing movies to Radarr with enforced constraints.

```bash
# Use the recommended preset (1080p, 15GB max, English, SDH subs)
./run.sh acquire radarr --preset horus_standard

# Preview what would be added
./run.sh acquire radarr --preset horus_standard --dry-run

# Add only specific emotions
./run.sh acquire radarr --preset horus_standard --emotion rage,anger
```

## Dogpile Integration

Use `/dogpile` with the `movie_scenes` preset for comprehensive movie research:

```bash
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/dogpile
./run.sh search "war movies betrayal scenes DDL intensity" --preset movie_scenes
```

The `movie_scenes` preset searches:
- IMDB, Rotten Tomatoes, Metacritic for reviews
- Letterboxd for community ratings
- Sublikescript, IMSDB for scripts
- OpenSubtitles for availability

## Cross-Project Workflow (Horus Example)

```
Horus Agent                              ingest-movie Skill
     |                                          |
     |-- /dogpile "rage movies" ------------------>
     |<-- Movie recommendations with reviews ------|
     |                                          |
     |-- "APPROVED: Troy - Achilles scene" ------->
     |                                          |
     |                  ./run.sh agent quick    |
     |                  --movie Troy            |
     |                  --emotion rage          |
     |                  --timestamp 01:15-01:17 |
     |                                          |
     |<-- Persona JSON created, inventory updated -|
     |                                          |
     |-- Import to ArangoDB knowledge graph ------>
```

## Sanity

```bash
./sanity.sh   # Verifies Typer CLI + scenes helpers load
```
