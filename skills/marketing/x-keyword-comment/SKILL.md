---
name: x-keyword-comment
description: "X (Twitter) keyword-based reply posting: search tweets by keyword, read each tweet's content, generate contextual replies from a configured brand persona, and post replies to the reply area. Use when user wants to batch reply to X tweets by keyword, auto-comment on X topic tweets, drive traffic via X comments, X comment outreach, search X tweets and leave comments, bulk reply to Twitter search results, keyword comment on Twitter, post replies on X search page, Twitter keyword comment marketing, X reply campaign, engage with X discussions, or comment on tweets matching a topic."
---

# X — Keyword Comment

> keyword + reply intent → search X tweets → read tweet content → generate contextual replies → post to reply area

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Search X by keyword, read each tweet's content, generate contextual replies based on a configured brand persona, and post them — all within a browser-act session.

## Prerequisites

- `config/keyword-comment-config.json` has been filled in with actual product, persona, and tone values (all `YOUR_*` placeholders replaced before first run)

## Session Rule

`{SESSION}` is a temporary, per-run session name used in all `browser-act --session {SESSION}` commands below. It is generated at execution start (e.g., `xkc-{timestamp}`) and not persisted across runs.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current conversation → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Load Config

```bash
python -c "
import json, pathlib, sys
for base in ['.claude/skills/x-keyword-comment', 'output/x-keyword-comment']:
    cfg = pathlib.Path(base) / 'config/keyword-comment-config.json'
    if cfg.exists():
        print(json.dumps(json.loads(cfg.read_text(encoding='utf-8')), ensure_ascii=False, indent=2))
        sys.exit(0)
print('ERROR: config/keyword-comment-config.json not found', file=sys.stderr)
sys.exit(1)
"
```

Hold `product.*`, `persona.*`, `tone.*` fields in working memory for reply composition.

### 3. Browser Selection

List available browsers:

```bash
browser-act browser list
```

- If browsers exist → present the list to the user and let them choose which browser to use for this X session.
- If no browsers exist → guide the user to create one (e.g., `browser-act browser create --type stealth --headed`), then repeat the list step.

Once the user selects a browser, record its ID as `{BROWSER_ID}` for this run.

### 4. Open Session

Generate a unique session name (e.g., `xkc-{timestamp}`) as `{SESSION}`. Open the browser:

```bash
browser-act --session {SESSION} browser open {BROWSER_ID} https://x.com/ --headed
```

If the browser is already open with an active session, list sessions and reuse:

```bash
browser-act session list
```

Pick the session associated with `{BROWSER_ID}` and assign its name to `{SESSION}`.

### 5. Login Verification

If X login status has been confirmed in the current conversation → skip this step.

Otherwise: `browser-act --session {SESSION} get markdown` and check:
- Sidebar bottom shows `@username`, top navigation shows Home / Explore → logged in, continue
- Page shows a "Sign in" button with no logout entry → not logged in; inform the user that login is required and assist the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the logged-in user, never bypassing authentication or access controls. JS code is encapsulated in Python files under `scripts/`, invoked via `browser-act --session {SESSION} eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### AI Workflow: Pre-reply Warmup

Warm up the account before posting replies to simulate organic browsing behavior.

**Skip condition**: warmup already performed today and less than 4 hours ago, or user says "fast mode".

**Step 1 — Check notifications and messages (2–3 min)**

```bash
browser-act --session {SESSION} navigate "https://x.com/notifications"
browser-act --session {SESSION} wait stable
browser-act --session {SESSION} get markdown
sleep $((RANDOM % 31 + 60))   # 60–90 s
browser-act --session {SESSION} navigate "https://x.com/messages"
browser-act --session {SESSION} wait stable
browser-act --session {SESSION} get markdown
sleep $((RANDOM % 31 + 30))   # 30–60 s
```

**Step 2 — Browse feed and like (3–5 min)**

```bash
browser-act --session {SESSION} navigate "https://x.com/home"
browser-act --session {SESSION} wait stable
browser-act --session {SESSION} get markdown
```

Randomly pick 3–5 tweets from the feed. For each:

```bash
browser-act --session {SESSION} navigate "{tweet URL}"
browser-act --session {SESSION} wait stable
sleep $((RANDOM % 26 + 15))   # 15–40 s
# If content is relevant → like it:
browser-act --session {SESSION} state
browser-act --session {SESSION} click {Heart index}   # element with aria-label containing "Like"
browser-act --session {SESSION} wait stable
sleep $((RANDOM % 8 + 8))     # 8–15 s
browser-act --session {SESSION} navigate "https://x.com/home"
sleep $((RANDOM % 16 + 10))   # 10–25 s
```

Target: like 1–3 tweets; daily cap **20–30 likes** (avoid fast bulk likes that trigger rate limits).

**Step 3 — Keyword search browsing (2–3 min)**

```bash
browser-act --session {SESSION} navigate "https://x.com/search?q={KEYWORD_ENCODED}&f=live"
browser-act --session {SESSION} wait stable
browser-act --session {SESSION} get markdown
```

Open 2–3 results, spend 25–60 s each reading the full tweet (as reply material).

**Pre-action pause**

```bash
sleep $((RANDOM % 61 + 60))   # 60–120 s — simulate "browse first, then reply"
```

---

### DOM: Scan Replyable Tweets on Current Page

After navigating to the X search results page, scan all tweets with their reply button indices and content.

1. Navigate: `browser-act --session {SESSION} navigate "https://x.com/search?q={KEYWORD_ENCODED}&src=typed_query&f=live"`
   - `{KEYWORD_ENCODED}` is URL-encoded (spaces as `%20`)
   - `f=live` returns newest tweets; omit for Top tweets
2. Wait: `browser-act --session {SESSION} wait stable --timeout 30000`
3. (Optional) Scroll to load more: `browser-act --session {SESSION} scroll down --amount 1500` → `browser-act --session {SESSION} wait stable --timeout 10000` → re-scan
4. Scan: `browser-act --session {SESSION} eval "$(python scripts/scan-search-tweets.py --limit {N})"`

Parameters:
- `--limit`: max tweets to return, default `10`

Output example:
```json
{
  "totalReplyBtns": 8,
  "tweets": [
    {
      "i": 0,
      "tweetSnippet": "Breaking: Alibaba just killed the browser automation stack...",
      "authorHandle": "@AIGuideHQ",
      "authorUrl": "https://x.com/AIGuideHQ",
      "tweetUrl": "https://x.com/AIGuideHQ/status/2051969984847286536",
      "replyBtnIdx": 0
    }
  ]
}
```

> **`replyBtnIdx` note**: This is the reply button's position index among all `[data-testid="reply"]` buttons currently on the page. After posting a reply, the DOM partially updates (new reply inserts), shifting subsequent indices — **re-run `scan-search-tweets.py` after each reply to get fresh indices before the next one**.

### DOM: Click Reply Button (Open Editor)

Click the reply button for a specific tweet to open the reply input box.

`browser-act --session {SESSION} eval "$(python scripts/click-reply.py {replyBtnIdx})"`

Parameters:
- `{replyBtnIdx}`: the tweet's reply button index (positional argument, from `scan-search-tweets.py`)

Output example (success):
```json
{
  "ok": true,
  "replyBtnFound": true,
  "totalReplyBtns": 8
}
```

Output example (out of range):
```json
{
  "ok": false,
  "reason": "reply_btn_out_of_range",
  "total": 8
}
```

### DOM: Type Reply Text and Submit (Operation)

> **Architecture note**: X uses the Draft.js editor (`public-DraftEditor-content`). `document.execCommand('insertText')` only updates the DOM without triggering React internal state — the submit button stays disabled. You **must** use browser-act's native `input` command to simulate real keyboard input to activate the submit button. This is the only reliable method.

After clicking the reply button (`click-reply.py`), complete text input and submission:

1. Wait for editor mount: `browser-act --session {SESSION} wait --selector '[data-testid="tweetTextarea_0"]' --state attached --timeout 10000`
2. Get editor index: `browser-act --session {SESSION} state` → find `aria-label=Post text role=textbox` → note `{EDITOR_IDX}`
3. Input reply text: `browser-act --session {SESSION} input {EDITOR_IDX} '{reply_text}'`
4. Get submit button index: `browser-act --session {SESSION} state` → find button labeled `Reply` → note `{REPLY_BTN_IDX}`
5. Submit: `browser-act --session {SESSION} click {REPLY_BTN_IDX}`
6. Wait: `browser-act --session {SESSION} wait stable --timeout 10000`

Success signal: `browser-act --session {SESSION} network requests --filter CreateTweet --method POST --status 200` returns at least 1 record.

> **Closing the editor**: If the editor is empty, pressing Escape dismisses it directly with no dialog. If text has been typed and Escape is pressed (or the modal is otherwise closed), X shows a "Save post?" confirmation dialog (Save / Discard). To discard: `browser-act --session {SESSION} state` → find `Discard` button index → `browser-act --session {SESSION} click {DISCARD_IDX}`

### Composite: Full Keyword Reply Flow

> All operations remain on the X search page — no navigation to individual tweet detail pages required.

**Config**: Load `config/keyword-comment-config.json` and hold `product.*`, `persona.*`, `tone.*` fields in working memory before proceeding:

```bash
python -c "
import json, pathlib, sys
for base in ['.claude/skills/x-keyword-comment', 'output/x-keyword-comment']:
    cfg = pathlib.Path(base) / 'config/keyword-comment-config.json'
    if cfg.exists():
        print(json.dumps(json.loads(cfg.read_text(encoding='utf-8')), ensure_ascii=False, indent=2))
        sys.exit(0)
print('ERROR: config/keyword-comment-config.json not found', file=sys.stderr)
sys.exit(1)
"
```

1. `browser-act --session {SESSION} navigate "https://x.com/search?q={KEYWORD_ENCODED}&src=typed_query&f=live"` → `browser-act --session {SESSION} wait stable --timeout 30000`
2. Initial scan: `browser-act --session {SESSION} eval "$(python scripts/scan-search-tweets.py --limit {N})"` → candidate tweet list
3. If not enough candidates → `browser-act --session {SESSION} scroll down --amount 1500` → `browser-act --session {SESSION} wait stable --timeout 10000` → re-scan, merge results
4. Filter candidates by `authorUrl` / `tweetSnippet` (skip promotional or low-relevance tweets)
5. For each target tweet:
   - a. **Generate reply**: Use `intent` (caller-provided) + `tweetSnippet` + `authorHandle` + loaded config (`product.*`, `persona.*`, `tone.*`) to compose a 60–180 character ASCII reply. See `references/quality-checklist.md` (7-item checklist) and `references/reply-composition.md` (3 recommendation scenarios A/B/C).
   - b. `browser-act --session {SESSION} eval "$(python scripts/click-reply.py {replyBtnIdx})"` → open reply box
   - c. `browser-act --session {SESSION} wait --selector '[data-testid="tweetTextarea_0"]' --state attached --timeout 10000`
   - d. `browser-act --session {SESSION} state` → get editor index `{EDITOR_IDX}` → `browser-act --session {SESSION} input {EDITOR_IDX} '{reply_text}'`
   - e. `browser-act --session {SESSION} state` → get `Reply` button index `{REPLY_BTN_IDX}` → `browser-act --session {SESSION} click {REPLY_BTN_IDX}`
   - f. `browser-act --session {SESSION} wait stable --timeout 10000`
   - g. Verify: `browser-act --session {SESSION} network requests --filter CreateTweet --method POST --status 200`
   - h. Random interval: `sleep $((60 + RANDOM % 120))` (60–180 s between replies)
   - i. **Re-scan after each reply**: re-run `scan-search-tweets.py` to refresh `replyBtnIdx` values before the next reply

Output per tweet:
```json
{
  "authorUrl": "https://x.com/AIGuideHQ",
  "tweetUrl": "https://x.com/AIGuideHQ/status/2051969984847286536",
  "tweetSnippet": "Breaking: Alibaba just killed the browser automation stack...",
  "replyText": "The captcha point is real -- Playwright + Cloudflare means more glue than logic...",
  "posted": true,
  "skippedReason": null
}
```

## Pagination

**DOM Pagination**: Search results load as an infinite scroll. Trigger more: `browser-act --session {SESSION} scroll down --amount 1500` → `browser-act --session {SESSION} wait stable --timeout 10000` → re-scan. Termination: `totalReplyBtns` does not increase across 2 consecutive scrolls, or target reply count is reached.

## Success Criteria

`posted == true` for each tweet, confirmed by `browser-act --session {SESSION} network requests --filter CreateTweet --method POST --status 200` returning at least 1 record (editor disappearing after submission is a secondary signal only).

## Known Limitations

- **Windows non-ASCII encoding trap**: `browser-act input {idx} '{text}'` on Windows cmd (GBK active codepage) will corrupt non-ASCII characters (em-dash, full-width quotes, emoji) passed as arguments. Scripts call `sys.stdout.reconfigure(encoding='utf-8', newline='\n')`. Callers must also ensure UTF-8 terminal: run `chcp 65001` or `set PYTHONUTF8=1`, or restrict reply text to **ASCII-only characters**
- **Draft.js editor rejects execCommand**: `document.execCommand('insertText')` only updates the DOM without triggering React state — submit button stays disabled. Must use browser-act native `input` command
- **`replyBtnIdx` is not stable**: After each reply the DOM partially updates; the new reply may insert near the top, shifting all subsequent indices. Must re-scan before every reply
- **Reply rate**: X's CreateTweet API rate limit is 300/15min, but account-level risk controls are far stricter. Over 20 replies/hour risks rate limiting, verification prompts, or suspension. Recommended: 60–180 s between replies, max 50 replies/day per account
- **Account weight**: Accounts with no avatar, no bio, few followers (< 50), and no post history may have replies silently shadow-banned
- **Duplicate content filter**: Sending identical or similar replies in a short window is automatically intercepted
- **"Save post?" dialog**: Pressing Escape with text in the editor triggers a save confirmation; must click Discard to close
- **Platform ToS**: X's Terms of Service explicitly restrict automated behavior; accounts risk rate limiting, warnings, or permanent suspension

## Execution Efficiency

- **Batch orchestration**: For small counts (< 3) invoke directly; for larger counts write a bash loop script. **Do not parallelize** — rate limits apply per account
- **Test before batch**: Run the full flow (scan → post reply → verify CreateTweet) for 1 tweet first; only run the full batch after confirming it works
- **Re-scan after each reply**: `replyBtnIdx` changes with DOM updates; must re-run `scan-search-tweets.py` after every reply
- **Error resumption**: Save result per tweet (`posted` status + `tweetUrl` + `tweetSnippet` hash) incrementally; on failure, resume from breakpoint
- **Interval jitter**: 60–180 s random interval between replies
- **Stop on risk signals**: Immediately stop on: identity verification prompt, reply buttons disappearing, "You've reached your reply limit" message, or any suspension warning

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-keyword-comment-x-keyword-comment.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
