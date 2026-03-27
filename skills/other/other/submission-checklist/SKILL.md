---
name: submission-checklist
description: "Stage-based submission checklists for papers/reports: pre-submission, submission, revision/rebuttal, camera-ready. Includes templates (cover letter, rebuttal matrix) and quality gates."
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Submission Checklist（投稿 / 返修 / 相机就绪清单）

## 目标

把“投稿”拆成可执行、可复用的清单，避免典型的“低级错误导致 desk reject / major revision”的情况。

本 skill 不是写论文正文，而是为以下阶段提供**可执行 checklist + 模板**：
- Pre-submission（投稿前自检）
- Submission（提交包与系统填报）
- Revision / Rebuttal（返修与回复审稿意见）
- Camera-ready / Proof（相机就绪、校样阶段）

模板文件在 `templates/`：
- `pre-submission-checklist.md`
- `rebuttal-response-matrix.md`
- `camera-ready-checklist.md`
- `cover-letter.md`

---

## 何时使用

触发关键词：
- `投稿`、`submission`、`cover letter`、`highlights`
- `返修`、`revision`、`rebuttal`、`回复审稿意见`
- `camera-ready`、`proof`、`校样`
- `checklist`、`自检清单`

---

## 输入（最小信息）

1) 投向（期刊/会议/出版社）
2) 阶段（pre-submission / submission / revision / camera-ready）
3) 文档格式（LaTeX/Word/Quarto）

---

## 核心元规则（最容易漏）

### 1) Checklist 要“绑定产物”

每条 checklist 不是“建议”，而是能指向某个文件/位置：
- “图 2 导出 600dpi TIFF” → `figures/fig-02/out/fig-02.tiff`
- “统计检验写清楚” → `manuscript/methods.md#统计` 或 `main.tex` 对应段落

### 2) 返修回应要“可追踪”

每条 reviewer comment 必须对应：
1) 你做了什么改动（行动）
2) 你怎么回应（回复）
3) 改动在哪里（定位：页码/行号/章节）

模板：`templates/rebuttal-response-matrix.md`

---

## 交付建议（落地）

推荐固定输出一个 “submission bundle 目录”：
- `submission/cover-letter.md`
- `submission/highlights.md`
- `submission/submission-manifest.yml`
- `revision/rebuttal.md`（返修时）

并在 `submission-manifest.yml` 记录每个关键检查项是否完成。

