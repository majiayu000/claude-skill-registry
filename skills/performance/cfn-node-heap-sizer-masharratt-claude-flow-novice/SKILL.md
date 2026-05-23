---
name: cfn-node-heap-sizer
description: Task mode heap limiter for memory-constrained environments
version: 1.0.0
tags: [memory, heap, node, performance]
status: production
---

# CFN Node Heap Sizer Skill

## Purpose

Dynamically manages Node.js heap size for Task tool agents to prevent OOM (Out of Memory) issues in memory-constrained environments. The skill automatically detects execution mode and tool type to apply appropriate heap limits, ensuring stable performance across different CFN Loop operations.

## Usage

```bash
# Source the skill to use its functions
source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh

# Direct execution
bash .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh [COMMAND] [OPTIONS]

# Commands:
  limit <command> [heap_override]     # Set heap limits
  configure <mode> <tool> <size>      # Manual configuration
  validate                            # Check current settings
  exec <command> [heap] [args...]     # Execute with limits
  --help                             # Show help
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CFN_MODE` | Execution mode (task, cli, debug, test) | Auto-detected |
| `CFN_VALIDATION_LOG_DIR` | Directory for heap configuration logs | Optional |
| `NODE_OPTIONS` | Modified to include heap size limits | Updated by skill |

## Dependencies

### Required Dependencies
- `bash` v4.0+ - For associative arrays and parameter expansion
- `node` - Node.js runtime (for heap limiting)

### Optional Dependencies
- `cfn-task-mode-safety` - For enhanced mode detection
- `cfn-validation-runner-instrumentation` - For wrapped execution

### System Requirements
- Linux/macOS environment
- Ability to modify environment variables
- Write permissions to log directory (if using `CFN_VALIDATION_LOG_DIR`)

## Configuration

### Default Heap Sizes by Mode

| Mode | Heap Size | Use Case |
|------|-----------|----------|
| `task` | 2048 MB | Task mode (conservative) |
| `cli` | 8192 MB | CLI mode (production) |
| `debug` | 1024 MB | Debugging (minimal) |
| `test` | 3072 MB | Testing (moderate) |

### Default Heap Sizes by Tool Type

| Tool | Heap Size | Description |
|------|-----------|-------------|
| `node` | 2048 MB | Standard Node.js processes |
| `bun` | 3072 MB | Bun JavaScript runtime |
| `playwright` | 4096 MB | Browser automation |
| `test` | 1536 MB | Test runners |
| `validator` | 1024 MB | Code validation tools |
| `reviewer` | 1024 MB | Code review tools |
| `tester` | 1024 MB | Testing agents |

## Integration Examples

### 1. Agent Spawning Integration

```bash
#!/bin/bash
# Example agent script with heap limiting

# Source the heap sizer
source "$(dirname "$0")/../.claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh"

# Detect and apply heap limits
limit_node_heap "node"

# Run the agent with heap protection
node "$@"
```

### 2. CFN Loop Task Mode Integration

```bash
#!/bin/bash
# Integration with Task tool execution

AGENT_ID="validator-$(date +%s)"
export CFN_MODE="task"

# Apply heap limiting before execution
source ".claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh"
exec_with_heap_limit "node" "1024" "validator-agent.js" "$@"
```

### 3. Docker Environment Integration

```dockerfile
FROM node:18-alpine

# Copy heap sizer
COPY .claude/skills/cfn-node-heap-sizer /usr/local/cfn/skills/cfn-node-heap-sizer

# Configure environment
ENV CFN_MODE=task
ENV CFN_VALIDATION_LOG_DIR=/var/log/cfn

# Apply heap limits in entrypoint
ENTRYPOINT ["/bin/bash", "-c", "source /usr/local/cfn/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh && exec_with_heap_limit node \"$@\"", "--"]
```

### 4. CI/CD Pipeline Integration

```yaml
- name: Apply Heap Limits
  run: |
    source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh
    configure_node_options "task" "test" "1536"

- name: Run Tests
  run: |
    exec_with_heap_limit "npm" "test"
```

## Usage Examples

### Basic Usage

```bash
# Source the skill
source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh

# Limit heap for current session
limit_node_heap "node"

# Run with automatic detection
node script.js  # Will use configured heap size
```

### Custom Heap Size

```bash
# Override default heap size
limit_node_heap "node" "4096"

# Or execute directly with custom size
exec_with_heap_limit "node" "4096" "memory-intensive-script.js"
```

### Tool-Specific Configuration

```bash
# Configure for Playwright
source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh
configure_node_options "task" "playwright" "4096"

# Run Playwright tests
npx playwright test
```

### Validation and Monitoring

```bash
# Check current configuration
validate_heap_configuration

# Show current status
bash .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh
```

### Logging Integration

```bash
# Enable logging
export CFN_VALIDATION_LOG_DIR="./logs"

# Apply limits (will log configuration)
limit_node_heap "node"

# Check log files
ls -la $CFN_VALIDATION_LOG_DIR/heap-config_*.log
```

## Troubleshooting

### Common Issues

1. **Heap Size Not Applied**
   ```bash
   # Check if NODE_OPTIONS is set
   echo $NODE_OPTIONS

   # Validate current configuration
   bash .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh validate
   ```

2. **Mode Detection Issues**
   ```bash
   # Explicitly set mode
   export CFN_MODE="task"

   # Or detect mode
   source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh
   detect_execution_mode
   ```

3. **Insufficient Memory**
   ```bash
   # Increase heap size for specific tool
   exec_with_heap_limit "node" "6144" "heavy-processing.js"

   # Or use CLI mode for more memory
   export CFN_MODE="cli"
   limit_node_heap "node"
   ```

4. **Permission Issues with Logs**
   ```bash
   # Create log directory
   mkdir -p $CFN_VALIDATION_LOG_DIR
   chmod 755 $CFN_VALIDATION_LOG_DIR
   ```

5. **Tool Detection Failure**
   ```bash
   # Configure manually
   configure_node_options "task" "node" "2048"

   # Or specify tool in command
   exec_with_heap_limit "node" "2048" "tool-specific-script.js"
   ```

### Debug Mode

```bash
# Enable debug output
set -x

# Run with verbose output
source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh
detect_execution_mode
detect_tool_type "node" "script.js"
calculate_heap_size "task" "node"
```

### Performance Tuning

```bash
# For memory-intensive operations
export CFN_MODE="cli"
configure_node_options "cli" "node" "8192"

# For quick validation tasks
export CFN_MODE="task"
configure_node_options "task" "validator" "1024"
```

## Advanced Configuration

### Custom Heap Profiles

```bash
# Create custom heap profile
CUSTOM_HEAPS=(
    ["microservice"]="512"
    ["batch-job"]="16384"
    ["api-server"]="4096"
)

# Apply custom profile
configure_node_options "task" "microservice" "${CUSTOM_HEAPS[microservice]}"
```

### Integration with cfn-task-mode-safety

```bash
# Enhanced mode detection
source .claude/skills/cfn-task-mode-safety/mode-detection.sh
source .claude/skills/cfn-node-heap-sizer/task-mode-heap-limiter.sh

# Will use enhanced detection
limit_node_heap "node"
```

## Security Considerations

- Heap size modifications apply only to the current shell session
- No persistent changes to system-wide Node.js configuration
- Logs contain heap sizes but no sensitive data
- Tool detection based on command names (no command injection risk)

## Best Practices

1. Always source the script at the beginning of agent scripts
2. Use mode-specific heap sizes for different environments
3. Enable logging in production for monitoring
4. Validate configuration before critical operations
5. Use tool-specific configurations for specialized agents
6. Monitor OOM errors and adjust heap sizes accordingly