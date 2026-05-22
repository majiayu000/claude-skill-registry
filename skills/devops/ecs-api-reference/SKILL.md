---
name: ecs-api-reference
description: Amazon ECS API specification reference. Use when implementing ECS-compatible APIs in KECS to accurately reproduce request/response structures, parameters, error codes, and behaviors. Reference for implementing APIs like CreateCluster, CreateService, RunTask, RegisterTaskDefinition.
allowed-tools: Read, Grep, Glob
---

# Amazon ECS API Reference for KECS

Reference skill for implementing ECS-compatible APIs in KECS.

## Overview

This skill provides detailed specifications for the following ECS API categories:

1. **Cluster API** - Cluster management (`cluster-api.md`)
2. **Service API** - Service management (`service-api.md`)
3. **Task API** - Task execution and management (`task-api.md`)
4. **Task Definition API** - Task definition management (`task-definition-api.md`)
5. **Other APIs** - Tags, TaskSets, Attributes, Account Settings, etc. (`other-apis.md`)

## Use Cases

- Implementing new ECS API endpoints
- Verifying request/response structures of existing APIs
- Aligning error codes and behaviors with AWS ECS
- Writing API compatibility tests

## Common API Specifications

### HTTP Request Format
```
POST / HTTP/1.1
Host: ecs.{region}.amazonaws.com
Content-Type: application/x-amz-json-1.1
X-Amz-Target: AmazonEC2ContainerServiceV20141113.{ActionName}
```

### Common Error Codes
| Error | HTTP | Description |
|-------|------|-------------|
| ClientException | 400 | Client-side error (insufficient permissions, invalid ID, etc.) |
| InvalidParameterException | 400 | Invalid parameter |
| ServerException | 500 | Server error |
| ClusterNotFoundException | 400 | Cluster not found |
| ServiceNotFoundException | 400 | Service not found |

### Tag Limits
- Maximum 50 tags per resource
- Key length: Maximum 128 characters (UTF-8)
- Value length: Maximum 256 characters (UTF-8)
- `aws:` prefix is reserved (cannot edit or delete)

### Pagination
- maxResults: 1-100 (default 10 or 100 depending on API)
- nextToken: Opaque continuation token

### ARN Format
```
arn:aws:ecs:{region}:{account}:{resource-type}/{resource-id}
```
Resource types: cluster, service, task, task-definition, container-instance, capacity-provider, task-set

## Detailed Specifications

Refer to the following support files for detailed API specifications:

- `cluster-api.md` - CreateCluster, DescribeClusters, ListClusters, DeleteCluster, UpdateCluster
- `service-api.md` - CreateService, DescribeServices, UpdateService, DeleteService, ListServices
- `task-api.md` - RunTask, StopTask, DescribeTasks, ListTasks, ExecuteCommand
- `task-definition-api.md` - RegisterTaskDefinition, DeregisterTaskDefinition, DescribeTaskDefinition, ListTaskDefinitions
- `other-apis.md` - TagResource, ListTagsForResource, CreateTaskSet, PutAttributes, PutAccountSetting, etc.
