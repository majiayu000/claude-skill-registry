---
name: cocoindex-v1
description: This skill should be used when building data processing pipelines with CocoIndex v1, a Python library for incremental data transformation. Use when the task involves processing files/data into databases, creating vector embeddings, building knowledge graphs, ETL workflows, or any data pipeline requiring automatic change detection and incremental updates. CocoIndex v1 is Python-native (supports any Python types), has no DSL, and is currently under pre-release (version 1.0.0a1 or later).
---

# CocoIndex v1

CocoIndex v1 is a Python library for building incremental data processing pipelines with declarative target states. Think spreadsheets or React for data pipelines: declare what the output should look like based on current input, and CocoIndex automatically handles incremental updates, change detection, and syncing to external systems.

## Overview

CocoIndex v1 enables building data pipelines that:

- **Automatically handle incremental updates**: Only reprocess changed data
- **Use declarative target states**: Declare what should exist, not how to update
- **Support any Python types**: No custom DSL—use dataclasses, Pydantic, NamedTuple
- **Provide function memoization**: Skip expensive operations when inputs/code unchanged
- **Sync to multiple targets**: PostgreSQL, SQLite, LanceDB, Qdrant, file systems

**Key principle**: `TargetState = Transform(SourceState)`

## When to Use This Skill

Use this skill when building pipelines that involve:

- **Document processing**: PDF/Markdown conversion, text extraction, chunking
- **Vector embeddings**: Embedding documents/code for semantic search
- **Database transformations**: ETL from source DB to target DB
- **Knowledge graphs**: Extract entities and relationships from data
- **LLM-based extraction**: Structured data extraction using LLMs
- **File-based pipelines**: Transform files from one format to another
- **Incremental indexing**: Keep search indexes up-to-date with source changes

## Quick Start: Creating a New Project

### Initialize Project

Use the built-in CLI to create a new project:

```bash
cocoindex init my-project
cd my-project
```

This creates:

- `main.py` - Main app definition
- `pyproject.toml` - Dependencies with pre-release config
- `.env` - Environment configuration
- `README.md` - Quick start guide

### Add Dependencies for Specific Use Cases

Add dependencies to `pyproject.toml` based on your needs:

```toml
# For vector embeddings
dependencies = ["cocoindex>=1.0.0a1", "sentence-transformers", "asyncpg"]

# For PostgreSQL only
dependencies = ["cocoindex>=1.0.0a1", "asyncpg"]

# For LLM extraction
dependencies = ["cocoindex>=1.0.0a1", "litellm", "instructor", "pydantic>=2.0"]
```

See [references/setup_project.md](references/setup_project.md) for complete examples.

### Set Up Database (if using Postgres/Qdrant)

For PostgreSQL with Docker:

```bash
# Create docker-compose.yml with pgvector image
docker-compose up -d
```

For Qdrant with Docker:

```bash
# Create docker-compose.yml with Qdrant image
docker-compose up -d
```

See [references/setup_database.md](references/setup_database.md) for detailed setup instructions.

### Run the Pipeline

```bash
pip install -e .
cocoindex update main.py
```

## Core Concepts

### 1. Apps

An **app** is the top-level executable that binds a main function with parameters:

```python
import cocoindex as coco

@coco.function
def app_main(sourcedir: pathlib.Path, outdir: pathlib.Path) -> None:
    # Processing logic here
    ...

app = coco.App(
    coco.AppConfig(name="MyApp"),
    app_main,
    sourcedir=pathlib.Path("./data"),
    outdir=pathlib.Path("./output"),
)

if __name__ == "__main__":
    app.update(report_to_stdout=True)
```

### 2. Processing Components

A **processing component** groups an item's processing with its target states.

**Mount independent components** with `coco_aio.mount_each()` (preferred) or `coco_aio.mount()`:

```python
# Preferred: mount one component per item (async, keyed iterable)
await coco_aio.mount_each(process_file, files.items(), target_table)

# Equivalent async manual loop
for key, f in files.items():
    await coco_aio.mount(coco.component_subpath(key), process_file, f, target_table)

# Sync mount — only for CPU-intensive leaf components (no I/O)
coco.mount(coco.component_subpath(str(f.file_path.path)), process_file, f, target_table)
```

**Mount dependent components** with `use_mount()` when you need the return value:

```python
result = await coco_aio.use_mount(subpath, fn, *args)
```

**Mount targets** using connector convenience methods (async, subpath is automatic):

```python
target_table = await target_db.mount_table_target(
    table_name="my_table",
    table_schema=await postgres.TableSchema.from_class(MyRecord, primary_key=["id"]),
)
```

**Key points**:

- Each component runs independently
- **Async-first**: prefer `coco_aio.mount_each()` / `coco_aio.mount()` for all components; use sync `coco.mount()` only for CPU-intensive leaf work (no I/O)
- Use `use_mount()` when you need the return value of a child component
- Use stable paths for proper memoization
- Component path determines target state ownership

### 3. Function Memoization

Add `memo=True` to skip re-execution when inputs/code unchanged:

```python
@coco.function(memo=True)
def expensive_operation(data: str) -> Result:
    # LLM call, embedding generation, heavy computation
    result = expensive_transform(data)
    return result
```

### 4. Target States

**Declare** what should exist—CocoIndex handles creation/update/deletion:

```python
# File target
localfs.declare_file(outdir / "output.txt", content)

# Database row target
table.declare_row(row=MyRecord(id=1, name="example"))

# Vector point target (Qdrant)
collection.declare_point(point=PointStruct(id="1", vector=[...]))
```

### 5. Context for Shared Resources

Use `ContextKey` to share expensive resources across components:

```python
EMBEDDER = coco.ContextKey[SentenceTransformerEmbedder]("embedder")

@coco.lifespan
def coco_lifespan(builder: coco.EnvironmentBuilder):
    embedder = SentenceTransformerEmbedder("all-MiniLM-L6-v2")
    builder.provide(EMBEDDER, embedder)
    yield
```

The `@coco.lifespan` decorator registers the function to the default CocoIndex environment, which is shared among all apps by default.

```python
@coco.function
def process_item(text: str) -> None:
    embedder = coco.use_context(EMBEDDER)
    embedding = embedder.embed(text)
```

### 6. ID Generation

Generate stable, unique identifiers that persist across incremental updates:

```python
from cocoindex.resources.id import generate_id, IdGenerator

# Deterministic: same dep → same ID
chunk_id = generate_id(chunk.content)

# Always distinct: each call → new ID, even with same dep
id_gen = IdGenerator()
for chunk in chunks:
    chunk_id = id_gen.next_id(chunk.content)
    table.declare_row(row=Row(id=chunk_id, content=chunk.content))
```

Use `generate_id(dep)` when same content should yield same ID. Use `IdGenerator` when you need distinct IDs even for duplicate content. See [ID Generation docs](https://cocoindex.io/docs-v1/resource_types#id-generation) for details.

## Common Pipeline Patterns

### Pattern 1: File Transformation

Transform files from input to output directory:

```python
import pathlib
import cocoindex as coco
import cocoindex.asyncio as coco_aio
from cocoindex.connectors import localfs
from cocoindex.resources.file import PatternFilePathMatcher

@coco.function(memo=True)
def process_file(file, outdir):
    # CPU-bound transform — sync is fine here at the leaf
    content = file.read_text()
    transformed = transform_content(content)  # Your logic
    outname = file.file_path.path.stem + ".out"
    localfs.declare_file(outdir / outname, transformed, create_parent_dirs=True)

@coco.function
async def app_main(sourcedir, outdir):
    files = localfs.walk_dir(
        sourcedir,
        recursive=True,
        path_matcher=PatternFilePathMatcher(
            included_patterns=["*.txt", "*.md"],
            excluded_patterns=[".*/**"],
        ),
    )
    await coco_aio.mount_each(process_file, files.items(), outdir)

app = coco_aio.App(coco_aio.AppConfig(name="Transform"), app_main, sourcedir=pathlib.Path("./data"), outdir=pathlib.Path("./out"))
```

### Pattern 2: Vector Embedding Pipeline

Chunk and embed documents for semantic search:

```python
import pathlib
from dataclasses import dataclass
from typing import Annotated, AsyncIterator
import cocoindex as coco
import cocoindex.asyncio as coco_aio
from cocoindex.connectors import localfs, postgres
from cocoindex.ops.text import RecursiveSplitter
from cocoindex.ops.sentence_transformers import SentenceTransformerEmbedder
from cocoindex.resources.chunk import Chunk
from cocoindex.resources.file import FileLike, PatternFilePathMatcher
from cocoindex.resources.id import IdGenerator
from numpy.typing import NDArray

PG_DB = coco.ContextKey[postgres.PgDatabase]("pg_db")
_embedder = SentenceTransformerEmbedder("sentence-transformers/all-MiniLM-L6-v2")
_splitter = RecursiveSplitter()

@dataclass
class DocEmbedding:
    id: int  # Generated stable ID
    filename: str
    text: str
    embedding: Annotated[NDArray, _embedder]  # Auto-infer dimensions
    chunk_start: int
    chunk_end: int

@coco_aio.lifespan
async def coco_lifespan(builder: coco_aio.EnvironmentBuilder) -> AsyncIterator[None]:
    async with await postgres.create_pool(DATABASE_URL) as pool:
        builder.provide(PG_DB, postgres.register_db("embedding_db", pool))
        yield

@coco.function
async def process_chunk(chunk: Chunk, filename: pathlib.PurePath, id_gen: IdGenerator, table):
    table.declare_row(
        row=DocEmbedding(
            id=await id_gen.next_id(chunk.text),
            filename=str(filename),
            text=chunk.text,
            embedding=await _embedder.embed(chunk.text),
            chunk_start=chunk.start.char_offset,
            chunk_end=chunk.end.char_offset,
        ),
    )

@coco.function(memo=True)
async def process_file(file: FileLike, table):
    text = file.read_text()
    chunks = _splitter.split(text, chunk_size=1000, chunk_overlap=200)
    id_gen = IdGenerator()
    await coco_aio.map(process_chunk, chunks, file.file_path.path, id_gen, table)

@coco.function
async def app_main(sourcedir: pathlib.Path):
    target_db = coco.use_context(PG_DB)
    target_table = await target_db.mount_table_target(
        table_name="embeddings",
        table_schema=await postgres.TableSchema.from_class(
            DocEmbedding, primary_key=["id"],
        ),
    )

    files = localfs.walk_dir(sourcedir, recursive=True)
    await coco_aio.mount_each(process_file, files.items(), target_table)

app = coco_aio.App(coco_aio.AppConfig(name="Embedding"), app_main, sourcedir=Path("./data"))
```

### Pattern 3: LLM-Based Extraction

Extract structured data using LLMs:

```python
import instructor
from pydantic import BaseModel
from litellm import acompletion

_instructor_client = instructor.from_litellm(acompletion, mode=instructor.Mode.JSON)

class ExtractionResult(BaseModel):
    title: str
    topics: list[str]

@coco.function(memo=True)  # Memo avoids re-calling LLM
async def extract_and_store(content, message_id, table):
    result = await _instructor_client.chat.completions.create(
        model="gpt-4",
        response_model=ExtractionResult,
        messages=[{"role": "user", "content": f"Extract topics: {content}"}],
    )
    table.declare_row(row=Message(id=message_id, title=result.title, content=content))
```

## Connectors and Operations

CocoIndex v1 provides connectors for reading from and writing to various external systems including databases (SQL and vector), file systems, and more.

**For detailed connector documentation**, see:
- [references/connectors.md](references/connectors.md) - Complete connector reference with examples
- [Pattern examples](#common-pipeline-patterns) - Real-world usage in pipelines
- [AI-optimized docs](https://cocoindex.io/docs-v1/llms.txt) - Comprehensive online documentation

## Text and Embedding Operations

### Text Splitting

```python
from cocoindex.ops.text import RecursiveSplitter, detect_code_language

splitter = RecursiveSplitter()
language = detect_code_language(filename="example.py")

chunks = splitter.split(
    text,
    chunk_size=1000,
    min_chunk_size=300,
    chunk_overlap=200,
    language=language,  # Syntax-aware splitting
)
```

### Embeddings

```python
from cocoindex.ops.sentence_transformers import SentenceTransformerEmbedder

embedder = SentenceTransformerEmbedder("sentence-transformers/all-MiniLM-L6-v2")

# Sync
embedding = embedder.embed(text)

# Async
embedding = await embedder.embed_async(text)
```

## CLI Commands

### Run Pipeline

```bash
cocoindex update main.py              # Run app in main.py
cocoindex update main.py:my_app       # Run specific app
cocoindex update my_module:my_app     # Run from module
```

### Drop All State

```bash
cocoindex drop main.py [-f]           # Drop and reset
```

### List Apps

```bash
cocoindex ls main.py                  # List apps in file
cocoindex ls --db ./cocoindex.db      # List apps in DB
```

### Show Component Paths

```bash
cocoindex show main.py                # Show component tree
```

## Best Practices

### 1. Use Stable Component Paths

```python
# ✅ Good: Stable identifiers
coco.component_subpath("file", str(file.file_path.path))
coco.component_subpath("record", record.id)

# ❌ Bad: Unstable identifiers
coco.component_subpath("file", file)      # Object reference
coco.component_subpath("idx", idx)        # Index changes
```

### 2. Add Memoization for Expensive Operations

```python
# ✅ Good: Memoize expensive ops
@coco.function(memo=True)
async def process_chunk(chunk, table):
    embedding = await embedder.embed_async(chunk.text)  # Expensive!
    table.declare_row(...)

# ❌ Bad: No memoization
@coco.function  # Re-embeds every run
async def process_chunk(chunk, table):
    embedding = await embedder.embed_async(chunk.text)
```

### 3. Use Context for Shared Resources

```python
# ✅ Good: Load model once
@coco.lifespan
def coco_lifespan(builder):
    model = load_expensive_model()
    builder.provide(MODEL_KEY, model)
    yield

# ❌ Bad: Load model every time
@coco.function
def process(data):
    model = load_expensive_model()  # Loaded repeatedly!
```

### 4. Use Type Annotations

```python
# ✅ Good: Type-safe
from dataclasses import dataclass
from typing import Annotated
from numpy.typing import NDArray

@dataclass
class Record:
    id: int
    name: str
    vector: Annotated[NDArray, embedder]  # Auto-infer dimensions

# ❌ Bad: No type safety
record = {"id": 1, "name": "example", "vector": [...]}
```

### 5. Use Convenience APIs for Targets and Iteration

```python
# Target setup — subpath is automatic
table = await target_db.mount_table_target(
    table_name="my_table",
    table_schema=await postgres.TableSchema.from_class(MyRecord, primary_key=["id"]),
)

# Iterate with mount_each — keys become component subpaths
await coco_aio.mount_each(process_item, items.items(), table)
```

### 6. Prefer Async Mount

```python
# ✅ Default: async mount for I/O-bound or general-purpose components
@coco.function
async def app_main(sourcedir):
    await coco_aio.mount_each(process_file, files.items(), table)  # list of items
    await coco_aio.mount(coco.component_subpath("setup"), setup_fn)  # single component

# ✅ Sync mount only when the leaf function is CPU-intensive (no I/O)
@coco.function(memo=True)
def cpu_heavy_leaf(data: str) -> Result:
    return expensive_computation(data)  # Pure CPU work, no async needed

# ❌ Don't use sync mount inside async app_main for general components
@coco.function
async def app_main(sourcedir):
    for key, f in files.items():
        coco.mount(coco.component_subpath(key), process_file, f)  # Use await coco_aio.mount() instead
```

## Migration from Old API

| Before | After |
|--------|-------|
| `await mount_run(subpath, fn, *args).result()` | `await use_mount(subpath, fn, *args)` |
| `for key, item in items: mount(subpath(key), fn, item, *args)` | `mount_each(fn, items, *args)` |
| `with component_subpath("setup"): await mount_run(...)` | `await mount_target(target)` or `await db.mount_table_target(...)` |
| `await asyncio.gather(*(fn(item) for item in items))` | `await map(fn, items)` |

## Troubleshooting

### "Module not found" Error

Ensure pyproject.toml has pre-release config:

```toml
[tool.uv]
prerelease = "explicit"
```

### PostgreSQL pgvector Not Found

Enable the pgvector extension:

```bash
# Connect to your database and enable the extension
psql "postgres://localhost/db" -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

See [references/setup_database.md](references/setup_database.md) for detailed setup instructions.

### Memoization Not Working

Check component paths are stable:

```python
# Use stable IDs, not object references
coco.component_subpath(file.stable_key)  # ✅
coco.component_subpath(file)             # ❌
```

### Everything Reprocessing

Add `memo=True` to expensive functions:

```python
@coco.function(memo=True)  # Add this
async def process_item(item):
    ...
```

## Resources

### references/

- **[setup_project.md](references/setup_project.md)**: Project setup guide with dependency examples for different use cases
- **[setup_database.md](references/setup_database.md)**: Database setup guide (PostgreSQL, SQLite, LanceDB, Qdrant)
- **[connectors.md](references/connectors.md)**: Complete connector reference with usage examples
- **[patterns.md](references/patterns.md)**: Detailed pipeline patterns with full working code
- **[api_reference.md](references/api_reference.md)**: Quick API reference for common functions

### assets/

- **simple-template/**: Minimal project template structure

## Additional Resources

**For AI Agents:**
- [AI-Optimized Documentation](https://cocoindex.io/docs-v1/llms.txt) - Comprehensive documentation optimized for LLM consumption

**For Humans:**
- [CocoIndex Documentation](https://docs.cocoindex.dev/docs-v1/) - Full documentation site
- [Programming Guide](https://docs.cocoindex.dev/docs-v1/programming_guide/core_concepts) - Core concepts and patterns
- [GitHub Examples](https://github.com/cocoindex-io/cocoindex/tree/v1/examples) - Real-world example projects
- [CocoIndex on PyPI](https://pypi.org/project/cocoindex/) - Package repository (pre-release)

## Version Note

This skill is for **CocoIndex v1** (pre-release: `>=1.0.0a1`). It uses a completely different API from v0. Key differences:

- Python-native (no DSL)
- Any Python types supported
- No flow definitions required
- More flexible and seamless experience
