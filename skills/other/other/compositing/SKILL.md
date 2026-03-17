---
name: compositing
description: 使用 Remotion 合成最终视频。当需要将片头、录屏、配音、片尾组合成完整视频时使用。包含动画效果、时间线管理、多尺寸模板和故障处理。
argument-hint: [项目路径] [尺寸: 1080p/720p/vertical/square/4k]
---

# 视频合成技能

## 快速开始：使用模板

项目提供了可复用的配置和组件模板，位于 `templates/` 目录：

```bash
templates/
├── config/                # 配置模板
│   ├── scenes.ts          # 场景时间配置
│   ├── theme.ts           # 主题颜色配置
│   ├── types.ts           # TypeScript 类型定义
│   ├── videoPresets.ts    # 多尺寸视频预设
│   └── index.ts           # 统一导出
└── components/            # 组件模板
    ├── SubtitleDisplay.tsx    # 字幕组件
    ├── AnimatedText.tsx       # 动画文字组件
    ├── BackgroundEffects.tsx  # 背景效果组件
    ├── BrandElements.tsx      # 品牌元素组件
    ├── useResponsive.ts       # 响应式 Hook
    └── index.ts               # 统一导出
```

### 使用方法

1. 复制模板到项目目录：
```bash
cp -r templates/config src/config
cp -r templates/components src/components
```

2. 根据项目需要修改配置（颜色、场景时间等）

3. 在组件中导入使用：
```tsx
import { SCENES, FPS, VIDEO_DURATION } from "./config";
import { THEME, getGlowStyle } from "./config";
import { SubtitleDisplay, FadeInText, ParticleField } from "./components";
```

---

## 多尺寸视频模板

### 预设尺寸

| 名称 | 分辨率 | 比例 | 适用平台 |
|------|--------|------|----------|
| 1080p (默认) | 1920×1080 | 16:9 | YouTube, 官网 |
| 720p | 1280×720 | 16:9 | 快速预览, 低带宽 |
| vertical | 1080×1920 | 9:16 | 抖音, 小红书, Reels |
| square | 1080×1080 | 1:1 | Instagram, 微信 |
| 4K | 3840×2160 | 16:9 | 高端展示 |

### Remotion 多尺寸配置

```tsx
// videoPresets.ts
export const VIDEO_PRESETS = {
  "1080p": { width: 1920, height: 1080, name: "Full HD" },
  "720p": { width: 1280, height: 720, name: "HD" },
  "vertical": { width: 1080, height: 1920, name: "Vertical" },
  "square": { width: 1080, height: 1080, name: "Square" },
  "4k": { width: 3840, height: 2160, name: "4K" },
} as const;

export type VideoPreset = keyof typeof VIDEO_PRESETS;
```

### Root.tsx 多尺寸定义

```tsx
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import { VIDEO_PRESETS, VideoPreset } from "./videoPresets";

const FPS = 30;
const DURATION_SECONDS = 85;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 为每个尺寸创建 Composition */}
      {Object.entries(VIDEO_PRESETS).map(([key, preset]) => (
        <Composition
          key={key}
          id={`Video-${key}`}
          component={MainVideo}
          durationInFrames={DURATION_SECONDS * FPS}
          fps={FPS}
          width={preset.width}
          height={preset.height}
          defaultProps={{ preset: key as VideoPreset }}
        />
      ))}
    </>
  );
};
```

### 响应式组件适配

```tsx
// 根据视频尺寸调整布局
const ResponsiveLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { width, height } = useVideoConfig();
  const aspectRatio = width / height;

  // 竖屏布局 (9:16)
  if (aspectRatio < 1) {
    return (
      <AbsoluteFill style={{ flexDirection: "column", padding: "60px 40px" }}>
        {children}
      </AbsoluteFill>
    );
  }

  // 方形布局 (1:1)
  if (aspectRatio === 1) {
    return (
      <AbsoluteFill style={{ padding: "40px" }}>
        {children}
      </AbsoluteFill>
    );
  }

  // 横屏布局 (16:9)
  return (
    <AbsoluteFill style={{ padding: "60px 120px" }}>
      {children}
    </AbsoluteFill>
  );
};
```

### 字体大小适配

```tsx
// 根据分辨率计算字体大小
const getResponsiveFontSize = (baseSize: number): number => {
  const { width, height } = useVideoConfig();
  const scale = Math.min(width / 1920, height / 1080);
  return Math.round(baseSize * scale);
};

// 使用示例
const title = getResponsiveFontSize(72); // 1080p 下 72px
```

### 批量渲染脚本

```bash
#!/bin/bash
# render_all_sizes.sh

SIZES=("1080p" "720p" "vertical" "square")
OUTPUT_DIR="out"

for size in "${SIZES[@]}"; do
  echo "渲染 $size..."
  npx remotion render src/index.ts "Video-$size" "$OUTPUT_DIR/video_$size.mp4"
done

echo "所有尺寸渲染完成!"
```

---

## Remotion 基础

Remotion 是 React-based 的视频渲染框架，使用 React 组件定义视频内容。

### 核心概念

| 概念 | 说明 |
|------|------|
| Composition | 视频组合定义（分辨率、帧率、时长） |
| Sequence | 时间序列，控制内容出现时机 |
| useCurrentFrame | 获取当前帧数 |
| interpolate | 数值插值，用于动画 |
| spring | 弹性动画 |

### 基本结构

```tsx
import { Composition } from "remotion";

export const RemotionRoot = () => {
  return (
    <Composition
      id="FinalVideo"
      component={FinalVideo}
      durationInFrames={2550}  // 85秒 * 30fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

## 故障处理 (重要)

### 浏览器下载失败

**问题表现**:
```
Error: Tried to download file xxx, but the server sent no data for 20 seconds
```

**解决方案 A: 手动下载 Chrome Headless Shell**

```bash
# 1. 手动下载 (更长超时)
curl -L --connect-timeout 30 --max-time 300 \
  "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/mac-arm64/chrome-headless-shell-mac-arm64.zip" \
  -o /tmp/chrome-headless-shell.zip

# 2. 解压到 Remotion 缓存目录
mkdir -p ~/.cache/remotion
unzip /tmp/chrome-headless-shell.zip -d ~/.cache/remotion/

# 3. 渲染时指定浏览器路径
npx remotion render src/index.ts VideoId out/video.mp4 \
  --browser-executable="$HOME/.cache/remotion/chrome-headless-shell-mac-arm64/chrome-headless-shell"
```

**解决方案 B: 使用代理**

```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
npx remotion browser ensure
```

### 其他常见问题

| 问题 | 解决方案 |
|------|----------|
| Chrome 下载失败 | 手动下载或使用代理 |
| 视频文件找不到 | 确保在 `public/` 目录，用 `staticFile()` |
| 渲染内存不足 | `--concurrency=4` 减少并发 |
| 字体不显示 | 使用 `@remotion/google-fonts` |

## 字体配置

### 使用 Google Fonts (推荐)

```bash
npm install @remotion/google-fonts
```

```tsx
// 加载中文字体
import { loadFont } from "@remotion/google-fonts/NotoSansSC";
const { fontFamily } = loadFont();

// 在组件中使用
<div style={{ fontFamily }}>中文文字</div>
```

### 推荐中文字体

| 字体 | 包名 | 风格 |
|------|------|------|
| Noto Sans SC | NotoSansSC | 现代无衬线 |
| Noto Serif SC | NotoSerifSC | 经典衬线 |
| ZCOOL XiaoWei | ZCOOLXiaoWei | 手写风格 |

### 备选：系统字体栈

```tsx
const fontFamily = `
  "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
  "WenQuanYi Micro Hei", system-ui, sans-serif
`;
```

## 高级动画模式

### 1. Logo 弹性缩放 + 发光

```tsx
const LogoWithGlow: React.FC<{ src: string }> = ({ src }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const glowIntensity = interpolate(
    Math.sin(frame * 0.08),
    [-1, 1],
    [0.3, 0.8]
  );

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        filter: `drop-shadow(0 0 ${40 * glowIntensity}px #76B900)`,
      }}
    >
      <Img src={src} style={{ width: 400 }} />
    </div>
  );
};
```

### 2. 文字淡入 + 上移

```tsx
const FadeInText: React.FC<{ text: string; delay?: number }> = ({
  text,
  delay = 0,
}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [delay, delay + 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [delay, delay + 30], [20, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      {text}
    </div>
  );
};
```

### 3. 打字机效果

```tsx
const TypewriterText: React.FC<{ text: string; speed?: number }> = ({
  text,
  speed = 3,
}) => {
  const frame = useCurrentFrame();

  const charsToShow = Math.floor(
    interpolate(frame, [0, text.length * speed], [0, text.length], {
      extrapolateRight: "clamp",
    })
  );

  return <span>{text.slice(0, charsToShow)}</span>;
};
```

### 4. 年份大字弹入

```tsx
const YearDisplay: React.FC<{ year: string; color?: string }> = ({
  year,
  color = "#76B900",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 80 },
  });

  return (
    <div
      style={{
        fontSize: 200,
        fontWeight: "bold",
        color,
        transform: `scale(${scale})`,
        textShadow: `0 0 60px ${color}`,
      }}
    >
      {year}
    </div>
  );
};
```

### 5. 背景图渐变叠加

```tsx
const BackgroundWithOverlay: React.FC<{
  src: string;
  opacity?: number;
}> = ({ src, opacity = 0.3 }) => {
  return (
    <>
      <AbsoluteFill>
        <Img
          src={staticFile(src)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity,
          }}
        />
      </AbsoluteFill>
      {/* 渐变叠加层 */}
      <AbsoluteFill
        style={{
          background: "linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.8) 100%)",
        }}
      />
    </>
  );
};
```

### 6. 数据卡片动画

```tsx
const DataCard: React.FC<{
  value: string;
  label: string;
  delay: number;
}> = ({ value, label, delay }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const scale = interpolate(frame, [delay, delay + 20], [0.8, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        textAlign: "center",
      }}
    >
      <div style={{ fontSize: 56, color: "#76B900", fontWeight: "bold" }}>
        {value}
      </div>
      <div style={{ fontSize: 24, color: "#888" }}>{label}</div>
    </div>
  );
};
```

---

## 重要最佳实践

### 1. 防止随机字符闪烁 (重要!)

当使用随机生成的字符（如代码雨效果）时，**必须使用 useMemo + seeded random** 来防止每帧重新生成导致的闪烁。

**错误示例 (会闪烁):**
```tsx
// ❌ 错误：每帧都会重新生成随机字符
const CodeRain: React.FC = () => {
  const chars = Array.from({ length: 25 }, () =>
    String.fromCharCode(0x30A0 + Math.floor(Math.random() * 96))
  ).join("");
  return <div>{chars}</div>;
};
```

**正确示例:**
```tsx
// ✅ 正确：使用 useMemo + seeded random
const CodeRain: React.FC = () => {
  const codeLines = useMemo(() => {
    // Seeded random 确保相同种子产生相同结果
    const seededRandom = (seed: number) => {
      const x = Math.sin(seed * 9999) * 10000;
      return x - Math.floor(x);
    };

    return Array.from({ length: 25 }, (_, i) => ({
      chars: Array.from({ length: 25 }, (_, j) =>
        String.fromCharCode(0x30A0 + Math.floor(seededRandom(i * 100 + j) * 96))
      ).join(""),
    }));
  }, []); // 空依赖数组 = 只计算一次

  return (
    <>
      {codeLines.map((line, i) => (
        <div key={i}>{line.chars}</div>
      ))}
    </>
  );
};
```

### 2. 使用共享配置

将 FPS、场景时间、主题颜色等配置集中管理，避免重复定义和不一致：

```tsx
// ✅ 正确：从共享配置导入
import { SCENES, FPS, VIDEO_DURATION } from "./config/scenes";
import { THEME } from "./config/theme";

// ❌ 错误：在组件中重复定义
const FPS = 30;  // 避免这样做
const NVIDIA_GREEN = "#76B900";  // 应该用 THEME.primary
```

### 3. 场景时间验证

使用 `validateScenes()` 函数检查场景配置：

```tsx
import { validateScenes, SCENES } from "./config/scenes";

// 在开发时验证
const { valid, errors } = validateScenes();
if (!valid) {
  console.error("场景配置错误:", errors);
}
```

### 4. 神经网络粒子效果

用于 AI/科技主题视频的动态粒子可视化：

```tsx
import React, { useMemo } from "react";
import { useCurrentFrame } from "remotion";

interface NeuralNetworkProps {
  nodeCount?: number;
  color?: string;
  centerX?: number;
  centerY?: number;
  spreadX?: number;
  spreadY?: number;
}

/**
 * 神经网络可视化效果
 *
 * 效果：飘动的发光节点，模拟神经网络的活跃状态
 * 适用场景：AI 主题、数据可视化、科技感背景
 */
export const NeuralNetwork: React.FC<NeuralNetworkProps> = ({
  nodeCount = 40,
  color = "#76B900",
  centerX = 960,
  centerY = 480,
  spreadX = 350,
  spreadY = 180,
}) => {
  const frame = useCurrentFrame();

  // 使用 useMemo 缓存节点属性，防止闪烁
  const nodes = useMemo(() => {
    return Array.from({ length: nodeCount }, (_, i) => ({
      size: 4 + (i % 6),
      opacity: 0.25 + ((i % 8) * 0.06),
      offsetMultiplierX: i * 0.4,
      offsetMultiplierY: i * 0.3,
      speedX: 0.015,
      speedY: 0.012,
    }));
  }, [nodeCount]);

  return (
    <>
      {nodes.map((node, i) => {
        const x = Math.sin(frame * node.speedX + node.offsetMultiplierX) * spreadX + centerX;
        const y = Math.cos(frame * node.speedY + node.offsetMultiplierY) * spreadY + centerY;

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: node.size,
              height: node.size,
              borderRadius: "50%",
              backgroundColor: color,
              opacity: node.opacity,
              boxShadow: `0 0 ${node.size * 4}px ${color}`,
            }}
          />
        );
      })}
    </>
  );
};

// 使用示例
<NeuralNetwork
  nodeCount={50}
  color="#76B900"
  centerX={960}
  centerY={540}
  spreadX={400}
  spreadY={200}
/>
```

模板位置：`templates/components/BackgroundEffects.tsx`

---

## 图文视频组件模板

### 完整场景示例

```tsx
import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

const FPS = 30;

// 场景时间配置
const SCENES = {
  opening: { start: 0, duration: 8 },
  scene1: { start: 8, duration: 14 },
  scene2: { start: 22, duration: 16 },
  closing: { start: 38, duration: 12 },
};

// 主题颜色
const THEME = {
  primary: "#76B900",
  background: "#0a0a0a",
  text: "#ffffff",
  muted: "#888888",
};

// 场景组件
const OpeningScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({ frame, fps, config: { damping: 12 } });
  const titleOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateLeft: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: THEME.background, justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${logoScale})` }}>
        <Img src={staticFile("images/logo.png")} style={{ width: 400 }} />
      </div>
      <h1 style={{ color: THEME.text, fontSize: 72, opacity: titleOpacity }}>
        标题文字
      </h1>
    </AbsoluteFill>
  );
};

// 主视频组件
export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill>
      <Audio src={staticFile("audio/synced_voiceover.mp3")} volume={1} />

      <Sequence from={SCENES.opening.start * FPS} durationInFrames={SCENES.opening.duration * FPS}>
        <OpeningScene />
      </Sequence>

      {/* 更多场景... */}
    </AbsoluteFill>
  );
};
```

## 渲染命令

```bash
# 开发预览
npm run studio

# 渲染输出
npx remotion render src/index.ts VideoId out/video.mp4

# 指定浏览器路径
npx remotion render src/index.ts VideoId out/video.mp4 \
  --browser-executable="$HOME/.cache/remotion/chrome-headless-shell-mac-arm64/chrome-headless-shell"

# 减少并发 (内存不足时)
npx remotion render src/index.ts VideoId out/video.mp4 --concurrency=4
```

## 后期处理

### 音量标准化

```bash
# 渲染后标准化音量
ffmpeg -y -i out/video_raw.mp4 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:v copy \
  out/video_final.mp4
```

### 压缩优化

```bash
# 压缩视频 (保持质量)
ffmpeg -i out/video.mp4 -c:v libx264 -crf 23 -preset medium -c:a copy out/video_compressed.mp4
```

## 项目文件结构

```
src/
├── index.ts              # 入口文件
├── Root.tsx              # Composition 定义
├── MainVideo.tsx         # 主视频组件
├── scenes/               # 场景组件
│   ├── OpeningScene.tsx
│   ├── ContentScene.tsx
│   └── ClosingScene.tsx
├── components/           # 可复用组件
│   ├── Background.tsx
│   ├── AnimatedText.tsx
│   ├── DataCard.tsx
│   └── Logo.tsx
└── utils/
    ├── theme.ts          # 主题配置
    └── animations.ts     # 动画工具函数
```

## 检查清单

- [ ] 音频文件存在且路径正确
- [ ] 图片文件存在且路径正确
- [ ] 时间线计算正确（总帧数 = 各段之和）
- [ ] 场景之间无缝隙
- [ ] 字体正确加载
- [ ] 渲染输出无错误
- [ ] 音量已标准化
