---
name: google-gemini-file-search
description: Google Gemini File Search for managed RAG with 100+ file formats. Use for document Q&A, knowledge bases, or encountering immutability errors, quota issues, polling failures. Supports Gemini 3 Pro/Flash (Gemini 2.5 legacy).
license: MIT
metadata:
  version: "2.0.0"
  last_verified: "2025-11-18"
  production_tested: true
  token_savings: "~65%"
  errors_prevented: 8
  templates_included: 0
  references_included: 2
---

# Google Gemini File Search

**Status**: Production Ready | **Last Verified**: 2025-11-18

---

## What Is File Search?

Google Gemini File Search is **fully managed RAG** (Retrieval-Augmented Generation):
- Upload documents → Automatic chunking + embeddings + vector search + citations
- **No vector database setup** required
- **100+ file formats** supported (PDF, Word, Excel, code, Markdown, JSON, etc.)
- **Built-in grounding** with citation metadata
- **Cost-effective**: $0.15/1M tokens (one-time indexing), free storage + queries

**Key difference from other RAG:**
- Cloudflare Vectorize: You manage chunking/embeddings
- OpenAI Files API: Tied to Assistants API threads
- File Search: Fully managed, standalone RAG

---

## Quick Start (5 Minutes)

### 1. Get API Key & Install

Get API key: https://aistudio.google.com/apikey (Free tier: 1 GB storage, 1,500 requests/day)

```bash
bun add @google/genai
```

**Version:** 0.21.0+ | **Node.js:** 18+

### 2. Basic Example

```typescript
import { GoogleGenerativeAI } from '@google/genai';
import fs from 'fs';

const ai = new GoogleGenerativeAI(process.env.GOOGLE_AI_API_KEY);

// Create store
const fileStore = await ai.fileSearchStores.create({
  config: { displayName: 'my-knowledge-base' }
});

// Upload document
const operation = await ai.fileSearchStores.uploadToFileSearchStore({
  name: fileStore.name,
  file: fs.createReadStream('./manual.pdf'),
  config: {
    displayName: 'Installation Manual',
    chunkingConfig: {
      whiteSpaceConfig: {
        maxTokensPerChunk: 500,
        maxOverlapTokens: 50
      }
    }
  }
});

// Poll until done
while (!operation.done) {
  await new Promise(resolve => setTimeout(resolve, 1000));
  operation = await ai.operations.get({ name: operation.name });
}

// Query documents
const model = ai.getGenerativeModel({
  model: 'gemini-2.5-pro',  // Only 2.5 Pro/Flash supported
  tools: [{
    fileSearchTool: {
      fileSearchStores: [fileStore.name]
    }
  }]
});

const result = await model.generateContent('How do I install the product?');
console.log(result.response.text());

// Get citations
const grounding = result.response.candidates[0].groundingMetadata;
if (grounding) {
  console.log('Sources:', grounding.groundingChunks);
}
```

**Load `references/setup-guide.md` for complete walkthrough with batch uploads, error handling, and production checklist.**

---

## Critical Rules

### Always Do

1. **Use delete + re-upload** for updates (documents are immutable)
2. **Calculate 3x storage** (embeddings + metadata = ~3x file size)
3. **Configure chunking** (500 tokens for technical docs, 800 for prose)
4. **Poll operations** until `done: true` (with timeout)
5. **Use force: true** when deleting stores with documents
6. **Use Gemini 2.5 models** only (2.5-pro or 2.5-flash)
7. **Keep metadata under 20 fields** per document
8. **Estimate indexing costs** ($0.15/1M tokens one-time)

### Never Do

1. **Never try to update** documents (no PATCH API exists)
2. **Never assume storage = file size** (it's 3x)
3. **Never skip chunking config** (defaults may not be optimal)
4. **Never upload without polling** (operation may still be processing)
5. **Never delete without force** if store has documents
6. **Never use Gemini 1.5 models** (File Search requires 2.5)
7. **Never exceed 20 metadata fields** (hard limit)
8. **Never upload large files without cost estimate**

---

## Top 3 Errors Prevented

### Error 1: Document Immutability

**Problem:** Trying to update existing document

**Solution:** Delete + re-upload pattern

```typescript
// Find and delete old version
const docs = await ai.fileSearchStores.documents.list({
  parent: fileStore.name
});
const oldDoc = docs.documents.find(d => d.displayName === 'manual.pdf');
if (oldDoc) {
  await ai.fileSearchStores.documents.delete({
    name: oldDoc.name,
    force: true
  });
}

// Upload new version
await ai.fileSearchStores.uploadToFileSearchStore({
  name: fileStore.name,
  file: fs.createReadStream('manual-v2.pdf'),
  config: { displayName: 'manual.pdf' }
});
```

### Error 2: Storage Quota Exceeded

**Problem:** Storage calculation wrong (3x multiplier)

**Solution:** Estimate before upload

```typescript
const fileSize = fs.statSync('data.pdf').size;
const estimatedStorage = fileSize * 3;  // Embeddings + metadata

if (estimatedStorage > 1e9) {
  console.warn('⚠️ May exceed free tier 1 GB limit');
}
```

### Error 3: Model Compatibility

**Problem:** Using wrong model version

**Solution:** Use Gemini 2.5 only

```typescript
// ✅ CORRECT
const model = ai.getGenerativeModel({
  model: 'gemini-2.5-pro',  // or gemini-2.5-flash
  tools: [{ fileSearchTool: { fileSearchStores: [storeName] } }]
});

// ❌ WRONG
const model = ai.getGenerativeModel({
  model: 'gemini-1.5-pro',  // Not supported!
  tools: [{ fileSearchTool: { fileSearchStores: [storeName] } }]
});
```

**Load `references/error-catalog.md` for all 8 errors with detailed solutions including chunking, operation polling, metadata limits, and force delete requirements.**

---

## When to Use File Search

### Use File Search When:

- Want fully managed RAG (no vector DB)
- Cost predictability matters (one-time indexing)
- Need 100+ file format support
- Citations are important (built-in grounding)
- Simple deployment is priority
- Documents are relatively static

### Use Alternatives When:

**Cloudflare Vectorize** - Global edge performance, custom embeddings, real-time R2 updates
**OpenAI Files API** - Assistants API, conversational threads, very large collections (10,000+)

---

## Common Patterns

### Pattern 1: Customer Support Knowledge Base

```typescript
// Upload support docs with metadata
await ai.fileSearchStores.uploadToFileSearchStore({
  name: fileStore.name,
  file: fs.createReadStream('troubleshooting.pdf'),
  config: {
    displayName: 'Troubleshooting Guide',
    customMetadata: {
      doc_type: 'support',
      category: 'troubleshooting',
      language: 'en'
    }
  }
});
```

### Pattern 2: Batch Document Upload

```typescript
const files = ['doc1.pdf', 'doc2.md', 'doc3.docx'];
const uploadPromises = files.map(file =>
  ai.fileSearchStores.uploadToFileSearchStore({
    name: fileStore.name,
    file: fs.createReadStream(file),
    config: { displayName: file }
  })
);
const operations = await Promise.all(uploadPromises);

// Poll all operations
for (const op of operations) {
  let operation = op;
  while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    operation = await ai.operations.get({ name: operation.name });
  }
  console.log('✅', operation.response.displayName);
}
```

### Pattern 3: Document Update Flow

```typescript
// 1. List existing documents
const docs = await ai.fileSearchStores.documents.list({
  parent: fileStore.name
});

// 2. Delete old version
const oldDoc = docs.documents.find(d => d.displayName === 'manual.pdf');
if (oldDoc) {
  await ai.fileSearchStores.documents.delete({
    name: oldDoc.name,
    force: true
  });
}

// 3. Upload new version
const operation = await ai.fileSearchStores.uploadToFileSearchStore({
  name: fileStore.name,
  file: fs.createReadStream('manual-v2.pdf'),
  config: {
    displayName: 'manual.pdf',
    customMetadata: {
      version: '2.0',
      updated_at: new Date().toISOString()
    }
  }
});

// 4. Poll until done
while (!operation.done) {
  await new Promise(resolve => setTimeout(resolve, 1000));
  operation = await ai.operations.get({ name: operation.name });
}
```

**Load `references/setup-guide.md` for additional patterns including code documentation search and internal knowledge bases.**

---

## When to Load References

### Load `references/setup-guide.md` when:
- First-time File Search setup
- Need step-by-step walkthrough with all configuration options
- Configuring batch upload strategies
- Production deployment checklist
- Complete API initialization patterns

### Load `references/error-catalog.md` when:
- Encountering any of 8 common errors
- Need detailed error solutions with code examples
- Prevention checklist required
- Troubleshooting upload/query issues
- Understanding chunking, metadata, or cost calculation problems

---

## Supported File Formats

**100+ formats including:**
- **Documents**: PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx)
- **Text**: Markdown (.md), Plain text (.txt), JSON, CSV
- **Code**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, etc.

**Not supported:** Images in PDFs (text extraction only), Audio files, Video files

---

## Pricing

**Indexing (one-time):** $0.15 per 1M tokens
**Storage:** Free (10 GB - 1 TB depending on tier)
**Query embeddings:** Free (retrieved context counts as input tokens)

**Example:** 1,000-page document ≈ 500k tokens → Indexing cost: $0.075 → Storage: ~1.5 GB (3x multiplier)

---

## Chunking Guidelines

**Technical docs:** 500 tokens/chunk, 50 overlap
**Prose:** 800 tokens/chunk, 80 overlap
**Legal:** 300 tokens/chunk, 30 overlap

```typescript
chunkingConfig: {
  whiteSpaceConfig: {
    maxTokensPerChunk: 500,  // Smaller = more precise
    maxOverlapTokens: 50     // 10% overlap recommended
  }
}
```

---

## Resources

**References** (`references/`):
- `setup-guide.md` - Complete setup walkthrough (authentication, store creation, file upload, batch patterns, production checklist)
- `error-catalog.md` - All 8 documented errors with solutions (immutability, storage, chunking, metadata, costs, polling, force delete, model compatibility)

**Official Documentation**:
- **File Search Overview**: https://ai.google.dev/api/file-search
- **API Reference**: https://ai.google.dev/api/file-search/documents
- **Blog Post**: https://blog.google/technology/developers/file-search-gemini-api/

---

**Questions? Issues?**

1. Check `references/setup-guide.md` for complete setup
2. Review `references/error-catalog.md` for all 8 errors
3. Verify model version (must be Gemini 2.5)
4. Check storage calculation (3x file size)
