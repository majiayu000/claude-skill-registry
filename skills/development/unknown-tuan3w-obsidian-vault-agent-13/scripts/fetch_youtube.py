#!/usr/bin/env python3
# /// script
# dependencies = ["youtube-transcript-api>=1.0.0"]
# requires-python = ">=3.10"
# ///
"""
Fetch YouTube video transcript and metadata.

Uses youtube-transcript-api for transcript and yt-dlp for rich metadata.
Falls back to YouTube oEmbed API if yt-dlp unavailable.

Usage:
    uv run fetch_youtube.py "VIDEO_URL_OR_ID" [--lang en]

Output: JSON to stdout with title, channel, duration, transcript, etc.
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or plain ID."""
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    patterns = [
        r'(?:v=|/v/)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    print(f"ERROR: Could not extract video ID from: {url_or_id}", file=sys.stderr)
    sys.exit(1)


def get_metadata_ytdlp(video_id: str) -> dict | None:
    """Get rich metadata via yt-dlp --dump-json (preferred)."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        result = subprocess.run(
            ["yt-dlp", "--no-update", "--dump-json", "--skip-download", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"yt-dlp failed: {result.stderr[:200]}", file=sys.stderr)
            return None

        data = json.loads(result.stdout)
        duration_secs = data.get("duration", 0)
        hours, remainder = divmod(int(duration_secs), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            duration_fmt = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_fmt = f"{minutes}:{seconds:02d}"

        # Extract chapters if available
        chapters = []
        for ch in data.get("chapters", []) or []:
            chapters.append({
                "title": ch.get("title", ""),
                "start_time": ch.get("start_time", 0),
            })

        return {
            "title": data.get("title", ""),
            "channel": data.get("channel", data.get("uploader", "")),
            "channel_url": data.get("channel_url", data.get("uploader_url", "")),
            "upload_date": data.get("upload_date", ""),  # YYYYMMDD
            "duration": duration_fmt,
            "duration_seconds": duration_secs,
            "description": data.get("description", ""),
            "tags": data.get("tags", []),
            "categories": data.get("categories", []),
            "view_count": data.get("view_count", 0),
            "chapters": chapters,
            "source": "yt-dlp",
        }
    except FileNotFoundError:
        print("yt-dlp not found, falling back to oEmbed", file=sys.stderr)
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"yt-dlp error: {e}", file=sys.stderr)
        return None


def get_metadata_oembed(video_id: str) -> dict:
    """Fallback: get basic metadata via YouTube oEmbed API."""
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(video_url, safe='')}&format=json"
    req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "title": data.get("title", ""),
                "channel": data.get("author_name", ""),
                "channel_url": data.get("author_url", ""),
                "upload_date": "",
                "duration": "",
                "duration_seconds": 0,
                "description": "",
                "tags": [],
                "categories": [],
                "view_count": 0,
                "chapters": [],
                "source": "oembed",
            }
    except Exception as e:
        print(f"oEmbed error: {e}", file=sys.stderr)
        return {
            "title": "", "channel": "", "channel_url": "", "upload_date": "",
            "duration": "", "duration_seconds": 0, "description": "",
            "tags": [], "categories": [], "view_count": 0, "chapters": [],
            "source": "none",
        }


def get_transcript(video_id: str, lang: str = "en") -> dict:
    """Fetch transcript via youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("ERROR: youtube-transcript-api not installed", file=sys.stderr)
        sys.exit(1)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=[lang])

        segments = []
        full_text_parts = []
        for entry in transcript.snippets:
            segments.append({
                "start": round(entry.start, 1),
                "duration": round(entry.duration, 1),
                "text": entry.text,
            })
            full_text_parts.append(entry.text)

        return {
            "segments": segments,
            "full_text": " ".join(full_text_parts),
            "language": lang,
            "is_auto_generated": False,
            "error": None,
        }
    except Exception as e:
        error_name = type(e).__name__
        # Try auto-generated captions as fallback
        if "NoTranscriptFound" in error_name or "TranscriptNotAvailable" in error_name:
            try:
                transcript_list = ytt_api.list(video_id)
                # Try to find any available transcript
                for t in transcript_list:
                    try:
                        transcript = ytt_api.fetch(video_id, languages=[t.language_code])
                        segments = []
                        full_text_parts = []
                        for entry in transcript.snippets:
                            segments.append({
                                "start": round(entry.start, 1),
                                "duration": round(entry.duration, 1),
                                "text": entry.text,
                            })
                            full_text_parts.append(entry.text)

                        return {
                            "segments": segments,
                            "full_text": " ".join(full_text_parts),
                            "language": t.language_code,
                            "is_auto_generated": t.is_generated,
                            "error": None,
                        }
                    except Exception:
                        continue
            except Exception:
                pass

        return {
            "segments": [],
            "full_text": "",
            "language": lang,
            "is_auto_generated": False,
            "error": f"{error_name}: {str(e)[:200]}",
        }


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video data")
    parser.add_argument("video", help="YouTube URL or video ID")
    parser.add_argument("--lang", default="en", help="Preferred transcript language (default: en)")
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"Fetching metadata for {video_id}...", file=sys.stderr)

    # Try yt-dlp first, fall back to oEmbed
    metadata = get_metadata_ytdlp(video_id)
    if metadata is None:
        metadata = get_metadata_oembed(video_id)

    print(f"Fetching transcript for {video_id}...", file=sys.stderr)
    transcript = get_transcript(video_id, args.lang)

    result = {
        "video_id": video_id,
        "video_url": video_url,
        **metadata,
        "transcript": transcript,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
