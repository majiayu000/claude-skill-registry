---
name: access-control
description: Design RBAC/ABAC models, Principle of Least Privilege, Identity Management.
role: ops-security, eng-backend
triggers:
  - rbac
  - abac
  - authz
  - iam
  - permission
  - role
  - least privilege
---

# access-control Skill

Identity is the new perimeter. Authorization must be strict, consistent, and auditable.

## 1. Models
- **RBAC (Role-Based)**: `Admin`, `Editor`, `Viewer`. Simple, coarse-grained.
- **ABAC (Attribute-Based)**: `CanEdit if user.dept == doc.dept AND time < 5pm`. Flexible, complex.
- **ReBAC (Relationship-Based)**: `CanView if user is friend_of document.owner`. (Graph-based, e.g., Zanzibar).

## 2. Best Practices
- **Least Privilege**: Start with `Deny All`. Explicitly `Allow` specific actions.
- **Decoupling**: Decouple logic (`if user.isAdmin`) from policy (`can(user, 'delete:report')`). Use libraries like CASL or Oso.
- **No Hardcoded IDs**: Never checks `if (user.id === '123')`.

## 3. Infrastructure IAM
- **Service Accounts**: Separate identity for apps/machines. Rotate keys automatically.
- **Short-Lived Credentials**: Use OIDC/STS (AssumeRole) instead of long-lived access keys.

## 4. Audit
- **Log Decisions**: "User X tried to do Action Y on Resource Z -> Result: DENIED".
- **Review**: Quarterly review of `Admin` group membership.
