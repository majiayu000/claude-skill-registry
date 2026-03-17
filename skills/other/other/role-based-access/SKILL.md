---
name: role-based-access
description: Implement role-based access control (RBAC) with user roles (admin, lead, member) and permission middleware. Use when adding authorization or restricting endpoints by role.
allowed-tools: Read, Write, Edit, Glob
---

You implement RBAC for the QA Team Portal with three roles: admin, lead, and member.

## Roles & Permissions

**admin** - Full access to everything
- All CRUD operations
- User management
- System configuration

**lead** - Content management
- Create/Edit/Delete content (team, updates, tools, resources, research)
- View audit logs
- Cannot manage users

**member** - Read-only
- View public pages only
- No admin portal access

## Implementation

### 1. Permission Decorator

**Location:** `backend/app/core/permissions.py`

```python
from functools import wraps
from fastapi import HTTPException
from app.models.user import User

def require_role(*allowed_roles: str):
    """
    Decorator to require specific roles.

    Usage:
        @require_role("admin", "lead")
        async def update_team_member(...):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, **kwargs):
            if not current_user:
                raise HTTPException(401, "Authentication required")

            if current_user.role not in allowed_roles:
                raise HTTPException(
                    403,
                    f"Requires role: {' or '.join(allowed_roles)}"
                )

            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
```

### 2. Permission Dependencies

**Location:** `backend/app/api/deps.py`

```python
async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Require admin role."""
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access required")
    return current_user

async def get_current_lead_or_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Require lead or admin role."""
    if current_user.role not in ["admin", "lead"]:
        raise HTTPException(403, "Lead or admin access required")
    return current_user
```

### 3. Apply to Endpoints

**Location:** `backend/app/api/v1/endpoints/team_members.py`

```python
from app.api.deps import get_current_user, get_current_lead_or_admin

@router.get("/team-members")
async def get_team_members():
    """Public endpoint - no auth required."""
    ...

@router.post("/admin/team-members")
async def create_team_member(
    data: TeamMemberCreate,
    current_user: User = Depends(get_current_lead_or_admin)
):
    """Lead or admin can create team members."""
    ...

@router.delete("/admin/team-members/{id}")
async def delete_team_member(
    id: UUID,
    current_user: User = Depends(get_current_admin)
):
    """Only admin can delete."""
    ...
```

### 4. Resource-Level Permissions

```python
# Check if user can modify specific resource
async def can_modify_resource(
    user: User,
    resource_id: UUID,
    db: Session
) -> bool:
    """Check if user can modify resource."""
    if user.role == "admin":
        return True  # Admin can modify anything

    # Lead can only modify their own resources
    if user.role == "lead":
        resource = await crud.resource.get(db, id=resource_id)
        return resource and resource.created_by == user.id

    return False  # Members cannot modify
```

## Frontend Authorization

**Location:** `frontend/src/hooks/useAuth.ts`

```typescript
export const useAuth = () => {
  const { user } = useContext(AuthContext)

  const hasRole = (...roles: string[]) => {
    return user && roles.includes(user.role)
  }

  const isAdmin = () => hasRole('admin')
  const isLead = () => hasRole('lead', 'admin')
  const isMember = () => hasRole('member', 'lead', 'admin')

  return {
    user,
    hasRole,
    isAdmin,
    isLead,
    isMember
  }
}
```

**Usage in Components:**

```typescript
const { isAdmin, isLead } = useAuth()

return (
  <div>
    {isLead() && (
      <Button onClick={handleEdit}>Edit</Button>
    )}

    {isAdmin() && (
      <Button onClick={handleDelete}>Delete</Button>
    )}
  </div>
)
```

## Testing

```python
def test_admin_can_delete(client, admin_token):
    response = client.delete(
        "/api/v1/admin/team-members/123",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

def test_lead_cannot_delete(client, lead_token):
    response = client.delete(
        "/api/v1/admin/team-members/123",
        headers={"Authorization": f"Bearer {lead_token}"}
    )
    assert response.status_code == 403

def test_member_cannot_access_admin(client, member_token):
    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {member_token}"}
    )
    assert response.status_code == 403
```

## Report

✅ RBAC implemented with 3 roles
✅ Permission middleware created
✅ Endpoints protected by role
✅ Frontend authorization hooks added
✅ Tests passing
