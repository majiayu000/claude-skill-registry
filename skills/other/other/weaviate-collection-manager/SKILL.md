---
name: weaviate-collection-manager
description: Create, view, update, and delete Weaviate collections with schema management (for local Weaviate)
version: 2.0.0
author: Scott Askinosie
dependencies:
  - weaviate-connection
  - weaviate-local-setup
---

# Weaviate Collection Manager Skill

This skill helps you manage Weaviate collections on your **local Weaviate instance** - creating new ones, viewing existing schemas, and managing collection configurations.

## Important Note

**This skill is designed for LOCAL Weaviate instances only.** Ensure you have Weaviate running locally in Docker before using this skill.

## Purpose

Manage the structure and configuration of your local Weaviate vector database collections.

## When to Use This Skill

- User wants to create a new collection
- User asks to list all collections
- User needs to view a collection's schema
- User wants to delete a collection
- User asks about collection configuration

## Prerequisites Check

**Claude should verify these prerequisites before proceeding:**

1. ✅ **weaviate-local-setup** completed - Python environment and dependencies installed
2. ✅ **weaviate-connection** completed - Successfully connected to Weaviate
3. ✅ **Docker container running** - Weaviate is accessible at localhost:8080

**If any prerequisites are missing, Claude should:**
- Load the required prerequisite skill first
- Guide the user through the setup
- Then return to this skill

## Prerequisites

- **Local Weaviate running in Docker** (see **weaviate-local-setup** skill)
- Active Weaviate connection (use **weaviate-connection** skill first)
- Python weaviate-client library installed

## Operations

### 1. List All Collections

```python
import weaviate

# Assuming client is already connected
collections = client.collections.list_all()

print(f"Found {len(collections)} collections:\n")
for name, config in collections.items():
    print(f"📦 {name}")
    if hasattr(config, 'vectorizer_config'):
        print(f"   Vectorizer: {config.vectorizer_config}")
    print()
```

### 2. View Collection Details

```python
# Get specific collection
collection = client.collections.get("YourCollectionName")

# View configuration
config = collection.config.get()

print(f"Collection: {config.name}")
print(f"Vectorizer: {config.vectorizer}")
print(f"\nProperties:")
for prop in config.properties:
    print(f"  - {prop.name} ({prop.data_type})")
```

### 3. Create a New Collection

#### Simple Text Collection
```python
from weaviate.classes.config import Configure, Property, DataType

# Create collection with automatic vectorization
client.collections.create(
    name="Articles",
    description="Collection of article documents",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    properties=[
        Property(
            name="title",
            data_type=DataType.TEXT,
            description="Article title"
        ),
        Property(
            name="content",
            data_type=DataType.TEXT,
            description="Article content"
        ),
        Property(
            name="author",
            data_type=DataType.TEXT,
            skip_vectorization=True  # Don't vectorize author names
        ),
        Property(
            name="publishDate",
            data_type=DataType.DATE
        )
    ]
)

print("✅ Collection 'Articles' created successfully!")
```

#### Collection with Custom Vectors
```python
# For when you bring your own vectors
client.collections.create(
    name="CustomEmbeddings",
    vectorizer_config=Configure.Vectorizer.none(),  # No automatic vectorization
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="metadata", data_type=DataType.TEXT)
    ]
)
```

#### Multi-modal Collection (Text + Images)
```python
client.collections.create(
    name="ProductCatalog",
    vectorizer_config=Configure.Vectorizer.multi2vec_clip(),  # CLIP for images+text
    properties=[
        Property(name="name", data_type=DataType.TEXT),
        Property(name="description", data_type=DataType.TEXT),
        Property(name="image", data_type=DataType.BLOB),  # Base64 encoded image
        Property(name="price", data_type=DataType.NUMBER),
        Property(name="category", data_type=DataType.TEXT)
    ]
)
```

### 4. Configure Collection Settings

#### With Generative Module (for RAG)
```python
from weaviate.classes.config import Configure

client.collections.create(
    name="KnowledgeBase",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai(model="gpt-4"),  # Enable RAG
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT)
    ]
)
```

#### With Reranking
```python
client.collections.create(
    name="SearchableDocuments",
    vectorizer_config=Configure.Vectorizer.text2vec_cohere(),
    reranker_config=Configure.Reranker.cohere(),  # Improve search relevance
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="body", data_type=DataType.TEXT)
    ]
)
```

### 5. Delete a Collection

```python
# Delete collection (CAUTION: This is irreversible!)
client.collections.delete("CollectionName")
print("✅ Collection deleted")
```

## Common Data Types

| DataType | Description | Example |
|----------|-------------|---------|
| `TEXT` | String/text data | "Hello world" |
| `NUMBER` | Numeric values | 42, 3.14 |
| `INT` | Integer only | 42 |
| `BOOLEAN` | True/False | True |
| `DATE` | ISO 8601 dates | "2025-01-20T10:00:00Z" |
| `UUID` | Unique identifiers | Auto-generated |
| `BLOB` | Binary data (base64) | Images, files |
| `TEXT_ARRAY` | Array of strings | ["tag1", "tag2"] |
| `NUMBER_ARRAY` | Array of numbers | [1, 2, 3] |

## Vectorizer Options

| Vectorizer | Best For | Requires |
|------------|----------|----------|
| `text2vec_openai` | General text | OpenAI API key |
| `text2vec_cohere` | Multilingual text | Cohere API key |
| `text2vec_huggingface` | Custom models | HuggingFace model |
| `multi2vec_clip` | Images + Text | CLIP model |
| `none` | Bring your own vectors | Custom embeddings |

## Schema Design Best Practices

1. **Property Names**: Use camelCase (e.g., `firstName`, not `first_name`)
2. **Skip Vectorization**: Set `skip_vectorization=True` for IDs, dates, categories
3. **Descriptions**: Add clear descriptions to properties for better context
4. **Indexing**: Consider which properties need filtering/sorting

## Example: Complete Collection Setup

```python
from weaviate.classes.config import Configure, Property, DataType

# Create a well-structured collection for a document database
client.collections.create(
    name="TechnicalDocuments",
    description="Technical documentation with RAG capabilities",

    # Vectorization
    vectorizer_config=Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-small"
    ),

    # Enable RAG for Q&A
    generative_config=Configure.Generative.openai(
        model="gpt-4o"
    ),

    # Schema
    properties=[
        Property(
            name="title",
            data_type=DataType.TEXT,
            description="Document title",
            skip_vectorization=False
        ),
        Property(
            name="content",
            data_type=DataType.TEXT,
            description="Main document content",
            skip_vectorization=False  # This gets vectorized
        ),
        Property(
            name="section",
            data_type=DataType.TEXT,
            description="Document section/category",
            skip_vectorization=True  # Metadata, not for semantic search
        ),
        Property(
            name="page",
            data_type=DataType.INT,
            description="Page number"
        ),
        Property(
            name="hasImage",
            data_type=DataType.BOOLEAN,
            description="Whether page contains images"
        ),
        Property(
            name="tags",
            data_type=DataType.TEXT_ARRAY,
            description="Document tags",
            skip_vectorization=True
        )
    ]
)

print("✅ TechnicalDocuments collection created with RAG enabled!")
```

## Troubleshooting

### Error: "Collection already exists"
```python
# Check if collection exists first
if client.collections.exists("MyCollection"):
    print("Collection already exists")
else:
    client.collections.create(...)
```

### Error: "Invalid property name"
- Use camelCase, not snake_case
- Start with lowercase letter
- No special characters except underscore

### Error: "Vectorizer not available"
- Check API keys are configured
- Verify vectorizer module is enabled on your Weaviate instance

## Next Steps

After creating collections:
- Use **weaviate-data-ingestion** skill to add data
- Use **weaviate-query-agent** skill to search collections

## Additional Resources

- [Weaviate Schema Docs](https://weaviate.io/developers/weaviate/config-refs/schema)
- [Available Vectorizers](https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules)