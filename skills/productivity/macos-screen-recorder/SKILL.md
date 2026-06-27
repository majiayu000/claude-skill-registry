---
name: macos-screen-recorder
description: Headless macOS screen recorder that captures the main display PLUS system audio via ScreenCaptureKit — no BlackHole/loopback driver, no sudo, just the standard Screen Recording permission. Use when you need to script a screen recording WITH system sound on macOS from the CLI (demos, captures, voice-demo recording) — the case QuickTime and `screencapture -v` can't cover without a virtual audio device.
author: Conner K Ward
---

# macos-screen-recorder (sck-record)

`sck-record.swift` → compiled `sck-record` (binary gitignored; built by `setup-machine`, or
`swiftc -O sck-record.swift -o sck-record`). Records the main display + system audio via
ScreenCaptureKit.

```
./sck-record <out.mp4> <seconds>
```

**The one true differentiator:** system audio from the CLI with **zero install** — no
BlackHole / loopback virtual device, no sudo; only the standard Screen Recording permission
(granted once to whatever app shells out). It is *not* a general "better than OBS/Screen
Studio" tool — it fills exactly the headless-CLI-with-system-audio gap.

`sck-record` is the raw capture primitive — it records, nothing more. To polish a
recording afterward (idle speed-up, auto-zoom, keystroke chips, smoothed cursor,
vertical export), pair it with
[screenstudio-alternative-skill](https://github.com/connerkward/screenstudio-alternative-skill):
record with `sck-record --no-cursor <out.mp4> <seconds>`, then run its post-production
pass on the resulting mp4. (Auto-zoom and keystroke overlays additionally need an
input-event log captured *during* recording, which that skill supplies; `sck-record`'s
pixels alone cover idle speed-up, cursor smoothing, and vertical export.)
