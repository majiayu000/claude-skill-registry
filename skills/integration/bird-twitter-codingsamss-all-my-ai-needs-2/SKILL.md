---
name: bird-twitter
description: "Default X/Twitter read skill for this environment (browser login session via Bird CLI). Prefer this for reading tweets/timelines/search/bookmarks/trending. Actions: read tweets, search, view bookmarks, trending, news, timeline, mentions, lists. Keywords: twitter, x, tweet, trending, bookmarks, timeline."
---

# Bird Twitter Skill (Read-Only)

Read X/Twitter content using the Bird CLI tool. This skill only exposes read-only operations to avoid account suspension risks.

Default routing note for this machine:
- If user asks to read/search/browse X content, ALWAYS try this skill first.
- Do NOT default to `curl` scraping, third-party mirrors (fx/vx/nitter), or ad-hoc HTTP parsing when Bird is available.
- Use `xitter` only when official API or write actions are explicitly needed.
- Only fall back to non-Bird methods if Bird auth/command execution is unavailable, and explicitly state the fallback reason.

## When to Use This Skill

Triggered by:
- "read tweet [id/url]", "show tweet [id/url]"
- "search twitter [query]", "search x [query]"
- "my bookmarks", "twitter bookmarks"
- "trending", "twitter trends", "what's trending"
- "twitter news", "x news"
- "timeline", "i/timeline", "通知时间线", "device follow"
- "for you", "home", "home timeline", "首页推荐"
- "following", "following timeline", "首页关注流"
- "user timeline [username]", "timeline [username]", "user tweets [username]"
- "my mentions", "twitter mentions"
- "twitter lists", "my lists"
- "my feed"

## Terminology Mapping (Unified)

- `timeline` -> `x.com/i/timeline` (`device_follow` endpoint)
- `for you` / `首页推荐` / `home` -> `bird home -n 20`
- `following` / `首页关注流` -> `bird home --following -n 100`
- `timeline [username]` -> `bird user-tweets <username> -n 20`

Default rule: if user says only `timeline` with no qualifier, treat it as `i/timeline`.

## Prerequisites

1. Bird CLI must be installed: `brew install steipete/tap/bird`
2. Must be logged into X/Twitter in Chrome browser
3. Verify auth first without proxy:
   - `bird check --plain`
   - or `bird --cookie-source chrome --timeout 15000 whoami`
4. If your network requires proxy to reach X, add proxy env only when needed:
   - `HTTP_PROXY=http://127.0.0.1:7897`
   - `HTTPS_PROXY=http://127.0.0.1:7897`
5. If Python requests fail with SSL certificate verification behind proxy, ensure `certifi` is available (`python3 -c "import certifi; print(certifi.where())"`); when needed, pass the CA bundle explicitly via `--cafile`.

## Global Options

All commands should use:
- `--cookie-source chrome` to only use Chrome cookies (skip Safari/Firefox)
- `--timeout 15000` to avoid hanging requests
- proxy env (`HTTP_PROXY` / `HTTPS_PROXY`) only if your network requires it

Recommended command prefix (default, no proxy):
```bash
bird --cookie-source chrome --timeout 15000 <command>
```

If proxy is required in your environment:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 <command>
```

For `device_follow_timeline.py`:
- In this proxy environment, prefer a single-shot command with explicit `--cafile`; do not first try a bare command and then retry.
- Script now auto-detects `certifi` CA bundle and logs `SSL trust source`.
- You can explicitly force trust source with `--cafile <path>` / `--capath <dir>`; environment variables `SSL_CERT_FILE` / `SSL_CERT_DIR` are still supported.
- Emergency fallback only: set `BIRD_INSECURE_SSL=1` to retry once without SSL verification.

Example:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 home -n 20
```

## Commands

### 1. Check Auth Status
**Triggers:** "twitter auth", "bird whoami", "check twitter login"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 whoami
```

### 2. Read Tweet
**Triggers:** "read tweet [id]", "show tweet [url]", "get tweet"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 read <tweet-id-or-url>
```
Options: `--plain` for stable output without emoji/color

### 3. Read Thread
**Triggers:** "read thread [id]", "show thread [url]"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 thread <tweet-id-or-url>
```

### 4. Read Replies
**Triggers:** "show replies to [id]", "tweet replies"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 replies <tweet-id-or-url>
```
Notes:
- `replies` does not support `-n` / `--count` in current Bird CLI versions.
- Use `--max-pages <number>` or `--all` to control pagination when needed.

### 5. Search
**Triggers:** "search twitter [query]", "search x [query]", "find tweets about"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 search "<query>" -n 10
```

### 6. View Bookmarks
**Triggers:** "my bookmarks", "twitter bookmarks", "saved tweets"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 bookmarks -n 20
```

### 7. View Trending/News
**Triggers:** "trending", "twitter trends", "what's trending", "twitter news", "x news"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 news
```

### 8. View Home Timeline
**Triggers:** "home", "home timeline", "my feed", "for you", "首页推荐"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 home -n 20
```

### 8b. View Following Timeline
**Triggers:** "following", "following timeline", "首页关注流", "关注时间线"

Following 时间线按时间排序，是日常信息获取的主要入口。默认拉 100 条以覆盖近一天的内容，避免遗漏。
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 home --following -n 100
```

### 8c. View i/timeline (Device Follow)
**Triggers:** "timeline", "i/timeline", "notified timeline", "device follow", "通知时间线"

`x.com/i/timeline` 与 `home --following` 不是同一数据源。该命令直接请求 `device_follow` REST endpoint，默认读取 20 条。
```bash
SKILLS_HOME="$HOME/.codex/skills"
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
python3 "${SKILLS_HOME}/bird-twitter/scripts/device_follow_timeline.py" \
  --count 20 \
  --cafile "$(python3 -c 'import certifi; print(certifi.where())')"
```

如需严格对齐抓包参数，传入完整请求 URL：
```bash
SKILLS_HOME="$HOME/.codex/skills"
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
python3 "${SKILLS_HOME}/bird-twitter/scripts/device_follow_timeline.py" \
  --count 20 \
  --request-url "$BIRD_DEVICE_FOLLOW_URL"
```

### 9. View User Tweets
**Triggers:** "tweets from [username]", "timeline [username]", "[username]'s tweets"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 user-tweets <username> -n 20
```

### 10. View Likes
**Triggers:** "my likes", "liked tweets"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 likes -n 20
```

### 11. View Mentions
**Triggers:** "my mentions", "twitter mentions", "who mentioned me"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 mentions -n 20
```

### 12. View Lists
**Triggers:** "my lists", "twitter lists"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 lists
```

### 13. View List Timeline
**Triggers:** "list timeline [id]", "tweets from list"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 list-timeline <list-id-or-url> -n 20
```

### 14. View Following
**Triggers:** "who do I follow", "my following"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 following -n 50
```

### 15. View Followers
**Triggers:** "my followers", "who follows me"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 followers -n 50
```

### 16. User Info
**Triggers:** "about [username]", "user info [username]"
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 about <username>
```

## Output Options (Command-Specific)

Global output flag:
- `--plain` - Stable output without emoji or color (good for parsing)

Count flags (supported by many but not all commands):
- `-n <number>` or `--count <number>` - Limit number of results
- Commonly supported: `home`, `search`, `bookmarks`, `likes`, `mentions`, `user-tweets`, `list-timeline`, `following`, `followers`, `lists`, `news`

Pagination-only commands:
- `replies` / `thread` use `--max-pages <number>` or `--all` instead of `-n` / `--count`

When in doubt, check command-specific help first:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 <command> --help
```

## Practical Notes for Bookmark / Curation Work

- For bookmark triage, prefer `bird ... bookmarks -n <N> --plain` first to quickly scan authors, dates, and candidate URLs.
- Then enrich only shortlisted items with `bird read <tweet-url> --json`.
- Prefer `--json` over `--json-full` for long article-style tweets during batch analysis. In real sessions, `--json-full` can become very large (full `_raw` payload / article blocks) and may get truncated by wrappers or downstream JSON parsers.
- If you truly need `--json-full` for a long X Article in a scripted workflow, redirect stdout to a temporary file first, then parse that file locally. This avoids wrapper output caps corrupting JSON mid-payload.
- Use `--json-full` only when you specifically need raw article block structure, expanded metadata, or deep URL extraction from `_raw`.
- For article tweets, `bird read <tweet-url> --json` often exposes enough fields (for example `article.title`) to decide whether the item is already curated in a knowledge base.
- When `--json-full` includes `_raw.article.article_results.result.rest_id`, you can construct a stable X Article URL as `https://x.com/i/article/<rest_id>` and share that as the longform original.

## Important Notes

- This skill is READ-ONLY to avoid account suspension
- Uses unofficial X GraphQL API - may break without notice
- Requires browser login to X for cookie authentication
- If authentication fails, log into X in your browser and try again

## Excluded Commands (High Risk)

The following commands are intentionally NOT exposed due to account suspension risk:
- `bird tweet` - Post new tweets
- `bird reply` - Reply to tweets
- `bird follow` / `bird unfollow` - Follow/unfollow users
- `bird unbookmark` - Remove bookmarks
