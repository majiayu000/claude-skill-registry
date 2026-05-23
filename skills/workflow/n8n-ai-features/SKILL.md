---
name: n8n AI Features
description: AI capabilities in n8n - agents, LangChain, vector stores, LLM providers, RAG, AI workflows
allowed-tools: Read, Write, Edit, WebFetch
---

# n8n AI Features

Build AI-powered automation with n8n's AI nodes and LangChain integration.

## AI Agents

### Available Agent Types

#### Tools Agent
Most flexible - uses tools/functions to complete tasks.
```json
{
  "agent": "toolsAgent",
  "options": {
    "systemMessage": "You are a helpful assistant that can search and analyze data."
  }
}
```
- Best for: General-purpose tasks, API integrations
- Works with: Any tool node (HTTP, database, code)

#### Conversational Agent
Memory-enabled for multi-turn conversations.
```json
{
  "agent": "conversationalAgent",
  "options": {
    "systemMessage": "You are a customer support agent.",
    "maxIterations": 10
  }
}
```
- Best for: Chatbots, support systems
- Works with: Memory nodes for context

#### ReAct Agent
Reasoning + Acting - thinks step-by-step.
```json
{
  "agent": "reAct",
  "options": {
    "maxIterations": 15,
    "returnIntermediateSteps": true
  }
}
```
- Best for: Complex reasoning tasks
- Shows chain-of-thought

#### SQL Agent
Database-focused with schema awareness.
```json
{
  "agent": "sqlAgent",
  "options": {
    "topK": 10,
    "dialect": "postgresql"
  }
}
```
- Best for: Natural language to SQL
- Works with: Database credentials

#### Plan and Execute Agent
Plans first, then executes steps.
```json
{
  "agent": "planAndExecute",
  "options": {
    "humanInputMode": "never"
  }
}
```
- Best for: Multi-step complex tasks
- More deliberate than ReAct

## LangChain Nodes

### Chains

#### Basic LLM Chain
Simple prompt → response.
```
[Chat Trigger] → [Basic LLM Chain] → [Output]
                       ↑
               [OpenAI Chat Model]
```

Configuration:
```json
{
  "promptType": "define",
  "text": "Summarize this text: {{ $json.content }}"
}
```

#### Question and Answer Chain
RAG-based Q&A with context retrieval.
```
[Input] → [Retriever] → [Q&A Chain] → [Answer]
               ↑              ↑
        [Vector Store]  [LLM Model]
```

#### Summarization Chain
Long document summarization.
```json
{
  "type": "map_reduce",
  "options": {
    "chunkSize": 4000
  }
}
```
Types:
- `stuff` - Single pass (short docs)
- `map_reduce` - Chunk and combine (long docs)
- `refine` - Iterative refinement

#### Information Extractor
Structured data extraction from text.
```json
{
  "text": "={{ $json.document }}",
  "schema": {
    "type": "object",
    "properties": {
      "company": {"type": "string"},
      "revenue": {"type": "number"},
      "employees": {"type": "integer"}
    }
  }
}
```

#### Text Classifier
Categorize text into predefined labels.
```json
{
  "categories": ["positive", "negative", "neutral"],
  "text": "={{ $json.review }}"
}
```

#### Sentiment Analysis
Built-in sentiment detection.
```json
{
  "text": "={{ $json.feedback }}",
  "options": {
    "returnScore": true
  }
}
```

## LLM Providers

### OpenAI
```json
{
  "model": "gpt-4-turbo",
  "options": {
    "temperature": 0.7,
    "maxTokens": 2000,
    "topP": 1
  }
}
```
Models: `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`

### Anthropic Claude
```json
{
  "model": "claude-3-opus-20240229",
  "options": {
    "temperature": 0.5,
    "maxTokens": 4096
  }
}
```
Models: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`

### Google Gemini
```json
{
  "model": "gemini-pro",
  "options": {
    "temperature": 0.7
  }
}
```

### Ollama (Local)
```json
{
  "baseUrl": "http://localhost:11434",
  "model": "llama2",
  "options": {
    "temperature": 0.8
  }
}
```
- Self-hosted, no API costs
- Models: llama2, mistral, codellama, etc.

### Groq
```json
{
  "model": "mixtral-8x7b-32768",
  "options": {
    "temperature": 0.5
  }
}
```
- Ultra-fast inference
- Good for high-volume

### Mistral
```json
{
  "model": "mistral-large-latest",
  "options": {
    "temperature": 0.7
  }
}
```

## Vector Stores

### Supabase Vector
```json
{
  "tableName": "documents",
  "queryName": "match_documents",
  "options": {
    "matchThreshold": 0.8,
    "matchCount": 5
  }
}
```

Setup:
```sql
-- Enable pgvector extension
create extension if not exists vector;

-- Create documents table
create table documents (
  id uuid primary key default gen_random_uuid(),
  content text,
  metadata jsonb,
  embedding vector(1536)
);

-- Create matching function
create function match_documents(
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (id uuid, content text, similarity float)
language sql stable
as $$
  select id, content, 1 - (embedding <=> query_embedding) as similarity
  from documents
  where 1 - (embedding <=> query_embedding) > match_threshold
  order by embedding <=> query_embedding
  limit match_count;
$$;
```

### Pinecone
```json
{
  "indexName": "my-index",
  "namespace": "documents",
  "options": {
    "topK": 5
  }
}
```

### Qdrant
```json
{
  "collectionName": "documents",
  "url": "http://localhost:6333",
  "options": {
    "limit": 10,
    "scoreThreshold": 0.7
  }
}
```

### PGVector
```json
{
  "tableName": "embeddings",
  "options": {
    "distanceStrategy": "cosine",
    "k": 5
  }
}
```

### In-Memory Vector Store
```json
{
  "memoryKey": "document_store"
}
```
- Good for prototyping
- Lost on restart

## Embeddings

### OpenAI Embeddings
```json
{
  "model": "text-embedding-3-small",
  "options": {
    "batchSize": 512,
    "stripNewLines": true
  }
}
```
Models:
- `text-embedding-3-small` (1536 dims, cheaper)
- `text-embedding-3-large` (3072 dims, better)
- `text-embedding-ada-002` (legacy)

### Cohere Embeddings
```json
{
  "model": "embed-english-v3.0",
  "inputType": "search_document"
}
```

### Ollama Embeddings (Local)
```json
{
  "baseUrl": "http://localhost:11434",
  "model": "nomic-embed-text"
}
```

## Memory Nodes

### Buffer Memory
Simple conversation history.
```json
{
  "sessionKey": "={{ $json.userId }}",
  "contextWindowLength": 10
}
```

### Buffer Window Memory
Limited window of recent messages.
```json
{
  "sessionKey": "chat_{{ $json.sessionId }}",
  "windowSize": 5
}
```

### Motorhead Memory
External memory service.
```json
{
  "url": "http://localhost:8080",
  "sessionId": "={{ $json.userId }}"
}
```

### Zep Memory
Advanced memory with search.
```json
{
  "baseUrl": "http://localhost:8000",
  "sessionId": "user_123"
}
```

## RAG (Retrieval-Augmented Generation)

### Basic RAG Pattern
```
[Document Loader] → [Text Splitter] → [Embeddings] → [Vector Store]
                                                           ↓
[User Query] → [Retriever] → [Context + Query] → [LLM] → [Response]
```

### Document Loading
```
[HTTP Request] → [Extract Text] → [Text Splitter]
[Read File] → [Extract PDF] → [Text Splitter]
[Google Drive] → [Download] → [Text Splitter]
```

### Text Splitters

#### Character Text Splitter
```json
{
  "chunkSize": 1000,
  "chunkOverlap": 200,
  "separator": "\n\n"
}
```

#### Recursive Character Splitter
```json
{
  "chunkSize": 1000,
  "chunkOverlap": 200,
  "separators": ["\n\n", "\n", ". ", " "]
}
```
- Better for preserving context
- Tries larger separators first

#### Token Splitter
```json
{
  "chunkSize": 500,
  "chunkOverlap": 50,
  "encodingName": "cl100k_base"
}
```
- Token-accurate for LLM context

### Retrieval Configuration
```json
{
  "topK": 5,
  "scoreThreshold": 0.7,
  "searchType": "similarity"
}
```
Search types:
- `similarity` - Cosine similarity
- `mmr` - Maximum Marginal Relevance (diversity)

## AI Workflow Patterns

### Chatbot with Memory
```
[Chat Trigger]
      ↓
[Buffer Memory] ←→ [Conversational Agent]
                          ↓
                   [OpenAI Model]
                          ↓
                   [Response]
```

### Document Q&A System
```
[Webhook: /upload]           [Webhook: /query]
      ↓                            ↓
[PDF Extract]                [Supabase Retriever]
      ↓                            ↓
[Text Splitter]              [Q&A Chain]
      ↓                            ↓
[Embeddings]                 [OpenAI Model]
      ↓                            ↓
[Supabase Store]             [Response]
```

### Content Generation Pipeline
```
[Schedule: Daily]
      ↓
[HTTP: Get Topics] → [For Each Topic]
                          ↓
                   [Basic LLM Chain: Generate Article]
                          ↓
                   [Basic LLM Chain: Edit/Refine]
                          ↓
                   [HTTP: Post to CMS]
```

### AI-Powered Data Processing
```
[Webhook: Data Input]
      ↓
[Information Extractor]
      ↓
[Code: Validate/Transform]
      ↓
[If: Confidence > 0.8]
      ↓
[Database: Insert]
```

### Multi-Model Routing
```
[Input]
   ↓
[Text Classifier: Complexity]
   ↓
[Switch]
   ├→ simple → [GPT-3.5]
   ├→ medium → [GPT-4-Turbo]
   └→ complex → [Claude Opus]
         ↓
     [Merge]
         ↓
     [Output]
```

## MCP (Model Context Protocol) Integration

### MCP Client Node
Connect to MCP servers for extended capabilities.
```json
{
  "serverUrl": "http://localhost:3000/mcp",
  "tools": ["web_search", "calculator", "code_interpreter"]
}
```

## Best Practices

### 1. Prompt Engineering
```javascript
// Use structured prompts
const systemPrompt = `You are a helpful assistant.

RULES:
1. Be concise
2. Use bullet points
3. Cite sources

FORMAT:
- Summary: [brief answer]
- Details: [expanded explanation]
- Sources: [references]`;
```

### 2. Temperature Settings
| Use Case | Temperature |
|----------|-------------|
| Factual Q&A | 0.0 - 0.3 |
| Summarization | 0.3 - 0.5 |
| Creative writing | 0.7 - 0.9 |
| Brainstorming | 0.9 - 1.0 |

### 3. Token Management
- Monitor token usage per execution
- Use summarization for long contexts
- Implement chunking for large documents
- Cache embeddings to reduce API calls

### 4. Error Handling
```
[AI Node]
   ↓ (on error)
[Error Trigger]
   ↓
[Fallback Response]
   ↓
[Log Error]
```

### 5. Cost Optimization
- Use smaller models for simple tasks
- Cache frequent queries
- Batch similar requests
- Use local models (Ollama) for development

## Output Format
```
AI WORKFLOW:
  Purpose: [What it automates]
  LLM: [Model choice and why]
  Vector Store: [If RAG, which store]

NODES:
  1. [Trigger] - [Configuration]
  2. [AI Node] - [Model, temperature, prompt]
  ...

PROMPT TEMPLATE:
  System: [System message]
  User: [User message template]

CONSIDERATIONS:
  - Tokens: [Estimated usage]
  - Cost: [Per execution estimate]
  - Latency: [Expected response time]
```
