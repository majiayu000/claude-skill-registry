---
name: class-design
description: Python class design conventions for this codebase. Apply when writing or reviewing classes including interfaces, inheritance, composition, and attribute access.
user-invocable: false
---

# Class Design Conventions

Favor composition over inheritance. Use Protocol classes for interfaces and dependency injection for shared behavior.

## Quick Reference

| Principle | Pattern |
|-----------|---------|
| Interfaces | `Protocol` classes for duck typing |
| Shared behavior | Dependency injection or mixins |
| Inheritance depth | Maximum 2 levels |
| Framework base classes | OK to inherit (`BaseModel`, `nn.Module`) |
| Concrete inheritance | Forbidden—use mixins instead |
| Static methods | Avoid—use module-level functions |
| Internal APIs | Design for extension, not restriction |
| Private attributes | Only to avoid subclass naming conflicts |
| Getters/setters | Use plain attributes instead |

---

## Protocol Classes for Interfaces

Use `Protocol` to define interfaces. This enables duck typing with static type checking.

```python
# CORRECT - Protocol defines the interface
from typing import Protocol

class Tokenizer(Protocol):
    """Interface for text tokenization."""

    def tokenize(self, text: str) -> list[str]:
        """Split text into tokens."""
        ...

    def detokenize(self, tokens: list[str]) -> str:
        """Join tokens back into text."""
        ...


class SimpleTokenizer:
    """Whitespace tokenizer implementing Tokenizer protocol."""

    def tokenize(self, text: str) -> list[str]:
        return text.split()

    def detokenize(self, tokens: list[str]) -> str:
        return " ".join(tokens)


def process_text(tokenizer: Tokenizer, text: str) -> list[str]:
    """Works with any Tokenizer implementation."""
    return tokenizer.tokenize(text.lower())


# INCORRECT - abstract base class forces explicit inheritance
from abc import ABC, abstractmethod

class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        pass

class SimpleTokenizer(Tokenizer):  # Must explicitly inherit
    ...
```

### When to Use Protocol vs ABC

| Use Case | Choice |
|----------|--------|
| Define interface for type checking | `Protocol` |
| Duck typing with static analysis | `Protocol` |
| Need `isinstance()` checks at runtime | `ABC` with `@runtime_checkable` |
| Framework requires inheritance | `ABC` |

---

## Composition via Dependency Injection

Inject dependencies rather than inheriting behavior.

```python
# CORRECT - composition via dependency injection
from dataclasses import dataclass

@dataclass
class DocumentProcessor:
    """Processes documents using injected components."""

    tokenizer: Tokenizer
    embedder: Embedder
    storage: Storage

    def process(self, doc: Document) -> ProcessedDocument:
        tokens = self.tokenizer.tokenize(doc.content)
        embedding = self.embedder.embed(tokens)
        self.storage.save(doc.id, embedding)
        return ProcessedDocument(doc.id, tokens, embedding)


# Usage - compose with specific implementations
processor = DocumentProcessor(
    tokenizer=SimpleTokenizer(),
    embedder=OpenAIEmbedder(api_key=settings.api_key),
    storage=RedisStorage(url=settings.redis_url),
)

# INCORRECT - inheriting behavior from multiple classes
class DocumentProcessor(TokenizerMixin, EmbedderMixin, StorageMixin):
    def process(self, doc: Document) -> ProcessedDocument:
        tokens = self.tokenize(doc.content)  # Where does this come from?
        ...
```

---

## Inheritance Rules

### Maximum Depth: 2 Levels

```python
# CORRECT - shallow hierarchy
class BaseHandler:
    """Base handler with common functionality."""
    ...

class FileHandler(BaseHandler):
    """Handles file operations."""
    ...


# INCORRECT - too deep (3+ levels)
class BaseHandler:
    ...

class IOHandler(BaseHandler):
    ...

class FileHandler(IOHandler):  # Third level - forbidden
    ...
```

### Framework Base Classes: Allowed

Inherit from framework base classes that provide essential functionality.

```python
# CORRECT - inheriting from framework base classes
from pydantic import BaseModel
from torch import nn

class UserConfig(BaseModel):
    """User configuration with Pydantic validation."""
    name: str
    max_retries: int = 3


class Encoder(nn.Module):
    """Neural network encoder layer."""

    def __init__(self, input_dim: int, output_dim: int) -> None:
        super().__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x: Tensor) -> Tensor:
        return self.linear(x)
```

### Concrete Class Inheritance: Forbidden

Never inherit from concrete (non-abstract, non-framework) classes. Use mixins or composition.

```python
# INCORRECT - inheriting from concrete class
class FileProcessor:
    def process(self, path: Path) -> Data:
        content = path.read_text()
        return self.parse(content)

    def parse(self, content: str) -> Data:
        ...

class JsonProcessor(FileProcessor):  # Forbidden - FileProcessor is concrete
    def parse(self, content: str) -> Data:
        return json.loads(content)


# CORRECT - use composition
class JsonParser:
    """Parses JSON content."""

    def parse(self, content: str) -> Data:
        return json.loads(content)


@dataclass
class FileProcessor:
    """Processes files using an injected parser."""

    parser: Parser

    def process(self, path: Path) -> Data:
        content = path.read_text()
        return self.parser.parse(content)


# Usage
processor = FileProcessor(parser=JsonParser())
```

---

## Mixins for Shared Behavior

Use mixins only when composition isn't practical. Mixins should:
- Be small and focused on one capability
- Not maintain state
- Use clear naming (`*Mixin` suffix)

```python
# CORRECT - focused mixin for logging
class LoggingMixin:
    """Adds structured logging to a class."""

    @property
    def logger(self) -> Logger:
        return logging.getLogger(self.__class__.__name__)

    def log_operation(self, operation: str, **context: Any) -> None:
        self.logger.info(operation, extra=context)


class DataLoader(LoggingMixin):
    """Loads data with logging support."""

    def load(self, path: Path) -> Data:
        self.log_operation("load_start", path=str(path))
        data = self._load_impl(path)
        self.log_operation("load_complete", path=str(path), size=len(data))
        return data
```

---

## Avoid Static Methods

Use module-level functions instead of `@staticmethod`.

```python
# INCORRECT - static method
class MathUtils:
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(value, max_val))


# CORRECT - module-level function
def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value to the range [min_val, max_val]."""
    return max(min_val, min(value, max_val))
```

**Why avoid static methods?**
- They don't use class or instance state
- Module functions are simpler and more Pythonic
- Easier to import and test

---

## Plain Attributes Over Getters/Setters

Use plain attributes. Add `@property` only when you need computed values or validation.

```python
# CORRECT - plain attributes
@dataclass
class User:
    """User with plain attributes."""

    name: str
    email: str
    age: int


# CORRECT - property for computed value
class Rectangle:
    """Rectangle with computed area property."""

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        """Computed from width and height."""
        return self.width * self.height


# INCORRECT - unnecessary getters/setters
class User:
    def __init__(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
```

---

## Decision Flow

```
Need to define an interface?
├── Yes → Use Protocol
└── No → Need shared behavior?
    ├── Yes → Can inject as dependency?
    │   ├── Yes → Use composition (dependency injection)
    │   └── No → Use a focused Mixin
    └── No → Inheriting from framework base class?
        ├── Yes → OK (BaseModel, nn.Module, etc.)
        └── No → Is it concrete?
            ├── Yes → Forbidden - refactor to composition
            └── No → OK if depth ≤ 2 levels
```
