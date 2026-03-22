---
name: coding-java
cluster: coding
description: "Java 21+: records, sealed classes, pattern matching, virtual threads Loom, Spring Boot 3, Maven/Gradle"
tags: ["java","spring","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "java spring boot maven gradle virtual threads records sealed"
---

# coding-java

## Purpose
This skill enables the AI to assist with Java 21+ development, focusing on modern features like records, sealed classes, pattern matching, and virtual threads from Project Loom, plus Spring Boot 3 applications using Maven or Gradle for building and dependency management.

## When to Use
Use this skill for projects requiring Java 21+ syntax, such as implementing sealed classes for restricted inheritance, pattern matching in switch statements, or scalable applications with virtual threads. Apply it in backend development with Spring Boot 3, or when managing builds with Maven/Gradle for enterprise-grade Java apps.

## Key Capabilities
- Handle Java records for immutable data classes: Define with `record Point(int x, int y) {}`.
- Implement sealed classes to limit subclasses: Use `sealed interface Shape permits Circle, Square {}`.
- Utilize pattern matching in switch: Example: `switch (obj) { case String s -> process(s); default -> handleDefault(); }`.
- Manage virtual threads for concurrency: Launch with `Thread.startVirtualThread(() -> task());` in Java 21+.
- Build Spring Boot 3 apps: Configure with `@SpringBootApplication` and use embedded Tomcat.
- Automate builds: Run Maven with `mvn spring-boot:run` or Gradle with `gradle bootRun` for project compilation.

## Usage Patterns
To accomplish tasks, structure code or commands precisely. For example, to create a Java record for a data model:
1. Write: `public record User(String name, int age) {}`.
2. Use in main method: `User user = new User("Alice", 30); System.out.println(user);`.

Another example: Set up a Spring Boot 3 app with virtual threads.
1. Add dependency in pom.xml: `<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>`.
2. In controller: `@RestController public class MyController { @GetMapping("/") public String home() { Thread.startVirtualThread(() -> logMessage()); return "Hello"; } }`.
3. Run with Maven: `mvn spring-boot:run --define spring.threads.virtual.enabled=true`.

## Common Commands/API
Use these exact commands for building and running projects:
- Maven: `mvn clean install -DskipTests` to compile; `mvn spring-boot:run` to start app.
- Gradle: `gradle build --no-daemon` for compilation; `gradle bootRun --args='--server.port=8080'` for running.
- Java API for virtual threads: `ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor(); executor.submit(() -> { /* task code */ });`.
- Spring Boot API: Access endpoints like `http://localhost:8080/api/data` after defining `@GetMapping("/api/data") public ResponseEntity<?> getData() { return ResponseEntity.ok(data); }`.
- Config formats: Use application.properties for settings, e.g., `server.port=8080`; or YAML: `server: port: 8080`.

## Integration Notes
Integrate by setting environment variables for secure keys, e.g., export `$SPRING_API_KEY` for external services in Spring Boot. For IDEs, add plugins like Spring Tools Suite and configure build tools: In VS Code, use extensions for Maven/Gradle. To link with databases, add dependencies in build.gradle: `implementation 'org.springframework.boot:spring-boot-starter-data-jpa'`, then configure datasource in application.yml: `spring.datasource.url=jdbc:mysql://localhost/dbname`. Ensure Java 21+ is set via SDK manager.

## Error Handling
Handle errors prescriptively: For build failures, check logs for "Compilation error" and fix syntax, e.g., if sealed class is misused, ensure all permitted subclasses are defined. For virtual threads, catch `InterruptedException` with `try { Thread.startVirtualThread(() -> { throw new RuntimeException(); }); } catch (Exception e) { log.error(e.getMessage()); }`. In Spring Boot, use `@ExceptionHandler` for API errors: `@ControllerAdvice public class GlobalExceptionHandler { @ExceptionHandler(Exception.class) public ResponseEntity<?> handleError(Exception e) { return ResponseEntity.status(500).body("Error: " + e.getMessage()); } }`. For Maven/Gradle, use `--debug` flag to diagnose, e.g., `mvn clean install --debug`.

## Graph Relationships
- Related to: coding-general (via cluster 'coding' for shared coding tools).
- Connected to: coding-python (for cross-language development patterns).
- Links with: devops-deployment (for integrating Java builds with CI/CD pipelines).
