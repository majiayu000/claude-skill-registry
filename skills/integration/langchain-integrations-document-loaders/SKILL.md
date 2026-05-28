---
name: langchain-document-loaders
description: 使用 LangChain 中的文档加载器集成指南，用于处理 PDF、网页、文本文件和 API
language: js
---

# langchain-document-loaders (JavaScript/TypeScript)

## 概述

文档加载器将来自各种来源和格式的数据提取到 LangChain 的标准化文档格式中。它们对于构建 RAG 系统至关重要，因为它们将原始数据转换为可处理的文本块和元数据。

### 核心概念

- **文档**：具有 `pageContent`（文本）和 `metadata`（来源信息、页码等）的对象
- **加载器**：从特定来源/格式提取内容的类
- **元数据**：在加载期间保留的上下文信息（URL、文件路径、页码）
- **延迟加载**：流式传输文档而不将所有内容加载到内存中

## 加载器选择决策表

| 加载器类型 | 最适合 | 包 | 主要特性 |
|-------------|----------|---------|--------------|
| **PDFLoader** | PDF 文件 | `@langchain/community` | 提取文本和页码 |
| **CheerioWebBaseLoader** | 网页（静态） | `@langchain/community` | 使用 Cheerio 进行 HTML 解析 |
| **PlaywrightWebBaseLoader** | 网页（动态） | `@langchain/community` | JavaScript 渲染的内容 |
| **TextLoader** | 纯文本文件 | `langchain/document_loaders/fs/text` | 简单文本文件 |
| **JSONLoader** | JSON 文件/API | `langchain/document_loaders/fs/json` | 提取特定 JSON 字段 |
| **CSVLoader** | CSV 文件 | `@langchain/community` | 表格数据 |
| **DirectoryLoader** | 多个文件 | `langchain/document_loaders/fs/directory` | 从目录批量加载 |
| **GithubRepoLoader** | GitHub 仓库 | `@langchain/community` | 克隆和加载仓库文件 |
| **NotionLoader** | Notion 页面 | `@langchain/community` | Notion 工作区数据 |

### 何时选择每个加载器

**选择 PDFLoader 如果：**
- 您正在处理 PDF 文档
- 您需要页码元数据
- PDF 包含可提取的文本（不仅仅是图像）

**选择 CheerioWebBaseLoader 如果：**
- 您正在抓取静态网页
- 内容不需要 JavaScript
- 您想要快速、轻量级的抓取

**选择 PlaywrightWebBaseLoader 如果：**
- 网页需要 JavaScript 才能渲染
- 您需要与动态内容交互
- 您正在处理 SPA 或 React 应用

**选择 TextLoader 如果：**
- 您有简单的纯文本文件
- 不需要特殊解析
- 直接的文件到文档转换

## 代码示例

### PDF 加载器

```typescript
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";

// 加载 PDF 文件
const loader = new PDFLoader("path/to/document.pdf");
const docs = await loader.load();

console.log(`加载了 ${docs.length} 页`);
docs.forEach((doc, i) => {
  console.log(`第 ${i + 1} 页：`, doc.metadata);
  console.log(doc.pageContent.substring(0, 100));
});

// 每页都是单独的文档
// metadata 包括：source、pdf.totalPages、loc.pageNumber
```

### 网页抓取 - Cheerio（静态）

```typescript
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";

// 加载单个 URL
const loader = new CheerioWebBaseLoader(
  "https://docs.langchain.com"
);

const docs = await loader.load();
console.log(docs[0].pageContent);
console.log(docs[0].metadata); // { source: url, ... }

// 使用自定义选择器
const loaderWithSelector = new CheerioWebBaseLoader(
  "https://news.ycombinator.com",
  {
    selector: ".storylink",  // 仅提取特定元素
  }
);

// 多个 URL
const loaderMultiple = new CheerioWebBaseLoader([
  "https://example.com/page1",
  "https://example.com/page2",
]);
const allDocs = await loaderMultiple.load();
```

### 网页抓取 - Playwright（动态）

```typescript
import { PlaywrightWebBaseLoader } from "@langchain/community/document_loaders/web/playwright";

// 用于 JavaScript 渲染的页面
const loader = new PlaywrightWebBaseLoader("https://spa-app.com", {
  launchOptions: {
    headless: true,
  },
  gotoOptions: {
    waitUntil: "networkidle",  // 等待 JS 完成
  },
  evaluateOptions: {
    // 自定义评估函数
    evaluate: (page) => page.evaluate(() => document.body.innerText),
  },
});

const docs = await loader.load();
```

### 文本文件加载器

```typescript
import { TextLoader } from "langchain/document_loaders/fs/text";

const loader = new TextLoader("path/to/file.txt");
const docs = await loader.load();

// 返回包含整个文件内容的单个文档
console.log(docs[0].pageContent);
console.log(docs[0].metadata.source); // 文件路径
```

### JSON 加载器

```typescript
import { JSONLoader } from "langchain/document_loaders/fs/json";

// 使用特定字段提取加载 JSON
const loader = new JSONLoader(
  "path/to/data.json",
  ["/texts/*/content"]  // JSONPointer 以提取特定字段
);

const docs = await loader.load();

// 示例 JSON：{ "texts": [{ "content": "...", "id": 1 }] }
// 每个匹配的字段都成为一个文档
```

### CSV 加载器

```typescript
import { CSVLoader } from "@langchain/community/document_loaders/fs/csv";

const loader = new CSVLoader("path/to/data.csv", {
  column: "text",  // 用作 page_content 的列
  separator: ",",
});

const docs = await loader.load();

// 每行都成为一个文档
// 其他列存储在 metadata 中
```

### 目录加载器

```typescript
import { DirectoryLoader } from "langchain/document_loaders/fs/directory";
import { TextLoader } from "langchain/document_loaders/fs/text";
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";

// 从目录加载所有文件
const loader = new DirectoryLoader(
  "path/to/documents",
  {
    ".txt": (path) => new TextLoader(path),
    ".pdf": (path) => new PDFLoader(path),
  }
);

const docs = await loader.load();
console.log(`从目录加载了 ${docs.length} 个文档`);
```

### GitHub 加载器

```typescript
import { GithubRepoLoader } from "@langchain/community/document_loaders/web/github";

const loader = new GithubRepoLoader(
  "https://github.com/langchain-ai/langchainjs",
  {
    branch: "main",
    recursive: true,
    ignorePaths: ["node_modules/**", "dist/**"],
    maxConcurrency: 5,
  }
);

const docs = await loader.load();
// 每个文件都成为一个文档
```

### 自定义元数据示例

```typescript
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";

const loader = new CheerioWebBaseLoader("https://blog.com/post");
const docs = await loader.load();

// 添加自定义元数据
const enrichedDocs = docs.map(doc => ({
  ...doc,
  metadata: {
    ...doc.metadata,
    loadedAt: new Date().toISOString(),
    category: "blog",
  },
}));
```

### 延迟加载（内存高效）

```typescript
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";

const loader = new PDFLoader("large-file.pdf");

// 使用 lazy() 处理大文件 - 流式传输文档
for await (const doc of loader.lazy()) {
  console.log("正在处理页面：", doc.metadata.loc.pageNumber);
  // 一次处理一页，而不将所有页面加载到内存中
}
```

## 边界

### 代理可以做什么

✅ **从各种来源加载**
- PDF、文本、CSV、JSON 文件
- 网页（静态和动态）
- GitHub 仓库、Notion 页面
- API 和自定义来源

✅ **带元数据提取**
- 保留来源信息
- 添加自定义元数据字段
- 跟踪页码、URL、文件路径

✅ **高效处理**
- 对大文件使用延迟加载
- 批处理目录
- 流式传输数据而不加载所有内容

✅ **自定义提取**
- 使用 CSS 选择器进行网页抓取
- 提取特定的 JSON 字段
- 过滤和转换内容

### 代理不能做什么

❌ **从加密/受保护的文件中提取**
- 无法绕过受密码保护的 PDF
- 无法在没有凭据的情况下访问需要身份验证的网站

❌ **直接处理二进制数据**
- 无法在没有 OCR 的情况下从图像中提取
- 无法在没有转换器的情况下处理专有格式

❌ **处理所有 PDF 类型**
- 扫描的 PDF 需要 OCR
- 基于 PDF 的图像无法提取文本

❌ **绕过速率限制**
- 无法忽略网站速率限制
- 必须遵守 robots.txt

## 常见陷阱

### 1. **PDF 加载器需要安装**

```typescript
// ❌ 如果未安装 pdf-parse 将失败
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
const loader = new PDFLoader("file.pdf");

// ✅ 首先安装依赖项
// npm install pdf-parse

const loader = new PDFLoader("file.pdf");
const docs = await loader.load(); // 有效！
```

**修复**：安装所需的依赖项：`npm install pdf-parse`

### 2. **网页抓取被 CORS/Robots 阻止**

```typescript
// ❌ 可能因 CORS 或阻止而失败
const loader = new CheerioWebBaseLoader("https://protected-site.com");
await loader.load(); // 错误！

// ✅ 检查 robots.txt 并使用适当的加载器
// 对于客户端阻止，在 Node.js 中运行（服务端）
// 对于动态内容，使用 Playwright

const loader = new PlaywrightWebBaseLoader("https://protected-site.com");
```

**修复**：对于被阻止的站点，使用 PlaywrightWebBaseLoader 或检查 robots.txt。

### 3. **大文件和内存**

```typescript
// ❌ 将巨大的 PDF 加载到内存中
const loader = new PDFLoader("huge-book.pdf");
const docs = await loader.load(); // 可能会崩溃！

// ✅ 使用延迟加载
for await (const doc of loader.lazy()) {
  processDocument(doc);
  // 一次只有一页在内存中
}
```

**修复**：对大文件使用 `lazy()` 方法。

### 4. **路径解析问题**

```typescript
// ❌ 相对路径可能无法按预期工作
const loader = new TextLoader("./data/file.txt");

// ✅ 使用绝对路径或 path 模块
import path from "path";
const filePath = path.join(process.cwd(), "data", "file.txt");
const loader = new TextLoader(filePath);
```

**修复**：使用绝对路径或 `path` 模块以确保可靠性。

### 5. **Cheerio 与 Playwright 混淆**

```typescript
// ❌ 对动态内容使用 Cheerio
const loader = new CheerioWebBaseLoader("https://react-app.com");
const docs = await loader.load();
// 内容为空或不完整！

// ✅ 对 JavaScript 渲染的页面使用 Playwright
const loader = new PlaywrightWebBaseLoader("https://react-app.com", {
  gotoOptions: { waitUntil: "networkidle" }
});
```

**修复**：对 SPA 和动态内容使用 Playwright。

### 6. **JSON 指针语法**

```typescript
// ❌ 错误的 JSON 指针格式
const loader = new JSONLoader("data.json", ["texts.content"]);

// ✅ 正确的 JSON 指针格式（以 / 开头）
const loader = new JSONLoader("data.json", ["/texts/0/content"]);
```

**修复**：JSON 指针必须以 `/` 开头并使用 `/` 作为分隔符。

### 7. **目录加载器文件扩展名匹配**

```typescript
// ❌ 扩展名不匹配
const loader = new DirectoryLoader("docs", {
  "txt": (path) => new TextLoader(path),  // 错误！
});

// ✅ 包括点
const loader = new DirectoryLoader("docs", {
  ".txt": (path) => new TextLoader(path),
  ".pdf": (path) => new PDFLoader(path),
});
```

**修复**：文件扩展名必须包括点（`.txt`、`.pdf`）。

## 链接和资源

### 官方文档
- [LangChain JS 文档加载器](https://js.langchain.com/docs/integrations/document_loaders/)
- [PDF 加载器](https://js.langchain.com/docs/integrations/document_loaders/file_loaders/pdf)
- [Web 加载器](https://js.langchain.com/docs/integrations/document_loaders/web_loaders/)
- [文件系统加载器](https://js.langchain.com/docs/integrations/document_loaders/file_loaders/)

### 包安装
```bash
# 社区加载器
npm install @langchain/community

# PDF 支持
npm install pdf-parse

# 用于动态网页的 Playwright
npm install playwright
npx playwright install
```
