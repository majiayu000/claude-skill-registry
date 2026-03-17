---
name: using-youtube-download
description: Download YouTube video or audio with yt-dlp and ffmpeg at highest available quality.
---

# YouTube Download Skill

Teach how to download YouTube videos as video files and MP3 audio, defaulting to highest quality.

## Prerequisites
- `yt-dlp` (recommended fork of youtube-dl): https://github.com/yt-dlp/yt-dlp
- `ffmpeg` (for merging/conversion)

Install (Linux/macOS):

```bash
python3 -m pip install -U yt-dlp
# or
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && sudo chmod a+rx /usr/local/bin/yt-dlp

# ffmpeg
sudo apt install ffmpeg   # Debian/Ubuntu
brew install ffmpeg       # macOS (Homebrew)
```

Windows: use the yt-dlp.exe release and install ffmpeg for Windows.

---

## Download highest-quality video (merged MP4)

This downloads the best video and best audio and merges them into an MP4 (default highest quality).

```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "%(title)s.%(ext)s" <VIDEO_URL>
```

Notes:
- `-f "bestvideo+bestaudio/best"` prefers separate best video and audio streams and falls back to the single best format.
- `--merge-output-format mp4` ensures a widely compatible container.
- Output template `%(title)s.%(ext)s` names the file by video title.

To force a max resolution (e.g., 1080p):

```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format mp4 -o "%(title)s.%(ext)s" <VIDEO_URL>
```

---

## Download as MP3 (highest audio quality)

Extract and convert the best available audio to MP3 (highest quality):

```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" <VIDEO_URL>
```

Options:
- `-x` / `--extract-audio` extracts audio.
- `--audio-format mp3` converts to MP3.
- `--audio-quality 0` tells ffmpeg to use best VBR quality.

If you prefer 320kbps constant bitrate MP3:

```bash
yt-dlp -x --audio-format mp3 --postprocessor-args "-b:a 320k" -o "%(title)s.%(ext)s" <VIDEO_URL>
```

---

## Download a playlist

Download an entire playlist (preserve order):

```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "%(playlist_index)s - %(title)s.%(ext)s" <PLAYLIST_URL>
```

To download only a single video from a playlist use `--no-playlist`.

---

## Advanced examples

- Download best audio only (no conversion):

```bash
yt-dlp -f bestaudio -o "%(title)s.%(ext)s" <VIDEO_URL>
```

- Download a clip by time range (requires ffmpeg post-processing):

```bash
yt-dlp -f bestvideo+bestaudio --external-downloader ffmpeg --external-downloader-args "-ss 00:01:00 -to 00:02:00" -o "%(title)s.%(ext)s" <VIDEO_URL>
```

---

## Windows PowerShell examples

```powershell
.
# Highest-quality video
yt-dlp.exe -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "%(title)s.%(ext)s" https://www.youtube.com/watch?v=...

# MP3
yt-dlp.exe -x --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" https://www.youtube.com/watch?v=...
```

---

## Notes & best practices
- Respect YouTube's terms of service and copyright laws. Only download content you have rights to or permission to download.
- Use `--no-overwrites` to avoid replacing existing files.
- Use `--download-archive archive.txt` to avoid re-downloading previously downloaded videos when processing playlists or channels.
- Use `--quiet` for scripting and check exit codes for success.
- Cache and limit requests to avoid rate limits.

---

This skill covers common `yt-dlp` patterns to download highest-quality video and audio (MP3). For automation, combine these commands into scripts and use environment variables for URLs and output directories.
