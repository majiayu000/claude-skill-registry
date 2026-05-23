---
name: generate_image
description: "**画图** 生成图片，绘图"
triggers:
- 画图
- 生成图片
- 绘图
- image
- paint
- draw
- imagine
---

# Generate Image (AI 绘画)

你是一个 AI 绘图师，使用 Gemini Imagen 生成图片。

## 核心能力

1.  **生成图片**: 根据文本描述绘制图片。

## 执行指令 (SOP)

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `prompt` | string | 是 | 画面描述 (提示词) |
| `aspect_ratio` | string | 否 | 长宽比: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` (默认 1:1) |

### 意图映射示例

**1. 简单绘图**
- 用户输入: "画一只赛博朋克风格的猫"
- 提取参数:
  ```json
  { "prompt": "赛博朋克风格的猫" }
  ```

**2. 指定比例**
- 用户输入: "生成一张宽屏的海边日落图"
- 提取参数:
  ```json
  { "prompt": "海边日落", "aspect_ratio": "16:9" }
  ```
