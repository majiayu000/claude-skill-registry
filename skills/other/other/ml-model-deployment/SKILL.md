---
name: ml-model-deployment
description: LLM and ML model serving with vLLM, TGI, Triton, and TorchServe. Covers quantization formats (GPTQ/AWQ/GGUF), batching strategies, latency optimization, and inference framework selection.
---

# ML Model Deployment

## Inference Framework Selection

| Framework | Best For | Throughput | Latency | Ease of Setup |
|-----------|----------|------------|---------|---------------|
| vLLM | LLM serving, high throughput | Highest | Low | Easy |
| TGI (Text Gen Inference) | HF model serving, production | High | Low | Easy |
| Triton Inference Server | Multi-model, multi-framework | High | Lowest | Complex |
| TorchServe | PyTorch models, custom logic | Moderate | Moderate | Moderate |
| llama.cpp / Ollama | Edge, CPU, local dev | Low-Moderate | Variable | Easiest |

**Decision rule**: LLM serving -> vLLM. Multi-model/multi-framework -> Triton. Quick prototype -> TGI. Custom preprocessing pipeline -> TorchServe.

## vLLM Server Setup

### Basic Deployment

```python
# server.py -- OpenAI-compatible API out of the box
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    dtype="auto",
    tensor_parallel_size=2,         # Number of GPUs for tensor parallelism
    gpu_memory_utilization=0.90,    # Reserve 10% for KV cache overhead
    max_model_len=8192,
    enable_prefix_caching=True,     # Reuse KV cache for shared prefixes
    enforce_eager=False,            # Use CUDA graphs by default
)
```

```bash
# CLI launch -- production-ready with one command
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.90 \
    --max-model-len 8192 \
    --enable-prefix-caching \
    --port 8000

# Client usage (drop-in OpenAI replacement)
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "meta-llama/Llama-3.1-8B-Instruct",
         "prompt": "Hello", "max_tokens": 100}'
```

### KV Cache Sizing

```
KV cache memory per token = 2 * num_layers * num_kv_heads * head_dim * dtype_bytes
# Llama-3.1-8B (bf16): 2 * 32 * 8 * 128 * 2 = 128 KB/token
# At 8192 seq_len, 256 concurrent seqs: ~256 GB -- won't fit without quantization
```

**Gotcha**: `gpu_memory_utilization=0.95` leaves no room for KV cache growth. Start at 0.85-0.90 and tune. OOM during serving (not loading) means KV cache is too large.

## Quantization

### Format Comparison

| Format | Quality (vs FP16) | Speed Gain | GPU Required | Ecosystem |
|--------|-------------------|------------|--------------|-----------|
| GPTQ (4-bit) | 97-99% | 1.5-2x | Yes | vLLM, TGI, HF |
| AWQ (4-bit) | 97-99% | 1.5-2.5x | Yes | vLLM, TGI, HF |
| GGUF (Q4_K_M) | 95-98% | 1x (CPU) / 1.3x (GPU) | Optional | llama.cpp, Ollama |
| bitsandbytes NF4 | 95-97% | 0.8-1x | Yes | HF (training only) |
| FP8 (E4M3) | 99%+ | 1.5-2x | H100+ | vLLM, TensorRT-LLM |

**Decision rule**: GPU serving -> AWQ (best vLLM integration). CPU/edge -> GGUF. Training -> bitsandbytes NF4. H100 fleet -> FP8.

### Quantize with AutoAWQ

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "meta-llama/Llama-3.1-8B-Instruct"
quant_path = "llama-3.1-8b-instruct-awq"

model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM",        # GEMM for batch serving, GEMV for single-request
}

model.quantize(tokenizer, quant_config=quant_config)
model.save_quantized(quant_path)
tokenizer.save_pretrained(quant_path)
```

### Quantize with AutoGPTQ

```python
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

quant_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    damp_percent=0.1,
    desc_act=True,            # Activation-order quantization (better quality, slower)
)

model = AutoGPTQForCausalLM.from_pretrained(model_path, quant_config)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Calibration dataset -- 128-256 samples of representative input
examples = [tokenizer(t, return_tensors="pt") for t in calibration_texts[:128]]
model.quantize(examples)
model.save_quantized(quant_path)
```

**Gotcha**: Calibration data quality matters. Use domain-representative text, not random Wikipedia. Poor calibration -> quality collapse on your actual workload.

## Triton Inference Server

### Model Repository Structure

```
model_repository/
+-- llama_tokenizer/
|   +-- config.pbtxt
|   +-- 1/
|       +-- model.py          # Python backend for tokenization
+-- llama_model/
|   +-- config.pbtxt
|   +-- 1/
|       +-- model.plan         # TensorRT engine or ONNX model
+-- llama_ensemble/
    +-- config.pbtxt           # Chains tokenizer -> model -> detokenizer
```

### Triton Config (config.pbtxt)

```protobuf
name: "llama_model"
backend: "python"
max_batch_size: 64

input [
  { name: "input_ids"      data_type: TYPE_INT64  dims: [-1] },
  { name: "attention_mask"  data_type: TYPE_INT64  dims: [-1] }
]
output [
  { name: "logits"  data_type: TYPE_FP32  dims: [-1, -1] }
]

instance_group [
  { count: 1  kind: KIND_GPU  gpus: [0] }
]

dynamic_batching {
  preferred_batch_size: [8, 16, 32]
  max_queue_delay_microseconds: 100000
}
```

```bash
# Launch Triton
docker run --gpus all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 \
    -v $(pwd)/model_repository:/models \
    nvcr.io/nvidia/tritonserver:24.01-py3 \
    tritonserver --model-repository=/models
```

## TorchServe Handler

```python
# handler.py
import torch
from ts.torch_handler.base_handler import BaseHandler
from transformers import AutoModelForCausalLM, AutoTokenizer

class LLMHandler(BaseHandler):
    def initialize(self, context):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_dir = context.system_properties.get("model_dir")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir, torch_dtype=torch.bfloat16, device_map="auto"
        )
        self.model.eval()

    def preprocess(self, requests):
        texts = [r.get("data") or r.get("body") for r in requests]
        return self.tokenizer(texts, return_tensors="pt", padding=True).to(self.device)

    def inference(self, inputs):
        with torch.no_grad():
            return self.model.generate(**inputs, max_new_tokens=256)

    def postprocess(self, outputs):
        return [self.tokenizer.decode(o, skip_special_tokens=True) for o in outputs]
```

```bash
# Package and serve
torch-model-archiver --model-name llm --version 1.0 \
    --handler handler.py --extra-files "model_dir/" \
    --export-path model_store/

torchserve --start --model-store model_store --models llm=llm.mar
```

## Batching Strategies

| Strategy | Latency | Throughput | Implementation |
|----------|---------|------------|----------------|
| Static batching | Highest (waits for batch fill) | High | Triton `dynamic_batching` |
| Continuous batching | Lowest (no waiting) | Highest | vLLM, TGI (default) |
| Iteration-level batching | Low | High | vLLM PagedAttention |

**Continuous batching** is why vLLM/TGI outperform naive serving. New requests join mid-generation rather than waiting for the full batch to complete.

## Tensor Parallelism Gotchas

- TP degree must divide `num_attention_heads` and `num_kv_heads` evenly
- TP=2 on 2 GPUs with NVLink: good. TP=2 across PCIe: 30-50% slower than expected
- TP increases latency slightly (all-reduce overhead) but enables larger models
- For throughput-first workloads, prefer data parallelism (multiple vLLM instances) over high TP
- Pipeline parallelism (PP) is rarely worth it for serving; introduces bubbles

## Latency Optimization Checklist

- [ ] Enable CUDA graphs (`enforce_eager=False` in vLLM)
- [ ] Use prefix caching for shared system prompts
- [ ] Set `max_model_len` to actual max, not model's theoretical max (saves KV cache)
- [ ] AWQ/GPTQ quantization for 2x throughput with minimal quality loss
- [ ] Speculative decoding for latency-sensitive workloads (draft model + verify)
- [ ] Tune `gpu_memory_utilization` -- too high causes thrashing, too low wastes capacity
- [ ] Profile with `nsys` or `torch.profiler` to find actual bottleneck before optimizing
