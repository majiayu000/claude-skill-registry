---
name: nlm-new-topic
description: Creates a NotebookLM learning package for a topic. Automates notebook creation, source research, summary slides/video/audio/report, topic decomposition into sequential learning units, and per-unit infographics and video overviews. Supports optional source URLs and files. Use when user says "nlm-new-topic", "learning package for", or "notebooklm for".
user-invocable: true
---

# NLM New Topic — NotebookLM Learning Package Creator

Creates a complete NotebookLM learning package for any topic using the NLM CLI (`/Users/user/.local/bin/nlm`).

## Input Format

```
/nlm-new-topic <topic> [--url <url1> --url <url2>] [--file <path>]
```

- `<topic>` is **required**
- `--url` and `--file` are optional; if provided, these sources are added alongside auto-research

## Workflow

Execute the following 6 phases in order. Announce each phase as you enter it.

---

### Phase 1: Create Notebook

Create the notebook and capture its ID:

```bash
nlm notebook create "<topic>"
```

Capture the notebook ID from the output. This ID is used in every subsequent command.

If notebook creation fails, run `nlm doctor` and report the error to the user. Do not proceed.

---

### Phase 2: Research & Add Sources

**Step 2a — Add user-provided sources first (if any):**

For each `--url` argument:
```bash
nlm source add <notebook_id> --url <url> --wait
```

For each `--file` argument:
```bash
nlm source add <notebook_id> --file <path> --wait
```

Run these in parallel if multiple sources are provided.

**Step 2b — Auto-research:**

```bash
nlm research start "<topic>" -n <notebook_id> -m deep
```

This runs deep research (~5 minutes, ~40 sources). Then poll until complete:

```bash
nlm research status <notebook_id> --max-wait 300
```

Once complete, import all discovered sources:

```bash
nlm research import <notebook_id>
```

**Step 2c — Verify source count:**

```bash
nlm source list <notebook_id>
```

If fewer than 3 sources total, run a second fast research pass with a rephrased/broader query:

```bash
nlm research start "<broader topic query>" -n <notebook_id> -m fast
nlm research status <notebook_id> --max-wait 120
nlm research import <notebook_id>
```

If still 0 sources, ask the user to provide manual URLs.

---

### Phase 3: Summary Artifacts

Fire **all 5** summary artifact creation commands **in parallel** (do NOT wait between them):

```bash
nlm slides create <notebook_id> --focus "<topic>" -y
nlm video create <notebook_id> --focus "<topic>" -y
nlm audio create <notebook_id> --format deep_dive --focus "<topic>" -y
nlm report create <notebook_id> --format "Briefing Doc" -y
nlm mindmap create <notebook_id> --title "<topic>" -y
```

- `slides` → summary slide deck
- `video` → summary video overview
- `audio` → audio overview (podcast-style deep dive)
- `report` → briefing document
- `mindmap` → topic mind map

All commands use `-y` to skip confirmation prompts.

---

### Phase 4: Topic Decomposition

Get the AI summary of notebook content:

```bash
nlm notebook describe <notebook_id>
```

Then ask the notebook to decompose the topic into learning units:

```bash
nlm notebook query <notebook_id> "Break the topic '<topic>' into sequential learning units of roughly equal information density. Each unit should have a short title (3-6 words) and a one-sentence description. Order them logically: foundational concepts first, then intermediate, then advanced. Return as a numbered list with format: 'N. Title — Description'. Target count: 4-7 units."
```

**Parse the response** to extract unit titles for use as `--focus` parameters in Phase 5.

**Adjust target count based on source richness:**
- Fewer than 5 sources → aim for 3-4 units
- 5-9 sources → aim for 4-5 units
- 10+ sources → aim for 5-7 units

---

### Phase 5: Per-Unit Artifacts

Fire **ALL** per-unit artifact creation commands **in parallel** (maximize throughput):

For every learning unit, fire both commands simultaneously:

```bash
nlm infographic create <notebook_id> --focus "<unit title>" -y
nlm video create <notebook_id> --focus "<unit title>" -y
```

For example, with 5 units this fires 10 commands in parallel.

**Error handling — retry with backoff:**

If any command fails, retry up to 3 times with increasing backoff:
1. **Retry 1:** Wait 30 seconds, then retry
2. **Retry 2:** Wait 60 seconds, then retry
3. **Retry 3:** Wait 120 seconds, then retry

If a command still fails after all retries and the error contains "Try again later":
- **Stop retrying** that artifact type (e.g., all remaining infographics)
- **Tell the user** which artifacts failed and that the cause is likely a **daily creation limit** imposed by NotebookLM on their account tier
- **List the exact commands** the user can run manually later (tomorrow) to create the missing artifacts
- Continue with any other artifact types that are still succeeding

---

### Phase 6: Verify, Order & Report

**Step 6a — Check artifact status:**

```bash
nlm studio status <notebook_id> --json
```

Poll up to 3 times with 60-second intervals until all artifacts show complete status.

**Step 6b — Rename videos in sequence order:**

Use `nlm studio rename` to create a numbered playlist:

```bash
nlm studio rename <summary_video_id> "00 - <topic> Overview"
nlm studio rename <unit1_video_id> "01 - <unit1 title>"
nlm studio rename <unit2_video_id> "02 - <unit2 title>"
```

Continue for each unit video in learning order.

**Step 6c — Present final report:**

```
## Learning Package Complete: <topic>

**Notebook ID:** <notebook_id>
**Notebook URL:** https://notebooklm.google.com/notebook/<notebook_id>

### Sources
- <count> sources (N researched + M user-provided)

### Summary Artifacts
- Slide deck (full topic overview)
- Video overview: "00 - <topic> Overview"
- Audio overview (deep dive podcast)
- Briefing document
- Mind map

### Learning Units (Video Playlist Order)
- **01 - <unit1 title>** — Infographic + Video
- **02 - <unit2 title>** — Infographic + Video
- ...

### Download Commands
nlm download slide-deck <notebook_id>
nlm download video <notebook_id>
nlm download audio <notebook_id>
nlm download report <notebook_id>
nlm download infographic <notebook_id>
nlm download mind-map <notebook_id>
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **Notebook creation fails** | Run `nlm doctor` and report to user |
| **0 sources found** | Try broader query; if still 0, ask user for manual URLs |
| **Artifact creation fails** | Retry up to 3 times with backoff (30s, 60s, 120s) |
| **Artifact hits daily limit** | If error contains "Try again later" after retries, stop retrying that type, inform user of likely daily limit, list commands for manual creation |
| **Artifact stuck processing** | Poll up to 3 times at 60s intervals; note incomplete items in report |

## Key NLM CLI Flags Reference

| Command | Key Flags |
|---------|-----------|
| `research start` | `-n <notebook_id>`, `-m deep/fast`, `-s web/drive` |
| `research status` | `-t <task_id>`, `--max-wait 300`, `--full` |
| `research import` | notebook_id, optional task_id (auto-detects) |
| `source add` | `--url`, `--file`, `--youtube`, `--text`, `--wait` |
| `studio status` | `--full`/`-a`, `--json`/`-j` |
| `studio rename` | `<artifact_id> "<new_title>"` |
| `audio create` | `--format deep_dive/brief/critique/debate`, `--focus` |
| `report create` | `--format "Briefing Doc"/"Study Guide"/"Blog Post"` |
| `mindmap create` | `--title "<title>"` |
| `download video` | `--id <artifact_id>`, `-o <output_path>` |
| All artifact creates | `-y` (skip confirmation), `--focus "<topic>"` |
