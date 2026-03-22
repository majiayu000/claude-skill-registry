---
name: minicoil-training
description: >
  miniCOIL v1 sparse neural retrieval model training methodology: per-word linear layer training
  with triplet loss, word vocabulary from frequency-filtered English words, sparse retrieval with
  jina-embeddings-v2-small-en encoder, sparse embedding training pipelines, OpenWebText sentence
  extraction for self-supervised training, semi-hard triplet mining, and evaluation on BEIR
  benchmarks. English-only miniCOIL v1 (jina-embeddings, 30k words, mxbai-embed-large-v1 mining).
  Reference for building, training, and deploying sparse neural retrieval models compatible with
  inverted indexes and Qdrant.
---

# miniCOIL Training Reference

Complete reference for training miniCOIL sparse neural retrieval models. Covers the full pipeline from word vocabulary construction through evaluation.

## What is miniCOIL?

miniCOIL is a lightweight sparse neural retrieval model created by Qdrant. It adds contextual semantic awareness to BM25-style keyword matching while preserving inverted-index compatibility.

**The core problem:** The same word has different meanings in different contexts ("fruit bat" vs. "baseball bat"). BM25 is blind to this. miniCOIL trains a tiny per-word linear layer that projects sentence embeddings into a 4D meaning space, letting the inverted index distinguish word senses.

### Scoring Formula

```
score(D, Q) = SUM_{i: q_i in D}  IDF(q_i) * dot(layer_i(emb_Q), layer_i(emb_D))
```

Where `layer_i` is the per-word Linear(512, 4) + tanh projection for word `i`.

| Component           | Source   | What it captures                                       |
|---------------------|----------|--------------------------------------------------------|
| IDF(q_i)            | BM25     | Inverse document frequency — rare terms matter more    |
| layer_i(emb_Q)      | miniCOIL | 4D meaning vector for word i in query context          |
| layer_i(emb_D)      | miniCOIL | 4D meaning vector for word i in document context       |
| dot(...)            | miniCOIL | Semantic similarity between matched word meanings      |

The sum runs only over words present in both Q and D. When a word is not in the vocabulary, it is invisible to miniCOIL (Qdrant can combine with BM25 in hybrid search to cover these).

### Comparison with Alternatives

| Property                  | BM25 | SPLADE | COIL   | miniCOIL |
|---------------------------|------|--------|--------|----------|
| Semantic awareness        | No   | Yes    | Yes    | Yes      |
| Inverted index compatible | Yes  | Yes*   | No     | Yes      |
| Domain-independent        | Yes  | No     | No     | Yes      |
| Needs relevance labels    | No   | Yes    | Yes    | No       |
| Computational cost        | Low  | High   | Medium | Low      |
| Document expansion        | No   | Yes    | No     | No       |

*SPLADE uses document expansion which reduces sparsity and increases index size.

**Why not SPLADE?** Requires relevance-labeled training data, making it domain-dependent. Document expansion increases index size and computational cost.

**Why not COIL?** Uses subword tokenization and end-to-end relevance training. Domain-dependent and incompatible with standard inverted indexes.

**Why miniCOIL?** Self-supervised (no labeled data), domain-independent, inverted-index compatible, and lightweight enough to train on a laptop.

---

## Architecture

- **Input encoder:** `jina-embeddings-v2-small-en` (512D, 33M params)
- **Mining encoder:** `mxbai-embed-large-v1` (1024D)
- **Vocabulary:** 30,000 most common English words (cleaned, stemmed, >3 chars)
- **Layer:** `Linear(512, 4) + tanh` per word
- **Training data:** 40M sentences from OpenWebText
- **Training time:** ~50 seconds per word on single CPU
- **Training samples:** ~8,000 sentences per word

### Key Design Decisions

**Why per-word?** Each word gets its own tiny linear layer. This allows the model to learn distinct 4D representations for different contextual usages of the same word.

**Why 4D output?** Empirically found to be the sweet spot between expressiveness and sparsity. Each word occupies exactly 4 cells in the sparse vector. More dimensions = larger index, diminishing returns on quality.

**Why tanh activation?** Bounds output to [-1, 1], preventing any single word from dominating the sparse dot product. Allows negative values, which encode "this context is unlike the typical usage of this word."

**Why triplet loss (not contrastive)?** Triplet loss with semi-hard mining works well for learning relative similarity without needing explicit labels. The margin parameter directly controls how far apart different senses need to be in the 4D space.

---

## Full Training Pipeline

### Step 1: Build Word Vocabulary

Build a vocabulary of the 30,000 most common English words from frequency lists. Words are cleaned, stemmed, and filtered to keep only words with >3 characters.

**Output:** `word_vocabulary.json` (30,000 English words)

### Step 2: Extract Training Sentences

Extract sentences from OpenWebText, match against the word vocabulary, and store in a training database.

**Process:**
1. Stream OpenWebText data (40 million sentences)
2. Split into sentences at sentence-ending punctuation
3. Filter: keep sentences with 5-100 words
4. Tokenize to lowercase, match against word vocabulary
5. Store with cap per word to avoid topical bias
6. Target: ~8,000 sentences per word

### Step 3: Per-Word Training

The core training loop. For each word:

1. **Fetch sentences** containing this word from the training database
2. **Encode with input encoder** (jina-embeddings-v2-small-en, 512D)
3. **Encode with mining encoder** (mxbai-embed-large-v1, 1024D) for harder triplet mining
4. **Mine triplets** (see Triplet Mining section below)
5. **Train** `Linear(512, 4) + tanh` with `TripletMarginLoss(margin=0.3)`, SGD
6. **Save** trained weight and bias

**Training loop per word (pseudocode):**
```python
layer = nn.Linear(512, 4)
optimizer = SGD(layer.parameters())
loss_fn = TripletMarginLoss(margin=0.3)

for epoch in range(num_epochs):
    a_out = tanh(layer(embs[anchor_idx]))
    p_out = tanh(layer(embs[pos_idx]))
    n_out = tanh(layer(embs[neg_idx]))
    loss = loss_fn(a_out, p_out, n_out)
    loss.backward()
    optimizer.step()
```

**Output:** `word_layers.pt` -- dict of `{word: {"weight": Tensor[4,512], "bias": Tensor[4]}}`.

### Step 4: Sparse Encoding

Converts text to sparse vectors at inference time:

1. Tokenize input text -> extract lowercase word tokens
2. Look up word indices in the vocabulary
3. Encode full text with jina-embeddings-v2-small-en -> 512D dense embedding
4. For each matched word: `output = tanh(W @ emb + b)` -> 4D meaning vector
5. Build sparse vector: `word_index * 4 + offset -> value`
6. Filter near-zero values (`|v| < 1e-6`)

**Sparse index formula:** `sparse_index = word_index * OUTPUT_DIM + dim_offset`
where `word_index` is the word's position in the vocabulary (0-29999) and `dim_offset` is 0-3.

```python
from minicoil.encoder import MiniCoilEncoder

encoder = MiniCoilEncoder("data/")

# Single text
sparse = encoder.encode_sparse("The cat sat on the mat")
# Returns: {168: 0.42, 169: -0.31, 170: 0.85, 171: -0.12, ...}

# Batch encoding
results = encoder.encode_batch_sparse(
    ["doc one", "doc two"],
    batch_size=64,
)
```

### Step 5: Evaluation

Evaluates on BEIR retrieval benchmarks using IDF-weighted sparse dot product.

**Pipeline:**
1. Download BEIR dataset (zip from TU Darmstadt)
2. Encode corpus -> scipy CSR sparse matrix (cached to disk for reuse)
3. Compute IDF: `log(1 + (N - df + 0.5) / (df + 0.5))` -- same formula as Qdrant's `Modifier.IDF`
4. Encode queries -> sparse vectors
5. IDF-weighted sparse dot product: `score = q_sparse_idf @ corpus_csr.T`
6. Compute nDCG@10

```bash
# English monolingual (BEIR)
minicoil evaluate --datasets nq quora fiqa hotpotqa msmarco
```

**Benchmarks:**

| Benchmark     | BM25    | miniCOIL v1 |
|---------------|---------|-------------|
| NQ            | 0.305   | 0.319       |
| Quora         | 0.789   | 0.802       |
| FiQA          | 0.236   | 0.257       |
| HotpotQA      | 0.633   | 0.633       |
| MS MARCO      | --      | --          |

---

## Triplet Mining Algorithm

The triplet mining is the heart of miniCOIL's training quality.

### For each triplet to mine:

1. **Select anchor:** Random sentence index from the word's sentence set
2. **Compute similarities:** Cosine similarity between anchor and all other sentences using the mining encoder embeddings (mxbai-embed-large-v1)
3. **Select positive (same-sense, high similarity):**
   - Get top-20 most similar sentences (`TRIPLET_TOPK=20`)
   - Random selection from top-20
4. **Select negative (different-sense, semi-hard):**
   - Semi-hard criterion: `neg_sim < pos_sim AND neg_sim > NEG_SIM_FLOOR` (floor=-1.5)
   - Choose the closest negative (highest similarity that is still below positive) -- this is the "hardest" semi-hard negative
   - Fallback: if no semi-hard candidates exist, pick the least similar sentence overall

### Adaptive triplet count

Actual triplets per word: `min(num_triplets, num_sentences * TRIPLETS_PER_SENTENCE_MULTIPLIER)`. With `TRIPLETS_PER_SENTENCE_MULTIPLIER=5`, a word with 100 sentences gets min(5000, 500) = 500 triplets. This prevents over-mining words with few sentences.

---

## Sparse Encoding Format

### Vector Layout

Each word occupies 4 consecutive cells in the sparse vector:

```
Word 0:     indices 0, 1, 2, 3
Word 1:     indices 4, 5, 6, 7
Word 42:    indices 168, 169, 170, 171
...
Word 29999: indices 119996, 119997, 119998, 119999
```

Total sparse dimension: `num_words * 4` = 30,000 * 4 = 120,000

### Qdrant Integration

miniCOIL sparse vectors are directly compatible with Qdrant's sparse vector feature:

```python
from qdrant_client import models

# Collection with IDF modifier (critical for miniCOIL)
client.create_collection(
    collection_name="minicoil",
    vectors_config={},
    sparse_vectors_config={
        "text": models.SparseVectorParams(
            modifier=models.Modifier.IDF,  # Qdrant computes IDF at query time
        )
    },
)

# Convert miniCOIL output to Qdrant format
sparse_dict = encoder.encode_sparse("The cat sat on the mat")
sv = models.SparseVector(
    indices=list(sparse_dict.keys()),
    values=list(sparse_dict.values()),
)
```

For hybrid search (dense + sparse), the dense embedding can be reused from the same jina-embeddings-v2-small-en encoder.

---

## Hyperparameter Guidance

### When to Change What

| Symptom | Likely Cause | Parameter to Adjust |
|---------|-------------|-------------------|
| Training loss stuck > 0.15 | Margin too high or learning rate too low | Decrease `margin` (try 0.1) or increase `lr` |
| Training loss drops to 0.0 | Margin too low, triplets too easy | Increase `margin` (try 0.5) |
| Poor monolingual quality | Too few sentences per word | Increase training data or lower vocabulary size |
| Training too slow | Too many triplets or too many epochs | Reduce `num_triplets` (try 2000) or epochs |
| Sparse vectors too dense | Too many words match per text | Increase min word length or reduce vocabulary size |
| Low eval scores despite low training loss | Overfitting per-word | Reduce epochs or increase margin |

### Default Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `output_dim` | 4 | Sparse vector dimensions per word |
| `input_dim` | 512 | jina-embeddings-v2-small-en embedding dimension |
| `margin` | 0.3 | Triplet loss margin |
| `num_triplets` | 5000 | Max triplets mined per word |
| `TRIPLET_TOPK` | 20 | Top-K candidates for positive selection |
| `NEG_SIM_FLOOR` | -1.5 | Minimum similarity for semi-hard negatives |
| `MIN_SENTENCES_PER_WORD` | 10 | Skip words with fewer sentences |
| `SPARSE_EPSILON` | 1e-6 | Filter threshold for near-zero sparse values |

---

## Common Failure Modes and Debugging

### Training

**Problem:** Training loss oscillates or NaN
**Cause:** Learning rate too high or degenerate triplets
**Fix:** Lower learning rate. Check that words have enough sentences (>= 10).

**Problem:** Training takes too long
**Cause:** Large vocabulary (30k words)
**Fix:** ~50 seconds per word on CPU. Total ~17 hours for full vocabulary on single CPU. Can be parallelized.

### Evaluation

**Problem:** All nDCG@10 scores are 0.0
**Cause:** Sparse vectors are empty (no word matches in corpus)
**Fix:** Check that the word vocabulary matches the trained model. Verify tokenization is consistent.

**Problem:** Eval scores lower than expected
**Cause:** Wrong IDF weighting or tokenization mismatch
**Fix:** Ensure IDF formula matches Qdrant's `Modifier.IDF`. Check tokenization produces same tokens at train and eval time.

---

## Key References

- [miniCOIL article (Qdrant)](https://qdrant.tech/articles/minicoil/)
- [GitHub - qdrant/miniCOIL](https://github.com/qdrant/miniCOIL)
- [FastEmbed integration (v0.7.0+)](https://qdrant.tech/documentation/fastembed/fastembed-minicoil/)
- [HuggingFace model (Qdrant/minicoil-v1)](https://huggingface.co/Qdrant/minicoil-v1)
- [BEIR benchmark](https://github.com/beir-cellar/beir)

See `resources/architecture.md` for detailed architecture diagrams and data flow.
