---
name: slides-as-code
description: "Build research slides with text-first source (Slidev/Marp/Reveal/Quarto) and reproducible export (PDF). Includes structure, figure reuse rules, and quality checklist for top-tier scientific presentations."
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Slides as Code（顶级科研汇报的可复现幻灯片）

## 目标

解决常见问题：
- PPT 版本失控（final_v7）
- 图表重复截图、清晰度崩坏
- 汇报结构不稳定（信息密度失衡）

本 skill 让 slides 拥有：
- 文本源（Markdown / Quarto / LaTeX Beamer）
- 可复现导出（PDF、可选 PPTX）
- 图表复用（直接引用 `figures/` 最终导出，不截图）

---

## 技术路线（按约束选）

1) **Slidev**：开发者友好，组件化，适合组会/技术分享  
2) **Marp**：排版可控，适合快速生成简洁风格  
3) **Reveal.js**：网页交互强，适合 demo/交互展示  
4) **Quarto slides**：报告/论文/幻灯片一体化（推荐用于报告+slides联动）  

> 内容结构建议使用 `scientific-slides`；本 skill 更偏“工程化与导出管线”。

---

## 元规则（幻灯片质量的 80/20）

### 1) 一页一结论

- 标题就是结论，不是主题
- 每页只服务一个问题：What / Why / How / So what

### 2) 图不截图

- 图只从 `figures/**/out/` 引用（PDF/SVG/PNG）
- 禁止从论文 PDF 截图再贴回 PPT

### 3) 讲述顺序固定

推荐骨架：
1) 背景与缺口（1–2 页）
2) 方法直觉（1–2 页示意图）
3) 核心结果（3–6 页，每页一图一结论）
4) 局限与下一步（1–2 页）

---

## 模板

参考：`templates/slidev-structure.md`

