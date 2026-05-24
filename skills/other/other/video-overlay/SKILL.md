---
name: video-overlay
description: >
  Adds professional packaging and motion graphics to videos. Use when the user asks to add intros, outros, subtitles, transitions, watermarks, or lower thirds to a video. Supports multiple styles and custom options, no API key required.
version: 2.1.0
author: wells1137
tags: [video, editing, motion graphics, ffmpeg, moviepy, no-api-key]
---

# Overlay Skill

This skill adds a variety of professional packaging and motion graphics to videos, enhancing their overall quality. It supports both FFmpeg and MoviePy as backend engines and provides a rich set of preset templates and flexible custom parameters.

## When to Use

Use this skill when the user asks to:
- "Add an intro/outro to my video"
- "Put subtitles on this clip"
- "Create a transition between these two shots"
- "Add my logo as a watermark"
- "Put a title card at the beginning"
- "Add a lower third with my name and title"

## Core Features

| Feature          | Description                                    | Example Use Case                                  |
| :--------------- | :--------------------------------------------- | :------------------------------------------------ |
| **Intro/Outro**  | Add an engaging opening or a professional closing. | Brand logo animation, "Thanks for watching" screen. |
| **Subtitles/Titles** | Overlay static or dynamic text information.      | Dialogue subtitles, chapter titles, call-to-action text. |
| **Transitions**    | Create smooth or dynamic transitions between clips. | Fade between scenes, wipe to reveal next shot.      |
| **Watermark/Borders** | Add copyright information or decorative borders.   | Channel logo in corner, cinematic black bars.       |
| **Lower Thirds**   | Display names, locations, or other info.       | Interviewee name and title, location identifier.    |

## Usage Examples (Dialogue Format)

### 1. Add a Watermark

**User:** "Can you add my logo to this video? It should be in the top right corner."
*User uploads `my_video.mp4` and `logo.png`*

**Agent using `video-overlay`:**
```bash
python /home/ubuntu/skills/video-overlay/scripts/add_watermark.py --input my_video.mp4 --output video_with_watermark.mp4 --image logo.png --position top_right
```

### 2. Add Subtitles

**User:** "Add the subtitle 'Hello, world!' from 5 seconds to 10 seconds into the video."
*User uploads `my_video.mp4`*

**Agent using `video-overlay`:**
```bash
python /home/ubuntu/skills/video-overlay/scripts/add_subtitles.py --input my_video.mp4 --output video_with_subtitles.mp4 --text "Hello, world!" --start 00:00:05 --end 00:00:10 --style modern
```

## Resources

- **`/scripts/`**: Contains the Python implementation code for all features.
- **`/templates/presets.json`**: A JSON file containing preset styles for intros, subtitles, and lower thirds.
- **`/references/ffmpeg_moviepy_cheatsheet.md`**: A cheatsheet with common commands and tips for FFmpeg and MoviePy.
