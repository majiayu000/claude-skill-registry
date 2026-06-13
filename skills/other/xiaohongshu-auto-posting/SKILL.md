---
name: xiaohongshu-auto-posting
description: "Automates the complete Xiaohongshu (XHS / Little Red Book) content operation workflow: pain-point topic collection → style case collection → topic selection → content writing → publishing → performance tracking. Use when user mentions xiaohongshu auto posting, xhs auto post, little red book posting, xiaohongshu post, xiaohongshu auto posting, xiaohongshu content operations, xhs content marketing, post to xiaohongshu, publish on xhs, post on xiaohongshu, xiaohongshu promotion, xiaohongshu operations, xiaohongshu automation, xhs automation, track xhs performance, track xiaohongshu performance, xiaohongshu data tracking, xiaohongshu analytics, switch xhs account, update xhs keywords."
---

# Xiaohongshu Auto-Posting (XHS Auto-Posting)

> End-to-end Xiaohongshu content operation: topic discovery → style reference → writing → publishing → performance tracking.

## Language

All process output to user (progress updates, questions, status notifications) follows the user's language.

## Objective

Automate a complete Xiaohongshu content operation cycle for a configured product: discover high-engagement pain-point topics via search, collect writing style references, generate platform-native content aligned with the style fingerprint, publish with user approval, and track post-publish performance metrics.

## Prerequisites

- Xiaohongshu creator center (`creator.xiaohongshu.com`) already logged in on a configured stealth browser (browser ID stored in `session_state.json`)
- `workspaces/xhs-posting/` workspace (auto-created on first run)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

Covered in Phase 0.5 — login check is deferred until session state is loaded (Phase 0.2) and the browser is opened. If the user triggers Phase 6 directly (standalone tracking mode), still complete Phase 0.2 and Phase 0.5 first.

### 3. Session Lifecycle

Each execution generates a unique session name (`xhs-<YYYYMMDD>-<HHMM>`) to avoid cross-conversation conflicts. The session is opened once in Phase 0.5 and closed at the end of the workflow. All commands in this Skill reference the session via `$SESSION` — the actual name is determined at runtime.

---

## Runtime Workspace

All runtime files (config, drafts, publish records, screenshots) are written to **the user's working directory (CWD)** under `workspaces/xhs-posting/`. This directory is auto-created on first run.

```
workspaces/xhs-posting/          ← relative to user CWD
├── session_state.json            # account & product config
├── config/
│   └── keywords.json             # keyword pool
├── tracking/
│   └── published.json            # published note records
├── reports/                      # performance reports
└── <YYYY-MM-DD>/                 # per-run date directory
    ├── topics/
    ├── selected_topics.json
    ├── style_fingerprint.json
    ├── drafts/
    └── replies/
```

---

## Quick Start

```
/xiaohongshu-auto-posting
```

Standalone triggers (jump directly to the corresponding phase, skipping Phase 0–4):
- `"track performance"` / `"see data"` / `"data collection"` → Phase 6 performance tracking
- `"settings"` / `"switch account"` / `"update keywords"` → Phase 0 configuration wizard

---

## Operational Rules

Three rules that apply to every browser-act session. Violating any one causes silent failures or long hangs. Full details in `references/phase5-publish.md §0`.

**Rule 1 — Never pipe browser-act output directly**

Redirect state output to a temp file, then grep the file. Piping may background the command when output contains multi-byte characters, making the result unavailable synchronously.

```bash
# WRONG
browser-act --session $SESSION state | grep "Publish"
# CORRECT
browser-act --session $SESSION state > /tmp/s.txt 2>&1 && grep "Publish" /tmp/s.txt
```

**Rule 2 — Escape all non-ASCII content before passing to eval --stdin**

Non-ASCII literals (Chinese, emoji) in JS source cause encoding errors in the subprocess pipeline. Escape to `\uXXXX` first:

```python
def to_ascii_js(s):
    return ''.join(r'\u{:04x}'.format(ord(c)) if ord(c) > 127 else c for c in s)
js = to_ascii_js(open('tmp/script.js', encoding='utf-8').read())
subprocess.run([..., 'eval', '--stdin'], input=js.encode('ascii'), ...)
```

**Rule 3 — Use `click`, not `eval`, for actions that trigger navigation**

`eval` hangs (~30 s timeout) when the callback causes a page redirect. Always use `browser-act --session $SESSION click <index>` for the publish button, then verify the URL immediately after.

---

## Phase 0 — Initialization

### 0.1 Tool Check

Run `browser-act browser list`:
- Command not found → run `uv tool upgrade browser-act-cli || uv tool install browser-act-cli --python 3.12`, then continue
- Returns normally → continue

### 0.2 Session State Load

Read `workspaces/xhs-posting/session_state.json`:
- File does not exist, or `browser_id` is empty → proceed to **0.3 First-time Configuration Wizard**
- File exists and `browser_id` is non-empty → load and display current config, ask user to confirm or modify

`session_state.json` structure:

```json
{
  "browser_id": "",
  "account": {
    "nickname": "",
    "profile": ""
  },
  "product": {
    "name": "",
    "tagline": "",
    "url": "",
    "install_cmd": ""
  },
  "keywords_file": "workspaces/xhs-posting/config/keywords.json",
  "posting": {
    "daily_limit": 1,
    "min_interval_hours": 6,
    "last_posted_at": null
  }
}
```

### 0.3 First-time Configuration Wizard (when file does not exist or browser_id is empty)

**Step 1: Browser Selection**

Run `browser-act browser list`, then:

**When existing browsers are present**: display all browsers (id / name / type / desc / proxy), ask the user which one to use for posting:

```
Existing browsers:

#1  id=xxx  name="xxx"  type=stealth  desc="xxx"  proxy=XX
#2  id=xxx  name="xxx"  type=chrome   desc="xxx"

Select a browser number to use for posting, or enter "new" to create one:
>
```

**When no browsers exist, or user enters "new"**:

1. Load advanced guide: `browser-act get-skills advanced`
2. Ask the user:
   - Browser name (custom, e.g. "xhs-poster")
   - Proxy requirements (needed? region or custom URL?)
3. Create the browser following the advanced guide's Confirmation Gate protocol
4. Record the new browser ID, continue to Step 2

**Step 2: Product & Keyword Configuration**

Ask the user:
1. Product name (brand keyword, used in tags and body)
2. Product tagline (one-sentence description)
3. Product URL (website / GitHub / App Store, etc.)
4. Install / usage command (optional; for SaaS products, enter the core operation path)
5. Initial keywords (1–5, comma-separated, used for topic search)

Write to `workspaces/xhs-posting/session_state.json` and `workspaces/xhs-posting/config/keywords.json`, then continue to Phase 0.4.

### 0.4 Account Safety Check

- Read `posting.last_posted_at` from `session_state.json`
- If less than `min_interval_hours` have passed since the last post, notify the user and ask whether to force continue
- If today's post count ≥ `daily_limit`, notify the user

### 0.5 Browser Launch & Login Verification

Generate a unique session name for this execution:

```
$SESSION = "xhs-<YYYYMMDD>-<HHMM>"   # e.g., xhs-20260611-1430
```

Open the browser using the stored `browser_id`:

```bash
browser-act --session $SESSION browser open <browser_id> https://creator.xiaohongshu.com/new/home
browser-act --session $SESSION wait stable
```

Verify login: check that the current URL stays on `creator.xiaohongshu.com` (not redirected to the login page) and that a user avatar / nickname element is present in state.
- Not logged in → instruct the user to scan the QR code in `--headed` mode:
  ```bash
  browser-act --session $SESSION browser open <browser_id> https://creator.xiaohongshu.com/new/home --headed
  ```
  Wait for the user to confirm login, then continue.

---

## Phase 1 — Pain-Point Topic Collection

Full execution parameters: `references/phase1-topic-collection.md`.

**Overview:**

1. **Keyword rotation**: read the next keyword from `config/keywords.json` (sequential mode)
2. **XHS search**: search the keyword, sort by hottest, collect metadata for the top 10–15 notes
3. **Listing Pass**: extract shallow fields directly from search results (title, likes, collects, comments, snippet)
4. **Engagement scoring**: `score = likes + collects × 2 + comments × 1.5`
5. **Top 5 Deep**: click into the top 5 notes and extract deep fields (key quote, pain description, topic tags)
6. **Generate report**: output `workspaces/xhs-posting/<date>/topics/TOPICS_<kw-slug>.md`
7. **Display Top 5** and wait for user selection

---

## Phase 2 — Top Case Collection (Style Reference)

Full execution parameters: `references/phase2-case-collection.md`.

**Overview:**

1. Use the same search results as Phase 1; no additional request needed
2. Collect full text from the top 3 high-engagement notes (title + body + tags)
3. Analyze writing style: opening type, paragraph rhythm, emoji density, topic tag strategy
4. Generate Style Fingerprint
5. Write style fingerprint to `workspaces/xhs-posting/<date>/style_fingerprint.json`

Phase 2 runs **in parallel with Phase 1** (shared search results, different analysis angle).

---

## Phase 3 — Topic Selection

After displaying the Phase 1 Top 5, ask the user:

```
Here are the Top 5 topics. Which ones do you want to write?
(enter numbers like "1 3"; "all" for all; "skip" to pass today)
>
```

On receiving the reply:

1. Write the selected topic list to `workspaces/xhs-posting/<date>/selected_topics.json`
2. For each selected topic, confirm the publish strategy (publish now / save as draft)

If the user enters "skip" → end this run without advancing `last_index`.

---

## Phase 4 — Content Writing

Full writing guidelines: `references/phase4-writing.md`.

Write one draft per selected topic, **show a preview after each draft and wait for user approval** before moving to the next.

**Writing framework**: Pain resonance → Struggle / attempts → Product discovery → Concrete proof → Call to action

**Hard requirements**:
- Title ≤ 20 characters (must use native setter when writing; see `references/phase5-publish.md §5`)
- Body ≤ 1000 characters, clear paragraphs
- Topic tags: 3–5, covering keyword + product brand + scene term
- Must include a closing CTA (comment / save / follow)

**Pre-Write Gate** (confirm all items before writing begins):
1. `key_quote` extracted from Phase 1 deep pass
2. `pain_description` confirmed from Phase 1
3. `tools_tried` confirmed from Phase 1
4. Product info (name, install command) read from `session_state.json`
5. Style fingerprint (`style_fingerprint.json`) read

After writing, generate an HTML preview (see `references/phase4-writing.md §7`), display it in the conversation, then ask:

```
Preview above. Ready to publish?
- "ok" / "publish" — proceed to Phase 5 publishing
- "edit: <instruction>" — revise per instruction and re-preview
- "draft" — save as draft, do not publish
```

---

## Phase 5 — Publishing

Full execution parameters: `references/phase5-publish.md`.

**Overview:**

1. **Image generation**: use XHS Creator Center's built-in "Text-to-Image" feature to auto-generate a cover (recommended), or read a user-provided local image
2. **Image upload** (external image): two-step upload — `GET permit → PUT file` — to obtain `file_id`
3. **Content Verification Gate**: title ≤ 20 characters, body non-empty, topic tags present
4. **Fill Creator Center**: navigate → paste content → add topics → set cover
5. **Publish**: click the "Publish" button
6. **Capture publish URL**: extract `note_id` from the redirect URL or page
7. **Write record**: update `workspaces/xhs-posting/<date>/published.json`, update `posting.last_posted_at` in `session_state.json`

**Gate**: publish only executes after user approval of the content; auto-publishing unapproved content is not allowed.

---

## Phase 6 — Performance Tracking

Full execution parameters: `references/phase6-tracking.md`.

**Standalone trigger**: when the user says "track performance" / "see data" / similar trigger words, jump directly to this phase.

**Sub-actions:**

| Sub-action | Trigger | Description |
|------------|---------|-------------|
| 6.1 Single post 24h tracking | Auto-scheduled after Phase 5 publish | Revisit note_id 24h later, update initial metrics |
| 6.2 Batch data collection | User trigger / weekly | Pull latest data for all published notes from recent N days |
| 6.3 View comments | User trigger | View new comments, draft replies, reply after user approval |
| 6.4 Generate report | User trigger | Aggregate data, output table report |

Data stored locally in `workspaces/xhs-posting/tracking/`.

---

## Account Safety Rules

1. **Posting frequency**: ≤ 1 post per account per day, ≥ 6 hours between posts
2. **Content originality**: before each publish, check title similarity against historical posts (simple character-level check to avoid exact duplicates)
3. **Avoid sensitive terms**: body and title must not contain WeChat IDs, Weibo handles, contact info, or external links
4. **No artificial engagement**: do not simulate batch likes / collects / comments
5. **Topic tags**: use existing platform topics only; do not create new ones
6. **Image compliance**: use XHS built-in generated images or self-owned copyright images; do not use screenshots from others

---

## Success Criteria

- Phase 1: `candidates >= 10`, `deep-extracted notes = 5`, report file exists
- Phase 2: `style_fingerprint.json` written, `sample_notes count >= 1`
- Phase 4: user explicitly approves draft content
- Phase 5: redirect URL contains `published=true`, `note_id` captured and written to `published.json`
- Phase 6: all tracked note metrics updated without error

## Session Cleanup

After completing the workflow (any phase exit — normal completion, user abort, or error), close the session to release resources:

```bash
browser-act session close $SESSION
```

Do not close if the user explicitly requests to keep the session open for manual inspection.

---

## Known Limitations

- Max 1 post per account per day; minimum 6-hour interval enforced
- `window.__INITIAL_STATE__` hydration timing is inconsistent — retry once after 2 s if empty
- `search/notes` XHR may not appear in all browser fingerprints; fall back to `get markdown` if missing
- Topic chip insertion silently fails after `execCommand` body injection — always embed hashtags directly in body text (see `references/phase5-publish.md §4.3`)
- `note_id` may not be auto-capturable when note is under review; record as `pending_review` and fill in manually later

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/xiaohongshu-auto-posting-xhs-post.memory.md`

**Before execution**: if the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy accordingly.

**After execution**: if an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record which keywords were used or how many results were returned — those are task outputs, not experience.
