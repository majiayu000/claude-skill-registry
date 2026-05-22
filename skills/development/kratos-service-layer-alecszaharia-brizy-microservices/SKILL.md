---
name: kratos-service-layer
description: Generates gRPC/HTTP service handlers for go-kratos microservices. Creates service structs, handler methods, and integrates with protobuf definitions. Use when implementing RPC handlers, adding API endpoints, creating dual transport (HTTP/gRPC) handlers, or connecting transport layer to business logic in kratos services.
---

<essential_principles>
## How Kratos Service Layer Works

### Service Layer Role
Connects transport (gRPC/HTTP) to business logic:

**Responsibilities**:
- Handle gRPC/HTTP requests
- Map proto DTOs to business models (via mapper)
- Call use case methods
- Map results back to proto responses
- Convert business errors to gRPC status codes

### Service Struct Pattern
```go
type {Entity}Service struct {
	pb.Unimplemented{Entity}ServiceServer  // Embed unimplemented server
	uc domain.{Entity}UseCase             // Use case dependency (from domain package)
}
```

**Import**: `import "{service}/internal/biz/domain"`

### Handler Method Pattern
```go
func (s *{Entity}Service) Create{Entity}(ctx context.Context, in *pb.Request) (*pb.Response, error) {
	// 1. Map request to business model
	entity := {Entity}FromRequest(in)

	// 2. Call use case
	result, err := s.uc.Create{Entity}(ctx, entity)
	if err != nil {
		return nil, toServiceError(err)  // Map business error to gRPC error
	}

	// 3. Map result to response
	return &pb.Response{Entity: toProto{Entity}(result)}, nil
}
```
</essential_principles>

<intake>
What would you like to do?

1. Create service handlers for new entity
2. Add handler methods to existing service
3. View handler patterns and examples

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "create", "new" | `workflows/create-service.md` |
| 2, "add", "extend" | `workflows/add-handlers.md` |
| 3, "examples", "patterns" | `workflows/view-examples.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
**Core**: handler-pattern.md, service-structure.md, error-mapping.md
**Mappers**: mapper-conventions.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-service.md | Generate service handlers and mappers |
| add-handlers.md | Add methods to existing service |
| view-examples.md | Show patterns |
</workflows_index>

<success_criteria>
Service layer code is correct when:
- Service struct embeds Unimplemented{Entity}ServiceServer
- Constructor added to service.ProviderSet
- Handlers map DTOs via mapper functions
- Errors converted to gRPC status codes
- All methods have godoc comments
- User reminded to run `make generate`
</success_criteria>