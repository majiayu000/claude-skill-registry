---
name: tokenizer-design
description: BPE, WordPiece, SentencePiece, and Unigram tokenizer training, vocabulary optimization, domain extension, and multilingual design.
---

# Tokenizer Design

## When to Use

Design or modify tokenizers when training a model from scratch, adapting a model to a new domain/language with poor tokenization coverage, or optimizing inference efficiency via vocabulary tuning.

## Algorithm Selection

### Decision Table: Tokenizer Algorithm

| Algorithm | Library | Strengths | Weaknesses | Best For |
|-----------|---------|-----------|------------|----------|
| BPE | tokenizers, tiktoken | Deterministic, widely adopted | Greedy merges can miss global optima | GPT-family, general LLMs |
| WordPiece | tokenizers | Likelihood-driven merges | Slower training than BPE | BERT-family models |
| Unigram | SentencePiece | Probabilistic, multiple segmentations | More complex implementation | Multilingual, T5/XLNet |
| SentencePiece (BPE) | sentencepiece | Language-agnostic, raw text input | Less control over pre-tokenization | Multilingual, non-space languages |
| Byte-level BPE | tokenizers | No UNK tokens, full coverage | Longer sequences for non-Latin scripts | GPT-2/3/4, Llama |

### Decision Table: Vocabulary Size

| Vocab Size | Token Fertility | Training Cost | Best For |
|------------|----------------|---------------|----------|
| 8K-16K | High (more tokens/word) | Low | Small models, single language |
| 32K | Balanced | Medium | General monolingual (BERT, GPT-2) |
| 50K-64K | Lower | Medium-High | Large monolingual LLMs |
| 100K-128K | Low | High | Multilingual models |
| 200K+ | Very low | Very high | Massive multilingual (Gemma) |

## Training BPE from Scratch

### Using HuggingFace tokenizers Library

```python
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders, processors

def train_bpe_tokenizer(
    files: list[str],
    vocab_size: int = 32000,
    min_frequency: int = 2,
    output_path: str = "tokenizer.json",
):
    """Train a byte-level BPE tokenizer from scratch."""
    tokenizer = Tokenizer(models.BPE())

    # Byte-level pre-tokenization (GPT-2 style)
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder = decoders.ByteLevel()
    tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        min_frequency=min_frequency,
        special_tokens=["<|endoftext|>", "<|pad|>", "<|begin|>", "<|end|>"],
        show_progress=True,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
    )

    tokenizer.train(files, trainer)
    tokenizer.save(output_path)
    return tokenizer


# Usage
tokenizer = train_bpe_tokenizer(
    files=["corpus_part1.txt", "corpus_part2.txt"],
    vocab_size=32000,
)

# Verify
encoded = tokenizer.encode("Hello, world\! This is a test.")
print(f"Tokens: {encoded.tokens}")
print(f"IDs: {encoded.ids}")
print(f"Decoded: {tokenizer.decode(encoded.ids)}")
```

### SentencePiece Training

```python
import sentencepiece as spm


def train_sentencepiece(
    input_file: str,
    model_prefix: str = "sp_model",
    vocab_size: int = 32000,
    model_type: str = "unigram",  # or "bpe"
    character_coverage: float = 0.9995,
):
    """Train a SentencePiece model.

    character_coverage: 1.0 for Latin-heavy, 0.9995 for multilingual.
    """
    spm.SentencePieceTrainer.train(
        input=input_file,
        model_prefix=model_prefix,
        vocab_size=vocab_size,
        model_type=model_type,
        character_coverage=character_coverage,
        pad_id=0,
        unk_id=1,
        bos_id=2,
        eos_id=3,
        # Byte fallback for unknown characters
        byte_fallback=True,
        # Normalization
        normalization_rule_name="identity",  # or "nfkc"
        # Training efficiency
        input_sentence_size=5_000_000,
        shuffle_input_sentence=True,
        # Rare word handling
        max_sentencepiece_length=16,
        split_digits=True,
        allow_whitespace_only_pieces=True,
    )

    sp = spm.SentencePieceProcessor(model_file=f"{model_prefix}.model")
    return sp


# Usage
sp = train_sentencepiece("corpus.txt", vocab_size=32000, model_type="unigram")
print(sp.encode("Hello world", out_type=str))   # ['_Hello', '_world']
print(sp.encode("Hello world", out_type=int))   # [1234, 5678]
```

## Extending an Existing Tokenizer

### Adding Domain-Specific Tokens

```python
from transformers import AutoTokenizer


def extend_tokenizer(
    base_model: str,
    new_tokens: list[str],
    output_dir: str = "extended_tokenizer",
):
    """Extend a pretrained tokenizer with domain-specific tokens.

    Returns the tokenizer and number of tokens added (for model resize).
    """
    tokenizer = AutoTokenizer.from_pretrained(base_model)

    # Check fertility before adding
    for token in new_tokens[:5]:
        encoded = tokenizer.tokenize(token)
        print(f"  '{token}' -> {encoded} ({len(encoded)} tokens)")

    num_added = tokenizer.add_tokens(new_tokens)
    print(f"Added {num_added} tokens. New vocab size: {len(tokenizer)}")

    tokenizer.save_pretrained(output_dir)
    return tokenizer, num_added

```

## Fertility Analysis

### Measuring Tokenizer Efficiency

```python
from collections import Counter
import numpy as np


def fertility_analysis(tokenizer, texts: list[str]):
    """Analyze tokenizer fertility (tokens per word) on a corpus.

    Lower fertility = more efficient tokenization.
    """
    total_tokens = 0
    total_words = 0
    token_lengths = []
    unk_count = 0
    token_freq = Counter()

    unk_token_id = getattr(tokenizer, "unk_token_id", None)

    for text in texts:
        words = text.split()
        total_words += len(words)

        encoded = tokenizer.encode(text)
        total_tokens += len(encoded)
        token_lengths.append(len(encoded))

        if unk_token_id is not None:
            unk_count += encoded.count(unk_token_id)

        tokens = tokenizer.convert_ids_to_tokens(encoded)
        token_freq.update(tokens)

    fertility = total_tokens / max(total_words, 1)
    unk_rate = unk_count / max(total_tokens, 1)
    unused_vocab = len(tokenizer) - len(token_freq)

    print(f"Fertility (tokens/word): {fertility:.2f}")
    print(f"UNK rate: {unk_rate:.4%}")
    print(f"Avg sequence length: {np.mean(token_lengths):.1f}")
    print(f"Unused vocab tokens: {unused_vocab} / {len(tokenizer)}")
    print(f"Top 20 tokens: {token_freq.most_common(20)}")

    return {
        "fertility": fertility,
        "unk_rate": unk_rate,
        "avg_seq_len": np.mean(token_lengths),
        "unused_vocab": unused_vocab,
    }

```

## Gotchas and Anti-Patterns

### Vocab Size vs. Performance Tradeoffs
Larger vocab reduces sequence length (lower fertility) but increases embedding table size and softmax computation. For a 100K vocab model, the embedding matrix alone is ~400MB at float32. Diminishing returns above 64K for monolingual English. Profile actual downstream task performance, not just fertility.

### Special Token Handling
Special tokens must be consistent between tokenizer and model config. Common failure: adding `<tool_call>` to the tokenizer but forgetting to update `model.config.special_tokens_map`. Also: never place special tokens in positions that the model's positional encoding doesn't cover. Always verify with `tokenizer.all_special_tokens` after modification.

### Tokenizer-Model Mismatch
Using a tokenizer trained on a different corpus than the model causes silent performance degradation. The model's embedding layer learned representations for the original tokenizer's vocabulary distribution. Swapping tokenizers without retraining embeddings is almost always wrong. When extending, fine-tune the model on domain data after resizing embeddings.

### Byte Fallback Behavior
SentencePiece byte_fallback=True encodes unknown characters as byte sequences (e.g., `<0xE2><0x80><0x99>` for a curly quote). This eliminates UNK tokens but inflates sequence length for out-of-distribution scripts. A CJK-heavy input through a Latin-trained tokenizer with byte fallback can produce 3-4x longer sequences than a properly trained multilingual tokenizer.

### Pre-tokenization Leakage
Pre-tokenization rules (whitespace splitting, punctuation handling) bake in language assumptions. English-centric pre-tokenizers break on CJK (no spaces), agglutinative languages (Turkish, Finnish), or code (meaningful whitespace). SentencePiece avoids this by operating on raw text, but loses control over word boundary behavior.

### Normalization Side Effects
NFKC normalization (SentencePiece default) maps visually similar characters to canonical forms. This silently converts characters in code (full-width plus to `+`), math symbols, and CJK variants. Use `identity` normalization for code-heavy or multilingual corpora where character preservation matters.

### Training Data Bias in Vocabulary
The tokenizer's merge rules reflect training corpus frequency distribution. A tokenizer trained on English Wikipedia produces poor subwords for medical text, legal documents, or code. Domain-specific tokenizer training or targeted vocabulary extension is necessary when fertility spikes above 2.5x the baseline on domain text.
