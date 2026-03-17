---
name: review
description: Run a senior-level code review on staged or recent changes
---

Review the code changes using all 6 team persona review checklists.

1. Identify what changed: run `git diff --cached` (staged) or `git diff HEAD~1` (last commit)
2. Read every changed file completely

3. Review as **Alex Rivera** (Hardware/Lead):
   - Protocol compliance, typed exceptions, fail-safe behavior, rollback logic

4. Review as **Priya Sharma** (QA/Testing):
   - Test coverage (success/validation/error paths), fixture quality, audit log assertions

5. Review as **Daniel Okoye** (App Developer):
   - Typed Pydantic models, thin handlers, DI via `Depends()`, layered architecture

6. Review as **Janet Moore** (Security):
   - `hmac.compare_digest()` for secrets, uniform error messages, no info leakage, audit logging

7. Review as **Marcus Chen** (DevOps):
   - Env-only config, structured logging, health endpoint, graceful shutdown

8. Review as **Sofia Nakamura** (Product):
   - OpenAPI metadata, documentation currency, backwards compatibility

9. Output findings grouped by severity: **Critical**, **High**, **Medium**, **Low**
10. Include positive feedback for well-implemented patterns