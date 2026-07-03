---
name: agf-writing-docx-reports
description: 用 docx-js 写"阅读友好的中文 docx 报告"（决议书 / 评审报告 / 调研 / 分析 / 投标书等高密度报告型文档）。当用户要求把 markdown 内容转 docx 且抱怨"格式混乱 / 不专业 / 看不下去"时启用——pandoc 默认转换难以满足。提供：路径决策 / 设计 token / 可复用 helper 全套 / 11 个 pitfall / 生成-预览闭环。
---

# 写 docx 报告 — 高密度实战手册

> 重型参考材料（设计 token / spacing 数值 / 9 个 helper / 文档外壳 / 用法示例 / 装配顺序）在 `references/`，按下方索引**按需 Read 全文**，不要凭记忆手写。

## 何时用本 skill

| 信号 | 用本 skill |
|---|:--:|
| 用户要把 markdown 报告 → docx | ✅ |
| 报告是中文 / 含大量表格 / 需要视觉强调（决议 / 警示） | ✅ |
| 用户反馈"格式混乱 / 不专业 / 字段被分行 / 段前段后大 / 页边距宽" | ✅ |
| 报告需要封面页 / 自动目录 / 页眉页脚 / 警示框 | ✅ |
| 只是导出几页纯文本 / 没有表格 | ❌ 用 pandoc 默认即可 |
| 要做的是 PPT / Excel | ❌ 转 pptx / xlsx skill |

## 路径决策（3 选 1）

| 路径 | 何时选 | 代价 |
|---|---|---|
| **pandoc 默认** `pandoc x.md -o x.docx` | 内部草稿 / 纯文本为主 / 表格 ≤ 3 个 | 几秒；视觉无控制 |
| **pandoc + reference.docx** | 想统一字体 / 标题色但不要 callout | 中等；要先在 Word 里手工调样式做模板 |
| **docx-js 全定制**（本 skill 核心） | 正式对外报告 / 高密度表格 / 警示框 / 封面页 | 一次写 ~600 行 JS，复用率 90% |

判定经验：**用户说"格式混乱"基本就是要 docx-js**——根因是 pandoc 的列宽 auto + 无样式覆盖。

## References 索引（什么时候必读哪份）

| 场景 | 必读（Read 全文） |
|---|---|
| 动手写任何 docx-js 生成脚本前 | [`references/design-tokens-and-helpers.md`](./references/design-tokens-and-helpers.md)——设计 token / spacing 收紧数值 / 9 个可复用 helper + 用法示例 / 文档外壳模板 / 结构化数据→表格技巧 / 装配顺序，全套粘贴即用 |

## 配色铁律

- 标题用 `PRIMARY`（深蓝）不用默认黑——视觉层次靠颜色对比
- "强制不通过 / 警示 / 一票否决"用 `DANGER` + 浅红 BG callout
- "事实风险 / 即将逾期"用 `WARN` + 浅黄 BG callout
- 表头一律 `PRIMARY_LIGHT` 底，body 用 `ALT_ROW` 隔行底（zebra）
- 普通文本辅助信息（注释 / 路径）用 `MUTED` 灰

## spacing 要点（完整数值表见 references）

段前段后是 docx 最易膨胀的维度：default spacing（before 240+ / after 180+）= 19 页，收紧后 15 页（-21%）。收紧基准：H1=240/120、H2=160/80、H3=120/60、p=40/40、表格周边=30/30、bullet=30/30、cell margins=60/100。

## 11 个 pitfall（踩过的坑）

| # | 坑 | 解决 |
|:-:|---|---|
| 1 | 中文字体没指定 → LibreOffice 渲染丑 | 每个 TextRun 都带 `font: "PingFang SC"`（不能依赖 default styles） |
| 2 | 表格列宽 auto → 长字段强制换行 | 设计稿基准列宽 + `scaleWidths` 缩到 `CONTENT_WIDTH`；table.width + cell.width **两处都设** |
| 3 | `WidthType.PERCENTAGE` 在 Google Docs 渲染异常 | 全部用 `WidthType.DXA` |
| 4 | `ShadingType.SOLID` 让 cell 整块变黑 | 用 `ShadingType.CLEAR`（这是 docx 协议惯例反直觉的地方） |
| 5 | 段前段后 spacing 用默认 → 文档膨胀 30% | H1=240/120、H2=160/80、p=40/40、表格周边=30/30 |
| 6 | `PageBreak` 单独放 → 生成无效 XML | 必须在 Paragraph 里：`new Paragraph({ children: [new PageBreak()] })` 或 `pageBreakBefore: true` |
| 7 | bullet 用 `• Item` 字面字符 | 必须 `numbering.config` + `LevelFormat.BULLET` + Paragraph 的 `numbering: { reference: "bullets", level: 0 }` |
| 8 | docx-js 默认 A4，国内场景 OK；但海外项目要 Letter | A4: 11906×16838 / Letter: 12240×15840（都是 DXA） |
| 9 | cell margins **不计入** columnWidths → 实际可用窗口比想象小 | columnWidths 总和 == table.width；cell 内 padding 是 margins 单独算 |
| 10 | TOC 标题没出现 | Heading1/2/3 必须用确切 ID 覆盖样式 + `outlineLevel` 必填 |
| 11 | `validate.py` 依赖 defusedxml 可能没装 | 跳过 validate.py，用 `pandoc → plain` 反向读 + `unzip -l` 看结构替代 |

## 生成 → 预览 → 反馈闭环

```bash
# 1. 安装依赖
npm install -g docx

# 2. 写脚本到 /tmp/gen.js（不要写到项目目录，跑完即弃）

# 3. 跑生成
NODE_PATH=$(npm root -g) node /tmp/gen.js

# 4. 转 PDF 看效果（LibreOffice 会用 PingFang SC fallback）
python3 .claude/skills/docx/scripts/office/soffice.py --headless --convert-to pdf output.docx

# 5. 截图前 6 页
pdftoppm -jpeg -r 110 -f 1 -l 6 output.pdf /tmp/preview

# 6. Read JPG 验证视觉
#    （如有问题：改 token / 列宽 / spacing，回到 3）

# 7. 反向 pandoc 验证内容完整性
pandoc output.docx -t plain | head -60
```

**关键**：截图给用户看比 review JS 代码有效 10 倍。**像设计师一样反复看渲染图，别像程序员一样 review 代码**。

## 用户反馈映射（常见 → 调整）

| 用户反馈 | 你要调的 token |
|---|---|
| "页边距太宽" | `MARGIN` 左右 1440 → 720；重算 `CONTENT_WIDTH` |
| "表格分行" | 同上 + 重新分配 `widthsBefore`（让长字段列更宽） |
| "段前段后大" | H1 H2 H3 + p 的 spacing 全局缩 50% |
| "颜色太花" / "正式场合" | 砍掉 OK 绿 / WARN 黄，只保留 PRIMARY + DANGER + MUTED |
| "中文字体丑" | 检查每个 TextRun 是否带 `font: FONT`；考虑加 `Microsoft YaHei` 备选 |
| "想要封面页" | section 0 加居中大标题 + 元信息 + 红框 callout |
| "想要目录" | 加 `new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" })`；Word 打开后 F9 刷新 |
| "页码不对 / 没页眉" | section.headers/footers + `PageNumber.CURRENT` / `TOTAL_PAGES` |

## 决策矩阵 — 不需要 docx-js 的反例

| 场景 | 用什么 | 原因 |
|---|---|---|
| 1 页备忘录 | pandoc | 不值得写 600 行 JS |
| 内部 README | 留 markdown | 别强行 docx |
| 含复杂数学公式 | LaTeX → PDF | docx 公式渲染不稳 |
| 1000+ 行数据表 | xlsx skill | docx 表格大了渲染慢 |
| 简历 / 投递书 | Word 模板手填 | 别造轮子 |
| 含截图 / 图片 | docx-js + ImageRun（必须带 `type` 参数） | OK 但要算图片尺寸（EMU 单位，914400 = 1 inch） |

## 自检清单（交付前）

逐条 grep 验"11 个 pitfall"前三条（`font: FONT` 不漏 / 无 `PERCENTAGE` / 无 `SOLID`）+ 跑完整"生成 → 预览 → 反馈闭环"（soffice 转 PDF 截图自看 + 反向 `pandoc -t plain` 验内容没丢）。两节全过 = 可交付用户。
