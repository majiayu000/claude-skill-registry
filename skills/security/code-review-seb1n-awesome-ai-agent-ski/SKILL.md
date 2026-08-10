---
name: code-review
description: Perform thorough code reviews on files or pull requests, checking for bugs, security vulnerabilities, performance issues, and style violations. Use when the user requests code review or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills contributors
  version: 1.0.0
---

# Code Review

This skill enables an AI agent to conduct a structured, comprehensive code review on a source file, a set of changes, or a pull request. The agent examines the code across multiple quality dimensions — correctness, security, performance, readability, and maintainability — and produces a detailed review report with actionable feedback tied to specific lines of code.

## Workflow

1. **Parse the input and establish context.** Determine whether the input is a single file, a directory, or a pull request diff. If it is a pull request, fetch the diff and identify the base branch so that only the changed lines are reviewed. Read any related configuration files (linter configs, style guides, type definitions) to calibrate the review against the project's standards.

2. **Understand the intent of the change.** Read commit messages, PR descriptions, and surrounding code to understand what the author intended. This prevents false positives — a reviewer must know the goal before judging whether the code achieves it. Summarize the change in one sentence before proceeding.

3. **Check for correctness and bugs.** Walk through every changed function and trace the data flow. Look for null or undefined dereferences, off-by-one errors, incorrect boolean logic, unhandled error paths, race conditions in concurrent code, and resource leaks (open files, database connections, unreleased locks). Verify that edge cases — empty inputs, maximum values, unexpected types — are handled.

4. **Evaluate security.** Scan for common vulnerability patterns: unsanitized user input (SQL injection, XSS), hardcoded secrets or credentials, insecure cryptographic usage, overly permissive file or network access, and missing authentication or authorization checks. Flag any dependency additions and check for known CVEs.

5. **Assess performance and scalability.** Identify algorithmic complexity issues (nested loops over large collections, repeated database queries inside loops, unbounded memory growth). Check for unnecessary allocations, missing caching opportunities, and blocking calls in async contexts. Consider the expected data volume and whether the code will scale.

6. **Review readability and maintainability.** Evaluate naming clarity, function length, code duplication (DRY violations), and adherence to the project's style guide. Check that public functions have docstrings or type annotations. Verify that magic numbers are replaced with named constants and that complex logic has explanatory comments.

## Review Checklist

The agent evaluates every change against these categories:

| Category        | What to look for                                                        |
|-----------------|-------------------------------------------------------------------------|
| Bugs            | Null derefs, off-by-one, logic errors, unhandled exceptions             |
| Security        | Injection, XSS, hardcoded secrets, missing auth, insecure dependencies  |
| Performance     | O(n²) loops, N+1 queries, unnecessary allocations, blocking I/O        |
| Readability     | Unclear names, long functions, missing docs, inconsistent formatting    |
| DRY             | Copy-pasted blocks, duplicated logic that should be extracted           |
| Error handling  | Swallowed exceptions, missing retries, unclear error messages           |
| Testing         | Missing tests for new logic, broken existing tests, untested edge cases |

## Usage

Provide one or more of the following inputs:

- **File path** — a single source file to review in its entirety.
- **Directory path** — the agent reviews all source files in the directory.
- **Pull request URL** — e.g., `https://github.com/user/repo/pull/42`. The agent fetches the diff and reviews only the changed lines in context.
- **Diff or patch text** — raw unified diff pasted directly.
- **Focus area** (optional) — e.g., "focus on security" or "check performance only" to narrow the review scope.

## Examples

### Example 1 — Reviewing a Python function

Given this file `src/auth.py`:

```python
import hashlib

def authenticate(username, password, db):
    query = f"SELECT password_hash FROM users WHERE username = '{username}'"
    row = db.execute(query).fetchone()
    if row is None:
        return False
    stored_hash = row[0]
    input_hash = hashlib.md5(password.encode()).hexdigest()
    return input_hash == stored_hash
```

The agent produces the following review:

```
## Review: src/auth.py — authenticate()

### Critical — SQL Injection (line 4)
The query uses f-string interpolation with `username` directly in the SQL
string. An attacker can pass `' OR '1'='1` as the username to bypass
authentication entirely.

**Fix:** Use parameterized queries.
- row = db.execute(query).fetchone()
+ row = db.execute(
+     "SELECT password_hash FROM users WHERE username = ?", (username,)
+ ).fetchone()

### Critical — Weak Hashing Algorithm (line 9)
MD5 is cryptographically broken and unsuitable for password hashing. It is
vulnerable to rainbow table attacks and can be brute-forced in seconds on
modern hardware.

**Fix:** Use bcrypt or argon2 with a per-user salt.
- input_hash = hashlib.md5(password.encode()).hexdigest()
+ import bcrypt
+ return bcrypt.checkpw(password.encode(), stored_hash.encode())

### Warning — Timing Attack (line 10)
Direct string comparison of hashes with `==` leaks information through
timing differences. Use a constant-time comparison function.

**Fix:**
- return input_hash == stored_hash
+ import hmac
+ return hmac.compare_digest(input_hash, stored_hash)

### Info — Missing Type Annotations
Adding type hints improves readability and enables static analysis:
  def authenticate(username: str, password: str, db: Connection) -> bool:

**Summary:** 2 critical, 1 warning, 1 info. This function must not be
deployed until the SQL injection and hashing issues are resolved.
```

### Example 2 — Reviewing a pull request diff

Given a PR diff for `src/api/orders.js`:

```diff
@@ -12,6 +12,20 @@ const express = require("express");
 const router = express.Router();

+router.get("/orders", async (req, res) => {
+  const userId = req.query.userId;
+  const orders = await db.query("SELECT * FROM orders WHERE user_id = $1", [userId]);
+  const enriched = [];
+  for (const order of orders.rows) {
+    const items = await db.query("SELECT * FROM order_items WHERE order_id = $1", [order.id]);
+    order.items = items.rows;
+    enriched.push(order);
+  }
+  res.json(enriched);
+});
```

The agent produces:

```
## Review: src/api/orders.js — GET /orders

### Warning — N+1 Query (lines 18-21)
Each order triggers a separate SELECT for its items. For a user with 200
orders this executes 201 database queries. This will degrade significantly
under load.

**Fix:** Use a single JOIN or a batched IN query:
  const items = await db.query(
    "SELECT * FROM order_items WHERE order_id = ANY($1)",
    [orders.rows.map(o => o.id)]
  );
  // Then group items by order_id in application code.

### Warning — Missing Authorization Check (line 14)
The endpoint reads `userId` from the query string without verifying that
the authenticated user is allowed to view that user's orders. Any user
can read any other user's order history by changing the query parameter.

**Fix:** Validate that `req.user.id === userId` or that the requester
has an admin role before executing the query.

### Info — SELECT * Usage (lines 16, 19)
Selecting all columns returns data the client may not need (e.g.,
internal timestamps, soft-delete flags). Specify only the required columns
to reduce payload size and avoid leaking internal fields.

**Summary:** 0 critical, 2 warning, 1 info.
```

## Best Practices

- **Review the diff, not just the file.** Focus on changed lines and their immediate context. Avoid commenting on pre-existing issues unless they interact with the new changes.
- **Classify severity explicitly.** Use Critical / Warning / Info levels so the author knows what must be fixed before merging versus what is a suggestion.
- **Suggest concrete fixes, not vague complaints.** Instead of "this could be better," provide a replacement code snippet or a specific refactoring step.
- **Limit scope per review round.** If a file has dozens of issues, prioritize the top 5-7 most impactful ones. Overwhelming the author reduces the chance that anything gets fixed.
- **Acknowledge good patterns.** When the author makes a particularly clean abstraction or handles an edge case well, call it out. Positive feedback reinforces good habits.
- **Check tests alongside code.** If new logic lacks tests, flag it. If tests exist, verify they actually exercise the changed behavior and not just the happy path.

## Edge Cases

- **Generated or vendored code:** Files produced by code generators, protocol buffer compilers, or vendored dependencies should generally be excluded from review. The agent will skip files matching common generated-code patterns unless explicitly asked.
- **Large diffs (>1000 lines):** Very large pull requests are difficult to review thoroughly. The agent will warn the author and suggest splitting the PR, then focus on the highest-risk files first.
- **Language-specific idioms:** A pattern that is idiomatic in one language (e.g., Go's explicit error returns) may look like a code smell in another. The agent adjusts its expectations based on the detected language.
- **Incomplete context:** When reviewing a diff without access to the full repository, the agent may not be able to verify type definitions, configuration, or upstream callers. It will note assumptions explicitly.
- **Style-only changes:** If a PR contains only formatting or rename changes, the agent will confirm there are no semantic differences and produce a short approval rather than a full report.
