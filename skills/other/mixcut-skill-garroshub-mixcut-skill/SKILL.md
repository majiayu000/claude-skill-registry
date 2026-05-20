---
name: mixcut
description: >
  Create short mixed-cut videos from YouTube clips with automated analysis, clipping, and professional subtitle processing.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
  - Task
model: claude-3-5-sonnet-20240620
---

# MixCut Skill

## CRITICAL INSTRUCTION: MANDATORY CONFIGURATION

You MUST NOT proceed to downloading or processing until the Project Configuration is fully defined.

**Step 1: The Configuration Gate**
Check if the user has provided ALL of the following:
- **Video Title**: Main title for intro and segment cards.
- **Caption Language**: Target language for subtitles (e.g., English, etc.). *Crucial: No bilingual output.*
- **Aspect Ratio**: 16:9 (Desktop), 9:16 (Shorts/TikTok), or 1:1.
- **Target Duration**: 30s, 60s, 120s, or 180s.
- **Pace**: Fast, Medium, or Slow.
- **Style**: Highlight Montage or Beat-cut.
- **Transitions**: none, fade, slide, flash, or glitch.

If ANY of these are missing, you MUST use the `AskUserQuestion` tool to obtain them. 
DO NOT assume defaults.
DO NOT start downloading until configuration is complete.

---

## Workflow

### Phase 1: Sources & Workspace Setup
1. **Gather Sources**: Ask for YouTube URLs from the user.
2. **Setup Workspace**:
   - Ensure the directory `./work` exists in the project root.
   - Prepare `./work/assets` and `./work/outputs` subdirectories.

### Phase 2: Content Analysis
For each YouTube URL provided:
1. **Download**:
   - Run `python skills/Youtube-clipper-skill/scripts/download_video.py <url> "./work/assets/youtube"`
2. **Analyze**:
   - Run `python skills/Youtube-clipper-skill/scripts/analyze_subtitles.py <subtitle_path>`
3. **Selection**:
   - Present analyzed chapters/highlights to the user.
   - Confirm which segments to include in the final cut.

### Phase 3: Assembly & Processing
1. **Configuration**: Create `./work/mixcut_config.json` with global settings and source clip metadata (start, end, title).
2. **Processing**:
   - Run `python skills/mixcut/scripts/process_mixcut.py "./work/mixcut_config.json"`
   - This script automates clipping, media normalization (ffmpeg), and generates the initial `timeline.json` and `final.srt`.

### Phase 4: Professional Subtitle Cleaning (Agent-Driven)
*This phase ensures high-quality, professional subtitles.*

1. **Read Timeline**: Access `./work/timeline.json`.
2. **Subtitle Optimization**:
   Iterate through all subtitle entries and apply the following cleaning logic:
   - **Remove Noise**: Strip speaker markers (e.g., `>>`, `>>>`) and sound cues (e.g., `[Music]`, `[Applause]`).
   - **Deduplication**: Remove repeated words, stutters, and verbal fillers ("uh", "um", "you know").
   - **Flow Improvement**: Merge fragmented phrases into natural, readable sentences.
   - **Professional Polish**: Refine text into the target language using appropriate technical terminology.
3. **Update**: Save the optimized content back to `./work/timeline.json`.
4. **Synchronize**: Run `python skills/mixcut/scripts/process_mixcut.py "./work/mixcut_config.json" --action generate_srt` to sync changes to `final.srt`.

### Phase 5: Rendering
1. **Delegate to Remotion**:
   - Use the `remotion` skill to render the project located in `skills/mixcut/remotion`.
   - Provide the absolute path to `./work/timeline.json` as input props.
   - Set output to `./work/outputs/final_mixcut.mp4`.

### Phase 6: Delivery Guard & Verification
*Mandatory verification before completion.*

1. **Integrity Check**:
   - Verify `./work/outputs/final_mixcut.mp4` exists and has a file size > 0.
   - Verify `./work/outputs/final.srt` exists and has a file size > 0.
2. **Troubleshooting**: If files are missing or empty, identify the failure point in previous phases and re-run the necessary steps.

### Phase 7: Completion & Cleanup
1. **Report**: Provide the paths to the final video and subtitle files.
2. **Retention Policy**: Do NOT delete the `./work` directory until the user explicitly confirms the results or you have verified the outputs physically.

---

## Technical Guidelines
- **Path Management**: Always use absolute paths when delegating tasks to external skills.
- **Cross-Platform**: Avoid hardcoding drive letters; use system-agnostic path resolution.
- **Performance**: Use parallel tool calls for independent download/analysis tasks where supported.
