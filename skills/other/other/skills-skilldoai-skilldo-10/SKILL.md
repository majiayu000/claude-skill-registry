---
name: transformers
description: python library
version: 5.2.0
ecosystem: python
license: Apache 2.0 License"
generated_with: claude-sonnet-4-5-20250929
---

## Imports

```python
import transformers
from transformers import AutoTokenizer, pipeline
from transformers.utils.metrics import attach_tracer, traced
```

## Core Patterns

### Create inference pipelines (text + image) ✅ Current
```python
from transformers import pipeline

def main() -> None:
    text_gen = pipeline(task="text-generation", model="openai-community/gpt2")
    out = text_gen("The secret to baking a really good cake is ", max_new_tokens=40)
    print(out[0]["generated_text"])

    img_cls = pipeline(task="image-classification", model="facebook/dinov2-small-imagenet1k-1-layer")
    preds = img_cls("https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png")
    print(preds[:2])

if __name__ == "__main__":
    main()
```
* Prefer `transformers.pipeline(task=..., model=...)` for quick inference; it handles preprocessing/postprocessing and downloads/caches weights.

### Chat-style prompting with `text-generation` pipeline ✅ Current
```python
import torch
from transformers import pipeline

def main() -> None:
    chat = [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Give me 3 ideas for a weekend trip from Paris."},
    ]

    pipe = pipeline(
        task="text-generation",
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        dtype=torch.bfloat16,
        device_map="auto",
    )

    response = pipe(chat, max_new_tokens=200)
    # Many chat-capable pipelines return a list of messages in generated_text
    print(response[0]["generated_text"][-1]["content"])

if __name__ == "__main__":
    main()
```
* For chat/instruct models with proper chat templates, pass a list of `{role, content}` messages (not just a single string).
* Use `dtype=` and `device_map="auto"` to control memory/placement for larger models.
* Note: Not all models have chat templates; verify the model supports chat format before using this pattern.

### Load, modify, and save a tokenizer ✅ Current
```python
import tempfile
import shutil
from transformers import AutoTokenizer

def main() -> None:
    tmp_dir = tempfile.mkdtemp()
    try:
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

        # Add a special token and ensure it tokenizes as a single token
        special = "[SPECIAL_TOKEN_1]"
        tokenizer.add_tokens([special], special_tokens=True)
        assert tokenizer.tokenize(special) == [special]

        # Add extra special tokens without replacing existing ones
        extra = "[SPECIAL_TOKEN_2]"
        tokenizer.add_special_tokens({"extra_special_tokens": [extra]}, replace_extra_special_tokens=False)
        assert tokenizer.tokenize(extra) == [extra]

        # Save and reload round-trip
        tokenizer.save_pretrained(tmp_dir)
        reloaded = tokenizer.__class__.from_pretrained(tmp_dir)

        text = "He is very happy, UNwanté,dunning"
        assert tokenizer.encode(text, add_special_tokens=False) == reloaded.encode(text, add_special_tokens=False)
        assert tokenizer.get_vocab() == reloaded.get_vocab()

        # Common conventions
        assert reloaded.model_input_names[0] in ["input_ids", "input_values"]

        print("Tokenizer round-trip OK:", tmp_dir)
    finally:
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    main()
```
* `AutoTokenizer.from_pretrained()` loads a tokenizer from a model id or local directory.
* `save_pretrained()` + `from_pretrained()` should preserve vocab and tokenization behavior.

### Batch tokenize and decode with `__call__` and `BatchEncoding` ✅ Current
```python
from transformers import AutoTokenizer

def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    sequences = ["Hello world!", "Transformers tokenizers batch encode."]
    encoding = tokenizer(sequences, padding=True)

    # BatchEncoding behaves like a dict; `.data` exposes the underlying mapping
    data = encoding.data
    input_ids = data["input_ids"]

    decoded = [tokenizer.decode(ids, skip_special_tokens=True) for ids in input_ids]
    for src, dst in zip(sequences, decoded):
        print("SRC:", src)
        print("DEC:", dst)
        print("---")

if __name__ == "__main__":
    main()
```
* Use `tokenizer(texts, padding=True, truncation=True, return_tensors=...)` for batch preprocessing.
* Decode with `skip_special_tokens=True` for human-readable text.

### Instrument methods/functions with `attach_tracer` and `traced` ✅ Current
```python
from __future__ import annotations

from transformers.utils.metrics import attach_tracer, traced

@attach_tracer()
class ExampleClass:
    def __init__(self, name: str) -> None:
        self.name = name

    @traced
    def process_data(self, data: str) -> str:
        return f"Processed {data} with {self.name}"

    @traced(span_name="custom_operation")
    def special_operation(self, value: int) -> int:
        return value * 2

    @traced(
        additional_attributes=[
            ("name", "object.name", lambda x: x.upper()),
            ("name", "object.fixed_value", "static_value"),
        ]
    )
    def operation_with_attributes(self) -> str:
        return "Operation completed"

@traced
def standalone_function(arg1: int, arg2: int) -> int:
    return arg1 + arg2

def main() -> None:
    ex = ExampleClass("test_object")
    print(ex.process_data("sample"))
    print(ex.special_operation(42))
    print(ex.operation_with_attributes())
    print(standalone_function(1, 2))

if __name__ == "__main__":
    main()
```
* `@attach_tracer()` is a class decorator that ensures instances have `self.tracer`.
* `@traced` works on methods and standalone functions; supports `span_name=` and `additional_attributes=`.

### Register custom quantization methods ✅ Current
```python
from typing import Any
import torch
from transformers import AutoModelForCausalLM
from transformers.quantizers import HfQuantizer, register_quantization_config, register_quantizer
from transformers.utils.quantization_config import QuantizationConfigMixin

@register_quantization_config("custom")
class CustomConfig(QuantizationConfigMixin):
    def __init__(self) -> None:
        self.quant_method = "custom"
        self.bits = 8
    
    def to_dict(self) -> dict[str, Any]:
        return {"num_bits": self.bits}

@register_quantizer("custom")
class CustomQuantizer(HfQuantizer):
    def __init__(self, quantization_config, **kwargs) -> None:
        super().__init__(quantization_config, **kwargs)
        self.quantization_config = quantization_config
    
    def _process_model_before_weight_loading(self, model, **kwargs) -> bool:
        return True
    
    def _process_model_after_weight_loading(self, model, **kwargs) -> bool:
        return True
    
    def is_serializable(self) -> bool:
        return True
    
    def is_trainable(self) -> bool:
        return False

def main() -> None:
    model_8bit = AutoModelForCausalLM.from_pretrained(
        "facebook/opt-350m",
        quantization_config=CustomConfig(),
        dtype="auto"
    )
    print("Model loaded with custom quantization")

if __name__ == "__main__":
    main()
```
* Use `@register_quantization_config` to register a custom quantization configuration class.
* Use `@register_quantizer` to register the corresponding quantizer implementation.
* Extend `QuantizationConfigMixin` and `HfQuantizer` for full integration with the transformers quantization system.

## Configuration

- Installation (match backend/framework):
  - `pip install "transformers[torch]"` (PyTorch required per README: Python 3.10+, PyTorch 2.4+).
  - For JAX: `pip install "transformers[jax]"`
  - For TensorFlow: `pip install "transformers[tf]"`
- Model caching:
  - Models/tokenizers downloaded by `pipeline()` / `from_pretrained()` are cached and reused across runs (location depends on Hugging Face cache configuration).
- Device and precision for large models:
  - Prefer explicit compute configuration for pipelines: `dtype=torch.bfloat16` (or `torch.float16`) and `device_map="auto"`.
- Tokenizer behavior knobs (commonly passed to `from_pretrained()`):
  - Examples: `do_lower_case=True` (model-dependent), plus tokenizer-specific kwargs; they are persisted in `tokenizer.init_kwargs`.
- Special tokens:
  - Add tokens: `tokenizer.add_tokens([...], special_tokens=True)`
  - Add extra specials: `tokenizer.add_special_tokens({"extra_special_tokens": [...]}, replace_extra_special_tokens=False)`
  - Note: `additional_special_tokens` is deprecated in v5 and converted to `extra_special_tokens` (prefer `extra_special_tokens` for new code).

## Pitfalls

### Wrong: Shadowing the `pipeline` factory with a Pipeline instance
```python
from transformers import pipeline

pipeline = pipeline(task="text-generation", model="openai-community/gpt2")
# Now `pipeline(...)` is no longer the factory function; it's a Pipeline object.
pipeline = pipeline(task="image-classification", model="facebook/dinov2-small-imagenet1k-1-layer")
```

### Right: Use distinct variable names for pipeline instances
```python
from transformers import pipeline

text_gen = pipeline(task="text-generation", model="openai-community/gpt2")
img_cls = pipeline(task="image-classification", model="facebook/dinov2-small-imagenet1k-1-layer")
```

### Wrong: Treating a chat/instruct model as a plain string prompt
```python
from transformers import pipeline

pipe = pipeline(task="text-generation", model="meta-llama/Meta-Llama-3-8B-Instruct")
out = pipe("Hey, can you tell me any fun things to do in New York?")
print(out)
```

### Right: Provide chat history as a list of `{role, content}` messages
```python
import torch
from transformers import pipeline

chat = [
    {"role": "system", "content": "You are a sassy, wise-cracking robot as imagined by Hollywood circa 1986."},
    {"role": "user", "content": "Hey, can you tell me any fun things to do in New York?"},
]

pipe = pipeline(
    task="text-generation",
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    dtype=torch.bfloat16,
    device_map="auto",
)
response = pipe(chat, max_new_tokens=256)
print(response[0]["generated_text"][-1]["content"])
```

### Wrong: Calling a multimodal pipeline without required named inputs
```python
from transformers import pipeline

vqa = pipeline(task="visual-question-answering", model="Salesforce/blip-vqa-base")
# Missing `image=`; this cannot build inputs for VQA.
print(vqa("What is in the image?"))
```

### Right: Pass the task-specific named parameters
```python
from transformers import pipeline

vqa = pipeline(task="visual-question-answering", model="Salesforce/blip-vqa-base")
image_url = "https://huggingface.co/datasets/huggingface/documentation-images/"
image_url += "resolve/main/transformers/tasks/idefics-few-shot.jpg"
print(
    vqa(
        image=image_url,
        question="What is in the image?",
    )
)
```

### Wrong: Adding a special token without marking it as special
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokenizer.add_tokens(["[SPECIAL_TOKEN_1]"])  # not marked special
print(tokenizer.tokenize("[SPECIAL_TOKEN_1]"))
```

### Right: Mark special tokens (so tokenization/handling is consistent)
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokenizer.add_tokens(["[SPECIAL_TOKEN_1]"], special_tokens=True)
assert tokenizer.tokenize("[SPECIAL_TOKEN_1]") == ["[SPECIAL_TOKEN_1]"]
```

### Wrong: Using `PretrainedConfig` (lowercase)
```python
from transformers import PretrainedConfig  # Deprecated naming

config = PretrainedConfig()
```

### Right: Use `PreTrainedConfig` (PascalCase)
```python
from transformers import PreTrainedConfig

config = PreTrainedConfig()
```

### Wrong: Using old Python/PyTorch versions
```python
# Python 3.9 or PyTorch 2.3
# Transformers 5.2.0 will not work properly
```

### Right: Ensure minimum version requirements
```python
# Python 3.10+ and PyTorch 2.4+
# Verify before installing:
# python --version  # Should be 3.10 or higher
# pip install "transformers[torch]>=5.2.0"
```

## References

- Official Documentation: <https://huggingface.co/docs/transformers>
- GitHub Repository: <https://github.com/huggingface/transformers>
- Parrots image dataset: <https://huggingface.co/datasets/Narsil/image_dummy/raw/main/parrots.png>

## Migration from v4.x to v5.2.0

### Breaking Changes

1. **Minimum Python version**: Python 3.10+ is now required (previously 3.9+).
   - **Action**: Upgrade your Python environment to 3.10 or higher before upgrading transformers.

2. **Minimum PyTorch version**: PyTorch 2.4+ is now required (previously 2.3+).
   - **Action**: Upgrade PyTorch: `pip install "torch>=2.4"`

3. **Special tokens parameter naming**: `additional_special_tokens` is deprecated in favor of `extra_special_tokens`.
   - **Action**: Replace `{"additional_special_tokens": [...]}` with `{"extra_special_tokens": [...]}` when calling `tokenizer.add_special_tokens(...)`.

### Migration Steps

1. **Update environment**:
   ```bash
   # Ensure Python 3.10+
   python --version
   
   # Upgrade PyTorch
   pip install "torch>=2.4"
   
   # Upgrade transformers
   pip install "transformers[torch]>=5.2.0"
   ```

2. **Update tokenizer special tokens**:
   ```python
   # Old (deprecated in v5)
   tokenizer.add_special_tokens({"additional_special_tokens": ["[SPECIAL]"]})
   
   # New (v5+)
   tokenizer.add_special_tokens({"extra_special_tokens": ["[SPECIAL]"]})
   ```

3. **Update config class naming**:
   ```python
   # Old (deprecated)
   from transformers import PretrainedConfig
   
   # New
   from transformers import PreTrainedConfig
   ```

## API Reference

### Core Pipeline APIs

- **transformers.pipeline(task, model, \*\*kwargs)** - Create a task-specific `Pipeline`; key kwargs include `dtype=`, `device_map=`, `revision=`, `torch_dtype=`, `trust_remote_code=`.
- **transformers.Pipeline(\_\_call\_\_)** - Run inference on a single input or batch; returns task-specific structured outputs.
- **transformers.TextGenerationPipeline** - Pipeline for text generation tasks.

### Tokenizer APIs

- **transformers.AutoTokenizer.from_pretrained(pretrained_model_name_or_path, \*\*kwargs)** - Load tokenizer from Hub id or local directory; accepts tokenizer-specific kwargs.
- **transformers.PreTrainedTokenizer** - Base class for Python-based tokenizers.
- **transformers.PreTrainedTokenizerFast** - Fast tokenizer implementation using Rust backend.
- **transformers.PreTrainedTokenizerBase** - Abstract base class for all tokenizers; provides common interface.
- **PreTrainedTokenizerBase.save_pretrained(save_directory)** - Save tokenizer files/config to a directory for later reuse.
- **PreTrainedTokenizerBase.\_\_call\_\_(texts, padding=False, truncation=False, return_tensors=None, \*\*kwargs)** - Batch tokenize; returns a `BatchEncoding`.
- **PreTrainedTokenizerBase.encode(text, add_special_tokens=True, \*\*kwargs)** - Encode text to token ids.
- **PreTrainedTokenizerBase.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=True, \*\*kwargs)** - Decode token ids to text.
- **PreTrainedTokenizerBase.tokenize(text, \*\*kwargs)** - Convert text to token strings.
- **PreTrainedTokenizerBase.get_vocab()** - Return vocabulary mapping token string → id.
- **PreTrainedTokenizerBase.add_tokens(new_tokens, special_tokens=False)** - Add tokens to tokenizer; use `special_tokens=True` for special tokens.
- **PreTrainedTokenizerBase.add_special_tokens(special_tokens_dict, replace_extra_special_tokens=True)** - Add special tokens; supports `extra_special_tokens`.
- **PreTrainedTokenizerBase.model_input_names** - List of primary model input field names (often starts with `input_ids` or `input_values`).
- **transformers.BatchEncoding** - Output of tokenizer encode methods; dict-like with `.data` attribute.
- **transformers.BatchEncoding.data** - Underlying dict-like mapping of encoded fields (e.g., `input_ids`, `attention_mask`).
- **transformers.AddedToken** - Class representing an added token with specific behavior (single_word, lstrip, rstrip, etc.).

### Model Loading APIs

- **transformers.AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path, \*\*kwargs)** - Load causal language model; supports `config=`, `cache_dir=`, `quantization_config=`, `device_map=`, `dtype=`.
- **transformers.PreTrainedConfig** - Base class for all model configurations.
- **transformers.PretrainedConfig** ⚠️ Deprecated - Legacy alias for `PreTrainedConfig`; use `PreTrainedConfig` instead.

### Training APIs

- **transformers.TrainingArguments** - Configuration for training with Trainer.
- **transformers.Seq2SeqTrainingArguments** - Training arguments specialized for sequence-to-sequence models.
- **transformers.TrainerCallback** - Base class for Trainer callbacks.
- **transformers.EarlyStoppingCallback** - Callback for early stopping during training.

### Generation APIs

- **transformers.GenerationConfig** - Configuration for text generation.
- **transformers.GenerationMixin** - Mixin providing generation methods (generate, sample, etc.).
- **transformers.TextStreamer** - Stream generated tokens to stdout in real-time.
- **transformers.TextIteratorStreamer** - Iterator-based streamer for token-by-token generation.

### Data Handling APIs

- **transformers.DataCollatorWithPadding** - Collate examples with dynamic padding.
- **transformers.DataCollatorForLanguageModeling** - Collate for masked/causal language modeling.
- **transformers.DataCollatorForSeq2Seq** - Collate for sequence-to-sequence tasks.

### Quantization APIs

- **transformers.BitsAndBytesConfig** - Configuration for 8-bit/4-bit quantization using bitsandbytes.
- **transformers.GPTQConfig** - Configuration for GPTQ quantization.
- **transformers.AwqConfig** - Configuration for AWQ quantization.
- **transformers.quantizers.HfQuantizer** - Base class for custom quantizers.
- **transformers.quantizers.register_quantizer(quantization_method)** - Decorator to register custom quantizers.
- **transformers.quantizers.register_quantization_config(quantization_method)** - Decorator to register custom quantization configs.
- **transformers.utils.quantization_config.QuantizationConfigMixin** - Base class for quantization configuration classes.

### Multimodal APIs

- **transformers.ProcessorMixin** - Base class for multimodal processors.
- **transformers.FeatureExtractionMixin** - Base class for feature extractors.
- **transformers.ImageProcessingMixin** - Base class for image processors.

### Cache APIs

- **transformers.Cache** - Base class for KV cache implementations.
- **transformers.DynamicCache** - Dynamic KV cache that grows as needed.
- **transformers.StaticCache** - Pre-allocated static KV cache for fixed sizes.

### Utility APIs

- **transformers.HfArgumentParser** - Argument parser for dataclasses.
- **transformers.set_seed(seed)** - Set random seed for reproducibility.
- **transformers.logging.get_logger(name)** - Get a logger for transformers modules.
- **transformers.is_torch_available()** - Check if PyTorch is available.
- **transformers.is_tokenizers_available()** - Check if fast tokenizers backend is available.
- **transformers.is_vision_available()** - Check if vision dependencies are available.
- **transformers.convert_slow_tokenizer(slow_tokenizer)** - Convert a slow tokenizer to fast tokenizer.

### Metrics & Tracing APIs

- **transformers.utils.metrics.attach_tracer()** - Class decorator that attaches a tracer to instances (`self.tracer`).
- **transformers.utils.metrics.traced(span_name=None, additional_attributes=None)** - Decorator for methods/functions to create tracing spans; supports custom span names and attributes.
