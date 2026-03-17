---
name: weaviate-data-ingestion
description: Upload and process data into local Weaviate collections with support for single objects, batch uploads, and multi-modal content
version: 2.0.0
author: Scott Askinosie
dependencies:
  - weaviate-connection
  - weaviate-collection-manager
  - weaviate-local-setup
---

# Weaviate Data Ingestion Skill

This skill helps you upload data to your **local Weaviate collections** efficiently, handling everything from single objects to large batch imports.

## Important Note

**This skill is designed for LOCAL Weaviate instances only.** Ensure you have Weaviate running locally in Docker before using this skill.

## Purpose

Add data to your local Weaviate collections with automatic vectorization, proper error handling, and progress tracking.

## When to Use This Skill

- User wants to add data to a collection
- User needs to upload documents, articles, or records
- User has images or multi-modal content to ingest
- User wants to import data from files (JSON, CSV, text)
- User asks about batch uploading or bulk data import

## Prerequisites Check

**Claude should verify these prerequisites before proceeding:**

1. ✅ **weaviate-local-setup** completed - Python environment and dependencies installed
2. ✅ **weaviate-connection** completed - Successfully connected to Weaviate
3. ✅ **weaviate-collection-manager** used - Target collection exists
4. ✅ **Docker container running** - Weaviate is accessible at localhost:8080

**If any prerequisites are missing, Claude should:**
- Load the required prerequisite skill first
- Guide the user through the setup
- Then return to this skill

## Prerequisites

- **Local Weaviate running in Docker** (see **weaviate-local-setup** skill)
- Active Weaviate connection (use **weaviate-connection** skill first)
- Existing collection (use **weaviate-collection-manager** skill to create)
- Python weaviate-client library installed

## Operations

### 1. Add a Single Object

```python
import weaviate
from weaviate.classes.data import DataObject

# Assuming client is already connected
collection = client.collections.get("Articles")

# Add one object
uuid = collection.data.insert(
    properties={
        "title": "Introduction to Vector Databases",
        "content": "Vector databases enable semantic search by storing embeddings...",
        "author": "John Doe",
        "publishDate": "2025-01-20T10:00:00Z"
    }
)

print(f"✅ Object created with UUID: {uuid}")
```

### 2. Add Object with Custom Vector

```python
# If you bring your own embeddings
collection = client.collections.get("CustomEmbeddings")

uuid = collection.data.insert(
    properties={
        "text": "Your content here",
        "metadata": "Additional info"
    },
    vector=[0.1, 0.2, 0.3, ...]  # Your pre-computed embedding
)
```

### 3. Batch Upload Multiple Objects

#### Simple Batch Insert

```python
from weaviate.util import generate_uuid5

collection = client.collections.get("Articles")

# Prepare your data
articles = [
    {
        "title": "AI in 2025",
        "content": "Artificial intelligence continues to evolve...",
        "author": "Jane Smith",
        "publishDate": "2025-01-15T00:00:00Z"
    },
    {
        "title": "Vector Search Explained",
        "content": "Vector search allows you to find similar items...",
        "author": "Bob Johnson",
        "publishDate": "2025-01-18T00:00:00Z"
    },
    # ... more articles
]

# Batch insert with context manager (recommended)
with collection.batch.dynamic() as batch:
    for article in articles:
        batch.add_object(
            properties=article,
            # Optional: provide deterministic UUID based on content
            uuid=generate_uuid5(article['title'])
        )

print(f"✅ Inserted {len(articles)} articles")
```

#### Batch with Error Handling

```python
from weaviate.util import generate_uuid5

collection = client.collections.get("Articles")
failed_objects = []

with collection.batch.dynamic() as batch:
    for i, article in enumerate(articles):
        try:
            batch.add_object(
                properties=article,
                uuid=generate_uuid5(article.get('title', str(i)))
            )
        except Exception as e:
            failed_objects.append({"index": i, "error": str(e), "data": article})
            print(f"⚠️  Failed to add article {i}: {str(e)}")

# Check batch results
if batch.failed_objects:
    print(f"❌ {len(batch.failed_objects)} objects failed")
    for failed in batch.failed_objects:
        print(f"   Error: {failed.message}")
else:
    print(f"✅ All {len(articles)} objects inserted successfully")
```

### 4. Upload Data from JSON File

```python
import json

# Read JSON file
with open("articles.json", "r") as f:
    data = json.load(f)

collection = client.collections.get("Articles")

# Batch insert
with collection.batch.dynamic() as batch:
    for item in data:
        batch.add_object(properties=item)

print(f"✅ Imported {len(data)} objects from JSON")
```

### 5. Upload Data from CSV File

```python
import csv
from datetime import datetime

collection = client.collections.get("Articles")

with open("articles.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)

    with collection.batch.dynamic() as batch:
        for row in reader:
            # Transform CSV row to match schema
            batch.add_object(
                properties={
                    "title": row["title"],
                    "content": row["content"],
                    "author": row["author"],
                    "publishDate": datetime.fromisoformat(row["date"]).isoformat()
                }
            )

print("✅ CSV import complete")
```

### 6. Upload Images (Multi-modal Collections)

**⚠️ IMPORTANT: Verify Multimodal Vectorizer First**

Before uploading images, verify your collection uses a multimodal vectorizer:

```python
# Check collection configuration
collection = client.collections.get("ProductCatalog")
config = collection.config.get()

# Get vectorizer info
vectorizer = config.vectorizer.config.name if hasattr(config.vectorizer.config, 'name') else str(config.vectorizer)

# List of multimodal-compatible vectorizers
MULTIMODAL_VECTORIZERS = [
    'multi2vec-clip',
    'multi2vec-bind',
    'img2vec-neural',
]

# Validate vectorizer
is_multimodal = any(mv in str(vectorizer).lower() for mv in MULTIMODAL_VECTORIZERS)

if not is_multimodal:
    print(f"❌ Warning: Collection uses '{vectorizer}' which may not support images properly")
    print(f"   Recommended vectorizers for images: {', '.join(MULTIMODAL_VECTORIZERS)}")
    print(f"   Images will be stored but may not be vectorized correctly for semantic search")

    # Prompt user to continue
    response = input("\nContinue anyway? (y/n): ")
    if response.lower() != 'y':
        print("Aborted. Use weaviate-collection-manager skill to create a multimodal collection.")
        exit()
else:
    print(f"✅ Collection uses multimodal vectorizer: {vectorizer}")
```

#### Single Image Upload

```python
import base64
from pathlib import Path

collection = client.collections.get("ProductCatalog")

def encode_image(image_path: str) -> str:
    """Convert image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Add product with image
image_base64 = encode_image("product_photo.jpg")

collection.data.insert(
    properties={
        "name": "Wireless Headphones",
        "description": "Premium noise-cancelling headphones",
        "image": image_base64,  # Base64 encoded
        "price": 299.99,
        "category": "Electronics"
    }
)

print("✅ Product with image uploaded")
```

#### Batch Upload Multiple Images

```python
from pathlib import Path
import base64

collection = client.collections.get("ProductCatalog")

# Directory with product images
image_dir = Path("products/")
products = [
    {"name": "Headphones", "price": 299.99, "image_file": "headphones.jpg"},
    {"name": "Laptop", "price": 1299.99, "image_file": "laptop.jpg"},
    {"name": "Phone", "price": 799.99, "image_file": "phone.jpg"},
]

with collection.batch.dynamic() as batch:
    for product in products:
        # Encode image
        image_path = image_dir / product["image_file"]
        with open(image_path, "rb") as img:
            image_base64 = base64.b64encode(img.read()).decode("utf-8")

        batch.add_object(
            properties={
                "name": product["name"],
                "description": f"Product: {product['name']}",
                "image": image_base64,
                "price": product["price"],
                "category": "Electronics"
            }
        )

print(f"✅ Uploaded {len(products)} products with images")
```

### 7. Upload Text Documents with Intelligent Chunking

#### Option A: Interactive Chunking (Recommended - No API Key)

When using Claude Skills interactively, ask Claude to analyze and chunk your document intelligently:

**Example Conversation:**
```
You: "I have a 50-page technical manual at /path/to/manual.pdf.
     Please read it, analyze the structure, and chunk it intelligently
     for my TechnicalDocuments collection."

Claude: *Reads the document*
        *Identifies sections, headings, logical boundaries*
        *Creates semantically complete chunks with metadata*
        *Uploads to Weaviate with proper section names, page numbers, topics*

        ✅ Uploaded 47 intelligent chunks:
           - HVAC Systems (pages 1-12): 8 chunks
           - Ductwork Design (pages 13-25): 12 chunks
           - Seismic Requirements (pages 26-35): 10 chunks
           ...
```

**Why This Works:**
- Claude understands document structure (headings, sections, topics)
- Chunks at natural semantic boundaries, not arbitrary character counts
- Extracts metadata automatically (section names, page numbers, image context)
- No API key needed - uses your existing Claude session
- Perfect for technical manuals, cookbooks, structured documents

**How to Use:**
1. Open the document in Claude (upload file or paste text)
2. Reference your collection name and desired chunking strategy
3. Claude analyzes structure and creates optimal chunks
4. Claude uploads directly to Weaviate with rich metadata

#### Option B: Simple Character-Based Chunking (No Intelligence)

For quick, automated chunking without semantic analysis:

```python
from pathlib import Path

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks (simple, no intelligence)"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

collection = client.collections.get("TechnicalDocuments")

# Read a long document
doc_path = Path("technical_manual.txt")
full_text = doc_path.read_text()

# Split into chunks
chunks = chunk_text(full_text, chunk_size=1000, overlap=200)

with collection.batch.dynamic() as batch:
    for i, chunk in enumerate(chunks):
        batch.add_object(
            properties={
                "title": f"Technical Manual - Section {i+1}",
                "content": chunk,
                "section": "Overview",
                "page": i + 1,
                "hasImage": False,
                "tags": ["technical", "manual"]
            }
        )

print(f"✅ Uploaded {len(chunks)} document chunks")
```

**Limitations:**
- Breaks at arbitrary character positions (may split sentences mid-word)
- No understanding of document structure
- Can't extract metadata automatically
- May separate related content

#### Option C: Markdown/Heading-Based Chunking

For documents with clear markdown structure:

```python
import re
from pathlib import Path

def chunk_by_headings(markdown_text: str) -> list[dict]:
    """Split markdown by ## headings, preserving structure"""
    chunks = []

    # Split on h2 headings
    sections = re.split(r'^## ', markdown_text, flags=re.MULTILINE)

    for section in sections[1:]:  # Skip content before first heading
        lines = section.split('\n')
        heading = lines[0].strip()
        content = '\n'.join(lines[1:]).strip()

        if content:
            chunks.append({
                'title': heading,
                'content': content,
                'section': heading
            })

    return chunks

# Read markdown file
doc_path = Path("documentation.md")
markdown = doc_path.read_text()

# Chunk by headings
chunks = chunk_by_headings(markdown)

collection = client.collections.get("TechnicalDocuments")

with collection.batch.dynamic() as batch:
    for i, chunk in enumerate(chunks):
        batch.add_object(
            properties={
                "title": chunk['title'],
                "content": chunk['content'],
                "section": chunk['section'],
                "page": i + 1,
                "hasImage": False,
                "tags": ["documentation"]
            }
        )

print(f"✅ Uploaded {len(chunks)} sections")
```

#### Option D: PDF Chunking with Page Awareness

For PDF documents with page structure:

```python
import PyPDF2
from pathlib import Path

def chunk_pdf_by_pages(pdf_path: str, pages_per_chunk: int = 3) -> list[dict]:
    """Chunk PDF by grouping pages together"""
    chunks = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        for start_page in range(0, total_pages, pages_per_chunk):
            end_page = min(start_page + pages_per_chunk, total_pages)

            # Extract text from pages
            text = ""
            for page_num in range(start_page, end_page):
                text += reader.pages[page_num].extract_text()

            chunks.append({
                'content': text,
                'page_start': start_page + 1,
                'page_end': end_page,
                'page_range': f"{start_page + 1}-{end_page}"
            })

    return chunks

# Chunk PDF
pdf_chunks = chunk_pdf_by_pages("technical_manual.pdf", pages_per_chunk=3)

collection = client.collections.get("TechnicalDocuments")

with collection.batch.dynamic() as batch:
    for chunk in pdf_chunks:
        batch.add_object(
            properties={
                "title": f"Pages {chunk['page_range']}",
                "content": chunk['content'],
                "section": "Unknown",  # Could be enhanced with heading detection
                "page": chunk['page_start'],
                "pageRange": chunk['page_range'],
                "hasImage": False,
                "tags": ["technical", "manual"]
            }
        )

print(f"✅ Uploaded {len(pdf_chunks)} page-based chunks")
```

**Recommendation:** Use **Option A (Interactive Chunking)** for best results with technical documents. Claude can understand your document structure and create semantically meaningful chunks with proper metadata.

### 8. Progress Tracking for Large Uploads

```python
from tqdm import tqdm  # pip install tqdm

collection = client.collections.get("Articles")

# Large dataset
large_dataset = [...]  # List of thousands of objects

batch_size = 100
total_batches = (len(large_dataset) + batch_size - 1) // batch_size

with tqdm(total=len(large_dataset), desc="Uploading") as pbar:
    with collection.batch.dynamic() as batch:
        for item in large_dataset:
            batch.add_object(properties=item)
            pbar.update(1)

print("✅ Upload complete!")
```

### 9. Update Existing Object

```python
collection = client.collections.get("Articles")

# Update by UUID
collection.data.update(
    uuid="existing-uuid-here",
    properties={
        "title": "Updated Title",
        "content": "New content..."
    }
)

print("✅ Object updated")
```

### 10. Delete Objects

```python
# Delete single object
collection.data.delete_by_id("uuid-to-delete")

# Delete multiple objects matching criteria
from weaviate.classes.query import Filter

collection.data.delete_many(
    where=Filter.by_property("author").equal("John Doe")
)

print("✅ Objects deleted")
```

## Batch Configuration Options

### Dynamic Batching (Recommended)

```python
# Automatically optimizes batch size
with collection.batch.dynamic() as batch:
    for item in data:
        batch.add_object(properties=item)
```

### Fixed Batch Size

```python
# Control batch size manually
with collection.batch.fixed_size(batch_size=100) as batch:
    for item in data:
        batch.add_object(properties=item)
```

### Rate Limiting

```python
# Add rate limiting for API quota management
with collection.batch.rate_limit(requests_per_minute=600) as batch:
    for item in data:
        batch.add_object(properties=item)
```

## Data Validation Best Practices

### 1. Validate Before Insert

```python
def validate_article(article: dict) -> bool:
    """Validate article has required fields"""
    required_fields = ["title", "content", "author"]
    return all(field in article for field in required_fields)

# Filter valid articles
valid_articles = [a for a in articles if validate_article(a)]
invalid_count = len(articles) - len(valid_articles)

if invalid_count > 0:
    print(f"⚠️  Skipping {invalid_count} invalid articles")

# Upload only valid data
with collection.batch.dynamic() as batch:
    for article in valid_articles:
        batch.add_object(properties=article)
```

### 2. Handle Missing Fields

```python
def normalize_article(article: dict) -> dict:
    """Fill in missing fields with defaults"""
    return {
        "title": article.get("title", "Untitled"),
        "content": article.get("content", ""),
        "author": article.get("author", "Unknown"),
        "publishDate": article.get("publishDate", datetime.now().isoformat()),
        "tags": article.get("tags", [])
    }

normalized = [normalize_article(a) for a in articles]
```

### 3. Type Conversion

```python
from datetime import datetime

def prepare_for_weaviate(item: dict) -> dict:
    """Ensure correct data types"""
    return {
        "title": str(item["title"]),
        "content": str(item["content"]),
        "page": int(item["page"]),
        "hasImage": bool(item.get("hasImage", False)),
        "publishDate": datetime.fromisoformat(item["date"]).isoformat()
    }
```

## Performance Tips

1. **Use Batch Operations**: Always use batching for multiple objects (10-100x faster)
2. **Optimal Batch Size**: Start with 100-200 objects per batch
3. **Connection Reuse**: Keep one client connection for entire upload
4. **Progress Tracking**: Use `tqdm` for visibility on long uploads
5. **Error Recovery**: Save failed objects to retry later
6. **Parallel Processing**: For very large datasets, consider parallel batch uploads

## Complete Example: Import Document Collection

```python
import json
import base64
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import weaviate
from weaviate.util import generate_uuid5

# Connect
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=weaviate.auth.Auth.api_key(os.getenv("WEAVIATE_API_KEY"))
)

try:
    collection = client.collections.get("TechnicalDocuments")

    # Load data
    data_file = Path("documents.json")
    with open(data_file) as f:
        documents = json.load(f)

    print(f"📄 Loaded {len(documents)} documents")

    # Track results
    successful = 0
    failed = []

    # Batch upload with progress bar
    with tqdm(total=len(documents), desc="Uploading") as pbar:
        with collection.batch.dynamic() as batch:
            for i, doc in enumerate(documents):
                try:
                    # Encode image if present
                    if doc.get("image_path"):
                        with open(doc["image_path"], "rb") as img:
                            doc["image"] = base64.b64encode(img.read()).decode("utf-8")
                        del doc["image_path"]

                    # Add to batch
                    batch.add_object(
                        properties=doc,
                        uuid=generate_uuid5(f"{doc['title']}-{i}")
                    )
                    successful += 1

                except Exception as e:
                    failed.append({"index": i, "error": str(e)})

                pbar.update(1)

    # Results
    print(f"\n✅ Successfully uploaded: {successful}")
    if failed:
        print(f"❌ Failed: {len(failed)}")
        # Save failed items
        with open("failed_uploads.json", "w") as f:
            json.dump(failed, f, indent=2)
        print("   Failed items saved to failed_uploads.json")

finally:
    client.close()
```

## Troubleshooting

### Issue: "Object validation failed"
- **Cause**: Property types don't match schema
- **Solution**: Check data types match collection schema exactly
- **Example**: Collection expects `INT` but you're sending string "42"

### Issue: "Batch insert timeout"
- **Cause**: Batch size too large or network issues
- **Solution**: Reduce batch size or add retry logic

### Issue: "Invalid base64 for BLOB"
- **Cause**: Image not properly encoded
- **Solution**: Use `base64.b64encode().decode("utf-8")`

### Issue: "UUID already exists"
- **Cause**: Trying to insert duplicate UUID
- **Solution**: Use `generate_uuid5()` with unique content or let Weaviate auto-generate

### Issue: Images uploaded but semantic image search doesn't work

- **Cause**: Collection is using a text-only vectorizer (e.g., `text2vec-openai`, `text2vec-cohere`) instead of a multimodal vectorizer
- **Symptoms**:
  - Images store successfully as base64 strings
  - Searching for images by visual similarity returns poor results
  - Only text-based searches work
- **Solution**:
  1. Check your collection's vectorizer configuration:
     ```python
     config = collection.config.get()
     print(f"Current vectorizer: {config.vectorizer}")
     ```
  2. If using a text-only vectorizer, you have two options:
     - **Option A**: Create a new collection with a multimodal vectorizer (`multi2vec-clip` or `multi2vec-bind`) and re-import your data
     - **Option B**: Keep text-only vectorizer but understand images won't be semantically searchable (only stored as properties)
  3. Use the **weaviate-collection-manager** skill to create a properly configured multimodal collection

### Issue: "Vectorizer doesn't support this data type"

- **Cause**: Attempting to vectorize data types incompatible with the collection's vectorizer
- **Examples**:
  - Using `text2vec-*` vectorizers with image/audio/video data
  - Using `img2vec-*` vectorizers with text-only data
- **Solution**: Match your data types to compatible vectorizers:
  - **Text only**: `text2vec-openai`, `text2vec-cohere`, `text2vec-huggingface`
  - **Images + Text**: `multi2vec-clip`, `multi2vec-bind`
  - **Images only**: `img2vec-neural`
- **Prevention**: Always verify vectorizer compatibility before ingestion (see Section 6 validation code)

## Next Steps

After ingesting data:
- Use **weaviate-query-agent** skill to search and retrieve data
- Verify data with collection queries
- Monitor collection size and performance

## Additional Resources

- [Weaviate Batch Import Docs](https://weaviate.io/developers/weaviate/manage-data/import)
- [Data Types Reference](https://weaviate.io/developers/weaviate/config-refs/datatypes)