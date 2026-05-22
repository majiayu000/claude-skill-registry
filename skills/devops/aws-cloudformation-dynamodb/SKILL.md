---
name: aws-cloudformation-dynamodb
description: AWS CloudFormation patterns for DynamoDB tables, GSIs, LSIs, auto-scaling, and streams. Use when creating DynamoDB tables with CloudFormation, configuring primary keys, local/global secondary indexes, capacity modes (on-demand/provisioned), point-in-time recovery, encryption, TTL, and implementing template structure with Parameters, Outputs, Mappings, Conditions, cross-stack references.
category: aws
tags: [aws, cloudformation, dynamodb, nosql, database, serverless, tables, indexes, scaling, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation DynamoDB

## Overview

Create production-ready NoSQL database infrastructure using AWS CloudFormation templates. This skill covers DynamoDB tables, primary keys, secondary indexes (GSI/LSI), capacity modes, auto-scaling, encryption, TTL, streams, and best practices for parameters, outputs, and cross-stack references.

## When to Use

Use this skill when:
- Creating new DynamoDB tables with CloudFormation
- Configuring primary keys (partition key, sort key)
- Creating Global Secondary Indexes (GSI) and Local Secondary Indexes (LSI)
- Setting up capacity modes (on-demand or provisioned)
- Implementing auto-scaling with Application Auto Scaling
- Enabling point-in-time recovery and backup
- Configuring encryption at rest and in transit
- Setting up TTL for automatic data expiration
- Enabling DynamoDB Streams for change data capture
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import
- Using Transform for macros and reuse

## CloudFormation Template Structure

### Base Template with Standard Format

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table with GSI and auto-scaling

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Table Configuration
        Parameters:
          - TableName
          - BillingMode
          - PrimaryKeyName
          - PrimaryKeyType
      - Label:
          default: Capacity Settings
        Parameters:
          - ReadCapacityUnits
          - WriteCapacityUnits
          - MinReadCapacity
          - MaxReadCapacity
          - TargetUtilizationPercent

Parameters:
  TableName:
    Type: String
    Default: my-dynamodb-table
    Description: Name of the DynamoDB table

  BillingMode:
    Type: String
    Default: PAY_PER_REQUEST
    AllowedValues:
      - PAY_PER_REQUEST
      - PROVISIONED
    Description: Billing mode for the table

  PrimaryKeyName:
    Type: String
    Default: pk
    Description: Name of the partition key attribute

  PrimaryKeyType:
    Type: String
    Default: S
    AllowedValues:
      - S (String)
      - N (Number)
      - B (Binary)
    Description: Type of the partition key attribute

  ReadCapacityUnits:
    Type: Number
    Default: 5
    Description: Read capacity units (required for PROVISIONED mode)

  WriteCapacityUnits:
    Type: Number
    Default: 5
    Description: Write capacity units (required for PROVISIONED mode)

  MinReadCapacity:
    Type: Number
    Default: 5
    Description: Minimum read capacity for auto-scaling

  MaxReadCapacity:
    Type: Number
    Default: 100
    Description: Maximum read capacity for auto-scaling

  TargetUtilizationPercent:
    Type: Number
    Default: 70
    Description: Target utilization percentage for auto-scaling

Mappings:
  CapacityConfig:
    dev:
      ReadCapacity: 5
      WriteCapacity: 5
      MinRead: 5
      MaxRead: 20
      MinWrite: 5
      MaxWrite: 20
    staging:
      ReadCapacity: 10
      WriteCapacity: 10
      MinRead: 10
      MaxRead: 50
      MinWrite: 10
      MaxWrite: 50
    production:
      ReadCapacity: 25
      WriteCapacity: 25
      MinRead: 25
      MaxRead: 200
      MinWrite: 25
      MaxWrite: 200

Conditions:
  IsProvisioned: !Equals [!Ref BillingMode, PROVISIONED]
  IsDev: !Equals [!Ref Environment, dev]

Resources:
  # DynamoDB Table
  MyDynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Ref TableName
      BillingMode: !Ref BillingMode
      AttributeDefinitions:
        - AttributeName: !Ref PrimaryKeyName
          AttributeType: !Ref PrimaryKeyType
        - AttributeName: sk
          AttributeType: S
        - AttributeName: gsi_pk
          AttributeType: S
        - AttributeName: gsi_sk
          AttributeType: S
      KeySchema:
        - AttributeName: !Ref PrimaryKeyName
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: GSI
          KeySchema:
            - AttributeName: gsi_pk
              KeyType: HASH
            - AttributeName: gsi_sk
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput: !If
            - IsProvisioned
            - ReadCapacityUnits: !FindInMap [CapacityConfig, !Ref Environment, ReadCapacity]
              WriteCapacityUnits: !FindInMap [CapacityConfig, !Ref Environment, WriteCapacity]
            - !Ref AWS::NoValue
      ProvisionedThroughput: !If
        - IsProvisioned
        - ReadCapacityUnits: !FindInMap [CapacityConfig, !Ref Environment, ReadCapacity]
          WriteCapacityUnits: !FindInMap [CapacityConfig, !Ref Environment, WriteCapacity]
        - !Ref AWS::NoValue
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
        SSEType: AES256
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName

Outputs:
  TableName:
    Description: Name of the DynamoDB table
    Value: !Ref MyDynamoDBTable
    Export:
      Name: !Sub "${AWS::StackName}-TableName"

  TableArn:
    Description: ARN of the DynamoDB table
    Value: !GetAtt MyDynamoDBTable.Arn
    Export:
      Name: !Sub "${AWS::StackName}-TableArn"

  TableStreamArn:
    Description: ARN of the DynamoDB table stream
    Value: !GetAtt MyDynamoDBTable.StreamArn
    Export:
      Name: !Sub "${AWS::StackName}-TableStreamArn"
```

## Best Practices for Parameters

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  TableName:
    Type: String
    Description: Name of the DynamoDB table

  TableArn:
    Type: AWS::DynamoDB::Table::Arn
    Description: ARN of existing DynamoDB table

  TableStreamArn:
    Type: AWS::DynamoDB::Table::StreamArn
    Description: Stream ARN of DynamoDB table

  KMSKeyArn:
    Type: AWS::KMS::Key::Arn
    Description: KMS key for server-side encryption

  IAMRoleArn:
    Type: AWS::IAM::Role::Arn
    Description: IAM role for DynamoDB access
```

### Parameter Constraints

```yaml
Parameters:
  TableName:
    Type: String
    Default: my-table
    Description: DynamoDB table name
    ConstraintDescription: Must be 3-255 characters, alphanumeric and underscores
    MinLength: 3
    MaxLength: 255
    AllowedPattern: "[a-zA-Z0-9_]+"

  ReadCapacityUnits:
    Type: Number
    Default: 5
    Description: Read capacity units
    MinValue: 1
    MaxValue: 40000
    ConstraintDescription: Must be between 1 and 40000

  WriteCapacityUnits:
    Type: Number
    Default: 5
    Description: Write capacity units
    MinValue: 1
    MaxValue: 40000
    ConstraintDescription: Must be between 1 and 40000

  BillingMode:
    Type: String
    Default: PAY_PER_REQUEST
    Description: Billing mode
    AllowedValues:
      - PAY_PER_REQUEST
      - PROVISIONED
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Database Stack
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table infrastructure stack

Resources:
  MyDynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-table"
      BillingMode: PROVISIONED
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      ProvisionedThroughput:
        ReadCapacityUnits: 10
        WriteCapacityUnits: 10
      SSESpecification:
        SSEEnabled: true

Outputs:
  TableName:
    Description: Name of the DynamoDB table
    Value: !Ref MyDynamoDBTable
    Export:
      Name: !Sub "${AWS::StackName}-TableName"

  TableArn:
    Description: ARN of the DynamoDB table
    Value: !GetAtt MyDynamoDBTable.Arn
    Export:
      Name: !Sub "${AWS::StackName}-TableArn"

  TableStreamArn:
    Description: Stream ARN for Lambda triggers
    Value: !GetAtt MyDynamoDBTable.StreamArn
    Export:
      Name: !Sub "${AWS::StackName}-TableStreamArn"
```

```yaml
# Stack B - Application Stack (imports from Stack A)
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack using DynamoDB table

Parameters:
  DatabaseStackName:
    Type: String
    Default: database-stack
    Description: Name of the database stack

Resources:
  # Lambda function that uses DynamoDB
  DataProcessorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Runtime: python3.11
      Handler: handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/processor.zip
      Environment:
        Variables:
          TABLE_NAME: !ImportValue
            !Sub "${DatabaseStackName}-TableName"
      Policies:
        - DynamoDBReadPolicy:
            TableName: !ImportValue
              !Sub "${DatabaseStackName}-TableName"
        - DynamoDBWritePolicy:
            TableName: !ImportValue
              !Sub "${DatabaseStackName}-TableName"

  # Lambda trigger from DynamoDB Streams
  StreamProcessorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-stream-processor"
      Runtime: python3.11
      Handler: stream_handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/stream-processor.zip
      EventSourceMapping:
        EventSourceArn: !ImportValue
          !Sub "${DatabaseStackName}-TableStreamArn"
        FunctionName: !Ref StreamProcessorFunction
        StartingPosition: LATEST
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested DynamoDB stacks

Resources:
  # Nested stack for tables
  TablesStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/dynamodb-tables.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        TableNamePrefix: !Ref TableNamePrefix

  # Nested stack for auto-scaling
  AutoScalingStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/dynamodb-autoscaling.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        TableName: !GetAtt TablesStack.Outputs.MainTableName
        ReadCapacityUnits: !GetAtt TablesStack.Outputs.ReadCapacity
        WriteCapacityUnits: !GetAtt TablesStack.Outputs.WriteCapacity
```

## DynamoDB Tables with Advanced Configurations

### Table with GSI and LSI

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table with multiple GSIs and LSIs

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Resources:
  # DynamoDB Table with indexes
  OrdersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-orders"
      BillingMode: PROVISIONED
      AttributeDefinitions:
        # Primary key attributes
        - AttributeName: customer_id
          AttributeType: S
        - AttributeName: order_date
          AttributeType: S
        # GSI attributes
        - AttributeName: status
          AttributeType: S
        - AttributeName: order_total
          AttributeType: N
        - AttributeName: created_at
          AttributeType: S
        # LSI attributes
        - AttributeName: ship_date
          AttributeType: S
      KeySchema:
        - AttributeName: customer_id
          KeyType: HASH
        - AttributeName: order_date
          KeyType: RANGE
      # Global Secondary Indexes
      GlobalSecondaryIndexes:
        # GSI for status-based queries
        - IndexName: StatusIndex
          KeySchema:
            - AttributeName: status
              KeyType: HASH
            - AttributeName: order_date
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 10
            WriteCapacityUnits: 10
        # GSI for total-based queries
        - IndexName: TotalIndex
          KeySchema:
            - AttributeName: status
              KeyType: HASH
            - AttributeName: order_total
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 10
            WriteCapacityUnits: 10
      # Local Secondary Indexes
      LocalSecondaryIndexes:
        - IndexName: ShipDateIndex
          KeySchema:
            - AttributeName: customer_id
              KeyType: HASH
            - AttributeName: ship_date
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      ProvisionedThroughput:
        ReadCapacityUnits: 20
        WriteCapacityUnits: 20
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: DataClassification
          Value: confidential
```

### On-Demand Capacity Table

```yaml
Resources:
  # On-demand capacity table
  EventsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-events"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: event_id
          AttributeType: S
        - AttributeName: event_type
          AttributeType: S
        - AttributeName: timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: event_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: TypeTimestampIndex
          KeySchema:
            - AttributeName: event_type
              KeyType: HASH
            - AttributeName: timestamp
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: KEYS_ONLY
      SSESpecification:
        SSEEnabled: true
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
```

## Auto-Scaling Configuration

### Application Auto Scaling for Provisioned Tables

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table with auto-scaling

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Resources:
  # DynamoDB Table
  MyTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-table"
      BillingMode: PROVISIONED
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
        - AttributeName: gsi_pk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: GSI
          KeySchema:
            - AttributeName: gsi_pk
              KeyType: HASH
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5

  # Scalable Target for Table Read Capacity
  ReadScalingTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: !FindInMap [CapacityConfig, !Ref Environment, MaxReadCapacity]
      MinCapacity: !FindInMap [CapacityConfig, !Ref Environment, MinReadCapacity]
      ResourceId: !Sub "table/${MyTable}"
      RoleARN: !GetAtt AutoScalingRole.Arn
      ScalableDimension: dynamodb:table:ReadCapacityUnits
      ServiceNamespace: dynamodb

  # Scalable Target for Table Write Capacity
  WriteScalingTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: !FindInMap [CapacityConfig, !Ref Environment, MaxWriteCapacity]
      MinCapacity: !FindInMap [CapacityConfig, !Ref Environment, MinWriteCapacity]
      ResourceId: !Sub "table/${MyTable}"
      RoleARN: !GetAtt AutoScalingRole.Arn
      ScalableDimension: dynamodb:table:WriteCapacityUnits
      ServiceNamespace: dynamodb

  # Scalable Target for GSI Read Capacity
  GSIScalingTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 100
      MinCapacity: 5
      ResourceId: !Sub "table/${MyTable}/index/GSI"
      RoleARN: !GetAtt AutoScalingRole.Arn
      ScalableDimension: dynamodb:index:ReadCapacityUnits
      ServiceNamespace: dynamodb

  # Scaling Policy for Read Capacity
  ReadScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-read-scaling"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref ReadScalingTarget
      TargetTrackingScalingPolicyConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: DynamoDBReadCapacityUtilization
        TargetValue: 70
        ScaleInCooldown: 60
        ScaleOutCooldown: 60

  # Scaling Policy for Write Capacity
  WriteScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: !Sub "${AWS::StackName}-write-scaling"
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref WriteScalingTarget
      TargetTrackingScalingPolicyConfiguration:
        PredefinedMetricSpecification:
          PredefinedMetricType: DynamoDBWriteCapacityUtilization
        TargetValue: 70
        ScaleInCooldown: 60
        ScaleOutCooldown: 60

  # Auto Scaling IAM Role
  AutoScalingRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-dynamodb-autoscaling"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: application-autoscaling.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/DynamoDBAutoscaleRole

Mappings:
  CapacityConfig:
    dev:
      MinReadCapacity: 5
      MaxReadCapacity: 20
      MinWriteCapacity: 5
      MaxWriteCapacity: 20
    staging:
      MinReadCapacity: 10
      MaxReadCapacity: 50
      MinWriteCapacity: 10
      MaxWriteCapacity: 50
    production:
      MinReadCapacity: 25
      MaxReadCapacity: 200
      MinWriteCapacity: 25
      MaxWriteCapacity: 200
```

## DynamoDB Streams and Lambda Integration

### Table with Stream for Lambda Trigger

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table with stream for Lambda trigger

Resources:
  # DynamoDB Table with Stream
  OrdersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-orders"
      BillingMode: PROVISIONED
      AttributeDefinitions:
        - AttributeName: order_id
          AttributeType: S
        - AttributeName: customer_id
          AttributeType: S
        - AttributeName: status
          AttributeType: S
      KeySchema:
        - AttributeName: order_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: CustomerIndex
          KeySchema:
            - AttributeName: customer_id
              KeyType: HASH
            - AttributeName: status
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      ProvisionedThroughput:
        ReadCapacityUnits: 10
        WriteCapacityUnits: 10
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES

  # Lambda Function for processing stream
  StreamProcessorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-stream-processor"
      Runtime: python3.11
      Handler: handler.process_event
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/stream-processor.zip
      Timeout: 300
      Role: !GetAtt LambdaExecutionRole.Arn

  # Event Source Mapping
  StreamEventSource:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt OrdersTable.StreamArn
      FunctionName: !Ref StreamProcessorFunction
      StartingPosition: TRIM_HORIZON
      BatchSize: 100
      MaximumBatchingWindowInSeconds: 60
      DestinationConfig:
        OnFailure:
          Destination: !GetAtt DeadLetterQueue.Arn
      Enabled: true

  # Dead Letter Queue for failed events
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "${AWS::StackName}-stream-dlq"
      MessageRetentionPeriod: 86400

  # Lambda Execution Role
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lambda-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-dynamodb-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetRecords
                  - dynamodb:GetShardIterator
                  - dynamodb:DescribeStream
                  - dynamodb:ListStreams
                Resource: !GetAtt OrdersTable.StreamArn
              - Effect: Allow
                Action:
                  - sqs:SendMessage
                Resource: !GetAtt DeadLetterQueue.Arn
```

## TTL Configuration

### Table with Time-to-Live

```yaml
Resources:
  # Table with TTL for automatic data expiration
  SessionsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-sessions"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: session_id
          AttributeType: S
        - AttributeName: user_id
          AttributeType: S
      KeySchema:
        - AttributeName: session_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: UserIndex
          KeySchema:
            - AttributeName: user_id
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: NEW_IMAGE
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      SSESpecification:
        SSEEnabled: true

  # TTL for 24-hour expiration (example)
  SessionCleanupFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-session-cleanup"
      Runtime: python3.11
      Handler: handler.cleanup
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/session-cleanup.zip
      Role: !GetAtt LambdaExecutionRole.Arn

  # Scheduled rule for TTL cleanup
  SessionCleanupRule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub "${AWS::StackName}-session-cleanup"
      ScheduleExpression: "rate(1 hour)"
      State: ENABLED
      Targets:
        - Id: !Ref SessionCleanupFunction
          Arn: !GetAtt SessionCleanupFunction.Arn
```

## Encryption and Security

### Table with Customer Managed KMS Key

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table with customer-managed encryption

Resources:
  # KMS Key for encryption
  DynamoDBKMSKey:
    Type: AWS::KMS::Key
    Properties:
      KeyName: !Sub "${AWS::StackName}-dynamodb-key"
      Description: KMS key for DynamoDB encryption
      KeyPolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: Enable IAM policies
            Effect: Allow
            Principal:
              AWS: !GetAtt IAMRole.Arn
            Action:
              - kms:*
            Resource: "*"
          - Sid: Allow DynamoDB to use the key
            Effect: Allow
            Principal:
              Service: dynamodb.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:GenerateDataKey
              - kms:GenerateDataKeyWithoutPlaintext
            Resource: "*"

  # DynamoDB Table with customer-managed encryption
  SensitiveDataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-sensitive-data"
      BillingMode: PROVISIONED
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
        - AttributeName: category
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      ProvisionedThroughput:
        ReadCapacityUnits: 10
        WriteCapacityUnits: 10
      SSESpecification:
        SSEEnabled: true
        SSEType: KMS
        KMSMasterKeyId: !Ref DynamoDBKMSKey
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true

  # IAM Role for accessing encrypted table
  IAMRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-data-access-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-data-access"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:UpdateItem
                  - dynamodb:DeleteItem
                  - dynamodb:Query
                  - dynamodb:Scan
                Resource: !GetAtt SensitiveDataTable.Arn
              - Effect: Allow
                Action:
                  - kms:Decrypt
                  - kms:GenerateDataKey
                Resource: !GetAtt DynamoDBKMSKey.Arn
```

## Conditions and Transform

### Conditions for Environment-Specific Resources

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB with conditional resources

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

  EnableEncryption:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsDev: !Equals [!Ref Environment, dev]
  EnableEncryption: !Equals [!Ref EnableEncryption, true]
  EnablePITR: !Not [!Equals [!Ref Environment, dev]]
  EnableStream: !Or [!Equals [!Ref Environment, staging], !Equals [!Ref Environment, production]]

Resources:
  # Main table
  MyTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-table"
      BillingMode: !If [IsProduction, PROVISIONED, PAY_PER_REQUEST]
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      ProvisionedThroughput: !If
        - IsProduction
        - ReadCapacityUnits: 25
          WriteCapacityUnits: 25
        - !Ref AWS::NoValue
      StreamSpecification: !If
        - EnableStream
        - StreamViewType: NEW_AND_OLD_IMAGES
        - !Ref AWS::NoValue
      SSESpecification: !If
        - EnableEncryption
        - SSEEnabled: true
          SSEType: AES256
        - !Ref AWS::NoValue
      PointInTimeRecoverySpecification: !If
        - EnablePITR
        - PointInTimeRecoveryEnabled: true
        - !Ref AWS::NoValue
```

### Transform for SAM Template

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Description: Using SAM Transform for DynamoDB

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Environment:
      Variables:
        TABLE_NAME: !Ref DataTable

Resources:
  # SAM Simple Table (creates table with on-demand capacity)
  DataTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      TableName: !Sub "${AWS::StackName}-data"
      PrimaryKey:
        Name: id
        Type: String
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
      SSESpecification:
        SSEEnabled: true

  # Lambda function with DynamoDB access
  DataHandler:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-handler"
      Handler: handler.handler
      CodeUri: lambda/
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable
      Events:
        Api:
          Type: Api
          Properties:
            Path: /data
            Method: post
```

## Best Practices

### Security

- Enable server-side encryption (SSE) for all tables
- Use customer-managed KMS keys for sensitive data
- Enable point-in-time recovery for production tables
- Use IAM policies with minimum necessary permissions
- Enable VPC endpoints for private table access
- Configure AWS CloudTrail for auditing

### Performance

- Choose partition keys with uniform distribution
- Use GSIs for alternative access patterns
- Monitor consumed capacity and throttled requests
- Use auto-scaling for variable workloads
- Consider on-demand capacity for unpredictable traffic
- Implement proper data modeling for query patterns

### Monitoring

- Enable CloudWatch metrics with 1-minute granularity
- Create alarms for throttled requests
- Monitor table and index capacity utilization
- Use AWS DynamoDB Accelerator (DAX) for read-heavy workloads
- Implement proper error handling and retries

### Cost Optimization

- Use on-demand capacity when appropriate
- Right-size provisioned capacity based on metrics
- Use auto-scaling to handle peak loads
- Consider TTL for automatic data cleanup
- Archive old data to S3 with Data Pipeline or Glue

## CloudFormation Stack Management Best Practices

### Stack Policies

```yaml
Resources:
  DynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-table"

# Stack policy to protect table from deletion
StackPolicy:
  Type: AWS::CloudFormation::StackPolicy
  Properties:
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal: "*"
          Action: "Update:*"
          Resource: "*"
        - Effect: Deny
          Principal: "*"
          Action:
            - Update:Delete
          Resource:
            - LogicalId: DynamoDBTable
```

### Drift Detection

```bash
# Detect drift on a stack
aws cloudformation detect-drift --stack-name my-dynamodb-stack

# Get resource drift status
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-dynamodb-stack
```

## Related Resources

- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Application Auto Scaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html)

## Additional Files

For complete details on resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all DynamoDB CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
