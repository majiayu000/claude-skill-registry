---
name: section-ml-ai
description: 生成机器学习与 AI 类教程 (.rmd/.qmd)，涵盖算法原理、工程实践、模型评估、可解释性，强调 "问题定义 → 数据准备 → 模型训练
  → 评估优化 → 可解释性"。
---

---
name: section-ml-ai
description: Generate comprehensive R machine learning and AI tutorials (mlr3, tidymodels, xgboost, torch, etc.) with theory + practice workflow. Use when: (1) User requests ML/AI tutorials, (2) File names match 10xx-*.rmd pattern, (3) Keywords: classification, regression, clustering, feature engineering, hyperparameter tuning, random forest, SVM, neural networks.
---
## 核心任务

生成机器学习与 AI 类教程 (.rmd/.qmd)，涵盖算法原理、工程实践、模型评估、可解释性，强调 "问题定义 → 数据准备 → 模型训练 → 评估优化 → 可解释性"。

## 快速启动 (Quick Start)

1. **确定算法**: 如 "随机森林分类 (Random Forest)"。
2. **加载模板**: 阅读 [content-structure.md](references/content-structure.md) 获取 YAML 和标题结构。
3. **生成内容**: 遵循 "原理 -> 工作流 -> 训练 -> 评估 -> 调参 -> 可解释性" 流程。
4. **视觉设计**: 参考 [visual-templates.md](references/visual-templates.md) 生成封面图和算法流程图。
5. **质量检查**: 验证交叉验证与导航更新。

## 完整工作流程

### 步骤1: 逐部分生成教程内容（CRITICAL - 分段生成策略）

**⚠️ 重要：教程内容超过 300 行时必须分段生成，避免一次性输出过长内容。**

**分段生成流程**：

1. **第一部分**：生成 YAML 头部 + Setup + 教程目标 + 算法原理 + 数据准备（约 150-200 行）
2. **第二部分**：追加模型训练 + 模型评估 + 超参数优化（约 150-200 行）
3. **第三部分**：追加模型可解释性 + 实战案例 + 总结（约 100-150 行）
4. **验证完整性**：确认所有必需章节都已包含

**使用 `edit` 或 `bash` 追加内容时的注意事项**：
- 使用 `edit` 工具在特定位置插入内容
- 或使用 `cat >> file.rmd << 'EOF'` 追加大段内容
- 每次追加后检查文件行数确认成功

**内容生成要求**：
- **必须包含**: 完整的建模流程（数据划分、特征工程、训练、评估、调参）
- **可复现性**: 所有随机操作必须设置种子 `set.seed(2026)`

### 步骤1.5: 生成配图并在文章中引用（CRITICAL）

**⚠️ 必须完成的两步操作**：

**第一步：生成图片文件**

1. **封面图 (MANDATORY)**:
   - 路径：`doc/images/[number]-[topic]-cover.svg`
   - 风格：现代、专业、与主题相关
   - 工具：使用 `write` 工具创建 SVG 文件

2. **文内示意图 (MANDATORY - 每篇至少 1 张)**：
   - 路径：`doc/images/diagrams/ml-*.svg`
   - 格式：**必须使用 SVG 格式**（不要用 PNG，即使内容是 SVG 也要用 .svg 扩展名）
   - **尺寸要求**（CRITICAL）：
     - **推荐标准尺寸**: `viewBox="0 0 1400 800"` (宽 1400, 高 800)
     - **对比表格图**: 1400×800～1400×900 (横向宽幅)
     - **决策树**: 1400×800 (横向布局，避免过高导致显示不全)
     - **流程图**: 1200×600～1400×800 (横向流程)
     - **架构图**: 1000×800～1200×800
     - ⚠️ **避免**: 过高的纵向布局 (如 1000×1100)，会导致显示不全
   - 用途：**结构对比、流程图、决策树、算法原理示意**
   - 示例场景：
     - 多算法对比表格图
     - 算法选择决策树
     - ML 工作流程图
     - 特征工程流程
     - 模型架构示意图

**第二步：在文章中引用图片（CRITICAL - 必须执行）**

⚠️ **生成图片后必须立即在文章中添加引用，否则图片不会显示！**

**引用位置与方法**：

1. **封面图**：已在 YAML 头部 `image:` 字段引用，无需额外操作

2. **文内图必须用 Markdown 语法引用**：

   **正确做法**：
```markdown
## 算法对比分析

![六大聚类算法特性对比](images/diagrams/clustering-algorithms-comparison.svg)

**图示说明**：上图总结了六种算法在簇形状适应性、计算复杂度等维度的对比。
```

   **错误做法**（生成了图但不引用）：
   ```markdown
   ## 算法对比分析

   下面我们对比六种算法...
   （没有 ![...](images/...) 语法，图片不会显示）
   ```

**插入图片的最佳位置**：
- 算法对比表 → 在"总结与推荐"章节插入
- 决策树/流程图 → 在"算法选择"章节插入
- 工作流程图 → 在"教程目标"或"ML工作流程"章节插入
- 架构图 → 在"算法原理"章节插入

**图片生成与引用的完整示例**：

```markdown
# 步骤1: 使用 write 工具生成 SVG 图片
write(filePath="doc/images/diagrams/ml-workflow.svg", content="<svg>...</svg>")

# 步骤2: 在文章对应位置添加引用（使用 edit 工具）
## ML 工作流程概览

![机器学习完整工作流程](images/diagrams/ml-workflow.svg)

**流程说明**：上图展示了从数据准备到模型部署的完整流程...
```

**验证图片引用是否成功**：
```bash
# 检查文章中是否包含图片引用
grep "!\[.*\](images/diagrams/" doc/[number]-[topic].rmd
# 应该至少看到 1-2 条匹配结果
```

**⚠️ 常见错误**：
- ❌ 生成 SVG 内容但使用 `.png` 扩展名 → 图片无法显示
- ❌ 生成图片但不在文章中引用 → 图片无法显示
- ✅ 正确：生成 `.svg` 文件 + 在文章中用 Markdown 引用

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

   - 找到 `sidebar` -> `contents` -> `机器学习与 AI` 部分。
   - 添加新条目，**注意缩进**:
     ```yaml
               - text: "文章标题"
                 href: "[number]-[topic].rmd"
     ```
2. **更新 `doc/0001-guide.rmd`**:

   - 在对应分类的表格中添加一行：
     ```markdown
     | [算法名] | [文章标题]([number]-[topic].html) | [简短说明] |
     ```
3. **运行自动生成脚本 (MANDATORY)**:

   - 此脚本会根据 `_quarto.yml` 更新 `sections/machine-learning.qmd` 等分类索引页。

   ```bash
   # 在项目根目录下运行
   workdir="doc" Rscript doc/generate_sections.R
   ```
4. **更新 `README.md`**:

   - 在 `🧭 内容导航` -> `🚀 机器学习与 AI` 的对应折叠块中添加链接。

### 步骤4: 最终渲染与提交

1. **重新渲染受影响页面**:

   ```bash
   quarto render doc/sections/machine-learning.qmd
   quarto render doc/index.qmd
   ```
2. **提交代码**:

   ```bash
   git add doc/[number]-[topic].rmd doc/images/[number]-[topic]-cover.svg
   git add doc/_quarto.yml doc/0001-guide.rmd README.md doc/sections/machine-learning.qmd
   git commit -m "feat(ml): 新增[算法名称]机器学习教程"
   ```

## 写作规范

- **内容标准**:
  - **详细度**: 内容必须详尽，起到深入教程的作用。
  - **篇幅**: 不少于 300 行 (Not less than 300 lines)。
  - **比例**: 文字说明约占 70%，代码约占 30% (70% text, 30% code)。
  - **结构**: 必须提前构建全面的内容框架，然后根据框架填充详细内容。
- **框架**: 推荐使用 `mlr3` 或 `tidymodels` 现代框架。
- **指标**: 必须展示多个评估指标（如 ACC, AUC, F1 等）。
- **调参**: 必须包含超参数优化步骤（网格搜索或随机搜索）。

## 参考资源

- [content-structure.md](references/content-structure.md): 详细内容模板与标题规范。
- [visual-templates.md](references/visual-templates.md): SVG 封面与示意图模板库。
- [hyperparameter-guides.md](references/hyperparameter-guides.md): 常用算法调参指南。
