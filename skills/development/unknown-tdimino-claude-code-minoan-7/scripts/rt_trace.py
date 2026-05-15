#!/usr/bin/env python3
"""
rt_trace — Orchestrator for reverse image/video tracing.

Runs multiple identification engines in parallel and synthesizes results
into a unified report. Gracefully skips engines whose API keys are missing.

Usage:
    rt_trace.py image.jpg
    rt_trace.py image.jpg --engines vision gemini geospy
    rt_trace.py image.jpg --skip geospy
    rt_trace.py video.mp4 --keyframes --max 3
    rt_trace.py image.jpg --json

Engines (Phase 1 — free tier):
    vision  — Google Cloud Vision Web Detection
    geospy  — Picarta AI geolocation
    gemini  — Gemini multimodal identification

Future engines (Phase 2+):
    lens    — Google Lens via SerpAPI
    tineye  — TinEye duplicate search
    lenso   — Lenso.ai category search
    yandex  — Yandex Images via SerpAPI

Environment variables:
    GOOGLE_APPLICATION_CREDENTIALS or gcloud ADC  (vision)
    PICARTA_API_KEY or GEOSPY_API_KEY             (geospy)
    GOOGLE_API_KEY or GEMINI_API_KEY              (gemini)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

ENGINE_REGISTRY = {
    "vision": {"script": "rt_vision.py", "env": None},
    "gemini": {"script": "rt_gemini.py", "env": ["GOOGLE_API_KEY", "GEMINI_API_KEY"]},
    "geospy": {"script": "rt_geospy.py", "env": ["PICARTA_API_KEY", "GEOSPY_API_KEY"]},
}

ALL_ENGINES = list(ENGINE_REGISTRY.keys())


def check_engine_available(engine: str) -> tuple[bool, str]:
    spec = ENGINE_REGISTRY.get(engine)
    if not spec:
        return False, f"unknown engine '{engine}'"
    env_vars = spec["env"]
    if env_vars and not any(os.environ.get(v) for v in env_vars):
        return False, f"none of {', '.join(env_vars)} set"
    if engine == "vision":
        try:
            import google.cloud.vision  # noqa: F401
            return True, "ok"
        except ImportError:
            return False, "google-cloud-vision not installed"
    return True, "ok"


def run_engine(engine: str, image_path: str, extra_args: list[str] | None = None) -> dict:
    spec = ENGINE_REGISTRY.get(engine)
    if not spec:
        return {"engine": engine, "status": "error", "error": f"unknown engine '{engine}'"}

    script = SCRIPT_DIR / spec["script"]
    cmd = [sys.executable, str(script), image_path, "--json"]
    if extra_args:
        cmd.extend(extra_args)

    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        elapsed = time.time() - start

        if result.returncode != 0:
            return {
                "engine": engine,
                "status": "error",
                "error": result.stderr.strip(),
                "elapsed_seconds": round(elapsed, 2),
            }

        data = json.loads(result.stdout)
        data["status"] = "ok"
        data["elapsed_seconds"] = round(elapsed, 2)
        return data

    except subprocess.TimeoutExpired:
        return {"engine": engine, "status": "timeout", "elapsed_seconds": 60.0}
    except json.JSONDecodeError:
        return {"engine": engine, "status": "error", "error": "Invalid JSON from engine", "raw": result.stdout[:500]}
    except Exception as e:
        return {"engine": engine, "status": "error", "error": str(e)}


def is_video(path: str) -> bool:
    video_exts = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v"}
    return Path(path).suffix.lower() in video_exts


def extract_frames(video_path: str, keyframes: bool = True, max_frames: int = 3,
                   timestamps: list[str] | None = None) -> list[str]:
    script = SCRIPT_DIR / "rt_extract.py"
    cmd = [sys.executable, str(script), video_path, "--json", "--max", str(max_frames)]

    if timestamps:
        cmd.extend(["--timestamps"] + timestamps)
    elif keyframes:
        cmd.append("--keyframes")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"Frame extraction failed: {result.stderr}")

    data = json.loads(result.stdout)
    return data.get("frames", [])


def synthesize(results: list[dict]) -> dict:
    synthesis = {
        "best_guess": None,
        "media_identification": None,
        "location": None,
        "web_entities": [],
        "matching_pages": [],
        "confidence": "low",
    }

    for r in results:
        if r.get("status") != "ok":
            continue

        engine = r.get("engine", "")

        if engine == "vision" or "web_entities" in r:
            entities = r.get("web_entities", [])
            synthesis["web_entities"].extend(entities)
            if r.get("best_guess_labels"):
                synthesis["best_guess"] = r["best_guess_labels"][0]
            pages = r.get("pages_with_matching_images", [])
            synthesis["matching_pages"].extend(pages[:5])

        if engine == "gemini" or "identification" in r:
            ident = r.get("identification", {})
            if ident.get("title"):
                synthesis["media_identification"] = ident
                if ident.get("confidence") == "high":
                    synthesis["confidence"] = "high"
                elif ident.get("confidence") == "medium" and synthesis["confidence"] != "high":
                    synthesis["confidence"] = "medium"

        if engine == "geospy" or "predictions" in r:
            preds = r.get("predictions", [])
            if preds:
                synthesis["location"] = preds[0]
                if r.get("description"):
                    synthesis["location"]["description"] = r["description"]

    if synthesis["web_entities"]:
        synthesis["web_entities"].sort(key=lambda x: x.get("score", 0), reverse=True)
        synthesis["web_entities"] = synthesis["web_entities"][:10]

    if not synthesis["best_guess"] and (synthesis.get("media_identification") or {}).get("title"):
        synthesis["best_guess"] = synthesis["media_identification"]["title"]

    return synthesis


def format_report(results: list[dict], synthesis: dict, image_path: str) -> str:
    lines = ["=" * 60, f"REVERSE TRACE: {image_path}", "=" * 60, ""]

    if synthesis["best_guess"]:
        lines.append(f"BEST GUESS: {synthesis['best_guess']}")
        lines.append("")

    ident = synthesis.get("media_identification")
    if ident:
        lines.append("MEDIA IDENTIFICATION (Gemini):")
        if ident.get("title"):
            media = ident.get("media_type", "").replace("_", " ").title()
            lines.append(f"  {ident['title']} ({media})")
        if ident.get("season") and ident.get("episode"):
            lines.append(f"  Season {ident['season']}, Episode {ident['episode']}")
        if ident.get("characters"):
            lines.append(f"  Characters: {', '.join(ident['characters'])}")
        if ident.get("actors"):
            lines.append(f"  Actors: {', '.join(ident['actors'])}")
        if ident.get("year"):
            lines.append(f"  Year: {ident['year']}")
        if ident.get("reasoning"):
            lines.append(f"  Reasoning: {ident['reasoning']}")
        lines.append("")

    loc = synthesis.get("location")
    if loc:
        parts = [x for x in [loc.get("city"), loc.get("state"), loc.get("country")] if x]
        if parts:
            lines.append("GEOLOCATION (Picarta):")
            lines.append(f"  {', '.join(parts)}")
            if loc.get("latitude") is not None and loc.get("longitude") is not None:
                lines.append(f"  Coordinates: {loc['latitude']:.4f}, {loc['longitude']:.4f}")
            if loc.get("confidence"):
                lines.append(f"  Confidence: {loc['confidence']:.1%}")
            if loc.get("description"):
                lines.append(f"  Description: {loc['description']}")
            lines.append("")

    entities = synthesis.get("web_entities", [])
    if entities:
        lines.append("WEB ENTITIES (Vision API):")
        for e in entities[:10]:
            desc = e.get("description") or "(unnamed)"
            lines.append(f"  [{e.get('score', 0):.2f}] {desc}")
        lines.append("")

    pages = synthesis.get("matching_pages", [])
    if pages:
        lines.append(f"MATCHING PAGES ({len(pages)}):")
        for p in pages[:5]:
            lines.append(f"  {p.get('title', 'Untitled')}")
            lines.append(f"    {p.get('url', '')}")
        lines.append("")

    lines.append("ENGINE STATUS:")
    for r in results:
        engine = r.get("engine", "unknown")
        status = r.get("status", "unknown")
        elapsed = r.get("elapsed_seconds", 0)
        if status == "ok":
            lines.append(f"  {engine}: OK ({elapsed:.1f}s)")
        else:
            err = r.get("error", status)
            lines.append(f"  {engine}: {err}")

    lines.append("")
    lines.append(f"Overall confidence: {synthesis['confidence']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Reverse trace — identify image/video sources")
    parser.add_argument("input", help="Image or video file path")
    parser.add_argument("--engines", nargs="+", choices=ALL_ENGINES, help="Engines to run (default: all available)")
    parser.add_argument("--skip", nargs="+", choices=ALL_ENGINES, default=[], help="Engines to skip")
    parser.add_argument("--keyframes", action="store_true", help="Extract keyframes from video (default)")
    parser.add_argument("--timestamps", nargs="+", help="Extract specific timestamps from video")
    parser.add_argument("--max-frames", type=int, default=3, help="Max frames to extract from video (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--workers", type=int, default=3, choices=range(1, 11), metavar="N", help="Parallel workers 1-10 (default: 3)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    engines = args.engines or ALL_ENGINES
    engines = [e for e in engines if e not in args.skip]

    available_engines = []
    for engine in engines:
        ok, reason = check_engine_available(engine)
        if ok:
            available_engines.append(engine)
        else:
            print(f"Skipping {engine}: {reason}", file=sys.stderr)

    if not available_engines:
        print("Error: No engines available. Check API keys and dependencies.", file=sys.stderr)
        sys.exit(1)

    images = []
    if is_video(args.input):
        print(f"Extracting frames from video...", file=sys.stderr)
        images = extract_frames(args.input, keyframes=True, max_frames=args.max_frames,
                                timestamps=args.timestamps)
        if not images:
            print("Error: No frames extracted", file=sys.stderr)
            sys.exit(1)
        print(f"Extracted {len(images)} frames", file=sys.stderr)
    else:
        images = [args.input]

    all_results = []
    all_syntheses = []

    for image_path in images:
        print(f"\nTracing: {image_path}", file=sys.stderr)
        results = []

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(run_engine, engine, image_path): engine
                for engine in available_engines
            }
            for future in as_completed(futures):
                engine = futures[future]
                try:
                    result = future.result()
                    result["engine"] = engine
                    results.append(result)
                    status = result.get("status", "unknown")
                    print(f"  {engine}: {status}", file=sys.stderr)
                except Exception as e:
                    results.append({"engine": engine, "status": "error", "error": str(e)})
                    print(f"  {engine}: error — {e}", file=sys.stderr)

        engine_order = {e: i for i, e in enumerate(available_engines)}
        results.sort(key=lambda r: engine_order.get(r.get("engine", ""), 999))

        synthesis = synthesize(results)
        all_results.append({"image": image_path, "results": results, "synthesis": synthesis})
        all_syntheses.append(synthesis)

    if args.json:
        output = {"input": args.input, "traces": all_results}
        print(json.dumps(output, indent=2, default=str))
    else:
        for trace in all_results:
            print(format_report(trace["results"], trace["synthesis"], trace["image"]))
            print()


if __name__ == "__main__":
    main()
