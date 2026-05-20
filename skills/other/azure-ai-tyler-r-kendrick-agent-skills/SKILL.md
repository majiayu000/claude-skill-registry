---
name: azure-ai
description: "Use for Azure AI: Search, Speech, Foundry, OpenAI, Document Intelligence. Helps with search, vector/hybrid search, speech-to-text, text-to-speech, transcription, AI agents, prompt flows, OCR. USE FOR: AI Search, query search, vector search, hybrid search, semantic search, speech-to-text, text-to-speech, transcribe, AI agent, prompt flow, Foundry, OCR, convert text to speech. DO NOT USE FOR: Function apps/Functions (use azure-functions), databases (azure-postgres/azure-kusto), resources."
---

# Azure AI Services

## Services

| Service | Use When | MCP Tools | CLI |
|---------|----------|-----------|-----|
| AI Search | Full-text, vector, hybrid search | `azure__search` | `az search` |
| Speech | Speech-to-text, text-to-speech | `azure__speech` | - |
| Foundry | AI models, agents, prompt flows | `azure__foundry` | `az ml` |
| OpenAI | GPT models, embeddings, DALL-E | - | `az cognitiveservices` |
| Document Intelligence | Form extraction, OCR | - | - |

## MCP Server (Preferred)

When Azure MCP is enabled:

### AI Search
- `azure__search` with command `search_index_list` - List search indexes
- `azure__search` with command `search_index_get` - Get index details
- `azure__search` with command `search_query` - Query search index

### Speech
- `azure__speech` with command `speech_transcribe` - Speech to text
- `azure__speech` with command `speech_synthesize` - Text to speech

### Foundry
- `azure__foundry` with command `foundry_model_list` - List AI models
- `azure__foundry` with command `foundry_deployment_list` - List deployments
- `azure__foundry` with command `foundry_agent_list` - List AI agents

**If Azure MCP is not enabled:** Run `/azure:setup` or enable via `/mcp`.

## AI Search Capabilities

| Feature | Description |
|---------|-------------|
| Full-text search | Linguistic analysis, stemming |
| Vector search | Semantic similarity with embeddings |
| Hybrid search | Combined keyword + vector |
| AI enrichment | Entity extraction, OCR, sentiment |

## Speech Capabilities

| Feature | Description |
|---------|-------------|
| Speech-to-text | Real-time and batch transcription |
| Text-to-speech | Neural voices, SSML support |
| Speaker diarization | Identify who spoke when |
| Custom models | Domain-specific vocabulary |

## Foundry Capabilities

| Feature | Description |
|---------|-------------|
| Model catalog | GPT-4, Llama, Mistral, custom |
| AI agents | Multi-turn, tool calling, RAG |
| Prompt flow | Orchestration, evaluation |
| Fine-tuning | Custom model training |

## Service Details

For deep documentation on specific services:

- AI Search indexing and queries -> [Azure AI Search documentation](https://learn.microsoft.com/azure/search/search-what-is-azure-search)
- Speech transcription patterns -> [Azure AI Speech documentation](https://learn.microsoft.com/azure/ai-services/speech-service/overview)
- Foundry agents and flows -> [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-studio/what-is-ai-studio)
