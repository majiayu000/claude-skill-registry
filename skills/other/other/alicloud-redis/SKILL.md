---
name: alicloud-redis
description: Manage Alibaba Cloud Redis (Tair / R-KVStore) using the @alicloud/r-kvstore20150101 TypeScript SDK. Use when working with Redis or Tair instances, accounts, backups, security (whitelist/SSL/TDE/audit), parameters, monitoring, cluster scaling, direct connection, Tair Custom instances, and resource tagging. Covers all 157 APIs of the R-KVStore 20150101 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/r-kvstore20150101"
  api-version: "2015-01-01"
---

# Alibaba Cloud Redis (R-KVStore) Skill

Manage Redis and Tair instances via the `@alicloud/r-kvstore20150101` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/r-kvstore20150101 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including endpoints, instance types, architectures, Redis versions, pagination, and async polling.

## Client Initialization

```typescript
import Client from '@alicloud/r-kvstore20150101';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: 'r-kvstore.aliyuncs.com',
  regionId: 'cn-hangzhou',
}));
```

## API Overview (157 APIs in 8 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Instance Management | 82 | createInstance, describeInstances, modifyInstanceSpec | [references/instance.md](references/instance.md) |
| Account Management | 7 | createAccount, grantAccountPrivilege, resetAccountPassword | [references/account.md](references/account.md) |
| Backup & Recovery | 11 | createBackup, describeBackups, modifyBackupPolicy, restoreInstance | [references/backup.md](references/backup.md) |
| Security & Encryption | 23 | modifySecurityIps, modifyInstanceSSL, modifyInstanceTDE, modifyAuditLogConfig | [references/security.md](references/security.md) |
| Parameter Management | 11 | describeParameters, createParameterGroup, modifyInstanceParameter | [references/parameter.md](references/parameter.md) |
| Monitoring & Performance | 8 | describeHistoryMonitorValues, describeSlowLogRecords | [references/monitoring.md](references/monitoring.md) |
| Tair Custom Instance | 12 | createTairKVCacheCustomInstance, describeTairKVCacheCustomInstances | [references/tair-custom.md](references/tair-custom.md) |
| Tag & Resource | 5 | tagResources, untagResources, listTagResources | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### RPC-Style with instanceId

Most APIs require `instanceId` as the primary identifier:

```typescript
import * as models from '@alicloud/r-kvstore20150101/dist/models';

const { body } = await client.describeInstanceAttribute(
  new models.DescribeInstanceAttributeRequest({
    instanceId: 'r-bp1xxxxxxxxxxxxx',
  })
);
```

### Page-Based Pagination

```typescript
let pageNumber = 1;
let all: any[] = [];
while (true) {
  const { body } = await client.describeInstances(new models.DescribeInstancesRequest({
    regionId: 'cn-hangzhou', pageSize: 50, pageNumber,
  }));
  all.push(...(body.instances?.KVStoreInstance || []));
  if (all.length >= (body.totalCount || 0)) break;
  pageNumber++;
}
```

### Async Operation Polling

Many operations are async — poll instance status until target state:

```typescript
while (true) {
  const { body } = await client.describeInstanceAttribute(
    new models.DescribeInstanceAttributeRequest({ instanceId })
  );
  const status = body.instances?.DBInstanceAttribute?.[0]?.instanceStatus;
  if (status === 'Normal') break;
  await new Promise(r => setTimeout(r, 5000));
}
```

### Multi-Type Support

R-KVStore supports Redis Community and Tair (DRAM/Persistent Memory/ESSD):

```typescript
// Redis Community
const { body: redis } = await client.createInstance(new models.CreateInstanceRequest({
  regionId: 'cn-hangzhou', instanceType: 'Redis', engineVersion: '7.0',
  instanceClass: 'redis.master.small.default', chargeType: 'PostPaid',
  password: process.env.REDIS_PASSWORD!, vpcId: 'vpc-xxx', vSwitchId: 'vsw-xxx',
}));

// Tair (Enhanced Redis)
const { body: tair } = await client.createTairInstance(new models.CreateTairInstanceRequest({
  regionId: 'cn-hangzhou', instanceType: 'tair_rdb',
  instanceClass: 'tair.rdb.2g', chargeType: 'PostPaid',
  password: process.env.REDIS_PASSWORD!, vpcId: 'vpc-xxx', vSwitchId: 'vsw-xxx',
}));
```

### Config as JSON String

Instance configuration is passed as a JSON string:

```typescript
await client.modifyInstanceConfig(new models.ModifyInstanceConfigRequest({
  instanceId,
  config: JSON.stringify({
    'maxmemory-policy': 'allkeys-lru',
    'timeout': '300',
  }),
}));
```

### Error Handling

```typescript
try {
  await client.createInstance(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Create Redis Instance with Account

```
createInstance → waitForNormal → createAccount → modifySecurityIps
```

### 2. Create Tair Cluster

```
createTairInstance → waitForNormal → describeClusterMemberInfo
```

### 3. Backup and Recovery

```
modifyBackupPolicy → createBackup → describeBackups → restoreInstance
```

### 4. Security Hardening

```
modifySecurityIps → modifyInstanceSSL → modifyInstanceTDE → modifyAuditLogConfig
```

### 5. Cluster Scaling

```
describeClusterMemberInfo → addShardingNode / deleteShardingNode
```

### 6. Direct Connection Mode

```
allocateDirectConnection → describeDBInstanceNetInfo → releaseDirectConnection
```

### 7. Parameter Tuning

```
describeParameterTemplates → createParameterGroup → modifyInstanceParameter
```

### 8. Performance Monitoring

```
describeMonitorItems → describeHistoryMonitorValues → describeSlowLogRecords → createCacheAnalysisTask
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **Instance CRUD/lifecycle/spec/network/cluster/proxy**: `references/instance.md`
- **Account CRUD/password/privileges**: `references/account.md`
- **Backup/restore/cache analysis**: `references/backup.md`
- **IP whitelist/SSL/TDE/audit/global whitelist**: `references/security.md`
- **Parameters/parameter groups/templates**: `references/parameter.md`
- **Performance monitoring/slow logs/running logs**: `references/monitoring.md`
- **TairKVCache custom instances**: `references/tair-custom.md`
- **Resource tagging**: `references/tag-resource.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Instance listing, creation, and deletion
- Account management
- Backup creation and listing
- IP whitelist and SSL configuration
- Audit log management
- Performance monitoring and slow log analysis
- Parameter management
- Resource tagging
