---
name: spring-ai-mcp-server-patterns
description: Model Context Protocol (MCP) server implementation patterns with Spring AI. Use when building MCP servers to extend AI capabilities with custom tools, resources, and prompt templates using Spring's official AI framework.
category: ai-integration
tags: [spring-ai, mcp, model-context-protocol, tools, function-calling, prompts, java, spring-boot, enterprise]
version: 1.0.0
allowed-tools: Read, Write, Bash, WebFetch
---

# Spring AI MCP Server Implementation Patterns

Implement Model Context Protocol (MCP) servers with Spring AI to extend AI capabilities with standardized tools, resources, and prompt templates using Spring's native AI abstractions.

## When to Use

Use this skill when building:
- AI applications requiring external tool integration with Spring AI
- Enterprise MCP servers with Spring ecosystem integration
- Function calling servers with Spring AI's declarative patterns
- Prompt template servers for standardized AI interactions
- Spring Boot applications with native MCP integration
- Production-ready MCP servers with Spring Security and monitoring
- Microservices that expose AI capabilities via MCP protocol
- Hybrid systems using both Spring AI and traditional Spring components

## Quick Start

### Basic MCP Server with Spring AI

Create a simple MCP server with function calling:

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
        // Implementation
        return new WeatherData(city, "Sunny", 22.5);
    }
}
```

### Function Calling Setup

Configure function calling in `application.properties`:

```properties
spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.mcp.enabled=true
spring.ai.mcp.transport=stdio
```

### Build Configuration

Add Spring AI MCP dependencies to your project:

**Maven:**
```xml
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

**Gradle:**
```gradle
dependencies {
    implementation 'org.springframework.ai:spring-ai-mcp-server:1.0.0'
    implementation 'org.springframework.ai:spring-ai-starter-model-openai:1.0.0'
}
```

**Or use Spring Boot starter:**
```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mcp-starter</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Core Concepts

### MCP Architecture with Spring AI

MCP standardizes AI application connections with Spring AI abstractions:
- **Tools**: Executable functions using `@Tool` annotation
- **Resources**: Data sources accessible via Spring components
- **Prompts**: Template-based interactions with `@PromptTemplate`
- **Transport**: Spring-managed communication channels

```
AI Application ←→ MCP Client ←→ Spring AI ←→ MCP Server ←→ Spring Services
```

### Key Spring AI Components

- **@Tool**: Declares methods as callable functions for AI models
- **@ToolParam**: Documents parameter purposes for AI understanding
- **@PromptTemplate**: Defines reusable prompt patterns
- **@Model**: Specifies AI model configurations
- **FunctionCallback**: Low-level function calling integration

## Implementation Patterns

### Tool Creation Pattern

Create tools with Spring AI's declarative approach:

```java
@Component
public class DatabaseTools {

    private final JdbcTemplate jdbcTemplate;

    public DatabaseTools(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Tool(description = "Execute a safe read-only SQL query")
    public List<Map<String, Object>> executeQuery(
            @ToolParam("SQL SELECT query") String query,
            @ToolParam(value = "Query parameters", required = false)
            Map<String, Object> params) {

        // Validate query is read-only
        if (!query.trim().toUpperCase().startsWith("SELECT")) {
            throw new IllegalArgumentException("Only SELECT queries are allowed");
        }

        return jdbcTemplate.queryForList(query, params);
    }

    @Tool(description = "Get table schema information")
    public TableSchema getTableSchema(
            @ToolParam("Table name") String tableName) {

        String sql = "SELECT column_name, data_type " +
                     "FROM information_schema.columns " +
                     "WHERE table_name = ?";

        List<Map<String, Object>> columns = jdbcTemplate.queryForList(sql, tableName);
        return new TableSchema(tableName, columns);
    }
}

record TableSchema(String tableName, List<Map<String, Object>> columns) {}
```

### Advanced Tool Pattern with Validation

```java
@Component
public class ApiTools {

    private final WebClient webClient;

    public ApiTools(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

    @Tool(description = "Make HTTP GET request to an API")
    public ApiResponse callApi(
            @ToolParam("API URL") String url,
            @ToolParam(value = "Headers as JSON string", required = false)
            String headersJson) {

        // Validate URL
        try {
            new URL(url);
        } catch (MalformedURLException e) {
            throw new IllegalArgumentException("Invalid URL format");
        }

        // Parse headers if provided
        HttpHeaders headers = new HttpHeaders();
        if (headersJson != null && !headersJson.isBlank()) {
            try {
                Map<String, String> headersMap = new ObjectMapper()
                    .readValue(headersJson, Map.class);
                headersMap.forEach(headers::add);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException("Invalid headers JSON");
            }
        }

        return webClient.get()
                .uri(url)
                .headers(h -> h.addAll(headers))
                .retrieve()
                .bodyToMono(ApiResponse.class)
                .block();
    }
}

record ApiResponse(int status, Map<String, Object> body, HttpHeaders headers) {}
```

### Prompt Template Pattern

Create reusable prompt templates with Spring AI:

```java
@Component
public class CodeReviewPrompts {

    @PromptTemplate(
        name = "java-code-review",
        description = "Review Java code for best practices and issues"
    )
    public Prompt createJavaCodeReviewPrompt(
            @PromptParam("code") String code,
            @PromptParam(value = "focusAreas", required = false)
            List<String> focusAreas) {

        String focus = focusAreas != null ?
            String.join(", ", focusAreas) :
            "general best practices";

        return Prompt.builder()
                .system("You are an expert Java code reviewer with 20 years of experience.")
                .user("""
                    Review the following Java code for {focus}:

                    ```java
                    {code}
                    ```

                    Provide feedback in the following format:
                    1. Critical issues (must fix)
                    2. Warnings (should fix)
                    3. Suggestions (consider improving)
                    4. Positive aspects

                    Be specific and provide code examples where relevant.
                    """.replace("{code}", code).replace("{focus}", focus))
                .build();
    }

    @PromptTemplate(
        name = "generate-unit-tests",
        description = "Generate comprehensive unit tests for Java code"
    )
    public Prompt createTestGenerationPrompt(
            @PromptParam("code") String code,
            @PromptParam("className") String className,
            @PromptParam(value = "testingFramework", required = false)
            String framework) {

        String testFramework = framework != null ? framework : "JUnit 5";

        return Prompt.builder()
                .system("You are an expert in test-driven development.")
                .user("""
                    Generate comprehensive unit tests for the following Java class using {testFramework}:

                    ```java
                    {code}
                    ```

                    Class: {className}

                    Requirements:
                    1. Test all public methods
                    2. Include edge cases and boundary conditions
                    3. Use appropriate assertions
                    4. Follow AAA pattern (Arrange, Act, Assert)
                    5. Include test method naming best practices
                    6. Mock external dependencies
                    """.replace("{code}", code)
                      .replace("{className}", className)
                      .replace("{testFramework}", testFramework))
                .build();
    }
}
```

### Function Callback Pattern

Low-level function calling integration:

```java
@Configuration
public class FunctionConfig {

    @Bean
    public FunctionCallback weatherFunction() {
        return FunctionCallback.builder()
                .function("getCurrentWeather", new WeatherService())
                .description("Get the current weather for a location")
                .inputType(WeatherRequest.class)
                .build();
    }

    @Bean
    public FunctionCallback calculatorFunction() {
        return FunctionCallbackWrapper.builder(new Calculator())
                .withName("calculate")
                .withDescription("Perform mathematical calculations")
                .build();
    }
}

class WeatherService implements Function<WeatherRequest, WeatherResponse> {
    @Override
    public WeatherResponse apply(WeatherRequest request) {
        // Call weather API
        return new WeatherResponse(request.location(), 72, "Sunny");
    }
}

record WeatherRequest(String location) {}
record WeatherResponse(String location, double temperature, String condition) {}

class Calculator implements BiFunction<String, Map<String, Object>, String> {
    @Override
    public String apply(String functionName, Map<String, Object> args) {
        // Perform calculation based on args
        return "result";
    }
}
```

## Spring Boot Integration

### Auto-Configuration

Set up MCP server with Spring Boot auto-configuration:

```java
@Configuration
@AutoConfigureAfter({WebMvcAutoConfiguration.class})
@ConditionalOnClass({McpServer.class, ChatModel.class})
@ConditionalOnProperty(name = "spring.ai.mcp.enabled", havingValue = "true", matchIfMissing = true)
public class McpAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public McpServerProperties mcpServerProperties() {
        return new McpServerProperties();
    }

    @Bean
    @ConditionalOnMissingBean
    public McpServer mcpServer(
            List<FunctionCallback> functionCallbacks,
            List<PromptTemplate> promptTemplates,
            McpServerProperties properties
    ) {
        McpServer.Builder builder = McpServer.builder()
                .serverInfo("spring-ai-mcp", "1.0.0")
                .transport(properties.getTransport().create());

        // Register function callbacks as tools
        functionCallbacks.forEach(callback ->
                builder.tool(Tool.fromFunctionCallback(callback))
        );

        // Register prompt templates
        promptTemplates.forEach(template ->
                builder.prompt(Prompt.fromTemplate(template))
        );

        return builder.build();
    }

    @Bean
    @ConditionalOnProperty(name = "spring.ai.mcp.actuator.enabled", havingValue = "true")
    public McpHealthIndicator mcpHealthIndicator(McpServer mcpServer) {
        return new McpHealthIndicator(mcpServer);
    }
}

@ConfigurationProperties(prefix = "spring.ai.mcp")
public class McpServerProperties {
    private boolean enabled = true;
    private TransportConfig transport = new TransportConfig();
    private ActuatorConfig actuator = new ActuatorConfig();

    // Getters and setters

    public static class TransportConfig {
        private TransportType type = TransportType.STDIO;
        private HttpConfig http = new HttpConfig();

        public Transport create() {
            return switch (type) {
                case STDIO -> new StdioTransport();
                case HTTP -> new HttpTransport(http.getPort());
                case SSE -> new SseTransport(http.getPort(), http.getPath());
            };
        }
    }

    public static class HttpConfig {
        private int port = 8080;
        private String path = "/mcp";
        // Getters and setters
    }

    public static class ActuatorConfig {
        private boolean enabled = true;
        // Getters and setters
    }

    public enum TransportType {
        STDIO, HTTP, SSE
    }
}
```

### Application Properties

Configure MCP server in `application.yml`:

```yaml
spring:
  ai:
    mcp:
      enabled: true
      transport:
        type: stdio  # Options: stdio, http, sse
        http:
          port: 8080
          path: /mcp
      actuator:
        enabled: true
      tools:
        package-scan: com.example.tools
      prompts:
        package-scan: com.example.prompts
      security:
        enabled: true
        allowed-tools:
          - getWeather
          - executeQuery
        admin-tools:
          - admin_*
```

### Custom Server Configuration

For advanced configuration:

```java
@Configuration
public class CustomMcpConfig {

    @Bean
    public McpServerCustomizer mcpServerCustomizer() {
        return server -> {
            server.addToolInterceptor((tool, args, chain) -> {
                log.info("Executing tool: {}", tool.name());
                long start = System.currentTimeMillis();
                Object result = chain.execute(tool, args);
                long duration = System.currentTimeMillis() - start;
                log.info("Tool {} executed in {}ms", tool.name(), duration);
                metrics.recordToolExecution(tool.name(), duration);
                return result;
            });
        };
    }

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

@Service
public class SecurityService {
    public boolean isToolAllowed(User user, String toolName) {
        // Implement tool access control logic
        return true;
    }
}
```

## Security & Best Practices

### Tool Security

Implement secure tool execution with Spring Security:

```java
@Component
public class SecureToolExecutor {

    private final McpServer mcpServer;
    private final SecurityContextHolder strategy;

    public SecureToolExecutor(McpServer mcpServer, SecurityContextHolder strategy) {
        this.mcpServer = mcpServer;
        this.strategy = strategy;
    }

    public ToolResult executeTool(String toolName, Map<String, Object> arguments) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();

        if (!(auth instanceof UserAuthentication userAuth)) {
            throw new AccessDeniedException("User not authenticated");
        }

        // Check tool permissions
        if (!hasToolPermission(userAuth.getUser(), toolName)) {
            throw new AccessDeniedException("Tool not allowed: " + toolName);
        }

        // Validate arguments against injection patterns
        validateArguments(arguments);

        // Execute with audit logging
        logToolExecution(userAuth.getUser(), toolName, arguments);

        try {
            ToolResult result = mcpServer.executeTool(toolName, arguments);
            logToolSuccess(userAuth.getUser(), toolName);
            return result;
        } catch (Exception e) {
            logToolFailure(userAuth.getUser(), toolName, e);
            throw new ToolExecutionException("Tool execution failed", e);
        }
    }

    private boolean hasToolPermission(User user, String toolName) {
        // Implement permission logic based on user roles and tool sensitivity
        return user.getAuthorities().stream()
                .anyMatch(auth -> auth.getAuthority().equals("TOOL_" + toolName) ||
                                 auth.getAuthority().equals("ROLE_ADMIN"));
    }

    private void validateArguments(Map<String, Object> arguments) {
        // Implement argument validation to prevent injection attacks
        arguments.forEach((key, value) -> {
            if (value instanceof String str) {
                if (str.contains(";") || str.contains("--")) {
                    throw new IllegalArgumentException("Invalid characters in argument: " + key);
                }
            }
        });
    }

    private void logToolExecution(User user, String toolName, Map<String, Object> arguments) {
        // Implement audit logging
    }

    private void logToolSuccess(User user, String toolName) {
        // Log successful execution
    }

    private void logToolFailure(User user, String toolName, Exception e) {
        // Log failed execution
    }
}

class ToolExecutionException extends RuntimeException {
    public ToolExecutionException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### Input Validation

Use Spring's validation framework:

```java
@Component
public class ValidatedTools {

    @Tool(description = "Process user data with validation")
    @Validated
    public ProcessingResult processUserData(
            @ToolParam("User data to process") @Valid UserData data) {
        // Implementation
        return new ProcessingResult("success", data);
    }
}

record UserData(
    @NotBlank(message = "Name is required")
    @Size(max = 100, message = "Name must be 100 characters or less")
    String name,

    @NotNull(message = "Age is required")
    @Min(value = 18, message = "Must be 18 or older")
    @Max(value = 120, message = "Age must be realistic")
    Integer age,

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    String email
) {}

// Custom validator for sensitive operations
@Component
public class SensitiveOperationValidator {

    public void validateOperation(String operation, User user, Map<String, Object> params) {
        if (isSensitiveOperation(operation)) {
            requireAdditionalAuthentication(user);
            validateOperationLimits(user, operation);
            logSensitiveOperation(user, operation, params);
        }
    }

    private boolean isSensitiveOperation(String operation) {
        return operation.startsWith("delete") || operation.startsWith("update");
    }

    private void requireAdditionalAuthentication(User user) {
        // Implement MFA or re-authentication
    }

    private void validateOperationLimits(User user, String operation) {
        // Check rate limits and quotas
    }

    private void logSensitiveOperation(User user, String operation, Map<String, Object> params) {
        // Secure audit logging
    }
}
```

### Error Handling

Implement comprehensive error handling:

```java
@ControllerAdvice
public class McpExceptionHandler {

    @ExceptionHandler(ToolExecutionException.class)
    public ResponseEntity<ErrorResponse> handleToolExecutionException(
            ToolExecutionException ex, WebRequest request) {

        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error("Tool Execution Failed")
                .message(ex.getMessage())
                .path(((ServletWebRequest) request).getRequest().getRequestURI())
                .build();

        log.error("Tool execution failed: {}", ex.getMessage(), ex);
        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(
            AccessDeniedException ex, WebRequest request) {

        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.FORBIDDEN.value())
                .error("Access Denied")
                .message("You do not have permission to execute this tool")
                .path(((ServletWebRequest) request).getRequest().getRequestURI())
                .build();

        log.warn("Access denied: {}", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleValidationError(
            IllegalArgumentException ex, WebRequest request) {

        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error("Validation Error")
                .message(ex.getMessage())
                .path(((ServletWebRequest) request).getRequest().getRequestURI())
                .build();

        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(
            Exception ex, WebRequest request) {

        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error("Internal Server Error")
                .message("An unexpected error occurred")
                .path(((ServletWebRequest) request).getRequest().getRequestURI())
                .build();

        log.error("Unexpected error: {}", ex.getMessage(), ex);
        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @Data
    @Builder
    static class ErrorResponse {
        private LocalDateTime timestamp;
        private int status;
        private String error;
        private String message;
        private String path;
    }
}
```

## Advanced Patterns

### Dynamic Tool Registration

Register tools at runtime:

```javan@Service
public class DynamicToolRegistry {

    private final McpServer mcpServer;
    private final Map<String, ToolRegistration> registeredTools = new ConcurrentHashMap<>();

    public DynamicToolRegistry(McpServer mcpServer) {
        this.mcpServer = mcpServer;
    }

    public void registerTool(ToolRegistration registration) {
        registeredTools.put(registration.getId(), registration);

        Tool tool = Tool.builder()
                .name(registration.getName())
                .description(registration.getDescription())
                .inputSchema(registration.getInputSchema())
                .function(args -> executeDynamicTool(registration.getId(), args))
                .build();

        mcpServer.addTool(tool);
        log.info("Registered dynamic tool: {}", registration.getName());
    }

    public void unregisterTool(String toolId) {
        ToolRegistration registration = registeredTools.remove(toolId);
        if (registration != null) {
            mcpServer.removeTool(registration.getName());
            log.info("Unregistered dynamic tool: {}", registration.getName());
        }
    }

    private Object executeDynamicTool(String toolId, Map<String, Object> args) {
        ToolRegistration registration = registeredTools.get(toolId);
        if (registration == null) {
            throw new IllegalStateException("Tool not found: " + toolId);
        }

        // Execute based on registration type
        return switch (registration.getType()) {
            case GROOVY_SCRIPT -> executeGroovyScript(registration, args);
            case SPRING_BEAN -> executeSpringBeanMethod(registration, args);
            case HTTP_ENDPOINT -> callHttpEndpoint(registration, args);
        };
    }

    private Object executeGroovyScript(ToolRegistration registration, Map<String, Object> args) {
        // Implement Groovy script execution
        return null;
    }

    private Object executeSpringBeanMethod(ToolRegistration registration, Map<String, Object> args) {
        // Implement Spring bean method invocation
        return null;
    }

    private Object callHttpEndpoint(ToolRegistration registration, Map<String, Object> args) {
        // Implement HTTP call
        return null;
    }
}

@Data
@Builder
class ToolRegistration {
    private String id;
    private String name;
    private String description;
    private Map<String, Object> inputSchema;
    private ToolType type;
    private String target; // script, bean name, or URL
    private Map<String, String> metadata;
}

enum ToolType {
    GROOVY_SCRIPT,
    SPRING_BEAN,
    HTTP_ENDPOINT
}
```

### Multi-Model Support

Support multiple AI models:

```java
@Configuration
public class MultiModelConfig {

    @Bean
    @Primary
    public ChatModel primaryChatModel(@Value("${spring.ai.primary.model}") String modelName) {
        return switch (modelName) {
            case "gpt-4" -> new OpenAiChatModel(OpenAiApi.builder()
                    .apiKey(System.getenv("OPENAI_API_KEY"))
                    .build());
            case "claude" -> new AnthropicChatModel(AnthropicApi.builder()
                    .apiKey(System.getenv("ANTHROPIC_API_KEY"))
                    .build());
            default -> throw new IllegalArgumentException("Unsupported model: " + modelName);
        };
    }

    @Bean
    public Map<String, ChatModel> allChatModels() {
        Map<String, ChatModel> models = new HashMap<>();

        models.put("gpt-4", new OpenAiChatModel(OpenAiApi.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .build()));

        models.put("gpt-3.5", new OpenAiChatModel(OpenAiApi.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .model("gpt-3.5-turbo")
                .build()));

        models.put("claude-opus", new AnthropicChatModel(AnthropicApi.builder()
                .apiKey(System.getenv("ANTHROPIC_API_KEY"))
                .model("claude-3-opus-20240229")
                .build()));

        return models;
    }

    @Bean
    public ModelSelector modelSelector(Map<String, ChatModel> models) {
        return new SpringAiModelSelector(models);
    }
}

@Component
public class SpringAiModelSelector implements ModelSelector {

    private final Map<String, ChatModel> models;

    public SpringAiModelSelector(Map<String, ChatModel> models) {
        this.models = models;
    }

    @Override
    public ChatModel selectModel(Prompt prompt, Map<String, Object> context) {
        // Select model based on prompt complexity, cost, latency requirements
        String modelName = determineBestModel(prompt, context);
        return models.get(modelName);
    }

    private String determineBestModel(Prompt prompt, Map<String, Object> context) {
        // Implement model selection logic
        // Consider: prompt length, complexity, cost constraints, latency requirements
        return "gpt-4";
    }
}
```

### Caching and Performance

Implement caching for tools and prompts:

```java
@Configuration
@EnableCaching
public class McpCacheConfig {

    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager(
            "tool-results",
            "prompt-templates",
            "function-callbacks"
        );
    }
}

@Component
public class CachedToolExecutor {

    private final McpServer mcpServer;

    public CachedToolExecutor(McpServer mcpServer) {
        this.mcpServer = mcpServer;
    }

    @Cacheable(
        value = "tool-results",
        key = "#toolName + '_' + #args.hashCode()",
        unless = "#result.isCacheable() == false"
    )
    public ToolResult executeTool(String toolName, Map<String, Object> args) {
        return mcpServer.executeTool(toolName, args);
    }

    @CacheEvict(value = "tool-results", allEntries = true)
    public void clearToolCache() {
        // Clear cache when tools are updated
    }

    @Cacheable(value = "prompt-templates", key = "#templateName")
    public PromptTemplate getPromptTemplate(String templateName) {
        return mcpServer.getPromptTemplate(templateName);
    }
}
```

## Testing

### Unit Testing Tools

```java
@SpringBootTest
class DatabaseToolsTest {

    @Autowired
    private DatabaseTools databaseTools;

    @MockBean
    private JdbcTemplate jdbcTemplate;

    @Test
    void testExecuteQuery_Success() {
        // Given
        String query = "SELECT * FROM users WHERE id = ?";
        Map<String, Object> params = Map.of("id", 1);

        List<Map<String, Object>> expectedResults = List.of(
            Map.of("id", 1, "name", "John")
        );

        when(jdbcTemplate.queryForList(anyString(), anyMap()))
            .thenReturn(expectedResults);

        // When
        List<Map<String, Object>> results = databaseTools.executeQuery(query, params);

        // Then
        assertThat(results).isEqualTo(expectedResults);
        verify(jdbcTemplate).queryForList(query, params);
    }

    @Test
    void testExecuteQuery_InvalidQuery_ThrowsException() {
        // Given
        String query = "DROP TABLE users";

        // When & Then
        assertThatThrownBy(() -> databaseTools.executeQuery(query, null))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Only SELECT queries are allowed");

        verifyNoInteractions(jdbcTemplate);
    }

    @Test
    void testGetTableSchema_Success() {
        // Given
        String tableName = "users";
        List<Map<String, Object>> columns = List.of(
            Map.of("column_name", "id", "data_type", "integer"),
            Map.of("column_name", "name", "data_type", "varchar")
        );

        when(jdbcTemplate.queryForList(anyString(), eq(tableName)))
            .thenReturn(columns);

        // When
        TableSchema schema = databaseTools.getTableSchema(tableName);

        // Then
        assertThat(schema.tableName()).isEqualTo(tableName);
        assertThat(schema.columns()).isEqualTo(columns);
    }
}
```

### Integration Testing

```java
@SpringBootTest
@AutoConfigureMockMvc
class McpServerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private McpServer mcpServer;

    @MockBean
    private DatabaseTools databaseTools;

    @Test
    void testExecuteTool_Success() throws Exception {
        // Given
        String toolName = "executeQuery";
        Map<String, Object> args = Map.of(
            "query", "SELECT * FROM users",
            "params", Map.of()
        );

        List<Map<String, Object>> expectedResult = List.of(
            Map.of("id", 1, "name", "Test User")
        );

        when(databaseTools.executeQuery(anyString(), anyMap()))
            .thenReturn(expectedResult);

        // When & Then
        mockMvc.perform(post("/mcp/tools/executeQuery")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(args)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray())
                .andExpect(jsonPath("$.result[0].id").value(1));
    }

    @Test
    void testListTools_Success() throws Exception {
        // When & Then
        mockMvc.perform(get("/mcp/tools"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tools").isArray());
    }

    @Test
    void testHealthEndpoint() throws Exception {
        // When & Then
        mockMvc.perform(get("/actuator/health/mcp"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }
}
```

### Integration Testing with Testcontainers

```java
@SpringBootTest
@Testcontainers
@AutoConfigureMockMvc
class McpServerIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void properties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testDatabaseToolWithRealDatabase() throws Exception {
        // Given
        String query = "SELECT current_database(), current_user";
        Map<String, Object> request = Map.of(
                "tool", "executeQuery",
                "arguments", Map.of("query", query)
        );

        // When & Then
        mockMvc.perform(post("/mcp/tools/executeQuery")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data[0].current_database").value("testdb"))
                .andExpect(jsonPath("$.data[0].current_user").value("test"));
    }
}
```

### Testing with @WebMvcTest (Slice Test)

```java
@WebMvcTest(controllers = McpController.class)
class McpControllerSliceTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private McpServer mcpServer;

    @MockBean
    private ToolRegistry toolRegistry;

    @Test
    void testListToolsEndpoint() throws Exception {
        // Given
        Tool tool1 = Tool.builder().name("tool1").description("Tool 1").build();
        Tool tool2 = Tool.builder().name("tool2").description("Tool 2").build();

        when(toolRegistry.listTools()).thenReturn(List.of(tool1, tool2));

        // When & Then
        mockMvc.perform(get("/mcp/tools"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tools").isArray())
                .andExpect(jsonPath("$.tools.length()").value(2))
                .andExpect(jsonPath("$.tools[0].name").value("tool1"));
    }
}
```

### Testing Tool Validation

```java
@ExtendWith(MockitoExtension.class)
class ToolValidationTest {

    private ToolValidator validator;

    @BeforeEach
    void setUp() {
        McpServerProperties properties = new McpServerProperties();
        properties.getTools().getValidation().setMaxArgumentsSize(1000);
        validator = new DefaultToolValidator(properties);
    }

    @Test
    void testValidArguments() {
        // Given
        Tool tool = Tool.builder()
                .name("testTool")
                .method(getTestMethod())
                .build();
        Map<String, Object> args = Map.of("param1", "value1", "param2", 123);

        // When & Then
        assertDoesNotThrow(() -> validator.validateArguments(tool, args));
    }

    @Test
    void testArgumentsTooLarge() {
        // Given
        Tool tool = Tool.builder().name("testTool").build();
        Map<String, Object> args = Map.of("largeParam", "x".repeat(2000));

        // When & Then
        ValidationException exception = assertThrows(
                ValidationException.class,
                () -> validator.validateArguments(tool, args)
        );
        assertThat(exception.getMessage()).contains("Arguments too large");
    }
}
```

### Testing Security Integration

```java
@SpringBootTest
@AutoConfigureMockMvc
@WithMockUser(roles = {"USER"})
class McpSecurityTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testUserCanAccessRegularTools() throws Exception {
        mockMvc.perform(get("/mcp/tools/getWeather"))
                .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(roles = {"USER"})
    void testUserCannotAccessAdminTools() throws Exception {
        mockMvc.perform(get("/mcp/tools/admin/deleteData"))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = {"ADMIN"})
    void testAdminCanAccessAllTools() throws Exception {
        mockMvc.perform(get("/mcp/tools/admin/deleteData"))
                .andExpect(status().isOk());
    }
}
```

### Configuration Testing

```java
@SpringBootTest
@EnableConfigurationProperties(McpServerProperties.class)
class McpPropertiesTest {

    @Autowired
    private McpServerProperties properties;

    @Test
    void testDefaultValues() {
        assertThat(properties.getServer().getName()).isEqualTo("spring-ai-mcp-server");
        assertThat(properties.getTransport().getType()).isEqualTo(TransportType.STDIO);
        assertThat(properties.getSecurity().isEnabled()).isFalse();
    }
}
```

### application.properties

```properties
# Spring AI Configuration
spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.openai.chat.options.model=gpt-4o-mini
spring.ai.openai.chat.options.temperature=0.7

# MCP Server Configuration
spring.ai.mcp.enabled=true
spring.ai.mcp.server.name=spring-ai-mcp-server
spring.ai.mcp.server.version=1.0.0
spring.ai.mcp.transport.type=stdio

# HTTP Transport (if enabled)
spring.ai.mcp.transport.http.port=8080
spring.ai.mcp.transport.http.path=/mcp
spring.ai.mcp.transport.http.cors.enabled=true
spring.ai.mcp.transport.http.cors.allowed-origins=*

# Security Configuration
spring.ai.mcp.security.enabled=true
spring.ai.mcp.security.authorization.mode=role-based
spring.ai.mcp.security.authorization.default-deny=true
spring.ai.mcp.security.audit.enabled=true

# Tool Configuration
spring.ai.mcp.tools.package-scan=com.example.mcp.tools
spring.ai.mcp.tools.validation.enabled=true
spring.ai.mcp.tools.validation.max-execution-time=30s
spring.ai.mcp.tools.caching.enabled=true
spring.ai.mcp.tools.caching.ttl=5m

# Prompt Configuration
spring.ai.mcp.prompts.package-scan=com.example.mcp.prompts
spring.ai.mcp.prompts.caching.enabled=true
spring.ai.mcp.prompts.caching.ttl=1h

# Actuator and Monitoring
spring.ai.mcp.actuator.enabled=true
spring.ai.mcp.metrics.enabled=true
spring.ai.mcp.metrics.export.prometheus.enabled=true
spring.ai.mcp.logging.enabled=true
spring.ai.mcp.logging.level=DEBUG

# Performance Tuning
spring.ai.mcp.thread-pool.core-size=10
spring.ai.mcp.thread-pool.max-size=50
spring.ai.mcp.thread-pool.queue-capacity=100
spring.ai.mcp.rate-limiter.enabled=true
spring.ai.mcp.rate-limiter.requests-per-minute=100
```

## Best Practices

1. **Use Declarative Annotations**: Prefer `@Tool` and `@PromptTemplate` over manual registration
2. **Implement Security**: Always validate user permissions and sanitize inputs
3. **Add Documentation**: Document all tools, parameters, and return values clearly
4. **Handle Errors Gracefully**: Implement proper error handling and user-friendly messages
5. **Use Caching**: Cache expensive operations and frequently used prompts
6. **Monitor Performance**: Track tool execution times and success rates
7. **Test Thoroughly**: Write unit and integration tests for all tools
8. **Version Your API**: Maintain backward compatibility when updating tools
9. **Use Type Safety**: Leverage Java's type system with records and sealed interfaces
10. **Implement Rate Limiting**: Protect against abuse and ensure fair usage

## Migration from LangChain4j

If migrating from LangChain4j MCP to Spring AI MCP:

### Key Differences
- **Annotations**: Spring AI uses `@Tool` instead of LangChain4j's `@ToolMethod`
- **Configuration**: Spring AI emphasizes auto-configuration and properties
- **Integration**: Deeper integration with Spring ecosystem (Security, Data, WebFlux)
- **Function Calling**: Spring AI uses `FunctionCallback` for low-level control

### Migration Steps

1. Replace LangChain4j `@ToolMethod` with Spring AI `@Tool`
2. Update configuration from `application.properties` to Spring AI properties
3. Migrate tool providers to Spring components with `@Component`
4. Update prompt templates to use Spring AI's prompt abstractions
5. Replace LangChain4j-specific types with Spring AI equivalents

### Example Migration

```java
// Before: LangChain4j
@ToolMethod("Get weather information")
public String getWeather(@P("city name") String city) {
    return weatherService.getWeather(city);
}

// After: Spring AI
@Component
public class WeatherTools {
    @Tool(description = "Get weather information")
    public String getWeather(@ToolParam("City name") String city) {
        return weatherService.getWeather(city);
    }
}
```

## Examples

For comprehensive examples, see [examples.md](./references/examples.md) including:
- Basic MCP server setup
- Multi-tool enterprise servers
- Secure tool implementations
- Integration with Spring Data
- Real-time data streaming
- Multi-modal applications

## API Reference

Complete API documentation is available in [api-reference.md](./references/api-reference.md) covering:
- Core annotations and interfaces
- Configuration properties
- Transport implementations
- Security integrations
- Testing utilities

## References

- [Spring AI Documentation](https://docs.spring.io/spring-ai/reference/)
- [Model Context Protocol Specification](https://modelcontextprotocol.org/)
- [LangChain4j MCP Patterns](../langchain4j/langchain4j-mcp-server-patterns/SKILL.md)
- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
