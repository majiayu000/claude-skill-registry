---
name: LaTeX工具
description: 从官方或内置模板创建、编译和校验数学建模 LaTeX 论文项目，并可配合 DOCX 工具把完整 LaTeX 论文转换为 Word。
---

# LaTeX 工具

## 路径与写入

- 当前目录为 `LATEX_TOOL_ROOT`，只读。
- 模板和脚本从本目录读取；论文项目只写入 `PROJECT_ROOT`。
- 官方模板、题目附件和 Skill 文件保持只读；先复制，再填充。
- 默认不覆盖已有输出目录。
- 初始化生成 `latex-project.json`，记录主入口、竞赛配置、模板来源、版本、哈希与资源绑定；不要手工删除或伪造。

## 环境诊断

开始初始化和写作前，按官方模板选择引擎与参考文献后端并执行：

```powershell
python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" doctor `
  --engine xelatex `
  --bibliography-backend biber `
  --need-pandoc
```

仅生成 LaTeX/PDF 时省略 `--need-pandoc`。诊断会检查 `latexmk`、所选引擎、BibTeX/Biber、`pypdf`、`pdfimages`、`pdftoppm`，需要生成 Word 时再检查 Pandoc。任一必需项缺失都先报告阻塞，不要写完整论文后才发现无法编译或校验。

## 模板优先级

1. 用户提供的当届官方 LaTeX 模板项目。
2. 从目标竞赛官方网站取得的当届 LaTeX 模板项目。
3. `assets/templates/cumcm/` 或 `assets/templates/mcm-icm/` 构建基线。

内置模板只在没有官方 LaTeX 模板时使用，不替代当届官方规则。复制官方模板目录时保留其 `.cls`、`.sty`、`.bst`、字体和图片资源，不重写导言区或文档类。

## 初始化

```powershell
python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" init `
  "<PROJECT_ROOT>/完整论文-LaTeX" `
  --contest cumcm `
  --template "<PROJECT_ROOT>/当届官方LaTeX模板" `
  --main "src/paper.tex" `
  --template-source "<官方模板页面URL>" `
  --template-version "<适用届次或版本>"
```

没有官方模板时同时省略 `--template`、`--main` 和模板元数据。官方模板入口为 `main.tex` 或只有一个顶层 `.tex` 时可省略 `--main`；入口位于子目录或存在多个候选文件时必须按官方说明显式指定，不能猜测。CUMCM、MCM/ICM 以外的竞赛使用 `--contest generic`，且必须提供当届官方模板。初始化后在复制件中填充正文，并把核验后的 BibTeX 条目放入项目；不得修改模板源文件。

## 绑定代码与图表资源

代码和图表的权威版本保留在 `PROJECT_ROOT`，不要只在 LaTeX 项目中维护第二份。把需要随论文交付的代码或图表复制到 LaTeX 项目后，立即建立哈希绑定：

```powershell
python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" bind `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  "<PROJECT_ROOT>/figures" `
  "figs"

python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" bind `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  "<PROJECT_ROOT>/code" `
  "code"
```

权威代码位于项目根目录时也可逐文件绑定，例如把 `<PROJECT_ROOT>/问题1_求解.py` 绑定到现有副本 `code/问题1_求解.py`。命令只在权威来源与现有副本内容一致时写入 `latex-project.json`，不会替用户复制或覆盖文件。权威来源或副本变化后，先重新同步文件，再重跑 `bind`。校验和编译会扫描任意目录中的新增或已修改代码、数据和图像资源，并阻断缺失、未绑定或哈希漂移的副本，不局限于固定目录名。

## 编译

优先使用 `latexmk` 管理交叉引用和参考文献；未安装时，只对不含外部 BibTeX/BibLaTeX 文献库的项目回退为连续两次运行指定引擎。含外部文献库的完整论文必须安装 `latexmk`。默认使用 XeLaTeX，且不启用 shell escape。实际编译在系统临时目录中的完整项目副本执行，真实源码目录保持只读语义；编译后再次比较副本与原始源码哈希，任何改写都会阻断发布。

```powershell
python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" build `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  --engine xelatex `
  --timeout 180 `
  --publish "<PROJECT_ROOT>/完整论文.pdf"
```

若官方模板明确要求 LuaLaTeX 或 pdfLaTeX，再改用 `--engine lualatex` 或 `--engine pdflatex`。缺少宏包时报告环境问题，不自动联网安装，也不擅自替换官方文档类。编译日志中的未解析引用、LaTeX/宏包/文档类预警、Overfull/Underfull box 和字体预警默认阻断发布；构建目录可以保留失败产物用于诊断，但不会生成 `PROJECT_ROOT/完整论文.pdf`。

只有已经逐项确认且当届官方规则或用户明确允许的预警，才能用精确正则和具体理由覆盖：

```powershell
python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" build `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  --publish "<PROJECT_ROOT>/完整论文.pdf" `
  --allow-warning "Overfull \\hbox \(0\.1pt" `
  --override-reason "已在最终尺寸逐页检查，0.1pt 不造成裁切"
```

构建中间产物固定写入项目根目录的 `build/`，不接受其他 `--output-dir`，避免生成文件混入源码哈希。默认拒绝覆盖已发布 PDF；确认旧版本可以替换时才加 `--overwrite`。每次构建都会在 PDF 旁写入 `.build.json`，记录源码/PDF/模板哈希、工具版本、关键参数、原始命令、告警与覆盖理由。PDF 与清单成对替换，任一替换失败都会恢复旧文件；发布 PDF 只有在清单标记通过时才生成。

## 校验

```powershell
python "<SKILL_ROOT>/tools/latex/scripts/latex_paper.py" validate `
  "<PROJECT_ROOT>/完整论文-LaTeX/main.tex" `
  --pdf "<PROJECT_ROOT>/完整论文.pdf" `
  --contest cumcm `
  --quality-checks `
  --questions q1 q2 q3 `
  --min-image-dpi 300 `
  --max-pages <当届官方正文上限> `
  --body-start-page <正文在PDF中的第一页>
```

论文包含附录时再加 `--appendix-start-page <附录在PDF中的第一页>`，且源码必须真实包含 `\appendix` 或 `appendices` 环境。CUMCM 电子版 PDF 若第 1 页为摘要、正文从第 2 页开始，可传 `--body-start-page 2`；必须以实际 PDF 和当届官方模板为准。工具会尝试根据附录首个章节标题自动定位，但无法唯一定位时会阻断并要求显式页码，不能退回用 PDF 总页数猜测正文页数。`mcm-icm` 与 `generic` 的 `--max-pages` 默认校验 PDF 总页数，不套用 CUMCM 的正文口径，也不接受正文/附录页码参数。

校验器递归读取项目内的 `\input` 与 `\include`，忽略 `verbatim`、`lstlisting`、`minted`、`comment` 和 `\verb` 中的伪命令，并检查：

- 摘要、关键词和未清理占位符；
- 字词单位、成对的行间公式、非空图/表、PDF 总页数和正文页数；
- 图片文件是否存在，`label` 是否重复，图表是否有题注、真实内容和图表环境外的正文引用；
- `fig:q1-*` 等标签是否覆盖 `--questions` 声明的全部子问题；
- `\cite` 是否能在 BibTeX 或 `\bibitem` 中找到对应条目；
- 手工参考文献是否被正文引用；
- PDF 是否由当前源码构建，源码与 PDF 哈希是否匹配；
- LaTeX 项目中的代码和图表副本是否与 `PROJECT_ROOT` 权威来源绑定且未漂移；
- PDF 空白页、页面尺寸、字体嵌入和内嵌位图 DPI。

CUMCM 的约 15000 字词单位、约 20 页、5 个公式和 3 个表只是可覆盖的完整度质量目标。CUMCM 与 MCM/ICM 均默认至少 8 幅图；页数上限等官方硬约束必须从目标届次规则读取后通过参数传入。MCM/ICM 不内置永久页数阈值。

所有阈值必须是非负数，页数上限和最低 DPI 必须为正数。降低默认质量目标或临时使用 `--no-require-pdf` 跳过 PDF 审计时，必须同时传入 `--override-reason "<官方条款、用户要求或阶段性原因>"`，并由校验报告记录；跳过 PDF 的报告不能用于最终交付。质量校验必须通过 `--questions` 明确列出全部子问题，不能只为问题一集中出图。

安全编译链不启用 shell escape，因此 `\includegraphics` 只直接接受 PDF、PNG、JPG/JPEG。编程手仍可保留可编辑 SVG 源图，但论文引用前必须从同一绘图代码导出 PDF 或 PNG；不要依赖编译期 SVG/EPS 转换。

通过自动校验后仍需用 `pdftoppm` 渲染并打开编译 PDF，抽检摘要页、分页、页眉页脚、字体、公式、表格、图片和参考文献。源码正则、PDF 对象检查或一次成功编译都不能替代版面抽检。

## 转换为 DOCX

需要同时交付 Word 时，读取 `../docx/SKILL.md`，调用 `equations.py convert-latex` 或后端 DOCX 工具的 `convert_latex` 动作。LaTeX 源码仍须独立编译 PDF；DOCX 转换不能替代 LaTeX 编译与校验。
