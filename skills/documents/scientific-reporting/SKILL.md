---
name: scientific-reporting
description: "Write research/technical reports with strong structure + figure standards. Supports Markdown/HTML/PDF outputs (Quarto optional), executive summary, methods, results, discussion, and reproducibility appendix."
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Scientific Reporting（科研/技术报告）

## 你遇到的痛点（为什么需要这个 skill）

很多“报告写作失败”不是写不出来，而是：
- 路由误入 `docs-media`（被 PDF/Word 关键词抢走）
- 报告没有结构（缺少 Executive Summary / 方法可复现 / 结果可追溯）
- 图表不达标（截图、低 DPI、字体不一致、颜色不友好）

这个 skill 的职责是：**把报告当成可交付工程**，并把图表与叙事纳入同一规范。

---

## 适用场景（关键词）

- 中文：`科研报告`、`技术报告`、`项目报告`、`实验报告`、`分析报告`、`HTML 报告`、`PDF 报告`
- 英文：`technical report`、`research report`、`HTML report`、`Quarto`、`RMarkdown`

不适用：
- 仅“抽取 PDF 文本/解析 docx” → `docs-media/pdf/docx/markitdown`

---

## 输入（最小信息）

1) 受众：老板/评审/客户/组会同学（决定写作风格与解释深度）
2) 目的：决策/复现/汇报/归档（决定是否必须包含 appendix）
3) 输出格式：`Markdown` / `HTML` / `PDF`（可多选）
4) 数据与图：是否已有数据、已有图、或需要从数据生成图

---

## 输出（默认目录）

推荐输出为（可按项目名建子目录）：
- `reports/<topic>/report.md`（source-of-truth）
- `reports/<topic>/report.html`（可选）
- `reports/<topic>/report.pdf`（可选）
- `reports/<topic>/figures/`（报告引用的图，来源于 `figures/**/out`）
- `reports/<topic>/appendix/`（方法、参数、环境、额外图表）

模板：`templates/report-skeleton.md`

---

## 工作流（强制顺序）

### Phase 1 — 结构先行（先搭骨架）

报告必须包含（即使简写）：
1) Executive Summary（结论先行）
2) Context（问题与约束）
3) Methods（可复现：数据/流程/参数）
4) Results（以图为骨架）
5) Discussion（解释意义、局限、建议）
6) Appendix（可选但推荐：环境/补充图/表）

### Phase 2 — 结果以图为锚

- 图表走 `scientific-visualization`（publication-quality）
- 示意图走 `scientific-schematics`（流程/机制/系统图）
- 文本解释走 `scientific-writing`（段落化、避免 bullet 作为最终稿）

### Phase 3 — 导出策略（HTML/PDF）

如果要 HTML：
- 优先：Markdown + 静态图（PDF/SVG/PNG）
- 需要交互：Plotly 输出 HTML（并提供静态 fallback）

如果要 PDF：
- 重点：图字体与线宽在最终版面可读
- 禁止：把网页截图当 PDF

---

## 质量门禁（报告交付前）

- [ ] “结论先行”：读 Executive Summary 就能知道要点与建议
- [ ] “可复现”：Methods + Appendix 足以复现关键结果
- [ ] “图可用”：统一字体、色盲友好、导出格式正确
- [ ] “可追溯”：每个结论能指向某张图/某个表/某段计算

