---
name: springboot-patterns
description: Spring Boot and Java best practices. Use when developing REST APIs, services, repositories, or any Java code. Applies DDD architecture, transaction management, and code style conventions.
---

# Spring Boot Best Practices

## Project Structure (Domain-Driven Design)

```
src/main/java/com/example/
├── {domain}/                    # One package per domain
│   ├── domain/                  # Domain layer - entities and repository interfaces
│   │   ├── {Entity}.java        # JPA entity
│   │   └── {Entity}Repository.java  # Spring Data JPA repository interface
│   ├── application/             # Application layer - business logic
│   │   └── {Entity}ApplicationService.java
│   └── interfaces/              # Interface layer - REST controllers
│       └── rest/
│           ├── {Entity}Controller.java
│           └── {Entity}Mapper.java
├── shared/                      # Cross-cutting concerns
│   ├── application/
│   ├── domain/
│   └── interfaces/rest/
└── api/generated/               # OpenAPI generated code (do not edit)
```

## Transaction Management

### Minimize Transaction Scope
Only wrap the actual database operation in a transaction, not the entire method:

```java
// Good - minimal transaction scope
public EntityDto updateEntity(String ref, UpdateEntityRequestDto request) {
    Entity entity = refResolver.resolve(ref);

    if (request.getTitle() != null) {
        entity.setTitle(request.getTitle());
    }
    // ... other field updates

    Entity saved = transactionTemplate.execute(status -> entityRepository.save(entity));
    return entityMapper.toDto(saved);
}

// Bad - entire method in transaction
public EntityDto updateEntity(String ref, UpdateEntityRequestDto request) {
    return transactionTemplate.execute(status -> {
        Entity entity = refResolver.resolve(ref);  // Read doesn't need transaction
        // ... field updates don't need transaction
        Entity saved = entityRepository.save(entity);  // Only this needs transaction
        return entityMapper.toDto(saved);
    });
}
```

### Use TransactionTemplate, Not @Transactional
Prefer `TransactionTemplate` over `@Transactional` annotation for explicit control:

```java
@Service
@RequiredArgsConstructor
public class EntityApplicationService {
    private final TransactionTemplate transactionTemplate;
    private final EntityRepository entityRepository;

    public void deleteEntity(String ref) {
        Entity entity = refResolver.resolve(ref);
        transactionTemplate.executeWithoutResult(status -> entityRepository.delete(entity));
    }
}
```

### When Full Transaction Is Needed
Keep full transaction scope when operations must be atomic:

```java
// Create needs full transaction for sequence number atomicity
public EntityDto createEntity(CreateEntityRequestDto request) {
    return transactionTemplate.execute(status -> {
        int sequenceNumber = getNextSequenceNumber();  // Read
        Entity entity = new Entity(..., sequenceNumber, ...);  // Must be atomic
        return entityMapper.toDto(entityRepository.save(entity));  // Write
    });
}
```

## Lombok Usage

### Use @RequiredArgsConstructor for Dependency Injection
Never write constructors manually for Spring beans:

```java
// Good
@Service
@RequiredArgsConstructor
public class EntityApplicationService {
    private final EntityRepository entityRepository;
    private final RefResolver refResolver;
    private final EntityMapper entityMapper;
}

// Bad
@Service
public class EntityApplicationService {
    private final EntityRepository entityRepository;

    public EntityApplicationService(EntityRepository entityRepository) {
        this.entityRepository = entityRepository;
    }
}
```

### Standard Lombok Annotations for Entities

```java
@Entity
@Table(name = "entities")
@Getter
@Setter
@NoArgsConstructor(access = AccessLevel.PROTECTED)  // JPA requires no-arg constructor
public class Entity {
    // fields...

    // Required-args constructor for creating new instances
    public Entity(String publicId, int sequenceNumber, ...) {
        // initialization
    }
}
```

## OpenAPI Generated Code

### DTO Suffix Convention
All generated model classes have `Dto` suffix to distinguish from domain entities:

- Domain: `Entity`, `Project`, `Task`
- DTOs: `EntityDto`, `ProjectDto`, `TaskDto`, `CreateEntityRequestDto`

### Never Import with Wildcards
Always use explicit imports:

```java
// Good
import com.example.api.generated.model.EntityDto;
import com.example.api.generated.model.CreateEntityRequestDto;

// Bad
import com.example.api.generated.model.*;
```

### Controller Implementation
Controllers implement generated API interfaces:

```java
@RestController
@RequiredArgsConstructor
public class EntityController implements EntitiesApi {
    private final EntityApplicationService entityApplicationService;

    @Override
    public ResponseEntity<EntityDto> createEntity(CreateEntityRequestDto request) {
        EntityDto created = entityApplicationService.createEntity(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

## Mapper Pattern

Mappers convert between domain entities and DTOs:

```java
@Component
public class EntityMapper {

    public EntityDto toDto(Entity domain) {
        EntityDto dto = new EntityDto();
        dto.setPublicId(domain.getPublicId());
        dto.setTitle(domain.getTitle());
        dto.setStatus(toApiStatus(domain.getStatus()));
        // ... map all fields
        return dto;
    }

    public EntityStatus toDomainStatus(EntityStatusDto apiStatus) {
        return switch (apiStatus) {
            case ACTIVE -> EntityStatus.ACTIVE;
            case INACTIVE -> EntityStatus.INACTIVE;
            case ARCHIVED -> EntityStatus.ARCHIVED;
        };
    }

    private EntityStatusDto toApiStatus(EntityStatus domainStatus) {
        return switch (domainStatus) {
            case ACTIVE -> EntityStatusDto.ACTIVE;
            case INACTIVE -> EntityStatusDto.INACTIVE;
            case ARCHIVED -> EntityStatusDto.ARCHIVED;
        };
    }
}
```

## Reference Resolution Pattern

Use `RefResolver` for looking up entities by publicId or displayKey:

```java
@Component
@RequiredArgsConstructor
public class RefResolver {
    private final EntityRepository entityRepository;

    public Entity resolve(String ref) {
        return entityRepository.findByPublicId(ref)
            .or(() -> entityRepository.findByKey(ref))
            .orElseThrow(() -> new EntityNotFoundException("Entity", ref));
    }

    // For optional references (can be null or empty string to clear)
    public Entity resolveOptional(String ref) {
        if (ref == null || ref.isBlank()) {
            return null;
        }
        return resolve(ref);
    }
}
```

## Exception Handling

### Custom Exceptions

```java
public class EntityNotFoundException extends RuntimeException {
    public EntityNotFoundException(String entityType, String reference) {
        super(entityType + " not found: " + reference);
    }
}

public class ResourceConflictException extends RuntimeException {
    public ResourceConflictException(String message) {
        super(message);
    }
}
```

### Global Exception Handler

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponseDto> handleNotFound(EntityNotFoundException ex) {
        ErrorResponseDto error = new ErrorResponseDto();
        error.setCode("NOT_FOUND");
        error.setMessage(ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponseDto> handleValidation(MethodArgumentNotValidException ex) {
        ErrorResponseDto error = new ErrorResponseDto();
        error.setCode("VALIDATION_ERROR");
        error.setMessage("Validation failed");
        error.setDetails(ex.getBindingResult().getFieldErrors().stream()
            .map(fe -> {
                FieldErrorDto fieldError = new FieldErrorDto();
                fieldError.setField(fe.getField());
                fieldError.setMessage(fe.getDefaultMessage());
                return fieldError;
            })
            .toList());
        return ResponseEntity.badRequest().body(error);
    }
}
```

## Testing Patterns

### Integration Tests with Schema Isolation

```java
@AutoConfigureMockMvc
@Transactional
class EntityControllerTest extends AbstractIntegrationTest {

    private static final String SCHEMA_NAME = "entity_controller_test";

    @DynamicPropertySource
    static void configureSchema(DynamicPropertyRegistry registry) {
        AbstractIntegrationTest.configureSchema(registry, SCHEMA_NAME);
    }

    @Autowired private MockMvc mockMvc;
    @MockitoBean private CurrentUserService currentUserService;

    @BeforeEach
    void setUp() {
        testUser = userRepository.save(new User(...));
        when(currentUserService.getCurrentUser()).thenReturn(testUser);
    }

    @Test
    @WithMockUser(username = "user")
    void createEntity_shouldReturnCreatedEntity() throws Exception {
        CreateEntityRequestDto request = new CreateEntityRequestDto();
        request.setTitle("Test Entity");

        mockMvc.perform(post("/entities")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.title").value("Test Entity"));
    }
}
```

## Code Style

### Checkstyle Rules
- No star imports (`import x.y.*`)
- No unused imports
- No redundant imports

### Spotless Formatting
Run `mvn spotless:apply` before committing.

### Switch Expressions
Use modern switch expressions:

```java
// Good
private EntityStatusDto toApiStatus(EntityStatus status) {
    return switch (status) {
        case ACTIVE -> EntityStatusDto.ACTIVE;
        case INACTIVE -> EntityStatusDto.INACTIVE;
        case ARCHIVED -> EntityStatusDto.ARCHIVED;
    };
}

// Bad
private EntityStatusDto toApiStatus(EntityStatus status) {
    switch (status) {
        case ACTIVE: return EntityStatusDto.ACTIVE;
        case INACTIVE: return EntityStatusDto.INACTIVE;
        case ARCHIVED: return EntityStatusDto.ARCHIVED;
        default: throw new IllegalArgumentException();
    }
}
```

## Build Commands

```bash
# Generate OpenAPI code
mvn generate-sources

# Format code
mvn spotless:apply

# Check style
mvn checkstyle:check

# Run tests
mvn test

# Full build
mvn clean verify
```
