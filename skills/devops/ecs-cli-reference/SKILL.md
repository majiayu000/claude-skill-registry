---
name: ecs-cli-reference
description: AWS CLI ECS command reference. Use when understanding how users interact with ECS via AWS CLI, including command syntax, options, examples, and output formats. Essential for KECS compatibility.
allowed-tools: Read, Grep, Glob
---

# AWS CLI ECS Command Reference

This skill provides comprehensive AWS CLI ECS command specifications to ensure KECS compatibility with user expectations when using `aws ecs` commands.

## Overview

AWS CLI ECS commands allow users to interact with Amazon ECS services. KECS emulates these APIs, so understanding CLI behavior is crucial for compatibility.

### Global CLI Options

All ECS commands support these global options:

| Option | Description |
|--------|-------------|
| `--region` | AWS region to use |
| `--profile` | Named credential profile |
| `--output` | Output format: `json`, `text`, `table`, `yaml`, `yaml-stream` |
| `--query` | JMESPath filter for response |
| `--endpoint-url` | Override service endpoint (critical for KECS) |
| `--debug` | Enable debug logging |
| `--no-verify-ssl` | Disable SSL verification |
| `--no-paginate` | Disable automatic pagination |

### Pagination Options

For paginated operations:
- `--max-items`: Total items to return
- `--page-size`: Items per API call
- `--starting-token`: Resume from previous response

### Input Options

- `--cli-input-json`: Read arguments from JSON
- `--cli-input-yaml`: Read arguments from YAML
- `--generate-cli-skeleton`: Print request skeleton

## Command Categories

### Core Resources
- **Cluster Commands**: create-cluster, describe-clusters, list-clusters, delete-cluster, update-cluster
- **Service Commands**: create-service, describe-services, list-services, update-service, delete-service
- **Task Commands**: run-task, stop-task, describe-tasks, list-tasks, execute-command
- **Task Definition Commands**: register-task-definition, deregister-task-definition, describe-task-definition, list-task-definitions, list-task-definition-families

### Advanced Features
- **TaskSet Commands**: create-task-set, describe-task-sets, update-task-set, delete-task-set
- **Capacity Provider Commands**: create-capacity-provider, describe-capacity-providers, update-capacity-provider, delete-capacity-provider, put-cluster-capacity-providers
- **Attribute Commands**: put-attributes, list-attributes, delete-attributes
- **Tag Commands**: tag-resource, untag-resource, list-tags-for-resource
- **Account Settings**: put-account-setting, put-account-setting-default, list-account-settings, delete-account-setting

## KECS-Specific Usage

When using AWS CLI with KECS:

```bash
# Point to KECS endpoint
export AWS_ENDPOINT_URL=http://localhost:8080

# Or per-command
aws ecs list-clusters --endpoint-url http://localhost:8080

# With custom kubeconfig
export KUBECONFIG=/tmp/kecs-instance.config
aws ecs describe-clusters --cluster default
```

## Support Files

- `cluster-commands.md`: Cluster lifecycle commands
- `service-commands.md`: Service management commands
- `task-commands.md`: Task execution and management
- `task-definition-commands.md`: Task definition registration
- `other-commands.md`: Tags, attributes, account settings, capacity providers, task sets
