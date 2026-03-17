---
name: 123-java-exception-handling
description: Use when you need to apply Java exception handling best practices — including using specific exception types, managing resources with try-with-resources, securing exception messages, preserving error context via exception chaining, validating inputs early with fail-fast principles, handling thread interruption correctly, documenting exceptions with @throws, enforcing logging policy, translating exceptions at API boundaries, managing retries and idempotency, enforcing timeouts, attaching suppressed exceptions, and propagating failures in async/reactive code. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Exception Handling Guidelines

Identify and apply robust Java exception handling practices to improve error clarity, security, debuggability, and system reliability.

**Core areas:** Specific exception types instead of generic `Exception`/`RuntimeException`, try-with-resources for automatic resource cleanup, secure exception messages that avoid information leakage, exception chaining to preserve full error context, early input validation with `IllegalArgumentException`/`NullPointerException`, `InterruptedException` handling with interrupted-status restoration, `@throws` JavaDoc documentation, fail-fast principle, structured logging with correlation IDs avoiding log-and-throw duplication, API boundary translation via centralized exception mappers, bounded retry with backoff for idempotent operations only, timeout enforcement with deadline propagation, `Throwable#addSuppressed` for secondary cleanup failures, never catching `Throwable`/`Error`, observability via error metrics, and failure propagation in async `CompletionStage` code.

**Prerequisites:** Run `./mvnw compile` before applying any changes. If compilation fails, **stop immediately** — do not proceed until the project is in a valid state.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 categorizes exception handling issues by severity (CRITICAL, MAINTAINABILITY, SECURITY, OBSERVABILITY) and area (validation, resource management, logging, boundary translation, async propagation). Step 3 replaces generic exception catches with specific types and introduces custom exceptions where needed. Step 4 wraps resource-managing code with try-with-resources. Step 5 audits exception messages for sensitive data exposure and sanitizes them. Step 6 adds exception chaining (`initCause`/constructor) to preserve original context. Step 7 adds early null/argument validation at method entry points. Step 8 fixes `InterruptedException` handling to restore interrupted status. Step 9 aligns logging to log-once-at-boundary policy with correlation IDs. Step 10 adds centralized exception mappers at API boundaries (controllers, message handlers). Step 11 applies bounded retry with backoff only to idempotent operations. Step 12 enforces timeouts and propagates deadline-exceeded errors. Step 13 uses `addSuppressed` when rethrowing after cleanup failures. Step 14 removes any catches of `Throwable` or `Error`. Step 15 emits error-class metrics and ensures observability for SLO/SLA monitoring. Step 16 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each exception handling pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/127-java-exception-handling.md](references/127-java-exception-handling.md).
