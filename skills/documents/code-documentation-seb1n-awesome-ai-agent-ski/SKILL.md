---
name: code-documentation
description: "Automatically generate clear, comprehensive documentation for codebases — including API references, inline docstrings, README files, and usage guides. Use when the user requests code documentation or provides relevant inputs for this workflow."
license: "MIT"
metadata:
  author: "awesome-ai-agent-skills contributors"
  version: "1.1.0"
---

# Code Documentation

This skill enables an AI agent to analyze source code and produce high-quality documentation in multiple formats. It covers everything from single-function docstrings to full project README files, ensuring that both human developers and downstream tooling (IDEs, doc generators) benefit from consistent, accurate descriptions.

## Workflow

1. **Inventory the Codebase**: Walk the project tree and catalog public modules, classes, functions, constants, and type definitions. Note which symbols already have documentation and which are missing or stale.

2. **Determine Documentation Scope**: Based on the user's request, decide whether to generate inline docstrings, a standalone API reference, a project-level README, or a combination. Match the output format to the project's existing conventions (JSDoc, Google-style Python docstrings, TypeDoc, RDoc, etc.).

3. **Analyze Signatures and Behavior**: For each symbol, inspect parameter types, return types, default values, raised exceptions, and side effects. Read surrounding test files when available to understand intended usage and edge cases.

4. **Generate Documentation**: Write documentation that includes a one-line summary, an extended description when the logic is non-trivial, parameter and return-value documentation with types, exception/error documentation, and at least one usage example for public API surfaces.

5. **Insert or Update In-Place**: For inline documentation (docstrings, JSDoc comments), insert the generated text directly above or inside the relevant symbol. For standalone files (README, API reference), create or update the Markdown file at the project root or a `docs/` directory.

6. **Validate and Cross-Reference**: Verify that documented parameter names match the actual signature, that referenced types exist, and that examples are syntactically valid. Flag any inconsistencies for the user to review.

## Supported Formats

- **Python**: Google-style docstrings, NumPy-style docstrings, Sphinx reStructuredText
- **JavaScript / TypeScript**: JSDoc (`@param`, `@returns`, `@throws`), TypeDoc annotations
- **Java**: Javadoc (`@param`, `@return`, `@throws`)
- **Go**: Godoc comment conventions (comment block immediately above the declaration)
- **Rust**: `///` doc comments with Markdown, `#[doc]` attributes
- **Ruby**: YARD (`@param`, `@return`, `@example`)
- **Markdown**: README files, CHANGELOG entries, architecture decision records (ADRs)

## Usage

Point the agent at a file, directory, or specific symbol and describe what documentation you need. Examples of valid requests:

- "Add Google-style docstrings to every public function in `src/services/`."
- "Generate a README for this project based on its structure and package.json."
- "Document this class with JSDoc, including examples for each method."

The agent will respect existing documentation style in the project. If no convention is detected, it will ask which format to use or default to the most common style for the language.

## Examples

### Example 1 — Documenting a Python Class with Google-Style Docstrings

**User Request**: "Add docstrings to this class and its methods."

**Before**:
```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self._last_refill = time.monotonic()

    def consume(self, tokens=1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self._last_refill = now
```

**After**:
```python
class TokenBucket:
    """A token-bucket rate limiter.

    Tokens are added at a constant rate and consumed by callers.
    When the bucket is empty, requests are rejected until enough
    tokens have accumulated.

    Args:
        capacity: Maximum number of tokens the bucket can hold.
        refill_rate: Tokens added per second.

    Example:
        >>> bucket = TokenBucket(capacity=10, refill_rate=2)
        >>> bucket.consume(3)
        True
    """

    def __init__(self, capacity: float, refill_rate: float) -> None:
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self._last_refill = time.monotonic()

    def consume(self, tokens: int = 1) -> bool:
        """Attempt to consume tokens from the bucket.

        Triggers an internal refill based on elapsed time before
        checking availability.

        Args:
            tokens: Number of tokens to consume. Defaults to 1.

        Returns:
            True if the tokens were available and consumed, False otherwise.
        """
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self) -> None:
        """Refill the bucket based on time elapsed since the last refill."""
        now = time.monotonic()
        elapsed = now - self._last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self._last_refill = now
```

### Example 2 — Generating a Project README from Structure

**User Request**: "Generate a README for this project."

Given a project with the following layout:
```
myapi/
├── package.json          (name: @acme/myapi, scripts: dev, build, test)
├── src/
│   ├── index.ts          (Express app entry point)
│   ├── routes/
│   │   ├── users.ts
│   │   └── orders.ts
│   └── middleware/
│       └── auth.ts
├── tests/
│   └── users.test.ts
└── Dockerfile
```

**Generated README.md**:
```markdown
# @acme/myapi

A RESTful API service built with Express and TypeScript.

## Getting Started

### Prerequisites

- Node.js >= 18
- npm or yarn

### Installation

git clone https://github.com/acme/myapi.git
cd myapi
npm install

### Running Locally

npm run dev        # Start the dev server with hot reload
npm run build      # Compile TypeScript to dist/
npm test           # Run the test suite

### Docker

docker build -t myapi .
docker run -p 3000:3000 myapi

## API Endpoints

| Method | Path           | Description           |
|--------|----------------|-----------------------|
| GET    | /users         | List all users        |
| POST   | /users         | Create a new user     |
| GET    | /orders        | List all orders       |
| POST   | /orders        | Create a new order    |

## Project Structure

- `src/index.ts` — Application entry point and server bootstrap.
- `src/routes/` — Route handlers grouped by resource.
- `src/middleware/auth.ts` — JWT authentication middleware.
- `tests/` — Jest test files.

## License

MIT
```

## Best Practices

- **Match the project's existing style.** If the codebase uses NumPy-style docstrings, do not switch to Google-style mid-project. Consistency matters more than personal preference.
- **Document the "why," not just the "what."** Parameter types are often obvious from signatures; focus on intent, constraints, and non-obvious behavior.
- **Include at least one example for every public API symbol.** Examples are the most-read part of any documentation and catch subtle misunderstandings.
- **Keep README files scannable.** Use headings, tables, and code blocks. Developers skim — put the most important information (install, run, deploy) first.
- **Do not document private internals unless asked.** Over-documenting implementation details creates maintenance burden and can mislead readers into depending on unstable APIs.
- **Regenerate docs when the code changes.** Stale documentation is worse than no documentation. Prefer tooling that validates docs against signatures at CI time.

## Edge Cases

- **Dynamically generated APIs**: When routes or methods are registered at runtime (e.g., via decorators or plugin systems), static analysis may miss them. Warn the user and suggest runtime introspection or manual annotation.
- **Overloaded or generic functions**: For TypeScript overloads or Python `@overload`, document each signature variant separately with its own parameter descriptions and examples.
- **Monorepos**: When a repository contains multiple packages, generate a root README that links to per-package READMEs rather than one monolithic document.
- **Non-English codebases**: If variable names and existing comments are in another language, ask the user whether documentation should be in English or the project's primary language.
- **Proprietary or sensitive code**: Avoid including internal URLs, credentials, or business logic details in generated READMEs that may become public. Redact or generalize where necessary.
