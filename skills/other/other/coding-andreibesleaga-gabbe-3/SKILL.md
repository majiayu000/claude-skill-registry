---
name: ci-autofix
description: Autonomous CI/CD Remediation. Parses failure logs from GitHub Actions/GitLab CI, identifies the root cause (Lint, Type Error, Test Failure), and attempts to generate and commit a fix.
triggers: [ci failed, build broken, test failed, lint error, fix ci, auto-fix]
context_cost: high
---

# CI Auto-Fix Skill

## Goal
Restore the "Green Build" state by autonomously fixing common CI failures.

## Flow

### 1. Log Analysis
**Input**: CI Failure Log / Terminal Output
**Action**: Identify the *first* failure type.
*   **Linting**: Prettier/ESLint errors? (e.g., "Missing semicolon", "Unused var").
*   **Type Check**: TypeScript/MyPy errors? (e.g., "Type 'string' is not assignable to type 'number'").
*   **Unit Test**: Assertion failure? (e.g., "Expected 200, got 500").
*   **Build**: Webpack/Rustc error? (e.g., "Module not found").

### 2. Diagnosis & Strategy
*   **Pattern Matching**:
    *   `TS2322` -> Fix type definition or cast.
    *   `Module not found` -> Check `package.json` or import path.
    *   `AssertionError` -> Read test case vs implementation (Review `spec.md`).

### 3. Auto-Remediation Loop
1.  **Isolate**: Create a temporary fix branch (optional) or stash.
2.  **Fix**: Apply the code change.
3.  **Local Verify**: Run the specific failing command locally (e.g., `npm run lint`).
    *   *If Pass*: Commit and Push.
    *   *If Fail*: Retry with "Self-Correction" context (feed error back to LLM).

### 4. Safety
*   **Max Retries**: 3 attempts per failure.
*   **Escalation**: If auto-fix fails 3 times, alert Human with "Request for Intervention".
