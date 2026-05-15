#!/usr/bin/env python3
"""
rt_extract — Extract frames from video files for reverse tracing.

Uses ffmpeg to extract keyframes or frames at specific timestamps.
Outputs image files to a directory for downstream analysis.

Usage:
    rt_extract.py video.mp4 --timestamps 0:30 1:15 2:00
    rt_extract.py video.mp4 --keyframes --max 5
    rt_extract.py video.mp4 --interval 10  # every 10 seconds
    rt_extract.py video.mp4 --keyframes --output-dir ./frames

Requires: ffmpeg
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def get_duration(video_path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", video_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def extract_at_timestamps(video_path: str, timestamps: list[str], output_dir: str) -> list[str]:
    outputs = []
    for i, ts in enumerate(timestamps):
        out_path = os.path.join(output_dir, f"frame_{i:04d}_{ts.replace(':', '-')}.jpg")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", ts, "-i", video_path, "-frames:v", "1", "-q:v", "2", out_path],
            capture_output=True, text=True
        )
        if os.path.exists(out_path):
            outputs.append(out_path)
    return outputs


def extract_keyframes(video_path: str, output_dir: str, max_frames: int = 10) -> list[str]:
    pattern = os.path.join(output_dir, "keyframe_%04d.jpg")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", f"select=eq(pict_type\\,I)",
            "-vsync", "vfr", "-q:v", "2",
            "-frames:v", str(max_frames),
            pattern
        ],
        capture_output=True, text=True
    )
    outputs = sorted(
        [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("keyframe_")]
    )
    return outputs


def extract_interval(video_path: str, output_dir: str, interval: float, max_frames: int = 20) -> list[str]:
    duration = get_duration(video_path)
    timestamps = []
    t = 0.0
    while t < duration and len(timestamps) < max_frames:
        m, s = divmod(int(t), 60)
        h, m = divmod(m, 60)
        timestamps.append(f"{h}:{m:02d}:{s:02d}")
        t += interval
    return extract_at_timestamps(video_path, timestamps, output_dir)


def main():
    parser = argparse.ArgumentParser(description="Extract frames from video for reverse tracing")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--timestamps", nargs="+", help="Specific timestamps to extract (e.g. 0:30 1:15)")
    parser.add_argument("--keyframes", action="store_true", help="Extract I-frames (keyframes)")
    parser.add_argument("--interval", type=float, help="Extract a frame every N seconds")
    parser.add_argument("--max", type=int, default=10, help="Maximum number of frames to extract (default: 10)")
    parser.add_argument("--output-dir", help="Output directory (default: temp directory)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"Error: {args.video} not found", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or tempfile.mkdtemp(prefix="rt_frames_")
    os.makedirs(output_dir, exist_ok=True)

    if not args.timestamps and not args.keyframes and not args.interval:
        args.keyframes = True

    frames = []
    if args.timestamps:
        frames = extract_at_timestamps(args.video, args.timestamps, output_dir)
    elif args.keyframes:
        frames = extract_keyframes(args.video, output_dir, args.max)
    elif args.interval:
        frames = extract_interval(args.video, output_dir, args.interval, args.max)

    if args.json:
        print(json.dumps({"video": args.video, "output_dir": output_dir, "frames": frames, "count": len(frames)}, indent=2))
    else:
        print(f"Extracted {len(frames)} frames to {output_dir}")
        for f in frames:
            print(f"  {f}")


if __name__ == "__main__":
    main()
