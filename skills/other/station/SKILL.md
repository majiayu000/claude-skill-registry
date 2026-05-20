---
name: station
description: Use Station CLI (`stn`) for AI agent orchestration - creating agents, running tasks, managing environments, and deploying agent teams. Prefer CLI for file operations and exploration; use MCP tools for programmatic agent execution and detailed queries.
---

# Station CLI

Station is a self-hosted AI agent orchestration platform. You interact with it via the `stn` CLI or MCP tools (41+ available via `stn stdio`).

## When to Use CLI vs MCP Tools

| Task | Use CLI | Use MCP Tool |
|------|---------|--------------|
| Create/edit agent files | `stn agent create`, edit `.prompt` files | - |
| Run an agent | `stn agent run <name> "<task>"` | `call_agent` |
| List agents/environments | `stn agent list`, `stn env list` | `list_agents`, `list_environments` |
| Add MCP servers | `stn mcp add <name>` | `add_mcp_server_to_environment` |
| Sync configurations | `stn sync <env>` | - |
| Install bundles | `stn bundle install <url>` | - |
| Inspect runs | `stn runs list` | `inspect_run`, `list_runs` |
| Deploy | `stn deploy <env>` | - |
| Start services | `stn serve`, `stn jaeger up` | - |

**Rule of thumb**: CLI for setup, file operations, deployment. MCP tools for programmatic execution and queries within conversations.

## Quick Reference

### Initialization

```bash
# Initialize Station with AI provider
stn init --provider openai --ship       # OpenAI with Ship filesystem tools
stn init --provider anthropic --ship    # Anthropic (requires OAuth: stn auth anthropic login)
stn init --provider gemini --ship       # Google Gemini

# Initialize in specific directory (git-backed workspace)
stn init --provider openai --config ./my-workspace

# Start Jaeger for observability
stn jaeger up                           # View traces at http://localhost:16686
```

### Agent Management

```bash
# List agents
stn agent list                          # All agents in default environment
stn agent list --env production         # Agents in specific environment

# Show agent details
stn agent show <agent-name>             # Full configuration

# Run an agent
stn agent run <name> "<task>"           # Execute with task
stn agent run incident-coordinator "High latency on API"
stn agent run cost-analyzer "Analyze this week's AWS spend" --env production
stn agent run my-agent "task" --tail    # Follow output in real-time

# Delete agent
stn agent delete <name>
```

### Environment Management

```bash
# List environments
stn env list

# Sync file configurations to database
stn sync default                        # Sync default environment
stn sync default --browser              # Secure input for secrets (recommended for AI)
stn sync default --dry-run              # Preview changes
stn sync default --validate             # Validate only
```

### MCP Server Configuration

```bash
# Add MCP server
stn mcp add <name> --command <cmd> --args "<args>"

# Examples
stn mcp add filesystem --command npx --args "-y,@modelcontextprotocol/server-filesystem,/path"
stn mcp add github --command npx --args "-y,@modelcontextprotocol/server-github" --env "GITHUB_TOKEN={{.TOKEN}}"
stn mcp add playwright --command npx --args "-y,@playwright/mcp@latest"

# Add OpenAPI spec as MCP server
stn mcp add-openapi petstore --url https://petstore3.swagger.io/api/v3/openapi.json

# List and manage
stn mcp list                            # List configurations
stn mcp tools                           # List available tools
stn mcp status                          # Show sync status
stn mcp delete <config-id>              # Remove configuration
```

### Bundle Management

```bash
# Install bundle from URL or CloudShip
stn bundle install <url-or-id> <environment>
stn bundle install https://example.com/bundle.tar.gz my-env
stn bundle install devops-security-bundle security

# Create bundle from environment
stn bundle create <environment>
stn bundle create default --output ./my-bundle.tar.gz

# Share bundle to CloudShip
stn bundle share <environment>

# Export required variables from bundle (for CI/CD)
stn bundle export-vars ./my-bundle.tar.gz --format yaml
stn bundle export-vars ./my-bundle.tar.gz --format env
stn bundle export-vars <cloudship-bundle-id> --format yaml
```

### Workflow Management

```bash
# List workflows
stn workflow list
stn workflow list --env production

# Run workflow
stn workflow run <name>
stn workflow run incident-response --input '{"severity": "high"}'

# Manage approvals (for human-in-the-loop)
stn workflow approvals list
stn workflow approvals approve <approval-id>
stn workflow approvals reject <approval-id> --reason "Not authorized"

# Inspect and validate
stn workflow inspect <run-id>
stn workflow validate <name>
stn workflow export <name> --output workflow.yaml
```

### Server & Deployment

```bash
# Start Station server (web UI at :8585)
stn serve
stn serve --dev                         # Development mode

# Docker container mode
stn up                                  # Interactive setup
stn up --bundle <bundle-id>             # Run specific bundle
stn status                              # Check container status
stn logs -f                             # Follow logs
stn down                                # Stop container

# DEPLOY TO CLOUD (3 methods)
# Method 1: Local environment
stn deploy <environment> --target fly   # Deploy to Fly.io
stn deploy production --target k8s      # Deploy to Kubernetes
stn deploy production --target ansible  # Deploy via Ansible (SSH + Docker)

# Method 2: CloudShip bundle ID (no local environment needed)
stn deploy --bundle-id <uuid> --target fly
stn deploy --bundle-id <uuid> --target k8s --name my-station

# Method 3: Local bundle file
stn deploy --bundle ./my-bundle.tar.gz --target fly
stn deploy --bundle ./my-bundle.tar.gz --target k8s

# Deploy flags
--target        fly, kubernetes/k8s, ansible (default: fly)
--bundle-id     CloudShip bundle UUID (uses base image)
--bundle        Local .tar.gz bundle file
--name          Custom app name
--region        Deployment region (default: ord)
--namespace     Kubernetes namespace
--dry-run       Generate configs only, don't deploy
--auto-stop     Enable idle auto-stop (Fly.io)
--destroy       Tear down deployment

# IMPORTANT: K8s and Ansible require a container registry
# Fly.io has built-in registry, no extra setup needed

# Export variables for CI/CD
stn deploy export-vars default --format yaml > deploy-vars.yml
```

### Benchmarking & Reports

```bash
# Run benchmarks
stn benchmark run <agent-name>
stn benchmark list

# Generate reports
stn report create <name>
stn report list
```

### Runs History

```bash
# List runs
stn runs list
stn runs list --agent <name>
stn runs list --limit 20

# Inspect run details (via MCP tools is more detailed)
```

## File Structure

Station stores configurations at `~/.config/station/`:

```
~/.config/station/
├── config.yaml                 # Main configuration
├── station.db                  # SQLite database
└── environments/
    └── default/
        ├── *.prompt            # Agent definitions
        ├── *.json              # MCP server configurations
        └── variables.yml       # Template variable values
```

## Agent File Format (dotprompt)

Agents are `.prompt` files with YAML frontmatter:

```yaml
---
metadata:
  name: "my-agent"
  description: "What this agent does"
model: gpt-4o-mini
max_steps: 8
tools:
  - "__tool_name"              # MCP tools prefixed with __
---
{{role "system"}}
You are a helpful agent that [purpose].

{{role "user"}}
{{userInput}}
```

### Multi-Agent Hierarchy (Coordinator Pattern)

```yaml
---
metadata:
  name: "coordinator"
  description: "Orchestrates specialist agents"
model: gpt-4o-mini
max_steps: 20
agents:
  - "specialist-a"             # Becomes __agent_specialist_a tool
  - "specialist-b"
---
{{role "system"}}
You coordinate specialists:
- @specialist-a: handles X
- @specialist-b: handles Y

Delegate using __agent_<name> tools, then synthesize results.

{{role "user"}}
{{userInput}}
```

## MCP Server Configuration Format

JSON files in environment directories:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/mcp-server"],
      "env": {
        "API_KEY": "{{.API_KEY}}"
      }
    }
  }
}
```

Template variables (`{{.VAR}}`) are resolved during `stn sync`.

## Common Workflows

### 1. Create New Agent

```bash
# Create agent file
cat > ~/.config/station/environments/default/my-agent.prompt << 'EOF'
---
metadata:
  name: "my-agent"
  description: "Description here"
model: gpt-4o-mini
max_steps: 5
tools: []
---
{{role "system"}}
You are a helpful agent.

{{role "user"}}
{{userInput}}
EOF

# Sync to database
stn sync default

# Run it
stn agent run my-agent "Hello, what can you do?"
```

### 2. Add External Tools

```bash
# Add GitHub MCP server with template variable
stn mcp add github \
  --command npx \
  --args "-y,@modelcontextprotocol/server-github" \
  --env "GITHUB_TOKEN={{.GITHUB_TOKEN}}"

# Sync (will prompt for GITHUB_TOKEN)
stn sync default --browser

# Now agents can use __github_* tools
```

### 3. Create Agent Team

```bash
# Create specialist agents first
# Edit files at ~/.config/station/environments/default/

# Create coordinator that uses them
cat > ~/.config/station/environments/default/coordinator.prompt << 'EOF'
---
metadata:
  name: "coordinator"
  description: "Coordinates investigation"
model: gpt-4o-mini
max_steps: 15
agents:
  - "logs-analyst"
  - "metrics-analyst"
---
{{role "system"}}
Coordinate these specialists to investigate issues.

{{role "user"}}
{{userInput}}
EOF

stn sync default
stn agent run coordinator "Investigate high latency"
```

### 4. Install and Use Bundle

```bash
# Install SRE bundle
stn bundle install https://github.com/cloudshipai/registry/releases/latest/download/sre-bundle.tar.gz sre

# Sync the environment
stn sync sre

# List and run agents
stn agent list --env sre
stn agent run incident-coordinator "API returning 503 errors" --env sre
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GEMINI_API_KEY` | Google Gemini API key |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint (default: http://localhost:4318) |
| `STATION_CONFIG_DIR` | Override config directory |

## Troubleshooting

### Agent not finding tools
```bash
stn sync <environment>          # Resync configurations
stn mcp tools                   # Verify tools are loaded
```

### MCP server not starting
```bash
stn mcp status                  # Check server status
# Test command manually:
npx -y @package/mcp-server
```

### View execution traces
```bash
stn jaeger up                   # Start Jaeger
# Open http://localhost:16686
# Search for service: station
```
