---
name: alicloud-cr
description: Manage Alibaba Cloud Container Registry (ACR) Enterprise Edition using the @alicloud/cr20181201 TypeScript SDK. Use when working with container image registries on Alibaba Cloud, including instance management, namespaces, image repositories, image tags, build rules, image synchronization, security scanning, delivery chains, Helm charts, artifact lifecycle, and event notifications. Covers all 115 APIs of the CR 20181201 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/cr20181201"
  api-version: "2018-12-01"
---

# Alibaba Cloud Container Registry (ACR) Skill

Manage Alibaba Cloud Container Registry Enterprise Edition instances, namespaces, repositories, images, builds, sync, security scanning, delivery chains, and Helm charts via the `@alicloud/cr20181201` TypeScript SDK.

## Prerequisites

Install the SDK and configure credentials before calling any API:

```bash
npm install @alicloud/cr20181201 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
export ALIBABA_CLOUD_REGION_ID="cn-hangzhou"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup details including regions, error handling, and pagination.

## Client Initialization

```typescript
import Client from '@alicloud/cr20181201';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  regionId: 'cn-hangzhou',
  endpoint: 'cr.cn-hangzhou.aliyuncs.com',
}));
```

## API Overview (115 APIs in 12 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Instance | 16 | listInstance, getInstance, getInstanceUsage, getAuthorizationToken | [references/instance.md](references/instance.md) |
| Namespace | 5 | createNamespace, listNamespace, deleteNamespace | [references/namespace.md](references/namespace.md) |
| Repository | 12 | createRepository, listRepository, getRepository, createRepoTrigger | [references/repository.md](references/repository.md) |
| Image Tag | 4 | createRepoTag, listRepoTag, deleteRepoTag | [references/image-tag.md](references/image-tag.md) |
| Build | 11 | createRepoBuildRule, listRepoBuildRecord, getRepoBuildRecordStatus | [references/build.md](references/build.md) |
| Sync | 8 | createRepoSyncRule, createRepoSyncTask, listRepoSyncTask | [references/sync.md](references/sync.md) |
| Security | 11 | createRepoTagScanTask, listRepoTagScanResult, createScanRule | [references/security.md](references/security.md) |
| Artifact | 19 | createArtifactBuildRule, createArtifactLifecycleRule, createArtifactSubscriptionRule | [references/artifact.md](references/artifact.md) |
| Delivery Chain | 6 | createChain, listChain, listChainInstance | [references/chain.md](references/chain.md) |
| Helm Chart | 12 | createChartNamespace, createChartRepository, listChartRelease | [references/chart.md](references/chart.md) |
| Event Center | 4 | updateEventCenterRule, listEventCenterRecord | [references/event.md](references/event.md) |
| Tag & Resource | 7 | tagResources, listTagResources, createStorageDomainRoutingRule | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### Almost All APIs Require `instanceId`

Get it first via `listInstance`:

```typescript
const { body } = await client.listInstance({ pageNo: 1, pageSize: 30 });
const instanceId = body.instances?.[0]?.instanceId;
```

### Pagination

List APIs use `pageNo` + `pageSize`. Loop until results are fewer than `pageSize`:

```typescript
let page = 1, all: any[] = [];
while (true) {
  const { body } = await client.listRepository({ instanceId, pageNo: page, pageSize: 30 });
  all.push(...(body.repositories || []));
  if (!body.repositories || body.repositories.length < 30) break;
  page++;
}
```

### Error Handling

```typescript
try {
  await client.someApi(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Create Repository

```
listInstance → createNamespace → createRepository
```

### 2. Cross-Region Sync

```
createRepoSyncRule → createRepoSyncTask → getRepoSyncTask (poll)
```

### 3. Security Scan

```
createRepoTagScanTask → getRepoTagScanStatus (poll) → listRepoTagScanResult
```

### 4. Auto-Build from Git

```
createRepoSourceCodeRepo → createRepoBuildRule → (push triggers build)
```

### 5. Artifact Lifecycle

```
createArtifactLifecycleRule → listArtifactLifecycleRule
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

When you need parameter details for a specific API, load the corresponding reference file:

- **Instance/Auth/Endpoint**: `references/instance.md`
- **Namespace CRUD**: `references/namespace.md`
- **Repository/Trigger/SourceCode**: `references/repository.md`
- **Image Tags**: `references/image-tag.md`
- **Build Rules/Records/Logs**: `references/build.md`
- **Sync Rules/Tasks**: `references/sync.md`
- **Scan Rules/Tasks/Results**: `references/security.md`
- **Artifact Build/Lifecycle/Subscription**: `references/artifact.md`
- **Delivery Chain**: `references/chain.md`
- **Helm Chart Namespace/Repo/Release**: `references/chart.md`
- **Event Rules/Records**: `references/event.md`
- **Tags/Storage Routing**: `references/tag-resource.md`

Each reference file contains per-API documentation with parameter tables (name, type, required, description, example).

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Instance listing and usage queries
- Namespace and repository creation
- Image tag listing and deletion
- Security scan triggering and result retrieval
- Cross-region sync rule creation
- Build rule configuration
- Helm chart repository listing
