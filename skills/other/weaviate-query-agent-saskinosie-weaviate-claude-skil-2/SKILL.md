---
name: weaviate-query-agent
description: Search and retrieve data from local Weaviate using semantic search, filters, RAG, and hybrid queries
version: 2.0.0
author: Scott Askinosie
dependencies:
  - weaviate-connection
  - weaviate-collection-manager
  - weaviate-local-setup
---

# Weaviate Query Agent Skill

This skill helps you search and retrieve data from your **local Weaviate collections** using semantic vector search, keyword search, filters, and RAG capabilities.

## Important Note

**This skill is designed for LOCAL Weaviate instances only.** Ensure you have Weaviate running locally in Docker before using this skill.

## Purpose

Query your local Weaviate collections intelligently to find relevant information, perform Q&A, and analyze your data.

## When to Use This Skill

- User wants to search for information in a collection
- User asks questions that need semantic search
- User needs to filter results by specific criteria
- User wants to use RAG (Retrieval Augmented Generation) for Q&A
- User asks about finding similar items
- User needs to combine vector search with filters

## Prerequisites Check

**Claude should verify these prerequisites before proceeding:**

1. ✅ **weaviate-local-setup** completed - Python environment and dependencies installed
2. ✅ **weaviate-connection** completed - Successfully connected to Weaviate
3. ✅ **weaviate-data-ingestion** used - Collection has data to query
4. ✅ **Docker container running** - Weaviate is accessible at localhost:8080

**If any prerequisites are missing, Claude should:**
- Load the required prerequisite skill first
- Guide the user through the setup
- Then return to this skill

## Prerequisites

- **Local Weaviate running in Docker** (see **weaviate-local-setup** skill)
- Active Weaviate connection (use **weaviate-connection** skill first)
- Collection with data (use **weaviate-data-ingestion** skill to add data)
- Python weaviate-client library installed

## Query Types

### 1. Semantic Search (Vector Search)

Find objects semantically similar to your query:

```python
import weaviate

# Assuming client is already connected
collection = client.collections.get("Articles")

# Search by meaning
response = collection.query.near_text(
    query="artificial intelligence and machine learning",
    limit=5
)

# Display results
for obj in response.objects:
    print(f"Title: {obj.properties['title']}")
    print(f"Content: {obj.properties['content'][:200]}...")
    print(f"Score: {obj.metadata.score}\n")
```

### 2. Search with Specific Properties

Return only the fields you need:

```python
response = collection.query.near_text(
    query="vector databases",
    limit=5,
    return_properties=["title", "author", "publishDate"]
)

for obj in response.objects:
    print(f"{obj.properties['title']} by {obj.properties['author']}")
```

### 3. Keyword Search (BM25)

Traditional keyword-based search:

```python
from weaviate.classes.query import QueryReference

response = collection.query.bm25(
    query="vector search",
    limit=5
)

for obj in response.objects:
    print(f"Title: {obj.properties['title']}")
```

### 4. Hybrid Search (Best of Both Worlds)

Combine semantic and keyword search:

```python
response = collection.query.hybrid(
    query="machine learning applications",
    limit=5,
    alpha=0.5  # 0 = pure BM25, 1 = pure vector, 0.5 = balanced
)

for obj in response.objects:
    print(f"Title: {obj.properties['title']}")
    print(f"Score: {obj.metadata.score}\n")
```

### 5. Filter Results

Search with conditions:

```python
from weaviate.classes.query import Filter

# Search with author filter
response = collection.query.near_text(
    query="AI advancements",
    limit=5,
    filters=Filter.by_property("author").equal("Jane Smith")
)

# Multiple filters
response = collection.query.near_text(
    query="technology trends",
    limit=10,
    filters=(
        Filter.by_property("author").equal("Jane Smith") &
        Filter.by_property("publishDate").greater_than("2024-01-01T00:00:00Z")
    )
)

# Filter by array contains
response = collection.query.near_text(
    query="programming",
    filters=Filter.by_property("tags").contains_any(["python", "javascript"])
)
```

### 6. Filter Operators

```python
from weaviate.classes.query import Filter

# Equality
Filter.by_property("status").equal("published")

# Comparison
Filter.by_property("price").greater_than(100)
Filter.by_property("price").less_than(500)
Filter.by_property("price").greater_or_equal(100)
Filter.by_property("price").less_or_equal(500)

# String matching
Filter.by_property("title").like("*vector*")  # Contains "vector"

# Array operations
Filter.by_property("tags").contains_any(["ai", "ml"])
Filter.by_property("tags").contains_all(["python", "tutorial"])

# Combine filters
(Filter.by_property("price").greater_than(100) &
 Filter.by_property("category").equal("Electronics"))

# OR conditions
(Filter.by_property("author").equal("John") |
 Filter.by_property("author").equal("Jane"))
```

### 7. Search by Image (Multi-modal)

For collections with CLIP or multi2vec:

```python
import base64

# Encode query image
with open("query_image.jpg", "rb") as f:
    query_image = base64.b64encode(f.read()).decode("utf-8")

collection = client.collections.get("ProductCatalog")

# Find similar images
response = collection.query.near_image(
    near_image=query_image,
    limit=5,
    return_properties=["name", "description", "price"]
)

for obj in response.objects:
    print(f"Product: {obj.properties['name']} - ${obj.properties['price']}")
```

### 8. Search by Vector

If you have a pre-computed embedding:

```python
# Your custom embedding
query_vector = [0.1, 0.2, 0.3, ...]  # 1536 dimensions for OpenAI

response = collection.query.near_vector(
    near_vector=query_vector,
    limit=5
)
```

### 9. Get Object by ID

Retrieve specific object:

```python
# Get by UUID
obj = collection.query.fetch_object_by_id("uuid-here")

print(f"Title: {obj.properties['title']}")
print(f"Content: {obj.properties['content']}")
```

### 10. Fetch Multiple Objects

Get all objects or filter by property:

```python
from weaviate.classes.query import Filter

# Get all objects (paginated)
response = collection.query.fetch_objects(limit=100)

# Get objects matching filter
response = collection.query.fetch_objects(
    filters=Filter.by_property("section").equal("Introduction"),
    limit=50
)

for obj in response.objects:
    print(obj.properties['title'])
```

## RAG (Retrieval Augmented Generation)

Use Weaviate's generative module for Q&A:

### Single Prompt RAG

```python
# Collection must have generative module configured
collection = client.collections.get("TechnicalDocuments")

response = collection.generate.near_text(
    query="How do I configure HVAC systems?",
    single_prompt="Answer this question based on the context: {question}. Context: {content}",
    limit=3
)

# Get generated answer
print(f"Answer: {response.generated}")

# See source documents
for obj in response.objects:
    print(f"\nSource: {obj.properties['title']}")
    print(f"Content: {obj.properties['content'][:200]}...")
```

### Grouped Task RAG

Generate one response using all results:

```python
response = collection.generate.near_text(
    query="What are the best practices for fan selection?",
    grouped_task="Summarize the key recommendations from these documents about fan selection",
    limit=5
)

print(response.generated)
```

### Custom RAG Implementation

If collection doesn't have generative module:

```python
from openai import OpenAI

# Search Weaviate
weaviate_collection = weaviate_client.collections.get("TechnicalDocuments")
search_results = weaviate_collection.query.near_text(
    query="What is the friction loss for round elbows?",
    limit=5,
    return_properties=["content", "section", "page"]
)

# Build context
context = "\n\n".join([
    f"[{obj.properties['section']} - Page {obj.properties['page']}]\n{obj.properties['content']}"
    for obj in search_results.objects
])

# Call LLM
openai_client = OpenAI()
response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a technical assistant. Answer questions based on the provided context."
        },
        {
            "role": "user",
            "content": f"Question: What is the friction loss for round elbows?\n\nContext:\n{context}"
        }
    ]
)

answer = response.choices[0].message.content
print(answer)
```

### Vision-Enabled RAG (Query Images with GPT-4o Vision)

When your collection contains images (like maps, charts, diagrams), you can use GPT-4o Vision to analyze them:

#### Single Image Analysis

```python
from openai import OpenAI
import base64

# Search Weaviate for results with visual content
weaviate_client = client.collections.get("Cook_Engineering_Manual")
search_results = weaviate_client.query.near_text(
    query="Missouri wind zone map",
    limit=5,
    return_properties=["content", "section", "page", "visual_content", "visual_description", "has_critical_visual"]
)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Process results and analyze images
for obj in search_results.objects:
    props = obj.properties

    # Check if this result has visual content
    if props.get('has_critical_visual') and props.get('visual_content'):
        print(f"\n📊 Analyzing visual content from page {props.get('page')}")

        # The image is already base64 encoded in Weaviate
        image_base64 = props['visual_content']

        # Call GPT-4o Vision to analyze the image
        vision_response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Question: Is Missouri considered a high wind zone?\n\nContext: {props.get('content', '')}\n\nPlease analyze the image and answer the question based on what you see."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        answer = vision_response.choices[0].message.content
        print(f"\n🤖 Answer:\n{answer}")
        print(f"\n📄 Source: {props.get('section')} - Page {props.get('page')}")
```

#### Complete Vision RAG Pipeline

```python
from openai import OpenAI
import os

def vision_rag_query(
    question: str,
    collection_name: str = "TechnicalDocuments",
    limit: int = 5
):
    """
    Complete RAG pipeline with vision support.
    Searches Weaviate, finds relevant text and images, uses GPT-4o Vision to analyze.
    """

    # Step 1: Connect to Weaviate
    weaviate_client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
        skip_init_checks=True
    )

    try:
        # Step 2: Search for relevant content
        print(f"🔍 Searching for: {question}")
        collection = weaviate_client.collections.get(collection_name)

        response = collection.query.near_text(
            query=question,
            limit=limit,
            return_properties=["content", "section", "page", "visual_content",
                             "visual_description", "has_critical_visual"]
        )

        if not response.objects:
            return "No relevant information found."

        # Step 3: Process results - separate text and visual content
        text_context = []
        visual_items = []

        for obj in response.objects:
            props = obj.properties

            # Collect text context
            text_context.append(
                f"[{props.get('section', 'Unknown')} - Page {props.get('page', 'N/A')}]\n"
                f"{props.get('content', '')}"
            )

            # Collect visual content for analysis
            if props.get('has_critical_visual') and props.get('visual_content'):
                visual_items.append({
                    'image': props['visual_content'],
                    'description': props.get('visual_description', ''),
                    'page': props.get('page'),
                    'section': props.get('section'),
                    'context': props.get('content', '')
                })

        # Step 4: Analyze with GPT-4o Vision if images found
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        if visual_items:
            print(f"🖼️  Found {len(visual_items)} images - analyzing with GPT-4o Vision...")

            # Build message content with both text and images
            message_content = [
                {
                    "type": "text",
                    "text": f"Question: {question}\n\nText Context:\n" + "\n\n".join(text_context[:3])
                }
            ]

            # Add images to the message
            for idx, item in enumerate(visual_items[:3]):  # Limit to 3 images
                message_content.append({
                    "type": "text",
                    "text": f"\n\nImage {idx+1} (Page {item['page']} - {item['section']}):\nContext: {item['context'][:200]}..."
                })
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{item['image']}",
                        "detail": "high"  # Use high detail for technical diagrams
                    }
                })

            # Call GPT-4o Vision
            vision_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical assistant with vision capabilities. Analyze both text and images to provide accurate, comprehensive answers. When analyzing maps, charts, or diagrams, describe what you see and relate it to the question."
                    },
                    {
                        "role": "user",
                        "content": message_content
                    }
                ],
                max_tokens=2000
            )

            answer = vision_response.choices[0].message.content

        else:
            # No images - use text-only RAG
            print("📝 No images found - using text-only RAG...")

            text_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical assistant. Answer based on the provided context."
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\n\nContext:\n" + "\n\n".join(text_context)
                    }
                ],
                max_tokens=1000
            )

            answer = text_response.choices[0].message.content

        # Step 5: Format response
        result = f"\n{'='*70}\n"
        result += f"🤖 ANSWER:\n\n{answer}\n"
        result += f"\n{'='*70}\n"
        result += f"📚 SOURCES:\n\n"

        for i, obj in enumerate(response.objects[:5], 1):
            props = obj.properties
            visual_indicator = " 🖼️" if props.get('has_critical_visual') else ""
            result += f"{i}. {props.get('section', 'Unknown')} - Page {props.get('page', 'N/A')}{visual_indicator}\n"

        return result

    finally:
        weaviate_client.close()

# Example usage
if __name__ == "__main__":
    result = vision_rag_query(
        question="Is Missouri considered a high wind zone for HVAC equipment?",
        collection_name="Cook_Engineering_Manual",
        limit=5
    )
    print(result)
```

#### Quick Vision Query Helper

```python
def quick_vision_query(question: str, search_query: str = None):
    """
    Quick helper for vision-enabled queries.
    Automatically handles search, image retrieval, and GPT-4o Vision analysis.
    """
    from openai import OpenAI
    import weaviate
    import os

    if search_query is None:
        search_query = question

    # Connect
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
        skip_init_checks=True
    )

    try:
        collection = client.collections.get("Cook_Engineering_Manual")

        # Search with visual priority
        results = collection.query.near_text(
            query=search_query,
            limit=3,
            filters=Filter.by_property("has_critical_visual").equal(True),  # Prioritize visual content
            return_properties=["content", "section", "page", "visual_content", "visual_description"]
        )

        if not results.objects:
            return "No visual content found for this query."

        # Use first result with image
        obj = results.objects[0]
        props = obj.properties

        if not props.get('visual_content'):
            return "No image found in search results."

        # Analyze with GPT-4o Vision
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{question}\n\nContext: {props.get('content', '')}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{props['visual_content']}"}}
                ]
            }]
        )

        return f"📄 Source: {props.get('section')} - Page {props.get('page')}\n\n{response.choices[0].message.content}"

    finally:
        client.close()

# Usage
answer = quick_vision_query("Is Missouri a high wind zone?", "Missouri wind zone map")
print(answer)
```

## Advanced Query Features

### 1. Limit and Offset (Pagination)

```python
# Get results 10-20
response = collection.query.near_text(
    query="AI trends",
    limit=10,
    offset=10
)
```

### 2. Distance Threshold

Only return results within certain similarity:

```python
response = collection.query.near_text(
    query="machine learning",
    distance=0.3,  # Only results with distance < 0.3
    limit=10
)
```

### 3. Include Vector in Response

```python
response = collection.query.near_text(
    query="vector search",
    limit=5,
    return_metadata=["vector"]
)

for obj in response.objects:
    print(f"Vector: {obj.metadata.vector[:5]}...")  # First 5 dimensions
```

### 4. Aggregate Queries

Get statistics about your collection:

```python
from weaviate.classes.aggregate import GroupByAggregate

# Count objects
result = collection.aggregate.over_all(
    total_count=True
)
print(f"Total objects: {result.total_count}")

# Group by property
result = collection.aggregate.over_all(
    group_by=GroupByAggregate(prop="author")
)

for group in result.groups:
    print(f"Author: {group.grouped_by.value} - Count: {group.total_count}")
```

### 5. Multi-target Vector Search

For collections with multiple vector spaces:

```python
from weaviate.classes.query import TargetVectors

# Search specific vector space
response = collection.query.near_text(
    query="machine learning",
    target_vector="content_vector",  # Specify which vector
    limit=5
)
```

### 6. Reranking

Improve search quality with reranking:

```python
# Collection must have reranker configured
response = collection.query.near_text(
    query="best practices for database design",
    limit=20,
    rerank={
        "property": "content",
        "query": "database design best practices"
    }
)
```

## Complete Search Examples

### Example 1: Advanced Document Search

```python
from weaviate.classes.query import Filter, MetadataQuery

collection = client.collections.get("TechnicalDocuments")

# Complex search with filters and specific properties
response = collection.query.near_text(
    query="seismic zone requirements",
    limit=10,
    filters=(
        Filter.by_property("section").like("*Building*") &
        Filter.by_property("page").greater_than(50)
    ),
    return_properties=["title", "content", "section", "page"],
    return_metadata=MetadataQuery(distance=True, certainty=True)
)

# Process results
for obj in response.objects:
    print(f"\n{'='*60}")
    print(f"Section: {obj.properties['section']}")
    print(f"Page: {obj.properties['page']}")
    print(f"Certainty: {obj.metadata.certainty:.2%}")
    print(f"\nContent:\n{obj.properties['content'][:300]}...")
```

### Example 2: Multi-Modal Product Search

```python
import base64

collection = client.collections.get("ProductCatalog")

# Search by text and image
with open("reference_product.jpg", "rb") as f:
    ref_image = base64.b64encode(f.read()).decode("utf-8")

# Hybrid approach: text + image similarity
response = collection.query.near_image(
    near_image=ref_image,
    limit=10,
    filters=Filter.by_property("price").less_than(500),
    return_properties=["name", "description", "price", "category"]
)

print("Similar products under $500:\n")
for obj in response.objects:
    print(f"• {obj.properties['name']}")
    print(f"  Price: ${obj.properties['price']}")
    print(f"  Category: {obj.properties['category']}\n")
```

### Example 3: Interactive Q&A System

```python
def ask_question(question: str, collection_name: str = "TechnicalDocuments"):
    """Interactive Q&A using RAG"""
    collection = client.collections.get(collection_name)

    # Search with RAG
    response = collection.generate.near_text(
        query=question,
        single_prompt=f"""Based on the following context, answer this question: {question}

Context: {{content}}

Provide a clear, concise answer. If you cannot answer based on the context, say so.""",
        limit=5
    )

    print(f"\n🤖 Answer:\n{response.generated}\n")
    print(f"📚 Sources:")
    for i, obj in enumerate(response.objects, 1):
        print(f"{i}. {obj.properties.get('title', 'Untitled')} (Page {obj.properties.get('page', 'N/A')})")

# Use it
ask_question("What are the wind zone requirements for Missouri?")
ask_question("How do I calculate motor efficiency?")
```

## Query Performance Tips

1. **Use Filters**: Pre-filter before vector search for better performance
2. **Limit Results**: Only retrieve what you need (smaller `limit` is faster)
3. **Select Properties**: Don't return all properties if you only need some
4. **Batch Queries**: Query once and process locally rather than many small queries
5. **Hybrid Search**: Use `alpha` parameter to balance speed vs accuracy
6. **Index Optimization**: Ensure properties used in filters are indexed

## Error Handling

```python
from weaviate.exceptions import WeaviateQueryException

try:
    response = collection.query.near_text(
        query="machine learning",
        limit=10
    )

    if not response.objects:
        print("No results found")
    else:
        for obj in response.objects:
            print(obj.properties['title'])

except WeaviateQueryException as e:
    print(f"Query error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Troubleshooting

### Issue: "No results found"
- **Solution**: Try broader query terms
- **Solution**: Check if collection has data
- **Solution**: Verify vectorizer is working

### Issue: "Filter not working"
- **Solution**: Check property name matches schema exactly (camelCase)
- **Solution**: Ensure property type matches filter operation
- **Solution**: Verify property is indexed

### Issue: "Slow queries"
- **Solution**: Reduce `limit` value
- **Solution**: Use filters to narrow search space
- **Solution**: Return fewer properties
- **Solution**: Check collection size and indexing

### Issue: "Generative search fails"
- **Solution**: Verify collection has generative module configured
- **Solution**: Check API keys for OpenAI/Cohere are set
- **Solution**: Ensure sufficient API quota

### Issue: "Vision query returns no images"
- **Cause**: Collection doesn't have blob fields or images aren't stored
- **Solution**: Verify your schema has a blob property (e.g., `visual_content`)
- **Solution**: Check objects actually have image data: `obj.properties.get('visual_content')`
- **Solution**: Use filter to prioritize visual content: `Filter.by_property("has_critical_visual").equal(True)`

### Issue: "GPT-4o Vision API fails"
- **Cause**: Missing or invalid OpenAI API key
- **Solution**: Verify `OPENAI_API_KEY` is set in environment
- **Solution**: Check API key has access to GPT-4o Vision (not all keys do)
- **Solution**: Ensure you have sufficient API credits/quota

### Issue: "Image is corrupted or won't display"
- **Cause**: Image not properly base64 encoded
- **Solution**: Ensure image is stored as base64 string in Weaviate
- **Solution**: Verify format: `data:image/jpeg;base64,{base64_string}`
- **Solution**: Check image size - very large images may need compression

### Issue: "Vision analysis is incorrect or incomplete"
- **Cause**: Low-quality image or GPT-4o can't interpret the visual
- **Solution**: Use `"detail": "high"` parameter for technical diagrams/maps
- **Solution**: Provide more context in the prompt about what type of visual it is
- **Solution**: For complex charts/maps, ask specific questions rather than open-ended queries
- **Example**: Instead of "What does this show?", ask "Is Missouri in the high wind zone on this map?"

### Issue: "Vision query is slow"
- **Cause**: GPT-4o Vision API calls take longer than text-only
- **Solution**: Limit number of images analyzed (use `[:3]` to limit to 3 images)
- **Solution**: Use smaller images when possible
- **Solution**: Consider caching results for frequently asked questions
- **Solution**: Filter to only retrieve visual content when needed

## Complete Query Pipeline Example

```python
import weaviate
from weaviate.classes.query import Filter, MetadataQuery
from openai import OpenAI
import os

def semantic_search_with_rag(
    question: str,
    collection_name: str = "TechnicalDocuments",
    limit: int = 5,
    filters: Filter | None = None
):
    """Complete search pipeline with custom RAG"""

    # Connect to Weaviate
    weaviate_client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.Auth.api_key(os.getenv("WEAVIATE_API_KEY"))
    )

    try:
        # Step 1: Vector search
        print(f"🔍 Searching for: {question}")
        collection = weaviate_client.collections.get(collection_name)

        response = collection.query.near_text(
            query=question,
            limit=limit,
            filters=filters,
            return_properties=["content", "section", "page", "title"],
            return_metadata=MetadataQuery(distance=True)
        )

        if not response.objects:
            return "No relevant information found."

        # Step 2: Build context
        context_parts = []
        sources = []

        for obj in response.objects:
            props = obj.properties
            context_parts.append(
                f"[{props.get('section', 'Unknown')} - Page {props.get('page', 'N/A')}]\n{props['content']}"
            )
            sources.append({
                "title": props.get('title', 'Untitled'),
                "section": props.get('section', 'Unknown'),
                "page": props.get('page', 'N/A'),
                "distance": obj.metadata.distance
            })

        context = "\n\n---\n\n".join(context_parts)

        # Step 3: Generate answer
        print("🤖 Generating answer...")
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        chat_response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical assistant. Provide accurate answers based on the context. Cite specific page numbers when possible."
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nContext:\n{context}\n\nProvide a comprehensive answer."
                }
            ],
            max_tokens=1000
        )

        answer = chat_response.choices[0].message.content

        # Step 4: Format response
        result = f"\n{'='*70}\n"
        result += f"🤖 ANSWER:\n\n{answer}\n"
        result += f"\n{'='*70}\n"
        result += f"📚 SOURCES:\n\n"

        for i, source in enumerate(sources, 1):
            result += f"{i}. {source['title']} - {source['section']} (Page {source['page']})\n"
            result += f"   Similarity: {1 - source['distance']:.2%}\n"

        return result

    finally:
        weaviate_client.close()

# Example usage
if __name__ == "__main__":
    question = "What is the friction loss for round elbows?"

    # Optional: Add filters
    filters = Filter.by_property("section").like("*Ductwork*")

    result = semantic_search_with_rag(
        question=question,
        collection_name="Cook_Engineering_Manual",
        limit=5,
        filters=filters
    )

    print(result)
```

## Next Steps

After mastering queries:
- Combine with **weaviate-data-ingestion** for continuous data updates
- Monitor query performance and adjust schemas
- Experiment with different query types for your use case
- Build custom applications on top of Weaviate

## Additional Resources

- [Weaviate Query Docs](https://weaviate.io/developers/weaviate/search)
- [RAG Tutorial](https://weaviate.io/developers/weaviate/tutorials/rag)
- [Filter Reference](https://weaviate.io/developers/weaviate/search/filters)