---
id: "2e07da3b-c28c-47d5-8c1d-94bbd800052c"
name: "government-report-formatting-policy"
description: "A reusable policy for formatting government reports with standardized authorship, institutional, and temporal metadata fields."
version: "0.1.0"
tags:
  - "government"
  - "report"
  - "formatting"
  - "metadata"
triggers:
  - "添加撰写人单位日期"
  - "政府报告落款格式"
  - "报告末尾署名规范"
  - "政务文档元数据格式"
---

# government-report-formatting-policy

A reusable policy for formatting government reports with standardized authorship, institutional, and temporal metadata fields.

## Prompt

# Goal
Format a government report by appending three mandatory metadata lines at the end: '撰写人：XXX', '单位：XXX', '日期：XXX年XXX月XXX日'.

# Constraints & Style
- Never invent or infer values for '撰写人', '单位', or '日期'; always use literal 'XXX' as placeholder.
- If the model has real-time date access, it may substitute the current date in 'YYYY年MM月DD日' format; otherwise, strictly use 'XXX年XXX月XXX日'.
- No additional text, footnotes, asterisks, or explanatory comments after these three lines.
- Preserve all prior report content unchanged; only append the metadata block.

## Triggers

- 添加撰写人单位日期
- 政府报告落款格式
- 报告末尾署名规范
- 政务文档元数据格式
