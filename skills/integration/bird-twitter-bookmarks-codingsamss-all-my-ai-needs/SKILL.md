---
name: bird-twitter-bookmarks
description: "Manage X/Twitter bookmarks locally with Field Theory CLI. Actions: sync, search, list, classify, stats, viz, l2-label, review queue. Keywords: x bookmarks, twitter bookmarks, fieldtheory, ft."
---

# Field Theory Bookmarks Skill

使用 `fieldtheory`（`ft`）管理 X/Twitter 收藏夹的本地数据副本：同步、检索、筛选、分类、统计与可视化。并支持 unknown 条目的 L2 细分标签与低置信度复核队列。

## 适用场景

触发关键词：

- `x 收藏夹` / `twitter bookmarks` / `bookmarks`
- `fieldtheory` / `ft`
- `同步收藏夹` / `搜索收藏` / `分类收藏`
- `收藏夹统计` / `收藏夹可视化`

## 前置条件

1. 已安装 `Node.js 20+` 与 `fieldtheory` CLI。
2. Chrome 已登录 `x.com`。
3. 当前网络环境访问 X 需要走本地代理，并启用 Node 环境代理：
   - `NODE_USE_ENV_PROXY=1`
   - `HTTP_PROXY=http://127.0.0.1:7897`
   - `HTTPS_PROXY=http://127.0.0.1:7897`

推荐命令前缀：

```bash
NODE_USE_ENV_PROXY=1 HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 ft <command>
```

## 核心命令

### 1) 首次同步

```bash
NODE_USE_ENV_PROXY=1 HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 ft sync
```

快速自测（只拉 1 页）：

```bash
NODE_USE_ENV_PROXY=1 HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 ft sync --max-pages 1
```

### 2) 搜索与查看

```bash
ft search "agent memory"
ft list --author wangray --limit 20
ft show <tweet_id>
```

### 3) 分类与统计

```bash
ft classify --regex
ft categories
ft domains
ft stats
ft viz
```

### 3.1) unknown 条目 L2 细分（新增）

脚本路径（同步后）：

```bash
SCRIPT="${CLAUDE_HOME:-$HOME/.claude}/skills/bird-twitter-bookmarks/scripts/bookmark_l2_labels.py"
```

初始化本地表结构（幂等）：

```bash
python3 "$SCRIPT" bootstrap
```

先 dry-run 看效果：

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 python3 "$SCRIPT" classify-unknown --engine auto --dry-run --verbose
```

正式执行（unknown -> L2 标签）：

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 python3 "$SCRIPT" classify-unknown \
  --engine codex \
  --single-stage \
  --stage1-model gpt-5.4-mini \
  --stage1-effort medium \
  --batch-size 10 \
  --skip-link-fetch \
  --min-confidence 0.7 \
  --min-context-chars 24 \
  --low-context-cap 0.55
```

查看覆盖与分布：

```bash
python3 "$SCRIPT" report
```

查看低置信度复核队列：

```bash
python3 "$SCRIPT" review --limit 20
```

### 4) 路径与状态

```bash
ft path
ft status
```

## 数据路径

默认存储目录：

```bash
~/.ft-bookmarks/
```

可覆盖为自定义目录：

```bash
FT_DATA_DIR=/path/to/dir ft sync
```

## 安全说明

- 默认是本地落盘，不会自动修改 X 平台内的收藏夹结构。
- `ft classify` 会调用本机可用的 `claude` 或 `codex` CLI 做分类（非纯离线规则）。
- 若只想本地规则分类，可用 `ft classify --regex`。
- 若出现 `fetch failed`，优先检查是否缺少 `NODE_USE_ENV_PROXY=1`。
- L2 标签脚本仅写入本地 SQLite 附加表（`bookmark_link_context`/`bookmark_labels`/`bookmark_review_queue`），不会改动 X 平台内容。
- 质量闸门：对“信息不足（仅链接）”条目自动降置信度并进入复核队列，避免误判被当作高质量结果。
