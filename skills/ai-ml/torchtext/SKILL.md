---
name: torchtext
description: Natural Language Processing utilities for PyTorch (Legacy). Includes tokenizers, vocabulary building, and DataPipe-based dataset handling for text processing pipelines. (torchtext, tokenizer, vocab, datapipe, regextokenizer, nlp-pipeline)
---

## Overview

TorchText is a legacy library for NLP in PyTorch. While it is in a maintenance phase, it remains a common tool for handling classic NLP datasets and building vocabularies via DataPipes.

## When to Use

Use TorchText for maintaining legacy NLP projects or when utilizing its built-in DataPipe-based datasets. For new projects, transitioning to native PyTorch or other modern NLP libraries is recommended.

## Decision Tree

1. Are you starting a new NLP project?
   - CONSIDER: Using Hugging Face or native PyTorch instead of TorchText.
2. Do you need a high-performance tokenizer for production?
   - USE: `RegexTokenizer` and compile it with `torch.jit.script`.
3. Are you using DataPipes with multiple workers?
   - ENSURE: Use a proper `worker_init_fn` in the `DataLoader` to avoid data duplication.

## Workflows

1. **Building a Text Processing Pipeline**
   1. Initialize a tokenizer (e.g., `BERTTokenizer`).
   2. Construct a `Vocab` object using `build_vocab_from_iterator` from a dataset.
   3. Create a pipeline using `transforms.Sequential` containing: Tokenizer -> VocabTransform -> AddToken -> Truncate -> ToTensor.
   4. Pass raw strings through the pipeline to get padded tensors.

2. **Using Built-in NLP Datasets**
   1. Import a dataset from `torchtext.datasets` (e.g., IMDB, AG_NEWS).
   2. Initialize the `DataPipe` for the desired split ('train', 'test').
   3. Setup a `DataLoader` with `shuffle=True` and a proper `worker_init_fn`.
   4. Iterate through the `DataPipe` to get `(label, text)` pairs.

3. **Custom Regex Tokenization**
   1. Define a list of regex patterns and their replacements.
   2. Instantiate `RegexTokenizer` with the patterns.
   3. Optionally use `torch.jit.script` to compile the tokenizer for production.
   4. Apply the tokenizer to raw strings to generate tokens.

## Non-Obvious Insights

- **Maintenance Status**: Development of TorchText stopped as of April 2024 (v0.18), marking it as a legacy library.
- **Data Duplication Risk**: DataPipe-based datasets require explicit handling in the `DataLoader` (via worker initialization) to ensure that multiple workers don't serve the same data shards.
- **Inference Speed**: Many transforms like `BERTTokenizer` are reimplemented in TorchScript, allowing for high-performance inference without a full Python runtime.

## Evidence

- "Warning TorchText development is stopped and the 0.18 release (April 2024) will be the last stable release." (https://pytorch.org/text/stable/index.html)
- "RegexTokenizer: Regex tokenizer for a string sentence that applies all regex replacements... backed by the C++ RE2 engine." (https://pytorch.org/text/stable/transforms.html)

## Scripts

- `scripts/torchtext_tool.py`: Example of building a vocabulary and tokenizer pipeline.
- `scripts/torchtext_tool.js`: Node.js interface for invoking TorchText pipelines.

## Dependencies

- torchtext
- torch
- torchdata

## References

- [TorchText Reference](references/README.md)