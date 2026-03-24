---
name: aws-cloudformation-vpc
description: Provides AWS CloudFormation patterns for VPC foundations, including subnets, route tables, internet and NAT gateways, endpoints, and reusable outputs. Use when creating a new network baseline, segmenting public and private workloads, or preparing CloudFormation networking stacks for application deployments.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation VPC Infrastructure

## Overview

Use this skill to build a VPC foundation with CloudFormation in a way that stays readable, reusable, and safe to evolve.

The key goals are:
- a clear subnet and routing model
- predictable connectivity for public and private workloads
- outputs that downstream stacks can consume without duplicating network logic

Use the `references/` files for larger templates and extended service combinations.

## When to Use

Use this skill when:
- creating a new VPC stack for an application or shared platform
- adding public and private subnets across one or more Availability Zones
- wiring internet access, NAT egress, or private endpoints
- exporting VPC, subnet, route table, and security-group-adjacent identifiers for other stacks
- reviewing a networking change for blast radius, route correctness, or cost
- preparing reusable infrastructure for ECS, EKS, Lambda, EC2, or RDS stacks

Typical trigger phrases include `cloudformation vpc`, `private subnet`, `nat gateway`, `route table`, `vpc endpoint`, and `export subnet ids`.

## Instructions

### 1. Start with the address plan

Before writing resources, define:
- VPC CIDR range
- number of Availability Zones
- public, private, and isolated subnet ranges
- which workloads need internet ingress, NAT egress, or only private AWS service access

This prevents route-table sprawl and painful subnet replacement later.

### 2. Build the core network resources in layers

Create the stack in this order:
- VPC and subnets
- Internet Gateway for public ingress and egress
- NAT gateways if private subnets need outbound internet access
- route tables and subnet associations
- optional VPC endpoints for private access to AWS services

Keep each layer easy to inspect in the template and avoid mixing unrelated application resources into the same stack.

### 3. Parameterize only the environment-dependent values

Useful parameters usually include:
- environment name
- VPC CIDR and subnet CIDRs
- number of AZs or explicit subnet IDs in nested-stack scenarios
- flags for optional endpoints or NAT layout

Do not parameterize every route or tag unless it meaningfully changes between environments.

### 4. Export only what consumers really need

Typical outputs are:
- VPC ID
- public, private, and isolated subnet IDs
- route table IDs when downstream stacks must attach routes
- security boundaries or prefix-list references only when another stack consumes them

Stable outputs make application stacks easier to compose and migrate.

### 5. Validate networking behavior, not just template syntax

Before rollout:
- validate the template and review change sets
- confirm subnet associations and default routes are correct
- check NAT placement and expected egress paths
- verify endpoint routes or prefix lists for private AWS service access
- review overlapping CIDR or peering implications when integrating with existing networks

## Examples

### Example 1: Two-tier VPC baseline

```yaml
Resources:
  Vpc:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true

  PublicSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref Vpc
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true
      AvailabilityZone: !Select [0, !GetAZs ""]

  PrivateSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref Vpc
      CidrBlock: 10.0.11.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
```

Use this as the base layer, then add route tables, gateway attachments, and endpoint resources explicitly.

### Example 2: Export subnet IDs for application stacks

```yaml
Outputs:
  PrivateSubnetIds:
    Description: Private subnets for ECS, Lambda, or RDS workloads
    Value: !Join [",", [!Ref PrivateSubnetA, !Ref PrivateSubnetB]]
    Export:
      Name: !Sub "${AWS::StackName}-PrivateSubnetIds"
```

If consumers need a list object rather than a joined string, prefer nested stacks or stack parameters over brittle parsing in downstream templates.

## Best Practices

- Keep public, private, and isolated subnet purposes explicit in names and tags.
- Prefer one NAT gateway per AZ for resilient production environments when the budget allows it.
- Use VPC endpoints to reduce unnecessary NAT traffic for AWS service access.
- Export VPC and subnet identifiers from the network stack instead of recreating network assumptions elsewhere.
- Review network changes with dependency stacks because route and subnet changes can have broad blast radius.
- Keep the root skill focused and move larger networking variants to `references/examples.md`.

## Constraints and Warnings

- NAT gateways can dominate network cost in small environments.
- CIDR overlap blocks peering, transit, and future network expansion.
- Route-table or subnet replacements can interrupt traffic even when the template is valid.
- Endpoint quotas, AZ availability, and service-specific subnet requirements vary by region.
- Hardcoding Availability Zones can reduce portability across accounts and regions.

## References

- `references/examples.md`
- `references/reference.md`

## Related Skills

- `aws-cloudformation-ec2`
- `aws-cloudformation-rds`
- `aws-cloudformation-ecs`
- `aws-cloudformation-security`
