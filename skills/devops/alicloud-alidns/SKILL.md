---
name: alicloud-alidns
description: Manage Alibaba Cloud DNS (Alidns) using the @alicloud/alidns20150109 TypeScript SDK. Use when working with DNS resolution on Alibaba Cloud, including domain management, DNS record CRUD (A, AAAA, CNAME, MX, TXT, SRV, CAA, etc.), DNS load balancing (DNSSLB), custom resolution lines, DNSSEC, domain groups, batch operations, Cloud GTM (Global Traffic Manager), DNS GTM, GTM Classic, recursive DNS, DNS cache, Public DNS (PDNS), DNS over HTTPS (DoH), ISP cache flush, domain statistics, and resource tagging. Covers all 234 APIs of the Alidns 20150109 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/alidns20150109"
  api-version: "2015-01-09"
---

# Alibaba Cloud DNS (Alidns) Skill

Manage DNS domains, records, traffic management, and resolution services via the `@alicloud/alidns20150109` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/alidns20150109 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including endpoints, record types, line values, and TTL.

## Client Initialization

```typescript
import Client from '@alicloud/alidns20150109';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: 'alidns.cn-hangzhou.aliyuncs.com',
}));
```

## API Overview (234 APIs in 13 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Domain Management | 39 | addDomain, describeDomains, describeDomainInfo, operateBatchDomain | [references/domain.md](references/domain.md) |
| DNS Records | 14 | addDomainRecord, updateDomainRecord, describeDomainRecords | [references/record.md](references/record.md) |
| DNSSLB | 3 | setDNSSLBStatus, updateDNSSLBWeight | [references/dnsslb.md](references/dnsslb.md) |
| Custom Lines | 6 | addCustomLine, describeSupportLines | [references/custom-line.md](references/custom-line.md) |
| Cloud GTM | 50 | createCloudGtmAddress, listCloudGtmInstances | [references/cloud-gtm.md](references/cloud-gtm.md) |
| DNS GTM | 28 | addDnsGtmAccessStrategy, describeDnsGtmInstances | [references/dns-gtm.md](references/dns-gtm.md) |
| GTM Classic | 35 | addGtmAccessStrategy, describeGtmInstances | [references/gtm-classic.md](references/gtm-classic.md) |
| Recursion DNS | 18 | addRecursionRecord, listRecursionZones | [references/recursion.md](references/recursion.md) |
| DNS Cache | 5 | addDnsCacheDomain, describeDnsCacheDomains | [references/dns-cache.md](references/dns-cache.md) |
| Public DNS | 18 | createPdnsAppKey, describePdnsThreatStatistics | [references/pdns.md](references/pdns.md) |
| DoH | 6 | describeDohAccountStatistics, describeDohDomainStatistics | [references/doh.md](references/doh.md) |
| ISP Cache Flush | 6 | submitIspFlushCacheTask, describeIspFlushCacheTasks | [references/isp-flush.md](references/isp-flush.md) |
| Tag & Resource | 6 | tagResources, untagResources, describeTags | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### Global Service (No regionId Required)

Unlike ECS/FC, Alidns is a global service. Most APIs do not require `regionId`:

```typescript
import * as models from '@alicloud/alidns20150109/dist/models';

// No regionId needed
const { body } = await client.describeDomains(new models.DescribeDomainsRequest({
  pageSize: 100,
  pageNumber: 1,
}));
```

### Record CRUD

DNS records are identified by `recordId` (returned on creation):

```typescript
// Add record
const { body } = await client.addDomainRecord(new models.AddDomainRecordRequest({
  domainName: 'example.com',
  RR: 'www',           // Subdomain prefix (@ for root)
  type: 'A',           // A, AAAA, CNAME, MX, TXT, NS, SRV, CAA
  value: '1.2.3.4',    // Record value
  TTL: 600,            // Time to live in seconds
  line: 'default',     // Resolution line
}));
const recordId = body.recordId;

// Update record
await client.updateDomainRecord(new models.UpdateDomainRecordRequest({
  recordId, RR: 'www', type: 'A', value: '5.6.7.8', TTL: 300,
}));

// Delete record
await client.deleteDomainRecord(new models.DeleteDomainRecordRequest({ recordId }));
```

### Page-Based Pagination

Most Describe APIs use `pageNumber` + `pageSize`:

```typescript
let pageNumber = 1;
let all: any[] = [];
while (true) {
  const { body } = await client.describeDomainRecords(new models.DescribeDomainRecordsRequest({
    domainName: 'example.com', pageSize: 500, pageNumber,
  }));
  all.push(...(body.domainRecords?.record || []));
  if (all.length >= (body.totalCount || 0)) break;
  pageNumber++;
}
```

### Error Handling

```typescript
try {
  await client.addDomainRecord(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Add Domain & Records

```
addDomain → addDomainRecord (A/CNAME/MX) → describeDomainRecords
```

### 2. Update & Delete Records

```
describeDomainRecords → updateDomainRecord → setDomainRecordStatus → deleteDomainRecord
```

### 3. DNS Load Balancing

```
addDomainRecord (multiple A) → setDNSSLBStatus → updateDNSSLBWeight → describeDNSSLBSubDomains
```

### 4. Domain Groups

```
addDomainGroup → changeDomainGroup → describeDomainGroups
```

### 5. Enable DNSSEC

```
setDomainDnssecStatus → describeDomainDnssecInfo → add DS at registrar
```

### 6. Custom Lines

```
addCustomLine → addDomainRecord (with line) → describeCustomLines
```

### 7. Batch Operations

```
operateBatchDomain → describeBatchResultCount → describeBatchResultDetail
```

### 8. DNS Statistics

```
describeDomainStatistics → describeRecordStatistics → describeDomainLogs
```

### 9. ISP Cache Flush

```
describeIspFlushCacheRemainQuota → submitIspFlushCacheTask → describeIspFlushCacheTasks
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **Domain CRUD/groups/DNSSEC/batch/stats**: `references/domain.md`
- **DNS record add/update/delete/query**: `references/record.md`
- **DNS load balancing**: `references/dnsslb.md`
- **Custom/ISP resolution lines**: `references/custom-line.md`
- **Cloud GTM instances/configs/pools/monitors**: `references/cloud-gtm.md`
- **DNS GTM strategies/pools/monitors**: `references/dns-gtm.md`
- **GTM Classic strategies/pools/recovery**: `references/gtm-classic.md`
- **Recursive DNS zones/records**: `references/recursion.md`
- **DNS cache domains**: `references/dns-cache.md`
- **Public DNS service/threats/stats**: `references/pdns.md`
- **DNS over HTTPS stats**: `references/doh.md`
- **ISP cache flush tasks**: `references/isp-flush.md`
- **Tags/resources/logs**: `references/tag-resource.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Domain listing, adding, and deletion
- DNS record CRUD with all record types
- DNSSLB enable and weight configuration
- Domain group management
- DNSSEC enable and info retrieval
- Domain statistics queries
- Resource tagging
