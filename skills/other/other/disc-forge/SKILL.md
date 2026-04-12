---
name: disc-forge
description: Burn Red Book audio CDs on macOS from local music files or a remote music library via cdrdao, with CD-Text pulled from ID3 tags. This skill should be used when the user asks to burn a CD, burn an album, make an audio CD, burn a soundtrack for the car, or create a mixtape disc. Handles full-album burns and cherry-picked playlists.
argument-hint: "--source <path|host:/path> --name <name> [--speed N] [--gaps] [--dry-run]"
---

# disc-forge

Automated audio CD burning for macOS via cdrdao. Turns "burn the BSG Season 1 soundtrack to a CD" into a single command.

## When to Use

- User asks to burn an album, soundtrack, or playlist to an audio CD for a car stereo or home stereo
- Source music lives in a local folder or on a remote machine reachable over SSH
- A USB CD burner is plugged into the current Mac
- User wants Red Book audio CDs (the ones that play in any standard CD player), not MP3 data CDs

**Out of scope (v1):** MP3 data CDs (needs `drutil burn` + filesystem image instead), DVD burning, CD ripping (use XLD), multi-session discs, DDP mastering.

## Quick Start

Burn a full album from a local staging directory with one command:

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source ~/Music/BSG-S1-OST \
  --name BSG-S1
```

That runs the full pipeline: preflight → stage → duration check → parallel WAV conversion → TOC build with CD-Text → cdrdao write at 16x → cleanup → eject. Takes ~5–7 minutes for an 80-minute disc. cdrdao streams its own progress to stdout; a 10-second countdown precedes the actual burn so `Ctrl-C` aborts safely.

Before the first burn, make sure a blank writable CD-R or CD-RW is in the drive — `preflight.py` will abort early if not.

## The Pipeline

`burn_audio_cd.py` is the master orchestrator. It chains the six scripts in sequence and halts on any failure, preserving staging for debugging. Each script is also independently usable.

| Stage | Script | What it does |
|---|---|---|
| 1 | `preflight.py` | Verifies `cdrdao` + `ffmpeg`, drive reachable, **blank writable disc inserted**. Notes (non-fatally) if drutil reports the drive "Unsupported" and explains cdrdao bypasses DiscRecording. |
| 2 | `stage_tracks.py` | Pulls source files. Remote sources (`host:/path`) use **tar-over-SSH**, not rsync. Local sources use `cp`. Filters to one format (default `mp3`) to dedupe MP3+WMA and MP3+M4A siblings. |
| 3 | `check_duration.py` | Totals runtime via ffprobe. Aborts if the album overruns 80-min Red Book capacity. Prints a format histogram so leftover duplicates show up. |
| 4 | `convert_to_wav.py` | Parallel ffmpeg MP3→44.1 kHz/16-bit/stereo PCM (the exact Red Book format). Idempotent — skips WAVs already fresh. |
| 5 | `build_toc.py` | Generates cdrdao TOC with `CD_TEXT` blocks. Pulls title/artist/album from the **original** source file's ID3 tags (WAVs don't carry ID3). Gapless by default; `--gaps` inserts 2-sec spacers. |
| 6 | `cdrdao write` | Actual burn. `--speed 16 --eject` by default. Streams progress. |
| 7 | cleanup | Deletes `<name>-wav/` on success. Keeps `<name>/` MP3 staging for re-burns. |

## Scripts

All scripts support `--help`. All live under `~/.claude/skills/disc-forge/scripts/`. Default staging root is `~/burn-staging/<name>/`.

```
preflight.py         # preflight.py [--json]
stage_tracks.py      # stage_tracks.py --source <path|host:/path> --dest <name> [--format mp3]
check_duration.py    # check_duration.py <staging-dir> [--ceiling 80] [--json]
convert_to_wav.py    # convert_to_wav.py <staging-dir> [--output <wav-dir>] [--jobs N]
build_toc.py         # build_toc.py --wav-dir <wavs> --source-dir <mp3s> --output <toc> [--gaps]
burn_audio_cd.py     # burn_audio_cd.py --source <path|host:/path> --name <name> [--speed 16] [--gaps] [--dry-run] [--keep-wavs] [--ceiling 80]
```

Key `burn_audio_cd.py` flags:

- `--dry-run` — runs everything through TOC generation, skips the cdrdao write. Use to validate the whole pipeline on a disposable run.
- `--gaps` — 2-sec spacers between tracks (pop albums). Default is gapless (right for OSTs, film scores, live albums).
- `--speed N` — cdrdao write speed multiplier. Default 16. Drop to 10 for maximum reliability on cheap media.
- `--keep-wavs` — preserve the intermediate WAV staging dir after the burn (normally deleted).
- `--ceiling N` — CD capacity in minutes for the fit check. Default 80. Set to 74 for older 74-min media.

## Recipes

**Burn a full soundtrack from a remote music library over SSH** (tar-over-SSH handles paths with spaces):

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source "music-server:/Volumes/Music/BSG Season 1 - OST/" \
  --name BSG-S1
```

Replace `music-server` with any `~/.ssh/config` alias. The script detects the `host:/path` form and switches to SSH transport automatically.

**Burn from a pre-staged local directory:**

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source ~/burn-staging/BSG-S1 \
  --name BSG-S1
```

The orchestrator detects that source == staging dir and skips the stage step.

**Dry-run the pipeline** (validate without burning a coaster):

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source ~/burn-staging/BSG-S1 \
  --name BSG-S1 \
  --dry-run
```

Runs every stage through TOC generation. Prints the cdrdao command you'd run next and the `cdrdao show-toc` command to validate the generated TOC.

**Pop album with 2-sec gaps** (Led Zeppelin, Pink Floyd, etc.):

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source ~/Music/DarkSideOfTheMoon \
  --name DSOTM \
  --gaps
```

**Cherry-picked mixtape** (tracks from multiple albums):

Stage tracks manually into a single folder first, then point the orchestrator at it:

```bash
mkdir -p ~/burn-staging/my-mixtape
cp ~/Music/BladeRunner/01\ Main\ Titles.mp3 ~/burn-staging/my-mixtape/
cp ~/Music/Inception/01\ Half\ Remembered\ Dream.mp3 ~/burn-staging/my-mixtape/
# ... rename files with numeric prefixes to force desired order ...
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source ~/burn-staging/my-mixtape \
  --name my-mixtape
```

Track order is determined by `sorted()` on filenames — use numeric prefixes (`01_`, `02_`, …) to force a specific sequence.

## Critical Reminders

Full expansions (with *why*) live in `references/gotchas.md`.

- **Apple's bundled `rsync` (openrsync 2.6.9) splits remote paths on spaces.** `stage_tracks.py` uses tar-over-SSH instead. Never use macOS's `rsync` against remote paths containing spaces.
- **cdrdao 1.2.6 rejects MP3 input directly.** The binary contains the literal string `"AIFF and MP3 not supported by cdrdao"`. WAV conversion is mandatory — `convert_to_wav.py` handles it. (Burn.app is the alternative if you want to skip WAV conversion — see `references/burn-app-fallback.md`.)
- **`drutil` "Unsupported" label is a red herring** for cdrdao. It only affects Apple's DiscRecording framework (Finder burn / Music.app burn / Burn.app), not cdrdao. `preflight.py` surfaces the label as a note, not an error.
- **CD-Text must come from source ID3 tags, not WAVs.** PCM WAV has no tagging container. `build_toc.py` reads tags from the original file, references the matching WAV in `AUDIOFILE`.
- **macOS Sequoia killed Music.app and Finder's burn-to-disc.** Don't fall back to them.
- **SMB over Tailscale does not work** on macOS: File Sharing binds only to the LAN interface, not the Tailscale tun. Use SSH transport (tar-over-SSH) for any remote music library reached via Tailscale.

## References

| File | Contents |
|---|---|
| `references/gotchas.md` | Full expanded failure-mode inventory. Every trap explained with *why*, so the rule generalizes to novel drives and macOS versions. |
| `references/cdrdao-toc-format.md` | cdrdao TOC syntax cheatsheet: minimal skeleton, `CD_TEXT` blocks, PREGAP semantics, special-character escaping, how to run `cdrdao show-toc` to validate. |
| `references/remote-music-library.md` | Pattern for pulling music from a remote machine over SSH when the library path contains spaces. |
| `references/burn-app-fallback.md` | If cdrdao refuses the drive: Burn.app GUI fallback with exact click sequence. |

## Dependencies

- `cdrdao` — `brew install cdrdao`
- `ffmpeg` + `ffprobe` — `brew install ffmpeg`
- A USB CD burner that speaks MMC. Tested with the ASUS SDRW-08U9M-U, which works despite `drutil` labeling it "Unsupported" — any generic MMC USB drive should behave the same.
- SSH access to the remote host (only when sourcing music from another machine)
