---
name: x-article-canonicalization
description: "将 X/Twitter 长文高保真落库到 Obsidian/知识库：用 bird --json-full 重建 block 顺序、保留可点击链接、本地化图片，并区分可精确定位的正文插图与待定位附图。"
version: "1.0.0"
author: Hermes Agent
license: MIT
---

# X Article Canonicalization

把 X/Twitter 长文高保真保存到本地知识库（尤其是 Obsidian 的“推特精选”一类 canonical 原文层）。

适用场景：
- 用户说“收录到推特精选/知识沉淀”
- 用户要求“完整保存 / 原文转录 / 含图保存 / 1:1 保留”
- 用户后续还要 bridge 到 llm-wiki / raw/articles

不适用场景：
- 只想快速看内容摘要
- 只需要纯文本，不关心图和版式

## 核心原则

1. canonical 正文来源必须用 `bird read <url> --json-full`
2. 不用 `--plain` 当 canonical 主来源
3. 正文顺序按 `content_state.blocks` 重建
4. 链接尽量保留为 markdown 超链接
5. 图片只有在“能精确定位”时才插回正文
6. 不能精确定位的图片，单列到“原文附图（待定位）”
7. 对中文知识库，canonical 笔记默认写成中文整理版，而不是英文原文整段直贴

## 推荐流程

### 1. 抓原文 JSON

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
bird --cookie-source chrome --timeout 30000 read <tweet-url> --json-full > /tmp/x-article.json
```

重点字段：
- `article_results.result.content_state.blocks`
- `article_results.result.content_state.entityMap`
- `article_results.result.cover_media`
- `article_results.result.media_entities`

### 2. 下载媒体并建立映射

媒体来源分两类：
- `cover_media.media_info.original_img_url` → 封面图
- `media_entities[].media_info.original_img_url` → 正文图/附图候选

本地化到：
- `assets/<slug>/img-0.ext`
- `assets/<slug>/img-1.ext`
- ...

### 3. 重建正文

按 `content_state.blocks` 顺序处理：
- `header-two` → 二级标题
- `unstyled` → 普通段落
- `blockquote` → 引用块
- `unordered-list-item` → 无序列表
- `atomic` → 需要看 `entityMap`

#### atomic 处理规则

只有当 `atomic` block 对应的 `entityMap` 项是 `MEDIA`，且能拿到明确 `mediaId` 时，才把对应图片插回正文当前位置。

也就是：
- `atomic + MEDIA` = 正文原位插图
- `atomic + LINK / TWEET / 其他` = 不是正文图片，不要误插图

### 4. 嵌入推文和外链

不要写成这种不可点击文本：
- `[嵌入推文: https://x.com/... ]`

应该写成：
- `[嵌入推文｜作者名 / 简短说明](https://x.com/...)`

正文里的文章/项目链接也尽量保留 markdown 超链接。

### 5. 处理“无法精确定位”的图片

经验坑点：
Bird 的 `media_entities` 可能给出多张图，但 `content_state.blocks` 并不一定给出这些图的精确插入位置。

这时不要猜，也不要全部强塞回正文。

正确做法：
- 把能精确定位的图插回正文
- 把其余图单独放到：

```md
## 原文附图（Bird 导出的 block 结构未给出精确插入位点）
```

并在小节里逐张保留。

## 推荐正文结构

```md
---
frontmatter...
---

![封面图](assets/<slug>/img-0.jpg)

# 中文标题

中文导语/摘要

## 第一节
正文...

![图 1｜说明](assets/<slug>/img-1.jpg)

## 第二节
正文...

[嵌入推文｜说明](https://x.com/i/status/...)

## 原文附图（Bird 导出的 block 结构未给出精确插入位点）

### 图 2｜说明
![图 2](assets/<slug>/img-2.jpg)
```

## 最小验收清单（DoD）

交付前至少核对：
- [ ] 正文主来源来自 `--json-full`
- [ ] canonical 是中文整理版（若用户未要求保留原英文）
- [ ] `cover_media` 已下载并引用
- [ ] 所有 `atomic + MEDIA` 图片都已按原位插入
- [ ] 无法精确定位的图片没有乱插，已移入附图区
- [ ] 文中的嵌入推文 / 外链是可点击 markdown 链接
- [ ] 图片满足：`expected_body_media_count <= downloaded_count == referenced_count_total`

其中：
- `expected_body_media_count` = block 里可精确定位的正文图数量
- `downloaded_count` = 实际下载图片数
- `referenced_count_total` = 正文原位图 + 附图区图片总引用数

## 常见错误

错误做法：
- 直接用 `--plain` 当 canonical 原文
- 把英文全文直接塞进中文知识库
- 把所有图片都堆到文末
- 看见 `media_entities` 就假定每张图都有准确正文位置
- 把嵌入推文写成不可点击的裸文本

正确做法：
- 用 `--json-full`
- 先按 blocks 重建，再决定图片位置
- 不能定位的图，明确标成附图，而不是瞎猜

## 与 llm-wiki 的关系

如果后续还要 ingest 进 llm-wiki：
1. 先完成 canonical 笔记
2. 再创建 `raw/articles/*.md` source bridge
3. 再走 `analysis -> generation` ingest

这样可以把“高保真原文层”和“结构化知识层”分开，避免 sources 路径漂移。