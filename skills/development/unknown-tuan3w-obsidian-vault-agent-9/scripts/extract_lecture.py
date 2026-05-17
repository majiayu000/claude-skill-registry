#!/usr/bin/env python3
# /// script
# dependencies = ["mlx-whisper"]
# requires-python = ">=3.10"
# ///
"""
Extract transcript and key frames from a local video file.

Uses ffmpeg for audio extraction and frame capture,
mlx-whisper for speech-to-text transcription (Apple Silicon optimized).

Usage:
    uv run extract_lecture.py "/path/to/video.mp4" --output-dir /tmp/lecture-extract

Output: JSON to stdout with transcript and frame paths.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile


def get_video_info(video_path: str) -> dict:
    """Get video metadata via ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", video_path,
            ],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(result.stdout)
        duration = float(data.get("format", {}).get("duration", 0))
        video_stream = next(
            (s for s in data.get("streams", []) if s["codec_type"] == "video"), {}
        )
        return {
            "duration_seconds": duration,
            "width": video_stream.get("width", 0),
            "height": video_stream.get("height", 0),
            "codec": video_stream.get("codec_name", ""),
        }
    except Exception as e:
        print(f"ffprobe error: {e}", file=sys.stderr)
        return {"duration_seconds": 0, "width": 0, "height": 0, "codec": ""}


def format_duration(seconds: float) -> str:
    """Format seconds as H:MM:SS or M:SS."""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def extract_audio(video_path: str, output_dir: str) -> str:
    """Extract audio as 16kHz mono WAV for whisper."""
    audio_path = os.path.join(output_dir, "audio.wav")
    print("Extracting audio...", file=sys.stderr)
    subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            audio_path, "-y",
        ],
        capture_output=True, timeout=300,
    )
    return audio_path


def transcribe(audio_path: str) -> dict:
    """Transcribe audio using mlx-whisper."""
    print("Transcribing with mlx-whisper (this may take a few minutes)...", file=sys.stderr)
    try:
        import mlx_whisper
        result = mlx_whisper.transcribe(
            audio_path,
            path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
            language="vi",
        )
        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": round(seg["start"], 1),
                "end": round(seg["end"], 1),
                "text": seg["text"].strip(),
            })

        return {
            "full_text": result.get("text", "").strip(),
            "segments": segments,
            "language": result.get("language", "vi"),
            "error": None,
        }
    except ImportError:
        return {
            "full_text": "",
            "segments": [],
            "language": "vi",
            "error": "mlx-whisper not installed. Run: pip3 install --break-system-packages mlx-whisper",
        }
    except Exception as e:
        return {
            "full_text": "",
            "segments": [],
            "language": "vi",
            "error": f"{type(e).__name__}: {str(e)[:300]}",
        }


def extract_frames(video_path: str, output_dir: str, duration: float, interval: int = 120) -> list[str]:
    """Extract one frame every `interval` seconds. Returns list of frame paths."""
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    timestamps = []
    t = 10  # skip first 10 seconds (usually intro/loading)
    while t < duration - 5:
        timestamps.append(t)
        t += interval

    # Ensure we get at least a few frames for short videos
    if len(timestamps) < 3 and duration > 30:
        timestamps = [10, duration * 0.33, duration * 0.66]

    frames = []
    print(f"Extracting {len(timestamps)} frames...", file=sys.stderr)
    for i, ts in enumerate(timestamps):
        h, rem = divmod(int(ts), 3600)
        m, s = divmod(rem, 60)
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        display_time = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        frame_path = os.path.join(frames_dir, f"frame-{i+1:02d}.jpg")
        subprocess.run(
            [
                "ffmpeg", "-ss", time_str, "-i", video_path,
                "-frames:v", "1", "-q:v", "2",
                frame_path, "-y",
            ],
            capture_output=True, timeout=30,
        )
        if os.path.exists(frame_path):
            frames.append({
                "path": frame_path,
                "timestamp_seconds": ts,
                "timestamp": display_time,
            })

    return frames


def deduplicate_frames(frames: list[dict], max_frames: int = 10) -> list[dict]:
    """Remove near-duplicate frames by comparing file sizes as a simple heuristic."""
    if len(frames) <= max_frames:
        return frames

    # Use file size as a rough proxy for visual similarity
    sized = [(f, os.path.getsize(f["path"])) for f in frames]

    # Always keep first and last
    selected = [sized[0]]
    for i in range(1, len(sized)):
        prev_size = selected[-1][1]
        curr_size = sized[i][1]
        # Skip if size is very similar to previous (likely same slide)
        ratio = min(prev_size, curr_size) / max(prev_size, curr_size) if max(prev_size, curr_size) > 0 else 1
        if ratio < 0.92:  # at least 8% difference
            selected.append(sized[i])

    # If still too many, sample evenly
    if len(selected) > max_frames:
        step = len(selected) / max_frames
        selected = [selected[int(i * step)] for i in range(max_frames)]

    return [f for f, _ in selected]


def main():
    parser = argparse.ArgumentParser(description="Extract lecture content from video")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: auto temp dir)")
    parser.add_argument("--frame-interval", type=int, default=120, help="Seconds between frame captures (default: 120)")
    parser.add_argument("--max-frames", type=int, default=10, help="Maximum frames to keep (default: 10)")
    parser.add_argument("--skip-transcribe", action="store_true", help="Skip transcription (for testing)")
    args = parser.parse_args()

    video_path = os.path.abspath(args.video)
    if not os.path.exists(video_path):
        print(f"ERROR: File not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    if args.output_dir:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)
    else:
        video_hash = hashlib.md5(video_path.encode()).hexdigest()[:8]
        output_dir = os.path.join(tempfile.gettempdir(), f"lecture-{video_hash}")
        os.makedirs(output_dir, exist_ok=True)

    # Get video info
    info = get_video_info(video_path)
    duration = info["duration_seconds"]
    print(f"Video: {format_duration(duration)}, {info['width']}x{info['height']}", file=sys.stderr)

    # Extract audio and transcribe
    if args.skip_transcribe:
        transcript = {"full_text": "", "segments": [], "language": "vi", "error": "skipped"}
    else:
        audio_path = extract_audio(video_path, output_dir)
        transcript = transcribe(audio_path)
        # Clean up audio file to save space
        try:
            os.remove(audio_path)
        except OSError:
            pass

    # Extract and deduplicate frames
    all_frames = extract_frames(video_path, output_dir, duration, args.frame_interval)
    selected_frames = deduplicate_frames(all_frames, args.max_frames)

    # Remove unselected frames
    selected_paths = {f["path"] for f in selected_frames}
    for f in all_frames:
        if f["path"] not in selected_paths:
            try:
                os.remove(f["path"])
            except OSError:
                pass

    result = {
        "video_path": video_path,
        "filename": os.path.basename(video_path),
        "duration": format_duration(duration),
        "duration_seconds": duration,
        "width": info["width"],
        "height": info["height"],
        "output_dir": output_dir,
        "transcript": transcript,
        "frames": selected_frames,
        "frame_count": len(selected_frames),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
