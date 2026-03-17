---
scope: universal
description: |
  Design consistent error codes following the PREFIX_CATEGORY_NUMBER format.
  Use when: defining error codes, creating error handling, designing APIs.
  Keywords: error code, error handling, error format, API errors, 錯誤碼, 錯誤處理.
---

# Error Code Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/error-code-guide/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2025-12-30
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [Error Code Standards](../../core/error-code-standards.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill helps design consistent error codes following the standard format, enabling better debugging, monitoring, and user experience.

## Quick Reference

### Error Code Format

```
<PREFIX>_<CATEGORY>_<NUMBER>
```

| Component | Description | Example |
|-----------|-------------|---------|
| PREFIX | Application/service identifier | AUTH, PAY, USR |
| CATEGORY | Error category | VAL, SYS, BIZ |
| NUMBER | Unique numeric identifier | 001, 100, 404 |

### Examples

```
AUTH_VAL_001    → Authentication validation error
PAY_SYS_503     → Payment system unavailable
USR_BIZ_100     → User business rule violation
API_NET_408     → API network timeout
```

### Error Categories

| Category | Full Name | Description | HTTP Status |
|----------|-----------|-------------|-------------|
| **VAL** | Validation | Client input validation failures | 400 |
| **BIZ** | Business | Business rule violations | 422 |
| **SYS** | System | Internal system failures | 500 |
| **NET** | Network | Communication failures | 502/503/504 |
| **AUTH** | Auth | Security-related errors | 401/403 |

### Category Code Ranges

| Range | Description | Example |
|-------|-------------|---------|
| *_VAL_001-099 | Field validation | Missing required field |
| *_VAL_100-199 | Format validation | Invalid email format |
| *_VAL_200-299 | Constraint validation | Password too short |
| *_BIZ_001-099 | State violations | Order already cancelled |
| *_BIZ_100-199 | Rule violations | Cannot return after 30 days |
| *_BIZ_200-299 | Limit violations | Daily limit exceeded |
| *_AUTH_001-099 | Authentication | Invalid credentials |
| *_AUTH_100-199 | Authorization | Insufficient permissions |
| *_AUTH_200-299 | Token/session | Token expired |

## HTTP Status Code Mapping

| Category | HTTP Status | Description |
|----------|-------------|-------------|
| VAL | 400 | Bad Request |
| BIZ | 422 | Unprocessable Entity |
| AUTH (001-099) | 401 | Unauthorized |
| AUTH (100-199) | 403 | Forbidden |
| SYS | 500 | Internal Server Error |
| NET | 502/503/504 | Gateway errors |

## Detailed Guidelines

For complete standards, see:
- [Error Code Standards](../../core/error-code-standards.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/error-codes.ai.yaml`

## Error Response Format

### Single Error

```json
{
  "success": false,
  "error": {
    "code": "AUTH_VAL_001",
    "message": "Email is required",
    "field": "email",
    "requestId": "req_abc123"
  }
}
```

### Multiple Errors

```json
{
  "success": false,
  "errors": [
    {
      "code": "AUTH_VAL_001",
      "message": "Email is required",
      "field": "email"
    },
    {
      "code": "AUTH_VAL_201",
      "message": "Password must be at least 8 characters",
      "field": "password"
    }
  ],
  "requestId": "req_abc123"
}
```

## Internal Error Object

```typescript
interface ApplicationError {
  // Core fields
  code: string;          // "AUTH_VAL_001"
  message: string;       // Technical message for logs

  // User-facing
  userMessage: string;   // Localized user message
  userMessageKey: string; // i18n key: "error.auth.val.001"

  // Context
  field?: string;        // Affected field: "email"
  details?: object;      // Additional context

  // Debugging
  timestamp: string;     // ISO 8601
  requestId: string;     // Correlation ID
}
```

## Internationalization (i18n)

### Message Key Format

```
error.<prefix>.<category>.<number>
```

### Example Translation Files

```yaml
# en.yaml
error:
  auth:
    val:
      001: "Email is required"
      101: "Invalid email format"
    auth:
      001: "Invalid credentials"

# zh-TW.yaml
error:
  auth:
    val:
      001: "電子郵件為必填欄位"
      101: "電子郵件格式無效"
    auth:
      001: "帳號或密碼錯誤"
```

## Examples

### ✅ Good Error Codes

```javascript
AUTH_VAL_001  // Missing required field: email
AUTH_VAL_101  // Invalid email format
ORDER_BIZ_001 // Order already cancelled
ORDER_BIZ_201 // Daily purchase limit exceeded
DB_SYS_001    // Database query failed
SEC_AUTH_001  // Invalid credentials
SEC_AUTH_201  // Token expired
```

### ❌ Bad Error Codes

```javascript
ERR_001       // Too vague, no prefix or category
INVALID       // Not descriptive
error         // Not a code
AUTH_ERROR    // Missing number
```

## Checklist

- [ ] Unique code for each error
- [ ] Category matches error type
- [ ] User message is localized
- [ ] HTTP status is correct
- [ ] Error is documented
- [ ] Code is in registry

---

## Configuration Detection

This skill supports project-specific configuration.

### Detection Order

1. Check for existing error code patterns in codebase
2. Check `CONTRIBUTING.md` for error code guidelines
3. If not found, **default to PREFIX_CATEGORY_NUMBER format**

### First-Time Setup

If no error code standard found:

1. Suggest: "This project hasn't configured error code standards. Would you like to set up an error code registry?"
2. Suggest creating `errors/registry.ts`:

```typescript
export const ErrorCodes = {
  AUTH_VAL_001: {
    code: 'AUTH_VAL_001',
    httpStatus: 400,
    messageKey: 'error.auth.val.001',
    description: 'Email field is required',
  },
  // ... more codes
} as const;
```

---

## Related Standards

- [Error Code Standards](../../core/error-code-standards.md)
- [Logging Standards](../../core/logging-standards.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-30 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
