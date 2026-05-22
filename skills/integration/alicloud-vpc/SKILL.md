---
name: alicloud-vpc
description: Manage Alibaba Cloud VPC networking using the @alicloud/vpc20160428 TypeScript SDK. Use when working with virtual private clouds, VSwitches, route tables, EIPs, NAT gateways, VPN gateways, Express Connect, BGP routing, network ACLs, flow logs, traffic mirroring, IPv6, HAVIP, gateway endpoints, and resource tagging. Covers all 396 APIs of the VPC 20160428 version.
license: Apache-2.0
metadata:
  author: alicloud
  version: "1.0"
  sdk-package: "@alicloud/vpc20160428"
  api-version: "2016-04-28"
---

# Alibaba Cloud VPC Skill

Manage VPC networking infrastructure via the `@alicloud/vpc20160428` TypeScript SDK.

## Prerequisites

```bash
npm install @alicloud/vpc20160428 @alicloud/openapi-core @darabonba/typescript
```

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="<your-key-id>"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="<your-key-secret>"
```

See [scripts/setup_client.ts](scripts/setup_client.ts) for a reusable client factory, and [references/quickstart.md](references/quickstart.md) for full setup including endpoints, CIDR blocks, pagination, and async polling.

## Client Initialization

```typescript
import Client from '@alicloud/vpc20160428';
import { Config } from '@alicloud/openapi-core';

const client = new Client(new Config({
  accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
  accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
  endpoint: 'vpc.aliyuncs.com',
  regionId: 'cn-hangzhou',
}));
```

## API Overview (396 APIs in 13 Domains)

| Domain | APIs | Key Operations | Reference |
|--------|------|----------------|-----------|
| VPC Management | 32 | createVpc, describeVpcs, modifyVpcAttribute | [references/vpc.md](references/vpc.md) |
| VSwitch | 11 | createVSwitch, describeVSwitches | [references/vswitch.md](references/vswitch.md) |
| Route Table & Entry | 33 | createRouteEntry, describeRouteTables | [references/route-table.md](references/route-table.md) |
| Elastic IP (EIP) | 47 | allocateEipAddress, associateEipAddress | [references/eip.md](references/eip.md) |
| NAT Gateway | 30 | createNatGateway, createSnatEntry, createForwardEntry | [references/nat-gateway.md](references/nat-gateway.md) |
| VPN Gateway | 62 | createVpnGateway, createVpnConnection, createSslVpnServer | [references/vpn.md](references/vpn.md) |
| Express Connect & VBR | 83 | createPhysicalConnection, createVirtualBorderRouter | [references/express-connect.md](references/express-connect.md) |
| BGP Routing | 11 | createBgpGroup, createBgpPeer, addBgpNetwork | [references/bgp.md](references/bgp.md) |
| Network ACL | 9 | createNetworkAcl, associateNetworkAcl | [references/network-acl.md](references/network-acl.md) |
| Flow Log | 8 | createFlowLog, activeFlowLog | [references/flow-log.md](references/flow-log.md) |
| Traffic Mirror | 14 | createTrafficMirrorSession, createTrafficMirrorFilter | [references/traffic-mirror.md](references/traffic-mirror.md) |
| IPv6 & HAVIP | 47 | createIpv6Gateway, createHaVip, allocateIpv6Address | [references/ipv6.md](references/ipv6.md) |
| Tag, Region & Zone | 9 | tagResources, describeRegions, describeZones | [references/tag-resource.md](references/tag-resource.md) |

## Core Patterns

### RPC-Style with regionId

All VPC APIs require `regionId` to specify the target region:

```typescript
import * as models from '@alicloud/vpc20160428/dist/models';

const { body } = await client.describeVpcs(new models.DescribeVpcsRequest({
  regionId: 'cn-hangzhou',
  pageSize: 50,
  pageNumber: 1,
}));
```

### Resource Lifecycle (Async)

Most create operations are asynchronous. Poll status after creation:

```typescript
// Create VPC
const { body } = await client.createVpc(new models.CreateVpcRequest({
  regionId: 'cn-hangzhou',
  cidrBlock: '10.0.0.0/8',
  vpcName: 'my-vpc',
}));

// Poll until Available
let status = '';
while (status !== 'Available') {
  const { body: desc } = await client.describeVpcs(new models.DescribeVpcsRequest({
    regionId: 'cn-hangzhou', vpcId: body.vpcId,
  }));
  status = desc.vpcs?.vpc?.[0]?.status || '';
  if (status !== 'Available') await new Promise(r => setTimeout(r, 2000));
}
```

### Page-Based Pagination

Most Describe APIs use `pageNumber` + `pageSize`:

```typescript
let pageNumber = 1;
let all: any[] = [];
while (true) {
  const { body } = await client.describeVpcs(new models.DescribeVpcsRequest({
    regionId: 'cn-hangzhou', pageSize: 50, pageNumber,
  }));
  all.push(...(body.vpcs?.vpc || []));
  if (all.length >= (body.totalCount || 0)) break;
  pageNumber++;
}
```

### Error Handling

```typescript
try {
  await client.createVpc(request);
} catch (err: any) {
  console.error(`Code: ${err.code}, Message: ${err.message}, RequestId: ${err.data?.RequestId}`);
}
```

## Common Workflows

### 1. VPC + VSwitch Setup

```
createVpc → createVSwitch (per zone) → createNetworkAcl → associateNetworkAcl
```

### 2. NAT Gateway for Internet Access

```
createNatGateway → allocateEipAddress → associateEipAddress → createSnatEntry → createForwardEntry
```

### 3. Site-to-Site VPN

```
createVpnGateway → createCustomerGateway → createVpnConnection → createVpnRouteEntry
```

### 4. VPC Peering

```
createVpcPeerConnection → acceptVpcPeerConnection → createRouteEntry (both sides)
```

### 5. Express Connect

```
createPhysicalConnection → createVirtualBorderRouter → createBgpGroup → createBgpPeer → addBgpNetwork
```

### 6. Flow Log

```
createFlowLog → activeFlowLog → describeFlowLogs
```

### 7. Traffic Mirroring

```
createTrafficMirrorFilter → createTrafficMirrorFilterRules → createTrafficMirrorSession
```

### 8. EIP & Bandwidth

```
allocateEipAddress → associateEipAddress → createCommonBandwidthPackage → addCommonBandwidthPackageIp
```

See [references/workflows.md](references/workflows.md) for detailed workflow examples with full code.

## API Reference Quick Index

Load the corresponding reference file for parameter details:

- **VPC CRUD/CIDR/DHCP/vRouter**: `references/vpc.md`
- **VSwitch CRUD/CIDR reservation**: `references/vswitch.md`
- **Route tables/entries/gateway routes**: `references/route-table.md`
- **EIP/bandwidth packages/public IP pools**: `references/eip.md`
- **NAT gateway/SNAT/DNAT/Full NAT/NAT IP**: `references/nat-gateway.md`
- **VPN gateway/IPsec/SSL VPN/tunnels**: `references/vpn.md`
- **Physical connections/VBR/peering/prefix lists**: `references/express-connect.md`
- **BGP groups/peers/networks**: `references/bgp.md`
- **Network ACL rules**: `references/network-acl.md`
- **Flow log capture/analysis**: `references/flow-log.md`
- **Traffic mirror filters/sessions**: `references/traffic-mirror.md`
- **IPv6 gateway/translator/HAVIP/gateway endpoints**: `references/ipv6.md`
- **Tags/regions/zones**: `references/tag-resource.md`

Each reference file contains per-API documentation with method signatures and parameter tables.

## Code Examples

See [scripts/examples.ts](scripts/examples.ts) for ready-to-use code covering:

- VPC and VSwitch CRUD
- Route entry management
- EIP allocation, binding, and release
- NAT gateway with SNAT/DNAT rules
- Network ACL creation
- Flow log creation and activation
- Resource tagging
