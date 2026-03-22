---
name: long-doc-generator
description: 超长文档生成工具，支持项目文档、商业文案、技术规格书。触发词：生成文档、写方案、技术规格书。
version: v1.0
---

# Long-Doc-Generator Skill

> **用途**: 生成超长文档（项目尺度、商业尺度、技术规格书）
>
> **研究基础**: 100+ 篇技术文章/官方文档分析

---

## 能力矩阵

| 场景 | 规模 | 支持度 |
|------|------|--------|
| 项目尺度文档 | <50K tokens | ✅ 完全支持 |
| 商业尺度文案 | 50K-200K tokens | ✅ 支持 |
| 技术规格书 | 200K+ tokens | ⚠️ 需多次会话 |

---

## 使用方法

```bash
# 基础用法
node ~/ai-projects/skills/long-doc-generator/scripts/generate.mjs "生成 API 文档"

# 指定文档类型
node ~/ai-projects/skills/long-doc-generator/scripts/generate.mjs "技术方案" --type proposal

# 深度研究模式
node ~/ai-projects/skills/long-doc-generator/scripts/generate.mjs "市场调研" --deep
```

---

## 核心技术

### 1. 层级分块 (Header-Based Chunking)

按 Markdown 标题层级自动分块，保持文档结构完整性。

### 2. 结构化摘要 (Structured Summarization)

每完成一章，生成结构化摘要保存上下文。

### 3. 进度追踪 (Progress Tracking)

实时写入进度文件，支持会话中断后恢复。

### 4. 质量审查 (Quality Review)

内置审查清单，确保文档质量。

---

## 输出格式

```markdown
## 文档信息
- 标题：XXX
- 生成时间：2026-03-15
- 总字数：XX,XXX
- 章节数：X

## 生成日志
- [x] Phase 1: 大纲生成
- [x] Phase 2: 第 1 章
- [x] Phase 3: 第 2 章
- [ ] Phase 4: 第 3 章
```

---

## 配置文件

```json
{
  "chunk_strategy": "header",
  "max_chunk_tokens": 4000,
  "output_limit": 25000,
  "progress_file": "progress.md",
  "auto_save": true
}
```

---

## 参考文档

- [研究报告](../../../.claude/insights/reports/long-output-technical-control.md)
- [Anthropic 上下文工程指南](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

*Skill v1.0 - 基于深度研究成果*
