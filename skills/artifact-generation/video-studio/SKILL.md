---
name: "video-studio"
description: "Use when the user asks to create or edit videos end-to-end (script→video, auto-cut/jumpcut, captions/subtitles, polishing for Shorts/Reels/TikTok). Current implemented backend: local FFmpeg (probe/render/jumpcut/burn-subtitles/polish). Planned/optional backends: Remotion (motion graphics templates), VectCutAPI (CapCut/剪映 timeline editing), and video-audio-mcp (MCP tool wrapper) when available. Produces a finished video artifact (MP4 by default) from assets + copy + a design/storyboard plan."
---

# Video Studio (自动视频制作 / 剪辑 / 打磨)

目标：把「素材（视频/音频/图片）+ 文案 + 编排/设计方案」自动变成可发布的成片，并在最后做一轮“打磨”（节奏、转场、字幕、音量、编码）。

## 何时使用
- 你要“从 0 生成一个视频”（口播/科普/产品介绍/短视频）
- 你要“自动剪辑已有视频/音频”（去静音、裁切、拼接、转场、加字幕、加 Logo/BGM）
- 你要“适配平台规格”（9:16 / 1:1 / 16:9、码率、分辨率、时长上限）
- 你要“自动抛光”（音量标准化、fade in/out、H.264/yuv420p、帧率、字幕烧录）

## 背后能力（融合方案）
本 skill 不绑定单一引擎，而是按可用性选择 backend：

1. **FFmpeg（基线后端，必备）**
   - 本地快速剪辑、拼接、字幕烧录、音频混音、编码打磨
2. **Remotion（可选，做“像设计稿一样”的动效视频）**
   - 程序化动效、模板化片头片尾、动态字幕/图表
3. **VectCutAPI（可选，高阶时间线后端）**
   - 如果你有剪映/CapCut + VectCutAPI 服务，可用 API/MCP 进行更复杂的轨道/特效/关键帧
4. **video-audio-mcp（可选，MCP 封装的 FFmpeg 工具箱）**
   - 如果已配置该 MCP server，可把常用 FFmpeg 操作当成工具调用（trim/concat/subtitles/overlays/remove_silence）

## 先跑一次环境探测（强烈推荐）
在当前项目目录里执行：

```powershell
python C:\Users\羽裳\.codex\skills\video-studio\scripts\video_studio.py probe
```

它会输出 JSON，说明：
- `ffmpeg/ffprobe` 是否可用（没有则给出安装建议）
- `node/npm/npx` 是否可用（Remotion 需要）
- `vectcut_base_url` 是否可连（可选）

## 产物约定（建议）
- 中间文件：`outputs/video-studio/tmp/`
- 最终成片：`outputs/video-studio/final/`

你可以把素材放在：
- `assets/video/` `assets/audio/` `assets/images/` `assets/fonts/`

## 最小闭环：用 spec 直接生成视频（FFmpeg backend）
1) 写一个 spec（可参考本 skill 的 `references/sample_spec.json`）

2) 运行：

```powershell
python C:\Users\羽裳\.codex\skills\video-studio\scripts\video_studio.py render --spec C:\path\to\spec.json
```

## “打磨”步骤（推荐作为最后一步）
```powershell
python C:\Users\羽裳\.codex\skills\video-studio\scripts\video_studio.py polish --in .\outputs\video-studio\final\video.mp4 --out .\outputs\video-studio\final\video.polished.mp4
```

打磨会尽量做到：
- H.264 + yuv420p（平台兼容）
- 统一帧率/分辨率
- 音量标准化（EBU R128 loudnorm）
- 可选 fade in/out

## 自动剪辑：JumpCut（去静音/去停顿）
适合“口播/访谈/课程录屏”这类有明显停顿的视频：自动检测静音区间并拼接，提高节奏流畅度。

```powershell
python C:\Users\羽裳\.codex\skills\video-studio\scripts\video_studio.py jumpcut --in .\assets\video\talking.mp4 --out .\outputs\video-studio\final\talking.jumpcut.mp4
```

常用参数：
- `--silence-threshold-db`：静音阈值（例如 `-35`）
- `--min-silence`：最短静音时长（例如 `0.4`）
- `--pad`：保留在静音边界的 padding（避免“咬字被切掉”）

## 字幕烧录（SRT → MP4）
如果你已经有 `captions.srt`（来自转录或人工），可直接烧录：

```powershell
python C:\Users\羽裳\.codex\skills\video-studio\scripts\video_studio.py burn-subtitles --in .\outputs\video-studio\final\video.mp4 --srt .\assets\captions.srt --out .\outputs\video-studio\final\video.subbed.mp4
```

## 需要 AI 生成素材时（可选）
这个 skill **优先复用既有 skill**，避免重复造轮子：
- 图片/背景：`$imagegen`（需要 `OPENAI_API_KEY`）
- 配音：`$speech`（需要 `OPENAI_API_KEY`）
- 转录：`$transcribe`（需要 `OPENAI_API_KEY`）

典型全自动流程：
1) 文案 → 生成配音（speech）
2) 配音 → 生成字幕（transcribe 或手工脚本）
3) 文案/分镜 → 生成背景图（imagegen）
4) 用本 skill 的 `render/polish` 合成出片

## 质量门禁（交付前自检）
- 成片可播放（本地播放器 + 秒开）
- 分辨率/帧率符合平台（例如 1080x1920@30fps）
- 音量不过爆、不太小（主讲语音清晰，BGM 不盖人声）
- 字幕不超出安全区（手机端不被 UI 遮挡）

## 边界
- 本 skill 会生成/编辑视频文件，但不会替你发布到平台。
- 高级“像剪映一样”的轨道编辑：优先走 VectCutAPI（如果你有服务），否则用 FFmpeg 的能力做到“够用的自动剪辑”。
