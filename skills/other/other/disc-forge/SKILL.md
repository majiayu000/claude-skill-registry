---
name: disc-forge
description: "Burn Red Book audio CDs or MP3 data CDs on macOS via cdrdao, sourcing from Hoodrat HDD or local files. Audio CDs carry CD-Text from ID3 tags; MP3 discs use ISO9660+Joliet (~700 MB). Handles full-album burns and cherry-picked playlists. Triggers on 'burn CD', 'burn album', 'make audio CD', 'mixtape disc', 'soundtrack for the car'."
argument-hint: "--source <path|host:/path> --name <name> [--mp3-disc] [--speed N] [--gaps] [--dry-run]"
---

# disc-forge

Automated CD burning for macOS via cdrdao. Two modes:
- **Audio CD (default)** — Red Book, plays in any CD player, 80-min capacity, CD-Text from ID3 tags
- **MP3 data CD (`--mp3-disc`)** — plays in MP3-capable stereos (most 2005+ car head units), 700 MB capacity, ISO9660+Joliet filesystem

Turns "burn the BSG soundtrack to a CD" or "make an MP3 disc of these mantras" into a single command.

## When to Use

- User asks to burn an album, soundtrack, or playlist to an audio CD for a car stereo / home stereo
- Source music lives on Hoodrat HDD (Mac Mini) or in a local folder
- A USB CD burner is plugged into the current Mac
- User wants either a Red Book audio CD or an MP3 data CD

**Out of scope:** DVD burning, CD ripping (use XLD — see `~/.claude/agent_docs/music.md`), multi-session discs, DDP mastering, mixed-mode discs (audio + data on one disc).

## Quick Start

Burn a full album from Hoodrat HDD with one command:

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source "mac-mini-ts:/Volumes/Hoodrat HDD/Musica/BSG.S1 - OST/" \
  --name BSG-S1
```

That runs the full pipeline: preflight → tar-over-SSH stage → duration check → parallel WAV conversion → TOC build with CD-Text → cdrdao write at 16x → cleanup → eject. Takes ~5–7 minutes for an 80-minute disc. cdrdao streams its own progress to stdout; a 10-second countdown precedes the actual burn so `Ctrl-C` still aborts safely.

Before the first burn, make sure a blank writable CD-R or CD-RW is in the drive — `preflight.py` will abort early if not.

## The Pipeline

`burn_audio_cd.py` is the master orchestrator. It chains the stage scripts in sequence and halts on any failure, preserving staging for debugging. Each script is also independently usable.

**Shared stages** (both modes):

| Stage | Script | What it does |
|---|---|---|
| 1 | `preflight.py` | Verifies `cdrdao` + `ffmpeg`, drive reachable, **blank writable disc inserted**. Retries `drutil status` for ~3 s after `cdrdao drive-info` (which briefly locks the drive). Surfaces the `Unsupported` drutil label as an informational note — cdrdao bypasses DiscRecording. |
| 2 | `stage_tracks.py` | Pulls source files. Remote sources (`mac-mini-ts:/path`) use **tar-over-SSH**, not rsync. Local sources use `cp`. Filters to one format (default `mp3`) to dedupe MP3+WMA and MP3+M4A siblings. |
| final | `cdrdao write` | Actual burn. `--speed 16 --eject` by default. Streams progress. |

**Audio CD stages** (default):

| Stage | Script | What it does |
|---|---|---|
| 3 | `check_duration.py` | Totals runtime via ffprobe. Aborts if the album overruns 80-min Red Book capacity. Prints a format histogram so leftover duplicates show up. |
| 4 | `convert_to_wav.py` | Parallel ffmpeg MP3→44.1 kHz/16-bit/stereo PCM (the exact Red Book format). Idempotent — skips WAVs already fresh. |
| 5 | `build_toc.py` | cdrdao TOC with `CD_TEXT` blocks. Pulls title/artist/album from the **original** source file's ID3 tags (WAVs don't carry ID3). Gapless by default; `--gaps` inserts 2-sec spacers. |
| cleanup | inline | Deletes `<name>-wav/` on success. Keeps `<name>/` MP3 staging for re-burns. |

**MP3 data CD stages** (`--mp3-disc`):

| Stage | Script | What it does |
|---|---|---|
| 3 | inline (orchestrator) | Sum of file sizes vs. 700 MB ceiling. Aborts if over. |
| 4 | `build_data_toc.py` | `hdiutil makehybrid -iso -joliet` builds an ISO9660+Joliet image containing the files. Emits a cdrdao data TOC (`CD_ROM` / `TRACK MODE1` / `DATAFILE`). Volume label derived from `--name` (sanitized A-Z/0-9/_). |
| cleanup | inline | Deletes `<name>.iso` on success. Keeps `<name>/` source staging for re-burns. |

## Scripts

All scripts support `--help`. All live under `~/.claude/skills/disc-forge/scripts/`. Default staging root is `~/burn-staging/<name>/`.

```
preflight.py         # preflight.py [--json]
stage_tracks.py      # stage_tracks.py --source <path|host:/path> --dest <name> [--format mp3]
check_duration.py    # check_duration.py <staging-dir> [--ceiling 80] [--json]
convert_to_wav.py    # convert_to_wav.py <staging-dir> [--output <wav-dir>] [--jobs N]
build_toc.py         # build_toc.py --wav-dir <wavs> --source-dir <mp3s> --output <toc> [--gaps]
build_data_toc.py    # build_data_toc.py --source-dir <dir> --volume-label <label> --iso-output <iso> --toc-output <toc>
burn_audio_cd.py     # burn_audio_cd.py --source <path|host:/path> --name <name> [--mp3-disc] [--speed 16] [--gaps] [--dry-run] [--keep-wavs] [--ceiling 80]
```

Key `burn_audio_cd.py` flags:

- `--mp3-disc` — burn an MP3 data CD (ISO9660+Joliet) instead of a Red Book audio CD. 700 MB capacity, plays in MP3-capable car stereos (most 2005+ head units).
- `--data-ceiling N` — MP3 data disc capacity ceiling in MB (default 700, only with `--mp3-disc`).
- `--dry-run` — runs everything through TOC generation, skips the cdrdao write. Use to validate the whole pipeline on a disposable run.
- `--gaps` — 2-sec spacers between tracks (pop albums). Default is gapless (right for OSTs, film scores, live albums). Audio mode only.
- `--speed N` — cdrdao write speed multiplier. Default 16. Drop to 10 for maximum reliability on cheap media.
- `--keep-wavs` — preserve the intermediate WAV staging dir (audio mode) or ISO (data mode) after the burn.
- `--ceiling N` — audio CD capacity in minutes for the fit check. Default 80. Set to 74 for older 74-min media.

## Recipes

**Burn a full soundtrack from Hoodrat HDD** (the canonical path):

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source "mac-mini-ts:/Volumes/Hoodrat HDD/Musica/Blade Runner - OST/" \
  --name BladeRunner-OST
```

**Burn from a pre-staged local directory** (when tracks are already on the laptop):

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

**MP3 data CD for a modern car stereo** (2005+ head units, ~700 MB capacity):

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source ~/burn-staging/mantras \
  --name mantras \
  --mp3-disc
```

Volume label derives from `--name` (sanitized to uppercase A-Z/0-9/_). Stage MP3s with numeric prefixes (`01 Foo.mp3`, `02 Bar.mp3`) to force track order — most stereos play alphabetically. For MP4/Opus/M4A sources, transcode to MP3 first (stage_tracks.py filters to `.mp3` by default).

**Pop album with 2-sec gaps** (Led Zeppelin, Pink Floyd, etc.):

```bash
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py \
  --source "mac-mini-ts:/Volumes/Hoodrat HDD/Musica/Dark Side Of The Moon/" \
  --name DSOTM \
  --gaps
```

**Cherry-picked mixtape** (tracks from multiple albums):

Stage tracks manually into a single folder first, then point the orchestrator at it:

```bash
mkdir -p ~/burn-staging/my-mixtape
scp "mac-mini-ts:/Volumes/Hoodrat HDD/Musica/Blade Runner - OST/01 Main Titles.mp3" ~/burn-staging/my-mixtape/
scp "mac-mini-ts:/Volumes/Hoodrat HDD/Musica/Inception OST [2010]/01 Half Remembered Dream.mp3" ~/burn-staging/my-mixtape/
# ... rename files with numeric prefixes to force desired order ...
python3 ~/.claude/skills/disc-forge/scripts/burn_audio_cd.py --source ~/burn-staging/my-mixtape --name my-mixtape
```

Track order is determined by `sorted()` on filenames — use numeric prefixes (`01_`, `02_`, …) to force a specific sequence.

## Critical Reminders

Full expansions (with *why*) live in `references/gotchas.md`.

- **SMB is not reachable over Tailscale.** Port 445 is refused on `mac-mini-ts`; only port 22 works. Use SSH transport. `stage_tracks.py` already does this.
- **Apple's bundled `rsync` (openrsync 2.6.9) splits remote paths on spaces.** `stage_tracks.py` uses tar-over-SSH instead. Never use `rsync` for Hoodrat HDD.
- **cdrdao 1.2.6 rejects MP3 input directly.** The binary contains the literal string `"AIFF and MP3 not supported by cdrdao"`. WAV conversion is mandatory — `convert_to_wav.py` handles it. (Burn.app is the alternative if you want to skip WAV conversion — see `references/burn-app-fallback.md`.)
- **`drutil` "Unsupported" label is a red herring** for cdrdao. It only affects Apple's DiscRecording framework (Finder burn / Music.app burn / Burn.app), not cdrdao. `preflight.py` surfaces the label as a warning, not an error.
- **CD-Text must come from source ID3 tags, not WAVs.** PCM WAV has no tagging container. `build_toc.py` reads tags from the original file, references the matching WAV in `AUDIOFILE`.
- **macOS Sequoia killed Music.app and Finder's burn-to-disc.** Don't fall back to them.

## References

| File | Contents |
|---|---|
| `references/gotchas.md` | Full expanded failure-mode inventory from the author's first burn. Every trap explained with *why*, so the rule generalizes to novel drives and macOS versions. |
| `references/cdrdao-toc-format.md` | cdrdao TOC syntax cheatsheet: minimal skeleton, `CD_TEXT` blocks, PREGAP semantics, special-character escaping, how to run `cdrdao show-toc` to validate. |
| `references/hoodrat-layout.md` | Pointer to `~/.claude/agent_docs/music.md` (the canonical Hoodrat HDD layout) plus a one-line cheatsheet. |
| `references/burn-app-fallback.md` | If cdrdao refuses the drive: Burn.app GUI fallback with exact click sequence. |

## Dependencies

- `cdrdao` — `brew install cdrdao`
- `ffmpeg` + `ffprobe` — `brew install ffmpeg`
- SSH access to `mac-mini-ts` (only when sourcing from Hoodrat HDD)
- A USB CD burner that speaks MMC. The ASUS SDRW-08U9M-U works despite drutil labeling it Unsupported.
