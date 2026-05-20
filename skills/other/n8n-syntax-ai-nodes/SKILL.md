---
name: n8n-syntax-ai-nodes
description: >
  Use when building AI or LLM workflows in n8n v1.x (v1.19.4+). Prevents
  incorrect sub-node wiring by mismatching NodeConnectionTypes. Covers agent
  nodes (6 types), chain nodes, tool nodes, memory backends (8 types), vector
  stores (11 types), output parsers, text splitters, retrievers, AI sub-node
  connections (12 NodeConnectionTypes), langchain integration, RAG patterns,
  and human-in-the-loop.
  Keywords: n8n, AI nodes, LLM, langchain, RAG, vector store, agents.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x (v1.19.4+ for AI features)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n AI/LLM Cluster Node System

> n8n integrates with LangChain to provide advanced AI capabilities via a **cluster node architecture** — root nodes connected to specialized sub-nodes through typed connectors. Requires n8n v1.19.4+.

## Quick Reference

### Cluster Node Architecture

AI workflows in n8n use **root nodes** (agents, chains) connected to **sub-nodes** (models, memory, tools) through typed AI connectors. Root nodes NEVER work alone — they ALWAYS require at least one Chat Model sub-node.

```
┌─────────────────────────────────────────────────┐
│  ROOT NODE (Agent/Chain)                        │
│  ┌──────────┬──────────┬──────────┬───────────┐ │
│  │ai_language│ai_memory │ai_tool   │ai_output  │ │
│  │Model     │          │          │Parser     │ │
│  └────┬─────┴────┬─────┴────┬─────┴─────┬─────┘ │
└───────┼──────────┼──────────┼───────────┼───────┘
        │          │          │           │
   ┌────▼────┐ ┌──▼───┐ ┌───▼────┐ ┌───▼──────┐
   │Chat     │ │Memory│ │Tool    │ │Output    │
   │Model    │ │Node  │ │Node(s) │ │Parser    │
   └─────────┘ └──────┘ └────────┘ └──────────┘
```

### AI Node Type Reference

| Category | Nodes | Purpose |
|----------|-------|---------|
| **Agents** | Conversational, OpenAI Functions, Plan and Execute, ReAct, SQL, Tools Agent | Autonomous reasoning + tool use |
| **Chains** | Basic LLM, Summarization, Retrieval QA | Linear prompt-response pipelines |
| **Specialized** | Information Extractor, Text Classifier, Sentiment Analysis, LangChain Code | Task-specific AI operations |
| **Chat Models** | OpenAI, Anthropic, Azure OpenAI, Google Gemini, Groq, Ollama, Mistral, + more | LLM provider connections |
| **Memory** | Simple, Window Buffer, Token Buffer, Summary, PostgresChat, Redis, Xata, Zep | Conversation state persistence |
| **Vector Stores** | Pinecone, Qdrant, Supabase, PGVector, Chroma, Weaviate, In-Memory, Milvus, MongoDB Atlas, Azure AI Search, Redis | Vector similarity search backends |
| **Embeddings** | OpenAI, Cohere, Google, HuggingFace, Mistral, Ollama, Azure OpenAI | Text-to-vector conversion |
| **Text Splitters** | Character, Recursive Character, Token | Document chunking for RAG |
| **Output Parsers** | Structured, Auto-fixing, Item List | Response format enforcement |
| **Retrievers** | Vector Store, MultiQuery, Contextual Compression, Workflow | Document retrieval strategies |
| **Tools** | Calculator, Custom Code Tool, SearXNG, SerpApi, Wikipedia, Wolfram Alpha, Vector Store Q&A | Agent capabilities |

### Sub-Node Connection Types (NodeConnectionType)

| Connection Type | Constant | Connects To |
|----------------|----------|-------------|
| `ai_agent` | `NodeConnectionTypes.AiAgent` | Agent sub-nodes |
| `ai_chain` | `NodeConnectionTypes.AiChain` | Chain sub-nodes |
| `ai_document` | `NodeConnectionTypes.AiDocument` | Document loaders |
| `ai_embedding` | `NodeConnectionTypes.AiEmbedding` | Embedding models |
| `ai_languageModel` | `NodeConnectionTypes.AiLanguageModel` | Chat/LLM models |
| `ai_memory` | `NodeConnectionTypes.AiMemory` | Memory backends |
| `ai_outputParser` | `NodeConnectionTypes.AiOutputParser` | Output parsers |
| `ai_retriever` | `NodeConnectionTypes.AiRetriever` | Retrievers |
| `ai_reranker` | `NodeConnectionTypes.AiReranker` | Reranking models |
| `ai_textSplitter` | `NodeConnectionTypes.AiTextSplitter` | Text splitters |
| `ai_tool` | `NodeConnectionTypes.AiTool` | Agent tools |
| `ai_vectorStore` | `NodeConnectionTypes.AiVectorStore` | Vector stores |

---

## Decision Trees

### Which Agent Type to Use

```
Need autonomous AI reasoning?
├─ YES: Does the task require tool use?
│  ├─ YES: Which provider?
│  │  ├─ OpenAI with function calling → OpenAI Functions Agent
│  │  ├─ Any provider, general tools → Tools Agent (RECOMMENDED default)
│  │  └─ Need step-by-step planning → Plan and Execute Agent
│  └─ NO: Simple conversation?
│     ├─ YES → Conversational Agent
│     └─ NO: Need reasoning trace? → ReAct Agent
├─ Database queries? → SQL Agent
└─ NO: Simple prompt-response?
   ├─ Single prompt → Basic LLM Chain
   ├─ Summarize text → Summarization Chain
   └─ Q&A over documents → Retrieval QA Chain
```

**Rule**: ALWAYS start with **Tools Agent** unless you have a specific reason to use another type. It is the most flexible and works with any chat model provider.

### Which Memory Type to Use

```
Need conversation memory?
├─ NO → Skip memory sub-node entirely
├─ YES: Persistence required?
│  ├─ NO (in-memory only):
│  │  ├─ Simple buffer → Simple Memory (default 5 exchanges)
│  │  └─ Token-limited → Token Buffer Memory
│  └─ YES (survives restarts):
│     ├─ PostgreSQL available → PostgresChat Memory
│     ├─ Redis available → Redis Chat Memory
│     ├─ Need summarization → Summary Memory
│     └─ Managed service → Zep or Xata Memory
```

### Which Vector Store to Use

```
Need vector similarity search?
├─ Testing/prototyping → In-Memory Vector Store
├─ Production:
│  ├─ Managed cloud service:
│  │  ├─ Pinecone (fully managed, scalable)
│  │  ├─ Qdrant (open-source, self-hostable)
│  │  ├─ Weaviate (hybrid search)
│  │  └─ Azure AI Search (Azure ecosystem)
│  ├─ Existing database:
│  │  ├─ PostgreSQL → PGVector
│  │  ├─ Supabase → Supabase Vector Store
│  │  ├─ MongoDB → MongoDB Atlas
│  │  └─ Redis → Redis Vector Store
│  └─ Self-hosted → Chroma or Milvus
```

---

## Core Patterns

### Pattern 1: Basic Agent Workflow

```
[Trigger] → [Tools Agent]
                ├── ai_languageModel → [OpenAI Chat Model]
                ├── ai_memory → [Simple Memory]
                └── ai_tool → [Calculator]
                             [Wikipedia]
                             [Custom Code Tool]
```

ALWAYS connect at least one Chat Model sub-node. NEVER leave the `ai_languageModel` connector empty.

### Pattern 2: RAG Data Insertion

```
[Trigger] → [Get Documents] → [Vector Store (Insert Documents)]
                                  ├── ai_embedding → [OpenAI Embeddings]
                                  └── ai_document → [Default Data Loader]
                                                       └── ai_textSplitter → [Recursive Character Text Splitter]
```

ALWAYS use a text splitter when inserting documents. NEVER insert full documents without splitting — it degrades retrieval quality.

**Text splitting guidance:**
- ALWAYS use Recursive Character Text Splitter as the default choice
- Use chunk sizes of 200-500 tokens for fine-grained retrieval
- ALWAYS set overlap (10-20% of chunk size) to preserve context across boundaries

### Pattern 3: RAG Retrieval via Agent

```
[Chat Trigger] → [Tools Agent]
                     ├── ai_languageModel → [OpenAI Chat Model]
                     ├── ai_memory → [Postgres Chat Memory]
                     └── ai_tool → [Vector Store Q&A Tool]
                                       └── ai_vectorStore → [Pinecone]
                                                               └── ai_embedding → [OpenAI Embeddings]
```

### Pattern 4: RAG Retrieval via Chain

```
[Chat Trigger] → [Retrieval QA Chain]
                     ├── ai_languageModel → [OpenAI Chat Model]
                     └── ai_retriever → [Vector Store Retriever]
                                            └── ai_vectorStore → [PGVector]
                                                                    └── ai_embedding → [OpenAI Embeddings]
```

### Pattern 5: Human-in-the-Loop

```
[Chat Trigger] → [Tools Agent]
                     ├── ai_languageModel → [Chat Model]
                     └── ai_tool → [Tool with Approval]
                                       ├── Approve → [Execute Action]
                                       └── Deny → [Notify User]
```

- 9 notification channels: Chat, Slack, Discord, Telegram, Microsoft Teams, Gmail, WhatsApp, Google Chat, Microsoft Outlook
- Access tool context: `$tool.name` (tool identifier), `$tool.parameters` (AI-determined values)
- Use `$fromAI()` for dynamic parameter specification in tool nodes
- ALWAYS include human review information in the system prompt so the AI understands the approval workflow

---

## Critical Rules

### ALWAYS
- ALWAYS connect a Chat Model sub-node to every agent and chain root node
- ALWAYS use the same embedding model for insertion AND retrieval in RAG workflows
- ALWAYS use Recursive Character Text Splitter unless you have a specific reason not to
- ALWAYS set chunk overlap when splitting documents for RAG
- ALWAYS use Tools Agent as the default agent type
- ALWAYS include a system prompt that describes available tools and expected behavior
- ALWAYS test AI workflows with pinned data before activating in production

### NEVER
- NEVER mix embedding models between insertion and retrieval — vectors become incompatible
- NEVER skip text splitting when inserting documents into vector stores
- NEVER connect sub-nodes to incompatible connector types (e.g., a memory node to an `ai_tool` connector)
- NEVER use Basic LLM Chain when you need tool use — use an Agent instead
- NEVER store sensitive data in AI memory without considering data retention policies
- NEVER use In-Memory Vector Store in production — data is lost on restart
- NEVER assume AI agent output is deterministic — ALWAYS validate critical outputs

---

## Sub-Node Connection Rules

| Root Node Type | Required Connections | Optional Connections |
|---------------|---------------------|---------------------|
| Tools Agent | `ai_languageModel` | `ai_memory`, `ai_tool`, `ai_outputParser` |
| OpenAI Functions Agent | `ai_languageModel` (OpenAI only) | `ai_memory`, `ai_tool`, `ai_outputParser` |
| Conversational Agent | `ai_languageModel` | `ai_memory`, `ai_tool`, `ai_outputParser` |
| ReAct Agent | `ai_languageModel` | `ai_memory`, `ai_tool`, `ai_outputParser` |
| Plan and Execute Agent | `ai_languageModel` | `ai_memory`, `ai_tool`, `ai_outputParser` |
| SQL Agent | `ai_languageModel` | `ai_memory` |
| Basic LLM Chain | `ai_languageModel` | `ai_outputParser`, `ai_memory` |
| Summarization Chain | `ai_languageModel` | — |
| Retrieval QA Chain | `ai_languageModel`, `ai_retriever` | — |
| Vector Store (Insert) | `ai_embedding`, `ai_document` | — |
| Vector Store (Retrieve) | `ai_embedding` | — |

---

## `supplyData()` Method

AI sub-nodes implement `supplyData()` instead of `execute()`. This method returns the LangChain object (model, memory, tool, etc.) that the root node consumes:

```typescript
// AI sub-node pattern (e.g., a memory node)
async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
    const memory = new BufferMemory({ /* config */ });
    return { response: memory };
}
```

Root nodes call `getInputConnectionData()` to retrieve sub-node outputs:

```typescript
// Inside agent/chain root node
const model = await this.getInputConnectionData('ai_languageModel', itemIndex);
const memory = await this.getInputConnectionData('ai_memory', itemIndex);
const tools = await this.getInputConnectionData('ai_tool', itemIndex);
```

---

## LangChain Code Node

The LangChain Code node provides special built-in methods for custom LangChain operations. These methods are ONLY available in the LangChain Code node, NOT in regular Code nodes.

Use the LangChain Code node when:
- Built-in AI nodes do not cover your use case
- You need custom LangChain chain composition
- You need advanced prompt engineering beyond what the UI supports

---

## Reference Links

- [AI Node Types and Methods](references/methods.md) — Complete node catalog with providers and parameters
- [AI Workflow Examples](references/examples.md) — Agent, RAG, and tool usage workflow patterns
- [AI Anti-Patterns](references/anti-patterns.md) — Common mistakes and how to avoid them
