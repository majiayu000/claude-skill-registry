---
name: claudecode
description: Agent Skill（Claude Skill）是 Anthropic 推出的一种基于文件系统的模块化能力标准。它本质上是一种“渐进式披露”
  (Progressive Disclosure)的提示词管理机制。
---

## 1.  概念：Agent Skill

**定义**：
Agent Skill（Claude Skill）是 Anthropic 推出的一种**基于文件系统的模块化能力标准**。它本质上是一种“渐进式披露” (Progressive Disclosure)的提示词管理机制。
### 核心比喻：一本“带目录的书”
传统的 System Prompt 往往把所有规则一次性塞给 AI，既浪费 Token 又容易让模型混淆。Agent Skill 将能力分层管理，就像一本书：
*   **第1层：元数据 (Metadata) ≈ 目录**
    *   **内容**：技能的名称 (`name`) 和简短描述 (`description`)。
    *   **加载机制**：**始终加载**。AI 只看目录，判断“用户的问题我需不需要查这本书”。
    *   **优势**：极度节省 Token，几乎不占内存。
*   **第2层：指令 (Instructions) ≈ 正文**
    *   **内容**：具体的 Prompt、操作步骤、约束条件。
    *   **加载机制**：**按需加载**。只有当 AI 决定调用该技能时，才会读取这部分内容进入上下文。
*   **第3层：资源 (Resources) ≈ 附录**
    *   **内容**：辅助脚本 (`scripts/`)、模板文件 (`templates/`) 或参考数据。
    *   **加载机制**：**按需调用**。在指令执行过程中被引用时才读取。
### Agent Skill的特点
1.  **标准化**：不仅仅是 Claude，Cursor、Codex、OpenCode 等新一代 AI 编程工具均开始支持此标准。
2.  **低消耗**：解决了“随着能力增加，Context Window 爆炸”的问题。
3.  **配合 MCP**：Skill 定义“SOP（标准作业程序）”，MCP 提供“工具接口（如读写文件）”，两者结合实现复杂的 Agent 工作流。

---

## 2. Skill配置指南
假设您已安装好 `Claude Code` 并通过 `settings.json` 配置了 DeepSeek/GLM 等兼容模型，以下是加载skill的完整流程。

### 📂 第一步：建立“技能库”
Claude Code 会自动扫描用户根目录下的 `.claude/skills` 文件夹。

**标准路径结构**（请务必遵守此层级）：
```text
C:\Users\用户名\.claude\skills\        <-- skill所在目录
│
├── 📂 pdf-summary\                    <-- [技能包] 文件夹名建议用 kebab-case
│   │
│   ├── 📄 SKILL.md                    <-- [🔴 核心] 必须叫 SKILL.md (大写)
│   │
│   ├── 📂 scripts\                    <-- [手脚] 存放 Python/Bash 脚本
│   │   └── 🐍 extract.py
│   │
│   └── 📂 templates\                  <-- [素材] 存放输出模板
│       └── 📄 format.txt
│
└── 📂 git-automator\                  <-- 另一个技能包
    └── 📄 SKILL.md
```

### 📝 第二步：编写 `SKILL.md` (标准定义)
这是 Agent Skill 标准的核心。Claude 会先读取 Frontmatter (元数据) 来决定何时调用。
**你并不需要亲自撰写SKILL.md，网络上有很多官方/第三方的优质SKILL，比如GitHub上的awesome-claude-skills。**

**文件内容示例 (`C:\Users\用户名\.claude\skills\xlsx\SKILL.md`)**：
````markdown

---
# 【1. 元数据区 / Metadata】
# 作用：Claude 启动时只会读取这一小部分。description 必须准确概括功能，
# 只有当用户的问题与这段描述匹配时，下方的指令区才会被加载。

name: csv-data-summarizer
description: 使用 Python 和 pandas 分析 CSV 文件，生成统计摘要并绘制快速可视化图表。
metadata:
  version: 2.1.0
  dependencies: python>=3.8, pandas>=2.0.0
---

# CSV Data Summarizer
<!-- 【2. 指令区 / Instructions】 -->
<!-- 作用：当技能被触发后，Claude 会遵循这里的规则去执行任务 -->

## When to Use (触发时机)
当用户满足以下条件时使用此 Skill：
- 上传或引用了一个 CSV 文件
- 要求对表格数据进行摘要、分析或可视化
- 想要了解数据的结构和质量

## Critical Behavior (核心行为准则)
⚠️ **绝对准则**：
1. **禁止询问用户意图**：不要问 "你想让我做什么？" 或提供选项。
2. **立即执行全量分析**：自动运行分析、生成所有相关图表并展示结果。
3. **智能适配**：根据数据内容（销售、客户、财务等）自动决定分析方向，无需用户指定。

## Automatic Steps (自动化步骤)
1. **加载与检查**：读取 CSV 到 pandas DataFrame。
2. **识别结构**：判断列类型（日期、数值、分类）。
3. **执行分析**：根据数据类型生成统计数据（如时间序列趋势、相关性热力图等）。
4. **生成输出**：一次性展示概览、统计数据、缺失值分析和可视化图表。

---

# Files
<!-- 【3. 资源区 / Resources】 -->
<!-- 作用：列出此 Skill 需要调用的具体文件（位于同级目录中） -->

- `analyze.py` - 核心分析逻辑代码
- `requirements.txt` - Python 依赖库列表
- `resources/sample.csv` - 用于测试的示例数据

````

### 🚀 第三步：加载与触发
1.  **重启 Claude Code**：
    关闭并重新打开终端，输入 `claude` 启动。
2.  **检查加载**：
    在对话框中输入指令 `/doctor` 或者直接问它：
    > "你现在加载了哪些 skills？"
    它会列出已发现的技能，例如：`pdf-summary-pro`。
3.  **触发使用**：
    无需特殊命令，直接用自然语言：
    > "帮我读一下桌面上这个 annual_report.pdf，我要看财报摘要"
    Claude 会识别意图 -> 自动命中 `SKILL.md` -> 执行内部逻辑。

---

## 3. 补充

### 核心机制：渐进式披露
Claude 不是一次性把所有 Skill 的内容都塞进 Context (上下文) 里的。
1.  **启动时**：只加载 `SKILL.md` 顶部的 `name` 和 `description` (元数据)。这几乎不消耗 Token。
2.  **命中时**：只有当用户的问题与 `description` 匹配时，Claude 才会将该 `SKILL.md` 的正文和相关脚本加载进上下文。
*这意味着你可以安装 100 个技能，而不会让 Claude 变笨或变慢。*

### 安全提示
下载别人的 Agent Skill (比如从 GitHub 上的 `awesome-claude-skills`) 时要格外小心。
因为 Agent Skill 标准允许包含 `scripts/` 文件夹，**这意味着它可以在你的电脑上执行任意 Python/Shell 代码**。在运行陌生 Skill 之前，务必检查 `scripts/` 下的代码逻辑。

### 完全自主权
如果想给claude code完全自主权，而不是每次调用skill或更改代码都询问你是否同意，那么，可以使用这个命令来启动claude code:

```bash
claude --dangerously-skip-permissions
```

但是，就像这个命令内容一样，dangerously（危险地），开启后 Claude 拥有了**完全的自主权**。
- **风险**：它可能会直接修改你的代码、删除文件、安装依赖或执行 shell 命令，而不会再次征求你的同意。
- **建议**：仅在你信任当前任务环境，或者在版本控制（Git）已经提交了代码（方便回滚）的情况下使用此模式。

## 4. 最终文件夹层级结构 - 样例：

```text
C:\Users\用户名\.claude\skills\                  <-- 【根目录】所有 Skill 的存放位置
│
├── 📂 pptx-creation/                          <-- 【Skill 1】PPT 演示文稿生成助手
│   │                                              (参考自 anthropics/skills/pptx)
│   │
│   ├── 📄 SKILL.md                            <-- 🔴 核心：定义 "制作PPT" 的指令入口
│   │                                              (内容：指示Claude调用Python脚本生成幻灯片)
│   │
│   ├── 📂 scripts/                            <-- 执行代码库
│   │   └── 🐍 generate_slides.py              <-- 脚本：使用 python-pptx 库构建 PPT 文件
│   │
│   └── 📂 assets/                             <-- 静态资源库
│       ├── 📊 corporate_template.pptx         <-- 模板：包含公司Logo和配色方案的主母版
│       └── 📄 layout_config.json              <-- 配置：定义标题、正文在页面上的坐标位置
│
└── 📂 xlsx-analysis/                          <-- 【Skill 2】Excel 数据清洗与分析
    │                                              (参考自 anthropics/skills/xlsx)
    │
    ├── 📄 SKILL.md                            <-- 🔴 核心：定义 "分析表格" 的指令入口
    │                                              (内容：指示Claude读取Excel并生成图表)
    │
    ├── 📂 scripts/                            <-- 执行代码库
    │   ├── 🐍 clean_data.py                   <-- 脚本：使用 pandas 清洗空值和错误格式
    │   └── 🐍 create_pivot_table.py           <-- 脚本：自动生成数据透视表
    │
    └── 📂 examples/                           <-- 示例库 (用于 Few-Shot Prompting)
        ├── 📄 prompt_examples.txt             <-- 教程：教 Claude 如何写对应的 Python 代码
        └── 📉 sample_output.xlsx              <-- 样例：期望的输出格式参考文件
```