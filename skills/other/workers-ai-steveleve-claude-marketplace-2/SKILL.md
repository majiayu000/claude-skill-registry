---
name: Workers AI
description: This skill should be used when the user asks about "Workers AI", "AI models", "text generation", "embeddings", "semantic search", "RAG", "Retrieval Augmented Generation", "AI inference", "LLaMA", "Llama", "bge embeddings", "@cf/ models", "AI Gateway", or discusses implementing AI features, choosing AI models, generating embeddings, or building RAG systems on Cloudflare Workers.
version: 0.1.0
---

# Workers AI

## Purpose

This skill provides comprehensive guidance for using Workers AI, Cloudflare's AI inference platform. It covers available models, inference patterns, embedding generation, RAG (Retrieval Augmented Generation) architectures, AI Gateway integration, and best practices for AI workloads. Use this skill when implementing AI features, selecting models, building RAG systems, or optimizing AI inference on Workers.

## Workers AI Overview

Workers AI provides serverless AI inference at the edge with:
- **Text Generation**: LLMs for chat, completion, summarization
- **Embeddings**: Vector representations for semantic search
- **Image Generation**: Text-to-image models
- **Vision**: Image classification and object detection
- **Speech**: Text-to-speech and automatic speech recognition
- **Translation**: Language translation models

### Key Benefits

- **Edge deployment**: Low latency inference globally
- **No infrastructure**: Serverless, auto-scaling
- **Integrated**: Native integration with Workers, Vectorize, D1
- **Cost-effective**: Pay per inference, no minimum
- **Latest models**: Llama 3.1, Mistral, BAAI embeddings

## Project-Specific Model Decisions

Before recommending a model:
1. Check `.claude/cloudflare-expert.local.md` for existing decisions in the "AI Model Decisions" section
2. If found, use the saved decision and mention: "Based on your project's saved configuration..."
3. If not found, describe options with trade-offs and let the user decide
4. After user decides, offer to save the decision to memory with rationale

## Model Information Freshness

**Fetch fresh info via Docs MCP when**:
- User asks for "latest" or "current" models
- Memory decision is older than 90 days
- Starting a new project
- User mentions an unknown model

**Use skill knowledge when**:
- Explaining patterns (RAG workflow, chunking)
- Showing code patterns (API usage)
- Teaching concepts (temperature, top-k)

## Model Categories

### Text Generation Models

**LLaMA 3.1** (Long context, multilingual):
- `@cf/meta/llama-3.1-8b-instruct` - Chat and instruction following
- Best for: Conversational AI, Q&A, summarization, general text generation
- Context window: 128K tokens
- Multilingual support

**Mistral** (Fast, efficient):
- `@cf/mistral/mistral-7b-instruct-v0.2` - Fast instruction following
- Best for: Quick responses, simpler tasks
- Context window: 32K tokens

**Qwen** (Balanced efficiency):
- `@cf/qwen/qwen1.5-14b-chat-awq` - Quantized for efficiency
- Best for: Balance between speed and quality

See `references/model-selection-framework.md` for decision criteria and `references/workers-ai-models.md` for complete model catalog.

### Embedding Models

**BGE Base** (English, balanced):
- `@cf/baai/bge-base-en-v1.5` - High-quality English embeddings
- Dimensions: 768
- Best for: RAG, semantic search, English content

**BGE Large** (Higher quality, slower):
- `@cf/baai/bge-large-en-v1.5` - Higher quality, more compute
- Dimensions: 1024
- Best for: When quality is critical

**BGE Small** (Fast, compact):
- `@cf/baai/bge-small-en-v1.5` - Faster, smaller model
- Dimensions: 384
- Best for: When speed is critical, large volumes

**BGE M3** (Multilingual):
- `@cf/baai/bge-m3` - Multilingual support
- Best for: Multi-language content

### Image Generation

**Stable Diffusion**:
- `@cf/stabilityai/stable-diffusion-xl-base-1.0` - Text-to-image
- `@cf/bytedance/stable-diffusion-xl-lightning` - Faster generation
- Best for: Creating images from text descriptions

### Vision Models

**Image Classification**:
- `@cf/microsoft/resnet-50` - Object recognition
- Best for: Classifying image content

### Speech Models

**Text-to-Speech**:
- `@cf/meta/m2m100-1.2b` - Multilingual speech synthesis

**Automatic Speech Recognition**:
- `@cf/openai/whisper` - Speech-to-text
- Best for: Transcribing audio

## Text Generation

### Basic Inference

```javascript
export default {
  async fetch(request, env, ctx) {
    const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'What is Cloudflare Workers?' }
      ]
    });

    return new Response(JSON.stringify(response));
  }
};
```

### Streaming Responses

```javascript
const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [
    { role: 'user', content: 'Write a story about...' }
  ],
  stream: true
});

return new Response(stream, {
  headers: { 'Content-Type': 'text/event-stream' }
});
```

### Model Parameters

```javascript
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [/* messages */],
  max_tokens: 512,        // Max tokens to generate
  temperature: 0.7,       // Creativity (0-1, higher = more random)
  top_p: 0.9,            // Nucleus sampling
  top_k: 40,             // Top-k sampling
  repetition_penalty: 1.2 // Penalize repetition
});
```

**Parameter guidelines**:
- **temperature**: 0.1-0.3 for factual, 0.7-0.9 for creative
- **max_tokens**: Set based on expected response length
- **top_p/top_k**: Usually leave at defaults unless fine-tuning behavior

## Embeddings

### Generating Embeddings

```javascript
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: ['Hello world', 'Another sentence']
}) as { data: number[][] };

const vector1 = embeddings.data[0]; // [0.123, -0.456, ...]
const vector2 = embeddings.data[1];
```

**Important TypeScript note**: Always add `as { data: number[][] }` type assertion when using embeddings API.

### Batch Processing

```javascript
// Batch multiple texts for efficiency
const texts = documents.map(d => d.content);

// Process in batches of 100 (recommended batch size)
const batchSize = 100;
const allEmbeddings = [];

for (let i = 0; i < texts.length; i += batchSize) {
  const batch = texts.slice(i, i + batchSize);
  const result = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
    text: batch
  }) as { data: number[][] };

  allEmbeddings.push(...result.data);
}
```

### Text Chunking for Embeddings

For long documents, split into chunks before embedding:

```javascript
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 500,      // Characters per chunk
  chunkOverlap: 50     // Overlap between chunks
});

const chunks = await splitter.splitText(longDocument);

// Generate embedding for each chunk
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: chunks
}) as { data: number[][] };

// Store each chunk with its embedding
for (let i = 0; i < chunks.length; i++) {
  await env.VECTOR_INDEX.insert([{
    id: `${docId}-chunk-${i}`,
    values: embeddings.data[i],
    metadata: { text: chunks[i], docId, chunkIndex: i }
  }]);
}
```

See `references/rag-architecture-patterns.md` for complete RAG implementation patterns.

## RAG (Retrieval Augmented Generation)

### Basic RAG Pattern

```javascript
async function answerQuestion(question, env) {
  // 1. Generate question embedding
  const questionEmbedding = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
    text: [question]
  }) as { data: number[][] };

  // 2. Find similar documents
  const similar = await env.VECTOR_INDEX.query(questionEmbedding.data[0], {
    topK: 3,
    returnMetadata: true
  });

  // 3. Build context from retrieved documents
  const context = similar.matches
    .map(match => match.metadata.text)
    .join('\n\n');

  // 4. Generate answer with context
  const answer = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      {
        role: 'system',
        content: 'Answer the question using only the provided context. If the answer is not in the context, say "I don\'t have enough information."'
      },
      {
        role: 'user',
        content: `Context:\n${context}\n\nQuestion: ${question}`
      }
    ]
  });

  return {
    answer: answer.response,
    sources: similar.matches.map(m => ({
      score: m.score,
      text: m.metadata.text
    }))
  };
}
```

### Advanced RAG with Reranking

```javascript
async function advancedRAG(question, env) {
  // 1. Retrieve more candidates (top 10)
  const questionEmbedding = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
    text: [question]
  }) as { data: number[][] };

  const candidates = await env.VECTOR_INDEX.query(questionEmbedding.data[0], {
    topK: 10
  });

  // 2. Rerank with LLM for relevance
  const reranked = [];
  for (const candidate of candidates.matches) {
    const relevance = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      messages: [{
        role: 'user',
        content: `Rate the relevance of this passage to the question on a scale of 0-10:\n\nQuestion: ${question}\n\nPassage: ${candidate.metadata.text}\n\nRating (just the number):`
      }],
      max_tokens: 5
    });

    const score = parseInt(relevance.response);
    if (score >= 7) {
      reranked.push({ ...candidate, rerankScore: score });
    }
  }

  // 3. Use top reranked results
  reranked.sort((a, b) => b.rerankScore - a.rerankScore);
  const topResults = reranked.slice(0, 3);

  const context = topResults.map(r => r.metadata.text).join('\n\n');

  // 4. Generate answer
  const answer = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [{
      role: 'system',
      content: 'Answer based on the context provided.'
    }, {
      role: 'user',
      content: `Context:\n${context}\n\nQuestion: ${question}`
    }]
  });

  return { answer: answer.response, sources: topResults };
}
```

See `examples/rag-implementation.js` for complete RAG examples.

## AI Gateway

AI Gateway provides caching, rate limiting, and analytics for AI requests.

### Configuration

```jsonc
// wrangler.jsonc
{
  "ai": {
    "binding": "AI",
    "gateway_id": "my-gateway"
  }
}
```

### Benefits

- **Caching**: Cache identical requests, reduce costs
- **Rate limiting**: Protect against abuse
- **Analytics**: Track usage, costs, latency
- **Fallback**: Automatic retry and fallback logic

### Usage

```javascript
// Requests automatically go through AI Gateway when configured
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{ role: 'user', content: 'Hello' }]
});
// Gateway handles caching, rate limiting, analytics automatically
```

## Best Practices

### Model Selection

1. **Text Generation**:
   - Simple tasks: `mistral-7b-instruct`
   - Complex tasks: `llama-3.1-8b-instruct`
   - Long context: `llama-3.1-8b-instruct` (128K context)

2. **Embeddings**:
   - English: `bge-base-en-v1.5`
   - Multilingual: `bge-m3`
   - Speed critical: `bge-small-en-v1.5`
   - Quality critical: `bge-large-en-v1.5`

### Prompt Engineering

**Good prompts**:
```javascript
// Be specific
{ role: 'user', content: 'Summarize this article in 3 bullet points: ...' }

// Provide context
{ role: 'system', content: 'You are an expert programmer.' }

// Use examples (few-shot)
{
  role: 'user',
  content: 'Example: Input "hello" -> Output "HELLO"\nInput "world" ->'
}
```

**Avoid**:
- Vague instructions
- Very long prompts without structure
- Asking for multiple unrelated tasks in one request

### Cost Optimization

1. **Cache results**: Use KV to cache AI responses
   ```javascript
   const cacheKey = `ai:${hash(prompt)}`;
   let cached = await env.CACHE.get(cacheKey);
   if (!cached) {
     cached = await env.AI.run(model, params);
     await env.CACHE.put(cacheKey, JSON.stringify(cached), {
       expirationTtl: 3600
     });
   }
   ```

2. **Use AI Gateway**: Automatic caching and rate limiting

3. **Batch embeddings**: Process multiple texts together

4. **Right-size models**: Use smaller models when possible

5. **Optimize prompts**: Shorter prompts = lower cost

### Performance Optimization

1. **Streaming**: Use streaming for long responses to improve perceived latency

2. **Parallel requests**: Use `Promise.all()` for independent AI calls
   ```javascript
   const [summary, sentiment] = await Promise.all([
     env.AI.run(model, { messages: [summaryPrompt] }),
     env.AI.run(model, { messages: [sentimentPrompt] })
   ]);
   ```

3. **Early termination**: Use `max_tokens` to limit output

4. **Async with waitUntil**: For non-critical AI tasks
   ```javascript
   ctx.waitUntil(
     generateAnalytics(request, env)
   );
   ```

### RAG Best Practices

1. **Chunk size**: 300-500 characters for optimal retrieval

2. **Overlap**: 10-20% overlap between chunks to preserve context

3. **Top-K selection**: 3-5 documents usually optimal

4. **Reranking**: Consider LLM-based reranking for better quality

5. **Metadata**: Store source information for citation

6. **Hybrid search**: Combine vector search with keyword search for best results

## Pricing and Limits

### Pricing Model

- Charged per **neuron** (unit of inference)
- Varies by model complexity
- Free tier available
- AI Gateway caching reduces costs

### Rate Limits

- Model-specific rate limits
- Scale based on account type
- Use AI Gateway for automatic rate limiting

### Quotas

- Free tier: Limited neurons/month
- Paid tier: Higher limits, pay as you go
- Enterprise: Custom quotas

See Cloudflare documentation or use cloudflare-docs-specialist agent for current pricing.

## Common Patterns

### Pattern 1: Conversational AI

```javascript
// Maintain conversation history
const history = await env.KV.get(`chat:${sessionId}`, 'json') || [];

history.push({ role: 'user', content: userMessage });

const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: history
});

history.push({ role: 'assistant', content: response.response });

await env.KV.put(`chat:${sessionId}`, JSON.stringify(history), {
  expirationTtl: 3600
});
```

### Pattern 2: Document Analysis

```javascript
// Analyze document with AI
const analysis = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{
    role: 'user',
    content: `Analyze this document and extract:\n1. Main topics\n2. Key entities\n3. Sentiment\n\nDocument: ${documentText}`
  }]
});
```

### Pattern 3: Content Generation

```javascript
// Generate content with specific format
const blogPost = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{
    role: 'system',
    content: 'You are a professional blog writer.'
  }, {
    role: 'user',
    content: `Write a blog post about ${topic}. Format:\n# Title\n## Introduction\n## Main Points\n## Conclusion`
  }],
  temperature: 0.8  // Higher creativity for content generation
});
```

### Pattern 4: Data Extraction

```javascript
// Extract structured data from unstructured text
const extracted = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{
    role: 'user',
    content: `Extract the following from this email and return as JSON:\n- Name\n- Email\n- Company\n- Message\n\nEmail: ${emailText}\n\nJSON:`
  }],
  temperature: 0.1  // Low temperature for factual extraction
});

const data = JSON.parse(extracted.response);
```

## Troubleshooting

**Issue**: "Model not found"
- **Solution**: Check model name, ensure it starts with `@cf/`

**Issue**: "Rate limit exceeded"
- **Solution**: Use AI Gateway, implement caching, batch requests

**Issue**: "Embeddings dimension mismatch"
- **Solution**: Ensure Vectorize index dimensions match embedding model (e.g., 768 for bge-base-en-v1.5)

**Issue**: "Timeout on long generation"
- **Solution**: Use streaming, reduce `max_tokens`, or split into smaller requests

**Issue**: "Poor RAG results"
- **Solution**: Improve chunking strategy, increase top-K, add reranking, refine prompts

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/workers-ai-models.md`** - Complete model catalog with specs and use cases
- **`references/rag-architecture-patterns.md`** - RAG implementation patterns and strategies

### Example Files

Working examples in `examples/`:
- **`rag-implementation.js`** - Complete RAG system with Vectorize
- **`text-generation-examples.js`** - Various text generation patterns

### Documentation Links

For the latest Workers AI documentation:
- Workers AI overview: https://developers.cloudflare.com/workers-ai/
- Models: https://developers.cloudflare.com/workers-ai/models/
- AI Gateway: https://developers.cloudflare.com/ai-gateway/

Use the cloudflare-docs-specialist agent to search AI documentation and the workers-ai-specialist agent for implementation guidance.
