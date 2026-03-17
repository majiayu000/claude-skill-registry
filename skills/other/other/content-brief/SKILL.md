---
name: content-brief
description: "Use when you need to research a target keyword before creating a page — discovers SERP competitors, analyzes their content strategy, builds a keyword pool, and outputs a structured Brief that feeds directly into /shipany-page-builder."
---

# Content Brief Generator

## Skill 边界

| 范围 | 说明 |
|------|------|
| **输入** | 目标关键词（必需）、用户关键词+搜索量（可选）、竞品 URL（可选） |
| **输出** | Markdown Brief 报告、`/tmp/competitor-analysis.json` |
| **修改** | 不修改任何项目代码、页面文件、配置文件 |
| **不做** | 不创建页面（交给 `/shipany-page-builder`）、不翻译（交给 `/auto-i18n`） |

### When NOT to use

- 页面已有且只需优化 SEO → 用 `/shipany-page-builder` 或 `/i18n-content-audit`
- 只需关键词拓展而不需要完整 Brief → 用 `/keyword-research`
- 只需分析单个竞品 → 用 `/competitor-analysis`
- 翻译已有英文页面 → 用 `/auto-i18n`

---

## BLOCKING REQUIREMENTS — 按顺序执行

**你必须完成每个 CHECKPOINT 才能进入下一步。不可跳过任何 CHECKPOINT。**

---

## PRE-EXECUTION: 标准化输入

**BLOCKING:** 先从用户请求中提取结构化输入。

需要确认：
- `keyword`: 目标关键词（如 "AI Image Generator"）
- `locale`: 目标语言（默认 en）
- `user_keywords`: 用户提供的关键词+搜索量（如有）
- `competitor_urls`: 用户指定的竞品 URL（如有，否则自动发现）

**确认格式：**
"INPUT: keyword='{keyword}', locale={locale}, user_keywords={N}个, competitor_urls={N}个"

---

## CHECKPOINT 1: SERP 发现 — 找到 10 个竞品

**BLOCKING:** 必须找到至少 10 个有效竞品 URL。

### 步骤

1. **WebSearch 搜索目标关键词**
   - 搜索 `{keyword}` 获取 SERP 结果
   - 如果结果不够，补充搜索：`best {keyword}`, `{keyword} online free`

2. **筛选竞品 URL**
   - 取 SERP 前 10 个**有机结果**（排除广告、自家域名 makemypic.ai）
   - 优先选择：产品页、功能页、工具页（非新闻/博客/论坛/Wikipedia）
   - 如用户提供了 competitor_urls，**合并进来**（用户指定的优先）

3. **补充搜索（如不足 10 个）**
   - 搜索 `{keyword} alternatives`, `{keyword} tools`
   - 目标：**恰好 10 个竞品 URL**

**确认格式：**
"CHECKPOINT 1 COMPLETE: 发现 {N} 个竞品 URL"

列出全部 URL。

---

## CHECKPOINT 2: 竞品深度分析

**BLOCKING:** 必须获取至少 7/10 个竞品的完整数据。

### 步骤

1. **运行竞品分析脚本**

```bash
python3 .claude/skills/content-brief/scripts/analyze_competitors.py \
  --keyword "{keyword}" \
  --urls "{url1},{url2},...,{url10}" \
  --locale {locale} \
  --output /tmp/competitor-analysis.json
```

2. **读取分析报告**
   读取 `/tmp/competitor-analysis.json`，提取：
   - 每个竞品的字数、标题结构、关键词密度
   - 聚合摘要：平均字数、常见章节、特征占比
   - **竞品 H2 关键词模式**（`h2_keyword_patterns`）：高频词、短语、修饰词
   - 推荐页面结构

3. **第 2 层：WebFetch 补充**（对脚本抓取失败或数据不足的页面）
   - 判断标准：`word_count < 100` 或 `h2_count = 0` 或 `error` → **数据不足**
   - **必须逐个调用 WebFetch，不可并行**（并行会导致 Sibling tool call errored 级联失败）
   - 对每个数据不足的页面：
     ```
     WebFetch: {url}
     提取: 页面标题、所有 H2 标题、大致字数、是否有 FAQ/demo/gallery
     ```
   - 将结果补充到报告中

4. **第 3 层：Playwright 浏览器兜底**（对脚本 + WebFetch 都失败的页面）
   - 触发条件：WebFetch 返回 403、timeout 或 TLS 错误
   - Playwright 是真实 Chromium 浏览器，能绕过 Cloudflare 等反爬虫
   - 对每个仍失败的页面，**逐个执行**：
     ```
     1. mcp__playwright__playwright_navigate → {url}
     2. mcp__playwright__playwright_get_visible_html (cleanHtml=true, maxLength=50000)
     3. 从 HTML 中提取: title, H2 列表, 大致字数, FAQ/demo/gallery 特征
     ```
   - 提取完成后关闭浏览器：`mcp__playwright__playwright_close`
   - **目标：至少 7/10 个竞品有完整数据**

5. **错误恢复**
   - 如果脚本执行失败：检查 Python3 是否可用，检查网络
   - 三层都失败的页面：标注 "blocked" 原因，不影响整体分析
   - 如果三层合计 < 5 个竞品有数据：告知用户，列出已获取的数据继续

5. **输出竞品洞察报告**

对每个竞品：
```
#N domain.com (字数: XXXX)
  H1: "..."
  H2 结构: [列出所有 H2]
  关键词策略: primary X次, 密度 X%
  特色: [demo/gallery/comparison/FAQ等]
```

聚合输出（含 H2 关键词模式）：
```
共性总结:
  - X/10 有在线 demo/generator
  - X/10 有 showcase/gallery
  - 平均字数: XXXX
  - 平均 FAQ: X 个

竞品 H2 关键词模式:
  - 高频词: image(8), generator(7), free(5), ...
  - 高频短语: "image generator"(6), "art generator"(3), ...
  - 常用修饰词: free, best, online, top, ...

差异化机会:
  - [基于竞品弱点识别的机会]
```

**确认格式：**
"CHECKPOINT 2 COMPLETE: 分析 {N}/10 竞品，平均字数 {X}，H2 高频词 {top3}"

---

## CHECKPOINT 3: 关键词策略

**BLOCKING:** 必须产出完整的关键词池和分布策略。

### 步骤

1. **AI 关键词拓展**
   基于目标关键词 + CHECKPOINT 2 的竞品 H2 关键词模式，生成：
   - **长尾词** (long_tail): 8-12 个（如 "free AI image generator online"）
   - **语义变体** (semantic): 5-8 个（如 "text-to-image AI", "AI art creator"）
   - **相关词** (related): 5-8 个（如 "stable diffusion", "AI art styles"）

   **关键：参考竞品 H2 中的高频词和修饰词来指导拓展方向！**
   - 竞品高频修饰词（如 free, best, online）应融入长尾词
   - 竞品高频短语应考虑纳入语义变体

2. **合并用户提供的关键词**（如有）
   - 用户提供的关键词**优先保留**
   - 如用户提供了搜索量，标注在关键词旁边
   - 去重：如用户关键词与 AI 拓展重叠，以用户版本为准
   - 在 Brief 中标注来源（"用户" vs "调研"）

3. **参考竞品关键词用法**
   - 从 CHECKPOINT 2 的 `h2_keyword_patterns.top_words` 和 `top_bigrams` 中提取
   - 识别竞品普遍使用但我们可能遗漏的关键词

4. **规划关键词分布**
   参考 [_shared/references/seo-standards.md](../_shared/references/seo-standards.md) 中的分布规则：
   ```
   H1: [primary keyword + value proposition]
   H2-1: [primary 或 long-tail]  ← primary ≤50%
   H2-2: [semantic variant]       ← variants 50%+
   H2-3: [related term]
   H2-4: [long-tail]
   ...
   密度目标: 参照 seo-standards.md 中 {locale} 的 Target Density
   ```

**确认格式：**
"CHECKPOINT 3 COMPLETE: 关键词池 {N}个 (primary 1, long-tail {N}, semantic {N}, related {N}), 用户提供 {N}个"

---

## CHECKPOINT 4: 内容规划 & Brief 输出

**BLOCKING:** Brief 必须通过质量门控。

### 步骤

1. **推荐页面结构**
   基于 CHECKPOINT 2 的竞品分析和推荐结构：
   - **只从项目已有的 block 中选择！**
   - 参考 [references/01-block-registry.md](references/01-block-registry.md)
   - 标注每个 section 的理由（X/10 竞品有这个章节）

2. **设定目标参数**
   参考 [_shared/references/seo-standards.md](../_shared/references/seo-standards.md)：
   - 目标字数：取竞品平均值和 SEO 标准最低值中的**较大值**
   - FAQ 数量：基于竞品平均值（不少于 6 个）
   - 关键词密度：使用 seo-standards.md 中对应 locale 的 Target Density

3. **识别差异化机会**
   - 竞品普遍缺少的内容（如 stats 数据背书、comparison 对比）
   - 竞品做得不好的地方（如 FAQ 质量差、缺少 schema）
   - 我们独有的优势（如交互式 generator、showcases-flow）

4. **输出结构化 Brief**
   按照 [references/02-brief-template.md](references/02-brief-template.md) 格式输出。

### Brief 质量门控

输出前自检：
- [ ] 关键词表包含 4 种类型（primary, long-tail, semantic, related）
- [ ] 用户提供的关键词已合并且标注来源
- [ ] 竞品洞察表有 10 行（数据不足的标注原因）
- [ ] 每个推荐 Block 都在 01-block-registry.md 中存在
- [ ] 目标字数 ≥ seo-standards.md 中对应 locale 最低值
- [ ] FAQ 数量 ≥ 6
- [ ] 密度目标在 seo-standards.md 健康范围内
- [ ] show_sections JSON 可直接用于 page-builder

**确认格式：**
"CHECKPOINT 4 COMPLETE: Brief 已生成，推荐 {N} 个 section，目标 {X} words，质量门控 {N}/{N} 通过"

---

## Quick Reference

**SEO 标准:** 参考 [_shared/references/seo-standards.md](../_shared/references/seo-standards.md)
**可用 Block:** 参考 [references/01-block-registry.md](references/01-block-registry.md)
**Brief 模板:** 参考 [references/02-brief-template.md](references/02-brief-template.md)
**竞品分析脚本:** `scripts/analyze_competitors.py`（零依赖，用 `python3` 执行）

---

## 与其他 Skill 的关系

```
/content-brief (本 Skill — 调研 + 规划)
    ↓ Brief 作为输入
/shipany-page-builder (创建页面)
    ↓ 国际化
/auto-i18n (翻译)
    ↓ 审计
/i18n-content-audit (质量检查)
```

### 增强调研（高竞争关键词建议主动使用）

在 CHECKPOINT 3 中，对于高竞争关键词，**建议主动调用**：
- `/keyword-research` — 更深入的关键词拓展和 topic cluster 分析
- `/serp-analysis` — SERP 特征分析（featured snippet、PAA、SERP 布局）

**判断标准：** 如果 CHECKPOINT 2 发现竞品平均字数 > 2000 或竞品数 > 8 个产品页，说明竞争激烈，建议主动使用上述 Skill。

---

**Last Updated:** 2026-02-07
