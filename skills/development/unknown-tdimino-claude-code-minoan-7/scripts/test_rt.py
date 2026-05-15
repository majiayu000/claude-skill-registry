#!/usr/bin/env python3
"""
test_rt — Test suite for reverse-trace scripts.

Validates that each engine script runs, handles missing API keys gracefully,
and produces valid JSON output. Uses a test image downloaded from the web.

Usage:
    test_rt.py                    # Run all tests
    test_rt.py --engine vision    # Test specific engine
    test_rt.py --quick            # Syntax/import checks only, no API calls
    test_rt.py --with-image PATH  # Use a specific test image
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

ENGINES = {
    "extract": {"script": "rt_extract.py", "needs_video": True},
    "vision": {"script": "rt_vision.py", "env": None},
    "geospy": {"script": "rt_geospy.py", "env": ["PICARTA_API_KEY", "GEOSPY_API_KEY"]},
    "gemini": {"script": "rt_gemini.py", "env": ["GOOGLE_API_KEY", "GEMINI_API_KEY"]},
    "trace": {"script": "rt_trace.py", "env": None},
}

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
SKIP = "\033[33mSKIP\033[0m"


def create_test_image(output_path: str):
    try:
        from PIL import Image
        img = Image.new("RGB", (200, 200), color=(100, 149, 237))
        img.save(output_path, "JPEG")
        return True
    except ImportError:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=200x200:d=1",
             "-frames:v", "1", output_path],
            capture_output=True
        )
        return os.path.exists(output_path)


def test_syntax(engine_name: str) -> tuple[bool, str]:
    script = SCRIPT_DIR / ENGINES[engine_name]["script"]
    result = subprocess.run(
        [sys.executable, "-c", f"import py_compile; py_compile.compile('{script}', doraise=True)"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return True, "syntax ok"
    return False, result.stderr.strip()[:200]


def test_help(engine_name: str) -> tuple[bool, str]:
    script = SCRIPT_DIR / ENGINES[engine_name]["script"]
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0 and "usage" in result.stdout.lower():
        return True, "help ok"
    return False, f"returncode={result.returncode}"


def test_missing_file(engine_name: str) -> tuple[bool, str]:
    if engine_name == "extract":
        return True, "n/a"
    script = SCRIPT_DIR / ENGINES[engine_name]["script"]
    result = subprocess.run(
        [sys.executable, str(script), "/nonexistent/image.jpg", "--json"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return True, "correctly fails on missing file"
    return False, "should have failed"


def test_json_output(engine_name: str, image_path: str) -> tuple[bool, str]:
    info = ENGINES[engine_name]
    env_var = info.get("env")
    if env_var:
        env_vars = env_var if isinstance(env_var, list) else [env_var]
        if not any(os.environ.get(v) for v in env_vars):
            return None, f"{', '.join(env_vars)} not set"

    if info.get("needs_video"):
        return None, "needs video file"

    script = SCRIPT_DIR / info["script"]
    cmd = [sys.executable, str(script), image_path, "--json"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return False, f"exit {result.returncode}: {result.stderr[:200]}"

    try:
        data = json.loads(result.stdout)
        return True, f"valid JSON, {len(result.stdout)} bytes"
    except json.JSONDecodeError as e:
        return False, f"invalid JSON: {e}"


def main():
    parser = argparse.ArgumentParser(description="Test reverse-trace scripts")
    parser.add_argument("--engine", choices=list(ENGINES.keys()), help="Test specific engine")
    parser.add_argument("--quick", action="store_true", help="Syntax/import checks only")
    parser.add_argument("--with-image", help="Path to test image")
    args = parser.parse_args()

    engines_to_test = [args.engine] if args.engine else list(ENGINES.keys())

    if args.with_image:
        test_image = args.with_image
    else:
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        test_image = tmp.name
        tmp.close()
        if not create_test_image(test_image):
            print(f"{FAIL} Could not create test image", file=sys.stderr)
            sys.exit(1)

    print(f"Test image: {test_image}")
    print()

    total, passed, failed, skipped = 0, 0, 0, 0

    for engine in engines_to_test:
        print(f"--- {engine} ---")

        ok, msg = test_syntax(engine)
        total += 1
        print(f"  syntax:       {PASS if ok else FAIL} — {msg}")
        if ok:
            passed += 1
        else:
            failed += 1

        ok, msg = test_help(engine)
        total += 1
        print(f"  --help:       {PASS if ok else FAIL} — {msg}")
        if ok:
            passed += 1
        else:
            failed += 1

        ok, msg = test_missing_file(engine)
        total += 1
        print(f"  missing file: {PASS if ok else FAIL} — {msg}")
        if ok:
            passed += 1
        else:
            failed += 1

        if not args.quick:
            ok, msg = test_json_output(engine, test_image)
            total += 1
            if ok is None:
                print(f"  json output:  {SKIP} — {msg}")
                skipped += 1
            elif ok:
                print(f"  json output:  {PASS} — {msg}")
                passed += 1
            else:
                print(f"  json output:  {FAIL} — {msg}")
                failed += 1

        print()

    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped / {total} total")

    if not args.with_image and os.path.exists(test_image):
        os.unlink(test_image)

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
