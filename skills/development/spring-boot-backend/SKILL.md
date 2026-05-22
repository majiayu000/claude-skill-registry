---
name: spring-boot-backend
description: Build and implement Spring Boot 3 backend with Java 17 - REST APIs, JPA entities, services, repositories, security (JWT), and database migrations for Photo Map MVP. This skill should be used when creating, developing, or implementing *.java files, backend endpoints, business logic, database entities, DTOs, authentication, or API error handling. File types .java, .xml, .properties, .yml, .sql (project)
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Spring Boot Backend Development - Photo Map MVP

## Project Context

**Stack:** Spring Boot 3.2.11+, Java 17 LTS, PostgreSQL 15, Spring Security 6 (JWT stateless)

**Core Features:**
1. Authentication - JWT login/registration, BCrypt hashing
2. Photo Management - Upload with EXIF extraction, asynchronous processing, CRUD operations
3. User Scoping - Strict data isolation (users see only their own photos)
4. Admin API - User management (ADMIN role)

**Key Constraints:**
- MVP scope - simple solutions preferred
- Mikrus VPS - limited resources (synchronous API, async background processing)
- **User isolation CRITICAL** - ALL queries MUST include userId filtering

---

## Architecture Principles

### Layered Architecture

**Controller** (HTTP only) → **Service** (business logic) → **Repository** (data access) → **Database**

### User Scoping Pattern (CRITICAL)

**All photo queries MUST include userId to enforce data isolation:**

```java
// ❌ BAD: Security vulnerability - any user can access any photo
public Photo getPhoto(final Long photoId) {
    return photoRepository.findById(photoId).orElseThrow();
}

// ✅ GOOD: User can only access their own photos
public Photo getPhoto(final Long photoId, final Long userId) {
    return photoRepository.findByIdAndUserId(photoId, userId)
        .orElseThrow(() -> new ResourceNotFoundException("Photo not found"));
}
```

### Transaction Management

- Use `@Transactional` on service methods
- Read operations: `@Transactional(readOnly = true)`
- Write operations: `@Transactional` (default)

**For detailed architecture:** See `references/architecture.md` for:
- ALL 5 SOLID principles (SRP, OCP, LSP, ISP, DIP)
- Design patterns (Constructor Injection, Static Factory Methods)
- Service orchestration patterns

---

## When to Use What

### Code Quality
- **Use `final` keyword:** Method params, local variables, injected dependencies → `references/java-quality.md`
- **Modern Java 17:** Records for DTOs, Text Blocks for SQL, Stream.toList() → `references/java-quality.md`

### Architecture
- **@Service:** Business logic, orchestrates repositories → `references/architecture.md`
- **@Component:** Utilities, non-business services
- **Records:** Immutable response DTOs → `references/rest-api-patterns.md`
- **@Data classes:** Request DTOs with validation → `references/rest-api-patterns.md`

### Data Access
- **Derived queries:** Simple queries (findByUserId) → `references/jpa-patterns.md`
- **@Query (JPQL):** Complex queries with multiple conditions → `references/jpa-patterns.md`
- **Native SQL:** Database-specific features, performance optimization → `references/jpa-patterns.md`

### Async Processing
- **Spring Integration File:** Photo upload processing → `references/async-processing.md`

---

## Implementation Workflows

### REST Endpoint Workflow

**Step-by-step guide:** `templates/rest-endpoint-template.md`

**Quick checklist:**
1. Create DTO (Record for response, @Data for request) → `references/rest-api-patterns.md`
2. Create/Update Entity with User relationship → `references/jpa-patterns.md`
3. Create Repository with user scoping methods → `references/jpa-patterns.md`
4. Implement Service with @Transactional → `templates/service-template.md`
5. Create Controller with proper HTTP status codes → `references/rest-api-patterns.md`

**Complete examples:** `examples/photo-controller.java`, `examples/photo-service.java`, `examples/photo-repository.java`

### Service Implementation

**Template:** `templates/service-template.md`

**Key rules:**
- Constructor injection with `final` fields (@RequiredArgsConstructor)
- `@Transactional(readOnly = true)` for read operations
- **All methods MUST accept userId parameter** (user scoping)
- Throw `ResourceNotFoundException` when not found
- Log at appropriate levels (debug, info, error)

### Security & JWT

**Complete patterns:** `references/security-jwt.md`

**Quick setup:**
- SecurityConfig: `examples/security-config.java`
- JWT Token Provider: `examples/jwt-token-provider.java`
- User Entity with UserDetails: `examples/user-entity.java`

### Testing

**Unit tests:** Service layer with Mockito → `references/testing.md`
**Controller tests:** MockMvc with @WebMvcTest → `references/testing.md`
**Coverage requirement:** >70% for new code

---

## Key Reminders

### Security (CRITICAL)
- ✅ **User scoping:** ALL photo queries include userId
- ✅ **JWT validation:** Token signature & expiration checked on every request
- ✅ **BCrypt passwords:** Never store plain text
- ✅ **DTOs only:** Never expose entities to API

### Performance
- ✅ `@Transactional(readOnly = true)` for queries
- ✅ Database indexes on user_id, frequently queried columns
- ✅ `FetchType.LAZY` for relationships
- ❌ NO premature optimization - keep simple for MVP

### MVP Scope
- ✅ Implement only features from `.ai/prd.md`
- ✅ Synchronous processing for API, asynchronous for photo processing
- ✅ Simple solutions over complex ones
- ❌ NO features beyond MVP requirements

---

## Quick Reference

### File Structure for Feature
```
src/main/java/com/photomap/
├── controller/   # {Resource}Controller.java
├── service/      # {Resource}Service.java
├── repository/   # {Resource}Repository.java
├── model/        # {Resource}.java (Entity)
└── dto/          # {Resource}Dto.java, {Resource}CreateRequest.java
```

### Pattern Lookup

| Need | Solution | Reference |
|------|----------|-----------|
| REST endpoint | Follow layered architecture | `templates/rest-endpoint-template.md` |
| User scoping | findByIdAndUserId() | `references/jpa-patterns.md` |
| Validation | Bean Validation annotations | `references/validation.md` |
| Security | JWT + Spring Security | `references/security-jwt.md` |
| Async processing | Spring Integration File | `references/async-processing.md` |
| Testing | Mockito + MockMvc | `references/testing.md` |
| Database changes | Flyway migrations | `references/database-migrations.md` |

### Naming Conventions

- **Controller:** `{Resource}Controller` (e.g., PhotoController)
- **Service:** `{Resource}Service` (e.g., PhotoService)
- **Repository:** `{Resource}Repository` (e.g., PhotoRepository)
- **Entity:** `{Resource}` (e.g., Photo)
- **DTO:** `{Resource}Dto`, `{Resource}CreateRequest`

---

## Related Documentation

**Project context:**
- `.ai/prd.md` - MVP requirements
- `.ai/tech-stack.md` - Technology specifications
- `.ai/db-plan.md` - Database schema
- `.ai/api-plan.md` - REST API specification

**Skill resources:**
- `references/` - Detailed patterns and best practices (loaded on demand)
- `examples/` - Complete working examples
- `templates/` - Fill-in-the-blanks templates for common tasks
