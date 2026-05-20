---
name: nlp-engineering
version: 0.1.0
description: >
  Use this skill when building NLP pipelines, implementing text classification,
  semantic search, embeddings, or summarization. Triggers on text preprocessing,
  tokenization, embeddings, vector search, named entity recognition, sentiment
  analysis, text classification, summarization, and any task requiring natural
  language processing.
category: ai-ml
tags: [nlp, embeddings, text-processing, search, classification]
recommended_skills: [prompt-engineering, llm-app-development, data-science, computer-vision]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# NLP Engineering

A practical framework for building production NLP systems. This skill covers the
full stack of natural language processing - from raw text ingestion through
tokenization, embedding, retrieval, classification, and generation - with an
emphasis on making the right architectural choices at each layer. Designed for
engineers who know Python and ML basics and need opinionated guidance on building
reliable, scalable text processing pipelines.

---

## When to use this skill

Trigger this skill when the user:

- Builds a text preprocessing or cleaning pipeline
- Generates or stores embeddings for documents or queries
- Implements semantic search or similarity-based retrieval
- Classifies text into categories (sentiment, intent, topic, etc.)
- Extracts named entities, relationships, or structured data from text
- Summarizes long documents (extractive or abstractive)
- Chunks documents for RAG (Retrieval-Augmented Generation) pipelines
- Tunes tokenization strategies (BPE, wordpiece, whitespace)

Do NOT trigger this skill for:

- Pure LLM prompt engineering or chain-of-thought with no text processing pipeline
- Speech-to-text or image captioning (separate modalities with different toolchains)

---

## Key principles

1. **Preprocessing is load-bearing** - Garbage in, garbage out. Inconsistent
   casing, stray HTML, and unicode noise degrade every downstream component.
   Invest in a reproducible cleaning pipeline before touching a model.

2. **Match the model to the task** - A 66M-parameter sentence-transformer is
   often better than GPT-4 embeddings for a narrow domain retrieval task, and
   100x cheaper. Pick the smallest model that hits your quality bar.

3. **Embed offline, search online** - Pre-compute embeddings at index time.
   Doing embedding + vector search in the request path is an avoidable latency
   sink. Only re-embed at write time (new docs) or on model upgrade.

4. **Chunk with overlap, not just length** - Fixed-length chunking without
   overlap splits sentences at boundaries and degrades retrieval recall. Always
   use a sliding window with 10-20% overlap and respect sentence boundaries.

5. **Evaluate before you ship** - Define offline metrics (precision@k, NDCG,
   ROUGE, F1) before building. An NLP system without evals is a system you
   cannot improve or regress-test.

---

## Core concepts

### Tokenization

Tokenization converts raw text into a sequence of tokens a model can process.
Modern models use subword tokenizers (BPE, WordPiece, SentencePiece) rather
than whitespace splitting, allowing them to handle out-of-vocabulary words
gracefully by decomposing them into known subword units.

Key considerations: token budget (LLMs have context windows), language coverage
(multilingual text needs a multilingual tokenizer), and domain vocabulary
(medical/legal/code text may have poor tokenization with general-purpose tokenizers).

### Embeddings

An embedding is a dense vector representation of text that encodes semantic
meaning. Similar texts produce vectors with high cosine similarity. Embeddings
are the foundation of semantic search, clustering, and classification.

Two categories: **encoding models** (sentence-transformers, E5, BGE) are fast,
cheap, and purpose-built for retrieval. **LLM embeddings** (OpenAI
`text-embedding-3`, Cohere Embed) are convenient API calls but cost money per
token and introduce external latency.

### Attention and transformers

Transformers process the full token sequence in parallel using self-attention,
letting every token attend to every other token. This gives transformer-based
models long-range context understanding that recurrent models lacked. For NLP
tasks, you almost never need to implement attention from scratch - use
HuggingFace `transformers` and fine-tune a pretrained checkpoint.

### Vector similarity

Three distance metrics dominate:

| Metric | Formula (conceptual) | Best for |
|---|---|---|
| Cosine similarity | angle between vectors | Normalized embeddings, most retrieval |
| Dot product | magnitude + angle | When vector magnitude carries information |
| Euclidean distance | straight-line distance | Rare; prefer cosine for NLP |

Most vector stores (Pinecone, Weaviate, pgvector, FAISS) default to cosine or
dot product. Normalize your embeddings before storing them to make cosine and
dot product equivalent.

---

## Common tasks

### Text preprocessing pipeline

Build a reproducible cleaning pipeline before any modeling step. Apply in this
order: decode -> strip HTML -> normalize unicode -> lowercase -> remove noise ->
normalize whitespace.

```python
import re
import unicodedata
from bs4 import BeautifulSoup

def preprocess(text: str, lowercase: bool = True) -> str:
    # 1. Decode HTML entities and strip tags
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")

    # 2. Normalize unicode (NFD -> NFC, remove combining chars if needed)
    text = unicodedata.normalize("NFC", text)

    # 3. Lowercase
    if lowercase:
        text = text.lower()

    # 4. Remove URLs, emails, special tokens
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)

    # 5. Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

# Usage
clean = preprocess("<p>Visit https://example.com for more info.</p>")
# -> "visit for more info."
```

> Persist the preprocessing config (lowercase flag, regex patterns) alongside
> your model so training and inference use identical transformations.

### Generate embeddings

Use `sentence-transformers` for local, cost-free embeddings or the OpenAI API
for convenience. Always batch your calls.

```python
# Option A: sentence-transformers (local, free, fast on GPU)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

documents = ["The quick brown fox", "Machine learning is fun", "NLP rocks"]

# encode() handles batching internally; show_progress_bar for large corpora
embeddings = model.encode(documents, normalize_embeddings=True, show_progress_bar=True)
# -> numpy array, shape (3, 384)

# Option B: OpenAI embeddings API
from openai import OpenAI

client = OpenAI()

def embed_batch(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    # Strip newlines - they degrade embedding quality per OpenAI docs
    texts = [t.replace("\n", " ") for t in texts]
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]
```

### Build semantic search

Index embeddings into a vector store and retrieve by cosine similarity at query
time. This example uses FAISS for local search and pgvector for PostgreSQL.

```python
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# --- Indexing ---
docs = ["Python is a programming language.", "The Eiffel Tower is in Paris.", ...]
doc_embeddings = model.encode(docs, normalize_embeddings=True).astype("float32")

# Inner product on normalized vectors = cosine similarity
index = faiss.IndexFlatIP(doc_embeddings.shape[1])
index.add(doc_embeddings)

# --- Retrieval ---
def search(query: str, top_k: int = 5) -> list[tuple[str, float]]:
    q_emb = model.encode([query], normalize_embeddings=True).astype("float32")
    scores, indices = index.search(q_emb, top_k)
    return [(docs[i], float(scores[0][j])) for j, i in enumerate(indices[0])]

results = search("programming languages for data science")
# -> [("Python is a programming language.", 0.87), ...]
```

> For production, use `faiss.IndexIVFFlat` (approximate, faster) or a managed
> vector store (pgvector, Pinecone, Weaviate) rather than exact `IndexFlatIP`.

### Text classification with transformers

Fine-tune a pretrained encoder for sequence classification. HuggingFace
`transformers` + `datasets` is the standard stack.

```python
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
import torch

MODEL_ID = "distilbert-base-uncased"
LABELS = ["negative", "neutral", "positive"]
id2label = {i: l for i, l in enumerate(LABELS)}
label2id = {l: i for i, l in enumerate(LABELS)}

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_ID, num_labels=len(LABELS), id2label=id2label, label2id=label2id
)

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)

# train_data: list of {"text": str, "label": int}
train_ds = Dataset.from_list(train_data).map(tokenize, batched=True)

args = TrainingArguments(
    output_dir="./sentiment-model",
    num_train_epochs=3,
    per_device_train_batch_size=32,
    evaluation_strategy="epoch",
    save_strategy="best",
    load_best_model_at_end=True,
)

trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=eval_ds)
trainer.train()
```

> Use `distilbert` or `roberta-base` for most classification tasks. Only
> escalate to larger models if the smaller ones underperform after fine-tuning.

### NER pipeline

Use spaCy for fast rule-augmented NER or a HuggingFace token classification
model for custom entity types.

```python
import spacy
from transformers import pipeline

# Option A: spaCy (fast, battle-tested for standard entities)
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> list[dict]:
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
        for ent in doc.ents
    ]

entities = extract_entities("Apple Inc. was founded by Steve Jobs in Cupertino.")
# -> [{"text": "Apple Inc.", "label": "ORG", ...}, {"text": "Steve Jobs", "label": "PERSON", ...}]

# Option B: HuggingFace token classification (custom entities, higher accuracy)
ner = pipeline(
    "token-classification",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple",  # merges B-/I- tokens into spans
)
results = ner("OpenAI released GPT-4 in San Francisco.")
```

### Extractive and abstractive summarization

Choose extractive for faithfulness (no hallucination risk) and abstractive for
fluency.

```python
# --- Extractive: rank sentences by TF-IDF centrality ---
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extractive_summary(text: str, n_sentences: int = 3) -> str:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    tfidf = TfidfVectorizer().fit_transform(sentences)
    sim_matrix = cosine_similarity(tfidf)
    scores = sim_matrix.sum(axis=1)
    top_indices = np.argsort(scores)[-n_sentences:][::-1]
    return ". ".join(sentences[i] for i in sorted(top_indices)) + "."

# --- Abstractive: seq2seq model ---
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def abstractive_summary(text: str, max_length: int = 130) -> str:
    # BART has a 1024-token context window - chunk long documents first
    result = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return result[0]["summary_text"]
```

### Chunking strategies for long documents

Chunking is critical for RAG quality. Poor chunking is the single most common
cause of poor retrieval recall.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 64,
) -> list[dict]:
    """
    Recursive splitter tries paragraph -> sentence -> word boundaries in order.
    chunk_overlap ensures context continuity across chunk boundaries.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_text(text)
    return [{"text": chunk, "chunk_index": i, "total_chunks": len(chunks)} for i, chunk in enumerate(chunks)]

# Semantic chunking (group sentences by embedding similarity instead of length)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

semantic_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",  # split where similarity drops sharply
    breakpoint_threshold_amount=95,
)
semantic_chunks = semantic_splitter.create_documents([text])
```

> Rule of thumb: chunk_size 256-512 tokens for precise retrieval, 512-1024 for
> richer context. Always store chunk metadata (source doc ID, page, position)
> alongside the embedding.

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Embedding raw HTML or markdown | Markup tokens poison the semantic space | Strip all markup in preprocessing before embedding |
| Fixed-size chunks with no overlap | Splits sentences at boundaries, breaks coherence | Use recursive splitter with 10-20% overlap |
| Re-embedding at query time if corpus is static | Unnecessary latency on every request | Pre-compute all embeddings offline; embed only on writes |
| Using Euclidean distance for text similarity | Less meaningful than cosine for high-dimensional sparse-ish vectors | Normalize embeddings and use cosine/dot product |
| Fine-tuning a large model before trying a small pretrained one | Expensive, slow, often unnecessary | Benchmark a frozen small model first; fine-tune only if quality gap exists |
| Ignoring tokenizer mismatch between training and inference | Token boundaries differ, degrading model accuracy | Use the same tokenizer class and vocab for train and serve |

---

## Gotchas

1. **Embedding model upgrades invalidate the entire index** - Switching from `BAAI/bge-small-en-v1.5` to `text-embedding-3-small` (or any other model) produces vectors in a different semantic space. Mixing embeddings from two different models in the same index causes meaningless similarity scores. When upgrading embedding models, you must re-embed and re-index every document in the corpus before the new model can be used in production.

2. **Preprocessing applied at index time must be applied identically at query time** - If you lowercase and strip HTML when building the index but forget to apply the same preprocessing to the query string, queries produce poor recall because the normalized index vectors don't match un-normalized query vectors. Encapsulate preprocessing in a shared function called by both the indexing pipeline and the query path.

3. **FAISS `IndexFlatIP` does exact search but does not scale past ~1M vectors** - For production corpora above ~500K documents, exact search latency becomes unacceptable. Use `IndexIVFFlat` (inverted file index, approximate) or a managed vector store. The tradeoff is recall (95-99% instead of 100%) for 10-100x faster search. Benchmark recall vs. latency before committing to an ANN approach.

4. **HuggingFace `pipeline()` loads the full model on every call in scripts** - Calling `pipeline("token-classification", model="...")` inside a request handler or loop re-loads the model weights from disk on every invocation, causing massive latency. Instantiate the pipeline once at module load time (or application startup) and reuse the same instance across all requests.

5. **Sentence boundary detection matters more than chunk size for retrieval quality** - Splitting text every N characters without checking for sentence boundaries creates chunks that start or end mid-sentence. These partial-sentence chunks retrieve poorly because their vectors average semantically incomplete text. Use `RecursiveCharacterTextSplitter` with sentence-aware separators (`["\n\n", "\n", ". ", " "]`) rather than a character-count-only splitter.

---

## References

For detailed comparison tables and implementation guidance on specific topics,
read the relevant file from the `references/` folder:

- `references/embedding-models.md` - comparison of OpenAI, Cohere, sentence-transformers, E5, BGE with dimensions, benchmarks, and cost

Only load a references file if the current task requires it - they are long and
will consume context.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
