---
name: kubernetes-flux
description: Kubernetes cluster management and troubleshooting. Query pods, deployments, services, logs, and events. Supports context switching, scaling, and rollout management. Use for Kubernetes debugging, monitoring, and operations.
allowed-tools: read, write, bash
version: 1.0
best_practices:
  - Verify kubectl is configured before operations
  - Use namespace flags for clarity
  - Check current context before cluster operations
  - Avoid destructive operations without confirmation
  - Mask secrets in output
error_handling: graceful
streaming: supported
safety_level: high
---

# Kubernetes Flux Skill

## Overview

This skill provides comprehensive Kubernetes cluster management through kubectl, enabling AI agents to inspect, troubleshoot, and manage Kubernetes resources with progressive disclosure for optimal context usage.

**Context Savings**: ~92% reduction

- **MCP Mode**: ~30,000 tokens always loaded (multiple tools + schemas)
- **Skill Mode**: ~800 tokens metadata + on-demand loading

## When to Use

- Debugging application pods and containers
- Monitoring deployment rollouts and status
- Analyzing service networking and endpoints
- Investigating cluster events and errors
- Troubleshooting performance issues
- Managing application scaling
- Port forwarding for local development
- Namespace and resource discovery

## Requirements

- kubectl installed and configured
- Valid KUBECONFIG file or default context
- Cluster access credentials
- Appropriate RBAC permissions for operations

## Quick Reference

```bash
# List available tools
python executor.py --list

# Get pods in current namespace
python executor.py --tool list_pods --args '{}'

# Get pods in specific namespace
python executor.py --tool list_pods --args '{"namespace": "production"}'

# Describe a pod
python executor.py --tool describe_pod --args '{"name": "my-app-123", "namespace": "default"}'

# Get pod logs
python executor.py --tool get_logs --args '{"name": "my-app-123", "namespace": "default"}'

# List recent events
python executor.py --tool list_events --args '{"namespace": "default", "limit": 20}'
```

## Tools

The skill provides 18 tools across discovery, inspection, management, and troubleshooting categories:

### Resource Discovery (6 tools)

#### list_pods

List pods in a namespace with status information.

| Parameter        | Type    | Description                        | Default         |
| ---------------- | ------- | ---------------------------------- | --------------- |
| `namespace`      | string  | Namespace to query                 | current context |
| `selector`       | string  | Label selector (e.g., "app=nginx") | none            |
| `all_namespaces` | boolean | List across all namespaces         | false           |

**Example**:

```bash
python executor.py --tool list_pods --args '{"namespace": "production", "selector": "app=web"}'
```

**Output Fields**: NAME, READY, STATUS, RESTARTS, AGE, NODE

#### list_deployments

List deployments with replica status.

| Parameter        | Type    | Description                | Default         |
| ---------------- | ------- | -------------------------- | --------------- |
| `namespace`      | string  | Namespace to query         | current context |
| `selector`       | string  | Label selector             | none            |
| `all_namespaces` | boolean | List across all namespaces | false           |

**Example**:

```bash
python executor.py --tool list_deployments --args '{"namespace": "production"}'
```

**Output Fields**: NAME, READY, UP-TO-DATE, AVAILABLE, AGE

#### list_services

List services with cluster IPs and ports.

| Parameter        | Type    | Description                | Default         |
| ---------------- | ------- | -------------------------- | --------------- |
| `namespace`      | string  | Namespace to query         | current context |
| `selector`       | string  | Label selector             | none            |
| `all_namespaces` | boolean | List across all namespaces | false           |

**Example**:

```bash
python executor.py --tool list_services --args '{"namespace": "default"}'
```

**Output Fields**: NAME, TYPE, CLUSTER-IP, EXTERNAL-IP, PORT(S), AGE

#### list_configmaps

List ConfigMaps in a namespace.

| Parameter        | Type    | Description                | Default         |
| ---------------- | ------- | -------------------------- | --------------- |
| `namespace`      | string  | Namespace to query         | current context |
| `all_namespaces` | boolean | List across all namespaces | false           |

**Example**:

```bash
python executor.py --tool list_configmaps --args '{"namespace": "default"}'
```

#### list_secrets

List Secrets in a namespace (names only, values masked).

| Parameter        | Type    | Description                | Default         |
| ---------------- | ------- | -------------------------- | --------------- |
| `namespace`      | string  | Namespace to query         | current context |
| `all_namespaces` | boolean | List across all namespaces | false           |

**Example**:

```bash
python executor.py --tool list_secrets --args '{"namespace": "default"}'
```

**Safety**: Secret values are NEVER displayed. Only metadata is shown.

#### list_namespaces

List all available namespaces.

**Example**:

```bash
python executor.py --tool list_namespaces --args '{}'
```

**Output Fields**: NAME, STATUS, AGE

### Resource Inspection (5 tools)

#### describe_pod

Get detailed information about a specific pod.

| Parameter   | Type   | Description | Required          |
| ----------- | ------ | ----------- | ----------------- |
| `name`      | string | Pod name    | Yes               |
| `namespace` | string | Namespace   | No (uses current) |

**Example**:

```bash
python executor.py --tool describe_pod --args '{"name": "nginx-abc123", "namespace": "default"}'
```

**Output Includes**: Events, Conditions, Volumes, Containers, Resource Limits, Node Assignment

#### describe_deployment

Get detailed information about a deployment.

| Parameter   | Type   | Description     | Required          |
| ----------- | ------ | --------------- | ----------------- |
| `name`      | string | Deployment name | Yes               |
| `namespace` | string | Namespace       | No (uses current) |

**Example**:

```bash
python executor.py --tool describe_deployment --args '{"name": "web-app", "namespace": "production"}'
```

#### describe_service

Get detailed information about a service.

| Parameter   | Type   | Description  | Required          |
| ----------- | ------ | ------------ | ----------------- |
| `name`      | string | Service name | Yes               |
| `namespace` | string | Namespace    | No (uses current) |

**Example**:

```bash
python executor.py --tool describe_service --args '{"name": "api-service", "namespace": "default"}'
```

#### describe_configmap

Get ConfigMap contents and metadata.

| Parameter   | Type   | Description    | Required          |
| ----------- | ------ | -------------- | ----------------- |
| `name`      | string | ConfigMap name | Yes               |
| `namespace` | string | Namespace      | No (uses current) |

**Example**:

```bash
python executor.py --tool describe_configmap --args '{"name": "app-config", "namespace": "default"}'
```

#### describe_secret

Get Secret metadata (values masked for security).

| Parameter   | Type   | Description | Required          |
| ----------- | ------ | ----------- | ----------------- |
| `name`      | string | Secret name | Yes               |
| `namespace` | string | Namespace   | No (uses current) |

**Example**:

```bash
python executor.py --tool describe_secret --args '{"name": "db-credentials", "namespace": "default"}'
```

**Safety**: Secret values are base64-decoded but MASKED. Only keys and metadata shown.

### Troubleshooting (4 tools)

#### get_logs

Retrieve container logs from a pod.

| Parameter   | Type    | Description                       | Default         |
| ----------- | ------- | --------------------------------- | --------------- |
| `name`      | string  | Pod name                          | Required        |
| `namespace` | string  | Namespace                         | current context |
| `container` | string  | Container name                    | first container |
| `tail`      | number  | Number of lines                   | 100             |
| `previous`  | boolean | Get logs from previous container  | false           |
| `since`     | string  | Time duration (e.g., "1h", "30m") | none            |

**Example**:

```bash
python executor.py --tool get_logs --args '{"name": "app-pod", "tail": 50, "since": "1h"}'
```

#### list_events

List recent events in a namespace.

| Parameter        | Type    | Description           | Default         |
| ---------------- | ------- | --------------------- | --------------- |
| `namespace`      | string  | Namespace to query    | current context |
| `limit`          | number  | Number of events      | 50              |
| `all_namespaces` | boolean | All namespaces        | false           |
| `field_selector` | string  | Field selector filter | none            |

**Example**:

```bash
python executor.py --tool list_events --args '{"namespace": "production", "limit": 100}'
```

**Output**: Events sorted by timestamp (most recent first)

#### watch_events

Stream real-time events (30-second window).

| Parameter   | Type   | Description              | Default         |
| ----------- | ------ | ------------------------ | --------------- |
| `namespace` | string | Namespace to watch       | current context |
| `duration`  | number | Watch duration (seconds) | 30              |

**Example**:

```bash
python executor.py --tool watch_events --args '{"namespace": "default", "duration": 60}'
```

**Note**: Automatically terminates after duration to prevent indefinite streaming.

#### exec_pod

Execute read-only commands in a pod (read-only by default).

| Parameter   | Type   | Description        | Required             |
| ----------- | ------ | ------------------ | -------------------- |
| `name`      | string | Pod name           | Yes                  |
| `namespace` | string | Namespace          | No (uses current)    |
| `container` | string | Container name     | No (first container) |
| `command`   | array  | Command to execute | Yes                  |

**Example**:

```bash
python executor.py --tool exec_pod --args '{"name": "app-pod", "command": ["ls", "-la", "/app"]}'
```

**Safety**:

- Destructive commands (rm, dd, mkfs) are BLOCKED
- Write operations require explicit confirmation flag
- Default timeout: 10 seconds

### Management (3 tools)

#### scale_deployment

Scale a deployment to a specific replica count.

| Parameter   | Type   | Description           | Required          |
| ----------- | ------ | --------------------- | ----------------- |
| `name`      | string | Deployment name       | Yes               |
| `replicas`  | number | Desired replica count | Yes               |
| `namespace` | string | Namespace             | No (uses current) |

**Example**:

```bash
python executor.py --tool scale_deployment --args '{"name": "web-app", "replicas": 5, "namespace": "production"}'
```

**Safety**: Requires confirmation for scale operations in production namespaces.

#### rollout_status

Check the rollout status of a deployment.

| Parameter   | Type   | Description     | Required          |
| ----------- | ------ | --------------- | ----------------- |
| `name`      | string | Deployment name | Yes               |
| `namespace` | string | Namespace       | No (uses current) |

**Example**:

```bash
python executor.py --tool rollout_status --args '{"name": "api-server", "namespace": "production"}'
```

#### port_forward

Forward a local port to a pod (for debugging).

| Parameter     | Type   | Description                | Required          |
| ------------- | ------ | -------------------------- | ----------------- |
| `name`        | string | Pod name                   | Yes               |
| `local_port`  | number | Local port                 | Yes               |
| `remote_port` | number | Pod port                   | Yes               |
| `namespace`   | string | Namespace                  | No (uses current) |
| `duration`    | number | Forward duration (seconds) | 60                |

**Example**:

```bash
python executor.py --tool port_forward --args '{"name": "db-pod", "local_port": 5432, "remote_port": 5432, "duration": 300}'
```

**Note**: Port forward automatically terminates after duration.

## Context Management

The skill provides context management tools:

#### get_current_context

Display the current kubectl context.

**Example**:

```bash
python executor.py --tool get_current_context --args '{}'
```

#### switch_context

Switch to a different kubectl context.

| Parameter | Type   | Description  | Required |
| --------- | ------ | ------------ | -------- |
| `context` | string | Context name | Yes      |

**Example**:

```bash
python executor.py --tool switch_context --args '{"context": "production-cluster"}'
```

**Safety**: Prompts for confirmation when switching to production contexts.

#### list_contexts

List all available kubectl contexts.

**Example**:

```bash
python executor.py --tool list_contexts --args '{}'
```

## Common Workflows

### Troubleshoot a Failing Pod

```bash
# 1. List pods to find the problematic one
python executor.py --tool list_pods --args '{"namespace": "production"}'

# 2. Describe the pod for detailed status
python executor.py --tool describe_pod --args '{"name": "app-xyz", "namespace": "production"}'

# 3. Check recent events
python executor.py --tool list_events --args '{"namespace": "production", "limit": 20}'

# 4. Get container logs
python executor.py --tool get_logs --args '{"name": "app-xyz", "namespace": "production", "tail": 200}'
```

### Monitor Deployment Rollout

```bash
# 1. Check deployment status
python executor.py --tool list_deployments --args '{"namespace": "production"}'

# 2. Get rollout status
python executor.py --tool rollout_status --args '{"name": "web-app", "namespace": "production"}'

# 3. Watch for events
python executor.py --tool watch_events --args '{"namespace": "production", "duration": 60}'

# 4. Verify pod readiness
python executor.py --tool list_pods --args '{"namespace": "production", "selector": "app=web-app"}'
```

### Debug Service Connectivity

```bash
# 1. List services
python executor.py --tool list_services --args '{"namespace": "default"}'

# 2. Describe service for endpoint details
python executor.py --tool describe_service --args '{"name": "api-service", "namespace": "default"}'

# 3. Check pods backing the service
python executor.py --tool list_pods --args '{"namespace": "default", "selector": "app=api"}'

# 4. Port forward for local testing
python executor.py --tool port_forward --args '{"name": "api-pod", "local_port": 8080, "remote_port": 8080}'
```

### Investigate ConfigMap/Secret Issues

```bash
# 1. List ConfigMaps
python executor.py --tool list_configmaps --args '{"namespace": "default"}'

# 2. Describe ConfigMap contents
python executor.py --tool describe_configmap --args '{"name": "app-config", "namespace": "default"}'

# 3. List Secrets (names only)
python executor.py --tool list_secrets --args '{"namespace": "default"}'

# 4. Check Secret metadata (values masked)
python executor.py --tool describe_secret --args '{"name": "db-creds", "namespace": "default"}'
```

### Scale Application

```bash
# 1. Check current deployment state
python executor.py --tool list_deployments --args '{"namespace": "production"}'

# 2. Scale deployment
python executor.py --tool scale_deployment --args '{"name": "web-app", "replicas": 10, "namespace": "production"}'

# 3. Monitor rollout
python executor.py --tool rollout_status --args '{"name": "web-app", "namespace": "production"}'

# 4. Verify pod count
python executor.py --tool list_pods --args '{"namespace": "production", "selector": "app=web-app"}'
```

## Configuration

### Environment Variables

| Variable            | Description               | Default          |
| ------------------- | ------------------------- | ---------------- |
| `KUBECONFIG`        | Path to kubeconfig file   | `~/.kube/config` |
| `KUBECTL_CONTEXT`   | Default kubectl context   | current-context  |
| `KUBECTL_NAMESPACE` | Default namespace         | from context     |
| `KUBECTL_TIMEOUT`   | Command timeout (seconds) | 30               |

### Setup

1. **Install kubectl**:

   ```bash
   # macOS
   brew install kubectl

   # Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

   # Windows
   choco install kubernetes-cli
   ```

2. **Configure cluster access**:

   ```bash
   # Verify kubectl is configured
   kubectl cluster-info

   # List available contexts
   kubectl config get-contexts

   # Set default namespace (optional)
   kubectl config set-context --current --namespace=my-namespace
   ```

3. **Verify RBAC permissions**:

   ```bash
   # Check your permissions
   kubectl auth can-i --list

   # Verify read access to pods
   kubectl auth can-i get pods
   ```

4. **Use the skill**:
   ```bash
   python .claude/skills/kubernetes-flux/executor.py --list
   ```

## Safety Features

### Blocked Operations

The following operations are BLOCKED by default to prevent accidental damage:

- **DELETE operations**: `kubectl delete` commands are blocked unless explicitly allowed
- **Destructive exec commands**: `rm`, `dd`, `mkfs`, `sudo` are blocked in exec_pod
- **Secret exposure**: Secret values are always masked in output
- **Production context switching**: Requires confirmation for production/prod namespaces

### Confirmation Required

These operations require explicit confirmation:

- Scaling deployments in production namespaces
- Switching to production contexts
- Exec into pods with write operations
- Port forwarding on privileged ports (< 1024)

### Masked Output

The following data is automatically masked:

- Secret values (base64 decoded but shown as `***MASKED***`)
- Authentication tokens in ConfigMaps
- Database passwords and connection strings
- API keys and credentials

## Error Handling

**Common Errors**:

| Error                         | Cause                         | Fix                                       |
| ----------------------------- | ----------------------------- | ----------------------------------------- |
| `kubectl not found`           | kubectl not installed         | Install kubectl                           |
| `Unable to connect to server` | Cluster unreachable           | Check network, VPN, or cluster status     |
| `Forbidden`                   | Insufficient RBAC permissions | Request cluster admin for permissions     |
| `NotFound`                    | Resource doesn't exist        | Verify name and namespace                 |
| `context deadline exceeded`   | Timeout                       | Increase KUBECTL_TIMEOUT or check cluster |

**Recovery**:

- Check current context: `python executor.py --tool get_current_context`
- Verify cluster connectivity: `kubectl cluster-info`
- Check RBAC permissions: `kubectl auth can-i get pods`
- Review recent events for cluster issues

## Integration with Agents

This skill integrates with the following agents:

### Primary Agents

- **devops**: Infrastructure management, deployments, scaling
- **incident-responder**: Troubleshooting, debugging, post-mortems

### Secondary Agents

- **cloud-integrator**: Cloud-native Kubernetes integrations (GKE, EKS, AKS)
- **developer**: Application deployment and debugging
- **qa**: Integration testing in Kubernetes environments
- **security-architect**: Security audits, RBAC configuration

## Progressive Disclosure

The skill uses progressive disclosure to minimize context usage:

1. **Initial Load**: Only metadata and tool names (~800 tokens)
2. **Tool Invocation**: Specific tool schema loaded on-demand (~100-200 tokens)
3. **Result Streaming**: Large outputs streamed incrementally
4. **Context Cleanup**: Old results cleared after use

**Context Optimization**:

- Use `--tail` to limit log output
- Use `--limit` to restrict event counts
- Use selectors to filter pod/deployment lists
- Prefer specific operations over broad discovery

## Troubleshooting

### Skill Issues

**Executor not found**:

```bash
# Verify Python is installed
python --version

# Check file exists
ls -la .claude/skills/kubernetes-flux/executor.py
```

**kubectl not working**:

```bash
# Verify kubectl installation
kubectl version --client

# Check kubeconfig
kubectl config view

# Test cluster connectivity
kubectl cluster-info
```

**Permission denied**:

```bash
# Check RBAC permissions
kubectl auth can-i get pods
kubectl auth can-i describe deployments

# Contact cluster admin for permissions
```

**Context issues**:

```bash
# List available contexts
python executor.py --tool list_contexts

# Switch context
python executor.py --tool switch_context --args '{"context": "my-cluster"}'

# Verify current context
python executor.py --tool get_current_context
```

## Performance Considerations

- **Large clusters**: Use selectors and namespaces to filter results
- **Log queries**: Use `--tail` and `--since` to limit output
- **Event streaming**: Use `duration` parameter to prevent indefinite watches
- **Port forwarding**: Always set duration to prevent orphaned processes
- **Exec operations**: Set timeout to prevent hanging commands

## Related

- **kubectl Documentation**: https://kubernetes.io/docs/reference/kubectl/
- **Kubernetes API**: https://kubernetes.io/docs/reference/kubernetes-api/
- **MCP Source**: Flux159/mcp-server-kubernetes
- **Cloud Integration**: `.claude/skills/cloud-run/` (GCP Cloud Run)
- **MCP Converter**: `.claude/skills/mcp-converter/`

## Sources

- [mcp-server-kubernetes - GitHub](https://github.com/Flux159/mcp-server-kubernetes)
- [Kubernetes MCP Community](https://github.com/topics/kubernetes-mcp)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/kubectl/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
