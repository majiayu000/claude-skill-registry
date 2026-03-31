---
name: latex-submission-pipeline
description: "LaTeX submission pipeline: templates, local build (latexmk), bibliography (bibtex/biber), lint (chktex), formatting (latexindent), CI build (GitHub Actions), and submission zip packaging."
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# LaTeX Submission Pipeline（LaTeX 投稿工程链）

## 适用

当用户需要：
- 套用期刊/会议 LaTeX 模板（ACM/IEEE/NeurIPS 等）
- 解决编译错误、引用错误、字体缺失、图片格式不兼容
- 接入 GitHub Actions 自动编译 PDF / 打包 submission zip
- 做格式化（latexindent）与 lint（chktex）

---

## 最小流程（从 0 到可提交）

### 1) 选择模板与约束

用 `venue-templates` 找对应模板或官方要求：
- 页边距、双栏/单栏、匿名/非匿名、附录策略

### 2) 本地可复现构建

推荐统一入口（任选其一）：
- `latexmk -pdf -interaction=nonstopmode -halt-on-error`
- 或在项目中提供 `scripts/build.ps1` / `scripts/build.sh`

### 3) 引用稳定（BibTeX/Biber）

元规则：
- `.bib` 是 source-of-truth
- 同一项目不要混用手工引用与 BibTeX（至少主文统一）

### 4) 图表导出与兼容性

对投稿系统最稳的组合：
- 矢量：`PDF`（matplotlib 导出）
- 栅格：`TIFF 600dpi`（显微/照片/heatmap 视情况）

### 5) Lint + Format（可选但强烈建议）

- Lint：`chktex`（常见 LaTeX 坑）
- Format：`latexindent`（减少 diff 噪声）

### 6) CI 自动编译（GitHub Actions）

模板：`templates/github-actions-latex.yml`（参考 `xu-cheng/latex-action`）

---

## 常见失败点（速查）

- 图像格式：EPS/PDF/PNG/TIFF 混用导致编译失败（优先统一 PDF）
- 字体：投稿要求嵌入字体（PDF 检查）
- Overfull box：大量警告影响排版质量（需要在关键位置修）
- 参考文献缺字段：DOI/年份/期刊名缺失造成审稿人观感差

