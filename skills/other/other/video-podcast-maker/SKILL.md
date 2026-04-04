---
name: video-podcast-maker
description: Use when user provides a topic and wants an automated video podcast created, OR when user wants to learn/analyze video design patterns from reference videos — handles research, script writing, TTS audio synthesis, Remotion video creation, and final MP4 output with background music. Also supports design learning from reference videos (learn command), style profile management, and design reference library. Supports Bilibili, YouTube, Xiaohongshu, Douyin, and WeChat Channels platforms with independent language configuration (zh-CN, en-US).
argument-hint: "[topic]"
effort: high
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent
# --- Claude Code fields above, OpenClaw/SkillsMP fields below ---
author: Agents365-ai
category: Content Creation
version: 2.0.0
created: 2025-01-27
updated: 2026-04-03
bilibili: https://space.bilibili.com/441831884
github: https://github.com/Agents365-ai/video-podcast-maker
dependencies:
  - remotion-best-practices
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - ffmpeg
        - node
        - npx
    primaryEnv: AZURE_SPEECH_KEY
    emoji: "🎬"
    homepage: https://github.com/Agents365-ai/video-podcast-maker
    os: ["macos", "linux"]
    install:
      - kind: brew
        formula: ffmpeg
        bins: [ffmpeg]
      - kind: uv
        package: edge-tts
        bins: [edge-tts]
---

> **REQUIRED: Load Remotion Best Practices First**
>
> This skill depends on `remotion-best-practices`. **You MUST invoke it before proceeding:**
> ```
> Skill tool: skill="remotion-best-practices"
> ```

# Video Podcast Maker

## Quick Start

Open Claude Code and say: **"Make a video podcast about $ARGUMENTS"**

Or invoke directly: `/video-podcast-maker AI Agent tutorial`

---

## Design Learning

Extract visual design patterns from reference videos or images, store them in a searchable library, and apply them to new video compositions.

### Commands

```bash
# Learn from images (Claude Vision analyzes design patterns)
python3 learn_design.py ./screenshot1.png ./screenshot2.png

# Learn from a local video (ffmpeg extracts frames automatically)
python3 learn_design.py ./reference.mp4

# Learn from a URL (Playwright captures screenshots — experimental)
python3 learn_design.py https://www.bilibili.com/video/BV1xx411c7mD

# Save with a named profile and tags
python3 learn_design.py ./reference.mp4 --profile "tech-minimal" --tags "tech,minimal,dark"
```

### Reference Library Commands

```
references list          # List all stored references (auto-cleans orphaned entries)
references show <id>     # Show full design report for a reference
references delete <id>   # Delete a reference and its files
```

### Style Profile Commands

```
profiles list            # List all saved style profiles
profiles show <name>     # Show profile props_override
profiles delete <name>   # Delete a style profile
profiles create <name>   # Create a new style profile interactively
```

### Pre-Workflow Usage

When the user provides a reference video or image alongside a video creation request, extract design patterns before Step 1 and apply them as session overrides. See `references/workflow-steps.md` → Pre-workflow section for the full extraction flow.

### Step 9 Integration

Before choosing visual design in Step 9, check for matching style profiles or reference library entries. Apply the best match as a starting point for Remotion composition props. See `references/workflow-steps.md` → Step 9 Style Profile Integration for the priority chain.

---

## Auto Update Check

**Agent behavior:** Check for updates at most once per day (throttled by timestamp file):

```bash
STAMP="${CLAUDE_SKILL_DIR}/.last_update_check"
NOW=$(date +%s)
LAST=$(cat "$STAMP" 2>/dev/null || echo 0)
if [ $((NOW - LAST)) -gt 86400 ]; then
  timeout 5 git -C ${CLAUDE_SKILL_DIR} fetch --quiet 2>/dev/null || true
  LOCAL=$(git -C ${CLAUDE_SKILL_DIR} rev-parse HEAD 2>/dev/null)
  REMOTE=$(git -C ${CLAUDE_SKILL_DIR} rev-parse origin/main 2>/dev/null)
  echo "$NOW" > "$STAMP"
  if [ -n "$LOCAL" ] && [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
    echo "UPDATE_AVAILABLE"
  else
    echo "UP_TO_DATE"
  fi
else
  echo "SKIPPED_RECENT_CHECK"
fi
```

- **Update available**: Ask user via AskUserQuestion. Yes → `git -C ${CLAUDE_SKILL_DIR} pull`. No → continue.
- **Up to date / Skipped**: Continue silently.

---

## Prerequisites Check

!`( missing=""; node -v >/dev/null 2>&1 || missing="$missing node"; python3 --version >/dev/null 2>&1 || missing="$missing python3"; ffmpeg -version >/dev/null 2>&1 || missing="$missing ffmpeg"; [ -n "$AZURE_SPEECH_KEY" ] || missing="$missing AZURE_SPEECH_KEY"; if [ -n "$missing" ]; then echo "MISSING:$missing"; else echo "ALL_OK"; fi )`

**If MISSING reported above**, see README.md for full setup instructions (install commands, API key setup, Remotion project init).

---

## Overview

Automated pipeline for professional **Bilibili horizontal knowledge videos** from a topic.

> **Target: Bilibili horizontal video (16:9)**
> - Resolution: 3840×2160 (4K) or 1920×1080 (1080p)
> - Style: Clean white (default)

**Tech stack:** Claude + Azure TTS + Remotion + FFmpeg

### Output Specs

| Parameter | Horizontal (16:9) | Vertical (9:16) |
|-----------|-------------------|-----------------|
| **Resolution** | 3840×2160 (4K) | 2160×3840 (4K) |
| **Frame rate** | 30 fps | 30 fps |
| **Encoding** | H.264, 16Mbps | H.264, 16Mbps |
| **Audio** | AAC, 192kbps | AAC, 192kbps |
| **Duration** | 1-15 min | 60-90s (highlight) |

---

## Execution Modes

**Agent behavior:** Detect user intent at workflow start:

- "Make a video about..." / no special instructions → **Auto Mode**
- "I want to control each step" / mentions interactive → **Interactive Mode**
- Default: **Auto Mode**

### Auto Mode (Default)

Full pipeline with sensible defaults. **Only 1 mandatory stop:**

1. **Step 10**: After 720p preview render — user reviews, confirms before 4K

| Step | Decision | Auto Default |
|------|----------|-------------|
| 3 | Title position | top-center |
| 5 | Media assets | Skip (text-only animations) |
| 7 | Thumbnail method | Remotion-generated (16:9 + 4:3) |
| 9 | Outro animation | Pre-made MP4 (white/black by theme) |
| 9 | Preview method | Preview render (720p, self-validates) |
| 12 | Subtitles | Skip |
| 14 | Cleanup | Auto-clean temp files |

Users can override any default in their initial request:
- "make a video about AI, burn subtitles" → auto + subtitles on
- "use dark theme, AI thumbnails" → auto + dark + imagen
- "need screenshots" → auto + media collection enabled

### Interactive Mode

Prompts at each decision point. Activated by:
- "interactive mode" / "I want to choose each option"
- User explicitly requests control

---

## Workflow State & Resume

> **Planned feature (not yet implemented).** Currently, workflow progress is tracked via Claude's conversation context. If a session is interrupted, re-invoke the skill and Claude will check existing files in `videos/{name}/` to determine where to resume.

---

## Technical Rules

Hard constraints for video production — visual design is Claude's creative freedom:

| Rule | Requirement |
|------|-------------|
| **Single Project** | All videos under `videos/{name}/` in user's Remotion project. NEVER create a new project per video. |
| **4K Output** | 3840×2160, use `scale(2)` wrapper over 1920×1080 design space |
| **Content Width** | ≥85% of screen width |
| **Bottom Safe Zone** | Bottom 100px reserved for subtitles |
| **Audio Sync** | All animations driven by `timing.json` timestamps |
| **Thumbnail** | MUST generate 16:9 (1920×1080) AND 4:3 (1200×900). Title ≥80px bold, high contrast. |
| **Font** | PingFang SC / Noto Sans SC for Chinese text |

---

## Additional Resources

Claude loads these files on demand — **do NOT load all at once**:

- **[references/workflow-steps.md](references/workflow-steps.md)**: Detailed step-by-step instructions (Steps 1-14). Load at workflow start.
- **[references/design-guide.md](references/design-guide.md)**: Visual minimums, typography, layout patterns, checklists. **MUST load before Step 9.**
- **[references/troubleshooting.md](references/troubleshooting.md)**: Error fixes, BGM options, preference commands, preference learning. Load on error or user request.
- **[examples/](examples/)**: Real production video projects. Claude may reference these for composition structure and timing.json format.

---

## Directory Structure

```
project-root/                           # Remotion project root
├── src/remotion/                       # Remotion source
│   ├── compositions/                   # Video composition definitions
│   ├── Root.tsx                        # Remotion entry
│   └── index.ts                        # Exports
│
├── public/                             # Remotion default (unused — use --public-dir videos/{name}/)
│
├── videos/{video-name}/                # Video project assets
│   ├── workflow_state.json             # Workflow progress
│   ├── topic_definition.md             # Step 1
│   ├── topic_research.md               # Step 2
│   ├── podcast.txt                     # Step 4: narration script
│   ├── podcast_audio.wav               # Step 8: TTS audio
│   ├── podcast_audio.srt               # Step 8: subtitles
│   ├── timing.json                     # Step 8: timeline
│   ├── thumbnail_*.png                 # Step 7
│   ├── output.mp4                      # Step 10
│   ├── video_with_bgm.mp4             # Step 11
│   ├── final_video.mp4                 # Step 12: final output
│   └── bgm.mp3                         # Background music
│
└── remotion.config.ts
```

> **Important**: Always use `--public-dir` and full output path for Remotion render:
> ```bash
> npx remotion render src/remotion/index.ts CompositionId videos/{name}/output.mp4 --public-dir videos/{name}/
> ```

### Naming Rules

**Video name `{video-name}`**: lowercase English, hyphen-separated (e.g., `reference-manager-comparison`)

**Section name `{section}`**: lowercase English, underscore-separated, matches `[SECTION:xxx]`

**Thumbnail naming** (16:9 AND 4:3 both required):
| Type | 16:9 | 4:3 |
|------|------|-----|
| Remotion | `thumbnail_remotion_16x9.png` | `thumbnail_remotion_4x3.png` |
| AI | `thumbnail_ai_16x9.png` | `thumbnail_ai_4x3.png` |

### Public Directory

Use `--public-dir videos/{name}/` for all Remotion commands. Each video's assets (timing.json, podcast_audio.wav, bgm.mp3) stay in its own directory — no copying to `public/` needed. This enables parallel renders of different videos.

```bash
# All render/studio/still commands use --public-dir
npx remotion studio src/remotion/index.ts --public-dir videos/{name}/
npx remotion render src/remotion/index.ts CompositionId videos/{name}/output.mp4 --public-dir videos/{name}/ --video-bitrate 16M
npx remotion still src/remotion/index.ts Thumbnail16x9 videos/{name}/thumbnail.png --public-dir videos/{name}/
```

---

## Workflow

### Progress Tracking

At Step 1 start:
1. Create `videos/{name}/workflow_state.json`
2. Use `TaskCreate` to create tasks per step. Mark `in_progress` on start, `completed` on finish.
3. Each step updates BOTH `workflow_state.json` AND TaskUpdate.

```
 1. Define topic direction → topic_definition.md
 2. Research topic → topic_research.md
 3. Design video sections (5-7 chapters)
 4. Write narration script → podcast.txt
 5. Collect media assets → media_manifest.json
 6. Generate publish info (Part 1) → publish_info.md
 7. Generate thumbnails (16:9 + 4:3) → thumbnail_*.png
 8. Generate TTS audio → podcast_audio.wav, timing.json
 9. Create Remotion composition + Studio preview
10. Render 4K video → output.mp4
11. Mix background music → video_with_bgm.mp4
12. Add subtitles (optional) → final_video.mp4
13. Complete publish info (Part 2) → chapter timestamps
14. Verify output & cleanup
15. Generate vertical shorts (optional) → shorts/
```

### Validation Checkpoints

**After Step 8 (TTS)**:
- [ ] `podcast_audio.wav` exists and plays correctly
- [ ] `timing.json` has all sections with correct timestamps
- [ ] `podcast_audio.srt` encoding is UTF-8

**After Step 10 (Render)**:
- [ ] `output.mp4` resolution is 3840x2160
- [ ] Audio-video sync verified
- [ ] No black frames

---

## Key Commands Reference

See **CLAUDE.md** for the full command reference (TTS, Remotion, FFmpeg, shorts generation).

---

## User Preference System

Skill learns and applies preferences automatically. See [references/troubleshooting.md](references/troubleshooting.md) for commands and learning details.

### Storage Files

| File | Purpose |
|------|---------|
| `user_prefs.json` | Learned preferences (auto-created from template) |
| `user_prefs.template.json` | Default values |
| `prefs_schema.json` | JSON schema definition |

### Priority

```
Final = merge(Root.tsx defaults < global < topic_patterns[type] < current instructions)
```

### User Commands

| Command | Effect |
|---------|--------|
| "show preferences" | Show current preferences |
| "reset preferences" | Reset to defaults |
| "save as X default" | Save to topic_patterns |

---

## Troubleshooting & Preferences

> **Full reference:** Read [references/troubleshooting.md](references/troubleshooting.md) on errors, preference questions, or BGM options.
