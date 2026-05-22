---
name: sybil
description: Use Sybil for testing code examples in documentation and docstrings. Covers pytest integration, parsers, skip directives, and namespace management.
---

# Sybil Documentation Testing

Sybil validates code examples embedded in documentation and docstrings by parsing and executing them as part of normal test runs.

**Official Documentation**: https://sybil.readthedocs.io/en/latest/

## Installation

```bash
pip install sybil[pytest]
```

## Pytest Integration

Configure in `conftest.py`. See [pytest integration docs](https://sybil.readthedocs.io/en/latest/integration.html#pytest-integration).

```python
from sybil import Sybil
from sybil.parsers.markdown.codeblock import PythonCodeBlockParser
from sybil.parsers.markdown.skip import SkipParser

pytest_collect_file = Sybil(
    parsers=[
        SkipParser(),
        PythonCodeBlockParser(),
    ],
    patterns=["*.md", "**/*.py"],
).pytest()
```

### Sybil Parameters

See [API reference](https://sybil.readthedocs.io/en/latest/api.html#sybil.Sybil).

| Parameter        | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `parsers`        | Sequence of parser callables                                    |
| `patterns`       | File glob patterns to include (e.g., `["*.md", "src/**/*.py"]`) |
| `excludes`       | File glob patterns to exclude                                   |
| `setup`          | Callable receiving namespace dict, called before each document  |
| `teardown`       | Callable receiving namespace dict, called after each document   |
| `fixtures`       | List of pytest fixture names to inject into namespace           |
| `document_types` | Map file extensions to Document classes                         |

### Document Types

See [API reference](https://sybil.readthedocs.io/en/latest/api.html#documents).

- **Default**: Parse entire file
- `PythonDocument`: Import `.py` file as module, names available in namespace
- `PythonDocStringDocument`: Parse only docstrings from `.py` files

```python
from sybil.document import PythonDocStringDocument

pytest_collect_file = Sybil(
    parsers=[...],
    patterns=["src/**/*.py"],
    document_types={".py": PythonDocStringDocument},
).pytest()
```

### Fixtures

```python
import pytest
from sybil import Sybil


@pytest.fixture
def my_fixture():
    return {"key": "value"}


pytest_collect_file = Sybil(
    parsers=[...],
    patterns=["*.md"],
    fixtures=["my_fixture"],  # Available in document namespace
).pytest()
```

### Setup/Teardown

```python
def sybil_setup(namespace):
    namespace["helper"] = lambda x: x * 2


def sybil_teardown(namespace):
    pass  # Cleanup if needed


pytest_collect_file = Sybil(
    parsers=[...],
    setup=sybil_setup,
    teardown=sybil_teardown,
).pytest()
```

## Disable pytest's Built-in Doctest

Add to `pyproject.toml` to prevent conflicts:

```toml
[tool.pytest.ini_options]
addopts = "-p no:doctest"
```

## Markdown Parsers

See [Markdown parsers docs](https://sybil.readthedocs.io/en/latest/markdown.html).

```python
from sybil.parsers.markdown.codeblock import PythonCodeBlockParser, CodeBlockParser
from sybil.parsers.markdown.skip import SkipParser
from sybil.parsers.markdown.clear import ClearNamespaceParser
```

## Skip Directives

See [skip directive docs](https://sybil.readthedocs.io/en/latest/markdown.html#skipping-examples).

**SkipParser must come before other parsers** to handle skip directives.

````markdown
<!-- skip: next -->

```python
# This example is skipped
```
````

<!-- skip: next "reason for skipping" -->

```python
# Skipped and reported as skipped test with reason
```

<!-- skip: start -->

```python
# Multiple examples
```

```python
# All skipped
```

<!-- skip: end -->

<!-- skip: next if(condition_var) -->

```python
# Conditionally skipped based on namespace variable
```

````
## Invisible Code Blocks

Setup code that doesn't render in documentation. See [invisible code blocks docs](https://sybil.readthedocs.io/en/latest/markdown.html#invisible-code-blocks).

```markdown
<!-- invisible-code-block: python
setup_var = "hidden setup"
-->
````

## Clear Namespace

Reset the document namespace for isolation. See [clear namespace docs](https://sybil.readthedocs.io/en/latest/markdown.html#clearing-the-namespace).

```markdown
<!-- clear-namespace -->
```

## Custom Evaluators

See [evaluators API](https://sybil.readthedocs.io/en/latest/api.html#evaluators).

```python
from sybil.parsers.markdown.codeblock import CodeBlockParser
from sybil.evaluators.python import PythonEvaluator

# Custom evaluator with future imports
evaluator = PythonEvaluator(future_imports=["annotations"])

parser = CodeBlockParser(language="python", evaluator=evaluator)
```

## Running Sybil Tests

Sybil tests are collected like regular pytest tests. To run only Sybil tests:

```bash
# Run tests from specific directory containing documented code
pytest src/mypackage/ -v

# Exclude regular tests, only run documentation examples
pytest docs/ -v
```

To exclude Sybil tests from regular test runs, use pytest's `--ignore` flag or configure `addopts` in `pyproject.toml`.

## Example: Complete conftest.py

```python
"""Sybil configuration for docstring testing."""

from sybil import Sybil
from sybil.document import PythonDocStringDocument
from sybil.evaluators.python import PythonEvaluator
from sybil.parsers.markdown.codeblock import CodeBlockParser
from sybil.parsers.markdown.skip import SkipParser

import mypackage


def sybil_setup(namespace):
    """Pre-populate namespace for all examples."""
    namespace["pkg"] = mypackage


def sybil_teardown(namespace):
    """Cleanup after document."""
    pass


pytest_collect_file = Sybil(
    parsers=[
        SkipParser(),
        CodeBlockParser(language="python", evaluator=PythonEvaluator()),
        CodeBlockParser(language="py", evaluator=PythonEvaluator()),
    ],
    patterns=["src/mypackage/**/*.py"],
    document_types={".py": PythonDocStringDocument},
    setup=sybil_setup,
    teardown=sybil_teardown,
    excludes=[
        "**/tests/**",
        "**/_internal/**",
    ],
).pytest()
```
