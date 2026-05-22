---
name: aws-cloudformation-rds
description: AWS CloudFormation patterns for Amazon RDS databases. Use when creating RDS instances (MySQL, PostgreSQL, Aurora), DB clusters, multi-AZ deployments, parameter groups, subnet groups, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references.
category: aws
tags: [aws, cloudformation, rds, database, mysql, postgresql, aurora, mariadb, oracle, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation RDS Database

## Overview

Create production-ready Amazon RDS infrastructure using AWS CloudFormation templates. This skill covers RDS instances (MySQL, PostgreSQL, Aurora, MariaDB), DB clusters, multi-AZ deployments, parameter groups, subnet groups, security groups, template structure best practices, parameter patterns, and cross-stack references for modular, reusable infrastructure as code.

## When to Use

Use this skill when:
- Creating new RDS database instances (MySQL, PostgreSQL, Aurora, MariaDB)
- Configuring DB clusters with read replicas
- Setting up multi-AZ deployments for high availability
- Creating DB parameter groups and option groups
- Configuring DB subnet groups for VPC deployment
- Implementing template Parameters with AWS-specific types
- Creating Outputs for cross-stack references
- Organizing templates with Mappings and Conditions
- Designing reusable, modular CloudFormation templates
- Integrating with Secrets Manager for credential management

## Quick Start

### Basic MySQL RDS Instance

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Simple MySQL RDS instance with basic configuration

Parameters:
  DBInstanceIdentifier:
    Type: String
    Default: mydatabase
    Description: Database instance identifier

  MasterUsername:
    Type: String
    Default: admin
    Description: Master username

  MasterUserPassword:
    Type: String
    NoEcho: true
    Description: Master user password

  DBInstanceClass:
    Type: String
    Default: db.t3.micro
    AllowedValues:
      - db.t3.micro
      - db.t3.small
      - db.t3.medium

Resources:
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subnet group for RDS
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: !Ref DBInstanceIdentifier
      DBInstanceClass: !Ref DBInstanceClass
      Engine: mysql
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      AllocatedStorage: "20"
      StorageType: gp3
      MultiAZ: false

Outputs:
  DBInstanceEndpoint:
    Description: Database endpoint address
    Value: !GetAtt DBInstance.Endpoint.Address

  DBInstancePort:
    Description: Database port
    Value: !GetAtt DBInstance.Endpoint.Port
```

### Aurora MySQL Cluster

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Aurora MySQL cluster with writer and reader instances

Parameters:
  DBClusterIdentifier:
    Type: String
    Default: my-aurora-cluster
    Description: Cluster identifier

  MasterUsername:
    Type: String
    Default: admin

  MasterUserPassword:
    Type: String
    NoEcho: true

Resources:
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subnet group for Aurora
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  DBCluster:
    Type: AWS::RDS::DBCluster
    Properties:
      DBClusterIdentifier: !Ref DBClusterIdentifier
      Engine: aurora-mysql
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      DatabaseName: mydb
      EngineMode: provisioned
      Port: 3306

  DBInstanceWriter:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: !Sub ${DBClusterIdentifier}-writer
      DBClusterIdentifier: !Ref DBCluster
      Engine: aurora-mysql
      DBInstanceClass: db.t3.medium

  DBInstanceReader:
    Type: AWS::RDS::DBInstance
    DependsOn: DBInstanceWriter
    Properties:
      DBInstanceIdentifier: !Sub ${DBClusterIdentifier}-reader
      DBClusterIdentifier: !Ref DBCluster
      Engine: aurora-mysql
      DBInstanceClass: db.t3.medium
      PromotionTier: 2

Outputs:
  ClusterEndpoint:
    Description: Writer endpoint
    Value: !GetAtt DBCluster.Endpoint

  ReaderEndpoint:
    Description: Reader endpoint
    Value: !GetAtt DBCluster.ReadEndpoint
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
Description: My RDS Database Template
```

### Description

Add a description to document the template's purpose. Must appear after the format version.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  This template creates an RDS MySQL instance with:
  - Multi-AZ deployment for high availability
  - Encrypted storage
  - Automated backups
  - Performance Insights enabled
```

### Metadata

Use `Metadata` for additional information about resources or parameters, including AWS::CloudFormation::Interface for parameter grouping.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Database Configuration
        Parameters:
          - DBInstanceIdentifier
          - Engine
          - DBInstanceClass
      - Label:
          default: Credentials
        Parameters:
          - MasterUsername
          - MasterUserPassword
      - Label:
          default: Network
        Parameters:
          - DBSubnetGroupName
          - VPCSecurityGroups
    ParameterLabels:
      DBInstanceIdentifier:
        default: Database Instance ID
      MasterUsername:
        default: Master Username
```

### Resources Section

The `Resources` section is the only required section. It defines AWS resources to provision.

```yaml
Resources:
  # DB Subnet Group (required for VPC deployment)
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subnet group for RDS deployment
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  # DB Parameter Group
  DBParameterGroup:
    Type: AWS::RDS::DBParameterGroup
    Properties:
      Description: Custom parameter group for MySQL
      Family: mysql8.0
      Parameters:
        max_connections: 200
        innodb_buffer_pool_size: 1073741824

  # DB Instance
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: mydbinstance
      DBInstanceClass: db.t3.micro
      Engine: mysql
      MasterUsername: admin
      MasterUserPassword: !Ref DBPassword
      DBSubnetGroupName: !Ref DBSubnetGroup
      DBParameterGroupName: !Ref DBParameterGroup
```

## Parameters

### Parameter Types

Use AWS-specific parameter types for validation and easier selection in the console.

```yaml
Parameters:
  # DB instance identifier
  DBInstanceIdentifier:
    Type: String
    Description: Database instance identifier

  # AWS-specific parameter types for validation
  DBInstanceClass:
    Type: AWS::RDS::DBInstance::InstanceType
    Description: RDS instance class
    Default: db.t3.micro

  # Engine version from SSM
  EngineVersion:
    Type: AWS::RDS::DBInstance::Version
    Description: Database engine version
    Default: 8.0

  # For existing VPC security groups
  VPCSecurityGroups:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Security groups for RDS instance
```

### AWS::RDS::DBInstance::InstanceType Values

Common RDS instance types:

```yaml
Parameters:
  DBInstanceClass:
    Type: String
    AllowedValues:
      - db.t3.micro
      - db.t3.small
      - db.t3.medium
      - db.t3.large
      - db.t3.xlarge
      - db.t3.2xlarge
      - db.m5.large
      - db.m5.xlarge
      - db.m5.2xlarge
      - db.m5.4xlarge
      - db.r5.large
      - db.r5.xlarge
      - db.r5.2xlarge
```

### Parameter Constraints

Add constraints to validate parameter values.

```yaml
Parameters:
  DBInstanceIdentifier:
    Type: String
    Description: Database instance identifier
    Default: mydatabase
    AllowedPattern: "^[a-zA-Z][a-zA-Z0-9]*$"
    ConstraintDescription: Must begin with a letter; contain only alphanumeric characters
    MinLength: 1
    MaxLength: 63

  MasterUsername:
    Type: String
    Description: Master username
    Default: admin
    AllowedPattern: "^[a-zA-Z][a-zA-Z0-9]*$"
    MinLength: 1
    MaxLength: 16
    NoEcho: true

  MasterUserPassword:
    Type: String
    Description: Master user password
    NoEcho: true
    MinLength: 8
    MaxLength: 41
    AllowedPattern: "[a-zA-Z0-9]*"

  AllocatedStorage:
    Type: Number
    Description: Allocated storage in GB
    Default: 20
    MinValue: 20
    MaxValue: 65536

  DBPort:
    Type: Number
    Description: Database port
    Default: 3306
    MinValue: 1150
    MaxValue: 65535
```

### Engine and Version Parameters

```yaml
Parameters:
  Engine:
    Type: String
    Description: Database engine
    Default: mysql
    AllowedValues:
      - mysql
      - postgres
      - oracle-ee
      - oracle-se2
      - sqlserver-ee
      - sqlserver-se
      - sqlserver-ex
      - sqlserver-web
      - aurora
      - aurora-mysql
      - aurora-postgresql
      - mariadb

  EngineVersion:
    Type: String
    Description: Database engine version
    Default: 8.0.35

  DBFamily:
    Type: String
    Description: Parameter group family
    Default: mysql8.0
    AllowedValues:
      - mysql5.6
      - mysql5.7
      - mysql8.0
      - postgres11
      - postgres12
      - postgres13
      - postgres14
      - postgres15
      - postgres16
      - aurora5.6
      - aurora-mysql5.7
      - aurora-mysql8.0
      - aurora-postgresql11
      - aurora-postgresql14
```

### SSM Parameter Types

Reference Systems Manager parameters for dynamic values.

```yaml
Parameters:
  LatestMySQLVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Description: Latest MySQL version from SSM
    Default: /rds/mysql/latest/version

  LatestPostgreSQLVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Description: Latest PostgreSQL version from SSM
    Default: /rds/postgres/latest/version
```

### NoEcho for Sensitive Data

Use `NoEcho` for passwords and sensitive values to mask them in console output.

```yaml
Parameters:
  MasterUserPassword:
    Type: String
    Description: Master user password
    NoEcho: true
    MinLength: 8
    MaxLength: 41
```

## Mappings

Use `Mappings` for static configuration data based on regions or instance types.

```yaml
Mappings:
  InstanceTypeConfig:
    db.t3.micro:
      CPU: 2
      MemoryGiB: 1
      StorageGB: 20
    db.t3.small:
      CPU: 2
      MemoryGiB: 2
      StorageGB: 20
    db.t3.medium:
      CPU: 2
      MemoryGiB: 4
      StorageGB: 20
    db.m5.large:
      CPU: 2
      MemoryGiB: 8
      StorageGB: 100

  RegionDatabasePort:
    us-east-1:
      MySQL: 3306
      PostgreSQL: 5432
    us-west-2:
      MySQL: 3306
      PostgreSQL: 5432
    eu-west-1:
      MySQL: 3306
      PostgreSQL: 5432

Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: !FindInMap [InstanceTypeConfig, !Ref DBInstanceClass, CPU]
      Engine: mysql
      # ...
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
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      MultiAZ: !Ref EnableMultiAZ
      StorageEncrypted: !Ref EnableEncryption
      # Production gets automated backups
      BackupRetentionPeriod: !If [IsProduction, 35, 7]
      DeletionProtection: !If [IsProduction, true, false]
```

### Condition Functions

```yaml
Conditions:
  IsDev: !Equals [!Ref Environment, development]
  IsStaging: !Equals [!Ref Environment, staging]
  IsProduction: !Equals [!Ref Environment, production]

  HasLicense: !Not [!Condition IsDev]

Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      # Use license-included for production
      LicenseModel: !If [HasLicense, "license-included", "bring-your-own-license"]
      # Production uses provisioned IOPS
      StorageType: !If [IsProduction, "io1", "gp3"]
      Iops: !If [IsProduction, 3000, !Ref AWS::NoValue]
```

## Transform

Use `Transform` for macros like AWS::Serverless for SAM templates.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: Serverless RDS application template

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11

Resources:
  RDSFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      CodeUri: function/
      Policies:
        - RDSFullAccessPolicy:
            DBInstanceIdentifier: !Ref DBInstanceIdentifier
      Environment:
        Variables:
          DB_HOST: !GetAtt DBInstance.Endpoint.Address
          DB_NAME: !Ref DBName
          DB_USER: !Ref MasterUsername
```

## Outputs and Cross-Stack References

### Basic Outputs

```yaml
Outputs:
  DBInstanceId:
    Description: Database Instance ID
    Value: !Ref DBInstance

  DBInstanceEndpoint:
    Description: Database endpoint address
    Value: !GetAtt DBInstance.Endpoint.Address

  DBInstancePort:
    Description: Database port
    Value: !GetAtt DBInstance.Endpoint.Port

  DBInstanceArn:
    Description: Database Instance ARN
    Value: !GetAtt DBInstance.Arn

  DBInstanceClass:
    Description: Database Instance Class
    Value: !Ref DBInstanceClass
```

### Exporting Values for Cross-Stack References

Export values so other stacks can import them.

```yaml
Outputs:
  DBInstanceId:
    Description: Database Instance ID for other stacks
    Value: !Ref DBInstance
    Export:
      Name: !Sub ${AWS::StackName}-DBInstanceId

  DBInstanceEndpoint:
    Description: Database endpoint for application stacks
    Value: !GetAtt DBInstance.Endpoint.Address
    Export:
      Name: !Sub ${AWS::StackName}-DBEndpoint

  DBInstancePort:
    Description: Database port for application stacks
    Value: !GetAtt DBInstance.Endpoint.Port
    Export:
      Name: !Sub ${AWS::StackName}-DBPort

  DBConnectionString:
    Description: Full connection string for applications
    Value: !Sub jdbc:mysql://${DBInstanceEndpoint}:${DBInstancePort}/${DBName}
    Export:
      Name: !Sub ${AWS::StackName}-DBConnectionString
```

### Importing Values in Another Stack

```yaml
Parameters:
  # Import via AWS::RDS::DBInstance::Id for console selection
  DBInstanceId:
    Type: AWS::RDS::DBInstance::Id
    Description: RDS instance ID from database stack

  # Or use Fn::ImportValue for programmatic access
  DBEndpoint:
    Type: String
    Description: Database endpoint address

Resources:
  ApplicationDatabaseConfig:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/database/endpoint
      Value: !Ref DBEndpoint
      Type: String
```

### Cross-Stack Reference Pattern

Create a dedicated database stack that exports values:

```yaml
# database-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Database infrastructure stack

Parameters:
  EnvironmentName:
    Type: String
    Default: production

Resources:
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: !Sub Subnet group for ${EnvironmentName}
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass.t3.medium: db
      Engine: mysql
      MasterUsername: admin
      MasterUserPassword: !Ref DBPassword
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      MultiAZ: true
      StorageEncrypted: true

Outputs:
  DBInstanceId:
    Value: !Ref DBInstance
    Export:
      Name: !Sub ${EnvironmentName}-DBInstanceId

  DBEndpoint:
    Value: !GetAtt DBInstance.Endpoint.Address
    Export:
      Name: !Sub ${EnvironmentName}-DBEndpoint

  DBArn:
    Value: !GetAtt DBInstance.Arn
    Export:
      Name: !Sub ${EnvironmentName}-DBArn

  DBSubnetGroupName:
    Value: !Ref DBSubnetGroup
    Export:
      Name: !Sub ${EnvironmentName}-DBSubnetGroupName
```

Application stack imports these values:

```yaml
# application-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack that imports from database stack

Parameters:
  DatabaseStackName:
    Type: String
    Description: Name of the database stack
    Default: database-stack

Resources:
  ApplicationConfig:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/database/endpoint
      Value: !ImportValue
        Fn::Sub: ${DatabaseStackName}-DBEndpoint
      Type: String

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Runtime: python3.11
      Handler: app.handler
      Environment:
        Variables:
          DB_ENDPOINT: !ImportValue
            Fn::Sub: ${DatabaseStackName}-DBEndpoint
```

## RDS Database Components

### DB Subnet Group

Required for VPC deployment. Must include at least 2 subnets in different AZs.

```yaml
Resources:
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subnet group for RDS instance
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
        - !Ref PrivateSubnet3
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-dbsubnet
```

### DB Parameter Group

Custom parameter groups for database configuration.

```yaml
Resources:
  DBParameterGroup:
    Type: AWS::RDS::DBParameterGroup
    Properties:
      Description: Custom parameter group for MySQL 8.0
      Family: mysql8.0
      Parameters:
        # Connection settings
        max_connections: 200
        max_user_connections: 200

        # Memory settings
        innodb_buffer_pool_size: 1073741824
        innodb_buffer_pool_instances: 4

        # Query cache (MySQL 5.7)
        query_cache_type: 1
        query_cache_size: 268435456

        # Timezone
        default_time_zone: "+00:00"

        # Character set
        character_set_server: utf8mb4
        collation_server: utf8mb4_unicode_ci

      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-dbparam
```

### DB Option Group

For database features like Oracle XML or SQL Server features.

```yaml
Resources:
  DBOptionGroup:
    Type: AWS::RDS::DBOptionGroup
    Properties:
      EngineName: oracle-ee
      MajorEngineVersion: "19"
      OptionGroupDescription: Option group for Oracle 19c
      Options:
        - OptionName: OEM
          OptionVersion: "19"
          Port: 5500
          VpcSecurityGroupMemberships:
            - !Ref OEMSecurityGroup
        - OptionName: SSL
          OptionSettings:
            - Name: SQLNET.SSL_VERSION
              Value: "1.2"
```

### DB Instance - MySQL

```yaml
Resources:
  MySQLDBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: mysql-instance
      DBInstanceClass: db.t3.medium
      Engine: mysql
      EngineVersion: "8.0.35"
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      AllocatedStorage: "100"
      StorageType: gp3
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      DBParameterGroupName: !Ref DBParameterGroup
      StorageEncrypted: true
      MultiAZ: true
      BackupRetentionPeriod: 35
      DeletionProtection: true
      EnablePerformanceInsights: true
      PerformanceInsightsRetentionPeriod: 731
      AutoMinorVersionUpgrade: false
      Tags:
        - Key: Environment
          Value: !Ref Environment
```

### DB Instance - PostgreSQL

```yaml
Resources:
  PostgreSQLDBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: postgres-instance
      DBInstanceClass: db.t3.medium
      Engine: postgres
      EngineVersion: "16.1"
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      AllocatedStorage: "100"
      StorageType: gp3
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      DBParameterGroupName: !Ref DBParameterGroup
      StorageEncrypted: true
      MultiAZ: true
      BackupRetentionPeriod: 35
      DeletionProtection: true
      EnablePerformanceInsights: true
      PubliclyAccessible: false
```

### Aurora MySQL Cluster

```yaml
Resources:
  AuroraMySQLCluster:
    Type: AWS::RDS::DBCluster
    Properties:
      DBClusterIdentifier: aurora-mysql-cluster
      Engine: aurora-mysql
      EngineVersion: "8.0.mysql_aurora.3.02.0"
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      DatabaseName: mydb
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      DBClusterParameterGroupName: !Ref AuroraClusterParameterGroup
      StorageEncrypted: true
      EngineMode: provisioned
      Port: 3306
      EnableIAMDatabaseAuthentication: true

  AuroraDBInstanceWriter:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: aurora-writer
      DBClusterIdentifier: !Ref AuroraMySQLCluster
      Engine: aurora-mysql
      DBInstanceClass: db.r5.large
      PromotionTier: 1

  AuroraDBInstanceReader:
    Type: AWS::RDS::DBInstance
    DependsOn: AuroraDBInstanceWriter
    Properties:
      DBInstanceIdentifier: aurora-reader
      DBClusterIdentifier: !Ref AuroraMySQLCluster
      Engine: aurora-mysql
      DBInstanceClass: db.r5.large
      PromotionTier: 2
```

### Aurora PostgreSQL Cluster

```yaml
Resources:
  AuroraPostgresCluster:
    Type: AWS::RDS::DBCluster
    Properties:
      DBClusterIdentifier: aurora-pg-cluster
      Engine: aurora-postgresql
      EngineVersion: "15.4"
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      DatabaseName: mydb
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      StorageEncrypted: true
      EngineMode: provisioned
      Port: 5432

  AuroraPostgresInstanceWriter:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: aurora-pg-writer
      DBClusterIdentifier: !Ref AuroraPostgresCluster
      Engine: aurora-postgresql
      DBInstanceClass: db.r5.large
      PromotionTier: 1

  AuroraPostgresInstanceReader:
    Type: AWS::RDS::DBInstance
    DependsOn: AuroraPostgresInstanceWriter
    Properties:
      DBInstanceIdentifier: aurora-pg-reader
      DBClusterIdentifier: !Ref AuroraPostgresCluster
      Engine: aurora-postgresql
      DBInstanceClass: db.r5.large
      PromotionTier: 2
```

### Aurora Serverless Cluster

```yaml
Resources:
  AuroraServerlessCluster:
    Type: AWS::RDS::DBCluster
    Properties:
      DBClusterIdentifier: aurora-serverless
      Engine: aurora-mysql
      EngineVersion: "5.6.mysql_aurora.2.12.0"
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      DatabaseName: mydb
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      EngineMode: serverless
      ScalingConfiguration:
        AutoPause: true
        MinCapacity: 2
        MaxCapacity: 32
        SecondsUntilAutoPause: 300
```

### DB Cluster Parameter Group (Aurora)

```yaml
Resources:
  AuroraClusterParameterGroup:
    Type: AWS::RDS::DBClusterParameterGroup
    Properties:
      Description: Custom cluster parameter group for Aurora MySQL
      Family: aurora-mysql8.0
      Parameters:
        character_set_server: utf8mb4
        collation_server: utf8mb4_unicode_ci
        max_connections: 1000
        innodb_buffer_pool_size: 2147483648
        slow_query_log: "ON"
        long_query_time: 2
```

## Security and Secrets

### Using Secrets Manager for Credentials

```yaml
Resources:
  DBCredentialsSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub ${AWS::StackName}/rds/credentials
      Description: RDS database credentials
      SecretString: !Sub |
        {
          "username": "${MasterUsername}",
          "password": "${MasterUserPassword}",
          "host": !GetAtt DBInstance.Endpoint.Address,
          "port": !GetAtt DBInstance.Endpoint.Port,
          "dbname": "mydb"
        }

  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: db.t3.medium
      Engine: mysql
      MasterUsername: !Sub "{{resolve:secretsmanager:${DBCredentialsSecret}:SecretString:username}}"
      MasterUserPassword: !Sub "{{resolve:secretsmanager:${DBCredentialsSecret}:SecretString:password}}"
      # ...
```

### DB Security Group (for EC2-Classic)

```yaml
Resources:
  DBSecurityGroup:
    Type: AWS::RDS::DBSecurityGroup
    Properties:
      DBSecurityGroupDescription: Security group for RDS instance
      EC2VpcId: !Ref VPCId
      # For EC2-Classic, use DBSecurityGroupIngress
      DBSecurityGroupIngress:
        - EC2SecurityGroupId: !Ref AppSecurityGroup
        - EC2SecurityGroupName: default
```

### VPC Security Groups (Recommended)

For VPC deployment, use EC2 security groups instead:

```yaml
Resources:
  DBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for RDS
      VpcId: !Ref VPCId
      GroupName: !Sub ${AWS::StackName}-rds-sg
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          SourceSecurityGroupId: !Ref AppSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName}-rds-sg

  AppSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for application
      VpcId: !Ref VPCId
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          DestinationSecurityGroupId: !Ref DBSecurityGroup
```

## High Availability and Multi-AZ

### Multi-AZ Deployment

```yaml
Parameters:
  EnableMultiAZ:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      # Multi-AZ is not supported for Aurora clusters (automatic)
      MultiAZ: !Ref EnableMultiAZ
      # For multi-AZ, use a standby in a different AZ
      AvailabilityZone: !If
        - IsMultiAZ
        - !Select [1, !GetAZs '']
        - !Ref AWS::NoValue
      # For single-AZ, specify no AZ (AWS selects)
```

### Read Replicas

```yaml
Resources:
  # Primary instance
  PrimaryDBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: db.r5.large
      Engine: mysql
      SourceDBInstanceIdentifier: !Ref ExistingDBInstance

  # Read replica in different region
  CrossRegionReadReplica:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: my-cross-region-replica
      SourceDBInstanceIdentifier: !Sub arn:aws:rds:us-west-2:${AWS::AccountId}:db:${PrimaryDBInstance}
      DBInstanceClass: db.r5.large
      Engine: mysql
```

### Enhanced Monitoring and Performance Insights

```yaml
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      EnablePerformanceInsights: true
      PerformanceInsightsRetentionPeriod: 731
      PerformanceInsightsKMSKeyId: !Ref PerformanceInsightsKey

      # Enhanced Monitoring
      MonitoringInterval: 60
      MonitoringRoleArn: !GetAtt MonitoringRole.Arn

      # Database insights
      EnableCloudwatchLogsExports:
        - audit
        - error
        - general
        - slowquery

# IAM Role for Enhanced Monitoring
Resources:
  MonitoringRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: monitoring.rds.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole
```

## Best Practices

### Use AWS-Specific Parameter Types

Always use AWS-specific parameter types for validation and easier selection.

```yaml
Parameters:
  DBInstanceClass:
    Type: AWS::RDS::DBInstance::InstanceType
    Description: RDS instance type

  DBInstanceIdentifier:
    Type: String
    AllowedPattern: "^[a-zA-Z][a-zA-Z0-9]*$"
```

### Enable Encryption at Rest

Always enable encryption for production databases.

```yaml
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      StorageEncrypted: true
      KmsKeyId: !Ref EncryptionKey
```

### Use Multi-AZ for Production

```yaml
Conditions:
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      MultiAZ: !If [IsProduction, true, false]
      BackupRetentionPeriod: !If [IsProduction, 35, 7]
      DeletionProtection: !If [IsProduction, true, false]
```

### Enable Performance Insights

```yaml
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      EnablePerformanceInsights: true
      PerformanceInsightsRetentionPeriod: 731
      PerformanceInsightsKMSKeyId: !Ref PK
```

### Use Proper Naming Conventions

```yaml
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${Environment}-${Application}-rds
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName
        - Key: ManagedBy
          Value: CloudFormation
```

### Use Secrets Manager for Credentials

```yaml
Resources:
  DBCredentials:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub ${AWS::StackName}/rds/credentials
      SecretString: !Sub '{"username":"${MasterUsername}","password":"${MasterUserPassword}"}'

  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      MasterUsername: !Sub "{{resolve:secretsmanager:${DBCredentials}:SecretString:username}}"
      MasterUserPassword: !Sub "{{resolve:secretsmanager:${DBCredentials}:SecretString:password}}"
```

### Separate Database and Application Stacks

```yaml
# database-stack.yaml - Rarely changes
AWSTemplateFormatVersion: 2010-09-09
Description: Database infrastructure (VPC, subnets, RDS instance)
Resources:
  DBSubnetGroup: AWS::RDS::DBSubnetGroup
  DBInstance: AWS::RDS::DBInstance
  DBParameterGroup: AWS::RDS::DBParameterGroup

# application-stack.yaml - Changes frequently
AWSTemplateFormatVersion: 2010-09-09
Description: Application resources
Parameters:
  DatabaseStackName:
    Type: String
Resources:
  ApplicationConfig: AWS::SSM::Parameter
```

### Use Pseudo Parameters

Use pseudo parameters for region-agnostic templates.

```yaml
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: !Sub ${AWS::StackName}-${AWS::Region}
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

Stack policies protect critical resources from unintended updates during stack operations. For RDS databases, this is essential to prevent accidental modifications that could cause data loss or downtime.

### Basic Stack Policy

```yaml
{
  "Statement" : [
    {
      "Effect" : "Allow",
      "Action" : "Update:*",
      "Principal": "*",
      "Resource" : "*"
    },
    {
      "Effect" : "Deny",
      "Action" : "Update:*",
      "Principal": "*",
      "Resource" : "LogicalResourceId/DBInstance"
    },
    {
      "Effect" : "Deny",
      "Action" : "Update:*",
      "Principal": "*",
      "Resource" : "LogicalResourceId/DBCluster"
    }
  ]
}
```

### Stack Policy for Production RDS

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
      "Resource": "LogicalResourceId/DBInstance"
    },
    {
      "Effect": "Deny",
      "Action": [
        "Update:Replace",
        "Update:Delete"
      ],
      "Principal": "*",
      "Resource": "LogicalResourceId/DBCluster"
    },
    {
      "Effect": "Deny",
      "Action": "Update:Delete",
      "Principal": "*",
      "Resource": "LogicalResourceId/DBSubnetGroup"
    },
    {
      "Effect": "Allow",
      "Action": "Update:Modify",
      "Principal": "*",
      "Resource": "LogicalResourceId/DBInstance",
      "Condition": {
        "StringEquals": {
          "ResourceAttribute/StorageEncrypted": "true"
        }
      }
    }
  ]
}
```

### Setting Stack Policy

```bash
# Set stack policy during creation
aws cloudformation create-stack \
  --stack-name my-rds-stack \
  --template-body file://template.yaml \
  --stack-policy-body file://stack-policy.json

# Set stack policy on existing stack
aws cloudformation set-stack-policy \
  --stack-name my-rds-stack \
  --stack-policy-body file://stack-policy.json

# View current stack policy
aws cloudformation get-stack-policy \
  --stack-name my-rds-stack \
  --query StackPolicyBody \
  --output text
```

## Termination Protection

Termination protection is **critical for RDS databases** as it prevents accidental deletion that could result in data loss. This should be enabled for all production databases.

### Enabling Termination Protection

```bash
# Enable termination protection on stack creation
aws cloudformation create-stack \
  --stack-name production-rds \
  --template-body file://template.yaml \
  --enable-termination-protection

# Enable termination protection on existing stack
aws cloudformation update-termination-protection \
  --stack-name production-rds \
  --enable-termination-protection

# Check if termination protection is enabled
aws cloudformation describe-stacks \
  --stack-name production-rds \
  --query 'Stacks[0].EnableTerminationProtection' \
  --output boolean

# Disable termination protection (requires confirmation)
aws cloudformation update-termination-protection \
  --stack-name production-rds \
  --no-enable-termination-protection
```

### Termination Protection in Template

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: RDS instance with termination protection enabled

Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: production-db
      DBInstanceClass: db.r5.large
      Engine: mysql
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      StorageEncrypted: true
      MultiAZ: true
      DeletionProtection: true
      # Termination protection is set at stack level, not resource level
```

### Deletion Protection vs Termination Protection

| Feature | DeletionProtection | Termination Protection |
|---------|-------------------|------------------------|
| **Level** | Resource level (DBInstance) | Stack level |
| **Prevents** | DELETE_DB_INSTANCE API call | CloudFormation stack deletion |
| **Console UI** | Instance settings | Stack settings |
| **Override** | Cannot be overridden | Can be disabled with confirmation |
| **Recommended for** | All production RDS instances | All production stacks with RDS |

### Deletion Protection Best Practice

```yaml
Conditions:
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      # Always enable deletion protection
      DeletionProtection: !If [IsProduction, true, false]
      # Additional production safeguards
      MultiAZ: !If [IsProduction, true, false]
      BackupRetentionPeriod: !If [IsProduction, 35, 7]
```

## Drift Detection

Drift detection identifies when the actual infrastructure configuration differs from the CloudFormation template. This is crucial for RDS to ensure security and compliance.

### Detecting Drift

```bash
# Detect drift on entire stack
aws cloudformation detect-stack-drift \
  --stack-name production-rds

# Detect drift on specific resources
aws cloudformation detect-stack-drift \
  --stack-name production-rds \
  --logical-resource-ids DBInstance,DBParameterGroup

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>

# Check drift status for all resources
aws cloudformation describe-stack-resource-drifts \
  --stack-name production-rds
```

### Drift Detection Status Response

```json
{
  "StackResourceDrifts": [
    {
      "LogicalResourceId": "DBInstance",
      "PhysicalResourceId": "production-db-instance-id",
      "ResourceType": "AWS::RDS::DBInstance",
      "StackId": "arn:aws:cloudformation:us-east-1:123456789:stack/production-rds/...",
      "DriftStatus": "MODIFIED",
      "PropertyDifferences": [
        {
          "PropertyPath": "MultiAZ",
          "ExpectedValue": "true",
          "ActualValue": "false"
        },
        {
          "PropertyPath": "BackupRetentionPeriod",
          "ExpectedValue": "35",
          "ActualValue": "7"
        }
      ]
    }
  ]
}
```

### Automated Drift Detection Schedule

```bash
# Create a Lambda function to check drift weekly
# and send SNS notification if drift is detected

aws events put-rule \
  --name rds-drift-detection \
  --schedule-expression "rate(7 days)"

aws events put-targets \
  --rule rds-drift-detection \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:123456789:function/drift-checker"
```

### Drift Detection Script

```bash
#!/bin/bash
# check-rds-drift.sh

STACK_NAME=$1
DRIFT_STATUS=$(aws cloudformation detect-stack-drift \
  --stack-name $STACK_NAME \
  --query StackDriftStatus \
  --output text 2>/dev/null)

if [ "$DRIFT_STATUS" == "DRIFTED" ]; then
  echo "Drift detected on stack $STACK_NAME"
  aws cloudformation describe-stack-resources \
    --stack-name $STACK_NAME \
    --query 'StackResources[?ResourceStatusReason!=`null`]' \
    --output table
  # Send notification
  aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:123456789:rds-drift-alert \
    --message "Drift detected on stack $STACK_NAME"
else
  echo "No drift detected on stack $STACK_NAME"
fi
```

## Change Sets

Change sets allow you to preview how proposed changes will affect your stack before execution. This is essential for RDS to understand potential impact.

### Creating and Viewing a Change Set

```bash
# Create change set for stack update
aws cloudformation create-change-set \
  --stack-name production-rds \
  --change-set-name preview-changes \
  --template-body file://updated-template.yaml \
  --capabilities CAPABILITY_IAM \
  --change-set-type UPDATE

# List change sets for a stack
aws cloudformation list-change-sets \
  --stack-name production-rds

# Describe change set
aws cloudformation describe-change-set \
  --stack-name production-rds \
  --change-set-name preview-changes

# Execute change set
aws cloudformation execute-change-set \
  --stack-name production-rds \
  --change-set-name preview-changes

# Delete change set (if not executing)
aws cloudformation delete-change-set \
  --stack-name production-rds \
  --change-set-name preview-changes
```

### Change Set Response Example

```json
{
  "ChangeSetName": "preview-changes",
  "ChangeSetId": "arn:aws:cloudformation:us-east-1:123456789:changeSet/...",
  "StackId": "arn:aws:cloudformation:us-east-1:123456789:stack/...",
  "Status": "CREATE_COMPLETE",
  "Changes": [
    {
      "Type": "Resource",
      "ResourceChange": {
        "Action": "Modify",
        "LogicalResourceId": "DBInstance",
        "PhysicalResourceId": "production-db",
        "ResourceType": "AWS::RDS::DBInstance",
        "Replacement": "False",
        "Scope": [
          "Properties"
        ],
        "Details": [
          {
            "Target": {
              "Attribute": "Properties",
              "Name": "MultiAZ"
            },
            "Evaluation": "Static",
            "ChangeSource": "Parameter",
            "BeforeValue": "false",
            "AfterValue": "true"
          }
        ]
      }
    }
  ]
}
```

### Change Set for RDS Modifications

```bash
# Change set that will modify RDS instance class
aws cloudformation create-change-set \
  --stack-name production-rds \
  --change-set-name modify-instance-class \
  --template-body file://modify-instance-template.yaml \
  --parameters parameter-overrides DBInstanceClass=db.r5.xlarge

# Change set for adding read replica
aws cloudformation create-change-set \
  --stack-name production-rds \
  --change-set-name add-read-replica \
  --template-body file://add-replica-template.yaml

# Change set that requires replacement (causes downtime)
aws cloudformation create-change-set \
  --stack-name production-rds \
  --change-set-name change-engine-version \
  --template-body file://change-version-template.yaml
```

### Change Set Types

| Change Set Type | Description | Use Case |
|----------------|-------------|----------|
| `UPDATE` | Creates changes for existing stack | Modifying existing resources |
| `CREATE` | Simulates stack creation | Validating new templates |
| `IMPORT` | Imports existing resources | Moving resources to CloudFormation |

### Change Set Best Practices for RDS

```bash
# Always create change set before updating RDS
aws cloudformation create-change-set \
  --stack-name production-rds \
  --change-set-name pre-update-preview \
  --template-body file://updated-template.yaml

# Review changes carefully
aws cloudformation describe-change-set \
  --stack-name production-rds \
  --change-set-name pre-update-preview \
  --query 'Changes[].ResourceChange'

# Check for replacement operations
aws cloudformation describe-change-set \
  --stack-name production-rds \
  --change-set-name pre-update-preview \
  --query 'Changes[?ResourceChange.Replacement==`True`]'

# Only execute if changes are acceptable
aws cloudformation execute-change-set \
  --stack-name production-rds \
  --change-set-name pre-update-preview
```

## Related Resources

- For advanced patterns: See [EXAMPLES.md](EXAMPLES.md)
- For reference: See [REFERENCE.md](REFERENCE.md)
- AWS CloudFormation User Guide: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
- RDS Documentation: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/
- RDS Best Practices: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html
- Aurora Documentation: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/
