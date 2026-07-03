---
name: agf-writing-pptx-reports
description: 用 python-pptx 写"现代化中文制度 / 党政 / 企业宣贯 PPT"（含决议书提报、评审报告、管理办法、培训宣贯等 23 页量级 deck）。当用户要求程序化生成 PPT 且抱怨"老土 / 字体丑 / 表格乱 / 文字溢出 / 中文字体 fallback / 缺架构图"时启用——`python-pptx` 默认 API 一堆坑必须主动避开。提供：路径决策 / 设计 token / 12 个 helper 全套 / 7 个致丑反模式 / 12 个关键技巧 / LibreOffice 渲染验证闭环 / 跨平台中文字体生效 lxml 写法 / 配套 draw.io 画架构图选型（中文字体、配色、8 大坑、嵌入 PPT 链路）。
---

# 写 pptx 报告 — 高密度实战手册

> 沉淀自《AI 4A 架构评审管理办法》v1.0 PPT 实战（23 页，GAC 红主调，含双视图嵌入流程图），全部踩过 + 验证过的坑与方法。重型参考材料在 `references/`，按下方索引**按需 Read 全文**，不要凭记忆写代码。

## 何时用本 skill

| 信号 | 用本 skill |
|---|:--:|
| 需要程序化生成 PPT（数据驱动 / 模板批量 / 内容版本化） | ✅ |
| 中文制度 / 党政 / 企业内部宣贯 deck | ✅ |
| 用户反馈"老土 / 字体丑 / 表格乱 / 文字溢出 / 中文字体 fallback" | ✅ |
| 内容会反复迭代，PPT 必须从源码可重生成 | ✅ |
| 需要 mermaid 流程图嵌入 + 双视图卡片化 | ✅ |
| 高度自由排版 / 视觉冲击型营销 deck | ❌ 直接 Keynote / Figma |
| 复杂动画 / 视频嵌入 | ❌ python-pptx 弱项 |
| 一次性单页海报 | ❌ 直接画 |
| 要 docx / xlsx | ❌ 转 writing-docx-reports / xlsx skill |

## 路径决策（4 选 1）

| 路径 | 何时选 | 代价 |
|---|---|---|
| **手动复制 .pptx 模板编辑** | 一次性 deck / 设计师介入 / 不需重生成 | 几分钟；后续维护成本高 |
| **`pptx` skill 局部改** | 已有 .pptx 做小幅修改（≤ 5 张 slide / 仅换文字）| 中等；不适合从零生成 |
| **基于模板 + `python-pptx` 混合** ⭐ | 仓库已有 .pptx 模板 / 视觉风格已定 / 需版本化 + 重生成 | 一次 ~500 行；保留模板视觉投入 + 代码可重跑 |
| **`python-pptx` 全定制** | 没现成模板 / 视觉自己定义 / 跨平台中文 / 23+ 页量级 | 一次 ~800 行 Python，复用率 90% |

判定经验：
- **本仓库 `template/` 已有 1 个 .pptx 模板**（`Template.pptx`，coral 团队风）→ 默认走"基于模板 + python-pptx 混合"，不要重造视觉
- **用户说"老土 / 中文字体不对 / 表格乱"** 基本意味着要"模板混合"或"全定制"——只有"手动复制"路径根治不了
- **用户给了具体模板路径**（如 "用 Template.pptx"）→ 必走"模板混合"路径，并先读对应的 `template-*-guide.md`

## References 索引（什么时候必读哪份）

| 场景 | 必读（Read 全文） |
|---|---|
| 走"基于模板 + python-pptx 混合"路径（动手前） | [`references/template-based-generation.md`](./references/template-based-generation.md)（7 步流程 / 模板分析三件套 / Placeholder vs Shape / 关键文件指针）+ 对应 `template-*-guide.md`（如 [`template-team-guide.md`](./template-team-guide.md)）|
| 写 helper / 设计 token / 字号 layout / 品牌色板（任何写代码前） | [`references/design-tokens-and-techniques.md`](./references/design-tokens-and-techniques.md)（设计 token + 12 个关键技巧完整代码 + 品牌色获取 3 步）+ [`template.py`](./template.py)（可直接 `python3 template.py` 跑样例）|
| deck 缺架构 / 流程 / 矩阵图（走 draw.io 前） | [`diagram-generation-guide.md`](./diagram-generation-guide.md)（500 行：安装 CLI / mxGraph 模板 / AGF token / 字号体系 / 8 大致丑坑 / 批量工作流 / 嵌入链路）|
| mermaid 出图嵌 PPT / 多 PNG 合 PDF 提报 / 查外部资源链接与沉淀来源 | [`references/rendering-and-embedding.md`](./references/rendering-and-embedding.md) |
| 操作 .pptx 底层（unpack / thumbnail / pack） | [`.claude/skills/pptx/SKILL.md`](../pptx/SKILL.md)（Anthropic 低层 skill）|

## 工具链（macOS 实测）

| 用途 | 工具 | 装法 |
|---|---|---|
| **PPT 生成** | `python-pptx ≥ 1.0` | `pip3 install --user --break-system-packages python-pptx` |
| **XML 微调**（EA 字体 / 表格属性 / 阴影） | `lxml` | 通常已装 |
| **PPT → PDF**（实际渲染验证）| `soffice`（LibreOffice）| `brew install --cask libreoffice` |
| **PDF → PNG**（视觉验证）| `pdftocairo`（poppler）| `brew install poppler` |
| **多 PNG → PDF 合并** | `sips`（系统自带）+ `pdfunite` | `brew install poppler` |
| **mermaid 流程图** | `mmdc` | `brew install mermaid-cli` |

⚠ **不要装 PrinceXML**（商业 + 免费版水印）；不要走 `pandoc --pdf-engine=prince` 这条路。

## ★ 图层 — 架构图 / 流程图先于 PPT

- deck 里 5+ 张架构 / 流程 / 矩阵 / 决策图 → **图先行 + 单独生成 PNG → PPT 嵌入**
- 选型速判（≤ 5min）：deck 总图数 ≤ 10 → 全 Mermaid；> 10 张或需"视觉一致" → 全 draw.io 沉本到底，**不混搭**（完整选型表见 guide §1）
- 触发信号：用户说"deck 缺图 / 架构看不懂 / 文字墙"；某 slide 描述完没图可塞；派单含"需要 N 张架构图"或"图先行"
- 走 draw.io 前**先读 `diagram-generation-guide.md` 全文**（见上方索引）
- ⚠️ **字体一致性**：图与 PPT 一律 **PingFang SC**（PPT 用 `_fix_ph_font(ph, name="PingFang SC")`）；别图用 Heiti SC、PPT 用 PingFang SC 造成跨页面字体跳变

## ★ 7 个致丑反模式（必须主动避开）

| # | 反模式 | 为什么丑 | 正确做法 |
|:-:|---|---|---|
| 1 | 顶部厚色带（≥0.5"）每页都重复 | 压死页面空间 + 视觉疲劳 | 6pt 极细线 + 右上 140pt 装饰大数字 |
| 2 | 每页同一 `header(title, page)` 通用模板 | 章节同质化、无层次感 | 章节扉页与内容页分两种 layout |
| 3 | 表格全网格（Excel 风）+ 默认 banding | 老土 + 信息密度低 | 表头深色 + 0 内边框 + 自定义斑马纹 |
| 4 | 一页 5+ 种饱和色（绿/蓝/红/橙/紫） | 眼花、权重失序 | 1 主色 + 1 强调色 + 灰阶 + 白 |
| 5 | 全屏文字墙（一页 >100 字）| 没人会读完 | 卡片化（每个信息单元独立矩形） |
| 6 | 标题用艺术字 / 阴影 / 3D / 渐变铺底 | 党政"信封风" | 简洁字体 + 1pt 横线分隔 |
| 7 | emoji 滥用（🚀 ✅ 🎉 等活泼感）| 制度文件不严肃 | 仅 ⚠ ⛔ 🔒 类警示性图标 |

## ★ 关键坑速记（完整代码与解法见 references，坑本身必须先记住）

| # | 坑 | 正解 |
|:-:|---|---|
| 1 | `font.name` 只写 `<a:latin>`，中文跨平台 fallback 丑字体 | `set_font` 用 lxml 显式写 `<a:ea>` + `<a:cs>`（技巧 #1）|
| 2 | `set_font(run)` 改不动 placeholder 中文字体（`<a:ea>` 继承自 master）| placeholder 一律 `_fix_ph_font(ph, ...)`，自加 textbox 才用 `set_font(run, ...)` |
| 3 | textbox 默认 margin 非 0 → 文字神秘偏右/偏下 | `margin_left/right/top/bottom = Emu(0)` |
| 4 | 大字号装饰数字被自动换行（"01" → 两行）| `word_wrap=False`；宽度 ≥ 字符数 × 0.6 × 字号pt / 72 |
| 5 | 表格默认 banding 出怪横纹 / 行高失控 | `tblPr` 关 `firstRow`/`bandRow` + 显式 `row.height`，斑马纹手动填色 |
| 6 | `shape.fill = None` 不是"无填充"，是"默认"（会有边）| `fill.background()` / `line.fill.background()` |
| 7 | 模板自带样例 slide 污染输出 | 加载后立即 `clear_template_slides(prs)`（template.py 提供）|
| 8 | LibreOffice 渲染页数 < `len(prs.slides)` 误判为代码 bug | 模板含"工具说明页"不被渲染，先看 `template-*-guide.md` |

## ★ 迭代验证流程（生死循环）

**最致命的错误**：只用 `python-pptx` 读回验证文件合法性，不看实际渲染。字符溢出 / 表格被截 / 文字遮挡 / 行高失控 / 中文字体 fallback——**只能靠 LibreOffice 渲染 PDF + 看 PNG 才能发现**。

```bash
python3 build-ppt.py                                        # 1. 生成
cd /tmp && rm -rf preview && mkdir preview && cd preview
soffice --headless --convert-to pdf /path/to/output.pptx    # 2. 转 PDF（实际渲染）
pdftocairo -png -r 100 output.pdf p                         # 3. 转 PNG（视觉）
# 4. 用 Read tool 看关键页（封面、表格页、嵌入图页、警示页）
# 5. 发现问题 → 改 build-ppt.py → 回到 1
```

**每页 3 步检查**：✓ 文字是否被截断 / 溢出框 / 遮挡？ ✓ 中文字体是否正确（不是 fallback 到丑字体）？ ✓ 表格 / 列宽是否合理，斑马纹是否生效？

## Checklist — 交付前自检

**通用（所有路径都查）**：
- [ ] 跨平台中文字体（用了 lxml 写 `<a:ea>` + `<a:cs>`）
- [ ] 没有文字被截断 / 溢出 / 遮挡（LibreOffice 实测）
- [ ] 没有 emoji 滥用（仅 ⚠ ⛔ 🔒 类警示性）
- [ ] 单一主色 + 1 强调色（不超过 7 个色变量，上限 12）
- [ ] 表格关了 `firstRow` / `bandRow`（防 banding）
- [ ] 大字号 textbox 设了 `word_wrap=False`
- [ ] 所有 textbox 设了 `margin_left/right = 0`
- [ ] `line_spacing` 显式设置（标题 1.0 / 正文 1.45）
- [ ] 每页有页脚 + 页码 `N / TOTAL`
- [ ] 章节扉页与内容页 layout 不同
- [ ] 图片用 `height=Inches(N)` 等比缩放（不变形）
- [ ] 不依赖 PrinceXML / 商业 PDF 引擎
- [ ] 可用 `python3 build-ppt.py` 一键重生成

**基于模板路径专项（增加 4 项）**：
- [ ] 加载模板后已用 `clear_template_slides(prs)` 清空所有样例 slide
- [ ] 所有 placeholder 都已用 `_fix_ph_font(ph, ...)` 修字体（不是 `set_font(run, ...)`）
- [ ] 已对照 LibreOffice 输出页数 vs `len(prs.slides)` —— 不一致时确认是"模板含工具说明页"而非代码 bug
- [ ] 已读过对应的 `template-*-guide.md`（如 `template-team-guide.md`），知道该模板的可用 layout / 配色 / 字体坑

## Anti-prompt — 让 Claude 不要做的事

把上文 Checklist 反过来念即是 anti-prompt（每条 `[ ]` → "不要 X"），不在此重列。Checklist 未覆盖的唯一一条额外禁令：

```
- 不要 commit 渲染产物（HTML / PDF / .pyc）— 在 .gitignore 里
```
