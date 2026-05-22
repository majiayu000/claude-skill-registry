---
name: gemini-integration
description: |
  Google Gemini API 集成指南：提供 AI 分析、提示词工程、流式响应和多模态处理的最佳实践。
  Use when: 需要集成 Gemini API、编写提示词、处理流式响应、多模态输入。
  Triggers: "Gemini", "AI", "LLM", "提示词", "prompt", "流式", "streaming", "多模态"
category: ai-integration
---

# Gemini Integration (Google Gemini API 集成指南)

> 🤖 **核心理念**: 标准化 Gemini API 集成流程，确保 AI 功能的可靠性、性能和用户体验。

## When to Use This Skill

使用此技能当你需要：
- 集成 Google Gemini API 进行 AI 分析
- 编写和优化提示词 (Prompt Engineering)
- 实现流式响应 (Streaming Response)
- 处理多模态输入 (文本、图片、文档)
- 构建金融分析 AI 功能
- 实现多轮对话系统

## Not For / Boundaries

此技能不适用于：
- 其他 LLM 提供商 (OpenAI, Claude 等)
- 本地模型部署
- 模型微调 (Fine-tuning)

---

## Quick Reference

### 🎯 Gemini 集成标准工作流

```
需求分析 → 模型选择 → 提示词设计 → API 集成 → 流式处理 → 测试验证
    ↓          ↓           ↓           ↓          ↓          ↓
  场景定义   性能/成本   结构化输出   错误处理   用户体验   质量评估
```

### 📋 集成前必问清单

| 问题 | 目的 |
|------|------|
| 1. 使用哪个模型？ | gemini-2.0-flash / gemini-1.5-pro |
| 2. 需要流式响应吗？ | 长文本生成建议流式 |
| 3. 输入类型是什么？ | 纯文本 / 图片 / 文档 |
| 4. 输出格式要求？ | 自由文本 / JSON / 结构化 |
| 5. 上下文长度需求？ | 影响模型选择和成本 |
| 6. 安全过滤级别？ | 金融场景需要适当配置 |

### 🔍 模型选择指南

| 模型 | 适用场景 | 特点 |
|------|----------|------|
| `gemini-2.0-flash` | 通用任务、快速响应 | 速度快、成本低 |
| `gemini-1.5-pro` | 复杂分析、长上下文 | 能力强、上下文长 |
| `gemini-1.5-flash` | 平衡性能和成本 | 中等速度和能力 |

---

## API 集成基础

### 环境配置

```bash
# .env.local
GEMINI_API_KEY=your_api_key_here

# Vercel 环境变量同步
vercel env add GEMINI_API_KEY production
vercel env add GEMINI_API_KEY preview
```

### 基础客户端配置

```typescript
// src/services/ai/gemini-client.ts
import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from '@google/generative-ai';

// 初始化客户端
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

// 安全设置 (金融场景推荐)
const safetySettings = [
  {
    category: HarmCategory.HARM_CATEGORY_HARASSMENT,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
  {
    category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
  {
    category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
  {
    category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
];

// 生成配置
const generationConfig = {
  temperature: 0.7,        // 创造性 (0-1)
  topP: 0.95,              // 核采样
  topK: 40,                // Top-K 采样
  maxOutputTokens: 8192,   // 最大输出长度
};

// 获取模型实例
export function getModel(modelName = 'gemini-2.0-flash') {
  return genAI.getGenerativeModel({
    model: modelName,
    safetySettings,
    generationConfig,
  });
}

// 获取流式模型
export function getStreamingModel(modelName = 'gemini-2.0-flash') {
  return genAI.getGenerativeModel({
    model: modelName,
    safetySettings,
    generationConfig,
  });
}
```

### 基础文本生成

```typescript
// src/services/ai/generate.ts
import { getModel } from './gemini-client';

export async function generateText(prompt: string): Promise<string> {
  const model = getModel();
  
  try {
    const result = await model.generateContent(prompt);
    const response = result.response;
    return response.text();
  } catch (error) {
    console.error('[Gemini] 生成失败:', error);
    throw new GeminiError('文本生成失败', error);
  }
}

// 自定义错误类
export class GeminiError extends Error {
  constructor(message: string, public readonly cause?: unknown) {
    super(message);
    this.name = 'GeminiError';
  }
}
```

---

## 流式响应处理

### 服务端流式生成

```typescript
// src/services/ai/streaming.ts
import { getStreamingModel } from './gemini-client';

/**
 * 流式生成文本
 * @param prompt 提示词
 * @param onChunk 每个 chunk 的回调
 */
export async function generateStream(
  prompt: string,
  onChunk: (chunk: string) => void
): Promise<string> {
  const model = getStreamingModel();
  
  try {
    const result = await model.generateContentStream(prompt);
    let fullText = '';
    
    for await (const chunk of result.stream) {
      const chunkText = chunk.text();
      fullText += chunkText;
      onChunk(chunkText);
    }
    
    return fullText;
  } catch (error) {
    console.error('[Gemini] 流式生成失败:', error);
    throw new GeminiError('流式生成失败', error);
  }
}
```

### API Route 流式响应

```typescript
// app/api/ai/stream/route.ts
import { getStreamingModel } from '@/services/ai/gemini-client';

export async function POST(request: Request) {
  const { prompt, systemPrompt } = await request.json();
  
  const model = getStreamingModel();
  
  // 创建 ReadableStream
  const stream = new ReadableStream({
    async start(controller) {
      try {
        const fullPrompt = systemPrompt 
          ? `${systemPrompt}\n\n${prompt}` 
          : prompt;
          
        const result = await model.generateContentStream(fullPrompt);
        
        for await (const chunk of result.stream) {
          const text = chunk.text();
          // 发送 SSE 格式数据
          controller.enqueue(
            new TextEncoder().encode(`data: ${JSON.stringify({ text })}\n\n`)
          );
        }
        
        // 发送结束信号
        controller.enqueue(
          new TextEncoder().encode('data: [DONE]\n\n')
        );
        controller.close();
      } catch (error) {
        controller.enqueue(
          new TextEncoder().encode(
            `data: ${JSON.stringify({ error: '生成失败' })}\n\n`
          )
        );
        controller.close();
      }
    },
  });
  
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

### 前端流式消费

```typescript
// src/hooks/useStreamingChat.ts
import { useState, useCallback } from 'react';

interface UseStreamingChatOptions {
  onChunk?: (chunk: string) => void;
  onComplete?: (fullText: string) => void;
  onError?: (error: Error) => void;
}

export function useStreamingChat(options: UseStreamingChatOptions = {}) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedText, setStreamedText] = useState('');
  
  const sendMessage = useCallback(async (prompt: string, systemPrompt?: string) => {
    setIsStreaming(true);
    setStreamedText('');
    
    try {
      const response = await fetch('/api/ai/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, systemPrompt }),
      });
      
      if (!response.ok) {
        throw new Error('请求失败');
      }
      
      const reader = response.body?.getReader();
      if (!reader) throw new Error('无法读取响应');
      
      const decoder = new TextDecoder();
      let fullText = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            
            try {
              const parsed = JSON.parse(data);
              if (parsed.text) {
                fullText += parsed.text;
                setStreamedText(fullText);
                options.onChunk?.(parsed.text);
              }
              if (parsed.error) {
                throw new Error(parsed.error);
              }
            } catch (e) {
              // 忽略解析错误
            }
          }
        }
      }
      
      options.onComplete?.(fullText);
      return fullText;
    } catch (error) {
      const err = error instanceof Error ? error : new Error('未知错误');
      options.onError?.(err);
      throw err;
    } finally {
      setIsStreaming(false);
    }
  }, [options]);
  
  return {
    sendMessage,
    isStreaming,
    streamedText,
  };
}
```

### 流式响应 UI 组件

```typescript
// src/components/StreamingMessage.tsx
'use client';

import { useStreamingChat } from '@/hooks/useStreamingChat';
import { useState } from 'react';

export function StreamingMessage() {
  const [input, setInput] = useState('');
  const { sendMessage, isStreaming, streamedText } = useStreamingChat({
    onComplete: (text) => {
      console.log('生成完成:', text.length, '字符');
    },
  });
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    
    await sendMessage(input);
    setInput('');
  };
  
  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入问题..."
          className="flex-1 px-4 py-2 border rounded-lg"
          disabled={isStreaming}
        />
        <button
          type="submit"
          disabled={isStreaming}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:opacity-50"
        >
          {isStreaming ? '生成中...' : '发送'}
        </button>
      </form>
      
      {streamedText && (
        <div className="p-4 bg-gray-50 rounded-lg whitespace-pre-wrap">
          {streamedText}
          {isStreaming && <span className="animate-pulse">▊</span>}
        </div>
      )}
    </div>
  );
}
```

---

## 多模态输入处理

### 图片分析

```typescript
// src/services/ai/vision.ts
import { getModel } from './gemini-client';

/**
 * 分析图片内容
 */
export async function analyzeImage(
  imageBase64: string,
  mimeType: string,
  prompt: string
): Promise<string> {
  const model = getModel('gemini-1.5-pro'); // 视觉任务推荐 pro 模型
  
  const imagePart = {
    inlineData: {
      data: imageBase64,
      mimeType,
    },
  };
  
  try {
    const result = await model.generateContent([prompt, imagePart]);
    return result.response.text();
  } catch (error) {
    console.error('[Gemini] 图片分析失败:', error);
    throw new GeminiError('图片分析失败', error);
  }
}

/**
 * 从 URL 分析图片
 */
export async function analyzeImageFromUrl(
  imageUrl: string,
  prompt: string
): Promise<string> {
  // 获取图片数据
  const response = await fetch(imageUrl);
  const arrayBuffer = await response.arrayBuffer();
  const base64 = Buffer.from(arrayBuffer).toString('base64');
  const mimeType = response.headers.get('content-type') || 'image/jpeg';
  
  return analyzeImage(base64, mimeType, prompt);
}
```

### 文档分析

```typescript
// src/services/ai/document.ts
import { getModel } from './gemini-client';

/**
 * 分析 PDF 文档
 */
export async function analyzePDF(
  pdfBase64: string,
  prompt: string
): Promise<string> {
  const model = getModel('gemini-1.5-pro');
  
  const pdfPart = {
    inlineData: {
      data: pdfBase64,
      mimeType: 'application/pdf',
    },
  };
  
  try {
    const result = await model.generateContent([prompt, pdfPart]);
    return result.response.text();
  } catch (error) {
    console.error('[Gemini] PDF 分析失败:', error);
    throw new GeminiError('PDF 分析失败', error);
  }
}

/**
 * 分析多个文件
 */
export async function analyzeMultipleFiles(
  files: Array<{ data: string; mimeType: string }>,
  prompt: string
): Promise<string> {
  const model = getModel('gemini-1.5-pro');
  
  const parts = files.map(file => ({
    inlineData: {
      data: file.data,
      mimeType: file.mimeType,
    },
  }));
  
  try {
    const result = await model.generateContent([prompt, ...parts]);
    return result.response.text();
  } catch (error) {
    console.error('[Gemini] 多文件分析失败:', error);
    throw new GeminiError('多文件分析失败', error);
  }
}
```

---

## 多轮对话

### 对话管理

```typescript
// src/services/ai/chat.ts
import { getModel } from './gemini-client';
import type { Content } from '@google/generative-ai';

export interface ChatMessage {
  role: 'user' | 'model';
  content: string;
}

/**
 * 创建对话会话
 */
export function createChatSession(systemPrompt?: string) {
  const model = getModel();
  
  const history: Content[] = [];
  
  // 如果有系统提示词，作为第一条消息
  if (systemPrompt) {
    history.push({
      role: 'user',
      parts: [{ text: `系统指令: ${systemPrompt}` }],
    });
    history.push({
      role: 'model',
      parts: [{ text: '我已理解系统指令，准备好为您服务。' }],
    });
  }
  
  const chat = model.startChat({ history });
  
  return {
    /**
     * 发送消息
     */
    async sendMessage(message: string): Promise<string> {
      const result = await chat.sendMessage(message);
      return result.response.text();
    },
    
    /**
     * 流式发送消息
     */
    async sendMessageStream(
      message: string,
      onChunk: (chunk: string) => void
    ): Promise<string> {
      const result = await chat.sendMessageStream(message);
      let fullText = '';
      
      for await (const chunk of result.stream) {
        const text = chunk.text();
        fullText += text;
        onChunk(text);
      }
      
      return fullText;
    },
    
    /**
     * 获取对话历史
     */
    getHistory(): ChatMessage[] {
      return chat.getHistory().map(msg => ({
        role: msg.role as 'user' | 'model',
        content: msg.parts.map(p => (p as { text: string }).text).join(''),
      }));
    },
  };
}
```

### 对话 Hook

```typescript
// src/hooks/useChat.ts
import { useState, useCallback, useRef } from 'react';
import { createChatSession, ChatMessage } from '@/services/ai/chat';

export function useChat(systemPrompt?: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatRef = useRef(createChatSession(systemPrompt));
  
  const sendMessage = useCallback(async (content: string) => {
    setIsLoading(true);
    
    // 添加用户消息
    setMessages(prev => [...prev, { role: 'user', content }]);
    
    try {
      // 添加空的 AI 消息用于流式更新
      setMessages(prev => [...prev, { role: 'model', content: '' }]);
      
      await chatRef.current.sendMessageStream(content, (chunk) => {
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];
          if (lastMessage.role === 'model') {
            lastMessage.content += chunk;
          }
          return newMessages;
        });
      });
    } catch (error) {
      // 移除空的 AI 消息
      setMessages(prev => prev.slice(0, -1));
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const reset = useCallback(() => {
    chatRef.current = createChatSession(systemPrompt);
    setMessages([]);
  }, [systemPrompt]);
  
  return {
    messages,
    sendMessage,
    isLoading,
    reset,
  };
}
```

---

## 结构化输出

### JSON 输出

```typescript
// src/services/ai/structured.ts
import { getModel } from './gemini-client';

/**
 * 生成结构化 JSON 输出
 */
export async function generateJSON<T>(
  prompt: string,
  schema: string
): Promise<T> {
  const model = getModel();
  
  const structuredPrompt = `
${prompt}

请严格按照以下 JSON Schema 格式输出，不要包含任何其他文字：
${schema}

只输出 JSON，不要有任何解释或 markdown 格式。
`;
  
  try {
    const result = await model.generateContent(structuredPrompt);
    const text = result.response.text();
    
    // 清理可能的 markdown 代码块
    const cleanedText = text
      .replace(/```json\n?/g, '')
      .replace(/```\n?/g, '')
      .trim();
    
    return JSON.parse(cleanedText) as T;
  } catch (error) {
    console.error('[Gemini] JSON 生成失败:', error);
    throw new GeminiError('JSON 生成失败', error);
  }
}

// 使用示例
interface StockAnalysis {
  symbol: string;
  recommendation: 'buy' | 'hold' | 'sell';
  targetPrice: number;
  riskLevel: 'low' | 'medium' | 'high';
  reasons: string[];
}

const analysis = await generateJSON<StockAnalysis>(
  '分析苹果公司 (AAPL) 的股票',
  `{
    "symbol": "string",
    "recommendation": "buy | hold | sell",
    "targetPrice": "number",
    "riskLevel": "low | medium | high",
    "reasons": ["string"]
  }`
);
```

---

## 错误处理

### Gemini 特定错误

```typescript
// src/services/ai/errors.ts

export class GeminiError extends Error {
  constructor(
    message: string,
    public readonly cause?: unknown,
    public readonly code?: string
  ) {
    super(message);
    this.name = 'GeminiError';
  }
}

export class GeminiRateLimitError extends GeminiError {
  constructor(retryAfter?: number) {
    super(`API 请求过于频繁，请 ${retryAfter || 60} 秒后重试`);
    this.name = 'GeminiRateLimitError';
  }
}

export class GeminiSafetyError extends GeminiError {
  constructor(public readonly blockedCategories: string[]) {
    super('内容被安全过滤器拦截');
    this.name = 'GeminiSafetyError';
  }
}

export class GeminiQuotaError extends GeminiError {
  constructor() {
    super('API 配额已用尽');
    this.name = 'GeminiQuotaError';
  }
}

/**
 * 处理 Gemini API 错误
 */
export function handleGeminiError(error: unknown): never {
  if (error instanceof GeminiError) {
    throw error;
  }
  
  const errorMessage = error instanceof Error ? error.message : String(error);
  
  // 速率限制
  if (errorMessage.includes('429') || errorMessage.includes('rate limit')) {
    throw new GeminiRateLimitError();
  }
  
  // 配额用尽
  if (errorMessage.includes('quota') || errorMessage.includes('billing')) {
    throw new GeminiQuotaError();
  }
  
  // 安全过滤
  if (errorMessage.includes('safety') || errorMessage.includes('blocked')) {
    throw new GeminiSafetyError([]);
  }
  
  throw new GeminiError('Gemini API 调用失败', error);
}
```

### 重试包装器

```typescript
// src/services/ai/retry.ts
import { GeminiError, GeminiRateLimitError, handleGeminiError } from './errors';

interface RetryOptions {
  maxRetries?: number;
  baseDelay?: number;
  maxDelay?: number;
}

export async function withGeminiRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = options;
  
  let lastError: Error | undefined;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      try {
        handleGeminiError(error);
      } catch (geminiError) {
        lastError = geminiError as Error;
        
        // 不重试的错误
        if (
          !(geminiError instanceof GeminiRateLimitError) &&
          attempt === maxRetries
        ) {
          throw geminiError;
        }
        
        // 计算延迟
        const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
        console.log(`[Gemini] 重试 ${attempt + 1}/${maxRetries}，等待 ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError;
}
```

---

## 性能优化

### 请求缓存

```typescript
// src/services/ai/cache.ts

const cache = new Map<string, { result: string; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟

/**
 * 带缓存的生成
 */
export async function generateWithCache(
  prompt: string,
  generator: (prompt: string) => Promise<string>
): Promise<string> {
  const cacheKey = hashPrompt(prompt);
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    console.log('[Gemini] 命中缓存');
    return cached.result;
  }
  
  const result = await generator(prompt);
  cache.set(cacheKey, { result, timestamp: Date.now() });
  
  return result;
}

function hashPrompt(prompt: string): string {
  // 简单哈希，生产环境建议使用更好的哈希算法
  let hash = 0;
  for (let i = 0; i < prompt.length; i++) {
    const char = prompt.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return hash.toString(36);
}
```

### 并发控制

```typescript
// src/services/ai/concurrency.ts

class ConcurrencyLimiter {
  private running = 0;
  private queue: Array<() => void> = [];
  
  constructor(private maxConcurrent: number) {}
  
  async run<T>(fn: () => Promise<T>): Promise<T> {
    if (this.running >= this.maxConcurrent) {
      await new Promise<void>(resolve => this.queue.push(resolve));
    }
    
    this.running++;
    
    try {
      return await fn();
    } finally {
      this.running--;
      const next = this.queue.shift();
      if (next) next();
    }
  }
}

// 限制并发请求数
export const geminiLimiter = new ConcurrencyLimiter(5);

// 使用
const result = await geminiLimiter.run(() => generateText(prompt));
```

---

## 最佳实践

### ✅ 推荐做法

| 做法 | 说明 |
|------|------|
| 使用流式响应 | 长文本生成提升用户体验 |
| 结构化提示词 | 使用模板确保输出一致性 |
| 错误重试 | 处理临时性 API 错误 |
| 请求缓存 | 相同请求避免重复调用 |
| 并发控制 | 避免触发速率限制 |
| 安全过滤 | 配置适当的安全级别 |

### ❌ 避免做法

| 做法 | 问题 |
|------|------|
| 前端直接调用 API | 暴露 API Key |
| 忽略错误处理 | 用户体验差 |
| 无限制并发 | 触发速率限制 |
| 硬编码提示词 | 难以维护和优化 |
| 忽略 Token 限制 | 请求失败或截断 |

---

## References

- `references/prompt-templates.md`: 金融分析提示词模板、多轮对话模板

---

## Maintenance

- **Sources**: Google Gemini API 官方文档, 项目实践经验
- **Last Updated**: 2025-01-01
- **Known Limits**: 
  - API 速率限制需根据账户级别调整
  - 多模态功能需要 Pro 模型
  - 长上下文场景成本较高
