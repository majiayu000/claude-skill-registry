---
name: sqlite-vec
description: sqlite-vec extension for vector similarity search in SQLite. Use when storing embeddings, performing KNN queries, or building semantic search features. Triggers on sqlite-vec, vec0, MATCH, vec_distance, partition key, float[N], int8[N], bit[N], serialize_float32, serialize_int8, vec_f32, vec_int8, vec_bit, vec_normalize, vec_quantize_binary, distance_metric, metadata columns, auxiliary columns.
---

# sqlite-vec

sqlite-vec is a lightweight SQLite extension for vector similarity search. It enables storing and querying vector embeddings directly in SQLite databases without external vector databases.

## Quick Reference

### Load Extension
```python
import sqlite3
import sqlite_vec
from sqlite_vec import serialize_float32

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)
```

### Basic KNN Query
```sql
-- Create table
CREATE VIRTUAL TABLE vec_items USING vec0(
  embedding float[4]
);

-- Insert vectors (use serialize_float32() in Python)
INSERT INTO vec_items(rowid, embedding)
VALUES (1, X'CDCCCC3DCDCC4C3E9A99993E00008040');

-- KNN query
SELECT rowid, distance
FROM vec_items
WHERE embedding MATCH '[0.3, 0.3, 0.3, 0.3]'
  AND k = 10
ORDER BY distance;
```

## Core Concepts

### Vector Types

sqlite-vec supports three vector element types:

1. **float[N]** - 32-bit floating point (4 bytes per element)
   - Most common for embeddings (OpenAI, Cohere, etc.)
   - Example: `float[1536]` for text-embedding-3-small

2. **int8[N]** - 8-bit signed integers (1 byte per element)
   - Range: -128 to 127
   - Used for quantized embeddings

3. **bit[N]** - Binary vectors (1 bit per element, packed into bytes)
   - Most compact storage
   - Used for binary quantization

### Binary Serialization Format

Vectors must be provided as binary BLOBs or JSON strings. Python helper functions:

```python
from sqlite_vec import serialize_float32, serialize_int8
import struct

# Float32 vectors
vector = [0.1, 0.2, 0.3, 0.4]
blob = serialize_float32(vector)
# Equivalent to: struct.pack("%sf" % len(vector), *vector)

# Int8 vectors
int_vector = [1, 2, 3, 4]
blob = serialize_int8(int_vector)
# Equivalent to: struct.pack("%sb" % len(int_vector), *int_vector)
```

NumPy arrays can be passed directly (must cast to float32):
```python
import numpy as np
embedding = np.array([0.1, 0.2, 0.3, 0.4]).astype(np.float32)
db.execute("SELECT vec_length(?)", [embedding])
```

## vec0 Virtual Tables

The vec0 virtual table is the primary data structure for vector search.

### Basic Table Creation
```sql
CREATE VIRTUAL TABLE vec_documents USING vec0(
  document_id integer primary key,
  contents_embedding float[768]
);
```

### Distance Metrics
```sql
CREATE VIRTUAL TABLE vec_items USING vec0(
  embedding float[768] distance_metric=cosine
);
```

Supported metrics: `l2` (default), `cosine`, `hamming` (bit vectors only)

### Column Types

vec0 tables support four column types:

1. **Vector columns** - Store embeddings (float[N], int8[N], bit[N])
2. **Metadata columns** - Indexed, filterable in KNN queries
3. **Partition key columns** - Internal sharding for faster filtered queries
4. **Auxiliary columns** - Unindexed storage (prefix with +)

Example with all column types:
```sql
CREATE VIRTUAL TABLE vec_knowledge_base USING vec0(
  document_id integer primary key,

  -- Partition keys (sharding)
  organization_id integer partition key,
  created_month text partition key,

  -- Vector column
  content_embedding float[768] distance_metric=cosine,

  -- Metadata columns (filterable in KNN)
  document_type text,
  language text,
  word_count integer,
  is_public boolean,

  -- Auxiliary columns (not filterable)
  +title text,
  +full_content text,
  +url text
);
```

## KNN Queries

### Standard Query Syntax
```sql
SELECT rowid, distance
FROM vec_items
WHERE embedding MATCH ?
  AND k = 10
ORDER BY distance;
```

Key components:
- `WHERE embedding MATCH ?` - Triggers KNN query
- `AND k = 10` - Limit to 10 nearest neighbors
- `ORDER BY distance` - Sort results by proximity

### Metadata Filtering
```sql
SELECT document_id, distance
FROM vec_movies
WHERE synopsis_embedding MATCH ?
  AND k = 5
  AND genre = 'scifi'
  AND num_reviews BETWEEN 100 AND 500
  AND mean_rating > 3.5
  AND contains_violence = false
ORDER BY distance;
```

Supported operators on metadata: `=`, `!=`, `>`, `>=`, `<`, `<=`, `BETWEEN`

Not supported: `IS NULL`, `LIKE`, `GLOB`, `REGEXP`, scalar functions

### Partition Key Filtering
```sql
SELECT document_id, distance
FROM vec_documents
WHERE contents_embedding MATCH ?
  AND k = 20
  AND user_id = 123  -- Partition key pre-filters
ORDER BY distance;
```

Partition keys enable multi-tenant or temporal sharding. Best practices:
- Each unique partition value should have 100+ vectors
- Use 1-2 partition keys maximum
- Avoid over-sharding (too many unique values)

### Joining with Source Tables
```sql
WITH knn_matches AS (
  SELECT document_id, distance
  FROM vec_documents
  WHERE contents_embedding MATCH ?
    AND k = 10
)
SELECT
  documents.id,
  documents.title,
  knn_matches.distance
FROM knn_matches
LEFT JOIN documents ON documents.id = knn_matches.document_id
ORDER BY knn_matches.distance;
```

## Distance Functions

For manual distance calculations (non-vec0 tables):

```sql
-- L2 distance
SELECT vec_distance_l2('[1, 2]', '[3, 4]');
-- 2.8284...

-- Cosine distance
SELECT vec_distance_cosine('[1, 1]', '[2, 2]');
-- ~0.0

-- Hamming distance (bit vectors)
SELECT vec_distance_hamming(vec_bit(X'F0'), vec_bit(X'0F'));
-- 8
```

## Vector Operations

### Constructors
```sql
-- Float32
SELECT vec_f32('[.1, .2, .3, 4]');  -- Subtype 223

-- Int8
SELECT vec_int8('[1, 2, 3, 4]');  -- Subtype 225

-- Bit
SELECT vec_bit(X'F0');  -- Subtype 224
```

### Metadata Functions
```sql
-- Get length
SELECT vec_length('[1, 2, 3]');  -- 3

-- Get type
SELECT vec_type(vec_int8('[1, 2]'));  -- 'int8'

-- Convert to JSON
SELECT vec_to_json(vec_f32('[1, 2]'));  -- '[1.000000,2.000000]'
```

### Arithmetic
```sql
-- Add vectors
SELECT vec_to_json(
  vec_add('[.1, .2, .3]', '[.4, .5, .6]')
);
-- '[0.500000,0.700000,0.900000]'

-- Subtract vectors
SELECT vec_to_json(
  vec_sub('[.1, .2, .3]', '[.4, .5, .6]')
);
-- '[-0.300000,-0.300000,-0.300000]'
```

### Transformations
```sql
-- Normalize (L2 norm)
SELECT vec_to_json(
  vec_normalize('[2, 3, 1, -4]')
);
-- '[0.365148,0.547723,0.182574,-0.730297]'

-- Slice (for Matryoshka embeddings)
SELECT vec_to_json(
  vec_slice('[1, 2, 3, 4]', 0, 2)
);
-- '[1.000000,2.000000]'

-- Matryoshka pattern: slice then normalize
SELECT vec_normalize(vec_slice(embedding, 0, 256))
FROM vec_items;
```

### Quantization
```sql
-- Binary quantization (positive→1, negative→0)
SELECT vec_quantize_binary('[1, 2, 3, 4, -5, -6, -7, -8]');
-- X'0F'

-- Visualize
SELECT vec_to_json(
  vec_quantize_binary('[1, 2, -3, 4, -5, 6, -7, 8]')
);
-- '[0,1,0,0,1,0,1,0]'
```

### Iteration
```sql
-- Iterate through elements
SELECT rowid, value
FROM vec_each('[1, 2, 3, 4]');
/*
┌───────┬───────┐
│ rowid │ value │
├───────┼───────┤
│ 0     │ 1     │
│ 1     │ 2     │
│ 2     │ 3     │
│ 3     │ 4     │
└───────┴───────┘
*/
```

## Python Integration

### Complete Example
```python
import sqlite3
import sqlite_vec
from sqlite_vec import serialize_float32

# Setup
db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

# Create table
db.execute("""
    CREATE VIRTUAL TABLE vec_items USING vec0(
        embedding float[4]
    )
""")

# Insert vectors
items = [
    (1, [0.1, 0.1, 0.1, 0.1]),
    (2, [0.2, 0.2, 0.2, 0.2]),
    (3, [0.3, 0.3, 0.3, 0.3])
]

with db:
    for rowid, vector in items:
        db.execute(
            "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
            [rowid, serialize_float32(vector)]
        )

# Query
query = [0.25, 0.25, 0.25, 0.25]
results = db.execute(
    """
    SELECT rowid, distance
    FROM vec_items
    WHERE embedding MATCH ?
      AND k = 2
    ORDER BY distance
    """,
    [serialize_float32(query)]
).fetchall()

for rowid, distance in results:
    print(f"rowid={rowid}, distance={distance}")
```

### Embedding API Integration
```python
from openai import OpenAI
from sqlite_vec import serialize_float32

client = OpenAI()

# Generate embedding
response = client.embeddings.create(
    input="your text here",
    model="text-embedding-3-small"
)
embedding = response.data[0].embedding

# Store in sqlite-vec
db.execute(
    "INSERT INTO vec_documents(id, embedding) VALUES(?, ?)",
    [doc_id, serialize_float32(embedding)]
)

# Query
query_embedding = client.embeddings.create(
    input="search query",
    model="text-embedding-3-small"
).data[0].embedding

results = db.execute(
    """
    SELECT id, distance
    FROM vec_documents
    WHERE embedding MATCH ?
      AND k = 10
    """,
    [serialize_float32(query_embedding)]
).fetchall()
```

## Performance Tips

1. **Use partition keys** for multi-tenant or temporally-filtered queries
2. **Keep k reasonable** (10-100 for most use cases)
3. **Filter with metadata** columns when possible
4. **Choose appropriate distance metric** for your embeddings
5. **Batch operations** in transactions
6. **Use auxiliary columns** for large data not needed in filtering
7. **Ensure partition keys have 100+ vectors** per unique value

## Common Patterns

### Multi-tenant Search
```sql
CREATE VIRTUAL TABLE vec_docs USING vec0(
  doc_id integer primary key,
  user_id integer partition key,
  embedding float[768]
);

SELECT doc_id, distance
FROM vec_docs
WHERE embedding MATCH ? AND k = 10 AND user_id = 123;
```

### Hybrid Search
```sql
SELECT product_id, distance
FROM vec_products
WHERE embedding MATCH ?
  AND k = 20
  AND category = 'electronics'
  AND price < 1000.0
ORDER BY distance;
```

### Matryoshka Embeddings
```sql
-- Adaptive dimensions: slice then normalize
SELECT vec_normalize(vec_slice(embedding, 0, 256))
FROM vec_items;
```

## Reference Files

- [setup.md](./references/setup.md) - Installation, extension loading, Python bindings, NumPy integration
- [tables.md](./references/tables.md) - vec0 table creation, column types, metadata/partition/auxiliary columns
- [queries.md](./references/queries.md) - KNN query patterns, metadata filtering, partition filtering, optimization
- [operations.md](./references/operations.md) - Vector operations, constructors, transformations, quantization, batch operations

## Resources

- Official documentation: https://alexgarcia.xyz/sqlite-vec
- GitHub repository: https://github.com/asg017/sqlite-vec
- Python package: https://pypi.org/project/sqlite-vec/
- API reference: https://alexgarcia.xyz/sqlite-vec/api-reference.html
