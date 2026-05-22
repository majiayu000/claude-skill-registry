---
name: aws-cloudformation-iam
description: AWS CloudFormation patterns for IAM users, roles, policies, and managed policies. Use when creating IAM resources with CloudFormation, implementing least privilege access, configuring cross-account access, setting up identity centers, managing permissions boundaries, and organizing template structure with Parameters, Outputs, Mappings, Conditions for secure infrastructure deployments.
category: aws
tags: [aws, cloudformation, iam, security, authentication, authorization, roles, policies, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation IAM Security

Create production-ready IAM infrastructure using AWS CloudFormation templates. This skill covers users, roles, policies, managed policies, permission boundaries, and best practices for implementing least privilege access.

## When to Use

Use this skill when:
- Creating new IAM users with CloudFormation
- Configuring IAM roles for AWS services
- Defining inline policies and managed policies
- Implementing cross-account access with STS
- Creating permission boundaries
- Organizing templates with Parameters, Outputs, Mappings, Conditions
- Implementing cross-stack references for IAM resources
- Configuring IAM Identity Center (SSO)
- Managing service control policies (SCP)

## CloudFormation Template Structure

### Standard Format Base Template

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM infrastructure with users, roles, and policies

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: User Configuration
        Parameters:
          - UserName
          - UserPermissionsBoundary
      - Label:
          default: Role Configuration
        Parameters:
          - RoleName
          - AssumeRolePolicyService

Parameters:
  UserName:
    Type: String
    Default: app-user
    Description: Name of the IAM user
    MinLength: 1
    MaxLength: 64

  UserPermissionsBoundary:
    Type: String
    Description: IAM policy ARN for permissions boundary
    Default: ""

  RoleName:
    Type: String
    Default: app-execution-role
    Description: Name of the IAM role

  AssumeRolePolicyService:
    Type: String
    Default: lambda.amazonaws.com
    Description: Service that can assume the role
    AllowedValues:
      - lambda.amazonaws.com
      - ec2.amazonaws.com
      - ecs-tasks.amazonaws.com
      - eks.amazonaws.com
      - states.amazonaws.com

Mappings:
  EnvironmentConfig:
    dev:
      MaxSessionDuration: 3600
      PolicyArns: []
    staging:
      MaxSessionDuration: 7200
      PolicyArns:
        - arn:aws:iam::aws:policy/ReadOnlyAccess
    production:
      MaxSessionDuration: 43200
      PolicyArns:
        - arn:aws:iam::aws:policy/ReadOnlyAccess
        - arn:aws:iam::aws:policy/SecurityAudit

Conditions:
  HasPermissionsBoundary: !Not [!Equals [!Ref UserPermissionsBoundary, ""]]
  IsProduction: !Equals [!Ref Environment, production]

Transform:
  - AWS::Serverless-2016-10-31

Resources:
  # IAM User
  AppUser:
    Type: AWS::IAM::User
    Properties:
      UserName: !Ref UserName
      PermissionsBoundary: !If
        - HasPermissionsBoundary
        - !Ref UserPermissionsBoundary
        - !Ref AWS::NoValue
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName

Outputs:
  UserArn:
    Description: ARN of the IAM user
    Value: !GetAtt AppUser.Arn
    Export:
      Name: !Sub "${AWS::StackName}-UserArn"
```

## Parameters Best Practices

### AWS-Specific Parameter Types

```yaml
Parameters:
  # AWS-specific types for validation
  UserArn:
    Type: AWS::IAM::User::Arn
    Description: IAM user ARN for reference

  RoleArn:
    Type: AWS::IAM::Role::Arn
    Description: IAM role ARN for reference

  PolicyArn:
    Type: AWS::IAM::Policy::Arn
    Description: IAM policy ARN

  ManagedPolicyArn:
    Type: AWS::IAM::ManagedPolicy::Arn
    Description: AWS managed policy ARN

  InstanceProfileArn:
    Type: AWS::IAM::InstanceProfile::Arn
    Description: IAM instance profile ARN

  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy::Resource
    Description: S3 bucket policy reference
```

### Parameter Constraints

```yaml
Parameters:
  UserName:
    Type: String
    Default: app-user
    Description: IAM username
    MinLength: 1
    MaxLength: 64
    ConstraintDescription: Must be 1-64 characters
    AllowedPattern: "[a-zA-Z0-9+=,.@_-]+"

  RoleName:
    Type: String
    Default: execution-role
    Description: IAM role name
    MinLength: 1
    MaxLength: 64
    ConstraintDescription: Must be 1-64 characters
    AllowedPattern: "[a-zA-Z0-9+=,.@_-]+"

  MaxSessionDuration:
    Type: Number
    Default: 3600
    Description: Maximum session duration in seconds
    MinValue: 900
    MaxValue: 43200
    ConstraintDescription: Must be between 900 and 43200 seconds

  AccessKeyRotationFrequency:
    Type: Number
    Default: 90
    Description: Days between access key rotations
    MinValue: 1
    MaxValue: 365
    ConstraintDescription: Must be between 1 and 365 days
```

### SSM Parameter References per Policy ARNs

```yaml
Parameters:
  ReadOnlyPolicyArn:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /iam/policies/read-only-arn
    Description: ARN of the read-only policy from SSM

  CustomPolicyDocument:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /iam/policies/custom-policy-json
    Description: Policy document from SSM Parameter Store
```

## Outputs and Cross-Stack References

### Export/Import Patterns for IAM

```yaml
# Stack A - IAM Core Stack
AWSTemplateFormatVersion: 2010-09-09
Description: Core IAM infrastructure stack

Resources:
  # Execution Role for applications
  ApplicationExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-execution-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      MaxSessionDuration: 3600

  # Role for Cross-Account Access
  CrossAccountReadRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-crossaccount-read"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${TargetAccountId}:root"
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                sts:Externalid: !Ref ExternalId
      Policies:
        - PolicyName: ReadOnlyAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:GetObjectVersion
                Resource: !Ref SourceBucketArn
              - Effect: Allow
                Action:
                  - dynamodb:Query
                  - dynamodb:Scan
                  - dynamodb:GetItem
                Resource: !Ref SourceTableArn

Outputs:
  ApplicationExecutionRoleArn:
    Description: ARN of the application execution role
    Value: !GetAtt ApplicationExecutionRole.Arn
    Export:
      Name: !Sub "${AWS::StackName}-ExecutionRoleArn"

  CrossAccountReadRoleArn:
    Description: ARN for cross-account read access
    Value: !GetAtt CrossAccountReadRole.Arn
    Export:
      Name: !Sub "${AWS::StackName}-CrossAccountReadRoleArn"

  CrossAccountReadRoleExternalId:
    Description: External ID for cross-account role assumption
    Value: !Ref ExternalId
    Export:
      Name: !Sub "${AWS::StackName}-CrossAccountExternalId"
```

```yaml
# Stack B - Application Stack (imports from IAM Stack)
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack importing IAM roles

Parameters:
  IAMStackName:
    Type: String
    Default: iam-core
    Description: Name of the IAM stack

Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Runtime: python3.11
      Handler: app.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/function.zip
      Role: !ImportValue
        !Sub "${IAMStackName}-ExecutionRoleArn"
      Environment:
        Variables:
          TARGET_BUCKET: !Ref TargetBucket
```

### Nested Stacks for IAM Modularity

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Main stack with nested IAM stacks

Resources:
  # Nested stack for users
  IAMUsersStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/iam-users.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        UserNames: !Ref UserNames

  # Nested stack for roles
  IAMRolesStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/iam-roles.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
        TrustedServices: !Ref TrustedServices

  # Nested stack for policies
  IAMPoliciesStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/iam-policies.yaml
      TimeoutInMinutes: 15
      Parameters:
        Environment: !Ref Environment
```

## IAM Users

### User with Access Keys

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM user with programmatic access

Resources:
  AppUser:
    Type: AWS::IAM::User
    Properties:
      UserName: !Sub "${AWS::StackName}-app-user"
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName

  UserAccessKey:
    Type: AWS::IAM::AccessKey
    Properties:
      UserName: !Ref AppUser
      Status: Active
      Serial: 1

  UserSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/iam-user-credentials"
      Description: IAM user access key credentials
      SecretString: !Sub |
        {
          "username": "${AppUser.UserName}",
          "access_key": "${UserAccessKey.Ref}",
          "secret_key": "{{resolve:secretsmanager:${UserAccessKey.SecretAccessKey}}}"
        }

Outputs:
  AccessKeyId:
    Description: Access Key ID for the user
    Value: !Ref UserAccessKey
    Export:
      Name: !Sub "${AWS::StackName}-AccessKeyId"

  SecretArn:
    Description: ARN of the secret containing credentials
    Value: !Ref UserSecret
```

### User with Console Password

```yaml
Resources:
  ConsoleUser:
    Type: AWS::IAM::User
    Properties:
      UserName: !Sub "${AWS::StackName}-console-user"

  UserLoginProfile:
    Type: AWS::IAM::UserLoginProfile
    Properties:
      UserName: !Ref ConsoleUser
      Password: !Ref InitialPassword
      PasswordResetRequired: true

  UserPasswordSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/console-password"
      Description: Initial console login password
      SecretString: !Ref InitialPassword
```

### User with Permissions Boundary

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM user with permissions boundary

Resources:
  # Permissions boundary policy
  ReadOnlyBoundaryPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      Description: Read-only permissions boundary
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Deny
            Action: "*"
            Resource: "*"
            NotPrincipal:
              - !GetAtt ReadOnlyRole.Arn

  AppUser:
    Type: AWS::IAM::User
    Properties:
      UserName: !Sub "${AWS::StackName}-restricted-user"
      PermissionsBoundary: !Ref ReadOnlyBoundaryPolicy
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/ReadOnlyAccess
```

## IAM Roles

### Role for Lambda Execution

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Lambda execution role with least privilege

Resources:
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-lambda-execution"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
        - arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-dynamodb-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:Query
                  - dynamodb:Scan
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:UpdateItem
                  - dynamodb:DeleteItem
                Resource: !GetAtt DataTable.Arn
                Condition:
                  StringEquals:
                    dynamodb:TableName: !Ref TableName
              - Effect: Allow
                Action:
                  - dynamodb:DescribeTable
                Resource: "*"
        - PolicyName: !Sub "${AWS::StackName}-secrets-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                  - secretsmanager:DescribeSecret
                Resource: !Ref SecretsArn
        - PolicyName: !Sub "${AWS::StackName}-kms-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - kms:Decrypt
                  - kms:DescribeKey
                Resource: !Ref KmsKeyArn

  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Ref TableName
      BillingMode: PAY_PER_REQUEST
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
```

### Role for ECS Tasks

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: ECS task execution role

Resources:
  ECSTaskExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-ecs-task-execution"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-ecr-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - ecr:GetDownloadUrlForLayer
                  - ecr:BatchGetImage
                  - ecr:BatchCheckLayerAvailability
                Resource: !Ref EcrRepositoryArn
              - Effect: Allow
                Action:
                  - ecr:GetAuthorizationToken
                Resource: "*"
        - PolicyName: !Sub "${AWS::StackName}-cloudwatch-logs"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:CreateLogGroup
                Resource: !Ref LogGroupArn

  ECSTaskRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-ecs-task"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-app-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - sqs:ReceiveMessage
                  - sqs:DeleteMessage
                  - sqs:GetQueueAttributes
                Resource: !GetAtt Queue.Arn
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref TopicArn
```

### Role for Cross-Account Access

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Cross-account access role

Parameters:
  SourceAccountId:
    Type: String
    Description: AWS account ID that can assume this role

  ExternalId:
    Type: String
    Description: External ID for trust relationship

Resources:
  CrossAccountReadRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-crossaccount-read"
      Description: Role for cross-account read access
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${SourceAccountId}:root"
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                sts:Externalid: !Ref ExternalId
              IpAddress:
                aws:SourceIp:
                  - 10.0.0.0/8
                  - 172.16.0.0/12
      MaxSessionDuration: 7200
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-s3-read"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:GetObjectVersion
                  - s3:ListBucket
                Resource:
                  - !Ref SourceBucketArn
                  - !Sub "${SourceBucketArn}/*"
        - PolicyName: !Sub "${AWS::StackName}-dynamodb-read"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:Query
                  - dynamodb:Scan
                  - dynamodb:GetItem
                  - dynamodb:DescribeTable
                Resource:
                  - !GetAtt SourceTable.Arn
                  - !Sub "${GetAtt SourceTable.Arn}/index/*"

Outputs:
  RoleArn:
    Description: ARN of the cross-account role
    Value: !GetAtt CrossAccountReadRole.Arn
    Export:
      Name: !Sub "${AWS::StackName}-CrossAccountRoleArn"
```

### Role for API Gateway with Cognito

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: API Gateway execution role for Cognito authorization

Resources:
  ApiGatewayCognitoAuthorizerRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-apigw-cognito-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: apigateway.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-cognito-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - cognito-idp:DescribeUserPool
                  - cognito-idp:DescribeUserPoolClient
                Resource: !Ref UserPoolArn

  ApiGatewayExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-apigw-execution"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: apigateway.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-lambda-invoke"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - lambda:InvokeFunction
                Resource: !Ref LambdaFunctionArn
```

### Role for EKS Pods

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM role for EKS pod execution

Resources:
  EKSPodRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-eks-pod-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                aws:SourceArn: !Sub "arn:aws:eks:${AWS::Region}:${AWS::AccountId}:cluster/${EKSClusterName}"
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/SecretsManagerReadWrite
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-s3-read"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:GetObjectVersion
                Resource: !Sub "${DataBucketArn}/*"

  EKSPodExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-eks-execution"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
        - arn:aws:iam::aws:policy/CloudWatchLogsReadOnly
```

### Role for CodeBuild

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM role for CodeBuild project

Resources:
  CodeBuildRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-codebuild-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: codebuild.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-source-access"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:GetObjectVersion
                Resource:
                  - !Ref SourceBucketArn
                  - !Sub "${SourceBucketArn}/*"
              - Effect: Allow
                Action:
                  - s3:PutObject
                Resource:
                  - !Ref BuildOutputBucketArn
                  - !Sub "${BuildOutputBucketArn}/*"
              - Effect: Allow
                Action:
                  - codecommit:GitPull
                Resource: !Ref CodecommitRepositoryArn
              - Effect: Allow
                Action:
                  - codebuild:CreateReportGroup
                  - codebuild:CreateReport
                  - codebuild:UpdateReport
                  - codebuild:BatchPutTestCases
                  - codebuild:BatchPutCodeCoverages
                Resource: "*"
```

### Role for Step Functions

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM role for Step Functions state machine

Resources:
  StepFunctionsExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-stepfunctions-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: states.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-lambda-tasks"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - lambda:InvokeFunction
                  - lambda:InvokeAsync
                Resource:
                  - !Ref ProcessFunctionArn
                  - !Ref ValidateFunctionARN
                  - !Ref NotifyFunctionArn
        - PolicyName: !Sub "${AWS::StackName}-dynamodb-tasks"
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
                Resource:
                  - !GetAtt WorkflowTable.Arn
                  - !Sub "${GetAtt WorkflowTable.Arn}/*"
        - PolicyName: !Sub "${AWS::StackName}-sns-tasks"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref NotificationTopicArn
        - PolicyName: !Sub "${AWS::StackName}-events"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - events:PutTargets
                  - events:PutRule
                  - events:DescribeRule
                Resource: "*"
```

## IAM Policies

### Inline Policy for S3 Access

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Role with S3 access policies

Resources:
  S3AccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-s3-access"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-s3-readonly"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:GetObjectVersion
                  - s3:GetBucketPolicy
                  - s3:GetBucketPolicyStatus
                Resource:
                  - !Ref DataBucketArn
                  - !Sub "${DataBucketArn}/*"
              - Effect: Allow
                Action:
                  - s3:ListBucket
                Resource: !Ref DataBucketArn
                Condition:
                  StringLike:
                    s3:prefix:
                      - ""
                      - "documents/*"
                      - "reports/*"

        - PolicyName: !Sub "${AWS::StackName}-s3-write"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:PutObject
                  - s3:PutObjectAcl
                  - s3:DeleteObject
                Resource: !Sub "${DataBucketArn}/processed/*"
```

### Custom Managed Policy

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Custom managed policy for DynamoDB access

Resources:
  DynamoDBFullAccessPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      Description: Full access to specific DynamoDB tables
      ManagedPolicyName: !Sub "${AWS::StackName}-dynamodb-full-access"
      Groups:
        - !Ref AppUserGroup
      Roles:
        - !Ref AppExecutionRole
      Users:
        - !Ref AppUser
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Action:
              - dynamodb:CreateTable
              - dynamodb:UpdateTable
              - dynamodb:DeleteTable
              - dynamodb:DescribeTable
              - dynamodb:DescribeTimeToLive
              - dynamodb:ListTagsOfResource
            Resource: !GetAtt DataTable.Arn
          - Effect: Allow
            Action:
              - dynamodb:Query
              - dynamodb:Scan
              - dynamodb:GetItem
              - dynamodb:PutItem
              - dynamodb:UpdateItem
              - dynamodb:DeleteItem
              - dynamodb:BatchGetItem
              - dynamodb:BatchWriteItem
            Resource:
              - !GetAtt DataTable.Arn
              - !Sub "${GetAtt DataTable.Arn}/index/*"
          - Effect: Allow
            Action:
              - dynamodb:DescribeLimits
              - dynamodb:ListTables
            Resource: "*"
```

### Policy with Conditions

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Policy with IP and time-based conditions

Resources:
  RestrictedAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-restricted-access"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-conditional-access"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub "${DataBucketArn}/*"
                Condition:
                  IpAddress:
                    aws:SourceIp:
                      - 10.0.0.0/8
                      - 192.168.1.0/24
                  StringEquals:
                    s3:ExistingObjectTag/classification: internal
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:Query
                Resource: !GetAtt DataTable.Arn
                Condition:
                  StringEquals:
                    dynamodb:Select: SPECIFIC_ATTRIBUTES
                    dynamodb:Attributes:
                      - id
                      - name
                      - status
```

## Permission Boundaries

### Permission Boundary for Developers

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Permission boundary for developer roles

Resources:
  DeveloperBoundaryPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      Description: Permission boundary for developers - denies production write access
      ManagedPolicyName: !Sub "${AWS::StackName}-developer-boundary"
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Deny
            Action:
              - "*"
            Resource: "*"
            Condition:
              StringEquals:
                aws:RequestedRegion:
                  - us-east-1
                  - us-west-2
              StringLike:
                aws:ResourceTag/environment:
                  - production
                  - prod
          - Effect: Deny
            Action:
              - iam:CreateUser
              - iam:DeleteUser
              - iam:PutUserPolicy
              - iam:AttachUserPolicy
              - iam:DetachUserPolicy
            Resource: "*"
          - Effect: Deny
            Action:
              - iam:CreateRole
              - iam:DeleteRole
              - iam:AttachRolePolicy
              - iam:DetachRolePolicy
            Resource: "*"
          - Effect: Allow
            Action:
              - s3:Get*
              - s3:List*
            Resource: "*"
          - Effect: Allow
            Action:
              - dynamodb:Get*
              - dynamodb:Query
              - dynamodb:Scan
            Resource: "*"
          - Effect: Allow
            Action:
              - lambda:InvokeFunction
              - lambda:GetFunction
            Resource: "*"

  DeveloperRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-developer"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Ref DeveloperUserArn
            Action: sts:AssumeRole
      PermissionsBoundary: !Ref DeveloperBoundaryPolicy
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/ReadOnlyAccess
```

## IAM Identity Center (SSO)

### SSO Permission Set

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM Identity Center permission set

Resources:
  SSOPermissionSet:
    Type: AWS::SSO::PermissionSet
    Properties:
      InstanceArn: !Ref SSOInstanceArn
      PermissionSetName: !Sub "${AWS::StackName}-admin-permissions"
      Description: Administrator access permission set
      SessionDuration: PT8H
      RelayStateType: sso.amazonaws.com
      ManagedPolicies:
        - arn:aws:iam::aws:policy/AdministratorAccess
      InlinePolicy: |
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "aws-portal:*Billing",
                "aws-portal:*Usage"
              ],
              "Resource": "*"
            }
          ]
        }

  SSOAssignment:
    Type: AWS::SSO::AccountAssignment
    Properties:
      InstanceArn: !Ref SSOInstanceArn
      PermissionSetArn: !Ref SSOPermissionSet
      PrincipalId: !Ref SSOGroupId
      PrincipalType: GROUP
      TargetId: !Ref TargetAWSAccountId
      TargetType: AWS_ACCOUNT
```

### SSO Custom Policy with Conditions

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: SSO permission set with custom policies

Resources:
  ReadOnlyPermissionSet:
    Type: AWS::SSO::PermissionSet
    Properties:
      InstanceArn: !Ref SSOInstanceArn
      PermissionSetName: !Sub "${AWS::StackName}-read-only"
      Description: Read-only access for auditors
      SessionDuration: PT4H
      ManagedPolicies:
        - arn:aws:iam::aws:policy/ReadOnlyAccess
      InlinePolicy: |
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:ListBucket"
              ],
              "Resource": [
                "arn:aws:s3:::${DataBucketArn}",
                "arn:aws:s3:::${DataBucketArn}/*"
              ]
            },
            {
              "Effect": "Deny",
              "Action": [
                "s3:DeleteObject",
                "s3:PutObject"
              ],
              "Resource": [
                "arn:aws:s3:::${DataBucketArn}/*"
              ]
            }
          ]
        }
```

## Service Control Policies (SCP)

### SCP for Organizational Units

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Service control policy for production OU

Resources:
  ProductionSCP:
    Type: AWS::Organizations::Policy
    Properties:
      Name: !Sub "${AWS::StackName}-production-restrictions"
      Description: SCP to restrict actions in production accounts
      Type: SERVICE_CONTROL_POLICY
      Content:
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "DenyDeleteResources",
              "Effect": "Deny",
              "Action": [
                "s3:DeleteBucket",
                "dynamodb:DeleteTable",
                "rds:DeleteDBInstance",
                "lambda:DeleteFunction"
              ],
              "Resource": "*",
              "Condition": {
                "StringEquals": {
                  "aws:ResourceTag/environment": "production"
                }
              }
            },
            {
              "Sid": "RequireEncryption",
              "Effect": "Deny",
              "Action": [
                "s3:PutObject",
                "dynamodb:PutItem"
              ],
              "Resource": "*",
              "Condition": {
                "StringNotEquals": {
                  "s3:x-amz-server-side-encryption": "AES256"
                }
              }
            },
            {
              "Sid": "DenyRootAccess",
              "Effect": "Deny",
              "Action": [
                "iam:CreateAccessKey",
                "iam:CreateLoginProfile",
                "iam:EnableMFADevice"
              ],
              "Resource": "*",
              "Condition": {
                "StringEquals": {
                  "aws:PrincipalTag/role": "breakglass"
                }
              }
            },
            {
              "Sid": "AllowKnownServices",
              "Effect": "Allow",
              "Action": "*",
              "Resource": "*",
              "NotPrincipal": {
                "AWS": [
                  "arn:aws:iam::aws:policy/AdministratorAccess"
                ]
              }
            }
          ]
        }
```

## Conditions and Transform

### Conditions for Environment-Specific Roles

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: IAM resources with conditional configurations

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  IsDevelopment: !Equals [!Ref Environment, dev]
  CreateAdminRole: !Or [!Equals [!Ref Environment, staging], !Equals [!Ref Environment, production]]

Resources:
  # Base role for all environments
  BaseExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-base-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      MaxSessionDuration: !FindInMap [EnvironmentConfig, !Ref Environment, MaxSessionDuration]
      Policies:
        - PolicyName: !Sub "${AWS::StackName}-base-policy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: "*"

  # Admin role only for staging and production
  AdminRole:
    Type: AWS::IAM::Role
    Condition: CreateAdminRole
    Properties:
      RoleName: !Sub "${AWS::StackName}-admin-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Ref AdminUserArn
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/ReadOnlyAccess
        - !If
          - IsProduction
          - arn:aws:iam::aws:policy/ViewBilling
          - !Ref AWS::NoValue

Mappings:
  EnvironmentConfig:
    dev:
      MaxSessionDuration: 3600
    staging:
      MaxSessionDuration: 7200
    production:
      MaxSessionDuration: 43200
```

### Transform for Policy Reuse

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: Using SAM Transform for IAM patterns

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Policies:
      - S3ReadPolicy:
          BucketName: !Ref DataBucket
      - DynamoDBCrudPolicy:
          TableName: !Ref DataTable
      - SecretsManagerReadWrite:
          SecretArn: !Ref AppSecret

Resources:
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-processor"
      Handler: app.handler
      CodeUri: lambda_function/
      Environment:
        Variables:
          LOG_LEVEL: INFO
```

## Best Practices

### Security

- Always apply least privilege: start with minimal permissions and add only what's needed
- Use IAM Access Analyzer to identify excessive permissions
- Implement permission boundaries to limit maximum permissions
- Use condition keys for granular restrictions (aws:SourceIp, aws:ResourceTag, aws:RequestedRegion)
- Enable MFA for all IAM users
- Rotate access keys regularly (max 90 days)
- Use roles instead of long-term credentials where possible
- Implement external ID for cross-account trust
- Use service-linked roles for AWS services

### Template Organization

- Separate IAM into dedicated stacks for clear ownership
- Use nested stacks for modularity
- Export only necessary values for cross-stack references
- Always document intent with Description fields
- Use Parameters for environment-specific configuration
- Implement conditions to manage variants without duplication
- Tag all IAM resources for tracking and cost allocation

### Monitoring

- Enable CloudTrail for audit of all IAM actions
- Configure S3 Object Lock for critical policy files
- Use IAM Access Analyzer for periodic reports
- Implement SCP for organizational guardrails
- Create alarms for unauthorized access

### Compliance

- Implement separation of duties policies
- Use AWS managed policies for standard compliance
- Document all deviations from standards
- Maintain audit trail for at least 90 days
- Apply encryption at rest and in transit

## CloudFormation Stack Management Best Practices

### Stack Policies

Stack Policies prevent unintended updates to critical resources during stack updates.

```yaml
Resources:
  # Stack Policy to protect IAM roles from updates
  IAMStackPolicy:
    Type: AWS::CloudFormation::StackPolicy
    Properties:
      PolicyDocument:
        Statement:
          - Effect: Deny
            Action: Update:Replace
            UpdateReplacePolicy: Retain
            Resource: "*"
            Condition:
              StringEquals:
                aws:ResourceTag/Protected: "true"
          - Effect: Allow
            Action: Update:*
            Resource: "*"
```

### Termination Protection

Enable termination protection to prevent accidental stack deletion.

```yaml
Resources:
  ProductionStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/iam-template.yaml
      TerminationProtection: true
```

CLI commands for termination protection:
```bash
# Enable termination protection
aws cloudformation update-termination-protection \
  --stack-name my-iam-stack \
  --enable-termination-protection

# Disable termination protection
aws cloudformation update-termination-protection \
  --stack-name my-iam-stack \
  --no-enable-termination-protection
```

### Drift Detection

Detect when infrastructure has diverged from the template definition.

```bash
# Detect drift on a stack
aws cloudformation detect-drift \
  --stack-name my-iam-stack

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>

# Get drift detection results
aws cloudformation describe-stack-resource-drifts \
  --stack-name my-iam-stack
```

### Change Sets

Preview and review changes before executing them.

```bash
# Create a change set
aws cloudformation create-change-set \
  --stack-name my-iam-stack \
  --change-set-name my-changeset \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# List change sets
aws cloudformation list-change-sets \
  --stack-name my-iam-stack

# Describe change set
aws cloudformation describe-change-set \
  --stack-name my-iam-stack \
  --change-set-name my-changeset

# Execute change set
aws cloudformation execute-change-set \
  --stack-name my-iam-stack \
  --change-set-name my-changeset

# Delete change set (if not executing)
aws cloudformation delete-change-set \
  --stack-name my-iam-stack \
  --change-set-name my-changeset
```

## Related Resources

- [IAM Documentation](https://docs.aws.amazon.com/iam/)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [IAM Best Practices](https://docs.aws.amazon.com/iam/latest/UserGuide/best-practices.html)
- [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)

## Additional Files

For complete details on IAM resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation IAM resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples
