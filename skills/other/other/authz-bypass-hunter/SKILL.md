---
name: authz-bypass-hunter
description: Hunt for authorization bypass vulnerabilities including IDOR, privilege escalation, missing access controls, broken object-level authorization. Use when auditing authentication/authorization code or API endpoints.
---

# Authorization Bypass Hunter

## Purpose

Systematically identify authorization vulnerabilities: IDOR, privilege escalation, broken access control, missing permission checks, role confusion, and horizontal/vertical privilege escalation.

## Focus Areas

- **IDOR (Insecure Direct Object References)**: User-controllable IDs accessing other users' data
- **Broken Object Level Authorization (BOLA)**: API endpoints not validating resource ownership
- **Broken Function Level Authorization (BFLA)**: Admin functions accessible to regular users
- **Missing Access Controls**: Endpoints without any authorization checks
- **Role/Permission Confusion**: Inconsistent role checks across code paths
- **JWT/Session Issues**: Token manipulation, session fixation

## Audit Checklist

### 1. Identify Authorization Entry Points
```
- API endpoints with resource IDs (/api/user/{id}, /api/order/{id})
- Query parameters (userId=, accountId=, orderId=)
- Request body fields controlling resource access
- File paths/names in requests
- GraphQL queries with object references
```

### 2. Check for Missing Checks
```
Look for patterns:
- Direct database queries without user filter
- Fetching resource by ID only (not ownership)
- Missing @authorize, @permission decorators
- Inconsistent middleware application
```

### 3. Verify Ownership Validation
```
VULNERABLE:
  order = Order.find(params[:id])  # No user check!

SECURE:
  order = current_user.orders.find(params[:id])  # Scoped to user
```

## Output Format

When you find authorization issues, report as:

```yaml
findings:
  - title: "IDOR in GET /api/users/{id}/profile"
    severity: high
    attack_scenario: "Authenticated user changes {id} parameter to access other users' profiles"
    preconditions: "Valid session required"
    reachability: auth_required
    impact: "Unauthorized access to PII of any user"
    confidence: high
    cwe_id: "CWE-639"
    affected_assets:
      - "/api/users/{id}/profile"
      - "src/controllers/user_controller.rs:42"
    taint_path: "request.params['id'] -> User.find(id) -> response"
```

## Key Patterns to Hunt

### Missing User Scope (Most Common)
```rust
// VULNERABLE - no ownership check
pub async fn get_order(id: i32) -> Order {
    Order::find(id).await
}

// SECURE - scoped to user
pub async fn get_order(user: User, id: i32) -> Order {
    Order::find_by_user(user.id, id).await
}
```

### Inconsistent Role Checks
```python
# VULNERABLE - role checked in UI but not API
@app.route('/admin/users')  # No @admin_required!
def list_users():
    return User.all()
```

### Parameter Pollution
```
# If both accepted, which wins?
GET /api/profile?userId=1001&userId=1000
```

### HTTP Method Bypass
```
GET /api/admin/users/1000 → 403 Forbidden
POST /api/admin/users/1000 → 200 OK  # Vulnerable!
```

## Severity Guidelines

| Pattern | Severity |
|---------|----------|
| IDOR to admin data | Critical |
| IDOR to PII | High |
| IDOR to non-sensitive data | Medium |
| Missing role check (admin functions) | Critical |
| Missing role check (user functions) | High |
| Horizontal privilege escalation | High |
| Vertical privilege escalation | Critical |

## KYCo Integration

Register authorization bypass findings using the kyco CLI:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Register Finding
```bash
kyco finding create \
  --title "IDOR in GET /api/users/{id}/profile" \
  --project PROJECT_ID \
  --severity high \
  --cwe CWE-639 \
  --attack-scenario "Authenticated user changes {id} parameter to access other users' profiles" \
  --impact "Unauthorized access to PII of any user" \
  --assets "/api/users/{id}/profile,src/controllers/user_controller.rs:42"
```

### 3. View in Kanban
```bash
kyco gui  # Opens GUI with Kanban board
kyco finding list --project PROJECT_ID  # CLI listing
```

### Common CWE IDs for Authorization Issues
- CWE-639: Authorization Bypass Through User-Controlled Key (IDOR)
- CWE-862: Missing Authorization
- CWE-863: Incorrect Authorization
- CWE-284: Improper Access Control
- CWE-285: Improper Authorization
