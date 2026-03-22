---
name: validate
description: Validate current implementation against active spec
---

Check if the current code changes satisfy the requirements in the active spec.
Read the spec from specs/active/, run `pnpm test`, and report:
1. Which requirements are satisfied
2. Which requirements are missing or incomplete
3. Any test failures and what they mean
4. Whether the implementation is ready for `specsafe qa`
