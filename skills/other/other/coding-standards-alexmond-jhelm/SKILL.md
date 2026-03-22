---
name: coding-standards
description: jhelm project coding standards and conventions for Java 21 with Lombok and Maven
user-invocable: false
---

## jhelm Coding Standards

### Style
- **Indentation**: Tabs (enforced by `spring-javaformat-maven-plugin`)
- **Naming**: Classes `PascalCase`, methods/variables `camelCase`, constants `UPPER_SNAKE_CASE`
- **Javadoc**: HTML tags for links, `{@code true}`/`{@code false}` for booleans, accurate `@param`/`@return` tags

### Lombok
- `@Getter`/`@Setter` for simple fields, `@Data` for POJOs/DTOs
- `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor` for complex objects
- `@Slf4j` for logging
- `@Accessors(fluent = true)` for internal DSL-like classes

### Modern Java 21
- **Text blocks** (`"""..."""`) for multi-line strings
- **Enhanced switch** (arrow syntax)
- **Streams/Lambdas** for collection manipulation
- **try-with-resources** for system resource streams (e.g., `Files.walk()`)

### Error Handling
- SLF4J via `@Slf4j` — no `System.out.println` in production code (CLI output in `jhelm-app` is the exception)
- Descriptive exceptions; always include original cause when rethrowing
- Prefer `must*` function variants when strict validation is required

### Dependencies
- Manage versions in root `pom.xml` `<dependencyManagement>`
- Define dependency versions as properties in root `pom.xml` `<properties>` (unless managed by Spring Boot parent)
- Keep `jhelm-gotemplate` free of Spring dependencies

### Size Guidelines

Two thresholds apply — **consider** and **enforce**:

| Scope | Consider refactoring | Checkstyle enforces (build fails) |
|---|---|---|
| **File** | > 500 lines | > 1000 lines |
| **Method** | > 50 lines | > 80 lines |

**Consider (500 lines / 50 lines):** A warning signal. Before adding more code to a large file or method, ask whether it should be split. Extract helpers, separate concerns, or move related methods to a dedicated class.

**Enforce (1000 lines / 80 lines):** Hard limit. The build fails at `validate` phase. Refactoring is required — no exceptions except the suppressions below.

**Current suppressions** (`checkstyle-suppressions.xml`):
- `Lexer.java`, `Parser.java` — state machines; long methods are inherent to the pattern
- `HelmChartTemplates.java` — methods return static YAML text blocks, not logic
- `*Test.java` — test files are exempt from both size limits

### Checkstyle Rules (enforced — violations fail build)
- **Catch variable**: must be `ex`, not `e` (SpringCatch)
- **Braces required**: `if/else/for/while` always need `{}` (NeedBraces)
- **Lambda params**: single-param lambdas need parens: `(r) -> ...` not `r -> ...` (SpringLambda)
- **Lambda blocks**: `-> { return x; }` → `-> x` when body is single expression (SpringLambda)
- **Ternary conditions**: wrap in parens: `(a != null) ? x : y` (SpringTernary)
- **No star imports**: expand `.*` to explicit class imports (AvoidStarImport)
- **Inner classes last**: inner/nested types must appear after all methods (InnerTypeLast)
- **Utility classes**: must have `private Constructor() {}` AND be `final` (SpringHideUtilityClassConstructor + FinalClass)
- **Annotation arrays**: no trailing comma before `})` in `@CsvSource`, etc. (AnnotationUseStyle)

Auto-fix: `./mvnw spring-javaformat:apply` then use the `/checkstyle` skill for remaining violations.

### Testing
- JUnit 5 (`org.junit.jupiter.api`) with `Assertions`
- `@TempDir` for temporary files
- Always run tests after code changes

### Test Data: Prefer Real over Mocks

**Prefer real test data over mocks.** Mocks are slow to maintain, hide intent, and test the wrong thing when the real thing is easy to use.

| Scenario | Preferred approach |
|---|---|
| Template rendering | Inline Go template strings or files in `src/test/resources/test-charts/` |
| YAML parsing | Inline YAML text blocks or files in test resources |
| Chart loading/untarring | Minimal chart dir in `src/test/resources/test-charts/`, or small programmatic `.tgz` |
| File system operations | `@TempDir` with real files |
| HTTP calls (updateRepo, pullFromUrl, OCI) | Mockito mock on `CloseableHttpClient` — acceptable, network is unavoidable |
| Kubernetes API calls | Mockito mock on `KubeService` — acceptable |

**When Mockito IS appropriate:**
- HTTP client (`CloseableHttpClient`) — network I/O has no real alternative
- Kubernetes client (`KubeService`) — requires a live cluster
- External services with no local substitute

**Creating minimal test charts** — place in `src/test/resources/test-charts/<name>/`:
```
Chart.yaml   (name, version, apiVersion)
values.yaml  (minimal defaults)
templates/   (one simple template)
```
Use `new TarArchiveOutputStream(new GzipCompressorOutputStream(...))` in a helper method when a `.tgz` is needed in-memory.

### Parameterized Tests
Use `@ParameterizedTest` to avoid code duplication and loops in tests. Prefer parameterized tests over:
- Multiple near-identical `@Test` methods that differ only in input/expected values
- `for` loops inside test methods that iterate over test cases
- Copy-pasted test logic with different data

**Common sources:**
- `@CsvSource` — inline comma-separated values for simple types
- `@ValueSource` — single-argument tests with strings, ints, etc.
- `@MethodSource` — complex objects or multi-arg via static factory method returning `Stream<Arguments>`
- `@EnumSource` — iterate over enum values

**Example — prefer this:**
```java
@ParameterizedTest
@CsvSource({
    "hello, HELLO",
    "world, WORLD",
    "'', ''"
})
void testUpperCase(String input, String expected) {
    assertEquals(expected, input.toUpperCase());
}
```

**Over this:**
```java
@Test
void testUpperCase() {
    assertEquals("HELLO", "hello".toUpperCase());
    assertEquals("WORLD", "world".toUpperCase());
    assertEquals("", "".toUpperCase());
}
```

**Use `@MethodSource` for complex data:**
```java
@ParameterizedTest
@MethodSource("templateTestCases")
void testTemplateRendering(String template, Map<String, Object> data, String expected) {
    // ...
}

static Stream<Arguments> templateTestCases() {
    return Stream.of(
        Arguments.of("{{ .name }}", Map.of("name", "Alice"), "Alice"),
        Arguments.of("{{ .count }}", Map.of("count", 42), "42")
    );
}
```
