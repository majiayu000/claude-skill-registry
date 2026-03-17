---
name: nlm-deepdive
description: Deep dives into a subtopic within an existing NotebookLM notebook. Decomposes the subtopic into sequential learning units and creates per-unit infographics and video overviews in parallel, then renames videos into playlist order. Use when user says "nlm-deepdive", "deep dive into", or "drill down into".
user-invocable: true
---

# NLM Deep Dive — Subtopic Learning Unit Generator

Deep dives into a subtopic within an **existing** NotebookLM notebook using the NLM CLI (`/Users/user/.local/bin/nlm`). Decomposes the subtopic into sequential learning units and generates per-unit infographics and video overviews, then renames videos into playlist order.

## Input Format

```
/nlm-deepdive <subtopic> [--notebook <notebook_id>]
```

- `<subtopic>` is **required**
- `--notebook` is optional; if omitted, notebooks are listed and matched by topic relevance

## Workflow

Execute the following 4 phases in order. Announce each phase as you enter it.

---

### Phase 1: Identify Notebook

**If `--notebook <id>` is provided:**

Verify the notebook exists:

```bash
nlm notebook get <notebook_id>
```

If it fails, list all notebooks and ask the user to pick (see fallback below).

**If `--notebook` is NOT provided:**

List all notebooks:

```bash
nlm notebook list --title
```

Match the subtopic against notebook titles to find the most relevant one:
- If **exactly one** good match → confirm with the user and proceed
- If **multiple candidates** or **no clear match** → present the top 3 options and ask the user to pick
- If **no notebooks exist** → tell the user to create one first (e.g., with `/nlm-new-topic`)

---

### Phase 2: Topic Decomposition

**Step 2a — Understand notebook content:**

```bash
nlm notebook describe <notebook_id>
```

**Step 2b — Check source count to calibrate unit count:**

```bash
nlm source list <notebook_id>
```

Use source count to set target unit range:
- Fewer than 5 sources → 3-4 units
- 5-9 sources → 4-5 units
- 10+ sources → 5-7 units

**Step 2c — Decompose the subtopic into learning units:**

```bash
nlm notebook query <notebook_id> "Break the subtopic '<subtopic>' into sequential learning units of roughly equal information density. Each unit should have a short title (3-6 words) and a one-sentence description. Order them logically: foundational concepts first, then intermediate, then advanced. Return as a numbered list with format: 'N. Title — Description'. Target count: <target_count> units."
```

**Parse the response** to extract unit titles for use as `--focus` parameters in Phase 3.

---

### Phase 3: Per-Unit Artifacts (Parallel)

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

### Phase 4: Verify, Order & Report

**Step 4a — Check artifact status:**

```bash
nlm studio status <notebook_id> --json
```

Poll up to 3 times with 60-second intervals until all new artifacts show complete status.

**Step 4b — Rename videos in sequence order:**

Use `nlm studio rename` to create a numbered playlist:

```bash
nlm studio rename <unit1_video_id> "01 - <unit1 title>"
nlm studio rename <unit2_video_id> "02 - <unit2 title>"
```

Continue for each unit video in learning order.

**Step 4c — Present final report:**

```
## Deep Dive Complete: <subtopic>

**Notebook ID:** <notebook_id>
**Notebook URL:** https://notebooklm.google.com/notebook/<notebook_id>

### Learning Units (Video Playlist Order)
- **01 - <unit1 title>** — Infographic + Video
- **02 - <unit2 title>** — Infographic + Video
- ...

### Failed Artifacts (if any)
- <list any failures>

### Download Commands
nlm download video <notebook_id>
nlm download infographic <notebook_id>
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **Notebook not found** | List all notebooks, ask user to pick |
| **No clear notebook match** | Show top 3 candidates, ask user |
| **Artifact creation fails** | Retry up to 3 times with backoff (30s, 60s, 120s) |
| **Artifact hits daily limit** | If error contains "Try again later" after retries, stop retrying that type, inform user of likely daily limit, list commands for manual creation |
| **Artifact stuck processing** | Poll up to 3 times at 60s intervals; note incomplete items in report |

## Key NLM CLI Commands Used

| Command | Key Flags |
|---------|-----------|
| `notebook list` | `--title`/`-t`, `--json`/`-j` |
| `notebook get` | `<notebook_id>` |
| `notebook describe` | `<notebook_id>` |
| `notebook query` | `<notebook_id> "<prompt>"` |
| `source list` | `<notebook_id>` |
| `infographic create` | `--focus "<topic>"`, `-y` |
| `video create` | `--focus "<topic>"`, `-y` |
| `studio status` | `--full`/`-a`, `--json`/`-j` |
| `studio rename` | `<artifact_id> "<new_title>"` |
