---
name: aws-agentic-ai
aliases:
  - bedrock-agentcore
  - aws-agentic-ai
description: AWS Bedrock AgentCore comprehensive expert for deploying and managing all AgentCore services. Use when working with Gateway, Runtime, Memory, Identity, or any AgentCore component. Covers MCP target deployment, credential management, schema optimization, runtime configuration, memory management, and identity services.
context: fork
model: sonnet
skills:
  - aws-mcp-setup
allowed-tools:
  - mcp__aws-mcp__*
  - mcp__awsdocs__*
  - Bash(aws bedrock-agentcore-control *)
  - Bash(aws bedrock-agentcore-runtime *)
  - Bash(aws bedrock *)
  - Bash(aws s3 cp *)
  - Bash(aws s3 ls *)
  - Bash(aws secretsmanager *)
  - Bash(aws sts get-caller-identity)
hooks:
  PreToolUse:
    - matcher: Bash(aws bedrock-agentcore-control create-*)
      command: aws sts get-caller-identity --query Account --output text
      once: true
---

# AWS Bedrock AgentCore

AWS Bedrock AgentCore provides a complete platform for deploying and scaling AI agents with seven core services. This skill guides you through service selection, deployment patterns, and integration workflows using AWS CLI.

## AWS Documentation Requirement

**CRITICAL**: This skill requires AWS MCP tools for accurate, up-to-date AWS information.

### Before Answering AWS Questions

1. **Always verify** using AWS MCP tools (if available):
   - `mcp__aws-mcp__aws___search_documentation` or `mcp__*awsdocs*__aws___search_documentation` - Search AWS docs
   - `mcp__aws-mcp__aws___read_documentation` or `mcp__*awsdocs*__aws___read_documentation` - Read specific pages
   - `mcp__aws-mcp__aws___get_regional_availability` - Check service availability

2. **If AWS MCP tools are unavailable**:
   - Guide user to configure AWS MCP using the `aws-mcp-setup` skill (auto-loaded as dependency)
   - Help determine which option fits their environment:
     - Has uvx + AWS credentials → Full AWS MCP Server
     - No Python/credentials → AWS Documentation MCP (no auth)
   - If cannot determine → Ask user which option to use

## When to Use This Skill

Use this skill when you need to:
- Deploy REST APIs as MCP tools for AI agents (Gateway)
- Execute agents in serverless runtime (Runtime)
- Add conversation memory to agents (Memory)
- Manage API credentials and authentication (Identity)
- Enable agents to execute code securely (Code Interpreter)
- Allow agents to interact with websites (Browser)
- Monitor and trace agent performance (Observability)

## Available Services

| Service | Use For | Documentation |
|---------|---------|---------------|
| **Gateway** | Converting REST APIs to MCP tools | [`services/gateway/README.md`](services/gateway/README.md) |
| **Runtime** | Deploying and scaling agents | [`services/runtime/README.md`](services/runtime/README.md) |
| **Memory** | Managing conversation state | [`services/memory/README.md`](services/memory/README.md) |
| **Identity** | Credential and access management | [`services/identity/README.md`](services/identity/README.md) |
| **Code Interpreter** | Secure code execution in sandboxes | [`services/code-interpreter/README.md`](services/code-interpreter/README.md) |
| **Browser** | Web automation and scraping | [`services/browser/README.md`](services/browser/README.md) |
| **Observability** | Tracing and monitoring | [`services/observability/README.md`](services/observability/README.md) |

## Common Workflows

### Deploying a Gateway Target

**MANDATORY - READ DETAILED DOCUMENTATION**: See [`services/gateway/README.md`](services/gateway/README.md) for complete Gateway setup guide including deployment strategies, troubleshooting, and IAM configuration.

**Quick Workflow**:
1. Upload OpenAPI schema to S3
2. *(API Key auth only)* Create credential provider and store API key
3. Create gateway target linking schema (and credentials if using API key)
4. Verify target status and test connectivity

> **Note**: Credential provider is only needed for API key authentication. Lambda targets use IAM roles, and MCP servers use OAuth.

### Managing Credentials

**MANDATORY - READ DETAILED DOCUMENTATION**: See [`cross-service/credential-management.md`](cross-service/credential-management.md) for unified credential management patterns across all services.

**Quick Workflow**:
1. Use Identity service credential providers for all API keys
2. Link providers to gateway targets via ARN references
3. Rotate credentials quarterly through credential provider updates
4. Monitor usage with CloudWatch metrics

### Monitoring Agents

**MANDATORY - READ DETAILED DOCUMENTATION**: See [`services/observability/README.md`](services/observability/README.md) for comprehensive monitoring setup.

**Quick Workflow**:
1. Enable observability for agents
2. Configure CloudWatch dashboards for metrics
3. Set up alarms for error rates and latency
4. Use X-Ray for distributed tracing

## Service-Specific Documentation

For detailed documentation on each AgentCore service, see the following resources:

### Gateway Service
- **Overview**: [`services/gateway/README.md`](services/gateway/README.md)
- **Deployment Strategies**: [`services/gateway/deployment-strategies.md`](services/gateway/deployment-strategies.md)
- **Troubleshooting**: [`services/gateway/troubleshooting-guide.md`](services/gateway/troubleshooting-guide.md)

### Runtime, Memory, Identity, Code Interpreter, Browser, Observability
Each service has comprehensive documentation in its respective directory:
- [`services/runtime/README.md`](services/runtime/README.md)
- [`services/memory/README.md`](services/memory/README.md)
- [`services/identity/README.md`](services/identity/README.md)
- [`services/code-interpreter/README.md`](services/code-interpreter/README.md)
- [`services/browser/README.md`](services/browser/README.md)
- [`services/observability/README.md`](services/observability/README.md)

## Cross-Service Resources

For patterns and best practices that span multiple AgentCore services:

- **Credential Management**: [`cross-service/credential-management.md`](cross-service/credential-management.md) - Unified credential patterns, security practices, rotation procedures

## Additional Resources

- **AWS Documentation**: [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- **API Reference**: [Bedrock AgentCore Control Plane API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/)
- **AWS CLI Reference**: [bedrock-agentcore-control commands](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock-agentcore-control/index.html)

