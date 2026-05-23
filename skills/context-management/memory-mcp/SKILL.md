---
name: memory-mcp
description: Use and troubleshoot the Memory MCP server for episodic memory retrieval and pattern analysis. Use this skill when working with MCP server tools (query_memory, analyze_patterns, advanced_pattern_analysis), validating the MCP implementation, or debugging MCP server issues.
---

# Memory MCP Server

Interact with and troubleshoot the Memory Model Context Protocol (MCP) server for the self-learning memory system.

## When to Use

- Starting or configuring the memory-mcp server
- Using MCP tools for memory retrieval and pattern analysis
- Validating the MCP server implementation
- Debugging MCP server issues (connection, tool execution, performance)
- Testing MCP tools using the MCP inspector
- Understanding MCP configuration and environment variables

## MCP Server Overview

The memory-mcp server exposes episodic memory functionality through the Model Context Protocol, allowing AI agents to:
- Query past experiences and learned patterns
- Analyze successful strategies from historical episodes
- Execute code in a secure sandbox environment
- Perform advanced statistical and predictive analysis
- Monitor server health and metrics

**Location**: `./target/release/memory-mcp-server`
**Configuration**: `.mcp.json`
**Transport**: stdio (Standard Input/Output)

## Available MCP Tools

### 1. query_memory

Query episodic memory for relevant past experiences and learned patterns.

**Parameters**:
- `query` (required): Search query describing the task or context
- `domain` (required): Task domain (e.g., 'web-api', 'data-processing')
- `task_type` (optional): Type of task - `code_generation`, `debugging`, `refactoring`, `testing`, `analysis`, `documentation`
- `limit` (default: 10): Maximum number of episodes to retrieve

**Example**:
```json
{
  "query": "implement async storage with error handling",
  "domain": "rust-backend",
  "task_type": "code_generation",
  "limit": 5
}
```

**Use when**: You need relevant past experiences to inform current work.

### 2. analyze_patterns

Analyze patterns from past episodes to identify successful strategies.

**Parameters**:
- `task_type` (required): Type of task to analyze patterns for
- `min_success_rate` (default: 0.7): Minimum success rate (0.0-1.0)
- `limit` (default: 20): Maximum number of patterns to return

**Example**:
```json
{
  "task_type": "debugging",
  "min_success_rate": 0.8,
  "limit": 10
}
```

**Use when**: You want to identify proven successful approaches for a task type.

### 3. advanced_pattern_analysis

Perform advanced statistical analysis, predictive modeling, and causal inference on time series data.

**Parameters**:
- `analysis_type` (required): `statistical`, `predictive`, or `comprehensive`
- `time_series_data` (required): Object mapping variable names to numeric arrays
- `config` (optional): Analysis configuration
  - `significance_level` (default: 0.05): Statistical significance level
  - `forecast_horizon` (default: 10): Steps to forecast ahead
  - `anomaly_sensitivity` (default: 0.5): Anomaly detection sensitivity
  - `enable_causal_inference` (default: true): Perform causal analysis
  - `max_data_points` (default: 10000): Maximum data points
  - `parallel_processing` (default: true): Enable parallel processing

**Example**:
```json
{
  "analysis_type": "comprehensive",
  "time_series_data": {
    "latency_ms": [120, 115, 130, 125, 140],
    "success_rate": [0.95, 0.98, 0.96, 0.97, 0.99]
  },
  "config": {
    "forecast_horizon": 5,
    "anomaly_sensitivity": 0.6
  }
}
```

**Use when**: You need deep statistical insights and predictions from historical data.

### 4. execute_agent_code

Execute TypeScript/JavaScript code in a secure sandbox environment.

**Parameters**:
- `code` (required): TypeScript/JavaScript code to execute
- `context` (required): Execution context
  - `task`: Task description
  - `input`: Input data as JSON object

**Example**:
```json
{
  "code": "function process(data) { return data.map(x => x * 2); } process(context.input.numbers);",
  "context": {
    "task": "Double all numbers in array",
    "input": { "numbers": [1, 2, 3, 4, 5] }
  }
}
```

**Note**: Only available if WASM sandbox is enabled.

**Use when**: You need to safely execute user-provided or generated code.

### 5. health_check

Check the health status of the MCP server and its components.

**Parameters**: None

**Use when**: Diagnosing server issues or verifying operational status.

### 6. get_metrics

Get comprehensive monitoring metrics and statistics.

**Parameters**:
- `metric_type` (default: "all"): `all`, `performance`, `episodes`, or `system`

**Use when**: Monitoring server performance or gathering operational insights.

## Configuration

### .mcp.json Structure

```json
{
  "mcpServers": {
    "memory-mcp": {
      "type": "stdio",
      "command": "./target/release/memory-mcp-server",
      "args": [],
      "env": {
        "TURSO_DATABASE_URL": "file:/workspaces/feat-phase3/data/memory.db",
        "LOCAL_DATABASE_URL": "sqlite:/workspaces/feat-phase3/data/memory.db",
        "REDB_CACHE_PATH": "/workspaces/feat-phase3/data/cache.redb",
        "REDB_MAX_CACHE_SIZE": "1000",
        "MCP_CACHE_WARMING_ENABLED": "true",
        "MEMORY_MAX_EPISODES_CACHE": "1000",
        "MEMORY_CACHE_TTL_SECONDS": "1800",
        "RUST_LOG": "off"
      }
    }
  }
}
```

### Environment Variables

- **TURSO_DATABASE_URL**: Primary database URL (file:// for local)
- **LOCAL_DATABASE_URL**: Local SQLite database URL
- **REDB_CACHE_PATH**: Path to redb cache file
- **REDB_MAX_CACHE_SIZE**: Maximum cache entries (default: 1000)
- **MCP_CACHE_WARMING_ENABLED**: Enable cache warming on startup
- **MEMORY_MAX_EPISODES_CACHE**: Maximum episodes in cache
- **MEMORY_CACHE_TTL_SECONDS**: Cache time-to-live in seconds
- **RUST_LOG**: Logging level (off, error, warn, info, debug, trace)

## Starting the MCP Server

### Build the Server

```bash
cargo build --release --bin memory-mcp-server
```

### Run Directly

```bash
# With environment variables
export TURSO_DATABASE_URL="file:./data/memory.db"
export LOCAL_DATABASE_URL="sqlite:./data/memory.db"
export REDB_CACHE_PATH="./data/cache.redb"
export RUST_LOG=info

./target/release/memory-mcp-server
```

### Run via MCP Inspector

The MCP Inspector is the recommended tool for testing and validation.

```bash
npx -y @modelcontextprotocol/inspector ./target/release/memory-mcp-server
```

This opens a web interface at `http://localhost:5173` where you can:
- List available tools
- Test tool execution
- View request/response JSON
- Debug connection issues
- Validate tool schemas

See: https://modelcontextprotocol.io/docs/tools/inspector

## Validation Workflow

Use the MCP Inspector to validate implementation against best practices:

### Step 1: Build and Prepare

```bash
cargo build --release --bin memory-mcp-server
```

### Step 2: Launch Inspector

```bash
npx -y @modelcontextprotocol/inspector ./target/release/memory-mcp-server
```

### Step 3: Validate Tools

1. **List Tools**: Click "List Tools" - verify all expected tools appear
2. **Check Schemas**: Review each tool's input schema for correctness
3. **Test Execution**: Execute each tool with sample inputs
4. **Verify Responses**: Confirm responses match expected format

### Step 4: Test Core Workflows

- **Memory Retrieval**: Test `query_memory` with various domains/task types
- **Pattern Analysis**: Test `analyze_patterns` with different success rates
- **Advanced Analysis**: Test `advanced_pattern_analysis` with time series data
- **Health**: Verify `health_check` returns valid status
- **Metrics**: Check `get_metrics` provides comprehensive data

### Step 5: Performance Testing

- Test with large datasets
- Verify timeout handling
- Check memory usage
- Monitor response times

## Troubleshooting

### Common Issues

#### Server Won't Start

**Symptoms**: Process exits immediately or hangs

**Checks**:
1. Binary exists: `ls -la ./target/release/memory-mcp-server`
2. Binary is executable: `chmod +x ./target/release/memory-mcp-server`
3. Database files exist: `ls -la ./data/`
4. Environment variables set: `env | grep -E '(TURSO|REDB|RUST_LOG)'`

**Solutions**:
```bash
# Rebuild
cargo build --release --bin memory-mcp-server

# Create data directory
mkdir -p ./data

# Set environment variables
export TURSO_DATABASE_URL="file:./data/memory.db"
export LOCAL_DATABASE_URL="sqlite:./data/memory.db"
export REDB_CACHE_PATH="./data/cache.redb"
```

#### Tool Execution Fails

**Symptoms**: Tool returns errors or unexpected results

**Checks**:
1. Enable debug logging: `RUST_LOG=debug`
2. Validate input JSON against schema
3. Check database connectivity
4. Verify cache is accessible

**Debug Commands**:
```bash
# Run with debug logging
RUST_LOG=debug ./target/release/memory-mcp-server

# Check database
sqlite3 ./data/memory.db ".tables"

# Verify cache
ls -lh ./data/cache.redb
```

#### Performance Issues

**Symptoms**: Slow responses, timeouts

**Checks**:
1. Cache size configuration
2. Database size
3. Number of cached episodes
4. Concurrent requests

**Solutions**:
```bash
# Adjust cache settings
export REDB_MAX_CACHE_SIZE="2000"
export MEMORY_MAX_EPISODES_CACHE="2000"

# Reduce cache TTL
export MEMORY_CACHE_TTL_SECONDS="900"

# Disable cache warming if startup is slow
export MCP_CACHE_WARMING_ENABLED="false"
```

#### Connection Issues

**Symptoms**: Inspector can't connect, stdio communication fails

**Checks**:
1. Server process is running
2. No other process on same stdio
3. Binary path is correct
4. Shell environment is clean

**Solutions**:
```bash
# Kill existing processes
pkill memory-mcp-server

# Verify no zombie processes
ps aux | grep memory-mcp-server

# Restart inspector
npx -y @modelcontextprotocol/inspector ./target/release/memory-mcp-server
```

## Best Practices

### Tool Usage

✓ **DO**:
- Use `query_memory` before starting new tasks to learn from past experiences
- Set appropriate `limit` values to avoid over-retrieving
- Specify `task_type` to get more relevant results
- Use `analyze_patterns` to identify proven strategies
- Run `health_check` periodically in production
- Monitor metrics with `get_metrics` for performance insights

✗ **DON'T**:
- Query without a clear domain/task context
- Ignore min_success_rate when analyzing patterns
- Execute untrusted code without sandbox validation
- Run advanced analysis on tiny datasets (< 10 points)
- Skip health checks in production deployments

### Configuration

✓ **DO**:
- Use environment variables for all configuration
- Set RUST_LOG=off in production for performance
- Enable cache warming for better cold-start performance
- Use absolute paths for database files
- Configure appropriate cache sizes based on workload

✗ **DON'T**:
- Hardcode database paths in code
- Enable debug logging in production
- Use file:// URLs with relative paths
- Set cache size too small (< 100 episodes)
- Forget to create data directory before first run

### Testing

✓ **DO**:
- Always use MCP Inspector for validation
- Test all tools before deploying
- Verify schema compliance
- Test with realistic data volumes
- Check error handling with invalid inputs

✗ **DON'T**:
- Deploy without inspector validation
- Skip schema validation
- Test only happy paths
- Ignore performance testing
- Assume tools work without verification

## Integration Examples

### Query Memory Before Code Generation

```typescript
// Step 1: Query relevant past experiences
const context = await query_memory({
  query: "implement REST API with authentication",
  domain: "web-api",
  task_type: "code_generation",
  limit: 5
});

// Step 2: Analyze patterns from successful implementations
const patterns = await analyze_patterns({
  task_type: "code_generation",
  min_success_rate: 0.8,
  limit: 10
});

// Step 3: Use insights to inform implementation
// [Generate code using learned patterns]
```

### Performance Analysis Workflow

```typescript
// Step 1: Collect metrics over time
const metrics = await get_metrics({
  metric_type: "performance"
});

// Step 2: Perform advanced analysis
const analysis = await advanced_pattern_analysis({
  analysis_type: "comprehensive",
  time_series_data: {
    latency_ms: metrics.latency_history,
    success_rate: metrics.success_history
  },
  config: {
    forecast_horizon: 10,
    enable_causal_inference: true
  }
});

// Step 3: Use predictions to optimize
// [Apply optimizations based on forecasts]
```

## Related Resources

- **MCP Inspector**: https://modelcontextprotocol.io/docs/tools/inspector
- **MCP Specification**: https://modelcontextprotocol.io/
- **Project Configuration**: `.mcp.json`
- **Server Source**: `memory-mcp/src/bin/server.rs`
- **Tool Definitions**: `memory-mcp/src/server.rs`

## Summary

The memory-mcp skill helps you:
- ✓ Start and configure the MCP server
- ✓ Use all available MCP tools effectively
- ✓ Validate implementation with MCP Inspector
- ✓ Troubleshoot common issues
- ✓ Follow best practices for production deployment
- ✓ Integrate memory retrieval into workflows

Always validate using the MCP Inspector before deploying to production.
