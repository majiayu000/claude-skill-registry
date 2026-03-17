---
name: Embedding Models
description: Comprehensive guide for text embedding models and usage, including popular models, selection criteria, generation, evaluation, and production optimization.
---

# Embedding Models

## Overview

Comprehensive guide for text embedding models and usage. This skill covers embedding concepts (dense vectors, semantic similarity, distance metrics), popular models (OpenAI, Sentence Transformers, Cohere, BGE), model selection criteria, embedding generation (batch processing, caching), dimensionality reduction (PCA, t-SNE), fine-tuning, evaluation metrics (precision, recall, F1), storage strategies (numpy, pickle, HDF5), production optimization, and use cases (semantic search, clustering, classification).

## Prerequisites

- Understanding of vector spaces and linear algebra
- Knowledge of machine learning fundamentals
- Familiarity with Python and NumPy
- Understanding of cosine similarity and distance metrics
- Basic knowledge of transformers and deep learning
- Familiarity with scikit-learn for evaluation

## Key Concepts

### Embedding Fundamentals

- **Dense Vectors**: Fixed-size numerical representations of text
- **Semantic Similarity**: Similar meanings have similar vectors
- **Dimensionality**: Number of dimensions in the vector space
- **Distance Metrics**: Cosine similarity, Euclidean distance, Manhattan distance

### Popular Embedding Models

- **OpenAI Embeddings**: text-embedding-3-small (1536 dims), text-embedding-3-large (3072 dims)
- **Sentence Transformers**: all-MiniLM-L6-v2 (384 dims), all-mpnet-base-v2 (768 dims)
- **Cohere Embeddings**: embed-english-v3.0 (1024 dims)
- **BGE Models**: BAAI/bge-small-en-v1.5 (384 dims), BAAI/bge-large-en-v1.5 (1024 dims)

### Model Selection Criteria

- **Use Case**: Semantic search, classification, clustering
- **Budget**: Free (open-source) vs paid (API)
- **Performance**: Speed vs accuracy tradeoff
- **Dimensionality**: Lower dimensions = faster, higher = more accurate

### Evaluation Metrics

- **Retrieval**: Precision@K, Recall@K, MRR (Mean Reciprocal Rank)
- **Classification**: Accuracy, F1, precision, recall
- **Clustering**: Silhouette score, Davies-Bouldin index

### Storage Formats

- **NumPy**: Fast loading, simple format
- **Pickle**: Python native, supports metadata
- **HDF5**: Efficient for large datasets, supports compression

## Implementation Guide

### Embedding Concepts

#### Understanding Embeddings

```python
"""
Embeddings are dense vector representations of text that capture semantic meaning.

Key Concepts:
- Dense vectors: Fixed-size numerical representations
- Semantic similarity: Similar meanings have similar vectors
- Dimensionality: Number of dimensions in the vector
- Distance metrics: Cosine similarity, Euclidean distance

Example:
"cat" -> [0.2, -0.5, 0.8, ...]  # 384-dim vector
"dog" -> [0.3, -0.4, 0.7, ...]  # 384-dim vector

The vectors for "cat" and "dog" are similar because they're both animals.
"""

class EmbeddingConcepts:
    """Understanding embedding concepts."""

    @staticmethod
    def explain_embeddings():
        """Explain embedding concepts."""
        return {
            "dense_vectors": "Fixed-size numerical representations of text",
            "semantic_similarity": "Similar meanings have similar vectors",
            "dimensionality": "Number of dimensions in the vector",
            "distance_metrics": "Cosine similarity, Euclidean distance"
        }

    @staticmethod
    def compare_distance_metrics():
        """Compare different distance metrics."""
        import numpy as np

        # Example vectors
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])

        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        cosine_sim = dot_product / (norm1 * norm2)

        # Euclidean distance
        euclidean_dist = np.linalg.norm(vec1 - vec2)

        # Manhattan distance
        manhattan_dist = np.sum(np.abs(vec1 - vec2))

        return {
            "cosine_similarity": cosine_sim,
            "euclidean_distance": euclidean_dist,
            "manhattan_distance": manhattan_dist
        }

# Usage
concepts = EmbeddingConcepts()
print(concepts.explain_embeddings())

metrics = concepts.compare_distance_metrics()
print(f"Cosine similarity: {metrics['cosine_similarity']:.3f}")
```

### Popular Models

#### OpenAI Embeddings

```python
from openai import OpenAI
import numpy as np

class OpenAIEmbeddings:
    """OpenAI embedding API."""

    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text."""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return np.array(response.data[0].embedding)

    def embed_texts(self, texts: list) -> list[np.ndarray]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [np.array(data.embedding) for data in response.data]

    def get_embedding_dimension(self) -> int:
        """Get embedding dimension."""
        sample = self.embed_text("sample")
        return len(sample)

# Usage
embeddings = OpenAIEmbeddings(api_key="your-api-key")

# Single embedding
embedding = embeddings.embed_text("Hello, world!")
print(f"Embedding shape: {embedding.shape}")

# Batch embeddings
texts = ["Hello", "World", "How are you?"]
batch_embeddings = embeddings.embed_texts(texts)
print(f"Batch embeddings: {len(batch_embeddings)} vectors")

# Get dimension
dim = embeddings.get_embedding_dimension()
print(f"Embedding dimension: {dim}")
```

#### Sentence Transformers

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SentenceTransformerEmbeddings:
    """Sentence Transformers (Hugging Face) embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text."""
        embedding = self.model.encode(text)
        return embedding

    def embed_texts(self, texts: list) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts)
        return embeddings

    def embed_documents(self, documents: list) -> np.ndarray:
        """Generate embeddings for documents."""
        embeddings = self.model.encode(documents)
        return embeddings

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute similarity between two texts."""
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)

        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        )

        return similarity

# Usage
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Single embedding
embedding = embeddings.embed_text("Hello, world!")
print(f"Embedding shape: {embedding.shape}")

# Batch embeddings
texts = ["Hello", "World", "How are you?"]
batch_embeddings = embeddings.embed_texts(texts)
print(f"Batch embeddings shape: {batch_embeddings.shape}")

# Compute similarity
similarity = embeddings.compute_similarity("cat", "dog")
print(f"Similarity between 'cat' and 'dog': {similarity:.3f}")
```

#### Cohere Embeddings

```python
import cohere
import numpy as np

class CohereEmbeddings:
    """Cohere embedding API."""

    def __init__(self, api_key: str, model: str = "embed-english-v3.0"):
        self.client = cohere.Client(api_key=api_key)
        self.model = model

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text."""
        response = self.client.embed(
            texts=[text],
            model=self.model
        )
        return np.array(response.embeddings[0])

    def embed_texts(self, texts: list) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        response = self.client.embed(
            texts=texts,
            model=self.model
        )
        return np.array(response.embeddings)

    def embed_documents(self, documents: list) -> np.ndarray:
        """Generate embeddings for documents."""
        response = self.client.embed(
            texts=documents,
            input_type="search_document",
            model=self.model
        )
        return np.array(response.embeddings)

# Usage
embeddings = CohereEmbeddings(api_key="your-api-key")

# Single embedding
embedding = embeddings.embed_text("Hello, world!")
print(f"Embedding shape: {embedding.shape}")

# Batch embeddings
texts = ["Hello", "World", "How are you?"]
batch_embeddings = embeddings.embed_texts(texts)
print(f"Batch embeddings shape: {batch_embeddings.shape}")
```

#### BGE Models

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class BGEEmbeddings:
    """BGE (BAAI General Embedding) models."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text."""
        embedding = self.model.encode(text)
        return embedding

    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for query (optimized for search)."""
        embedding = self.model.encode(query)
        return embedding

    def embed_documents(self, documents: list) -> np.ndarray:
        """Generate embeddings for documents."""
        embeddings = self.model.encode(documents)
        return embeddings

    def compute_scores(self, query: str, documents: list) -> np.ndarray:
        """Compute relevance scores for documents."""
        query_emb = self.embed_query(query)
        doc_embeddings = self.embed_documents(documents)

        # Cosine similarity
        scores = np.dot(doc_embeddings, query_emb) / (
            np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_emb)
        )

        return scores

# Usage
embeddings = BGEEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Query embedding
query = "What is capital of France?"
query_emb = embeddings.embed_query(query)

# Document embeddings
documents = [
    "Paris is capital of France.",
    "London is capital of UK.",
    "Berlin is capital of Germany."
]
doc_embeddings = embeddings.embed_documents(documents)

# Compute scores
scores = embeddings.compute_scores(query, documents)
print(f"Scores: {scores}")
```

### Model Selection Criteria

#### Model Comparison

```python
import pandas as pd

class EmbeddingModelComparison:
    """Compare different embedding models."""

    def __init__(self):
        self.models = {
            "openai_small": {
                "name": "text-embedding-3-small",
                "dimensions": 1536,
                "cost_per_1k_tokens": 0.00002,
                "speed": "fast"
            },
            "openai_large": {
                "name": "text-embedding-3-large",
                "dimensions": 3072,
                "cost_per_1k_tokens": 0.00013,
                "speed": "medium"
            },
            "sentence_transformers": {
                "name": "all-MiniLM-L6-v2",
                "dimensions": 384,
                "cost_per_1k_tokens": 0,
                "speed": "fast"
            },
            "bge_small": {
                "name": "BAAI/bge-small-en-v1.5",
                "dimensions": 384,
                "cost_per_1k_tokens": 0,
                "speed": "medium"
            },
            "bge_large": {
                "name": "BAAI/bge-large-en-v1.5",
                "dimensions": 1024,
                "cost_per_1k_tokens": 0,
                "speed": "slow"
            }
        }

    def get_model_recommendation(
        self,
        use_case: str = "general",
        budget: str = "free",
        performance_priority: str = "speed"
    ) -> str:
        """Get model recommendation based on criteria."""

        # Filter by budget
        if budget == "free":
            available_models = {
                k: v for k, v in self.models.items()
                if v["cost_per_1k_tokens"] == 0
            }
        else:
            available_models = self.models

        # Filter by use case
        if use_case == "semantic_search":
            # Prefer models optimized for search
            search_optimized = ["bge_small", "bge_large"]
            available_models = {
                k: v for k, v in available_models.items()
                if k in search_optimized
            }
        elif use_case == "classification":
            # Prefer larger models
            available_models = {
                k: v for k, v in available_models.items()
                if v["dimensions"] >= 768
            }
        elif use_case == "clustering":
            # Prefer balanced models
            available_models = {
                k: v for k, v in available_models.items()
                if 384 <= v["dimensions"] <= 768
            }

        # Sort by performance priority
        if performance_priority == "speed":
            speed_order = {"fast": 0, "medium": 1, "slow": 2}
            sorted_models = sorted(
                available_models.items(),
                key=lambda x: speed_order.get(x[1]["speed"], 3)
            )
        elif performance_priority == "accuracy":
            sorted_models = sorted(
                available_models.items(),
                key=lambda x: -x[1]["dimensions"]
            )
        else:
            sorted_models = list(available_models.items())

        return sorted_models[0][0]

    def compare_models(self, model_names: list) -> pd.DataFrame:
        """Compare models in a table."""
        comparison_data = []

        for name in model_names:
            if name in self.models:
                model_info = self.models[name]
                comparison_data.append({
                    "Model": name,
                    "Dimensions": model_info["dimensions"],
                    "Cost/1K tokens": model_info["cost_per_1k_tokens"],
                    "Speed": model_info["speed"]
                })

        return pd.DataFrame(comparison_data)

# Usage
comparator = EmbeddingModelComparison()

# Get recommendation
recommendation = comparator.get_model_recommendation(
    use_case="semantic_search",
    budget="free",
    performance_priority="speed"
)
print(f"Recommended model: {recommendation}")

# Compare models
comparison = comparator.compare_models([
    "openai_small", "sentence_transformers", "bge_small"
])
print(comparison)
```

#### Selection Decision Tree

```python
class EmbeddingModelSelector:
    """Decision tree for model selection."""

    @staticmethod
    def select_model(
        data_size: str,
        latency_requirement: str,
        accuracy_requirement: str,
        budget: str
    ) -> str:
        """Select model based on requirements."""

        # Small data, low latency, low accuracy, free budget
        if (data_size == "small" and latency_requirement == "low" and
            accuracy_requirement == "low" and budget == "free"):
            return "sentence_transformers"

        # Large data, high latency, high accuracy, paid budget
        if (data_size == "large" and latency_requirement == "high" and
            accuracy_requirement == "high" and budget == "paid"):
            return "openai_large"

        # Medium data, medium latency, medium accuracy, free budget
        if (data_size == "medium" and latency_requirement == "medium" and
            accuracy_requirement == "medium" and budget == "free"):
            return "bge_small"

        # Semantic search use case
        if latency_requirement == "low" and accuracy_requirement == "high":
            return "bge_large"

        # Default
        return "sentence_transformers"

    @staticmethod
    def get_model_config(model_name: str) -> dict:
        """Get configuration for selected model."""
        configs = {
            "sentence_transformers": {
                "model_name": "all-MiniLM-L6-v2",
                "dimensions": 384,
                "batch_size": 32,
                "normalize": True
            },
            "bge_small": {
                "model_name": "BAAI/bge-small-en-v1.5",
                "dimensions": 384,
                "batch_size": 32,
                "normalize": True,
                "query_prompt": "Represent this sentence for searching relevant passages:"
            },
            "bge_large": {
                "model_name": "BAAI/bge-large-en-v1.5",
                "dimensions": 1024,
                "batch_size": 16,
                "normalize": True,
                "query_prompt": "Represent this sentence for searching relevant passages:"
            },
            "openai_small": {
                "model_name": "text-embedding-3-small",
                "dimensions": 1536,
                "batch_size": 100,
                "normalize": False
            },
            "openai_large": {
                "model_name": "text-embedding-3-large",
                "dimensions": 3072,
                "batch_size": 100,
                "normalize": False
            }
        }

        return configs.get(model_name, configs["sentence_transformers"])

# Usage
selector = EmbeddingModelSelector()

model_name = selector.select_model(
    data_size="medium",
    latency_requirement="low",
    accuracy_requirement="medium",
    budget="free"
)

config = selector.get_model_config(model_name)
print(f"Selected model: {model_name}")
print(f"Configuration: {config}")
```

### Embedding Generation

#### Batch Processing

```python
import numpy as np
from typing import List
from tqdm import tqdm

class BatchEmbeddingGenerator:
    """Generate embeddings in batches."""

    def __init__(self, embedding_model, batch_size: int = 32):
        self.embedding_model = embedding_model
        self.batch_size = batch_size

    def generate_embeddings(
        self,
        texts: List[str],
        show_progress: bool = True
    ) -> np.ndarray:
        """Generate embeddings for texts in batches."""
        all_embeddings = []

        # Process in batches
        batches = [
            texts[i:i + self.batch_size]
            for i in range(0, len(texts), self.batch_size)
        ]

        iterator = tqdm(batches) if show_progress else batches

        for batch in iterator:
            if hasattr(self.embedding_model, 'encode'):
                embeddings = self.embedding_model.encode(batch)
            elif hasattr(self.embedding_model, 'embed_texts'):
                embeddings = self.embedding_model.embed_texts(batch)
            else:
                embeddings = [self.embedding_model.embed_text(t) for t in batch]

            all_embeddings.extend(embeddings)

        return np.array(all_embeddings)

    def generate_embeddings_async(
        self,
        texts: List[str]
    ) -> np.ndarray:
        """Generate embeddings asynchronously."""
        import asyncio

        async def process_batch(batch):
            if hasattr(self.embedding_model, 'encode'):
                return self.embedding_model.encode(batch)
            else:
                return [self.embedding_model.embed_text(t) for t in batch]

        async def process_all():
            batches = [
                texts[i:i + self.batch_size]
                for i in range(0, len(texts), self.batch_size)
            ]

            tasks = [process_batch(batch) for batch in batches]
            results = await asyncio.gather(*tasks)

            return np.concatenate(results)

        return asyncio.run(process_all())

# Usage
# Using Sentence Transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
generator = BatchEmbeddingGenerator(model, batch_size=64)

texts = ["Text 1", "Text 2", "Text 3", ...]  # Many texts

# Generate embeddings
embeddings = generator.generate_embeddings(texts)
print(f"Generated {len(embeddings)} embeddings of shape {embeddings.shape}")
```

#### Caching

```python
import numpy as np
import hashlib
import pickle
from pathlib import Path
from typing import Optional

class EmbeddingCache:
    """Cache embeddings to avoid recomputation."""

    def __init__(self, cache_dir: str = "./embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding."""
        cache_key = self._get_cache_key(text)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        return None

    def set(self, text: str, embedding: np.ndarray):
        """Cache embedding."""
        cache_key = self._get_cache_key(text)
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        with open(cache_file, 'wb') as f:
            pickle.dump(embedding, f)

    def get_or_generate(
        self,
        text: str,
        embedding_model
    ) -> np.ndarray:
        """Get cached embedding or generate new one."""
        cached = self.get(text)
        if cached is not None:
            return cached

        # Generate new embedding
        if hasattr(embedding_model, 'encode'):
            embedding = embedding_model.encode(text)
        else:
            embedding = embedding_model.embed_text(text)

        # Cache it
        self.set(text, embedding)

        return embedding

    def clear(self):
        """Clear all cache."""
        for file in self.cache_dir.glob("*.pkl"):
            file.unlink()

# Usage
cache = EmbeddingCache()

# First call - generates and caches
embedding1 = cache.get_or_generate("Hello, world!", embedding_model)

# Second call - retrieves from cache
embedding2 = cache.get_or_generate("Hello, world!", embedding_model)

print(f"Embeddings are equal: {np.allclose(embedding1, embedding2)}")
```

### Dimensionality Reduction

```python
import numpy as np
from sklearn.decomposition import PCA, TSNE
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

class DimensionalityReducer:
    """Reduce embedding dimensionality."""

    def __init__(self, method: str = "pca"):
        self.method = method
        self.reducer = None

    def fit(self, embeddings: np.ndarray, n_components: int = 2):
        """Fit dimensionality reduction."""
        if self.method == "pca":
            self.reducer = PCA(n_components=n_components)
        elif self.method == "tsne":
            self.reducer = TSNE(n_components=n_components)
        elif self.method == "mds":
            self.reducer = MDS(n_components=n_components)
        else:
            raise ValueError(f"Unknown method: {self.method}")

        self.reducer.fit(embeddings)
        return self.reducer

    def transform(self, embeddings: np.ndarray) -> np.ndarray:
        """Transform embeddings to reduced space."""
        return self.reducer.transform(embeddings)

    def fit_transform(self, embeddings: np.ndarray, n_components: int = 2) -> np.ndarray:
        """Fit and transform in one step."""
        self.fit(embeddings, n_components)
        return self.transform(embeddings)

    def visualize(self, embeddings: np.ndarray, labels: list = None):
        """Visualize reduced embeddings."""
        reduced = self.fit_transform(embeddings)

        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap='viridis', alpha=0.6)
        plt.colorbar(scatter)
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.title(f'Embedding Visualization ({self.method.upper()})')
        plt.show()

# Usage
# Generate sample embeddings
np.random.seed(42)
embeddings = np.random.randn(100, 384)  # 100 samples, 384 dimensions
labels = np.random.randint(0, 3, 100)  # 3 clusters

# PCA reduction
pca_reducer = DimensionalityReducer(method="pca")
pca_reduced = pca_reducer.fit_transform(embeddings, n_components=2)
print(f"PCA reduced shape: {pca_reduced.shape}")

# t-SNE visualization
tsne_reducer = DimensionalityReducer(method="tsne")
tsne_reducer.visualize(embeddings, labels)
```

### Fine-Tuning Embeddings

```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import torch
from typing import List

class EmbeddingFineTuner:
    """Fine-tune embedding models on custom data."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        max_length: int = 512,
        batch_size: int = 16,
        epochs: int = 3
    ):
        self.model = SentenceTransformer(model_name)
        self.max_length = max_length
        self.batch_size = batch_size
        self.epochs = epochs

    def prepare_data(
        self,
        texts: List[str],
        labels: List[int] = None
    ) -> List[InputExample]:
        """Prepare data for fine-tuning."""
        examples = []

        for i, text in enumerate(texts):
            label = labels[i] if labels else 0
            examples.append(InputExample(texts=[text], label=label))

        return examples

    def fine_tune(
        self,
        train_texts: List[str],
        train_labels: List[int],
        val_texts: List[str] = None,
        val_labels: List[int] = None
    ):
        """Fine-tune model."""
        # Prepare data
        train_examples = self.prepare_data(train_texts, train_labels)

        # Create data loader
        train_dataloader = DataLoader(
            train_examples,
            shuffle=True,
            batch_size=self.batch_size
        )

        # Define loss function
        train_loss = losses.CosineSimilarityLoss(model=self.model)

        # Fine-tune
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=self.epochs,
            warmup_steps=100,
            use_amp=True
        )

        # Save fine-tuned model
        self.model.save(f"./fine_tuned_model")

        return self.model

    def evaluate(
        self,
        texts: List[str],
        labels: List[int]
    ) -> float:
        """Evaluate fine-tuned model."""
        from sentence_transformers.evaluation import SentenceEvaluator

        evaluator = SentenceEvaluator(
            texts,
            labels
        )

        metrics = evaluator(self.model)

        return metrics

# Usage
finetuner = EmbeddingFineTuner(
    model_name="all-MiniLM-L6-v2",
    epochs=3
)

# Fine-tune data
train_texts = [
    "This is a positive sentence.",
    "This is another positive sentence.",
    "This is a negative sentence.",
    "This is another negative sentence."
]
train_labels = [1, 1, 0, 0]

# Fine-tune
fine_tuned_model = finetuner.fine_tune(train_texts, train_labels)

# Evaluate
test_texts = ["This is a test sentence.", "Another test sentence."]
test_labels = [1, 0]
metrics = finetuner.evaluate(test_texts, test_labels)
print(f"Evaluation metrics: {metrics}")
```

### Evaluation Metrics

```python
import numpy as np
from typing import List, Tuple
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)

class EmbeddingEvaluator:
    """Evaluate embedding model performance."""

    @staticmethod
    def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Compute cosine similarity between embeddings."""
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        return dot_product / (norm1 * norm2)

    @staticmethod
    def evaluate_retrieval(
        query_embeddings: np.ndarray,
        document_embeddings: np.ndarray,
        relevant_docs: List[List[int]],
        k: int = 10
    ) -> dict:
        """Evaluate retrieval performance."""
        results = {
            "precision": [],
            "recall": [],
            "f1": []
        }

        for query_idx, relevant in enumerate(relevant_docs):
            # Compute similarities
            similarities = []
            for doc_idx in range(len(document_embeddings)):
                sim = EmbeddingEvaluator.cosine_similarity(
                    query_embeddings[query_idx],
                    document_embeddings[doc_idx]
                )
                similarities.append(sim)

            # Get top-k documents
            top_k_indices = np.argsort(similarities)[-k:]

            # Calculate metrics
            retrieved_set = set(top_k_indices)
            relevant_set = set(relevant)

            true_positives = len(retrieved_set & relevant_set)
            precision = true_positives / k
            recall = true_positives / len(relevant) if relevant else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            results["precision"].append(precision)
            results["recall"].append(recall)
            results["f1"].append(f1)

        return {
            "avg_precision": np.mean(results["precision"]),
            "avg_recall": np.mean(results["recall"]),
            "avg_f1": np.mean(results["f1"])
        }

    @staticmethod
    def evaluate_clustering(
        embeddings: np.ndarray,
        true_labels: np.ndarray,
        predicted_labels: np.ndarray
    ) -> dict:
        """Evaluate clustering performance."""
        return {
            "accuracy": accuracy_score(true_labels, predicted_labels),
            "precision": precision_score(true_labels, predicted_labels, average='weighted'),
            "recall": recall_score(true_labels, predicted_labels, average='weighted'),
            "f1": f1_score(true_labels, predicted_labels, average='weighted')
        }

# Usage
evaluator = EmbeddingEvaluator()

# Generate sample data
np.random.seed(42)
query_embeddings = np.random.randn(10, 384)
document_embeddings = np.random.randn(100, 384)
relevant_docs = [
    [5, 10, 15],  # Relevant docs for query 0
    [2, 8, 12],  # Relevant docs for query 1
    # ... more queries
]

# Evaluate retrieval
retrieval_metrics = evaluator.evaluate_retrieval(
    query_embeddings,
    document_embeddings,
    relevant_docs,
    k=10
)

print(f"Retrieval metrics: {retrieval_metrics}")
```

### Storage Strategies

```python
import numpy as np
import pickle
from pathlib import Path
from typing import List
import h5py

class EmbeddingStorage:
    """Store embeddings efficiently."""

    def __init__(self, storage_type: str = "numpy"):
        self.storage_type = storage_type
        self.storage_path = Path("./embeddings")
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_numpy(self, embeddings: np.ndarray, filename: str):
        """Save embeddings as numpy file."""
        file_path = self.storage_path / f"{filename}.npy"
        np.save(file_path, embeddings)

    def load_numpy(self, filename: str) -> np.ndarray:
        """Load embeddings from numpy file."""
        file_path = self.storage_path / f"{filename}.npy"
        return np.load(file_path)

    def save_pickle(self, embeddings: np.ndarray, metadata: dict, filename: str):
        """Save embeddings with metadata as pickle."""
        file_path = self.storage_path / f"{filename}.pkl"

        data = {
            "embeddings": embeddings,
            "metadata": metadata
        }

        with open(file_path, 'wb') as f:
            pickle.dump(data, f)

    def load_pickle(self, filename: str) -> tuple:
        """Load embeddings with metadata."""
        file_path = self.storage_path / f"{filename}.pkl"

        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        return data["embeddings"], data["metadata"]

    def save_hdf5(self, embeddings: np.ndarray, texts: List[str], filename: str):
        """Save embeddings in HDF5 format."""
        file_path = self.storage_path / f"{filename}.h5"

        with h5py.File(file_path, 'w') as f:
            f.create_dataset('embeddings', data=embeddings)
            f.create_dataset('texts', data=texts)

    def load_hdf5(self, filename: str) -> tuple:
        """Load embeddings from HDF5 format."""
        file_path = self.storage_path / f"{filename}.h5"

        with h5py.File(file_path, 'r') as f:
            embeddings = f['embeddings'][:]
            texts = f['texts'][:]

        return embeddings, texts

# Usage
storage = EmbeddingStorage(storage_type="numpy")

# Generate sample embeddings
embeddings = np.random.randn(100, 384)
texts = [f"Text {i}" for i in range(100)]
metadata = {"model": "all-MiniLM-L6-v2", "dimension": 384}

# Save
storage.save_numpy(embeddings, "embeddings")
storage.save_pickle(embeddings, metadata, "embeddings_with_meta")
storage.save_hdf5(embeddings, texts, "embeddings_hdf5")

# Load
loaded_embeddings = storage.load_numpy("embeddings")
loaded_with_meta, meta = storage.load_pickle("embeddings_with_meta")
loaded_embeddings, loaded_texts = storage.load_hdf5("embeddings_hdf5")
```

### Production Optimization

```python
import numpy as np
from typing import List
from concurrent.futures import ThreadPoolExecutor
import time

class ProductionEmbeddingOptimizer:
    """Optimize embedding generation for production."""

    def __init__(self, embedding_model, max_workers: int = 4):
        self.embedding_model = embedding_model
        self.max_workers = max_workers

    def batch_generate(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> np.ndarray:
        """Generate embeddings in batches."""
        all_embeddings = []

        batches = [
            texts[i:i + batch_size]
            for i in range(0, len(texts), batch_size)
        ]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for batch in batches:
                future = executor.submit(self._process_batch, batch)
                futures.append(future)

            for future in futures:
                embeddings = future.result()
                all_embeddings.extend(embeddings)

        return np.array(all_embeddings)

    def _process_batch(self, batch: List[str]) -> np.ndarray:
        """Process a single batch."""
        if hasattr(self.embedding_model, 'encode'):
            return self.embedding_model.encode(batch)
        elif hasattr(self.embedding_model, 'embed_texts'):
            embeddings = self.embedding_model.embed_texts(batch)
            return np.array(embeddings)
        else:
            return np.array([self.embedding_model.embed_text(t) for t in batch])

    def benchmark(self, texts: List[str], num_runs: int = 5) -> dict:
        """Benchmark embedding generation."""
        results = {
            "latency_ms": [],
            "throughput_per_sec": []
        }

        for _ in range(num_runs):
            start_time = time.time()

            embeddings = self.batch_generate(texts)

            end_time = time.time()
            latency = (end_time - start_time) * 1000
            throughput = len(texts) / (end_time - start_time)

            results["latency_ms"].append(latency)
            results["throughput_per_sec"].append(throughput)

        return {
            "avg_latency_ms": np.mean(results["latency_ms"]),
            "avg_throughput_per_sec": np.mean(results["throughput_per_sec"]),
            "min_latency_ms": np.min(results["latency_ms"]),
            "max_latency_ms": np.max(results["latency_ms"])
        }

# Usage
optimizer = ProductionEmbeddingOptimizer(embedding_model, max_workers=4)

# Benchmark
texts = ["Text " + str(i) for i in range(100)]
benchmark_results = optimizer.benchmark(texts, num_runs=5)

print(f"Average latency: {benchmark_results['avg_latency_ms']:.2f}ms")
print(f"Average throughput: {benchmark_results['avg_throughput_per_sec']:.2f} texts/sec")
```

### Use Cases

#### Semantic Search

```python
import numpy as np
from typing import List, Tuple

class SemanticSearch:
    """Semantic search using embeddings."""

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.document_embeddings = None
        self.documents = None

    def index_documents(self, documents: List[str]):
        """Index documents by generating embeddings."""
        self.documents = documents
        self.document_embeddings = self.embedding_model.encode(documents)

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """Search for similar documents."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)

        # Compute similarities
        similarities = []
        for doc_embedding in self.document_embeddings:
            sim = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append(sim)

        # Get top-k
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append((self.documents[idx], similarities[idx]))

        return results

# Usage
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
search = SemanticSearch(model)

# Index documents
documents = [
    "Paris is the capital of France.",
    "London is the capital of the UK.",
    "Berlin is the capital of Germany.",
    "Madrid is the capital of Spain."
]
search.index_documents(documents)

# Search
results = search.search("capital of France", top_k=2)
for doc, score in results:
    print(f"Score: {score:.3f} | {doc}")
```

#### Clustering

```python
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

class EmbeddingClustering:
    """Cluster documents using embeddings."""

    def __init__(self, n_clusters: int = 3):
        self.n_clusters = n_clusters

    def kmeans_cluster(self, embeddings: np.ndarray) -> np.ndarray:
        """K-means clustering."""
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        return labels

    def dbscan_cluster(self, embeddings: np.ndarray) -> np.ndarray:
        """DBSCAN clustering (density-based)."""
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        labels = dbscan.fit_predict(embeddings)
        return labels

    def visualize_clusters(self, embeddings: np.ndarray, labels: np.ndarray):
        """Visualize clusters in 2D."""
        from sklearn.decomposition import PCA

        # Reduce to 2D for visualization
        pca = PCA(n_components=2)
        embeddings_2d = pca.fit_transform(embeddings)

        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(
            embeddings_2d[:, 0],
            embeddings_2d[:, 1],
            c=labels,
            cmap='viridis',
            alpha=0.6
        )
        plt.colorbar(scatter)
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.title('Document Clusters')
        plt.show()

    def evaluate_clustering(self, embeddings: np.ndarray, labels: np.ndarray) -> float:
        """Evaluate clustering quality."""
        if len(set(labels)) > 1:
            return silhouette_score(embeddings, labels)
        return 0.0

# Usage
clusterer = EmbeddingClustering(n_clusters=3)

# Generate sample embeddings
np.random.seed(42)
embeddings = np.random.randn(100, 384)

# K-means clustering
kmeans_labels = clusterer.kmeans_cluster(embeddings)
silhouette = clusterer.evaluate_clustering(embeddings, kmeans_labels)
print(f"K-means silhouette score: {silhouette:.3f}")

# Visualize
clusterer.visualize_clusters(embeddings, kmeans_labels)
```

#### Classification

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class EmbeddingClassifier:
    """Classify documents using embeddings."""

    def __init__(self):
        self.classifier = LogisticRegression(random_state=42)

    def train(
        self,
        embeddings: np.ndarray,
        labels: np.ndarray,
        test_size: float = 0.2
    ) -> dict:
        """Train classifier on embeddings."""
        X_train, X_test, y_train, y_test = train_test_split(
            embeddings, labels, test_size=test_size, random_state=42
        )

        self.classifier.fit(X_train, y_train)

        # Predict on test set
        y_pred = self.classifier.predict(X_test)

        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        return {
            "accuracy": accuracy,
            "report": report
        }

    def predict(self, embeddings: np.ndarray) -> np.ndarray:
        """Predict labels for embeddings."""
        return self.classifier.predict(embeddings)

    def predict_proba(self, embeddings: np.ndarray) -> np.ndarray:
        """Predict probabilities for embeddings."""
        return self.classifier.predict_proba(embeddings)

# Usage
classifier = EmbeddingClassifier()

# Generate sample data
np.random.seed(42)
embeddings = np.random.randn(100, 384)
labels = np.random.randint(0, 3, 100)  # 3 classes

# Train
results = classifier.train(embeddings, labels)
print(f"Accuracy: {results['accuracy']:.3f}")
print(f"Classification report:\n{results['report']}")
```

## Best Practices

### Embedding Generation

- **Use batch processing** for efficiency
- **Implement caching** to avoid recomputation
- **Normalize embeddings** for consistent similarity calculations
- **Choose appropriate batch size** based on memory constraints

### Model Selection

- **Consider use case**: Semantic search, classification, clustering
- **Evaluate tradeoffs**: Speed vs accuracy vs cost
- **Test multiple models** on your specific data
- **Monitor performance** in production

### Storage

- **Use efficient formats**: HDF5 for large datasets
- **Include metadata**: Model name, dimensions, timestamp
- **Implement versioning**: Track model changes
- **Consider compression** for storage efficiency

### Production

- **Implement retry logic** for API calls
- **Use connection pooling** for performance
- **Monitor costs** for paid APIs
- **Set appropriate timeouts** for reliability

### Evaluation

- **Use appropriate metrics**: Precision, recall, F1 for retrieval
- **Establish baselines** before optimization
- **Monitor drift** over time
- **A/B test** different models

## Related Skills

- [`06-ai-ml-production/rag-implementation`](06-ai-ml-production/rag-implementation/SKILL.md)
- [`06-ai-ml-production/vector-search`](06-ai-ml-production/vector-search/SKILL.md)
- [`04-database/vector-database`](04-database/vector-database/SKILL.md)
- [`07-document-processing/rag-chunking-metadata-strategy`](07-document-processing/rag-chunking-metadata-strategy/SKILL.md)
