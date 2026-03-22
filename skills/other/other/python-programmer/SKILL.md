---
name: python-programmer
description: Python-specific idioms, philosophy, and expert-level patterns. Use when working with Python code, including Jupyter notebooks (.ipynb). Covers Pythonic thinking, common pitfalls from other language backgrounds, testing ecosystem navigation, type hints trade-offs, and when to use modern Python features.
---

# Python Programmer

<skill_scope skill="python-programmer">
This skill provides guidance on Python-specific idioms, philosophy, and expert-level judgment calls. Python's design emphasizes readability and "one obvious way" to do things, but achieving truly Pythonic code requires understanding when and why to use Python's idioms.

**Related skills:**
- `software-engineer` — Core engineering philosophy, system design principles
- `functional-programmer` — When functional approaches are clearer
- `test-driven-development` — Testing philosophy and TDD principles
</skill_scope>

## When to Use This Skill

<when_to_use>
Use this skill when:
- Working with Python code
- Deciding when Python is the right tool for a problem
- Navigating between Python's "obvious ways" and edge cases
- Choosing between testing frameworks, type systems, or async patterns
- Avoiding anti-patterns from Java, C, or JavaScript backgrounds
- Making trade-offs between Pythonic idioms and readability
</when_to_use>

## Core Philosophy

<core_philosophy>
**For foundational software engineering principles, see the software-engineer skill.**

### The Zen of Python (PEP 20)

Python's design philosophy is captured in "The Zen of Python" (`import this`). Key principles:

**Quote to remember:** "Explicit is better than implicit. Simple is better than complex. Readability counts." — Tim Peters, PEP 20

**In practice:**
- Favor clarity over cleverness
- One obvious way beats multiple equivalent ways
- Code is read more than written (optimize for readers)
- Practicality beats purity (Python isn't a pure functional or OO language)

**Staff insight:** The Zen is philosophy, not law. Sometimes implicit is fine (e.g., context managers hide `__enter__` and `__exit__`). Sometimes there are two ways (e.g., list comprehension vs `map`). The Zen guides judgment; it doesn't eliminate it.

<pythonic_vs_readable>
### When Pythonic Idioms Hurt Readability

The Zen says both "Explicit is better than implicit" and to use Python idioms. When they conflict, optimize for readers.

| Code Characteristic | Use Pythonic Idiom | Use Explicit Form |
|---------------------|-------------------|-------------------|
| Reader must pause to parse | No | Yes |
| Requires advanced feature knowledge | No | Yes |
| In critical path / main logic | No | Yes |
| In isolated utility function | Yes | Maybe |
| Junior engineer would need to look it up | No | Yes |
| Saves 1-2 lines at cost of clarity | No | Yes |
| Standard pattern (e.g., simple dict comprehension) | Yes | No |
| Clever trick (e.g., tuple sort keys, walrus operator chains) | No | Yes |

**Heuristics:**
- If you need a comment explaining the trick, the trick is too clever
- Nested comprehensions beyond 2 levels need explicit loops
- Walrus operator (`:=`) in comprehension conditions is usually too clever
- Code golf is not a virtue — readable beats concise
</pythonic_vs_readable>

<eafp_principle>
### EAFP vs LBYL

Python culture prefers EAFP (i.e., try/except) over LBYL (i.e., check-then-act). Use EAFP for dict lookups, file access, network calls, and anywhere race conditions matter. Use LBYL for pre-flight validation before expensive operations and performance-critical tight loops where the exceptional case is common.

**Staff insight:** EAFP is about correctness and clarity, not performance. The file existence check has a race condition; the exception handling doesn't. But exceptions have real cost (e.g., stack unwinding, traceback construction) — they're fine when the exceptional case is rare, not for expected control flow in loops.
</eafp_principle>

<duck_typing>
### Duck Typing and Protocols

Prefer protocols (i.e., behavior) over explicit type checking. Don't use `isinstance` except with abstract base classes at system boundaries. Use `typing.Protocol` for duck-typed interfaces — it gives you structural subtyping with type checker support. Use `@runtime_checkable` only when you genuinely need runtime protocol checking.
</duck_typing>
</core_philosophy>

## Safety Constraints

<safety_constraints>
- **NEVER** use mutable default arguments (e.g., lists, dicts, sets) without the `None` sentinel pattern
- **NEVER** use `global` for shared state — use classes or explicit parameter passing
- **NEVER** catch bare `Exception` or bare `except:` and swallow errors silently
- **NEVER** use `eval()` or `exec()` on untrusted input
- **NEVER** sacrifice readability for cleverness — a 4-line loop beats a cryptic 1-line comprehension
- **NEVER** recommend or configure darglint — it was archived December 2022 and receives no maintenance; use pydoclint
- **NEVER** generate `requirements.txt` or `setup.py` for new projects — use `pyproject.toml` with uv
- **NEVER** use `typing.Optional[X]` when targeting Python 3.10+ — use `X | None` instead
- **NEVER** use bare `except:` without an exception type
- **NEVER** use `from __future__ import annotations` in new code — it's superseded by PEP 649 (i.e., deferred evaluation, default in 3.14)
- **ALWAYS** use context managers (`with`) for file handles, locks, and database connections
- **ALWAYS** use parameterized queries — never string concatenation for SQL
- **ALWAYS** validate and sanitize untrusted input at system boundaries
- **ALWAYS** include `if __name__ == "__main__":` guard in executable scripts
- **ALWAYS** follow existing project conventions for docstring style, tooling, and package management — don't fight established codebases
</safety_constraints>

## Fundamental Principles

<fundamental_principles>
<comprehensions>
### Comprehensions: Simple Cases Only

List/dict/set comprehensions are Pythonic for *simple* transformations.

**Complexity limits:**
- One `for` clause: usually fine
- Two `for` clauses: acceptable for obvious Cartesian products
- Three+ `for` clauses: use explicit loops
- Walrus operator (`:=`) in conditions: almost always too clever
- More than one filter condition: use explicit loops
- Any logic requiring explanation: use explicit loops
- Side effects: never use comprehensions

**Staff insight:** Comprehensions are readable when they fit on one line and scan left-to-right. The moment you nest, chain conditions, or use walrus operators, you're optimizing for concision over clarity.
</comprehensions>

<context_managers>
### Context Managers

Always use `with` for files, locks, and database connections. Use `contextlib.contextmanager` for simple cases, `ExitStack` for dynamic resource management. Don't write try/finally when a context manager expresses intent better.
</context_managers>

<iterators_generators>
### Iterators and Generators

Use generators for large/infinite sequences and one-pass iteration. Use lists when you need multiple passes, random access, or length upfront. Generator expressions in function calls avoid intermediate lists: `sum(x**2 for x in numbers)`.
</iterators_generators>

<mutable_defaults>
### Mutable Default Arguments

Default arguments are evaluated once at function definition. Use `None` as a sentinel for mutable defaults:

```python
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```
</mutable_defaults>
</fundamental_principles>

## Type System

<type_system>
### Type Hints Are Mandatory

Type hints are required for all production code. They provide explicit, machine-readable contracts; enable static analysis; and are critical for LLM-assisted development.

**Where to use type hints:**
- All public APIs, function signatures, and class attributes: required
- Internal functions in non-trivial modules: required
- Local variables: only when type isn't obvious from context
- Throwaway scripts (i.e., < 50 lines, one-time use): optional

<modern_type_syntax>
### Modern Type Syntax

**Union types (3.10+):** Use `X | None` instead of `Optional[X]`. Use `int | str` instead of `Union[int, str]`.

**Type parameter syntax (3.12+, PEP 695):** Use the bracket syntax for generics:

```python
# Modern (3.12+)
def first[T](items: list[T]) -> T: ...
type Vector[T] = list[T]

# Legacy (pre-3.12) — don't use in new code targeting 3.12+
from typing import TypeVar
T = TypeVar('T')
def first(items: list[T]) -> T: ...
```

**Deferred annotations (3.14+, PEP 649/749):** Annotations are now evaluated lazily by default. `from __future__ import annotations` (PEP 563) is superseded — don't use it in new code. It still works but has different semantics: PEP 563 stringifies annotations, while PEP 649 stores an evaluator function. For code targeting 3.10-3.13, PEP 563 remains useful for forward references.

**Other useful features:**
- `TypedDict` for structured dictionaries
- `Protocol` for structural subtyping (i.e., duck typing with types)
- `ParamSpec` and `Concatenate` for higher-order functions
- `typing.assert_never` for exhaustiveness checking in match statements
- `@override` decorator (3.12+) for explicit method overriding
</modern_type_syntax>

<type_checkers>
### Type Checkers

**ty (Astral):** Preferred for most projects. Written in Rust; dramatically faster than alternatives. Currently in beta (v0.0.x) but effective at catching real bugs in typical codebases. Use ty unless you need Pydantic or Django ORM integration, which it doesn't yet support.

**mypy:** The reference implementation with the broadest ecosystem support. Use mypy when you need its plugin API for dynamic frameworks (e.g., Pydantic, SQLAlchemy, Django ORM) or when your project already uses it. Configure with `strict = true` in `pyproject.toml`.

**pyright/basedpyright:** The dominant IDE type checker (powers Pylance in VS Code). Richer type narrowing than mypy; checks unannotated code by default. Consider basedpyright for LSP integration in non-VS Code editors.

| Context | Recommendation |
|---------|---------------|
| New project, no Pydantic/Django | ty |
| Pydantic or Django ORM | mypy (with framework plugin) |
| IDE/LSP experience | pyright or basedpyright |
| Existing mypy project | Keep mypy |
| Maximum strictness in CI | mypy `--strict` or basedpyright |
</type_checkers>
</type_system>

## Documentation

<documentation_requirements>
### Sphinx Docstrings

Python documentation uses Sphinx with reStructuredText. Comprehensive documentation is mandatory for all production code.

**Every module:** Module-level docstring explaining purpose and main components.

**Every public class:** Class docstring with purpose, responsibilities, and invariants.

**Every public function/method:**
- One-sentence summary (first line)
- Parameters with `:param:` and `:type:` (when `:type:` adds constraints beyond the signature)
- Return value with `:returns:` and `:rtype:`
- Exceptions with `:raises:`
- Usage examples for non-trivial functions

**Every test:** Docstring explaining what behavior is being tested and why.

See `references/docstring-example.py` for a complete example.

<docstring_type_annotations>
### When to Include `:type:` Annotations

Include `:type:` alongside type hints only when it adds information beyond the signature:

| Situation | Include `:type:`? | Example |
|-----------|------------------|---------|
| Type hint says `int`, no constraints | No | Signature suffices |
| Parameter must be positive | Yes | `:type: int (must be positive)` |
| Accepts specific enum values | Yes | `:type: str ("json" or "xml")` |
| Complex generic with usage notes | Yes | Explain expected structure |
| Simple `str`, `bool`, `list[str]` | No | Signature suffices |

Omit `:type:` when it would mechanically duplicate the signature. The goal is useful documentation, not ceremony.
</docstring_type_annotations>

<docstring_style_choice>
### Docstring Style

For **new projects**, use Sphinx/reST style (`:param:`, `:type:`, `:returns:`, `:rtype:`, `:raises:`). For **existing projects**, follow the established convention — don't convert a Google-style codebase to Sphinx mid-project. pydoclint supports all three styles (`sphinx`, `google`, `numpy`); configure it to match your project.
</docstring_style_choice>
</documentation_requirements>

## Python Tooling

<python_tooling>
### Mandatory Tools

**Ruff (linting and formatting):**
- Replaces Black, Flake8, isort, pydocstyle, and pyupgrade in a single Rust-based tool
- `ruff check` for linting, `ruff format` for Black-compatible formatting
- 10-100x faster than the tools it replaces
- Includes partial Bandit rules (`S` rule set) for common security checks
- Configure in `pyproject.toml` under `[tool.ruff]`

**pydoclint (docstring linting):**
- Validates docstring sections (params, returns, raises) match function signatures
- Replaces darglint, which was archived December 2022 — **do NOT use darglint**
- Supports Sphinx, Google, and NumPy docstring styles
- Runs standalone or as a flake8 plugin (install with `pydoclint[flake8]`)
- Required because Ruff's DOC rules are still in preview and don't yet support Sphinx style or DOC101 (i.e., missing parameter detection)
- Configure in `pyproject.toml` under `[tool.pydoclint]`

**Bandit (security linting — when needed):**
- Security vulnerability scanner for Python code
- Ruff's `S` rules cover most common security checks; use standalone Bandit only for security-critical projects needing full coverage (e.g., cryptographic vulnerability detection, severity classifications)
- Configure in `pyproject.toml`

**Type checker:** See `<type_checkers>` — use ty, mypy, or pyright depending on your project's needs.

<project_management>
### Project Management

**uv (primary project tool):**
- Ultra-fast Python package installer, project manager, and Python version manager
- Handles project initialization (`uv init`), dependency management (`uv add`/`uv remove`), lockfiles (`uv.lock`), building (`uv build`), publishing (`uv publish`), and script execution (`uv run`)
- Use for all new projects

**Hatch (matrix testing):**
- Use alongside uv specifically when you need declarative local multi-Python-version testing:
  ```toml
  [[tool.hatch.envs.hatch-test.matrix]]
  python = ["3.12", "3.13", "3.14"]
  ```
  Then `hatch test --all` runs tests across all versions locally.
- If you only test against one Python version locally and rely on CI for matrix testing, uv alone suffices
- Hatch also provides VCS-driven versioning (`hatch-vcs`) and custom build hooks if needed

| Workflow | Tool |
|----------|------|
| New project setup | `uv init --package` |
| Add dependencies | `uv add <pkg>` |
| Run tests | `uv run pytest` |
| Build and publish | `uv build && uv publish` |
| Local multi-version testing | Hatch (`hatch test --all`) |
| CI matrix testing | uv + GitHub Actions matrix |
</project_management>

### Dependency Version Specification

**NEVER guess or assume dependency versions.** Verify current versions on PyPI before adding any dependency.

| Constraint | When to Use |
|------------|-------------|
| `>=MAJOR.MINOR` | Default — allows patch updates, guards against old bugs |
| `>=MAJOR.MINOR,<NEXT_MAJOR` | When major version breaks are likely |
| `==EXACT` | Avoid — use lock files for reproducibility instead |

**Staff insight:** LLMs confidently hallucinate version numbers. The cost of a PyPI search is trivial compared to debugging phantom compatibility issues. This is especially critical for fast-moving ecosystems where major versions ship monthly.

See `references/pyproject-example.toml` for a starter project configuration.
</python_tooling>

## Testing

<testing_ecosystem>
**For general testing philosophy and TDD principles, see the test-driven-development skill.** This section covers Python-specific practices.

**Use pytest** for all new projects. It's the community standard: plain functions, simple `assert` with introspection, powerful fixtures, rich plugin ecosystem. Use `unittest` only in existing codebases that already use it.

**Core testing principle** (restated from test-driven-development skill): Mock at architectural boundaries (e.g., external systems, injected dependencies), not internal implementation details. The `unittest.mock` module is still useful with pytest.
</testing_ecosystem>

## Async Patterns

<async_patterns>
Use async/await for I/O-bound concurrency with many concurrent connections (e.g., web servers, websockets, batch HTTP requests). Don't use it for CPU-bound tasks, simple scripts, or when overhead isn't justified.

**Common mistakes:**
- Mixing sync and async code (e.g., blocking the event loop with synchronous `requests` or `psycopg2`)
- Using sync libraries in async contexts — use aiohttp, asyncpg, motor, redis.asyncio instead
- Premature async adoption when threads suffice

Bridge sync-to-async with `asyncio.to_thread()` (3.9+) when needed for CPU-bound work in async contexts.

**Staff insight:** Start with synchronous code. Add threads for I/O concurrency. Move to async only when you have many concurrent connections and measurable evidence it helps.
</async_patterns>

## Modern Python (3.12+)

<modern_python>
<python_312_features>
### Python 3.12

- **PEP 695**: Type parameter syntax (`def func[T](x: T) -> T`) — see `<modern_type_syntax>`
- **`@override` decorator**: Explicit intent for method overriding, caught by type checkers
- **F-string improvements**: Multi-line expressions, nesting, reused quote types all allowed
- **`distutils` removed** from stdlib; use `uv build`
</python_312_features>

<python_313_features>
### Python 3.13

- **Free-threaded build (experimental)**: GIL-optional via `--disable-gil` build flag; ~40% single-threaded overhead in this version
- **Improved REPL**: Color output, multi-line editing, better history
- **`locals()` semantics change**: Now returns a copy, not a proxy to the frame
</python_313_features>

<python_314_features>
### Python 3.14 (Current Stable)

- **PEP 649/749**: Deferred annotation evaluation is now the default — see `<modern_type_syntax>`
- **PEP 750**: Template strings (`t"Hello {name}"`) — evaluate to `Template` objects instead of `str`, enabling safe SQL interpolation, HTML templating, and structured logging
- **PEP 779**: Free-threaded build is now **officially supported** (Phase II), no longer experimental; single-threaded overhead reduced to ~5-10%
- **PEP 758**: `except` clauses no longer require parentheses for multiple exceptions: `except TimeoutError, ConnectionError:`
- **PEP 734**: `concurrent.interpreters` — multiple interpreters per process with `InterpreterPoolExecutor`
- **PEP 768**: Zero-overhead external debugger interface; `pdb` can attach to running processes
</python_314_features>

<gil_and_concurrency>
### The GIL and Concurrency

Python's Global Interpreter Lock historically prevented true parallelism for CPU-bound threads. This is changing.

**Current state (3.14):**
- The standard build still has the GIL (default behavior unchanged)
- The free-threaded build (PEP 779) removes the GIL and is officially supported, with ~5-10% single-threaded overhead
- Free-threading enables true parallel threads for CPU-bound work without `multiprocessing`

**Practical guidance today:**
- For I/O-bound concurrency: `asyncio` or threads (both work with or without GIL)
- For CPU-bound parallelism: `multiprocessing` remains the safe default; free-threaded builds are viable for early adopters
- `asyncio.to_thread()` (3.9+) bridges sync code into async contexts

**Staff insight:** Free-threading is the future but ecosystem support (e.g., C extensions, third-party libraries) is still maturing. For most projects, `multiprocessing` for CPU-bound work and threads/async for I/O-bound work remain the pragmatic choices.
</gil_and_concurrency>
</modern_python>

## When Python Works and Struggles

<python_fitness>
**Python excels at:** Rapid prototyping, scripting and automation, data analysis (e.g., NumPy, pandas), web services (e.g., FastAPI, Django), and education.

**Python struggles with:** Performance-critical tight loops (use NumPy or drop to C/Rust), real-time systems, mobile development, systems programming, and CPU-bound parallelism (though free-threading is changing this).

**Staff insight:** Use Python where its strengths (e.g., development speed, ecosystem, readability) outweigh its weaknesses. Don't force it into low-level, high-performance, or mobile domains.
</python_fitness>

## Common Pitfalls

<common_pitfalls>
<common_mistakes>
### By Background

<from_java>
**From Java:**
- Class hierarchies where composition or duck typing suffice
- Getters/setters instead of properties or public attributes
- Checked exception thinking (Python has no checked exceptions)
- Over-verbose code where Python values conciseness
</from_java>

<from_c>
**From C/C++:**
- Manual memory management thinking (trust the garbage collector)
- Low-level optimization before profiling (most code isn't the bottleneck)
</from_c>

<from_javascript>
**From JavaScript:**
- Callback patterns instead of async/await or sequential code
- Prototypal inheritance thinking (Python uses class-based)
</from_javascript>
</common_mistakes>

<python_specific_pitfalls>
### Python-Specific

- **Late binding in closures**: Closures capture variables by reference. Use default arguments (`lambda i=i: i`) or `functools.partial` to capture values in loop-generated functions
- **Truthiness confusion**: Empty containers, zero, `None`, and `False` are all falsy. Use `is None` when checking for `None` specifically, not `not x`
- **`global` abuse**: Pass parameters explicitly or use classes. `functools.lru_cache` replaces most caching-via-global patterns
- **Import cycles**: Use `TYPE_CHECKING` guard for type-only imports; restructure modules to break real circular dependencies
- **`pathlib` neglect**: Prefer `pathlib.Path` over `os.path` for path manipulation — it's more readable and less error-prone
- **Lambda assignment**: Don't assign lambdas to variables (PEP 8 E731) — use `def` for named functions
</python_specific_pitfalls>
</common_pitfalls>

## Dataclasses and attrs

<data_classes>
Use dataclasses (3.7+) for simple data containers. Use `slots=True` (3.10+) for memory efficiency and faster attribute access. Use `frozen=True` for immutability. Use `attrs` when you need validators, converters, or `evolve()` — its `define`/`field` API is more powerful than dataclasses for complex cases.

Dataclasses aren't a replacement for all classes — they're for data-focused classes. Use them for configuration, API responses, and value objects. Don't shoehorn behavior-heavy classes into dataclasses.
</data_classes>

## Resources

<resources>
**Official Documentation:**
- Python Documentation: https://docs.python.org/3/
- PEP Index: https://peps.python.org/
- PEP 8 Style Guide: https://peps.python.org/pep-0008/

**Tooling:**
- Ruff Documentation: https://docs.astral.sh/ruff/
- uv Documentation: https://docs.astral.sh/uv/
- ty Documentation: https://docs.astral.sh/ty/
- pydoclint Documentation: https://jsh9.github.io/pydoclint/
- MyPy Documentation: https://mypy.readthedocs.io/
- pytest Documentation: https://docs.pytest.org/
- Hatch Documentation: https://hatch.pypa.io/

**Style Guides:**
- Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
</resources>

<summary>
## Summary

Python programming emphasizes:
- **Readability over cleverness** — Code is read more than written; don't show off
- **Type hints everywhere** — Essential for code quality and LLM-assisted development; use PEP 695 syntax on 3.12+
- **Comprehensive documentation** — Sphinx docstrings with meaningful content, not mechanical `:type:` duplication
- **Modern tooling** — Ruff for linting/formatting, pydoclint for docstring validation, uv for project management, ty or mypy for type checking
- **EAFP over LBYL** — Try and catch exceptions rather than checking first
- **Duck typing with Protocols** — Accept behavior, not types
- **Simple Pythonic idioms** — Comprehensions for simple cases, explicit loops for complex ones

**All new projects must use uv for project management, with Ruff, pydoclint, and a type checker (ty or mypy) enabled in CI/CD.** Do NOT use darglint (archived 2022). Type hints and documentation are mandatory for all production code (exception: throwaway scripts). Follow existing project conventions rather than fighting established codebases.
</summary>
