---
name: gemini-image
description: 当用户想要生成图片、画图、绘画、创建图像、AI作画时使用此 Skill。支持文生图和图生图。
---

# Gemini 图像生成

当用户表达画图意图时（如"画一个..."、"生成图片..."、"帮我创作..."），使用此 Skill。

## 调用步骤

### 1. 读取配置
- 读取 `config/secrets.md` 获取 API Key

### 2. 构造 prompt

| 模式 | prompt 格式 | 示例 |
|-----|------------|------|
| 文生图 | `描述文字` | `一只可爱的橘猫` |
| 图生图 | `图片URL 描述文字` | `https://xxx.jpg 画类似风格` |
| 多图参考 | `URL1 URL2 描述文字` | `https://a.jpg https://b.jpg 融合两张图` |

图生图需先上传图片，参考 `tips/image-upload.md`。

### 3. 调用 API

```bash
curl -s -X POST "https://api.apicore.ai/v1/images/generations" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "模型名称",
    "prompt": "提示词",
    "size": "尺寸比例",
    "n": 1
  }'
```

### 4. 返回结果

从响应中提取 `data[0].url` 返回给用户。

## 参考文档

- `tips/image-upload.md` - 图片上传方法
- `tips/chinese-text.md` - 中文文字处理技巧
