---
name: auth-rbac
description: Implementação de autenticação e controle de acesso baseado em roles (RBAC) em Laravel incluindo Guards, Policies, Gates, Permissions, Middleware de autorização, e integração com pacotes como Spatie Permission. Usar para implementar login/registro, controle de acesso por perfil, permissões granulares, proteção de rotas, e auditoria de acessos.
---

# Auth RBAC

Skill para autenticação e controle de acesso baseado em roles em Laravel.

## Conceitos Fundamentais

```
┌─────────────────────────────────────────────────────────────┐
│                    HIERARQUIA RBAC                          │
├─────────────────────────────────────────────────────────────┤
│  USER ──┬── ROLE ──┬── PERMISSION                          │
│         │          │                                        │
│  João ──┼── Admin ─┼── users.create                        │
│         │          ├── users.edit                          │
│         │          ├── users.delete                        │
│         │          └── contracts.*                         │
│         │                                                   │
│  Maria ─┼── Manager ┼── users.view                         │
│         │           ├── contracts.create                   │
│         │           └── contracts.edit                     │
│         │                                                   │
│  Pedro ─┴── Viewer ─┴── *.view                             │
└─────────────────────────────────────────────────────────────┘
```

## Setup com Spatie Permission

```bash
# Instalar pacote
composer require spatie/laravel-permission

# Publicar migrations e config
php artisan vendor:publish --provider="Spatie\Permission\PermissionServiceProvider"

# Rodar migrations
php artisan migrate
```

### Configurar Model User

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Spatie\Permission\Traits\HasRoles;

class User extends Authenticatable
{
    use HasRoles;

    // ...
}
```

### Criar Roles e Permissions

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;

class RolesAndPermissionsSeeder extends Seeder
{
    public function run(): void
    {
        // Reset cached roles and permissions
        app()[\Spatie\Permission\PermissionRegistrar::class]->forgetCachedPermissions();

        // Criar permissions
        $permissions = [
            // Users
            'users.view',
            'users.create',
            'users.edit',
            'users.delete',
            
            // Contracts
            'contracts.view',
            'contracts.create',
            'contracts.edit',
            'contracts.delete',
            'contracts.approve',
            
            // Payments
            'payments.view',
            'payments.create',
            'payments.process',
            
            // Reports
            'reports.view',
            'reports.export',
            
            // Settings
            'settings.view',
            'settings.edit',
        ];

        foreach ($permissions as $permission) {
            Permission::create(['name' => $permission]);
        }

        // Criar roles e atribuir permissions
        
        // Super Admin - todas as permissões
        $superAdmin = Role::create(['name' => 'super-admin']);
        $superAdmin->givePermissionTo(Permission::all());

        // Admin - quase tudo, exceto settings
        $admin = Role::create(['name' => 'admin']);
        $admin->givePermissionTo([
            'users.view', 'users.create', 'users.edit',
            'contracts.view', 'contracts.create', 'contracts.edit', 'contracts.delete', 'contracts.approve',
            'payments.view', 'payments.create', 'payments.process',
            'reports.view', 'reports.export',
        ]);

        // Manager - gerencia contratos e pagamentos
        $manager = Role::create(['name' => 'manager']);
        $manager->givePermissionTo([
            'users.view',
            'contracts.view', 'contracts.create', 'contracts.edit',
            'payments.view', 'payments.create',
            'reports.view',
        ]);

        // Operator - operações básicas
        $operator = Role::create(['name' => 'operator']);
        $operator->givePermissionTo([
            'contracts.view', 'contracts.create',
            'payments.view',
        ]);

        // Viewer - apenas visualização
        $viewer = Role::create(['name' => 'viewer']);
        $viewer->givePermissionTo([
            'contracts.view',
            'payments.view',
            'reports.view',
        ]);

        // Criar super admin inicial
        $user = \App\Models\User::factory()->create([
            'name' => 'Super Admin',
            'email' => 'admin@sistema.com',
        ]);
        $user->assignRole('super-admin');
    }
}
```

## Gates e Policies

### Definir Gates

```php
<?php
// app/Providers/AuthServiceProvider.php

namespace App\Providers;

use App\Models\Contract;
use App\Models\User;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;

class AuthServiceProvider extends ServiceProvider
{
    protected $policies = [
        Contract::class => \App\Policies\ContractPolicy::class,
    ];

    public function boot(): void
    {
        // Super admin bypassa todas as verificações
        Gate::before(function (User $user, string $ability) {
            if ($user->hasRole('super-admin')) {
                return true;
            }
        });

        // Gates customizados
        Gate::define('access-admin', function (User $user) {
            return $user->hasAnyRole(['super-admin', 'admin']);
        });

        Gate::define('view-reports', function (User $user) {
            return $user->hasPermissionTo('reports.view');
        });

        Gate::define('manage-team', function (User $user) {
            return $user->hasAnyRole(['super-admin', 'admin', 'manager']);
        });
    }
}
```

### Criar Policy

```php
<?php

namespace App\Policies;

use App\Models\Contract;
use App\Models\User;

class ContractPolicy
{
    /**
     * Antes de qualquer verificação
     */
    public function before(User $user, string $ability): ?bool
    {
        if ($user->hasRole('super-admin')) {
            return true;
        }
        return null; // Continua para os métodos específicos
    }

    /**
     * Pode listar contratos?
     */
    public function viewAny(User $user): bool
    {
        return $user->hasPermissionTo('contracts.view');
    }

    /**
     * Pode ver este contrato específico?
     */
    public function view(User $user, Contract $contract): bool
    {
        // Pode ver se tem permissão OU se é dono do contrato
        return $user->hasPermissionTo('contracts.view')
            || $contract->user_id === $user->id;
    }

    /**
     * Pode criar contratos?
     */
    public function create(User $user): bool
    {
        return $user->hasPermissionTo('contracts.create');
    }

    /**
     * Pode editar este contrato?
     */
    public function update(User $user, Contract $contract): bool
    {
        // Não pode editar contratos finalizados
        if ($contract->status === 'completed') {
            return false;
        }

        return $user->hasPermissionTo('contracts.edit')
            || $contract->user_id === $user->id;
    }

    /**
     * Pode excluir este contrato?
     */
    public function delete(User $user, Contract $contract): bool
    {
        // Só admin pode excluir
        return $user->hasPermissionTo('contracts.delete');
    }

    /**
     * Pode aprovar este contrato?
     */
    public function approve(User $user, Contract $contract): bool
    {
        // Não pode aprovar próprio contrato
        if ($contract->user_id === $user->id) {
            return false;
        }

        return $user->hasPermissionTo('contracts.approve');
    }
}
```

## Middleware de Autorização

### Registrar Middleware

```php
<?php
// bootstrap/app.php (Laravel 11)

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'role' => \Spatie\Permission\Middleware\RoleMiddleware::class,
        'permission' => \Spatie\Permission\Middleware\PermissionMiddleware::class,
        'role_or_permission' => \Spatie\Permission\Middleware\RoleOrPermissionMiddleware::class,
    ]);
})
```

### Proteger Rotas

```php
<?php
// routes/web.php

use Illuminate\Support\Facades\Route;

// Área administrativa - requer role admin
Route::middleware(['auth', 'role:admin|super-admin'])->prefix('admin')->group(function () {
    Route::get('/dashboard', [AdminController::class, 'dashboard']);
    Route::resource('users', UserController::class);
});

// Rotas por permissão
Route::middleware(['auth', 'permission:contracts.view'])->group(function () {
    Route::get('/contracts', [ContractController::class, 'index']);
});

Route::middleware(['auth', 'permission:contracts.create'])->group(function () {
    Route::get('/contracts/create', [ContractController::class, 'create']);
    Route::post('/contracts', [ContractController::class, 'store']);
});

// Múltiplas permissões (qualquer uma)
Route::middleware(['auth', 'permission:reports.view|reports.export'])->group(function () {
    Route::get('/reports', [ReportController::class, 'index']);
});

// Rotas de API com Sanctum
Route::middleware(['auth:sanctum', 'permission:api.access'])->prefix('api')->group(function () {
    Route::apiResource('contracts', Api\ContractController::class);
});
```

## Uso em Controllers

```php
<?php

namespace App\Http\Controllers;

use App\Models\Contract;
use Illuminate\Http\Request;

class ContractController extends Controller
{
    public function __construct()
    {
        // Autorização automática via Policy
        $this->authorizeResource(Contract::class, 'contract');
    }

    public function index()
    {
        // Policy: viewAny já verificada pelo authorizeResource
        $contracts = Contract::paginate();
        return view('contracts.index', compact('contracts'));
    }

    public function show(Contract $contract)
    {
        // Policy: view já verificada
        return view('contracts.show', compact('contract'));
    }

    public function approve(Contract $contract)
    {
        // Verificação manual para ação customizada
        $this->authorize('approve', $contract);
        
        $contract->update(['status' => 'approved']);
        
        return redirect()->back()->with('success', 'Contrato aprovado!');
    }

    public function massDelete(Request $request)
    {
        // Verificar permissão diretamente
        if (!auth()->user()->hasPermissionTo('contracts.delete')) {
            abort(403, 'Acesso negado');
        }

        Contract::whereIn('id', $request->ids)->delete();
        
        return response()->json(['message' => 'Contratos excluídos']);
    }
}
```

## Uso em Blade

```blade
{{-- Verificar Role --}}
@role('admin')
    <a href="/admin">Painel Admin</a>
@endrole

@hasrole('super-admin')
    <a href="/settings">Configurações</a>
@endhasrole

{{-- Verificar múltiplas roles --}}
@hasanyrole('admin|manager')
    <a href="/team">Gerenciar Equipe</a>
@endhasanyrole

{{-- Verificar Permission --}}
@can('contracts.create')
    <a href="/contracts/create" class="btn btn-primary">Novo Contrato</a>
@endcan

@cannot('contracts.delete')
    <span class="text-gray-400">Sem permissão para excluir</span>
@endcannot

{{-- Verificar Policy --}}
@can('update', $contract)
    <a href="{{ route('contracts.edit', $contract) }}">Editar</a>
@endcan

@can('approve', $contract)
    <form action="{{ route('contracts.approve', $contract) }}" method="POST">
        @csrf
        <button type="submit">Aprovar</button>
    </form>
@endcan

{{-- Menu dinâmico baseado em permissões --}}
<nav>
    @can('contracts.view')
        <a href="/contracts">Contratos</a>
    @endcan
    
    @can('payments.view')
        <a href="/payments">Pagamentos</a>
    @endcan
    
    @can('reports.view')
        <a href="/reports">Relatórios</a>
    @endcan
    
    @can('access-admin')
        <a href="/admin">Administração</a>
    @endcan
</nav>
```

## API de Gerenciamento

```php
<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;

class RoleController extends Controller
{
    public function index()
    {
        $roles = Role::with('permissions')->get();
        return view('admin.roles.index', compact('roles'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|unique:roles,name',
            'permissions' => 'array',
        ]);

        $role = Role::create(['name' => $request->name]);
        $role->syncPermissions($request->permissions ?? []);

        return redirect()->route('admin.roles.index')
            ->with('success', 'Role criada com sucesso!');
    }

    public function update(Request $request, Role $role)
    {
        $request->validate([
            'name' => 'required|unique:roles,name,' . $role->id,
            'permissions' => 'array',
        ]);

        $role->update(['name' => $request->name]);
        $role->syncPermissions($request->permissions ?? []);

        return redirect()->route('admin.roles.index')
            ->with('success', 'Role atualizada!');
    }
}

class UserRoleController extends Controller
{
    public function update(Request $request, User $user)
    {
        $request->validate([
            'roles' => 'array',
            'roles.*' => 'exists:roles,name',
        ]);

        // Sync roles (remove antigas, adiciona novas)
        $user->syncRoles($request->roles ?? []);

        return redirect()->back()->with('success', 'Roles atualizadas!');
    }

    public function addPermission(Request $request, User $user)
    {
        $request->validate([
            'permission' => 'required|exists:permissions,name',
        ]);

        // Permissão direta (além das roles)
        $user->givePermissionTo($request->permission);

        return redirect()->back()->with('success', 'Permissão adicionada!');
    }
}
```

## Auditoria de Acessos

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class AccessLog extends Model
{
    protected $fillable = [
        'user_id',
        'action',
        'resource',
        'resource_id',
        'ip_address',
        'user_agent',
        'granted',
        'metadata',
    ];

    protected $casts = [
        'granted' => 'boolean',
        'metadata' => 'array',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}

// Middleware de auditoria
class AuditAccess
{
    public function handle(Request $request, Closure $next)
    {
        $response = $next($request);

        if (auth()->check()) {
            AccessLog::create([
                'user_id' => auth()->id(),
                'action' => $request->method(),
                'resource' => $request->path(),
                'ip_address' => $request->ip(),
                'user_agent' => $request->userAgent(),
                'granted' => $response->status() < 400,
            ]);
        }

        return $response;
    }
}
```

## Hierarquia Militar (SKYNET-COPAC)

```php
<?php

namespace Database\Seeders;

use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;

class MilitaryRolesSeeder extends Seeder
{
    public function run(): void
    {
        // Hierarquia: Comandante > Oficial > Suboficial > Praça
        
        $comandante = Role::create(['name' => 'comandante']);
        $oficial = Role::create(['name' => 'oficial']);
        $suboficial = Role::create(['name' => 'suboficial']);
        $praca = Role::create(['name' => 'praca']);

        // Comandante: acesso total
        $comandante->givePermissionTo(Permission::all());

        // Oficial: gerencia documentos e pessoal
        $oficial->givePermissionTo([
            'documents.view', 'documents.create', 'documents.edit', 'documents.approve',
            'personnel.view', 'personnel.edit',
            'reports.view', 'reports.export',
        ]);

        // Suboficial: operações diárias
        $suboficial->givePermissionTo([
            'documents.view', 'documents.create',
            'personnel.view',
            'reports.view',
        ]);

        // Praça: apenas visualização
        $praca->givePermissionTo([
            'documents.view',
            'personnel.view',
        ]);
    }
}
```

## Checklist de Implementação

```markdown
## Autenticação
- [ ] Login/Logout funcionando
- [ ] Registro (se aplicável)
- [ ] Reset de senha
- [ ] Email verification (se aplicável)
- [ ] Two-factor authentication (se aplicável)

## Autorização
- [ ] Roles definidas
- [ ] Permissions granulares
- [ ] Policies para cada Model
- [ ] Gates para ações globais
- [ ] Middleware nas rotas
- [ ] Verificações no Blade

## Segurança
- [ ] CSRF protection
- [ ] Rate limiting em login
- [ ] Logout em outros dispositivos
- [ ] Auditoria de acessos
- [ ] Expiração de sessão
```
