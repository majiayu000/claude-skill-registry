---
name: spring-boot-in-action
description: >
  Write and review Spring Boot applications using practices from "Spring Boot in Action"
  by Craig Walls. Covers auto-configuration, starter dependencies, externalizing
  configuration with properties and profiles, Spring Security, testing with MockMvc
  and @SpringBootTest, Spring Actuator for production observability, and deployment
  strategies (JAR, WAR, Cloud Foundry). Use when building Spring Boot apps, configuring
  beans, writing integration tests, setting up health checks, or deploying to production.
  Trigger on: "Spring Boot", "Spring", "@SpringBootApplication", "auto-configuration",
  "application.properties", "application.yml", "@RestController", "@Service",
  "@Repository", "SpringBootTest", "Actuator", "starter", ".java files", "Maven", "Gradle".
---

# Spring Boot in Action Skill

Apply the practices from Craig Walls' "Spring Boot in Action" to review existing code and write new Spring Boot applications. This skill operates in two modes: **Review Mode** (analyze code for violations of Spring Boot idioms) and **Write Mode** (produce clean, idiomatic Spring Boot from scratch).

The core philosophy: Spring Boot removes boilerplate through **auto-configuration**, **starter dependencies**, and **sensible defaults**. Fight the framework only when necessary — and when you do, prefer `application.properties` over code.

## Reference Files

- `practices-catalog.md` — Before/after examples for auto-configuration, starters, properties, profiles, security, testing, Actuator, and deployment

## How to Use This Skill

**Before responding**, read `practices-catalog.md` for the topic at hand. For configuration issues read the properties/profiles section. For test code read the testing section. For a full review, read all sections.

---

## Mode 1: Code Review

When the user asks you to **review** Spring Boot code, follow this process:

### Step 1: Identify the Layer
Determine whether the code is a controller, service, repository, configuration class, or test. Review focus shifts by layer.

### Step 2: Analyze the Code

Check these areas in order of severity:

1. **Auto-Configuration** (Ch 2, 3): Is auto-configuration being fought manually? Look for `@Bean` definitions that replicate what Spring Boot already provides (DataSource, Jackson, Security, etc.). Remove manual config where auto-config suffices.

2. **Starter Dependencies** (Ch 2): Are dependencies declared individually instead of using starters? `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, `spring-boot-starter-security` etc. bundle correct transitive dependencies and version-manage them.

3. **Externalized Configuration** (Ch 3): Are values hardcoded that belong in `application.properties`? Ports, URLs, credentials, timeouts should all be externalized. Use `@ConfigurationProperties` for type-safe config objects; use `@Value` only for single values.

4. **Profiles** (Ch 3): Is environment-specific config (dev DB vs prod DB) handled with `if` statements or system properties? Use `@Profile` and `application-{profile}.properties` instead.

5. **Security** (Ch 3): Is `WebSecurityConfigurerAdapter` extended when simple property-based config would suffice? Is HTTP Basic enabled in production? Are actuator endpoints exposed without auth?

6. **Testing** (Ch 4):
   - Use `@SpringBootTest` for full integration tests, not raw `new MyService()`
   - Use `@WebMvcTest` for controller-only tests (no full context)
   - Use `@DataJpaTest` for repository tests (in-memory DB, no web layer)
   - Use `MockMvc` for controller assertions without starting a server
   - Use `@MockBean` to replace real beans with mocks in slice tests
   - Avoid `@SpringBootTest(webEnvironment = RANDOM_PORT)` unless testing the full HTTP stack

7. **Actuator** (Ch 7): Is the application missing health/metrics endpoints? Is `/actuator` fully exposed without security? Are custom health indicators implemented for critical dependencies?

8. **Deployment** (Ch 8): Is `spring.profiles.active` set for production? Is database migration (Flyway/Liquibase) configured? Is the app packaged as a self-contained JAR (preferred) or WAR?

9. **General Idioms**:
   - Constructor injection over field injection (`@Autowired` on fields)
   - `@RestController` = `@Controller` + `@ResponseBody` — use it for REST APIs
   - Return `ResponseEntity<T>` from controllers when status codes matter
   - `Optional<T>` from repository methods, never `null`

### Step 3: Report Findings
For each issue, report:
- **Chapter reference** (e.g., "Ch 3: Externalized Configuration")
- **Location** in the code
- **What's wrong** (the anti-pattern)
- **How to fix it** (the Spring Boot idiomatic way)
- **Priority**: Critical (security/bugs), Important (maintainability), Suggestion (polish)

### Step 4: Provide Fixed Code
Offer a corrected version with comments explaining each change.

---

## Mode 2: Writing New Code

When the user asks you to **write** new Spring Boot code, apply these core principles:

### Project Bootstrap (Ch 1, 2)

1. **Start with Spring Initializr** (Ch 1). Use `start.spring.io` or `spring init` CLI. Select starters upfront — don't add raw dependencies manually.

2. **Use starters, not individual dependencies** (Ch 2). `spring-boot-starter-web` includes Tomcat, Spring MVC, Jackson, and logging at compatible versions. Never declare `spring-webmvc` + `jackson-databind` + `tomcat-embed-core` separately.

3. **The main class is the only required boilerplate** (Ch 2):
   ```java
   @SpringBootApplication
   public class MyApp {
       public static void main(String[] args) {
           SpringApplication.run(MyApp.class, args);
       }
   }
   ```
   `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`.

### Configuration (Ch 3)

4. **Externalize all environment-specific values** (Ch 3). Nothing deployment-specific belongs in code. Use `application.properties` / `application.yml` for defaults.

5. **Use `@ConfigurationProperties` for grouped config** (Ch 3). Bind a prefix to a POJO — type-safe, IDE-friendly, testable:
   ```java
   @ConfigurationProperties(prefix = "app.mail")
   @Component
   public class MailProperties {
       private String host;
       private int port = 25;
       // getters + setters
   }
   ```

6. **Use profiles for environment differences** (Ch 3). `application-dev.properties` overrides `application.properties` when `spring.profiles.active=dev`. Never use `if (env.equals("production"))` in code.

7. **Override auto-configuration surgically** (Ch 3). Use `spring.*` properties first. Only define a `@Bean` when properties are insufficient. Annotate with `@ConditionalOnMissingBean` if providing a fallback.

8. **Customize error pages declaratively** (Ch 3). Place `error/404.html`, `error/500.html` in `src/main/resources/templates/error/`. No custom `ErrorController` needed for basic cases.

### Security (Ch 3)

9. **Extend `WebSecurityConfigurerAdapter` only for custom rules** (Ch 3). For simple HTTP Basic with custom users, `spring.security.user.name` / `spring.security.user.password` properties suffice.

10. **Always secure Actuator endpoints in production** (Ch 7). Expose only `health` and `info` publicly; require authentication for `env`, `beans`, `mappings`, `shutdown`.

### REST Controllers (Ch 2)

11. **Use `@RestController` for API endpoints** (Ch 2). Eliminates `@ResponseBody` on every method.

12. **Return `ResponseEntity<T>` when HTTP status matters** (Ch 2). `ResponseEntity.ok(body)`, `ResponseEntity.notFound().build()`, `ResponseEntity.status(201).body(created)`.

13. **Use constructor injection, not field injection** (Ch 2). Constructor injection makes dependencies explicit and enables testing without Spring context:
    ```java
    // Prefer this:
    @RestController
    public class BookController {
        private final BookRepository repo;
        public BookController(BookRepository repo) { this.repo = repo; }
    }
    ```

14. **Use `Optional` from repository queries** (Ch 2). `repo.findById(id).orElseThrow(() -> new ResponseStatusException(NOT_FOUND))`.

### Testing (Ch 4)

15. **Match test slice to the layer being tested** (Ch 4):
    - Web layer only → `@WebMvcTest(MyController.class)` + `MockMvc`
    - Repository only → `@DataJpaTest`
    - Full app → `@SpringBootTest`
    - External service → `@MockBean` to replace

16. **Use `MockMvc` for controller assertions without starting a server** (Ch 4):
    ```java
    mockMvc.perform(get("/books/1"))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.title").value("Spring Boot in Action"));
    ```

17. **Use `@MockBean` to isolate the unit under test** (Ch 4). Replaces the real bean in the Spring context with a Mockito mock — cleaner than manual wiring.

18. **Test security explicitly** (Ch 4). Use `.with(user("admin").roles("ADMIN"))` or `@WithMockUser` to assert secured endpoints reject unauthenticated requests.

### Actuator (Ch 7)

19. **Enable Actuator in every production app** (Ch 7). Add `spring-boot-starter-actuator`. At minimum expose `health` and `info`.

20. **Write custom `HealthIndicator` for critical dependencies** (Ch 7):
    ```java
    @Component
    public class DatabaseHealthIndicator implements HealthIndicator {
        @Override
        public Health health() {
            return canConnect() ? Health.up().build()
                                : Health.down().withDetail("reason", "timeout").build();
        }
    }
    ```

21. **Add custom metrics via `MeterRegistry`** (Ch 7). Counter, gauge, timer — gives Prometheus/Grafana visibility into business events.

22. **Restrict Actuator exposure in production** (Ch 7):
    ```properties
    management.endpoints.web.exposure.include=health,info
    management.endpoint.health.show-details=when-authorized
    ```

### Deployment (Ch 8)

23. **Package as an executable JAR by default** (Ch 8). `mvn package` produces a fat JAR with embedded Tomcat. Run with `java -jar app.jar`. No application server needed.

24. **Create a production profile** (Ch 8). `application-production.properties` sets `spring.datasource.url`, disables dev tools, sets log levels to WARN.

25. **Use Flyway or Liquibase for database migrations** (Ch 8). Add `spring-boot-starter-flyway`; place scripts in `classpath:db/migration/V1__init.sql`. Never use `spring.jpa.hibernate.ddl-auto=create` in production.

---

## Starter Cheat Sheet (Ch 2, Appendix B)

| Need | Starter |
|------|---------|
| REST API | `spring-boot-starter-web` |
| JPA / Hibernate | `spring-boot-starter-data-jpa` |
| Security | `spring-boot-starter-security` |
| Observability | `spring-boot-starter-actuator` |
| Testing | `spring-boot-starter-test` |
| Thymeleaf views | `spring-boot-starter-thymeleaf` |
| Redis cache | `spring-boot-starter-data-redis` |
| Messaging | `spring-boot-starter-amqp` |
| DB migration | `flyway-core` |

---

## Code Structure Template

```java
// Main class (Ch 2)
@SpringBootApplication
public class LibraryApp {
    public static void main(String[] args) {
        SpringApplication.run(LibraryApp.class, args);
    }
}

// Entity (Ch 2)
@Entity
public class Book {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;
    private String isbn;
    // constructors, getters, setters
}

// Repository (Ch 2)
public interface BookRepository extends JpaRepository<Book, Long> {
    List<Book> findByTitleContainingIgnoreCase(String title);
}

// Service (Ch 2) — constructor injection
@Service
public class BookService {
    private final BookRepository repo;
    public BookService(BookRepository repo) { this.repo = repo; }

    public Book findById(Long id) {
        return repo.findById(id)
                   .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }
}

// Controller (Ch 2)
@RestController
@RequestMapping("/api/books")
public class BookController {
    private final BookService service;
    public BookController(BookService service) { this.service = service; }

    @GetMapping("/{id}")
    public ResponseEntity<Book> getBook(@PathVariable Long id) {
        return ResponseEntity.ok(service.findById(id));
    }

    @PostMapping
    public ResponseEntity<Book> createBook(@RequestBody Book book) {
        Book saved = service.save(book);
        URI location = URI.create("/api/books/" + saved.getId());
        return ResponseEntity.created(location).body(saved);
    }
}

// application.properties (Ch 3)
// spring.datasource.url=jdbc:postgresql://localhost/library
// spring.datasource.username=${DB_USER}
// spring.datasource.password=${DB_PASS}
// spring.jpa.hibernate.ddl-auto=validate
// management.endpoints.web.exposure.include=health,info

// application-dev.properties (Ch 3)
// spring.datasource.url=jdbc:h2:mem:library
// spring.jpa.hibernate.ddl-auto=create-drop
// logging.level.org.springframework=DEBUG
```

---

## Priority of Practices by Impact

### Critical (Security & Correctness)
- Ch 3: Never hardcode credentials — use `${ENV_VAR}` in properties
- Ch 3: Secure Actuator endpoints — `env`, `beans`, `shutdown` must require auth
- Ch 4: Test secured endpoints explicitly — assert 401/403 on unauthenticated requests
- Ch 8: Never use `ddl-auto=create` in production — use Flyway/Liquibase

### Important (Idiom & Maintainability)
- Ch 2: Constructor injection over `@Autowired` field injection
- Ch 2: `@RestController` over `@Controller` + `@ResponseBody` for APIs
- Ch 2: `Optional` from repository, never `null`
- Ch 3: `@ConfigurationProperties` over scattered `@Value` for grouped config
- Ch 3: Profiles for environment differences — not `if` statements
- Ch 4: `@WebMvcTest` for controller tests — not full `@SpringBootTest`
- Ch 7: Custom `HealthIndicator` for each critical dependency

### Suggestions (Polish)
- Ch 3: Custom error pages in `templates/error/` — no code needed
- Ch 7: Custom metrics via `MeterRegistry` for business events
- Ch 8: Production profile disables dev tools, sets WARN log level
- Ch 2: Use `spring-boot-devtools` in dev for live reload
