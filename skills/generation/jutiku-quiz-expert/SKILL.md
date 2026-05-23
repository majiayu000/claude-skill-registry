---
name: Jutiku_Quiz_Expert
description: 专门用于从文档生成结构化试题的智能体。分析内容属性（大纲型 vs 知识型），提取关键点，并生成 JSON 或 Markdown 格式的高质量试题。当用户要求"根据文件出题"、"创建测验"、"制作试卷"或"提取考题"时使用此技能。
version: 1.2
author: budaobu
---

# 出题专家 (Quiz Expert)

本技能将引导你完成从源文档生成专业题库的全过程。

## 路径约定

在开始执行任务前，先确定关键路径：

- **$WORK_DIR**：当前工作目录。执行 `pwd` (Linux/macOS) 或 `Get-Location` (Windows) 获取，作为所有相对路径的基准。
- **$SKILL_DIR**：本 skill 所在目录。根据 skill 名称 `Jutiku_Quiz_Expert` 定位：
  - **Linux 容器环境（实际执行环境）**: `find /mnt/skills -ipath "*/Jutiku_Quiz_Expert/SKILL.md" 2>/dev/null | head -1`
  - 获取到 SKILL.md 文件路径后，取其所在目录作为 $SKILL_DIR
  - 备选方案：直接尝试 `/mnt/skills/user/Jutiku_Quiz_Expert/` 或使用 `view /mnt/skills/` 查看目录结构
- **源文件目录**：`$WORK_DIR/`（用户上传的文件直接放在工作目录根部）
- **转换文件目录**：`$WORK_DIR/source/`（存放 markitdown 转换后的 .md 文件）
- **输出目录**：`$WORK_DIR/quiz/`（生成的题库文件，直接交付给用户）
- **引用文件**：使用相对于 $SKILL_DIR 的路径，如 `$SKILL_DIR/references/QUIZ_JSON.md`

路径结构示意：
```
$WORK_DIR/                       # 当前工作目录
├── 2023年度报告.pdf             # 用户源文件
├── source/                      # 转换后的 markdown 文件
│   └── 2023年度报告.md
├── quiz/                        # 输出目录（直接交付）
│   └── 2024-01-29_100000.json  # 或 .md（根据用户指定）
└── temp/                        # 存放其他临时处理文件

$SKILL_DIR/                      # skill 所在目录
├── SKILL.md             # skill 文件，即本文件
└── references/
    ├── QUIZ_JSON.md
    └── QUIZ_MARKDOWN.md
```

---

## 工作流程 (Workflow)

### 0. 初始化路径
1. **确定工作目录**：
   - 执行 `pwd` 获取当前工作目录，设为 `$WORK_DIR`
   
2. **定位 skill 目录**：
```bash
   SKILL_PATH=$(find /mnt/skills -ipath "*/Jutiku_Quiz_Expert/SKILL.md" 2>/dev/null | head -1)
   SKILL_DIR=$(dirname "$SKILL_PATH")
```
   - 备选方案：直接尝试 `/mnt/skills/user/Jutiku_Quiz_Expert/` 或使用 `view /mnt/skills/` 查看目录结构

3. **创建必要的子目录**：
```bash
   mkdir -p "$WORK_DIR/source" "$WORK_DIR/quiz"
```

4. **识别输出格式**：
   - 检查用户输入中是否包含格式关键词：
     - "markdown" / "md" / "可读" → 输出 Markdown 格式
     - "json" / "结构化" → 输出 JSON 格式
   - **默认格式**：JSON

### 1. 文件定位与准备
1.  **定位源文件**：在 `$WORK_DIR/` 根目录下查找用户指定的文件。
    - 使用 `view $WORK_DIR/` 列出可用文件。
    - 如果用户提供的是模糊名称，查找最匹配的文件。
    
2.  **格式转换**：
    - 如果文件**不是** `.md` 格式（例如 .doc, .docx, .pdf）：
        - **环境检查**：检查是否已安装 `python` (或 `python3`) 和 `pip`。
            - **如果未安装 Python**：
                - 告知用户需要安装 Python 3.8+。
                - **Linux**: `sudo apt install python3 python3-pip`
                - **macOS**: `brew install python`
                - **Windows**: `winget install Python.Python.3` 或访问 python.org
        - **工具检查与安装**：
            - 运行 `markitdown --version` 检查是否已安装。
            - 如果未安装：`pip install markitdown --break-system-packages`
        - **转换**：
            - 使用 `markitdown` 命令行工具将文件转换为 Markdown 格式。
            - **命令格式**：`markitdown "$WORK_DIR/{源文件名}" > "$WORK_DIR/source/{同文件名}.md"`
            - 注意：使用双引号包裹文件名以处理空格。
    - 如果已经是 `.md` 文件，复制到 `$WORK_DIR/source/{文件名}.md` 进行处理。

### 2. 内容预处理与分析
1.  **读取规则文档**：
    - 根据用户指定的输出格式，读取对应的规范文档：
      - **JSON 格式**：读取 `$SKILL_DIR/references/QUIZ_JSON.md` 了解 JSON Schema 规范
      - **Markdown 格式**：读取 `$SKILL_DIR/references/QUIZ_MARKDOWN.md` 了解 Markdown 模板规范

2.  **读取与分块检查**：
    - 读取 `$WORK_DIR/source/` 中转换后的 `.md` 文件内容。
    - **智能分块 (Smart Chunking)**：检查文本长度。
        - **如果 字符数 > 15,000**：
            - **切分策略**：按 Markdown 二级标题 (`##`) 或三级标题 (`###`) 将文档切分为多个逻辑块 (Chunks)。确保切分点不破坏段落完整性。
            - **配额分配**：根据各块的篇幅比例或重要性，分配题目生成数量（如总共 20 题，A 章节占 20% 篇幅，则分配 4 题）。
            - **执行模式**：标记为 `Batch_Mode`，后续将对每个块独立生成并合并。
        - **否则**：保持单一大文本，标记为 `Single_Mode`。

3.  **属性打分**：分析文本结构和内容（若是分块模式，取前 30% 内容或摘要进行分析），判断其类型（分值 0.0 - 1.0）：
    - **大纲型 (Outline-oriented)**：具有结构化的标题、要点、简短摘要。
    - **知识/资料型 (Knowledge/Data-oriented)**：密集的段落、详细的解释、事实、数据。

4.  **策略选择**：
    - **如果 大纲型得分 > 0.7**：使用 **大纲扩展模式**。
        - 提取大纲结构。
        - 针对每个关键点/标题，生成涵盖核心概念的题目。
    - **如果 知识型得分 > 0.7**：使用 **全覆盖模式**。
        - 分析全文内容（或逐个处理块）。
        - 生成覆盖整个内容范围的题目，确保没有遗漏重要信息。
    - **否则**：使用平衡方法。

### 3. 题目生成规则
根据选定的策略和输出格式生成题目，严格遵守对应规范文档中定义的**生成规则与约束**。

主要约束包括：
- **题型**：单选、多选、判断、填空、简答。
- **判断题**：选项固定为"正确"和"错误"。
- **难度**：按 3:5:2 比例分布简单、中等、困难题目。
- **结构**：确保所有必填字段完整（qid, type, explanation 等）。

### 4. 质量验证与修正
在生成题目之后，执行自我审查循环 (Self-Correction Loop)，确保题目质量：

1.  **准确性核查 (Fact Check)**：
    - 针对每一道题，**回溯原文**。
    - 验证：正确答案是否能从原文中找到明确依据？
    - 修正：如果发现幻觉或推断过度，根据原文修正答案或删除该题。
2.  **逻辑性核查 (Logic Check)**：
    - 检查选项：是否存在歧义？干扰项是否过于明显错误？
    - 检查解析：`explanation` 是否清晰解释了为什么选 A 而不选 B？
3.  **格式核查 (Format Check)**：
    - 验证输出结构是否符合对应的 Schema 或模板规范。
    - 确保所有必需字段 (`qid`, `lev`, `point` 等) 均已填充且类型正确。

### 5. 输出与交付
根据用户指定的格式（默认 JSON）在 `$WORK_DIR/quiz/` 目录下生成文件。

#### JSON 格式（默认）
- **路径**：`$WORK_DIR/quiz/{YYYY-MM-DD_HHMMSS}.json`
- **格式**：遵循严格的 JSON 语法。
- **Schema**：参见 `$SKILL_DIR/references/QUIZ_JSON.md`

#### Markdown 格式（可选）
- **路径**：`$WORK_DIR/quiz/{YYYY-MM-DD_HHMMSS}.md`
- **格式**：用户友好的可读格式。
- **模板**：参见 `$SKILL_DIR/references/QUIZ_MARKDOWN.md`

#### 交付方式
- 使用 `present_files` 工具将生成的文件直接展示给用户。
- 用户可通过界面下载文件。

## 工具与命令
- 使用 `pwd` 获取当前工作目录。
- 使用 `view` 查看目录和文件（跨平台统一接口）。
- 使用 `bash_tool` 执行命令（在 Linux 容器中运行，支持标准 bash 语法）。
- 使用 `create_file` 保存最终输出文件。
- 使用 `present_files` 交付文件给用户。

## 用户请求示例

### 示例 1：默认 JSON 格式
> "根据 `2023年度报告.pdf` 生成 20 道题目"

执行流程：
1. **初始化**：获取 $WORK_DIR 和 $SKILL_DIR，创建子目录，识别输出格式为 JSON（默认）
2. **读取规范**：`view $SKILL_DIR/references/QUIZ_JSON.md`
3. **查找**：在 `$WORK_DIR/` 找到 `2023年度报告.pdf`
4. **转换**：`markitdown "$WORK_DIR/2023年度报告.pdf" > "$WORK_DIR/source/2023年度报告.md"`
5. **分析**：数据密集 → 知识型模式
6. **生成**：创建 20 道题目（财务统计、战略目标等）
7. **输出**：保存到 `$WORK_DIR/quiz/2024-01-29_100000.json`
8. **交付**：`present_files` 展示文件给用户

### 示例 2：指定 Markdown 格式
> "根据 `Python入门.docx` 生成 15 道题目，输出为 markdown 格式"

执行流程：
1. **初始化**：获取路径，创建子目录，识别输出格式为 Markdown
2. **读取规范**：`view $SKILL_DIR/references/QUIZ_MARKDOWN.md`
3. **查找与转换**：处理 `Python入门.docx`
4. **分析**：大纲结构 → 大纲扩展模式
5. **生成**：创建 15 道题目
6. **输出**：保存到 `$WORK_DIR/quiz/2024-01-29_100000.md`
7. **交付**：展示文件给用户