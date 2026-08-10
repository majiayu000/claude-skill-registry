---
name: context-optimization
description: "Optimize a complete candidate context package by deduplicating, filtering, ordering, and allocating its token budget. Use when retrieved or assembled material is noisy or exceeds the useful context budget; use context-ranking for scoring chunks and context-compression for shrinking selected content."
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: "1.0.0"
---

# Context Optimization

Context optimization is the process of refining the raw context assembled for an AI model so that every token contributes meaningfully to the task. In a typical RAG or agent pipeline, the retrieved context often contains redundant passages, marginally relevant chunks, and poorly ordered information. Optimization transforms this raw material into a lean, high-signal context block that improves answer quality, reduces inference cost, and makes the most of the model's attention budget.

## Workflow

1. **Audit the Raw Context**: Inventory every piece of context that has been gathered -- retrieved documents, conversation history, tool outputs, and metadata. Measure the total token count and compare it against the available context budget. Identify the compression ratio needed if the raw context exceeds the budget.

2. **Deduplicate Overlapping Content**: Scan the context for near-duplicate passages that convey the same information. This is common in RAG pipelines where chunking with overlap produces multiple chunks covering the same paragraph, or when multiple source documents repeat the same facts. Use semantic similarity (cosine distance > 0.92) or exact n-gram overlap detection to identify duplicates, then keep only the most complete version of each piece of information.

3. **Score Relevance and Information Density**: Assign each context chunk two scores: a relevance score (how closely it relates to the current query) and an information density score (how many useful facts it conveys per token). Relevance can be measured via the retrieval score or a lightweight cross-encoder pass. Density can be estimated by counting named entities, code identifiers, numerical data, and key terms relative to chunk length. Multiply the two scores to produce a composite utility score.

4. **Filter Low-Value Content**: Remove chunks whose composite utility score falls below a threshold. A good starting point is to keep the top 60-70% of chunks by utility score. Also remove boilerplate text (copyright notices, navigation menus, repeated headers) that contributes zero information. Be conservative -- it is better to include a marginally relevant chunk than to lose a critical fact.

5. **Reorder by Priority**: Arrange the remaining chunks to maximize the model's attention. Place the highest-utility chunks first (models attend most to the beginning of the context) and the second-highest near the end (models also attend to recency). Avoid burying critical information in the middle of a long context block -- this is the "lost in the middle" zone where model attention is weakest.

6. **Validate Coverage**: After filtering and reordering, verify that the optimized context still covers all aspects of the query. If the query has multiple sub-questions, ensure at least one chunk addresses each. If coverage gaps appear, selectively re-add previously filtered chunks that fill the gap, even if their utility score was below the threshold.

## Techniques

- **Deduplication**: Identifies and removes redundant passages using semantic similarity thresholds or n-gram overlap detection. Critical in RAG pipelines where overlapping chunks often repeat the same sentences. Keeps the most complete or highest-scoring version.
- **Relevance Filtering**: Removes chunks that fall below a relevance threshold. Uses the original retrieval score, a reranker score, or keyword overlap with the query as the signal. Aggressiveness should be tuned -- filtering too hard causes coverage gaps.
- **Information Density Scoring**: Estimates how much useful information a chunk contains per token. Dense chunks (packed with facts, code, or data) are preferred over verbose, low-density prose. Useful for deciding which chunks to keep when two have similar relevance scores.
- **Priority-Based Ordering**: Arranges chunks so the model sees the most important information first and last, avoiding the "lost in the middle" effect. This is especially impactful for long context windows (32K+ tokens) where attention degradation is more pronounced.
- **Context Window Strategies**: Different model context windows require different optimization approaches. For small windows (4K tokens), aggressive filtering and compression are essential. For medium windows (32K), focus on deduplication and ordering. For large windows (128K+), ordering and density scoring matter most, since there is room for more material but the lost-in-the-middle effect is amplified.

## Usage

Provide the raw context (a list of text chunks with optional metadata and scores), the user query, and the target token budget. The skill returns an optimized context block -- deduplicated, filtered, scored, and reordered -- ready for prompt assembly. Optionally provide a coverage checklist (key topics the context must address) to prevent important information from being filtered out.

## Examples

### Example 1: Optimizing Context for a Multi-File Code Edit Task

**Task:** "Refactor the authentication module to use async/await instead of callbacks."

**Raw Context (7 chunks, ~4,200 tokens):**

| # | Source | Relevance | Density | Content Summary |
|---|--------|-----------|---------|-----------------|
| 1 | `src/auth/login.js:1-45` | 0.93 | High | Login function using callback-based `db.findUser()` |
| 2 | `src/auth/login.js:20-55` | 0.90 | High | Overlapping chunk -- duplicates lines 20-45 of chunk 1, adds token refresh logic |
| 3 | `src/auth/middleware.js:1-30` | 0.88 | High | Auth middleware with callback-based token verification |
| 4 | `README.md:100-130` | 0.45 | Low | Project setup instructions -- no code, no auth details |
| 5 | `src/auth/register.js:1-40` | 0.82 | High | Registration function using callbacks |
| 6 | `package.json:1-25` | 0.35 | Low | Dependency list -- no auth-related logic |
| 7 | `src/auth/login.js:40-70` | 0.91 | High | Token generation and session creation with callbacks |

**Optimization Steps:**
1. **Deduplicate:** Chunks 1 and 2 overlap on lines 20-45. Merge into a single chunk covering lines 1-55 of `login.js`.
2. **Filter:** Remove chunk 4 (README setup instructions, relevance 0.45) and chunk 6 (`package.json`, relevance 0.35) -- below the 0.50 threshold.
3. **Reorder:** Place merged login.js chunk first (highest relevance), then the token generation chunk, then middleware.js, then register.js.

**Optimized Context (~2,800 tokens, 33% reduction):**
1. `src/auth/login.js:1-55` (merged) -- Login function with callback-based DB lookup and token refresh
2. `src/auth/login.js:40-70` -- Token generation and session creation
3. `src/auth/middleware.js:1-30` -- Auth middleware with callback token verification
4. `src/auth/register.js:1-40` -- Registration function using callbacks

### Example 2: Optimizing RAG-Retrieved Context to Eliminate Redundancy

**Query:** "What is the company's return policy for electronics?"

**Raw Retrieved Chunks (6 chunks, ~3,000 tokens):**
1. `returns-policy.md` (score 0.95) -- "Electronics purchased from our store may be returned within 30 days of purchase. Items must be in original packaging with all accessories. A 15% restocking fee applies to opened items."
2. `faq.md` (score 0.88) -- "Q: Can I return electronics? A: Yes, within 30 days. Items must be in original packaging. A 15% restocking fee applies to opened items. See our returns policy for full details."
3. `holiday-policy.md` (score 0.72) -- "During the holiday season (Nov 15 - Jan 15), the return window for all products, including electronics, is extended to 60 days. All other conditions apply."
4. `shipping-info.md` (score 0.40) -- "We ship electronics via insured ground shipping. Delivery takes 3-7 business days."
5. `returns-policy.md` (score 0.85) -- "Refunds are processed to the original payment method within 5-10 business days. Defective items are exempt from the restocking fee and may be returned within 90 days."
6. `store-locator.md` (score 0.30) -- "Visit any of our 200 retail locations nationwide."

**Optimization Steps:**
1. **Deduplicate:** Chunks 1 and 2 convey nearly identical information (30-day window, original packaging, 15% fee). Keep chunk 1 (higher score, more authoritative source).
2. **Filter:** Remove chunk 4 (shipping info, not about returns, score 0.40) and chunk 6 (store locator, irrelevant, score 0.30).
3. **Reorder:** Chunk 1 (core policy) then chunk 5 (refund processing) then chunk 3 (holiday extension).

**Optimized Context (~900 tokens, 70% reduction):**
1. Core policy: 30-day return window, original packaging required, 15% restocking fee for opened items.
2. Refund details: processed to original payment method in 5-10 business days; defective items exempt from restocking fee, 90-day window.
3. Holiday extension: Nov 15 - Jan 15, return window extended to 60 days.

## Best Practices

- **Deduplicate before filtering** -- removing redundant passages first gives you a clearer picture of the unique information available, leading to better filtering decisions.
- **Tune thresholds on your domain** -- relevance and density score thresholds vary by use case. A code-generation task may need stricter relevance filtering than a general Q&A task. Calibrate on a labeled evaluation set.
- **Preserve diversity of sources** -- when multiple chunks have similar scores, prefer keeping chunks from different source documents to increase coverage and reduce bias toward a single source.
- **Account for the lost-in-the-middle effect** -- for context windows above 8K tokens, place the most critical chunks at the beginning and end of the context block. Test with your specific model, as the effect varies across architectures.
- **Log what you filter** -- record which chunks were removed and why. This makes it possible to debug cases where the model gives an incomplete answer because a needed chunk was filtered out.
- **Re-optimize when the query changes** -- context that was optimal for one query may be suboptimal for a follow-up. In multi-turn conversations, re-run optimization when the user's intent shifts.

## Edge Cases

- **All chunks are highly relevant**: When every chunk scores above the threshold, skip filtering and focus on deduplication and ordering. Do not force removal of good content just to hit an arbitrary reduction target.
- **Query covers multiple distinct topics**: A complex query like "Compare the return policy and warranty terms" requires context covering both topics. Ensure the coverage validation step checks for both and does not filter all chunks about one topic.
- **Very small context windows (4K tokens)**: With tight budgets, aggressive compression after optimization may still be needed. Optimize first to remove waste, then compress the remainder if it still exceeds the budget.
- **Rapidly changing source data**: In live systems where documents are updated frequently, cached optimization results may become stale. Invalidate and re-optimize when source documents change.
- **Context with mixed content types**: When context includes prose, code, tables, and JSON, apply type-specific density scoring -- a 10-line code snippet is typically denser than a 10-line prose paragraph.
