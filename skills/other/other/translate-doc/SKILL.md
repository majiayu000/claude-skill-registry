---
name: translate-doc
description: Translate project documents between Chinese and English, supporting single files, directories, and batch modes while preserving formatting and domain terminology
---

# Translate Doc

翻译项目中的文档文件（中↔英），支持单文件、目录批量、和全项目模式。适用于 docs/、demos/、README 等所有 Markdown 文件。

## Trigger

```
/translate-doc <target>           # 单文件或目录
/translate-doc <target> --to en   # 强制指定目标语言
```

- `<target>` 可以是：
  - 单个文件路径：`docs/aider.md`、`demos/aider/search-replace/README.md`
  - 目录路径：`demos/aider/`（翻译目录下所有 .md 文件）
  - 特殊关键词：`all-docs`（翻译 docs/ 下所有分析文档）

## 语言检测与输出

### 自动检测方向

- 文档主要语言为中文 → 翻译为英文
- 文档主要语言为英文 → 翻译为中文
- 可用 `--to en` 或 `--to zh` 强制指定

### 输出路径规则

| 源文件 | 输出文件 |
|--------|----------|
| `docs/aider.md` | `docs/aider.en.md` |
| `demos/aider/README.md` | `demos/aider/README.en.md` |
| `demos/aider/search-replace/README.md` | `demos/aider/search-replace/README.en.md` |
| `README_CN.md` | `README.md`（特殊处理） |

后缀规则：`<name>.<target-lang>.md`（如 `.en.md`、`.zh.md`）

## 保持不变的内容

以下元素 **不翻译**：

1. **代码块**（``` 围栏块）— 保持原样
2. **行内代码**（`反引号`内容）— 保持原样
3. **文件路径** 和 **URL** — 保持原样
4. **技术标识符** — 变量名、函数名、类名、CLI flag
5. **Mermaid/ASCII 图表** — 保持原样
6. **YAML frontmatter** — 保持原样
7. **表格结构** — 翻译单元格内容，保留 `|` 和 `-` 格式
8. **HTML 注释标记** — 如 `<!-- PROGRESS_START -->` 等 marker，保持原样
9. **Skill 命令** — 如 `/analyze-agent`、`/create-demo` 等，保持原样

## 领域术语表

翻译时使用统一的术语对照，确保跨文档一致性：

| 中文 | English | 备注 |
|------|---------|------|
| 主循环 | Agent Loop | |
| 上下文管理 | Context Management | |
| 上下文窗口 | Context Window | |
| 编辑应用 | Edit Apply | |
| 工具系统 | Tool System | |
| 提示词工程 | Prompt Engineering | |
| 错误处理与恢复 | Error Handling & Recovery | |
| 关键创新点 | Key Innovations | |
| 跨 Agent 对比 | Cross-Agent Comparison | |
| MVP 组件 | MVP Components | 不翻译 MVP |
| 进阶机制 | Advanced Mechanisms | |
| 完整串联 | Full Integration | |
| 分析文档 | Analysis Doc | |
| 机制复现 | Mechanism Reproduction / Demo | |
| 维度 | Dimension | 如 D1-D8 |
| 单一数据源 | Single Source of Truth | |
| 浅克隆 | Shallow Clone | |
| 覆盖缺口 | Coverage Gap | |
| 分析漂移 | Analysis Drift | |

首次出现技术术语时，可附带原文：如 "Agent Loop（主循环）" 或 "主循环 (Agent Loop)"。后续出现直接使用目标语言。

## 翻译质量要求

- 保持相同的标题层级（`#`、`##`、`###` 等）
- 保持相同的章节编号
- 保留 Markdown 格式（加粗、斜体、列表、链接）
- 使用自然、地道的目标语言表达
- 中译英时避免直译，用英文技术文档的惯用表达
- 英译中时保留常用英文技术术语不强行翻译（如 agent、demo、hook、skill）

## 工作流

### 单文件模式

1. 读取源文件
2. 检测主要语言
3. 按上述规则翻译
4. 写入翻译文件（与源文件同目录）
5. 报告：源文件、目标文件、翻译方向

### 目录模式

1. 扫描目录下所有 `.md` 文件（不含已有的 `.en.md`/`.zh.md` 翻译件）
2. 列出待翻译文件清单，确认后开始
3. 逐一翻译，跳过已有最新翻译的文件
4. 汇总报告：翻译了 N 个文件，跳过 M 个

### all-docs 模式

1. 扫描 `docs/` 下所有 `<agent>.md`（排除 TEMPLATE.md 和已有翻译件）
2. 列出待翻译清单
3. 逐一翻译
4. 汇总报告
