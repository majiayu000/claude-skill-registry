---
id: "a4c19899-f95b-41b5-a47b-6b2b06892b68"
name: "end / size / fs"
description: "General SOP for common requests related to end, size, fs."
version: "0.1.0"
tags:
  - "end"
  - "size"
  - "fs"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# end / size / fs

General SOP for common requests related to end, size, fs.

## Prompt

Follow this SOP (replace specifics with placeholders like <PROJECT>/<ENV>/<VERSION>):
1) Offline OpenAI-format conversation source.
2) Title: e15bb1fe86f7b246f97ed628afa963a4.json#conv_1
3) Use the user questions below as the PRIMARY extraction evidence.
4) Use the full conversation below as SECONDARY context reference.
5) In the full conversation section, assistant/model replies are reference-only and not skill evidence.
6) Primary User Questions (main evidence):
7) 如何用图模型中边的权重刻画八邻域相邻像素的关联性
8) 有哪些将图像建模为图的论文和方法
9) 具体有哪些论文
10) 帮我写个matlab代码，一个矩阵，矩阵每个位置上储存了一个坐标，以每个像素为中心它的八领域可以得到两点之间的斜率和截距，八领域也就是八条直线，我想将八条直线的斜率加权求平均，得到的值作为输出矩阵中中心像素对应位置的输出值，返回一个新的矩阵，应该怎么写

For each step, include: action, checks, and failure rollback/fallback plan.
Output format: for each step number, provide status/result and what to do next.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.
