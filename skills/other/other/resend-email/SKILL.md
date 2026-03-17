---
name: resend-email
description: Enforces project Resend email conventions when implementing email sending, templates, batch operations, and newsletter broadcasts. This skill ensures consistent patterns for email service methods, error handling, retry logic, and Sentry integration.
---

# Resend Email Skill

## Purpose

This skill enforces the project Resend email conventions automatically during email implementation. It ensures consistent patterns for service architecture, email sending operations, template management, broadcast handling, error handling, and Sentry integration.

## Activation

This skill activates when:

- Creating or modifying `src/lib/services/resend*.ts` files
- Working with email template files in `src/lib/email-templates/`
- Implementing email sending operations via Resend
- Creating broadcast or newsletter functionality
- Any code that imports from `resend` package
- Files containing email-related operations (send, batch, broadcast)

## Workflow

1. Detect Resend email work (imports from `resend` or uses ResendService patterns)
2. Load `references/Resend-Email-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of email patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### Service Architecture

- Use `ResendService` static class pattern
- Methods must have `Async` suffix for async operations
- Apply circuit breaker protection via `circuitBreakers.externalService()`
- Implement retry logic via `withDatabaseRetry()`
- Add Sentry breadcrumbs on success, capture exceptions on failure

### Email Sending

| Operation    | Method                                  | Limit              |
| ------------ | --------------------------------------- | ------------------ |
| Single email | `resend.emails.send()`                  | 1 per call         |
| Batch emails | `resend.batch.send()`                   | Up to 100 per call |
| Broadcast    | `resend.broadcasts.create()` + `send()` | Audience-based     |

### Template Patterns

| Type                 | Use Case                            | Location                   |
| -------------------- | ----------------------------------- | -------------------------- |
| Inline HTML          | Simple confirmations, notifications | Private static methods     |
| React Email          | Complex newsletters, rich content   | `src/lib/email-templates/` |
| Resend API Templates | Variable-based templates            | Resend dashboard/API       |

### Error Handling

- Return `{ failedEmails, sentCount }` for bulk operations
- Return `boolean` for single operations
- Use `level: 'warning'` for non-critical failures
- Never fail entire operation for partial failures

### Broadcasts & Audiences

- Always include `{{{RESEND_UNSUBSCRIBE_URL}}}` in broadcasts
- Use variable syntax: `{{{VARIABLE|fallback}}}`
- Support scheduled sending via `scheduledAt` parameter

## Anti-Patterns to Avoid

1. **Never** include PII in Sentry context
2. **Never** skip circuit breaker protection
3. **Never** exceed 100 emails per batch call
4. **Never** hardcode email addresses
5. **Never** send broadcasts without unsubscribe link
6. **Never** use external CSS in email templates (inline only)
7. **Never** skip retry logic for email operations

## Usage Pattern Reference

| Use Case              | Method                          | Skills Needed                   |
| --------------------- | ------------------------------- | ------------------------------- |
| Waitlist confirmation | `sendWaitlistConfirmationAsync` | resend-email                    |
| Welcome email         | `sendNewsletterWelcomeAsync`    | resend-email                    |
| Bulk notifications    | `sendLaunchNotificationsAsync`  | resend-email                    |
| Newsletter broadcast  | `sendBroadcastAsync`            | resend-email, sentry-monitoring |
| React template email  | `sendWithTemplateAsync`         | resend-email                    |

## References

- `references/Resend-Email-Conventions.md` - Complete Resend email conventions
