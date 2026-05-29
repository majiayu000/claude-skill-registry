---
name: Video Clipper
description: Create video clips from chapter timestamps using ffmpeg. Use when given a video file and timestamps/chapters to split into separate clips.
version: 1.0.0
dependencies: ffmpeg
allowed-tools: [Bash, Read]
---

# Video Clipper

## Overview
This Skill uses ffmpeg to create video clips from a source video file. It supports two modes:
1. **Multi-chapter mode**: Split a video into multiple clips based on chapter timestamps
2. **Single snippet mode**: Extract one clip from a time range (e.g., "55s to 2m35s")

Supports multiple video formats (MP4, MOV, AVI, MKV) and offers both fast stream copy mode and re-encode mode for consistent quality.

## When to Apply
Use this Skill when:
- User has a video file and wants to split it into clips
- User provides chapter markers or timestamps with topic names
- User wants to extract a specific segment with a time range (e.g., "55s to 2m35s", "1:30 to 5:45")
- User wants to create a single clip snippet from a time range
- User has completed Video Transcript Analyzer skill and now wants to create clips from those timestamps
- User asks to "split video by chapters", "create clips from timestamps", "extract video segments", or "create a clip from X to Y"

Do NOT use this Skill for:
- Video editing (adding effects, transitions, etc.)
- Audio-only files (use audio processing tools instead)
- Combining/merging multiple videos
- Format conversion only (use ffmpeg directly)

## Inputs

**For Multi-Chapter Mode:**
1. **Video file path** - Full path to source video (MP4, MOV, AVI, MKV, etc.)
2. **Chapter list with timestamps** - One of these formats:
   - `00:00:00 - Chapter Name`
   - `00:05:30 - Another Chapter`
   - `HH:MM:SS - Chapter Name`
   - `MM:SS - Chapter Name` (for videos under 1 hour)
3. **Output directory** (optional) - Where to save clips
4. **Encoding preference** (optional) - "copy" or "encode"

**For Single Snippet Mode:**
1. **Video file path** - Full path to source video
2. **Time range** - Natural language or standard formats:
   - `55s to 2m35s` (natural language)
   - `1:30 to 5:45` (MM:SS format)
   - `00:01:30 to 00:05:45` (HH:MM:SS format)
   - Start and end time in any mix of formats
3. **Output filename** (optional) - Name for the clip file
4. **Encoding preference** (optional) - "copy" or "encode"

## Outputs

**For Multi-Chapter Mode:**
- Individual video clip file for each chapter with sanitized filename
- Format: `01-Chapter_Name.mp4` (numbered, spaces replaced with underscores)
- Summary report with all clips, durations, sizes, and commands used

**For Single Snippet Mode:**
- One video clip file with specified or auto-generated name
- Format: `[video_name]_[start]-[end].mp4` or custom filename
- Brief report with clip duration, size, and command used

## Instructions for Claude

### Step 1: Validate Prerequisites

First, check if ffmpeg is installed:
```bash
which ffmpeg && ffmpeg -version
```

If not installed, provide installation instructions:
- **macOS**: `brew install ffmpeg`
- **Linux (Ubuntu/Debian)**: `sudo apt-get install ffmpeg`
- **Linux (RHEL/CentOS)**: `sudo yum install ffmpeg`

Ask user to install ffmpeg before proceeding if missing.

### Step 2: Detect Mode (Single Snippet vs Multi-Chapter)

Check the user's request to determine which mode to use:

**Single Snippet Mode indicators:**
- User provides a time range: "55s to 2m35s", "from 1:30 to 5:45", "extract 0:55 to 2:35"
- User says: "create a clip from X to Y", "extract segment", "get the part between X and Y"
- User provides start and end times without chapter names
- Only ONE time range is mentioned

**Multi-Chapter Mode indicators:**
- User provides multiple timestamps with names/descriptions
- User says: "split into chapters", "create clips from these timestamps"
- User has a list of timestamps with chapter names
- Multiple time ranges or chapter markers

**If Single Snippet Mode detected**, skip to **Step 2a: Single Snippet Workflow** below.
**If Multi-Chapter Mode detected**, continue to **Step 2b: Multi-Chapter Workflow** below.
**If unclear**, ask user: "Would you like to create (1) a single clip from a time range, or (2) multiple clips from chapter timestamps?"

### Step 2a: Single Snippet Workflow

For creating one clip from a time range:

1. **Get video file path**:
   - If not provided, ask: "Please provide the full path to your video file"
   - Validate file exists: `ls -lh [filepath]`
   - Show file size and duration

2. **Parse time range**:
   - Look for patterns like:
     - `55s to 2m35s` → convert to seconds: 55 to 155
     - `1:30 to 5:45` → convert to seconds: 90 to 345
     - `00:01:30 to 00:05:45` → already in HH:MM:SS format
   - Support formats:
     - `Xs` (seconds): 55s = 55 seconds
     - `Xm` or `XmYs` (minutes): 2m35s = 155 seconds, 5m = 300 seconds
     - `XhYm` or `XhYmZs` (hours): 1h30m = 5400 seconds
     - `MM:SS`: 1:30 = 90 seconds
     - `HH:MM:SS`: 00:01:30 = 90 seconds
   - If time range not clear, ask: "What time range would you like to extract? (e.g., '55s to 2m35s' or '1:30 to 5:45')"

3. **Get output filename**:
   - If not provided, generate: `[video_name]_[start]-[end].mp4`
   - Example: `customer-call_00-55_02-35.mp4`
   - Ask: "What would you like to name this clip? (Press Enter for: [suggested_name])"

4. **Get encoding preference**:
   - Ask: "Encoding mode: 'copy' (fast) or 'encode' (precise)? Default: copy"

5. **Convert times to HH:MM:SS format** for ffmpeg:
   ```python
   def seconds_to_timestamp(seconds):
       h = seconds // 3600
       m = (seconds % 3600) // 60
       s = seconds % 60
       return f"{h:02d}:{m:02d}:{s:02d}"
   ```

6. **Generate ffmpeg command**:
   - Copy mode: `ffmpeg -i [video] -ss [start] -to [end] -c copy -avoid_negative_ts 1 "[output]"`
   - Encode mode: `ffmpeg -i [video] -ss [start] -to [end] -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k "[output]"`

7. **Execute command**:
   - Show command to user
   - Execute and capture output
   - Verify clip was created

8. **Report results**:
   ```markdown
   # Video Clip Created

   **Source:** [video_path]
   **Time Range:** [start] to [end] ([duration])
   **Output:** [output_path]
   **Size:** [file_size]
   **Encoding:** [copy/encode]

   **Command used:**
   ```bash
   [ffmpeg command]
   ```
   ```

9. **Skip to Step 9 (Quality Checks)**

### Step 2b: Multi-Chapter Workflow

For creating multiple clips from chapter timestamps:

(Continue with existing workflow below...)

### Step 3: Gather Required Information (Multi-Chapter Mode)

Check what information is provided. If missing, prompt for:

1. **Video file path**:
   - Ask: "Please provide the full path to your video file (e.g., /Users/name/video.mp4)"
   - Validate file exists using `ls -lh [filepath]`
   - Show file size and confirm with user

2. **Chapter timestamps**:
   - Ask: "Please provide your chapter list with timestamps in this format:
     ```
     00:00:00 - Introduction
     00:05:30 - Main Topic
     00:15:45 - Q&A
     ```
     (Tip: If you have a video transcript, try the Video Transcript Analyzer skill first to generate timestamps)"
   - Wait for user to provide timestamps

3. **Output directory**:
   - Ask: "Where would you like to save the clips? (Press Enter for default: same folder as source video with '_clips' suffix)"
   - Default: `[video_directory]/[video_name]_clips/`

4. **Encoding mode**:
   - Ask: "Choose encoding mode:
     - 'copy' (fast, no re-encode, may have keyframe issues at boundaries)
     - 'encode' (slower, consistent quality, precise cuts)
     Default: copy"

### Step 4: Parse and Validate Timestamps (Multi-Chapter Mode)

1. **Parse timestamp format**:
   ```python
   import re
   from datetime import datetime, timedelta

   def parse_timestamp(ts_str):
       """Convert HH:MM:SS or MM:SS to seconds"""
       parts = ts_str.strip().split(':')
       if len(parts) == 3:  # HH:MM:SS
           h, m, s = map(int, parts)
           return h * 3600 + m * 60 + s
       elif len(parts) == 2:  # MM:SS
           m, s = map(int, parts)
           return m * 60 + s
       else:
           raise ValueError(f"Invalid timestamp format: {ts_str}")

   def parse_chapter_line(line):
       """Parse '00:05:30 - Chapter Name' format"""
       match = re.match(r'(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2})\s*-\s*(.+)', line.strip())
       if match:
           timestamp, name = match.groups()
           return parse_timestamp(timestamp), name.strip()
       return None
   ```

2. **Validate timestamps**:
   - Check all timestamps are in ascending order
   - Warn if any timestamps are out of order
   - Check for duplicate timestamps
   - Ensure first timestamp is 00:00:00 or close to start

3. **Get video duration**:
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 [video_file]
   ```

4. **Calculate end times**:
   - For each chapter, end time = next chapter's start time
   - For last chapter, end time = video duration
   - Validate no chapter extends beyond video duration

### Step 5: Sanitize Filenames (Multi-Chapter Mode)

Create safe filenames from chapter names:
```python
import re

def sanitize_filename(name):
    """Convert chapter name to safe filename"""
    # Remove or replace special characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Replace multiple underscores with single
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Limit length to 100 chars
    if len(name) > 100:
        name = name[:100]
    return name
```

Generate filenames:
- Format: `{number:02d}-{sanitized_name}.{extension}`
- Example: `01-Introduction.mp4`, `02-Main_Topic.mp4`
- Number chapters sequentially starting from 01

### Step 6: Create Output Directory (Multi-Chapter Mode)

```bash
mkdir -p [output_directory]
```

Show user where clips will be saved.

### Step 7: Generate ffmpeg Commands (Multi-Chapter Mode)

**For "copy" mode (fast, no re-encode):**
```bash
ffmpeg -i [input_video] -ss [start_time] -to [end_time] -c copy -avoid_negative_ts 1 "[output_file]"
```

**For "encode" mode (slower, precise):**
```bash
ffmpeg -i [input_video] -ss [start_time] -to [end_time] -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k "[output_file]"
```

**Key parameters:**
- `-ss [start_time]`: Start time in HH:MM:SS format
- `-to [end_time]`: End time in HH:MM:SS format
- `-c copy`: Stream copy (no re-encode)
- `-c:v libx264`: Video codec for encoding
- `-preset medium`: Encoding speed/quality balance
- `-crf 23`: Quality level (18-28, lower is better)
- `-c:a aac`: Audio codec
- `-avoid_negative_ts 1`: Fix timestamp issues in copy mode

### Step 8: Execute Clipping Commands (Multi-Chapter Mode)

1. **Show execution plan**:
   ```
   Creating [N] clips from [video_name]:
   1. [00:00:00 - 00:05:30] → 01-Introduction.mp4
   2. [00:05:30 - 00:15:45] → 02-Main_Topic.mp4
   ...
   ```

2. **Execute commands sequentially**:
   - Run one ffmpeg command at a time
   - Show progress: "Creating clip 1 of N..."
   - Capture any errors or warnings
   - Validate each output file was created and has size > 0

3. **For parallel execution** (optional, if user wants speed):
   - Can run multiple ffmpeg commands in background
   - Monitor all processes
   - Wait for all to complete before reporting
   - Only use if system has multiple cores and user approves

### Step 9: Verify and Report Results (Both Modes)

1. **Check each output file**:
   ```bash
   ls -lh [output_directory]/*.mp4
   ```

2. **Get clip durations**:
   ```bash
   for file in [output_directory]/*.mp4; do
     ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file"
   done
   ```

3. **Generate summary report**:
   ```markdown
   # Video Clipping Complete

   ## Source Video
   - File: [path]
   - Duration: [HH:MM:SS]
   - Size: [size]

   ## Created Clips

   | # | Clip Name | Duration | Size | Time Range |
   |---|-----------|----------|------|------------|
   | 1 | 01-Introduction.mp4 | 05:30 | 15.2 MB | 00:00:00 - 00:05:30 |
   | 2 | 02-Main_Topic.mp4 | 10:15 | 28.4 MB | 00:05:30 - 00:15:45 |

   ## Summary
   - Total clips created: [N]
   - Total size: [total_size]
   - Output location: [directory]
   - Encoding mode: [copy/encode]

   ## Warnings/Errors
   [List any issues encountered]

   ## Commands Used
   ```bash
   [Show all ffmpeg commands for reference]
   ```
   ```

### Step 10: Quality Checks (Both Modes)

Before finalizing:
- [ ] All expected clip files exist
- [ ] Each file has size > 0 bytes
- [ ] Clip durations match expected ranges (within 1-2 seconds)
- [ ] Filenames are properly sanitized (no special characters) [Multi-chapter only]
- [ ] No ffmpeg errors in output
- [ ] Summary report shows all clips

If using "copy" mode, warn user:
> Note: Copy mode may result in clips that don't start exactly at the specified timestamp due to keyframe positions. If precise cuts are needed, re-run with "encode" mode.

### Error Handling

**Common errors and solutions:**

1. **ffmpeg not found**:
   - Error: `command not found: ffmpeg`
   - Solution: Provide installation instructions

2. **Invalid timestamp**:
   - Error: Timestamp parsing fails
   - Solution: Show expected format, ask user to correct

3. **Timestamp beyond video duration**:
   - Error: End time > video length
   - Solution: Adjust last chapter to end at video duration

4. **File not found**:
   - Error: Input video doesn't exist
   - Solution: Ask user to verify path, suggest using tab completion

5. **Permission denied**:
   - Error: Cannot write to output directory
   - Solution: Check directory permissions, suggest alternative location

6. **Codec errors in copy mode**:
   - Error: "Non-monotonous DTS in output stream"
   - Solution: Re-run with encode mode or add `-avoid_negative_ts 1`

7. **Overlapping timestamps**:
   - Error: Timestamps out of order
   - Solution: Sort timestamps, ask user to confirm order

## Examples

### Example 1: Single Snippet from Time Range

**User says:** "Create a clip from 55s to 2m35s"
**User provides:** `/Users/alice/videos/customer-call.mp4`

**Workflow:**
1. Validate ffmpeg installed ✓
2. Detect Single Snippet Mode (time range provided)
3. Parse time range: 55s = 55 seconds, 2m35s = 155 seconds
4. Convert to HH:MM:SS: 00:00:55 to 00:02:35
5. Suggest filename: `customer-call_00-55_02-35.mp4`
6. User accepts default filename
7. Ask encoding preference: user chooses "copy"
8. Generate ffmpeg command:
   ```bash
   ffmpeg -i /Users/alice/videos/customer-call.mp4 -ss 00:00:55 -to 00:02:35 -c copy -avoid_negative_ts 1 "customer-call_00-55_02-35.mp4"
   ```
9. Execute command
10. Report results:
    ```
    # Video Clip Created

    **Source:** /Users/alice/videos/customer-call.mp4
    **Time Range:** 00:00:55 to 00:02:35 (1m 40s)
    **Output:** /Users/alice/videos/customer-call_00-55_02-35.mp4
    **Size:** 8.2 MB
    **Encoding:** copy
    ```

**Output file:**
```
/Users/alice/videos/customer-call_00-55_02-35.mp4 (8.2 MB, 1m 40s)
```

### Example 2: Basic Usage with SRT Timestamps (Multi-Chapter)

**User provides:**
```
Video: /Users/alice/videos/customer-call.mp4
Chapters:
00:00:00 - Introduction
00:02:57 - Memberships & Registration
00:09:41 - Lists vs Views
00:15:30 - API Limitations
```

**Workflow:**
1. Validate ffmpeg installed
2. Check video file exists (352 MB, 18:45 duration)
3. Parse 4 chapters with timestamps
4. Ask for encoding preference (user chooses "copy")
5. Create output directory: `/Users/alice/videos/customer-call_clips/`
6. Generate 4 ffmpeg commands
7. Execute sequentially
8. Verify all 4 clips created

**Output files:**
```
/Users/alice/videos/customer-call_clips/
  01-Introduction.mp4 (15.2 MB, 02:57)
  02-Memberships_Registration.mp4 (28.4 MB, 06:44)
  03-Lists_vs_Views.mp4 (24.1 MB, 05:49)
  04-API_Limitations.mp4 (12.8 MB, 03:15)
```

### Example 3: From Video Transcript Analyzer Output (Multi-Chapter)

**User says:** "I just ran Video Transcript Analyzer on my interview. Can you create clips from those chapters?"

**Workflow:**
1. Ask user: "Please share the video file path and the chapter timestamps from the analysis"
2. User provides video path and copies the "Topical Breakdown" section timestamps
3. Parse timestamps:
   ```
   00:02:57 - Memberships & Registration Management
   00:09:41 - Lists vs Views Disconnect
   00:15:30 - API Limitations
   00:20:15 - Workflow Automation Issues
   ```
4. Get video duration: 25:42
5. Calculate last chapter ends at 25:42
6. Ask encoding preference (user chooses "encode" for precise cuts)
7. Create clips with re-encoding
8. Report: 4 clips created, 156 MB total

### Example 4: Simple Timestamps - MM:SS format (Multi-Chapter)

**User provides:**
```
Video: /home/user/videos/tutorial.mp4
Chapters:
0:00 - Intro
5:30 - Setup
12:45 - Demo
18:20 - Q&A
```

**Workflow:**
1. Parse MM:SS format timestamps (convert to seconds)
2. Validate video is 22:15 long
3. Calculate end times:
   - Intro: 0:00 - 5:30
   - Setup: 5:30 - 12:45
   - Demo: 12:45 - 18:20
   - Q&A: 18:20 - 22:15
4. Create 4 clips in encode mode (user requested precise cuts)
5. Success: All clips created

## Testing Checklist

- [ ] ffmpeg detection works correctly
- [ ] Handles both HH:MM:SS and MM:SS timestamp formats
- [ ] Validates timestamps are in ascending order
- [ ] Correctly calculates end times from next chapter start
- [ ] Last chapter uses video duration as end time
- [ ] Sanitizes filenames (removes special chars, replaces spaces)
- [ ] Creates output directory if it doesn't exist
- [ ] Both "copy" and "encode" modes work
- [ ] Generates proper ffmpeg commands
- [ ] Verifies all output files created
- [ ] Reports file sizes and durations accurately
- [ ] Handles errors gracefully (missing video, invalid timestamps)
- [ ] Warns about copy mode keyframe limitations
- [ ] Provides summary report with all details

## Security and Privacy

**File Access:**
- Only reads user-specified video file
- Only writes to user-specified output directory
- Does not modify source video file
- Validates all paths before execution

**Command Execution:**
- All ffmpeg commands shown to user before execution
- No arbitrary command injection
- Filenames sanitized to prevent shell injection
- Uses absolute paths to prevent directory traversal

**Privacy:**
- Video content never sent to external services
- All processing done locally with ffmpeg
- Chapter names may contain sensitive info - handle appropriately
- Output files remain in user's filesystem

## Resources

See `resources/` folder for:
- **EXAMPLES.md**: Detailed examples with full input/output
- **REFERENCE.md**: ffmpeg command reference, timestamp formats, troubleshooting guide
- **README.md**: User-facing documentation

## Related Skills (Workflow Chain)

This skill is part of the **video processing workflow**:

```
┌─────────────────────┐
│   wistia-uploader   │  → Upload video, get transcript
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  video-transcript-analyzer  │  → Analyze transcript, get timestamps
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────┐
│    video-clipper    │  ← YOU ARE HERE
│   (create clips)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   wistia-uploader   │  → (Optional) Upload clips to Wistia
└─────────────────────┘
```

**Preceding skill:** `video-transcript-analyzer` - Use this first to generate chapter timestamps from a transcript

**Following skill:** `wistia-uploader` - Optionally upload the created clips to Wistia for hosting
