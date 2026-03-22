---
name: sparse-retrieval-eval
description: >
  Evaluate sparse retrieval models on standard IR benchmarks (BEIR, MIRACL, mMARCO).
  Covers all IR metrics (nDCG@k, Recall@k, MAP, MRR), dataset loading, sparse corpus
  encoding to CSR matrices, IDF-weighted retrieval, caching, and result interpretation.
  Triggers on: evaluate retrieval, BEIR benchmark, nDCG, recall@k, sparse retrieval
  evaluation, MIRACL evaluation, information retrieval metrics, IR evaluation,
  search quality metrics.
---

# Sparse Retrieval Evaluation

Complete reference for evaluating sparse retrieval models on standard IR benchmarks.

---

## 1. IR Evaluation Metrics

All metrics implementations are in `resources/metrics.py` (importable).

### nDCG@k (Normalized Discounted Cumulative Gain)

The standard metric for graded relevance. Used as the primary metric in BEIR and MIRACL.

```
DCG@k  = sum_{i=1}^{k} (2^{rel_i} - 1) / log2(i + 1)
nDCG@k = DCG@k / IDCG@k
```

Where IDCG@k is DCG@k computed on the ideal (best possible) ranking. Range: [0, 1].

**Implementation note:** The denominator is `log2(i + 1)` where `i` is 1-indexed. In 0-indexed code this becomes `log2(i + 2)`.

### Recall@k

Fraction of relevant documents found in the top-k results.

```
Recall@k = |retrieved@k ∩ relevant| / |relevant|
```

**Important:** Only documents with relevance > 0 in qrels count as relevant. Documents absent from qrels are non-relevant (score 0), not unjudged.

### MAP (Mean Average Precision)

For binary relevance. Average of precision values at each relevant-document rank.

```
AP(q) = (1/|relevant|) * sum_{k where doc_k relevant} Precision@k
MAP   = mean over queries of AP(q)
```

### MRR (Mean Reciprocal Rank)

```
RR(q) = 1 / rank_of_first_relevant_doc    (0 if none)
MRR   = mean over queries of RR(q)
```

### Using the metrics module

```python
from resources.metrics import evaluate_retrieval

# all_retrieved: {qid: [(doc_id, score), ...]}  -- sorted by score descending
# all_qrels:     {qid: {doc_id: int_relevance}}
results = evaluate_retrieval(all_retrieved, all_qrels, k_values=[1, 5, 10, 100])
# Returns: {"nDCG@10": 0.45, "Recall@100": 0.82, "MAP": 0.38, "MRR": 0.52, ...}
```

---

## 2. Loading Datasets

### 2.1 BEIR Datasets

BEIR provides a standard suite of IR benchmarks. Each dataset has `corpus.jsonl`, `queries.jsonl`, and `qrels/{split}.tsv`.

```python
import json, csv, os, urllib.request, zipfile

BEIR_URL = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{name}.zip"

def download_beir(name: str, data_dir: str = "data/beir") -> str:
    """Download and extract a BEIR dataset. Returns path to extracted dir."""
    os.makedirs(data_dir, exist_ok=True)
    zip_path = os.path.join(data_dir, f"{name}.zip")
    extract_path = os.path.join(data_dir, name)
    if not os.path.exists(extract_path):
        urllib.request.urlretrieve(BEIR_URL.format(name=name), zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(data_dir)
        os.remove(zip_path)
    return extract_path

def load_beir_corpus(dataset_path: str) -> dict[str, str]:
    """Load corpus as {doc_id: text}."""
    corpus = {}
    with open(os.path.join(dataset_path, "corpus.jsonl")) as f:
        for line in f:
            obj = json.loads(line)
            # BEIR convention: concatenate title and text
            text = (obj.get("title", "") + " " + obj.get("text", "")).strip()
            corpus[obj["_id"]] = text
    return corpus

def load_beir_queries(dataset_path: str) -> dict[str, str]:
    """Load queries as {query_id: text}."""
    queries = {}
    with open(os.path.join(dataset_path, "queries.jsonl")) as f:
        for line in f:
            obj = json.loads(line)
            queries[obj["_id"]] = obj["text"]
    return queries

def load_beir_qrels(dataset_path: str, split: str = "test") -> dict[str, dict[str, int]]:
    """Load qrels as {query_id: {doc_id: relevance}}."""
    qrels: dict[str, dict[str, int]] = {}
    qrels_path = os.path.join(dataset_path, "qrels", f"{split}.tsv")
    with open(qrels_path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            qid = row["query-id"]
            did = row["corpus-id"]
            rel = int(row["score"])
            qrels.setdefault(qid, {})[did] = rel
    return qrels
```

**Available BEIR datasets:** nfcorpus, fiqa, arguana, scidocs, scifact, trec-covid, nq, hotpotqa, dbpedia-entity, fever, climate-fever, quora, msmarco, cqadupstack, bioasq, signal1m, trec-news, robust04.

**Standard evaluation:** nDCG@10 on the test split.

### 2.2 MIRACL (Multilingual)

MIRACL provides multilingual IR benchmarks across 18 languages via HuggingFace.

```python
from datasets import load_dataset

def load_miracl(lang: str = "en", split: str = "dev"):
    """Load MIRACL topics/qrels and corpus for a given language.

    Args:
        lang: ISO language code (ar, bn, de, en, es, fa, fi, fr, hi, id,
              ja, ko, ru, sw, te, th, yo, zh).
        split: "train" or "dev" (test qrels are hidden).

    Returns:
        corpus: dict[str, str]  -- {doc_id: text}
        queries: dict[str, str] -- {query_id: text}
        qrels: dict[str, dict[str, int]] -- {qid: {did: relevance}}
    """
    # Topics and qrels
    topics_ds = load_dataset("miracl/miracl", lang, split=split)
    queries = {}
    qrels = {}
    for row in topics_ds:
        qid = row["query_id"]
        queries[qid] = row["query"]
        qrels[qid] = {}
        for pos in row.get("positive_passages", []):
            qrels[qid][pos["docid"]] = 1
        for neg in row.get("negative_passages", []):
            qrels[qid][neg["docid"]] = 0

    # Corpus (sharded, potentially large)
    corpus_ds = load_dataset("miracl/miracl-corpus", lang, split="train")
    corpus = {}
    for doc in corpus_ds:
        text = (doc.get("title", "") + " " + doc.get("text", "")).strip()
        corpus[doc["docid"]] = text

    return corpus, queries, qrels
```

**Important notes:**
- MIRACL test qrels are hidden (used for leaderboard). Use `dev` split for local evaluation.
- Corpus can be very large (e.g., English has ~33M passages). Consider streaming: `load_dataset(..., streaming=True)`.
- Standard metric: nDCG@10 on dev split.

### 2.3 mMARCO (Cross-lingual)

mMARCO provides translated MS MARCO passages and queries for cross-lingual evaluation.

```python
from datasets import load_dataset

def load_mmarco(
    doc_lang: str = "english",
    query_lang: str = "english",
    split: str = "train",
    max_docs: int | None = None,
):
    """Load mMARCO corpus and queries.

    Languages: arabic, chinese, dutch, english, french, german, hindi,
    indonesian, italian, japanese, portuguese, russian, spanish, vietnamese.

    For cross-lingual eval: use different doc_lang and query_lang.
    """
    # Documents
    collection = load_dataset(
        "unicamp-dl/mmarco", f"collection-{doc_lang}", split="collection"
    )
    corpus = {}
    for i, doc in enumerate(collection):
        if max_docs and i >= max_docs:
            break
        corpus[str(doc["id"])] = doc["text"]

    # Queries
    queries_ds = load_dataset(
        "unicamp-dl/mmarco", f"queries-{query_lang}", split=split
    )
    queries = {}
    for row in queries_ds:
        queries[str(row["id"])] = row["text"]

    return corpus, queries
```

**Note:** mMARCO uses MS MARCO qrels. Download them separately or use the `beir/msmarco` variant.

---

## 3. Sparse Encoding & CSR Matrix

### 3.1 Encoding Sparse Vectors to CSR

For large corpora, store the encoded representations as a scipy CSR (Compressed Sparse Row) matrix.

```python
from scipy.sparse import csr_matrix, save_npz, load_npz
import numpy as np

def encode_to_csr(
    sparse_vecs: list[dict[int, float]],
    sparse_dim: int,
) -> csr_matrix:
    """Convert a list of sparse vectors to a CSR matrix.

    Args:
        sparse_vecs: Each element is {dimension_index: value}.
        sparse_dim: Total vocabulary / dimension size.

    Returns:
        CSR matrix of shape (len(sparse_vecs), sparse_dim).
    """
    rows, cols, vals = [], [], []
    for i, sv in enumerate(sparse_vecs):
        if sv:
            dims = list(sv.keys())
            values = list(sv.values())
            rows.append(np.full(len(dims), i, dtype=np.int32))
            cols.append(np.array(dims, dtype=np.int32))
            vals.append(np.array(values, dtype=np.float32))
    if rows:
        all_rows = np.concatenate(rows)
        all_cols = np.concatenate(cols)
        all_vals = np.concatenate(vals)
    else:
        all_rows = np.array([], dtype=np.int32)
        all_cols = np.array([], dtype=np.int32)
        all_vals = np.array([], dtype=np.float32)
    return csr_matrix(
        (all_vals, (all_rows, all_cols)),
        shape=(len(sparse_vecs), sparse_dim),
    )
```

### 3.2 Batched Encoding for Large Corpora

For corpora that exceed memory, encode in batches and vertically stack.

```python
from scipy.sparse import vstack

def encode_corpus_batched(
    texts: list[str],
    encode_fn,  # callable: list[str] -> list[dict[int, float]]
    sparse_dim: int,
    batch_size: int = 512,
) -> csr_matrix:
    """Encode a large corpus in batches, returning a single CSR matrix."""
    matrices = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        vecs = encode_fn(batch)
        matrices.append(encode_to_csr(vecs, sparse_dim))
    return vstack(matrices, format="csr")
```

---

## 4. IDF Computation

Sparse retrieval models (SPLADE, etc.) output raw term weights. To match BM25-style scoring, apply IDF weighting at query time.

### 4.1 Computing IDF from the Corpus Matrix

```python
def compute_idf(corpus_matrix: csr_matrix) -> np.ndarray:
    """Compute IDF weights from document frequencies in the corpus.

    Uses Qdrant's BM25-inspired formula:
        idf(t) = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))

    where N = total documents, df(t) = documents containing term t.

    Args:
        corpus_matrix: CSR matrix of shape (N, vocab_size).

    Returns:
        1D array of IDF values, shape (vocab_size,).
    """
    N = corpus_matrix.shape[0]
    # Document frequency: number of docs where each dimension is non-zero
    df = np.array((corpus_matrix != 0).sum(axis=0)).flatten().astype(np.float64)
    idf = np.log(1.0 + (N - df + 0.5) / (df + 0.5))
    return idf.astype(np.float32)
```

**Note:** Unlike the classic BM25 IDF formula `ln((N - df + 0.5) / (df + 0.5))` which can go negative for terms in >50% of docs, this `ln(1 + ...)` variant is always non-negative. This is the same formula Qdrant uses for sparse vector search with `Modifier.IDF`.

---

## 5. IDF-Weighted Sparse Retrieval

### 5.1 Retrieval Pipeline

```python
def retrieve_top_k(
    query_vec: dict[int, float],
    corpus_matrix: csr_matrix,
    idf: np.ndarray,
    k: int = 100,
) -> list[tuple[int, float]]:
    """Retrieve top-k documents for a single query using IDF-weighted dot product.

    Score(q, d) = sum_{t in q ∩ d} query_weight(t) * doc_weight(t) * idf(t)

    Args:
        query_vec: Sparse query vector {dim: weight}.
        corpus_matrix: CSR matrix (N, vocab_size).
        idf: IDF array (vocab_size,).
        k: Number of results to return.

    Returns:
        List of (doc_index, score) sorted by score descending.
    """
    if not query_vec:
        return []

    # Build IDF-weighted query as a dense array (only non-zero dims matter)
    dims = np.array(list(query_vec.keys()), dtype=np.int32)
    weights = np.array(list(query_vec.values()), dtype=np.float32)
    weighted_query = np.zeros(corpus_matrix.shape[1], dtype=np.float32)
    weighted_query[dims] = weights * idf[dims]

    # Sparse-dense dot product (scipy handles this efficiently)
    scores = corpus_matrix.dot(weighted_query)

    # argpartition is O(N) vs O(N log N) for full sort
    if k < len(scores):
        top_indices = np.argpartition(scores, -k)[-k:]
        top_indices = top_indices[np.argsort(-scores[top_indices])]
    else:
        top_indices = np.argsort(-scores)

    return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]


def retrieve_all_queries(
    query_vecs: dict[str, dict[int, float]],
    corpus_matrix: csr_matrix,
    idf: np.ndarray,
    doc_ids: list[str],
    k: int = 100,
) -> dict[str, list[tuple[str, float]]]:
    """Retrieve for all queries. Returns {qid: [(doc_id, score), ...]}."""
    all_results = {}
    for qid, qvec in query_vecs.items():
        results = retrieve_top_k(qvec, corpus_matrix, idf, k)
        all_results[qid] = [(doc_ids[idx], score) for idx, score in results]
    return all_results
```

### 5.2 Batched Query Retrieval (Faster)

For many queries, batch them into a matrix multiply.

```python
def retrieve_batch(
    query_vecs: list[dict[int, float]],
    corpus_matrix: csr_matrix,
    idf: np.ndarray,
    k: int = 100,
) -> list[list[tuple[int, float]]]:
    """Batch retrieval using matrix multiplication.

    Converts queries to a CSR matrix, multiplies against corpus, extracts top-k.
    Much faster than per-query retrieval for large query sets.
    """
    sparse_dim = corpus_matrix.shape[1]
    # Build IDF-weighted query matrix
    rows, cols, vals = [], [], []
    for i, qvec in enumerate(query_vecs):
        if qvec:
            dims = list(qvec.keys())
            weights = list(qvec.values())
            idf_weights = [w * float(idf[d]) for d, w in zip(dims, weights)]
            rows.append(np.full(len(dims), i, dtype=np.int32))
            cols.append(np.array(dims, dtype=np.int32))
            vals.append(np.array(idf_weights, dtype=np.float32))

    if not rows:
        return [[] for _ in query_vecs]

    query_matrix = csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(len(query_vecs), sparse_dim),
    )

    # (num_queries, num_docs) = query_matrix @ corpus_matrix.T
    score_matrix = query_matrix.dot(corpus_matrix.T).toarray()

    results = []
    for i in range(len(query_vecs)):
        scores = score_matrix[i]
        if k < len(scores):
            top_idx = np.argpartition(scores, -k)[-k:]
            top_idx = top_idx[np.argsort(-scores[top_idx])]
        else:
            top_idx = np.argsort(-scores)
        results.append(
            [(int(idx), float(scores[idx])) for idx in top_idx if scores[idx] > 0]
        )
    return results
```

**Memory warning:** `score_matrix` is dense (num_queries x num_docs). For large corpora, process queries in small batches (e.g., 32-64 at a time).

---

## 6. Caching Encoded Corpora

Encoding a large corpus is expensive. Always cache the CSR matrix and IDF.

```python
import os
from scipy.sparse import save_npz, load_npz

def save_encoded_corpus(
    path: str,
    corpus_matrix: csr_matrix,
    idf: np.ndarray,
    doc_ids: list[str],
):
    """Save encoded corpus to disk."""
    os.makedirs(path, exist_ok=True)
    save_npz(os.path.join(path, "corpus.npz"), corpus_matrix)
    np.save(os.path.join(path, "idf.npy"), idf)
    with open(os.path.join(path, "doc_ids.txt"), "w") as f:
        for did in doc_ids:
            f.write(did + "\n")

def load_encoded_corpus(path: str):
    """Load cached encoded corpus."""
    corpus_matrix = load_npz(os.path.join(path, "corpus.npz"))
    idf = np.load(os.path.join(path, "idf.npy"))
    with open(os.path.join(path, "doc_ids.txt")) as f:
        doc_ids = [line.strip() for line in f]
    return corpus_matrix, idf, doc_ids
```

**Cache naming convention:** `cache/{model_name}/{dataset_name}/` -- this way different models or datasets never collide.

---

## 7. Complete Evaluation Pipeline

```python
def evaluate_sparse_model(
    model,                    # Has .encode_documents(texts) and .encode_queries(texts)
    corpus: dict[str, str],   # {doc_id: text}
    queries: dict[str, str],  # {query_id: text}
    qrels: dict[str, dict[str, int]],
    sparse_dim: int,
    cache_dir: str | None = None,
    batch_size: int = 512,
    k: int = 100,
) -> dict[str, float]:
    """Full evaluation pipeline for a sparse retrieval model.

    Steps:
    1. Encode corpus to CSR (or load from cache)
    2. Compute IDF from corpus
    3. Encode queries
    4. Retrieve top-k with IDF weighting
    5. Compute all metrics
    """
    doc_ids = list(corpus.keys())
    doc_texts = [corpus[did] for did in doc_ids]

    # Step 1-2: Encode corpus + compute IDF
    if cache_dir and os.path.exists(os.path.join(cache_dir, "corpus.npz")):
        corpus_matrix, idf, doc_ids = load_encoded_corpus(cache_dir)
    else:
        corpus_matrix = encode_corpus_batched(
            doc_texts, model.encode_documents, sparse_dim, batch_size
        )
        idf = compute_idf(corpus_matrix)
        if cache_dir:
            save_encoded_corpus(cache_dir, corpus_matrix, idf, doc_ids)

    # Step 3: Encode queries
    query_ids = [qid for qid in qrels if qid in queries]  # Only eval queries with qrels
    query_texts = [queries[qid] for qid in query_ids]
    query_vecs = model.encode_queries(query_texts)  # list[dict[int, float]]
    query_vec_map = dict(zip(query_ids, query_vecs))

    # Step 4: Retrieve
    all_retrieved = retrieve_all_queries(
        query_vec_map, corpus_matrix, idf, doc_ids, k=k
    )

    # Step 5: Evaluate
    from resources.metrics import evaluate_retrieval
    return evaluate_retrieval(all_retrieved, qrels, k_values=[1, 5, 10, 100])
```

---

## 8. Interpreting Results

### Reference Baselines (BEIR nDCG@10)

| Model            | NQ    | FiQA  | SciFact | HotpotQA | Avg   |
|------------------|-------|-------|---------|----------|-------|
| BM25             | 0.329 | 0.236 | 0.665   | 0.602    | 0.458 |
| SPLADE++ ED      | 0.521 | 0.346 | 0.693   | 0.684    | 0.561 |
| SPLADE++ SD      | 0.524 | 0.347 | 0.699   | 0.687    | 0.564 |
| Efficient SPLADE | 0.490 | 0.330 | 0.680   | 0.650    | 0.538 |

### What to Look For

- **nDCG@10 is the primary metric** for BEIR/MIRACL. Report this first.
- **Recall@100** measures retrieval coverage (important for re-ranking pipelines).
- **MAP and MRR** are secondary; useful for binary relevance datasets.
- Compare against BM25 baseline -- a sparse learned model should beat it.
- Large gap between Recall@100 and nDCG@10 suggests good coverage but poor ranking.
- High MRR but low nDCG@10 means the model finds *one* relevant doc well but misses others.

### Statistical Significance

For robust comparison, use paired t-test or bootstrap:

```python
from scipy.stats import ttest_rel

def paired_significance(
    per_query_a: list[float],
    per_query_b: list[float],
) -> float:
    """Return p-value for paired two-tailed t-test."""
    _, pval = ttest_rel(per_query_a, per_query_b)
    return pval
```

Report p < 0.05 as statistically significant.

---

## 9. Common Pitfalls

### Forgetting IDF Weighting
**Symptom:** nDCG@10 far below expected (e.g., 0.15 instead of 0.45).
**Cause:** Using raw sparse weights without IDF. Common terms dominate scoring.
**Fix:** Always multiply query weights by IDF: `score = q_weight * d_weight * idf`.

### Wrong qrels Split
**Symptom:** Zero or near-zero scores on all metrics.
**Cause:** Using `test` split qrels but `dev` split queries, or vice versa.
**Fix:** Ensure query IDs in your retrieval results match the qrels. Print overlap count:
```python
overlap = set(all_retrieved.keys()) & set(all_qrels.keys())
print(f"Evaluating {len(overlap)} / {len(all_qrels)} queries")
```

### Corpus Truncation Bias
**Symptom:** Suspiciously high scores on a subset evaluation.
**Cause:** Evaluating on a truncated corpus makes retrieval easier.
**Fix:** Always encode the full corpus. If you must subsample, include all qrels-relevant docs.

### Document ID Type Mismatch
**Symptom:** All metrics are 0.
**Cause:** qrels use string IDs `"123"` but retrieval returns int IDs `123`, or vice versa.
**Fix:** Ensure consistent string types everywhere. Cast explicitly.

### MIRACL Negative Passages Trap
**Symptom:** Inflated recall because negative passages from MIRACL are treated as relevant.
**Cause:** MIRACL `negative_passages` have relevance 0 but are present in qrels.
**Fix:** When computing recall, only count documents with relevance > 0 as relevant:
```python
relevant = {did for did, rel in qrel.items() if rel > 0}
```

### Memory Explosion on Batch Retrieval
**Symptom:** OOM when running batched matrix multiply.
**Cause:** Dense score matrix (num_queries x num_docs) for large corpora.
**Fix:** Process queries in small batches (32-64) or use per-query retrieval.

### Not Sorting Retrieved Results
**Symptom:** nDCG is random/low despite good recall.
**Cause:** Results not sorted by score descending before evaluation.
**Fix:** Always sort: `retrieved.sort(key=lambda x: x[1], reverse=True)`.
