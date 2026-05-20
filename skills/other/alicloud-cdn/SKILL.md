---
name: alicloud-cdn
description: Manage Alibaba Cloud CDN using the @alicloud/cdn20180510 TypeScript SDK. Use when working with CDN domain acceleration, domain configuration, SSL certificates, cache refresh/prefetch, real-time monitoring, traffic analysis, log management, usage/billing, IP tools, Function Compute triggers, delivery tasks, and resource tagging. Covers all 168 APIs of the CDN 20180510 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/cdn20180510"
  api-version: "2018-05-10"
---

# Alibaba Cloud CDN Skill

Manage CDN content delivery network via the `@alicloud/cdn20180510` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/cdn20180510 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including endpoints, domain types, source types, function configurations, and time formats.

## Client Initialization

```typescript
import Client from '@alicloud/cdn20180510';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: 'cdn.aliyuncs.com',
}));
```

CDN is a global service — use the single endpoint `cdn.aliyuncs.com` for all operations.

## API Overview (168 APIs in 11 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Domain Management | 31 | addCdnDomain, describeUserDomains, deleteCdnDomain | [references/domain.md](references/domain.md) |
| Domain Configuration | 20 | batchSetCdnDomainConfig, setCdnDomainStagingConfig | [references/domain-config.md](references/domain-config.md) |
| SSL Certificate | 9 | setCdnDomainSSLCertificate, describeCdnCertificateList | [references/certificate.md](references/certificate.md) |
| Cache Refresh & Prefetch | 7 | refreshObjectCaches, pushObjectCache, describeRefreshTasks | [references/cache-refresh.md](references/cache-refresh.md) |
| Monitoring & Statistics | 44 | describeDomainRealTimeQpsData, describeDomainBpsData | [references/monitoring.md](references/monitoring.md) |
| Log Management | 15 | describeCdnDomainLogs, createRealTimeLogDelivery | [references/log.md](references/log.md) |
| Usage & Billing | 15 | describeDomainUsageData, describeCdnUserBillHistory | [references/usage.md](references/usage.md) |
| IP & Network Tools | 10 | describeIpInfo, setCdnFullDomainsBlockIP | [references/ip-tool.md](references/ip-tool.md) |
| Function Compute Trigger | 5 | addFCTrigger, updateFCTrigger, describeFCTrigger | [references/fc-trigger.md](references/fc-trigger.md) |
| Deliver & Report Tasks | 8 | createCdnDeliverTask, describeCdnReport | [references/deliver-task.md](references/deliver-task.md) |
| Tag & Resource | 4 | tagResources, untagResources, listTagResources | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### RPC-Style (Global Service)

CDN APIs do not require `regionId`. Parameters are flat fields in a Request object:

```typescript
import * as models from '@alicloud/cdn20180510/dist/models';

const { body } = await client.describeUserDomains(new models.DescribeUserDomainsRequest({
  pageSize: 50,
  pageNumber: 1,
}));
```

### Domain Configuration via JSON Functions

Use `batchSetCdnDomainConfig` with a JSON `functions` array to configure domain features:

```typescript
await client.batchSetCdnDomainConfig(new models.BatchSetCdnDomainConfigRequest({
  domainNames: 'cdn.example.com',
  functions: JSON.stringify([
    {
      functionName: 'filetype_based_ttl_set',
      functionArgs: [
        { argName: 'ttl', argValue: '2592000' },
        { argName: 'file_type', argValue: 'jpg,png,gif,css,js' },
        { argName: 'weight', argValue: '1' },
      ],
    },
  ]),
}));
```

### Page-Based Pagination

```typescript
let pageNumber = 1;
let all: any[] = [];
while (true) {
  const { body } = await client.describeUserDomains(new models.DescribeUserDomainsRequest({
    pageSize: 50, pageNumber,
  }));
  all.push(...(body.domains?.pageData || []));
  if (all.length >= (body.totalCount || 0)) break;
  pageNumber++;
}
```

### Time Range for Monitoring

Most monitoring APIs accept ISO 8601 time ranges:

```typescript
const { body } = await client.describeDomainRealTimeQpsData(
  new models.DescribeDomainRealTimeQpsDataRequest({
    domainName: 'cdn.example.com',
    startTime: '2026-02-15T00:00:00Z',
    endTime: '2026-02-16T00:00:00Z',
  })
);
```

### Error Handling

```typescript
try {
  await client.addCdnDomain(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Add and Configure CDN Domain

```
addCdnDomain → verifyDomainOwner → setCdnDomainSSLCertificate → batchSetCdnDomainConfig
```

### 2. SSL Certificate Management

```
describeCdnCertificateList → setCdnDomainSSLCertificate → describeCdnDomainCertificateInfo
```

### 3. Cache Refresh & Prefetch

```
refreshObjectCaches (URL/Dir) → pushObjectCache → describeRefreshTasks → describeRefreshQuota
```

### 4. Real-Time Monitoring

```
describeDomainRealTimeQpsData → describeDomainRealTimeBpsData → describeDomainRealTimeHttpCodeData
```

### 5. Traffic Analysis

```
describeDomainTopUrlVisit → describeDomainTopClientIpVisit → describeDomainISPData → describeDomainRegionData
```

### 6. Log Management

```
describeCdnDomainLogs → createRealTimeLogDelivery → describeRealtimeDeliveryAcc
```

### 7. Usage & Billing

```
describeCdnUserBillType → describeDomainUsageData → createUsageDetailDataExportTask
```

### 8. IP Verification & Blocking

```
describeIpInfo → setCdnFullDomainsBlockIP → describeCdnFullDomainsBlockIPHistory
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **Domain CRUD/batch/verification/ownership**: `references/domain.md`
- **Function configs/staging/gray deployment**: `references/domain-config.md`
- **SSL/TLS certificate binding**: `references/certificate.md`
- **URL/directory refresh and prefetch**: `references/cache-refresh.md`
- **Real-time QPS/BPS/hit rate/HTTP codes/traffic**: `references/monitoring.md`
- **Access logs/real-time log delivery**: `references/log.md`
- **Usage data/billing/quota/export**: `references/usage.md`
- **IP check/VIP query/IP blocking**: `references/ip-tool.md`
- **Edge function triggers**: `references/fc-trigger.md`
- **Scheduled delivery/report tasks**: `references/deliver-task.md`
- **Resource tagging**: `references/tag-resource.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Domain listing, adding, and deletion
- Domain configuration (HTTPS force, cache TTL)
- SSL certificate binding
- Cache refresh (URL/directory) and prefetch
- Real-time QPS and bandwidth monitoring
- Top URL analysis
- Log download
- IP verification
- Usage data queries
- Resource tagging
