---
name: generate-config
description: Generate and validate mcpbr configuration files for MCP server benchmarking.
---

# Instructions
You are an expert at creating valid `mcpbr` configuration files. Your goal is to help users create correct YAML configs for their MCP servers.

## Critical Requirements

1. **Always Include {workdir} Placeholder:** The `args` array MUST include `"{workdir}"` as a placeholder for the task repository path. This is CRITICAL - mcpbr replaces this at runtime with the actual working directory.

2. **Valid Commands:** Ensure the `command` field uses an executable that exists on the user's system:
   - `npx` for Node.js-based MCP servers
   - `uvx` for Python MCP servers via uv
   - `python` or `python3` for direct Python execution
   - Custom binaries (verify they exist with `which <command>`)

3. **Model Aliases:** Use short aliases when possible:
   - `sonnet` instead of `claude-sonnet-4-5-20250929`
   - `opus` instead of `claude-opus-4-5-20251101`
   - `haiku` instead of `claude-haiku-4-5-20251001`

4. **Required Fields:** Every config MUST have:
   - `mcp_server.command`
   - `mcp_server.args` (with `"{workdir}"`)
   - `provider` (usually `"anthropic"`)
   - `agent_harness` (usually `"claude-code"`)
   - `model`
   - `dataset` (or rely on benchmark default)

## Common MCP Server Configurations

### Anthropic Filesystem Server
```yaml
mcp_server:
  name: "filesystem"
  command: "npx"
  args:
    - "-y"
    - "@modelcontextprotocol/server-filesystem"
    - "{workdir}"
  env: {}
```

### Custom Python MCP Server
```yaml
mcp_server:
  name: "my-server"
  command: "uvx"
  args:
    - "my-mcp-server"
    - "--workspace"
    - "{workdir}"
  env:
    LOG_LEVEL: "debug"
```

### Supermodel Codebase Analysis
```yaml
mcp_server:
  name: "supermodel"
  command: "npx"
  args:
    - "-y"
    - "@supermodeltools/mcp-server"
  env:
    SUPERMODEL_API_KEY: "${SUPERMODEL_API_KEY}"
```

## Configuration Template

When generating a new config, use this template:

```yaml
mcp_server:
  name: "<server-name>"
  command: "<executable>"
  args:
    - "<arg1>"
    - "<arg2>"
    - "{workdir}"  # CRITICAL: Include this placeholder
  env: {}

provider: "anthropic"
agent_harness: "claude-code"

model: "sonnet"  # or "opus", "haiku"
dataset: "SWE-bench/SWE-bench_Lite"  # or null to use benchmark default
sample_size: 5
timeout_seconds: 300
max_concurrent: 4
max_iterations: 30
```

## Validation Steps

Before saving a config, validate:

1. **Workdir Placeholder:** Ensure `"{workdir}"` appears in `args` array.
2. **Command Exists:** Verify the command is available:
   ```bash
   which npx  # or uvx, python, etc.
   ```
3. **Syntax:** YAML syntax is correct (no tabs, proper indentation).
4. **Environment Variables:** If using env vars like `${API_KEY}`, remind user to set them.

## Benchmark-Specific Configurations

### SWE-bench (Default)
```yaml
# ... mcp_server config ...
provider: "anthropic"
agent_harness: "claude-code"
model: "sonnet"
dataset: "SWE-bench/SWE-bench_Lite"  # or SWE-bench/SWE-bench_Verified
sample_size: 10
```

### CyberGym
```yaml
# ... mcp_server config ...
provider: "anthropic"
agent_harness: "claude-code"
model: "sonnet"
benchmark: "cybergym"
dataset: "sunblaze-ucb/cybergym"
cybergym_level: 2  # 0-3
sample_size: 10
```

### MCPToolBench++
```yaml
# ... mcp_server config ...
provider: "anthropic"
agent_harness: "claude-code"
model: "sonnet"
benchmark: "mcptoolbench"
dataset: "MCPToolBench/MCPToolBenchPP"
sample_size: 10
```

## Custom Agent Prompts

Users can customize the agent prompt using the `agent_prompt` field:

```yaml
agent_prompt: |
  Fix the following bug in this repository:

  {problem_statement}

  Make the minimal changes necessary to fix the issue.
  Focus on the root cause, not symptoms.
```

**Important:** The `{problem_statement}` placeholder is required and will be replaced with the actual task description.

## Common Mistakes to Avoid

1. **Missing {workdir}:** Forgetting to include `"{workdir}"` in args.
2. **Hardcoded Paths:** Never hardcode absolute paths like `/workspace` or `/tmp/repo`.
3. **Invalid Commands:** Using commands that don't exist (e.g., `uv` instead of `uvx`).
4. **Wrong Indentation:** YAML is whitespace-sensitive. Use 2 spaces, not tabs.
5. **Missing Quotes:** Environment variable references like `"${VAR}"` need quotes.

## Example Workflow

When a user asks to create a config:

1. Ask about their MCP server:
   - What package/command runs the server?
   - Does it need any special arguments or environment variables?
   - Is it Node.js-based (npx) or Python-based (uvx)?

2. Generate the config based on their answers.

3. Validate the config:
   - Check for `{workdir}` placeholder
   - Verify command exists
   - Confirm YAML syntax

4. Save the config (usually to `mcpbr.yaml`).

5. Optionally test the config with a small sample:
   ```bash
   mcpbr run -c mcpbr.yaml -n 1 -v
   ```

## Helpful Commands

```bash
# Generate a default config
mcpbr init

# List available models
mcpbr models

# List available benchmarks
mcpbr benchmarks

# Validate config by doing a dry run with 1 task
mcpbr run -c config.yaml -n 1 -v
```
