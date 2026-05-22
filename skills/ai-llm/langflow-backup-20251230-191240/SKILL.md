---
name: langflow
description: A powerful Python-based visual framework for building and deploying AI-powered agents and workflows with Model Context Protocol (MCP) integration, drag-and-drop interface, and enterprise-grade deployment options
repository: https://github.com/langflow-ai/langflow
documentation: https://docs.langflow.org/
version: 1.7.1
license: MIT
stars: 142000
languages:
  - Python (53.9%)
  - TypeScript (24.4%)
  - JavaScript (20.7%)
category: AI Workflow Development
tags:
  - langflow
  - ai-agents
  - visual-workflow
  - model-context-protocol
  - mcp
  - low-code
  - llm-orchestration
  - python
  - typescript
  - deployment
---

# Langflow - Visual AI Workflow Platform

## Overview

**Langflow** is an open-source, Python-based platform for building and deploying AI-powered agents and workflows through a visual drag-and-drop interface. With 142,000+ GitHub stars and used by 1,500+ projects, Langflow enables rapid prototyping of AI applications without requiring extensive coding knowledge.

## Key Features

### 🎨 Visual Development Environment
- **Drag-and-Drop Canvas**: Build complex AI workflows visually by connecting component nodes
- **Interactive Playground**: Test and debug flows in real-time without full stack development
- **Component Library**: 200+ pre-built components for LLMs, data sources, agents, tools, and MCP servers
- **Custom Components**: Full Python customization for specialized use cases

### 🤖 Agent & MCP Integration
- **AI Agents**: LLM-powered agents with autonomous tool selection and execution
- **MCP Client & Server**: Built-in Model Context Protocol support for tool integration
- **Multi-Agent Coordination**: Orchestrate multiple agents working together
- **Tool Ecosystem**: Calculator, Web Search, URL fetcher, file operations, and custom tools

### 🚀 Deployment Options
- **Local Development**: Desktop app for macOS/Windows or Python package installation
- **Docker Containers**: Portable, reproducible deployments
- **Kubernetes**: Production-grade orchestration with high availability
- **Cloud Platforms**: Native support for Google Cloud, Hugging Face Spaces, and more
- **API Export**: RESTful API endpoints for external integrations

### 🔧 Production Features
- **Observability**: Integrated LangSmith and LangFuse monitoring
- **Authentication**: API key management with role-based access control
- **Security**: HTTPS support, CORS configuration, reverse proxy compatibility
- **Versioning**: Component version control and flow history
- **JSON Export**: Portable flow definitions for backup and sharing

## Architecture

### Component-Based Design
```
Flow (Workflow)
├── Components (Building Blocks)
│   ├── Inputs/Outputs (Ports)
│   ├── Parameters (Configuration)
│   └── Python Code (Logic)
├── Edges (Connections)
└── Canvas (Visual Editor)
```

### Component Categories
1. **Core Components**: Generic functionality (loops, parsing, multi-provider integrations)
2. **Bundles**: Service-specific components grouped by provider (OpenAI, Anthropic, etc.)
3. **Legacy**: Deprecated components (hidden by default)

### MCP Integration Architecture
- **MCP Client**: Connect to external MCP servers for tool access
- **MCP Server**: Expose Langflow flows as tools for other applications
- **Connection Modes**: JSON config, STDIO (local), HTTP/SSE (remote)

## Installation

### Prerequisites
- **Python**: 3.10-3.13 (macOS/Linux) or 3.10-3.12 (Windows)
- **Package Manager**: `uv` (recommended)
- **Hardware Minimum**: Dual-core CPU, 2GB RAM
- **Hardware Recommended**: Multi-core CPU, 4GB+ RAM

### Quick Start (Python Package)
```bash
# Create virtual environment
uv venv langflow-env

# Activate environment
# macOS/Linux:
source langflow-env/bin/activate
# Windows:
langflow-env\Scripts\activate

# Install Langflow
uv pip install langflow

# Launch
uv run langflow run

# Access at http://127.0.0.1:7860
```

### Docker Installation
```bash
docker run -p 7860:7860 langflowai/langflow:latest
```

### Desktop Application
Download from https://www.langflow.org/desktop

**Note**: Desktop version lacks Shareable Playground and Voice Mode features.

## Use Cases

### 1. Building an AI Agent Flow
```
Chat Input → Agent (with Tools) → Chat Output
             ↓
         [Calculator, Web Search, URL Fetcher]
```

**Steps**:
1. Add Agent component and configure LLM provider (OpenAI, Anthropic, etc.)
2. Connect Chat Input/Output components
3. Attach tools by enabling "Tool Mode" on components
4. Add system instructions for specialized behavior
5. Test in Playground with real queries

### 2. Model Context Protocol Integration
**Scenario**: Agent with external MCP server tools

1. Navigate to **Settings → MCP Servers**
2. Add MCP server connection:
   - **STDIO Mode**: Local server (command + args)
   - **HTTP/SSE Mode**: Remote server (URL)
   - **JSON Config**: Direct configuration object
3. Add **MCP Tools** component to flow
4. Connect to Agent component
5. Agent automatically discovers and uses available tools

**Example**: Using `mcp-server-fetch` to summarize tech news

### 3. Production Deployment (Kubernetes)
```yaml
# High availability deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langflow
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: langflow
        image: langflowai/langflow:latest
        env:
        - name: LANGFLOW_AUTO_LOGIN
          value: "false"
        - name: LANGFLOW_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: langflow-secrets
              key: secret-key
```

### 4. API Authentication Setup
```bash
# Generate API key via CLI
uv run langflow api-key

# Generate secure secret key
python3 -c "from secrets import token_urlsafe; print(f'LANGFLOW_SECRET_KEY={token_urlsafe(32)}')"

# Use in requests
curl -X POST "https://your-instance/api/v1/run" \
  -H "x-api-key: $LANGFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"flow_id": "abc123", "inputs": {...}}'
```

### 5. Custom Component Development
**Create Python component**:
```python
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message

class CustomGreetingComponent(Component):
    display_name = "Custom Greeting"
    description = "Greets users with custom message"

    inputs = [
        MessageTextInput(
            name="user_name",
            display_name="User Name",
            info="Name to greet"
        )
    ]

    outputs = [
        Output(display_name="Greeting", name="output", method="greet")
    ]

    def greet(self) -> Message:
        name = self.user_name
        return Message(text=f"Hello, {name}! Welcome to Langflow.")
```

### 6. Multi-Agent Workflow
**Scenario**: Research agent + summarization agent

1. **Agent 1 (Researcher)**: Web Search tool + URL fetcher
2. **Agent 2 (Summarizer)**: Receives research results, generates summary
3. **Flow Control**: Parse output from Agent 1 → Feed to Agent 2
4. **Chat Output**: Display final summarized research

## Security Best Practices

### Authentication Configuration
```bash
# Disable auto-login for multi-user environments
export LANGFLOW_AUTO_LOGIN=False

# Set custom secret key (required for production)
export LANGFLOW_SECRET_KEY=$(python3 -c "from secrets import token_urlsafe; print(token_urlsafe(32))")

# Configure CORS (specific origins only)
export LANGFLOW_CORS_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"
```

### Deployment Security
- **Never expose port 7860 directly** - use reverse proxy (Nginx, Caddy)
- **Enable HTTPS** with Let's Encrypt or custom certificates
- **Restrict CORS origins** - avoid wildcards in production
- **Secure API keys** - rotate regularly, use environment variables
- **Role-based access** - API keys inherit creator's privileges

## Advanced Features

### Flow Embedding
**HTML Embedding**:
```html
<iframe src="https://your-langflow-instance/embed/flow-id"
        width="100%" height="600px"></iframe>
```

**React/Angular**: Use API endpoints to integrate flows into applications

### Component Freezing
Lock component outputs during development:
1. Right-click component → **Freeze**
2. Component preserves last output without re-execution
3. Speeds up iterative testing of other components

### Flow Versioning
- **Component Versioning**: Copied components maintain original version
- **Flow Export**: JSON-based portability across Langflow instances
- **History Tracking**: Monitor changes and rollback if needed

### Observability Integration
**LangSmith**:
```python
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_api_key
```

**LangFuse**:
```python
export LANGFUSE_PUBLIC_KEY=your_public_key
export LANGFUSE_SECRET_KEY=your_secret_key
```

## Common Workflows

### 1. RAG (Retrieval-Augmented Generation)
```
Document Loader → Text Splitter → Embeddings → Vector Store
                                                      ↓
User Query → Retriever → Context + Query → LLM → Response
```

### 2. Agent with Memory
```
Chat Input → Agent (with Chat Memory) → Tools → LLM → Chat Output
             ↑                                         ↓
             └──────────── Session Storage ────────────┘
```

### 3. Sequential Processing
```
Input → Component A → Parse → Component B → Format → Output
```

## Troubleshooting

### Port Already in Use
```bash
# Change default port
uv run langflow run --port 8080
```

### Missing Dependencies
```bash
# Reinstall with all extras
uv pip install langflow[all]
```

### Docker Container Issues
```bash
# View logs
docker logs langflow-container

# Restart with fresh state
docker rm langflow-container
docker run -p 7860:7860 -v langflow-data:/app/data langflowai/langflow:latest
```

### MCP Server Connection Failures
- Verify server command and arguments in STDIO mode
- Check network connectivity for HTTP/SSE mode
- Review environment variables in `.env` file
- Enable debug logging for detailed error messages

## Community & Resources

### Official Links
- **Documentation**: https://docs.langflow.org/
- **GitHub**: https://github.com/langflow-ai/langflow (142k stars)
- **Discord**: https://discord.gg/EqksyE2EX9
- **Twitter**: https://twitter.com/langflow_ai

### Key Statistics
- **Contributors**: 331 developers
- **Used by**: 1,500+ projects
- **Latest Release**: v1.7.1 (December 2025)
- **License**: MIT

### Learning Resources
- Quickstart Tutorial: https://docs.langflow.org/get-started-quickstart
- Component Reference: https://docs.langflow.org/concepts-components
- Deployment Guides: https://docs.langflow.org/deployment-overview
- API Documentation: https://docs.langflow.org/api-reference-api-examples

## When to Use This Skill

Use the Langflow skill when:
- ✅ Building AI agent workflows with visual interface
- ✅ Prototyping LLM applications rapidly without extensive coding
- ✅ Integrating Model Context Protocol (MCP) servers and tools
- ✅ Deploying production AI agents with observability and security
- ✅ Creating multi-agent coordination systems
- ✅ Developing RAG (Retrieval-Augmented Generation) applications
- ✅ Exposing AI workflows as API endpoints
- ✅ Building custom components for specialized AI tasks
- ✅ Setting up local or cloud-based AI development environments
- ✅ Testing and debugging complex LLM workflows interactively

## Related Technologies

- **LangChain**: Python framework for LLM applications (Langflow is built on LangChain)
- **Model Context Protocol (MCP)**: Tool integration standard (native support)
- **OpenAI API**: LLM provider (integrated)
- **Anthropic Claude**: LLM provider (integrated)
- **LangSmith**: Observability platform (integrated)
- **LangFuse**: Open-source observability (integrated)
- **Docker**: Containerization (deployment option)
- **Kubernetes**: Orchestration (production deployment)

---

**Skill Type**: AI Workflow Development Platform
**Complexity Level**: Beginner to Advanced
**Maintenance Status**: ✅ Active (v1.7.1, December 2025)
**Community Health**: ✅ Excellent (142k stars, 331 contributors, 1500+ projects)
