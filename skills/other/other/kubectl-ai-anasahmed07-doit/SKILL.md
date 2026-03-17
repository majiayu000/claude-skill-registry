---
name: kubectl-ai
description: AI-powered Kubernetes operations using kubectl-ai from Google Cloud Platform. This skill should be used when managing Kubernetes clusters with natural language commands, generating manifests, troubleshooting issues, and performing AI-assisted DevOps. Use this skill for Phase IV AIOps integration with Minikube and cloud clusters.
---

# kubectl-ai Skill

## Overview

kubectl-ai is an intelligent interface from Google Cloud Platform that translates natural language into precise Kubernetes operations. It supports multiple LLM providers (Gemini, OpenAI, Azure OpenAI, Ollama, Grok) and can generate, apply, and troubleshoot Kubernetes resources.

## Installation

### macOS (ARM64)
```bash
# Download
curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Darwin_arm64.tar.gz

# Extract and install
tar -zxvf kubectl-ai_Darwin_arm64.tar.gz
chmod a+x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/
```

### macOS (AMD64)
```bash
curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Darwin_x86_64.tar.gz
tar -zxvf kubectl-ai_Darwin_x86_64.tar.gz
chmod a+x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/
```

### Linux
```bash
curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Linux_x86_64.tar.gz
tar -zxvf kubectl-ai_Linux_x86_64.tar.gz
chmod a+x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/
```

## Configuration

### Set API Keys

```bash
# Gemini (default)
export GEMINI_API_KEY=your_api_key_here

# OpenAI
export OPENAI_API_KEY=your_api_key_here

# Azure OpenAI
export AZURE_OPENAI_ENDPOINT=your_endpoint_here
export AZURE_OPENAI_API_KEY=your_api_key_here

# Grok
export GROK_API_KEY=your_xai_api_key_here
```

### Verify Setup

```bash
# Check kubectl-ai is working
kubectl-ai --help

# Interactive mode
kubectl-ai
```

## Usage Patterns

### Basic Commands

```bash
# Interactive mode (default)
kubectl-ai

# Single command (quiet mode)
kubectl-ai -quiet "show me all pods in the default namespace"

# Specify model
kubectl-ai --model gemini-2.5-pro "list all deployments"
```

### Using Different Providers

```bash
# Gemini (default)
kubectl-ai "show all services"

# OpenAI
kubectl-ai --llm-provider=openai --model=gpt-4.1 "scale nginx to 5 replicas"

# Azure OpenAI
kubectl-ai --llm-provider=azopenai --model=your_deployment_name "check pod logs"

# Grok
kubectl-ai --llm-provider=grok --model=grok-3-beta "describe the cluster"

# Ollama (local)
kubectl-ai --llm-provider ollama --model gemma3:12b-it-qat --enable-tool-use-shim "list pods"
```

## Common Operations

### Information Gathering

```bash
# List resources
kubectl-ai -quiet "show me all pods in the default namespace"
kubectl-ai -quiet "list all deployments across all namespaces"
kubectl-ai -quiet "what services are running?"

# Describe resources
kubectl-ai -quiet "describe the nginx deployment"
kubectl-ai -quiet "show me the logs from the api pod"
kubectl-ai -quiet "what's consuming the most memory?"
```

### Creating Resources

```bash
# Create deployment
kubectl-ai -quiet "create a deployment named nginx with 3 replicas using nginx:latest image"

# Create service
kubectl-ai -quiet "expose the nginx deployment on port 80"

# Create configmap
kubectl-ai -quiet "create a configmap called app-config with DATABASE_URL=postgres://db:5432"
```

### Scaling and Updates

```bash
# Scale deployment
kubectl-ai -quiet "scale the nginx deployment to 5 replicas"
kubectl-ai -quiet "double the capacity for the nginx app"

# Update image
kubectl-ai -quiet "update the api deployment to use image api:v2.0"

# Rolling restart
kubectl-ai -quiet "restart the api deployment"
```

### Troubleshooting

```bash
# Check pod issues
kubectl-ai -quiet "why is the api pod failing?"
kubectl-ai -quiet "check logs for nginx app in hello namespace"
kubectl-ai -quiet "show events for failing pods"

# Resource issues
kubectl-ai -quiet "which pods are using the most CPU?"
kubectl-ai -quiet "find pods that are in CrashLoopBackOff"

# Network issues
kubectl-ai -quiet "test connectivity to the database service"
```

### Cleanup

```bash
# Delete resources
kubectl-ai -quiet "delete all pods in pending state"
kubectl-ai -quiet "remove the nginx deployment"
kubectl-ai -quiet "clean up completed jobs"
```

## Pipeline Input

kubectl-ai accepts input from stdin:

```bash
# Explain error log
cat error.log | kubectl-ai "explain the error"

# Process kubectl output
kubectl get pods -o yaml | kubectl-ai "find pods without resource limits"

# Analyze manifest
cat deployment.yaml | kubectl-ai "review this manifest for best practices"
```

## Interactive Mode Commands

When running `kubectl-ai` without arguments:

```
>> help           # Show available commands
>> models         # List available models (Ollama)
>> clear          # Clear conversation
>> exit           # Exit interactive mode
```

## MCP Server Mode

kubectl-ai can run as an MCP server for integration with AI tools:

```bash
# Start as MCP server
kubectl-ai --kubeconfig ~/.kube/config --mcp-server
```

### Claude Integration (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "kubectl-ai": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/config", "--mcp-server"],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": "/Users/your-username",
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

## TaskFlow Examples

```bash
# Deploy TaskFlow components
kubectl-ai -quiet "create a deployment for taskflow-api with image taskflow/api:latest on port 8000"
kubectl-ai -quiet "create a ClusterIP service for the taskflow-api deployment"

# Configure networking
kubectl-ai -quiet "create an ingress for taskflow with /api pointing to api service and / pointing to web service"

# Troubleshoot
kubectl-ai -quiet "why is the taskflow-api pod not starting?"
kubectl-ai -quiet "check the logs from all taskflow pods"

# Scale for load
kubectl-ai -quiet "scale all taskflow deployments to 3 replicas"
```

## Best Practices

1. **Use quiet mode for scripts**: `-quiet` flag for automation
2. **Review before applying**: kubectl-ai shows commands before execution
3. **Specify namespace**: Include namespace in prompts to avoid confusion
4. **Use specific models**: `--model gemini-2.5-flash-preview-04-17` for faster responses
5. **Combine with kubectl**: Use kubectl-ai for complex tasks, kubectl for simple ones

## Resources

Refer to `references/prompt-patterns.md` for effective prompt patterns.
