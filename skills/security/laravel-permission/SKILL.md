---
name: laravel-permission
description: Spatie Laravel Permission - roles, permissions, middleware, Blade directives. Use when implementing RBAC, role-based access control, or user authorization.
user-invocable: false
---

# Laravel Permission (Spatie)

## Installation

```bash
composer require spatie/laravel-permission
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"
php artisan optimize:clear
php artisan migrate
```

---

## User Model Setup

```php
use Spatie\Permission\Traits\HasRoles;

class User extends Authenticatable
{
    use HasRoles;
}
```

---

## Create Roles & Permissions

```php
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;

// Roles
$admin = Role::create(['name' => 'admin']);
$writer = Role::create(['name' => 'writer']);

// Permissions
Permission::create(['name' => 'edit articles']);
Permission::create(['name' => 'publish articles']);

// Assign permissions to role
$admin->givePermissionTo(['edit articles', 'publish articles']);
```

---

## Assign to Users

```php
// Assign role
$user->assignRole('writer');
$user->assignRole(['writer', 'admin']);

// Direct permissions
$user->givePermissionTo('edit articles');

// Sync (replace all)
$user->syncRoles(['writer']);
$user->syncPermissions(['edit articles']);

// Remove
$user->removeRole('writer');
$user->revokePermissionTo('edit articles');
```

---

## Check Permissions

```php
// Check role
$user->hasRole('admin');
$user->hasAnyRole(['writer', 'admin']);
$user->hasAllRoles(['writer', 'admin']);

// Check permission
$user->hasPermissionTo('edit articles');
$user->can('edit articles');

// Get all
$user->getRoleNames();
$user->getPermissionNames();
```

---

## Middleware

```php
// routes/web.php
Route::middleware(['role:admin'])->group(function () {
    Route::get('/admin', [AdminController::class, 'index']);
});

Route::middleware(['permission:publish articles'])->group(function () {
    Route::post('/publish', [ArticleController::class, 'publish']);
});

// Role OR permission
Route::middleware(['role_or_permission:admin|edit articles'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});
```

---

## Blade Directives

```blade
@role('admin')
    <a href="/admin">Admin Panel</a>
@endrole

@hasrole('writer|admin')
    <p>Editor access</p>
@endhasrole

@can('edit articles')
    <button>Edit</button>
@endcan

@canany(['edit articles', 'publish articles'])
    <div>Actions available</div>
@endcanany
```

---

## Seeder Example

```php
// database/seeders/RoleSeeder.php
public function run(): void
{
    $admin = Role::create(['name' => 'admin']);
    $admin->givePermissionTo(Permission::all());

    $writer = Role::create(['name' => 'writer']);
    $writer->givePermissionTo(['edit articles']);
}
```

---

## Best Practices

1. **Seed roles/permissions** in `DatabaseSeeder`
2. **Cache reset** after changes: `php artisan permission:cache-reset`
3. **Multi-guard** support in `config/permission.php`
4. **Teams** for multi-tenant: `'teams' => true`
5. **Naming** use kebab-case: `edit-articles`
