---
name: database-migration-create
description: Safely creates database migrations
---

## Procedure

1. Analyze the schema change requirement.
2. Write the SQL migration file (UP and DOWN if needed).
3. Review for locking issues or data loss risks.
4. Update ORM definitions/types.
5. Apply migration locally to verify.
