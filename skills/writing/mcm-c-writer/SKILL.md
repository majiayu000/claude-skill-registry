---
name: mcm-c-writer
description: Paper/memo writer for COMAP MCM/ICM Problem C. Use when you need to draft the 1-page Summary Sheet, 1-2 page memo/letter, and the main report narrative with clear assumptions, model explanation, validation, uncertainty, and citations. References LaTeX template in MCM-Latex-template.
---

# MCM/ICM C题论文手（Summary + Memo + Report）

## 目标

- 用“评委友好”的结构写清楚：你做了什么、为什么合理、结果有多可靠、能给什么建议。
- 输出三件套：
  - **One-page Summary Sheet**
  - **One- to two-page memo/letter**（写给题目指定对象）
  - **Main report**（方法与验证细节）

## 模板入口（本仓库）

- 优先使用：`MCM-Latex-template/MCM-main.tex`（及同目录 sty）
- 目标是把你最终内容“塞进模板结构”，而不是反过来改模板。

## 默认产物口径（与代码协作）

- 图：`outputs/figures/`（png/pdf）
- 表：`outputs/tables/`（csv/tex）
- 预测与区间：`outputs/predictions/`（csv）

写作要求：正文中引用任何图/表，必须能在上述目录里找到对应文件名（便于赛时协作）。

## 写作工作流

1. **先定“叙事骨架”（先写标题与小标题）**
   - Problem restatement（用你自己的话重述目标与输出）。
   - Assumptions & Data policy（必须写外生数据是否允许）。
   - Model 1/2/3（对应题目子问）。
   - Validation & Uncertainty（区间、稳健性、误差来源）。
   - Recommendations（面向对象的可执行建议）。
   - Limitations（诚实但不自毁）。

2. **Summary Sheet（1 页）固定配方**
   - **一句话任务**：我们要预测/分类/制定策略……
   - **方法概览**：用到的核心模型（最多 3 个词组）。
   - **关键发现 3 条**：每条带一个数字/区间。
   - **建议 3 条**：每条可行动、可落地。
   - **不确定性一句话**：主要误差来自哪里。

3. **Memo/Letter（1-2 页）写给“非技术受众”**
   - 第一段：目的 + 结论（不要铺垫）。
   - 中段：3-5 个 bullet 讲证据（每个都能被图表支撑）。
   - 末段：行动建议 + 风险 + 下一步。

4. **Main report 的表达原则**
   - **少公式，多解释**：公式只放关键处，并解释每个符号。
   - **每个模型都必须回答**：
     - 输入是什么？输出是什么？为什么这样建？怎么验证？何时会失败？
   - 图表必须服务于“论证链”，不要堆图。

4.1 **炫技写作（让高级方法“看起来值钱”）**
   - 区间类结果必须同时给：
     - 区间水平（90%/95%）
     - 覆盖率（empirical coverage，若能算）
     - 区间宽度（越窄越好，但要保证覆盖）
   - 稳健性必须一句话总结：
     - “在不同切分/不同窗口/不同超参下，核心结论是否保持一致？”
   - 任何炫技模块都用“1 句动机 + 1 张证据图/表 + 1 句结论”写完，不写长篇教程。

5. **引用与合规**
   - 外部数据/背景材料必须给出处。
   - 若使用生成式 AI：按 COMAP 政策在文末附 “AI Use Report”（通常不计页数）。

## 质量门槛（交付前自检）

- Summary Sheet 与 Memo 在不看正文的情况下也能读懂并相信你。
- 明确写了：数据来源、外生数据政策、关键假设。
- 每个结论都有“证据载体”（表/图/区间/验证结果）。
- 有至少一段讨论模型局限与稳健性。
