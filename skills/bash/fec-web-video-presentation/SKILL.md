---
name: fec-web-video-presentation
description: Use when turning an article, talk script, lesson, product demo, or narrated explanation into a recordable 16:9 web presentation with step-driven scenes, optional narration alignment, theme tokens, and screen-recording guidance; Chinese triggers include 网页视频, 动态演示, 口播稿转视频, 可录屏演示, 16:9 演示.
---

# 网页视频演示

## Purpose

把文章、口播稿、课程、产品讲解或技术分享转成可录屏的 16:9 网页演示。产物应像一个可点击推进的视频舞台：每一步承载一个口播节拍，视觉设计服务内容节奏，并能用浏览器稳定录制。

## Procedure

1. 判断输入形态
   - 用户给文章或长文时，先拆成口播稿和 outline。
   - 用户给现成口播稿时，保留原顺序，只补 outline、章节和 step。
   - 用户只给主题但没有内容时，先要求素材、大纲或目标要点；不要替用户虚构整篇内容。

2. 生成内容计划
   - 按 [content-plan.md](references/content-plan.md) 输出 script 与 outline。
   - script 决定讲述顺序和每个节拍；outline 决定章节、step、估时、屏幕信息和素材清单。
   - outline 只描述内容密度和画面任务，不提前写死具体动画实现。

3. 对齐演示系统
   - 从 [theme-system.md](references/theme-system.md) 或 [starter-themes.json](data/starter-themes.json) 选择一个 starter theme，也可以按项目品牌重新定义 token。
   - 使用 [create-video-presentation.mjs](scripts/create-video-presentation.mjs) 创建最小 Vite + React + TypeScript 演示骨架：
     ```bash
     node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs ./presentation --theme editorial-slate
     ```
   - 如只想预览可选主题或计划写入内容：
     ```bash
     node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs --list-themes
     node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs --dry-run ./presentation --theme editorial-slate
     ```

4. 实现章节
   - 每章按 [chapter-craft.md](references/chapter-craft.md) 实现。
   - 每个 step 独占舞台，屏幕只承载当前口播节拍需要用户理解的核心内容。
   - 章节必须有可见的视觉演示、图形、布局变化、状态推进或数据/媒体呈现；不要交付纯文本幻灯片。
   - 第一章应作为风格锚点优先完成并验收，再继续其它章节。

5. 录屏和音频
   - 使用 [recording-and-audio.md](references/recording-and-audio.md) 检查舞台比例、导航、录制模式和可选音频同步。
   - 音频可以来自用户已有文件、宿主工具或项目自己的 TTS 流程；本技能不绑定特定 TTS 供应商。

6. 交付前验证
   - 浏览器打开演示，检查 16:9 缩放、键盘/点击推进、step 数、文本溢出、隐藏控件、控制台错误和录屏路径。
   - 若章节数量、顺序或 step 数变化，重置本地持久化 key 或清理旧进度，避免恢复到不存在的 step。

## Constraints

- 不把网页视频做成普通营销落地页、静态 PPT 或长滚动文章。
- 不复制参考项目的主题、模板章节、长提示词或脚手架实现；按当前项目生成原创骨架。
- 不在 outline 阶段锁死每个动画名称；动画应由章节内容关系驱动。
- 不使用假数据、假引用、假产品截图或不可检查媒体填充画面。
- 不让控件、页码、说明文字或调试面板污染录屏画面；必要控件默认隐藏或弱化。
- 不为音频合成引入项目外供应商约定；TTS 属于可选适配层。

## Expected Output

输出 script、outline、可运行的 16:9 网页演示骨架或章节实现，并说明主题、章节/step 数、录屏方式、可选音频路径和验证结果。最终演示应可通过点击或键盘稳定推进，视觉节奏贴合口播内容，且适合浏览器录屏。
