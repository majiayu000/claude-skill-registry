---
name: context-ranking
description: "Rank an existing set of context chunks by relevance, diversity, freshness, and utility. Use when retrieval has already produced candidates that must be scored or reranked; use context-retrieval when the source corpus still needs to be searched."
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: "1.0.0"
---

# Context Ranking

Context ranking is the process of ordering retrieved text chunks so the most relevant, diverse, and useful information rises to the top. In any retrieval pipeline, the initial search returns a broad set of candidates -- many of which are only tangentially related to the query. Ranking transforms this unordered candidate set into a prioritized list, enabling downstream steps (context assembly, prompt construction) to select the best material and discard the rest. Effective ranking is the difference between a grounded, precise answer and a vague, off-topic one.

## Workflow

1. **Collect Candidate Chunks**: Gather the initial set of retrieved chunks from the search layer. This is typically the top-k results (k = 15-30) from a vector search, keyword search, or hybrid search. Each chunk arrives with a preliminary score (e.g., cosine similarity or BM25 score) and source metadata.

2. **Apply First-Stage Scoring**: Score each candidate with a fast, lightweight algorithm. BM25 is the standard choice for keyword relevance; cosine similarity between the query embedding and chunk embedding is the standard for semantic relevance. In hybrid pipelines, compute both scores and combine them using Reciprocal Rank Fusion (RRF) or a weighted linear combination. This stage is meant to be fast and run over all candidates.

3. **Rerank with a Cross-Encoder**: Pass the top candidates (typically 15-25) from the first stage through a cross-encoder reranker. Unlike bi-encoder embeddings that score query and document independently, a cross-encoder processes the query and chunk together with full attention, producing much more accurate relevance scores. Models like Cohere Rerank, `bge-reranker-v2-m3`, or ColBERTv2 are commonly used. This step is slower but dramatically improves precision.

4. **Apply Diversity Selection**: After reranking, the top results may cluster around a single subtopic, leaving other aspects of the query uncovered. Apply Maximal Marginal Relevance (MMR) or a similar diversity algorithm to penalize chunks that are too similar to already-selected chunks. This ensures the final ranked list covers the breadth of the query, not just its most obvious interpretation.

5. **Assign Final Scores and Rank**: Combine the reranker relevance score with the diversity penalty and any domain-specific boosting signals (e.g., recency boost, source authority weight) into a final composite score. Sort chunks by this composite score in descending order. The top-n chunks (n = 3-7) form the final ranked context to be injected into the prompt.

6. **Attach Metadata and Confidence**: Annotate each ranked chunk with its final score, source path, and a confidence tier (high / medium / low). This metadata helps the downstream prompt assembly step decide how to present the context and allows the model to calibrate its confidence when citing sources.

## Key Concepts

- **BM25**: A probabilistic keyword-matching algorithm based on term frequency, inverse document frequency, and document length normalization. Excels at matching exact terms and rare keywords. Fast and interpretable, but blind to synonyms and paraphrases. The standard first-stage ranker for keyword search.
- **Cosine Similarity**: Measures the angle between two embedding vectors. Values range from -1 to 1, with higher values indicating greater semantic similarity. The standard first-stage ranker for semantic search. Quality depends heavily on the embedding model used.
- **Cross-Encoder Reranking**: A transformer model that takes the concatenation of query and document as input and outputs a relevance score. Because it applies full cross-attention between query and document tokens, it captures fine-grained relevance that bi-encoders miss. Typically 5-20x slower than cosine similarity but produces significantly better ranking.
- **Maximal Marginal Relevance (MMR)**: An algorithm that iteratively selects chunks by balancing relevance to the query against redundancy with already-selected chunks. Controlled by a lambda parameter: lambda = 1.0 selects purely by relevance, lambda = 0.0 selects purely by diversity, and values around 0.5-0.7 balance both. Essential for multi-faceted queries.
- **Reciprocal Rank Fusion (RRF)**: A score-combining method used in hybrid search. For each chunk, compute 1/(k + rank) for each ranking source, then sum. This produces a fused ranking that is robust to score scale differences between BM25 and cosine similarity.

## Usage

Provide a query and a list of candidate text chunks (with optional preliminary scores and metadata). The skill scores, reranks, and diversifies the chunks, returning a ranked list with final scores and confidence tiers. Specify the desired number of output chunks (top-n) and an optional diversity parameter (MMR lambda).

## Examples

### Example 1: Ranking Code Search Results for a Debugging Query

**Query:** "Why does the WebSocket connection drop after 60 seconds of inactivity?"

**Candidate Chunks (from hybrid search, top-8):**

| # | Source | BM25 | Cosine | Content Summary |
|---|--------|------|--------|-----------------|
| 1 | `src/ws/server.ts:40-65` | 12.4 | 0.88 | WebSocket server config with `pingInterval: 30000` and `pingTimeout: 60000` |
| 2 | `src/ws/server.ts:80-95` | 8.1 | 0.82 | Connection cleanup handler that logs "connection timed out" |
| 3 | `docs/websocket.md:15-30` | 6.3 | 0.79 | Documentation: "Connections are kept alive via ping/pong. Default timeout is 60s." |
| 4 | `src/ws/client.ts:10-35` | 5.7 | 0.84 | Client-side WebSocket wrapper -- does not implement pong response handler |
| 5 | `nginx.conf:22-28` | 9.8 | 0.71 | Nginx proxy config: `proxy_read_timeout 60s` for WebSocket upstream |
| 6 | `CHANGELOG.md:44-50` | 3.2 | 0.55 | "v2.1: Fixed WebSocket reconnection logic" -- no timeout details |
| 7 | `src/ws/server.ts:100-120` | 4.5 | 0.76 | Rate limiting middleware for WebSocket messages |
| 8 | `package.json:15-20` | 2.1 | 0.45 | `"ws": "^8.14.0"` dependency entry |

**After Cross-Encoder Reranking:**

| Rank | # | Reranker Score | Reason |
|------|---|----------------|--------|
| 1 | 1 | 0.96 | Directly shows the 60s timeout configuration |
| 2 | 5 | 0.93 | Nginx proxy timeout -- a second cause of 60s drops |
| 3 | 4 | 0.89 | Client missing pong handler -- explains why pings fail |
| 4 | 2 | 0.85 | Cleanup handler confirms timeout behavior |
| 5 | 3 | 0.78 | Documentation corroborates the 60s default |
| 6 | 7 | 0.42 | Rate limiting -- marginally related |
| 7 | 6 | 0.30 | Changelog -- no useful detail |
| 8 | 8 | 0.15 | Package.json -- irrelevant |

**After MMR Diversity Selection (top-5, lambda=0.6):**
1. `src/ws/server.ts:40-65` (score 0.96) -- Server-side 60s timeout config
2. `nginx.conf:22-28` (score 0.93) -- Nginx proxy 60s read timeout (different source of the problem)
3. `src/ws/client.ts:10-35` (score 0.89) -- Client missing pong handler (client-side root cause)
4. `src/ws/server.ts:80-95` (score 0.85) -- Cleanup handler confirms the timeout behavior
5. `docs/websocket.md:15-30` (score 0.78) -- Documentation confirming 60s default

The ranked list covers three distinct causes (server config, nginx proxy, client pong handler) plus confirmation from the cleanup handler and docs.

### Example 2: Ranking Documentation Chunks for a Q&A Task

**Query:** "How do I configure SSO with SAML for my organization?"

**Candidate Chunks (top-6 from vector search):**

| # | Source | Cosine | Content Summary |
|---|--------|--------|-----------------|
| 1 | `docs/sso/saml-setup.md` | 0.91 | Step-by-step SAML configuration: metadata URL, certificate upload, attribute mapping |
| 2 | `docs/sso/overview.md` | 0.85 | Overview of SSO options: SAML, OIDC, LDAP. High-level comparison. |
| 3 | `docs/sso/saml-setup.md` | 0.83 | Troubleshooting SAML errors: invalid signature, clock skew, missing NameID |
| 4 | `docs/sso/oidc-setup.md` | 0.80 | OIDC configuration guide -- not SAML |
| 5 | `docs/admin/org-settings.md` | 0.77 | Organization settings page: where to find the SSO configuration panel |
| 6 | `blog/sso-announcement.md` | 0.72 | Blog post announcing SSO feature launch -- marketing copy, no setup details |

**After Cross-Encoder Reranking and MMR (top-4, lambda=0.7):**
1. `docs/sso/saml-setup.md` (setup guide, score 0.95) -- Direct answer: step-by-step SAML configuration
2. `docs/admin/org-settings.md` (score 0.82) -- Where to access the SSO settings (different doc, complements #1)
3. `docs/sso/saml-setup.md` (troubleshooting, score 0.79) -- Anticipates common errors the user may encounter
4. `docs/sso/overview.md` (score 0.71) -- Provides broader context on SSO options

Chunk 4 (OIDC guide) was filtered as irrelevant to SAML. Chunk 6 (blog post) was filtered for low information density.

## Best Practices

- **Always rerank** -- never rely solely on embedding cosine similarity or BM25 for final ranking. A cross-encoder reranker on the top 15-25 results consistently improves precision by 15-30% in benchmarks.
- **Use hybrid first-stage scoring** -- combining BM25 and cosine similarity via RRF outperforms either alone, especially on queries that mix specific terms with general intent.
- **Apply MMR for multi-faceted queries** -- queries like "What causes X and how do I fix it?" have two sub-intents. Without diversity selection, the top results may all address causes and none address fixes.
- **Tune the MMR lambda parameter** -- start with lambda = 0.6 (slightly favoring relevance over diversity) and adjust based on your use case. Factoid Q&A benefits from higher lambda (0.7-0.8), while exploratory research benefits from lower lambda (0.4-0.5).
- **Cache reranker results** -- cross-encoder inference is expensive. If the same query-chunk pairs recur (common in multi-turn conversations), cache the reranker scores to avoid redundant computation.
- **Evaluate with NDCG and MRR** -- use Normalized Discounted Cumulative Gain and Mean Reciprocal Rank on a labeled test set to measure ranking quality. These metrics are more informative than simple Recall@k for ranking evaluation.

## Edge Cases

- **Tie scores**: When multiple chunks receive identical or near-identical reranker scores, break ties by preferring chunks from more authoritative sources, more recent documents, or chunks with higher information density.
- **Single-result queries**: Some queries have exactly one relevant chunk in the corpus. The ranking pipeline should still work correctly -- the reranker should score that chunk highly and MMR should not penalize it for lack of diversity.
- **Adversarial or noisy chunks**: Web-scraped or user-generated content may contain SEO spam or irrelevant keyword stuffing that inflates BM25 scores. The cross-encoder reranker typically handles this well, but consider adding a quality filter as a pre-processing step.
- **Cross-lingual queries**: When the query language differs from the corpus language, ensure the embedding model and reranker support cross-lingual matching, or add a translation step before ranking.
- **Very large candidate sets (100+)**: If the initial retrieval returns hundreds of candidates, add an intermediate filtering step (e.g., score threshold cutoff) before the cross-encoder to keep reranking latency manageable.
