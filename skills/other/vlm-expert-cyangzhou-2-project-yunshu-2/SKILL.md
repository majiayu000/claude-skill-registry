---
name: VLM_Expert
description: 实现基于视觉的 AI 对话能力，支持分析图像、描述视觉内容并进行多模态交互。
---

# VLM (Vision Chat) 技能

使 AI 能够理解并响应结合了图像和文本提示的内容。

## 核心功能
- **图像分析**: 识别图片中的物体和场景。
- **多图对比**: 同时分析多张图片。

## CLI 示例
```bash
z-ai vision --prompt "图中有什么？" --image "./photo.jpg"
```