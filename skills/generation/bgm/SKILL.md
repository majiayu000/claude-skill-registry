---
name: bgm
description: 为视频添加背景音乐。支持免版权音乐来源、音量混合、淡入淡出效果。当需要为视频添加背景音乐、调整音乐与配音音量平衡时使用。
argument-hint: [视频类型: epic/corporate/upbeat/ambient]
---

# 背景音乐技能

## 免版权音乐来源

| 来源 | 网址 | 特点 |
|------|------|------|
| Pixabay Music | https://pixabay.com/music/ | 完全免费，无需署名 |
| Free Music Archive | https://freemusicarchive.org/ | CC 授权，部分需署名 |
| Uppbeat | https://uppbeat.io/ | 免费版每月限量 |
| Mixkit | https://mixkit.co/free-stock-music/ | 完全免费 |

**推荐**: Pixabay Music (无需署名，商用免费)

## 音乐风格选择

| 视频类型 | 推荐风格 | 关键词搜索 |
|----------|----------|------------|
| 科技历程 | Epic, Cinematic | "epic cinematic", "technology" |
| 产品介绍 | Corporate, Upbeat | "corporate", "business" |
| 教程视频 | Ambient, Soft | "ambient", "background" |
| 发布会 | Inspiring, Motivational | "inspiring", "motivational" |
| 创意内容 | Modern, Electronic | "modern", "electronic" |

## FFmpeg 音频混合

### 基础混合（配音优先）

```bash
# 将 BGM 与配音混合，BGM 音量降低
# 配音密集时推荐 volume=0.05，配音稀疏时可用 0.08-0.10
ffmpeg -i voiceover.mp3 -i bgm.mp3 \
  -filter_complex "[1:a]volume=0.05[bgm];[0:a][bgm]amix=inputs=2:duration=first[out]" \
  -map "[out]" mixed_audio.mp3
```

### 带淡入淡出效果

```bash
# BGM 淡入3秒，淡出3秒
ffmpeg -i voiceover.mp3 -i bgm.mp3 \
  -filter_complex "
    [1:a]volume=0.05,afade=t=in:st=0:d=3,afade=t=out:st=82:d=3[bgm];
    [0:a][bgm]amix=inputs=2:duration=first[out]
  " \
  -map "[out]" mixed_audio.mp3
```

### 完整音频处理流程

```bash
# 1. 处理 BGM（循环、淡入淡出、降低音量）
ffmpeg -stream_loop -1 -i bgm_original.mp3 \
  -t 85 \
  -af "volume=0.05,afade=t=in:st=0:d=3,afade=t=out:st=82:d=3" \
  bgm_processed.mp3

# 2. 混合配音和 BGM
ffmpeg -i voiceover.mp3 -i bgm_processed.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[out]" \
  -map "[out]" final_audio.mp3

# 3. 音量标准化
ffmpeg -i final_audio.mp3 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  final_audio_normalized.mp3
```

## 音量平衡建议

### 核心原则

**配音清晰度优先**：BGM 必须作为"背景"存在，绝不能盖过配音。人声频率(85-255Hz基频 + 泛音)与 BGM 重叠时尤其需要注意。

| 音频类型 | 相对音量 | 说明 |
|----------|----------|------|
| 配音 | 1.0 (100%) | 主音频，保持原音量 |
| BGM（有密集配音） | **0.05-0.08** | 确保配音清晰可辨 |
| BGM（有稀疏配音） | 0.08-0.12 | 配音间隙较多时 |
| BGM（无配音段落） | 0.15-0.25 | 片头/片尾/转场 |
| BGM（纯音乐段落） | 0.30-0.50 | 无配音时可提高 |

### 音量选择决策树

```
视频有配音吗？
├── 是 → 配音密度高吗（>70%时间有语音）？
│   ├── 是 → BGM volume = 0.05-0.06 (推荐 0.05)
│   └── 否 → BGM volume = 0.08-0.10
└── 否 → BGM volume = 0.25-0.40
```

### 测试方法

在正式渲染前，截取30秒包含配音的片段测试：
```bash
# 快速测试不同音量
for vol in 0.04 0.05 0.06 0.08; do
  ffmpeg -y -i bgm.mp3 -i voiceover.mp3 \
    -filter_complex "[0:a]volume=$vol[bgm];[1:a][bgm]amix=inputs=2[out]" \
    -map "[out]" -t 30 test_vol_$vol.mp3
done
```

### 动态音量控制（高级）

```bash
# 配音出现时自动降低 BGM（侧链压缩效果）
ffmpeg -i voiceover.mp3 -i bgm.mp3 \
  -filter_complex "
    [0:a]asplit=2[vo][vo_sidechain];
    [1:a]volume=0.3[bgm];
    [bgm][vo_sidechain]sidechaincompress=threshold=0.02:ratio=8:attack=50:release=500[bgm_ducked];
    [vo][bgm_ducked]amix=inputs=2:duration=first[out]
  " \
  -map "[out]" ducked_audio.mp3
```

## 智能 BGM 长度计算

### 问题：无脑循环的弊端

简单的 `-stream_loop -1` 会导致：
- BGM 在非自然位置截断
- 音乐节奏与视频内容不匹配
- 循环接缝处听感不自然

### 解决方案：场景感知的 BGM 选择

#### 策略 1: 选择合适长度的音乐

**优先选择**时长接近或略长于视频的 BGM：

| 视频时长 | 推荐 BGM 时长 | 策略 |
|----------|---------------|------|
| < 60s | 60-90s | 单曲裁剪 |
| 60-120s | 90-180s | 单曲裁剪 + 淡出 |
| 120-300s | 180-360s | 单曲或精心设计的接缝 |
| > 300s | 多首拼接 | 场景转换处切换 |

#### 策略 2: 基于场景结构计算

```python
# 场景时间配置
SCENES = {
    "opening": {"start": 0, "duration": 8},    # 片头
    "scene1": {"start": 8, "duration": 14},    # 场景1
    "scene2": {"start": 22, "duration": 16},   # 场景2
    "scene3": {"start": 38, "duration": 14},   # 场景3
    "scene4": {"start": 52, "duration": 20},   # 场景4
    "closing": {"start": 72, "duration": 13},  # 片尾
}

def calculate_bgm_strategy(scenes: dict, bgm_duration: float, video_duration: float):
    """
    计算 BGM 使用策略

    Returns:
        dict: 包含 trim_end, need_loop, loop_point 等信息
    """
    if bgm_duration >= video_duration:
        # BGM 够长，直接裁剪
        return {
            "strategy": "single_trim",
            "trim_end": video_duration,
            "need_loop": False
        }

    # BGM 不够长，找最佳循环点（场景边界）
    scene_boundaries = sorted([s["start"] for s in scenes.values()])

    # 找到最接近 BGM 时长的场景边界
    best_loop_point = min(
        scene_boundaries,
        key=lambda x: abs(x - bgm_duration) if x <= bgm_duration else float('inf')
    )

    return {
        "strategy": "scene_aware_loop",
        "loop_point": best_loop_point,
        "bgm_duration": bgm_duration,
        "loops_needed": math.ceil(video_duration / best_loop_point)
    }
```

#### 策略 3: 动态音量适配场景

不同场景使用不同 BGM 音量：

```python
# 场景音量配置
SCENE_VOLUMES = {
    "opening": 0.15,    # 片头无配音，音量较高
    "scene1": 0.05,     # 有配音场景
    "scene2": 0.05,
    "scene3": 0.05,
    "scene4": 0.05,
    "closing": 0.12,    # 片尾配音较少
}

def generate_volume_filter(scenes: dict, volumes: dict, fps: int = 30):
    """生成 FFmpeg 音量自动化滤镜"""
    points = []
    for name, scene in scenes.items():
        start_frame = scene["start"] * fps
        vol = volumes.get(name, 0.05)
        points.append(f"volume=enable='between(t,{scene['start']},{scene['start']+scene['duration']})':volume={vol}")

    return ",".join(points)
```

### FFmpeg 场景感知混合

```bash
# 使用 aeval 实现场景动态音量
# 片头(0-8s): 0.15, 正片(8-72s): 0.05, 片尾(72-85s): 0.12

ffmpeg -i voiceover.mp3 -i bgm.mp3 \
  -filter_complex "
    [1:a]volume='if(lt(t,8),0.15,if(lt(t,72),0.05,0.12))':eval=frame,
    afade=t=in:st=0:d=3,
    afade=t=out:st=82:d=3[bgm];
    [0:a][bgm]amix=inputs=2:duration=first[out]
  " \
  -map "[out]" mixed_audio.mp3
```

### 最佳实践

1. **优先选择时长合适的 BGM**：避免循环，选择 >= 视频时长的音乐
2. **如果必须循环**：在场景转换处设置循环点，而非音乐结尾
3. **场景边界淡入淡出**：循环接缝处使用交叉淡化
4. **动态音量**：片头片尾可略高，配音密集段落降低

---

## Remotion 动态音量控制 (推荐)

除了使用 FFmpeg 预处理，还可以在 Remotion 中直接实现动态音量控制。这种方式更灵活，便于调试。

### 基础用法：场景感知音量

```tsx
import { Audio, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { SCENES } from "./config/scenes";

// 场景音量配置
const SCENE_VOLUMES = {
  opening: 0.15,   // 片头无配音，音量较高
  scene1: 0.05,    // 有配音场景
  scene2: 0.05,
  scene3: 0.05,
  scene4: 0.05,
  closing: 0.12,   // 片尾配音较少
};

// 动态音量函数
const getDynamicVolume = (frame: number, fps: number): number => {
  const currentTime = frame / fps;

  // 遍历场景找到当前所在场景
  for (const [sceneName, scene] of Object.entries(SCENES)) {
    const sceneEnd = scene.start + scene.duration;
    if (currentTime >= scene.start && currentTime < sceneEnd) {
      return SCENE_VOLUMES[sceneName as keyof typeof SCENE_VOLUMES] ?? 0.05;
    }
  }
  return 0.05; // 默认音量
};

// 在组件中使用
export const VideoWithDynamicBGM: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <>
      {/* 配音 - 固定音量 */}
      <Audio src={staticFile("audio/voiceover.mp3")} volume={1} />

      {/* BGM - 动态音量 */}
      <Audio
        src={staticFile("audio/bgm.mp3")}
        volume={(frame) => getDynamicVolume(frame, fps)}
      />
    </>
  );
};
```

### 进阶用法：平滑过渡

```tsx
import { interpolate } from "remotion";

const getSmoothVolume = (frame: number, fps: number): number => {
  const currentTime = frame / fps;

  // 片头 (0-8s): 0.15 -> 片头结束前0.5s开始降低
  if (currentTime < 7.5) return 0.15;
  if (currentTime < 8) {
    return interpolate(currentTime, [7.5, 8], [0.15, 0.05]);
  }

  // 正片 (8-71.5s): 0.05
  if (currentTime < 71.5) return 0.05;

  // 正片结束 -> 片尾 (71.5-72s): 平滑过渡到 0.12
  if (currentTime < 72) {
    return interpolate(currentTime, [71.5, 72], [0.05, 0.12]);
  }

  // 片尾 (72-85s): 0.12
  return 0.12;
};
```

### 组件模板

```tsx
// components/DynamicBGM.tsx
import React from "react";
import { Audio, staticFile, useVideoConfig } from "remotion";

interface DynamicBGMProps {
  /** BGM 文件路径 (相对于 public/) */
  src: string;
  /** 场景音量配置 */
  sceneVolumes: Record<string, number>;
  /** 场景时间配置 */
  scenes: Record<string, { start: number; duration: number }>;
  /** 是否启用平滑过渡 (默认 true) */
  smoothTransition?: boolean;
  /** 过渡时长 (秒, 默认 0.5) */
  transitionDuration?: number;
}

export const DynamicBGM: React.FC<DynamicBGMProps> = ({
  src,
  sceneVolumes,
  scenes,
  smoothTransition = true,
  transitionDuration = 0.5,
}) => {
  const { fps } = useVideoConfig();

  const getVolume = (frame: number): number => {
    const currentTime = frame / fps;

    for (const [sceneName, scene] of Object.entries(scenes)) {
      const sceneEnd = scene.start + scene.duration;
      if (currentTime >= scene.start && currentTime < sceneEnd) {
        return sceneVolumes[sceneName] ?? 0.05;
      }
    }
    return 0.05;
  };

  return (
    <Audio
      src={staticFile(src)}
      volume={(frame) => getVolume(frame)}
    />
  );
};
```

### FFmpeg vs Remotion 对比

| 方面 | FFmpeg 预处理 | Remotion 动态控制 |
|------|--------------|------------------|
| 调试便捷性 | ⚠️ 需重新处理音频 | ✅ 实时预览 |
| 灵活性 | ⚠️ 固定一次 | ✅ 随时调整 |
| 渲染性能 | ✅ 无额外开销 | ⚠️ 微小开销 |
| 文件大小 | ⚠️ 预混合体积大 | ✅ 分离存储 |
| 推荐场景 | 最终交付 | 开发调试 |

**建议工作流**：
1. 开发阶段使用 Remotion 动态控制快速调试
2. 确定最终参数后，使用 FFmpeg 预处理生成交付版本

---

## Python 脚本模板

```python
#!/usr/bin/env python3
"""
背景音乐处理脚本
"""

import subprocess
from pathlib import Path

def process_bgm(
    bgm_path: str,
    voiceover_path: str,
    output_path: str,
    video_duration: float,
    bgm_volume: float = 0.05,  # 默认低音量，确保配音清晰
    fade_duration: float = 3.0
):
    """
    处理背景音乐并与配音混合

    Args:
        bgm_path: BGM 文件路径
        voiceover_path: 配音文件路径
        output_path: 输出文件路径
        video_duration: 视频总时长（秒）
        bgm_volume: BGM 相对音量 (0.0-1.0)
        fade_duration: 淡入淡出时长（秒）
    """
    fade_out_start = video_duration - fade_duration

    # 构建 filter_complex
    filter_complex = f"""
        [1:a]aloop=loop=-1:size=2e+09,atrim=0:{video_duration},
        volume={bgm_volume},
        afade=t=in:st=0:d={fade_duration},
        afade=t=out:st={fade_out_start}:d={fade_duration}[bgm];
        [0:a][bgm]amix=inputs=2:duration=first[out]
    """.replace("\n", "").replace("  ", "")

    cmd = [
        "ffmpeg", "-y",
        "-i", voiceover_path,
        "-i", bgm_path,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"✓ 混合音频输出: {output_path}")

def normalize_audio(input_path: str, output_path: str):
    """音量标准化到 -16 LUFS"""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ 标准化输出: {output_path}")

# 使用示例
if __name__ == "__main__":
    process_bgm(
        bgm_path="public/audio/bgm_epic.mp3",
        voiceover_path="public/audio/synced_voiceover.mp3",
        output_path="public/audio/mixed_audio.mp3",
        video_duration=85,
        bgm_volume=0.05,  # 配音密集时推荐 0.05
        fade_duration=3.0
    )

    normalize_audio(
        input_path="public/audio/mixed_audio.mp3",
        output_path="public/audio/final_audio.mp3"
    )
```

## Remotion 集成

在 Remotion 组件中使用混合后的音频：

```tsx
import { Audio, staticFile } from "remotion";

export const FinalVideo: React.FC = () => {
  return (
    <>
      {/* 使用混合后的音频（配音 + BGM） */}
      <Audio src={staticFile("audio/final_audio.mp3")} volume={1} />

      {/* 或者分开控制 */}
      <Audio src={staticFile("audio/synced_voiceover.mp3")} volume={1} />
      <Audio
        src={staticFile("audio/bgm.mp3")}
        volume={(f) => {
          // 淡入淡出控制
          const fps = 30;
          if (f < 3 * fps) return (f / (3 * fps)) * 0.12;
          if (f > 82 * fps) return ((85 * fps - f) / (3 * fps)) * 0.12;
          return 0.12;
        }}
      />
    </>
  );
};
```

## 工作流程

```
1. 确定视频风格 → 选择音乐关键词
2. 从免版权网站下载 BGM
3. 处理 BGM（循环/裁剪到视频时长）
4. 添加淡入淡出效果
5. 与配音混合（配音优先）
6. 音量标准化
7. 集成到视频
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| BGM 太响干扰配音 | 降低 volume 到 0.04-0.06（配音密集时推荐 0.05） |
| BGM 不够长 | 优先选择更长的音乐；必须循环时在场景边界处接缝 |
| 淡入淡出太突然 | 增加 fade_duration 到 4-5 秒 |
| 混合后音量不一致 | 使用 loudnorm 滤镜标准化 |
| 风格不匹配 | 重新选择更合适的 BGM |
| 循环接缝明显 | 使用交叉淡化或在场景转换处设置循环点 |
