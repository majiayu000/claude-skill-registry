---
name: code-quality
description: Node.js code quality standards for the serverless function runtime. Use when writing, reviewing, or refactoring JavaScript/TypeScript code.
---

# Code Quality — Skill

## Purpose

Maintain consistent, spec-compliant code throughout the serverless function runtime implementation.

## When to Use

- Writing new source files
- Reviewing or refactoring existing code
- Making implementation decisions about structure or patterns

## Language and Runtime Conventions

1. **Node.js with modern JavaScript or TypeScript.** Use ES modules (`import`/`export`).
2. **Web-standard `Request`/`Response`** for the handler contract. Use the global `Request` and `Response` objects (Node.js 18+ built-in) or a minimal polyfill.
3. **Minimal dependencies.** Do not add frameworks or libraries unless strictly required by the spec. Prefer Node.js built-ins.
4. **No TypeScript compilation complexity.** If using TypeScript, keep the build step simple. Plain JavaScript is acceptable.

## Code Structure Conventions

1. **One module, one responsibility.** Each file should have a clear, single purpose.
2. **Named exports for public API.** Default exports only for handler method functions.
3. **Handler functions are named by HTTP method**: `export function GET(request) {}`, `export function POST(request) {}`.
4. **No global mutable state** except where explicitly required by the spec (warm module reuse via module-level variables is allowed per REQ-RTG-006).

## Error Handling Conventions

1. **Runtime errors use the spec's JSON format**: `{"errorCode": "<CODE>", "message": "<detail>"}`.
2. **Error codes are exactly**: `ROUTE_NOT_FOUND`, `METHOD_NOT_ALLOWED`, `HANDLER_EXCEPTION`, `INVALID_HANDLER_RESPONSE`, `INVOCATION_TIMEOUT`.
3. **HTTP status mapping is fixed**: 404, 405, 500, 500, 504 respectively.
4. **Handler exceptions must be caught** and mapped to `HANDLER_EXCEPTION` with the original error message.
5. **Timeout enforcement uses AbortController or equivalent** — do not rely on unref'd timers alone.

## Testing Conventions

1. **E2E tests run via `npm test`** (REQ-RCV-006).
2. **Tests start the runtime, send HTTP requests, and assert responses.** No mocking of the runtime itself.
3. **Each spec scenario (Section 6) maps to at least one test case.**
4. **Test exit code 0 on success** (REQ-RCV-007).

## Quality Checklist

- [ ] All source files use ES modules
- [ ] Handler contract uses Web-standard Request/Response
- [ ] No unnecessary dependencies added
- [ ] Error responses match spec JSON format exactly
- [ ] Timeout enforcement is 3000ms per invocation
- [ ] No debug prints or commented-out code in committed files
- [ ] Each file has a single, clear responsibility
