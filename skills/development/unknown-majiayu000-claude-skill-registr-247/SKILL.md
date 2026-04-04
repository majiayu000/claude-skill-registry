---
name: audit-logging
description: Implement comprehensive audit logging for all admin actions, capturing user ID, action type, entity changes, IP address, and user agent. Use when tracking system activities or adding audit trails.
allowed-tools: Read, Write, Edit, Bash, Glob
---

You implement audit logging for all administrative actions in the QA Team Portal.

## Requirements from PROJECT_PLAN.md

- Log all create, update, delete operations
- Capture user ID, timestamp, IP, user agent
- Display audit trail in admin panel
- Export logs to CSV
- Retention policy: 1 year minimum

## Implementation

### 1. Audit Log Model

**Location:** `backend/app/models/audit_log.py`

```python
from sqlalchemy import Column, String, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # create, update, delete, login
    entity_type = Column(String(50), nullable=False)  # team_member, tool, etc.
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    old_values = Column(JSON, nullable=True)  # Before update/delete
    new_values = Column(JSON, nullable=True)  # After create/update
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

### 2. Audit Service

**Location:** `backend/app/services/audit_service.py`

```python
from fastapi import Request
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.models.user import User

class AuditService:
    """Service for logging admin activities."""

    @staticmethod
    async def log_action(
        db: Session,
        user: User,
        action: str,
        entity_type: str,
        entity_id: str = None,
        old_values: dict = None,
        new_values: dict = None,
        request: Request = None
    ):
        """
        Log an audit event.

        Args:
            db: Database session
            user: Current user
            action: Action type (create, update, delete, login)
            entity_type: Type of entity (team_member, tool, etc.)
            entity_id: ID of entity
            old_values: Values before change
            new_values: Values after change
            request: FastAPI request object
        """
        ip_address = None
        user_agent = None

        if request:
            # Get real IP (behind proxy)
            ip_address = request.headers.get(
                "X-Forwarded-For",
                request.client.host
            ).split(',')[0].strip()

            user_agent = request.headers.get("User-Agent")

        audit_log = AuditLog(
            user_id=user.id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.add(audit_log)
        db.commit()

        return audit_log
```

### 3. Audit Middleware

**Location:** `backend/app/middleware/audit_middleware.py`

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.services.audit_service import AuditService

class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically log admin actions."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Only log successful admin operations
        if (
            response.status_code < 400 and
            request.url.path.startswith("/api/v1/admin/") and
            request.method in ["POST", "PUT", "PATCH", "DELETE"]
        ):
            # Audit logging handled in endpoints
            # This middleware can be used for additional logging
            pass

        return response
```

### 4. Usage in Endpoints

**Location:** `backend/app/api/v1/endpoints/team_members.py`

```python
from app.services.audit_service import AuditService

@router.post("/admin/team-members")
async def create_team_member(
    data: TeamMemberCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_lead_or_admin)
):
    """Create team member with audit logging."""
    # Create team member
    team_member = await crud.team_member.create(db, obj_in=data)

    # Log action
    await AuditService.log_action(
        db=db,
        user=current_user,
        action="create",
        entity_type="team_member",
        entity_id=str(team_member.id),
        new_values=data.dict(),
        request=request
    )

    return team_member

@router.put("/admin/team-members/{id}")
async def update_team_member(
    id: UUID,
    data: TeamMemberUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_lead_or_admin)
):
    """Update team member with audit logging."""
    # Get old values
    old_member = await crud.team_member.get(db, id=id)
    old_values = TeamMemberResponse.from_orm(old_member).dict()

    # Update team member
    updated_member = await crud.team_member.update(
        db,
        db_obj=old_member,
        obj_in=data
    )

    # Log action
    await AuditService.log_action(
        db=db,
        user=current_user,
        action="update",
        entity_type="team_member",
        entity_id=str(id),
        old_values=old_values,
        new_values=data.dict(exclude_unset=True),
        request=request
    )

    return updated_member

@router.delete("/admin/team-members/{id}")
async def delete_team_member(
    id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete team member with audit logging."""
    # Get old values before deletion
    team_member = await crud.team_member.get(db, id=id)
    old_values = TeamMemberResponse.from_orm(team_member).dict()

    # Delete
    await crud.team_member.remove(db, id=id)

    # Log action
    await AuditService.log_action(
        db=db,
        user=current_user,
        action="delete",
        entity_type="team_member",
        entity_id=str(id),
        old_values=old_values,
        request=request
    )

    return {"message": "Deleted successfully"}
```

### 5. Audit Log API

**Location:** `backend/app/api/v1/endpoints/audit_logs.py`

```python
@router.get("/admin/audit-logs")
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    action: str = None,
    entity_type: str = None,
    user_id: UUID = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_lead_or_admin)
):
    """Get audit logs with filters."""
    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if start_date:
        query = query.filter(AuditLog.created_at >= start_date)
    if end_date:
        query = query.filter(AuditLog.created_at <= end_date)

    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

    return logs

@router.get("/admin/audit-logs/export")
async def export_audit_logs_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Export audit logs to CSV."""
    import csv
    from io import StringIO

    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()

    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'Timestamp', 'User', 'Action', 'Entity Type',
        'Entity ID', 'IP Address', 'User Agent'
    ])

    # Data
    for log in logs:
        writer.writerow([
            log.created_at.isoformat(),
            log.user_id,
            log.action,
            log.entity_type,
            log.entity_id or '',
            log.ip_address or '',
            log.user_agent or ''
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=audit_logs.csv"}
    )
```

### 6. Frontend Audit Log Viewer

**Location:** `frontend/src/components/admin/audit/AuditLogs.tsx`

```typescript
export const AuditLogs = () => {
  const [logs, setLogs] = useState([])
  const [filters, setFilters] = useState({
    action: '',
    entity_type: '',
    start_date: '',
    end_date: ''
  })

  useEffect(() => {
    fetchLogs()
  }, [filters])

  const fetchLogs = async () => {
    const response = await api.get('/admin/audit-logs', { params: filters })
    setLogs(response.data)
  }

  const exportCSV = () => {
    window.open('/api/v1/admin/audit-logs/export', '_blank')
  }

  return (
    <div>
      <div className="flex justify-between mb-4">
        <h1>Audit Logs</h1>
        <Button onClick={exportCSV}>Export CSV</Button>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-4 gap-4 mb-4">
        <Select value={filters.action} onValueChange={...}>
          <option value="">All Actions</option>
          <option value="create">Create</option>
          <option value="update">Update</option>
          <option value="delete">Delete</option>
        </Select>

        {/* More filters */}
      </div>

      {/* Table */}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Timestamp</TableHead>
            <TableHead>User</TableHead>
            <TableHead>Action</TableHead>
            <TableHead>Entity</TableHead>
            <TableHead>IP Address</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {logs.map(log => (
            <TableRow key={log.id}>
              <TableCell>{formatDate(log.created_at)}</TableCell>
              <TableCell>{log.user_email}</TableCell>
              <TableCell>
                <Badge variant={getActionVariant(log.action)}>
                  {log.action}
                </Badge>
              </TableCell>
              <TableCell>{log.entity_type}</TableCell>
              <TableCell>{log.ip_address}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

## Cleanup Policy

**Location:** `backend/scripts/cleanup_audit_logs.py`

```python
# Run this as a cron job to enforce retention policy
from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.models.audit_log import AuditLog

def cleanup_old_logs(days: int = 365):
    """Delete audit logs older than specified days."""
    db = SessionLocal()
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    deleted = db.query(AuditLog).filter(
        AuditLog.created_at < cutoff_date
    ).delete()

    db.commit()
    print(f"Deleted {deleted} old audit logs")

if __name__ == "__main__":
    cleanup_old_logs(365)  # 1 year retention
```

## Testing

```python
def test_audit_log_created_on_create(client, admin_token, db):
    response = client.post(
        "/api/v1/admin/team-members",
        json={"name": "Test", "role": "QA Engineer"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201

    # Check audit log created
    audit_log = db.query(AuditLog).filter(
        AuditLog.action == "create",
        AuditLog.entity_type == "team_member"
    ).first()

    assert audit_log is not None
    assert audit_log.new_values["name"] == "Test"
```

## Report

✅ Audit logging implemented
✅ All CRUD operations logged
✅ IP address and user agent captured
✅ Audit log viewer created
✅ CSV export functional
✅ Retention policy defined (1 year)
✅ Tests passing
