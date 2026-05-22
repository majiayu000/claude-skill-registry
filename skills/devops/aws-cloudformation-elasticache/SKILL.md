---
name: aws-cloudformation-elasticache
description: AWS CloudFormation patterns for Amazon ElastiCache. Use when creating ElastiCache clusters (Redis, Memcached), replication groups, parameter groups, subnet groups, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references for distributed caching infrastructure.
category: aws
tags: [aws, cloudformation, elasticache, redis, memcached, cache, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation ElastiCache

## Overview

Create production-ready Amazon ElastiCache infrastructure using AWS CloudFormation templates. This skill covers Redis clusters, Memcached clusters, replication groups, parameter groups, subnet groups, security groups, template structure best practices, parameter patterns, and cross-stack references for modular, reusable infrastructure as code.

## When to Use

Use this skill when:
- Creating new ElastiCache Redis clusters (standalone or clustered)
- Setting up Redis Replication Groups for high availability
- Creating Memcached clusters for distributed caching
- Configuring ElastiCache Parameter Groups
- Setting up ElastiCache Subnet Groups for VPC deployment
- Implementing template Parameters with AWS-specific types
- Creating Outputs for cross-stack references
- Organizing templates with Mappings and Conditions
- Designing reusable, modular CloudFormation templates for caching infrastructure

## Quick Start

### Basic Redis Cluster

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Simple Redis ElastiCache cluster with basic configuration

Parameters:
  CacheNodeType:
    Type: String
    Default: cache.t3.micro
    Description: Cache node instance type

  NumCacheNodes:
    Type: Number
    Default: 1
    Description: Number of cache nodes

Resources:
  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup
    Properties:
      Description: Subnet group for ElastiCache
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheNodeType: !Ref CacheNodeType
      NumCacheNodes: !Ref NumCacheNodes
      Engine: redis
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup

Outputs:
  RedisEndpoint:
    Description: Redis cluster endpoint address
    Value: !GetAtt CacheCluster.RedisEndpoint.Address

  RedisPort:
    Description: Redis cluster port
    Value: !GetAtt CacheCluster.RedisEndpoint.Port
```

### Redis Replication Group

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Redis Replication Group with primary and read replicas

Parameters:
  CacheNodeType:
    Type: String
    Default: cache.t3.micro
    Description: Cache node instance type

Resources:
  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup
    Properties:
      Description: Subnet group for Redis replication
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  ReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupDescription: Primary and replicas for HA
      Engine: redis
      CacheNodeType: !Ref CacheNodeType
      NumNodeGroups: 1
      ReplicasPerNodeGroup: 1
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup

Outputs:
  PrimaryEndpoint:
    Description: Primary endpoint for write operations
    Value: !GetAtt ReplicationGroup.PrimaryEndPoint.Address

  ReaderEndpoint:
    Description: Reader endpoint for read operations
    Value: !GetAtt ReplicationGroup.ReaderEndPoint.Address
```

## Template Structure

### Template Sections Overview

AWS CloudFormation templates are JSON or YAML files with specific sections. Each section serves a purpose in defining your infrastructure.

```yaml
AWSTemplateFormatVersion: 2010-09-09  # Required - template version
Description: Optional description string  # Optional description

# Section order matters for readability but CloudFormation accepts any order
Mappings: {}       # Static configuration tables
Metadata: {}       # Additional information about resources
Parameters: {}     # Input values for customization
Rules: {}          # Parameter validation rules
Conditions: {}     # Conditional resource creation
Transform: {}      # Macro processing (e.g., AWS::Serverless)
Resources: {}      # AWS resources to create (REQUIRED)
Outputs: {}        # Return values after stack creation
```

### Format Version

The `AWSTemplateFormatVersion` identifies the template version. Current version is `2010-09-09`.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ElastiCache Redis Cluster Template
```

### Description

Add a description to document the template's purpose. Must appear after the format version.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  This template creates an ElastiCache Redis cluster with:
  - Multi-AZ deployment for high availability
  - Automatic failover enabled
  - Encrypted at-rest and in-transit
  - Parameter group for custom configuration
```

### Metadata

Use `Metadata` for additional information about resources or parameters, including AWS::CloudFormation::Interface for parameter grouping.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Cache Configuration
        Parameters:
          - CacheNodeType
          - NumCacheNodes
          - Engine
      - Label:
          default: Network
        Parameters:
          - CacheSubnetGroupName
          - VpcSecurityGroupIds
    ParameterLabels:
      CacheNodeType:
        default: Cache Node Instance Type
      NumCacheNodes:
        default: Number of Cache Nodes
```

### Resources Section

The `Resources` section is the only required section. It defines AWS resources to provision.

```yaml
Resources:
  # Cache Subnet Group (required for VPC deployment)
  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup
    Properties:
      Description: Subnet group for ElastiCache deployment
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  # Cache Parameter Group
  CacheParameterGroup:
    Type: AWS::ElastiCache::ParameterGroup
    Properties:
      Description: Custom parameter group for Redis
      Family: redis7.x
      Parameters:
        maxmemory-policy: allkeys-lru
        timeout: 300

  # Cache Cluster
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheNodeType: cache.t3.micro
      NumCacheNodes: 1
      Engine: redis
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref CacheParameterGroup
```

## Parameters

### Parameter Types

Use AWS-specific parameter types for validation and easier selection in the console.

```yaml
Parameters:
  CacheNodeType:
    Type: String
    Description: ElastiCache node instance type
    Default: cache.t3.micro

  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup::Name
    Description: Existing cache subnet group

  VpcSecurityGroupId:
    Type: AWS::EC2::SecurityGroup::Id
    Description: Security group for cache cluster
```

### AWS::ElastiCache::CacheCluster::CacheNodeType Values

Common ElastiCache node types:

```yaml
Parameters:
  CacheNodeType:
    Type: String
    Default: cache.t3.micro
    AllowedValues:
      - cache.t3.micro
      - cache.t3.small
      - cache.t3.medium
      - cache.t3.large
      - cache.m5.large
      - cache.m5.xlarge
      - cache.m5.2xlarge
      - cache.m5.4xlarge
      - cache.r5.large
      - cache.r5.xlarge
      - cache.r5.2xlarge
      - cache.r5.4xlarge
      - cache.r6g.large
      - cache.r6g.xlarge
      - cache.r6g.2xlarge
```

### Parameter Constraints

Add constraints to validate parameter values.

```yaml
Parameters:
  CacheClusterId:
    Type: String
    Description: Cache cluster identifier
    Default: myrediscluster
    AllowedPattern: "[a-zA-Z][a-zA-Z0-9]*"
    ConstraintDescription: Must begin with a letter; contain only alphanumeric characters
    MinLength: 1
    MaxLength: 50

  NumCacheNodes:
    Type: Number
    Description: Number of cache nodes
    Default: 1
    MinValue: 1
    MaxValue: 10

  CachePort:
    Type: Number
    Description: Cache port number
    Default: 6379
    MinValue: 1024
    MaxValue: 65535
```

### Engine and Version Parameters

```yaml
Parameters:
  Engine:
    Type: String
    Description: Cache engine
    Default: redis
    AllowedValues:
      - redis
      - memcached

  EngineVersion:
    Type: String
    Description: Cache engine version
    Default: 7.0

  EngineVersionMajor:
    Type: String
    Description: Cache engine major version
    Default: "7.0"
    AllowedValues:
      - "6.x"
      - "7.0"
```

### SSM Parameter Types

Reference Systems Manager parameters for dynamic values.

```yaml
Parameters:
  LatestRedisVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Description: Latest Redis version from SSM
    Default: /elasticache/redis/latest/version

  LatestMemcachedVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Description: Latest Memcached version from SSM
    Default: /elasticache/memcached/latest/version
```

## Mappings

Use `Mappings` for static configuration data based on regions or instance types.

```yaml
Mappings:
  CacheNodeConfig:
    cache.t3.micro:
      CPU: 2
      MemoryMiB: 555
      NetworkGbits: 5
    cache.t3.medium:
      CPU: 2
      MemoryMiB: 3218
      NetworkGbits: 10
    cache.m5.large:
      CPU: 2
      MemoryMiB: 6910
      NetworkGbits: 10
    cache.r5.large:
      CPU: 2
      MemoryMiB: 13866
      NetworkGbits: 10

  RegionMap:
    us-east-1:
      RedisPort: 6379
      MemcachedPort: 11211
    us-west-2:
      RedisPort: 6379
      MemcachedPort: 11211
    eu-west-1:
      RedisPort: 6379
      MemcachedPort: 11211

Resources:
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheNodeType: !Ref CacheNodeType
      NumCacheNodes: 1
      Engine: redis
      CachePort: !FindInMap [RegionMap, !Ref AWS::Region, RedisPort]
```

## Conditions

Use `Conditions` to conditionally create resources based on parameters.

```yaml
Parameters:
  EnableMultiAZ:
    Type: String
    Default: false
    AllowedValues:
      - true
      - false

  EnableEncryption:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

  Environment:
    Type: String
    Default: development
    AllowedValues:
      - development
      - staging
      - production

Conditions:
  IsMultiAZ: !Equals [!Ref EnableMultiAZ, true]
  IsEncrypted: !Equals [!Ref EnableEncryption, true]
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheNodeType: !Ref CacheNodeType
      NumCacheNodes: !If [IsMultiAZ, 2, 1]
      Engine: redis
      AutomaticFailoverEnabled: !If [IsMultiAZ, true, false]
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

### Condition Functions

```yaml
Conditions:
  IsDev: !Equals [!Ref Environment, development]
  IsStaging: !Equals [!Ref Environment, staging]
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      # Production gets larger instances
      CacheNodeType: !If [IsProduction, cache.r5.large, cache.t3.micro]
      # Production gets multi-AZ
      NumCacheNodes: !If [IsProduction, 3, 1]
      AutomaticFailoverEnabled: !If [IsProduction, true, false]
```

## Transform

Use `Transform` for macros like AWS::Serverless for SAM templates.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: Serverless ElastiCache application template

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11

Resources:
  CacheFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      CodeUri: function/
      Policies:
        - ElastiCacheFullAccessPolicy:
            CacheClusterId: !Ref CacheCluster
      Environment:
        Variables:
          CACHE_ENDPOINT: !GetAtt CacheCluster.RedisEndpoint.Address
          CACHE_PORT: !GetAtt CacheCluster.RedisEndpoint.Port
```

## Outputs and Cross-Stack References

### Basic Outputs

```yaml
Outputs:
  CacheClusterId:
    Description: Cache Cluster ID
    Value: !Ref CacheCluster

  CacheClusterEndpoint:
    Description: Cache cluster endpoint address
    Value: !GetAtt CacheCluster.RedisEndpoint.Address

  CacheClusterPort:
    Description: Cache cluster port
    Value: !GetAtt CacheCluster.RedisEndpoint.Port

  CacheClusterArn:
    Description: Cache Cluster ARN
    Value: !GetAtt CacheCluster.Arn

  CacheNodeType:
    Description: Cache Node Type
    Value: !Ref CacheNodeType
```

### Exporting Values for Cross-Stack References

Export values so other stacks can import them.

```yaml
Outputs:
  CacheClusterId:
    Description: Cache Cluster ID for other stacks
    Value: !Ref CacheCluster
    Export:
      Name: !Sub ${AWS::StackName}-CacheClusterId

  CacheClusterEndpoint:
    Description: Cache cluster endpoint for application stacks
    Value: !GetAtt CacheCluster.RedisEndpoint.Address
    Export:
      Name: !Sub ${AWS::StackName}-CacheEndpoint

  CacheClusterPort:
    Description: Cache cluster port for application stacks
    Value: !GetAtt CacheCluster.RedisEndpoint.Port
    Export:
      Name: !Sub ${AWS::StackName}-CachePort

  ConnectionString:
    Description: Full connection string for applications
    Value: !Sub redis://${CacheClusterEndpoint}:${CacheClusterPort}/0
    Export:
      Name: !Sub ${AWS::StackName}-CacheConnectionString
```

### Importing Values in Another Stack

```yaml
Parameters:
  CacheClusterId:
    Type: AWS::ElastiCache::Cluster::Id
    Description: Cache cluster ID from cache stack

  CacheEndpoint:
    Type: String
    Description: Cache cluster endpoint address

Resources:
  ApplicationConfig:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/cache/endpoint
      Value: !Ref CacheEndpoint
      Type: String
```

### Cross-Stack Reference Pattern

Create a dedicated cache stack that exports values:

```yaml
# cache-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Cache infrastructure stack

Parameters:
  EnvironmentName:
    Type: String
    Default: production

Resources:
  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup
    Properties:
      Description: !Sub Subnet group for ${EnvironmentName}
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  CacheParameterGroup:
    Type: AWS::ElastiCache::ParameterGroup
    Properties:
      Description: Redis parameter group
      Family: redis7.x
      Parameters:
        maxmemory-policy: allkeys-lru

  CacheSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Cache security group
      VpcId: !Ref VPCId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 6379
          ToPort: 6379
          SourceSecurityGroupId: !Ref AppSecurityGroup

  ReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupDescription: Redis replication for ${EnvironmentName}
      Engine: redis
      CacheNodeType: cache.r5.large
      NumNodeGroups: 1
      ReplicasPerNodeGroup: 1
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref CacheParameterGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup

Outputs:
  CacheClusterId:
    Value: !Ref ReplicationGroup
    Export:
      Name: !Sub ${EnvironmentName}-CacheClusterId

  CacheEndpoint:
    Value: !GetAtt ReplicationGroup.PrimaryEndPoint.Address
    Export:
      Name: !Sub ${EnvironmentName}-CacheEndpoint

  CachePort:
    Value: !GetAtt ReplicationGroup.PrimaryEndPoint.Port
    Export:
      Name: !Sub ${EnvironmentName}-CachePort

  CacheReaderEndpoint:
    Value: !GetAtt ReplicationGroup.ReaderEndPoint.Address
    Export:
      Name: !Sub ${EnvironmentName}-CacheReaderEndpoint
```

Application stack imports these values:

```yaml
# application-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack that imports from cache stack

Parameters:
  CacheStackName:
    Type: String
    Description: Name of the cache stack
    Default: cache-stack

Resources:
  ApplicationConfig:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/cache/endpoint
      Value: !ImportValue
        Fn::Sub: ${CacheStackName}-CacheEndpoint
      Type: String

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.11
      Handler: app.handler
      Environment:
        Variables:
          CACHE_ENDPOINT: !ImportValue
            Fn::Sub: ${CacheStackName}-CacheEndpoint
```

## ElastiCache Components

### Cache Subnet Group

Required for VPC deployment. Must include at least 2 subnets in different AZs.

```yaml
Resources:
  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup
    Properties:
      Description: Subnet group for ElastiCache
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
        - !Ref PrivateSubnet3
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-cache-subnet
```

### Cache Parameter Group

Custom parameter groups for cache configuration.

```yaml
Resources:
  CacheParameterGroup:
    Type: AWS::ElastiCache::ParameterGroup
    Properties:
      Description: Custom parameter group for Redis 7.x
      Family: redis7.x
      Parameters:
        # Memory management
        maxmemory-policy: allkeys-lru
        maxmemory-samples: 5

        # Connection settings
        timeout: 300
        tcp-keepalive: 300

        # Slow log
        slowlog-log-slower-than: 10000
        slowlog-max-len: 128

      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-cache-param
```

### Redis Parameter Groups (Common Configurations)

```yaml
# For caching with LRU eviction
CacheParameterGroup:
  Type: AWS::ElastiCache::ParameterGroup
  Properties:
    Description: Redis LRU cache config
    Family: redis7.x
    Parameters:
      maxmemory-policy: allkeys-lru
      maxmemory-samples: 5

# For session storage
CacheParameterGroup:
  Type: AWS::ElastiCache::ParameterGroup
  Properties:
    Description: Redis session store config
    Family: redis7.x
    Parameters:
      maxmemory-policy: volatile-lru
      timeout: 3600
      tcp-keepalive: 60

# For Redis Cluster
CacheParameterGroup:
  Type: AWS::ElastiCache::ParameterGroup
  Properties:
    Description: Redis Cluster config
    Family: redis7.x
    Parameters:
      cluster-enabled: yes
      timeout: 5000
```

### Memcached Parameter Groups (Common Configurations)

```yaml
Resources:
  MemcachedParameterGroup:
    Type: AWS::ElastiCache::ParameterGroup
    Properties:
      Description: Memcached parameter group
      Family: memcached1.6
      Parameters:
        max_item_size: 10485760
        request_max_size: 2097152
        connection_idle_timeout: 600
```

### Cache Cluster - Redis Standalone

```yaml
Resources:
  RedisCacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheClusterIdentifier: redis-standalone
      CacheNodeType: cache.t3.medium
      NumCacheNodes: 1
      Engine: redis
      EngineVersion: "7.0"
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref CacheParameterGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
      AutoMinorVersionUpgrade: true
      SnapshotRetentionLimit: 0
      SnapshotWindow: 05:00-06:00
```

### Cache Cluster - Memcached

```yaml
Resources:
  MemcachedCacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheClusterIdentifier: memcached-cluster
      CacheNodeType: cache.m5.large
      NumCacheNodes: 3
      Engine: memcached
      EngineVersion: "1.6"
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref MemcachedParameterGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

### Replication Group - Redis with Automatic Failover

```yaml
Resources:
  RedisReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupIdentifier: redis-replication
      ReplicationGroupDescription: Redis with automatic failover
      Engine: redis
      EngineVersion: "7.0"
      CacheNodeType: cache.r5.large
      NumNodeGroups: 1
      ReplicasPerNodeGroup: 2
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref CacheParameterGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

### Replication Group - Redis Cluster Mode

```yaml
Resources:
  RedisClusterReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupIdentifier: redis-cluster
      ReplicationGroupDescription: Redis Cluster with data partitioning
      Engine: redis
      EngineVersion: "7.0"
      CacheNodeType: cache.r5.xlarge
      NumNodeGroups: 3
      ReplicasPerNodeGroup: 1
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref CacheParameterGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

### Cache Security Group

```yaml
Resources:
  CacheSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for ElastiCache
      VpcId: !Ref VPCId
      GroupName: !Sub ${AWS::StackName}-cache-sg
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 6379
          ToPort: 6379
          SourceSecurityGroupId: !Ref AppSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-cache-sg
```

### Global Replication Group (Cross-Region)

```yaml
Resources:
  GlobalReplicationGroup:
    Type: AWS::ElastiCache::GlobalReplicationGroup
    Properties:
      GlobalReplicationGroupIdSuffix: global
      GlobalReplicationGroupDescription: Global Redis replication
      Members:
        - ReplicationGroupId: !Ref PrimaryReplicationGroup
          ReplicationGroupRegion: !Ref AWS::Region
        - ReplicationGroupId: !Ref SecondaryReplicationGroup
          ReplicationGroupRegion: us-west-2
```

## Security and Encryption

### Encryption at Rest and In Transit

```yaml
Resources:
  CacheParameterGroup:
    Type: AWS::ElastiCache::ParameterGroup
    Properties:
      Description: Redis with encryption
      Family: redis7.x
      Parameters:
        # TLS configuration
        tls-enabled: yes

  CacheSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Encrypted cache security group
      VpcId: !Ref VPCId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 6379
          ToPort: 6379
          SourceSecurityGroupId: !Ref AppSecurityGroup

  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheNodeType: cache.r5.large
      NumCacheNodes: 1
      Engine: redis
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      CacheParameterGroupName: !Ref CacheParameterGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
      # Encryption settings
      AtRestEncryptionEnabled: true
      TransitEncryptionEnabled: true
      AuthToken: !Ref CacheAuthToken
```

### Using Secrets Manager for Auth Token

```yaml
Resources:
  CacheAuthTokenSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub ${AWS::StackName}/elasticache/auth-token
      Description: ElastiCache Redis authentication token
      SecretString: !Sub '{"auth-token":"${CacheAuthToken}"}'

  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheNodeType: cache.r5.large
      NumCacheNodes: 1
      Engine: redis
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
      TransitEncryptionEnabled: true
      AuthToken: !Ref CacheAuthToken
```

## High Availability and Scaling

### Multi-AZ with Automatic Failover

```yaml
Resources:
  RedisReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupDescription: Multi-AZ Redis with failover
      Engine: redis
      CacheNodeType: cache.r5.large
      NumNodeGroups: 1
      ReplicasPerNodeGroup: 2
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

### Memcached Horizontal Scaling

```yaml
Parameters:
  NumCacheNodes:
    Type: Number
    Default: 3
    MinValue: 1
    MaxValue: 20

Resources:
  MemcachedCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheClusterIdentifier: memcached-cluster
      CacheNodeType: cache.m5.xlarge
      NumCacheNodes: !Ref NumCacheNodes
      Engine: memcached
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

### Redis Scaling - Read Replicas

```yaml
Resources:
  RedisReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      ReplicationGroupDescription: Redis with read replicas
      Engine: redis
      CacheNodeType: cache.r5.large
      NumNodeGroups: 1
      ReplicasPerNodeGroup: 3
      AutomaticFailoverEnabled: true
      MultiAZEnabled: true
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup
```

## Best Practices

### Use AWS-Specific Parameter Types

Always use AWS-specific parameter types for validation and easier selection.

```yaml
Parameters:
  CacheNodeType:
    Type: AWS::ElastiCache::CacheCluster::CacheNodeType
    Description: ElastiCache node type

  CacheSubnetGroup:
    Type: AWS::ElastiCache::SubnetGroup::Name
    Description: Cache subnet group

  VpcSecurityGroup:
    Type: AWS::EC2::SecurityGroup::Id
    Description: Security group for cache
```

### Enable Encryption for Production

```yaml
Resources:
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      # Encryption at rest
      AtRestEncryptionEnabled: true
      # Encryption in transit
      TransitEncryptionEnabled: true
      # Authentication
      AuthToken: !Ref CacheAuthToken
```

### Use Multi-AZ for Production

```yaml
Conditions:
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  RedisReplicationGroup:
    Type: AWS::ElastiCache::ReplicationGroup
    Properties:
      AutomaticFailoverEnabled: !If [IsProduction, true, false]
      MultiAZEnabled: !If [IsProduction, true, false]
      ReplicasPerNodeGroup: !If [IsProduction, 2, 1]
```

### Use Proper Naming Conventions

```yaml
Resources:
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${Environment}-${Application}-redis
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName
        - Key: ManagedBy
          Value: CloudFormation
```

### Separate Cache and Application Stacks

```yaml
# cache-stack.yaml - Rarely changes
AWSTemplateFormatVersion: 2010-09-09
Description: Cache infrastructure (VPC, subnets, ElastiCache)
Resources:
  CacheSubnetGroup: AWS::ElastiCache::SubnetGroup
  CacheParameterGroup: AWS::ElastiCache::ParameterGroup
  CacheSecurityGroup: AWS::EC2::SecurityGroup
  CacheCluster: AWS::ElastiCache::Cluster

# application-stack.yaml - Changes frequently
AWSTemplateFormatVersion: 2010-09-09
Description: Application resources
Parameters:
  CacheStackName:
    Type: String
Resources:
  ApplicationConfig: AWS::SSM::Parameter
```

### Use Pseudo Parameters

Use pseudo parameters for region-agnostic templates.

```yaml
Resources:
  CacheCluster:
    Type: AWS::ElastiCache::Cluster
    Properties:
      CacheClusterIdentifier: !Sub ${AWS::StackName}-${AWS::Region}
      Tags:
        - Key: Region
          Value: !Ref AWS::Region
        - Key: AccountId
          Value: !Ref AWS::AccountId
```

### Validate Before Deployment

```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Use cfn-lint for advanced validation
pip install cfn-lint
cfn-lint template.yaml

# Check for AWS-specific issues
cfn-lint template.yaml --region us-east-1
```

## Stack Policies

Stack policies protect critical resources from unintended updates during stack operations.

```yaml
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "Update:Replace",
        "Update:Delete"
      ],
      "Principal": "*",
      "Resource": "LogicalResourceId/CacheCluster"
    },
    {
      "Effect": "Deny",
      "Action": [
        "Update:Replace",
        "Update:Delete"
      ],
      "Principal": "*",
      "Resource": "LogicalResourceId/ReplicationGroup"
    }
  ]
}
```

## Drift Detection

Drift detection identifies when the actual infrastructure configuration differs from the CloudFormation template.

### Detecting Drift

```bash
# Detect drift on entire stack
aws cloudformation detect-stack-drift \
  --stack-name production-elasticache

# Detect drift on specific resources
aws cloudformation detect-stack-drift \
  --stack-name production-elasticache \
  --logical-resource-ids CacheCluster,CacheParameterGroup

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>
```

### Drift Detection Response

```json
{
  "StackResourceDrifts": [
    {
      "LogicalResourceId": "CacheCluster",
      "PhysicalResourceId": "production-cache-cluster",
      "ResourceType": "AWS::ElastiCache::Cluster",
      "StackId": "arn:aws:cloudformation:us-east-1:123456789:stack/production-elasticache/...",
      "DriftStatus": "MODIFIED",
      "PropertyDifferences": [
        {
          "PropertyPath": "NumCacheNodes",
          "ExpectedValue": "3",
          "ActualValue": "2"
        }
      ]
    }
  ]
}
```

## Related Resources

- For advanced patterns: See [EXAMPLES.md](EXAMPLES.md)
- For reference: See [REFERENCE.md](REFERENCE.md)
- AWS CloudFormation User Guide: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
- ElastiCache Documentation: https://docs.aws.amazon.com/AmazonElastiCache/latest/redsug/
- Redis Documentation: https://redis.io/documentation
- Memcached Documentation: https://memcached.org/documentation
