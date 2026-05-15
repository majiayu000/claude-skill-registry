#!/usr/bin/env python3
"""
rt_geospy — AI geolocation from images via Picarta.

Sends an image to Picarta's geolocation API and returns predicted
geographic coordinates, city, country, and confidence scores.

(Originally targeted GeoSpy, which pivoted to enterprise-only under
the Raven brand in 2026. Picarta provides the same capability with
a free developer tier.)

Usage:
    rt_geospy.py image.jpg
    rt_geospy.py image.jpg --top-k 3
    rt_geospy.py image.jpg --json

Requires: PICARTA_API_KEY env var (get at https://picarta.ai/api)
          Falls back to GEOSPY_API_KEY for backward compatibility.
Install:  pip install picarta
"""

import argparse
import json
import os
import sys


API_KEY = os.environ.get("PICARTA_API_KEY") or os.environ.get("GEOSPY_API_KEY")


def predict_location(image_path: str, top_k: int = 3) -> dict:
    import json as _json
    from picarta import Picarta

    if not API_KEY:
        raise RuntimeError("PICARTA_API_KEY environment variable not set (get one at https://picarta.ai/api)")

    localizer = Picarta(API_KEY)
    raw = localizer.localize(img_path=image_path, top_k=top_k)

    data = _json.loads(raw) if isinstance(raw, str) else raw

    result = {
        "source": image_path,
        "engine": "geospy",
        "predictions": [],
    }

    if "topk_predictions_dict" in data:
        for _rank, pred in sorted(data["topk_predictions_dict"].items(), key=lambda x: int(x[0])):
            addr = pred.get("address", {})
            gps = pred.get("gps", [None, None])
            result["predictions"].append({
                "latitude": gps[0] if len(gps) > 0 else None,
                "longitude": gps[1] if len(gps) > 1 else None,
                "city": addr.get("city"),
                "state": addr.get("province"),
                "country": addr.get("country"),
                "confidence": pred.get("confidence"),
            })
    elif "ai_lat" in data:
        result["predictions"].append({
            "latitude": data.get("ai_lat"),
            "longitude": data.get("ai_lon"),
            "city": data.get("city"),
            "state": data.get("province"),
            "country": data.get("ai_country"),
            "confidence": data.get("ai_confidence"),
        })
    else:
        result["raw"] = data

    if data.get("city") or data.get("province") or data.get("ai_country"):
        result["description"] = ", ".join(
            x for x in [data.get("city"), data.get("province"), data.get("ai_country")] if x
        )

    return result


def format_text(result: dict) -> str:
    lines = [f"Source: {result['source']}", ""]

    predictions = result.get("predictions", [])
    if predictions:
        lines.append(f"Location predictions ({len(predictions)}):")
        for i, p in enumerate(predictions, 1):
            parts = [x for x in [p.get("city"), p.get("state"), p.get("country")] if x]
            location = ", ".join(parts) or "Unknown"
            conf = f" ({p['confidence']:.1%})" if p.get("confidence") else ""
            coords = ""
            if p.get("latitude") is not None and p.get("longitude") is not None:
                coords = f" [{p['latitude']:.4f}, {p['longitude']:.4f}]"
            lines.append(f"  {i}. {location}{conf}{coords}")
    elif result.get("raw"):
        lines.append("Raw response:")
        lines.append(f"  {json.dumps(result['raw'], indent=2)}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI image geolocation via Picarta")
    parser.add_argument("image", help="Image file path")
    parser.add_argument("--top-k", type=int, default=3, help="Number of predictions (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)

    try:
        result = predict_location(args.image, args.top_k)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
