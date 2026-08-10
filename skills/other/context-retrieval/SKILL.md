---
name: context-retrieval
description: "Retrieve relevant information from a knowledge base using semantic, keyword, or hybrid search to ground a query. Use when the task starts with a corpus or index that must be searched; use context-ranking when candidate chunks already exist and only need ordering."
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: "1.0.0"
---

# Context Retrieval

Context retrieval is the process of finding and assembling the most relevant pieces of information from a knowledge base to ground an AI agent's responses in factual, up-to-date data. It is the backbone of Retrieval Augmented Generation (RAG) and ensures that generated outputs are accurate and verifiable rather than hallucinated.

## Workflow

1. **Embed the Query**: Convert the user's natural-language query into a dense vector representation using an embedding model (e.g., OpenAI `text-embedding-3-small`, Cohere `embed-v3`, or an open-source model like `bge-large`). The embedding captures the semantic meaning of the query so it can be compared against stored documents.

2. **Search the Vector Store**: Send the query embedding to a vector database (Pinecone, Weaviate, Qdrant, Chroma, etc.) and perform an approximate nearest-neighbor (ANN) search. Request the top-k candidate chunks, typically k = 10–20 to give the reranker enough material to work with.

3. **Rerank the Results**: Pass the candidate chunks through a cross-encoder reranker (e.g., Cohere Rerank, `bge-reranker-large`, or a ColBERT model). The reranker scores each chunk against the original query with full attention, producing much more accurate relevance scores than cosine similarity alone. Keep the top-n results (typically n = 3–5).

4. **Assemble the Context Window**: Concatenate the selected chunks into a single context block, ordered by relevance score descending. Prepend source metadata (file path, URL, page number) to each chunk so the agent can cite its sources. Ensure the total token count fits the model's budget for the context section of the prompt.

5. **Generate the Response**: Feed the assembled context into the LLM prompt alongside the original query and a system instruction that tells the model to answer only from the provided context. This grounds the response in retrieved facts and reduces hallucination.

6. **Validate and Cite**: After generation, verify that the answer references information actually present in the retrieved chunks. Attach inline citations or a references section so the user can trace each claim back to a source document.

## Key Concepts

- **Semantic Search**: Uses vector embeddings to find documents by meaning rather than exact keyword match. Excels at paraphrasing and synonym handling but can miss precise technical terms.
- **Keyword Search (BM25)**: Traditional term-frequency search that excels at exact matches and rare terms. Fast and interpretable but blind to synonyms.
- **Hybrid Search**: Combines semantic and keyword search (e.g., weighted fusion of BM25 + cosine similarity scores) to get the best of both worlds. Most production RAG systems use hybrid retrieval.
- **Chunking Strategies**: Documents must be split into chunks before indexing. Common strategies include fixed-size token windows (256–512 tokens with 50-token overlap), sentence-boundary splitting, and recursive character splitting. Smaller chunks improve precision; larger chunks preserve more context.
- **Embedding Models**: The choice of embedding model affects retrieval quality. Larger models (1024+ dimensions) capture more nuance but cost more to store and query. Always benchmark on your domain before choosing.

## Usage

To use this skill, you need a pre-indexed knowledge base with document embeddings stored in a vector database. Provide a natural-language query as input. The skill returns the retrieved context block ready for prompt assembly, along with source metadata for citation.

## Examples

### Example 1: Retrieving Codebase Context for a Code Question

**Query:** "How does the authentication middleware validate JWT tokens?"

**Retrieved Chunks (after reranking):**

| Rank | Source | Score | Snippet |
|------|--------|-------|---------|
| 1 | `src/middleware/auth.ts:14-38` | 0.94 | `export function validateToken(req, res, next) { const token = req.headers.authorization?.split(' ')[1]; if (!token) return res.status(401).json({ error: 'Missing token' }); try { const decoded = jwt.verify(token, process.env.JWT_SECRET); req.user = decoded; next(); } catch (e) { return res.status(403).json({ error: 'Invalid token' }); } }` |
| 2 | `docs/auth-flow.md:8-22` | 0.87 | "The JWT is signed with HS256 using the JWT_SECRET env var. Tokens expire after 24 hours. The middleware extracts the token from the Authorization header, verifies the signature, and attaches the decoded payload to `req.user`." |
| 3 | `tests/auth.test.ts:5-19` | 0.72 | Test cases covering valid token, expired token, and malformed token scenarios. |

**Assembled Prompt:**
```
Answer the following question using ONLY the provided context. Cite file paths.

Context:
[1] src/middleware/auth.ts:14-38 — export function validateToken(req, res, next) { ... }
[2] docs/auth-flow.md:8-22 — The JWT is signed with HS256 using the JWT_SECRET env var...
[3] tests/auth.test.ts:5-19 — Test cases covering valid token, expired token...

Question: How does the authentication middleware validate JWT tokens?
```

### Example 2: Retrieving Product Docs for a Support Question

**Query:** "How do I reset my password if I no longer have access to my email?"

**Retrieved Chunks:**
1. `help/account-recovery.md` (score 0.91) — "If you cannot access your registered email, navigate to Settings > Account > Identity Verification. You will be asked to verify your identity using your phone number or a government-issued ID. Once verified, you can set a new email and reset your password."
2. `help/password-reset.md` (score 0.85) — "To reset your password, click 'Forgot Password' on the login page. A reset link will be sent to your registered email address. The link expires after 1 hour."

**Generated Answer:** "Since you no longer have access to your email, use the identity verification flow: go to Settings > Account > Identity Verification, verify via phone number or government ID, update your email address, then reset your password from the login page. [Sources: help/account-recovery.md, help/password-reset.md]"

## Best Practices

- **Use hybrid retrieval** in production — combining BM25 keyword search with semantic vector search consistently outperforms either approach alone.
- **Always rerank** — a cross-encoder reranker on the top-20 results dramatically improves precision compared to relying on embedding cosine similarity alone.
- **Chunk with overlap** — use 10–20% token overlap between adjacent chunks to prevent splitting critical information across chunk boundaries.
- **Include metadata** — store file paths, section headings, timestamps, and authors alongside embeddings so retrieved context is traceable and citable.
- **Tune top-k empirically** — retrieve more candidates than you need (k = 15–20), then let the reranker narrow to the best 3–5. This balances recall and precision.
- **Benchmark regularly** — measure retrieval quality with metrics like Recall@k, MRR, and NDCG on a labeled evaluation set from your domain.

## Edge Cases

- **No relevant results found**: When the top retrieval score is below a confidence threshold (e.g., < 0.5), the agent should acknowledge that it does not have enough information rather than fabricating an answer.
- **Contradictory sources**: If retrieved chunks contain conflicting information, surface both perspectives and note the discrepancy rather than silently picking one.
- **Stale or outdated content**: Documents indexed months ago may be outdated. Include timestamps in metadata and prefer more recent chunks when scores are close.
- **Very short or very long queries**: Single-word queries may produce noisy results — consider query expansion. Very long queries may benefit from decomposition into sub-queries with results merged.
- **Multi-language knowledge bases**: Ensure the embedding model supports the languages present in the corpus, or use a translation step before embedding.
