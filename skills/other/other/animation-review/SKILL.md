---
name: animation-review
description: Review web animations by recording the browser and sending video to Gemini for frame-level analysis
---

# Animation Review

Review animations and interactions by recording the browser and sending the video to Gemini for structured analysis.

## Prerequisites

- `ffmpeg` installed (`brew install ffmpeg`)
- `playwright` Python package with Chromium (`pip install playwright && playwright install chromium`)
- `google-genai` Python package (`pip install google-genai`)
- `GEMINI_API_KEY` environment variable set
- For manual recording only: macOS Screen Recording permission granted to terminal app

## How Gemini fits in

Gemini is the **eyes** — it watches the recording and describes what it sees with precision. You are the **hands** — you translate those observations into code changes with full codebase context.

**Treat all Gemini analysis as observational evidence, not authoritative diagnosis.** Gemini cannot see the code. When it suggests root causes or implementation fixes, treat these as hypotheses from an external observer who can see the symptoms but not the source. Its frame-level descriptions of *what happens visually* are reliable. Its theories about *why* are informed guesses that you should verify against the actual code.

This applies across all modes, but especially to `diagnose` (where Gemini hypothesizes about bugs) and `inspire` (where Gemini decomposes effects without knowing your tech stack).

### Interpreting timestamps and durations

Gemini can only observe what's in the sampled frames. Its temporal precision depends on the analysis FPS:

| Mode | FPS | Frame interval | What this means |
|------|-----|---------------|-----------------|
| **check** | 5 | 200ms | A "300ms animation" could be anywhere from 200-400ms (1-2 frames). Timestamps are ±200ms. Good enough for "does it happen" but not for timing accuracy. |
| **review** | 12 | 83ms | A "300ms animation" is ~3-4 frames. Easing character is visible. Durations are accurate within ~80ms — enough to judge "too fast" vs "too slow". |
| **diagnose/inspire** | 24 | 42ms | A "300ms animation" is ~7 frames. Easing curves, stagger offsets, and glitch moments are precisely observable. Durations are accurate within ~40ms. |

When Gemini reports a duration like "~400ms with ease-out", consider the mode's precision. At 5fps that could really be 200-600ms. At 24fps it's likely 360-440ms. The system prompt tells Gemini to report in frame counts alongside milliseconds so you can judge precision yourself.

If you're debugging a timing issue and Gemini's temporal precision isn't sufficient, re-run at a higher mode. A `check` that reveals "something's off with the timing" can be followed up with a `diagnose` for frame-precise detail. You can also escalate just a specific time range — see "Escalating a region" below.

## Workflow

### 1. Determine source and mode

There are two entry points — figure out which applies:

**User provides a video file.** The user has a screen recording (.mov, .mp4, .webm) — either of their own UI or a reference they want to recreate. Skip straight to step 3 (Analyze). No recording step needed. User-provided videos are typically 30-60fps, which is more than enough for any analysis mode — Gemini downsamples to the mode's FPS automatically.

**Agent captures from the browser.** The animation is running in a local dev server and needs to be recorded. Proceed to step 2 (Record), then step 3 (Analyze).

Choose the analysis mode based on what question you're trying to answer:

| Mode | FPS | Model | Question | When to use |
|------|-----|-------|----------|-------------|
| **check** | 5 | Flash | "Does it work?" | First pass — verify the animation fires, completes, and doesn't visually break. Early development, after wiring up a new animation, smoke testing. |
| **review** | 12 | Flash | "How does it feel?" | Design and polish — evaluate easing, timing, choreography, and overall quality. Use when the animation works but needs refinement, or for design review before shipping. |
| **diagnose** | 24 | Pro | "What's going wrong?" | Bug investigation — the animation has a specific visual problem (jump, stutter, misalignment, timing glitch). Need frame-precise evidence to locate the root cause in code. |
| **inspire** | 24 | Pro | "What's happening here?" | Reference analysis — the user has a video showing a desired effect and wants a technical decomposition to guide implementation. |

**Decision guide for agents:**

- User says "check if this works" / "does the animation play" / just implemented something new → **check**
- User says "how does this look" / "review the animation" / "is the timing right" / design feedback → **review**
- User says "there's a bug" / "it jumps" / "something's wrong with" / describes a specific visual issue → **diagnose**
- User provides a video of someone else's UI / "I want it to look like this" / "recreate this effect" → **inspire**
  - For **inspire**: if the user hasn't said which part of the video or which specific effect to focus on, **ask them before running the analysis.** A full-video decomposition without focus will be vague and unhelpful.

If the mode isn't clear from context, ask the user.

### 2. Record (skip if user provided a video)

The recording step captures browser interactions as video. **Record generously, analyze precisely** — Playwright's video always includes the full session (page load through close), so capture more than you need. The recorder always records at 24fps (the Gemini analysis maximum) so that any analysis mode can sample at full resolution, including escalation of a specific time range to `diagnose`. The recorder logs a timeline showing when each action executed relative to the video start — use these timestamps with `--start`/`--end` on `analyze.py` to focus Gemini on the relevant window.

#### Automated (preferred) — Claude drives the browser

Use `record_browser.py` when Claude is performing the interactions. Playwright records the page internally, then transcodes to mp4. No screen recording permissions needed.

```bash
# Record a page load animation
python3 ~/.claude/skills/animation-review/scripts/record_browser.py http://localhost:3000

# Click a button, wait for animation, record everything
python3 ~/.claude/skills/animation-review/scripts/record_browser.py http://localhost:3000 \
  -a 'click:.play-btn' -a 'wait:2000'

# Carousel: click through slides
python3 ~/.claude/skills/animation-review/scripts/record_browser.py http://localhost:5173/carousel \
  -a 'wait:1000' -a 'click:.next' -a 'wait:800' -a 'click:.next' -a 'wait:800'

# Scroll-triggered animation
python3 ~/.claude/skills/animation-review/scripts/record_browser.py http://localhost:3000 \
  -a 'scroll:500' -a 'wait:1000' -a 'scroll:500' -a 'wait:1000'

# Custom viewport size
python3 ~/.claude/skills/animation-review/scripts/record_browser.py http://localhost:3000 \
  -W 1920 -H 1080 -a 'click:.hero-cta' -a 'wait:3000'
```

Action format for `-a`:
- `wait:MS` — wait N milliseconds
- `click:SELECTOR` — click an element
- `scroll:PIXELS` — scroll down (negative for up)
- `hover:SELECTOR` — hover over an element
- `press:KEY` — press a key (Enter, Tab, ArrowRight, etc.)
- `type:SELECTOR|TEXT` — type into an element (pipe separates selector from text)

Construct actions from what you know about the animation trigger. For page-load animations, no actions are needed — the recording captures from navigation onward.

Use `--wait-before` to adjust the pause after page load (default 500ms) and `--wait-after` to adjust the pause after the last action (default 1000ms).

The recorder prints a timeline to stderr showing when each action ran:
```
  → click:.play-btn (at 1.8s)
  → wait:2000 (at 1.9s)
Timeline: actions 1.8s–3.9s, total 4.9s
```
These timestamps are measured Python-side (wall clock), not from the video encoder, so they're approximate — **always add ~1s buffer on each side** when using `--start`/`--end`. For the example above, use `--start 1s --end 5s`.

#### After recording: notify the user

Once the recording finishes, **immediately move it to `.animation-review/`** and tell the user before starting analysis. This lets them verify the capture while Gemini runs. The flow:

1. Move the video from `/tmp/` to `.animation-review/<timestamp>_<mode>.mp4`
2. Message the user with something like:

   > Recorded 4.9s of the carousel interaction. You can preview the recording here: `.animation-review/2026-02-09_153042_diagnose.mp4`
   >
   > Running **diagnose** analysis at 24fps with gemini-2.5-pro — focusing on 1s–5s where the actions occurred.

3. Run `analyze.py` pointing at the video's new path. Do not wait for user input — continue straight to analysis.

This way the user can scrub through the video while analysis runs and flag if it missed the right interaction.

#### Manual — User triggers the interaction

Use `record.sh` when the user needs to interact with a real browser window manually. Requires macOS Screen Recording permission.

```bash
bash ~/.claude/skills/animation-review/scripts/record.sh -d 10 -f 15
bash ~/.claude/skills/animation-review/scripts/record.sh -d 8 -f 15 -r "1280x720+0+0"
```

### 3. Analyze

Run the analysis script with the appropriate mode. The mode sets FPS, model, and system prompt automatically. If you moved the video to `.animation-review/` in the previous step, pass that path with `-v`.

```bash
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t <mode> \
  -v <video_path> -p "<context>"
```

You can override defaults with `-f` (FPS), `-m` (model), `--raw` (force text), `--json` (force structured), and `--start`/`--end` to clip to a time range.

#### What context to supply (`-p`)

The context prompt is critical — it tells Gemini what to look for. What you include depends on the mode:

**check** — Minimal. What the animation is supposed to do.
```bash
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t check \
  -p "Cards should fade in on page load with staggered timing"
```

**review** — What it should do + what "good" looks like. Include design intent, desired feel, or reference points.
```bash
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t review \
  -p "Modal slides up from bottom with spring easing. Should feel snappy but not aggressive. Backdrop fades in simultaneously."
```

**diagnose** — What it should do + what's going wrong + any specific observations from the user. The richer the context, the better the hypothesis.
```bash
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t diagnose \
  -v /path/to/bug-recording.mov \
  -p "Circular carousel: clicking an item clones it and animates into a detail view. Closing should animate back to the original position. BUG: the closing animation doesn't return to the correct position — there's a visible jump at the end. The carousel may have rotated while the detail view was open."
```

**inspire** — Which element or effect in the video is relevant + what the user wants to achieve. **If the user hasn't specified which part of the video to focus on, ask them before running the analysis.**
```bash
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t inspire \
  -v /path/to/reference.mov \
  -p "Focus on the card flip transition at 0:03-0:05. The card rotates on its vertical axis while the back face content fades in. I want to recreate this for our product cards."
```

#### Escalating a region

When a lower-FPS analysis (check or review) reveals something that needs closer inspection, you can re-analyze just that time range at higher FPS — no need to re-analyze the whole video. Use `--start` and `--end` to clip, and switch to a higher mode:

```bash
# Initial review spotted a glitch around 3-5 seconds
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t review \
  -v /path/to/recording.mov \
  -p "Page transition with staggered card animations"

# Escalate just that region to diagnose at 24fps
python3 ~/.claude/skills/animation-review/scripts/analyze.py -t diagnose \
  -v /path/to/recording.mov \
  --start 2s --end 6s \
  -p "Cards appear to overlap briefly around 3-4s. One card seems to jump position."
```

This sends the same video file to Gemini but tells it to only sample frames within the specified range, at the new mode's FPS. No ffmpeg trimming needed — the API handles the clipping server-side. This is cheaper and faster than re-analyzing the full video at 24fps with Pro.

The offsets use seconds (e.g. `3s`, `1.5s`, `90s`). Add a small buffer around the moment of interest — if the glitch is at ~4s, use `--start 3s --end 6s` to capture context on either side.

### 4. Present findings

Show the results to the user. How you present depends on the mode:

- **check**: Brief pass/fail summary. Flag anything broken.
- **review**: Score, key observations about feel and polish, and any recommendations.
- **diagnose**: The visual evidence first (what happens frame by frame), then hypotheses about root cause, then suggested debugging steps. Be clear about what's observed fact vs what's Gemini's theory.
- **inspire**: The effect decomposition as a spec — properties, timing, choreography. This becomes the reference for implementation.

### 5. Fix and re-verify

Use the analysis feedback to modify code. For non-trivial fixes, record and analyze again to verify the improvement.

## Output formats

Each mode defaults to the output format that works best for it. Use `--raw` or `--json` to override.

**check, review** default to structured JSON:

```json
{
  "summary": "Brief overall assessment",
  "animations": [
    {
      "element": "What's animating",
      "type": "slide | fade | scale | rotate | color | morph | scroll | other",
      "timestamp": "MM:SS",
      "duration_ms": 300,
      "easing": "ease-out, spring, linear, etc.",
      "quality": "smooth | acceptable | janky | broken"
    }
  ],
  "issues": [
    {
      "timestamp": "MM:SS",
      "severity": "low | medium | high",
      "description": "What's wrong",
      "suggestion": "How to fix it"
    }
  ],
  "score": 8,
  "recommendations": ["Actionable improvements"]
}
```

**diagnose** defaults to raw text (narrative detail matters). Structured output via `--json` uses:

```json
{
  "summary": "Brief overall assessment",
  "observations": [
    {
      "timestamp": "MM:SS",
      "description": "What happens at this moment",
      "expected": "What should happen",
      "actual": "What actually happens"
    }
  ],
  "hypotheses": [
    {
      "cause": "Possible root cause",
      "evidence": "What visual evidence supports this",
      "debugging_steps": ["Step to confirm or rule out this hypothesis"]
    }
  ]
}
```

**inspire** defaults to raw text. Structured output via `--json` uses a decomposition schema:

```json
{
  "summary": "Brief description of the overall effect",
  "effects": [
    {
      "element": "What's animating",
      "trigger": "click | scroll | hover | load | etc.",
      "properties": ["opacity", "transform", "clip-path"],
      "from_state": "Starting visual state",
      "to_state": "Ending visual state",
      "duration_ms": 400,
      "delay_ms": 0,
      "easing": "Description of the timing curve feel",
      "timestamp": "MM:SS"
    }
  ],
  "choreography": "How the effects relate to each other in time",
  "notable_details": ["Subtle touches that make it feel polished"]
}
```

Use `--raw` on any mode for narrative output, or `--json` to force structured output on modes that default to raw.

## Saved results

By default, the analysis script saves both the video and the analysis output to a `.animation-review/` directory in the current working directory:

```
.animation-review/
  2026-02-09_153042_diagnose.mov     # video
  2026-02-09_153042_diagnose.md      # analysis (raw modes → .md, structured → .json)
  2026-02-08_091200_review.mp4
  2026-02-08_091200_review.json
```

This means previous analyses can be referenced later without keeping them in context or re-running the analysis. To refer back to a previous result, check `.animation-review/` for recent files.

**Automatic cleanup:** On each run, files older than 14 days are deleted. No manual cleanup needed.

**Git:** If the project is a git repo, the script automatically adds `.animation-review/` to `.gitignore` on first run.

**Opt out:** Pass `--no-save` to skip saving (output still goes to stdout as usual).

For user-provided videos, the file is copied into the results directory. For Playwright recordings from `/tmp`, the file is moved (no reason to keep the temp copy).

## Tips

- **FPS must be specified via mode or `-f`** — without it, Gemini defaults to 1fps which is useless for animation review.
- Max FPS is 24 (Gemini API limit). The script caps automatically if you go over.
- Accepted video formats: `.mp4`, `.mov`, `.webm`. QuickTime screen recordings (h264 .mov) work directly.
- Use `--raw` for diagnose and inspire when you want Gemini to give detailed narrative explanations (this is the default for those modes).
- Use `--json` for check and review when you want machine-parseable results (this is the default for those modes).
- For automated recording, prefer short focused clips over long recordings. Capture just the interaction.
- Use `--headed` on `record_browser.py` to watch the browser while it records (useful for debugging the action sequence itself).
