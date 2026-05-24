---
name: paper-analyzer
description: 自动分析Zotero库中的文献，生成带LaTeX公式的Markdown报告，使用Auto-Annotation工具将AI的深度见解以无损批注形式注入回 Zotero，并将报告上传为Zotero Note。
version: 1.6.0
author: Zhaohong Liu
tags:
  - zotero
  - paper-analysis
  - auto-annotation
---

# Paper Analyzer

## 🎯 目标 (Objective)
你是一个顶级的 Robotics & AI 系统级研究员。你的核心任务是根据用户的 Prompt，连接本地 Zotero 数据库与 Cyber Brain 缓存。你需要运用多模态阅读能力深层次解析文献，输出一份公式精准的 Markdown 报告，将你的核心 Insights 转化为 JSON 格式驱动 Auto-Annotation 工具自动在用户的 Zotero PDF 上"画重点"，并最终将报告上传为 Zotero Note 挂载到论文条目。

## 🛠️ 可用工具 (Available CLI Tools)

本 Skill 依赖以下两个 CLI 脚本，位于项目 `src/scripts/` 目录下。所有脚本必须在 `jarvis` conda 环境中执行。

### 1. `src/scripts/zotero_highlight.py` - Zotero 批注注入工具
通过 Zotero Web API 向 PDF 添加高亮批注（无损注入，不修改原始 PDF）。

**用法：**
```bash
# 查看 PDF 信息（页数、尺寸）
python src/scripts/zotero_highlight.py --info <pdf_path>

# 搜索文本位置（预检查）
python src/scripts/zotero_highlight.py --search <pdf_path> <query>

# JSON 文件模式（推荐）
python src/scripts/zotero_highlight.py --json <json_file>
```

**参数：**
| 参数 | 说明 |
|------|------|
| `--info`, `-i` | 显示 PDF 信息并退出 |
| `--search`, `-s` | 跨页面搜索文本 |
| `--json`, `-j` | 从 JSON 文件读取参数 |

**可用颜色：**
- `#ffd400` - 黄色（默认）
- `#ff6666` - 红色（重要）
- `#5fb236` - 绿色（支持论点）
- `#2ea8e5` - 蓝色（定义/概念）
- `#a28ae5` - 紫色（方法论）

### 2. `src/scripts/upload_report_note.py` - 报告上传工具
将 Markdown 报告转换为 HTML 并上传至 Zotero，作为论文条目的附属 Note。

**用法：**
```bash
python src/scripts/upload_report_note.py --report <report_path> --zotero-key <item_key> [options]
```

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--report` | Markdown 报告文件路径 | (必填) |
| `--zotero-key` | **父条目 Item Key**（非 attachment_key） | (必填) |
| `--tags` | 逗号分隔的标签列表 | 无 |

**示例：**
```bash
# 上传报告并添加标签
python src/scripts/upload_report_note.py --report "./temp/SNX599P2_report.md" --zotero-key GEPUIWCR --tags summary,auto-generated

# 仅上传报告（无标签）
python src/scripts/upload_report_note.py --report "./temp/ABC123_report.md" --zotero-key XYZ789
```

**处理逻辑：**
- 转换为 Zotero 支持的 HTML 格式
- 保留标题、列表、表格、代码块、LaTeX 公式等

**返回值：**
- 成功时返回退出码 `0`，并打印 `Successfully created note: <note_key>`
- 失败时返回退出码 `1`，并打印错误信息
---

## 📋 工作流 (Execution Workflow)

请严格按照以下五个阶段的顺序执行操作。

### 阶段 1：精准定位文献 (Locate via Zotero MCP)

1.  调用 `zotero-mcp` 提供的检索工具，根据用户提供的标题或关键字找到对应的论文记录。
2.  在返回的元数据中，提取当前 PDF 附件的最关键信息。
3.  **你必须明确获取并记录以下三个变量**：
    *   `item_key`: 父条目文献的 Item Key（用于挂载 Note）。
    *   `attachment_key`: PDF 附件的 Item Key（用于批注注入和临时文件命名）。
    *   `pdf_path`: 本地硬盘中该 PDF 附件的绝对路径。

### 阶段 2：多模态认知与双轨输出 (Multimodal Synthesis)

依靠你的原生多模态能力，根据 `pdf_path` 直接阅读 PDF 内容，生成以下两部分内容。

#### 输出 A：高级 Markdown 总结报告

在生成总结报告前，你必须**首先执行领域分类**，并严格根据分类结果加载对应的分析框架。

最终生成的独立 Markdown 文件请保存为 `./temp/reports/{attachment_key}_report.md`。

**第一步：文献领域分类与框架加载 (Classification & Template Selection)**
请先阅读论文的摘要和引言，判断其所属的核心研究领域，并按以下优先级决定使用的分析模板：
1. **Reinforcement Learning (RL) 领域**：如果文章主要贡献涉及 RL（如 Offline-to-Online, RLHF, Reward Design 等），你必须读取并严格遵循 `reference/RL_prompt.md` 中的结构进行深度拆解。
2. **Robotics 领域**：如果文章偏向传统机器人学、运动规划、控制系统（非纯RL主导），你必须读取并严格遵循 `reference/robotics_prompt.md` 中的结构进行分析。
3. **General AI / 其他学术领域**：如果都不属于上述两类，请严格使用下方的**【通用进阶学术报告模板】**。

**第二步：执行总结与核心约束 (Report Generation Rules)**
无论你使用哪种模板生成报告，都必须在 Markdown 文本中严格遵守以下两条底层约束：
- **逻辑层级**：保持极高的学术严谨性，不要只停留在表面翻译，要深入拆解"为什么这么做 (Derivation & Motivation)"。
- **公式无损 (Lossless Math)**：所有的数学推导、损失函数、动力学方程等必须使用原生 LaTeX 语法输出。**行内公式使用 `$...$`，独立公式使用 `$$...$$`（使用独立公式时，`$$` 的上方和下方必须各空一行）**。

---

**【通用进阶学术报告模板】 (Fallback Template)**
*(注：仅在文章不属于 RL 或 Robotics 时使用此框架)*

```markdown
# {论文标题}

> **一句话总结 (One-Sentence Summary)**: [用极简的专业语言说明这篇文章填补了什么空白，或提出了什么核心创新]

## 1. 研究动机与逻辑演进 (Motivation & The Logic Chain)
- **核心痛点 (The Problem)**: 作者试图解决以前方法中的什么具体缺陷？
- **逻辑推进 (The Evolution)**: 提出该解决方案的直觉是什么？作者是如何顺理成章地推导出这个方法的？

## 2. 方法论与机制设计 (Methodology & Architecture)
- **系统概览**: 简述最终提出的核心架构或机制。
- **核心数学定义**:
  *(详细且准确地写出关键的数学定义、目标函数或伪代码逻辑)*

$$
L_{total} = L_{task} + \lambda L_{reg}
$$
*(必须对上述公式中出现的每一个符号进行物理或数学含义的解释)*

## 3. 实验验证 (Experimental Reality)
- **实验设置**: 简述 Benchmark、数据集或测试环境。
- **核心结论**: 定量分析的主要声明是什么？(例如："在XX数据集上提升了XX%")

## 4. 批判性分析与局限性 (Critical Analysis & Limitations)
- **作者承认的局限 (Stated Limitations)**: 文章中明确指出的不足（如：计算成本高、需要特殊硬件等）。
- **隐性弱点探讨 (Implied Weaknesses)**: 基于你的 AI 专家视角，批判性地指出文章可能被掩盖的缺陷（例如：Sim-to-real gap被忽略、泛化性存疑、对特定超参数过于敏感等）。

**关键约束：**
- **学术框架**：按照 Motivation, Method, Experiments, Limitations 的框架组织
- **公式无损**：所有数学公式使用 LaTeX 语法（`$...$` 或 `$$...$$`，使用 `$$...$$` 时需要上下各空一行）
- **输出语言**：使用中文输出，但对专业术语保持英文原文
---

#### 输出 B：Auto-Annotation 批注动作列表

-   **路径**: `./temp/annotation/{attachment_key}_annotations.json`
-   **内容**: 一个 JSON 数组，包含 5-8 个最具决定性的句子及其批注。

**🎨 强制颜色语义规范 (Strict Color Coding)**
*   🟡 `"#ffd400"`: **研究动机与痛点**
*   🔴 `"#ff6666"`: **核心创新与机制**
*   🟢 `"#5fb236"`: **实验细节与关键结论**
*   🟣 `"#a28ae5"`: **局限性与隐性假设**
*   🔵 `"#2ea8e5"`: **关键定义与基础**

**🧠 批注点评要求 (Comment Depth)**
`comment` 字段必须以 **"💡 AI Insight: "** 或 **"⚠️ 批判性思考: "** 开头，深入解释引文在论文逻辑链中的作用。

**📝 JSON 格式示例**
```json
[
  {
    "pdf_path": "D:/Zotero/storage/ABC123/paper.pdf",
    "attachment_key": "ABC123",
    "target_text": "However, traditional search-based methods suffer from...",
    "page": 0,
    "comment": "💡 AI Insight: 核心痛点 - 点出了传统规划器的实时性缺陷。",
    "color": "#ffd400"
  },
  {
    "pdf_path": "D:/Zotero/storage/ABC123/paper.pdf",
    "attachment_key": "ABC123",
    "target_text": "We formulate the problem as a Markov Decision Process...",
    "page": 2,
    "comment": "💡 AI Insight: 核心创新点 - 本文最关键的MDP设计。",
    "color": "#ff6666"
  }
]
```
**注意**: `target_text` 字段应为要高亮的原文文本。避免在其中包含数学符号或希腊字母。

### 阶段 3：执行无损批注注入 (Trigger Auto-Annotation)

1.  **创建目录**: 确保 `./temp/annotation/` 目录存在。
2.  **写入 JSON**: 将阶段 2 生成的批注列表写入 `./temp/annotation/{attachment_key}_annotations.json`。
3.  **强制预检查**: 在注入批注前，使用 `--search` 模式验证文本位置，确保页码正确。
    ```bash
    python src/scripts/zotero_highlight.py --search "{pdf_path}" "你想高亮的纯英文关键词"
    ```
4.  **执行注入**: 调用 `zotero_highlight.py` 工具，使用 `--json` 模式执行批注。
    ```bash
    python src/scripts/zotero_highlight.py --json "./temp/annotation/{attachment_key}_annotations.json"
    ```
    该工具会逐条处理 JSON 文件中的所有批注对象。

### 阶段 4：上传报告至 Zotero (Upload Report as Note)

将阶段 2 生成的 Markdown 报告转换为 HTML 并上传至 Zotero，作为论文条目的附属 Note。

**工具说明：**
`src/scripts/upload_report_note.py` 会自动：
1. 读取 Markdown 报告文件
2. 转换为 HTML 格式
3. 通过 Zotero Web API 创建 Note 并挂载到指定条目

**执行命令模板：**
```bash
python src/scripts/upload_report_note.py --report "./temp/reports/{attachment_key}_report.md" --zotero-key {item_key} --tags summary,auto-generated
```
**注意**: `--zotero-key` 必须使用阶段 1 获取的 `item_key` (父条目)。

**参数说明：**
| 参数 | 说明 | 示例 |
|------|------|------|
| `--report` | Markdown 报告文件路径 | `./temp/reports/SNX599P2_report.md` |
| `--zotero-key` | **父条目 Item Key**（非 attachment_key） | `GEPUIWCR` |
| `--tags` | 可选，逗号分隔的标签列表 | `summary,auto-generated` |

⚠️ **重要**：`--zotero-key` 必须使用阶段 1 获取的 `item_key`（父条目）.

**成功标志：**
- 返回退出码 `0`
- 打印 `Successfully created note: XXXXXXXX`

### 阶段 5：同步归档至 Obsidian (Sync to Obsidian Vault)

将生成的 Markdown 报告归档到 Obsidian。

1. **读取内容**：读取本地临时文件 `./temp/reports/{attachment_key}_report.md` 的内容。
2. **写入文件**：将内容写入 Obsidian 的收件箱路径（通常为 `00 Inbox/{Paper_Title}.md`）。Use Obsidian MCP.
3. **添加 Frontmatter**：确保 Markdown 文件头包含 YAML Frontmatter，以便后续分类器识别。如果生成的报告中没有，请在写入时添加：
   ```yaml
   ---
   tags: [robotics]
   title: {Paper_Title}
   ---
   ```
  具体tag, date根据论文和实际时间填入; For tags, do not use brackets, just a comma-separated string.

---
## 🧠 系统指令与学术准则
-   **Critical Thinking**: 在报告和批注中，需保持对 Sim-to-real Gap, Real-time Performance, Sensor Latency, Generalization 等方面的学术审视。
-   **Error Recovery**: 如果批注注入时发生坐标定位错误，请尝试缩短 `target_text` 并避免使用数学符号。
-   **环境要求**: 所有 Python 脚本必须在 `jarvis` conda 环境中执行。

---
## 🔧 故障排除 (Troubleshooting)
-   **文本匹配失败**:
    1.  使用 `--search` 预检查文本位置和页码。
    2.  确保 `target_text` 不含数学符号/希腊字母，优先使用纯英文。
    3.  工具会自动尝试缩短文本，但手动缩短至 10-20 词可能更有效。
-   **JSON 路径解析错误**: 确保 JSON 中的文件路径使用正斜杠 `/` 或双反斜杠 ``。
-   **中文乱码**: `zotero_highlight.py` 的 `--json` 模式默认使用 UTF-8，可解决此问题。
-   **SSL 连接错误**: 工具内置了指数退避重试。如果持续失败，请检查网络和 Zotero 同步状态。