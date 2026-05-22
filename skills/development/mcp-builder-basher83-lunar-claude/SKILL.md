---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs
  to interact with external services through well-designed tools. Use when building MCP servers to
  integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external
services through well-designed tools. The quality of an MCP server is measured by how
well it enables LLMs to accomplish real-world tasks.

---

## Process

## 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow
tools can be more convenient for specific tasks, while comprehensive coverage gives
agents flexibility to compose operations. Performance varies by client - some clients
benefit from code execution that combines basic tools, while others work better with
higher-level workflows. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent
prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate
results. Design tools that return focused, relevant data. Some clients support code
execution which can help agents filter and process data efficiently.

**Optimize for Limited Context:**
Agents have constrained context windows - make every token count. Return high-signal
information, not exhaustive data dumps. Provide "concise" vs "detailed" response format
options. Default to human-readable identifiers over technical codes (names over IDs).
Consider the agent's context budget as a scarce resource.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next
steps. Suggest specific next steps: "Try using filter='active_only' to reduce results".
Make errors educational, not just diagnostic. Help agents learn proper tool usage
through clear feedback.

**Use Evaluation-Driven Development:**
Create realistic evaluation scenarios early. Let agent feedback drive tool improvements.
Prototype quickly and iterate based on actual agent performance.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:

- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**

- **Language**: TypeScript (high-quality SDK support and good compatibility in many
  execution environments e.g. MCPB. Plus AI models are good at generating TypeScript
  code, benefiting from its broad usage, static typing and good linting tools)
- **Transport**: Streamable HTTP for remote servers, using stateless JSON (simpler to
  scale and maintain, as opposed to stateful sessions and streaming responses). stdio
  for local servers.

**Load framework documentation:**

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines

**For TypeScript (recommended):**

- **TypeScript SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**

- **Python SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python Guide](./reference/python_mcp_server.md) - Python patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication
requirements, and data models. Use web search and WebFetch as needed. Read through
**ALL** available API documentation:

- Official API reference documentation
- Authentication and authorization requirements
- Rate limiting and pagination patterns
- Error responses and status codes
- Available endpoints and their parameters
- Data models and schemas

**Tool Selection:**

Prioritize comprehensive API coverage. List endpoints to implement, starting with the
most common operations. List the most valuable endpoints/operations to implement.
Prioritize tools that enable the most common and important use cases. Consider which
tools work together to enable complex workflows.

**Shared Utilities and Helpers:**

Identify common API request patterns. Plan pagination helpers. Design filtering and
formatting utilities. Plan error handling strategies.

**Input/Output Design:**

Define input validation models (Pydantic for Python, Zod for TypeScript). Design
consistent response formats (e.g., JSON or Markdown), and configurable levels of detail
(e.g., Detailed or Concise). Plan for large-scale usage (thousands of users/resources).
Implement character limits and truncation strategies (e.g., 25,000 tokens).

**Error Handling Strategy:**

Plan graceful failure modes. Design clear, actionable, LLM-friendly, natural language
error messages which prompt further action. Consider rate limiting and timeout
scenarios. Handle authentication and authorization errors.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

See language-specific guides for project setup:

- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [🐍 Python Guide](./reference/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement Core Infrastructure

Create shared utilities:

- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**

- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions
- Include proper constraints (min/max length, regex patterns, min/max values, ranges)
- Provide clear, descriptive field descriptions
- Include diverse examples in field descriptions

**Output Schema:**

- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses (TypeScript SDK feature)
- Helps clients understand and process tool outputs

**Tool Description:**

- Concise summary of functionality
- Parameter descriptions
- Return type schema
- One-line summary of what the tool does
- Detailed explanation of purpose and functionality
- Explicit parameter types with examples
- Complete return type schema
- Usage examples (when to use, when not to use)
- Error handling documentation, which outlines how to proceed given specific errors

**Implementation:**

- Async/await for I/O operations
- Proper error handling with actionable messages
- Support pagination where applicable
- Return both text content and structured data when using modern SDKs
- Use shared utilities to avoid code duplication
- Follow async/await patterns for all I/O
- Implement proper error handling
- Support multiple response formats (JSON and Markdown)
- Respect pagination parameters
- Check character limits and truncate appropriately

**Annotations:**

- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: Review and Test

#### 3.1 Code Quality Review

Review for:

- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

**To ensure quality, review the code for:**

- **DRY Principle**: No duplicated code between tools
- **Composability**: Shared logic extracted into functions
- **Consistency**: Similar operations return similar formats
- **Error Handling**: All external calls have error handling
- **Type Safety**: Full type coverage (Python type hints, TypeScript types)
- **Documentation**: Every tool has comprehensive docstrings/descriptions

#### 3.2 Build and Test

**TypeScript:**

- Run `npm run build` to verify compilation
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**

- Verify syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector

**Important:** MCP servers are long-running processes that wait for requests over
stdio/stdin or sse/http. Running them directly in your main process (e.g.,
`python server.py` or `node dist/index.js`) will cause your process to hang
indefinitely.

**Safe ways to test the server:**

- Use the evaluation harness (see Phase 4) - recommended approach
- Run the server in tmux to keep it outside your main process
- Use a timeout when testing: `timeout 5s python server.py`
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**For Python:**

- Verify Python syntax: `python -m py_compile your_server.py`
- Check imports work correctly by reviewing the file
- To manually test: Run server in tmux, then test with evaluation harness in main process
- Or use the evaluation harness directly (it manages the server for stdio transport)

**For Node/TypeScript:**

- Run `npm run build` and ensure it completes without errors
- Verify dist/index.js is created
- To manually test: Run server in tmux, then test with evaluation harness in main process
- Or use the evaluation harness directly (it manages the server for stdio transport)

See language-specific guides for detailed testing approaches and quality checklists.

#### 3.3 Use Quality Checklist

To verify implementation quality, load the appropriate checklist from the language-specific guide:

- Python: see "Quality Checklist" in [🐍 Python Guide](./reference/python_mcp_server.md)
- Node/TypeScript: see "Quality Checklist" in [⚡ TypeScript Guide](./reference/node_mcp_server.md)

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Load [✅ Evaluation Guide](./reference/evaluation.md) for complete evaluation guidelines.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

To create effective evaluations, follow the process outlined in the evaluation guide:

1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:

- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

## Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core MCP Documentation (Load First)

- **MCP Protocol**: Start with sitemap at `https://modelcontextprotocol.io/sitemap.xml`, then fetch specific pages with `.md` suffix
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Universal MCP guidelines including:
  - Server and tool naming conventions
  - Response format guidelines (JSON vs Markdown)
  - Pagination best practices
  - Transport selection (streamable HTTP vs stdio)
  - Security and error handling standards
  - Character limits and truncation strategies
  - Tool development guidelines

### SDK Documentation (Load During Phase 1/2)

- **Python SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### Language-Specific Implementation Guides (Load During Phase 2)

- [🐍 Python Implementation Guide](./reference/python_mcp_server.md) - Complete Python/FastMCP guide with:
  - Server initialization patterns
  - Pydantic model examples
  - Tool registration with `@mcp.tool`
  - Complete working examples
  - Quality checklist

- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md) - Complete TypeScript guide with:
  - Project structure
  - Zod schema patterns
  - Tool registration with `server.registerTool`
  - Complete working examples
  - Quality checklist

### Evaluation Guide (Load During Phase 4)

- [✅ Evaluation Guide](./reference/evaluation.md) - Complete evaluation creation guide with:
  - Question creation guidelines
  - Answer verification strategies
  - XML format specifications
  - Example questions and answers
  - Running an evaluation with the provided scripts
