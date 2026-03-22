---
name: time
slug: time
description: LLM temporal reasoning scaffold for the temporal CLI.
when_to_use: Use when a task involves dates, deadlines, scheduling, or relative time reasoning.
metadata: {"openclaw":{"requires":{"bins":["temporal"]}}}
---

# time

Use `temporal` to anchor work at NOW and place events as spatial distances (ahead/behind) for reliable temporal reasoning.

## Ego-Moving Metaphor (Required)

Use one frame only: you move forward through time.
- Future is ahead of you.
- Past is behind you.
- Correct: "We are approaching the deadline."
- Incorrect: "The deadline is approaching."

## Prerequisites

- `temporal` must be on your `$PATH`.
- If `temporal` is not on `$PATH`, run `scripts/install.sh` from the skill directory.
- `scripts/install.sh` auto-detects OS/arch, verifies SHA-256 checksums from values bundled in the installer (not from the release checksums file), and installs to `/usr/local/bin/temporal` when writable or `~/.local/bin/temporal` otherwise.
- Installer defaults to `v0.1.0`. You can override version/install dir with `TEMPORAL_VERSION` and `TEMPORAL_INSTALL_DIR`.
- For versions without a bundled checksum, set `TEMPORAL_SHA256` to an independently obtained digest.
- Ensure `~/.local/bin` is on your `$PATH` (for example, `export PATH="$HOME/.local/bin:$PATH"` in your shell profile).
- Note: The OS-specific `curl` examples below install binaries without checksum verification; prefer `scripts/install.sh` when possible.
- Install (macOS Apple Silicon):
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-darwin-arm64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- Install (macOS Intel):
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-darwin-x64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- Install (Linux x64):
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-linux-x64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- Install (Linux ARM64):
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-linux-arm64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- Install a custom version with explicit checksum:
  `TEMPORAL_VERSION=v0.1.1 TEMPORAL_SHA256=<sha256> ./scripts/install.sh`
- Install/build instructions: [github.com/Ikana/temporal](https://github.com/Ikana/temporal)

## Quick Start

```bash
temporal init
temporal add "Sprint review" --on "2026-02-21" --type ceremony
temporal add "v0.3.0 deadline" --in "13 days" --type milestone --notes "new auth flow"
temporal show
```

## Commands

### `init [--timezone <iana_tz>] [--force]`

Create `time.md` with NOW as the anchor. Use `--force` to overwrite an existing file.

### `now [--timezone <iana_tz>]`

Update only the NOW section timestamp metadata. Does not recalculate event distances.

### `add <event> (--in <duration> | --on <date> | --at <datetime>) [--type <type>] [--notes <text>]`

Add one event with exactly one time selector:
- `--in`: relative duration (`"3 days"`, `"in 4 hours"`, `"2 days ago"`)
- `--on`: date input (`"2026-03-01"`, `"tomorrow"`, `"next Monday"`)
- `--at`: ISO datetime (`"2026-02-20T14:00:00Z"`)

### `show`

Print full `time.md` to stdout.

### `past`

Print NOW + the Behind (Past) timeline section.

### `ahead`

Print NOW + the Ahead (Future) timeline section.

### `refresh`

Move NOW to current time and recalculate all event distances/order.

### `remove <event>`

Remove an event from timeline and sequences.

### `seq <name> <event1> <event2> [event3...]`

Create/update a named sequence chain.

### `span <name> --from <when> --to <when>`

Create/update a named duration span. `--from` must be before `--to`.

## Annotated `time.md` Format

```markdown
# Time Context

## Now
- **timestamp**: 2026-02-19T09:00:00.000Z   <!-- anchor -->
- **weekday**: Thursday
- **week**: 8 of 52
- **quarter**: Q1 2026
- **timezone**: Europe/Amsterdam

## Timeline

### Behind (Past)
| distance | event | type | notes | iso |
|----------|-------|------|-------|-----|
| 1 day behind | bug #42 reported | issue | auth timeout | 2026-02-18T10:00:00.000Z |

### Ahead (Future)
| distance | event | type | notes | iso |
|----------|-------|------|-------|-----|
| 2 days ahead | sprint review | ceremony | demo v0.2.1 | 2026-02-21T14:00:00.000Z |

## Sequences
### release-cycle
v0.2.0 released → bug #42 reported → [NOW] → sprint review → v0.3.0 deadline

## Durations
| span | from | to | length |
|------|------|----|--------|
| current sprint | 5 days behind | 2 days ahead | 7 days |
```

## Scratch Pad Pattern (`/tmp`)

Use this for one-shot reasoning so project files stay clean:

```bash
cd /tmp
temporal init --force
temporal add "Draft due" --on "2026-02-25"
temporal add "Client review" --in "3 days"
temporal show
# draft your output using the timeline
rm -f time.md
```

## Sequences

Use sequences to express ordered chains for planning:

```bash
temporal seq "release-cycle" "RFC drafted" "Implementation starts" "Testing" "Launch"
```

`show` places `[NOW]` at the correct position relative to sequence events.

## Spans

Use spans for time windows:

```bash
temporal span "Sprint 12" --from "2026-02-17" --to "2026-02-28"
```

The Durations table shows from/to distances and total length.

## Key Rules

- Run `temporal refresh` before reading `time.md` when it may be stale.
- Event names must be unique; remove before re-adding the same name.
- Markdown timeline output is written to stdout.
- Errors/warnings are written to stderr.
- `temporal` is fully non-interactive (no prompts).
