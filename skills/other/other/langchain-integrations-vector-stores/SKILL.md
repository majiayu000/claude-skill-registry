---
name: langchain-vector-stores
description: LangChain 向量存储集成使用指南，包括 Chroma、Pinecone、FAISS 和内存向量存储
language: js
---

# langchain-vector-stores (JavaScript/TypeScript)

## 概述

向量存储是经过优化的数据库，用于存储和搜索高维向量（嵌入）。它们通过基于向量相似度而非关键字匹配来查找相似文档，从而实现语义搜索。对于 RAG（检索增强生成）系统至关重要。

### 核心概念

- **向量数据库**：用于存储和查询嵌入的专用数据库
- **相似度搜索**：使用向量距离度量（余弦、欧几里得）查找相似文档
- **元数据过滤**：将向量搜索与元数据过滤器结合
- **持久化**：某些向量存储在内存中运行，其他持久化到磁盘/云
- **扩展性**：不同的存储具有不同的可扩展性特征

## 向量存储选择决策表

| 向量存储 | 最适用于 | 包 | 持久化 | 可扩展性 | 主要特性 |
|--------------|----------|---------|-------------|-------------|--------------|
| **FAISS** | 本地、高性能 | `@langchain/community` | 磁盘 | 中等 | 快速、支持 CPU/GPU、本地 |
| **Chroma** | 开发、简单 | `@langchain/community` | 磁盘 | 中等 | 易于设置、本地优先、Python API |
| **Pinecone** | 生产环境、托管 | `@langchain/pinecone` | 云 | 高 | 完全托管、自动扩展、免运维 |
| **Memory** | 测试、原型 | `langchain/vectorstores/memory` | 仅内存 | 低 | 简单、无设置、临时 |
| **Weaviate** | GraphQL、混合搜索 | `@langchain/weaviate` | 云/自托管 | 高 | GraphQL、混合搜索、模块化 |
| **Qdrant** | 高性能、过滤 | `@langchain/qdrant` | 云/自托管 | 高 | 快速、高级过滤、基于 Rust |
| **Supabase** | PostgreSQL 用户 | `@langchain/community` | 云/自托管 | 高 | PostgreSQL 扩展、熟悉的工具 |

### 何时选择各存储

**选择 FAISS 如果：**
- 您需要高性能的本地向量搜索
- 您希望避免外部依赖
- 您有大量向量（数百万）需要快速搜索

**选择 Chroma 如果：**
- 您想要简单的本地开发
- 您需要易于持久化而无需复杂设置
- 您正在构建原型或小型应用程序

**选择 Pinecone 如果：**
- 您正在构建生产应用程序
- 您希望零运维开销
- 您需要自动扩展和高可用性

**选择内存向量存储如果：**
- 您正在测试或原型开发
- 数据持久化不是必需的
- 您想要尽可能简单的设置

**选择 Weaviate/Qdrant 如果：**
- 您需要高级过滤和混合搜索
- 您希望在部署上有灵活性（云或自托管）
- 您需要大规模的高性能

## 代码示例

### 内存向量存储（最简单）

```typescript
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

// 内存向量存储 - 适合测试
const vectorStore = new MemoryVectorStore(new OpenAIEmbeddings());

// 添加文档
await vectorStore.addDocuments([
  { pageContent: "LangChain is a framework for LLM apps", metadata: { source: "docs" } },
  { pageContent: "Vector stores enable semantic search", metadata: { source: "docs" } },
  { pageContent: "Paris is the capital of France", metadata: { source: "wiki" } },
]);

// 相似度搜索
const results = await vectorStore.similaritySearch("What is LangChain?", 2);
console.log(results);

// 带分数的搜索
const resultsWithScore = await vectorStore.similaritySearchWithScore("LangChain", 2);
resultsWithScore.forEach(([doc, score]) => {
  console.log(`Score: ${score}, Content: ${doc.pageContent}`);
});
```

### FAISS 向量存储

```typescript
import { FaissStore } from "@langchain/community/vectorstores/faiss";
import { OpenAIEmbeddings } from "@langchain/openai";

const embeddings = new OpenAIEmbeddings();

// 从文档创建
const vectorStore = await FaissStore.fromDocuments(
  [
    { pageContent: "Document 1 content", metadata: { id: 1 } },
    { pageContent: "Document 2 content", metadata: { id: 2 } },
  ],
  embeddings
);

// 搜索
const results = await vectorStore.similaritySearch("query", 3);

// 保存到磁盘
await vectorStore.save("./faiss_index");

// 从磁盘加载
const loadedStore = await FaissStore.load("./faiss_index", embeddings);
```

### Chroma 向量存储

```typescript
import { Chroma } from "@langchain/community/vectorstores/chroma";
import { OpenAIEmbeddings } from "@langchain/openai";

// 需要运行 Chroma 服务器：docker run -p 8000:8000 chromadb/chroma
const vectorStore = await Chroma.fromDocuments(
  [
    { pageContent: "Text 1", metadata: { category: "A" } },
    { pageContent: "Text 2", metadata: { category: "B" } },
  ],
  new OpenAIEmbeddings(),
  {
    collectionName: "my-collection",
    url: "http://localhost:8000", // Chroma 服务器 URL
  }
);

// 带元数据过滤器的搜索
const results = await vectorStore.similaritySearch("query", 3, {
  category: "A"
});

// 删除集合
await vectorStore.delete({ collectionName: "my-collection" });
```

### Pinecone 向量存储

```typescript
import { PineconeStore } from "@langchain/pinecone";
import { Pinecone } from "@pinecone-database/pinecone";
import { OpenAIEmbeddings } from "@langchain/openai";

// 初始化 Pinecone 客户端
const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY,
});

const pineconeIndex = pinecone.Index("my-index");

// 创建向量存储
const vectorStore = await PineconeStore.fromDocuments(
  [
    { pageContent: "Content 1", metadata: { topic: "tech" } },
    { pageContent: "Content 2", metadata: { topic: "science" } },
  ],
  new OpenAIEmbeddings(),
  {
    pineconeIndex,
    maxConcurrency: 5,
  }
);

// 带元数据过滤器的搜索
const results = await vectorStore.similaritySearch("query", 3, {
  topic: "tech"
});

// 作为检索器使用
const retriever = vectorStore.asRetriever({
  k: 5,
  searchType: "similarity",
});
const docs = await retriever.getRelevantDocuments("query");
```

### 增量添加文档

```typescript
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

const vectorStore = new MemoryVectorStore(new OpenAIEmbeddings());

// 一次或批量添加文档
await vectorStore.addDocuments([
  { pageContent: "Document 1", metadata: {} },
]);

// 稍后添加更多
await vectorStore.addDocuments([
  { pageContent: "Document 2", metadata: {} },
  { pageContent: "Document 3", metadata: {} },
]);

// 或从文本添加
await vectorStore.addTexts(
  ["Text 1", "Text 2"],
  [{ source: "A" }, { source: "B" }]
);
```

### 作为检索器使用

```typescript
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

const vectorStore = await MemoryVectorStore.fromDocuments(
  documents,
  new OpenAIEmbeddings()
);

// 转换为检索器
const retriever = vectorStore.asRetriever({
  k: 4, // 返回前 4 个结果
  searchType: "similarity", // 或 "mmr" 用于最大边际相关性
});

// 在链中使用
import { ChatOpenAI } from "@langchain/openai";
import { createRetrievalChain } from "langchain/chains/retrieval";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";
import { ChatPromptTemplate } from "@langchain/core/prompts";

const llm = new ChatOpenAI();
const prompt = ChatPromptTemplate.fromTemplate(`
Answer based on context:
{context}

Question: {input}
`);

const combineDocsChain = await createStuffDocumentsChain({ llm, prompt });
const chain = await createRetrievalChain({
  retriever,
  combineDocsChain,
});

const result = await chain.invoke({ input: "What is LangChain?" });
```

### 最大边际相关性 (MMR)

```typescript
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

const vectorStore = await MemoryVectorStore.fromTexts(
  ["text1", "text2", "text3"],
  [{}, {}, {}],
  new OpenAIEmbeddings()
);

// MMR 平衡相关性和多样性
const results = await vectorStore.maxMarginalRelevanceSearch("query", {
  k: 3,
  fetchK: 10, // 获取 10 个候选，返回 3 个多样化结果
  lambda: 0.5, // 0 = 最大多样性，1 = 最大相关性
});
```

## 边界

### Agent 能够做的

✅ **初始化向量存储**
- 设置任何支持的向量存储
- 使用嵌入和连接详情进行配置

✅ **添加和查询文档**
- 添加带元数据的文档
- 执行相似度搜索
- 使用元数据过滤器

✅ **持久化和加载**
- 将向量存储保存到磁盘（FAISS、Chroma）
- 加载现有向量存储
- 管理集合

✅ **作为检索器使用**
- 将向量存储转换为检索器
- 与链和 Agent 集成
- 配置搜索参数（k、过滤器等）

✅ **选择适当的存储**
- 根据规模、性能、持久化需求进行选择
- 以最小的代码更改切换存储

### Agent 不能做的

❌ **混合来自不同模型的嵌入**
- 不能在同一向量存储中使用不同的嵌入模型
- 必须使用一致的嵌入

❌ **绕过提供程序限制**
- 不能超过 Pinecone 索引大小限制
- 不能绕过免费层限制

❌ **在创建后修改向量维度**
- 创建后无法更改嵌入维度
- 必须使用新嵌入重新创建存储

❌ **在没有正确设置的情况下查询**
- 不能在服务器未运行时使用 Chroma
- 不能在没有 API 密钥和索引的情况下使用 Pinecone

## 注意事项

### 1. **嵌入模型一致性**

```typescript
// ❌ 错误：为索引和查询使用不同的嵌入
const store1 = await MemoryVectorStore.fromDocuments(
  docs,
  new OpenAIEmbeddings({ model: "text-embedding-3-small" })
);

const results = await store1.similaritySearch("query"); // 使用相同的嵌入 ✓

// 但如果重新创建：
const store2 = new MemoryVectorStore(
  new OpenAIEmbeddings({ model: "text-embedding-ada-002" }) // 不同!
);
// 查询将无法正常工作!

// ✅ 正确：保持嵌入实例
const embeddings = new OpenAIEmbeddings({ model: "text-embedding-3-small" });
const store = await MemoryVectorStore.fromDocuments(docs, embeddings);
// 始终使用相同的嵌入实例
```

**修复方法**：为创建和查询使用相同的嵌入模型实例。

### 2. **Chroma 服务器必须运行**

```typescript
// ❌ Chroma 未运行
import { Chroma } from "@langchain/community/vectorstores/chroma";

const store = await Chroma.fromDocuments(docs, embeddings, {
  url: "http://localhost:8000"
});
// 错误：连接被拒绝!

// ✅ 先启动 Chroma
// 终端：docker run -p 8000:8000 chromadb/chroma
// 或：chroma run --path ./chroma_data

const store = await Chroma.fromDocuments(docs, embeddings, {
  url: "http://localhost:8000"
}); // 可以工作!
```

**修复方法**：在创建向量存储之前确保 Chroma 服务器正在运行。

### 3. **Pinecone 索引必须存在**

```typescript
// ❌ 索引不存在
import { Pinecone } from "@pinecone-database/pinecone";

const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY });
const index = pinecone.Index("nonexistent-index"); // 不会创建索引!

// ✅ 先创建索引
// 在 Pinecone 控制台或通过 API 执行此操作
const pinecone = new Pinecone({ apiKey: process.env.PINECONE_API_KEY });

// 检查索引是否存在，如需要则创建
const indexList = await pinecone.listIndexes();
if (!indexList.indexes?.some(idx => idx.name === "my-index")) {
  await pinecone.createIndex({
    name: "my-index",
    dimension: 1536, // 必须匹配嵌入维度
    metric: "cosine",
    spec: { serverless: { cloud: "aws", region: "us-east-1" } }
  });
}

const index = pinecone.Index("my-index");
```

**修复方法**：在使用前创建 Pinecone 索引。

### 4. **FAISS 保存/加载路径问题**

```typescript
// ❌ 相对路径问题
await vectorStore.save("./index"); // 可能根据当前工作目录失败

// ✅ 使用绝对路径或明确指定
import path from "path";
const indexPath = path.join(process.cwd(), "data", "faiss_index");
await vectorStore.save(indexPath);

// 使用相同路径加载
const loadedStore = await FaissStore.load(indexPath, embeddings);
```

**修复方法**：使用绝对路径或注意当前工作目录。

### 5. **内存向量存储是临时的**

```typescript
// ❌ 期望持久化
const vectorStore = new MemoryVectorStore(embeddings);
await vectorStore.addDocuments(docs);
// 应用重启...
// 所有数据丢失!

// ✅ 在生产中使用持久化存储
import { FaissStore } from "@langchain/community/vectorstores/faiss";

const vectorStore = await FaissStore.fromDocuments(docs, embeddings);
await vectorStore.save("./faiss_index"); // 持久化到磁盘
```

**修复方法**：对于持久化数据，使用 FAISS、Chroma 或云存储（Pinecone）。

### 6. **元数据过滤语法各异**

```typescript
// 不同的存储有不同的过滤语法
// Pinecone
const pineconeResults = await pineconeStore.similaritySearch("query", 3, {
  category: "tech" // 简单的键值
});

// Chroma
const chromaResults = await chromaStore.similaritySearch("query", 3, {
  where: { category: "tech" } // 嵌套结构
});

// 查看每个存储的文档以了解过滤语法!
```

**修复方法**：阅读特定向量存储的文档以了解过滤语法。

### 7. **维度不匹配**

```typescript
// ❌ 使用错误的维度创建 Pinecone 索引
await pinecone.createIndex({
  name: "my-index",
  dimension: 1536, // OpenAI ada-002 维度
});

// 但使用不同的嵌入!
const store = await PineconeStore.fromDocuments(
  docs,
  new OpenAIEmbeddings({ model: "text-embedding-3-small", dimensions: 512 }),
  { pineconeIndex }
); // 错误：维度不匹配!

// ✅ 匹配维度
const embeddings = new OpenAIEmbeddings({ model: "text-embedding-3-small" });
// 默认为 1536，匹配 Pinecone 索引
```

**修复方法**：确保向量存储维度配置与嵌入维度匹配。

## 相关资源

### 官方文档
- [LangChain JS 向量存储](https://js.langchain.com/docs/integrations/vectorstores/)
- [FAISS](https://js.langchain.com/docs/integrations/vectorstores/faiss)
- [Chroma](https://js.langchain.com/docs/integrations/vectorstores/chroma)
- [Pinecone](https://js.langchain.com/docs/integrations/vectorstores/pinecone)
- [内存向量存储](https://js.langchain.com/docs/integrations/vectorstores/memory)

### 提供商文档
- [FAISS 库](https://github.com/facebookresearch/faiss)
- [Chroma](https://docs.trychroma.com/)
- [Pinecone](https://docs.pinecone.io/)
- [Weaviate](https://weaviate.io/developers/weaviate)
- [Qdrant](https://qdrant.tech/documentation/)

### 包安装
```bash
# 社区包（包括 FAISS、Chroma 等）
npm install @langchain/community

# Pinecone
npm install @langchain/pinecone @pinecone-database/pinecone

# Weaviate
npm install @langchain/weaviate weaviate-ts-client

# Qdrant
npm install @langchain/qdrant @qdrant/js-client-rest
```
