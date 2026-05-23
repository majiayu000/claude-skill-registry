---
name: section-intro-guide
description: Generate comprehensive R introductory guides (learning paths, basic concepts, beginner tutorials) with theory + practice workflow. Use when: (1) User requests R introductory tutorials, (2) File names match 00xx-*.rmd pattern, (3) Keywords: beginner, learning path, basic knowledge, RStudio setup, RMarkdown intro.
---
## 核心任务

生成符合初学者需求的入门指南类教程 (.rmd/.qmd)，强调 "概念 → 流程 → 代码 → 解释" 结构，确保 70% 文字 + 30% 代码比例。

## 快速启动 (Quick Start)

1. **确定主题**: 如 "R 语言数据结构 (Data Structures)"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "目标 -> 路线 -> 概念 -> 实践 -> 错误纠偏" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和学习路径图。
5. **质量检查**: 验证文字比例与导航更新。

## 完整工作流程

### 步骤1: 生成教程内容与封面

按 [content-structure.md](references/content-structure.md) 结构生成文件。

- **必须包含**: `## 教程目标与适用场景` 到 `## 进阶扩展` 的标准结构。
- **文字比例**: 必须确保文字解释占 70% 以上，假设读者是零基础。
- **封面图 (MANDATORY)**: 必须生成 `doc/images/00[number]-[topic]-cover.svg`。
- **原理图**: 复杂逻辑，结构图，代码不好展现的，必须AI生图生成 `doc/images/diagrams/stat-*.svg（或者png），由AI直接生成`，比如一些思维导图，可视化内容，使用md语法在文章内引用

### 步骤2: 验证渲染 (CRITICAL)

在提交前必须进行本地渲染验证，确保代码可运行且格式正确。

```bash
# 渲染单文件验证内容
quarto render doc/00[number]-[topic].rmd

# 确保无报错、包缺失或格式问题
```

### 步骤3: 更新导航系统 (CRITICAL)

必须执行以下步骤，否则新文章无法在网站侧边栏和分类页显示。

1. **更新 `doc/_quarto.yml`**:

   - 找到 `sidebar` -> `contents` -> `入门指南` 部分。
   - 添加新条目，**注意缩进**:
     ```yaml
               - text: "文章标题"
                 href: "00xx-filename.rmd"
     ```
2. **更新 `doc/0001-guide.rmd`**:

   - 在对应分类的表格中添加一行：
     ```markdown
     | [主题名] | [文章标题](00xx-filename.html) | [简短说明] |
     ```
3. **运行自动生成脚本 (MANDATORY)**:

   - 此脚本会根据 `_quarto.yml` 更新 `sections/guide.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `🏗️ 开发环境` 或相关折叠块中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/guide.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/00xx-*.rmd doc/images/00xx-*-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/guide.qmd
   git commit -m "feat(guide): 新增[教程标题]入门教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **语言**: 客观、科学、结构清晰，以段落叙述为主。
- **代码**: 优先使用 `pkg::fn()`；随机过程设置 `set.seed(2026)`。
- **标题**: 使用中文标题，层级清晰（一级到三级）。

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [learning-roadmap.md](references/learning-roadmap.md): R 语言学习路线参考。
