---
name: baoyu-wechat-summary
description: Summarizes WeChat group chat highlights into a structured digest using the local wx-cli binary (https://github.com/jackwener/wx-cli). Generates a normal digest by default; a roast (毒舌) version is opt-in. Maintains per-group history (history.json + history-digests.jsonl) and per-user profiles across runs, with privacy guardrails baked in. Use when the user asks to "总结群聊", "群聊精华", "群聊摘要", "summarize group chat", "group chat digest", mentions a WeChat group name with a time range, says "帮我看看 XX 群最近聊了什么", "XX 群有什么值得看的", or asks to "回溯画像" / "初始化画像" / "backfill profiles". Adds the roast version when the user says "毒舌版", "roast 版", "再来个毒舌的", or similar.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-wechat-summary
    requires:
      anyBins:
        - wx
---

# WeChat Group Summary

群聊精华提取专家。把零散的微信群聊记录提炼成结构化、可读性强的简报，并维护跨次运行的群聊历史与群友画像。底层依赖外部 [wx-cli](https://github.com/jackwener/wx-cli) 二进制（`wx` 命令），不打包脚本。

> **⚠️ Sandbox restriction**
>
> wx-cli reads from `~/.wx-cli/` (config, cache, daemon socket) and from WeChat's data directory (`~/Library/Containers/com.tencent.xinWeChat/` on macOS). Both paths are outside Claude Code's default sandbox. Every `wx` command in this skill needs to run with `dangerouslyDisableSandbox: true` from the start — don't waste a sandbox attempt first. The user can use `/sandbox` to view/edit restrictions.

## User Input Tools

When this skill prompts the user, follow this tool-selection rule (priority order):

1. **Prefer built-in user-input tools** exposed by the current agent runtime — e.g., `AskUserQuestion`, `request_user_input`, `clarify`, `ask_user`, or any equivalent.
2. **Fallback**: if no such tool exists, emit a numbered plain-text message and ask the user to reply with the chosen number/answer for each question.
3. **Batching**: if the tool supports multiple questions per call, combine all applicable questions into a single call; if only single-question, ask them one at a time in priority order.

Concrete `AskUserQuestion` references below are examples — substitute the local equivalent in other runtimes.

## Prerequisites

Before invoking the workflow, verify the environment. Run these checks in order; stop at the first failure and surface the exact next command the user needs.

1. **wx-cli installed** — run `wx --version`. If missing, tell the user to install it themselves (`npm install -g @jackwener/wx-cli` or use one of the alternatives at https://github.com/jackwener/wx-cli). **Do NOT auto-install** — this repo forbids piped/silent installs.
2. **`~/.wx-cli` directory owned by the current user** — `sudo wx init` historically chowned this directory to root, which breaks every subsequent non-sudo `wx` call. Check:
   ```bash
   ls -la ~/.wx-cli/ 2>/dev/null | head -5
   ```
   If the directory exists but the owner is `root` (or anything other than `$(whoami)`), tell the user to repair it themselves:
   ```bash
   sudo chown -R $(whoami) ~/.wx-cli
   sudo rm -f ~/.wx-cli/daemon.pid ~/.wx-cli/daemon.sock
   wx daemon start
   ```
   The skill should NOT run `sudo` on the user's behalf.
3. **wx-cli initialized** — `wx sessions` should return data. If it fails with "no keys" / "init required", instruct the user to run `wx init` while WeChat is running (on macOS, `codesign --force --deep --sign - /Applications/WeChat.app` first). Prefer non-sudo init; only fall back to `sudo wx init` if the user's wx-cli version requires it — and warn them that they'll need step 2's chown after.
4. **WeChat 4.x running and logged in** — required for the daemon to find data files.

## Preferences (EXTEND.md)

Check EXTEND.md in priority order — the first one found wins:

| Priority | Path | Scope |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-wechat-summary/EXTEND.md` (relative to project root) | Project |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-wechat-summary/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-wechat-summary/EXTEND.md` | User home |

| Result | Action |
|--------|--------|
| Found | Read, parse, apply. On first use in session, briefly remind: "Using preferences from [path]. Edit it to change defaults." |
| Not found | **MUST** run first-time setup (BLOCKING) before generating any digest — do NOT silently use defaults. |

### Supported keys

EXTEND.md is plain text with `key: value` or `key=value` lines, `#` for comments, case-insensitive keys.

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `self_wxid` | string | (required) | The owning account's wxid. Messages whose `from_wxid` matches this are attributed to the user. |
| `self_display` | string | (required) | Display name to substitute for the user's own messages in digest text. |
| `default_version` | `normal` / `roast` / `both` | `normal` | Which version(s) to generate when the user doesn't say otherwise. |
| `default_time_range` | string (e.g. `7d`, `24h`, `1d`) | (none) | Default range when the user omits time and there's no incremental anchor. |
| `data_root` | path | `{project_root}/wechat` | Override where digest folders live. |

A starter template lives at [EXTEND.md.example](EXTEND.md.example).

### First-Time Setup (BLOCKING)

If no EXTEND.md is found, do NOT silently proceed.

**Step A — Try to auto-discover `self_wxid` and `self_display` first.** Run (in order, stop at the first that succeeds):

```bash
# 1. If wx-cli exposes a whoami, use it
wx whoami --json 2>/dev/null

# 2. Otherwise, find self-sent messages in recent sessions
wx sessions --json --limit 20 2>/dev/null
```

For option 2, scan the sessions for any private/group thread the user has sent into and read one of their own `from_wxid` / `from_nickname` pairs. If you can confidently pre-fill both values, use them as defaults in the question below; otherwise leave the fields blank for the user to fill in.

**Step B — Confirm with one `AskUserQuestion` call (batched), pre-filling whatever auto-discovery found:**

- `self_wxid` (e.g., `wxid_abc123`) — fall-back hint: the user can find it with `wx contacts --query "<own nickname>"`, or by inspecting any of their own sent messages in `wx sessions --json`
- `self_display` (e.g., `宝玉`) — how they want their messages attributed
- `default_version` — pick one of `normal` / `roast` / `both`
- `data_root` — where digest folders live. Default: `{project_root}/wechat`. Enter a custom absolute path (e.g. `~/Documents/wechat-digests`) or leave blank for default.
- Save location — pick one of project / XDG / home

Write EXTEND.md to the chosen path. If the user provided a non-default `data_root`, include it as an uncommented line; otherwise omit it (the default applies automatically). Confirm "Preferences saved to [path]. Edit it any time to change defaults.", then continue with the digest workflow.

## Workflow

### Step 1: Parse the user's request

Extract:

- **Group name** (or partial name for fuzzy matching)
- **Time range** — interpret flexibly:
  - "最近 1 天" / "今天" / "last 24 hours" → 1 day
  - "最近 3 天" → 3 days
  - "最近 7 天" / "这周" → 7 days
  - "最近 30 天" / "最近一个月" → 30 days
  - "某天" (e.g. "3 月 5 号") → that specific date
  - "某天到某天" (e.g. "3 月 1 号到 3 月 5 号") → date range
  - "从上次开始" / "继续" / "接着上次" / "since last" → **incremental mode**: read `history.json` for this group, use `last_digest.last_message_time` as the start
  - No time specified → **incremental mode**. If no `history.json` exists yet, fall back to `default_time_range` from EXTEND.md if set, else last 24 hours.
- **Version(s) to generate**:
  - Start from `default_version` in EXTEND.md.
  - User request overrides: keywords "毒舌"/"roast"/"挑衅"/"再来个毒的"/"sass" → force `include_roast=true`. Keywords "只要正经的"/"normal only"/"不要毒舌" → force `include_normal=true, include_roast=false`. "都来一份"/"两个版本都要"/"both" → both.
  - At least one of `include_normal`/`include_roast` must end up true.

Convert relative ranges into absolute `--since YYYY-MM-DD --until YYYY-MM-DD` pairs using today's local date.

### Step 2: Find the group + resolve folder path

```bash
wx contacts --query "<group_name>" --json
```

Filter for entries whose `username` ends in `@chatroom`. If multiple groups match, use `AskUserQuestion` to disambiguate. If none match, fall back to `wx sessions --json` and search there before asking the user.

Once resolved, compute the folder path:

```
{data_root}/{group_id}-{sanitized_group_name}/
```

where `data_root` is from EXTEND.md (default `{project_root}/wechat`).

**Sanitize the group name** — replace any of `/ \ : * ? " < > | NUL` and control characters with `_`. Trim trailing dots and whitespace. Don't strip emoji or Chinese characters.

**Group-rename detection**: list existing folders under `{data_root}/` and find any folder whose name starts with `{group_id}-`. If one exists but the suffix differs (group was renamed), rename the existing folder to the new `{group_id}-{sanitized_new_name}` form. If a target with the new name already exists (rare), keep both and prefer the existing one for this run.

### Step 3: Fetch messages

For small batches (single-day digest, typically < 200 messages), pipe JSON into the agent directly:

```bash
wx history "<group_name_or_id>" --since YYYY-MM-DD --until YYYY-MM-DD -n 5000 --json
```

For **large batches** (weekly / monthly digests, > 200 messages), redirect to `$TMPDIR` first so the raw payload never sits in conversation context:

```bash
wx history "<group_name_or_id>" --since YYYY-MM-DD --until YYYY-MM-DD -n 5000 --json > "$TMPDIR/wx-messages.json"
wc -c "$TMPDIR/wx-messages.json"
jq 'length' "$TMPDIR/wx-messages.json"
```

Then read the file in slices via `Read` with `offset` + `limit`, or process with `jq` queries (e.g. `jq '.[0:200]'`, `jq '[.[] | {id, from_nickname, timestamp, content: (.content | .[0:50])}]'` for a lightweight skeleton pass). Reading all 500+ messages at once will burn token budget unnecessarily.

Notes:

- `--since` is inclusive; `--until` is interpreted as a date (the whole day). If the user asked for "today only", set both to today.
- `-n 5000` is a defensive cap; for very active groups, raise it and re-fetch.
- Filter the returned messages by their `timestamp` to be safe (some daemons may return adjacent days).
- **Range splitting**: for ranges > 7 days OR > 500 messages, prefer generating per-3-day digests and then a meta-summary over forcing one giant digest — the categorization quality degrades sharply past a week's worth of unrelated topics.

**Incremental mode**: after the fetch, drop any message whose `timestamp` is `<=` the `last_message_time` from `history.json`. If zero messages remain, tell the user "上次摘要后没有新消息，已跳过生成" and exit.

### Step 3.5: Parse the message schema

`wx history --json` returns an array of message objects. Use the fields that are present; tolerate missing fields:

- **`id` / `msg_id` / `local_id`** — message identifier (use whichever wx-cli emits). Reference IDs in working notes as anchors when building the skeleton.
- **`from_wxid`** — stable sender identifier
- **`from_nickname`** — display name (may be the group remark or original nickname)
- **`content`** — text payload. Examples:
  - Plain text → use as-is
  - `[图片]` → opaque placeholder; see image handling below
  - `[表情]` → emoji/sticker; skip in body unless surrounded by discussion
  - `[视频]` / `[文件]` → media reference; skip unless discussed
  - `[链接] <title>` or `[链接/文件] <title>` → shared article; the title IS the information — quote it and credit the sharer
  - `[系统] ... revokemsg` → revoked; exclude from digest and from leaderboard
- **`timestamp`** — convert to `MM-DD HH:MM` for display (and use full ISO for `generated_at`)
- **`chat_type`** — sanity-check `group`
- **Quote/reply** — try `quote_id`, `reply_to`, `quoted_msg_id`, or any nested `quote` object. If present, use it as strong attribution. If absent, fall back to context but flag the inferred link as uncertain.

### Step 3.6: Resolve self + ambiguous nicknames

- Substitute `self_display` for every message whose `from_wxid` matches `self_wxid` (from EXTEND.md). Apply this in the leaderboard, portraits, and body text. The user MUST appear under their real display name and count toward stats — never skip them.
- Scan all unique senders for ambiguous handles: ≤2 characters, common programming words (`nil`, `null`, `test`, `admin`, `user`, `undefined`), single emoji, or otherwise low-information. For each, run `wx contacts --query "<nick>" --json --limit 5` and pick a meaningful name in this priority: remark > nickname > wxid. Apply the substitution everywhere in the digest.

### Step 3.7: Load user profiles

For each unique sender appearing in this batch:

- Look in `{folder}/profiles/{wxid}-*.md` by `wxid` prefix match. Read the matched file if found.
- If `include_roast`, **also** look in `{folder}/profiles-roast/{wxid}-*.md` for the roast pass.

Compile a condensed **profile context block** as internal working memory — do NOT write it into the final digest. Example shape:

```
== 群友历史画像（来自 profiles/）==
K. H：空中直播员 / 生活百科全书。常见话题：旅行、金融、美食。经典金句："要不要买moderna"。
可可苏玛：...
```

Rules:

- Only load profiles for users active in this batch — never preload everyone.
- Profile is **background**, not template. Current messages are still the primary source.
- Use historical labels for **continuity** ("又双叒叕化身空中直播员") or **contrast** ("一向省钱的 XX 今天居然...").
- **Strict separation**: normal pass reads only `profiles/`, roast pass reads only `profiles-roast/`. Never cross-load.

See [references/profiles.md](references/profiles.md) for the full file format.

### Step 3.8: Detect existing in-chat digests (optional)

Some users (e.g., the original 宝玉 workflow) post digests directly into the group as messages. If we don't notice these, the new digest will re-cover the same ground.

Scan the fetched messages for signals of a prior in-chat digest:

- `from_wxid == self_wxid` AND
- `content` contains `群聊精华` OR `消息统计:` OR `📊 消息统计` OR a leaderboard pattern (e.g. `^\d+\. .+: \d+ 条`), AND
- `content` length > 1500 chars.

If a match is found:

1. Extract the digest's covered date or range from the title line (e.g., `xxx 群聊精华 · 2026-05-12` or `... · 2026-05-10 ~ 2026-05-12`).
2. Surface the finding to the user via `AskUserQuestion`:
   - "Detected an in-chat digest by you covering {范围}. Use {范围 end + 1} as the start instead of `history.json`?"
   - Options: `Yes, skip up to {end of detected range}` / `No, use history.json` / `No, cover everything in the requested range`.
3. Apply the chosen anchor.

This is a heuristic — when uncertain (multiple matches, malformed title), default to `history.json` and tell the user what was skipped.

Generate the digest in three rounds so nothing slips through. The methodology stays here in SKILL.md; the content/style rules live in [references/output-formats.md](references/output-formats.md) — read that file in Round 2 before drafting.

#### Round 1 — Build the skeleton

Read every message in order. **Skip image fetching/decoding** in this round. List every distinct discussion topic. Bias toward over-listing — trim in Round 3.

Internal working format (not written to the final file):

```
== 话题清单（共 N 条消息）==
1. [HH:MM-HH:MM] 话题名称（参与者：A, B, C）— 一句话概括（锚点 id：54052, 54055, 54063）
2. [HH:MM-HH:MM] 话题名称（参与者：D, E）— 一句话概括（锚点 id：54100-54112）
...

== 可能需要图片上下文的话题 ==
- 话题 3：锚点 id=49661（图片是讨论主体）

== 发言统计 ==
1. XXX — N 条  2. YYY — N 条  ...
```

Topic principles:

- Topic-switch signals: time gap > 30 min, participant change, content jump.
- 2+ participants OR substantive content qualifies as a topic; pure emoji-banter does not.
- **Strict attribution**: each topic must record "who said what". Don't fuse adjacent messages from different senders just because they're close in time — when minutes apart or interleaved with others, split into separate topics. Prefer two topics over one wrongly-merged topic.
- **Carry anchor IDs**: list the key message IDs for each topic. In Round 2, jump back to these IDs in the raw messages and verify content, don't guess from context. If `quote_id` / `reply_to` is present, use the ID chain — that's the most reliable attribution.

**Flag-for-images criteria** (any one triggers): an explicit comment on an image (`看发型是X？`, `这是谁？`, `笑死`), multiple people piling onto the same image without saying what it is, an image as the core information (晒单/截图/资料), an explanatory line right after an image (`gpt-image-2`, `太可怕了`), or cross-sender ambiguity (B says "这个看着像 X" but the previous image is from A).

#### Round 2 — Flesh out + write the digest

For each topic in the skeleton, jump back to its anchor IDs and expand into full content with quotes and clear attribution. Then write the digest file.

**Image handling** (limited — wx-cli does not decode chat images):

For each flagged topic, check whether a description file already exists at `{folder}/imgs/{message_id}.txt`. If yes, read it (one-line plain text) and weave its content into the topic. If no, treat the image as opaque (`[图片]`) and write around it — describe what the surrounding messages tell us, but don't invent visual content.

The `imgs/` directory exists as an **extension point**: a user (or a future wx-cli capability) can drop `{message_id}.txt` files with one-line descriptions, and the skill will pick them up. The skill itself does NOT generate these files in this version.

**Use the profile context block** (from Step 3.7):

- Echo continuity for matching behavior ("又双叒叕直播飞行体验")
- Highlight contrast for departures ("一向话少的 XX 今天突然爆发")
- Callback past quotes ("继上次'要不要买 moderna'之后，这次又...")
- Don't sacrifice current material to force a callback.

**Writing order**: write the body categories first, then the opening overview based on the finished body (so the hook is accurate).

Detailed structure, voice, formatting rules, and content guidelines are in [references/output-formats.md](references/output-formats.md). Load that file now if not already loaded.

#### Round 3 — Audit

Walk the Round 1 skeleton against the finished digest. Check:

- Any listed topic missing from the digest?
- Quotes, names, product/tool names preserved verbatim?
- Categorization makes sense — is anything in the wrong bucket?

Fix in place. When clean, confirm and proceed.

### Step 7: Save the digest file(s)

If `include_normal`:

- Single date → `{folder}/YYYY-MM-DD.md`
- Date range → `{folder}/YYYY-MM-DD_YYYY-MM-DD.md`
- Overwrite if the same date/range already exists.

If `include_roast`:

- Same naming, but with `-roast` suffix: `YYYY-MM-DD-roast.md` or `YYYY-MM-DD_YYYY-MM-DD-roast.md`.

Both versions share the same statistics (message count, leaderboard) and the same underlying skeleton.

### Step 8: Save history (two files)

Maintain two files in the group folder:

#### `history.json` — single record, fast read

Always reflects only the most recent normal digest. Overwrite on each run when `include_normal=true`.

```json
{
  "group_id": "12345678901@chatroom",
  "group_name": "相亲相爱一家人",
  "folder": "12345678901@chatroom-相亲相爱一家人",
  "last_digest": {
    "file": "2026-03-12.md",
    "date_range": "2026-03-12",
    "generated_at": "2026-03-12T10:30:00+08:00",
    "message_count": 150,
    "last_message_time": "03-12 18:45"
  }
}
```

- `group_name` updates on every run (handles renames).
- `folder` records the current folder basename for cross-reference.
- `last_message_time` is the timestamp of the most recent message included, in `MM-DD HH:MM` — used by incremental mode.
- Roast-only runs do NOT touch this file.

#### `history-digests.jsonl` — append-only archive

One JSON object per line, same shape as `last_digest`. Every normal-version run appends one line (in chronological order). Used by backfill and historical lookups. Never read for incremental mode (which only needs the latest).

```jsonl
{"file":"2026-03-10.md","date_range":"2026-03-10","generated_at":"2026-03-10T09:00:00+08:00","message_count":420,"last_message_time":"03-10 22:30"}
{"file":"2026-03-11.md","date_range":"2026-03-11","generated_at":"2026-03-11T09:05:00+08:00","message_count":312,"last_message_time":"03-11 23:10"}
{"file":"2026-03-12.md","date_range":"2026-03-12","generated_at":"2026-03-12T10:30:00+08:00","message_count":150,"last_message_time":"03-12 18:45"}
```

If a normal digest with the same `file` name is regenerated, append a new line anyway (the JSONL is a strict log; readers can dedupe by `file` if they need to).

### Step 8.5: Update user profiles

For each user with 3+ messages in this batch who appeared in the 群友画像 section:

- If `include_normal`, update `{folder}/profiles/{wxid}-{nickname}.md`.
- If `include_roast`, update `{folder}/profiles-roast/{wxid}-{nickname}.md`.

Counts, frontmatter updates, append-only rules for quotes and events, and privacy guardrails are detailed in [references/profiles.md](references/profiles.md). Load that file when running this step.

### Completion checklist

Profile updates are easy to forget once the digest is on disk. Before reporting the run as "done", verify every applicable file:

- [ ] `{folder}/YYYY-MM-DD.md` written (if `include_normal`)
- [ ] `{folder}/YYYY-MM-DD-roast.md` written (if `include_roast`)
- [ ] `{folder}/history.json` overwritten with the new `last_digest` (if `include_normal`)
- [ ] `{folder}/history-digests.jsonl` appended one line (if `include_normal`)
- [ ] `{folder}/profiles/{wxid}-*.md` updated for every user with 3+ messages (if `include_normal`)
- [ ] `{folder}/profiles-roast/{wxid}-*.md` updated for every user with 3+ messages (if `include_roast`)

If any item is unchecked, finish it before declaring success. Don't ship a digest with a stale `history.json` — incremental mode depends on it.

### Step 9: Backfill (user-triggered)

When the user says "回溯画像" / "初始化画像" / "backfill profiles":

1. Confirm the target group (if not specified, ask which one).
2. List all digest files in `{folder}/` and `history-digests.jsonl`.
3. Read existing digests in batches of 10–15 to avoid context blowup.
4. For users appearing in 3+ digests, seed profile files using their leaderboard counts, portrait paragraphs, and quoted lines from the historical digests.
5. Write to `profiles/` (and `profiles-roast/` if any `-roast.md` files exist).
6. Report back: how many profiles were created, how many users covered.

Full procedure in [references/profiles.md](references/profiles.md).

## Storage layout

```
{data_root}/                                        # default: {project_root}/wechat/
└── {group_id}-{group_name}/                        # e.g. 12345678901@chatroom-相亲相爱一家人/
    ├── history.json                                # last digest pointer (fast)
    ├── history-digests.jsonl                       # append-only archive
    ├── 2026-03-12.md                               # normal digest, single date
    ├── 2026-03-12-roast.md                         # roast digest (only if generated)
    ├── 2026-03-10_2026-03-12.md                    # normal digest, date range
    ├── profiles/                                   # normal user profiles
    │   ├── onlytiancai-胡浩🐸.md
    │   └── ...
    ├── profiles-roast/                             # roast user profiles (only if any roast generated)
    │   ├── onlytiancai-胡浩🐸.md
    │   └── ...
    └── imgs/                                       # optional image-description files
        ├── 49661.txt                               # one-line plain text description
        └── ...
```

## wx-cli quick reference

| Command | Purpose |
|---------|---------|
| `wx --version` | Sanity-check that wx-cli is installed |
| `wx sessions --json` | List recent sessions; useful for verifying init and finding the user's own wxid |
| `wx contacts --query "<name>" --json` | Fuzzy-match contacts/groups by display name, remark, or wxid |
| `wx history "<group>" --since DATE --until DATE -n N --json` | Pull a group's messages within a date range as JSON |
| `wx members "<group>" --json` | List a group's members (rarely needed; mostly for completeness) |
| `wx stats "<group>" --since DATE` | wx-cli's built-in stats; we compute our own from `wx history` JSON so the format matches our digest |
| `wx daemon status` / `wx daemon stop` / `wx daemon logs --follow` | Daemon lifecycle (troubleshooting) |

All `wx` commands accept `--json` for machine-readable output. Default output is YAML — only use it for human eyeballing during debugging.

## Troubleshooting

When a `wx` command fails, diagnose by the symptom, not by retrying blindly. Common patterns:

| Symptom | Cause | Fix (tell the user to run these — do NOT run `sudo` for them) |
|---------|-------|----------------------------------------------------------------|
| `Operation not permitted` / `Access denied to ~/.wx-cli` | Sandbox is on | Re-run the command with `dangerouslyDisableSandbox: true`. Persistent fix: `/sandbox` to allow `~/.wx-cli` and the WeChat data dir. |
| `无法写入 /Users/<u>/.wx-cli` / `Permission denied` | `~/.wx-cli` is owned by root (legacy `sudo wx init`) | `sudo chown -R $(whoami) ~/.wx-cli && sudo rm -f ~/.wx-cli/daemon.{pid,sock} && wx daemon start` |
| `wx history` hangs / times out / returns nothing | Daemon is stuck | `wx daemon stop && rm -f ~/.wx-cli/daemon.{pid,sock} && wx daemon start`, then retry |
| `no keys` / `init required` after the daemon was working | Keys went stale (WeChat restart, version upgrade) | Make sure WeChat is running, then `wx init --force` (non-sudo first; only `sudo` if your wx-cli version requires it) |
| `wx contacts` returns zero rows for a group you know exists | Group is folded into 折叠群 or the daemon hasn't indexed it yet | `wx sessions --json` and search there; if missing, run `wx daemon stop && wx daemon start` and retry |
| Messages returned but `--since` / `--until` window looks wrong | Date string not in `YYYY-MM-DD` format, or off-by-one timezone | Confirm the dates are local-time `YYYY-MM-DD`. Re-filter the JSON by `timestamp` locally as a belt-and-suspenders step. |
| Empty result for a chat that should have activity | `-n` cap too low for a noisy group | Raise `-n` (e.g. to 20000) and re-fetch |

**Recovery order when nothing makes sense:**

1. Is WeChat running?
2. Is `~/.wx-cli` owned by `$(whoami)`?
3. Is the daemon healthy? (`wx daemon status`)
4. Restart the daemon (`wx daemon stop && wx daemon start`)
5. Last resort: `wx init --force` (while WeChat is running)

Never auto-retry inside the skill — every failure should produce a clear diagnostic plus the exact command the user needs to run.

## Notes and limitations

- **Image content is opaque**. wx-cli does not decode chat images. The skill respects an `imgs/{message_id}.txt` extension point but does not auto-populate it. When a topic depends heavily on an image with no description file, the digest should say so honestly rather than invent visual content.
- **Reply attribution is best-effort**. If wx-cli's output exposes a quote/reply field, use it. Otherwise fall back to context and flag uncertain inferences in working notes.
- **Local time only**. Date parsing uses the agent's local time zone. Cross-time-zone group members may show timestamps that don't match their wall clock. Per the format rules, never use timestamps to infer sleep or location.
- **wx-cli reinit**. If `wx history` suddenly returns nothing after a WeChat restart, the keys may be stale. Tell the user to run `sudo wx init --force` (while WeChat is running) and retry.
