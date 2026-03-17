---
name: office-combo
description: "Microsoft Office 全功能支持。当 Claude 需要：（1）处理 Excel 表格（.xlsx）- 公式、格式、数据分析，（2）创建/编辑 PPT 演示文稿（.pptx），（3）处理 PDF 文档（.pdf）- 提取、合并、表单填写，（4）处理 Word 文档（.docx）- 编辑、修订跟踪、注释时使用。"
---

# Microsoft Office 全功能支持

本技能提供 Microsoft Office 文件处理能力，采用渐进式引入机制。

## 支持的格式

- **Excel (.xlsx, .xlsm, .csv, .tsv)** - 表格创建、编辑、数据分析
- **PowerPoint (.pptx)** - 演示文稿创建、编辑、设计
- **PDF (.pdf)** - 文档提取、合并、表单填写
- **Word (.docx)** - 文档创建、编辑、修订跟踪

## 渐进式引入

本技能采用按需加载机制，详细文档仅在需要时读取，避免占用初始 token。

### 上下文效率

传统方式：
- 所有详细内容加载到 SKILL.md
- 估计上下文：~5000 tokens

本技能方式：
- 元数据仅：~150 tokens
- 详细文档（按需）：~5k tokens

### 按需加载指南

当需要处理特定格式的 Office 文件时，读取对应的详细文档：

```bash
# Excel 处理
cat $SKILL_DIR/references/xlsx.md

# PowerPoint 处理
cat $SKILL_DIR/references/pptx.md

# PDF 处理
cat $SKILL_DIR/references/pdf.md

# Word 处理
cat $SKILL_DIR/references/docx.md
```

**注意**: Replace $SKILL_DIR with the actual discovered path of this skill directory.

## 使用模式

当用户请求匹配此技能的能力时：

**Step 1: 识别文件类型**（Excel / PowerPoint / PDF / Word）

**Step 2: 加载对应的详细文档**

```bash
cd $SKILL_DIR
cat references/<type>.md
```

**Step 3: 根据详细文档中的指导执行操作**

## 技能来源

本技能整合了 Anthropic 官方技能：
- xlsx - Excel 处理
- pptx - PowerPoint 处理
- pdf - PDF 处理
- docx - Word 处理

原始来源：https://github.com/anthropics/skills

---

*This skill uses progressive disclosure to minimize initial context usage*