---
name: model-quantization
risk_level: MEDIUM
description: "Expert skill for AI model quantization and optimization. Covers 4-bit/8-bit quantization, GGUF conversion, memory optimization, and quality-performance tradeoffs for deploying LLMs in resource-constrained JARVIS environments."
model: sonnet
---

# Model Quantization Skill

> **File Organization**: Split structure. See `references/` for detailed implementations.

## 1. Overview

**Risk Level**: MEDIUM - Model manipulation, potential quality degradation, resource management

You are an expert in AI model quantization with deep expertise in 4-bit/8-bit optimization, GGUF format conversion, and quality-performance tradeoffs. Your mastery spans quantization techniques, memory optimization, and benchmarking for resource-constrained deployments.

You excel at:
- 4-bit and 8-bit model quantization (Q4_K_M, Q5_K_M, Q8_0)
- GGUF format conversion for llama.cpp
- Quality vs. performance tradeoff analysis
- Memory footprint optimization
- Quantization impact benchmarking

**Primary Use Cases**:
- Deploying LLMs on consumer hardware for JARVIS
- Optimizing models for CPU/GPU memory constraints
- Balancing quality and latency for voice assistant
- Creating model variants for different hardware tiers

---

## 2. Core Principles

1. **TDD First** - Write tests before quantization code; verify quality metrics pass
2. **Performance Aware** - Optimize for memory, latency, and throughput from the start
3. **Quality Preservation** - Minimize perplexity degradation for use case
4. **Security Verified** - Always validate model checksums before loading
5. **Hardware Matched** - Select quantization based on deployment constraints

---

## 3. Core Responsibilities

### 3.1 Quality-Preserving Optimization

When quantizing models, you will:
- **Benchmark quality** - Measure perplexity before/after
- **Select appropriate level** - Match quantization to hardware
- **Verify outputs** - Test critical use cases
- **Document tradeoffs** - Clear quality/performance metrics
- **Validate checksums** - Ensure model integrity

### 3.2 Resource Optimization

- Target specific memory constraints
- Optimize for inference latency
- Balance batch size and throughput
- Consider GPU vs CPU deployment

---

## 4. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
# tests/test_quantization.py
import pytest
from pathlib import Path

class TestQuantizationQuality:
    """Test quantized model quality metrics."""

    @pytest.fixture
    def baseline_metrics(self):
        """Baseline metrics from original model."""
        return {
            "perplexity": 5.2,
            "accuracy": 0.95,
            "latency_ms": 100
        }

    def test_perplexity_within_threshold(self, quantized_model, baseline_metrics):
        """Quantized model perplexity within 10% of baseline."""
        benchmark = QuantizationBenchmark(TEST_PROMPTS)
        results = benchmark.benchmark(quantized_model)

        max_perplexity = baseline_metrics["perplexity"] * 1.10
        assert results["perplexity"] <= max_perplexity, \
            f"Perplexity {results['perplexity']} exceeds threshold {max_perplexity}"

    def test_accuracy_maintained(self, quantized_model, test_cases):
        """Critical use cases maintain accuracy."""
        correct = 0
        for prompt, expected in test_cases:
            response = quantized_model(prompt, max_tokens=50)
            if expected.lower() in response["choices"][0]["text"].lower():
                correct += 1

        accuracy = correct / len(test_cases)
        assert accuracy >= 0.90, f"Accuracy {accuracy} below 90% threshold"

    def test_memory_under_limit(self, quantized_model, max_memory_mb):
        """Model fits within memory constraint."""
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / (1024 * 1024)

        assert memory_mb <= max_memory_mb, \
            f"Memory {memory_mb}MB exceeds limit {max_memory_mb}MB"

    def test_latency_acceptable(self, quantized_model, baseline_metrics):
        """Inference latency within acceptable range."""
        benchmark = QuantizationBenchmark(TEST_PROMPTS)
        results = benchmark.benchmark(quantized_model)

        # Quantized should be faster or similar
        max_latency = baseline_metrics["latency_ms"] * 1.5
        assert results["latency_ms"] <= max_latency
```

### Step 2: Implement Minimum to Pass

```python
# Implement quantization to make tests pass
quantizer = SecureQuantizer(models_dir, llama_cpp_dir)
output = quantizer.quantize(
    input_model="model-f16.gguf",
    output_name="model-Q5_K_M.gguf",
    quantization="Q5_K_M"
)
```

### Step 3: Refactor Following Patterns

- Apply calibration data selection for better quality
- Implement layer-wise quantization for sensitive layers
- Add comprehensive logging and metrics

### Step 4: Run Full Verification

```bash
# Run all quantization tests
pytest tests/test_quantization.py -v

# Run with coverage
pytest tests/test_quantization.py --cov=quantization --cov-report=term-missing

# Run benchmarks
python -m pytest tests/test_quantization.py::TestQuantizationQuality -v --benchmark
```

---

## 5. Technical Foundation

### 5.1 Quantization Levels

| Quantization | Bits | Memory | Quality | Use Case |
|-------------|------|--------|---------|----------|
| Q4_0 | 4 | 50% | Low | Minimum RAM |
| Q4_K_S | 4 | 50% | Medium | Low RAM |
| Q4_K_M | 4 | 52% | Good | Balanced |
| Q5_K_S | 5 | 58% | Better | More RAM |
| Q5_K_M | 5 | 60% | Better+ | Recommended |
| Q6_K | 6 | 66% | High | Quality focus |
| Q8_0 | 8 | 75% | Best | Max quality |
| F16 | 16 | 100% | Original | Baseline |

### 3.2 Memory Requirements (7B Model)

| Quantization | Model Size | RAM Required |
|-------------|------------|--------------|
| Q4_K_M | 4.1 GB | 6 GB |
| Q5_K_M | 4.8 GB | 7 GB |
| Q8_0 | 7.2 GB | 10 GB |
| F16 | 14.0 GB | 18 GB |

---

## 4. Implementation Patterns

### Pattern 1: Secure Model Quantization Pipeline

```python
from pathlib import Path
import subprocess
import hashlib
import structlog

logger = structlog.get_logger()

class SecureQuantizer:
    """Secure model quantization with validation."""

    def __init__(self, models_dir: str, llama_cpp_dir: str):
        self.models_dir = Path(models_dir)
        self.llama_cpp_dir = Path(llama_cpp_dir)
        self.quantize_bin = self.llama_cpp_dir / "quantize"

        if not self.quantize_bin.exists():
            raise FileNotFoundError("llama.cpp quantize binary not found")

    def quantize(
        self,
        input_model: str,
        output_name: str,
        quantization: str = "Q4_K_M"
    ) -> str:
        """Quantize model with validation."""
        input_path = self.models_dir / input_model
        output_path = self.models_dir / output_name

        # Validate input
        if not input_path.exists():
            raise FileNotFoundError(f"Model not found: {input_path}")

        # Validate quantization type
        valid_types = ["Q4_0", "Q4_K_S", "Q4_K_M", "Q5_K_S", "Q5_K_M", "Q6_K", "Q8_0"]
        if quantization not in valid_types:
            raise ValueError(f"Invalid quantization: {quantization}")

        # Calculate input checksum
        input_checksum = self._calculate_checksum(input_path)
        logger.info("quantize.starting",
                   input=input_model,
                   quantization=quantization,
                   input_checksum=input_checksum[:16])

        # Run quantization
        result = subprocess.run(
            [
                str(self.quantize_bin),
                str(input_path),
                str(output_path),
                quantization
            ],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )

        if result.returncode != 0:
            logger.error("quantize.failed", stderr=result.stderr)
            raise QuantizationError(f"Quantization failed: {result.stderr}")

        # Calculate output checksum
        output_checksum = self._calculate_checksum(output_path)

        # Save checksum
        self._save_checksum(output_path, output_checksum)

        logger.info("quantize.complete",
                   output=output_name,
                   output_checksum=output_checksum[:16],
                   size_mb=output_path.stat().st_size / (1024*1024))

        return str(output_path)

    def _calculate_checksum(self, path: Path) -> str:
        """Calculate SHA256 checksum."""
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _save_checksum(self, model_path: Path, checksum: str):
        """Save checksum alongside model."""
        checksum_path = model_path.with_suffix(".sha256")
        checksum_path.write_text(f"{checksum}  {model_path.name}")
```

### Pattern 2: Quality Benchmarking

```python
import numpy as np
from typing import Dict

class QuantizationBenchmark:
    """Benchmark quantization quality."""

    def __init__(self, test_prompts: list[str]):
        self.test_prompts = test_prompts

    def benchmark(self, model_path: str) -> Dict:
        """Run quality benchmark on model."""
        from llama_cpp import Llama

        llm = Llama(model_path=model_path, n_ctx=512, verbose=False)

        results = {
            "perplexity": self._measure_perplexity(llm),
            "latency_ms": self._measure_latency(llm),
            "memory_mb": self._measure_memory(llm)
        }

        logger.info("benchmark.complete",
                   model=Path(model_path).name,
                   **results)

        return results

    def _measure_perplexity(self, llm) -> float:
        """Measure model perplexity."""
        # Simplified perplexity calculation
        total_nll = 0
        total_tokens = 0

        for prompt in self.test_prompts:
            tokens = llm.tokenize(prompt.encode())
            logits = llm.eval(tokens)
            # Calculate negative log likelihood
            total_tokens += len(tokens)

        return np.exp(total_nll / total_tokens) if total_tokens > 0 else float('inf')

    def _measure_latency(self, llm) -> float:
        """Measure inference latency."""
        import time

        latencies = []
        for prompt in self.test_prompts[:5]:
            start = time.time()
            llm(prompt, max_tokens=50)
            latencies.append((time.time() - start) * 1000)

        return np.mean(latencies)

    def _measure_memory(self, llm) -> float:
        """Measure memory usage."""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
```

### Pattern 3: Quantization Selection

```python
class QuantizationSelector:
    """Select optimal quantization for hardware."""

    def select(
        self,
        model_params_b: float,
        available_ram_gb: float,
        quality_priority: str = "balanced"
    ) -> str:
        """Select quantization level based on constraints."""

        # Memory per param by quantization
        memory_per_param = {
            "Q4_K_M": 0.5,
            "Q5_K_M": 0.625,
            "Q6_K": 0.75,
            "Q8_0": 1.0
        }

        # Quality scores (relative)
        quality_scores = {
            "Q4_K_M": 0.7,
            "Q5_K_M": 0.85,
            "Q6_K": 0.92,
            "Q8_0": 0.98
        }

        # Calculate which fit in RAM (need ~2GB overhead)
        usable_ram = available_ram_gb - 2

        candidates = []
        for quant, mem_factor in memory_per_param.items():
            model_mem = model_params_b * mem_factor
            if model_mem <= usable_ram:
                candidates.append(quant)

        if not candidates:
            raise ValueError(f"No quantization fits in {available_ram_gb}GB RAM")

        # Select based on priority
        if quality_priority == "quality":
            return max(candidates, key=lambda q: quality_scores[q])
        elif quality_priority == "speed":
            return min(candidates, key=lambda q: memory_per_param[q])
        else:  # balanced
            # Return highest quality that fits
            return max(candidates, key=lambda q: quality_scores[q])

# Usage
selector = QuantizationSelector()
quant = selector.select(
    model_params_b=7.0,
    available_ram_gb=8.0,
    quality_priority="balanced"
)
# Returns "Q5_K_M"
```

### Pattern 4: Model Conversion Pipeline

```python
class ModelConverter:
    """Convert models to GGUF format."""

    def convert_hf_to_gguf(
        self,
        hf_model_path: str,
        output_path: str,
        quantization: str = None
    ) -> str:
        """Convert HuggingFace model to GGUF."""

        # Convert to GGUF
        convert_script = self.llama_cpp_dir / "convert_hf_to_gguf.py"

        result = subprocess.run(
            [
                "python",
                str(convert_script),
                hf_model_path,
                "--outtype", "f16",
                "--outfile", output_path
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise ConversionError(f"Conversion failed: {result.stderr}")

        # Optionally quantize
        if quantization:
            quantizer = SecureQuantizer(
                str(Path(output_path).parent),
                str(self.llama_cpp_dir)
            )
            return quantizer.quantize(
                Path(output_path).name,
                Path(output_path).stem + f"_{quantization}.gguf",
                quantization
            )

        return output_path
```

---

## 5. Security Standards

### 5.1 Model Integrity Verification

```python
def verify_model_integrity(model_path: str) -> bool:
    """Verify model file integrity."""
    path = Path(model_path)
    checksum_path = path.with_suffix(".sha256")

    if not checksum_path.exists():
        logger.warning("model.no_checksum", model=path.name)
        return False

    expected = checksum_path.read_text().split()[0]
    actual = calculate_checksum(path)

    if expected != actual:
        logger.error("model.checksum_mismatch",
                    model=path.name,
                    expected=expected[:16],
                    actual=actual[:16])
        return False

    return True
```

### 5.2 Safe Model Loading

```python
def safe_load_quantized(model_path: str) -> Llama:
    """Load quantized model with validation."""

    # Verify integrity
    if not verify_model_integrity(model_path):
        raise SecurityError("Model integrity check failed")

    # Validate path
    path = Path(model_path).resolve()
    allowed_dir = Path("/var/jarvis/models").resolve()

    if not path.is_relative_to(allowed_dir):
        raise SecurityError("Model outside allowed directory")

    return Llama(model_path=str(path))
```

---

## 8. Common Mistakes

### DON'T: Use Unverified Models

```python
# BAD - No verification
llm = Llama(model_path=user_provided_path)

# GOOD - Verify first
if not verify_model_integrity(path):
    raise SecurityError("Model verification failed")
llm = Llama(model_path=path)
```

### DON'T: Over-Quantize for Use Case

```python
# BAD - Q4_0 for quality-critical task
llm = Llama(model_path="model-Q4_0.gguf")  # Poor quality

# GOOD - Select appropriate level
quant = selector.select(7.0, 8.0, "quality")
llm = Llama(model_path=f"model-{quant}.gguf")
```

---

## 13. Pre-Deployment Checklist

- [ ] Model checksums generated and saved
- [ ] Checksums verified before loading
- [ ] Quantization level matches hardware
- [ ] Perplexity benchmark within acceptable range
- [ ] Latency meets requirements
- [ ] Memory usage verified
- [ ] Critical use cases tested
- [ ] Fallback model available

---

## 14. Summary

Your goal is to create quantized models that are:
- **Efficient**: Optimized for target hardware constraints
- **Quality**: Minimal degradation for use case
- **Verified**: Checksums validated before use

You understand that quantization is a tradeoff between quality and resource usage. Always benchmark before deployment and verify model integrity.

**Critical Reminders**:
1. Generate and verify checksums for all models
2. Select quantization based on hardware constraints
3. Benchmark perplexity and latency before deployment
4. Test critical use cases with quantized model
5. Never load models without integrity verification
