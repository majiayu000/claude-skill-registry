#!/usr/bin/env python3
"""
rt_vision — Google Cloud Vision Web Detection for reverse image tracing.

The highest-signal reverse image search API available. Returns web entities
(e.g. "Breaking Bad S5E14"), pages containing the image, visually similar
images, and best-guess labels.

Usage:
    rt_vision.py image.jpg
    rt_vision.py image.jpg --max-results 20 --include-geo
    rt_vision.py https://example.com/image.jpg
    rt_vision.py image.jpg --json

Requires: GOOGLE_APPLICATION_CREDENTIALS env var (service account JSON path)
          or Application Default Credentials via `gcloud auth application-default login`
Install:  pip install google-cloud-vision
"""

import argparse
import json
import os
import sys
from pathlib import Path


def detect_web(image_source: str, max_results: int = 10, include_geo: bool = False) -> dict:
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.Image()

    if image_source.startswith(("http://", "https://")):
        image.source = vision.ImageSource(image_uri=image_source)
    else:
        with open(image_source, "rb") as f:
            image.content = f.read()

    web_params = vision.WebDetectionParams(include_geo_results=include_geo)
    image_context = vision.ImageContext(web_detection_params=web_params)

    response = client.web_detection(
        image=image,
        image_context=image_context,
        max_results=max_results,
    )

    if response.error.message:
        raise RuntimeError(f"Vision API error: {response.error.message}")

    web = response.web_detection
    result = {
        "source": image_source,
        "engine": "vision",
        "web_entities": [],
        "best_guess_labels": [],
        "pages_with_matching_images": [],
        "full_matching_images": [],
        "partial_matching_images": [],
        "visually_similar_images": [],
    }

    for entity in web.web_entities:
        result["web_entities"].append({
            "entity_id": entity.entity_id,
            "description": entity.description,
            "score": round(entity.score, 4),
        })

    for label in web.best_guess_labels:
        result["best_guess_labels"].append(label.label)

    for page in web.pages_with_matching_images:
        page_info = {"url": page.url, "title": page.page_title}
        if page.full_matching_images:
            page_info["full_matches"] = [img.url for img in page.full_matching_images]
        if page.partial_matching_images:
            page_info["partial_matches"] = [img.url for img in page.partial_matching_images]
        result["pages_with_matching_images"].append(page_info)

    for img in web.full_matching_images:
        result["full_matching_images"].append(img.url)

    for img in web.partial_matching_images:
        result["partial_matching_images"].append(img.url)

    for img in web.visually_similar_images:
        result["visually_similar_images"].append(img.url)

    return result


def format_text(result: dict) -> str:
    lines = [f"Source: {result['source']}", ""]

    if result["best_guess_labels"]:
        lines.append(f"Best guess: {', '.join(result['best_guess_labels'])}")
        lines.append("")

    if result["web_entities"]:
        lines.append("Web Entities:")
        for e in result["web_entities"][:15]:
            desc = e["description"] or "(unnamed)"
            lines.append(f"  [{e['score']:.2f}] {desc} ({e['entity_id']})")
        lines.append("")

    if result["pages_with_matching_images"]:
        lines.append(f"Pages with matches ({len(result['pages_with_matching_images'])}):")
        for p in result["pages_with_matching_images"][:10]:
            lines.append(f"  {p['title']}")
            lines.append(f"    {p['url']}")
        lines.append("")

    if result["visually_similar_images"]:
        lines.append(f"Visually similar ({len(result['visually_similar_images'])}):")
        for url in result["visually_similar_images"][:5]:
            lines.append(f"  {url}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Google Cloud Vision Web Detection")
    parser.add_argument("image", help="Image file path or URL")
    parser.add_argument("--max-results", type=int, default=10, help="Max results per category (default: 10)")
    parser.add_argument("--include-geo", action="store_true", help="Include geo results in web detection")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if not args.image.startswith(("http://", "https://")) and not os.path.exists(args.image):
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)

    try:
        result = detect_web(args.image, args.max_results, args.include_geo)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
