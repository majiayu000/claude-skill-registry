# CFN Docker Agent Spawning Skill

**Purpose:** Spawn agents in isolated Docker containers with skill-based MCP selection, resource management, and authentication.

## Overview

This skill manages the lifecycle of container-based agents, providing isolated execution environments with controlled resource usage, secure MCP access, and comprehensive monitoring capabilities.

## Architecture

```bash
Agent Spawning Request
    ↓
Container Configuration (memory, CPU, volumes)
    ↓
Docker Container Creation
    ↓
MCP Token Generation & Injection
    ↓
Agent Initialization (claude-flow-novice agent-spawn)
    ↓
Resource Monitoring & Management
```

## Core Functions

### 1. Container Configuration
Generate Docker container specifications based on agent type and requirements:

```bash
# Configure container for frontend engineer
cfn-docker-agent-spawn configure \
  --agent-type react-frontend-engineer \
  --memory-limit 1g \
  --cpu-limit 1.0 \
  --network mcp-network
```

### 2. Container Creation
Create and start Docker containers with proper isolation:

```bash
# Spawn agent container
cfn-docker-agent-spawn create \
  --agent-id agent-frontend-001 \
  --agent-type react-frontend-engineer \
  --task-id task-authentication \
  --context "${TASK_CONTEXT}"
```

### 3. MCP Integration
Configure secure MCP server access with authentication tokens:

```bash
# Setup MCP access for container
cfn-docker-agent-spawn setup-mcp \
  --container-id agent-frontend-001 \
  --mcp-servers playwright \
  --token-file /tmp/mcp-tokens.json
```

### 4. Resource Management
Monitor and manage container resources:

```bash
# Monitor container resources
cfn-docker-agent-spawn monitor \
  --container-id agent-frontend-001 \
  --alert-threshold 90%
```

## Container Specification

### Standard Configuration
```yaml
# Docker container specification
agent-container:
  image: claude-flow-novice:agent
  hostname: agent-{{AGENT_ID}}
  networks:
    - mcp-network
  volumes:
    - ./.claude:/app/.claude:ro
    - ./src:/app/src:ro
    - agent-workspace-{{AGENT_ID}}:/app/workspace
  environment:
    - AGENT_ID={{AGENT_ID}}
    - AGENT_TYPE={{AGENT_TYPE}}
    - TASK_ID={{TASK_ID}}
    - REDIS_URL=redis://redis:6379
    - MCP_TOKENS_FILE=/tmp/mcp-tokens.json
  resources:
    memory: {{MEMORY_LIMIT}}
    cpu: {{CPU_LIMIT}}
  restart_policy: unless-stopped
```

### Volume Mounts
- **Codebase**: Read-only mount for source code and skills
- **Agent Configuration**: Read-only mount for .claude directory
- **Workspace**: Writable mount for agent work output
- **Token Store**: Temporary file for MCP authentication tokens

### Environment Variables
- `AGENT_ID`: Unique container identifier
- `AGENT_TYPE`: Agent type for skill-based selection
- `TASK_ID`: CFN Loop task identifier
- `REDIS_URL`: Redis connection string
- `MCP_TOKENS_FILE`: Path to MCP authentication tokens

## Usage Patterns

### Basic Agent Spawning
```bash
# Spawn single agent
cfn-docker-agent-spawn \
  --agent-type react-frontend-engineer \
  --task-id "implement-ui" \
  --memory-limit 1g
```

### Batch Agent Spawning
```bash
# Spawn team of agents
cfn-docker-agent-spawn batch \
  --team frontend \
  --agents 3 \
  --task-id "ui-development" \
  --memory-limit 1g \
  --network mcp-network
```

### Custom Configuration
```bash
# Spawn with custom configuration
cfn-docker-agent-spawn \
  --agent-type security-specialist \
  --custom-config config/security-agent.json \
  --environment "DEBUG=true,LOG_LEVEL=verbose" \
  --volume /data/secrets:/app/secrets:ro
```

## Resource Management

### Memory Limits
| Agent Type | Default Limit | Maximum Recommended |
|------------|---------------|---------------------|
| **Frontend Engineer** | 1GB | 2GB |
| **Backend Developer** | 768MB | 1.5GB |
| **Security Specialist** | 1.5GB | 3GB |
| **DevOps Engineer** | 1GB | 2GB |

### CPU Limits
- **Standard Agents**: 0.5-1.0 CPU units
- **Resource-Intensive Agents**: 1.0-2.0 CPU units
- **Batch Operations**: 0.3-0.5 CPU units per agent

### Network Configuration

**Multi-Worktree Network Isolation:**

For multi-worktree environments, use project-scoped network names:

```bash
# Set project name from environment (set by run-in-worktree.sh)
PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cfn-default}"

# Create isolated network for MCP communication (worktree-scoped)
docker network create "${PROJECT_NAME}_mcp-network" --driver bridge

# Connect containers to MCP network
docker network connect "${PROJECT_NAME}_mcp-network" agent-frontend-001
docker network connect "${PROJECT_NAME}_mcp-network" playwright-mcp
```

**Service Discovery Within Networks:**

Agents within the Docker network can access services by name:
```bash
# Use service names (not container names) for connections
redis-cli -h redis              # Resolves to Redis service
psql -h postgres                # Resolves to PostgreSQL service
curl http://orchestrator:3001   # Resolves to orchestrator service
```

**Why Project-Scoped Networks?**
- Prevents network name conflicts between worktrees
- Isolates agent communication per branch
- Enables simultaneous multi-worktree development
- Automatically managed by docker-compose with COMPOSE_PROJECT_NAME

## Integration with CFN Docker Skills

### Skill-Based MCP Selection
```bash
# Get MCP configuration for agent
MCP_CONFIG=$(cfn-docker-skill-mcp-selector select --agent-type ${AGENT_TYPE})

# Spawn with MCP configuration
cfn-docker-agent-spawn \
  --agent-type ${AGENT_TYPE} \
  --mcp-config "${MCP_CONFIG}" \
  --auto-tokens
```

### Redis Coordination
```bash
# Register agent in Redis
cfn-docker-redis-coordination register \
  --agent-id ${AGENT_ID} \
  --container-id ${CONTAINER_ID} \
  --status "spawning"

# Update agent status
cfn-docker-redis-coordination update-status \
  --agent-id ${AGENT_ID} \
  --status "running"
```

### Loop Orchestration
```bash
# Spawn agents for Loop 3 implementation
cfn-docker-loop-orchestration spawn-loop3 \
  --task-context "${TASK_CONTEXT}" \
  --agent-count 3 \
  --parallel
```

## Monitoring and Observability

### Resource Monitoring
```bash
# Real-time resource usage
cfn-docker-agent-spawn stats \
  --agent-id agent-frontend-001 \
  --format json

# Historical resource data
cfn-docker-agent-spawn history \
  --agent-id agent-frontend-001 \
  --duration 1h
```

### Health Checks
```bash
# Container health status
cfn-docker-agent-spawn health \
  --agent-id agent-frontend-001

# MCP server connectivity
cfn-docker-agent-spawn check-mcp \
  --agent-id agent-frontend-001 \
  --servers playwright,redis
```

### Logging
```bash
# Container logs
cfn-docker-agent-spawn logs \
  --agent-id agent-frontend-001 \
  --tail 100

# Structured logs for monitoring
cfn-docker-agent-spawn logs \
  --agent-id agent-frontend-001 \
  --format json \
  --output /var/log/agents/${AGENT_ID}.log
```

## Error Handling

### Container Failure Recovery
```bash
# Automatic restart on failure
cfn-docker-agent-spawn \
  --agent-type ${AGENT_TYPE} \
  --restart-policy on-failure \
  --restart-count 3

# Manual recovery
cfn-docker-agent-spawn recover \
  --agent-id agent-frontend-001 \
  --backup-state
```

### Resource Exhaustion Handling
```bash
# Memory pressure handling
cfn-docker-agent-spawn \
  --memory-limit 1g \
  --memory-swap 1.5g \
  --oom-kill-disable

# CPU throttling
cfn-docker-agent-spawn \
  --cpu-limit 1.0 \
  --cpu-shares 1024
```

### Network Isolation Issues
```bash
# Network connectivity validation
cfn-docker-agent-spawn validate-network \
  --agent-id agent-frontend-001 \
  --targets redis:6379,playwright-mcp:3000

# Network repair
cfn-docker-agent-spawn repair-network \
  --agent-id agent-frontend-001 \
  --recreate-network
```

## Performance Optimization

### Startup Optimization
- **Pre-warmed Images**: Use Docker image layer caching
- **Parallel Startup**: Spawn multiple containers concurrently
- **Lazy Loading**: Load MCP servers on-demand
- **Resource Pre-allocation**: Reserve resources in advance

### Memory Optimization
- **Selective MCP Loading**: Only load required MCP servers
- **Workspace Cleanup**: Clean temporary files automatically
- **Garbage Collection**: Optimize Node.js memory management
- **Shared Libraries**: Use shared mounts for common dependencies

### Network Optimization
- **Local Network**: Use Docker bridge networks for MCP communication
- **Connection Pooling**: Reuse MCP server connections
- **DNS Caching**: Cache MCP server DNS resolution
- **Compression**: Compress large data transfers

## Security Considerations

### Container Isolation
- **Read-only Codebase**: Prevent code modification
- **Limited Privileges**: Run as non-root user
- **Resource Limits**: Prevent DoS attacks
- **Network Segmentation**: Isolate agent networks

### Token Security
- **Secure Token Storage**: Use tmpfs for token files
- **Token Expiration**: Automatic token rotation
- **Access Logging**: Log all token usage
- **Revocation**: Immediate token invalidation

### File System Security
- **Restricted Access**: Limit file system access
- **Workspace Isolation**: Isolate agent workspaces
- **Temporary Files**: Secure cleanup of temporary files
- **Audit Logging**: Log all file system operations

## Testing and Validation

### Unit Tests
- Container creation and configuration
- Resource limit enforcement
- Network connectivity validation
- Token injection and validation

### Integration Tests
- End-to-end agent spawning workflow
- MCP server connectivity and authentication
- Resource monitoring and alerting
- Error handling and recovery

### Performance Tests
- Container startup time measurement
- Resource usage benchmarking
- Concurrent spawning scalability
- Network performance validation

## Troubleshooting

### Common Issues
1. **Container Won't Start**: Check image availability and resource limits
2. **MCP Connection Failed**: Verify network configuration and token validity
3. **Memory Issues**: Monitor usage and adjust limits
4. **Permission Errors**: Check volume mounts and user permissions

### Debug Commands
```bash
# Debug container creation
cfn-docker-agent-spawn debug \
  --agent-type ${AGENT_TYPE} \
  --verbose \
  --dry-run

# Inspect container configuration
cfn-docker-agent-spawn inspect \
  --container-id ${CONTAINER_ID} \
  --format json

# Validate MCP connectivity
cfn-docker-agent-spawn test-mcp \
  --container-id ${CONTAINER_ID} \
  --all-servers
```

## Best Practices

### Resource Planning
- **Conservative Limits**: Start with lower memory limits and increase as needed
- **Monitoring**: Implement comprehensive resource monitoring
- **Capacity Planning**: Plan for peak usage scenarios
- **Resource Cleanup**: Clean up unused containers and volumes

### Security Hardening
- **Minimal Images**: Use minimal Docker images
- **Regular Updates**: Keep base images updated
- **Scanning**: Regularly scan images for vulnerabilities
- **Access Control**: Implement proper access controls

### Operational Excellence
- **Automation**: Automate container lifecycle management
- **Observability**: Implement comprehensive monitoring
- **Documentation**: Maintain detailed configuration documentation
- **Backup**: Backup critical container configurations