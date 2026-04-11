---
name: linuxdo
description: "Read LINUX DO forum content via Discourse JSON API + Chrome Cookie auth. Actions: check login, latest topics, top/trending, full-text search, read topic details, browse categories. Keywords: linuxdo, linux.do, l站, 帖子, 搜索, 最新, 热门, 分类, discourse, forum."
---

# LINUX DO Skill (Read-Only)

通过本地 Python 脚本只读访问 LINUX DO（linux.do）论坛内容。默认使用 Discourse JSON API + Chrome Cookie 自动提取认证，可访问有信任等级限制的帖子。

## Prerequisites

1. Python3 可用。
2. macOS + Chrome（已登录 linux.do；首次可能弹出 Keychain 授权，请点“允许”）。
3. 网络可访问 `https://linux.do`；如需代理，建议：
   - `HTTP_PROXY=http://127.0.0.1:7897`
   - `HTTPS_PROXY=http://127.0.0.1:7897`

推荐命令前缀：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SCRIPT="$CODEX_HOME/skills/linuxdo/scripts/linuxdo.py"
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 python3 "$SCRIPT" <subcommand>
```

## Commands

### 1. 查看登录身份
**Triggers:** `linuxdo 登录状态`、`linuxdo whoami`、`l站身份`

```bash
python3 "$SCRIPT" whoami
```

### 2. 查看最新帖子
**Triggers:** `linuxdo 最新帖子`、`l站最新`、`latest linuxdo`

```bash
python3 "$SCRIPT" latest --limit 20 --page 0
```

### 3. 查看热门帖子
**Triggers:** `linuxdo 热门`、`l站热帖`、`linuxdo top`、`l站 trending`

```bash
python3 "$SCRIPT" top --period weekly --limit 20
```

`--period` 可选：`daily` / `weekly` / `monthly` / `yearly` / `all`

### 4. 全文搜索
**Triggers:** `搜索 linuxdo`、`linuxdo 搜索`、`search linuxdo`、`l站搜索`

```bash
python3 "$SCRIPT" search "OpenAI" --limit 10
```

### 5. 查看帖子详情
**Triggers:** `查看 linuxdo 帖子`、`读帖`、`linuxdo topic`、`看看这个帖子`

```bash
python3 "$SCRIPT" topic "https://linux.do/t/topic/1611298" --posts 5
```

支持输入格式：
- `https://linux.do/t/topic/1611298`
- `topic/1611298`
- `1611298`

### 6. 分类浏览
**Triggers:** `linuxdo 分类`、`l站分类`、`linuxdo categories`

列出分类：

```bash
python3 "$SCRIPT" category
```

查看分类帖子：

```bash
python3 "$SCRIPT" category develop --limit 20
```

## Auth Behavior

默认认证优先级：
1. `--cookie` 显式传入
2. `--cookie-file`（支持 `name=value; ...` 或 Netscape Cookie 文件）
3. 环境变量 `LINUXDO_COOKIE`
4. macOS 下自动提取 Chrome Cookies（推荐）

示例：

```bash
python3 "$SCRIPT" --cookie-file ~/.config/linuxdo/cookie.txt topic 1611298 --posts 3
```

## Important Notes

- 本 skill 仅开放只读能力，不包含发帖、回帖、点赞等写操作。
- 若命中 Cloudflare challenge：
  1. 保持与浏览器一致的代理出口
  2. 复用浏览器登录态（Chrome Cookie）
  3. 降低请求频率，避免短时间高频请求
