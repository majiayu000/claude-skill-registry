---
name: aauth
description: AAuth Laravel RBAC package implementation assistant
---

# AAuth Implementation Guide

AAuth is a Laravel RBAC package with organization hierarchy and parametric permissions.

## Installation

```bash
composer require aurora-web-software/aauth
```

```bash
php artisan vendor:publish --tag=aauth-config
php artisan vendor:publish --tag=aauth-migrations
php artisan migrate
```

## Step 1: Prepare User Model

Your User model must implement `AAuthUserContract`:

```php
<?php

namespace App\Models;

use AuroraWebSoftware\AAuth\Contracts\AAuthUserContract;
use AuroraWebSoftware\AAuth\Traits\AAuthUser;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements AAuthUserContract
{
    use AAuthUser;

    // Your existing code...
}
```

## Step 2: Basic Permission Checks

### In Controllers

```php
use AuroraWebSoftware\AAuth\Facades\AAuth;

class PostController extends Controller
{
    public function edit(Post $post)
    {
        // Simple permission check
        if (!AAuth::can('edit-post')) {
            abort(403);
        }

        return view('posts.edit', compact('post'));
    }

    public function approve(Post $post)
    {
        // Parametric permission - check if user can approve this amount
        if (!AAuth::can('approve-budget', [$post->amount])) {
            abort(403, 'Budget limit exceeded');
        }

        $post->approve();
        return redirect()->back();
    }
}
```

### Using passOrAbort (Shortcut)

```php
public function edit(Post $post)
{
    AAuth::passOrAbort('edit-post');

    return view('posts.edit', compact('post'));
}
```

## Step 3: Middleware Usage

### Register Middleware (Laravel 11+)

```php
// bootstrap/app.php
->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'aauth.permission' => \AuroraWebSoftware\AAuth\Http\Middleware\AAuthPermission::class,
        'aauth.role' => \AuroraWebSoftware\AAuth\Http\Middleware\AAuthRole::class,
    ]);
})
```

### Apply to Routes

```php
// Permission middleware
Route::get('/posts/{post}/edit', [PostController::class, 'edit'])
    ->middleware('aauth.permission:edit-post');

// Role middleware
Route::get('/admin/dashboard', [AdminController::class, 'index'])
    ->middleware('aauth.role:admin');

// Multiple permissions
Route::resource('users', UserController::class)
    ->middleware('aauth.permission:manage-users');
```

## Step 4: Blade Directives

```blade
{{-- Show only if user has permission --}}
@aauth('edit-post')
    <a href="{{ route('posts.edit', $post) }}">Edit</a>
@endaauth

{{-- With parametric permission --}}
@aauth('approve-budget', [1000])
    <button>Approve</button>
@endaauth
```

## Step 5: Role Management

### Create Roles

```php
use AuroraWebSoftware\AAuth\Models\Role;

// System role (global, no organization)
$adminRole = Role::create([
    'name' => 'admin',
    'type' => 'system',
    'status' => 'active',
]);

// Organization role (tied to organization hierarchy)
$managerRole = Role::create([
    'name' => 'manager',
    'type' => 'organization',
    'organization_scope_id' => $scopeId,
    'status' => 'active',
]);
```

### Assign Permissions to Role

```php
use AuroraWebSoftware\AAuth\Services\RolePermissionService;

$service = app(RolePermissionService::class);

// Simple permission
$service->givePermissionToRole($roleId, 'edit-post');

// Parametric permission with max value
$service->givePermissionToRole($roleId, 'approve-budget', [
    'max_amount' => 5000
]);

// Parametric permission with allowed values
$service->givePermissionToRole($roleId, 'manage-department', [
    'departments' => ['HR', 'IT', 'Finance']
]);
```

### Assign Role to User

```php
$service->attachRoleToUser($user, $roleId, $organizationNodeId);
```

## Step 6: Organization Hierarchy (Optional)

### Create Organization Scope

```php
use AuroraWebSoftware\AAuth\Models\OrganizationScope;

// Define hierarchy levels
OrganizationScope::create(['name' => 'Company', 'level' => 1]);
OrganizationScope::create(['name' => 'Department', 'level' => 2]);
OrganizationScope::create(['name' => 'Team', 'level' => 3]);
```

### Create Organization Nodes

```php
use AuroraWebSoftware\AAuth\Models\OrganizationNode;

// Root node
$company = OrganizationNode::create([
    'name' => 'Acme Corp',
    'organization_scope_id' => 1,
    'path' => '1',
]);

// Child nodes
$hrDept = OrganizationNode::create([
    'name' => 'HR Department',
    'organization_scope_id' => 2,
    'parent_id' => $company->id,
    'path' => '1/2',
]);
```

### Query User's Accessible Nodes

```php
// Get all accessible organization nodes
$nodes = AAuth::organizationNodes();

// With query builder for custom filters
$nodes = AAuth::organizationNodesQuery()
    ->where('organization_scope_id', 2)
    ->get();

// Check if node is descendant
if (AAuth::descendant($parentNodeId, $childNodeId)) {
    // User can access this node
}
```

## Step 7: Caching Configuration

Edit `config/aauth-advanced.php`:

```php
'cache' => [
    'enabled' => env('AAUTH_CACHE_ENABLED', true),
    'store' => env('AAUTH_CACHE_STORE', null), // null = default driver
    'ttl' => env('AAUTH_CACHE_TTL', 3600),
    'prefix' => env('AAUTH_CACHE_PREFIX', 'aauth'),
],
```

In `.env`:
```
AAUTH_CACHE_ENABLED=true
AAUTH_CACHE_STORE=redis
AAUTH_CACHE_TTL=3600
```

## Step 8: Super Admin (Optional)

Enable users to bypass all permission checks:

```php
// config/aauth-advanced.php
'super_admin' => [
    'enabled' => env('AAUTH_SUPER_ADMIN_ENABLED', true),
    'column' => 'is_super_admin',
],
```

Add column to users table:
```php
$table->boolean('is_super_admin')->default(false);
```

## Common Scenarios

### Scenario 1: Blog with Roles

```php
// Create roles
$adminRole = Role::create(['name' => 'admin', 'type' => 'system', 'status' => 'active']);
$editorRole = Role::create(['name' => 'editor', 'type' => 'system', 'status' => 'active']);
$authorRole = Role::create(['name' => 'author', 'type' => 'system', 'status' => 'active']);

// Assign permissions
$service->givePermissionToRole($adminRole->id, 'manage-users');
$service->givePermissionToRole($adminRole->id, 'manage-posts');
$service->givePermissionToRole($editorRole->id, 'edit-any-post');
$service->givePermissionToRole($authorRole->id, 'create-post');
$service->givePermissionToRole($authorRole->id, 'edit-own-post');
```

### Scenario 2: Multi-Tenant with Budget Limits

```php
// Department manager can approve up to 10,000
$service->givePermissionToRole($deptManagerRole->id, 'approve-budget', [
    'max_amount' => 10000
]);

// Team lead can approve up to 1,000
$service->givePermissionToRole($teamLeadRole->id, 'approve-budget', [
    'max_amount' => 1000
]);

// In controller
public function approvePurchase(Purchase $purchase)
{
    if (!AAuth::can('approve-budget', [$purchase->amount])) {
        abort(403, 'Amount exceeds your approval limit');
    }

    $purchase->approve();
}
```

### Scenario 3: Department-Based Access

```php
// Give access to specific departments
$service->givePermissionToRole($roleId, 'view-reports', [
    'departments' => ['HR', 'Finance']
]);

// Check access
if (AAuth::can('view-reports', ['HR'])) {
    // Can view HR reports
}
```

## Helper Functions

```php
// Global helper function
if (aauth_can('edit-post')) {
    // ...
}

// With parameters
if (aauth_can('approve-budget', [5000])) {
    // ...
}
```

## Troubleshooting

### Permission Not Working

1. **Clear cache**: `php artisan cache:clear`
2. **Check role has permission**:
   ```php
   $role = Role::find($roleId);
   dd($role->rolePermissions);
   ```
3. **Check user has role**:
   ```php
   dd($user->roles);
   ```

### Cache Not Updating

```php
// Clear AAuth context manually
AAuth::clearContext();

// Or clear specific cache keys
Cache::forget('aauth:role:' . $roleId);
```

### Super Admin Not Working

Check your User model has the column:
```php
dd($user->is_super_admin);
```

Check config is enabled:
```php
dd(config('aauth-advanced.super_admin.enabled'));
```

## Quick Reference

### Permission Types

| Type | Role Parameter | Check Example |
|------|---------------|---------------|
| Simple | `null` | `AAuth::can('edit-post')` |
| Max Value | `['max_amount' => 5000]` | `AAuth::can('approve-budget', [3000])` |
| Boolean | `['is_admin' => true]` | `AAuth::can('admin-access', [true])` |
| Allowed Values | `['depts' => ['HR','IT']]` | `AAuth::can('view-dept', ['HR'])` |

### Essential Methods

| Method | Description |
|--------|-------------|
| `AAuth::can($permission, $params)` | Check permission |
| `AAuth::passOrAbort($permission)` | Check or 403 |
| `AAuth::currentRole()` | Get active role |
| `AAuth::switchableRoles()` | Get user's roles |
| `AAuth::organizationNodes()` | Get accessible nodes |
| `AAuth::clearContext()` | Clear cached context |

### Middleware

| Middleware | Usage |
|------------|-------|
| `aauth.permission:edit-post` | Check permission |
| `aauth.role:admin` | Check role name |
