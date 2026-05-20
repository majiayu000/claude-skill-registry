---
name: permission-authorization
description: "Implements permission-based authorization with custom attributes, policy providers, and authorization handlers. Provides granular access control beyond simple role-based authorization."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Microsoft.AspNetCore.Authorization
---

# Permission-Based Authorization Setup

## Overview

This skill implements fine-grained permission-based authorization:

- **Custom [HasPermission] attribute** - Declarative permission requirements
- **Policy provider** - Dynamically creates policies from permissions
- **Authorization handler** - Validates user permissions
- **Claims transformation** - Converts roles to permissions

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `Permissions` | Static permission constants |
| `Roles` | Static role constants |
| `HasPermissionAttribute` | Custom authorize attribute |
| `PermissionAuthorizationHandler` | Validates permissions |
| `PermissionAuthorizationPolicyProvider` | Creates policies dynamically |
| `RoleToPermissionClaimsTransformation` | Maps roles to permissions |

---

## Authorization Structure

```
/Infrastructure/Authorization/
├── Permissions.cs
├── Roles.cs
├── HasPermissionAttribute.cs
├── PermissionRequirement.cs
├── PermissionAuthorizationHandler.cs
├── PermissionAuthorizationPolicyProvider.cs
├── RoleToPermissionClaimsTransformation.cs
└── AuthorizationExtensions.cs
```

---

## Template: Permissions Definition

```csharp
// src/{name}.infrastructure/Authorization/Permissions.cs
namespace {name}.infrastructure.authorization;

/// <summary>
/// All available permissions in the system
/// Format: {resource}:{action}
/// </summary>
public static class Permissions
{
    // ═══════════════════════════════════════════════════════════════
    // ORGANIZATION PERMISSIONS
    // ═══════════════════════════════════════════════════════════════
    public const string OrganizationsRead = "organizations:read";
    public const string OrganizationsWrite = "organizations:write";
    public const string OrganizationsDelete = "organizations:delete";
    public const string OrganizationsManageSettings = "organizations:manage_settings";

    // ═══════════════════════════════════════════════════════════════
    // USER PERMISSIONS
    // ═══════════════════════════════════════════════════════════════
    public const string UsersRead = "users:read";
    public const string UsersWrite = "users:write";
    public const string UsersDelete = "users:delete";
    public const string UsersManageRoles = "users:manage_roles";

    // ═══════════════════════════════════════════════════════════════
    // DEPARTMENT PERMISSIONS
    // ═══════════════════════════════════════════════════════════════
    public const string DepartmentsRead = "departments:read";
    public const string DepartmentsWrite = "departments:write";
    public const string DepartmentsDelete = "departments:delete";

    // ═══════════════════════════════════════════════════════════════
    // ASSESSMENT PERMISSIONS
    // ═══════════════════════════════════════════════════════════════
    public const string AssessmentsRead = "assessments:read";
    public const string AssessmentsWrite = "assessments:write";
    public const string AssessmentsSubmit = "assessments:submit";
    public const string AssessmentsReview = "assessments:review";

    // ═══════════════════════════════════════════════════════════════
    // REPORT PERMISSIONS
    // ═══════════════════════════════════════════════════════════════
    public const string ReportsRead = "reports:read";
    public const string ReportsExport = "reports:export";
    public const string ReportsViewSensitive = "reports:view_sensitive";

    // ═══════════════════════════════════════════════════════════════
    // ADMIN PERMISSIONS
    // ═══════════════════════════════════════════════════════════════
    public const string AdminAccess = "admin:access";
    public const string AdminManageSystem = "admin:manage_system";
}
```

---

## Template: Roles Definition

```csharp
// src/{name}.infrastructure/Authorization/Roles.cs
namespace {name}.infrastructure.authorization;

/// <summary>
/// All available roles in the system
/// </summary>
public static class Roles
{
    public const string SuperAdmin = "SuperAdmin";
    public const string Admin = "Admin";
    public const string Consultant = "Consultant";
    public const string Manager = "Manager";
    public const string Associate = "Associate";
    public const string Viewer = "Viewer";
}
```

---

## Template: Role-Permission Mapping

```csharp
// src/{name}.infrastructure/Authorization/RolePermissions.cs
namespace {name}.infrastructure.authorization;

/// <summary>
/// Maps roles to their granted permissions
/// </summary>
public static class RolePermissions
{
    private static readonly Dictionary<string, HashSet<string>> RolePermissionMap = new()
    {
        // ═══════════════════════════════════════════════════════════════
        // SUPER ADMIN - Full system access
        // ═══════════════════════════════════════════════════════════════
        [Roles.SuperAdmin] = new HashSet<string>
        {
            Permissions.OrganizationsRead,
            Permissions.OrganizationsWrite,
            Permissions.OrganizationsDelete,
            Permissions.OrganizationsManageSettings,
            Permissions.UsersRead,
            Permissions.UsersWrite,
            Permissions.UsersDelete,
            Permissions.UsersManageRoles,
            Permissions.DepartmentsRead,
            Permissions.DepartmentsWrite,
            Permissions.DepartmentsDelete,
            Permissions.AssessmentsRead,
            Permissions.AssessmentsWrite,
            Permissions.AssessmentsSubmit,
            Permissions.AssessmentsReview,
            Permissions.ReportsRead,
            Permissions.ReportsExport,
            Permissions.ReportsViewSensitive,
            Permissions.AdminAccess,
            Permissions.AdminManageSystem
        },

        // ═══════════════════════════════════════════════════════════════
        // ADMIN - Organization-level admin
        // ═══════════════════════════════════════════════════════════════
        [Roles.Admin] = new HashSet<string>
        {
            Permissions.OrganizationsRead,
            Permissions.OrganizationsWrite,
            Permissions.OrganizationsManageSettings,
            Permissions.UsersRead,
            Permissions.UsersWrite,
            Permissions.UsersManageRoles,
            Permissions.DepartmentsRead,
            Permissions.DepartmentsWrite,
            Permissions.DepartmentsDelete,
            Permissions.AssessmentsRead,
            Permissions.AssessmentsWrite,
            Permissions.AssessmentsReview,
            Permissions.ReportsRead,
            Permissions.ReportsExport,
            Permissions.ReportsViewSensitive,
            Permissions.AdminAccess
        },

        // ═══════════════════════════════════════════════════════════════
        // CONSULTANT - External consultants
        // ═══════════════════════════════════════════════════════════════
        [Roles.Consultant] = new HashSet<string>
        {
            Permissions.OrganizationsRead,
            Permissions.UsersRead,
            Permissions.DepartmentsRead,
            Permissions.AssessmentsRead,
            Permissions.AssessmentsReview,
            Permissions.ReportsRead,
            Permissions.ReportsExport
        },

        // ═══════════════════════════════════════════════════════════════
        // MANAGER - Department managers
        // ═══════════════════════════════════════════════════════════════
        [Roles.Manager] = new HashSet<string>
        {
            Permissions.OrganizationsRead,
            Permissions.UsersRead,
            Permissions.DepartmentsRead,
            Permissions.DepartmentsWrite,
            Permissions.AssessmentsRead,
            Permissions.AssessmentsWrite,
            Permissions.AssessmentsSubmit,
            Permissions.AssessmentsReview,
            Permissions.ReportsRead
        },

        // ═══════════════════════════════════════════════════════════════
        // ASSOCIATE - Regular employees
        // ═══════════════════════════════════════════════════════════════
        [Roles.Associate] = new HashSet<string>
        {
            Permissions.OrganizationsRead,
            Permissions.UsersRead,
            Permissions.DepartmentsRead,
            Permissions.AssessmentsRead,
            Permissions.AssessmentsSubmit
        },

        // ═══════════════════════════════════════════════════════════════
        // VIEWER - Read-only access
        // ═══════════════════════════════════════════════════════════════
        [Roles.Viewer] = new HashSet<string>
        {
            Permissions.OrganizationsRead,
            Permissions.DepartmentsRead,
            Permissions.AssessmentsRead,
            Permissions.ReportsRead
        }
    };

    /// <summary>
    /// Gets all permissions for a role
    /// </summary>
    public static IReadOnlySet<string> GetPermissionsForRole(string role)
    {
        return RolePermissionMap.TryGetValue(role, out var permissions)
            ? permissions
            : new HashSet<string>();
    }

    /// <summary>
    /// Gets all permissions for multiple roles
    /// </summary>
    public static IReadOnlySet<string> GetPermissionsForRoles(IEnumerable<string> roles)
    {
        var allPermissions = new HashSet<string>();

        foreach (var role in roles)
        {
            var permissions = GetPermissionsForRole(role);
            allPermissions.UnionWith(permissions);
        }

        return allPermissions;
    }

    /// <summary>
    /// Checks if a role has a specific permission
    /// </summary>
    public static bool HasPermission(string role, string permission)
    {
        return RolePermissionMap.TryGetValue(role, out var permissions)
            && permissions.Contains(permission);
    }
}
```

---

## Template: HasPermission Attribute

```csharp
// src/{name}.infrastructure/Authorization/HasPermissionAttribute.cs
using Microsoft.AspNetCore.Authorization;

namespace {name}.infrastructure.authorization;

/// <summary>
/// Custom authorization attribute that requires a specific permission
/// </summary>
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method, AllowMultiple = true)]
public sealed class HasPermissionAttribute : AuthorizeAttribute
{
    public HasPermissionAttribute(string permission)
        : base(policy: permission)
    {
    }
}
```

---

## Template: Permission Requirement

```csharp
// src/{name}.infrastructure/Authorization/PermissionRequirement.cs
using Microsoft.AspNetCore.Authorization;

namespace {name}.infrastructure.authorization;

/// <summary>
/// Authorization requirement for a specific permission
/// </summary>
public sealed class PermissionRequirement : IAuthorizationRequirement
{
    public string Permission { get; }

    public PermissionRequirement(string permission)
    {
        Permission = permission;
    }
}
```

---

## Template: Permission Authorization Handler

```csharp
// src/{name}.infrastructure/Authorization/PermissionAuthorizationHandler.cs
using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;

namespace {name}.infrastructure.authorization;

/// <summary>
/// Handles permission-based authorization requirements
/// </summary>
internal sealed class PermissionAuthorizationHandler 
    : AuthorizationHandler<PermissionRequirement>
{
    private readonly ILogger<PermissionAuthorizationHandler> _logger;

    public PermissionAuthorizationHandler(
        ILogger<PermissionAuthorizationHandler> logger)
    {
        _logger = logger;
    }

    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        PermissionRequirement requirement)
    {
        // Get permissions from claims (added by claims transformation)
        var permissions = context.User
            .FindAll("permission")
            .Select(c => c.Value)
            .ToHashSet();

        if (permissions.Contains(requirement.Permission))
        {
            _logger.LogDebug(
                "User {UserId} authorized for permission {Permission}",
                context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value,
                requirement.Permission);

            context.Succeed(requirement);
        }
        else
        {
            _logger.LogWarning(
                "User {UserId} denied permission {Permission}. User has permissions: {Permissions}",
                context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value,
                requirement.Permission,
                string.Join(", ", permissions));
        }

        return Task.CompletedTask;
    }
}
```

---

## Template: Permission Policy Provider

```csharp
// src/{name}.infrastructure/Authorization/PermissionAuthorizationPolicyProvider.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Options;

namespace {name}.infrastructure.authorization;

/// <summary>
/// Dynamically creates authorization policies based on permission names
/// </summary>
internal sealed class PermissionAuthorizationPolicyProvider 
    : DefaultAuthorizationPolicyProvider
{
    private readonly AuthorizationOptions _options;

    public PermissionAuthorizationPolicyProvider(
        IOptions<AuthorizationOptions> options)
        : base(options)
    {
        _options = options.Value;
    }

    public override async Task<AuthorizationPolicy?> GetPolicyAsync(string policyName)
    {
        // First check if policy exists in options
        var policy = await base.GetPolicyAsync(policyName);

        if (policy is not null)
        {
            return policy;
        }

        // If not found, create a permission-based policy
        // Policy name is the permission (e.g., "users:read")
        policy = new AuthorizationPolicyBuilder()
            .AddRequirements(new PermissionRequirement(policyName))
            .Build();

        // Cache the policy
        _options.AddPolicy(policyName, policy);

        return policy;
    }
}
```

---

## Template: Claims Transformation

```csharp
// src/{name}.infrastructure/Authorization/RoleToPermissionClaimsTransformation.cs
using System.Security.Claims;
using Microsoft.AspNetCore.Authentication;

namespace {name}.infrastructure.authorization;

/// <summary>
/// Transforms role claims into permission claims
/// </summary>
internal sealed class RoleToPermissionClaimsTransformation 
    : IClaimsTransformation
{
    public Task<ClaimsPrincipal> TransformAsync(ClaimsPrincipal principal)
    {
        // Get all role claims
        var roles = principal
            .FindAll(ClaimTypes.Role)
            .Select(c => c.Value)
            .ToList();

        if (!roles.Any())
        {
            return Task.FromResult(principal);
        }

        // Get permissions for all roles
        var permissions = RolePermissions.GetPermissionsForRoles(roles);

        // Create new identity with permission claims
        var identity = principal.Identity as ClaimsIdentity;

        if (identity is null)
        {
            return Task.FromResult(principal);
        }

        // Add permission claims (only if not already present)
        foreach (var permission in permissions)
        {
            if (!principal.HasClaim("permission", permission))
            {
                identity.AddClaim(new Claim("permission", permission));
            }
        }

        return Task.FromResult(principal);
    }
}
```

---

## Template: Authorization Registration

```csharp
// src/{name}.infrastructure/Authorization/AuthorizationExtensions.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.DependencyInjection;

namespace {name}.infrastructure.authorization;

public static class AuthorizationExtensions
{
    public static IServiceCollection AddPermissionAuthorization(
        this IServiceCollection services)
    {
        // Register policy provider
        services.AddSingleton<IAuthorizationPolicyProvider, 
            PermissionAuthorizationPolicyProvider>();

        // Register authorization handler
        services.AddScoped<IAuthorizationHandler, 
            PermissionAuthorizationHandler>();

        // Register claims transformation
        services.AddScoped<IClaimsTransformation, 
            RoleToPermissionClaimsTransformation>();

        // Configure authorization
        services.AddAuthorization(options =>
        {
            // Default policy requires authentication
            options.DefaultPolicy = new AuthorizationPolicyBuilder()
                .RequireAuthenticatedUser()
                .Build();

            // Fallback policy for endpoints without [Authorize]
            options.FallbackPolicy = null;  // Allow anonymous by default

            // Add named policies for common scenarios
            options.AddPolicy("AdminOnly", policy =>
                policy.RequireRole(Roles.SuperAdmin, Roles.Admin));

            options.AddPolicy("ManagerOrAbove", policy =>
                policy.RequireRole(Roles.SuperAdmin, Roles.Admin, Roles.Manager));
        });

        return services;
    }
}
```

---

## Usage in Controllers

```csharp
// src/{name}.api/Controllers/Users/UserController.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using {name}.infrastructure.authorization;

[Authorize]  // Requires authentication
[ApiController]
[Route("api/v1/users")]
public class UserController : ControllerBase
{
    // ═══════════════════════════════════════════════════════════════
    // PUBLIC: Any authenticated user
    // ═══════════════════════════════════════════════════════════════
    [HttpGet("{id}")]
    [HasPermission(Permissions.UsersRead)]
    public async Task<IActionResult> GetById(Guid id) { }

    // ═══════════════════════════════════════════════════════════════
    // CREATE: Requires write permission
    // ═══════════════════════════════════════════════════════════════
    [HttpPost]
    [HasPermission(Permissions.UsersWrite)]
    public async Task<IActionResult> Create([FromBody] CreateUserRequest request) { }

    // ═══════════════════════════════════════════════════════════════
    // DELETE: Requires delete permission
    // ═══════════════════════════════════════════════════════════════
    [HttpDelete("{id}")]
    [HasPermission(Permissions.UsersDelete)]
    public async Task<IActionResult> Delete(Guid id) { }

    // ═══════════════════════════════════════════════════════════════
    // MULTIPLE PERMISSIONS: All required
    // ═══════════════════════════════════════════════════════════════
    [HttpPost("{id}/roles")]
    [HasPermission(Permissions.UsersWrite)]
    [HasPermission(Permissions.UsersManageRoles)]
    public async Task<IActionResult> AssignRole(Guid id, [FromBody] AssignRoleRequest request) { }

    // ═══════════════════════════════════════════════════════════════
    // ROLE-BASED: Use built-in attribute
    // ═══════════════════════════════════════════════════════════════
    [HttpGet("admin/dashboard")]
    [Authorize(Roles = Roles.SuperAdmin + "," + Roles.Admin)]
    public async Task<IActionResult> GetAdminDashboard() { }

    // ═══════════════════════════════════════════════════════════════
    // NAMED POLICY
    // ═══════════════════════════════════════════════════════════════
    [HttpDelete("organization/{orgId}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> DeleteOrganization(Guid orgId) { }
}
```

---

## Usage in Handlers (Imperative)

```csharp
// src/{name}.application/{Feature}/DoSomething/DoSomethingCommandHandler.cs
using Microsoft.AspNetCore.Authorization;
using {name}.application.abstractions.authentication;

internal sealed class DoSomethingCommandHandler 
    : ICommandHandler<DoSomethingCommand, Guid>
{
    private readonly IUserContext _userContext;
    private readonly IAuthorizationService _authorizationService;

    public DoSomethingCommandHandler(
        IUserContext userContext,
        IAuthorizationService authorizationService)
    {
        _userContext = userContext;
        _authorizationService = authorizationService;
    }

    public async Task<Result<Guid>> Handle(
        DoSomethingCommand request,
        CancellationToken cancellationToken)
    {
        // Check permission imperatively
        var authResult = await _authorizationService.AuthorizeAsync(
            _userContext.User,
            Permissions.SomethingWrite);

        if (!authResult.Succeeded)
        {
            return Result.Failure<Guid>(CommonErrors.Forbidden);
        }

        // Continue with operation...
    }
}
```

---

## Resource-Based Authorization

```csharp
// src/{name}.infrastructure/Authorization/DocumentAuthorizationHandler.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authorization.Infrastructure;

/// <summary>
/// Authorizes access to documents based on ownership
/// </summary>
internal sealed class DocumentAuthorizationHandler 
    : AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        var userId = context.User.FindFirst("sub")?.Value;

        if (string.IsNullOrEmpty(userId))
        {
            return Task.CompletedTask;
        }

        // Owner can do anything
        if (resource.OwnerId.ToString() == userId)
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        // Others need explicit permission based on operation
        if (requirement.Name == Operations.Read.Name)
        {
            if (context.User.HasClaim("permission", Permissions.DocumentsRead))
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}

// Define operations
public static class Operations
{
    public static readonly OperationAuthorizationRequirement Create = new() { Name = "Create" };
    public static readonly OperationAuthorizationRequirement Read = new() { Name = "Read" };
    public static readonly OperationAuthorizationRequirement Update = new() { Name = "Update" };
    public static readonly OperationAuthorizationRequirement Delete = new() { Name = "Delete" };
}
```

---

## Critical Rules

1. **Use constants for permissions** - No magic strings
2. **Permission naming convention** - `{resource}:{action}`
3. **Roles aggregate permissions** - Don't check roles directly
4. **Claims transformation** - Convert roles to permissions early
5. **Cache policies** - Policy provider caches dynamically created policies
6. **Multiple attributes = AND** - All permissions required
7. **Log authorization failures** - For security auditing
8. **Don't trust client claims** - Always validate on server
9. **Separate authn from authz** - Authentication ≠ Authorization
10. **Resource-based when needed** - For ownership checks

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Checking roles directly in code
if (user.IsInRole("Admin") || user.IsInRole("Manager"))
{
    // This scatters role logic everywhere
}

// ✅ CORRECT: Check permission
[HasPermission(Permissions.UsersWrite)]
public async Task<IActionResult> CreateUser() { }

// ❌ WRONG: Magic strings for permissions
[Authorize(Policy = "users:write")]  // Typo risk!

// ✅ CORRECT: Use constants
[HasPermission(Permissions.UsersWrite)]

// ❌ WRONG: Trusting client-provided permissions
var permissions = request.UserPermissions;  // Client can't set permissions!

// ✅ CORRECT: Derive from authenticated roles
// Claims transformation handles this automatically
```

---

## Related Skills

- `jwt-authentication` - Authentication setup
- `api-controller-generator` - Protected endpoints
- `dotnet-clean-architecture` - Infrastructure layer
