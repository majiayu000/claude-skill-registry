---
name: langchain-rag
description: Build Retrieval Augmented Generation (RAG) systems with LangChain - includes embeddings, vector stores, retrievers, document loaders, and text splitting
language: js
---

# langchain-rag (JavaScript/TypeScript)

## 概述

检索增强生成（RAG）通过从外部知识源获取相关上下文来增强 LLM 响应。RAG 系统在查询时检索文档并使用它们来生成响应，而不是仅依赖训练数据。

**核心概念：**
- **文档加载器（Document Loaders）**：从文件、Web、数据库摄取数据
- **文本分割器（Text Splitters）**：将文档分解为块
- **嵌入（Embeddings）**：将文本转换为向量
- **向量存储（Vector Stores）**：存储和搜索嵌入
- **检索器（Retrievers）**：为查询获取相关文档

## RAG 流水线

1. **索引**：加载 → 分割 → 嵌入 → 存储
2. **检索**：查询 → 嵌入 → 搜索 → 返回文档
3. **生成**：文档 + 查询 → LLM → 响应

## 决策表

### 向量存储选择

| 存储 | 何时使用 | 原因 |
|-------|-------------|-----|
| MemoryVectorStore | 开发、测试 | 内存中、快速、临时 |
| Chroma | 本地生产环境 | 持久化、开源 |
| Pinecone | 云端、可扩展 | 托管、快速、可扩展 |
| Faiss | 高性能 | 快速相似性搜索 |

### 嵌入模型选择

| 模型 | 何时使用 | 维度 |
|-------|-------------|-----------|
| text-embedding-3-small | 成本效益 | 1536 |
| text-embedding-3-large | 最佳质量 | 3072 |
| text-embedding-ada-002 | 旧版 | 1536 |

## 代码示例

### 基本 RAG 设置

```typescript
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "@langchain/classic/vectorstores/memory";
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

// 1. 加载文档（示例：内存中文本）
const docs = [
  { pageContent: "LangChain 是一个用于构建 LLM 应用程序的框架。", metadata: {} },
  { pageContent: "RAG 代表检索增强生成。", metadata: {} },
];

// 2. 分割文档
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 500,
  chunkOverlap: 50,
});
const splits = await splitter.splitDocuments(docs);

// 3. 创建嵌入并存储
const embeddings = new OpenAIEmbeddings({
  model: "text-embedding-3-small",
});

const vectorStore = await MemoryVectorStore.fromDocuments(splits, embeddings);

// 4. 创建检索器
const retriever = vectorStore.asRetriever(4); // 前 4 个结果

// 5. 在 RAG 中使用
const model = new ChatOpenAI({ model: "gpt-4.1" });

const query = "什么是 RAG？";
const relevantDocs = await retriever.invoke(query);

const context = relevantDocs.map(doc => doc.pageContent).join("\n\n");
const response = await model.invoke([
  { role: "system", content: `使用以下上下文回答问题：\n\n${context}` },
  { role: "user", content: query },
]);

console.log(response.content);
```

### 加载网页

```typescript
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";

const loader = new CheerioWebBaseLoader(
  "https://docs.langchain.com/oss/javascript/langchain/agents"
);

const docs = await loader.load();
console.log(`已加载 ${docs.length} 个文档`);
```

### 加载 PDF 文件

```typescript
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";

const loader = new PDFLoader("./document.pdf");
const docs = await loader.load();
```

### 高级文本分割

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,        // 每个块的字符数
  chunkOverlap: 200,      // 上下文连续性的重叠
  separators: ["\n\n", "\n", " ", ""],  // 分割层次结构
});

const splits = await splitter.splitDocuments(docs);
```

### 使用 Chroma（持久化）

```typescript
import { Chroma } from "@langchain/community/vectorstores/chroma";
import { OpenAIEmbeddings } from "@langchain/openai";

const embeddings = new OpenAIEmbeddings();

// 创建并填充
const vectorStore = await Chroma.fromDocuments(
  splits,
  embeddings,
  { collectionName: "my-docs" }
);

// 后续：加载现有的
const vectorStore2 = await Chroma.fromExistingCollection(
  embeddings,
  { collectionName: "my-docs" }
);
```

### 高级检索

```typescript
// 带分数的相似性搜索
const results = await vectorStore.similaritySearchWithScore(query, 5);
for (const [doc, score] of results) {
  console.log(`分数：${score}, 内容：${doc.pageContent}`);
}

// MMR（最大边际相关性）以增加多样性
const retriever = vectorStore.asRetriever({
  searchType: "mmr",
  searchKwargs: { fetchK: 20, lambda: 0.5 },
  k: 5,
});
```

### 元数据过滤

```typescript
// 在创建文档时添加元数据
const docs = [
  {
    pageContent: "Python 编程指南",
    metadata: { language: "python", topic: "programming" }
  },
  {
    pageContent: "JavaScript 教程",
    metadata: { language: "javascript", topic: "programming" }
  },
];

// 使用过滤器搜索
const results = await vectorStore.similaritySearch(
  "programming",
  5,
  { language: "python" }  // 仅 Python 文档
);
```

### RAG 与代理

```typescript
import { createAgent } from "langchain";
import { tool } from "langchain";
import { z } from "zod";

const searchDocs = tool(
  async ({ query }) => {
    const docs = await retriever.invoke(query);
    return docs.map(d => d.pageContent).join("\n\n");
  },
  {
    name: "search_docs",
    description: "搜索文档以获取相关信息",
    schema: z.object({
      query: z.string().describe("搜索查询"),
    }),
  }
);

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchDocs],
});

const result = await agent.invoke({
  messages: [{ role: "user", content: "如何创建代理？" }],
});
```

### 混合搜索（关键词 + 语义）

```typescript
// 结合关键词和向量搜索
import { similarity } from "ml-distance";

async function hybridSearch(query: string, k: number = 5) {
  // 向量搜索
  const vectorResults = await vectorStore.similaritySearch(query, k);

  // 关键词搜索（简单示例）
  const allDocs = await vectorStore.getAllDocuments();
  const keywordResults = allDocs.filter(doc =>
    doc.pageContent.toLowerCase().includes(query.toLowerCase())
  );

  // 结合和去重
  const combined = [...vectorResults, ...keywordResults];
  const unique = Array.from(new Set(combined.map(d => d.pageContent)))
    .map(content => combined.find(d => d.pageContent === content));

  return unique.slice(0, k);
}
```

## 边界

### 您可以配置什么

✅ **块大小/重叠**：控制文档分割
✅ **嵌入模型**：选择质量与成本
✅ **结果数量**：Top-k 检索
✅ **元数据过滤器**：按文档属性过滤
✅ **搜索算法**：相似性、MMR、混合

### 您不能配置什么

❌ **嵌入维度**（每个模型）：由模型固定
❌ **完美的检索**：语义搜索有局限性
❌ **实时文档更新**：需要重新索引

## 注意事项

### 1. 忘记分割文档

```typescript
// ❌ 问题：整个文档太大
await vectorStore.addDocuments(largeDocs);  // 可能达到 token 限制

// ✅ 解决方案：始终先分割
const splits = await splitter.splitDocuments(largeDocs);
await vectorStore.addDocuments(splits);
```

### 2. 块大小太小/太大

```typescript
// ❌ 问题：太小 - 失去上下文
const splitter = new RecursiveCharacterTextSplitter({ chunkSize: 50 });

// ❌ 问题：太大 - 达到限制
const splitter = new RecursiveCharacterTextSplitter({ chunkSize: 10000 });

// ✅ 解决方案：平衡（500-1500 通常很好）
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});
```

### 3. 没有重叠

```typescript
// ❌ 问题：没有重叠 - 上下文在边界处中断
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 0,  // 不好！
});

// ✅ 解决方案：使用重叠（块大小的 10-20%）
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,  // 20%
});
```

### 4. 不持久化向量存储

```typescript
// ❌ 问题：在生产环境中使用 MemoryVectorStore
const vectorStore = await MemoryVectorStore.fromDocuments(docs, embeddings);
// 重启后丢失！

// ✅ 解决方案：使用持久化存储
const vectorStore = await Chroma.fromDocuments(
  docs,
  embeddings,
  { collectionName: "prod-docs" }
);
```

## 文档链接

- [RAG 教程](https://docs.langchain.com/oss/javascript/langchain/rag)
- [文档加载器](https://docs.langchain.com/oss/javascript/integrations/document_loaders/index)
- [文本分割器](https://docs.langchain.com/oss/javascript/integrations/splitters/index)
- [向量存储](https://docs.langchain.com/oss/javascript/integrations/vectorstores/index)
- [嵌入](https://docs.langchain.com/oss/javascript/integrations/text_embedding/openai)
