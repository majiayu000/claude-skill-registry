---
name: authorization-models
description: Comprehensive authorization guidance covering RBAC, ABAC, ACL, ReBAC, and policy-as-code patterns. Use when designing permission systems, implementing access control, or choosing authorization strategies.
allowed-tools: Read, Glob, Grep, Task
---

# Authorization Models Skill

## Overview

This skill provides comprehensive guidance on authorization models and access control patterns. Authorization determines what authenticated users can do within a system.

**Key Principle:** Authorization should be declarative, centralized, and auditable.

## When to Use This Skill

- Designing a permission system from scratch
- Choosing between RBAC, ABAC, ACL, or ReBAC
- Implementing policy-as-code with OPA
- Migrating from simple role checks to fine-grained authorization
- Implementing the principle of least privilege
- Designing multi-tenant authorization
- Building a Zanzibar-style permission system

## Authorization Model Comparison

| Model | Best For | Complexity | Scalability | Flexibility |
|-------|----------|------------|-------------|-------------|
| **ACL** | File systems, simple resources | Low | Medium | Low |
| **RBAC** | Enterprise apps, clear job roles | Medium | High | Medium |
| **ABAC** | Complex policies, dynamic rules | High | High | High |
| **ReBAC** | Social graphs, document sharing | Medium-High | Very High | High |

## Quick Decision Tree

```text
Need authorization model?
├── Simple resource ownership?
│   └── ACL (Access Control Lists)
├── Clear organizational roles?
│   └── RBAC (Role-Based Access Control)
├── Complex, context-dependent rules?
│   └── ABAC (Attribute-Based Access Control)
└── Relationship-based access (sharing, hierarchies)?
    └── ReBAC (Relationship-Based Access Control)
```

## Role-Based Access Control (RBAC)

### Core Concepts

```csharp
/// <summary>
/// Fine-grained permissions for RBAC.
/// </summary>
[Flags]
public enum Permission
{
    None = 0,
    Read = 1,
    Create = 2,
    Update = 4,
    Delete = 8,
    Admin = 16,
    Approve = 32,
    Publish = 64,

    // Common combinations
    ReadWrite = Read | Update,
    Editor = Read | Create | Update,
    FullAccess = Read | Create | Update | Delete | Admin
}

/// <summary>
/// Role with associated permissions.
/// </summary>
public sealed record Role(string Name, Permission Permissions, string Description = "");

/// <summary>
/// Standard roles definition.
/// </summary>
public static class StandardRoles
{
    public static readonly Role Viewer = new("viewer", Permission.Read, "Read-only access");
    public static readonly Role Editor = new("editor", Permission.Editor, "Can create and edit content");
    public static readonly Role Admin = new("admin", Permission.FullAccess, "Full administrative access");

    public static readonly IReadOnlyDictionary<string, Role> All = new Dictionary<string, Role>
    {
        [Viewer.Name] = Viewer,
        [Editor.Name] = Editor,
        [Admin.Name] = Admin
    };
}
```

### RBAC Implementation

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

/// <summary>
/// Simple RBAC authorization service.
/// </summary>
public sealed class RbacAuthorizer
{
    private readonly Dictionary<string, HashSet<string>> _userRoles = new();

    public void AssignRole(string userId, string role)
    {
        if (!_userRoles.TryGetValue(userId, out var roles))
        {
            roles = new HashSet<string>();
            _userRoles[userId] = roles;
        }
        roles.Add(role);
    }

    public bool HasPermission(string userId, Permission permission)
    {
        if (!_userRoles.TryGetValue(userId, out var userRoles))
            return false;

        foreach (var roleName in userRoles)
        {
            if (StandardRoles.All.TryGetValue(roleName, out var role) &&
                role.Permissions.HasFlag(permission))
            {
                return true;
            }
        }
        return false;
    }

    public bool HasRole(string userId, string role) =>
        _userRoles.TryGetValue(userId, out var roles) && roles.Contains(role);
}

/// <summary>
/// ASP.NET Core authorization requirement for permissions.
/// </summary>
public sealed class PermissionRequirement(Permission permission) : IAuthorizationRequirement
{
    public Permission Permission { get; } = permission;
}

/// <summary>
/// Handler for permission-based authorization.
/// </summary>
public sealed class PermissionHandler(RbacAuthorizer authorizer) : AuthorizationHandler<PermissionRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        PermissionRequirement requirement)
    {
        var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (userId is not null && authorizer.HasPermission(userId, requirement.Permission))
        {
            context.Succeed(requirement);
        }
        return Task.CompletedTask;
    }
}

// Usage with attribute
[Authorize(Policy = "RequireCreate")]
[HttpPost("articles")]
public IActionResult CreateArticle([FromBody] ArticleDto article)
{
    // Only users with CREATE permission can access
    return Ok();
}
```

### Hierarchical RBAC

```csharp
/// <summary>
/// Role with inheritance support.
/// </summary>
public sealed class HierarchicalRole(
    string name,
    Permission directPermissions,
    HierarchicalRole? parent = null)
{
    public string Name { get; } = name;
    public HierarchicalRole? Parent { get; } = parent;

    /// <summary>
    /// Get all permissions including inherited from parent roles.
    /// </summary>
    public Permission AllPermissions
    {
        get
        {
            var permissions = directPermissions;
            var current = Parent;
            while (current is not null)
            {
                permissions |= current.AllPermissions;
                current = current.Parent;
            }
            return permissions;
        }
    }
}

// Role hierarchy: admin > editor > viewer
var viewerRole = new HierarchicalRole("viewer", Permission.Read);
var editorRole = new HierarchicalRole("editor", Permission.Create | Permission.Update, viewerRole);
var adminRole = new HierarchicalRole("admin", Permission.Delete | Permission.Admin, editorRole);

// adminRole.AllPermissions includes all permissions from parent roles
```

## Attribute-Based Access Control (ABAC)

### Core Concepts

```csharp
using System.Collections.Immutable;

/// <summary>
/// Context for an access decision.
/// </summary>
public sealed record AccessRequest(
    ImmutableDictionary<string, object> Subject,     // Who is requesting
    ImmutableDictionary<string, object> Resource,    // What they're accessing
    string Action,                                    // What they want to do
    ImmutableDictionary<string, object> Environment  // Context (time, location, etc.)
)
{
    public T GetSubjectAttribute<T>(string key, T defaultValue = default!) =>
        Subject.TryGetValue(key, out var value) && value is T typed ? typed : defaultValue;

    public T GetResourceAttribute<T>(string key, T defaultValue = default!) =>
        Resource.TryGetValue(key, out var value) && value is T typed ? typed : defaultValue;

    public T GetEnvironmentAttribute<T>(string key, T defaultValue = default!) =>
        Environment.TryGetValue(key, out var value) && value is T typed ? typed : defaultValue;
}

/// <summary>
/// Policy effect type.
/// </summary>
public enum PolicyEffect { Permit, Deny }

/// <summary>
/// Attribute-based policy evaluation.
/// </summary>
public sealed class AbacPolicy(
    string name,
    Func<AccessRequest, bool> condition,
    PolicyEffect effect = PolicyEffect.Permit)
{
    public string Name { get; } = name;

    /// <summary>
    /// Return effect if condition matches, null otherwise.
    /// </summary>
    public PolicyEffect? Evaluate(AccessRequest request) =>
        condition(request) ? effect : null;
}
```

### ABAC Policy Examples

```csharp
// Policy: Only managers can approve expenses over $1000
var managerApprovalPolicy = new AbacPolicy(
    name: "manager_approval",
    condition: req =>
        req.Action == "approve" &&
        req.GetResourceAttribute<string>("type") == "expense" &&
        req.GetResourceAttribute<decimal>("amount") > 1000 &&
        req.GetSubjectAttribute<string>("role") == "manager"
);

// Policy: Users can only access their own department's data
var departmentIsolationPolicy = new AbacPolicy(
    name: "department_isolation",
    condition: req =>
        req.GetSubjectAttribute<string>("department") ==
        req.GetResourceAttribute<string>("department")
);

// Policy: No access outside business hours
var businessHoursPolicy = new AbacPolicy(
    name: "business_hours",
    condition: req =>
    {
        var now = DateTime.Now;
        var hour = now.Hour;
        var dayOfWeek = now.DayOfWeek;
        return hour >= 9 && hour <= 17 &&
               dayOfWeek != DayOfWeek.Saturday &&
               dayOfWeek != DayOfWeek.Sunday;
    }
);

// Policy: Deny access from untrusted networks
var networkPolicy = new AbacPolicy(
    name: "trusted_network",
    condition: req =>
        req.GetEnvironmentAttribute<string>("ip_address", "")
           .StartsWith("10.0.", StringComparison.Ordinal)
);
```

### ABAC Policy Engine

```csharp
/// <summary>
/// Policy decision point (PDP) with deny-overrides algorithm.
/// </summary>
public sealed class AbacEngine(PolicyEffect defaultEffect = PolicyEffect.Deny)
{
    private readonly List<AbacPolicy> _policies = [];

    public void AddPolicy(AbacPolicy policy) => _policies.Add(policy);

    /// <summary>
    /// Evaluate all policies. Deny-overrides combining algorithm.
    /// </summary>
    public bool Evaluate(AccessRequest request)
    {
        var permitFound = false;

        foreach (var policy in _policies)
        {
            var effect = policy.Evaluate(request);
            if (effect == PolicyEffect.Deny)
            {
                return false;  // Explicit deny always wins
            }
            if (effect == PolicyEffect.Permit)
            {
                permitFound = true;
            }
        }

        return permitFound || defaultEffect == PolicyEffect.Permit;
    }
}

// Usage
var engine = new AbacEngine();
engine.AddPolicy(departmentIsolationPolicy);
engine.AddPolicy(businessHoursPolicy);

var request = new AccessRequest(
    Subject: ImmutableDictionary.CreateRange(new Dictionary<string, object>
    {
        ["user_id"] = "123",
        ["department"] = "engineering",
        ["role"] = "developer"
    }),
    Resource: ImmutableDictionary.CreateRange(new Dictionary<string, object>
    {
        ["id"] = "doc-456",
        ["department"] = "engineering",
        ["type"] = "document"
    }),
    Action: "read",
    Environment: ImmutableDictionary.CreateRange(new Dictionary<string, object>
    {
        ["ip_address"] = "10.0.1.50",
        ["time"] = DateTime.UtcNow
    })
);

if (engine.Evaluate(request))
{
    // Access granted
}
```

## Access Control Lists (ACL)

### Simple ACL Implementation

```csharp
/// <summary>
/// Unix-style ACL permissions.
/// </summary>
[Flags]
public enum AclPermission
{
    None = 0,
    Read = 1,
    Write = 2,
    Execute = 4,
    Delete = 8,
    Admin = 16,

    // Common combinations
    ReadWrite = Read | Write,
    Full = Read | Write | Execute | Delete | Admin
}

/// <summary>
/// Principal type for ACL entries.
/// </summary>
public enum PrincipalType { User, Group }

/// <summary>
/// Access control entry.
/// </summary>
public sealed class AclEntry(string principal, AclPermission permissions, PrincipalType principalType = PrincipalType.User)
{
    public string Principal { get; } = principal;
    public AclPermission Permissions { get; set; } = permissions;
    public PrincipalType PrincipalType { get; } = principalType;
}

/// <summary>
/// Access control list for a resource.
/// </summary>
public sealed class Acl(string resourceId, string owner)
{
    public string ResourceId { get; } = resourceId;
    public string Owner { get; } = owner;
    private readonly Dictionary<string, AclEntry> _entries = new();

    /// <summary>
    /// Grant permissions to a principal.
    /// </summary>
    public void Grant(string principal, AclPermission permissions, PrincipalType principalType = PrincipalType.User)
    {
        if (_entries.TryGetValue(principal, out var entry))
        {
            entry.Permissions |= permissions;
        }
        else
        {
            _entries[principal] = new AclEntry(principal, permissions, principalType);
        }
    }

    /// <summary>
    /// Revoke permissions from a principal.
    /// </summary>
    public void Revoke(string principal, AclPermission permissions)
    {
        if (_entries.TryGetValue(principal, out var entry))
        {
            entry.Permissions &= ~permissions;
            if (entry.Permissions == AclPermission.None)
            {
                _entries.Remove(principal);
            }
        }
    }

    /// <summary>
    /// Check if principal has permission.
    /// </summary>
    public bool Check(string principal, AclPermission permission, ISet<string>? userGroups = null)
    {
        // Owner has full access
        if (principal == Owner)
        {
            return true;
        }

        // Check direct user entry
        if (_entries.TryGetValue(principal, out var entry) &&
            entry.Permissions.HasFlag(permission))
        {
            return true;
        }

        // Check group entries
        if (userGroups is not null)
        {
            foreach (var group in userGroups)
            {
                if (_entries.TryGetValue(group, out var groupEntry) &&
                    groupEntry.PrincipalType == PrincipalType.Group &&
                    groupEntry.Permissions.HasFlag(permission))
                {
                    return true;
                }
            }
        }

        return false;
    }
}
```

### ACL Usage Example

```csharp
// Create ACL for a document
var docAcl = new Acl(resourceId: "doc-123", owner: "alice");

// Grant permissions
docAcl.Grant("bob", AclPermission.ReadWrite);
docAcl.Grant("engineering", AclPermission.Read, PrincipalType.Group);
docAcl.Grant("charlie", AclPermission.Read);

// Check permissions
docAcl.Check("alice", AclPermission.Delete);   // True (owner)
docAcl.Check("bob", AclPermission.Write);      // True (explicit grant)
docAcl.Check("bob", AclPermission.Delete);     // False (not granted)
docAcl.Check("dave", AclPermission.Read,
             userGroups: new HashSet<string> { "engineering" });  // True (group membership)
```

## Relationship-Based Access Control (ReBAC)

### Zanzibar-Style Model

```csharp
/// <summary>
/// A relationship tuple (object, relation, subject) in Zanzibar style.
/// </summary>
public readonly record struct Relationship(
    string ObjectType,
    string ObjectId,
    string Relation,
    string SubjectType,
    string SubjectId,
    string? SubjectRelation = null)  // For usersets
{
    public override string ToString()
    {
        var subject = $"{SubjectType}:{SubjectId}";
        if (SubjectRelation is not null)
        {
            subject += $"#{SubjectRelation}";
        }
        return $"{ObjectType}:{ObjectId}#{Relation}@{subject}";
    }
}

/// <summary>
/// Simple ReBAC implementation (Zanzibar-inspired).
/// </summary>
public sealed class ReBac
{
    // Store relationships: (object_type, object_id, relation) -> set of subjects
    private readonly Dictionary<(string ObjectType, string ObjectId, string Relation),
                                HashSet<(string SubjectType, string SubjectId, string? SubjectRelation)>> _tuples = new();

    // Relation definitions with computed relations
    // object_type -> relation -> set of parent relations for inheritance
    private readonly Dictionary<string, Dictionary<string, HashSet<string>>> _relationConfig = new();

    /// <summary>
    /// Define a relation and its inheritance.
    /// </summary>
    public void DefineRelation(string objectType, string relation, IEnumerable<string>? inheritsFrom = null)
    {
        if (!_relationConfig.TryGetValue(objectType, out var relations))
        {
            relations = new Dictionary<string, HashSet<string>>();
            _relationConfig[objectType] = relations;
        }
        relations[relation] = inheritsFrom?.ToHashSet() ?? [];
    }

    /// <summary>
    /// Write a relationship tuple.
    /// </summary>
    public void Write(Relationship rel)
    {
        var key = (rel.ObjectType, rel.ObjectId, rel.Relation);
        if (!_tuples.TryGetValue(key, out var subjects))
        {
            subjects = [];
            _tuples[key] = subjects;
        }
        subjects.Add((rel.SubjectType, rel.SubjectId, rel.SubjectRelation));
    }

    /// <summary>
    /// Delete a relationship tuple.
    /// </summary>
    public void Delete(Relationship rel)
    {
        var key = (rel.ObjectType, rel.ObjectId, rel.Relation);
        if (_tuples.TryGetValue(key, out var subjects))
        {
            subjects.Remove((rel.SubjectType, rel.SubjectId, rel.SubjectRelation));
        }
    }

    /// <summary>
    /// Check if subject has relation to object.
    /// </summary>
    public bool Check(string objectType, string objectId, string relation,
                      string subjectType, string subjectId)
    {
        var key = (objectType, objectId, relation);

        // Direct check
        if (_tuples.TryGetValue(key, out var subjects) &&
            subjects.Contains((subjectType, subjectId, null)))
        {
            return true;
        }

        // Check inherited relations
        if (_relationConfig.TryGetValue(objectType, out var relations) &&
            relations.TryGetValue(relation, out var inherited))
        {
            foreach (var parentRelation in inherited)
            {
                if (Check(objectType, objectId, parentRelation, subjectType, subjectId))
                {
                    return true;
                }
            }
        }

        // Check userset rewrite (e.g., folder:123#viewer@document:456#parent)
        if (_tuples.TryGetValue(key, out var tupleSubjects))
        {
            foreach (var (subjType, subjId, subjRel) in tupleSubjects)
            {
                if (subjRel is not null)
                {
                    // This is a userset - check if user has that relation on referenced object
                    if (Check(subjType, subjId, subjRel, subjectType, subjectId))
                    {
                        return true;
                    }
                }
            }
        }

        return false;
    }
}
```

### ReBAC Usage Example (Google Drive-style)

```csharp
// Initialize ReBAC
var rebac = new ReBac();

// Define relation hierarchy
// Editors can also view (editor inherits from viewer)
rebac.DefineRelation("document", "viewer", null);
rebac.DefineRelation("document", "editor", ["viewer"]);
rebac.DefineRelation("document", "owner", ["editor"]);

rebac.DefineRelation("folder", "viewer", null);
rebac.DefineRelation("folder", "editor", ["viewer"]);
rebac.DefineRelation("folder", "owner", ["editor"]);

// folder viewers are document viewers (documents inherit from parent folder)
rebac.DefineRelation("document", "parent", null);

// Create relationships
// Alice owns folder "projects"
rebac.Write(new Relationship("folder", "projects", "owner", "user", "alice"));

// Bob is an editor on folder "projects"
rebac.Write(new Relationship("folder", "projects", "editor", "user", "bob"));

// Document "spec" is in folder "projects"
// Anyone who can view the folder can view the document
rebac.Write(new Relationship("document", "spec", "parent", "folder", "projects",
                             SubjectRelation: "viewer"));

// Charlie has direct viewer access to document
rebac.Write(new Relationship("document", "spec", "viewer", "user", "charlie"));

// Check permissions
rebac.Check("folder", "projects", "owner", "user", "alice");    // True
rebac.Check("folder", "projects", "viewer", "user", "alice");   // True (owner->editor->viewer)
rebac.Check("folder", "projects", "editor", "user", "bob");     // True
rebac.Check("document", "spec", "viewer", "user", "bob");       // True (folder editor->viewer)
rebac.Check("document", "spec", "editor", "user", "charlie");   // False (only viewer)
```

## Policy-as-Code with Open Policy Agent (OPA)

### Rego Policy Basics

```rego
# policy.rego
package authz

import future.keywords.if
import future.keywords.in

# Default deny
default allow := false

# Allow if user has required permission
allow if {
    user_has_permission[input.action]
}

# User permissions based on roles
user_has_permission[permission] if {
    some role in input.user.roles
    some permission in role_permissions[role]
}

# Role to permission mapping
role_permissions := {
    "admin": ["read", "write", "delete", "admin"],
    "editor": ["read", "write"],
    "viewer": ["read"],
}

# Resource-specific rules
allow if {
    input.action == "read"
    input.resource.public == true
}

# Owner can always access their resources
allow if {
    input.resource.owner == input.user.id
}
```

### OPA Integration in .NET

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

/// <summary>
/// Client for Open Policy Agent.
/// </summary>
public sealed class OpaClient(HttpClient httpClient, string opaUrl = "http://localhost:8181") : IDisposable
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
    };

    /// <summary>
    /// Query OPA for a policy decision.
    /// </summary>
    public async Task<bool> CheckAsync(string policyPath, object inputData, CancellationToken cancellationToken = default)
    {
        var url = $"{opaUrl}/v1/data/{policyPath}";
        var request = new OpaRequest(inputData);

        var response = await httpClient.PostAsJsonAsync(url, request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<OpaResponse<bool>>(JsonOptions, cancellationToken);
        return result?.Result ?? false;
    }

    /// <summary>
    /// Run an arbitrary Rego query.
    /// </summary>
    public async Task<JsonElement?> QueryAsync(string query, object inputData, CancellationToken cancellationToken = default)
    {
        var url = $"{opaUrl}/v1/query";
        var request = new { query, input = inputData };

        var response = await httpClient.PostAsJsonAsync(url, request, JsonOptions, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<OpaResponse<JsonElement>>(JsonOptions, cancellationToken);
        return result?.Result;
    }

    public void Dispose() => httpClient.Dispose();

    private sealed record OpaRequest([property: JsonPropertyName("input")] object Input);
    private sealed record OpaResponse<T>([property: JsonPropertyName("result")] T? Result);
}

// Usage
using var httpClient = new HttpClient();
var opa = new OpaClient(httpClient);

var inputData = new
{
    user = new
    {
        id = "alice",
        roles = new[] { "editor" }
    },
    action = "write",
    resource = new
    {
        id = "doc-123",
        owner = "bob",
        @public = false
    }
};

if (await opa.CheckAsync("authz/allow", inputData))
{
    // Access granted
}
```

### OPA with ABAC Policies

```rego
# abac_policy.rego
package abac

import future.keywords.if
import future.keywords.in

default allow := false

# Time-based access
allow if {
    input.action == "read"
    is_business_hours
    user_in_same_department
}

is_business_hours if {
    time.hour(time.now_ns()) >= 9
    time.hour(time.now_ns()) <= 17
    time.weekday(time.now_ns()) < 5
}

user_in_same_department if {
    input.user.department == input.resource.department
}

# Expense approval rules
allow if {
    input.action == "approve"
    input.resource.type == "expense"
    can_approve_amount
}

can_approve_amount if {
    input.resource.amount <= 1000
    "employee" in input.user.roles
}

can_approve_amount if {
    input.resource.amount <= 10000
    "manager" in input.user.roles
}

can_approve_amount if {
    "director" in input.user.roles
}
```

## Authorization Libraries and Tools

### Comparison

| Tool | Model | Language | Best For |
|------|-------|----------|----------|
| **OPA** | ABAC/Policy | Rego | Kubernetes, microservices |
| **Casbin** | RBAC/ABAC/ACL | Multi-language | General purpose |
| **Oso** | ABAC/ReBAC | Polar | Application embedding |
| **SpiceDB** | ReBAC (Zanzibar) | gRPC | Large-scale permissions |
| **Cerbos** | ABAC | YAML | Cloud-native apps |

### Casbin Quick Start

```csharp
using Casbin;

// Define model (model.conf)
/*
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
*/

// Create enforcer
var enforcer = new Enforcer("model.conf", "policy.csv");

// Check permission
if (enforcer.Enforce("alice", "data1", "read"))
{
    // Access granted
}

// Add policy dynamically
await enforcer.AddPolicyAsync("bob", "data2", "write");
await enforcer.AddGroupingPolicyAsync("alice", "admin");

// For ASP.NET Core integration, use Casbin.AspNetCore
// services.AddCasbinAuthorization(options =>
// {
//     options.DefaultModelPath = "model.conf";
//     options.DefaultPolicyPath = "policy.csv";
// });
```

## Best Practices

### Design Principles

1. **Principle of Least Privilege**: Grant minimum permissions necessary
2. **Separation of Duties**: Require multiple parties for sensitive operations
3. **Defense in Depth**: Layer authorization checks at multiple levels
4. **Fail Secure**: Deny access when authorization state is unclear
5. **Centralize Logic**: Single policy decision point (PDP)
6. **Audit Everything**: Log all authorization decisions

### Implementation Guidelines

```csharp
// Good: Centralized authorization
public interface IAuditLogger
{
    Task LogAsync(string userId, string resourceId, string action, string decision, object? context);
}

/// <summary>
/// Centralized authorization service - single entry point for all decisions.
/// </summary>
public sealed class AuthorizationService(AbacEngine engine, IAuditLogger auditLogger)
{
    /// <summary>
    /// Single entry point for all authorization decisions.
    /// </summary>
    public async Task<bool> AuthorizeAsync(AccessRequest request)
    {
        var decision = engine.Evaluate(request);

        // Always audit
        await auditLogger.LogAsync(
            userId: request.GetSubjectAttribute<string>("user_id") ?? "unknown",
            resourceId: request.GetResourceAttribute<string>("id") ?? "unknown",
            action: request.Action,
            decision: decision ? "permit" : "deny",
            context: request.Environment
        );

        return decision;
    }
}

// Bad: Scattered authorization checks
public Document? GetDocument(string docId, User user)
{
    var doc = _repository.GetById(docId);
    // Authorization logic duplicated everywhere - avoid this pattern!
    if (user.Role == "admin" || doc?.OwnerId == user.Id)
    {
        return doc;
    }
    return null;
}
```

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Hardcoded roles | Inflexible, hard to change | Use permission-based checks |
| Missing negative tests | False sense of security | Test deny cases explicitly |
| Client-side only | Easily bypassed | Always enforce server-side |
| Overly complex policies | Hard to audit | Keep policies simple, composable |
| No audit trail | Can't investigate incidents | Log all decisions |

## Related Skills

- `authentication-patterns` - Verify identity before authorization
- `api-security` - Apply authorization at API boundaries
- `zero-trust` - Never trust, always verify architecture
- `secure-coding` - Prevent authorization bypass vulnerabilities

## References

**Deep Dives:**

- [RBAC Patterns](references/rbac-patterns.md) - Advanced RBAC with constraints
- [ABAC Implementation](references/abac-implementation.md) - Full XACML-style engine
- [Policy-as-Code](references/policy-as-code.md) - OPA, Cerbos, and testing patterns

## Security Checklist

### Design Phase

- [ ] Authorization model chosen based on requirements
- [ ] Principle of least privilege applied
- [ ] Roles/permissions documented
- [ ] Edge cases identified (inheritance, delegation)

### Implementation Phase

- [ ] Authorization centralized (single PDP)
- [ ] Server-side enforcement
- [ ] Consistent authorization checks on all endpoints
- [ ] Audit logging implemented

### Testing Phase

- [ ] Positive tests (allowed access works)
- [ ] Negative tests (denied access blocked)
- [ ] Privilege escalation tests
- [ ] Role hierarchy tests

### Operations Phase

- [ ] Regular permission reviews
- [ ] Unused roles/permissions removed
- [ ] Audit logs monitored
- [ ] Incident response plan for auth failures
