---
name: reverse-trace
description: >-
  Identify the source of an image or video frame — TV show episode, movie scene,
  geographic location, or original publication. This skill should be used when the
  user asks to identify where an image is from, trace a screenshot back to its source,
  geolocate a photo, find what show or movie a frame is from, or do a reverse image
  search. Chains Google Vision, Picarta geolocation, and Gemini in parallel with graceful
  degradation. Triggers on: reverse image search, identify source, what show is this,
  where was this taken, trace image, identify video, what movie, which episode,
  geolocate photo, image source.
---

# Reverse Trace

Identify the source of images and videos by running multiple reverse search APIs in parallel and synthesizing results into a confidence-ranked report. Each engine contributes a different signal — web entity matching, AI geolocation, multimodal LLM identification — and the orchestrator merges them because no single API reliably covers all identification scenarios.

## Prerequisites

At least one API credential must be set. Missing keys cause the orchestrator to skip that engine, not crash.

| Engine | Env Var | Free Tier | Signal |
|--------|---------|-----------|--------|
| Google Vision | `GOOGLE_APPLICATION_CREDENTIALS` or ADC | 1K/mo | Web entities, matching pages, similar images, best-guess labels |
| Picarta (geospy) | `PICARTA_API_KEY` or `GEOSPY_API_KEY` | Yes | Lat/lng, city, country, confidence score |
| Gemini | `GOOGLE_API_KEY` or `GEMINI_API_KEY` | Yes | Media type, title, season/episode, characters, actors |

To set up Vision ADC: `gcloud auth application-default login`

## Workflow

### Full pipeline (recommended default)

Run `rt_trace.py` to execute all available engines in parallel. For video input, keyframes are extracted first via ffmpeg.

```bash
python3 scripts/rt_trace.py image.jpg
python3 scripts/rt_trace.py video.mp4 --max-frames 3
python3 scripts/rt_trace.py image.jpg --json
python3 scripts/rt_trace.py image.jpg --skip geospy
python3 scripts/rt_trace.py image.jpg --engines vision gemini
```

### Individual engines

Use a single engine when only one type of identification is needed, to conserve API quota, or to debug a specific engine's output.

```bash
python3 scripts/rt_vision.py image.jpg              # Web entities + matching pages
python3 scripts/rt_geospy.py photo.jpg --top-k 3    # AI geolocation
python3 scripts/rt_gemini.py frame.jpg               # LLM media identification
python3 scripts/rt_extract.py video.mp4 --keyframes  # Frame extraction only
```

### Engine selection guide

| Goal | Engines to use | Why |
|------|---------------|-----|
| Identify TV show / movie | `gemini` + `vision` | Gemini recognizes characters from training data; Vision finds matching web pages that name the episode |
| Find where an image was published | `vision` | Web Detection returns pages hosting the image with titles and URLs |
| Geolocate a photo | `geospy` | Picarta AI geolocation from visual cues (architecture, vegetation, signage) |
| Full automated identification | `rt_trace.py` (all) | Parallel execution, merged synthesis, confidence ranking |

## Output format

Default output is a human-readable report with sections: BEST GUESS, MEDIA IDENTIFICATION, GEOLOCATION, WEB ENTITIES, MATCHING PAGES, ENGINE STATUS. Add `--json` for structured JSON suitable for piping or programmatic consumption.

## Adding new engines

The orchestrator uses a single `ENGINE_REGISTRY` dict. To add an engine:

1. Create `scripts/rt_<name>.py` following the existing pattern (argparse CLI, `--json` flag, env var auth, `engine` field in JSON output)
2. Add an entry to `ENGINE_REGISTRY` in `rt_trace.py` with `script` and `env` keys
3. The engine is automatically included in the parallel pipeline

Planned Phase 2 engines (paid APIs): SerpAPI Google Lens, TinEye, Lenso.ai, Yandex. See `references/expansion-roadmap.md` for API details, pricing, and implementation notes.
