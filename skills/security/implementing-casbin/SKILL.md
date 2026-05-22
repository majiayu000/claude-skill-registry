---
name: implementing-casbin
description: Implement role-based (RBAC) and attribute-based (ABAC) access control in Go using Casbin. Covers model configuration, GORM adapters, Chi/gRPC middleware, and production patterns. Use when implementing authorization in Go services.
version: 1.0.0
---

# Implementing Casbin Authorization

## Purpose

Implement fine-grained authorization in Go services using Casbin's policy-based access control. Supports RBAC (role-based), ABAC (attribute-based), and hybrid models with database-backed policy storage.

## When NOT to Use

- Simple API key authentication (use middleware directly)
- Single-user applications (no authorization needed)
- OAuth/OIDC token validation only (use dedicated auth libraries)
- Static, compile-time permissions (use Go interfaces/types)

---

## Quick Start Workflow

### Step 1: Install Dependencies

```bash
go get github.com/casbin/casbin/v2
go get github.com/casbin/gorm-adapter/v3
go get gorm.io/driver/postgres  # or mysql
```

### Step 2: Create Model File

Create `config/rbac_model.conf`:

```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && keyMatch2(r.obj, p.obj) && r.act == p.act
```

### Step 3: Initialize Enforcer with GORM

```go
package authz

import (
    "fmt"
    "github.com/casbin/casbin/v2"
    gormadapter "github.com/casbin/gorm-adapter/v3"
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
)

func NewEnforcer(dsn, modelPath string) (*casbin.Enforcer, error) {
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    if err != nil {
        return nil, fmt.Errorf("connect to database: %w", err)
    }

    adapter, err := gormadapter.NewAdapterByDB(db)
    if err != nil {
        return nil, fmt.Errorf("create adapter: %w", err)
    }

    e, err := casbin.NewEnforcer(modelPath, adapter)
    if err != nil {
        return nil, fmt.Errorf("create enforcer: %w", err)
    }

    e.EnableAutoSave(true)
    return e, nil
}
```

### Step 4: Add Chi Middleware

```go
func Authorize(e *casbin.Enforcer) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            user, ok := r.Context().Value("userID").(string)
            if !ok || user == "" {
                http.Error(w, "Unauthorized", http.StatusUnauthorized)
                return
            }

            allowed, err := e.Enforce(user, r.URL.Path, r.Method)
            if err != nil {
                http.Error(w, "Authorization error", http.StatusInternalServerError)
                return
            }
            if !allowed {
                http.Error(w, "Forbidden", http.StatusForbidden)
                return
            }
            next.ServeHTTP(w, r)
        })
    }
}
```

### Step 5: Define Policies

```go
// Add role
e.AddRoleForUser("alice", "admin")

// Add permissions for role
e.AddPolicy("admin", "/api/users/*", "GET")
e.AddPolicy("admin", "/api/users/*", "POST")

// Check permission
allowed, _ := e.Enforce("alice", "/api/users/123", "GET")  // true
```

---

## Model Configuration

### RBAC Model (Recommended Default)

```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && keyMatch2(r.obj, p.obj) && r.act == p.act
```

**Key parts:**
- `g(r.sub, p.sub)`: Role inheritance (user -> role)
- `keyMatch2`: Supports `/path/:id` patterns

### ABAC Model

```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub_rule, obj_rule, act

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = eval(p.sub_rule) && eval(p.obj_rule) && r.act == p.act
```

**Example:**
```go
// User can only access their own documents
e.AddPolicy("r.sub.ID == r.obj.OwnerID", "r.obj.Type == 'document'", "read")
```

### RBAC with Domains (Multi-Tenant)

```ini
[request_definition]
r = sub, dom, obj, act

[policy_definition]
p = sub, dom, obj, act

[role_definition]
g = _, _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub, r.dom) && r.dom == p.dom && keyMatch2(r.obj, p.obj) && r.act == p.act
```

**Example:**
```go
e.AddRoleForUserInDomain("alice", "admin", "tenant1")
e.AddPolicy("admin", "tenant1", "/api/*", "GET")
allowed, _ := e.Enforce("alice", "tenant1", "/api/users", "GET")  // true
```

---

## GORM Adapter Setup

### PostgreSQL

```go
dsn := "host=localhost user=app password=secret dbname=myapp port=5432 sslmode=disable"
db, _ := gorm.Open(postgres.Open(dsn), &gorm.Config{})
adapter, _ := gormadapter.NewAdapterByDB(db)
```

### MySQL

```go
dsn := "user:password@tcp(localhost:3306)/myapp?charset=utf8mb4&parseTime=True"
db, _ := gorm.Open(mysql.Open(dsn), &gorm.Config{})
adapter, _ := gormadapter.NewAdapterByDB(db)
```

### Connection Pooling

```go
sqlDB, _ := db.DB()
sqlDB.SetMaxIdleConns(10)
sqlDB.SetMaxOpenConns(100)
sqlDB.SetConnMaxLifetime(time.Hour)
```

---

## Policy Management

### Adding Policies

```go
e.AddPolicy("alice", "/api/users", "GET")           // Direct permission
e.AddRoleForUser("alice", "admin")                  // Assign role
e.AddRolesForUser("bob", []string{"viewer", "editor"})  // Multiple roles
```

### Removing Policies

```go
e.RemovePolicy("alice", "/api/users", "GET")
e.RemoveFilteredPolicy(0, "alice")    // All policies for subject
e.DeleteRoleForUser("alice", "admin")
```

### Querying Policies

```go
policies, _ := e.GetPolicy()                          // All policies
roles, _ := e.GetRolesForUser("alice")               // User's roles
permissions, _ := e.GetImplicitPermissionsForUser("alice")  // Including inherited
hasRole, _ := e.HasRoleForUser("alice", "admin")
```

---

## Testing

### Unit Test Setup

```go
func TestEnforcer(t *testing.T) {
    modelText := `
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
`
    m, _ := model.NewModelFromString(modelText)
    e, _ := casbin.NewEnforcer(m)

    e.AddPolicy("admin", "/users", "GET")
    e.AddRoleForUser("alice", "admin")

    allowed, _ := e.Enforce("alice", "/users", "GET")
    assert.True(t, allowed)
}
```

See TEMPLATES.md for complete test templates.

---

## Common Issues

### Policies not persisting

```go
e.EnableAutoSave(true)  // Enable auto-save
// Or: e.SavePolicy()   // Manual save
```

### keyMatch not working with path params

Use correct matcher function:
- `keyMatch2`: `/users/:id` patterns
- `keyMatch3`: `/users/{id}` patterns

### Slow performance with large policy sets

```go
// Load only relevant policies
filter := gormadapter.Filter{P: []string{"", "tenant1"}}
e.LoadFilteredPolicy(filter)

// Or batch enforcement
results, _ := e.BatchEnforce(requests)
```

---

## Integration with Other Skills

- **setup-go**: Run before Casbin setup
- **quality-check**: Lint authorization code
- **run-tests**: Execute authorization tests

---

## References

- [Casbin Documentation](https://casbin.org/docs/en/overview)
- [GORM Adapter](https://github.com/casbin/gorm-adapter)
- See **REFERENCE.md** for complete API reference and built-in functions
- See **TEMPLATES.md** for copy-paste middleware and test templates
