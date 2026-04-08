---
name: bird-twitter
description: "Read X/Twitter content via Bird CLI. Actions: read tweets, search, view bookmarks, trending, news, timeline, mentions, lists. Keywords: twitter, x, tweet, trending, bookmarks, timeline."
---

# Bird Twitter Skill (Read-Only)

Read X/Twitter content using the Bird CLI tool. This skill only exposes read-only operations to avoid account suspension risks.

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
3. In this environment, network access to X should go through local proxy:
   - `HTTP_PROXY=http://127.0.0.1:7897`
   - `HTTPS_PROXY=http://127.0.0.1:7897`
4. Run `HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 whoami` to verify authentication
5. If Python requests fail with SSL certificate verification behind proxy, ensure `certifi` is available (`python3 -c "import certifi; print(certifi.where())"`); when needed, pass the CA bundle explicitly via `--cafile`.

## Global Options

All commands should use:
- proxy env (`HTTP_PROXY` / `HTTPS_PROXY`)
- `--cookie-source chrome` to only use Chrome cookies (skip Safari/Firefox)
- `--timeout 15000` to avoid hanging requests

Recommended command prefix:
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
Notes:
- `--plain` 仅用于临时阅读/命令行快速查看，不得用于“收录/归档/完整保存”任务。
- 归档任务必须使用 `--json-full`，并从 `article.article_results.result.content_state`（正文结构）+ `media_entities`（图片资源）恢复图文顺序。

### 2b. Archive Tweet/Article (Text + Media)
**Use when:** 用户要求“收录/归档/完整保存/原文保留（含图）”
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 read --json-full <tweet-id-or-url>
```
Requirements:
- 保留原文结构（标题、列表、引用、代码块）
- 图片按原文顺序本地化并在文内原位引用
- 必做三数一致校验：预期图片数 = 下载成功数 = 文内引用数
- 结构重建必须以 `content_state.blocks` 为唯一顺序源，禁止用 `--plain` 文本推断结构
- `atomic` 块类型必须从 `entityMap.value.type` 判定（`MEDIA` / `MARKDOWN` / `DIVIDER`），禁止猜测
- `MEDIA` 必须通过 `mediaItems[].mediaId -> media_entities[].media_info.original_img_url` 映射原图
- 下载前先清理目标目录中“同编号不同扩展名”的旧文件，避免 `img-N.jpg/png` 并存
- 收尾必须做块级一致性校验：`MEDIA=标准图片引用数`、`MARKDOWN=代码块数`、`DIVIDER=分隔线数`
- 若存在人工补充图，必须显式标注“补充内容，非 X 原文正文”
- 最后执行一次未引用资产扫描，删除 `assets/hitw93-*/` 下未被任何 `.md` 引用的冗余文件

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
SKILLS_HOME="$HOME/.claude/skills"
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
python3 "${SKILLS_HOME}/bird-twitter/scripts/device_follow_timeline.py" \
  --count 20 \
  --cafile "$(python3 -c 'import certifi; print(certifi.where())')"
```

如需严格对齐抓包参数，传入完整请求 URL：
```bash
SKILLS_HOME="$HOME/.claude/skills"
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
- `--plain` 不可作为归档源（会丢失图文结构/媒体信息）

Count flags (supported by many but not all commands):
- `-n <number>` or `--count <number>` - Limit number of results
- Commonly supported: `home`, `search`, `bookmarks`, `likes`, `mentions`, `user-tweets`, `list-timeline`, `following`, `followers`, `lists`, `news`

Pagination-only commands:
- `replies` / `thread` use `--max-pages <number>` or `--all` instead of `-n` / `--count`

When in doubt, check command-specific help first:
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 bird --cookie-source chrome --timeout 15000 <command> --help
```

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
