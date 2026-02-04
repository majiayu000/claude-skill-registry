---
name: remotion-best-practices
description: "Remotion 视频创建最佳实践。当处理 Remotion 代码、创建视频动画、使用 React 制作视频、处理视频合成、动画、音频、字幕、图表、3D 内容，或提到「remotion」「视频制作」「react 视频」「动画视频」时使用。提供 Remotion 领域专业知识。"
license: MIT
---

# Remotion 最佳实践

本技能提供 Remotion 视频创建的专业知识和最佳实践。

## 何时使用

在处理 Remotion 代码时使用本技能，以获取领域专业知识。

## 如何使用

阅读各个规则文件以获取详细说明和代码示例。根据任务需要，按需加载相应的规则文件：

### 核心概念

- **Compositions（合成）**：定义视频合成、静态帧、文件夹、默认属性和动态元数据
- **Animations（动画）**：Remotion 的基础动画技能
- **Timing（时间）**：插值曲线 - 线性、缓动、弹簧动画
- **Sequencing（序列）**：Remotion 的序列模式 - 延迟、修剪、限制项目时长

### 媒体资源

- **Assets（资源）**：在 Remotion 中导入图像、视频、音频和字体
- **Images（图像）**：使用 Img 组件在 Remotion 中嵌入图像
- **Videos（视频）**：在 Remotion 中嵌入视频 - 修剪、音量、速度、循环、音调
- **Audio（音频）**：在 Remotion 中使用音频和声音 - 导入、修剪、音量、速度、音调
- **GIFs**：在 Remotion 的时间轴上同步显示 GIF

### 文本与字幕

- **Text Animations（文本动画）**：Remotion 的排版和文本动画模式
- **Measuring Text（测量文本）**：测量文本尺寸、将文本适配到容器、检查溢出
- **Display Captions（显示字幕）**：在 Remotion 中显示字幕，支持 TikTok 风格页面和单词高亮
- **Import SRT Captions（导入 SRT 字幕）**：使用 @remotion/captions 将 .srt 字幕文件导入 Remotion
- **Transcribe Captions（转录字幕）**：将音频转录以在 Remotion 中生成字幕

### 高级功能

- **3D Content（3D 内容）**：使用 Three.js 和 React Three Fiber 在 Remotion 中创建 3D 内容
- **Charts（图表）**：Remotion 的图表和数据可视化模式
- **Lottie**：在 Remotion 中嵌入 Lottie 动画
- **Maps（地图）**：使用 Mapbox 添加地图并为其添加动画
- **Transitions（过渡）**：Remotion 的场景过渡模式
- **Trimming（修剪）**：Remotion 的修剪模式 - 剪切动画的开头或结尾

### 工具与实用功能

- **Fonts（字体）**：在 Remotion 中加载 Google Fonts 和本地字体
- **Tailwind**：在 Remotion 中使用 TailwindCSS
- **Measuring DOM Nodes（测量 DOM 节点）**：在 Remotion 中测量 DOM 元素尺寸
- **Calculate Metadata（计算元数据）**：动态设置合成时长、尺寸和属性
- **Parameters（参数）**：通过添加 Zod schema 使视频可参数化

### Mediabunny 集成

- **Can Decode（可解码）**：使用 Mediabunny 检查浏览器是否可以解码视频
- **Extract Frames（提取帧）**：使用 Mediabunny 在特定时间戳从视频中提取帧
- **Get Audio Duration（获取音频时长）**：使用 Mediabunny 获取音频文件的时长（秒）
- **Get Video Dimensions（获取视频尺寸）**：使用 Mediabunny 获取视频文件的宽度和高度
- **Get Video Duration（获取视频时长）**：使用 Mediabunny 获取视频文件的时长（秒）

## 规则文件索引

详细规则和代码示例请参考 `references/` 目录下的文件：

### 核心规则
- `references/compositions.md` - 定义合成、静态帧、文件夹、默认属性和动态元数据
- `references/animations.md` - Remotion 的基础动画技能
- `references/timing.md` - 插值曲线：线性、缓动、弹簧动画
- `references/sequencing.md` - 序列模式：延迟、修剪、限制时长

### 媒体资源规则
- `references/assets.md` - 导入图像、视频、音频和字体
- `references/images.md` - 使用 Img 组件嵌入图像
- `references/videos.md` - 嵌入视频：修剪、音量、速度、循环、音调
- `references/audio.md` - 使用音频和声音：导入、修剪、音量、速度、音调
- `references/gifs.md` - 同步显示 GIF

### 文本与字幕规则
- `references/text-animations.md` - 排版和文本动画模式
- `references/measuring-text.md` - 测量文本尺寸、适配文本、检查溢出
- `references/display-captions.md` - 显示字幕，支持 TikTok 风格和单词高亮
- `references/import-srt-captions.md` - 导入 .srt 字幕文件
- `references/transcribe-captions.md` - 音频转录生成字幕

### 高级功能规则
- `references/3d.md` - 使用 Three.js 和 React Three Fiber 创建 3D 内容
- `references/charts.md` - 图表和数据可视化模式
- `references/lottie.md` - 嵌入 Lottie 动画
- `references/maps.md` - 使用 Mapbox 添加和动画化地图
- `references/transitions.md` - 场景过渡模式
- `references/trimming.md` - 修剪模式：剪切动画开头或结尾

### 工具与实用功能规则
- `references/fonts.md` - 加载 Google Fonts 和本地字体
- `references/tailwind.md` - 使用 TailwindCSS
- `references/measuring-dom-nodes.md` - 测量 DOM 元素尺寸
- `references/calculate-metadata.md` - 动态设置合成元数据
- `references/parameters.md` - 使用 Zod schema 使视频可参数化

### Mediabunny 集成规则
- `references/can-decode.md` - 检查视频是否可解码
- `references/extract-frames.md` - 从视频中提取帧
- `references/get-audio-duration.md` - 获取音频时长
- `references/get-video-dimensions.md` - 获取视频尺寸
- `references/get-video-duration.md` - 获取视频时长

## 使用建议

1. **按需加载**：根据当前任务，只加载相关的规则文件到上下文
2. **查看示例**：每个规则文件都包含代码示例，可直接参考
3. **组合使用**：多个规则可以组合使用，例如：动画 + 过渡 + 字幕
4. **性能优化**：注意视频渲染性能，合理使用修剪和序列化

## 常见任务模式

### 创建基础视频
1. 定义 Composition（`references/compositions.md`）
2. 添加动画（`references/animations.md`）
3. 导入资源（`references/assets.md`）

### 添加字幕
1. 导入或转录字幕（`references/import-srt-captions.md` 或 `references/transcribe-captions.md`）
2. 显示字幕（`references/display-captions.md`）

### 处理视频
1. 获取视频信息（`references/get-video-duration.md`、`references/get-video-dimensions.md`）
2. 嵌入和修剪（`references/videos.md`）
3. 添加过渡（`references/transitions.md`）

### 创建 3D 内容
1. 设置 Three.js（`references/3d.md`）
2. 添加动画和过渡

---

**注意**：本技能使用渐进式披露原则。SKILL.md 提供概览和索引，详细规则和代码示例在 `references/` 目录中，按需加载。
