---
name: Type Hints for ML Code
description: Apply appropriate type hints for ML/PyTorch code. Use when adding type annotations to ML code or addressing mypy errors.
---

# Type Hints for ML Code - Constitutional AI

## When to Apply

Automatically activate when:
- Adding type hints to ML code
- Addressing mypy type errors
- Working with PyTorch tensors, models, or optimizers
- Dealing with HuggingFace transformers types

## Project Type Checking Status

**Current mypy status:**
- **41 errors remaining** (documented in MYPY_ANALYSIS_REPORT.md)
- **Status**: Accepted as reasonable for ML research code
- **CI behavior**: `continue-on-error: true` (doesn't fail builds)

**Key insight**: Perfect type coverage is not the goal for ML code. Prioritize correctness and readability over type perfection.

## When to Use Type Hints

### ✅ Do Use Type Hints For

1. **Public API functions**
   ```python
   def load_model(model_name: str) -> tuple[AutoModelForCausalLM, AutoTokenizer]:
       """Load model and tokenizer."""
       pass
   ```

2. **Configuration dataclasses**
   ```python
   @dataclass
   class TrainingConfig:
       learning_rate: float
       batch_size: int
       num_epochs: int
   ```

3. **Clear input/output types**
   ```python
   def evaluate_text(text: str, framework: ConstitutionalFramework) -> dict[str, Any]:
       """Evaluate text against principles."""
       pass
   ```

4. **Helper functions with simple types**
   ```python
   def format_prompt(prompt: str, examples: list[str]) -> str:
       """Format prompt with examples."""
       pass
   ```

### ❌ Don't Force Type Hints For

1. **Complex tensor operations** (mypy struggles with tensor shapes)
2. **Dynamic PyTorch internals** (intentionally uses `Any`)
3. **NumPy operations** (overload resolution issues)
4. **Training loop internals** (too complex, low value)

## PyTorch Type Patterns

### Tensor Types

```python
import torch
from torch import Tensor

# ✅ Basic tensor type
def forward(inputs: Tensor) -> Tensor:
    return inputs * 2

# ✅ Optional tensor (common in ML)
def process_batch(
    inputs: Tensor,
    labels: Tensor | None = None
) -> Tensor:
    pass

# ⚠️ Avoid overly specific tensor types (mypy can't verify shapes)
# This is too specific and won't type-check well:
def bad_example(inputs: Tensor[int, 32, 768]) -> Tensor[int, 32, 10]:
    pass
```

### Model and Optimizer Types

```python
from torch.nn import Module
from torch.optim import Optimizer
from transformers import PreTrainedModel, PreTrainedTokenizer

# ✅ Use base classes for flexibility
def train_model(
    model: Module,  # or PreTrainedModel for HuggingFace
    optimizer: Optimizer,
    dataloader: DataLoader
) -> None:
    pass

# ✅ HuggingFace specific types
def generate_text(
    prompt: str,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
    max_length: int = 100
) -> str:
    pass
```

### Device Types

```python
from torch import device as Device

# ✅ Device type
def move_to_device(tensor: Tensor, device: Device | str) -> Tensor:
    return tensor.to(device)

# Common pattern:
device: str | Device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## Handling "Any" Type

### When `Any` is Acceptable

```python
from typing import Any

# ✅ For complex nested structures
def process_model_output(output: Any) -> dict[str, Any]:
    """Process model output (structure varies by model)."""
    pass

# ✅ For highly dynamic operations
def advanced_tensor_op(tensors: list[Tensor]) -> Any:
    """Complex operation with unpredictable output type."""
    pass

# ✅ For configuration dictionaries
config: dict[str, Any] = {
    'learning_rate': 0.001,
    'model_name': 'gpt2',
    'device': 'cuda',
}
```

### Prefer Specific Types When Possible

```python
# ❌ Too vague
def process_data(data: Any) -> Any:
    pass

# ✅ More specific
def process_data(data: list[dict[str, float]]) -> dict[str, Tensor]:
    pass
```

## Optional and Union Types

```python
from typing import Optional  # or use | None (Python 3.10+)

# Modern syntax (Python 3.10+)
def load_checkpoint(path: str | None = None) -> dict[str, Tensor] | None:
    if path is None:
        return None
    return torch.load(path)

# Equivalent older syntax
from typing import Optional, Union

def load_checkpoint(path: Optional[str] = None) -> Optional[dict[str, Tensor]]:
    pass
```

## Common ML Type Patterns

### Return Multiple Values

```python
# ✅ Tuple with type hints
def load_model(name: str) -> tuple[PreTrainedModel, PreTrainedTokenizer]:
    model = AutoModelForCausalLM.from_pretrained(name)
    tokenizer = AutoTokenizer.from_pretrained(name)
    return model, tokenizer

# Usage
model, tokenizer = load_model("gpt2")
```

### Dataclass for Complex Returns

```python
from dataclasses import dataclass

@dataclass
class EvaluationResult:
    any_flagged: bool
    flagged_principles: list[str]
    weighted_score: float
    details: dict[str, Any]

def evaluate_text(text: str) -> EvaluationResult:
    """Evaluate text and return structured result."""
    pass
```

### Generator Types

```python
from collections.abc import Iterator

def batch_generator(data: list[Tensor], batch_size: int) -> Iterator[Tensor]:
    """Generate batches from data."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]
```

## Known Mypy Challenges in Project

### Category 1: NumPy Overload Resolution (14 errors)

```python
# Mypy struggles with NumPy's 6+ overload variants
import numpy as np

# This may show mypy error, but it's correct at runtime
scores = np.array([1.0, 2.0, 3.0])  # mypy: "cannot infer type"
```

**Resolution**: Use `# type: ignore[misc]` or accept the error (CI allows it)

### Category 2: Optional Attribute Access (7 errors)

```python
# Mypy warns about potential None access
def process_model(model: PreTrainedModel | None):
    if model is not None:
        output = model.generate(...)  # mypy may still warn

# Resolution: Assert non-None or use type: ignore
```

### Category 3: Tensor Type Inference (8 errors)

```python
# PyTorch intentionally uses dynamic typing
loss = criterion(outputs, targets)  # mypy: "Cannot determine type"
```

**Resolution**: Accept as limitation - PyTorch is dynamically typed by design

## Type Hints Best Practices for This Project

### 1. Prioritize Public APIs

```python
# ✅ Type hints for exported functions
def setup_default_framework() -> ConstitutionalFramework:
    """Public API - should have types."""
    pass

# ⚠️ Optional for internal helpers
def _internal_helper(data):
    """Internal - types optional."""
    pass
```

### 2. Use `Any` Strategically

```python
# ✅ Good use of Any
def process_principle_config(config: dict[str, Any]) -> ConstitutionalPrinciple:
    """Config structure varies - Any is appropriate."""
    pass

# ❌ Overuse of Any
def add(a: Any, b: Any) -> Any:
    """Too vague - use specific types."""
    return a + b
```

### 3. Document Complex Types

```python
from typing import TypeAlias

# Define alias for complex type
TrainingBatch: TypeAlias = dict[str, Tensor]
EvalResults: TypeAlias = dict[str, float | bool | list[str]]

def train_step(batch: TrainingBatch) -> EvalResults:
    """Type alias makes signature readable."""
    pass
```

### 4. Handle Protocol/Abstract Types

```python
from typing import Protocol

class Evaluator(Protocol):
    """Protocol for evaluation functions."""
    def evaluate(self, text: str) -> dict[str, Any]: ...

def run_evaluation(text: str, evaluator: Evaluator) -> dict[str, Any]:
    """Accept any object matching Evaluator protocol."""
    return evaluator.evaluate(text)
```

## Mypy Configuration (from pyproject.toml)

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Not required for ML code
ignore_missing_imports = true  # Many ML libraries lack stubs
```

**Key settings:**
- `disallow_untyped_defs = false` - Types helpful but not required
- `ignore_missing_imports = true` - PyTorch, transformers lack complete type stubs

## When to Use `# type: ignore`

### Acceptable Use Cases

```python
# ✅ Known mypy limitation with NumPy
scores = np.array(data)  # type: ignore[misc]

# ✅ PyTorch dynamic typing
loss = criterion(outputs, targets)  # type: ignore[arg-type]

# ✅ Third-party library without stubs
from some_ml_lib import advanced_feature  # type: ignore
```

### Avoid Overuse

```python
# ❌ Don't ignore fixable errors
def add(a: int, b: int) -> str:
    return a + b  # type: ignore  # Fix the return type instead!

# ✅ Fix the actual issue
def add(a: int, b: int) -> int:
    return a + b
```

## Type Checking Commands

```bash
# Run mypy on all source code
mypy constitutional_ai/ --ignore-missing-imports

# Run on specific module
mypy constitutional_ai/framework.py

# Show error codes (useful for targeted ignores)
mypy constitutional_ai/ --show-error-codes

# Strict mode (educational, will fail)
mypy constitutional_ai/ --strict
```

## Summary: Type Hint Philosophy for ML Code

1. **Use type hints where they add clarity** (public APIs, config)
2. **Skip type hints where they fight the framework** (PyTorch internals)
3. **Accept mypy errors for known ML ecosystem limitations** (documented in MYPY_ANALYSIS_REPORT.md)
4. **Use `Any` strategically, not lazily** (complex structures = OK, simple functions = not OK)
5. **CI should pass with 41 known errors** (continue-on-error: true)
6. **Prioritize correctness over type perfection** (tests are the real validation)

## Quick Reference

| Type | When to Use | Example |
|------|-------------|---------|
| `str`, `int`, `float` | Primitives | `def format(text: str) -> str` |
| `list[T]`, `dict[K, V]` | Collections | `def process(data: list[str]) -> dict[str, int]` |
| `Tensor` | PyTorch tensors | `def forward(x: Tensor) -> Tensor` |
| `Module` | PyTorch models | `def train(model: Module) -> None` |
| `PreTrainedModel` | HF models | `def generate(model: PreTrainedModel) -> str` |
| `Any` | Unknown/dynamic | `def process(config: dict[str, Any]) -> Any` |
| `T \| None` | Optional | `def load(path: str \| None) -> Tensor \| None` |
| `tuple[A, B]` | Multiple returns | `def load_model() -> tuple[Module, Tokenizer]` |

**Remember**: The goal is helpful type hints, not perfect type coverage. This is research code.
