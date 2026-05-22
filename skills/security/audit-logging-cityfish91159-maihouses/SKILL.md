---
name: audit_logging
description: Ensure every critical action is logged (vital for UAG/Trust Room).
allowed-tools: Read, Edit, Write
---

# Audit Logging Protocol

## 1. Principles

- **No Invisible Actions**: Every state-changing API call (POST, PUT, DELETE) must produce a log entry.
- **Traceability**: Logs must include `userId`, `action`, `resourceId`, and `metadata`.

## 2. Implementation Standards

- **Backend (API)**:
  - Use the project's standard Logger service (e.g., `src/services/logger.ts` or similar).
  - Example:
    ```typescript
    await Logger.info({
      event: 'POST_CREATED',
      userId: user.id,
      metadata: { postId: newPost.id },
    });
    ```
- **Database (Supabase)**:
  - Ensure tables have `created_at`, `updated_at`, and `created_by` columns.
  - Check if specific Audit Table inserts are required (e.g. `audit_logs` table).

## 3. Verification Checklist

- [ ] Does the new API endpoint call `Logger`?
- [ ] Are logs visible in Supabase/Dashboards?
- [ ] Is the log level appropriate (Info vs Error)?
- [ ] Does the log contain enough context to debug issues later?
