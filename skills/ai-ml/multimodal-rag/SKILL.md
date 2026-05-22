---
name: multimodal-rag
description: CLIP, SigLIP 2, Voyage multimodal-3 patterns for image+text retrieval, cross-modal search, and multimodal document chunking. Use when building RAG with images, implementing visual search, or hybrid retrieval.
context: fork
agent: multimodal-specialist
version: 1.0.0
author: SkillForge
user-invocable: false
tags: [rag, multimodal, image-retrieval, clip, embeddings, vector-search, 2026]
---

# Multimodal RAG (2026)

Build retrieval-augmented generation systems that handle images, text, and mixed content.

## Overview

- Image + text retrieval (product search, documentation)
- Cross-modal search (text query -> image results)
- Multimodal document processing (PDFs with charts)
- Visual question answering with context
- Image similarity and deduplication
- Hybrid search pipelines

## Architecture Approaches

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Joint Embedding** (CLIP) | Direct comparison | Limited context | Pure image search |
| **Caption-based** | Works with text LLMs | Lossy conversion | Existing text RAG |
| **Hybrid** | Best accuracy | More complex | Production systems |

## Embedding Models (2026)

| Model | Context | Modalities | Best For |
|-------|---------|------------|----------|
| **Voyage multimodal-3** | 32K tokens | Text + Image | Long documents |
| **SigLIP 2** | Standard | Text + Image | Large-scale retrieval |
| **CLIP ViT-L/14** | 77 tokens | Text + Image | General purpose |
| **ImageBind** | Standard | 6 modalities | Audio/video included |
| **ColPali** | Document | Text + Image | PDF/document RAG |

## CLIP-Based Image Embeddings

```python
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

def embed_image(image_path: str) -> list[float]:
    """Generate CLIP embedding for an image."""
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)

    # Normalize for cosine similarity
    embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
    return embeddings[0].tolist()

def embed_text(text: str) -> list[float]:
    """Generate CLIP embedding for text query."""
    inputs = processor(text=[text], return_tensors="pt", padding=True)

    with torch.no_grad():
        embeddings = model.get_text_features(**inputs)

    embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
    return embeddings[0].tolist()

# Cross-modal search: text -> images
def search_images(query: str, image_embeddings: list, top_k: int = 5):
    """Search images using text query."""
    query_embedding = embed_text(query)

    # Compute similarities (cosine)
    similarities = [
        np.dot(query_embedding, img_emb)
        for img_emb in image_embeddings
    ]

    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return top_indices, [similarities[i] for i in top_indices]
```

## Voyage Multimodal-3 (Long Context)

```python
import voyageai

client = voyageai.Client()

def embed_multimodal_voyage(
    texts: list[str] = None,
    images: list[str] = None  # File paths or URLs
) -> list[list[float]]:
    """Embed text and/or images with 32K token context."""
    inputs = []

    if texts:
        inputs.extend([{"type": "text", "content": t} for t in texts])

    if images:
        for img_path in images:
            with open(img_path, "rb") as f:
                import base64
                b64 = base64.b64encode(f.read()).decode()
                inputs.append({
                    "type": "image",
                    "content": f"data:image/png;base64,{b64}"
                })

    response = client.multimodal_embed(
        inputs=inputs,
        model="voyage-multimodal-3"
    )

    return response.embeddings
```

## Hybrid RAG Pipeline

```python
from typing import Optional
import numpy as np

class MultimodalRAG:
    """Production multimodal RAG with hybrid retrieval."""

    def __init__(self, vector_db, vision_model, text_model):
        self.vector_db = vector_db
        self.vision_model = vision_model
        self.text_model = text_model

    async def index_document(
        self,
        doc_id: str,
        text: Optional[str] = None,
        image_path: Optional[str] = None,
        metadata: dict = None
    ):
        """Index a document with text and/or image."""
        embeddings = []

        if text:
            text_emb = embed_text(text)
            embeddings.append(("text", text_emb))

        if image_path:
            # Option 1: Direct image embedding
            img_emb = embed_image(image_path)
            embeddings.append(("image", img_emb))

            # Option 2: Generate caption for text search
            caption = await self.generate_caption(image_path)
            caption_emb = embed_text(caption)
            embeddings.append(("caption", caption_emb))

        # Store with shared document ID
        for emb_type, emb in embeddings:
            await self.vector_db.upsert(
                id=f"{doc_id}_{emb_type}",
                embedding=emb,
                metadata={
                    "doc_id": doc_id,
                    "type": emb_type,
                    "image_url": image_path,
                    "text": text,
                    **(metadata or {})
                }
            )

    async def generate_caption(self, image_path: str) -> str:
        """Generate text caption for image indexing."""
        # Use GPT-4o or Claude for high-quality captions
        response = await self.vision_model.analyze(
            image_path,
            prompt="Describe this image in detail for search indexing. "
                   "Include objects, text, colors, and context."
        )
        return response

    async def retrieve(
        self,
        query: str,
        query_image: Optional[str] = None,
        top_k: int = 10
    ) -> list[dict]:
        """Hybrid retrieval with optional image query."""
        results = []

        # Text query embedding
        text_emb = embed_text(query)
        text_results = await self.vector_db.search(
            embedding=text_emb,
            top_k=top_k
        )
        results.extend(text_results)

        # Image query embedding (if provided)
        if query_image:
            img_emb = embed_image(query_image)
            img_results = await self.vector_db.search(
                embedding=img_emb,
                top_k=top_k
            )
            results.extend(img_results)

        # Dedupe by doc_id, keep highest score
        seen = {}
        for r in results:
            doc_id = r["metadata"]["doc_id"]
            if doc_id not in seen or r["score"] > seen[doc_id]["score"]:
                seen[doc_id] = r

        return sorted(seen.values(), key=lambda x: x["score"], reverse=True)[:top_k]
```

## Multimodal Document Chunking

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class Chunk:
    content: str
    chunk_type: Literal["text", "image", "table", "chart"]
    page: int
    image_path: Optional[str] = None
    embedding: Optional[list[float]] = None

def chunk_multimodal_document(pdf_path: str) -> list[Chunk]:
    """Chunk PDF preserving images and tables."""
    from pdf2image import convert_from_path
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    chunks = []

    for page_num, page in enumerate(doc):
        # Extract text blocks
        text_blocks = page.get_text("blocks")
        current_text = ""

        for block in text_blocks:
            if block[6] == 0:  # Text block
                current_text += block[4] + "\n"
            else:  # Image block
                # Save current text chunk
                if current_text.strip():
                    chunks.append(Chunk(
                        content=current_text.strip(),
                        chunk_type="text",
                        page=page_num
                    ))
                    current_text = ""

                # Extract and save image
                xref = block[7]
                img = doc.extract_image(xref)
                img_path = f"/tmp/page{page_num}_img{xref}.{img['ext']}"
                with open(img_path, "wb") as f:
                    f.write(img["image"])

                # Generate caption for the image
                caption = generate_image_caption(img_path)

                chunks.append(Chunk(
                    content=caption,
                    chunk_type="image",
                    page=page_num,
                    image_path=img_path
                ))

        # Final text chunk
        if current_text.strip():
            chunks.append(Chunk(
                content=current_text.strip(),
                chunk_type="text",
                page=page_num
            ))

    return chunks
```

## Vector Database Setup (Milvus)

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

def setup_multimodal_collection():
    """Create Milvus collection for multimodal embeddings."""
    connections.connect("default", host="localhost", port="19530")

    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=256),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
        FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="chunk_type", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="image_url", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="page", dtype=DataType.INT64)
    ]

    schema = CollectionSchema(fields, "Multimodal document collection")
    collection = Collection("multimodal_docs", schema)

    # Create index for vector search
    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 16, "efConstruction": 256}
    }
    collection.create_index("embedding", index_params)

    return collection
```

## Multimodal Generation

```python
async def generate_with_context(
    query: str,
    retrieved_chunks: list[Chunk],
    model: str = "claude-opus-4-5-20251124"
) -> str:
    """Generate response using multimodal context."""
    content = []

    # Add retrieved images first (attention positioning)
    for chunk in retrieved_chunks:
        if chunk.chunk_type == "image" and chunk.image_path:
            base64_data, media_type = encode_image_base64(chunk.image_path)
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_data
                }
            })

    # Add text context
    text_context = "\n\n".join([
        f"[Page {c.page}]: {c.content}"
        for c in retrieved_chunks if c.chunk_type == "text"
    ])

    content.append({
        "type": "text",
        "text": f"""Use the following context to answer the question.

Context:
{text_context}

Question: {query}

Provide a detailed answer based on the context and images provided."""
    })

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": content}]
    )

    return response.content[0].text
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Long documents | Voyage multimodal-3 (32K context) |
| Scale retrieval | SigLIP 2 (optimized for large-scale) |
| PDF processing | ColPali (document-native) |
| Multi-modal search | Hybrid: CLIP + text embeddings |
| Production DB | Milvus or Pinecone with hybrid |

## Common Mistakes

- Embedding images without captions (limits text search)
- Not deduplicating by document ID
- Missing image URL storage (can't display results)
- Using only image OR text embeddings (use both)
- Ignoring chunk boundaries (split mid-paragraph)
- Not validating image retrieval quality

## Related Skills

- `vision-language-models` - Image analysis
- `embeddings` - Text embedding patterns
- `rag-retrieval` - Text RAG patterns
- `contextual-retrieval` - Hybrid BM25+vector

## Capability Details

### image-embeddings
**Keywords:** CLIP, image embedding, visual features, SigLIP
**Solves:**
- Convert images to vector representations
- Enable image similarity search
- Cross-modal retrieval

### cross-modal-search
**Keywords:** text to image, image to text, cross-modal
**Solves:**
- Find images from text queries
- Find text from image queries
- Bridge modalities

### multimodal-chunking
**Keywords:** chunk PDF, split document, extract images
**Solves:**
- Process documents with mixed content
- Preserve image-text relationships
- Handle tables and charts

### hybrid-retrieval
**Keywords:** hybrid search, fusion, multi-embedding
**Solves:**
- Combine text and image search
- Improve retrieval accuracy
- Handle diverse queries
