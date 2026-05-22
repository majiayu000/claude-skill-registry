---
name: ppt-deck
description: PPT 产出 playbook（目标/受众→故事线→版式设计→可访问性→交付），含 10/20/30 与 Microsoft Accessibility Checker 最佳实践。
---

# PPT 产出（从目标到可交付 Deck）

## When to use this skill
- 需要把一个主题变成可演示的 deck（汇报/方案/培训/融资/复盘）。
- 需要形成可复用的版式/模板（品牌规范、字体、配色、网格、图标风格）。
- 需要交付给更多受众时保证可访问性（标题、阅读顺序、对比度、alt text 等）。

## 必备输入
1) **受众与目标**：谁来听/读？希望他们会后做什么（决策/批准/理解/行动）？  
2) **场景与时长**：现场讲/线上讲/发文档自读？总时长与 Q&A 时间？  
3) **交付格式**：PPTX / PDF / Google Slides / Web（reveal.js）；是否需要讲稿/备注。  
4) **品牌规范**：字体、主/辅色、Logo 使用、图表/图标风格、封面样式。  
5) **内容资产**：已有数据、图表、截图、案例、引用来源（可追溯）。  
6) **强约束**（可选）：是否套用 10/20/30（<=10 张 / <=20 分钟 / 字号 >= 30pt）。

## 推荐故事线与页型
- 结构模板（任选其一）：`SCQA`、`金字塔`、`Before/After/Bridge`。  
- 常用页型（可直接列页）：封面 → TL;DR → 背景/现状 → 问题/机会 → 目标与原则 → 方案（可选项对比+推荐） → 实施计划（里程碑/资源/风险） → 指标与复盘 → 结尾 CTA → 附录。

## 工作流
1. **锁定目标与受众**：写出一句话目标+会后希望对方的行动。  
2. **选择故事线**：用上方模板列出章节，先写标题为“结论句”。  
3. **草拟大纲**：每页一句结论 + 3–5 个支持要点；将数据/图表占位。  
4. **版式与视觉**（可写入模板）：大字号（正文 ≥ 18pt）、高对比度、统一边距与对齐、图表减法（去 3D/装饰，突出关键数据）。  
5. **可访问性检查**：唯一标题、阅读顺序正确、所有视觉元素加 alt text、颜色不是唯一信息载体、足够对比度。  
6. **校对与打样**：在目标播放设备上试放；用 Accessibility Checker 过一遍。  
7. **交付打包**：生成源文件 + PDF 预览 + 讲稿 notes + SOURCES.md。

## 交付物清单
- `deck.pptx`（可编辑源文件）  
- `deck.pdf`（预览/分享）  
- `notes.md` 或 speaker notes 导出（讲稿/旁白）  
- `SOURCES.md`（数据/图片/引用来源，方便审计）

## 自动化提示
- **Web deck**：Markdown → reveal.js，适合版本管理与 CI 导出 PDF。  
- **离线 PPTX**：`python-pptx` 生成结构化页面+图表。  
- **纯图片→PPTX**：先用图像模型生成每页 16:9 图片，再用 `pptx_from_images` 拼成 `deck.pptx`。示例：
  ```json
  {"prompt":"封面：主题+副标题，极简风格，16:9，留白，深色背景，标题可读","size":"1600x900"}
  ```

## 参考资料
- Guy Kawasaki：10/20/30 规则：https://guykawasaki.com/the_102030_rule/  
- Microsoft：可访问性指南（alt text/阅读顺序/对比度/标题等）：https://support.microsoft.com/en-us/office/make-your-powerpoint-presentations-accessible-to-people-with-disabilities-6f7772b2-2f33-4bd2-8ca7-dae3b2b3ef25  
- Microsoft：Accessibility Checker 使用与修复流程：https://support.microsoft.com/en-us/office/improve-accessibility-with-the-accessibility-checker-a16f6de0-2f39-4a2b-8bd8-5ad801426c7f  
- Presentation Zen（演示设计与叙事）：http://www.presentationzen.com/
