---
name: java-ecosystem
description: Java 25 development patterns for the crypto-scout ecosystem including microservices, ActiveJ, and async I/O
license: MIT
compatibility: opencode
metadata:
  language: java
  version: "25"
  framework: activej
  domain: microservices
---

## What I Do

Provide comprehensive guidance for Java 25 development across the crypto-scout ecosystem, covering microservice patterns, ActiveJ framework usage, and async I/O operations.

## Core Architecture

### Launcher Pattern (ActiveJ)
```java
public final class Service extends Launcher {
    
    @Override
    protected Module getModule() {
        return combine(
            JmxModule.create(),
            ServiceGraphModule.create(),
            CoreModule.create(),
            ServiceModule.create(),
            WebModule.create()
        );
    }
    
    @Override
    protected void onStart() throws Exception {
        ConfigValidator.validate();
    }
    
    @Override
    protected void run() throws Exception {
        awaitShutdown();
    }
    
    public static void main(String[] args) throws Exception {
        new Service().launch(args);
    }
}
```

### Module Structure
| Module | Purpose | Location |
|--------|---------|----------|
| CoreModule | Reactor and virtual thread executor | All services |
| WebModule | HTTP server, clients, health routes | All services |
| ClientModule | AMQP publisher lifecycle | crypto-scout-client |
| CollectorModule | Repositories and services | crypto-scout-collector |
| AnalystModule | Analysis services | crypto-scout-analyst |

### Reactive Service Pattern
```java
public final class MyService extends AbstractReactive implements ReactiveService {
    private final Executor executor;
    private volatile Resource resource;
    
    public static MyService create(NioReactor reactor, Executor executor) {
        return new MyService(reactor, executor);
    }
    
    private MyService(NioReactor reactor, Executor executor) {
        super(reactor);
        this.executor = executor;
    }
    
    @Override
    public Promise<Void> start() {
        return Promise.ofBlocking(executor, () -> {
            // Initialize resources
            resource = createResource();
        });
    }
    
    @Override
    public Promise<Void> stop() {
        return Promise.ofBlocking(executor, () -> {
            // Cleanup resources
            closeResource(resource);
            resource = null;
        });
    }
}
```

## Code Style Essentials

### File Structure
```
1-23:   MIT License header
25:     Package declaration
26:     Blank line
27+:    Imports (java.* → third-party → static)
        Blank line
        Class declaration
```

### Import Organization
```java
import java.io.IOException;
import java.nio.file.Path;
import java.time.Duration;

import com.rabbitmq.stream.Environment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static com.github.akarazhev.cryptoscout.config.Constants.AmqpConfig.AMQP_RABBITMQ_HOST;
```

### Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `StreamService`, `AmqpPublisher` |
| Methods | camelCase with verb | `waitForDatabaseReady` |
| Constants | UPPER_SNAKE_CASE | `JDBC_URL`, `DB_USER` |
| Locals | `final var` | `final var timeout` |
| Tests | `<Class>Test` | `AmqpPublisherTest` |
| Test methods | `should<Subject><Action>` | `shouldPublishPayload` |

### Error Handling
```java
// Invalid state
if (resource == null) {
    throw new IllegalStateException("Resource not initialized: " + name);
}

// Try-with-resources
try (final var conn = dataSource.getConnection();
     final var stmt = conn.prepareStatement(sql)) {
    // Use resources
} catch (final SQLException e) {
    throw new IllegalStateException("Database error", e);
}

// Interrupt handling
try {
    Thread.sleep(duration.toMillis());
} catch (final InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

## Testing Patterns

### JUnit 6 (Jupiter)
```java
final class MyServiceTest {
    
    @BeforeAll
    static void setUp() {
        PodmanCompose.up();
    }
    
    @AfterAll
    static void tearDown() {
        PodmanCompose.down();
    }
    
    @Test
    void shouldServiceStartSuccessfully() throws Exception {
        final var service = createTestService();
        assertTrue(service.start().isResult());
    }
}
```

### Mock Data Usage
```java
// Load test fixtures
final var spotKlines = MockData.get(
    MockData.Source.BYBIT_SPOT, 
    MockData.Type.KLINE_1
);
final var fgi = MockData.get(
    MockData.Source.CRYPTO_SCOUT, 
    MockData.Type.FGI
);
```

## Configuration Pattern
```java
static final String VALUE = System.getProperty("property.key", "defaultValue");
static final int PORT = Integer.parseInt(System.getProperty("port.key", "5552"));
static final Duration TIMEOUT = Duration.ofMinutes(Long.getLong("timeout.key", 3L));
```

## When to Use Me

Use this skill when:
- Writing new Java classes or services
- Understanding ActiveJ patterns and lifecycle
- Implementing reactive services with Promise/async
- Organizing imports and file structure
- Following error handling and logging conventions
- Writing JUnit 6 tests with proper lifecycle
- Configuring services via system properties
