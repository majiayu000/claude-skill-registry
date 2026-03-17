---
name: access-control-rbac
description: Role-based access control (RBAC) with permissions and policies. Use for admin dashboards, enterprise access, multi-tenant apps, fine-grained authorization, or encountering permission hierarchies, role inheritance, policy conflicts.
---

# Access Control & RBAC

Implement secure access control systems with fine-grained permissions using RBAC, ABAC, or hybrid approaches.

## Access Control Models

| Model | Description | Best For |
|-------|-------------|----------|
| RBAC | Role-based - users assigned to roles with permissions | Most applications |
| ABAC | Attribute-based - policies evaluate user/resource attributes | Complex rules |
| MAC | Mandatory - system-enforced classification levels | Government/military |
| DAC | Discretionary - resource owners control access | File systems |
| ReBAC | Relationship-based - access via entity relationships | Social apps |

## Node.js RBAC Implementation

```javascript
class Permission {
  constructor(resource, action) {
    this.resource = resource;
    this.action = action;
  }

  matches(resource, action) {
    return (this.resource === '*' || this.resource === resource) &&
           (this.action === '*' || this.action === action);
  }
}

class Role {
  constructor(name, permissions = [], parent = null) {
    this.name = name;
    this.permissions = permissions;
    this.parent = parent;
  }

  hasPermission(resource, action) {
    if (this.permissions.some(p => p.matches(resource, action))) return true;
    return this.parent?.hasPermission(resource, action) ?? false;
  }
}

class RBACSystem {
  constructor() {
    this.roles = new Map();
    this.userRoles = new Map();
  }

  createRole(name, permissions = [], parentRole = null) {
    const parent = parentRole ? this.roles.get(parentRole) : null;
    this.roles.set(name, new Role(name, permissions, parent));
  }

  assignRole(userId, roleName) {
    const userRoles = this.userRoles.get(userId) || [];
    userRoles.push(this.roles.get(roleName));
    this.userRoles.set(userId, userRoles);
  }

  can(userId, resource, action) {
    const roles = this.userRoles.get(userId) || [];
    return roles.some(role => role.hasPermission(resource, action));
  }
}

// Express middleware
const requirePermission = (resource, action) => (req, res, next) => {
  if (!rbac.can(req.user.id, resource, action)) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
};

// Setup default roles
const rbac = new RBACSystem();
rbac.createRole('viewer', [new Permission('*', 'read')]);
rbac.createRole('editor', [new Permission('*', 'write')], 'viewer');
rbac.createRole('admin', [new Permission('*', '*')], 'editor');
```

## Python ABAC Pattern

```python
class Policy:
    def __init__(self, name, effect, resource, action, conditions):
        self.name = name
        self.effect = effect  # 'allow' or 'deny'
        self.resource = resource
        self.action = action
        self.conditions = conditions

    def matches(self, context):
        if self.resource != "*" and self.resource != context.get("resource"):
            return False
        if self.action != "*" and self.action != context.get("action"):
            return False
        return True

    def evaluate(self, context):
        return all(cond(context) for cond in self.conditions)


class ABACEngine:
    def __init__(self):
        self.policies = []

    def add_policy(self, policy):
        self.policies.append(policy)

    def check_access(self, context):
        for policy in self.policies:
            if policy.matches(context) and policy.evaluate(context):
                return policy.effect == 'allow'
        return False  # Deny by default


# Condition functions
def is_resource_owner(ctx):
    return ctx.get("user_id") == ctx.get("resource_owner_id")

def is_within_business_hours(ctx):
    from datetime import datetime
    return 9 <= datetime.now().hour < 18
```

See [references/python-abac.md](references/python-abac.md) for complete implementation with Flask integration.

## Java Spring Security

See [references/java-spring-security.md](references/java-spring-security.md) for enterprise implementation with:
- Spring Security configuration
- Method-level security with `@PreAuthorize`
- Custom permission service
- Custom security expressions

## Best Practices

**Do:**
- Apply least privilege principle
- Use role hierarchies to reduce duplication
- Audit all access changes
- Review permissions quarterly
- Cache permission checks for performance
- Separate authentication from authorization

**Don't:**
- Hardcode permission checks
- Allow permission creep without review
- Skip audit logging
- Use overly broad wildcards

## References

- [NIST RBAC Model](https://csrc.nist.gov/projects/role-based-access-control)
- [OWASP Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
