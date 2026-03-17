---
name: slack-gif-creator
description: 用于创建针对 Slack 优化的动画 GIF 的知识和工具集。提供约束条件、验证工具和动画概念。当用户请求为 Slack 创建动画 GIF 时使用，例如"为 Slack 制作一个 X 做 Y 的 GIF"。
license: 完整条款见 LICENSE.txt
---

# Slack GIF 创建器

一个提供工具和知识的工具包，用于创建针对 Slack 优化的动画 GIF。

## Slack 要求

**尺寸：**
- 表情符号 GIF：128x128（推荐）
- 消息 GIF：480x480

**参数：**
- FPS：10-30（较低的值可减小文件大小）
- 颜色：48-128（颜色越少 = 文件越小）
- 时长：表情符号 GIF 应控制在 3 秒以内

## 核心工作流程

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 创建构建器
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 生成帧
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # 使用 PIL 基础图形绘制你的动画
    # （圆形、多边形、线条等）

    builder.add_frame(frame)

# 3. 保存并优化
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

### 处理用户上传的图片
如果用户上传了图片，请考虑他们想要：
- **直接使用**（例如，"给这个添加动画"，"把这个分成帧"）
- **作为灵感参考**（例如，"制作类似这样的东西"）

使用 PIL 加载和处理图片：
```python
from PIL import Image

uploaded = Image.open('file.png')
# 直接使用，或仅作为颜色/风格的参考
```

### 从零开始绘制
从零开始绘制图形时，使用 PIL ImageDraw 基础图形：

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# 圆形/椭圆
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# 星形、三角形、任何多边形
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# 线条
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# 矩形
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**不要使用：** Emoji 字体（在不同平台上表现不一致）或假设此技能中有预打包的图形。

### 让图形更美观

图形应该看起来精致有创意，而不是简陋。以下是方法：

**使用较粗的线条** - 轮廓和线条始终设置 `width=2` 或更高。细线（width=1）看起来粗糙且业余。

**添加视觉深度**：
- 使用渐变背景（`create_gradient_background`）
- 叠加多个形状以增加复杂度（例如，一个星形内部套一个小星形）

**让形状更有趣**：
- 不要只画一个普通的圆 - 添加高光、光环或图案
- 星形可以有光晕（在后面绘制更大的半透明版本）
- 组合多个形状（星形 + 闪光、圆形 + 光环）

**注意颜色搭配**：
- 使用鲜艳的互补色
- 添加对比度（浅色形状用深色轮廓，深色形状用浅色轮廓）
- 考虑整体构图

**对于复杂形状**（心形、雪花等）：
- 使用多边形和椭圆的组合
- 仔细计算点位以保持对称
- 添加细节（心形可以有高光曲线，雪花有精细的分支）

要有创意和注重细节！好的 Slack GIF 应该看起来精致，而不是像占位图形。

## 可用工具

### GIFBuilder (`core.gif_builder`)
组装帧并为 Slack 优化：
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # 添加 PIL Image
builder.add_frames(frames)  # 添加帧列表
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### 验证器 (`core.validators`)
检查 GIF 是否符合 Slack 要求：
```python
from core.validators import validate_gif, is_slack_ready

# 详细验证
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# 快速检查
if is_slack_ready('my.gif'):
    print("准备就绪！")
```

### 缓动函数 (`core.easing`)
平滑运动而非线性：
```python
from core.easing import interpolate

# 进度从 0.0 到 1.0
t = i / (num_frames - 1)

# 应用缓动
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# 可用：linear, ease_in, ease_out, ease_in_out,
#      bounce_out, elastic_out, back_out
```

### 帧辅助函数 (`core.frame_composer`)
常用需求的便捷函数：
```python
from core.frame_composer import (
    create_blank_frame,         # 纯色背景
    create_gradient_background,  # 垂直渐变
    draw_circle,                # 圆形辅助函数
    draw_text,                  # 简单文字渲染
    draw_star                   # 五角星
)
```

## 动画概念

### 抖动/振动
用振荡偏移对象位置：
- 使用 `math.sin()` 或 `math.cos()` 配合帧索引
- 添加小的随机变化以获得自然感觉
- 应用于 x 和/或 y 位置

### 脉动/心跳
有节奏地缩放对象大小：
- 使用 `math.sin(t * frequency * 2 * math.pi)` 实现平滑脉动
- 对于心跳效果：两次快速脉动然后暂停（调整正弦波）
- 在基础大小的 0.8 到 1.2 倍之间缩放

### 弹跳
对象下落并弹起：
- 使用 `interpolate()` 配合 `easing='bounce_out'` 实现落地效果
- 使用 `easing='ease_in'` 实现下落（加速）效果
- 通过每帧增加 y 速度来模拟重力

### 旋转
围绕中心旋转对象：
- PIL：`image.rotate(angle, resample=Image.BICUBIC)`
- 对于摇摆效果：使用正弦波控制角度而非线性变化

### 淡入/淡出
逐渐出现或消失：
- 创建 RGBA 图像，调整 alpha 通道
- 或使用 `Image.blend(image1, image2, alpha)`
- 淡入：alpha 从 0 到 1
- 淡出：alpha 从 1 到 0

### 滑动
将对象从屏幕外移动到指定位置：
- 起始位置：帧边界外
- 结束位置：目标位置
- 使用 `interpolate()` 配合 `easing='ease_out'` 实现平滑停止
- 对于超越效果：使用 `easing='back_out'`

### 缩放
缩放和定位以实现缩放效果：
- 放大：从 0.1 缩放到 2.0，裁剪中心
- 缩小：从 2.0 缩放到 1.0
- 可添加运动模糊增加戏剧效果（PIL 滤镜）

### 爆炸/粒子迸发
创建向外辐射的粒子：
- 生成具有随机角度和速度的粒子
- 更新每个粒子：`x += vx`，`y += vy`
- 添加重力：`vy += gravity_constant`
- 随时间淡出粒子（降低 alpha）

## 优化策略

仅在被要求减小文件大小时，实施以下几种方法：

1. **减少帧数** - 降低 FPS（用 10 而不是 20）或缩短时长
2. **减少颜色** - `num_colors=48` 而不是 128
3. **减小尺寸** - 128x128 而不是 480x480
4. **移除重复帧** - 在 save() 中使用 `remove_duplicates=True`
5. **表情符号模式** - `optimize_for_emoji=True` 自动优化

```python
# 表情符号最大优化
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## 设计理念

本技能提供：
- **知识**：Slack 的要求和动画概念
- **工具**：GIFBuilder、验证器、缓动函数
- **灵活性**：使用 PIL 基础图形创建动画逻辑

本技能不提供：
- 僵化的动画模板或预制函数
- Emoji 字体渲染（在不同平台上表现不一致）
- 内置于技能中的预打包图形库

**关于用户上传的说明**：本技能不包含预构建的图形，但如果用户上传了图片，请使用 PIL 加载和处理它 - 根据他们的请求判断是直接使用还是仅作为灵感参考。

发挥创意！组合各种概念（弹跳 + 旋转、脉动 + 滑动等）并充分利用 PIL 的全部功能。

## 依赖项

```bash
pip install pillow imageio numpy
```
