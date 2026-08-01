---
name: section-r-packages
description: 生成 R 包使用教程 (.rmd/.qmd)，涵盖包定位、核心功能、完整示例、最佳实践。
---

---
name: section-r-packages
description: Generate comprehensive R package tutorials (tidyverse, data.table, mlr3, gtsummary, etc.) with theory + practice workflow. Use when: (1) User requests R package tutorials or reviews, (2) File names match [number]-[package].rmd pattern, (3) Keywords: tidyverse, dplyr, ggplot2, purrr, data.table, mlr3, package comparison.
---
## 核心任务

生成 R 包使用教程 (.rmd/.qmd)，涵盖包定位、核心功能、完整示例、最佳实践。

## 快速启动 (Quick Start)

1. **确定 R 包**: 如 "data.table 高效数据处理"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "包定位 -> 核心功能 -> 快速开始 -> 完整示例 -> 性能优化" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和架构示意图。
5. **质量检查**: 验证示例可复现性与导航更新。

## 完整工作流程

### 步骤1: 逐部分生成教程内容（CRITICAL - 分段生成策略）

**⚠️ 重要：教程内容超过 300 行时必须分段生成，避免一次性输出过长内容。**

**分段生成流程**：

1. **第一部分**：生成 YAML 头部 + Setup + 包简介 + 核心功能清单 + 快速开始（约 150-200 行）
2. **第二部分**：追加完整实战示例 + 性能对比 + 进阶技巧（约 150-200 行）
3. **第三部分**：追加最佳实践 + 常见问题 + 相关资源（约 100-150 行）

**内容生成要求**：
- **必须包含**: 包简介、核心功能清单、快速开始、完整实战示例
- **示例优先**: 每个功能都要有简洁但完整的可运行代码示例
- **可复现性**: 所有示例必须设置种子 `set.seed(2026)`

### 步骤1.5: 生成配图并在文章中引用（CRITICAL）

**⚠️ 必须完成的两步操作**：

**第一步：生成图片文件**

1. **封面图 (MANDATORY)**:
   - 路径：`doc/images/[number]-[topic]-cover.svg`
   - 风格：专业、展示包的核心功能

2. **文内示意图 (MANDATORY - 每篇至少 1 张)**：
   - 路径：`doc/images/diagrams/pkg-*.svg`
   - 格式：**必须使用 SVG 格式**（扩展名必须是 .svg）
   - **尺寸要求**（CRITICAL）：
     - **推荐标准尺寸**: `viewBox="0 0 1400 800"` (宽 1400, 高 800)
     - **对比表格图**: 1400×800～1400×900 (横向宽幅)
     - **功能架构图**: 1200×700～1400×800
     - **工作流程图**: 1200×600～1400×800 (横向流程)
     - **生态系统图**: 1000×700～1200×800
     - ⚠️ **避免**: 过高的纵向布局 (如 1000×1100)，会导致显示不全
   - 用途：**功能架构图、工作流程、包对比表**
   - 示例场景：
     - 包功能架构图
     - dplyr vs data.table 对比表
     - tidyverse 工作流程图
     - 包生态系统关系图

**第二步：在文章中引用图片（CRITICAL）**

⚠️ **生成图片后必须立即用 Markdown 语法在文章中引用！**

```markdown
## 功能架构

![data.table 核心功能架构](images/diagrams/pkg-datatable-arch.svg)

**架构说明**：上图展示了 data.table 的核心功能模块及其相互关系。
```

**插入位置**：
- 架构图 → "包简介"或"核心功能"章节
- 对比表 → "性能对比"章节
- 工作流程图 → "快速开始"章节

**验证**：
```bash
grep "!\[.*\](images/diagrams/" doc/[number]-[topic].rmd
```

### 步骤2: 验证渲染 (CRITICAL)

在提交前必须进行本地渲染验证，确保代码可运行且格式正确。

```bash
# 渲染单文件验证内容
quarto render doc/[number]-[package].rmd

# 确保无报错、包缺失或格式问题
```

### 步骤3: 更新导航系统 (CRITICAL)

必须执行以下步骤，否则新文章无法在网站侧边栏 and 分类页显示。

1. **更新 `doc/_quarto.yml`**:

   - 找到 `sidebar` -> `contents` -> `实用 R 包` 部分。
   - 添加新条目，**注意缩进**:
     ```yaml
               - text: "文章标题"
                 href: "[number]-[package].rmd"
     ```
2. **更新 `doc/0001-guide.rmd`**:

   - 在对应分类的表格中添加一行：
     ```markdown
     | [包名] | [文章标题]([number]-[package].html) | [简短说明] |
     ```
3. **运行自动生成脚本 (MANDATORY)**:

   - 此脚本会根据 `_quarto.yml` 更新 `sections/packages.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `📦 实用 R 包` 的对应折叠块中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/packages.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/[number]-[package].rmd doc/images/[number]-[topic]-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/packages.qmd
   git commit -m "feat(pkg): 新增[包名]教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **函数**: 包内函数明确使用 `package::function()`。
- **参数**: 每个重要参数都要在代码注释或文字中解释。
- **数据**: 优先使用内置数据集，避免外部文件依赖。

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [package-comparison.md](references/package-comparison.md): 常用 R 包对比参考。
