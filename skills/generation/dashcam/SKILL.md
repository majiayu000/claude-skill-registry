---
name: dashcam-frame-extraction
description: GPU-accelerated frame extraction for Movie_F dashcam videos. This skill should be used when the user needs to extract frames from Movie_F category dashcam videos placed in the Desktop CARDV folder. Extracts 3 frames per video (BEGIN, MIDDLE, END) using NVIDIA CUDA acceleration with automatic gap analysis, parallel processing, and strict error handling. This is specifically designed for Movie_F category only.
---

# Dashcam Frame Extraction Skill

## Purpose

This skill provides automated GPU-accelerated frame extraction for Movie_F dashcam videos. It extracts 3 frames per video (BEGIN at 1s, MIDDLE at 50%, END at duration-1s) using NVIDIA CUDA hardware acceleration, processes videos in parallel batches, and handles HEVC-encoded videos with the critical fixes required for successful extraction.

## When to Use This Skill

Use this skill when:
- User requests frame extraction from Movie_F dashcam videos
- User places new videos in `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/`
- User asks to "extract frames from Movie_F videos" or similar requests
- User needs to process dashcam footage for analysis or sampling

**Important**: This skill is specifically for **Movie_F category only**. Do not use for Park_F, Park_R, or other categories.

## Quick Start

To extract frames from Movie_F videos:

```bash
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam/scripts
bash run_extraction.sh
```

The script will:
1. Verify system requirements (GPU, disk space, FFmpeg)
2. Identify new videos needing extraction via gap analysis
3. Create batches of 50 videos each
4. Launch 4 parallel GPU workers
5. Monitor progress with updates every 30 seconds
6. Extract 3 frames per video to Google Drive

## How to Use This Skill

### Step 1: Read Agent Instructions (First Time)

For the first use or to understand the complete workflow, read the agent instructions:

```bash
cat references/AGENT_INSTRUCTIONS.md
```

This provides comprehensive guidance on:
- Your role as the extraction agent
- Expected workflow and user interaction
- Troubleshooting common issues
- Performance expectations
- Error handling

### Step 2: Run the Main Extraction Script

Execute the main orchestration script:

```bash
cd scripts
bash run_extraction.sh
```

This script handles the entire pipeline automatically:
- Pre-flight checks (GPU, FFmpeg, Python, disk space)
- Gap analysis (compares source videos vs existing frames)
- Batch creation (splits videos into batches of 50)
- Coordinator launch (manages parallel workers)
- Progress monitoring (displays updates every 30 seconds)

### Step 3: Monitor Progress

Progress updates appear automatically every 30 seconds showing:
- Videos processed / Total
- Batches completed
- Active workers
- Processing speed (videos/min)
- GPU utilization
- Estimated time remaining

Example output:
```
════════════════════════════════════════════════════════════════
📊 EXTRACTION PROGRESS - 02:15:30 PM
Videos: 45/150 (30%) | Batches: 1/3 | Workers: 4
Speed: 18.5 vids/min | 55.5 fps | ETA: 0.2h | GPU: 85%
════════════════════════════════════════════════════════════════
```

### Step 4: Verify Results

After completion, check extraction results:

```bash
bash scripts/show_results.sh
```

This displays:
- Baseline frame count
- Current frame count
- New frames extracted
- Videos processed
- Success rate

### Step 5: Verify Skill Health (Optional)

To verify the skill is properly configured and ready to use:

```bash
bash scripts/verify_skill.sh
```

This checks:
- All required files present
- Scripts are executable
- System requirements (GPU, FFmpeg, Python, disk space)
- Source and output directories accessible

## Core Scripts

The skill includes these executable scripts in `scripts/`:

### Main Scripts

1. **run_extraction.sh** - Main orchestration script
   - Entry point for frame extraction
   - Handles pre-flight checks
   - Performs gap analysis
   - Creates batches
   - Launches coordinator and monitor

2. **extract_frames_worker.py** - GPU worker process
   - Processes individual video batches
   - Uses CUDA for GPU-accelerated decoding
   - Extracts 3 frames per video
   - Critical HEVC fix applied (no CUDA output format)
   - Handles timeouts (30 seconds per frame)

3. **coordinator.sh** - Parallel batch coordinator
   - Manages 4 parallel workers
   - Monitors disk space (25GB minimum)
   - Handles worker lifecycle
   - Strict error handling (exits on any failure)

4. **monitor.sh** - Progress monitoring
   - Displays progress updates every 30 seconds
   - Calculates processing speed and ETA
   - Shows GPU utilization
   - Non-intrusive (doesn't clear screen)

### Utility Scripts

5. **show_results.sh** - Display extraction results
   - Shows baseline vs current frame counts
   - Calculates videos processed
   - Displays success rate

6. **verify_skill.sh** - Skill verification
   - Checks all documentation files present
   - Verifies scripts are executable
   - Tests system requirements
   - Validates configured paths

7. **auto_extract_movie_f.sh** - Legacy script
   - Original all-in-one script (kept for reference)
   - Use `run_extraction.sh` instead

## Reference Documentation

The skill includes comprehensive documentation in `references/`:

### For Agents

- **AGENT_INSTRUCTIONS.md** - Complete agent guide with responsibilities, troubleshooting, and workflow
- **START_HERE.md** - Quick start entry point for agents

### Technical Documentation

- **DOCUMENTATION.md** - Complete technical details, architecture, and fixes
- **CRITICAL_FIXES_CHECKLIST.md** - Pre-flight verification and troubleshooting guide
- **QUICK_REFERENCE.md** - One-page command reference

### Overview

- **SKILL_README.md** - Skill overview and features
- **README.md** - Project background and history
- **INDEX.md** - File navigation and directory structure

### Configuration

- **config.json** - All settings, paths, and parameters
- **requirements.txt** - System dependencies and requirements

## Critical Knowledge

### 1. HEVC CUDA Compatibility Fix

**Problem**: Videos are HEVC (H.265) encoded. Using `-hwaccel_output_format cuda` breaks JPEG conversion.

**Solution**: The worker script uses `-hwaccel cuda` for decoding ONLY, not output format.

**Location**: `scripts/extract_frames_worker.py` lines 46-48

**Impact**: Without this fix, 0% of videos will succeed.

### 2. Strict Error Handling

**Configuration**: Pipeline exits immediately on ANY failure.

**Coordinator**: Uses `set -euo pipefail` (strict mode)

**Worker**: Returns exit code 1 if any videos fail

**Why**: All videos must succeed. If any fail, investigate before continuing.

### 3. Filename Pattern Variations

Videos have inconsistent naming:
- `20250916042109_062060A.MP4`
- `20250916042109_062060_A.MP4`
- `20250916042109_062060.MP4`

**Solution**: Gap analysis checks all variations automatically.

### 4. Timeout Management

Each frame extraction has a 30-second timeout. Videos that timeout are marked as failed and stop the pipeline.

**Configuration**: `extract_frames_worker.py` line 62

## Configuration Settings

All settings are in `references/config.json`:

```json
{
  "num_workers": 4,          // Parallel GPU workers
  "batch_size": 50,          // Videos per batch
  "min_free_gb": 25,         // Minimum disk space required
  "timeout_seconds": 30      // Timeout per frame extraction
}
```

**Paths**:
- **Source**: `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F`
- **Output**: `/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples`
- **Work Dir**: `/home/yousuf/PROJECTS/PeopleNet/FrameExtraction`
- **Staging**: `/home/yousuf/PROJECTS/PeopleNet/Staging`

## Performance Expectations

- **Speed**: 15-20 videos/minute
- **GPU Utilization**: 60-90%
- **Success Rate**: 100% (stops on any failure)
- **Frames per Video**: 3 (BEGIN, MIDDLE, END)
- **Batch Size**: 50 videos
- **Parallel Workers**: 4

## System Requirements

- NVIDIA GPU with CUDA support
- FFmpeg compiled with CUDA hardware acceleration
- Python 3.7+ (uses standard library only - no pip packages)
- 25GB minimum free disk space
- Linux OS (tested on Ubuntu)

Verify requirements:
```bash
bash scripts/verify_skill.sh
```

## Troubleshooting

### Issue: 0% success rate
**Diagnosis**: HEVC fix not applied
**Solution**: Check `scripts/extract_frames_worker.py` - should NOT have `-hwaccel_output_format cuda`

### Issue: Process exits immediately
**Diagnosis**: Failure in first batch
**Solution**: Check logs in `/home/yousuf/PROJECTS/PeopleNet/FrameExtraction/logs/`, identify failed video, investigate

### Issue: Videos not found
**Diagnosis**: Filename pattern mismatch or wrong directory
**Solution**: Verify videos exist in `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/`

### Issue: Low disk space error
**Diagnosis**: Less than 25GB free space
**Solution**: Free up disk space or increase staging cleanup

For complete troubleshooting, see `references/CRITICAL_FIXES_CHECKLIST.md`

## Workflow Summary

1. **User places videos** in Desktop CARDV/Movie_F folder
2. **Agent invokes skill**: Runs `scripts/run_extraction.sh`
3. **System identifies** new videos via gap analysis
4. **System creates** batches of 50 videos each
5. **System launches** 4 parallel GPU workers
6. **System monitors** progress (updates every 30s)
7. **System extracts** 3 frames per video
8. **Agent reports** completion to user

## Frame Naming Convention

Frames are named: `{video_name}_{position}_{timestamp}ms.jpg`

Example:
```
20250916042109_062060A_BEGIN_001000ms.jpg
20250916042109_062060A_MIDDLE_030450ms.jpg
20250916042109_062060A_END_059900ms.jpg
```

## Emergency Stop

If extraction needs to be stopped:

```bash
# Kill all workers
pkill -f extract_frames_worker

# Kill coordinator
pkill -f coordinator

# Kill monitor
pkill -f monitor

# Clean up staging files
rm -rf /home/yousuf/PROJECTS/PeopleNet/Staging/*
```

## Version Information

- **Version**: 1.0
- **Category**: Movie_F ONLY
- **Status**: Production Ready
- **Last Updated**: 2025-01-14
- **Tested On**: Movie_F (1,426 videos, 85% success rate in initial run)

## Future Enhancements

The skill is designed for expansion:
- Auto-trigger via inotify when videos appear
- Email notifications on completion
- Multi-GPU support
- Retry mechanism for failed videos
- Frame verification (check for corruption)

Keep all scripts as additional features will be added in the near future.
