---
name: dataset-management
description: Dataset versioning with DVC, HF Datasets processing patterns, data curation workflows, quality checks, and annotation pipeline design with Label Studio and Argilla.
---

# Dataset Management

## Storage and Versioning Approach

| Approach | Best For | Version Control | Scale | Collaboration |
|----------|----------|----------------|-------|---------------|
| DVC + S3/GCS | Large datasets, ML pipelines | Git-like (content-addressed) | TB+ | Good |
| HF Datasets + Hub | Public datasets, sharing | Hub revisions | GB-TB | Best |
| Delta Lake | Data lake, Spark workflows | Time travel | PB | Enterprise |
| Git LFS | Small datasets (<1 GB) | Native git | GB | Native |
| Lakehouse (Iceberg) | Analytics + ML combined | Snapshots | PB | Enterprise |

**Decision rule**: ML project with existing git workflow -> DVC. Sharing/community -> HF Hub. Enterprise data platform -> Delta/Iceberg. Small and simple -> Git LFS.

## DVC Pipeline

### Setup

```bash
# Initialize DVC in an existing git repo
pip install dvc dvc-s3       # or dvc-gs, dvc-azure
dvc init
dvc remote add -d myremote s3://my-bucket/dvc-store

# Track a dataset
dvc add data/training.jsonl
git add data/training.jsonl.dvc data/.gitignore
git commit -m "Track training dataset v1"
dvc push
```

### DVC Pipeline Definition

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python scripts/prepare_data.py
    deps:
      - scripts/prepare_data.py
      - data/raw/
    outs:
      - data/processed/train.jsonl
      - data/processed/eval.jsonl
    params:
      - prepare.max_length
      - prepare.min_quality_score

  train:
    cmd: python scripts/train.py
    deps:
      - scripts/train.py
      - data/processed/train.jsonl
    outs:
      - models/adapter/
    params:
      - train.learning_rate
      - train.epochs
    metrics:
      - metrics/eval_results.json:
          cache: false

  evaluate:
    cmd: python scripts/evaluate.py
    deps:
      - scripts/evaluate.py
      - models/adapter/
      - data/processed/eval.jsonl
    metrics:
      - metrics/benchmark_results.json:
          cache: false
    plots:
      - metrics/confusion_matrix.csv
```


## HF Datasets Patterns

### Creating a Dataset from Scratch

```python
from datasets import Dataset, DatasetDict, Features, Value, ClassLabel

# From list of dicts
data = [
    {"text": "Great product!", "label": "positive"},
    {"text": "Terrible experience.", "label": "negative"},
]
ds = Dataset.from_dict({k: [d[k] for d in data] for k in data[0]})

# With explicit schema
features = Features({
    "text": Value("string"),
    "label": ClassLabel(names=["negative", "neutral", "positive"]),
    "metadata": {
        "source": Value("string"),
        "timestamp": Value("string"),
    },
})
ds = Dataset.from_dict(data_dict, features=features)

# Create train/test split
dataset = DatasetDict({
    "train": ds.select(range(0, int(len(ds) * 0.9))),
    "test": ds.select(range(int(len(ds) * 0.9), len(ds))),
})

# Push to Hub
dataset.push_to_hub("myorg/my-dataset", private=True)
```

### Processing Pipeline

```python
from datasets import load_dataset

ds = load_dataset("json", data_files="data/raw/*.jsonl", split="train")

# Chain transformations
processed = (
    ds
    .filter(lambda x: len(x["text"]) > 50)                          # Remove short
    .filter(lambda x: x["language"] == "en")                         # Language filter
    .map(clean_text, num_proc=8)                                     # Parallel cleaning
    .map(tokenize_and_align, batched=True, batch_size=1000)          # Batched tokenization
    .remove_columns(["raw_html", "metadata"])                        # Drop unneeded cols
    .shuffle(seed=42)
)

# Deduplicate by content hash
def add_hash(example):
    example["content_hash"] = hashlib.md5(example["text"].encode()).hexdigest()
    return example

processed = processed.map(add_hash)
unique_hashes = set()
def dedup(example):
    if example["content_hash"] in unique_hashes:
        return False
    unique_hashes.add(example["content_hash"])
    return True

processed = processed.filter(dedup)
```

**Gotcha**: `num_proc > 1` with `filter` that uses external mutable state (like `unique_hashes` above) is not safe. Dedup must run single-process or use a different approach (e.g., sort + batch dedup).

## Data Quality Checks

```python
from collections import Counter
import re

def quality_report(dataset):
    """Generate data quality report. Run before every training run."""
    report = {
        "total_examples": len(dataset),
        "empty_texts": sum(1 for x in dataset if not x["text"].strip()),
        "avg_length": sum(len(x["text"]) for x in dataset) / len(dataset),
        "length_p95": sorted(len(x["text"]) for x in dataset)[int(len(dataset) * 0.95)],
    }

    # Label distribution
    if "label" in dataset.column_names:
        labels = Counter(dataset["label"])
        report["label_distribution"] = dict(labels)
        report["label_imbalance_ratio"] = max(labels.values()) / max(min(labels.values()), 1)

    # Duplicate detection
    texts = dataset["text"]
    unique = len(set(texts))
    report["duplicates"] = len(texts) - unique
    report["duplicate_pct"] = (len(texts) - unique) / len(texts) * 100

    return report

def assert_data_quality(report, max_dup_pct=5.0, max_imbalance=10.0, min_examples=100):
    """Hard gates -- fail the pipeline if data is bad."""
    assert report["total_examples"] >= min_examples, f"Too few examples: {report['total_examples']}"
    assert report["empty_texts"] == 0, f"Found {report['empty_texts']} empty texts"
    assert report["duplicate_pct"] <= max_dup_pct, f"Duplicate rate too high: {report['duplicate_pct']:.1f}%"
    if "label_imbalance_ratio" in report:
        assert report["label_imbalance_ratio"] <= max_imbalance, \
            f"Label imbalance too high: {report['label_imbalance_ratio']:.1f}x"
```

## Annotation Pipeline

### Label Studio Setup

```python
# label_studio_config.xml -- for text classification
LABEL_CONFIG = """
<View>
  <Text name="text" value="$text"/>
  <Choices name="sentiment" toName="text" choice="single">
    <Choice value="positive"/>
    <Choice value="negative"/>
    <Choice value="neutral"/>
  </Choices>
</View>
"""

# Import tasks programmatically
from label_studio_sdk import Client

ls = Client(url="http://localhost:8080", api_key="your-key")
project = ls.start_project(title="Sentiment v2", label_config=LABEL_CONFIG)

# Import data
tasks = [{"data": {"text": example["text"]}} for example in unlabeled_data]
project.import_tasks(tasks)
```

## Gotchas and Anti-Patterns

### Data Leakage
- Always split before any processing that uses global statistics (normalization, TF-IDF)
- Check for near-duplicates across train/test, not just exact duplicates
- Time-series data: split by time, never randomly

### Train/Test Contamination
- If your eval set overlaps with a public training corpus, your benchmarks are meaningless
- Use n-gram overlap detection between your training data and standard benchmarks
- Keep a held-out "canary" test set that is never used during development

### Common Mistakes
- Shuffling before splitting grouped data (e.g., same user's reviews in both splits)
- Not versioning the preprocessing code alongside the data
- Filtering after splitting (can remove all examples of a class from test)
- Using `num_proc > 1` with stateful filter functions (race conditions)
- Not tracking dataset lineage (which raw data produced which processed version)
- Oversampling minority class in the test set (inflates metrics)
- Annotator fatigue in long labeling sessions (quality drops after ~2 hours)
