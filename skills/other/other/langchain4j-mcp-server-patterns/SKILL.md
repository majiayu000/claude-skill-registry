---
name: langchain4j-mcp-server-patterns
description: Provides LangChain4j patterns for implementing MCP (Model Context Protocol) servers, creating Java AI tools, exposing tool calling capabilities, and integrating MCP clients with AI services. Use when building a Java MCP server, implementing tool calling in Java, connecting LangChain4j to external MCP servers, or securing tool exposure for agent workflows.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# LangChain4j MCP Server Implementation Patterns

## Overview

Use this skill to design and implement Model Context Protocol (MCP) integrations with LangChain4j.

The main concerns are:
- defining a clean tool, resource, and prompt surface
- choosing the right transport and bootstrap model
- filtering unsafe capabilities before exposing them to agents or applications

Keep `SKILL.md` focused on the implementation flow. Use the bundled references for expanded examples and API-level detail.

## When to Use

Use this skill when:
- building a Java MCP server that exposes tools, resources, or prompts
- integrating LangChain4j with one or more external MCP servers
- wiring MCP support into a Spring Boot application
- filtering available tools by tenant, user role, or runtime context
- adding observability, resilience, and safe failure handling around MCP interactions
- reviewing an MCP integration for prompt-injection and side-effect risks

Typical trigger phrases include `langchain4j mcp`, `java mcp server`, `mcp tool provider`, `spring boot mcp`, and `connect langchain4j to mcp`.

## Instructions

### 1. Design the MCP surface before writing code

Decide what the server should expose:
- tools for actions with clear inputs and side effects
- resources for read-only or structured data access
- prompts only when a reusable template adds real value

Keep names stable, descriptions concrete, and schemas small enough for a client or model to understand quickly.

### 2. Implement providers with narrow responsibilities

Use separate classes for each concern:
- tool provider for executable functions
- resource provider for discoverable and readable data
- prompt provider for reusable prompt templates

Validate arguments before execution and return clear error messages for invalid input or unavailable dependencies.

### 3. Choose the transport intentionally

Use:
- stdio for local integrations, CLI tools, and sidecar processes
- HTTP or SSE for remote or shared services

Pin external server versions and document how the process is started, authenticated, and monitored.

### 4. Bridge MCP into LangChain4j carefully

When consuming MCP servers from LangChain4j:
- initialize clients during application startup
- cache tool lists only when stale metadata is acceptable
- filter tools by trust level, environment, or user permissions
- fail closed for dangerous tools rather than exposing everything by default

### 5. Add resilience and security controls

At minimum:
- bound execution time for external calls
- log server and tool identity for each failure
- sanitize content returned by external resources before using it downstream
- isolate privileged tools behind allowlists, qualifiers, or role checks

### 6. Validate the full workflow

Before shipping:
- verify tool discovery and invocation with a real MCP client
- test disconnected or slow server behavior
- confirm that tool filtering matches the intended authorization model
- check that prompts and resources do not leak secrets or unsafe instructions

## Examples

### Example 1: Minimal tool provider and stdio server bootstrap

```java
class WeatherToolProvider implements ToolProvider {

    @Override
    public List<ToolSpecification> listTools() {
        return List.of(
            ToolSpecification.builder()
                .name("get_weather")
                .description("Return the current weather for a city")
                .inputSchema(Map.of(
                    "type", "object",
                    "properties", Map.of(
                        "city", Map.of("type", "string")
                    ),
                    "required", List.of("city")
                ))
                .build()
        );
    }

    @Override
    public String executeTool(String name, String arguments) {
        return weatherService.lookup(arguments);
    }
}

MCPServer server = MCPServer.builder()
    .server(new StdioServer.Builder())
    .addToolProvider(new WeatherToolProvider())
    .build();

server.start();
```

Use this pattern for local tool execution or a sidecar process started by another application.

### Example 2: Expose MCP tools to a LangChain4j AI service with filtering

```java
McpToolProvider toolProvider = McpToolProvider.builder()
    .mcpClients(mcpClients)
    .failIfOneServerFails(false)
    .filter((client, tool) -> !tool.name().startsWith("admin_"))
    .build();

Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .toolProvider(toolProvider)
    .build();
```

Use this pattern when you want LangChain4j to consume external MCP servers while still enforcing trust boundaries.

## Best Practices

- Keep each tool focused, deterministic, and well-described.
- Prefer explicit schemas over free-form string arguments.
- Separate read-only resources from tools with side effects.
- Filter or disable privileged tools by default.
- Pin external MCP server packages or container versions.
- Capture metrics for connection failures, invocation latency, and tool error rates.
- Store longer protocol details and framework-specific wiring in `references/` instead of expanding `SKILL.md` indefinitely.

## Constraints and Warnings

- External MCP servers are untrusted integration boundaries and may expose malicious or misleading content.
- Do not forward raw resource content directly into autonomous tool execution without validation.
- Some LangChain4j and MCP APIs evolve quickly; adapt class names and builders to the versions already used in the project.
- Long-running or stateful tools need explicit timeout, cancellation, and cleanup behavior.
- Stdio-based servers require process lifecycle management and robust logging.

## References

- `references/examples.md`
- `references/api-reference.md`

## Related Skills

- `prompt-engineering`
- `spring-ai` 
- `clean-architecture`
