---
name: spring-ai-mcp-server-patterns
description: Provides Spring Boot MCP server patterns that create Model Context Protocol servers with Spring AI by defining tool handlers, exposing resources, configuring prompt templates, and setting up transports for AI function calling and tool calling. Use when building MCP servers to extend AI capabilities with Spring's official AI framework, implementing AI tools, custom function calling, or MCP client integration.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Spring AI MCP Server Implementation Patterns

Implements MCP servers with Spring AI for AI function calling, tool handlers, and MCP transport configuration.

## Overview

Production-ready MCP server patterns: `@Tool` functions, `@PromptTemplate` resources, and stdio/HTTP/SSE transports with Spring AI security.

## When to Use

MCP servers, Spring AI function calling, AI tools, tool calling, custom tool handlers, Spring Boot MCP, resource endpoints, or MCP transport configuration.

## Quick Reference

### Core Annotations

| Annotation | Target | Purpose |
|-----------|--------|---------|
| `@EnableMcpServer` | Class | Enable MCP server auto-configuration |
| `@Tool(description)` | Method | Declare AI-callable tool |
| `@ToolParam(value)` | Parameter | Document tool parameter for AI |
| `@PromptTemplate(name)` | Method | Declare reusable prompt template |
| `@PromptParam(value)` | Parameter | Document prompt parameter |

### Transport Types

| Transport | Use Case | Config |
|-----------|----------|--------|
| `stdio` | Local process / Claude Desktop | Default |
| `http` | Remote HTTP clients | `port`, `path` |
| `sse` | Real-time streaming clients | `port`, `path` |

### Key Dependencies

```xml
<!-- Maven -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mcp-server</artifactId>
    <version>1.0.0</version>
</dependency>
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
    <version>1.0.0</version>
</dependency>
```

```gradle
// Gradle
implementation 'org.springframework.ai:spring-ai-mcp-server:1.0.0'
implementation 'org.springframework.ai:spring-ai-starter-model-openai:1.0.0'
```

## Instructions

### 1. Project Setup

Add Spring AI MCP dependencies (see Quick Reference above), configure the AI model in `application.properties`, and enable MCP with `@EnableMcpServer`:

```java
@SpringBootApplication
@EnableMcpServer
public class MyMcpApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyMcpApplication.class, args);
    }
}
```

```properties
spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.mcp.enabled=true
spring.ai.mcp.transport.type=stdio
```

### 2. Define Tools

Annotate methods with `@Tool` inside `@Component` beans. Use `@ToolParam` to document parameters:

```java
@Component
public class WeatherTools {

    @Tool(description = "Get current weather for a city")
    public WeatherData getWeather(@ToolParam("City name") String city) {
        return weatherService.getCurrentWeather(city);
    }

    @Tool(description = "Get 5-day forecast for a city")
    public ForecastData getForecast(
            @ToolParam("City name") String city,
            @ToolParam(value = "Unit: celsius or fahrenheit", required = false) String unit) {
        return weatherService.getForecast(city, unit != null ? unit : "celsius");
    }
}
```

See [references/implementation-patterns.md](references/implementation-patterns.md) for database tools, API integration tools, and the `FunctionCallback` low-level pattern.

### 3. Create Prompt Templates

```java
@Component
public class CodeReviewPrompts {

    @PromptTemplate(
        name = "java-code-review",
        description = "Review Java code for best practices and issues"
    )
    public Prompt createCodeReviewPrompt(
            @PromptParam("code") String code,
            @PromptParam(value = "focusAreas", required = false) List<String> focusAreas) {

        String focus = focusAreas != null ? String.join(", ", focusAreas) : "general best practices";
        return Prompt.builder()
                .system("You are an expert Java code reviewer with 20 years of experience.")
                .user("Review the following Java code for " + focus + ":\n```java\n" + code + "\n```")
                .build();
    }
}
```

See [references/implementation-patterns.md](references/implementation-patterns.md) for additional prompt template patterns.

### 4. Configure Transport

```yaml
spring:
  ai:
    mcp:
      enabled: true
      transport:
        type: stdio       # stdio | http | sse
        http:
          port: 8080
          path: /mcp
      server:
        name: my-mcp-server
        version: 1.0.0
```

### 5. Add Security

```java
@Configuration
public class McpSecurityConfig {

    @Bean
    public ToolFilter toolFilter(SecurityService securityService) {
        return (tool, context) -> {
            User user = securityService.getCurrentUser();
            if (tool.name().startsWith("admin_")) {
                return user.hasRole("ADMIN");
            }
            return securityService.isToolAllowed(user, tool.name());
        };
    }
}
```

Use `@PreAuthorize("hasRole('ADMIN')")` on tool methods for method-level security. See [references/implementation-patterns.md](references/implementation-patterns.md) for full security patterns.

### 6. Testing

```java
@SpringBootTest
class WeatherToolsTest {

    @Autowired
    private WeatherTools weatherTools;

    @MockBean
    private WeatherService weatherService;

    @Test
    void testGetWeather_Success() {
        when(weatherService.getCurrentWeather("London"))
            .thenReturn(new WeatherData("London", "Cloudy", 15.0));

        WeatherData result = weatherTools.getWeather("London");

        assertThat(result.city()).isEqualTo("London");
        verify(weatherService).getCurrentWeather("London");
    }
}
```

See [references/testing-guide.md](references/testing-guide.md) for integration tests, Testcontainers, security tests, and slice tests.

## Best Practices

### Tool Design
- Keep tools focused — one operation per tool
- Use clear, action-oriented names (`getWeather`, `executeQuery`)
- Always annotate parameters with `@ToolParam` and descriptive text
- Return structured records/DTOs, not raw strings or maps
- Design tools to be idempotent when possible

### Security
- Validate and sanitize all inputs — AI-generated parameters are untrusted
- Use parameterized queries for SQL; validate and normalize paths for file tools
- Apply `@PreAuthorize` for role-based access on sensitive tools
- Audit log all data-modifying tool executions
- Never expose credentials or sensitive data in tool descriptions or error messages

### Performance
- Use `@Cacheable` for expensive operations with appropriate TTL
- Set timeouts for all external calls
- Use `@Async` for long-running operations
- Monitor with Micrometer metrics

### Error Handling
- Return structured error responses with user-friendly messages
- Log context (user, tool name, parameters) for debugging
- Implement retry logic for transient failures
- Implement `@ControllerAdvice` for consistent error responses

## Examples

### Example 1: Minimal Weather MCP Server

```java
@SpringBootApplication
@EnableMcpServer
public class WeatherMcpApplication {
    public static void main(String[] args) {
        SpringApplication.run(WeatherMcpApplication.class, args);
    }
}

@Component
public class WeatherTools {

    @Tool(description = "Get current weather for a city")
    public WeatherData getWeather(@ToolParam("City name") String city) {
        return new WeatherData(city, "Sunny", 22.5);
    }
}

record WeatherData(String city, String condition, double temperatureCelsius) {}
```

### Example 2: Secure Database Tool

```java
@Component
@PreAuthorize("hasRole('USER')")
public class DatabaseTools {

    private final JdbcTemplate jdbcTemplate;

    @Tool(description = "Execute a read-only SQL query and return results")
    public QueryResult executeQuery(
            @ToolParam("SQL SELECT query") String sql,
            @ToolParam(value = "Parameters as JSON map", required = false) String paramsJson) {

        if (!sql.trim().toUpperCase().startsWith("SELECT")) {
            throw new IllegalArgumentException("Only SELECT queries are allowed");
        }
        List<Map<String, Object>> rows = jdbcTemplate.queryForList(sql);
        return new QueryResult(rows, rows.size());
    }
}
```

See [references/examples.md](references/examples.md) for complete examples including file system tools, REST API integration, and prompt template servers.

## Constraints and Warnings

### Security
- **Never expose** sensitive data in tool descriptions, parameters, or error messages
- **Input validation is mandatory** — always validate before executing
- **External content is untrusted** — tools fetching URLs may receive prompt injection payloads; validate all fetched content
- **SQL injection**: use parameterized queries exclusively
- **Path traversal**: normalize and validate all file paths against a base path

### Operational
- Responses should be concise — large responses can exceed AI context window limits
- All tools must implement timeouts; default should be configurable
- Rate limit expensive operations
- Tools may be called concurrently — ensure thread safety

### Spring AI Specific
- Spring AI is actively developed — pin specific versions in production
- Error messages thrown by tools are exposed to AI models; sanitize them
- Choose transport type carefully: `stdio` for local processes, `http`/`sse` for remote clients

## References

Consult these files for detailed patterns and examples:

- **[references/implementation-patterns.md](references/implementation-patterns.md)** - Tool creation, prompt templates, FunctionCallback, Spring Boot auto-configuration, application properties
- **[references/advanced-patterns.md](references/advanced-patterns.md)** - Dynamic tool registration, multi-model support, caching, error handling
- **[references/testing-guide.md](references/testing-guide.md)** - Unit tests, integration tests, Testcontainers, security tests, slice tests
- **[references/examples.md](references/examples.md)** - Complete server examples: weather, database, file system, REST API, prompt templates
- **[references/api-reference.md](references/api-reference.md)** - Full API: annotations, interfaces, configuration classes, transport implementations, event system
- **[references/migration-guide.md](references/migration-guide.md)** - Migrating from LangChain4j MCP to Spring AI MCP
