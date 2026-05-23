---
name: linuxdo
description: "Read LINUX DO forum content via Discourse JSON API + Chrome Cookie auth. Actions: check login, latest topics, top/trending, full-text search, read topic details, browse categories. Keywords: linuxdo, linux.do, l站, 帖子, 搜索, 最新, 热门, 分类, discourse, forum."
---

# LINUX DO Skill (Read-Only)

通过本地 Python 脚本只读访问 LINUX DO（linux.do）论坛内容。使用 Discourse JSON API + Chrome Cookie 自动提取认证，可访问有信任等级限制的帖子。

## Prerequisites

1. Python3 可用。
2. macOS 系统（Chrome Cookie 自动提取依赖 Keychain + CommonCrypto）。
3. Chrome 已登录 linux.do（首次使用时系统会弹出 Keychain 授权对话框，请点击"允许"）。
4. 如网络环境受限，建议配置代理：
   - `HTTPS_PROXY=http://127.0.0.1:7897`

## Script Path

```
SKILLS_HOME="$HOME/.claude/skills"
SCRIPT="${SKILLS_HOME}/linuxdo/scripts/linuxdo.py"
```

## Cookie Authentication

脚本按优先级自动解析 Cookie 来源：
1. `--cookie "name=value; ..."` 命令行直传
2. `--cookie-file <path>` 或环境变量 `LINUXDO_COOKIE_FILE`
3. 环境变量 `LINUXDO_COOKIE`
4. Chrome Cookie 自动提取（macOS 默认，零配置）
5. 无认证（仅可访问公开内容）

手动回退（当 Chrome 提取失败时）：
```bash
# 从浏览器 DevTools > Application > Cookies 复制 Cookie 字符串
python3 "$SCRIPT" --cookie "_t=xxx; _forum_session=yyy" latest --limit 5
```

## Commands

### 1. 查看登录身份
**Triggers:** "linuxdo 登录状态", "linuxdo whoami", "l站身份"
```bash
python3 "$SCRIPT" whoami
```

### 2. 查看最新帖子
**Triggers:** "linuxdo 最新帖子", "l站最新", "latest linuxdo"
```bash
python3 "$SCRIPT" latest --limit 20
```
可选参数：
- `--page <n>`：翻页（从 0 开始）
- `--chars <n>`：摘要最大字符（默认 140）

### 3. 查看热门帖子
**Triggers:** "linuxdo 热门", "l站热帖", "linuxdo top", "l站 trending"
```bash
python3 "$SCRIPT" top --period weekly
```
可选参数：
- `--period`：`daily` / `weekly` / `monthly` / `yearly` / `all`（默认 weekly）
- `--limit <n>`：输出条数（默认 20）

### 4. 搜索帖子
**Triggers:** "搜索 linuxdo", "linuxdo 搜索", "search linuxdo", "l站搜索"
```bash
python3 "$SCRIPT" search "Claude Code" --limit 10
```
说明：
- 使用 Discourse 原生 search.json 全文搜索
- 支持 Discourse 搜索语法：`@username`、`#category`、`in:title`、`order:latest` 等
- 同时返回匹配主题和匹配回帖

### 5. 查看帖子详情
**Triggers:** "查看 linuxdo 帖子", "读帖", "linuxdo topic", "看看这个帖子"
```bash
python3 "$SCRIPT" topic 1611298 --posts 5
```
也支持：
- `topic "https://linux.do/t/topic/1611298"`
- `topic "topic/1611298"`
可选参数：
- `--posts <n>`：输出楼层数（默认 5）
- `--chars <n>`：每条内容最大字符（默认 300）
- `--page <n>`：楼层翻页（默认 0）

### 6. 浏览分类
**Triggers:** "linuxdo 分类", "l站分类", "linuxdo categories"

列出所有分类：
```bash
python3 "$SCRIPT" category
```

查看某分类帖子：
```bash
python3 "$SCRIPT" category develop --limit 20
```

内置分类映射（slug -> 中文名）：
- `develop` 开发调优 | `domestic` 国产替代 | `resource` 资源荟萃
- `wiki` 文档共建 | `job` 非我莫属 | `reading` 读书成诗
- `news` 前沿快讯 | `feeds` 网络记忆 | `welfare` 福利羊毛
- `gossip` 搞七捻三 | `square` 虫洞广场 | `feedback` 运营反馈

## Proxy Configuration

```bash
# 通过环境变量配置代理
HTTPS_PROXY=http://127.0.0.1:7897 python3 "$SCRIPT" latest --limit 5

# urllib 和 curl 均会使用该代理
```

## Important Notes

- 本 skill 仅开放只读能力，不包含发帖、回帖、点赞等写操作。
- Chrome Cookie 提取仅支持 macOS（依赖 Keychain + CommonCrypto）。
- 首次使用时系统会弹出 Keychain 授权对话框，选择"允许"即可。
- 若命中 Cloudflare 风控，脚本会自动回退到 curl 请求。

## Excluded Actions (Write Operations)

以下操作不开放：
- 发帖 / 回帖 / 编辑帖子
- 点赞 / 收藏 / 标记
- 用户设置修改
- 任何 POST/PUT/DELETE 请求
