---
name: adk-rag-agent
description: Build RAG (Retrieval-Augmented Generation) agents with Google ADK and Vertex AI RAG Engine. Use when implementing document Q&A, knowledge base search, or citation-backed responses. Covers VertexAiRagRetrieval tool, corpus setup, and citation formatting.
---

# Google ADK RAG Agent

Build agents that answer questions from document corpora using Vertex AI RAG Engine.

## Requirements

- Vertex AI backend (not Gemini API)
- Google Cloud project with Vertex AI enabled
- RAG corpus created in Vertex AI

## Environment Variables

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS=projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{CORPUS_ID}
```

## Core Implementation

```python
from google.adk import Agent
from google.adk.tools import VertexAiRagRetrieval

# Configure RAG retrieval tool
rag_tool = VertexAiRagRetrieval(
    name="retrieve_docs",
    description="Retrieve relevant documentation for the question",
    rag_corpus=os.environ["RAG_CORPUS"],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

# Create agent with RAG tool
agent = Agent(
    name="rag_agent",
    model="gemini-2.0-flash-001",
    instruction=INSTRUCTION_PROMPT,
    tools=[rag_tool],
)
```

## Instruction Prompt Pattern

```python
INSTRUCTION_PROMPT = """
You are an AI assistant with access to a specialized document corpus.

RETRIEVAL:
- Use retrieve_docs for specific knowledge questions
- Skip retrieval for casual conversation
- Ask clarifying questions when intent is unclear

SCOPE:
- Only answer questions related to the corpus
- Say "I don't have information about that" for out-of-scope queries

CITATIONS:
- Always cite sources at the end of responses
- Format: [Title](url) or [Document Section](url)
- Consolidate multiple citations from the same source
"""
```

## Corpus Setup

Create corpus via Vertex AI Console or SDK:

```python
from vertexai.preview import rag

# Create corpus
corpus = rag.create_corpus(display_name="my-corpus")

# Import documents (PDF, TXT, HTML)
rag.import_files(
    corpus_name=corpus.name,
    paths=["gs://bucket/doc.pdf"],  # or local files
    chunk_size=512,
    chunk_overlap=100,
)
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `similarity_top_k` | Max chunks to retrieve | 10 |
| `vector_distance_threshold` | Min similarity (0-1, lower=stricter) | 0.6 |
| `chunk_size` | Tokens per chunk at import | 512 |
| `chunk_overlap` | Overlap between chunks | 100 |

## Citation Best Practices

1. Single source → single citation at end
2. Multiple sources → list all citations
3. Same document, multiple chunks → consolidate into one citation
4. Never expose internal chunk IDs to users

## References

- [Corpus setup details](references/corpus-setup.md)
- [Sample repo](https://github.com/google/adk-samples/tree/main/python/agents/RAG)
