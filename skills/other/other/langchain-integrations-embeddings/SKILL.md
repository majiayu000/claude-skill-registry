---
name: langchain-embeddings
description: 使用 LangChain 中的嵌入模型集成指南，包括 OpenAI、Azure 和本地嵌入
language: js
---

# langchain-embeddings (JavaScript/TypeScript)

## 概述

嵌入模型将文本转换为捕获语义含义的数值向量表示。这些向量支持语义搜索、相似性比较，并且是使用向量数据库构建 RAG（检索增强生成）系统的关键。

### 核心概念

- **嵌入**：编码语义含义的密集向量文本表示
- **向量维度**：不同模型产生不同大小的向量（例如，OpenAI 为 1536，一些开源模型为 768）
- **相似性搜索**：通过比较向量距离查找相似文本（余弦相似性、欧几里得距离）
- **批处理**：高效地一次嵌入多个文本
- **用例**：语义搜索、文档检索、聚类、推荐系统

## 提供商选择决策表

| 提供商 | 最适合 | 模型示例 | 维度 | 包 | 主要特性 |
|----------|----------|----------------|------------|---------|--------------|
| **OpenAI** | 通用、高质量 | text-embedding-3-small、text-embedding-3-large、text-embedding-ada-002 | 1536、3072 | `@langchain/openai` | 高质量、可靠、灵活的维度 |
| **Azure OpenAI** | 企业、合规性 | text-embedding-ada-002 (Azure) | 1536 | `@langchain/openai` | 企业 SLA、数据驻留 |
| **Cohere** | 多语言、搜索优化 | embed-english-v3.0、embed-multilingual-v3.0 | 1024 | `@langchain/cohere` | 搜索/聚类模式、多语言 |
| **HuggingFace** | 开源、可定制 | all-MiniLM-L6-v2、BGE 模型 | 可变 | `@langchain/community` | 免费、本地推理、许多模型 |
| **Google** | GCP 集成 | textembedding-gecko | 768 | `@langchain/google-genai` | GCP 生态系统、多模态 |
| **Ollama** | 本地、隐私 | llama2、mistral、nomic-embed-text | 可变 | `@langchain/ollama` | 完全本地、无 API 成本、隐私 |

### 何时选择每个提供商

**选择 OpenAI 如果：**
- 您需要生产环境的高质量嵌入
- 您想要可靠、快速的基于 API 的嵌入
- 对于您的用例来说成本合理（每 100 万令牌约 0.13 美元）

**选择 Azure OpenAI 如果：**
- 您需要企业支持和 SLA
- 数据合规性/驻留至关重要
- 您已经在使用 Azure 基础设施

**选择 Cohere 如果：**
- 您需要多语言嵌入
- 您想要针对搜索与聚类优化的嵌入
- 您需要具有竞争力的定价

**选择 HuggingFace 如果：**
- 您想要使用开源模型
- 您需要特定的模型特征
- 您想要在本地或自己的基础设施上运行推理

**选择 Ollama 如果：**
- 隐私至关重要（完全本地）
- 您希望设置后零 API 成本
- 您有足够的本地计算资源

## 代码示例

### OpenAI 嵌入

```typescript
import { OpenAIEmbeddings } from "@langchain/openai";

// 基本初始化
const embeddings = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small",
  openAIApiKey: process.env.OPENAI_API_KEY, // 如果在 env 中设置则可选
});

// 嵌入单个查询
const queryEmbedding = await embeddings.embedQuery(
  "法国的首都是什么？"
);
console.log(`向量维度：${queryEmbedding.length}`);
console.log(`前几个值：${queryEmbedding.slice(0, 5)}`);

// 嵌入多个文档
const documents = [
  "巴黎是法国的首都。",
  "伦敦是英国的首都。",
  "柏林是德国的首都。",
];
const docEmbeddings = await embeddings.embedDocuments(documents);
console.log(`嵌入了 ${docEmbeddings.length} 个文档`);

// 使用具有自定义维度的较新模型
const smallEmbeddings = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small",
  dimensions: 512, // 从默认的 1536 减少以提高效率
});
```

### Azure OpenAI 嵌入

```typescript
import { AzureOpenAIEmbeddings } from "@langchain/openai";

const embeddings = new AzureOpenAIEmbeddings({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiInstanceName: process.env.AZURE_OPENAI_API_INSTANCE_NAME,
  azureOpenAIApiEmbeddingsDeploymentName: "text-embedding-ada-002",
  azureOpenAIApiVersion: "2024-02-01",
});

const embedding = await embeddings.embedQuery("你好世界");
```

### HuggingFace 嵌入（本地）

```typescript
import { HuggingFaceTransformersEmbeddings } from "@langchain/community/embeddings/hf_transformers";

// 使用 Transformers.js 在本地运行嵌入
const embeddings = new HuggingFaceTransformersEmbeddings({
  modelName: "Xenova/all-MiniLM-L6-v2",
});

const embedding = await embeddings.embedQuery("这在本地运行！");
```

### Ollama 嵌入（本地）

```typescript
import { OllamaEmbeddings } from "@langchain/ollama";

// 需要在本地运行 Ollama：ollama pull nomic-embed-text
const embeddings = new OllamaEmbeddings({
  model: "nomic-embed-text",
  baseUrl: "http://localhost:11434", // 默认 Ollama URL
});

const embedding = await embeddings.embedQuery("完全本地嵌入");
```

### Cohere 嵌入

```typescript
import { CohereEmbeddings } from "@langchain/cohere";

const embeddings = new CohereEmbeddings({
  apiKey: process.env.COHERE_API_KEY,
  model: "embed-english-v3.0",
  inputType: "search_query", // 或 "search_document"、"classification"、"clustering"
});

const queryEmbedding = await embeddings.embedQuery("搜索查询");
const docEmbeddings = await embeddings.embedDocuments(["doc1", "doc2"]);
```

### 计算相似性

```typescript
import { OpenAIEmbeddings } from "@langchain/openai";

const embeddings = new OpenAIEmbeddings();

// 嵌入查询和文档
const query = "什么是机器学习？";
const docs = [
  "机器学习是 AI 的一个分支",
  "巴黎是法国的首都",
  "神经网络在深度学习中使用",
];

const queryVec = await embeddings.embedQuery(query);
const docVecs = await embeddings.embedDocuments(docs);

// 计算余弦相似性
function cosineSimilarity(vecA: number[], vecB: number[]): number {
  const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
  const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
  const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

// 查找最相似的文档
const similarities = docVecs.map((docVec) =>
  cosineSimilarity(queryVec, docVec)
);
console.log("相似性：", similarities);
const mostSimilarIdx = similarities.indexOf(Math.max(...similarities));
console.log("最相似的文档：", docs[mostSimilarIdx]);
```

### 批处理以提高效率

```typescript
import { OpenAIEmbeddings } from "@langchain/openai";

const embeddings = new OpenAIEmbeddings({
  batchSize: 512, // OpenAI 允许在一个请求中最多 2048 个
});

// 高效地嵌入大文档集
const largeDocSet = Array.from({ length: 1000 }, (_, i) =>
  `文档 ${i}：一些内容在这里`
);

const docEmbeddings = await embeddings.embedDocuments(largeDocSet);
console.log(`批量嵌入了 ${docEmbeddings.length} 个文档`);
```

## 边界

### 代理可以做什么

✅ **初始化嵌入模型**
- 设置 OpenAI、Azure、Cohere、HuggingFace 或 Ollama 嵌入
- 配置 API 密钥和模型参数

✅ **嵌入文本内容**
- 使用 `embedQuery()` 嵌入单个查询
- 使用 `embedDocuments()` 嵌入多个文档
- 高效地处理大批量

✅ **将嵌入与向量存储一起使用**
- 将嵌入传递给向量存储构造函数
- 启用语义搜索功能

✅ **选择适当的模型**
- 根据质量、成本、延迟要求选择
- 对隐私问题使用本地模型

✅ **针对用例优化**
- 调整批量大小以提高效率
- 使用较小的维度以降低成本/存储

### 代理不能做什么

❌ **任意修改嵌入维度**
- 无法更改超出模型支持的维度
- text-embedding-3-* 模型支持自定义维度，旧模型不支持

❌ **混合来自不同模型的嵌入**
- 无法直接比较来自不同模型的嵌入
- 必须在相似性搜索中对所有嵌入使用相同模型

❌ **超过 API 速率限制**
- 无法绕过提供商速率限制
- 必须为大规模操作实施速率限制

❌ **在没有适当身份验证的情况下生成嵌入**
- 无法在没有有效 API 密钥的情况下使用云提供商
- 无法在没有适当凭据的情况下访问模型

## 常见陷阱

### 1. **模型一致性至关重要**

```typescript
// ❌ 错误：使用不同的模型
const embeddings1 = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small"
});
const embeddings2 = new OpenAIEmbeddings({
  modelName: "text-embedding-ada-002"
});

const queryVec = await embeddings1.embedQuery("query");
const docVec = await embeddings2.embedQuery("document");
// 相似性比较将毫无意义！

// ✅ 正确：对所有内容使用相同模型
const embeddings = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small"
});
const queryVec = await embeddings.embedQuery("query");
const docVec = await embeddings.embedQuery("document");
// 现在相似性有意义
```

**修复**：始终对要比较的所有文本使用相同的嵌入模型。

### 2. **批量大小限制**

```typescript
// ❌ 文档太多可能导致 API 错误
const embeddings = new OpenAIEmbeddings();
const hugeDocs = Array(5000).fill("text");
await embeddings.embedDocuments(hugeDocs); // 可能失败！

// ✅ 配置适当的批量大小
const embeddings = new OpenAIEmbeddings({
  batchSize: 512, // OpenAI 限制是 2048，使用较小的以确保安全
});
await embeddings.embedDocuments(hugeDocs); // 自动处理批量处理
```

**修复**：为提供商设置适当的 `batchSize` 参数。

### 3. **环境变量中的 API 密钥**

```typescript
// ❌ 硬编码 API 密钥
const embeddings = new OpenAIEmbeddings({
  openAIApiKey: "sk-...", // 永远不要提交这个！
});

// ✅ 使用环境变量
const embeddings = new OpenAIEmbeddings({
  openAIApiKey: process.env.OPENAI_API_KEY,
});

// ✅ 更好：自动检测
const embeddings = new OpenAIEmbeddings();
// 自动从环境读取 OPENAI_API_KEY
```

**修复**：使用环境变量存储 API 密钥。

### 4. **文本长度限制**

```typescript
// ❌ 文本太长
const embeddings = new OpenAIEmbeddings();
const veryLongText = "...".repeat(100000);
await embeddings.embedQuery(veryLongText); // 会失败！

// ✅ 首先分块长文本
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 8000, // OpenAI 限制约为 8191 个令牌
});
const chunks = await splitter.splitText(veryLongText);
const embeddings = await embeddings.embedDocuments(chunks);
```

**修复**：在嵌入之前将长文本分块。大多数模型有 8k 令牌限制。

### 5. **本地模型设置**

```typescript
// ❌ Ollama 未运行
import { OllamaEmbeddings } from "@langchain/ollama";
const embeddings = new OllamaEmbeddings({ model: "nomic-embed-text" });
await embeddings.embedQuery("test"); // 连接错误！

// ✅ 确保 Ollama 正在运行并已拉取模型
// 终端：
// ollama pull nomic-embed-text
// ollama serve

const embeddings = new OllamaEmbeddings({ model: "nomic-embed-text" });
await embeddings.embedQuery("test"); // 有效！
```

**修复**：对于本地模型，确保服务正在运行并已下载模型。

### 6. **Azure 配置复杂性**

```typescript
// ❌ 缺少必填字段
const embeddings = new AzureOpenAIEmbeddings({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
});

// ✅ 所有必填字段
const embeddings = new AzureOpenAIEmbeddings({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiInstanceName: "my-instance",
  azureOpenAIApiEmbeddingsDeploymentName: "text-embedding-ada-002",
  azureOpenAIApiVersion: "2024-02-01",
});
```

**修复**：Azure 需要实例名称、部署名称和 API 版本。

### 7. **向量存储中的维度不匹配**

```typescript
// ❌ 向量存储期望 1536 维度，模型产生 512
const embeddings = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small",
  dimensions: 512,
});

// 使用默认 1536 维度创建的向量存储
const vectorStore = await MemoryVectorStore.fromTexts(
  ["text1"],
  embeddings, // 不匹配！
);

// ✅ 一致的维度
const embeddings = new OpenAIEmbeddings({
  modelName: "text-embedding-3-small",
  // 不要覆盖维度，或确保向量存储匹配
});
```

**修复**：确保向量存储和嵌入使用兼容的维度。

## 链接和资源

### 官方文档
- [LangChain JS 嵌入概述](https://js.langchain.com/docs/integrations/text_embedding/)
- [OpenAI 嵌入](https://js.langchain.com/docs/integrations/text_embedding/openai)
- [Azure OpenAI 嵌入](https://js.langchain.com/docs/integrations/text_embedding/azure_openai)
- [HuggingFace 嵌入](https://js.langchain.com/docs/integrations/text_embedding/hugging_face)
- [Ollama 嵌入](https://js.langchain.com/docs/integrations/text_embedding/ollama)

### 提供商文档
- [OpenAI 嵌入指南](https://platform.openai.com/docs/guides/embeddings)
- [Cohere 嵌入](https://docs.cohere.com/docs/embeddings)
- [HuggingFace 模型](https://huggingface.co/models?pipeline_tag=feature-extraction)
- [Ollama](https://ollama.ai/)

### 包安装
```bash
# OpenAI
npm install @langchain/openai

# Cohere
npm install @langchain/cohere

# Ollama
npm install @langchain/ollama

# 社区 (HuggingFace 等)
npm install @langchain/community
```
