---
name: arch-check
description: Verify architecture health including layer violations, circular dependencies, package structure, and design pattern compliance
---

# Architecture Check Skill

Verify the codebase adheres to architectural principles, layer boundaries, and design patterns.

## Instructions

### 1. Verify Layer Architecture

This project follows a layered architecture:

```
┌─────────────────────────────────────────┐
│            Controller Layer             │  ← HTTP endpoints
├─────────────────────────────────────────┤
│             Service Layer               │  ← Business logic
├─────────────────────────────────────────┤
│    Provider / Strategy / Mapper Layer   │  ← Data access, transformations
├─────────────────────────────────────────┤
│              Model Layer                │  ← Domain objects (records)
└─────────────────────────────────────────┘
```

**Allowed Dependencies**:
- Controller → Service → Provider/Strategy/Mapper → Model
- All layers → Model (models are shared)
- Service → Service (peer services)

**Violations to detect**:
```java
// BAD: Controller importing Strategy
import ...service.strategy.FetchCurrentConditionsStrategy;

// BAD: Provider importing Controller
import ...controller.SpotsController;

// BAD: Model importing Service
import ...service.AggregatorService;
```

Use `Grep` to check imports in each layer:
```bash
# Controllers should not import strategies directly
grep -r "import.*strategy" src/main/java/**/controller/

# Providers should not import controllers or services
grep -r "import.*controller\|import.*service[^/]" src/main/java/**/provider/

# Models should not import anything except other models
grep -r "import.*service\|import.*controller\|import.*provider" src/main/java/**/model/
```

### 2. Detect Circular Dependencies

Check for circular imports between packages:

**Package dependency graph**:
```
controller → service → provider
                    → strategy
                    → mapper
          → model (allowed from all)
```

**Search patterns**:
```java
// Check if Service A imports Service B and vice versa
// File: ServiceA.java contains "import ...ServiceB"
// File: ServiceB.java contains "import ...ServiceA"
```

**Common circular dependency patterns**:
- Service A calls Service B, Service B calls Service A
- Listener/callback creating cycles
- Utility classes depending on domain classes

### 3. Package Structure Compliance

Verify expected package structure:

```
src/main/java/com/github/pwittchen/varun/
├── Application.java           # Main entry point
├── config/                    # Configuration classes
│   └── *Config.java
├── controller/                # REST controllers
│   └── *Controller.java
├── exception/                 # Custom exceptions
│   └── *Exception.java
├── mapper/                    # Data mappers
│   └── *Mapper.java
├── model/                     # Domain models (records)
│   └── *.java
├── provider/                  # Data providers
│   └── *Provider.java
└── service/                   # Business services
    ├── *Service.java
    └── strategy/              # Strategy implementations
        └── *Strategy*.java
```

**Check for**:
- Files in wrong packages (e.g., Service in controller package)
- Missing package conventions (e.g., Helper in service package)
- Inconsistent naming (e.g., `FooManager` instead of `FooService`)

### 4. Design Pattern Compliance

#### Strategy Pattern (CurrentConditions)
```java
// Interface
interface FetchCurrentConditionsStrategy {
    boolean canProcess(int windguruId);
    CurrentConditions fetch();
}

// Check all implementations:
// - Implement the interface
// - Have canProcess() method
// - Are registered/discoverable (via @Component or explicit registration)
```

#### Provider Pattern (Data Loading)
```java
// Check providers:
// - Single responsibility (one data source)
// - Return domain models
// - Don't contain business logic
```

#### Caching Pattern
```java
// Check cache usage:
// - Caches are in service layer (not controller)
// - Cache keys are consistent
// - Cache invalidation is handled
```

### 5. Dependency Injection Compliance

**Check for**:
```java
// BAD: Direct instantiation of services
private ForecastService service = new ForecastService();

// GOOD: Constructor injection
private final ForecastService service;
public MyService(ForecastService service) {
    this.service = service;
}

// BAD: Field injection (harder to test)
@Autowired
private ForecastService service;

// GOOD: Constructor injection with Lombok
@RequiredArgsConstructor
public class MyService {
    private final ForecastService forecastService;
}
```

Search for anti-patterns:
```bash
grep -r "@Autowired" src/main/java/
grep -r "new.*Service\(\)" src/main/java/
```

### 6. Single Responsibility Check

Analyze classes for responsibility violations:

**Warning signs**:
- Class > 500 lines (potential god class)
- More than 10 public methods
- More than 7 dependencies injected
- Mixed concerns (HTTP + business logic + data access)

**Check service classes**:
```java
// RED FLAG: Service doing too much
class BigService {
    void handleRequest()      // HTTP concern
    void processData()        // Business logic
    void saveToCache()        // Data concern
    void sendNotification()   // Side effect
    void formatResponse()     // Presentation
}
```

### 7. API Design Consistency

**Controller conventions**:
```java
// Check all controllers follow same patterns:
@RestController
@RequestMapping("/api/v1/...")
public class XxxController {
    // GET for reads
    @GetMapping("/{id}")
    public Mono<Xxx> getById(@PathVariable int id)

    // POST for creates
    @PostMapping
    public Mono<Xxx> create(@RequestBody XxxRequest request)

    // Consistent response types (Mono/Flux)
    // Consistent error handling
}
```

**Check for**:
- Mixed response types (some Mono, some blocking)
- Inconsistent URL patterns
- Missing @PathVariable/@RequestParam annotations
- Business logic in controllers

### 8. Configuration Separation

**Check configuration is externalized**:
```java
// BAD: Hardcoded values in code
private static final String API_URL = "https://api.example.com";
private static final int TIMEOUT = 5000;

// GOOD: Externalized configuration
@Value("${api.url}")
private String apiUrl;

// or
@ConfigurationProperties(prefix = "api")
public class ApiConfig {
    private String url;
    private int timeout;
}
```

Search for hardcoded values:
```bash
grep -r "http://" src/main/java/
grep -r "https://" src/main/java/
grep -rE "[0-9]{4,}" src/main/java/  # Large numbers (ports, timeouts)
```

### 9. Exception Handling Architecture

**Check exception flow**:
```
Controller → Service → Provider/Strategy
    ↑           ↑           ↑
    └───────────┴───────────┴── Exceptions bubble up

Controller: Translates to HTTP responses
Service: May wrap in domain exceptions
Provider: Throws low-level exceptions
```

**Verify**:
- Custom exceptions extend appropriate base
- Exceptions have meaningful messages
- No swallowed exceptions (empty catch blocks)
- Consistent error response format

### 10. Test Architecture

**Check test structure mirrors main**:
```
src/test/java/
├── controller/     # Controller tests (WebTestClient)
├── service/        # Service unit tests
├── provider/       # Provider tests
├── strategy/       # Strategy tests
└── integration/    # Integration tests

src/e2e/java/       # End-to-end tests (Playwright)
```

**Verify**:
- Tests exist for each layer
- Proper mocking (mock dependencies, not internals)
- No test interdependencies

## Output Format

```markdown
## Architecture Health Report

### Summary
| Check | Status | Issues |
|-------|--------|--------|
| Layer Violations | ✓/✗ | X |
| Circular Dependencies | ✓/✗ | X |
| Package Structure | ✓/✗ | X |
| Design Patterns | ✓/✗ | X |
| DI Compliance | ✓/✗ | X |
| Single Responsibility | ✓/✗ | X |
| API Consistency | ✓/✗ | X |

### Layer Violations

#### [Violation Description]
**File**: `path/to/file.java:line`
**Issue**: Controller directly imports Strategy
**Impact**: Bypasses service layer, harder to test
**Fix**: Inject service that uses strategy

### Circular Dependencies

```
ServiceA ←→ ServiceB (CIRCULAR)
```
**Fix**: Extract shared logic to new service, or use events

### Package Structure Issues

| File | Current Package | Expected Package |
|------|-----------------|------------------|
| FooHelper.java | service | util or helper |

### Design Pattern Violations

#### Strategy Pattern
- Missing: `XxxStrategy` not implementing interface
- Orphaned: `YyyStrategy` not registered

### Dependency Injection Issues

| File | Line | Issue | Fix |
|------|------|-------|-----|
| Service.java | 15 | Field injection | Use constructor |
| Handler.java | 23 | Direct instantiation | Inject dependency |

### Single Responsibility Concerns

| Class | Lines | Methods | Dependencies | Concern |
|-------|-------|---------|--------------|---------|
| BigService | 650 | 15 | 9 | Consider splitting |

### Hardcoded Values Found

| File | Line | Value | Recommendation |
|------|------|-------|----------------|
| Client.java | 42 | "https://..." | Move to config |

### Architecture Diagram (Current)

```
┌─────────────┐     ┌─────────────┐
│ Controller  │────▶│   Service   │
└─────────────┘     └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │Provider │  │Strategy │  │ Mapper  │
        └─────────┘  └─────────┘  └─────────┘
```

### Recommendations

1. **Critical**: Fix circular dependency between X and Y
2. **High**: Refactor BigService into smaller services
3. **Medium**: Move hardcoded URLs to configuration
4. **Low**: Rename FooManager to FooService for consistency
```

## Execution Steps

1. Use `Glob` to list all Java files by package
2. Use `Grep` to check imports in each layer
3. Read large files to check responsibilities
4. Verify design pattern implementations
5. Check for DI anti-patterns
6. Analyze configuration usage
7. Generate architecture health report

## Notes

- This project intentionally has no database layer (in-memory caching)
- Reactive types (Mono/Flux) should be consistent across layers
- Strategy pattern is used for weather station integrations
- Configuration is split between application.yml and code constants
- Some "violations" may be intentional trade-offs - use judgment
