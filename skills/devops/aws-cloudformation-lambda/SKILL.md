---
name: aws-cloudformation-lambda
description: AWS CloudFormation patterns for Lambda functions, layers, event sources, and integrations. Use when creating Lambda functions with CloudFormation, configuring API Gateway, Step Functions, EventBridge, SQS, SNS triggers, and implementing template structure with Parameters, Outputs, Mappings, Conditions, cross-stack references, and best practices for cold start optimization.
category: aws
tags: [aws, cloudformation, lambda, serverless, functions, api-gateway, step-functions, events, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Lambda Serverless

## Overview

Create production-ready serverless infrastructure using AWS CloudFormation templates. This skill covers Lambda functions, layers, event sources, API Gateway, Step Functions, cold start optimization, and best practices for parameters, outputs, and cross-stack references.

## When to Use

Use this skill when:
- Creating new Lambda functions with CloudFormation
- Configuring Lambda layers for shared code
- Integrating Lambda with API Gateway (REST and HTTP API)
- Implementing event sources (SQS, SNS, EventBridge, S3, DynamoDB)
- Creating Step Functions with Lambda workflows
- Optimizing cold start and performance
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references with export/import
- Using Transform for macros and reuse

## CloudFormation Template Structure

### Base Template with Standard Format

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda function with API Gateway integration

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Function Configuration
        Parameters:
          - FunctionName
          - Runtime
          - Handler
      - Label:
          default: Deployment Settings
        Parameters:
          - Environment
          - DeployStage

Parameters:
  FunctionName:
    Type: String
    Default: my-lambda-function
    Description: Name of the Lambda function

  Runtime:
    Type: String
    Default: python3.11
    AllowedValues:
      - python3.8
      - python3.9
      - python3.10
      - python3.11
      - nodejs18.x
      - nodejs20.x
      - java11
      - java17
      - java21

  Handler:
    Type: String
    Default: index.handler

  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

  DeployStage:
    Type: String
    Default: dev

Mappings:
  EnvironmentConfig:
    dev:
      MemorySize: 128
      Timeout: 30
      ReservedConcurrentExecutions: 5
    staging:
      MemorySize: 256
      Timeout: 60
      ReservedConcurrentExecutions: 20
    production:
      MemorySize: 512
      Timeout: 120
      ReservedConcurrentExecutions: 100

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsDev: !Equals [!Ref Environment, dev]

Transform:
  - AWS::Serverless-2016-10-31

Resources:
  # Lambda Function
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Ref FunctionName
      Runtime: !Ref Runtime
      Handler: !Ref Handler
      Code:
        S3Bucket: !Ref SourceBucket
        S3Key: !Sub "lambda/${Environment}/function.zip"
      MemorySize: !FindInMap [EnvironmentConfig, !Ref Environment, MemorySize]
      Timeout: !FindInMap [EnvironmentConfig, !Ref Environment, Timeout]
      Role: !GetAtt LambdaExecutionRole.Arn
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          LOG_LEVEL: !If [IsProduction, INFO, DEBUG]
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName

Outputs:
  LambdaFunctionArn:
    Description: ARN of the Lambda function
    Value: !GetAtt MyLambdaFunction.Arn
    Export:
      Name: !Sub "${AWS::StackName}-LambdaFunctionArn"
```

## Best Practices for Parameters

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  VPCId:
    Type: AWS::EC2::VPC::Id
    Description: VPC where Lambda will run

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnets for Lambda VPC config

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Security groups for Lambda

  LambdaRuntime:
    Type: AWS::Lambda::Runtime
    Description: Lambda runtime selection

  IAMRoleArn:
    Type: AWS::IAM::Role::Arn
    Description: IAM role for Lambda execution

  S3BucketForCode:
    Type: AWS::S3::Bucket
    Description: S3 bucket for Lambda code

  KMSKeyArn:
    Type: AWS::KMS::Key::Arn
    Description: KMS key for environment variables
```

### Parameter Constraints

```yaml
Parameters:
  FunctionName:
    Type: String
    Default: my-function
    Description: Lambda function name
    ConstraintDescription: Must be 1-64 characters, alphanumeric and hyphens
    MinLength: 1
    MaxLength: 64
    AllowedPattern: "[a-zA-Z0-9-_]+"

  MemorySize:
    Type: Number
    Default: 128
    Description: Memory allocation in MB
    MinValue: 128
    MaxValue: 10240
    ConstraintDescription: Must be between 128 and 10240 MB

  Timeout:
    Type: Number
    Default: 30
    Description: Function timeout in seconds
    MinValue: 1
    MaxValue: 900
    ConstraintDescription: Must be between 1 and 900 seconds

  EnvironmentName:
    Type: String
    Default: dev
    Description: Deployment environment
    AllowedValues:
      - dev
      - staging
      - production
    ConstraintDescription: Must be dev, staging, or production
```

### SSM Parameter References

```yaml
Parameters:
  DatabaseConnectionString:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /myapp/database/connection-string
    Description: Database connection string from SSM

  ApiKey:
    Type: AWS::SSM::Parameter::Value<SecureString>
    Default: /myapp/external-api/key
    Description: API key from SSM Parameter Store
```

## Outputs and Cross-Stack References

### Export/Import Patterns

```yaml
# Stack A - Network Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Network infrastructure stack

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-vpc"

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub "${AWS::StackName}-VPCId"

  PublicSubnetIds:
    Description: Public subnet IDs
    Value: !Join [",", [!Ref PublicSubnet1, !Ref PublicSubnet2]]
    Export:
      Name: !Sub "${AWS::StackName}-PublicSubnetIds"

  PrivateSubnetIds:
    Description: Private subnet IDs
    Value: !Join [",", [!Ref PrivateSubnet1, !Ref PrivateSubnet2]]
    Export:
      Name: !Sub "${AWS::StackName}-PrivateSubnetIds"

  LambdaSecurityGroupId:
    Description: Security group ID for Lambda
    Value: !Ref LambdaSecurityGroup
    Export:
      Name: !Sub "${AWS::StackName}-LambdaSecurityGroupId"
```

```yaml
# Stack B - Application Stack (imports from Stack A)
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda application stack

Parameters:
  NetworkStackName:
    Type: String
    Default: network-stack
    Description: Name of the network stack

Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Runtime: python3.11
      Handler: index.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !GetAtt LambdaExecutionRole.Arn
      VpcConfig:
        SecurityGroupIds:
          - !ImportValue
            !Sub "${NetworkStackName}-LambdaSecurityGroupId"
        SubnetIds:
          - !Select [0, !Split [",", !ImportValue !Sub "${NetworkStackName}-PrivateSubnetIds"]]
          - !Select [1, !Split [",", !ImportValue !Sub "${NetworkStackName}-PrivateSubnetIds"]]
```

### Nested Stacks for Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested Lambda stacks

Resources:
  # Nested stack for Lambda functions
  LambdaFunctionsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/lambda-functions.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        FunctionNamePrefix: !Ref FunctionNamePrefix

  # Nested stack for API Gateway
  ApiGatewayStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/api-gateway.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        LambdaFunctionArn: !GetAtt LambdaFunctionsStack.Outputs.FunctionArn
```

## Lambda Functions with Advanced Configurations

### Lambda Base with VPC and Environment

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda function with VPC, environment variables, and monitoring

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

  VpcConfig:
    Type: String
    Default: full
    AllowedValues:
      - none
      - full
      - internal

Resources:
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
        - PolicyName: !Sub "${AWS::StackName}-vpc-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - ec2:CreateNetworkInterface
                  - ec2:DescribeNetworkInterfaces
                  - ec2:DeleteNetworkInterface
                Resource: "*"
        - PolicyName: !Sub "${AWS::StackName}-secrets-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Ref SecretsArn

  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Runtime: python3.11
      Handler: index.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: !Sub "lambda/${Environment}/function.zip"
      MemorySize: 256
      Timeout: 60
      Role: !GetAtt LambdaExecutionRole.Arn
      VpcConfig:
        !If
          - IsFullVpc
          - SecurityGroupIds:
              - !Ref LambdaSecurityGroup
            SubnetIds:
              - !Ref PrivateSubnet1
              - !Ref PrivateSubnet2
          - !Ref AWS::NoValue
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          LOG_LEVEL: !If [IsProduction, INFO, DEBUG]
          DB_HOST: !Ref DatabaseHost
          DB_NAME: !Ref DatabaseName
      TracingConfig:
        Mode: !If [IsProduction, Active, PassThrough]
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName
        - Key: CostCenter
          Value: !Ref CostCenter

  LambdaFunctionUrl:
    Type: AWS::Lambda::Url
    Properties:
      AuthType: AWS_IAM
      TargetFunctionArn: !GetAtt MyLambdaFunction.Arn
      Cors:
        AllowCredentials: true
        AllowHeaders:
          - "*"
        AllowMethods:
          - GET
          - POST
        AllowOrigins:
          - !If [IsProduction, !Ref ProductionCorsOrigin, "*"]
        MaxAge: 86400

Conditions:
  IsFullVpc: !Equals [!Ref VpcConfig, full]
  IsProduction: !Equals [!Ref Environment, production]
```

### Lambda with Provisioned Concurrency

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-api"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/api.zip
      MemorySize: 512
      Timeout: 30
      Role: !GetAtt LambdaExecutionRole.Arn

  ProvisionedConcurrencyConfig:
    Type: AWS::Lambda::ProvisionedConcurrencyConfig
    Properties:
      FunctionName: !Ref MyLambdaFunction
      ProvisionedConcurrentExecutions: 5
      ProvisionedExecutionTarget:
        AllocationStrategy: PRICE_OPTIMIZED
```

## Lambda Layers

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda function with layers

Resources:
  CommonLibraryLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: !Sub "${AWS::StackName}-common-lib"
      Description: Common utilities for Lambda functions
      Content:
        S3Bucket: !Ref LayersBucket
        S3Key: layers/common-lib.zip
      CompatibleRuntimes:
        - python3.9
        - python3.10
        - python3.11
      CompatibleArchitectures:
        - x86_64
        - arm64

  DataProcessingLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: !Sub "${AWS::StackName}-data-processing"
      Description: Data processing utilities
      Content:
        S3Bucket: !Ref LayersBucket
        S3Key: layers/data-processing.zip
      CompatibleRuntimes:
        - python3.11

  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Runtime: python3.11
      Handler: index.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/processor.zip
      Layers:
        - !Ref CommonLibraryLayer
        - !Ref DataProcessingLayer
```

## API Gateway Integration

### API Gateway REST with Lambda Proxy

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: API Gateway REST with Lambda proxy integration

Resources:
  ApiGatewayRestApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: !Sub "${AWS::StackName}-api"
      Description: REST API for Lambda backend
      EndpointConfiguration:
        Types:
          - REGIONAL
      MinimumCompressionSize: 1024
      DisableExecuteApiEndpoint: false

  ApiGatewayResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      ParentId: !GetAtt ApiGatewayRestApi.RootResourceId
      PathPart: items

  ApiGatewayMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      ResourceId: !Ref ApiGatewayResource
      HttpMethod: GET
      AuthorizationType: COGNITO_USER_POOLS
      AuthorizerId: !Ref ApiGatewayAuthorizer
      RequestParameters:
        method.request.querystring.id: true
      Integration:
        Type: AWS_PROXY
        IntegrationHttpMethod: POST
        Uri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${MyLambdaFunction.Arn}/invocations"
        IntegrationResponses:
          - StatusCode: 200
            ResponseParameters:
              method.response.header.Access-Control-Allow-Origin: "'*'"
              method.response.header.Content-Type: "'application/json'"
        PassthroughBehavior: WHEN_NO_MATCH
      MethodResponses:
        - StatusCode: 200
          ResponseModels:
            application/json: Empty
          ResponseParameters:
            method.response.header.Access-Control-Allow-Origin: true

  ApiGatewayDeployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: ApiGatewayMethod
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      StageName: !Ref DeployStage
      StageDescription:
        LoggingLevel: !If [IsProduction, INFO, ERROR]
        DataTraceEnabled: !If [IsProduction, false, true]
        MetricsEnabled: true
        ThrottlingRateLimit: 100
        ThrottlingBurstLimit: 200
      Variables:
        Environment: !Ref Environment

  LambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref MyLambdaFunction
      Action: lambda:InvokeFunction
      Principal: apigateway.amazonaws.com
      SourceArn: !Sub "arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${ApiGatewayRestApi}/*/*/*"

  ApiGatewayAuthorizer:
    Type: AWS::ApiGateway::Authorizer
    Properties:
      Name: !Sub "${AWS::StackName}-authorizer"
      Type: COGNITO_USER_POOLS
      RestApiId: !Ref ApiGatewayRestApi
      ProviderARNs:
        - !Ref CognitoUserPoolArn
      IdentitySource: method.request.header.Authorization
      AuthorizerResultTtlInSeconds: 300

Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub "https://${ApiGatewayRestApi}.execute-api.${AWS::Region}.amazonaws.com/${DeployStage}/items"
```

### API Gateway HTTP API with Lambda

```yaml
Resources:
  HttpApi:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      Name: !Sub "${AWS::StackName}-http-api"
      ProtocolType: HTTP
      CorsConfiguration:
        AllowOrigins:
          - !If [IsProduction, !Ref ProductionDomain, "*"]
        AllowMethods:
          - GET
          - POST
          - PUT
          - DELETE
          - OPTIONS
        AllowHeaders:
          - "*"
        MaxAge: 86400

  HttpApiStage:
    Type: AWS::ApiGatewayV2::Stage
    Properties:
      ApiId: !Ref HttpApi
      StageName: !Ref DeployStage
      AutoDeploy: true
      DefaultRouteSettings:
        DetailedMetricsEnabled: true
        ThrottlingBurstLimit: 100
        ThrottlingRateLimit: 50

  HttpApiIntegration:
    Type: AWS::ApiGatewayV2::Integration
    Properties:
      ApiId: !Ref HttpApi
      IntegrationType: AWS_PROXY
      IntegrationUri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${MyLambdaFunction.Arn}/invocations"
      PayloadFormatVersion: "2.0"

  HttpApiRoute:
    Type: AWS::ApiGatewayV2::Route
    Properties:
      ApiId: !Ref HttpApi
      RouteKey: ANY /items/{id}
      Target: !Sub "integrations/${HttpApiIntegration.Id}"
```

## Event Sources

### SQS Event Source

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-sqs-processor"
      Runtime: python3.11
      Handler: sqs_handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/sqs-processor.zip
      Timeout: 300
      Role: !GetAtt LambdaExecutionRole.Arn

  Queue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "${AWS::StackName}-queue"
      VisibilityTimeout: 360
      MessageRetentionPeriod: 1209600
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 5

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub "${AWS::StackName}-dlq"

  EventSourceMapping:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      FunctionName: !Ref MyLambdaFunction
      EventSourceArn: !GetAtt Queue.Arn
      BatchSize: 10
      MaximumBatchingWindowInSeconds: 60
      ScalingConfig:
        MaximumConcurrency: 10
      FilterCriteria:
        Filters:
          - Pattern: '{"body": {"messageType": ["order", "notification"]}}'
      Enabled: true

  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-sqs-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-dlq-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - sqs:DeleteMessage
                  - sqs:ReceiveMessage
                Resource: !GetAtt DeadLetterQueue.Arn
```

### SNS Event Source

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-sns-processor"
      Runtime: python3.11
      Handler: sns_handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/sns-processor.zip

  Topic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-topic"
      DisplayName: !Sub "${AWS::StackName} Notifications"
      Subscription:
        - Endpoint: !GetAtt MyLambdaFunction.Arn
          Protocol: lambda
      Tags:
        - Key: Environment
          Value: !Ref Environment

  TopicPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      Topics:
        - !Ref Topic
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: sns.amazonaws.com
            Action: sns:Publish
            Resource: !Ref Topic

  LambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref MyLambdaFunction
      Action: lambda:InvokeFunction
      Principal: sns.amazonaws.com
      SourceArn: !Ref Topic
```

### EventBridge (CloudWatch Events)

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-scheduler"
      Runtime: python3.11
      Handler: scheduler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/scheduler.zip
      Timeout: 300
      Role: !GetAtt LambdaExecutionRole.Arn

  ScheduledRule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub "${AWS::StackName}-scheduled-rule"
      ScheduleExpression: "rate(5 minutes)"
      State: ENABLED
      Targets:
        - Id: !Ref MyLambdaFunction
          Arn: !GetAtt MyLambdaFunction.Arn
          RetryPolicy:
            MaximumEventAgeInSeconds: 86400
            MaximumRetryAttempts: 3

  LambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref MyLambdaFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ScheduledRule.Arn
```

### S3 Event Source

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-s3-processor"
      Runtime: python3.11
      Handler: s3_handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/s3-processor.zip
      Timeout: 300
      Role: !GetAtt LambdaExecutionRole.Arn

  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::StackName}-uploads-${AWS::AccountId}-${AWS::Region}"
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      VersioningConfiguration:
        Status: Enabled
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: suffix
                    Value: .csv
            Function: !GetAtt MyLambdaFunction.Arn
          - Event: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: prefix
                    Value: processed/
            Function: !GetAtt MyLambdaFunction.Arn

  LambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref MyLambdaFunction
      Action: lambda:InvokeFunction
      Principal: s3.amazonaws.com
      SourceArn: !GetAtt Bucket.Arn
```

## Step Functions Integration

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Step Functions with Lambda tasks

Resources:
  # Lambda functions for Step Functions
  ProcessItemFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-process-item"
      Runtime: python3.11
      Handler: process_item.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/process-item.zip
      Timeout: 300
      Role: !GetAtt LambdaExecutionRole.Arn

  ValidateItemFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-validate-item"
      Runtime: python3.11
      Handler: validate_item.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/validate-item.zip
      Timeout: 60
      Role: !GetAtt LambdaExecutionRole.Arn

  NotifyCompletionFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-notify-completion"
      Runtime: python3.11
      Handler: notify.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/notify.zip
      Timeout: 60
      Role: !GetAtt LambdaExecutionRole.Arn

  # Step Functions State Machine
  ProcessingStateMachine:
    Type: AWS::StepFunctions::StateMachine
    Properties:
      StateMachineName: !Sub "${AWS::StackName}-processor"
      StateMachineType: STANDARD
      DefinitionString: !Sub |
        {
          "Comment": "Item processing state machine",
          "StartAt": "ValidateItem",
          "States": {
            "ValidateItem": {
              "Type": "Task",
              "Resource": "${ValidateItemFunction.Arn}",
              "Retry": [
                {
                  "ErrorEquals": ["States.TaskFailed"],
                  "IntervalSeconds": 2,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "Next": "ProcessItem"
            },
            "ProcessItem": {
              "Type": "Task",
              "Resource": "${ProcessItemFunction.Arn}",
              "Retry": [
                {
                  "ErrorEquals": ["States.TaskFailed"],
                  "IntervalSeconds": 5,
                  "MaxAttempts": 2,
                  "BackoffRate": 2
                }
              ],
              "Catch": [
                {
                  "ErrorEquals": ["States.ALL"],
                  "Next": "HandleFailure"
                }
              ],
              "Next": "NotifyCompletion"
            },
            "NotifyCompletion": {
              "Type": "Task",
              "Resource": "${NotifyCompletionFunction.Arn}",
              "End": true
            },
            "HandleFailure": {
              "Type": "Pass",
              "End": true
            }
          }
        }
      RoleArn: !GetAtt StepFunctionsExecutionRole.Arn
      LoggingConfiguration:
        Level: ALL
        IncludeExecutionData: true
        Destinations:
          - CloudWatchLogsLogGroup: !Ref StateMachineLogGroup

  StepFunctionsExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-sfn-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: states.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-lambda-invoke"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - lambda:InvokeFunction
                Resource:
                  - !GetAtt ProcessItemFunction.Arn
                  - !GetAtt ValidateItemFunction.Arn
                  - !GetAtt NotifyCompletionFunction.Arn

  StateMachineLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/state-machine/${AWS::StackName}"
      RetentionInDays: 30
```

## Cold Start Optimization

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda function optimized for cold start

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Resources:
  # Use AWS::Serverless::Function for better cold start
  OptimizedLambdaFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-optimized"
      CodeUri: s3://bucket/function.zip
      Handler: app.handler
      Runtime: python3.11
      MemorySize: 512
      Timeout: 30
      EphemeralStorage:
        Size: 1024
      SnapStart:
        ApplyOn: PublishedVersions
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: !If [IsProduction, 5, 0]
      Layers:
        - !Ref CommonDependenciesLayer
      Environment:
        Variables:
          PYTHONPATH: "/var/task:/opt"
      Policies:
        - AWSLambdaVPCAccessExecutionRole
        - AmazonS3ReadOnlyAccess
      VpcConfig:
        SecurityGroupIds:
          - !Ref LambdaSecurityGroup
        SubnetIds: !Ref PrivateSubnetIds
      EventInvokeConfig:
        MaximumEventAgeInSeconds: 3600
        MaximumRetryAttempts: 2

  # Optimized layer with pre-installed dependencies
  CommonDependenciesLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: !Sub "${AWS::StackName}-dependencies"
      Description: Pre-installed Python dependencies for Lambda
      ContentUri: s3://bucket/layers/dependencies.zip
      CompatibleRuntimes:
        - python3.11
      CompatibleArchitectures:
        - x86_64
      RetentionPolicy: Retain

Conditions:
  IsProduction: !Equals [!Ref Environment, production]

Outputs:
  FunctionArn:
    Description: Lambda function ARN
    Value: !GetAtt OptimizedLambdaFunction.Arn
  FunctionUrl:
    Description: Lambda function URL for direct invocation
    Value: !GetAtt OptimizedLambdaFunction.Url
```

## Monitoring and Logging

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda with comprehensive monitoring

Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-monitored"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !GetAtt LambdaExecutionRole.Arn
      TracingConfig:
        Mode: Active

  # Log group with retention
  LambdaLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/lambda/${AWS::StackName}-monitored"
      RetentionInDays: 30
      KmsKeyId: !Ref LogKmsKey

  # Metric filter for errors
  ErrorMetricFilter:
    Type: AWS::Logs::MetricFilter
    Properties:
      LogGroupName: !Ref LambdaLogGroup
      FilterPattern: 'ERROR'
      MetricTransformations:
        - MetricValue: "1"
          MetricNamespace: !Sub "${AWS::StackName}/Lambda"
          MetricName: ErrorCount

  # CloudWatch Alarms
  HighErrorRateAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-high-error-rate"
      AlarmDescription: Alert when error rate exceeds threshold
      MetricName: Errors
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref MyLambdaFunction
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref AlertTopic

  HighThrottlesAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-high-throttles"
      AlarmDescription: Alert when throttling occurs
      MetricName: Throttles
      Namespace: AWS/Lambda
      Dimensions:
        - Name: FunctionName
          Value: !Ref MyLambdaFunction
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 3
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold

  AlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-alerts"

  # Lambda Destination for async invocations
  LambdaDestination:
    Type: AWS::Lambda::EventInvokeConfig
    Properties:
      FunctionName: !Ref MyLambdaFunction
      MaximumEventAgeInSeconds: 3600
      MaximumRetryAttempts: 2
      Qualifier: $LATEST
```

## Conditions and Transform

### Conditions for Environment-Specific Resources

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda with conditional resources

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production
    Description: Deployment environment

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsStaging: !Equals [!Ref Environment, staging]
  CreateDeadLetterQueue: !Or [!Equals [!Ref Environment, staging], !Equals [!Ref Environment, production]]
  EnableXray: !Not [!Equals [!Ref Environment, dev]]

Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: !Sub "lambda/${Environment}/function.zip"
      Timeout: !If [IsProduction, 60, 30]
      MemorySize: !If [IsProduction, 512, 256]
      Role: !GetAtt LambdaExecutionRole.Arn
      TracingConfig: !If
        - EnableXray
        - Mode: Active
        - !Ref AWS::NoValue
      Environment:
        Variables:
          LOG_LEVEL: !If [IsProduction, INFO, DEBUG]

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Condition: CreateDeadLetterQueue
    Properties:
      QueueName: !Sub "${AWS::StackName}-dlq"
```

### Transform for Code Reuse

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Description: Using SAM Transform for Lambda

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Tracing: Active
    Environment:
      Variables:
        LOG_LEVEL: INFO
    Metadata:
      DockerBuild: true
      Dockerfile: Dockerfile
      DockerContext: lambda_function/

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-sam-function"
      Handler: app.handler
      CodeUri: lambda_function/
      Policies:
        - S3ReadPolicy:
            BucketName: !Ref DataBucket
        - DynamoDBReadPolicy:
            TableName: !Ref DataTable
      Events:
        Api:
          Type: Api
          Properties:
            Path: /items
            Method: get
        SqsQueue:
          Type: SQS
          Properties:
            Queue: !GetAtt Queue.Arn
            BatchSize: 10
      AutoPublishAlias: !Ref Environment
      DeploymentPreference:
        Type: !Ref DeploymentConfig
        Alarms:
          - !Ref ErrorAlarm
          - !Ref LatencyAlarm

  DataTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      TableName: !Sub "${AWS::StackName}-table"
      PrimaryKey:
        Name: id
        Type: String

Parameters:
  Environment:
    Type: String
    Default: dev
  DeploymentConfig:
    Type: String
    Default: AllAtOnce
    AllowedValues:
      - Canary10Percent5Minutes
      - Canary10Percent10Minutes
      - Canary10Percent15Minutes
      - AllAtOnce
      - Linear10PercentEvery1Minute
      - Linear10PercentEvery2Minutes
      - Linear10PercentEvery3Minutes
```

## Best Practices

### Security

- Use IAM roles with minimum necessary permissions
- Encrypt environment variables with KMS
- Use VPC for private resource access
- Configure resource-based policies for invocations
- Enable AWS WAF for API Gateway protection
- Use API keys and throttling for protection

### Performance

- Choose memory size based on profiling
- Use provisioned concurrency for critical latency
- Optimize package size for cold start
- Use layers for shared dependencies
- Pre-compile code for interpreted languages
- Consider SnapStart for Java/.NET

### Monitoring

- Enable detailed metrics and tracing
- Configure appropriate log retention
- Create alarms for errors and throttling
- Use Lambda destinations for async error handling
- Implement distributed tracing

### Deployment

- Use change sets before deployment
- Test templates with cfn-lint
- Organize stacks by lifecycle and ownership
- Use nested stacks for modularity
- Implement blue/green deployments

## CloudFormation Stack Management Best Practices

### Stack Policies

Stack policies protect stack resources from unintentional updates that could cause critical changes or deletions.

```yaml
Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      # Function configuration

# Stack policy to protect Lambda function from updates
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
            - Update:Replace
            - Update:Delete
          Resource:
            - LogicalId: LambdaFunction
              ResourceType: AWS::Lambda::Function
          Condition:
            StringEquals:
              ResourceAttribute: Arn:
                Fn::Ref: LambdaFunction
```

### Termination Protection

Enable termination protection to prevent accidental stack deletion, especially for production environments.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda function with termination protection

Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !GetAtt LambdaExecutionRole.Arn

# Enable termination protection (must be set during stack creation)
# This is a stack-level attribute, not a resource
```

**Important**: Termination protection must be enabled during stack creation via AWS Console, CLI, or API:

```bash
aws cloudformation create-stack \
  --stack-name my-lambda-stack \
  --template-body file://template.yaml \
  --enable-termination-protection \
  --capabilities CAPABILITY_IAM
```

### Drift Detection

Detect when infrastructure has diverged from the CloudFormation template.

```yaml
Resources:
  # All Lambda resources support drift detection
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !GetAtt LambdaExecutionRole.Arn
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          LOG_LEVEL: !Ref LogLevel
```

**CLI commands for drift detection:**

```bash
# Detect drift on a stack
aws cloudformation detect-drift --stack-name my-lambda-stack

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>

# Get resource drift status
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-lambda-stack

# Compare actual vs expected resource properties
aws cloudformation get-stack-policy --stack-name my-lambda-stack
```

### Change Sets

Use change sets to preview and review stack changes before execution.

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-function"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !GetAtt LambdaExecutionRole.Arn
      MemorySize: !Ref MemorySize
      Timeout: !Ref Timeout

Parameters:
  MemorySize:
    Type: Number
    Default: 256
    Description: Memory allocation in MB

  Timeout:
    Type: Number
    Default: 30
    Description: Function timeout in seconds
```

**Change set workflow:**

```bash
# 1. Create a change set
aws cloudformation create-change-set \
  --stack-name my-lambda-stack \
  --change-set-name my-changeset \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=MemorySize,ParameterValue=512

# 2. Describe the change set to review changes
aws cloudformation describe-change-set \
  --stack-name my-lambda-stack \
  --change-set-name my-changeset

# 3. Execute the change set
aws cloudformation execute-change-set \
  --stack-name my-lambda-stack \
  --change-set-name my-changeset

# Or delete if changes are not acceptable
aws cloudformation delete-change-set \
  --stack-name my-lambda-stack \
  --change-set-name my-changeset
```

**Change set types:**
- `CREATE`: For new stacks
- `UPDATE`: For existing stacks
- `IMPORT`: For importing existing resources

## Related Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## Additional Files

For complete details on resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
