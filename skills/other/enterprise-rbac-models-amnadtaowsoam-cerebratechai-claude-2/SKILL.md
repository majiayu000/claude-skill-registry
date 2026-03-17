---
name: Enterprise RBAC Models
description: Comprehensive guide to implementing Role-Based Access Control for enterprise applications with hierarchical roles, custom permissions, and multi-level access
---

# Enterprise RBAC Models

## What is RBAC?

**Role-Based Access Control (RBAC):** Users → Roles → Permissions

### Model
```
Users: John, Jane, Bob
Roles: Admin, Manager, Member, Viewer
Permissions: create_project, delete_user, view_reports

John → Admin → {create_project, delete_user, view_reports, ...}
Jane → Manager → {create_project, view_reports}
Bob → Viewer → {view_reports}
```

### vs ACL (Access Control List)

**ACL:** Direct user permissions
```
John can create_project
John can delete_user
John can view_reports
(Doesn't scale!)
```

**RBAC:** Role-based permissions
```
John is Admin
Admin can create_project, delete_user, view_reports
(Scalable!)
```

### vs ABAC (Attribute-Based Access Control)

**ABAC:** Policy-based decisions
```
IF user.department == "Engineering" AND resource.sensitivity == "low"
THEN allow access
```

**When to Use:**
- **RBAC:** Most applications (simple, scalable)
- **ACL:** Very simple apps (few users, few permissions)
- **ABAC:** Complex policies (government, healthcare)

---

## Why Enterprises Need RBAC

### 1. Scalable

**Without RBAC:**
```
New employee joins
→ Assign 50 individual permissions manually
→ Error-prone, time-consuming
```

**With RBAC:**
```
New employee joins
→ Assign "Member" role
→ Automatically gets all member permissions
```

### 2. Auditable

**Questions:**
- Who has admin access?
- What can this user do?
- When did they get this permission?

**RBAC Provides:**
- List all users with "Admin" role
- List all permissions for "Manager" role
- Audit log of role assignments

### 3. Least Privilege Principle

**Principle:** Users should have minimum permissions needed

**RBAC Enforces:**
- Default role: Viewer (read-only)
- Promote to Member (can edit own)
- Promote to Manager (can edit all)
- Promote to Admin (full control)

### 4. Segregation of Duties

**Principle:** No single user should have too much power

**Example:**
- User can create invoice (Member)
- Different user must approve invoice (Manager)
- Prevents fraud

---

## RBAC Components

### 1. Users

**Definition:** People or service accounts

**Examples:**
- john.doe@example.com (person)
- api-service@example.com (service account)
- github-bot@example.com (bot)

### 2. Roles

**Definition:** Named collection of permissions

**Examples:**
- Admin (full control)
- Manager (create, edit, delete)
- Member (create, edit own)
- Viewer (read-only)

### 3. Permissions

**Definition:** Specific actions on resources

**Format:** `resource:action`

**Examples:**
- `project:create`
- `user:delete`
- `report:view`
- `billing:manage`

### 4. Resources

**Definition:** Things users act on

**Examples:**
- Projects
- Files
- Reports
- Users
- Settings

---

## Common Enterprise Roles

### Owner/Admin

**Permissions:** Full control
```
- project:*
- user:*
- billing:*
- settings:*
```

**Use Case:** Founder, CTO, IT admin

### Manager/Editor

**Permissions:** Create, edit, delete (but not billing/settings)
```
- project:create
- project:edit
- project:delete
- user:invite
- report:view
```

**Use Case:** Team lead, project manager

### Member/Contributor

**Permissions:** Create, edit own
```
- project:create
- project:edit_own
- file:upload
- report:view
```

**Use Case:** Engineer, designer, analyst

### Viewer/Reader

**Permissions:** Read-only
```
- project:view
- file:view
- report:view
```

**Use Case:** Stakeholder, auditor, contractor

### Billing Admin

**Permissions:** Manage billing only
```
- billing:view
- billing:manage
- invoice:download
```

**Use Case:** Finance team

### Support

**Permissions:** Limited access for support
```
- user:view
- project:view
- logs:view
```

**Use Case:** Customer support team

---

## Permission Naming Conventions

### Format 1: resource:action

```
project:create
project:edit
project:delete
project:view

user:create
user:edit
user:delete
user:view
```

**Pros:** Clear, consistent, easy to parse

### Format 2: action_resource

```
create_project
edit_project
delete_project
view_project
```

**Pros:** Reads like English

**Recommendation:** Use `resource:action` (more common)

### Wildcard Permissions

```
project:*        (all project permissions)
*:view           (view all resources)
*:*              (all permissions, superuser)
```

---

## Hierarchical Roles

### Inheritance

**Model:**
```
Admin inherits all permissions of Manager
Manager inherits all permissions of Member
Member inherits all permissions of Viewer
```

**Example:**
```
Viewer:
- project:view
- file:view

Member (inherits Viewer):
- project:view
- file:view
- project:create
- file:upload

Manager (inherits Member):
- project:view
- file:view
- project:create
- file:upload
- project:delete
- user:invite

Admin (inherits Manager):
- project:view
- file:view
- project:create
- file:upload
- project:delete
- user:invite
- user:delete
- billing:manage
- settings:*
```

### Implementation

```javascript
const roleHierarchy = {
  viewer: [],
  member: ['viewer'],
  manager: ['member'],
  admin: ['manager']
};

function getAllPermissions(role) {
  const permissions = new Set(rolePermissions[role]);
  
  // Add inherited permissions
  for (const parentRole of roleHierarchy[role]) {
    const parentPerms = getAllPermissions(parentRole);
    parentPerms.forEach(p => permissions.add(p));
  }
  
  return Array.from(permissions);
}
```

---

## Custom Roles (Enterprise Feature)

### What Are Custom Roles?

**Definition:** Customer defines their own roles with specific permissions

**Example:**
```
Customer creates "Auditor" role:
- project:view
- file:view
- logs:view
- report:export
(Read-only + export)
```

### Database Schema

```sql
CREATE TABLE custom_roles (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE custom_role_permissions (
  role_id UUID REFERENCES custom_roles(id),
  permission VARCHAR(255) NOT NULL,
  PRIMARY KEY (role_id, permission)
);
```

### Implementation

```javascript
// Create custom role
app.post('/api/roles', async (req, res) => {
  const { name, description, permissions } = req.body;
  
  const role = await db.customRoles.create({
    tenantId: req.user.tenantId,
    name,
    description
  });
  
  for (const permission of permissions) {
    await db.customRolePermissions.create({
      roleId: role.id,
      permission
    });
  }
  
  res.json(role);
});

// Assign custom role to user
app.post('/api/users/:userId/roles', async (req, res) => {
  const { roleId } = req.body;
  
  await db.userRoles.create({
    userId: req.params.userId,
    roleId
  });
  
  res.json({ success: true });
});
```

---

## Multi-Level RBAC

### Organization Level

**Scope:** Entire organization

**Roles:**
- Org Owner (full control over org)
- Org Admin (manage users, billing)
- Org Member (access to all projects)

### Project/Workspace Level

**Scope:** Specific project or workspace

**Roles:**
- Project Admin (full control over project)
- Project Member (can edit project)
- Project Viewer (can view project)

### Resource Level

**Scope:** Specific resource (document, file)

**Roles:**
- Document Owner (full control over document)
- Document Editor (can edit document)
- Document Viewer (can view document)

### Example

```
John is:
- Org Member (organization level)
- Project Admin in "Website Redesign" (project level)
- Document Owner of "Design Spec" (resource level)

Permissions:
- Can view all org projects (org member)
- Can manage "Website Redesign" project (project admin)
- Can delete "Design Spec" document (document owner)
```

---

## RBAC Implementation Patterns

### Database Schema

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255)
);

CREATE TABLE roles (
  id UUID PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE permissions (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id),
  role_id UUID REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE role_permissions (
  role_id UUID REFERENCES roles(id),
  permission_id UUID REFERENCES permissions(id),
  PRIMARY KEY (role_id, permission_id)
);
```

### Permission Checking

```javascript
async function hasPermission(userId, permission, resourceId = null) {
  // Get user's roles
  const userRoles = await db.userRoles
    .where({ userId })
    .join('roles', 'roles.id', 'user_roles.role_id')
    .select('roles.name');
  
  // Get permissions for those roles
  const rolePermissions = await db.rolePermissions
    .whereIn('role_id', userRoles.map(r => r.id))
    .join('permissions', 'permissions.id', 'role_permissions.permission_id')
    .select('permissions.name');
  
  // Check if user has permission
  const hasPermission = rolePermissions.some(p => 
    p.name === permission || p.name === permission.split(':')[0] + ':*'
  );
  
  // Check resource-level permissions (if applicable)
  if (resourceId) {
    const isOwner = await db.resources.findOne({
      id: resourceId,
      ownerId: userId
    });
    
    if (isOwner) return true;
  }
  
  return hasPermission;
}
```

### Middleware for API Routes

```javascript
function requirePermission(permission) {
  return async (req, res, next) => {
    const hasPermission = await hasPermission(req.user.id, permission);
    
    if (!hasPermission) {
      return res.status(403).json({
        error: 'Forbidden',
        message: `You don't have permission: ${permission}`
      });
    }
    
    next();
  };
}

// Usage
app.delete('/api/projects/:id',
  requirePermission('project:delete'),
  async (req, res) => {
    // Delete project
  }
);
```

### UI Components

```javascript
function CanAccess({ permission, children }) {
  const { user } = useAuth();
  const hasPermission = usePermission(user.id, permission);
  
  if (!hasPermission) return null;
  
  return children;
}

// Usage
<CanAccess permission="project:delete">
  <button onClick={deleteProject}>Delete Project</button>
</CanAccess>
```

---

## RBAC with Teams

### Model

```
Users belong to Teams
Teams have Roles in Workspaces
Users inherit permissions from Team Roles
```

### Example

```
Team: Engineering
Members: John, Jane, Bob

Workspace: Website Redesign
Engineering team has "Editor" role

Result:
- John can edit Website Redesign (via Engineering team)
- Jane can edit Website Redesign (via Engineering team)
- Bob can edit Website Redesign (via Engineering team)
```

### Database Schema

```sql
CREATE TABLE teams (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE team_members (
  team_id UUID REFERENCES teams(id),
  user_id UUID REFERENCES users(id),
  PRIMARY KEY (team_id, user_id)
);

CREATE TABLE team_workspace_roles (
  team_id UUID REFERENCES teams(id),
  workspace_id UUID REFERENCES workspaces(id),
  role_id UUID REFERENCES roles(id),
  PRIMARY KEY (team_id, workspace_id)
);
```

### Permission Checking

```javascript
async function hasPermission(userId, permission, workspaceId) {
  // Check direct user roles
  const directPermissions = await getUserPermissions(userId, workspaceId);
  
  // Check team roles
  const teams = await db.teamMembers.where({ userId });
  const teamPermissions = await getTeamPermissions(teams, workspaceId);
  
  const allPermissions = [...directPermissions, ...teamPermissions];
  
  return allPermissions.includes(permission);
}
```

---

## RBAC with SSO

### Map SSO Groups to Application Roles

**SAML Assertion:**
```xml
<saml:Attribute Name="groups">
  <saml:AttributeValue>Admins</saml:AttributeValue>
  <saml:AttributeValue>Engineering</saml:AttributeValue>
</saml:Attribute>
```

**Mapping Configuration:**
```javascript
const ssoGroupRoleMapping = {
  'Admins': 'admin',
  'Engineering': 'member',
  'Sales': 'member',
  'Executives': 'viewer'
};

async function handleSSOLogin(assertion) {
  const ssoGroups = assertion.attributes.groups || [];
  const roles = ssoGroups
    .map(group => ssoGroupRoleMapping[group])
    .filter(role => role !== undefined);
  
  // Assign roles to user
  await db.userRoles.deleteWhere({ userId: user.id });
  for (const roleName of roles) {
    const role = await db.roles.findOne({ name: roleName });
    await db.userRoles.create({ userId: user.id, roleId: role.id });
  }
}
```

### Override SSO-Assigned Roles (If Allowed)

**Option 1: SSO roles are authoritative (can't override)**
```javascript
// Always sync roles from SSO
await syncRolesFromSSO(user, ssoGroups);
```

**Option 2: SSO roles + manual roles**
```javascript
// Keep manual roles, add SSO roles
const manualRoles = await getManualRoles(user.id);
const ssoRoles = mapSSOGroups(ssoGroups);
const allRoles = [...manualRoles, ...ssoRoles];
```

---

## Permission Inheritance

### Org Admin → Project Admin

**Rule:** Org admin automatically has admin access to all projects

**Implementation:**
```javascript
async function hasPermission(userId, permission, projectId) {
  // Check if user is org admin
  const isOrgAdmin = await db.userRoles.findOne({
    userId,
    role: 'org_admin'
  });
  
  if (isOrgAdmin) return true;  // Org admin can do anything
  
  // Check project-level permissions
  const projectRole = await db.projectRoles.findOne({
    userId,
    projectId
  });
  
  return projectRole && hasPermissionForRole(projectRole.role, permission);
}
```

### Project Member → Resource Viewer

**Rule:** Project member can view all resources in project

**Implementation:**
```javascript
async function canViewResource(userId, resourceId) {
  const resource = await db.resources.findOne({ id: resourceId });
  const projectMember = await db.projectMembers.findOne({
    userId,
    projectId: resource.projectId
  });
  
  return projectMember !== null;
}
```

---

## Conditional Permissions

### Resource Owner

**Rule:** Can edit own documents (even if not editor role)

**Implementation:**
```javascript
async function canEditDocument(userId, documentId) {
  const document = await db.documents.findOne({ id: documentId });
  
  // Owner can always edit
  if (document.ownerId === userId) return true;
  
  // Check role-based permissions
  return await hasPermission(userId, 'document:edit');
}
```

### Time-Based

**Rule:** Temporary access (expires after 7 days)

**Implementation:**
```javascript
async function hasTemporaryAccess(userId, resourceId) {
  const access = await db.temporaryAccess.findOne({
    userId,
    resourceId,
    expiresAt: { $gt: new Date() }  // Not expired
  });
  
  return access !== null;
}
```

### Approval-Based

**Rule:** Request access, admin approves

**Implementation:**
```javascript
// Request access
app.post('/api/access-requests', async (req, res) => {
  const { resourceId, reason } = req.body;
  
  const request = await db.accessRequests.create({
    userId: req.user.id,
    resourceId,
    reason,
    status: 'pending'
  });
  
  // Notify admins
  await notifyAdmins(request);
  
  res.json(request);
});

// Approve access
app.post('/api/access-requests/:id/approve', async (req, res) => {
  const request = await db.accessRequests.findOne({ id: req.params.id });
  
  // Grant temporary access (7 days)
  await db.temporaryAccess.create({
    userId: request.userId,
    resourceId: request.resourceId,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  });
  
  request.status = 'approved';
  await request.save();
  
  res.json(request);
});
```

---

## RBAC Testing

### Test Each Role

```javascript
describe('RBAC', () => {
  test('Admin can delete projects', async () => {
    const admin = await createUser({ role: 'admin' });
    const canDelete = await hasPermission(admin.id, 'project:delete');
    expect(canDelete).toBe(true);
  });
  
  test('Member cannot delete projects', async () => {
    const member = await createUser({ role: 'member' });
    const canDelete = await hasPermission(member.id, 'project:delete');
    expect(canDelete).toBe(false);
  });
  
  test('Viewer can view projects', async () => {
    const viewer = await createUser({ role: 'viewer' });
    const canView = await hasPermission(viewer.id, 'project:view');
    expect(canView).toBe(true);
  });
});
```

### Test Permission Inheritance

```javascript
test('Manager inherits Member permissions', async () => {
  const manager = await createUser({ role: 'manager' });
  
  // Manager should have member permissions
  expect(await hasPermission(manager.id, 'project:create')).toBe(true);
  expect(await hasPermission(manager.id, 'project:edit')).toBe(true);
  
  // Plus manager-specific permissions
  expect(await hasPermission(manager.id, 'user:invite')).toBe(true);
});
```

### Test API Permissions

```javascript
test('DELETE /api/projects requires project:delete permission', async () => {
  const member = await createUser({ role: 'member' });
  const token = await generateToken(member);
  
  const response = await request(app)
    .delete('/api/projects/123')
    .set('Authorization', `Bearer ${token}`);
  
  expect(response.status).toBe(403);
  expect(response.body.error).toBe('Forbidden');
});
```

### Test UI Shows/Hides Correctly

```javascript
test('Delete button hidden for members', () => {
  const member = { role: 'member' };
  const { queryByText } = render(<ProjectPage user={member} />);
  
  expect(queryByText('Delete Project')).toBeNull();
});

test('Delete button visible for admins', () => {
  const admin = { role: 'admin' };
  const { getByText } = render(<ProjectPage user={admin} />);
  
  expect(getByText('Delete Project')).toBeInTheDocument();
});
```

---

## RBAC Audit Logging

### Log Permission Changes

```javascript
// Log role assignment
app.post('/api/users/:userId/roles', async (req, res) => {
  const { roleId } = req.body;
  
  await db.userRoles.create({
    userId: req.params.userId,
    roleId
  });
  
  // Audit log
  await db.auditLogs.create({
    action: 'role_assigned',
    actorId: req.user.id,
    targetUserId: req.params.userId,
    roleId,
    timestamp: new Date()
  });
  
  res.json({ success: true });
});
```

### Log Access Attempts

```javascript
async function hasPermission(userId, permission, resourceId) {
  const allowed = await checkPermission(userId, permission, resourceId);
  
  // Log access attempt
  await db.accessLogs.create({
    userId,
    permission,
    resourceId,
    allowed,
    timestamp: new Date()
  });
  
  return allowed;
}
```

### Regular Access Reviews

```javascript
// Generate access review report
app.get('/api/reports/access-review', async (req, res) => {
  const users = await db.users.all();
  const report = [];
  
  for (const user of users) {
    const roles = await db.userRoles.where({ userId: user.id });
    const permissions = await getAllPermissions(roles);
    
    report.push({
      user: user.email,
      roles: roles.map(r => r.name),
      permissions,
      lastLogin: user.lastLoginAt
    });
  }
  
  res.json(report);
});
```

---

## Tools and Libraries

### Casbin (Policy Engine)

**Features:**
- Policy-based access control
- Supports RBAC, ABAC, ACL
- Multiple languages (Go, Node.js, Python, Java)

**Example:**
```javascript
const casbin = require('casbin');

const enforcer = await casbin.newEnforcer('model.conf', 'policy.csv');

// Check permission
const allowed = await enforcer.enforce('john', 'project', 'delete');
```

### Oso (Authorization Library)

**Features:**
- Declarative policies (Polar language)
- Supports RBAC, ABAC
- Python, Ruby, Node.js, Java

**Example:**
```python
from oso import Oso

oso = Oso()
oso.load_files(["policy.polar"])

# Check permission
allowed = oso.is_allowed(user, "delete", project)
```

### AWS IAM (Inspiration)

**Concepts:**
- Users, Groups, Roles, Policies
- Policy documents (JSON)
- Resource-based policies

**Learn From:** AWS IAM design patterns

### Custom Implementation

**When to Use:** Most applications (RBAC is simple enough to implement)

**Benefits:**
- Full control
- No external dependencies
- Tailored to your needs

---

## Real RBAC Models

### GitHub

**Roles:**
- Owner (full control)
- Maintainer (manage repo, can't delete)
- Member (write access)
- Triage (manage issues)
- Read (read-only)

**Levels:**
- Organization level
- Repository level

### Google Workspace

**Roles:**
- Super Admin (full control)
- Admin (manage users, settings)
- User (standard access)

**Custom Roles:** Yes (enterprise feature)

### Salesforce

**Roles:**
- System Administrator (full control)
- Standard User (basic access)
- Custom roles (customer-defined)

**Levels:**
- Organization level
- Object level (per Salesforce object)

---

## Summary

### Quick Reference

**RBAC:** Users → Roles → Permissions

**Components:**
- Users (people, service accounts)
- Roles (Admin, Manager, Member, Viewer)
- Permissions (project:create, user:delete)
- Resources (projects, files, reports)

**Common Roles:**
- Owner/Admin (full control)
- Manager/Editor (create, edit, delete)
- Member/Contributor (create, edit own)
- Viewer/Reader (read-only)

**Permission Format:** `resource:action`

**Hierarchical Roles:**
- Admin inherits Manager
- Manager inherits Member
- Member inherits Viewer

**Multi-Level:**
- Organization level
- Project/workspace level
- Resource level

**Database Schema:**
- users, roles, permissions
- user_roles, role_permissions

**Permission Checking:**
```javascript
hasPermission(userId, permission, resourceId)
```

**Middleware:**
```javascript
requirePermission('project:delete')
```

**UI Components:**
```javascript
<CanAccess permission="project:delete">
  <button>Delete</button>
</CanAccess>
```

**Testing:**
- Test each role
- Test permission inheritance
- Test API permissions
- Test UI shows/hides

**Tools:**
- Casbin (policy engine)
- Oso (authorization library)
- Custom implementation (recommended)

## Best Practices

### RBAC Design Best Practices
- **Principle of Least Privilege**: Grant users only the minimum permissions needed to perform their job functions. Start with read-only access and escalate only when necessary.
- **Role Hierarchy**: Design a clear role hierarchy where higher-level roles inherit permissions from lower-level roles. This reduces duplication and simplifies management.
- **Permission Granularity**: Use fine-grained permissions (e.g., `project:create`, `project:edit_own`, `project:edit_all`) rather than coarse-grained ones (e.g., `project:manage`).
- **Separation of Duties**: Implement role separation for critical operations. For example, different users should be able to create invoices and approve invoices to prevent fraud.
- **Default Deny**: Always deny access by default and explicitly grant permissions. This prevents accidental access from missing permission checks.

### Implementation Best Practices
- **Database Design**: Use normalized schema with separate tables for users, roles, permissions, and their relationships. This allows for flexible querying and auditing.
- **Permission Caching**: Cache user permissions after initial lookup to avoid repeated database queries. Invalidate cache when roles or permissions change.
- **Middleware Pattern**: Implement permission checking as middleware in your API framework. This ensures consistent enforcement across all endpoints.
- **UI Integration**: Create reusable UI components (e.g., `<CanAccess>`) that conditionally render based on user permissions. This provides a better user experience.
- **Audit Logging**: Log all permission changes and access attempts. This is essential for security audits and compliance.

### Multi-Level RBAC Best Practices
- **Organization-Level Roles**: Define org-wide roles (Owner, Admin, Member) for administrative functions like billing and user management.
- **Project-Level Roles**: Define project-specific roles (Admin, Member, Viewer) for resource access within projects.
- **Resource-Level Permissions**: Implement resource ownership checks where users can always access resources they created, regardless of their role.
- **Permission Inheritance**: Ensure that org admins automatically have admin access to all projects, and project members can view all project resources.

### SSO Integration Best Practices
- **Group-to-Role Mapping**: Map SSO groups to application roles automatically. This allows IT admins to control access through their IdP.
- **JIT Provisioning**: Create users on first SSO login with default roles based on their group membership.
- **Role Synchronization**: Sync roles from SSO on each login to ensure users always have the correct permissions.
- **Override Capability**: Allow manual role overrides for special cases where SSO-assigned roles need adjustment.

### Testing Best Practices
- **Test Each Role**: Write tests for each role to verify they have expected permissions and are denied access to unauthorized resources.
- **Test Inheritance**: Verify that role inheritance works correctly and that higher-level roles have all permissions of lower-level roles.
- **Test API Endpoints**: Test that API endpoints properly enforce permissions and return appropriate error codes (403 Forbidden) for unauthorized access.
- **Test UI Components**: Verify that UI elements are shown/hidden based on user permissions.
- **Test Edge Cases**: Test resource ownership, time-based access, and approval-based access flows.

### Security Best Practices
- **Never Trust Client-Side**: Always validate permissions on the server-side, even if UI hides certain actions.
- **Secure Session Management**: Use secure, HTTP-only cookies with SameSite protection to prevent session hijacking.
- **Rate Limiting**: Implement rate limiting on permission checks to prevent brute force attacks.
- **Regular Access Reviews**: Conduct quarterly reviews of who has what permissions and revoke access that is no longer needed.
- **Log Suspicious Activity**: Alert on repeated permission denials, access from unusual locations, or access attempts outside business hours.

## Checklist

### RBAC Design Checklist
- [ ] Define user types and their access requirements
- [ ] Create a clear role hierarchy with inheritance
- [ ] Design fine-grained permissions using `resource:action` format
- [ ] Implement separation of duties for critical operations
- [ ] Apply principle of least privilege for all roles
- [ ] Document all roles and their permissions

### Implementation Checklist
- [ ] Design normalized database schema for users, roles, permissions
- [ ] Implement permission checking function with caching
- [ ] Create middleware for API permission enforcement
- [ ] Build UI components for conditional rendering
- [ ] Implement audit logging for permission changes
- [ ] Add error handling for unauthorized access (403)

### Multi-Level RBAC Checklist
- [ ] Define organization-level roles (Owner, Admin, Member)
- [ ] Define project-level roles (Admin, Member, Viewer)
- [ ] Implement resource ownership checks
- [ ] Configure permission inheritance between levels
- [ ] Test cross-level access permissions

### SSO Integration Checklist
- [ ] Configure SSO group-to-role mapping
- [ ] Implement JIT provisioning for new users
- [ ] Set up role synchronization on login
- [ ] Allow manual role overrides if needed
- [ ] Test SSO login with different group memberships

### Testing Checklist
- [ ] Write tests for each role's permissions
- [ ] Test role inheritance behavior
- [ ] Test API endpoint permission enforcement
- [ ] Test UI component visibility based on permissions
- [ ] Test edge cases (resource owner, time-based access)
- [ ] Run tests in CI/CD pipeline

### Security Checklist
- [ ] Validate all permissions on server-side
- [ ] Use secure, HTTP-only session cookies
- [ ] Implement rate limiting on permission checks
- [ ] Set up regular access review process
- [ ] Configure alerts for suspicious activity
- [ ] Review and update permissions quarterly

### Deployment Checklist
- [ ] Document RBAC model for users
- [ ] Create admin guide for role management
- [ ] Set up monitoring for permission errors
- [ ] Configure backup and restore for role data
- [ ] Train support team on common RBAC issues
- [ ] Create incident response process for permission issues
