---
name: weaviate-rag
description: Implement RAG systems using Weaviate vector database. Use when building semantic search, document retrieval, or knowledge base systems.
allowed-tools: Read, Write, Grep, Glob
---

# Weaviate RAG Configuration Skill

Configure MoodleNRW RAG system with Weaviate vector store.

## Trigger
- RAG system setup or troubleshooting
- Vector store configuration
- Document embedding requests

## Running Services
- **Weaviate HTTP**: `localhost:8095`
- **Weaviate gRPC**: `localhost:50055`
- **Chainlit UI**: `localhost:8000`

## Server Paths
- **RAG System**: `/opt/cloodle/tools/ai/multi_agent_rag_system/`
- **Chatbot**: `/opt/cloodle/tools/ai/moodle-chatbot/`

## Weaviate Client Configuration
```python
import weaviate

client = weaviate.Client(
    url="http://localhost:8095",
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY", "")
    }
)
```

## Docker Commands
```bash
# Start Weaviate
cd /opt/cloodle/tools/ai/multi_agent_rag_system
docker-compose up -d

# Check status
docker ps | grep weaviate

# View logs
docker logs multi_agent_rag_system_weaviate_1
```

## Schema Creation
```python
schema = {
    "class": "MoodleDocument",
    "vectorizer": "text2vec-transformers",
    "properties": [
        {"name": "content", "dataType": ["text"]},
        {"name": "source", "dataType": ["string"]},
        {"name": "course_id", "dataType": ["int"]}
    ]
}
client.schema.create_class(schema)
```

## Embedding Models (Local)
| Model | Dimensions | Best For |
|-------|------------|----------|
| nomic-embed-text | 768 | General purpose |
| bge-m3 | 1024 | Multilingual |
| mxbai-embed-large | 1024 | High quality |

## Start Chainlit
```bash
cd /opt/cloodle/tools/ai/multi_agent_rag_system
source .venv/bin/activate
chainlit run app.py
```
