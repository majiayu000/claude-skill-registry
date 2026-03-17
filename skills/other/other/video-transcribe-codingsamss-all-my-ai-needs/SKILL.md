---
name: video-transcribe
description: "Video/audio transcription, visual frame analysis and summary. Download video from any URL (Twitter, YouTube, Bilibili, etc.), transcribe speech to text, extract keyframes for visual analysis, and summarize content. Keywords: video, transcribe, 转录, 视频, 音频, audio, subtitle, 字幕, summary, 总结, 视频内容, 画面分析, 视觉分析, visual analysis, 视频画面, keyframe, whisper, groq, yt-dlp"
---

# Video Transcribe & Visual Analysis Skill

从任意视频/音频链接提取内容并分析。支持音频转录、视频画面分析、或两者综合。支持 Twitter/X、YouTube、Bilibili 等 1000+ 站点。

## 触发条件

当用户提到以下内容时触发：
- "这个视频说了什么"、"帮我看看这个视频"、"视频内容"、"转录"
- "transcribe this video"、"what does this video say"
- 分享了包含视频的链接并希望了解内容
- "总结这个视频"、"视频摘要"
- "提取字幕"、"语音转文字"
- "视频画面是什么"、"视频里展示了什么"、"分析视频画面"
- "analyze video visually"、"what's shown in this video"

## 模式判断

收到视频链接后，根据用户措辞判断分析模式。**按优先级从高到低匹配：**

### 1. 音频转录模式（audio）

用户**明确**要求处理语音/音频内容时使用。

- 命中关键词：转录、字幕、语音转文字、提取字幕、他说了什么话、transcribe、subtitle、speech-to-text
- 典型表达："帮我转录这个视频"、"提取字幕"、"视频里他说了什么话"
- 流程：仅提取音频 → Groq Whisper 转录 → 文本总结

### 2. 画面分析模式（visual）

用户**明确**要求分析视觉/画面内容时使用。

- 命中关键词：画面、视觉、展示了什么、出现了什么、看到了什么、视频截图、视频帧、visual、frame、what's shown
- 典型表达："视频画面是什么"、"视频里展示了什么"、"分析一下视频画面"
- 流程：下载视频 → 提取关键帧 → Claude 视觉分析 → 画面描述

### 3. 综合分析模式（full）— 默认

用户笼统地想了解视频内容，或意图不明确时使用。

- 命中关键词：分析、内容、说了什么、总结、帮我看看、什么内容、analyze、summary
- 典型表达："这个视频说了什么"、"帮我看看这个视频"、"分析一下这个视频"
- 流程：下载视频 → 提取关键帧分析画面 → 提取音频转录 → 综合总结
- **如果音频转录结果为空或无意义（纯音乐/无语音），自动退化为纯画面分析**
- **如果关键帧提取失败（纯音频文件），自动退化为纯音频转录**

## 前置条件

1. **yt-dlp** 已安装: `brew install yt-dlp`
2. **ffmpeg** 已安装: `brew install ffmpeg`
3. **GROQ_API_KEY** 环境变量已设置（音频转录需要）
   - 申请地址: https://console.groq.com
   - 纯画面分析模式不需要 Groq API

## 工作目录

所有临时文件保存到: `/tmp/video-transcribe/`

处理完成后自动清理中间文件，仅保留最终文本输出。

## 执行流程

收到视频链接后，先完成模式判断，再按以下步骤执行：

### Step 0: 清理工作目录

每次执行前，清理旧文件：

```bash
if [ -d /tmp/video-transcribe ]; then
  # 删除超过 1 天的文件
  find /tmp/video-transcribe -type f -mtime +1 -delete 2>/dev/null
  # 删除上次残留的所有中间文件（用 find 避免特殊字符文件名 glob 失败）
  find /tmp/video-transcribe -type f \( -name '*.mp3' -o -name '*.wav' -o -name '*.mp4' -o -name '*.webm' -o -name '*.jpg' \) -delete 2>/dev/null
fi
mkdir -p /tmp/video-transcribe
```

### Step 1: 下载

根据模式选择下载方式：

#### 音频模式：仅下载音频轨

```bash
yt-dlp --cookies-from-browser chrome \
  -x --audio-format mp3 --audio-quality 5 \
  -o '/tmp/video-transcribe/%(title)s.%(ext)s' \
  '$URL'
```

- `-x --audio-format mp3` - 只提取音频转 MP3
- `--audio-quality 5` - 中等质量（语音转录足够，减小体积）

#### 画面分析模式 / 综合模式：下载完整视频

```bash
yt-dlp --cookies-from-browser chrome \
  -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
  --merge-output-format mp4 \
  -o '/tmp/video-transcribe/%(title)s.%(ext)s' \
  '$URL'
```

- 限制 720p 分辨率，画面分析足够清晰且节省空间
- `--merge-output-format mp4` 确保输出为 mp4 便于后续 ffmpeg 处理

**错误处理（通用）：**
- cookies 失败 → 去掉 `--cookies-from-browser chrome` 重试
- 站点不支持 → 告知用户 yt-dlp 不支持该站点
- YouTube 报 `No video formats found` / `SABR` 错误 → 提示 `brew upgrade yt-dlp`
- 下载超时或文件过大 → 可加 `--max-filesize 500M` 限制

### Step 2: 处理

根据模式执行对应的处理流程。综合模式下 2A 和 2B 都要执行。

#### 2A: 音频转录（音频模式 / 综合模式）

**综合模式下，先从视频文件提取音频：**

```bash
ffmpeg -i '/tmp/video-transcribe/INPUT.mp4' \
  -vn -acodec libmp3lame -q:a 5 \
  '/tmp/video-transcribe/audio.mp3' -y
```

后续用 `audio.mp3` 替代 `INPUT.mp3`。

**检查文件大小：**

```bash
FILE_SIZE=$(stat -f%z '/tmp/video-transcribe/INPUT.mp3')
```

若文件 <= 24MB，直接转录。若 > 24MB，切分：

```bash
ffmpeg -i '/tmp/video-transcribe/INPUT.mp3' \
  -f segment -segment_time 1200 -c copy \
  '/tmp/video-transcribe/segment_%03d.mp3' -y
```

**调用 Groq Whisper API 转录：**

若直连 Groq 返回 `403 Forbidden`，为转录命令临时加代理环境变量后重试：

```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 <转录命令>
```

单文件：

```bash
curl -s -X POST \
  https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@/tmp/video-transcribe/INPUT.mp3" \
  -F "model=whisper-large-v3" \
  -F "response_format=text" \
  -F "language=zh" \
  -o '/tmp/video-transcribe/transcript.txt'
```

多段（切分后）：

```bash
> /tmp/video-transcribe/transcript.txt
for f in /tmp/video-transcribe/segment_*.mp3; do
  curl -s -X POST \
    https://api.groq.com/openai/v1/audio/transcriptions \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -F "file=@$f" \
    -F "model=whisper-large-v3" \
    -F "response_format=text" \
    >> '/tmp/video-transcribe/transcript.txt'
  echo "" >> '/tmp/video-transcribe/transcript.txt'
done
```

**参数说明：**
- `model=whisper-large-v3` - 最高精度模型
- `response_format=text` - 返回纯文本
- `language=zh` - 指定中文。英文用 `en`，不确定语言时省略此参数让模型自动检测

**错误处理：**
- 401：GROQ_API_KEY 无效或过期
- 403：网络受限，尝试加 `HTTP_PROXY` 与 `HTTPS_PROXY`
- 413：文件过大，需切分
- 429：速率限制，等待几秒后重试

**综合模式下判断转录结果：**
- 转录文本为空、极短（< 10 字符）、或内容无意义 → 判定为无有效语音，跳过音频部分，仅使用画面分析结果

#### 2B: 画面分析（画面模式 / 综合模式）

**提取关键帧：**

```bash
# 获取视频时长（秒）
DURATION=$(ffprobe -v error -show_entries format=duration \
  -of csv=p=0 '/tmp/video-transcribe/INPUT.mp4' | cut -d. -f1)

# 计算采样间隔（目标 8 帧，均匀分布）
INTERVAL=$((DURATION / 8))
[ "$INTERVAL" -lt 2 ] && INTERVAL=2

# 提取关键帧
ffmpeg -i '/tmp/video-transcribe/INPUT.mp4' \
  -vf "fps=1/$INTERVAL,scale=1280:-2" \
  -frames:v 8 \
  -q:v 2 \
  '/tmp/video-transcribe/frame_%03d.jpg' -y
```

**参数说明：**
- `fps=1/$INTERVAL` - 根据视频时长动态调整采样率，确保帧均匀覆盖全片
- `scale=1280:-2` - 宽度缩放到 1280px，高度自适应保持比例
- `-frames:v 8` - 最多提取 8 帧
- `-q:v 2` - JPEG 高质量（2），清晰度与文件大小平衡

**如果提取帧数不足 3 张（视频过短），降低间隔重试：**

```bash
ffmpeg -i '/tmp/video-transcribe/INPUT.mp4' \
  -vf "fps=2,scale=1280:-2" \
  -frames:v 8 \
  -q:v 2 \
  '/tmp/video-transcribe/frame_%03d.jpg' -y
```

**视觉分析：**

使用 Claude 自身的多模态视觉能力，用 Read 工具依次读取提取的帧图片（`/tmp/video-transcribe/frame_001.jpg` ~ `frame_008.jpg`），综合所有帧分析视频画面内容。

分析时重点关注：
- **场景变化** - 画面之间的转场和时间线推进
- **人物与物体** - 出现的人、动物、机器、物品等
- **文字与字幕** - 画面上叠加的文字、标题、水印
- **动作与事件** - 正在发生什么
- **画面风格** - 实拍/动画/对比/演示等

### Step 3: 输出总结

根据模式提供对应格式的总结：

#### 音频模式输出

1. 展示视频基本信息（标题、时长、语言）
2. 结构化总结：
   - **核心主题** - 一句话概括
   - **关键要点** - 3-5 个要点
   - **详细内容** - 按话题/章节组织的详细摘要
   - **值得关注** - 有价值的观点、数据、资源链接等

#### 画面分析模式输出

1. 展示视频基本信息（标题、时长、提取帧数）
2. 结构化总结：
   - **画面概述** - 视频整体展示了什么
   - **关键场景** - 按时间顺序描述主要画面变化
   - **视觉要素** - 出现的人物、物体、文字、图表等
   - **画面结论** - 从视觉内容推断视频主旨

#### 综合模式输出

1. 展示视频基本信息（标题、时长）
2. 综合总结：
   - **核心主题** - 结合画面和语音的一句话概括
   - **画面内容** - 视频展示了什么
   - **语音内容** - 说了什么（若有有效语音）
   - **关键要点** - 3-5 个要点
   - **综合分析** - 画面与语音结合的完整理解

### Step 4: 清理临时文件

处理完成后，清理所有中间文件：

```bash
# 删除视频、音频、帧图片等中间文件（用 find 避免特殊字符文件名 glob 失败）
find /tmp/video-transcribe -type f \( -name '*.mp4' -o -name '*.webm' -o -name '*.mp3' -o -name '*.wav' -o -name '*.jpg' \) -delete 2>/dev/null
```

保留 `transcript.txt` 供用户后续查阅。用户不再需要时：

```bash
rm -rf /tmp/video-transcribe/
```

## 支持的站点（部分）

yt-dlp 支持 1000+ 站点，常用的包括：
- Twitter/X
- YouTube
- Bilibili（哔哩哔哩）
- Vimeo
- TikTok / 抖音
- 微博视频
- 播客平台（Apple Podcasts、Spotify 等）

完整列表: `yt-dlp --list-extractors`

## 本地模式（备选）

如果无网络或不想使用在线 API，可以使用本地 whisper-cpp 转录：

1. 安装: `brew install whisper-cpp`
2. 下载模型: `curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin -o ~/.cache/whisper-cpp/ggml-small.bin`
3. 转码为 WAV: `ffmpeg -i INPUT.mp3 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y`
4. 转录: `whisper-cli -m ~/.cache/whisper-cpp/ggml-small.bin -f audio.wav -l auto --no-timestamps -otxt -of transcript`

本地模型精度低于 Groq whisper-large-v3，适合离线或隐私敏感场景。

## 注意事项

- 音频转录通过 Groq API 处理，音频会上传到 Groq 服务器
- 画面分析使用 Claude 自身视觉能力，帧图片不上传第三方服务
- 音频质量直接影响转录精度，背景噪音较大时精度会下降
- 非语音内容（纯音乐、音效）无法转录，综合模式会自动退化为画面分析
- 多语言混合内容可能需要指定主要语言（`language=zh` 或 `language=en`）
- Groq 免费额度充足，日常使用无需担心费用
- 视频下载限制 720p，画面分析足够清晰且节省带宽
- 关键帧最多 8 张，均匀覆盖视频主要内容