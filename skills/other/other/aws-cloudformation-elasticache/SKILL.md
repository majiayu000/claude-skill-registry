---
name: aws-cloudformation-elasticache
description: Provides AWS CloudFormation patterns for ElastiCache Redis or Memcached infrastructure, including subnet groups, parameter groups, security controls, and cross-stack outputs. Use when designing cache tiers, high-availability replication groups, encryption settings, or reusable CloudFormation templates for application caching.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation ElastiCache

## Overview

Use this skill to model ElastiCache infrastructure with CloudFormation without turning `SKILL.md` into a full service manual.

Focus on the delivery decisions that matter most:
- choosing the right cache topology
- placing the cache safely inside a VPC
- configuring availability, encryption, and exports for downstream stacks

Use the bundled `references/` documents for larger production templates and service-specific detail.

## When to Use

Use this skill when:
- creating a Redis or Memcached cache tier with CloudFormation
- deciding between `AWS::ElastiCache::CacheCluster` and `AWS::ElastiCache::ReplicationGroup`
- configuring subnet groups, parameter groups, and security groups for application access
- adding snapshots, maintenance windows, encryption, and Multi-AZ behavior
- exporting cache endpoints to application or platform stacks
- reviewing cache changes for replacement risk, downtime, or operational cost

Typical trigger phrases include `cloudformation elasticache`, `redis replication group`, `memcached cluster`, `cache subnet group`, and `export redis endpoint`.

## Instructions

### 1. Choose the cache topology first

Use:
- `ReplicationGroup` for production Redis-style deployments that need failover, replicas, or sharding
- `CacheCluster` for Memcached or simple single-node cache scenarios

Do not start with resource YAML before deciding whether the application needs durability, read replicas, cluster mode, or just an ephemeral cache.

### 2. Model the network boundary explicitly

Create and wire:
- a subnet group with private application subnets
- a security group that allows access only from the application tier
- parameter groups only when default engine settings are insufficient

Keep the cache private unless there is a very unusual and well-reviewed reason not to.

### 3. Configure durability and security based on environment

For production-style Redis deployments, decide on:
- automatic failover and Multi-AZ
- at-rest and in-transit encryption
- snapshot retention and maintenance windows
- authentication or auth token strategy where supported

For lower environments, document when a cheaper single-node configuration is acceptable.

### 4. Add reusable parameters and outputs

Parameterize only the settings that truly vary between environments, such as node type, subnet IDs, or snapshot retention.

Export outputs that other stacks need, typically:
- primary or configuration endpoint
- reader endpoint when applicable
- security group or subnet group identifiers only if downstream stacks genuinely depend on them

### 5. Validate the stack change before rollout

Before deployment:
- run template validation
- inspect whether changes replace the cluster or replication group
- review security group exposure and encryption settings
- confirm maintenance, backup, and scaling choices match the application's recovery expectations

## Examples

### Example 1: Redis replication group with private networking

```yaml
Parameters:
  CacheNodeType:
    Type: String
    Default: cache.t4g.small

Resources:
  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup
    Properties:
      Description: Private subnets for the cache tier
      SubnetIds: !Ref PrivateSubnetIds

  CacheSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Application access to Redis
      VpcId: !Ref VpcId

  RedisReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupDescription: Application Redis cluster
      Engine: redis
      CacheNodeType: !Ref CacheNodeType
      NumNodeGroups: 1
      ReplicasPerNodeGroup: 1
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      SecurityGroupIds:
        - !Ref CacheSecurityGroup
      TransitEncryptionEnabled: true
      AtRestEncryptionEnabled: true
```

### Example 2: Export an endpoint for another stack

```yaml
Outputs:
  RedisPrimaryEndpoint:
    Description: Primary endpoint used by the application stack
    Value: !GetAtt RedisReplicationGroup.PrimaryEndPoint.Address
    Export:
      Name: !Sub "${AWS::StackName}-RedisPrimaryEndpoint"
```

Keep outputs small and stable so consumer stacks do not break unnecessarily.

## Best Practices

- Prefer replication groups over single-node Redis for production systems.
- Put caches in private subnets and restrict ingress to known application security groups.
- Turn on encryption and snapshots unless there is a documented reason not to.
- Review replacement risk before changing engine version, cluster mode, or subnet design.
- Use parameters for environment-specific sizing, not for every possible knob.
- Keep deep template variants in `references/examples.md` instead of expanding the root skill endlessly.

## Constraints and Warnings

- Some ElastiCache changes cause replacement or data loss if applied carelessly.
- NAT, subnet, and routing mistakes can make the cache unreachable even when the stack succeeds.
- Multi-AZ, replicas, and larger node types can change cost significantly.
- Cache endpoints, encryption support, and auth features vary by engine and version.
- Snapshot and maintenance windows must align with the application's recovery and deployment practices.

## References

- `references/examples.md`
- `references/reference.md`

## Related Skills

- `aws-cloudformation-vpc`
- `aws-cloudformation-security`
- `aws-cloudformation-ecs`
- `aws-cloudformation-lambda`
