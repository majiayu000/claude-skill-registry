---
name: mistral-core-workflow-b
description: |
  Execute Mistral AI secondary workflows: Embeddings and Function Calling.
  Use when implementing semantic search, RAG applications,
  or tool-augmented LLM interactions.
  Trigger with phrases like "mistral embeddings", "mistral function calling",
  "mistral tools", "mistral RAG", "mistral semantic search".
allowed-tools: Read, Write, Edit, Bash(npm:*), Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI Core Workflow B: Embeddings & Function Calling

## Overview
Secondary workflows for Mistral AI: Text embeddings for semantic search and function calling for tool use.

## Prerequisites
- Completed `mistral-install-auth` setup
- Familiarity with `mistral-core-workflow-a`
- Valid API credentials configured

## Embeddings

### Step 1: Generate Text Embeddings

```typescript
import Mistral from '@mistralai/mistralai';

const client = new Mistral({
  apiKey: process.env.MISTRAL_API_KEY,
});

async function getEmbedding(text: string): Promise<number[]> {
  const response = await client.embeddings.create({
    model: 'mistral-embed',
    inputs: [text],
  });

  return response.data[0].embedding;
}

// Usage
const embedding = await getEmbedding('Machine learning is fascinating.');
console.log(`Embedding dimensions: ${embedding.length}`); // 1024
```

### Step 2: Batch Embeddings

```typescript
async function getBatchEmbeddings(texts: string[]): Promise<number[][]> {
  const response = await client.embeddings.create({
    model: 'mistral-embed',
    inputs: texts,
  });

  return response.data.map(d => d.embedding);
}

// Usage
const documents = [
  'Python is a programming language.',
  'JavaScript runs in browsers.',
  'Rust is memory safe.',
];
const embeddings = await getBatchEmbeddings(documents);
```

### Step 3: Semantic Search Implementation

```typescript
function cosineSimilarity(a: number[], b: number[]): number {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

interface Document {
  id: string;
  text: string;
  embedding?: number[];
}

class SemanticSearch {
  private documents: Document[] = [];
  private client: Mistral;

  constructor() {
    this.client = new Mistral({ apiKey: process.env.MISTRAL_API_KEY });
  }

  async indexDocuments(docs: Omit<Document, 'embedding'>[]): Promise<void> {
    const texts = docs.map(d => d.text);
    const response = await this.client.embeddings.create({
      model: 'mistral-embed',
      inputs: texts,
    });

    this.documents = docs.map((doc, i) => ({
      ...doc,
      embedding: response.data[i].embedding,
    }));
  }

  async search(query: string, topK = 5): Promise<Array<Document & { score: number }>> {
    const queryEmbedding = await this.getEmbedding(query);

    const results = this.documents
      .map(doc => ({
        ...doc,
        score: cosineSimilarity(queryEmbedding, doc.embedding!),
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);

    return results;
  }

  private async getEmbedding(text: string): Promise<number[]> {
    const response = await this.client.embeddings.create({
      model: 'mistral-embed',
      inputs: [text],
    });
    return response.data[0].embedding;
  }
}

// Usage
const search = new SemanticSearch();
await search.indexDocuments([
  { id: '1', text: 'How to bake chocolate chip cookies' },
  { id: '2', text: 'Machine learning fundamentals' },
  { id: '3', text: 'Best practices for React development' },
]);

const results = await search.search('AI tutorials', 2);
// Returns documents sorted by semantic similarity
```

## Function Calling

### Step 4: Define Tools

```typescript
interface Tool {
  type: 'function';
  function: {
    name: string;
    description: string;
    parameters: {
      type: 'object';
      properties: Record<string, { type: string; description: string }>;
      required: string[];
    };
  };
}

const tools: Tool[] = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get the current weather for a location',
      parameters: {
        type: 'object',
        properties: {
          location: {
            type: 'string',
            description: 'City and country, e.g., "London, UK"',
          },
          unit: {
            type: 'string',
            description: 'Temperature unit: "celsius" or "fahrenheit"',
          },
        },
        required: ['location'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'search_web',
      description: 'Search the web for information',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'The search query',
          },
        },
        required: ['query'],
      },
    },
  },
];
```

### Step 5: Implement Function Calling Loop

```typescript
import Mistral from '@mistralai/mistralai';

const client = new Mistral({
  apiKey: process.env.MISTRAL_API_KEY,
});

// Tool implementations
const toolFunctions: Record<string, (args: any) => Promise<string>> = {
  get_weather: async ({ location, unit = 'celsius' }) => {
    // Simulated weather API call
    return JSON.stringify({
      location,
      temperature: unit === 'celsius' ? 22 : 72,
      unit,
      condition: 'sunny',
    });
  },
  search_web: async ({ query }) => {
    // Simulated web search
    return JSON.stringify({
      results: [
        { title: `Result for: ${query}`, url: 'https://example.com' },
      ],
    });
  },
};

async function chatWithTools(userMessage: string): Promise<string> {
  const messages: any[] = [
    { role: 'user', content: userMessage },
  ];

  while (true) {
    const response = await client.chat.complete({
      model: 'mistral-large-latest',
      messages,
      tools,
      toolChoice: 'auto',
    });

    const choice = response.choices?.[0];
    const assistantMessage = choice?.message;

    if (!assistantMessage) {
      throw new Error('No response from model');
    }

    // Add assistant message to conversation
    messages.push(assistantMessage);

    // Check if model wants to call tools
    const toolCalls = assistantMessage.toolCalls;

    if (!toolCalls || toolCalls.length === 0) {
      // No tool calls, return final response
      return assistantMessage.content ?? '';
    }

    // Execute tool calls
    for (const toolCall of toolCalls) {
      const functionName = toolCall.function.name;
      const functionArgs = JSON.parse(toolCall.function.arguments);

      console.log(`Calling tool: ${functionName}`, functionArgs);

      const toolFn = toolFunctions[functionName];
      if (!toolFn) {
        throw new Error(`Unknown tool: ${functionName}`);
      }

      const result = await toolFn(functionArgs);

      // Add tool result to conversation
      messages.push({
        role: 'tool',
        name: functionName,
        content: result,
        toolCallId: toolCall.id,
      });
    }
  }
}

// Usage
const answer = await chatWithTools('What is the weather in Paris?');
console.log(answer);
// "The current weather in Paris is sunny with a temperature of 22°C."
```

### Step 6: RAG (Retrieval-Augmented Generation)

```typescript
class RAGChat {
  private search: SemanticSearch;
  private client: Mistral;

  constructor() {
    this.search = new SemanticSearch();
    this.client = new Mistral({ apiKey: process.env.MISTRAL_API_KEY });
  }

  async indexKnowledge(documents: { id: string; text: string }[]): Promise<void> {
    await this.search.indexDocuments(documents);
  }

  async chat(userQuery: string): Promise<string> {
    // Retrieve relevant documents
    const relevantDocs = await this.search.search(userQuery, 3);

    // Build context from retrieved documents
    const context = relevantDocs
      .map(doc => `[Source ${doc.id}]: ${doc.text}`)
      .join('\n\n');

    // Generate response with context
    const response = await this.client.chat.complete({
      model: 'mistral-small-latest',
      messages: [
        {
          role: 'system',
          content: `Answer questions based on the provided context. If the answer is not in the context, say so.

Context:
${context}`,
        },
        { role: 'user', content: userQuery },
      ],
    });

    return response.choices?.[0]?.message?.content ?? '';
  }
}

// Usage
const rag = new RAGChat();
await rag.indexKnowledge([
  { id: '1', text: 'Mistral AI was founded in 2023 in Paris, France.' },
  { id: '2', text: 'The mistral-embed model produces 1024-dimensional vectors.' },
]);

const answer = await rag.chat('When was Mistral AI founded?');
```

## Output
- Text embeddings (1024 dimensions)
- Semantic search implementation
- Function calling with tool execution
- RAG chat with retrieval

## Error Handling
| Aspect | Workflow A | Workflow B |
|--------|------------|------------|
| Use Case | Chat/Text Generation | Embeddings/Tools |
| Models | All chat models | mistral-embed + large |
| Complexity | Lower | Medium-Higher |
| Latency | Depends on tokens | Batching helps |

## Examples

### Python Embeddings
```python
import os
from mistralai import Mistral

client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=texts,
    )
    return [d.embedding for d in response.data]
```

### Python Function Calling
```python
import json
from mistralai import Mistral

client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"
)
```

## Resources
- [Mistral AI Embeddings](https://docs.mistral.ai/capabilities/embeddings/)
- [Mistral AI Function Calling](https://docs.mistral.ai/capabilities/function_calling/)
- [Mistral AI Agents](https://docs.mistral.ai/capabilities/agents/)

## Next Steps
For common errors, see `mistral-common-errors`.
