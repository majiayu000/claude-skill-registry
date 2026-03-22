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

Execute the following 5 phases in order. Announce each phase as you enter it.

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
nlm notebook query <notebook_id> "Break the subtopic '<subtopic>' into sequential learning units of roughly equal information density. Each unit MUST be mutually exclusive — no concept should appear in more than one unit. Each unit should have a short title (3-6 words), a one-sentence description of what it covers, and a one-sentence boundary note stating what it does NOT cover (i.e., what belongs to adjacent units). Order them logically: foundational concepts first, then intermediate, then advanced. Return as a numbered list with format: 'N. Title — Description. Boundary: <what this unit excludes>'. Target count: <target_count> units."
```

**Parse the response** to extract for each unit:
- **Title** (used for video naming)
- **Description** (what the unit covers)
- **Boundary** (what the unit excludes)

All three are used to build the `--focus` parameter in Phase 4.

---

### Phase 3: Source-to-Unit Mapping

Map notebook sources to relevant learning units so each unit's artifacts only draw from topically relevant sources. Reuse the source list already fetched in Step 2b.

**If the notebook has only 1 source, skip this phase entirely** — all artifacts use that single source.

**Step 3a — Collect source summaries:**

From the source list obtained in Step 2b, parse to get all source IDs and titles. Then run **ALL in parallel**:

```bash
nlm source describe <source_id> --json   # for each source
```

Collect `id`, `title`, `summary` (truncate to ~100 chars), and `keywords` (first 5). If `source describe` fails for a source, use only its title in the mapping prompt.

**Step 3b — Map sources to units:**

```bash
nlm notebook query <notebook_id> "Given these learning units:
1. <title> — <description>
2. <title> — <description>
...
And these sources:
- <source_id> '<title>': <summary_snippet> [keywords: kw1, kw2]
- <source_id> '<title>': <summary_snippet> [keywords: kw1, kw2]
...
For each learning unit, list ONLY the source IDs directly relevant to that unit's specific topic. A source may appear in multiple units. Format:
Unit 1: <id>, <id>, ...
Unit 2: <id>, <id>, ..."
```

**Step 3c — Parse the mapping:**

Build map: `unit_number → [source_id1, source_id2, ...]`

**Fallback rules:**
- If a unit maps to 0 sources → use ALL sources for that unit (omit `--source-ids`)
- If the mapping query returns unparseable output → use ALL sources for all units (degrades gracefully to current behavior)

---

### Phase 4: Per-Unit Artifacts (Parallel)

Fire **ALL** per-unit artifact creation commands **in parallel** (maximize throughput):

For every learning unit, fire both commands simultaneously using an **enriched focus prompt** that scopes content and prevents overlap with neighboring units. Include `--source-ids` from the Phase 3 mapping to restrict each artifact to relevant sources only:

```bash
nlm infographic create <notebook_id> --focus "Unit <N> of <total>: <unit title>. <unit description>. Does NOT cover: <boundary>." --source-ids <id1>,<id2>,<id3> -y
nlm video create <notebook_id> --focus "Unit <N> of <total>: <unit title>. <unit description>. Does NOT cover: <boundary>." --source-ids <id1>,<id2>,<id3> -y
```

Build the focus string from the parsed decomposition output (title + description + boundary). Use the source IDs from the Phase 3 mapping for each unit. If a unit has no mapped sources (fallback), omit `--source-ids` entirely for that unit. For example, with 5 units this fires 10 commands in parallel.

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

### Phase 5: Verify, Order & Report

**Step 5a — Check artifact status:**

```bash
nlm studio status <notebook_id> --json
```

Poll up to 3 times with 60-second intervals until all new artifacts show complete status.

**Step 5b — Determine deep dive sequence prefix:**

From the `studio status --json` output in step 5a, inspect existing video names for the pattern `DD<number>-`. Find the highest existing deep dive number and increment by 1. If no existing deep dive sequences are found, start at 1.

- No existing `DD*-` videos → prefix is `DD1-`
- Existing `DD1-` videos → prefix is `DD2-`
- Existing `DD1-` and `DD2-` videos → prefix is `DD3-`

**Step 5c — Rename videos in sequence order:**

Use `nlm studio rename` to create a numbered playlist with the determined prefix:

```bash
nlm studio rename <unit1_video_id> "DD<X>-01 - <unit1 title>"
nlm studio rename <unit2_video_id> "DD<X>-02 - <unit2 title>"
```

Where `<X>` is the deep dive sequence number from step 5b. Continue for each unit video in learning order. The `DD<X>-` prefix (Deep Dive #X) distinguishes these from the original new-topic sequence (`01`, `02`, ...) and from other deep dive sequences.

**Step 5d — Present final report:**

```
## Deep Dive Complete: <subtopic>

**Notebook ID:** <notebook_id>
**Notebook URL:** https://notebooklm.google.com/notebook/<notebook_id>

### Learning Units (Video Playlist Order)
- **DD<X>-01 - <unit1 title>** — Infographic + Video (<N> sources)
- **DD<X>-02 - <unit2 title>** — Infographic + Video (<N> sources)
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
| `source list` | `<notebook_id>`, `--json`/`-j` |
| `source describe` | `<source_id>`, `--json`/`-j` |
| `infographic create` | `--focus "<topic>"`, `--source-ids <id1>,<id2>`, `-y` |
| `video create` | `--focus "<topic>"`, `--source-ids <id1>,<id2>`, `-y` |
| `studio status` | `--full`/`-a`, `--json`/`-j` |
| `studio rename` | `<artifact_id> "<new_title>"` |
