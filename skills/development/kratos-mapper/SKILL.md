---
name: kratos-mapper
description: Generates bidirectional mapper functions (transformers/converters/adapters) between protobuf DTOs and business domain models for go-kratos services. Creates type-safe conversions with proper field mapping, handles timestamps, enums, optional fields, and pagination metadata transformations. Use when converting DTOs to domain models, transforming proto to biz models, mapping requests/responses, implementing type conversions, creating entity transformers, or handling DTO transformations between layers.
tags: [kratos, mapper, dto, converter, transformer, proto, domain-model, type-conversion]
keywords: [mapper, convert, transform, DTO, proto to domain, domain to proto, type conversion, request mapping, response mapping, transformer, converter, adapter]
version: 2.0.0
last_updated: 2026-01-12
---

<objective>
Generate mapper functions that convert between protobuf DTOs (requests/responses) and business domain models, ensuring type safety and proper field transformations.
</objective>

<quick_start>
For an entity, create mappers in `internal/service/mapper.go`:

```go
// Request → Business Model
func {Entity}FromCreateRequest(req *pb.Create{Entity}Request) *biz.{Entity} {
	return &biz.{Entity}{
		Name: req.Name,
		// Map fields...
	}
}

// Business Model → Proto Response
func toProto{Entity}(e *biz.{Entity}) *pb.{Entity} {
	return &pb.{Entity}{
		Id:   e.ID,
		Name: e.Name,
		// Map fields...
	}
}
```
</quick_start>

<mapper_patterns>
## Common Mapper Patterns

**Request to Business Model**:
```go
func {Entity}FromCreateRequest(req *pb.Create{Entity}Request) *biz.{Entity}
func {Entity}FromUpdateRequest(req *pb.Update{Entity}Request, id uint64) *biz.{Entity}
```

**Business Model to Proto**:
```go
func toProto{Entity}(e *biz.{Entity}) *pb.{Entity}
func toProto{Entities}(list []*biz.{Entity}) []*pb.{Entity}
```

**List Options**:
```go
func NewList{Entities}Options(req *pb.List{Entities}Request) *biz.List{Entities}Options {
	return &biz.List{Entities}Options{
		Pagination: pagination.PaginationParams{
			Offset: req.Offset,
			Limit:  req.Limit,
		},
	}
}
```

**Pagination Meta**:
```go
func toProtoPaginationMeta(meta *pagination.PaginationMeta) *pb.PaginationMeta {
	return &pb.PaginationMeta{
		Total:  meta.Total,
		Offset: meta.Offset,
		Limit:  meta.Limit,
	}
}
```
</mapper_patterns>

<naming_conventions>
## Naming Rules

**Proto → Business**: `{Entity}From{Operation}Request`
- Example: `SymbolFromCreateRequest`, `ProductFromUpdateRequest`

**Business → Proto**: `toProto{Entity}` or `toProto{Entities}`
- Example: `toProtoSymbol`, `toProtoSymbols`

**Options**: `NewList{Entities}Options`

**Helpers**: `toProto{Type}` for common types
- Example: `toProtoPaginationMeta`, `toProtoTimestamp`
</naming_conventions>

<type_conversions>
## Common Type Conversions

**IDs**: `uint64` ↔ `uint64` (direct)
**Strings**: `string` ↔ `string` (direct)
**Timestamps**: `time.Time` ↔ `*timestamppb.Timestamp`
```go
CreatedAt: timestamppb.New(e.CreatedAt)
```

**Optional Fields**: Use pointers
```go
// Business has *string, proto has string
Email: func() string {
	if e.Email != nil {
		return *e.Email
	}
	return ""
}()
```

**Enums**: Map string to proto enum
```go
Status: pb.Status(pb.Status_value[e.Status])
```
</type_conversions>

<file_organization>
## Where to Put Mappers

**Single entity**: `internal/service/mapper.go` (all mappers)
**Multiple entities**: `internal/service/{entity}_mapper.go` (per entity)

Keep mapper functions close to service handlers for easy reference.
</file_organization>

<success_criteria>
Mapper functions are correct when:
- [ ] Naming follows conventions ({Entity}From* vs toProto*)
- [ ] All proto fields mapped to business model fields
- [ ] Type conversions handled (timestamps, optionals, enums)
- [ ] Nil checks for optional/pointer fields
- [ ] List mappers use range loops
- [ ] Pagination helpers created if needed
- [ ] Functions are pure (no side effects)
</success_criteria>