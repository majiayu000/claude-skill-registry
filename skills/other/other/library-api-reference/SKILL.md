---
name: library-api-reference
description: "Look up, document, and troubleshoot internal libraries, SDKs, and APIs. Use when the user asks 'how does our X library work', 'what's the API for Y', 'document this internal tool', 'I keep getting errors from Z library', 'what are the gotchas with this SDK', or needs to understand undocumented internal code. Also triggers on 'API reference', 'library docs', 'SDK usage', 'internal tool documentation', 'common gotchas', 'how to use this package', or 'library documentation'."
version: 1.0.0
---

# Library API Reference

## Purpose

External libraries have official documentation, Stack Overflow answers, and community guides. Internal libraries have none of that. Shared utilities, internal SDKs, wrapper libraries, and team-built packages accumulate tribal knowledge that lives in Slack threads, outdated READMEs, and the memories of engineers who have since moved on. When a developer needs to use an internal library, they face a choice: read the source code line by line, or interrupt a colleague.

This skill bridges that gap. It systematically discovers, documents, and troubleshoots internal libraries by treating the codebase itself as the source of truth -- extracting API surfaces from type definitions, mining real usage patterns from call sites, and identifying gotchas from error handling, git history, and test fixtures.

## When to Activate

Trigger this skill when the user:

| Signal | Example |
|--------|---------|
| Asks how an internal library works | "How does our `@acme/http-client` work?" |
| Encounters unexplained errors from shared code | "I keep getting `AUTH_TOKEN_EXPIRED` from the auth library" |
| Needs to document an internal API | "Can you document the caching module?" |
| Asks about migration between versions | "How do I migrate from v2 to v3 of the config library?" |
| Wants to discover available internal tools | "What shared utilities do we have?" |
| Needs to understand configuration options | "What env vars does the logger need?" |
| Asks about gotchas or edge cases | "Any gotchas with the database wrapper?" |

## Core Workflow

### Phase 1: Discovery -- Identify the Library

Before documenting anything, locate the library and gather its foundational artifacts.

1. **Find the package root.** Search for `package.json`, `setup.py`, `Cargo.toml`, `go.mod`, or equivalent manifest files using Glob. Identify the library name, version, and declared dependencies.

2. **Locate existing documentation.** Search for README files, doc directories, wiki references, and inline documentation:
   - `Glob` for `**/README*`, `**/docs/**`, `**/CHANGELOG*`
   - `Grep` for JSDoc (`@param`, `@returns`, `@throws`), Python docstrings (`"""`), Rustdoc (`///`), or GoDoc comments

3. **Find type definitions.** These are the most reliable documentation source:
   - TypeScript: `*.d.ts` files, exported interfaces/types
   - Python: type hints, `.pyi` stub files
   - Go: exported types in package files
   - Java/Kotlin: public interface declarations

4. **Check for examples.** Search for `**/examples/**`, `**/demo/**`, or test files that demonstrate usage patterns.

**Output:** A summary of what was found -- package metadata, documentation status (present/outdated/missing), type coverage, and example availability.

### Phase 2: Interface Mapping -- Extract the Public API Surface

Map every publicly accessible entry point. Focus on what consumers can call, not internal implementation.

1. **Identify exports.** Find the main entry point (`index.ts`, `__init__.py`, `lib.rs`, `main.go`) and trace all re-exports. Build a list of:
   - Exported functions and their signatures
   - Exported classes/types/interfaces
   - Exported constants and configuration objects
   - Exported hooks (React) or middleware (Express/Koa)

2. **Extract configuration surface.** Search for:
   - Environment variable reads (`process.env`, `os.environ`, `std::env`)
   - Config file loading (`.yaml`, `.json`, `.toml` parsers)
   - Constructor parameters and option objects
   - Default values and fallback behavior

3. **Map error types.** Find all custom error classes, error codes, and error messages the library can produce:
   - `Grep` for `throw new`, `raise`, `return Err`, custom error classes
   - Catalog error codes and their meanings

4. **Present the API structured.** Use a table format:

| Function | Parameters | Returns | Throws | Description |
|----------|-----------|---------|--------|-------------|
| `createClient(opts)` | `ClientOptions` | `Client` | `ConfigError` | Creates a configured HTTP client |
| `client.get(url)` | `string, RequestOptions?` | `Promise<Response>` | `NetworkError, TimeoutError` | Performs a GET request |

### Phase 3: Usage Pattern Mining -- How Is It Actually Used?

Documentation tells you how a library *should* be used. Call sites tell you how it *is* used.

1. **Find import sites.** Grep for imports of the library across the codebase:
   - `import { ... } from '@acme/library'`
   - `from acme.library import ...`
   - `use acme::library::`

2. **Identify common patterns.** Look at the 5-10 most recent import sites. Categorize:
   - **Happy path:** Standard initialization + usage
   - **Error handling:** How callers handle failures
   - **Configuration:** What options callers typically pass
   - **Workarounds:** Any patterns that suggest the API is awkward

3. **Select 2-3 representative examples.** Choose call sites that demonstrate:
   - Basic usage (the simplest correct invocation)
   - Advanced usage (with configuration, error handling, or composition)
   - Edge case handling (retry logic, fallbacks, cleanup)

4. **Present examples with context.** Show the file path, the surrounding code, and a brief annotation explaining why this pattern exists.

### Phase 4: Gotcha Identification -- What Will Bite You?

This is the highest-value phase. Gotchas are invisible until they bite.

1. **Error handling archaeology.** Search for `try/catch` blocks, `.catch()` calls, and error callbacks around the library. Patterns like `// TODO: handle this properly` or `// HACK:` are gold.

2. **Git blame for recent fixes.** Run `git log` on the library source to find recent bug fixes. Each fix implies a gotcha that someone already hit:
   - Look at commit messages mentioning "fix", "bug", "workaround", "regression"
   - Check if the fix is a behavioral change that existing consumers might not know about

3. **Test fixtures as documentation.** Test files reveal edge cases the library authors considered important:
   - `Grep` for test descriptions (`describe`, `it`, `test`, `#[test]`)
   - Look for test names containing "edge", "fail", "error", "timeout", "retry", "race"
   - Test fixtures often encode assumptions about valid/invalid inputs

4. **TODO/FIXME/HACK comments.** These are unfinished documentation:
   - `Grep` for `TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX`, `DEPRECATED`
   - Each one is a known limitation that never made it to official docs

5. **Compile gotchas into a categorized list.** Use the categories from `references/common-library-gotchas.md` as a framework.

## Documentation Output Template

When documenting a function or module, use this structure. See `references/api-documentation-template.md` for the full fillable template.

```markdown
## `functionName(param1, param2, options?)`

**Description:** One-line explanation of what this function does and why you would use it.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `param1` | `string` | Yes | -- | The resource identifier |
| `param2` | `number` | Yes | -- | Timeout in milliseconds |
| `options` | `RequestOptions` | No | `{}` | Additional configuration |

**Returns:** `Promise<Result>` -- Description of the return value and its shape.

**Errors:**

| Error | Condition | Recovery |
|-------|-----------|----------|
| `ConfigError` | Missing required env var | Set `API_BASE_URL` |
| `TimeoutError` | Request exceeds timeout | Increase timeout or add retry |

**Example (happy path):**
// Show the simplest correct usage

**Example (error handling):**
// Show proper error handling

**Known Limitations:**
- Does not support streaming responses
- Connection pool limited to 10 concurrent requests

**Environment/Config Requirements:**
- `API_BASE_URL` -- Required, no default
- `API_TIMEOUT` -- Optional, defaults to 5000ms
```

## Gotchas -- Real Failure Modes When Using This Skill

These are pitfalls to watch for when researching and documenting internal libraries:

### Type Definitions May Lie

In loosely typed codebases (especially JavaScript with added TypeScript), type definitions may not match runtime behavior. A function typed as returning `Promise<User>` might actually return `Promise<User | null>` or throw an untyped error. **Always verify type signatures against actual usage and test files.**

### Implicit Dependencies Hide in Plain Sight

Internal libraries often depend on things that are not in their parameter lists:
- Environment variables that must be set before import
- Global initialization that must happen first (database connections, SDK setup)
- Peer dependencies that are assumed but not declared
- Specific Node.js/Python/runtime version requirements

**Mitigation:** Search for module-level side effects, top-level `await`, and initialization functions.

### Version Drift Across Consumers

When an internal library is consumed by multiple services, those services may pin different versions. A behavior you document from the source may not match what a particular consumer experiences. **Check the consumer's lockfile to verify the actual version in use.**

### Circular Dependencies Corrupt the Dependency Graph

Internal libraries that depend on each other create circular imports that manifest as `undefined` at runtime. When mapping library interfaces, watch for re-exports that create cycles. **Use `madge` (JS) or equivalent tools to visualize the dependency graph.**

### READMEs Are Unreliable

A README that was accurate when written may be months or years out of date. Treat READMEs as hypotheses, not facts. **Cross-reference every README claim with the current source code, especially default values, configuration options, and supported parameters.**

### Auto-Generated Docs Are Syntactically Correct but Semantically Stale

JSDoc, Sphinx, GoDoc, and similar tools generate documentation from code comments. These comments may describe the function's original behavior, not its current behavior. **Compare doc comments against the actual function body, especially after refactors.**

## Examples

### Example A: Documenting a Shared HTTP Client Wrapper

**User request:** "How does our `@acme/http-client` work? I need to make authenticated API calls."

**Workflow:**

1. **Discovery:** Glob for the package root. Find `packages/http-client/package.json`. Locate `src/index.ts` as the entry point. Find a README that mentions basic usage but is 8 months old.

2. **Interface Mapping:** Trace exports from `index.ts`:
   - `createClient(config: ClientConfig): HttpClient`
   - `HttpClient.get<T>(url, options?): Promise<ApiResponse<T>>`
   - `HttpClient.post<T>(url, body, options?): Promise<ApiResponse<T>>`
   - `ClientConfig` requires `baseUrl` and optional `auth`, `timeout`, `retryPolicy`
   - Env vars: `HTTP_CLIENT_TIMEOUT` (default 5000), `HTTP_CLIENT_MAX_RETRIES` (default 3)

3. **Usage Pattern Mining:** Find 12 import sites. Common pattern: all services create a singleton client in a `services/` directory, pass auth tokens from context. Two services override the retry policy for idempotent-unsafe endpoints.

4. **Gotcha Identification:**
   - Git log reveals a fix from 3 weeks ago: retry logic was retrying POST requests, which caused duplicate writes. Now only retries GET/HEAD by default.
   - A `// HACK: force content-type` comment in the source reveals that the client overrides `Content-Type` headers silently.
   - Tests reveal that `timeout: 0` means "no timeout" (not "immediate timeout").

### Example B: Troubleshooting a Failing Internal Auth Library

**User request:** "I keep getting `TOKEN_REFRESH_FAILED` from `@acme/auth`. It works in staging but fails in production."

**Workflow:**

1. **Discovery:** Find `packages/auth/src/token-manager.ts`. Identify the `TOKEN_REFRESH_FAILED` error code -- thrown when the refresh endpoint returns a non-200 status.

2. **Interface Mapping:** The `TokenManager` class has a `refreshToken()` method that calls `AUTH_REFRESH_URL`. This URL is read from the environment at module load time, not at call time.

3. **Usage Pattern Mining:** The user's service imports `TokenManager` as a singleton. In staging, `AUTH_REFRESH_URL` points to an internal endpoint. In production, it points to an external endpoint behind a different firewall rule.

4. **Gotcha Identification:**
   - The library reads `AUTH_REFRESH_URL` at import time. If the env var changes after import (common in hot-reload scenarios), the library uses the stale value.
   - Git blame shows a recent change: the refresh endpoint now requires an `X-Request-ID` header that the library does not send. This header is only enforced in production.
   - A test named `it('fails gracefully when refresh endpoint is unreachable')` reveals that the library throws `TOKEN_REFRESH_FAILED` for both network errors and auth errors -- the error message does not distinguish between them.

**Resolution:** The production `AUTH_REFRESH_URL` was correct, but the production auth service now requires `X-Request-ID`. The library needs an update to send this header, or the auth service needs to make the header optional.
