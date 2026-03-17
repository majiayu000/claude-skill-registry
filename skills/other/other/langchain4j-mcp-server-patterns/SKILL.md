---
name: langchain4j-mcp-server-patterns
description: Provides Model Context Protocol (MCP) server implementation patterns with LangChain4j. Use when building MCP servers to extend AI capabilities with custom tools, resources, and prompt templates.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# LangChain4j MCP Server Implementation Patterns

Implement Model Context Protocol (MCP) servers with LangChain4j to extend AI capabilities with standardized tools, resources, and prompt templates.

## Overview

The Model Context Protocol (MCP) is a standardized protocol for connecting AI applications to external data sources and tools. LangChain4j provides MCP server implementation patterns that enable AI systems to dynamically discover and execute tools, access resources, and use prompt templates through a standardized interface.

## When to Use

Use this skill when building:
- AI applications requiring external tool integration
- Enterprise MCP servers with multi-domain support (GitHub, databases, APIs)
- Dynamic tool providers with context-aware filtering
- Resource-based data access systems for AI models
- Prompt template servers for standardized AI interactions
- Scalable AI agents with resilient tool execution
- Multi-modal AI applications with diverse data sources
- Spring Boot applications with MCP integration
- Production-ready MCP servers with security and monitoring

## Instructions

Follow these steps to implement an MCP server with LangChain4j:

### 1. Create Tool Provider

Implement `ToolProvider` to define executable tools:

```java
class WeatherToolProvider implements ToolProvider {

    @Override
    public List<ToolSpecification> listTools() {
        return List.of(ToolSpecification.builder()
            .name("get_weather")
            .description("Get weather for a city")
            .inputSchema(Map.of(
                "type", "object",
                "properties", Map.of(
                    "city", Map.of("type", "string", "description", "City name")
                ),
                "required", List.of("city")
            ))
            .build());
    }

    @Override
    public String executeTool(String name, String arguments) {
        // Parse arguments and execute tool logic
        return "Weather data result";
    }
}
```

### 2. Configure MCP Server

Create and start the MCP server:

```java
MCPServer server = MCPServer.builder()
    .server(new StdioServer.Builder())
    .addToolProvider(new WeatherToolProvider())
    .build();

server.start();
```

### 3. Add Resource Provider

Implement resource providers for data access:

```java
class CompanyResourceProvider
    implements ResourceListProvider, ResourceReadHandler {

    @Override
    public List<McpResource> listResources() {
        return List.of(
            McpResource.builder()
                .uri("policies")
                .name("Company Policies")
                .mimeType("text/plain")
                .build()
        );
    }

    @Override
    public String readResource(String uri) {
        return loadResourceContent(uri);
    }
}
```

### 4. Integrate with Spring Boot

Configure MCP server in Spring Boot application:

```java
@Bean
public MCPSpringConfig mcpServer(List<ToolProvider> tools) {
    return MCPSpringConfig.builder()
        .tools(tools)
        .server(new StdioServer.Builder())
        .build();
}
```

### 5. Implement Security

Add tool filtering for access control:

```java
McpToolProvider secureProvider = McpToolProvider.builder()
    .mcpClients(mcpClient)
    .filter((client, tool) -> {
        if (tool.name().startsWith("admin_") && !isAdmin()) {
            return false;
        }
        return true;
    })
    .build();
```

## Quick Start

### Basic MCP Server

Create a simple MCP server with one tool:

```java
MCPServer server = MCPServer.builder()
    .server(new StdioServer.Builder())
    .addToolProvider(new SimpleWeatherToolProvider())
    .build();

server.start();
```

### Spring Boot Integration

Configure MCP server in Spring Boot:

```java
@Bean
public MCPSpringConfig mcpServer(List<ToolProvider> tools) {
    return MCPSpringConfig.builder()
        .tools(tools)
        .server(new StdioServer.Builder())
        .build();
}
```

## Core Concepts

### MCP Architecture

MCP standardizes AI application connections:
- **Tools**: Executable functions (database queries, API calls)
- **Resources**: Data sources (files, schemas, documentation)
- **Prompts**: Pre-configured templates for tasks
- **Transport**: Communication layer (stdio, HTTP, WebSocket)

```
AI Application ←→ MCP Client ←→ Transport ←→ MCP Server ←→ External Service
```

### Key Components

- **MCPServer**: Main server instance with configuration
- **ToolProvider**: Tool specification and execution interface
- **ResourceListProvider/ResourceReadHandler**: Resource access
- **PromptListProvider/PromptGetHandler**: Template management
- **Transport**: Communication mechanisms (stdio, HTTP)

## Implementation Patterns

### Tool Provider Pattern

Create tools with proper schema validation:

```java
class WeatherToolProvider implements ToolProvider {

    @Override
    public List<ToolSpecification> listTools() {
        return List.of(ToolSpecification.builder()
            .name("get_weather")
            .description("Get weather for a city")
            .inputSchema(Map.of(
                "type", "object",
                "properties", Map.of(
                    "city", Map.of("type", "string", "description", "City name")
                ),
                "required", List.of("city")
            ))
            .build());
    }

    @Override
    public String executeTool(String name, String arguments) {
        // Parse arguments and execute tool logic
        return "Weather data result";
    }
}
```

### Resource Provider Pattern

Provide static and dynamic resources:

```java
class CompanyResourceProvider
    implements ResourceListProvider, ResourceReadHandler {

    @Override
    public List<McpResource> listResources() {
        return List.of(
            McpResource.builder()
                .uri("policies")
                .name("Company Policies")
                .mimeType("text/plain")
                .build()
        );
    }

    @Override
    public String readResource(String uri) {
        return loadResourceContent(uri);
    }
}
```

### Prompt Template Pattern

Create reusable prompt templates:

```java
class PromptTemplateProvider
    implements PromptListProvider, PromptGetHandler {

    @Override
    public List<Prompt> listPrompts() {
        return List.of(
            Prompt.builder()
                .name("code-review")
                .description("Review code for quality")
                .build()
        );
    }

    @Override
    public String getPrompt(String name, Map<String, String> args) {
        return applyTemplate(name, args);
    }
}
```

## Transport Configuration

### Stdio Transport

Local process communication:

```java
McpTransport transport = new StdioMcpTransport.Builder()
    .command(List.of("npm", "exec", "@modelcontextprotocol/server-everything@0.6.2"))
    .logEvents(true)
    .build();
```

### HTTP Transport

Remote server communication:

```java
McpTransport transport = new HttpMcpTransport.Builder()
    .sseUrl("http://localhost:3001/sse")
    .logRequests(true)
    .logResponses(true)
    .build();
```

## Client Integration

### MCP Client Setup

Connect to MCP servers:

```java
McpClient client = new DefaultMcpClient.Builder()
    .key("my-client")
    .transport(transport)
    .cacheToolList(true)
    .build();

// List available tools
List<ToolSpecification> tools = client.listTools();
```

### Tool Provider Integration

Bridge MCP servers to LangChain4j AI services:

```java
McpToolProvider provider = McpToolProvider.builder()
    .mcpClients(mcpClient)
    .failIfOneServerFails(false)
    .filter((client, tool) -> filterByPermissions(tool))
    .build();

// Integrate with AI service
AIAssistant assistant = AiServices.builder(AIAssistant.class)
    .chatModel(chatModel)
    .toolProvider(provider)
    .build();
```

## Security & Best Practices

### Tool Security

Implement secure tool filtering:

```java
McpToolProvider secureProvider = McpToolProvider.builder()
    .mcpClients(mcpClient)
    .filter((client, tool) -> {
        if (tool.name().startsWith("admin_") && !isAdmin()) {
            return false;
        }
        return true;
    })
    .build();
```

### Resource Security

Apply access controls to resources:

```java
public boolean canAccessResource(String uri, User user) {
    return resourceService.hasAccess(uri, user);
}
```

### Error Handling

Implement robust error handling:

```java
try {
    String result = mcpClient.executeTool(request);
} catch (McpException e) {
    log.error("MCP execution failed: {}", e.getMessage());
    return fallbackResult();
}
```

## Advanced Patterns

### Multi-Server Configuration

Configure multiple MCP servers:

```java
@Bean
public List<McpClient> mcpClients(List<ServerConfig> configs) {
    return configs.stream()
        .map(this::createMcpClient)
        .collect(Collectors.toList());
}

@Bean
public McpToolProvider multiServerProvider(List<McpClient> clients) {
    return McpToolProvider.builder()
        .mcpClients(clients)
        .failIfOneServerFails(false)
        .build();
}
```

### Dynamic Tool Discovery

Runtime tool filtering based on context:

```java
McpToolProvider contextualProvider = McpToolProvider.builder()
    .mcpClients(clients)
    .filter((client, tool) -> isToolAllowed(user, tool, context))
    .build();
```

### Health Monitoring

Monitor MCP server health:

```java
@Component
public class McpHealthChecker {

    @Scheduled(fixedRate = 30000) // 30 seconds
    public void checkServers() {
        mcpClients.forEach(client -> {
            try {
                client.listTools();
                markHealthy(client.key());
            } catch (Exception e) {
                markUnhealthy(client.key(), e.getMessage());
            }
        });
    }
}
```

## Configuration

### Application Properties

Configure MCP servers in application.yml:

```yaml
mcp:
  servers:
    github:
      type: docker
      command: ["/usr/local/bin/docker", "run", "-e", "GITHUB_TOKEN", "-i", "mcp/github"]
      log-events: true
    database:
      type: stdio
      command: ["/usr/bin/npm", "exec", "@modelcontextprotocol/server-sqlite@0.6.2"]
      log-events: false
```

### Spring Boot Configuration

Configure MCP with Spring Boot:

```java
@Configuration
@EnableConfigurationProperties(McpProperties.class)
public class McpConfiguration {

    @Bean
    public MCPServer mcpServer(List<ToolProvider> providers) {
        return MCPServer.builder()
            .server(new StdioServer.Builder())
            .addToolProvider(providers)
            .enableLogging(true)
            .build();
    }
}
```

## Examples

### Example 1: Weather Tool Execution

**Input:**
```java
// Client invokes the weather tool
Map<String, Object> args = Map.of("city", "Milan");
String result = mcpClient.executeTool("get_weather", mapper.writeValueAsString(args));
```

**Output:**
```json
{
  "city": "Milan",
  "temperature": 22,
  "condition": "Partly Cloudy",
  "humidity": 65,
  "unit": "celsius"
}
```

### Example 2: Resource Retrieval

**Input:**
```java
// Client requests a resource by URI
String content = mcpClient.readResource("policies");
```

**Output:**
```
Company Remote Work Policy v2.0
Effective Date: January 1, 2025

1. Employees may work remotely up to 3 days per week...
```

### Example 3: Multi-Server Tool Discovery

**Input:**
```java
// List all tools from connected MCP servers
List<ToolSpecification> tools = mcpToolProvider.tools();
tools.forEach(t -> System.out.println(t.name() + ": " + t.description()));
```

**Output:**
```
get_weather: Get current weather for a city
search_documents: Search company knowledge base
send_notification: Send notification to user
admin_backup: Create system backup (admin only)
```

---

Refer to [examples.md](./references/examples.md) for comprehensive implementation examples including:
- Basic MCP server setup
- Multi-tool enterprise servers
- Resource and prompt providers
- Spring Boot integration
- Error handling patterns
- Security implementations

## API Reference

Complete API documentation is available in [api-reference.md](./references/api-reference.md) covering:
- Core MCP classes and interfaces
- Transport configuration
- Client and server patterns
- Error handling strategies
- Configuration management
- Testing and validation

## Best Practices

1. **Resource Management**: Always close MCP clients properly using try-with-resources
2. **Error Handling**: Implement graceful degradation when servers fail
3. **Security**: Use tool filtering and resource access controls
4. **Performance**: Enable caching and optimize tool execution
5. **Monitoring**: Implement health checks and observability
6. **Testing**: Create comprehensive test suites with mocks
7. **Documentation**: Document tools, resources, and prompts clearly
8. **Configuration**: Use structured configuration for maintainability

## References

- [LangChain4j Documentation](https://langchain4j.com/docs/)
- [Model Context Protocol Specification](https://modelcontextprotocol.org/)
- [API Reference](./references/api-reference.md)
- [Examples](./references/examples.md)

## Constraints and Warnings

- MCP servers should implement proper resource cleanup when stopped.
- **External MCP Server Security**: Only connect to trusted, verified MCP servers; external servers (including those launched via `npm exec` or HTTP/SSE endpoints) can expose untrusted tools, resources, and prompts that may influence agent behavior through indirect prompt injection.
- **Pin MCP Server Versions**: Always pin npm packages to specific versions (e.g., `@modelcontextprotocol/server-everything@0.6.2`) to prevent supply-chain attacks from unpinned dependencies.
- **Validate External Content**: Content retrieved from MCP server resources (e.g., GitHub issues, database records) is untrusted user-generated data; validate and sanitize before acting on it.
- Tool execution errors should be handled gracefully; never expose stack traces to clients.
- Resource URIs should be validated to prevent directory traversal attacks.
- Prompt templates should sanitize user inputs to prevent injection attacks.
- Stdio transport requires proper process lifecycle management.
- HTTP transport should implement authentication and rate limiting.
- Multi-server configurations require careful handling of server failures.
- Tool caching should have appropriate TTLs to prevent stale data.
- Be cautious with tools that have external side effects; they may be called unexpectedly by AI models.
