---
name: security-privileges
description: >
  Privilege system reference for the HMIS project. Use when adding new privileges,
  implementing access control, working with user roles, checking privilege-based
  rendering in XHTML, or auditing security controls.
user-invocable: true
---

# Privilege System Reference

## Core Principles

- **Declare privileges in `Privileges.java`** - append to enum without reordering
- **Check in controllers** via `webUserController.hasPrivilege(...)`
- **Assign through UI** via User Privileges admin interface; never seed in database
- **Name descriptively** so usage is obvious from enum value

## Common Privileges

| Privilege | Description |
|-----------|-------------|
| `StockTransactionViewRates` | Rate/value fields in stock transactions |
| `PharmacyTransferViewRates` | Rates in pharmacy transfer reports |
| `Developers` | All bill formats for dev/QA validation |

## Adding a New Privilege

1. Check `src/main/java/com/divudi/core/data/Privileges.java` - reuse existing if matching behavior exists
2. **Never rename or edit legacy enum values** (backward compatibility)
3. Add to most relevant section, keeping existing grouping
4. Update `src/main/webapp/admin/users/user_privileges.xhtml` for UI assignment
5. Extend `UserPrivilageController.createPrivilegeHolderTreeNodes()` for tree rendering

## Usage in XHTML

```xhtml
<p:column rendered="#{webUserController.hasPrivilege('PharmacyTransferViewRates')}">
    <h:outputText value="#{item.rate}" />
</p:column>
```

## Testing Checklist

- Log in WITHOUT the privilege - confirm UI element is hidden/disabled
- Log in WITH the privilege - verify workflow succeeds end-to-end
- Document new privilege in release notes

For complete reference, read [developer_docs/security/privilege-system.md](../../developer_docs/security/privilege-system.md).
