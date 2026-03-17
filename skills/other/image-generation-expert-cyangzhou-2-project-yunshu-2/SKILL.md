---
name: Image_Generation_Expert
description: 实现 AI 图像生成能力，支持根据文本描述创建高质量图像。
---

# 图像生成技能

根据文本提示词创建视觉内容。

## 支持尺寸
- 1024x1024 (正方形)
- 768x1344 (人像)
- 1344x768 (风景)

## 代码实现示例
```javascript
const response = await zai.images.generations.create({
  prompt: '阳光下的猫咪',
  size: '1024x1024'
});
```