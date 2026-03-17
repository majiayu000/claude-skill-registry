---
name: aliyun-api-ref
description: Alibaba Cloud API reference for developing aero-cli. Use this skill when adding new cloud provider features, fixing API calls, or extending FC/RDS/Redis/OSS/DNS/VPC integrations. Contains SDK usage patterns, API signatures, and error handling conventions specific to this project.
---

# Alibaba Cloud API Development Reference

## When to use this skill

Use this skill when:
- Adding or modifying Alibaba Cloud API calls in `src/providers/`
- Implementing new cloud service integrations (FC, RDS, Redis, OSS, DNS, VPC)
- Debugging API errors or handling new error codes
- Understanding SDK constructor patterns and authentication flow
- Working with pagination, retry logic, or async polling patterns

## Project Architecture

```
src/providers/       # Cloud service provider modules
  fc.ts              # Function Compute 3.0 (deploy, invoke, versions, aliases)
  infra.ts           # RDS Serverless (database provisioning)
  redis.ts           # Tair/Redis Serverless KV (cache provisioning)
  oss.ts             # Object Storage Service (static site deploy)
  domain.ts          # DNS + FC custom domain binding
  ssl.ts             # Let's Encrypt ACME + FC HTTPS binding
  vpc.ts             # VPC / VSwitch / SecurityGroup management
  logs.ts            # SLS log streaming
src/utils/
  sdk.ts             # Shared SDK constructor resolver + FC client factory
  retry.ts           # Exponential backoff retry wrapper
  config.ts          # Auth (AK/SK) and project config management
  errors.ts          # Error classification (conflict, not-found, etc.)
```

## SDK Usage Patterns

### Constructor Resolution

All Alibaba Cloud SDKs are loaded via `resolveSdkCtor()` to handle ESM/CJS interop:

```typescript
import Vpc, * as $Vpc from '@alicloud/vpc20160428';
import { resolveSdkCtor } from '../utils/sdk';

const VpcClientCtor = resolveSdkCtor<Vpc>(Vpc, '@alicloud/vpc20160428');
```

### Client Instantiation

Each provider creates its client with `@alicloud/openapi-client` Config:

```typescript
import * as $OpenApi from '@alicloud/openapi-client';

const client = new VpcClientCtor(new $OpenApi.Config({
  accessKeyId: auth.ak,
  accessKeySecret: auth.sk,
  regionId,
  endpoint: `vpc.${regionId}.aliyuncs.com`
}));
```

### Shared FC Client

FC client creation is centralized in `utils/sdk.ts`:

```typescript
import { createSharedFcClient } from '../utils/sdk';

const { auth, client } = createSharedFcClient();
// or with explicit auth:
const { client } = createSharedFcClient(authConfig);
```

## Authentication

Credentials are stored in `~/.ali-cli/auth.json` (mode 0o600):

```typescript
interface AuthConfig {
  accountId: string;  // Alibaba Cloud main account ID
  ak: string;         // AccessKey ID
  sk: string;         // AccessKey Secret
  region: string;     // Default region (e.g. cn-hangzhou)
}
```

Access via `Config.requireAuth()` or `Config.getAuth()`.

## Error Handling Conventions

### Error Classification (`utils/errors.ts`)

```typescript
// Check if error is a "resource already exists" conflict
isConflictError(err)  // matches: AlreadyExists, Conflict, Duplicate, Exist

// Format error message for display
formatErrorMessage(err)  // extracts .message from unknown error
```

### Retry Pattern (`utils/retry.ts`)

```typescript
import { withRetry } from '../utils/retry';

const result = await withRetry(
  () => client.someApiCall(request),
  { maxAttempts: 3, baseDelayMs: 1000 }
);
```

Retries on: Throttling, timeout, ECONNRESET, service unavailable.

### Empty Catch Blocks

When intentionally ignoring errors, always add a comment explaining why:

```typescript
} catch { /* role check may fail due to permissions, proceed to create attempt */ }
```

## Pagination Pattern

Use bounded `for` loops with `MAX_PAGES` guard, never `while(true)`:

```typescript
const MAX_PAGES = 50;
for (let page = 0; page < MAX_PAGES; page += 1) {
  const response = await client.listSomething(new ListRequest({
    limit: 100,
    nextToken
  }));
  const rows = response.body?.items || [];
  results.push(...rows);
  nextToken = response.body?.nextToken;
  if (!nextToken || rows.length === 0) break;
}
```

## API Quick Reference

Detailed API tables are in `references/`:

- `references/ref_fc_apis.md` — Function Compute 3.0 (86 APIs, version 2023-03-30)
- `references/ref_rds_apis.md` — RDS instance/database/account management
- `references/ref_redis_apis.md` — Redis/Tair instance management (146 APIs, version 2015-01-01)
- `references/ref_oss_apis.md` — Object Storage bucket/object operations
- `references/ref_dns_apis.md` — Cloud DNS domain/record management (235 APIs, version 2015-01-09)

### Key APIs Used by This Project

| Provider | Primary APIs | SDK Package |
|----------|-------------|-------------|
| FC | CreateFunction, UpdateFunction, InvokeFunction, PublishFunctionVersion, UpdateAlias, CreateCustomDomain | `@alicloud/fc20230330` |
| RDS | CreateDBInstance, DescribeDBInstances, CreateAccount, CreateDatabase, DescribeAvailableZones | `@alicloud/rds20140815` |
| Redis | CreateTairInstance, DescribeInstances, CreateAccount, ResetAccountPassword | `@alicloud/r-kvstore20150101` |
| OSS | putBucket, put (object), list, getBucketInfo | `ali-oss` |
| DNS | AddDomainRecord, UpdateDomainRecord, DeleteDomainRecord, DescribeSubDomainRecords | `@alicloud/alidns20150109` |
| VPC | DescribeVpcs, CreateVSwitch, DescribeVSwitches | `@alicloud/vpc20160428` |
| ECS | CreateSecurityGroup, AuthorizeSecurityGroup | `@alicloud/ecs20140526` |
| SLS | GetLogs | `@alicloud/sls20201230` |

## Provider Implementation Checklist

When adding a new provider or extending an existing one:

1. Use `resolveSdkCtor()` for SDK constructor resolution
2. Create client with proper `endpoint`, `connectTimeout`, `readTimeout`
3. Use `withRetry()` for API calls that may face transient failures
4. Use bounded pagination (never `while(true)`)
5. Classify errors with `isConflictError()` where applicable
6. Add comments to any intentionally empty catch blocks
7. Store sensitive outputs (passwords, connection strings) in `project.envs`
8. Mask credentials in CLI output via `maskConnectionString()`
