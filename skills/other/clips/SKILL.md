---
name: clips
description: 视频剪辑全链(download → transcribe → plan → cut → translate → karaoke)
expected_outputs:
  - "**/clips/index.html"
  - "**/clips/clip_*.mp4"
  - "**/clips/cut_report.json"
  - "**/clips/*.translations.*.json"
---

# clips · 视频剪辑(**必跑完 6 步 · 不允许中途 stop**)

NextFrame 完整 clips pipeline。**6 步全跑 · 每步 Bash 一次 tool · 一直走到 karaoke HTML**。

## 🔴 硬约束(违反 = 任务失败)

- ❌ **不允许中途 FINAL 停** · translate 和 karaoke 必须跑完
- ❌ **不允许在 plan 步输出完 plan.json 就停**
- ❌ **不允许说"现在我需要翻译..." 然后不调 tool**
- ✅ 每步调完 tool 立刻下一步
- ✅ 只有 karaoke 产出 index.html 后才能 FINAL

## 推进状态机(6 步 · 严格顺序)

1. `Bash("nf-guide clips download")` → 调 `nf-source download` · 产 source.mp4
2. `Bash("nf-guide clips transcribe")` → 调 `whisperx --model base.en`(小模型 · 避免 1GB 下载)· 产 sentences.json + words.json
3. `Bash("nf-guide clips plan")` → 你挑 1 个亮点写 plan.json(**只挑 1 个 · 省 translate 工作量**)
4. `Bash("nf-guide clips cut")` → ffmpeg 切 · 产 clip_01.mp4 + cut_report.json
5. `Bash("nf-guide clips translate")` → 翻译(**一次 Bash heredoc 写完整个 translations.zh.json · 不要逐句译**)· 产 clip_01.translations.zh.json
6. `Bash("nf-guide clips karaoke")` → 产 index.html(终点)

## 终点验收

`ls <episode>/clips/` 必须有:
- clip_01.mp4
- cut_report.json
- clip_01.translations.zh.json
- index.html(karaoke · 字级同步)

## 反例(上次 agent 踩的坑)

❌ 错:"现在我需要翻译这 4 个英文句子..."(输出纯文本后停)
✅ 对:直接 `Bash("cat > <path>/clip_01.translations.zh.json <<EOF ... EOF")` 一次写完

## 视频选择(agent 自主)

用户让你**自主选**一个短视频(< 60s · 新鲜 · 不要 me-at-the-zoo)· 用 yt-dlp 下。建议挑:TED 短演讲 / 新闻片段 / 搞笑短剧 / 科技演示。
