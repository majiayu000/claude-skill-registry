---
name: milvus-vectors
description: Work with vector search, embeddings, or semantic retrieval using Milvus on DGX Spark.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(curl:*)
---

# Milvus Vectors Skill

## Milvus Configuration

| Setting | Value |
|---------|-------|
| Endpoint | `https://dgx-milvus.pentatonic.com` |
| Collection | `products_v2` |
| Dimensions | 1024 |
| Embedding Model | NVIDIA NV-EmbedQA-E5-v5 |
| Auth | `Bearer root:Milvus` |

---

## Search Products

```javascript
async function searchProducts(embedding, { limit = 10, filter = null } = {}) {
  const body = {
    collectionName: "products_v2",
    data: [embedding],
    annsField: "embedding",
    limit,
    outputFields: ["canonical_id", "title", "brand", "price", "category", "image_url"],
  };

  if (filter) {
    body.filter = filter;  // e.g., "category == 'footwear'"
  }

  const response = await fetch("https://dgx-milvus.pentatonic.com/v2/vectordb/entities/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer root:Milvus",
    },
    body: JSON.stringify(body),
  });

  const result = await response.json();
  return result.data;
}
```

---

## Insert Product

```javascript
async function insertProduct(product, embedding) {
  const response = await fetch("https://dgx-milvus.pentatonic.com/v2/vectordb/entities/insert", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer root:Milvus",
    },
    body: JSON.stringify({
      collectionName: "products_v2",
      data: [{
        id: product.identity.canonical_id,  // Use canonical ID
        canonical_id: product.identity.canonical_id,
        title: product.attributes.core.title,
        brand: product.attributes.core.brand,
        category: product.taxonomy.category_path.join(" > "),
        price: product.value_profile?.msrp || 0,
        image_url: product.media?.images?.[0]?.url || "",
        embedding: embedding,
      }],
    }),
  });

  return response.json();
}
```

---

## Generate Embedding

```javascript
async function generateEmbedding(text) {
  const response = await fetch("https://dgx-embeddings.pentatonic.com/embed", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const result = await response.json();
  return result.embedding;  // 1024-dimensional vector
}

// For product identification
async function identifyProduct(imageDescription) {
  const embedding = await generateEmbedding(imageDescription);
  const candidates = await searchProducts(embedding, { limit: 5 });

  return candidates.map(c => ({
    canonical_id: c.canonical_id,
    title: c.title,
    brand: c.brand,
    score: c.distance,
  }));
}
```

---

## Collection Schema

```javascript
// Reference: products_v2 collection schema
const schema = {
  fields: [
    { name: "id", type: "VarChar", max_length: 64, is_primary: true },
    { name: "canonical_id", type: "VarChar", max_length: 64 },
    { name: "title", type: "VarChar", max_length: 512 },
    { name: "brand", type: "VarChar", max_length: 128 },
    { name: "category", type: "VarChar", max_length: 256 },
    { name: "price", type: "Float" },
    { name: "image_url", type: "VarChar", max_length: 512 },
    { name: "embedding", type: "FloatVector", dim: 1024 },
  ],
  index: {
    field_name: "embedding",
    index_type: "IVF_FLAT",
    metric_type: "COSINE",
    params: { nlist: 1024 },
  },
};
```

---

## Anti-Patterns

- Using non-canonical IDs in Milvus
- Not including canonical_id in outputFields
- Hardcoding embedding dimensions
- No error handling for Milvus failures
