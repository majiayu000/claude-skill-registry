---
name: code-investigation
description: Efficient codebase investigation for rapid-go. Use when understanding existing code before modifications, tracing request flows from API to database, finding where functionality is implemented, or analyzing impact before changes. ALWAYS use before modifying existing code, fixing bugs, or adding features.
---

# Code Investigation Guide

## Quick Start

```
Proto (API contract) -> Handler -> Usecase -> Repository -> DB
```

Use this flow to trace any feature. Start from what you know.

## Key Locations

| What | Where |
|------|-------|
| API contracts | `schema/proto/rapid/{admin_api,public_api,debug_api}/v1/` |
| Handlers | `internal/infrastructure/grpc/internal/handler/{admin,public,debug}/` |
| Usecases | `internal/usecase/*_impl.go` |
| Domain models | `internal/domain/model/` |
| Repository interfaces | `internal/domain/repository/` |
| Repository implementations | `internal/infrastructure/{mysql,postgresql,spanner}/repository/` |
| DI wiring | `internal/infrastructure/dependency/dependency.go` |
| Auth interceptors | `internal/infrastructure/grpc/internal/interceptor/` |

## Investigation Patterns

### Find an API endpoint

```bash
# Find by HTTP path
grep "/admin/v1/tenants" schema/proto/rapid/

# Find by RPC name
grep "CreateTenant" internal/infrastructure/grpc/internal/handler/admin/
```

### Trace request flow

1. Find RPC in `schema/proto/rapid/**/api.proto`
2. Find handler in `internal/infrastructure/grpc/internal/handler/{actor}/`
3. Find interactor in `internal/usecase/*_impl.go`
4. Find repository in `internal/domain/repository/` (interface) and `internal/infrastructure/*/repository/` (impl)

### Find all usages of a type

```bash
# Find usages of a domain model
grep "model.Staff" internal/

# Find usages of a repository method
grep "staffRepository.Get" internal/usecase/
```

### Check authorization logic

- Session extraction: `internal/infrastructure/grpc/internal/interceptor/session_interceptor/`
- Access control: `internal/infrastructure/grpc/internal/interceptor/authorization_interceptor/`
- Role checks in usecase: look for `param.AdminRole.IsRoot()` patterns

### Impact analysis before changes

1. Find interface definition in `internal/domain/repository/`
2. Find all implementations in `internal/infrastructure/*/repository/`
3. Find all callers in `internal/usecase/`
4. Check mock generation: `internal/domain/repository/mock/`

## Common Search Patterns

| Goal | Search |
|------|--------|
| Find entity by name | `grep "type Staff struct" internal/domain/model/` |
| Find error definition | `grep "StaffNotFoundErr" internal/domain/errors/` |
| Find input validation | `grep "type AdminCreateStaff" internal/usecase/input/` |
| Find marshaller | `grep "StaffToModel\|StaffToPb" internal/` |
| Find DI registration | `grep "AdminStaffInteractor" internal/infrastructure/dependency/` |

## Tips

- Start from proto for API-related investigation
- Start from domain model for business logic investigation
- Check `dependency.go` to understand how components are wired
- Marshallers exist in two places: repository (DB<->domain) and handler (domain<->proto)
