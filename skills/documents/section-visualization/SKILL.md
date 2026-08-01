---
name: section-visualization
description: 生成数据可视化类教程 (.rmd/.qmd)，涵盖图表原理、绘图代码、样式美化、结果解读。
---

---
name: section-visualization
description: Generate comprehensive R data visualization tutorials (ggplot2, chart types, styling, publication-ready plots) with theory + practice workflow. Use when: (1) User requests visualization tutorials, (2) File names match 20xx-*.rmd pattern, (3) Keywords: boxplot, scatterplot, heatmap, forestplot, sankey, ggplot2 styling, color palettes.
---
## 核心任务

生成数据可视化类教程 (.rmd/.qmd)，涵盖图表原理、绘图代码、样式美化、结果解读。

## 快速启动 (Quick Start)

1. **确定图表**: 如 "箱线图 (Boxplot)"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "图表用途 -> 数据准备 -> 绘图流程 -> 美化技巧 -> 解读说明" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和原理示意图。
5. **质量检查**: 使用 [quality-checklist.md](references/quality-checklist.md) 验证导航更新。

## 完整工作流程

### 步骤1: 逐部分生成教程内容（CRITICAL - 分段生成策略）

**⚠️ 重要：教程内容超过 300 行时必须分段生成，避免一次性输出过长内容。**

**分段生成流程**：

1. **第一部分**：生成 YAML 头部 + Setup + 图表用途 + 数据准备 + 基础图表（约 150-200 行）
2. **第二部分**：追加中级图表 + 美化技巧 + 主题定制（约 150-200 行）
3. **第三部分**：追加高级应用 + 常见问题 + 相关资源（约 100-150 行）
4. **验证完整性**：确认至少包含 3 个图表示例

**内容生成要求**：
- **必须包含**: 至少 3 个图表示例（基础 → 中级 → 高级）
- **可复现性**: 所有随机数据必须设置种子 `set.seed(2026)`

### 步骤1.5: 生成配图并在文章中引用（CRITICAL）

**⚠️ 必须完成的两步操作**：

**第一步：生成图片文件**

1. **封面图 (MANDATORY)**:
   - 路径：`doc/images/[number]-[topic]-cover.svg`
   - 风格：视觉吸引、展示图表类型

2. **文内示意图 (MANDATORY - 每篇至少 1 张)**：
   - 路径：`doc/images/diagrams/viz-*.svg`
   - 格式：**必须使用 SVG 格式**（扩展名必须是 .svg）
   - **尺寸要求**（CRITICAL）：
     - **推荐标准尺寸**: `viewBox="0 0 1400 800"` (宽 1400, 高 800)
     - **对比表格图**: 1400×800～1400×900 (横向宽幅)
     - **决策树**: 1400×800 (横向布局，避免过高导致显示不全)
     - **配色方案展示**: 1200×600～1400×700
     - **布局示意图**: 1000×600～1200×700
     - ⚠️ **避免**: 过高的纵向布局 (如 1000×1100)，会导致显示不全
   - 用途：**图表类型对比、配色方案、布局结构**
   - 示例场景：
     - 图表类型选择决策树
     - 常用配色方案展示
     - 布局排列示例
     - ggplot2 图层结构图
     - 图表对比表格

**第二步：在文章中引用图片（CRITICAL）**

⚠️ **生成图片后必须立即用 Markdown 语法在文章中引用！**

```markdown
## 图表类型选择指南

![常见图表类型选择决策树](images/diagrams/viz-chart-selection.svg)

**使用说明**：根据数据类型和展示目的，参考上图快速选择合适的图表。
```

**插入位置**：
- 配色方案图 → "配色方案"章节
- 图表选择树 → "图表用途"章节
- 布局示例 → "图形组合"章节

**验证**：
```bash
grep "!\[.*\](images/diagrams/" doc/[number]-[topic].rmd
```

### 步骤2: 验证渲染 (CRITICAL)

在提交前必须进行本地渲染验证，确保代码可运行且图片生成正确。

```bash
# 渲染单文件验证内容
quarto render doc/20[number]-[topic].rmd

# 确保图片生成在 doc/figure/ 目录下，无报错
```

### 步骤3: 更新导航系统 (CRITICAL)

必须执行以下步骤，否则新文章无法在网站侧边栏和分类页显示。

1. **更新 `doc/_quarto.yml`**:

   - 找到 `sidebar` -> `contents` -> `数据可视化` 部分。
   - 添加新条目，**注意缩进**:
     ```yaml
               - text: "文章标题"
                 href: "20xx-filename.rmd"
     ```
2. **更新 `doc/0001-guide.rmd`**:

   - 在对应分类的表格中添加一行：
     ```markdown
     | [图表名] | [文章标题](20xx-filename.html) | [简短说明] |
     ```
3. **运行自动生成脚本 (MANDATORY)**:

   - 此脚本会根据 `_quarto.yml` 更新 `sections/visualization.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `📈 数据可视化` 的对应表格中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/visualization.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/20xx-*.rmd doc/images/[topic]-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/visualization.qmd
   git commit -m "feat(viz): 新增[图表类型]可视化教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **图文比例**: 目标是每个代码块都有对应的图表输出。
- **配色**: 优先使用 `ggsci` 期刊配色、`ColorBrewer` 或 `viridis` (色盲友好)。
- **注释**: 每张图都要包含标题、坐标轴标签、图例标题。

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [quality-checklist.md](references/quality-checklist.md): 完整质量检查与导航更新指南。
- [color-palettes.md](references/color-palettes.md): 常用配色方案参考。
