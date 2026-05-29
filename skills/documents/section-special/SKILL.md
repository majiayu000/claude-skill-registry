---
name: section-special
description: Generate comprehensive R tutorials for specialized applications (health economics, qualitative research, signal processing, environmental epidemiology) with theory + practice workflow. Use when: (1) User requests domain-specific tutorials, (2) File names match [number]-[topic].rmd pattern, (3) Keywords: TreeAge, CEA, text mining, wavelet, VMD, DLNM, WQS, BKMR.
---
## 核心任务

生成特殊应用领域教程 (.rmd/.qmd)，涵盖领域背景、专业方法、完整流程、结果解释，强调 "领域背景 → 专业术语 → 分析框架 → 实践流程 → 结果解读"。

## 快速启动 (Quick Start)

1. **确定领域**: 如 "卫生经济学成本效果分析 (CEA)"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "背景 -> 术语 -> 原理 -> 实践 -> 领域解读" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和领域框架图。
5. **质量检查**: 验证术语准确性与导航更新。

## 完整工作流程

### 步骤1: 生成教程内容与封面

按 [content-structure.md](references/content-structure.md) 结构生成文件。

- **必须包含**: 领域背景、核心概念（中英对照）、方法原理、详尽实践步骤。
- **领域准确性**: 术语使用必须准确，遵循领域规范和指南。
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

   - 找到 `sidebar` -> `contents` -> `特殊应用` 部分。
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

   - 此脚本会根据 `_quarto.yml` 更新 `sections/special.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `🛠️ 特殊应用` 的对应折叠块中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/special.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/[number]-[topic].rmd doc/images/[number]-[topic]-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/special.qmd
   git commit -m "feat(spc): 新增[领域-方法]特殊应用教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **术语**: 首次出现的术语提供中英文对照和通俗解释。
- **解读**: 强调从领域视角（如临床意义、政策启示）解读统计结果。
- **完整性**: 包含数据伦理考虑（如适用）和报告规范说明。

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [domain-terminology.md](references/domain-terminology.md): 各领域核心术语库。
