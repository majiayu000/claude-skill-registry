---
name: DOCX工具
description: 创建、编辑、校验和转换 Word DOCX，支持把完整 LaTeX 论文转换为 DOCX，以及数学建模论文模板、原生公式、三线表、修订和批注。
---

# DOCX 工具

## 路径与写入

- 当前目录为本工具根目录，只读。
- 模板和脚本从本目录读取。
- 生成或修改后的 DOCX 必须写入用户 `PROJECT_ROOT`。
- 默认不覆盖输入文件或 Skill 文件。

## 数学建模论文推荐流程

采用“当届官方参考模板 + `python-docx` 构建 + OMML 公式 + OOXML 校验 + 渲染抽检”。官方模板控制页面、样式、分节、页眉页脚和编号；代码负责稳定写入内容。

```python
from pathlib import Path
import sys

scripts = Path("<SKILL_ROOT>") / "tools" / "docx" / "scripts"
sys.path.insert(0, str(scripts))
import paper_format as pf

doc = pf.new_document(
    contest="cumcm",
    template_path=Path("<PROJECT_ROOT>") / "当届官方模板.docx",
    preserve_template_content=False,
)
# 此示例只借用模板样式后追加正文。
# 若官方模板包含固定摘要页或编号页，应改为 True 并在原位置填充。
pf.title(doc, "论文题目")
pf.abstract_title(doc)
pf.body(doc, "摘要正文。")
pf.keywords(doc, "优化；预测")
pf.equation(doc, r"\min f(x)=\sum_{i=1}^{n}x_i^2")
pf.three_line_table(doc, [["符号", "说明"], ["x", "决策变量"]])
pf.save_document(doc, Path("<PROJECT_ROOT>"), contest="cumcm")
```

## 公式

### 直接写入

`scripts/equations.py` 把常用 LaTeX 子集转成 Word 原生 OMML。未知命令、未闭合分组和不支持环境会报错，不会静默生成错误文本。

```powershell
python scripts/equations.py replace "输入.docx" `
  --replace "EQ_OBJECTIVE" "\min f(x)=\sum_{i=1}^{n}x_i^2" `
  --output "<PROJECT_ROOT>/输出.docx"
```

同一占位符出现多次时会全部替换。支持分式、上下标、根式、n 次根、常用希腊字母与关系符号、反三角函数和常见矩阵，包括 `\nu`、`\mu`、`\approx`、`\arcsin`、`\arccos`、`\arctan`。

### 复杂公式

复杂 LaTeX 优先使用 Pandoc 的成熟转换：

```powershell
python scripts/equations.py generate "论文.md" `
  --output "<PROJECT_ROOT>/论文.docx" `
  --template "官方模板.docx"
```

转换后仍须校验和渲染抽检。

## 完整 LaTeX 论文转 DOCX

此功能需要预先安装 [Pandoc](https://pandoc.org/installing.html)，并保证 `pandoc` 命令可用；可先运行 `python scripts/check_env.py` 检查。工具将 `.tex` 主入口转换为 DOCX，从 LaTeX 项目目录读取相对图片，使用 citeproc 处理 BibTeX 引用，并把公式写为可编辑 OMML。传入当届官方 DOCX 作为参考模板，以继承 Word 样式和页面设置：

```powershell
python scripts/equations.py convert-latex `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  --output "<PROJECT_ROOT>/完整论文.docx" `
  --template "<PROJECT_ROOT>/当届官方模板.docx" `
  --timeout 120
```

工具会在转换前递归展开项目内的 `\input` 与 `\include`，但保留注释和字面量环境中的原文，拒绝越界路径和循环包含；转换成功后生成同名 `.conversion.json`，记录全部输入文件、输入/输出/模板哈希、Pandoc 路径与版本、命令、耗时和警告。DOCX 与清单成对替换，失败时恢复旧版本。默认拒绝覆盖已有输出；确认替换旧版本时才使用 `--overwrite`。

Pandoc 向标准错误输出的任何警告都会默认阻断发布，失败时不会留下 DOCX。只有逐项检查后，才能用精确正则和具体理由覆盖：

```powershell
python scripts/equations.py convert-latex `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  --output "<PROJECT_ROOT>/完整论文.docx" `
  --template "<PROJECT_ROOT>/当届官方模板.docx" `
  --allow-warning "<已核对的精确警告正则>" `
  --override-reason "<不影响交付的证据>"
```

自定义宏、LaTeX 专用环境、浮动体位置、交叉引用和参考文献样式可能需要在 Word 中修正。未提供 CSL 时 citeproc 使用 Pandoc 默认引文样式，因此竞赛要求特定引文格式时仍须在 Word 中核对。转换完成后必须执行 DOCX 结构校验、清单核对和渲染抽检，不能把“成功生成文件”等同于版式合格。

转换后以及交付前都要重新验证清单；源码、任一子文件、图片、BibTeX、参考模板、DOCX 或清单发生变化后必须重新转换：

```powershell
python scripts/equations.py verify-conversion `
  "<PROJECT_ROOT>/完整论文.docx"
```

## 解包、校验与重打包

DOCX/XLSX 共用的 OOXML 基础工具只保留在 `scripts/office/`：

```powershell
python scripts/office/unpack.py "输入.docx" "<PROJECT_ROOT>/unpacked"
python scripts/office/validate.py "<PROJECT_ROOT>/输出.docx"
python scripts/office/pack.py "<PROJECT_ROOT>/unpacked" "<PROJECT_ROOT>/输出.docx" --original "输入.docx"
```

不要在不理解 OOXML 关系和内容类型的情况下直接修改压缩包。

## 修订

```powershell
python scripts/accept_changes.py "输入.docx" "<PROJECT_ROOT>/已接受修订.docx"
```

工具使用隔离的 LibreOffice 配置。超时、非零退出或残留修订标记都会失败，失败时不发布输出文件。

## 批注

先解包，再添加批注元数据和文档标记。父批注不存在或批注 ID 重复时，工具会在写入前失败。

```powershell
python scripts/comment.py "<PROJECT_ROOT>/unpacked" 0 "批注意见"
python scripts/comment.py "<PROJECT_ROOT>/unpacked" 1 "回复意见" --parent 0
```

## 必做验证

```powershell
python scripts/check_env.py
python scripts/self_check.py
python scripts/office/validate.py "<PROJECT_ROOT>/完整论文.docx"
python scripts/paper_format.py validate "<PROJECT_ROOT>/完整论文.docx" --contest cumcm --rendered-pages <DOCX实际渲染页数>
python scripts/equations.py verify-conversion "<PROJECT_ROOT>/完整论文.docx"
```

`verify-conversion` 仅适用于由本工具的 Pandoc 转换生成、带 `.conversion.json` 的 DOCX；直接由 `paper_format.py` 构建时省略。`paper_format.py validate` 输出结构化指标，并在官方前置结构、篇幅质量目标、公式/图/表数量、图表编号与正文引用、参考文献双向对应或实际页数任一不满足时返回非零退出码。所有竞赛默认至少 8 幅图；CUMCM 默认的 15000 字词单位和约 20 页只是质量目标。以 2026 年官方规范为例，正文不超过 30 页才是硬约束。只有当届官方规则或用户明确要求允许偏离时才能调整目标并记录依据。结构校验后，把 DOCX 渲染成 PDF 或图片抽检分页、公式、表格、图片、页眉页脚和字体替换。
