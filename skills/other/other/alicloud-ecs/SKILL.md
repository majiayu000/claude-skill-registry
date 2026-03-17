---
name: alicloud-ecs
description: Manage Alibaba Cloud Elastic Compute Service (ECS) using the @alicloud/ecs20140526 TypeScript SDK. Use when working with cloud servers on Alibaba Cloud, including instance lifecycle (create, start, stop, reboot, delete), disks and snapshots, images, security groups, VPC networking, EIP, ENI, SSH key pairs, dedicated hosts, auto provisioning, launch templates, Cloud Assistant commands, tags, system events, diagnostics, storage capacity units, and prefix lists. Covers all 374 APIs of the ECS 20140526 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/ecs20140526"
  api-version: "2014-05-26"
---

# Alibaba Cloud ECS Skill

Manage cloud servers, disks, images, networks, security, and operations via the `@alicloud/ecs20140526` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/ecs20140526 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
export ALIBABA_CLOUD_REGION_ID="cn-hangzhou"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including regions, instance types, charge types, and pagination.

## Client Initialization

```typescript
import Client from '@alicloud/ecs20140526';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  regionId: 'cn-hangzhou',
  endpoint: 'ecs.cn-hangzhou.aliyuncs.com',
}));
```

## API Overview (374 APIs in 14 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| Instance | 71 | runInstances, startInstance, stopInstance, describeInstances | [references/instance.md](references/instance.md) |
| Disk & Snapshot | 46 | createDisk, attachDisk, createSnapshot, createAutoSnapshotPolicy | [references/disk.md](references/disk.md) |
| Image | 23 | createImage, copyImage, importImage, describeImages | [references/image.md](references/image.md) |
| Security Group | 15 | createSecurityGroup, authorizeSecurityGroup, revokeSecurityGroup | [references/security-group.md](references/security-group.md) |
| Network & EIP | 91 | createVpc, createVSwitch, allocateEipAddress, createNetworkInterface | [references/network.md](references/network.md) |
| SSH Key Pair | 6 | createKeyPair, attachKeyPair, describeKeyPairs | [references/key-pair.md](references/key-pair.md) |
| Dedicated Host | 15 | allocateDedicatedHosts, describeDedicatedHosts | [references/dedicated-host.md](references/dedicated-host.md) |
| Auto Provisioning | 20 | createAutoProvisioningGroup, createElasticityAssurance | [references/auto-scaling.md](references/auto-scaling.md) |
| Launch Template | 7 | createLaunchTemplate, describeLaunchTemplates | [references/launch-template.md](references/launch-template.md) |
| Cloud Assistant | 22 | runCommand, describeInvocationResults, createActivation | [references/command.md](references/command.md) |
| Tag & Resource | 18 | tagResources, describeRegions, describeZones | [references/tag-resource.md](references/tag-resource.md) |
| System Events | 20 | describeInstancesFullStatus, createDiagnosticReport | [references/system-event.md](references/system-event.md) |
| Storage & Deployment | 16 | createStorageSet, createDeploymentSet, createSavingsPlan | [references/storage-capacity.md](references/storage-capacity.md) |
| Prefix List | 5 | createPrefixList, describePrefixLists | [references/prefix-list.md](references/prefix-list.md) |

## Core Patterns

### RPC-Style API

ECS uses RPC-style APIs. All parameters are flat fields in a Request object:

```typescript
import * as models from '@alicloud/ecs20140526/dist/models';

const { body } = await client.describeInstances(new models.DescribeInstancesRequest({
  regionId: 'cn-hangzhou',
  instanceIds: JSON.stringify(['i-xxx1', 'i-xxx2']),
  pageSize: 10,
  pageNumber: 1,
}));
```

### regionId is Required

Almost all ECS APIs require `regionId`. Always include it:

```typescript
const request = new models.DescribeDisksRequest({
  regionId: 'cn-hangzhou',  // Required!
  diskIds: JSON.stringify(['d-xxx']),
});
```

### Page-Based Pagination

Most Describe/List APIs use `pageNumber` + `pageSize`:

```typescript
let pageNumber = 1;
let all: any[] = [];
while (true) {
  const { body } = await client.describeInstances(new models.DescribeInstancesRequest({
    regionId: 'cn-hangzhou', pageSize: 100, pageNumber,
  }));
  all.push(...(body.instances?.instance || []));
  if (all.length >= (body.totalCount || 0)) break;
  pageNumber++;
}
```

### JSON-Encoded Array Parameters

Some parameters accept JSON-encoded arrays:

```typescript
// instanceIds, diskIds, etc. are JSON strings
instanceIds: JSON.stringify(['i-xxx1', 'i-xxx2']),
diskIds: JSON.stringify(['d-xxx1']),
```

### Error Handling

```typescript
try {
  await client.describeInstances(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. Launch Instance

```
describeRegions → describeInstanceTypes → describeImages → createSecurityGroup → authorizeSecurityGroup → runInstances
```

### 2. Disk & Snapshot

```
createDisk → attachDisk → createSnapshot → createAutoSnapshotPolicy → applyAutoSnapshotPolicy
```

### 3. Image Management

```
createImage → copyImage → describeImages → importImage / exportImage
```

### 4. Security Group Rules

```
createSecurityGroup → authorizeSecurityGroup → authorizeSecurityGroupEgress → describeSecurityGroupAttribute
```

### 5. Instance Scaling

```
stopInstance → modifyInstanceSpec → startInstance
```

### 6. Remote Command Execution

```
describeCloudAssistantStatus → runCommand → describeInvocationResults
```

### 7. Network Interface

```
createNetworkInterface → attachNetworkInterface → assignPrivateIpAddresses
```

### 8. Key Pair Login

```
createKeyPair → runInstances (keyPairName) → attachKeyPair
```

### 9. Dedicated Host

```
describeDedicatedHostTypes → allocateDedicatedHosts → runInstances (dedicatedHostId)
```

### 10. Tag-Based Management

```
tagResources → describeInstances (tag filter) → untagResources
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **Instance lifecycle/types/pricing**: `references/instance.md`
- **Disk/snapshot/auto-snapshot**: `references/disk.md`
- **Image/pipeline/share**: `references/image.md`
- **Security group/rules**: `references/security-group.md`
- **VPC/VSwitch/EIP/ENI/NAT/Route**: `references/network.md`
- **SSH key pairs**: `references/key-pair.md`
- **Dedicated hosts/clusters**: `references/dedicated-host.md`
- **Auto provisioning/elasticity/capacity**: `references/auto-scaling.md`
- **Launch templates**: `references/launch-template.md`
- **Cloud Assistant commands**: `references/command.md`
- **Tags/regions/zones/tasks**: `references/tag-resource.md`
- **System events/diagnostics**: `references/system-event.md`
- **Storage sets/deployment sets/savings**: `references/storage-capacity.md`
- **Prefix lists**: `references/prefix-list.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- Instance CRUD and lifecycle management
- Security group creation and rule management
- Disk creation, attachment, and snapshot
- Image creation and listing
- SSH key pair management
- Cloud Assistant remote command execution
- Tag-based resource management
- Region and zone queries
