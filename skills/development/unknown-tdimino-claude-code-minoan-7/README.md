# reverse-trace

CLI toolkit for identifying the source of images and videos—TV show episodes, movie scenes, geographic locations, original publications. Chains multiple reverse search APIs in parallel and synthesizes results into a unified report.

## How it works

```
image/video → frame extraction → parallel engine queries → synthesis → report
                                  ├── Google Vision (web entities, matching pages)
                                  ├── Picarta (AI geolocation from visual cues)
                                  └── Gemini (LLM-based media identification)
```

Each engine runs independently and produces structured JSON. The orchestrator (`rt_trace.py`) runs them in parallel, merges results, deduplicates, and ranks by confidence.

## Quick start

```bash
# Single image — full pipeline
uv run --with google-cloud-vision --with google-genai --with picarta --with Pillow \
  python scripts/rt_trace.py screenshot.jpg

# Video — extracts keyframes first
uv run --with google-cloud-vision --with google-genai --with picarta --with Pillow \
  python scripts/rt_trace.py clip.mp4 --max-frames 3

# Individual engines
uv run --with google-cloud-vision python scripts/rt_vision.py image.jpg
uv run --with picarta python scripts/rt_geospy.py photo.jpg --top-k 3
uv run --with google-genai python scripts/rt_gemini.py frame.jpg --json
```

## Scripts

| Script | Engine | What it does | API key |
|--------|--------|-------------|---------|
| `rt_extract.py` | ffmpeg | Extract frames from video at timestamps, keyframes, or intervals | None (local) |
| `rt_vision.py` | Google Cloud Vision | Web Detection — entities, matching pages, similar images, best-guess labels | `GOOGLE_APPLICATION_CREDENTIALS` or ADC |
| `rt_geospy.py` | Picarta | AI geolocation — lat/lng, city, country, confidence | `PICARTA_API_KEY` or `GEOSPY_API_KEY` |
| `rt_gemini.py` | Gemini | Multimodal LLM identification — media type, title, episode, characters | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| `rt_trace.py` | Orchestrator | Runs all engines in parallel, synthesizes results | All of the above |
| `test_rt.py` | Tests | Syntax, help, error handling, JSON output validation | Optional |

## Environment variables

```bash
# Google Cloud Vision (free: 1K/mo)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
# or: gcloud auth application-default login

# Picarta geolocation (free tier at https://picarta.ai/api)
export PICARTA_API_KEY=your-key-here
# or legacy: export GEOSPY_API_KEY=your-key-here

# Gemini (free tier via AI Studio)
export GOOGLE_API_KEY=your-key-here
# or: export GEMINI_API_KEY=your-key-here
```

Missing keys don't crash the pipeline—the orchestrator skips unavailable engines and reports which ones ran.

## Output

Default output is a human-readable report:

```
============================================================
REVERSE TRACE: screenshot.jpg
============================================================

BEST GUESS: Breaking Bad Season 5 Episode 14

MEDIA IDENTIFICATION (Gemini):
  Breaking Bad (Tv Show)
  Season 5, Episode 14
  Characters: Walter White, Jesse Pinkman
  Actors: Bryan Cranston, Aaron Paul
  Year: 2013
  Confidence: high

GEOLOCATION (Picarta):
  Albuquerque, New Mexico, United States
  Coordinates: 35.0844, -106.6504

WEB ENTITIES (Vision API):
  [1.32] Breaking Bad
  [1.17] Bryan Cranston
  [0.98] Television

ENGINE STATUS:
  vision: OK (1.2s)
  gemini: OK (2.8s)
  geospy: OK (0.9s)
```

Add `--json` for machine-readable structured output.

## Expansion roadmap

Phase 2 (paid APIs):
- **SerpAPI Google Lens** — knowledge graph entities, best for pop culture ID ($50/mo)
- **TinEye** — exact provenance tracking, first-published dates ($200/mo)
- **Lenso.ai** — category-based search with face recognition (contact for pricing)
- **Yandex Images** — superior non-US face/scene matching ($50/mo via SerpAPI)

Phase 3 (custom corpus):
- **Twelve Labs** — index your own video library for scene search (free: 15 min)
- **Apify Google Lens** — cloud scraper alternative ($7.99/1K searches)

Adding a new engine: create `scripts/rt_<engine>.py` following the existing pattern (argparse CLI, `--json` flag, env var auth), then add an entry to `ENGINE_REGISTRY` in `rt_trace.py`.

## Tests

```bash
uv run python scripts/test_rt.py --quick    # Syntax + structure only
uv run python scripts/test_rt.py            # Full suite (calls APIs if keys present)
uv run python scripts/test_rt.py --engine gemini  # Test specific engine
```

## Dependencies

- Python 3.11+
- ffmpeg (for video frame extraction)
- `google-cloud-vision`, `google-genai`, `picarta`, `Pillow`
