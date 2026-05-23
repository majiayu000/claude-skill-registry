---
name: jj:split
description: "Split the current commit into multiple commits grouped by function"
---

# Split Commit by Function

Split a commit into multiple commits, grouping changes by functional purpose.

## Process

1. Run `jj status` to check if splitting `@` (has changes) or `@-` (working copy empty)
2. Run `jj show <rev> --summary` and `jj diff -r <rev> --stat` for overview
3. Analyze changes:
   - Small (≤5 files, ≤200 lines): run `jj diff -r <rev>` directly
   - Large: use `/jj-context` to group changes by purpose
4. Propose functional groups (implementation+tests together, config separate, migrations separate)
5. Ask user for approval via AskUserQuestion
6. Execute splits with **one-line** descriptions:
   ```bash
   jj split -r <rev> -m "<description>" file1 file2
   ```
7. Describe the last group (no split needed):
   ```bash
   jj describe -r @- -m "<description>"
   ```

**IMPORTANT**: Always use single-line commit messages. Never use multi-line descriptions or bullet points.

## Common Groupings

- Core feature + its tests together
- Configuration/infrastructure separate
- Database migrations separate
- Refactoring/cleanup separate
- API changes vs UI changes

## Example

```bash
# Split auth files into new commit
jj split -r @- -m "src/auth: add user authentication" src/auth.py test/test_auth.py

# Split API files
jj split -r @- -m "services/api: add rate limiting" src/api/rate_limit.py test/test_rate_limit.py

# Describe the remaining migration
jj describe -r @- -m "db/migrations: add users table"
```

Note: After each split, revision ID changes. Use `@-` for subsequent splits.
