---
name: section-operations
description: 生成实用操作类教程 (.rmd/.qmd)，涵盖数据处理、工具使用、工作流优化，强调 "任务目标 → 工具选择 → 操作步骤 → 结果验证"。
---

---
name: section-operations
description: Generate comprehensive R practical operation tutorials (data import/export, cleaning, transformation, regex, web scraping, environment setup) with theory + practice workflow. Use when: (1) User requests data processing or tool setup tutorials, (2) File names match 30xx-*.rmd pattern, (3) Keywords: readr, stringr, lubridate, rvest, RMarkdown/Quarto setup, Positron/RStudio config.
---
## 核心任务

生成实用操作类教程 (.rmd/.qmd)，涵盖数据处理、工具使用、工作流优化，强调 "任务目标 → 工具选择 → 操作步骤 → 结果验证"。

## 快速启动 (Quick Start)

1. **确定任务**: 如 "正则表达式处理字符串 (Regex)"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "目标 -> 准备 -> 基础操作 -> 实战案例 -> 进阶技巧" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和流程示意图。
5. **质量检查**: 验证路径规范与导航更新。

## 完整工作流程

### 步骤1: 生成教程内容与封面

按 [content-structure.md](references/content-structure.md) 结构生成文件。

- **必须包含**: 任务目标、准备工作、分步骤操作流程、至少一个实战案例。
- **操作导向**: 每步都应可直接操作，并提供预期输出说明。
- **封面图 (MANDATORY)**: 必须生成 `doc/images/[number]-[topic]-cover.svg`。
- **原理图**: 复杂逻辑，结构图，代码不好展现的，必须AI生图生成 `doc/images/diagrams/stat-*.svg（或者png），由AI直接生成`，比如一些思维导图，可视化内容。使用md语法在文章内引用

### 步骤2: 验证渲染 (CRITICAL)

在提交前必须进行本地渲染验证，确保代码可运行且格式正确。

```bash
# 渲染单文件验证内容
quarto render doc/[number]-[topic].rmd

# 确保无报错、包缺失或格式问题
```

### 步骤3: 更新导航系统 (CRITICAL)

必须执行以下步骤，否则新文章无法在网站侧边栏和分类页显示。

1. **更新 `doc/_quarto.yml`**:

   - 找到 `sidebar` -> `contents` -> `实用操作` 部分。
   - 添加新条目，**注意缩进**:
     ```yaml
               - text: "文章标题"
                 href: "[number]-[topic].rmd"
     ```
2. **更新 `doc/0001-guide.rmd`**:

   - 在对应分类的表格中添加一行：
     ```markdown
     | [主题名] | [文章标题]([number]-[topic].html) | [简短说明] |
     ```
3. **运行自动生成脚本 (MANDATORY)**:

   - 此脚本会根据 `_quarto.yml` 更新 `sections/operation.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `🛠️ 实用操作` 的对应折叠块中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/operation.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/[number]-[topic].rmd doc/images/[number]-[topic]-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/operation.qmd
   git commit -m "feat(ops): 新增[主题]实用操作教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **路径**: 优先使用相对路径 + `here` 包，避免硬编码绝对路径。
- **验证**: 每个关键步骤提供验证代码和检查清单。
- **风格**: 遵循 tidyverse 风格指南，适当添加注释。

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [data-cleaning-workflow.md](references/data-cleaning-workflow.md): 数据清洗标准工作流。
