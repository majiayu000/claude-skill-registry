---
name: feed-digest
description: |
  RSS/Atom 信息源聚合摘要。使用此 skill 当用户要求：(1) 获取 RSS/Feed 摘要，(2) 查看订阅源更新，(3) 总结今日信息流，(4) 分析多个信息源内容。支持智能分类、10分制评分筛选、关键词过滤。
---

# Feed Digest - 信息源聚合摘要

从配置的 RSS/Atom 源获取内容，智能分类、评分筛选、生成摘要。

## 工作流程

### 1. 读取用户配置

配置文件位置: `~/.claude/feeds.local.md`

```yaml
---
feeds:
  - url: https://example.com/feed.rss
    name: Example Site  # 可选，不填则自动获取
  - url: https://another.com/atom.xml
---
```

### 2. 获取 Feed 数据

```bash
# 从配置获取所有源
python3 ${CLAUDE_PLUGIN_ROOT}/skills/feed-digest/scripts/fetch_feeds.py ~/.claude/feeds.json

# 直接指定 URL
python3 ${CLAUDE_PLUGIN_ROOT}/skills/feed-digest/scripts/fetch_feeds.py --urls "url1,url2"

# 带关键词过滤
python3 ${CLAUDE_PLUGIN_ROOT}/skills/feed-digest/scripts/fetch_feeds.py config.json --filter "AI,Claude"
```

脚本返回 JSON，包含所有帖子的标题、描述、链接、来源等信息。

### 3. 智能分类与评分

对每篇内容按 [评分标准](references/scoring.md) 打分（10分制）：
- ≥7分: 精选推荐
- 4-6分: 值得一看
- <4分: 忽略

同时根据内容自动分类（技术开发、AI/ML、科技资讯等）。

### 4. 输出格式

```markdown
# Feed 摘要 (YYYY-MM-DD HH:MM)

共获取 N 篇内容，来自 M 个源，精选 X 篇

---

## 技术开发

### [标题](链接) - 8.5分
**来源**: xxx | **作者**: xxx

> 内容摘要（2-3句话）

---

## AI/ML

### [标题](链接) - 7.2分
...

---

## 值得一看

- [标题](链接) - 5.8分 (来源)
- [标题](链接) - 4.5分 (来源)

---

## 统计
- 获取源: M 个成功，N 个失败
- 热门来源: xxx (X篇)
- 高频关键词: AI, xxx, xxx
```

## 配置管理

### 添加源

在 `~/.claude/feeds.local.md` 的 YAML frontmatter 中添加：

```yaml
feeds:
  - url: https://news.ycombinator.com/rss
    name: Hacker News
  - url: https://linux.do/latest.rss
    name: Linux.do
```

### 关键词过滤

用户可指定关键词，只显示匹配的内容。脚本支持 `--filter` 参数。

## 注意事项

1. **网络**: 脚本使用 curl，自动适配系统代理（如 Shadowrocket TUN）
2. **并发**: 多源并发获取，默认 5 线程
3. **限制**: 每个源最多返回 feed 中的全部条目（通常 20-50 条）
4. **编码**: 支持 RSS 2.0 和 Atom 格式
