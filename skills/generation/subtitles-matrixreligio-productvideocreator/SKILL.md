---
name: subtitles
description: 自动生成视频字幕。解析配音文案，生成同步字幕，使用 Remotion 组件渲染。支持中英文双语字幕。
argument-hint: [配音元数据文件路径]
---

# 字幕自动生成技能

## 快速开始：使用模板

项目提供了可复用的字幕组件模板：

```tsx
// 从模板导入
import { SubtitleDisplay, createSubtitlesFromMetadata } from "./components/SubtitleDisplay";
import type { Subtitle } from "./config/types";
```

模板位置：`templates/components/SubtitleDisplay.tsx`

---

## 重要：字幕时间同步

**字幕时间必须基于 voiceover_metadata.json 的 `actual_duration`（实际时长），而非 `target_duration`（目标时长）。**

```tsx
// ✅ 正确：使用 actual_duration 计算 end 时间
const SUBTITLES: Subtitle[] = [
  {
    start: segment.start_time,
    end: segment.start_time + segment.actual_duration,  // 使用实际时长
    text: segment.text
  },
];

// ❌ 错误：使用 target_duration（可能导致字幕与音频不同步）
const SUBTITLES: Subtitle[] = [
  {
    start: segment.start_time,
    end: segment.start_time + segment.target_duration,  // 不要这样做
    text: segment.text
  },
];
```

### 验证字幕时间

```tsx
import { validateSubtitleTiming } from "./components/SubtitleDisplay";

const { valid, warnings } = validateSubtitleTiming(SUBTITLES, VIDEO_DURATION);
if (!valid) {
  console.warn("字幕时间警告:", warnings);
}
```

---

## 工作流程

```
配音元数据 (voiceover_metadata.json)
        ↓
   解析文案和时间线
        ↓
   生成字幕数据 (subtitles.json)
        ↓
   Remotion 字幕组件渲染
```

## 字幕数据格式

### 输入：配音元数据

```json
{
  "voice": "zh-CN-YunjianNeural",
  "total_duration": 85,
  "segments": [
    {
      "index": 0,
      "start_time": 0.5,
      "target_duration": 7.0,
      "actual_duration": 6.3,
      "text": "1993年，黄仁勋创立NVIDIA...",
      "language": "zh"
    }
  ]
}
```

### 输出：字幕数据

```json
{
  "subtitles": [
    {
      "id": 0,
      "startFrame": 15,
      "endFrame": 204,
      "text": "1993年，黄仁勋创立NVIDIA",
      "language": "zh"
    }
  ],
  "fps": 30,
  "style": {
    "fontSize": 48,
    "fontFamily": "Noto Sans SC",
    "color": "#FFFFFF",
    "backgroundColor": "rgba(0, 0, 0, 0.7)",
    "position": "bottom"
  }
}
```

## 字幕生成脚本

```python
#!/usr/bin/env python3
"""
字幕生成脚本 - 从配音元数据生成字幕
"""

import json
from pathlib import Path

FPS = 30
MAX_CHARS_PER_LINE = 20  # 中文每行最大字符数
MAX_WORDS_PER_LINE = 8   # 英文每行最大单词数

def split_text(text: str, language: str = "zh") -> list:
    """
    将长文本拆分成多行
    """
    if language == "zh":
        # 中文按字符拆分
        lines = []
        current_line = ""
        for char in text:
            if len(current_line) >= MAX_CHARS_PER_LINE:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        if current_line:
            lines.append(current_line)
        return lines
    else:
        # 英文按单词拆分
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            if len(current_line) >= MAX_WORDS_PER_LINE:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(" ".join(current_line))
        return lines

def generate_subtitles(metadata_path: str, output_path: str):
    """
    从配音元数据生成字幕文件
    """
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    subtitles = []
    subtitle_id = 0

    for segment in metadata["segments"]:
        text = segment.get("full_text", segment.get("text", ""))
        language = segment.get("language", "zh")
        start_time = segment["start_time"]
        duration = segment["actual_duration"]

        # 拆分长文本
        lines = split_text(text, language)

        # 计算每行显示时长
        line_duration = duration / len(lines) if lines else duration

        for i, line in enumerate(lines):
            line_start = start_time + i * line_duration
            line_end = line_start + line_duration

            subtitles.append({
                "id": subtitle_id,
                "startFrame": int(line_start * FPS),
                "endFrame": int(line_end * FPS),
                "text": line.strip(),
                "language": language
            })
            subtitle_id += 1

    output_data = {
        "subtitles": subtitles,
        "fps": FPS,
        "style": {
            "fontSize": 48,
            "fontFamily": "Noto Sans SC" if metadata["segments"][0].get("language") == "zh" else "Inter",
            "color": "#FFFFFF",
            "backgroundColor": "rgba(0, 0, 0, 0.7)",
            "position": "bottom",
            "padding": "12px 24px",
            "borderRadius": "8px"
        }
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✓ 生成 {len(subtitles)} 条字幕")
    print(f"✓ 输出: {output_path}")

if __name__ == "__main__":
    generate_subtitles(
        metadata_path="public/audio/voiceover_metadata.json",
        output_path="public/subtitles.json"
    )
```

## Remotion 字幕组件

### SubtitleDisplay.tsx

```tsx
import React from "react";
import { useCurrentFrame, interpolate, Easing } from "remotion";

interface Subtitle {
  id: number;
  startFrame: number;
  endFrame: number;
  text: string;
  language: string;
}

interface SubtitleStyle {
  fontSize: number;
  fontFamily: string;
  color: string;
  backgroundColor: string;
  position: "top" | "bottom" | "center";
  padding: string;
  borderRadius: string;
}

interface SubtitleDisplayProps {
  subtitles: Subtitle[];
  style: SubtitleStyle;
}

export const SubtitleDisplay: React.FC<SubtitleDisplayProps> = ({
  subtitles,
  style,
}) => {
  const frame = useCurrentFrame();

  // 找到当前帧应显示的字幕
  const currentSubtitle = subtitles.find(
    (sub) => frame >= sub.startFrame && frame < sub.endFrame
  );

  if (!currentSubtitle) return null;

  // 淡入淡出动画
  const fadeInDuration = 6; // 0.2秒
  const fadeOutDuration = 6;

  const opacity = interpolate(
    frame,
    [
      currentSubtitle.startFrame,
      currentSubtitle.startFrame + fadeInDuration,
      currentSubtitle.endFrame - fadeOutDuration,
      currentSubtitle.endFrame,
    ],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.ease,
    }
  );

  // 位置样式
  const positionStyle: React.CSSProperties =
    style.position === "top"
      ? { top: 60 }
      : style.position === "center"
      ? { top: "50%", transform: "translateY(-50%)" }
      : { bottom: 80 };

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        ...positionStyle,
      }}
    >
      <div
        style={{
          opacity,
          fontSize: style.fontSize,
          fontFamily: style.fontFamily,
          color: style.color,
          backgroundColor: style.backgroundColor,
          padding: style.padding,
          borderRadius: style.borderRadius,
          textAlign: "center",
          maxWidth: "80%",
          lineHeight: 1.4,
          textShadow: "2px 2px 4px rgba(0,0,0,0.8)",
        }}
      >
        {currentSubtitle.text}
      </div>
    </div>
  );
};
```

### 集成到主视频

```tsx
import React from "react";
import { Composition, staticFile } from "remotion";
import { SubtitleDisplay } from "./components/SubtitleDisplay";
import subtitleData from "../public/subtitles.json";

export const FinalVideo: React.FC = () => {
  return (
    <>
      {/* 其他视频内容 */}

      {/* 字幕层（最上层） */}
      <SubtitleDisplay
        subtitles={subtitleData.subtitles}
        style={subtitleData.style}
      />
    </>
  );
};
```

## 字幕样式配置

### 预设样式

| 风格 | fontSize | fontFamily | 背景 | 适用场景 |
|------|----------|------------|------|----------|
| 默认 | 48 | Noto Sans SC | rgba(0,0,0,0.7) | 通用 |
| 科技 | 42 | Inter | rgba(0,10,30,0.8) | 科技视频 |
| 简约 | 44 | sans-serif | transparent | 简洁风格 |
| 强调 | 56 | Noto Sans SC | #76B900 | 重点内容 |

### 双语字幕

```tsx
// 双语字幕显示
interface BilingualSubtitle {
  primary: string;    // 主语言
  secondary: string;  // 次语言
}

export const BilingualSubtitleDisplay: React.FC<{
  subtitles: BilingualSubtitle[];
}> = ({ subtitles }) => {
  // ...
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ fontSize: 48, marginBottom: 8 }}>
        {currentSubtitle.primary}
      </div>
      <div style={{ fontSize: 32, opacity: 0.8 }}>
        {currentSubtitle.secondary}
      </div>
    </div>
  );
};
```

## 字幕位置调整

```tsx
// 避免字幕遮挡重要内容
const getSubtitlePosition = (
  frame: number,
  scenes: Scene[]
): "top" | "bottom" => {
  const currentScene = scenes.find(
    (s) => frame >= s.startFrame && frame < s.endFrame
  );

  // 如果当前场景底部有重要内容，字幕显示在顶部
  if (currentScene?.hasBottomContent) {
    return "top";
  }
  return "bottom";
};
```

## SRT 格式导出（可选）

```python
def export_srt(subtitles: list, output_path: str, fps: int = 30):
    """导出 SRT 格式字幕文件"""
    def frame_to_timecode(frame: int) -> str:
        total_seconds = frame / fps
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    with open(output_path, "w", encoding="utf-8") as f:
        for i, sub in enumerate(subtitles, 1):
            f.write(f"{i}\n")
            f.write(f"{frame_to_timecode(sub['startFrame'])} --> {frame_to_timecode(sub['endFrame'])}\n")
            f.write(f"{sub['text']}\n\n")

    print(f"✓ SRT 导出: {output_path}")
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 字幕闪烁 | 增加 fadeInDuration/fadeOutDuration |
| 字幕太长 | 调整 MAX_CHARS_PER_LINE |
| 字体不显示 | 确保使用 @remotion/google-fonts 加载字体 |
| 字幕位置不对 | 调整 position 和 bottom/top 值 |
| 字幕遮挡内容 | 使用动态位置调整 |
