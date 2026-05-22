---
name: alicloud-rds
description: Manage Alibaba Cloud RDS using the @alicloud/rds20140815 TypeScript SDK. Use when working with relational database instances (MySQL, PostgreSQL, SQL Server, MariaDB), accounts, databases, backups, security, monitoring, parameters, read-only instances, database proxy, migration, cross-region DR, PostgreSQL extensions, RDS Custom instances, and resource tagging. Covers all 398 APIs of the RDS 20140815 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/rds20140815"
  api-version: "2014-08-15"
---

# Alibaba Cloud RDS Skill

Manage RDS relational database service via the `@alicloud/rds20140815` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/rds20140815 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including endpoints, database engines, instance categories, charge types, pagination, and async polling.

## Client Initialization

```typescript
import Client from '@alicloud/rds20140815';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: 'rds.aliyuncs.com',
  regionId: 'cn-hangzhou',
}));
```

## API Overview (398 APIs in 12 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Instance Management | 117 | createDBInstance, describeDBInstances, modifyDBInstanceSpec | [references/instance.md](references/instance.md) |
| Read-Only & Proxy | 19 | createReadOnlyDBInstance, createDBProxy, allocateReadWriteSplittingConnection | [references/readonly.md](references/readonly.md) |
| Account Management | 18 | createAccount, grantAccountPrivilege, resetAccountPassword | [references/account.md](references/account.md) |
| Database Management | 10 | createDatabase, deleteDatabase, describeDatabases | [references/database.md](references/database.md) |
| Backup & Recovery | 31 | createBackup, modifyBackupPolicy, restoreTable, createDdrInstance | [references/backup.md](references/backup.md) |
| Security & Network | 36 | modifySecurityIps, modifyDBInstanceSSL, modifyDBInstanceTDE | [references/security.md](references/security.md) |
| Monitoring & Diagnostics | 29 | describeDBInstancePerformance, describeSlowLogRecords | [references/monitoring.md](references/monitoring.md) |
| Parameter Management | 19 | modifyParameter, createParameterGroup, describeHistoryEvents | [references/parameter.md](references/parameter.md) |
| Migration & Import/Export | 24 | createMigrateTask, createCloudMigrationTask, createGADInstance | [references/migration.md](references/migration.md) |
| PostgreSQL Extensions | 32 | updatePostgresExtensions, upgradeDBInstanceMajorVersion | [references/postgres-ext.md](references/postgres-ext.md) |
| RDS Custom (RC) Instance | 76 | runRCInstances, createRCDisk, createRCSecurityGroup | [references/rc-instance.md](references/rc-instance.md) |
| Tag & Resource | 8 | tagResources, untagResources, modifyResourceGroup | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### RPC-Style with DBInstanceId

Most APIs require `DBInstanceId` as the primary identifier:

```typescript
import * as models from '@alicloud/rds20140815/dist/models';

const { body } = await client.describeDBInstanceAttribute(
  new models.DescribeDBInstanceAttributeRequest({
    DBInstanceId: 'rm-bp1xxxxxxxxxxxxx',
  })
);
```

### Page-Based Pagination

```typescript
let pageNumber = 1;
let all: any[] = [];
while (true) {
  const { body } = await client.describeDBInstances(new models.DescribeDBInstancesRequest({
    regionId: 'cn-hangzhou', pageSize: 100, pageNumber,
  }));
  all.push(...(body.items?.DBInstance || []));
  if (all.length >= (body.totalRecordCount || 0)) break;
  pageNumber++;
}
```

### Async Operation Polling

Many operations are async — poll instance status until target state:

```typescript
while (true) {
  const { body } = await client.describeDBInstanceAttribute(
    new models.DescribeDBInstanceAttributeRequest({ DBInstanceId: instanceId })
  );
  const status = body.items?.DBInstanceAttribute?.[0]?.DBInstanceStatus;
  if (status === 'Running') break;
  await new Promise(r => setTimeout(r, 10000));
}
```

### Multi-Engine Support

RDS supports MySQL, PostgreSQL, SQL Server, and MariaDB. Specify engine at creation:

```typescript
const { body } = await client.createDBInstance(new models.CreateDBInstanceRequest({
  regionId: 'cn-hangzhou',
  engine: 'MySQL',       // MySQL | PostgreSQL | SQLServer | MariaDB
  engineVersion: '8.0',
  DBInstanceClass: 'mysql.n2m.small.2c',
  DBInstanceStorage: 20,
  DBInstanceNetType: 'Intranet',
  payType: 'Postpaid',
  securityIPList: '10.0.0.0/8', // WARNING: never use 0.0.0.0/0 in production
  DBInstanceStorageType: 'cloud_essd',
}));
```

### Error Handling

```typescript
try {
  await client.createDBInstance(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Create Instance with Account and Database

```
createDBInstance → waitForRunning → createAccount → createDatabase → grantAccountPrivilege → modifySecurityIps
```

### 2. Read-Only Instance with Database Proxy

```
createReadOnlyDBInstance → createDBProxy → allocateReadWriteSplittingConnection
```

### 3. Backup and Point-in-Time Recovery

```
modifyBackupPolicy → createBackup → describeBackups → restoreTable
```

### 4. Cross-Region Disaster Recovery

```
modifyInstanceCrossBackupPolicy → describeCrossRegionBackups → createDdrInstance
```

### 5. Security Hardening

```
modifySecurityIps → modifyDBInstanceSSL → modifyDBInstanceTDE → modifySQLCollectorPolicy
```

### 6. Parameter Tuning

```
describeParameterTemplates → describeParameters → modifyParameter → restartDBInstance
```

### 7. Performance Monitoring

```
describeDBInstancePerformance → describeSlowLogRecords → createDiagnosticReport
```

### 8. PostgreSQL Major Version Upgrade

```
upgradeDBInstanceMajorVersionPrecheck → describeUpgradeMajorVersionPrecheckTask → upgradeDBInstanceMajorVersion
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **Instance CRUD/lifecycle/spec/network/pricing**: `references/instance.md`
- **Read-only instances/proxy/read-write splitting**: `references/readonly.md`
- **Account CRUD/password/privileges**: `references/account.md`
- **Database CRUD/charset/collation**: `references/database.md`
- **Backup/restore/cross-region DR**: `references/backup.md`
- **IP whitelist/SSL/TDE/security groups/masking**: `references/security.md`
- **Performance/slow queries/SQL audit/diagnostics**: `references/monitoring.md`
- **Parameters/parameter groups/events**: `references/parameter.md`
- **Migration/import/export/GAD**: `references/migration.md`
- **PostgreSQL extensions/PG HBA/replication/DuckDB**: `references/postgres-ext.md`
- **RDS Custom instances/disks/images/keys/commands**: `references/rc-instance.md`
- **Resource tagging**: `references/tag-resource.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Instance listing, creation, and deletion
- Account and database management
- Backup creation and listing
- IP whitelist and SSL configuration
- Performance monitoring and slow query analysis
- Parameter management
- Resource tagging
