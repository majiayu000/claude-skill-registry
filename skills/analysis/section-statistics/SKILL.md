---
name: section-statistics
description: 生成统计分析方法类教程 (.rmd/.qmd)，确保理论背景、模型假设、完整分析流程与结果解释并重。
---

---
name: section-statistics
description: Generate comprehensive R statistical method tutorials (regression, survival analysis, causal inference, Bayesian stats) with theory + practice workflow. Use when: (1) User requests statistical method tutorials, (2) File names match 10xx-*.rmd pattern, (3) Keywords: PSM, Cox, Meta-analysis, RCS, multilevel models, SEM, PCA, LCA.
---
## 核心任务

生成统计分析方法类教程 (.rmd/.qmd)，确保理论背景、模型假设、完整分析流程与结果解释并重。

## 快速启动 (Quick Start)

1. **确定方法**: 如 "泊松回归 (Poisson Regression)"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "通俗解释 -> 理论 -> 代码 -> 解读" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和原理示意图。
5. **质量检查**: 使用 [quality-checklist.md](references/quality-checklist.md) 验证导航更新。

## 完整工作流程

### 步骤0: 文件编号分配 (CRITICAL - 避免重复)

**在创建任何文件前，必须先确定可用编号！**

1. **检查现有编号**:

   ```bash
   ls doc/10*.rmd doc/10*.qmd | sort | tail -20
   ```
2. **选择下一个可用编号**:

   - 找到当前最大编号 (如 1099)
   - 新文件使用下一个编号 (如 1100，上一个编号＋1)
   - **绝对禁止**: 使用已存在的编号!
3. **编号冲突检测**:

   ```bash
   # 检查是否有重复编号
   ls doc/10*.rmd doc/10*.qmd | sed 's/.*\///;s/-.*//' | sort | uniq -d
   # 如果有输出，说明存在重复编号，必须先解决
   ```
4. **命名规范**:

   - 格式: `10[number]-[topic].rmd`
   - 示例: `1100-distributions.rmd`
   - 禁止: 同一编号用于不同主题

### 步骤1: 逐部分生成教程内容（CRITICAL - 分段生成策略）

**⚠️ 重要：教程内容超过 300 行时必须分段生成，避免一次性输出过长内容。**

**分段生成流程**：

1. **第一部分**：生成 YAML 头部 + Setup + 方法背景 + 核心原理 + 数据准备（约 150-200 行）
2. **第二部分**：追加模型构建 + 结果解释 + 模型诊断（约 150-200 行）
3. **第三部分**：追加进阶应用 + 常见问题 + 参考文献（约 100-150 行）
4. **验证完整性**：确认所有必需章节都已包含

**使用工具追加内容**：
- 推荐使用 `edit` 工具在特定位置插入
- 或使用 `bash` 的 `cat >> file.rmd << 'EOF'` 追加
- 每次追加后用 `wc -l` 检查行数

**内容生成要求**：
- **必须包含**: `## 方法背景与适用场景` 到 `## 参考文献` 的标准章节结构
- **零基础通俗解释**: 必须在开头用生活化类比解释核心原理
- **可复现性**: 所有随机操作必须设置种子 `set.seed(2026)`

### 步骤1.5: 生成配图并在文章中引用（CRITICAL）

**⚠️ 必须完成的两步操作**：

**第一步：生成图片文件**

1. **封面图 (MANDATORY)**:
   - 路径：`doc/images/[number]-[topic]-cover.svg`
   - 风格：学术、专业、与方法相关

2. **文内示意图 (MANDATORY - 每篇至少 1 张)**：
   - 路径：`doc/images/diagrams/stat-*.svg`
   - 格式：**必须使用 SVG 格式**（扩展名必须是 .svg）
   - **尺寸要求**（CRITICAL）：
     - **推荐标准尺寸**: `viewBox="0 0 1400 800"` (宽 1400, 高 800)
     - **对比表格图**: 1400×800～1400×900 (横向宽幅)
     - **决策树**: 1400×800 (横向布局，避免过高导致显示不全)
     - **流程图**: 1200×600～1400×800 (横向流程)
     - **DAG因果图**: 1000×700～1200×800
     - ⚠️ **避免**: 过高的纵向布局 (如 1000×1100)，会导致显示不全
   - 用途：**原理示意、流程图、对比表、决策树**
   - 示例场景：
     - 统计方法选择决策树
     - 模型假设检验流程图
     - 多种方法对比表格
     - 因果推断DAG图
     - 分析步骤流程图

**第二步：在文章中引用图片（CRITICAL）**

⚠️ **生成图片后必须立即在文章相应位置添加 Markdown 引用！**

```markdown
## 方法选择指南

![统计方法选择决策树](images/diagrams/stat-decision-tree.svg)

**决策说明**：上图展示了如何根据数据类型和研究目的选择合适的统计方法。
```

**插入位置建议**：
- 方法对比图 → "方法背景与适用场景"章节
- 流程图 → "完整分析流程"章节
- DAG图 → "因果推断"相关章节
- 假设检验图 → "模型诊断"章节

**验证图片引用**：
```bash
grep "!\[.*\](images/diagrams/" doc/[number]-[topic].rmd
```

### 步骤2: 验证渲染 (CRITICAL)

在提交前必须进行本地渲染验证，确保代码可运行且格式正确。

```bash
# 渲染单文件验证内容
quarto render doc/10[number]-[topic].rmd

# 确保无报错、包缺失或格式问题
```

**安装依赖**:
若渲染过程中提示缺少 R 包，请先安装：

```r
# 示例：安装常用统计包
install.packages(c("survival", "MatchIt", "lme4", "brms", "mediation"))
```

### 步骤3: 更新导航系统 (CRITICAL)

必须执行以下步骤，否则新文章无法在网站侧边栏和分类页显示。

**⚠️ 更新导航前务必验证**:

- 确认新文件已成功渲染
- 确认文件编号无冲突
- 确认YAML元数据正确

1. **更新 `doc/_quarto.yml`**:

   - 找到 `sidebar` -> `contents` -> `统计分析方法` 部分。
   - 添加 new 条目，**严格遵守 14 空格缩进**:
     ```yaml
               - text: "方法名称"
                 href: "10xx-filename.rmd"
     ```
2. **更新 `doc/0001-guide.rmd`**:

   - 在对应分类的表格中添加一行，保持索引同步。
3. **运行自动生成脚本 (MANDATORY)**:

   - 此脚本会根据 `_quarto.yml` 更新 `sections/statistics.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `📐 统计分析方法` 的对应表格中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/statistics.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/10xx-*.rmd doc/images/[topic]-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/statistics.qmd
   git commit -m "feat(stat): 新增[方法名称]统计教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **代码**: 优先使用 `pkg::fn()` 调用函数；必须提供完整的模拟数据生成代码。
- **解读**: 结果解读必须涵盖统计显著性与实际意义。
- **视觉**: SVG 标注必须全部使用中文。

## 代码块与表格格式规范 (CRITICAL)

### 图片居中 (MANDATORY)

**在 setup chunk 中设置全局图片居中**：

```r
knitr::opts_chunk$set(
  echo = TRUE,
  message = FALSE,
  warning = FALSE,
  fig.align = 'center'  # 所有图片居中
)
```

**或在单独代码块中设置**：

```r
```{r plot-name, fig.align='center', fig.width=8, fig.height=6}
# 图表代码
```
```

### 表格字体大小 (MANDATORY)

**所有 gt 表格必须设置合适的字体大小，避免表格过小难以阅读**：

```r
tibble(...) |>
  gt() |>
  tab_options(
    table.font.size = px(14),      # 表格字体 14px
    data_row.padding = px(8)       # 行间距 8px
  ) |>
  tab_style(
    style = cell_fill(color = "#E8F4F8"),
    locations = cells_column_labels()
  )
```

**推荐字体大小**：
- 常规表格：`px(14)`
- 大型对比表：`px(13)`
- 简洁表格：`px(15)`

**必须添加的 tab_options 参数**：
- `table.font.size`: 控制整体字号
- `data_row.padding`: 控制行间距，提升可读性
- `column_labels.font.size`: (可选) 单独设置表头字号

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [quality-checklist.md](references/quality-checklist.md): 完整质量检查与导航更新指南。
- [method-comparison.md](references/method-comparison.md): 统计方法对比表。
