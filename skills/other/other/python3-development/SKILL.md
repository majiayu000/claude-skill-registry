---
name: python3-development
description: 'The model must use this skill when : 1. working within any python project. 2. Python CLI applications with Typer and Rich are mentioned by the user. 2. tasked with Python script writing or editing. 3. building CI scripts or tools. 4. Creating portable Python scripts with stdlib only. 5. planning out a python package design. 6. running any python script or test. 7. writing tests (unit, integration, e2e, validation) for a python script, package, or application. Reviewing Python code against best practices or for code smells. 8. The python command fails to run or errors, or the python3 command shows errors. 9. pre-commit or linting errors occur in python files. 10. Writing or editing python code  in a git repository.\n<hint>This skill provides : 1. the users preferred workflow patterns for test-driven development, feature addition, refactoring, debugging, and code review using modern Python 3.11+ patterns (including PEP 723 inline metadata, native generics, and type-safe async processing). 2. References to favored modules. 3. Working pyproject.toml configurations. 4. Linting and formatting configuration and troubleshooting. 5. Resource files that provide solutions to known errors and linting issues. 6. Project layouts the user prefers.</hint>'
version: "1.1.0"
last_updated: "2025-11-04"
python_compatibility: "3.11+"
---

# Opinionated Python Development Skill

## Role Identification (Mandatory)

The model must identify its ROLE_TYPE and echo the following statement:

```text
My ROLE_TYPE is "<the role type>". I follow instructions given to "the model" and "<role name>".
```

Where:

- `<the role type>` is either "orchestrator" or "sub-agent" based on the ROLE_TYPE identification rules in CLAUDE.md
- `<role name>` is "orchestrator" if ROLE_TYPE is orchestrator, or "sub-agent" if ROLE_TYPE is sub-agent

**Example for orchestrator:**

```text
My ROLE_TYPE is "orchestrator". I follow instructions given to "the model" and "orchestrator".
```

**Example for sub-agent:**

```text
My ROLE_TYPE is "sub-agent". I follow instructions given to "the model" and "sub-agent".
```

---

Orchestration guide for Python development using specialized agents and modern Python 3.11-3.14 patterns.

## Skill Architecture

### Bundled Resources (Included in This Skill)

**Reference Documentation:**

- [User Project Conventions](./references/user-project-conventions.md) - Extracted conventions from user's production projects (MANDATORY for new projects)
- [Modern Python Modules](./references/modern-modules.md) - 50+ library guides with usage patterns and best practices
- [Tool & Library Registry](./references/tool-library-registry.md) - Development tools catalog for linting, testing, and build automation
- [API Reference](./references/api_reference.md) - API specifications and integration guides
- [Python Development Orchestration](./references/python-development-orchestration.md) - Detailed workflow patterns for TDD, feature addition, refactoring, and code review

**Command Templates and Guides** (`commands/`):

- Reference material for creating slash commands (NOT the actual slash commands)
- Command templates and patterns for development
- Testing and development workflow guides
- See [Commands README](./commands/README.md) for details

**Scripts and Assets:**

- Example scripts demonstrating patterns
- Configuration templates and boilerplate

### External Dependencies (Required - Not Bundled)

**Agents** (install to `~/.claude/agents/`):

- `@agent-python-cli-architect` - Python CLI development with Typer and Rich
- `@agent-python-pytest-architect` - Test suite creation and planning
- `@agent-python-code-reviewer` - Post-implementation code review
- `@agent-python-portable-script` - Standalone stdlib-only script creation
- `@agent-spec-architect` - Architecture design
- `@agent-spec-planner` - Task breakdown and planning
- `@agent-spec-analyst` - Requirements gathering

**Slash Commands** (install to `~/.claude/commands/`):

- `/modernpython` - Python 3.11+ pattern enforcement and legacy code detection
- `/shebangpython` - PEP 723 inline script metadata validation

**System Tools** (install via package manager or uv):

- `uv` - Python package and project manager (required)
- `ruff` - Linter and formatter
- `pyright` - Type checker (Microsoft)
- `mypy` - Static type checker
- `pytest` - Testing framework
- `pre-commit` - Git hook framework
- `mutmut` - Mutation testing (for critical code)
- `bandit` - Security scanner (for critical code)

**Installation Notes:**

- Agents and slash commands must be installed separately in their respective directories
- This skill provides orchestration guidance and references; agents perform actual implementation
- Use the `uv` skill for comprehensive uv documentation and package management guidance

## Core Concepts

### Python Development Standards

This skill provides orchestration patterns, modern Python 3.11+ standards, quality gates, and reference documentation for Python development.

**Commands** (external - in `~/.claude/commands/`):

- `/modernpython` - Validates Python 3.11+ patterns, identifies legacy code
- `/shebangpython` - Validates correct shebang for all Python scripts
- Note: This skill contains command templates in `commands/` directory, not the actual slash commands

**Reference Documentation**:

- Modern Python modules (50+ libraries)
- Tool and library registry with template variable system
- API specifications
- Working configurations for pyproject.toml, ruff, mypy, pytest

**Docstring Standard**: Google style (Args/Returns/Raises sections). See [User Project Conventions](./references/user-project-conventions.md) for ruff pydocstyle configuration (`convention = "google"`).

**CRITICAL: Pyproject.toml Template Variables**:

All pyproject.toml examples use explicit template variables (e.g., `{{project_name_from_directory_or_git_remote}}`) instead of generic placeholders. The model MUST replace ALL template variables with actual values before creating files. See [Tool & Library Registry sections 18-19](./references/tool-library-registry.md#18-pyprojecttoml-template-variable-reference) for:

- Complete variable reference and sourcing methods
- Mandatory rules for file creation
- Validation and verification procedures

### Script Dependency Trade-offs

Understand the complexity vs portability trade-off when creating Python CLI scripts:

**Scripts with dependencies (Typer + Rich via PEP 723)**:

- **Benefits**:
  - Less development complexity - Leverage well-tested libraries for argument parsing, formatting, validation
  - Less code to write - Typer handles CLI boilerplate, Rich handles output formatting
  - Better UX - Colors, progress bars, structured output built-in
  - Just as simple to execute - PEP 723 makes it a single-file executable; uv handles dependencies automatically
- **Trade-off**: Requires network access on first run (to fetch packages)

**stdlib-only scripts**:

- **Benefits**:
  - Maximum portability - Runs on ANY Python installation without network access
  - Best for: Air-gapped systems, restricted corporate environments, embedded systems
- **Trade-offs**:
  - More development complexity - Build everything from scratch (manual argparse, manual tree formatting, manual color codes)
  - More code to write and test - Everything must be implemented manually
  - Basic UX - Limited formatting without external libraries

**Default recommendation:** Use Typer + Rich with PEP 723 unless you have specific portability requirements that prevent network access.

**See:**

- [Python Development Orchestration Guide](./references/python-development-orchestration.md) for detailed agent selection criteria
- [Typer and Rich CLI Examples](./assets/typer_examples/index.md) for Rich width handling solutions

### Rich Panel and Table Width Handling

**Common Problem**: Rich containers (Panel, Table) wrap content at 80 characters in CI/non-TTY environments, breaking URLs, commands, and structured output.

**Two Solutions Depending on Context**:

#### Solution 1: Plain Text (No Containers)

For plain text output that shouldn't wrap:

```python
from rich.console import Console

console = Console()

# URLs, paths, commands - never wrap
console.print(long_url, crop=False, overflow="ignore")
```

#### Solution 2: Rich Containers (Panel/Table)

For Panel and Table that contain long content, `crop=False` alone doesn't work because containers calculate their own internal layout. Use `get_rendered_width()` helper with different patterns for Panel vs Table:

```python
from rich.console import Console, RenderableType
from rich.measure import Measurement
from rich.panel import Panel
from rich.table import Table

def get_rendered_width(renderable: RenderableType) -> int:
    """Get actual rendered width of Rich renderable.

    Handles color codes, Unicode, styling, padding, borders.
    Works with Panel, Table, or any Rich container.
    """
    temp_console = Console(width=9999)
    measurement = Measurement.get(temp_console, temp_console.options, renderable)
    return int(measurement.maximum)

console = Console()

# Panel: Set Console width (Panel fills Console width)
panel = Panel(long_content)
panel_width = get_rendered_width(panel)
console.width = panel_width  # Set Console width, NOT panel.width
console.print(panel, crop=False, overflow="ignore", no_wrap=True, soft_wrap=True)

# Table: Set Table width (Table controls its own width)
table = Table()
table.add_column("Type", style="cyan", no_wrap=True)
table.add_column("Value", style="green", no_wrap=True)
table.add_row("Data", long_content)
table.width = get_rendered_width(table)  # Set Table width
console.print(table, crop=False, overflow="ignore", no_wrap=True, soft_wrap=True)
```

**Executable Examples**: See [./assets/typer_examples/](./assets/typer_examples/index.md) for complete working scripts:

- `console_no_wrap_example.py` - Plain text wrapping solutions
- `console_containers_no_wrap.py` - Panel/Table width handling with `get_rendered_width()`

### Rich Emoji Usage

**Instruction**: In Rich console output, always use Rich emoji tokens instead of literal Unicode emojis.

**Use Rich emoji tokens**: `:white_check_mark: :cross_mark: :magnifying_glass:`

**Why**: Cross-platform compatibility, consistent rendering, markdown-safe alignment

**Example:**

```python
from rich.console import Console

console = Console()

# Correct - Rich emoji tokens
console.print(":white_check_mark: Task completed")
console.print(":cross_mark: Task failed")
console.print(":sparkles: New feature")
console.print(":rocket: Performance improvement")
```

**Benefits**:

- Rich emoji tokens work consistently across all terminals and fonts
- Avoid markdown table alignment issues (emoji width calculation problems)
- Enable proper width measurement in `get_rendered_width()`
- Ensure cross-platform compatibility (Windows, Linux, macOS)

**See**: [Rich Emoji Documentation](https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-emoji) for complete emoji token reference.

### Python Exception Handling

Catch exceptions only when you have a specific recovery action. Let all other errors propagate to the caller.

**Reason**: Fail-fast principle surfaces issues early rather than hiding them behind generic error messages.

**Pattern**:

```python
def get_user(id):
    return db.query(User, id)  # Errors surface naturally

def get_user_with_handling(id):
    try:
        return db.query(User, id)
    except ConnectionError:
        logger.warning("DB unavailable, using cache")
        return cache.get(f"user:{id}")  # Specific recovery action
```

When adding try/except, answer: "What specific error do I expect, and what is my recovery action?"

**See**: [Exception Handling in Python CLI Applications](./references/exception-handling.md) for comprehensive patterns including Typer exception chain prevention.

### Type Safety with Mypy

**REQUIREMENT**: All Python code MUST be comprehensively typed using Python 3.11+ native type hints.

**Python Version**: Python 3.11+ is required unless explicitly documented otherwise. Older versions are rare, documented exceptions.

**The model MUST read the official mypy documentation examples before implementing type patterns. Each subsection links to authoritative mypy docs.**

#### When to Use Generics

Use generics for type-safe container classes and functions that work with multiple types.

**Applicable scenarios:**

- Custom collection classes (stacks, queues, boxes)
- Functions accepting multiple type variants
- Decorators and factory methods
- Reusable protocols and type aliases

**MUST read examples before implementing**: [Mypy Generics Documentation](./references/mypy-docs/generics.rst)

**Python 3.11 Generic Pattern** (TypeVar with Generic):

```python
from typing import TypeVar, Generic, Sequence

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

def first(seq: Sequence[T]) -> T:
    return seq[0]
```

**Python 3.12+ Generic Pattern** (Native Syntax):

```python
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

def first[T](seq: Sequence[T]) -> T:
    return seq[0]
```

**Type Variable Bounds** (restrict to subtypes):

```python
from collections.abc import Sequence
from typing import Protocol

class SupportsAbs[T](Protocol):
    def __abs__(self) -> T: ...

def max_by_abs[T: SupportsAbs[float]](*xs: T) -> T:
    return max(xs, key=abs)
```

**Value Restrictions** (limit to specific types):

```python
def concat[S: (str, bytes)](x: S, y: S) -> S:
    return x + y  # Type-safe for str OR bytes, but not mixed
```

**Generic Method Chaining** (precise return types):

```python
from typing import Self

class Shape:
    scale: float = 1.0

    def set_scale(self, scale: float) -> Self:
        self.scale = scale
        return self  # Returns precise subclass type
```

#### When to Use Protocols

Use protocols for structural subtyping when you need duck typing with type safety. Protocols check whether an object has required methods/attributes regardless of inheritance.

**Applicable scenarios:**

- Accept any object with specific capabilities without requiring inheritance
- Define interfaces for duck-typed code
- Create flexible callback types
- Ensure compatibility without tight coupling

**MUST read examples before implementing**: [Mypy Protocols Documentation](./references/mypy-docs/protocols.rst)

**Basic Protocol Pattern**:

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def close_resource(resource: SupportsClose) -> None:
    resource.close()  # Works with ANY object having close() method

# No inheritance needed - structural match
class FileHandler:
    def close(self) -> None:
        print("Closing file")

close_resource(FileHandler())  # ✅ Type-safe
```

**Read-Only Attributes** (use @property to avoid invariance issues):

```python
from typing import Protocol

class Named(Protocol):
    @property
    def name(self) -> str: ...  # Read-only via property
```

**Recursive Protocols** (tree structures):

```python
from typing import Protocol

class TreeLike(Protocol):
    value: int

    @property
    def left(self) -> TreeLike | None: ...

    @property
    def right(self) -> TreeLike | None: ...
```

**Runtime Checks**:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: object) -> None:
    if isinstance(obj, Drawable):  # Runtime check enabled
        obj.draw()
```

**WARNING**: `isinstance()` with protocols only verifies attribute existence, NOT type correctness. Use for structural validation, not precise type guarantees.

#### TypedDict for Dictionary Typing

Use TypedDict for dictionaries with fixed schemas and string keys where each key has a specific value type.

**Applicable scenarios:**

- Dictionaries representing objects with predictable structure
- JSON-like data structures
- Configuration dictionaries
- API request/response payloads

**MUST read examples before implementing**: [Mypy TypedDict Documentation](./references/mypy-docs/typed_dict.rst)

**Required Fields Pattern** (all keys required):

```python
from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int
    director: str

movie: Movie = {
    "name": "Blade Runner",
    "year": 1982,
    "director": "Ridley Scott"
}  # All keys required
```

**Optional Fields Pattern** (total=False):

```python
from typing import TypedDict

class MovieOptions(TypedDict, total=False):
    subtitles: bool
    audio_language: str

options: MovieOptions = {}  # ✅ Empty dict valid
options2: MovieOptions = {"subtitles": True}  # ✅ Partial valid
```

**Mixed Required/Optional Pattern**:

```python
from typing import TypedDict

class MovieBase(TypedDict):
    name: str  # Required
    year: int  # Required

class Movie(MovieBase, total=False):
    director: str  # Optional
    rating: float  # Optional

movie: Movie = {"name": "Alien", "year": 1979}  # ✅ Valid
```

**CRITICAL**: Always annotate variables when assigning TypedDict literals. Without annotation, mypy infers `dict[str, Any]`:

```python
# ❌ Wrong - inferred as dict[str, Any]
movie = {"name": "Alien", "year": 1979}

# ✅ Correct - explicitly typed
movie: Movie = {"name": "Alien", "year": 1979}
```

#### Type Narrowing

Use type narrowing to refine broad union types to specific types based on runtime checks.

**Applicable scenarios:**

- Handling union types (e.g., `str | int | None`)
- Optional value processing
- Validating input types
- Control flow-based type refinement

**MUST read examples before implementing**: [Mypy Type Narrowing Documentation](./references/mypy-docs/type_narrowing.rst)

**isinstance() Narrowing**:

```python
def process_value(value: str | int) -> str:
    if isinstance(value, str):
        return value.upper()  # Narrowed to str
    else:
        return str(value * 2)  # Narrowed to int
```

**None Checks**:

```python
def greet(name: str | None) -> str:
    if name is not None:
        return f"Hello, {name}"  # Narrowed to str
    return "Hello, stranger"
```

**Type Guards** (custom narrowing functions):

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(values: list[object]) -> None:
    if is_str_list(values):
        # Narrowed to list[str] in this branch
        print(" ".join(values))
```

**TypeIs (Python 3.13+, more powerful than TypeGuard)**:

```python
from typing import TypeIs

def is_str(val: object) -> TypeIs[str]:
    return isinstance(val, str)

def process(val: str | int) -> None:
    if is_str(val):
        print(val.upper())  # Narrowed to str
    else:
        print(val * 2)  # Narrowed to int (complement type)
```

**Key difference**: TypeGuard narrows only the if-branch; TypeIs narrows both branches (if-branch to the specified type, else-branch to the complement).

#### attrs vs dataclasses vs pydantic

**Decision Matrix**:

| Feature                | attrs                              | dataclasses                            | pydantic                                 |
| ---------------------- | ---------------------------------- | -------------------------------------- | ---------------------------------------- |
| **Performance**        | Fastest (compiled)                 | Fast (native)                          | Slower (validation overhead)             |
| **Validation**         | Basic (via converters/validators)  | None (requires custom `__post_init__`) | Comprehensive (built-in)                 |
| **Immutability**       | `@frozen`                          | `frozen=True`                          | `frozen=True` (v2)                       |
| **Evolution**          | Excellent (`evolve()`)             | Basic (`replace()`)                    | Good (`model_copy()`)                    |
| **Slots**              | Automatic                          | Manual (`slots=True`)                  | Automatic (v2)                           |
| **Type Coercion**      | Manual                             | None                                   | Automatic                                |
| **JSON Serialization** | Manual                             | Manual                                 | Native (`model_dump_json()`)             |
| **Use When**           | High-performance, pure Python data | Stdlib-only requirement                | External data validation (APIs, configs) |

**attrs Pattern** (high performance, pure Python):

```python
from attrs import define, field

@define
class User:
    name: str
    age: int = field(validator=lambda i, a, v: v >= 0)
    email: str | None = None
```

**MUST read examples**: [Mypy Additional Features - Attrs](./references/mypy-docs/additional_features.rst)

**dataclasses Pattern** (stdlib-only):

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class User:
    name: str
    age: int
    email: str | None = None

    def __post_init__(self) -> None:
        if self.age < 0:
            raise ValueError("Age must be non-negative")
```

**pydantic Pattern** (external data validation):

```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    name: str
    age: int = Field(ge=0)
    email: str | None = None

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Age must be non-negative')
        return v
```

**Recommendation**:

- **Default**: Use `attrs` for internal data structures (best performance, most features)
- **Stdlib-only requirement**: Use `dataclasses`
- **External data (APIs, configs, user input)**: Use `pydantic` (if already a dependency)

**NEVER add pydantic as a dependency solely for dataclasses. Use attrs or stdlib dataclasses instead.**

#### Additional Mypy Features

**MUST read before using advanced patterns**: [Mypy Additional Features](./references/mypy-docs/additional_features.rst)

**Generic Dataclasses**:

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class Box(Generic[T]):
    value: T

int_box: Box[int] = Box(value=42)
str_box: Box[str] = Box(value="hello")
```

**Self Type for Method Chaining**:

```python
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self

    def set_value(self, value: int) -> Self:
        self.value = value
        return self

# Type-safe chaining
builder = Builder().set_name("test").set_value(42)
```

#### Mypy Configuration Best Practices

**Strict Mode Configuration** (pyproject.toml):

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_reexport = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
```

**Per-Module Overrides** (for gradual typing):

```toml
[[tool.mypy.overrides]]
module = "third_party_lib.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "legacy_code.*"
disallow_untyped_defs = false
```

**See**: [Tool & Library Registry - Mypy Configuration](./references/tool-library-registry.md) for complete configuration examples.

<section ROLE_TYPE="orchestrator">

## Agent Orchestration (Orchestrator Only)

### Delegation Pattern

The orchestrator delegates Python development tasks to specialized agents rather than implementing directly.

**Reason**: Agents have focused expertise and appropriate tool access for their specific domains.

**The orchestrator follows this pattern**:

1. Read the complete orchestration guide before delegating tasks
2. Choose appropriate agents based on task requirements
3. Provide clear context: file paths, success criteria, scope boundaries
4. Chain agents for complex workflows (design → implement → test → review)
5. Validate outputs with quality gates

**The orchestrator delegates rather than implements**:

| Task Type          | Delegation Target                |
| ------------------ | -------------------------------- |
| Python code        | `@agent-python-cli-architect`    |
| Test creation      | `@agent-python-pytest-architect` |
| Code review        | `@agent-python-code-reviewer`    |
| Stdlib-only script | `@agent-python-portable-script`  |
| Architecture       | `@agent-spec-architect`          |
| Task breakdown     | `@agent-spec-planner`            |
| Requirements       | `@agent-spec-analyst`            |

**Reason for delegation table**: Clear mapping prevents orchestrator from implementing when it should coordinate.

### Required Reading

**The orchestrator must read and understand the complete agent selection guide before delegating any Python development task:**

[Python Development Orchestration Guide](./references/python-development-orchestration.md)

This guide contains:

- Agent selection criteria and decision trees
- Workflow patterns (TDD, feature addition, code review, refactoring, debugging)
- Quality gates and validation requirements
- Delegation best practices

### Quick Reference Example

```text
User: "Build a CLI tool to process CSV files"

Orchestrator workflow:
1. Read orchestration guide for agent selection
2. Delegate to @agent-python-cli-architect
   "Create CSV processing CLI with Typer+Rich progress bars"
3. Delegate to @agent-python-pytest-architect
   "Create test suite for CSV processor"
4. Instruct agent to run: /shebangpython, /modernpython
5. Delegate to @agent-python-code-reviewer
   "Review CSV processor implementation"
6. Validate: Code quality checks (linting, formatting) performed and issues addressed per the holistic-linting skill, then uv run pytest
```

</section>

## Command Usage

### /modernpython

**Purpose**: Comprehensive reference guide for Python 3.11+ patterns with official PEP citations

**When to use**:

- As reference guide when writing new code
- Learning modern Python 3.11-3.14 features and patterns
- Understanding official PEPs (585, 604, 695, etc.)
- Identifying legacy patterns to avoid
- Finding modern alternatives for old code

**Note**: This is a reference document to READ, not an automated validation tool. Use it to guide your implementation choices.

**Usage**:

```text
/modernpython
→ Loads comprehensive reference guide
→ Provides Python 3.11+ pattern examples
→ Includes PEP citations with research tool guidance (prefer MCP tools: Ref/exa over WebFetch)
→ Shows legacy patterns to avoid
→ Shows modern alternatives to use
→ Framework-specific guides (Typer, Rich, pytest)

Research tool preference for PEP documentation:
1. mcp__Ref__ref_search_documentation(query="PEP {number} Python enhancement proposal")
2. mcp__exa__get_code_context_exa(query="PEP {number} implementation examples")
3. WebFetch as fallback

> [Web resource access, definitive guide for getting accurate data for high quality results](./references/accessing_online_resources.md)
```

**With file path argument**:

```text
/modernpython src/mymodule.py
→ Loads guide for reference while working on specified file
→ Use guide to manually identify and refactor legacy patterns
```

### /shebangpython

**Purpose**: Validate correct shebang for ALL Python scripts based on their dependencies and execution context

**When to use**:

- Creating any standalone executable Python script
- Validating script shebang correctness
- Ensuring scripts have proper execution configuration

**Required for**: ALL executable Python scripts (validates shebang matches script type)

**What it validates**:

- **Stdlib-only scripts**: `#!/usr/bin/env python3` (no PEP 723 needed - nothing to declare)
- **Scripts with dependencies**: `#!/usr/bin/env -S uv --quiet run --active --script` + PEP 723 metadata declaring those dependencies
- **Package executables**: `#!/usr/bin/env python3` (dependencies via package manager)
- **Library modules**: No shebang (not directly executable)

**See**: [PEP 723 Reference](./references/PEP723.md) for details on inline script metadata

**Pattern**:

```text
/shebangpython scripts/deploy.py
→ Analyzes imports to determine dependency type
→ **Corrects shebang** to match script type (edits file if wrong)
→ **Adds PEP 723 metadata** if external dependencies detected (edits file)
→ **Removes PEP 723 metadata** if stdlib-only (edits file)
→ Sets execute bit if needed
→ Provides detailed verification report
```

<section ROLE_TYPE="orchestrator">

## Core Workflows (Orchestrator Only)

The orchestrator follows established workflow patterns for Python development tasks. See [Python Development Orchestration Guide](./references/python-development-orchestration.md) for complete details.

### Workflow Overview

1. **TDD (Test-Driven Development)**: Design → Write Tests → Implement → Review → Validate
2. **Feature Addition**: Requirements → Architecture → Plan → Implement → Test → Review
3. **Code Review**: Self-Review → Standards Check → Agent Review → Fix → Re-validate
4. **Refactoring**: Tests First → Refactor → Validate → Review
5. **Debugging**: Reproduce → Trace → Fix → Test → Review

Each workflow uses agent chaining with specific quality gates. See the orchestration guide for complete patterns, examples, and best practices.

</section>

## Linting Discovery Protocol

**The model executes this discovery sequence before any linting or formatting operations**:

**Reason**: Projects use different tool configurations. Discovery ensures compatibility with project standards and CI pipelines.

### Discovery Sequence

1. **Check for git hook tool configuration**:

   ```bash
   # Verify .pre-commit-config.yaml exists
   test -f .pre-commit-config.yaml && echo "git hook config detected"
   ```

   **If found**: Detect and run the correct git hook tool:

   ```bash
   # Detect tool (outputs 'prek' or 'pre-commit')
   uv run python -c "print(open('.git/hooks/pre-commit').readlines()[1].split()[4].rstrip(':') if __import__('pathlib').Path('.git/hooks/pre-commit').exists() else 'prek')"

   # Or use the holistic-linting detection script if available
   uv run holistic-linting/scripts/detect-hook-tool.py run --files <files>
   ```

   Detection logic: reads `.git/hooks/pre-commit` line 2, token 5 identifies the tool. Defaults to `prek`.

   **Note**: prek is a Rust-based drop-in replacement for pre-commit. Both tools use the same `.pre-commit-config.yaml` and have identical CLI interfaces.

   **Use detected tool with**: `uv run <detected-tool> run --files <files>` for ALL quality checks

   - This runs the complete toolchain configured in the project
   - Includes formatting, linting, type checking, and custom validators
   - Matches exactly what runs in CI and blocks merges

2. **Else check CI pipeline configuration**:

   ```bash
   # Check for GitLab CI or GitHub Actions
   test -f .gitlab-ci.yml || find .github/workflows -name "*.yml" 2>/dev/null
   ```

   **If found**: Read the CI config to identify required linting tools and their exact commands

   - Look for `ruff`, `mypy`, `basedpyright`, `pyright`, `bandit` invocations
   - Note the exact commands and flags used
   - Execute those specific commands to ensure CI compatibility

3. **Else fallback to tool detection**:
   - Check `pyproject.toml` `[project.optional-dependencies]` or `[dependency-groups]` for dev tools
   - Use discovered tools with standard configurations

### Format-First Workflow

**The model always formats before linting.**

**Reason**: Formatting operations (like `ruff format`) automatically fix many linting issues (whitespace, line length, quote styles). Running linting before formatting wastes context and creates false positives.

**Mandatory sequence**:

1. **Format**: `uv run ruff format <files>` or via git hook tool (pre-commit/prek)
2. **Lint**: `uv run ruff check <files>` or via git hook tool
3. **Type check**: Use project-configured type checker
4. **Test**: `uv run pytest`

**When using git hook tool (pre-commit or prek)**:

```bash
# Detect which tool is installed, then run it
# Tool runs hooks in configured order (formatting first)
uv run <detected-tool> run --files <files>
```

The `.pre-commit-config.yaml` already specifies correct ordering - trust it.

### Type Checker Discovery

**The model detects which type checker the project uses**:

**Reason**: Projects standardize on different type checkers (basedpyright, pyright, mypy). Using the wrong one produces incompatible results.

**Detection priority**:

1. Check `.pre-commit-config.yaml` for `basedpyright`, `pyright`, or `mypy` hooks
2. Check `pyproject.toml` for `[tool.basedpyright]`, `[tool.pyright]`, or `[tool.mypy]` sections
3. Check `.gitlab-ci.yml` or GitHub Actions for type checker invocations

**Common patterns**:

- **basedpyright**: GitLab projects (native GitLab reporting format)
- **pyright**: General TypeScript-style projects
- **mypy**: Python-first type checking

**Example detection**:

```bash
# Check .pre-commit-config.yaml (works with both pre-commit and prek)
grep -E "basedpyright|pyright|mypy" .pre-commit-config.yaml

# Check pyproject.toml
grep -E "^\[tool\.(basedpyright|pyright|mypy)\]" pyproject.toml
```

Always detect from project configuration rather than assuming.

## Quality Gates

**The model follows the Linting Discovery Protocol before executing quality gates.**

**Every Python task must pass**:

1. **Format-first**: `uv run ruff format <files>` (or via git hook tool)
2. **Linting**: `uv run ruff check <files>` (clean, after formatting)
3. **Type checking**: Use **detected type checker** (`basedpyright`, `pyright`, or `mypy`)
4. **Tests**: `uv run pytest` (>80% coverage)
5. **Modern patterns**: `/modernpython` (no legacy typing)
6. **Script compliance**: `/shebangpython` (for standalone scripts)

**Preferred execution method**:

```bash
# If .pre-commit-config.yaml exists (runs all checks in correct order):
# First detect which tool is installed (pre-commit or prek), then:
uv run <detected-tool> run --files <changed_files>

# Else use individual tools in this exact sequence:
uv run ruff format <files>           # 1. Format first
uv run ruff check <files>            # 2. Lint after formatting
uv run <detected-type-checker> <files>  # 3. Type check (basedpyright/pyright/mypy)
uv run pytest                         # 4. Test
```

**For critical code** (payments, auth, security):

- Coverage >95%
- Mutation testing: `uv run mutmut run` (>90% score)
- Security scan: `uv run bandit -r packages/`

**CI Compatibility Verification**:

After local quality gates pass, verify CI will accept the changes:

1. If `.gitlab-ci.yml` exists: Check for additional validators not in pre-commit
2. If `.github/workflows/*.yml` exists: Check for additional quality gates
3. Ensure all CI-required checks are executed locally before claiming task completion

## Standard Project Structure

All Python projects use this directory layout:

**Reason**: Consistent structure enables reliable automation and clear separation between user code and dependencies.

```text
project-root/
├── pyproject.toml
├── packages/
│   └── package_name/      # Package code (hyphens in project name → underscores)
│       ├── __init__.py
│       └── ...
├── tests/
├── scripts/
├── sessions/              # Optional: cc-sessions framework
└── README.md
```

**Package Directory Naming**:

- Project name: `my-cli-tool` → Package directory: `packages/my_cli_tool/`
- Hyphens in project names become underscores in package directories
- The `packages/` directory distinguishes user code from external dependencies

**Hatchling Configuration**:

```toml
[tool.hatchling.build.targets.wheel]
packages = ["packages/package_name"]
```

This structure is consistent across all projects and enables clear separation of concerns.

## Integration

### External Reference Example

**Complete working example** (external): `~/.claude/agents/python-cli-demo.py`

This reference implementation demonstrates all recommended patterns:

- PEP 723 metadata with correct shebang
- Typer + Rich integration
- Modern Python 3.11+ (StrEnum, Protocol, TypeVar, Generics)
- Annotated syntax for CLI params
- Async processing
- Comprehensive docstrings

This file is not bundled with this skill and must be available in `~/.claude/agents/` separately. Use as reference when creating CLI tools.

### Using Asset Templates

When creating new Python projects, copy standard configuration files from the skill's assets directory to ensure consistency with established conventions:

**Reason**: Templates implement proven patterns and save setup time.

**Asset Directory Location**: `~/.claude/skills/python3-development/assets/`

**Available Templates**:

1. **version.py** - Dual-mode version management (hatch-vcs + importlib.metadata fallback)

   ```bash
   cp ~/.claude/skills/python3-development/assets/version.py packages/{package_name}/version.py
   ```

2. **hatch_build.py** - Build hook for binary/asset handling (only if needed)

   ```bash
   mkdir -p scripts/
   cp ~/.claude/skills/python3-development/assets/hatch_build.py scripts/hatch_build.py
   ```

3. **.markdownlint.json** - Markdown linting configuration

   ```bash
   cp ~/.claude/skills/python3-development/assets/.markdownlint.json .
   ```

4. **.pre-commit-config.yaml** - Standard git hooks configuration

   ```bash
   cp ~/.claude/skills/python3-development/assets/.pre-commit-config.yaml .

   # Install hooks using pre-commit or prek (whichever is available)
   # Both tools use the same configuration file and have identical interfaces
   uv run pre-commit install  # or: uv run prek install
   ```

5. **.editorconfig** - Editor formatting settings
   ```bash
   cp ~/.claude/skills/python3-development/assets/.editorconfig .
   ```

These templates implement the patterns documented in [User Project Conventions](./references/user-project-conventions.md) and ensure all projects follow the same standards for version management, linting, formatting, and build configuration.

<section ROLE_TYPE="orchestrator">

## Common Patterns to Follow (Orchestrator Only)

**Delegation Pattern**:

| Instead of                             | Use this pattern                                                               |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| Writing Python code directly           | Delegate to `@agent-python-cli-architect` with clear requirements              |
| Skipping validation steps              | Complete workflow: implement → test → review → validate                        |
| Pre-deciding technical implementations | Let agents determine HOW based on requirements                                 |
| Implementing and testing in same step  | Chain agents: `@agent-python-cli-architect` → `@agent-python-pytest-architect` |

**Reason**: Orchestrators coordinate workflows. Agents have specialized expertise and focused tool access for implementation.

For detailed pattern examples and corrections, see [Anti-Patterns section](./references/python-development-orchestration.md#anti-patterns-to-avoid) in the orchestration guide.

</section>

## Detailed Documentation

### Reference Documentation

**Core Orchestration Guide**: [Python Development Orchestration](./references/python-development-orchestration.md) - Detailed workflow patterns for TDD, feature addition, refactoring, and code review with comprehensive agent coordination strategies

**PEP 723 Specification**: [PEP 723 - Inline Script Metadata](./references/PEP723.md) - User-friendly guide to PEP 723 inline script metadata with examples and migration patterns

**Exception Handling**: [Exception Handling in Python CLI Applications with Typer](./references/exception-handling.md) - Critical guidance on preventing exception chain explosion in Typer applications with correct patterns for graceful error handling

**Typer and Rich Examples**: [Typer and Rich CLI Examples](./assets/typer_examples/index.md) - Executable examples demonstrating solutions to common problems with Rich Console text wrapping in CI/non-TTY environments and Panel/Table content wrapping

**Module Reference**: [Modern Python Modules](./references/modern-modules.md) - Comprehensive guide to 50+ modern Python libraries with deep-dive documentation for each module including usage patterns and best practices

**Tool Registry**: [Tool & Library Registry](./references/tool-library-registry.md) - Catalog of development tools, their purposes, and usage patterns for linting, testing, and build automation

**API Documentation**: [API Reference](./references/api_reference.md) - API specifications, integration guides, and programmatic interface documentation

#### Navigating Large References

To find specific modules in modern-modules.md:

```bash
grep -i "^### " references/modern-modules.md
```

To search for tools by category in tool-library-registry.md:

```bash
grep -A 5 "^## " references/tool-library-registry.md
```

To locate workflow patterns in python-development-orchestration.md:

```bash
grep -i "^## " references/python-development-orchestration.md
```

### External Commands

These slash commands are external dependencies installed in `~/.claude/commands/`:

- [/modernpython](~/.claude/commands/modernpython.md) - Python 3.11+ patterns and PEP references
- [/shebangpython](~/.claude/commands/shebangpython.md) - PEP 723 validation and shebang standards

## Summary

### Python Development Skill for All Roles

**For All Roles (Orchestrators and Agents)**:

- Modern Python 3.11+ standards and patterns
- Quality gates: ruff, pyright, mypy, pytest (>80% coverage)
- Command standards: /modernpython, /shebangpython
- Reference documentation for 50+ modern Python modules
- Tool and library registry

<section ROLE_TYPE="orchestrator">

**For Orchestrators Only**:

1. Read the [orchestration guide](./references/python-development-orchestration.md) before delegating
2. Choose the right agent based on task requirements
3. Provide clear context: file paths, success criteria, scope boundaries
4. Chain agents for complex workflows (design → test → implement → review)
5. Instruct agents to validate with quality gates and commands
6. Enable uv skill for package management

**Orchestration = Coordination + Delegation + Validation**

</section>
