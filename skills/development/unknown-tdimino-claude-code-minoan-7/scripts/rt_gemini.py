#!/usr/bin/env python3
"""
rt_gemini — Gemini multimodal image identification.

Sends an image to Gemini with a structured identification prompt.
Good for identifying TV shows, movies, characters, locations, art,
and other visual media from training data knowledge.

Usage:
    rt_gemini.py image.jpg
    rt_gemini.py image.jpg --question "What movie is this from?"
    rt_gemini.py image.jpg --model gemini-2.5-flash
    rt_gemini.py image.jpg --json

Requires: GOOGLE_API_KEY or GEMINI_API_KEY env var
Install:  pip install google-genai
"""

import argparse
import json
import os
import sys
from pathlib import Path


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

DEFAULT_PROMPT = """Analyze this image and identify its source. Provide your answer as structured JSON with these fields:

- "media_type": one of "tv_show", "movie", "photograph", "artwork", "screenshot", "meme", "stock_photo", "unknown"
- "title": the name of the show, movie, or work (null if unknown)
- "season": season number if TV (null otherwise)
- "episode": episode number or name if TV (null otherwise)
- "characters": list of character names visible (empty list if none recognized)
- "actors": list of actor names visible (empty list if none recognized)
- "location": described location or setting
- "year": estimated year of production or capture
- "confidence": your confidence level as "high", "medium", or "low"
- "reasoning": one sentence explaining your identification

Return ONLY valid JSON, no markdown fences or extra text."""


def identify_image(image_path: str, question: str | None = None, model_name: str = "gemini-2.5-flash") -> dict:
    from google import genai

    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=GOOGLE_API_KEY)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    mime = "image/jpeg"
    ext = Path(image_path).suffix.lower()
    if ext == ".png":
        mime = "image/png"
    elif ext == ".webp":
        mime = "image/webp"
    elif ext == ".gif":
        mime = "image/gif"

    image_part = genai.types.Part.from_bytes(data=image_bytes, mime_type=mime)
    prompt = question or DEFAULT_PROMPT

    response = client.models.generate_content(model=model_name, contents=[prompt, image_part])
    text = response.text.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    result = {
        "source": image_path,
        "engine": "gemini",
        "model": model_name,
    }

    try:
        parsed = json.loads(text)
        result["identification"] = parsed
    except json.JSONDecodeError:
        result["raw_response"] = text

    return result


def format_text(result: dict) -> str:
    lines = [f"Source: {result['source']}", f"Model: {result['model']}", ""]

    ident = result.get("identification")
    if ident:
        if ident.get("title"):
            media = ident.get("media_type", "").replace("_", " ").title()
            lines.append(f"Identified: {ident['title']} ({media})")
            if ident.get("season") and ident.get("episode"):
                lines.append(f"  Season {ident['season']}, Episode {ident['episode']}")
            if ident.get("year"):
                lines.append(f"  Year: {ident['year']}")
        else:
            lines.append("Could not identify specific media")

        if ident.get("characters"):
            lines.append(f"  Characters: {', '.join(ident['characters'])}")
        if ident.get("actors"):
            lines.append(f"  Actors: {', '.join(ident['actors'])}")
        if ident.get("location"):
            lines.append(f"  Location: {ident['location']}")
        if ident.get("confidence"):
            lines.append(f"  Confidence: {ident['confidence']}")
        if ident.get("reasoning"):
            lines.append(f"  Reasoning: {ident['reasoning']}")
    elif result.get("raw_response"):
        lines.append("Response:")
        lines.append(f"  {result['raw_response'][:500]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Gemini multimodal image identification")
    parser.add_argument("image", help="Image file path")
    parser.add_argument("--question", help="Custom question (default: structured identification prompt)")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model (default: gemini-2.5-flash)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)

    try:
        result = identify_image(args.image, args.question, args.model)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
