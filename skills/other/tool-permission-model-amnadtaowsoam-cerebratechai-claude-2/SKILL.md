---
name: Tool Permission Model
description: Comprehensive guide to implementing permission systems for AI agent tools including RBAC, approval workflows, and security policies
---

# Tool Permission Model

## Why Tool Permissions?

**Problem:** Agents can use powerful tools - need access control

### Risks Without Permissions
```
Agent deletes production database
Agent sends emails to all customers
Agent accesses sensitive data
Agent makes unauthorized purchases
```

### With Permissions
```
Agent can only use approved tools
Sensitive tools require approval
Actions are logged and auditable
Users control what agent can do
```

---

## Permission Models

### Role-Based Access Control (RBAC)
```
User has role → Role has permissions → Agent inherits permissions

Example:
- Admin role: Can use all tools
- User role: Can use read-only tools
- Guest role: Can use search tools only
```

### Attribute-Based Access Control (ABAC)
```
Permissions based on attributes:
- User attributes (department, level)
- Resource attributes (sensitivity, owner)
- Environment attributes (time, location)

Example:
- Finance department can use payment tools
- During business hours only
- For amounts < $1000
```

### Capability-Based Access Control
```
User grants specific capabilities to agent

Example:
- "You can search my emails"
- "You can book meetings on my calendar"
- "You cannot delete anything"
```

---

## Implementation

### Basic RBAC
```python
class ToolPermissions:
    def __init__(self):
        self.roles = {
            "admin": ["*"],  # All tools
            "user": ["search_web", "get_weather", "calculate"],
            "guest": ["search_web"]
        }
    
    def can_use_tool(self, user_role, tool_name):
        """Check if role has permission for tool"""
        allowed_tools = self.roles.get(user_role, [])
        
        # Check wildcard
        if "*" in allowed_tools:
            return True
        
        # Check specific tool
        return tool_name in allowed_tools

# Usage
permissions = ToolPermissions()

if permissions.can_use_tool(user_role="user", tool_name="search_web"):
    result = search_web(query)
else:
    raise PermissionError("Not allowed to use search_web")
```

### Database-Backed Permissions
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE tools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    risk_level VARCHAR(20)  -- low, medium, high, critical
);

CREATE TABLE role_tool_permissions (
    role_id INT REFERENCES roles(id),
    tool_id INT REFERENCES tools(id),
    can_use BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (role_id, tool_id)
);

CREATE TABLE user_roles (
    user_id VARCHAR(100),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

```python
def can_use_tool(user_id, tool_name):
    """Check if user has permission for tool"""
    result = db.query_one("""
        SELECT rtp.can_use, rtp.requires_approval
        FROM user_roles ur
        JOIN role_tool_permissions rtp ON ur.role_id = rtp.role_id
        JOIN tools t ON rtp.tool_id = t.id
        WHERE ur.user_id = %s AND t.name = %s
    """, (user_id, tool_name))
    
    if not result:
        return False, False
    
    return result["can_use"], result["requires_approval"]
```

---

## Tool Risk Levels

### Classify Tools by Risk
```python
TOOL_RISK_LEVELS = {
    # Low risk (read-only)
    "search_web": "low",
    "get_weather": "low",
    "calculate": "low",
    
    # Medium risk (write, non-destructive)
    "send_email": "medium",
    "create_calendar_event": "medium",
    
    # High risk (destructive)
    "delete_file": "high",
    "update_database": "high",
    
    # Critical risk (financial, security)
    "make_payment": "critical",
    "grant_access": "critical"
}
```

### Require Approval for High-Risk Tools
```python
def execute_tool_with_approval(user_id, tool_name, params):
    """Execute tool, requesting approval if needed"""
    risk_level = TOOL_RISK_LEVELS.get(tool_name, "medium")
    
    if risk_level in ["high", "critical"]:
        # Request approval
        approval_id = request_approval(
            user_id=user_id,
            tool_name=tool_name,
            params=params,
            risk_level=risk_level
        )
        
        # Wait for approval (or timeout)
        approved = wait_for_approval(approval_id, timeout_seconds=300)
        
        if not approved:
            raise PermissionError("Approval denied or timeout")
    
    # Execute tool
    return execute_tool(tool_name, params)
```

---

## Approval Workflows

### Request Approval
```python
def request_approval(user_id, tool_name, params, risk_level):
    """Request approval for tool execution"""
    approval_id = generate_id()
    
    # Store approval request
    db.execute("""
        INSERT INTO approval_requests
        (id, user_id, tool_name, params, risk_level, status, created_at)
        VALUES (%s, %s, %s, %s, %s, 'pending', NOW())
    """, (approval_id, user_id, tool_name, json.dumps(params), risk_level))
    
    # Notify user
    send_notification(
        user_id=user_id,
        title="Agent Approval Required",
        message=f"Agent wants to use {tool_name}. Approve?",
        actions=[
            {"label": "Approve", "action": f"approve:{approval_id}"},
            {"label": "Deny", "action": f"deny:{approval_id}"}
        ]
    )
    
    return approval_id
```

### Approve/Deny
```python
def approve_request(approval_id, user_id):
    """Approve tool execution"""
    db.execute("""
        UPDATE approval_requests
        SET status = 'approved', approved_by = %s, approved_at = NOW()
        WHERE id = %s
    """, (user_id, approval_id))
    
    log_event(f"User {user_id} approved {approval_id}")

def deny_request(approval_id, user_id, reason=None):
    """Deny tool execution"""
    db.execute("""
        UPDATE approval_requests
        SET status = 'denied', denied_by = %s, denied_at = NOW(), denial_reason = %s
        WHERE id = %s
    """, (user_id, approval_id, reason))
    
    log_event(f"User {user_id} denied {approval_id}: {reason}")
```

### Wait for Approval
```python
import time

def wait_for_approval(approval_id, timeout_seconds=300):
    """Wait for approval (or timeout)"""
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        status = db.query_one("""
            SELECT status FROM approval_requests WHERE id = %s
        """, (approval_id,))
        
        if status["status"] == "approved":
            return True
        
        if status["status"] == "denied":
            return False
        
        time.sleep(5)  # Check every 5 seconds
    
    # Timeout
    db.execute("""
        UPDATE approval_requests
        SET status = 'timeout'
        WHERE id = %s
    """, (approval_id,))
    
    return False
```

---

## Scoped Permissions

### Time-Based Permissions
```python
def can_use_tool_at_time(user_id, tool_name, current_time):
    """Check if user can use tool at current time"""
    permissions = db.query_one("""
        SELECT allowed_hours_start, allowed_hours_end
        FROM tool_permissions
        WHERE user_id = %s AND tool_name = %s
    """, (user_id, tool_name))
    
    if not permissions:
        return False
    
    current_hour = current_time.hour
    start_hour = permissions["allowed_hours_start"]
    end_hour = permissions["allowed_hours_end"]
    
    return start_hour <= current_hour < end_hour

# Example: Only allow during business hours (9 AM - 5 PM)
```

### Resource-Based Permissions
```python
def can_access_resource(user_id, resource_id):
    """Check if user can access specific resource"""
    # Check ownership
    resource = db.query_one("""
        SELECT owner_id FROM resources WHERE id = %s
    """, (resource_id,))
    
    if resource["owner_id"] == user_id:
        return True
    
    # Check shared access
    shared = db.query_one("""
        SELECT * FROM resource_shares
        WHERE resource_id = %s AND user_id = %s
    """, (resource_id, user_id))
    
    return shared is not None
```

### Budget-Based Permissions
```python
def can_make_payment(user_id, amount):
    """Check if user can make payment of given amount"""
    # Check user's spending limit
    limit = db.query_one("""
        SELECT daily_spending_limit FROM user_limits
        WHERE user_id = %s
    """, (user_id,))
    
    # Check today's spending
    spent_today = db.query_one("""
        SELECT COALESCE(SUM(amount), 0) as total
        FROM payments
        WHERE user_id = %s AND DATE(created_at) = CURRENT_DATE
    """, (user_id,))
    
    remaining = limit["daily_spending_limit"] - spent_today["total"]
    
    return amount <= remaining
```

---

## Delegation

### Delegate Permissions
```python
def delegate_permission(from_user_id, to_user_id, tool_name, expires_at=None):
    """Delegate permission to another user"""
    db.execute("""
        INSERT INTO delegated_permissions
        (from_user_id, to_user_id, tool_name, expires_at, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (from_user_id, to_user_id, tool_name, expires_at))
    
    log_event(f"User {from_user_id} delegated {tool_name} to {to_user_id}")

# Example: Manager delegates approval to assistant
delegate_permission(
    from_user_id="manager@example.com",
    to_user_id="assistant@example.com",
    tool_name="approve_expense",
    expires_at=datetime.now() + timedelta(days=7)
)
```

---

## Audit Trail

### Log Tool Usage
```python
def log_tool_usage(user_id, tool_name, params, result, approved_by=None):
    """Log tool usage for audit"""
    db.execute("""
        INSERT INTO tool_usage_log
        (user_id, tool_name, params, result, approved_by, timestamp)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """, (user_id, tool_name, json.dumps(params), json.dumps(result), approved_by))
```

### Query Audit Trail
```python
def get_tool_usage_history(user_id, start_date, end_date):
    """Get tool usage history for user"""
    return db.query("""
        SELECT tool_name, params, result, approved_by, timestamp
        FROM tool_usage_log
        WHERE user_id = %s
          AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp DESC
    """, (user_id, start_date, end_date))
```

---

## Best Practices

### 1. Principle of Least Privilege
```python
# Good: Only grant necessary permissions
user_permissions = ["search_web", "get_weather"]

# Bad: Grant all permissions
user_permissions = ["*"]
```

### 2. Require Approval for High-Risk Tools
```python
# Good
if TOOL_RISK_LEVELS[tool_name] == "critical":
    require_approval()

# Bad
# No approval for critical tools
```

### 3. Set Expiration on Delegations
```python
# Good
delegate_permission(from_user, to_user, tool, expires_at=now + timedelta(days=7))

# Bad
delegate_permission(from_user, to_user, tool)  # Never expires
```

### 4. Log Everything
```python
# Good
log_tool_usage(user_id, tool_name, params, result)

# Bad
# No logging
```

### 5. Regular Permission Audits
```python
# Review permissions quarterly
def audit_permissions():
    # Find users with excessive permissions
    # Find unused permissions
    # Find expired delegations
    pass
```

---

## Summary

**Tool Permissions:** Control what agents can do

**Permission Models:**
- RBAC (role-based)
- ABAC (attribute-based)
- Capability-based

**Risk Levels:**
- Low (read-only)
- Medium (write, non-destructive)
- High (destructive)
- Critical (financial, security)

**Approval Workflows:**
- Request approval
- Notify user
- Wait for approval
- Execute or deny

**Scoped Permissions:**
- Time-based (business hours)
- Resource-based (ownership)
- Budget-based (spending limits)

**Delegation:**
- Delegate permissions
- Set expiration
- Log delegation

**Audit Trail:**
- Log all tool usage
- Track approvals
- Query history

**Best Practices:**
- Least privilege
- Require approval for high-risk
- Set expiration
- Log everything
- Regular audits
