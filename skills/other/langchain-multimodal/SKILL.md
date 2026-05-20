---
name: langchain-multimodal
description: Work with multimodal inputs/outputs in LangChain - includes images, audio, video, content blocks, and vision capabilities
language: js
---

# langchain-multimodal (JavaScript/TypeScript)

## 概述

多模态支持让您能够处理图像、音频、视频和其他非文本数据。具有多模态功能的模型可以处理和生成这些不同格式的内容。

**核心概念：**
- **内容块（Content Blocks）**：多模态数据的结构化表示
- **视觉（Vision）**：使用 GPT-4V、Claude、Gemini 进行图像理解
- **音频/视频**：新模型中出现的支持
- **标准格式**：跨提供商的内容块结构

## 决策表

### 多模态的模型选择

| 任务 | 推荐模型 | 原因 |
|------|------------------|-----|
| 图像理解 | GPT-4.1、Claude Sonnet、Gemini | 强大的视觉功能 |
| 图像生成 | DALL-E（通过 OpenAI） | 专门用于生成 |
| 文档分析（PDF） | Claude、GPT-4.1 | 处理复杂的布局 |
| 音频转录 | Whisper（OpenAI） | 专门用于音频 |

### 输入方法

| 方法 | 何时使用 | 示例 |
|--------|-------------|---------|
| URL | 公共图像 | `{ type: "image", url: "https://..." }` |
| Base64 | 私有/本地图像 | `{ type: "image", data: "base64..." }` |
| 文件引用 | 提供商文件 API | `{ type: "image", fileId: "..." }` |

## 代码示例

### 基本图像输入（URL）

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "langchain";

const model = new ChatOpenAI({ model: "gpt-4.1" });

const message = new HumanMessage({
  contentBlocks: [
    { type: "text", text: "这张图片里有什么？" },
    {
      type: "image",
      url: "https://example.com/photo.jpg",
    },
  ],
});

const response = await model.invoke([message]);
console.log(response.content);
```

### Base64 图像输入

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "langchain";
import fs from "fs";

const model = new ChatOpenAI({ model: "gpt-4.1" });

// 读取图像并转换为 base64
const imageBuffer = fs.readFileSync("./photo.jpg");
const base64Image = imageBuffer.toString("base64");

const message = new HumanMessage({
  contentBlocks: [
    { type: "text", text: "详细描述这张图片" },
    {
      type: "image",
      data: base64Image,
      mimeType: "image/jpeg",
    },
  ],
});

const response = await model.invoke([message]);
```

### 多张图像

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage } from "langchain";

const model = new ChatOpenAI({ model: "gpt-4.1" });

const message = new HumanMessage({
  contentBlocks: [
    { type: "text", text: "比较这两张图片" },
    { type: "image", url: "https://example.com/image1.jpg" },
    { type: "image", url: "https://example.com/image2.jpg" },
  ],
});

const response = await model.invoke([message]);
```

### PDF 文档分析

```typescript
import { ChatAnthropic } from "@langchain/anthropic";
import { HumanMessage } from "langchain";
import fs from "fs";

const model = new ChatAnthropic({ model: "claude-sonnet-4-5-20250929" });

const pdfBuffer = fs.readFileSync("./document.pdf");
const base64Pdf = pdfBuffer.toString("base64");

const message = new HumanMessage({
  contentBlocks: [
    { type: "text", text: "总结这个 PDF 文档" },
    {
      type: "file",
      data: base64Pdf,
      mimeType: "application/pdf",
    },
  ],
});

const response = await model.invoke([message]);
```

### 音频输入（新兴）

```typescript
// 使用假设的音频支持的示例
const message = new HumanMessage({
  contentBlocks: [
    { type: "text", text: "转录这个音频" },
    {
      type: "audio",
      data: base64Audio,
      mimeType: "audio/mpeg",
    },
  ],
});
```

### 访问多模态输出

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ model: "gpt-4.1" });

const response = await model.invoke("创建一个日落的图像");

// 访问内容块
for (const block of response.contentBlocks) {
  if (block.type === "text") {
    console.log("文本：", block.text);
  } else if (block.type === "image") {
    console.log("图像 URL：", block.url);
    console.log("图像数据：", block.data?.substring(0, 50) + "...");
  }
}
```

### 使用 Claude 的视觉功能

```typescript
import { ChatAnthropic } from "@langchain/anthropic";
import { HumanMessage } from "langchain";

const model = new ChatAnthropic({
  model: "claude-sonnet-4-5-20250929",
});

const message = new HumanMessage({
  contentBlocks: [
    {
      type: "image",
      url: "https://example.com/chart.png",
    },
    {
      type: "text",
      text: "从这个图表中提取所有数据点并格式化为表格",
    },
  ],
});

const response = await model.invoke([message]);
```

### 使用 Gemini 的视觉功能

```typescript
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { HumanMessage } from "langchain";

const model = new ChatGoogleGenerativeAI({
  model: "gemini-2.5-flash",
});

const message = new HumanMessage({
  contentBlocks: [
    { type: "text", text: "这张图片中有什么物体？" },
    { type: "image", url: "https://example.com/scene.jpg" },
  ],
});

const response = await model.invoke([message]);
```

## 边界

### 您可以做什么

✅ **图像 URL**：通过 HTTPS 的公共图像
✅ **Base64 图像**：本地或私有图像
✅ **多张图像**：一起比较、分析
✅ **PDF 文档**：文本提取、分析
✅ **跨提供商格式**：标准内容块

### 您（尚）不能做什么

❌ **所有模型中的图像生成**：限于特定模型
❌ **视频理解**：新兴的、有限的支持
❌ **所有模型中的音频**：特定于模型
❌ **修改图像**：模型分析，不编辑

## 注意事项

### 1. 模型不支持多模态

```typescript
// ❌ 问题：使用仅文本模型
const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
await model.invoke([imageMessage]);  // 错误！

// ✅ 解决方案：使用支持视觉的模型
const model = new ChatOpenAI({ model: "gpt-4.1" });
```

### 2. 错误的内容块格式

```typescript
// ❌ 问题：旧格式
const message = new HumanMessage({
  content: [
    { type: "image_url", image_url: { url: "..." } }  // OpenAI 特定
  ]
});

// ✅ 解决方案：使用标准内容块
const message = new HumanMessage({
  contentBlocks: [
    { type: "image", url: "..." }  // 跨提供商
  ]
});
```

### 3. Base64 缺少 MIME 类型

```typescript
// ❌ 问题：没有 MIME 类型
{ type: "image", data: base64Data }  // 可能失败

// ✅ 解决方案：始终包含 MIME 类型
{ type: "image", data: base64Data, mimeType: "image/jpeg" }
```

### 4. 图像太大

```typescript
// ❌ 问题：图像超过大小限制
const hugeImage = fs.readFileSync("./10mb_image.jpg");
// 模型可能会拒绝

// ✅ 解决方案：首先调整大小或压缩图像
import sharp from "sharp";

const resized = await sharp("./10mb_image.jpg")
  .resize(1024, 1024, { fit: "inside" })
  .jpeg({ quality: 80 })
  .toBuffer();
```

## 文档链接

- [多模态指南](https://docs.langchain.com/oss/javascript/langchain/models)
- [消息和内容块](https://docs.langchain.com/oss/javascript/langchain/messages)
- [OpenAI 视觉](https://docs.langchain.com/oss/javascript/integrations/chat/openai)
- [Anthropic 视觉](https://docs.langchain.com/oss/javascript/integrations/chat/anthropic)
