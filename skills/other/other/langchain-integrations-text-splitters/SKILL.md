---
name: langchain-text-splitters
description: 使用 LangChain 中的文本分割器集成指南，包括递归、字符和语义分割器
language: js
---

# langchain-text-splitters (JavaScript/TypeScript)

## 概述

文本分割器将大型文档分成更小的块，这些块适合模型上下文窗口并实现有效检索。适当的分块对于 RAG 系统性能至关重要——块必须足够小以便检索，但也必须足够大以保留上下文。

### 核心概念

- **块大小**：每个文本块的目标大小（以字符或令牌为单位）
- **块重叠**：块之间重叠的字符/令牌数量（保留上下文）
- **分隔符**：用于分割文本的字符（换行符、句号、空格）
- **元数据**：在分割期间保留和丰富（包括 start_index）

## 分割器选择决策表

| 分割器 | 最适合 | 包 | 主要特性 |
|----------|----------|---------|--------------|
| **RecursiveCharacterTextSplitter** | 通用 | `@langchain/textsplitters` | 层次化分割、保留结构 |
| **CharacterTextSplitter** | 简单分割 | `@langchain/textsplitters` | 按单个分隔符分割 |
| **TokenTextSplitter** | 令牌感知分割 | `@langchain/textsplitters` | 计算实际令牌，而非字符 |
| **MarkdownTextSplitter** | Markdown 文档 | `@langchain/textsplitters` | 保留 markdown 结构 |
| **RecursiveJsonSplitter** | JSON 数据 | `@langchain/textsplitters` | 分割 JSON 同时保留结构 |

### 何时选择每个分割器

**选择 RecursiveCharacterTextSplitter 如果：**
- 您正在处理一般文本（默认选择）
- 您想保留自然文本结构
- 您需要平衡的块

**选择 TokenTextSplitter 如果：**
- 您需要精确的令牌计数以进行模型限制
- 对于您的用例，字符计数不可靠

**选择 MarkdownTextSplitter 如果：**
- 您正在处理 markdown 文档
- 您想保留标题和结构

## 代码示例

### RecursiveCharacterTextSplitter（推荐）

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

// 基本用法
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,      // 每个块的目标字符数
  chunkOverlap: 200,    // 块之间的重叠
});

const text = "长文档文本在这里...";
const chunks = await splitter.splitText(text);

console.log(`创建了 ${chunks.length} 个块`);
chunks.forEach((chunk, i) => {
  console.log(`块 ${i + 1}：${chunk.length} 个字符`);
});

// 分割文档（保留元数据）
import { Document } from "@langchain/core/documents";

const docs = [
  new Document({
    pageContent: "长文本...",
    metadata: { source: "doc1.pdf", page: 1 }
  })
];

const splitDocs = await splitter.splitDocuments(docs);
// 元数据被保留并丰富了 loc.lines
```

### RecursiveCharacterTextSplitter 的工作原理

```typescript
// 按顺序尝试在这些分隔符上分割：
// 1. "\n\n"（双换行 - 段落）
// 2. "\n"（单换行）
// 3. " "（空格）
// 4. ""（如果需要，逐字符）

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
  separators: ["\n\n", "\n", " ", ""], // 默认，可以自定义
});

// 这比简单分割更好地保留自然文本结构
```

### CharacterTextSplitter（简单）

```typescript
import { CharacterTextSplitter } from "@langchain/textsplitters";

// 按单个分隔符分割
const splitter = new CharacterTextSplitter({
  separator: "\n\n",    // 在双换行符上分割
  chunkSize: 1000,
  chunkOverlap: 200,
});

const chunks = await splitter.splitText(text);
```

### TokenTextSplitter（令牌感知）

```typescript
import { TokenTextSplitter } from "@langchain/textsplitters";

// 基于实际令牌计数分割
const splitter = new TokenTextSplitter({
  chunkSize: 512,       // 令牌数，而非字符
  chunkOverlap: 50,
  encodingName: "cl100k_base", // OpenAI 的编码
});

const chunks = await splitter.splitText(text);

// 适合精确的模型上下文窗口管理
// 1 个令牌 ≈ 4 个字符（英文文本），但会有变化
```

### MarkdownTextSplitter

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

// 分割 markdown 同时保留结构
const splitter = RecursiveCharacterTextSplitter.fromLanguage("markdown", {
  chunkSize: 1000,
  chunkOverlap: 200,
});

const markdown = `
# 标题 1

标题 1 下的一些内容。

## 标题 2

标题 2 下的内容。
`;

const chunks = await splitter.splitText(markdown);
// 尽量将标题与其内容保持在一起
```

### 分割长文档

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";

// 加载 PDF
const loader = new PDFLoader("large-document.pdf");
const docs = await loader.load();

// 分割成可管理的块
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});

const splitDocs = await splitter.splitDocuments(docs);

console.log(`${docs.length} 页被分割成 ${splitDocs.length} 个块`);

// 每个块都保留来源元数据
splitDocs.forEach(chunk => {
  console.log(chunk.metadata); // 包括原始页码
});
```

### 代码分割

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

// 分割代码同时保留结构
const jsSplitter = RecursiveCharacterTextSplitter.fromLanguage("js", {
  chunkSize: 500,
  chunkOverlap: 50,
});

const pythonSplitter = RecursiveCharacterTextSplitter.fromLanguage("python", {
  chunkSize: 500,
  chunkOverlap: 50,
});

// 使用特定语言的分隔符（函数、类等）
```

### 自定义分隔符

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

// 自定义分割逻辑
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 100,
  separators: [
    "\n\n\n",  // 三换行符（部分中断）
    "\n\n",    // 双换行符（段落）
    "\n",      // 单换行符
    ". ",      // 句子
    " ",       // 单词
    "",        // 字符
  ],
});
```

### 与向量存储集成分割

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";

// 完整的 RAG 管道
const loader = new CheerioWebBaseLoader("https://docs.example.com");
const docs = await loader.load();

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});

const splitDocs = await splitter.splitDocuments(docs);

const vectorStore = await MemoryVectorStore.fromDocuments(
  splitDocs,
  new OpenAIEmbeddings()
);

// 现在可以进行语义搜索
const results = await vectorStore.similaritySearch("query", 4);
```

## 边界

### 代理可以做什么

✅ **智能分割文本**
- 使用递归分割保留结构
- 配置块大小和重叠
- 选择适当的分隔符

✅ **处理各种格式**
- 纯文本、markdown、代码
- 带元数据的文档
- JSON 和结构化数据

✅ **针对用例优化**
- 平衡块大小与上下文
- 调整重叠以保持连续性
- 对模型使用基于令牌的分割

✅ **与管道集成**
- 与加载器和向量存储组合
- 通过分割保留元数据

### 代理不能做什么

❌ **保证语义边界**
- 分割器使用启发式方法，而非完美的语义理解
- 在边缘情况下可能在句子中间分割

❌ **完美估计令牌**
- 基于字符的分割器近似令牌
- 使用 TokenTextSplitter 进行精确计数

❌ **不丢失一些上下文的情况下分割**
- 即使有重叠，某些上下文也可能丢失
- 块大小与上下文之间的权衡

## 常见陷阱

### 1. **块大小与令牌限制**

```typescript
// ❌ 字符计数 != 令牌计数
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 4000,  // 字符
});
// GPT-3.5 有 4096 个令牌限制，这可能会超过！

// ✅ 使用 TokenTextSplitter 进行精确的令牌计数
import { TokenTextSplitter } from "@langchain/textsplitters";

const splitter = new TokenTextSplitter({
  chunkSize: 4000,  // 实际令牌
  encodingName: "cl100k_base",
});
```

**修复**：当令牌精度很重要时，使用 TokenTextSplitter。

### 2. **太小的块丢失上下文**

```typescript
// ❌ 块太小
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 100,    // 非常小
  chunkOverlap: 0,   // 无重叠
});
// 块缺乏足够的上下文以进行良好的检索

// ✅ 适当的块大小与重叠
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,   // 好的大小
  chunkOverlap: 200, // 20% 重叠
});
```

**修复**：对于大多数情况，使用 500-2000 个字符并带有 10-20% 的重叠。

### 3. **零重叠破坏连续性**

```typescript
// ❌ 无重叠
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 0,  // 边界处的信息可能丢失
});

// ✅ 使用重叠保留上下文
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,  // 20% 重叠是一个好的默认值
});
```

**修复**：始终使用重叠（通常是块大小的 10-20%）。

### 4. **元数据未保留**

```typescript
// ❌ 使用 splitText 丢失元数据
const chunks = await splitter.splitText(documentText);
// 没有元数据！

// ✅ 使用 splitDocuments 保留元数据
const docs = [new Document({
  pageContent: documentText,
  metadata: { source: "file.pdf" }
})];
const chunks = await splitter.splitDocuments(docs);
// 元数据被保留！
```

**修复**：使用 `splitDocuments()` 而不是 `splitText()` 来保留元数据。

## 链接和资源

### 官方文档
- [LangChain JS 文本分割器](https://js.langchain.com/docs/integrations/text_splitters/)
- [RecursiveCharacterTextSplitter](https://js.langchain.com/docs/modules/data_connection/document_transformers/)

### 包安装
```bash
npm install @langchain/textsplitters
```
