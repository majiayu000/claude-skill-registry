# macos-screen-recorder (sck-record)

*macos-screen-recorder (sck-record) is a macOS screen recorder that captures the screen with system audio via ScreenCaptureKit — CLI, no driver, no sudo — plus a Claude Code skill.*

![License: MIT](https://img.shields.io/badge/license-MIT-blue) ![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-d97757) ![macOS](https://img.shields.io/badge/macOS-13%2B-111) ![Swift · ScreenCaptureKit](https://img.shields.io/badge/Swift-ScreenCaptureKit-fa7343)

**Record your macOS screen *with the sound your Mac is playing* — headless, from the CLI — with no virtual audio driver, no BlackHole, no Loopback, no sudo. One Swift file built on [ScreenCaptureKit](https://developer.apple.com/documentation/screencapturekit), Apple's native capture framework.**

![sck-record usage: a terminal showing the one-line build (swiftc -O sck-record.swift), a 5-second capture writing demo.mp4 at 1920×1200 H.264 / AAC 48kHz, and an ffprobe confirming both a video stream and an audio stream — "← system audio present" — with a footer noting Screen Recording permission only, no driver install, no sudo](docs/usage.png)

*The whole gap, closed: `ffprobe` confirms the muxed file has both a video stream **and** a system-audio stream — captured with only the standard Screen Recording permission, no driver, no sudo.*

## 🤔 Why

macOS's built-in `screencapture -v` records **video only** — its `-g` flag captures the *microphone*, not what your speakers are playing. The usual fix is installing a virtual audio device (BlackHole, Loopback, Soundflower) and rerouting your output through it, which changes what *you* hear and may need a security-approval reboot. ScreenCaptureKit makes that unnecessary: since macOS 13 it can tap system audio directly under nothing but the standard Screen Recording grant. This is the smallest possible wrapper around that capability — one file, one binary, one command.

> **The one true differentiator:** system audio from a **headless CLI** with **zero install**. This is *not* a "better than OBS / Screen Studio" tool — it fills exactly the gap those don't: scriptable capture-with-sound, no driver.

## ✨ What it does

- 🔊 **Main display + system audio** — every app sound, browser tab, `say` voice, and music track your Mac outputs, muxed with the screen. **What you hear is untouched while recording.**
- 🎞️ **Standard H.264 / AAC `.mp4`** you can share immediately (8 Mbps video, 48 kHz stereo 160 kbps AAC).
- 🖥️ **Retina capture**, capped at 2560 px wide to keep files sane, up to 30 fps; cursor included (or `--no-cursor`).
- 🪶 **No daemons, no kernel extensions, no audio rerouting** — ~90 lines of Swift around `SCStream` + `AVAssetWriter`.

## 📦 Install (Claude Code plugin)

It ships as a skill — an AI agent (Claude Code) can drive it for you:

```
/plugin marketplace add connerkward/ckw-skills
/plugin install macos-screen-recorder@connerkward
```

Standalone (this repo only):

```
/plugin marketplace add connerkward/macos-screen-recorder-system-audio
/plugin install macos-screen-recorder@macos-screen-recorder
```

See **[docs/agents.md](docs/agents.md)** for the agent-driven workflow.

## 🛠️ Run it by hand (CLI)

**Requirements:** macOS 13 (Ventura)+ (the `SCStreamConfiguration.capturesAudio` API), and Xcode Command Line Tools (`xcode-select --install`).

```sh
swiftc -O sck-record.swift -o sck-record     # build once
./sck-record demo.mp4 5                       # or skip the build: swift sck-record.swift demo.mp4 5
```

```
sck-record [output.mp4] [seconds] [--no-cursor]
```

| Argument | Default | Description |
|---|---|---|
| `output.mp4` | `~/Desktop/sck.mp4` | Output file path. Overwritten if it exists. |
| `seconds` | `20` | Duration in seconds (fractional allowed). |
| `--no-cursor` | off | Omit the system cursor (for tools that overlay a smoothed synthetic one). |

The tool prints the output path and stops automatically after the requested duration.

## 🔐 Permissions

First run triggers macOS's **Screen Recording** permission prompt for the launching app (your terminal). Grant it under **System Settings → Privacy & Security → Screen & System Audio Recording**, then re-run. Same permission `screencapture` uses — **no separate audio permission**, because ScreenCaptureKit delivers system audio under the screen-recording grant. The microphone is never touched.

## ⚖️ How it compares

| Approach | System audio | Setup | Notes |
|---|---|---|---|
| **sck-record** | ✅ native | none | One binary, one permission. |
| `screencapture -v` (built-in) | ❌ | none | `-g` records the **mic**, not system output. |
| BlackHole / Loopback / Soundflower | ✅ via reroute | install driver, multi-output device, switch output | Rerouting changes what *you* hear; installs may need security approval. |
| OBS | ✅ via plugin/driver | install app, configure scenes + audio | Powerful, but heavyweight for "give me an mp4 of the next 10 seconds". |
| QuickTime screen recording | ❌ (mic only) | none | Needs a virtual driver for system audio. |

## 🔬 How it works

`SCStream` is configured with `capturesAudio = true`, yielding system-audio sample buffers alongside the screen frames. Both are muxed in real time into an `.mp4` by `AVAssetWriter` (H.264 video + AAC audio). They stay in sync because both inputs share the stream's presentation timestamps; writing starts on the first complete video frame. Read [sck-record.swift](sck-record.swift) — it's ~90 lines.

## 🚧 Limitations

- **Main display only** — no window or region selection.
- Fixed duration set up front; no interactive stop key (`Ctrl-C` aborts without finalizing).
- Output codec/bitrate hardcoded (H.264 8 Mbps / AAC 160 kbps) — it's one dictionary in the source to change to HEVC or other rates.

## 🗂️ Part of [ckw-skills](https://github.com/connerkward/ckw-skills)

The capture primitive behind the record→polish workflow: the [`screencast`](https://github.com/connerkward) skill calls this, and [`screenstudio-alt`](https://github.com/connerkward/screenstudio-alternative-skill) does the post-production (auto-zoom, idle speed-up, vertical export).

## License

[MIT](LICENSE) © Conner K Ward

---

🧭 **[ckw-skills](https://github.com/connerkward/ckw-skills)** — part of Conner K. Ward's collection of Claude Code skills & MCP servers.
