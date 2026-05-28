---
name: research-ai-sdk
description: Research Vercel AI SDK patterns, streaming, and multi-provider integration using Exa code search and Ref documentation
---

# Research Vercel AI SDK Patterns

Use this skill when you need to:
- Learn AI SDK streaming patterns
- Understand multi-provider integration (Anthropic, OpenAI, Google, etc.)
- Research tool calling and function execution
- Find structured output patterns
- Learn RAG (Retrieval Augmented Generation) patterns

## Process

1. **Identify AI Use Case**
   - Text generation, streaming, or structured output?
   - Tool calling or function execution?
   - Multi-modal (text, images, audio)?
   - Which provider (Anthropic, OpenAI, Google, etc.)?

2. **Search Documentation (Ref)**
   ```
   Query patterns:
   - "Vercel AI SDK [feature]"
   - "AI SDK streaming response"
   - "AI SDK tools function calling"
   - "AI SDK structured output Zod"
   ```

3. **Find Implementation Examples (Exa)**
   ```
   Query patterns:
   - "Vercel AI SDK streaming React component example"
   - "AI SDK tool calling Next.js server action"
   - "AI SDK Anthropic Claude function execution"
   - "AI SDK structured output Zod schema validation"
   ```

4. **Consider Project Stack**
   - Integration with Next.js Server Components/Actions
   - Type safety with TypeScript and Zod
   - Provider selection based on use case

## Common Research Topics

### Streaming
```typescript
// Documentation
Query: "Vercel AI SDK streaming response useChat"

// Code examples
Query: "AI SDK streamText Next.js route handler streaming response"
```

### Tool Calling
```typescript
// Documentation
Query: "AI SDK tools function calling schema"

// Code examples
Query: "AI SDK tool execution Zod schema Next.js example"
```

### Multi-Provider
```typescript
// Documentation
Query: "AI SDK provider abstraction Anthropic OpenAI"

// Code examples
Query: "AI SDK switch providers Claude GPT-4 configuration example"
```

### Structured Output
```typescript
// Documentation
Query: "AI SDK structured output generateObject Zod"

// Code examples
Query: "AI SDK generateObject Zod schema typed response example"
```

### RAG Patterns
```typescript
// Documentation
Query: "AI SDK embeddings vector search RAG"

// Code examples
Query: "AI SDK RAG pattern document retrieval context injection example"
```

## Provider-Specific Research

### Anthropic (Claude)
```typescript
Query: "AI SDK Anthropic Claude tool use streaming example"
Query: "AI SDK Claude 3.5 Sonnet function calling"
```

### OpenAI (GPT)
```typescript
Query: "AI SDK OpenAI GPT-4 function calling example"
Query: "AI SDK OpenAI streaming response Next.js"
```

### Google (Gemini)
```typescript
Query: "AI SDK Google Gemini multi-modal example"
Query: "AI SDK Gemini function calling tools"
```

## React Integration

### useChat Hook
```typescript
// Documentation
Query: "AI SDK useChat hook React"

// Code examples
Query: "AI SDK useChat streaming messages Next.js example"
```

### useCompletion Hook
```typescript
// Documentation
Query: "AI SDK useCompletion hook"

// Code examples
Query: "AI SDK useCompletion text generation form example"
```

### Server Actions
```typescript
// Documentation
Query: "AI SDK Next.js server actions generateText"

// Code examples
Query: "AI SDK server action form submission AI response example"
```

## Advanced Patterns

### Context Management
```
Query: "AI SDK conversation history context management example"
```

### Error Handling
```
Query: "AI SDK error handling retry fallback provider example"
```

### Streaming with Tools
```
Query: "AI SDK streaming tool calls partial results example"
```

### Multi-step Agents
```
Query: "AI SDK agent pattern multiple tool calls reasoning example"
```

## Output Format

Provide:
1. **Feature explanation** - How the AI SDK feature works
2. **Code examples** - Real implementations from Exa
3. **Provider comparison** - When to use which provider
4. **Type safety** - Zod schemas and TypeScript integration
5. **Best practices** - Error handling, rate limiting, costs
6. **Integration guide** - How to implement in this project

## Project Context

Your project uses:
- Vercel AI SDK 5.0.51
- Multiple providers: Anthropic, OpenAI, Google, Groq, Mistral, XAI
- Next.js 15 Server Components and Actions
- TypeScript with Zod validation
- React 19 with streaming

## Common Use Cases

### Chat Interface
```
Research: "AI SDK useChat streaming Next.js chat interface"
```

### Document Analysis
```
Research: "AI SDK document analysis tool calling structured output"
```

### Content Generation
```
Research: "AI SDK generateText streaming content generation"
```

### Code Generation
```
Research: "AI SDK code generation Anthropic Claude structured output"
```

## When to Use

- Implementing AI features
- Choosing AI providers
- Setting up streaming responses
- Creating tool/function calling
- Optimizing AI performance
- Debugging AI integrations
- Learning new AI SDK features

## Related Skills

- research-nextjs (for Next.js integration)
- research-react (for React hooks)
- research-typescript (for type safety)
