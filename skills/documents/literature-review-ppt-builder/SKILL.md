---
name: literature-review-ppt-builder
description: "将 ppt_content.md 转换为完整的 .pptx 演示文稿。当用户已有 ppt_content.md 文件（由 literature-review-ppt-generator 生成）并要求生成 PPT、制作幻灯片、导出 pptx、build ppt 时触发。需要配合原始 PDF 论文以提取配图。"
---

# Literature Review PPT Builder

将结构化的 `ppt_content.md` 转换为专业的 `.pptx` 演示文稿。

## 前置条件

- `ppt_content.md`：由 literature-review-ppt-generator 生成的 PPT 内容文件
- 原始 PDF 论文：用于提取 Figure/Table 图片
- `Template.pptx`：位于 `templates/` 目录的 PPT 模板

## 工作流程

### 1. 提取配图（使用 extract-pdf-figure skill）

**重要**: 先提取图片，确保图片文件存在于输出目录的 `asset/` 子目录。

```bash
# 批量提取 ppt_content.md 中引用的所有图表
python .claude/skills/extract-pdf-figure/scripts/extract_figures.py "PDFs/paper.pdf" --batch "Figure 1,Figure 2,Table 1" -d "$outputDir/asset/"

# 若需要仅主体内容（对应 [content-only] 标记）
python .claude/skills/extract-pdf-figure/scripts/extract_figures.py "PDFs/paper.pdf" "Figure 1" --no-extras -o "$outputDir/asset/Figure_1.png"
```

### 2. 生成 PPT

```bash
python .claude/skills/literature-review-ppt-builder/scripts/build_ppt.py \
    "$outputDir/ppt_content.md" \
    "$outputDir/asset/" \
    ".claude/skills/literature-review-ppt-builder/templates/Template.pptx" \
    "$outputDir/presentation.pptx"
```

参数说明：
| 参数 | 说明 |
|------|------|
| 参数 1 | ppt_content.md 文件路径 |
| 参数 2 | 图片目录路径 |
| 参数 3 | 模板文件路径 |
| 参数 4 | 输出 pptx 文件路径 |

### 3. 视觉检查

打开生成的 pptx 检查：
- 模板背景和分隔线是否保留
- 文字是否溢出
- 配图位置是否正确（右侧 40%）
- 粗体格式是否正确应用

---

## 与其他 Skills 的协作

### 三 Skills 工作流

```
┌─────────────────────────┐
│ literature-review-ppt-  │
│       generator         │
│                         │
│ 输入: PDF 论文          │
│ 输出: ppt_content.md    │
│       paper_summary.md  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│   extract-pdf-figure    │◄───│ 解析 ppt_content.md 中  │
│                         │    │ 的配图列表              │
│ 输入: PDF + 图表名称    │    └─────────────────────────┘
│ 输出: Figure_1.png 等   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ literature-review-ppt-  │
│        builder          │
│                         │
│ 输入: ppt_content.md    │
│       + 图片文件        │
│       + Template.pptx   │
│ 输出: presentation.pptx │
└─────────────────────────┘
```

### 图片命名对齐规范

| 组件 | 格式 | 示例 |
|------|------|------|
| **ppt-generator** 输出 | `Figure N`, `Figure N(a)`, `[content-only]` | `Figure 1`, `Figure 2(a) [content-only]` |
| **extract-pdf-figure** 输入 | 同上 | `"Figure 1"`, `"Figure 2(a)"` |
| **extract-pdf-figure** 输出 | `Figure_N.png` 或 `<pdf>_Figure_N.png` | `Figure_1.png`, `paper_Figure_1.png` |
| **ppt-builder** 查找 | 模糊匹配，支持多种格式 | 自动匹配 `Figure_1.png` 或 `*Figure_1*.png` |

### `[content-only]` 模式处理

在 `ppt_content.md` 中的 `[content-only]` 标记对应 `extract-pdf-figure` 的 `--no-extras` 参数：

```markdown
**配图**: 
- Figure 1              # 完整提取 → python ... "Figure 1"
- Figure 2 [content-only]  # 仅主体 → python ... "Figure 2" --no-extras
```

---

## 设计规范

### 字体配置

| 元素 | 字体 | 字号 | 样式 |
|------|------|------|------|
| 论文标题 | Times New Roman | 16pt | Bold |
| 来源信息 | Times New Roman | 11pt | Italic |
| 一级大纲（▶） | Times New Roman | 14pt | Bold |
| 二级大纲（▢） | Times New Roman | 12pt | Regular |
| 三级内容（•） | Times New Roman | 12pt | Regular |

### 布局规范

| 区域 | 位置 | 说明 |
|------|------|------|
| 模板区 | 顶部 1/5~3/10 | 第一页：TITLE + SOURCE；后续页：空白（保留背景和分隔线） |
| 内容起始 | 第一页 3/10，后续页 1/5 | 避开模板区 |
| 左侧文字 | 60% 宽度 | 大纲内容 |
| 右侧配图 | 40% 宽度 | 动态排布 1-4 张图 |

### 配色方案

| 元素 | 颜色代码 |
|------|----------|
| 标题 | `#1E3A5F` |
| 一级大纲 | `#2C5282` |
| 二级大纲 | `#333333` |
| 正文 | `#333333` |
| 来源信息 | `#666666` |

---

## ppt_content.md 格式说明

```markdown
# [论文完整标题]
*[来源信息]*

---

## Slide 1

▶ **1. 一级论点**
▢ 1.1 二级论点
  - 具体描述

**配图**: Figure 1, Table 2

**讲稿**:
（中文讲稿内容）

---

## Slide 2
...
```

解析规则：
- `#` 后为论文标题
- `*...*` 为来源信息
- `---` 分隔幻灯片
- `▶` 开头为一级大纲
- `▢` 开头为二级大纲
- `- ` 开头为三级内容
- `**配图**:` 后为图片列表
- `**讲稿**:` 后为 speaker notes

---

## 特殊情况处理

| 情况 | 处理方式 |
|------|----------|
| 图片提取失败 | 使用 `--mode pages` 转换后手动裁剪 |
| 文字溢出 | 减小字号或精简内容 |
| 配图模糊 | 提高 DPI 至 300 |
| 找不到图片文件 | 显示占位框提示手动插入 |
