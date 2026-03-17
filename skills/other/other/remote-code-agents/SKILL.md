---
name: remote-code-agents
description: "Delegate tasks to remote Claude Code agent containers for parallel execution, long-running analysis, or resource-intensive operations."
---

# Remote Code Agents

## Core Principle

When facing long-running tasks, complex analysis, or workloads better suited for dedicated compute resources, delegate them to remote Claude Code agent containers rather than executing locally.

**Note**: This skill supports both Claude Code agents (production-ready) and OpenRouter agents (⚠️ experimental, multi-model support).

## When to Use This Skill

### Always Use When:
- **Long-running analysis** that would block current workflow (> 5 minutes)
- **Resource-intensive tasks** like full codebase analysis or performance profiling
- **Parallel workload distribution** across multiple specialized agents
- **Background research** that doesn't block current development

### Example Scenarios:
- Code review of large pull requests
- Security audit of entire codebase
- Performance optimization analysis
- Documentation generation for multiple modules
- Test generation for legacy code
- Dependency update research

## Environment Configuration

Remote code agents require the following environment variables:

```bash
# Required: API endpoint for your remote agents
export REMOTE_AGENT_API_URL="http://your-agent-host:8080"

# Required: API key for authentication
export REMOTE_AGENT_API_KEY="your-secure-api-key"

# Optional: Default agent type
export REMOTE_AGENT_DEFAULT_TYPE="general"
```

**Note**: Never commit API keys or internal endpoints to version control. Use:
- `.env` files (gitignored)
- Secret management systems (Vault, AWS Secrets Manager)
- CI/CD secret variables

## Agent Types

### General Agent
**Use for**: Coding, debugging, refactoring, feature implementation

```bash
AGENT_TYPE=general
```

### Research Agent
**Use for**: Analysis, documentation, architecture review, research

```bash
AGENT_TYPE=research
```

### Testing Agent
**Use for**: Code review, test generation, QA analysis

```bash
AGENT_TYPE=testing
```

## Integration Patterns

### 1. Command-Line Delegation

If you have the `claude-task` CLI installed:

```bash
# Submit a task
TASK_ID=$(claude-task submit \
  "Analyze this codebase for performance bottlenecks in API endpoints" \
  --repo https://github.com/org/repo \
  --type research)

# Check status later
claude-task status $TASK_ID

# Wait for completion
claude-task wait $TASK_ID
```

### 2. API-Based Delegation

Using curl or HTTP clients:

```bash
# Submit task
curl -X POST "${REMOTE_AGENT_API_URL}/tasks" \
  -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code for security vulnerabilities",
    "repo_url": "https://github.com/org/repo",
    "branch": "main",
    "agent_type": "testing"
  }'

# Response: {"task_id": "uuid", "status": "submitted"}

# Check status
curl -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  "${REMOTE_AGENT_API_URL}/tasks/${TASK_ID}"

# Get results
curl -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  "${REMOTE_AGENT_API_URL}/tasks/${TASK_ID}/output"
```

### 3. CI/CD Integration

#### GitLab CI Example

```yaml
code-review:
  stage: review
  script:
    - |
      TASK_ID=$(curl -X POST "${REMOTE_AGENT_API_URL}/tasks" \
        -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
          \"prompt\": \"Review this merge request for bugs and security issues\",
          \"repo_url\": \"${CI_REPOSITORY_URL}\",
          \"branch\": \"${CI_COMMIT_REF_NAME}\",
          \"agent_type\": \"testing\"
        }" | jq -r '.task_id')

      # Wait for completion (with timeout)
      for i in {1..60}; do
        STATUS=$(curl -s -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
          "${REMOTE_AGENT_API_URL}/tasks/${TASK_ID}" | jq -r '.status')

        [ "$STATUS" = "completed" ] && break
        sleep 10
      done

      # Get and display results
      curl -s -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
        "${REMOTE_AGENT_API_URL}/tasks/${TASK_ID}/output"
  only:
    - merge_requests
```

#### GitHub Actions Example

```yaml
- name: Delegate to Remote Agent
  env:
    REMOTE_AGENT_API_URL: ${{ secrets.REMOTE_AGENT_API_URL }}
    REMOTE_AGENT_API_KEY: ${{ secrets.REMOTE_AGENT_API_KEY }}
  run: |
    TASK_ID=$(curl -X POST "${REMOTE_AGENT_API_URL}/tasks" \
      -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
      -H "Content-Type: application/json" \
      -d '{
        "prompt": "Generate tests for new features",
        "repo_url": "${{ github.repository }}",
        "agent_type": "testing"
      }' | jq -r '.task_id')

    echo "Task submitted: ${TASK_ID}"
```

### 4. From Current Session

When working interactively and you need to delegate:

```bash
# Explain to user what you're doing
echo "This analysis will take ~15 minutes. Delegating to remote agent..."

# Submit task
TASK_ID=$(curl -X POST "${REMOTE_AGENT_API_URL}/tasks" \
  -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Perform comprehensive security audit of authentication system",
    "repo_url": "https://github.com/org/repo",
    "agent_type": "research"
  }' | jq -r '.task_id')

echo "Task ID: ${TASK_ID}"
echo "You can check status with: curl -H 'X-API-Key: ${REMOTE_AGENT_API_KEY}' ${REMOTE_AGENT_API_URL}/tasks/${TASK_ID}"
```

## Task Lifecycle

### States
- **pending**: Task queued, waiting for agent
- **processing**: Agent actively working on task
- **completed**: Task finished successfully
- **failed**: Task encountered errors

### Monitoring

```bash
# List all tasks
curl -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  "${REMOTE_AGENT_API_URL}/tasks"

# Filter by status
curl -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  "${REMOTE_AGENT_API_URL}/tasks?status=completed"

# Get available agents
curl -H "X-API-Key: ${REMOTE_AGENT_API_KEY}" \
  "${REMOTE_AGENT_API_URL}/agents"
```

## Best Practices

### 1. Clear Task Descriptions
Be specific in your prompts:

❌ **Bad**: "Fix bugs"
✅ **Good**: "Review the authentication module for security vulnerabilities, focusing on JWT validation and password hashing"

### 2. Choose Appropriate Agent Type
- **General**: Implementation, debugging, refactoring
- **Research**: Analysis, documentation, investigation
- **Testing**: Reviews, test generation, QA

### 3. Don't Wait for Long Tasks
For tasks > 5 minutes:
```bash
# Submit and continue working
TASK_ID=$(submit_task "Long analysis task")
echo "Check later: claude-task status ${TASK_ID}"

# Return to it later when needed
```

### 4. Security Considerations
- Never expose API keys in code
- Use environment variables or secret management
- Rotate API keys regularly
- Limit agent access to necessary repositories only

### 5. Repository Access
Ensure remote agents can access repositories:
- Use public repos, OR
- Configure SSH keys/tokens on agent host, OR
- Use repository mirrors accessible to agents

## Setting Up Remote Agents

If you want to set up your own remote agent infrastructure:

### Requirements
- Docker-capable server (Linux, macOS, Windows)
- Anthropic API key
- Network accessibility (VPN, Tailscale, or public IP)

### Basic Setup
```bash
# Create agent directory
mkdir -p ~/claude-agents

# Configure environment
cat > ~/claude-agents/.env <<EOF
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
API_KEY=your-secure-random-api-key
EOF

# Deploy using Docker Compose
# (See repository examples for docker-compose.yml)

docker-compose up -d
```

### Recommended: Use Private Network
- Tailscale, ZeroTier, or WireGuard VPN
- Avoid exposing to public internet
- Use mTLS if public exposure required

## Integration with Other Skills

### Combines With:
- **git-platform-cli**: Get repo URLs for delegation
- **code-review**: Delegate reviews to testing agent
- **test-driven-development**: Generate tests via testing agent
- **systematic-debugging**: Delegate root cause analysis

### Example Combined Workflow:

```bash
# 1. Get current branch/repo info (git-platform-cli)
REPO_URL=$(git remote get-url origin)
BRANCH=$(git branch --show-current)

# 2. Delegate code review (remote-code-agents)
TASK_ID=$(claude-task submit \
  "Review changes in ${BRANCH} for bugs, security, and performance" \
  --repo "${REPO_URL}" \
  --type testing)

# 3. Continue local work while agent reviews

# 4. Later: Check results
claude-task status ${TASK_ID}
```

## Commitment

When delegating to remote agents, I will:

- [ ] Use appropriate agent type for the task
- [ ] Provide clear, specific task descriptions
- [ ] Configure environment variables, never hardcode credentials
- [ ] Inform user when delegating long-running tasks
- [ ] Monitor task status for time-sensitive work
- [ ] Consider security implications of repository access
- [ ] Document task IDs for later reference
- [ ] Choose delegation over local execution for resource-intensive work

---

**Note**: This skill requires external infrastructure. Ensure remote agents are configured and accessible before use.
