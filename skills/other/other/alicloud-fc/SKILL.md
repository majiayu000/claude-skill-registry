---
name: alicloud-fc
description: Manage Alibaba Cloud Function Compute (FC) 3.0 using the @alicloud/fc20230330 TypeScript SDK. Use when working with serverless functions on Alibaba Cloud, including function CRUD, invocation, versions, aliases, triggers (HTTP/Timer/OSS/CDN/MNS), async invocation, concurrency and scaling configs, provisioned instances, custom domains, layers, VPC bindings, sessions, and resource tagging. Covers all 67 APIs of the FC 20230330 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/fc20230330"
  api-version: "2023-03-30"
---

# Alibaba Cloud Function Compute (FC) 3.0 Skill

Manage serverless functions, triggers, aliases, layers, custom domains, scaling, and async invocations via the `@alicloud/fc20230330` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/fc20230330 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
export ALIBABA_CLOUD_REGION_ID="cn-hangzhou"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including regions, runtimes, error handling, and pagination.

## Client Initialization

```typescript
import Client from '@alicloud/fc20230330';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  regionId: 'cn-hangzhou',
  endpoint: 'cn-hangzhou.fc.aliyuncs.com',
}));
```

## API Overview (67 APIs in 10 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Function | 12 | createFunction, getFunction, invokeFunction, publishFunctionVersion | [references/function.md](references/function.md) |
| Alias | 5 | createAlias, updateAlias, listAliases | [references/alias.md](references/alias.md) |
| Trigger | 5 | createTrigger, getTrigger, listTriggers | [references/trigger.md](references/trigger.md) |
| Async Invocation | 7 | putAsyncInvokeConfig, listAsyncTasks, stopAsyncTask | [references/async.md](references/async.md) |
| Concurrency & Scaling | 12 | putConcurrencyConfig, putScalingConfig, putProvisionConfig | [references/concurrency-scaling.md](references/concurrency-scaling.md) |
| Custom Domain | 5 | createCustomDomain, updateCustomDomain, listCustomDomains | [references/custom-domain.md](references/custom-domain.md) |
| Layer | 7 | createLayerVersion, listLayers, putLayerACL | [references/layer.md](references/layer.md) |
| Instance & Session | 6 | listInstances, createSession, listSessions | [references/instance-session.md](references/instance-session.md) |
| VPC Binding | 3 | createVpcBinding, listVpcBindings | [references/vpc.md](references/vpc.md) |
| Tag & Resource | 5 | tagResources, listTagResources, describeRegions | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### RESTful Path Parameters

FC 3.0 uses RESTful style. Path parameters (e.g., `functionName`) are direct method arguments:

```typescript
// getFunction(functionName, request)
const { body } = await client.getFunction('my-func', { qualifier: 'LATEST' });

// deleteAlias(functionName, aliasName)
await client.deleteAlias('my-func', 'staging');
```

### Body Input Pattern

Create/Update APIs pass structured data via `body`:

```typescript
await client.createFunction({
  body: {
    functionName: 'hello',
    runtime: 'nodejs18',
    handler: 'index.handler',
    memorySize: 512,
    timeout: 60,
    code: { zipFile: base64Zip },
  },
});
```

### Cursor-Based Pagination

List APIs use `nextToken` + `limit` (not `pageNo`/`pageSize`):

```typescript
let nextToken: string | undefined;
let all: any[] = [];
do {
  const { body } = await client.listFunctions({ limit: 100, nextToken });
  all.push(...(body.functions || []));
  nextToken = body.nextToken;
} while (nextToken);
```

### Error Handling

```typescript
try {
  await client.getFunction('my-func', {});
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Deploy Function

```
createFunction → invokeFunction → publishFunctionVersion → createAlias
```

### 2. Event-Driven Trigger

```
createFunction → createTrigger (HTTP/Timer/OSS/CDN)
```

### 3. Blue-Green / Canary Deployment

```
updateFunction → publishFunctionVersion → updateAlias (additionalVersionWeight)
```

### 4. Async with Dead Letter Queue

```
putAsyncInvokeConfig (destinationConfig) → invokeFunction → listAsyncTasks
```

### 5. Provisioned Instances

```
putProvisionConfig → getProvisionConfig → listInstances
```

### 6. Custom Domain + HTTPS

```
createCustomDomain (routeConfig, certConfig) → getCustomDomain
```

### 7. Layer Management

```
createLayerVersion → updateFunction (layers) → putLayerACL
```

### 8. Scaling Configuration

```
putScalingConfig → putConcurrencyConfig → getScalingConfig
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **Function CRUD/Invoke/Versions**: `references/function.md`
- **Alias CRUD**: `references/alias.md`
- **Trigger CRUD**: `references/trigger.md`
- **Async Config/Tasks**: `references/async.md`
- **Concurrency/Scaling/Provision**: `references/concurrency-scaling.md`
- **Custom Domain**: `references/custom-domain.md`
- **Layer Versions/ACL**: `references/layer.md`
- **Instances/Sessions**: `references/instance-session.md`
- **VPC Bindings**: `references/vpc.md`
- **Tags/Resource Group/Regions**: `references/tag-resource.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Function creation, listing, and invocation
- Version publishing and alias-based canary deployment
- HTTP and Timer trigger creation
- Async invocation configuration
- Provisioned instance setup
- Layer creation and listing
- Custom domain binding
- Scaling and concurrency configuration
