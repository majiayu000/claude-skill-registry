---
name: aws-cloudformation-security
description: AWS CloudFormation patterns for infrastructure security, secrets management, encryption, and secure data handling. Use when creating secure CloudFormation templates with AWS Secrets Manager, KMS encryption, secure parameters, IAM policies, VPC security groups, TLS/SSL certificates, and encrypted traffic configurations. Covers template structure, parameter best practices, cross-stack references, and defense-in-depth strategies.
category: aws
tags: [aws, cloudformation, security, kms, secrets-manager, iam, encryption, tls, ssl, vpc, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Security

## Overview

Create secure AWS infrastructure using CloudFormation templates with security best practices. This skill covers encryption with AWS KMS, secrets management with Secrets Manager, secure parameters, IAM least privilege, security groups, TLS/SSL certificates, and defense-in-depth strategies.

## When to Use

Use this skill when:
- Creating CloudFormation templates with encryption at-rest and in-transit
- Managing secrets and credentials with AWS Secrets Manager
- Configuring AWS KMS for encryption keys
- Implementing secure parameters with SSM Parameter Store
- Creating IAM policies with least privilege
- Configuring security groups and network security
- Implementing secure cross-stack references
- Configuring TLS/SSL for AWS services
- Applying defense-in-depth for infrastructure

## CloudFormation Template Structure

### Base Template with Security Section

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Secure infrastructure template with encryption and secrets management

Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Encryption Settings
        Parameters:
          - EncryptionKeyArn
          - SecretsKmsKeyId
      - Label:
          default: Security Configuration
        Parameters:
          - SecurityLevel
          - EnableVPCPeering

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production

  EncryptionKeyArn:
    Type: AWS::KMS::Key::Arn
    Description: KMS key ARN for encryption

  SecretsKmsKeyId:
    Type: String
    Description: KMS key ID for secrets encryption

Mappings:
  SecurityConfig:
    dev:
      EnableDetailedMonitoring: false
      RequireMultiAZ: false
    staging:
      EnableDetailedMonitoring: true
      RequireMultiAZ: false
    production:
      EnableDetailedMonitoring: true
      RequireMultiAZ: true

Conditions:
  IsProduction: !Equals [!Ref Environment, production]
  EnableEnhancedMonitoring: !Equals [!Ref Environment, production]

Resources:
  # Resources will be defined here

Outputs:
  SecurityConfigurationOutput:
    Description: Security configuration applied
    Value: !Ref Environment
```

## AWS KMS - Encryption

### Complete KMS Key with Full Policy

```yaml
Resources:
  # Master KMS Key for application
  ApplicationKmsKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "KMS Key for application encryption"
      KeyPolicy:
        Version: "2012-10-17"
        Id: "application-key-policy"
        Statement:
          # Allow key management to administrators
          - Sid: "EnableIAMPolicies"
            Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:role/AdminRole"
            Action:
              - kms:Create*
              - kms:Describe*
              - kms:Enable*
              - kms:List*
              - kms:Put*
              - kms:Update*
              - kms:Revoke*
              - kms:Disable*
              - kms:Get*
              - kms:Delete*
              - kms:TagResource
              - kms:UntagResource
            Resource: "*"
            Condition:
              StringEquals:
                aws:PrincipalOrgID: !Ref OrganizationId

          # Allow encryption/decryption for application roles
          - Sid: "AllowCryptographicOperations"
            Effect: Allow
            Principal:
              AWS:
                - !Sub "arn:aws:iam::${AWS::AccountId}:role/LambdaExecutionRole"
                - !Sub "arn:aws:iam::${AWS::AccountId}:role/ECSTaskRole"
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:GenerateDataKey*
              - kms:ReEncrypt*
            Resource: "*"

          # Allow key usage for specific services
          - Sid: "AllowKeyUsageForSpecificServices"
            Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
                - ecs.amazonaws.com
                - rds.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:GenerateDataKey*
            Resource: "*"

      KeyUsage: ENCRYPT_DECRYPT
      EnableKeyRotation: true
      PendingWindowInDays: 30

  # Alias for the key
  ApplicationKmsKeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: !Sub "alias/application-${Environment}"
      TargetKeyId: !Ref ApplicationKmsKey

  # KMS Key for S3 bucket encryption
  S3KmsKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "KMS Key for S3 bucket encryption"
      KeyPolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: "AllowS3Encryption"
            Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:GenerateDataKey*
            Resource: "*"
            Condition:
              StringEquals:
                aws:SourceAccount: !Ref AWS::AccountId

  # KMS Key for RDS encryption
  RdsKmsKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "KMS Key for RDS database encryption"
      KeyPolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: "AllowRDSEncryption"
            Effect: Allow
            Principal:
              Service: rds.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:GenerateDataKey*
            Resource: "*"
```

### S3 Bucket with KMS Encryption

```yaml
Resources:
  EncryptedS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "secure-bucket-${AWS::AccountId}-${AWS::Region}"
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !Ref S3KmsKey
            BucketKeyEnabled: true

      VersioningConfiguration:
        Status: Enabled

      LifecycleConfiguration:
        Rules:
          - Id: ArchiveOldVersions
            Status: Enabled
            NoncurrentVersionExpiration:
              NoncurrentDays: 90

      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Encrypted
          Value: "true"
```

## AWS Secrets Manager

### Secrets Manager with Automatic Rotation

```yaml
Resources:
  # Database credentials secret
  DatabaseSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/database/credentials"
      Description: "Database credentials with automatic rotation"
      SecretString: !Sub |
        {
          "username": "${DBUsername}",
          "password": "${DBPassword}",
          "host": "${DBHost}",
          "port": "${DBPort}",
          "dbname": "${DBName}",
          "engine": "postgresql"
        }
      KmsKeyId: !Ref SecretsKmsKeyId

      # Enable automatic rotation
      RotationRules:
        AutomaticallyAfterDays: 30

      # Rotation Lambda configuration
      RotationLambdaARN: !GetAtt SecretRotationFunction.Arn

      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: CloudFormation
        - Key: RotationEnabled
          Value: "true"

  # Secret with resource-based policy
  ApiSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/api/keys"
      Description: "API keys for external service authentication"
      SecretString: !Sub |
        {
          "api_key": "${ExternalApiKey}",
          "api_secret": "${ExternalApiSecret}",
          "endpoint": "https://api.example.com"
        }
      KmsKeyId: !Ref SecretsKmsKeyId

      # Resource-based policy for access control
      ResourcePolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: "AllowLambdaAccess"
            Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:role/LambdaExecutionRole"
            Action:
              - secretsmanager:GetSecretValue
              - secretsmanager:DescribeSecret
            Resource: "*"
            Condition:
              StringEquals:
                aws:ResourceTag/Environment: !Ref Environment

          - Sid: "DenyUnencryptedAccess"
            Effect: Deny
            Principal: "*"
            Action:
              - secretsmanager:GetSecretValue
            Resource: "*"
            Condition:
              StringEquals:
                kms:ViaService: !Sub "secretsmanager.${AWS::Region}.amazonaws.com"
              StringNotEquals:
                kms:EncryptContext: !Sub "secretsmanager:${AWS::StackName}"

  # Secret with cross-account access
  SharedSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/shared/credentials"
      Description: "Secret shared across accounts"
      SecretString: !Sub |
        {
          "shared_key": "${SharedKey}",
          "shared_value": "${SharedValue}"
        }
      KmsKeyId: !Ref SecretsKmsKeyId

      # Cross-account access policy
      ResourcePolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: "AllowCrossAccountRead"
            Effect: Allow
            Principal:
              AWS:
                - !Sub "arn:aws:iam::${ProductionAccountId}:role/SharedSecretReader"
            Action:
              - secretsmanager:GetSecretValue
              - secretsmanager:DescribeSecret
            Resource: "*"
```

### SSM Parameter Store with SecureString

```yaml
Parameters:
  # SSM Parameter for database connection
  DBCredentialsParam:
    Type: AWS::SSM::Parameter::Value<SecureString>
    NoEcho: true
    Description: Database credentials from SSM Parameter Store
    Value: !Sub "/${Environment}/database/credentials"

  # SSM Parameter with specific path
  ApiKeyParam:
    Type: AWS::SSM::Parameter::Value<SecureString>
    NoEcho: true
    Description: API key for external service
    Value: !Sub "/${Environment}/external-api/key"

Resources:
  # Lambda function using SSM parameters
  SecureLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-secure-function"
      Runtime: python3.11
      Handler: handler.handler
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/secure-function.zip
      Role: !GetAtt LambdaExecutionRole.Arn
      Environment:
        Variables:
          DB_CREDENTIALS_SSM_PATH: !Sub "/${Environment}/database/credentials"
          API_KEY_SSM_PATH: !Sub "/${Environment}/external-api/key"
```

## IAM Security - Least Privilege

### IAM Role with Granular Policies

```yaml
Resources:
  # Lambda Execution Role with minimal permissions
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
            Condition:
              StringEquals:
                aws:SourceAccount: !Ref AWS::AccountId
                lambda:SourceFunctionArn: !Ref SecureLambdaFunctionArn

      # Permissions boundary for enhanced security
      PermissionsBoundary: !Ref PermissionsBoundaryPolicy

      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

      Policies:
        # Policy for specific secrets access
        - PolicyName: SecretsAccessPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                  - secretsmanager:DescribeSecret
                Resource: !Ref DatabaseSecretArn
                Condition:
                  StringEquals:
                    secretsmanager:SecretTarget: !Sub "${DatabaseSecretArn}:${DatabaseSecret}"

              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Ref ApiSecretArn

        # Policy for specific S3 access
        - PolicyName: S3AccessPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource:
                  - !Sub "${DataBucket.Arn}/*"
                  - !Sub "${DataBucket.Arn}"
                Condition:
                  StringEquals:
                    s3:ResourceAccount: !Ref AWS::AccountId

              - Effect: Deny
                Action:
                  - s3:DeleteObject*
                Resource:
                  - !Sub "${DataBucket.Arn}/*"
                Condition:
                  Bool:
                    aws:MultiFactorAuthPresent: true

        # Policy for CloudWatch Logs
        - PolicyName: CloudWatchLogsPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: !Sub "${LogGroup.Arn}:*"

      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: LeastPrivilege
          Value: "true"

  # Permissions Boundary Policy
  PermissionsBoundaryPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      Description: "Permissions boundary for Lambda execution role"
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: "DenyAccessToAllExceptSpecified"
            Effect: Deny
            Action:
              - "*"
            Resource: "*"
            Condition:
              StringNotEqualsIfExists:
                aws:RequestedRegion:
                  - !Ref AWS::Region
              ArnNotEqualsIfExists:
                aws:SourceArn: !Ref AllowedResourceArns
```

### IAM Policy for Cross-Account Access

```yaml
Resources:
  # Role for cross-account access
  CrossAccountRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-cross-account-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS:
                - !Sub "arn:aws:iam::${ProductionAccountId}:root"
                - !Sub "arn:aws:iam::${StagingAccountId}:role/CrossAccountAccessRole"
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                aws:PrincipalAccount: !Ref ProductionAccountId
              Bool:
                aws:MultiFactorAuthPresent: true

      Policies:
        - PolicyName: CrossAccountReadOnlyPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject*
                  - s3:List*
                Resource:
                  - !Sub "${SharedBucket.Arn}"
                  - !Sub "${SharedBucket.Arn}/*"

              - Effect: Allow
                Action:
                  - dynamodb:Query
                  - dynamodb:Scan
                  - dynamodb:GetItem
                Resource:
                  - !Sub "${SharedTable.Arn}"
                  - !Sub "${SharedTable.Arn}/index/*"

              - Effect: Deny
                Action:
                  - s3:DeleteObject*
                  - s3:PutObject*
                Resource:
                  - !Sub "${SharedBucket.Arn}/*"
```

## VPC Security

### Security Groups with Restrictive Rules

```yaml
Resources:
  # Security Group for application
  ApplicationSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-app-sg"
      GroupDescription: "Security group for application tier"
      VpcId: !Ref VPCId
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-app-sg"
        - Key: Environment
          Value: !Ref Environment

      # Inbound rules - only necessary traffic
      SecurityGroupIngress:
        # HTTP from ALB
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref ALBSecurityGroup
          Description: "HTTP from ALB"

        # HTTPS from ALB
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref ALBSecurityGroup
          Description: "HTTPS from ALB"

        # SSH from bastion only (if needed)
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          SourceSecurityGroupId: !Ref BastionSecurityGroup
          Description: "SSH access from bastion"

        # Custom TCP for internal services
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref InternalSecurityGroup
          Description: "Internal service communication"

      # Outbound rules - limited
      SecurityGroupEgress:
        # HTTPS outbound for API calls
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: "HTTPS outbound"

        # DNS outbound
        - IpProtocol: udp
          FromPort: 53
          ToPort: 53
          CidrIp: 10.0.0.0/16
          Description: "DNS outbound for VPC"

  # Security Group for database
  DatabaseSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-db-sg"
      GroupDescription: "Security group for database tier"
      VpcId: !Ref VPCId
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-db-sg"

      # Inbound - only from application security group
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref ApplicationSecurityGroup
          Description: "PostgreSQL from application tier"

      # Outbound - minimum required
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: "HTTPS for updates and patches"

  # Security Group for ALB
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-alb-sg"
      GroupDescription: "Security group for ALB"
      VpcId: !Ref VPCId

      SecurityGroupIngress:
        # HTTP from internet
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: "HTTP from internet"

        # HTTPS from internet
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: "HTTPS from internet"

      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref ApplicationSecurityGroup
          Description: "Forward to application"

  # VPC Endpoint for Secrets Manager
  SecretsManagerVPCEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref VPCId
      ServiceName: !Sub "com.amazonaws.${AWS::Region}.secretsmanager"
      VpcEndpointType: Interface
      Subnets:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      SecurityGroups:
        - !Ref ApplicationSecurityGroup
      PrivateDnsEnabled: true
```

## TLS/SSL Certificates with ACM

### Certificate Manager for API Gateway

```yaml
Resources:
  # SSL Certificate for domain
  SSLCertificate:
    Type: AWS::CertificateManager::Certificate
    Properties:
      DomainName: !Ref DomainName
      SubjectAlternativeNames:
        - !Sub "*.${DomainName}"
        - !Ref AdditionalDomainName

      ValidationMethod: DNS

      DomainValidationOptions:
        - DomainName: !Ref DomainName
          Route53HostedZoneId: !Ref HostedZoneId

      Options:
        CertificateTransparencyLoggingPreference: ENABLED

      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: CloudFormation

  # Certificate for regional API Gateway
  RegionalCertificate:
    Type: AWS::CertificateManager::Certificate
    Properties:
      DomainName: !Sub "${Environment}.${DomainName}"
      ValidationMethod: DNS
      DomainValidationOptions:
        - DomainName: !Sub "${Environment}.${DomainName}"
          Route53HostedZoneId: !Ref HostedZoneId

  # API Gateway with TLS 1.2+
  SecureApiGateway:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: !Sub "${AWS::StackName}-secure-api"
      Description: "Secure REST API with TLS enforcement"
      EndpointConfiguration:
        Types:
          - REGIONAL
      MinimumCompressionSize: 1024

      # Policy to enforce HTTPS
      Policy:
        Version: "2012-10-17"
        Statement:
          - Effect: Deny
            Principal: "*"
            Action: execute-api:Invoke
            Resource: !Sub "arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${SecureApiGateway}/*"
            Condition:
              Bool:
                aws:SecureTransport: "false"

  # Custom Domain per API Gateway
  ApiGatewayDomain:
    Type: AWS::ApiGateway::DomainName
    Properties:
      DomainName: !Sub "api.${DomainName}"
      RegionalCertificateArn: !Ref RegionalCertificate
      EndpointConfiguration:
        Types:
          - REGIONAL

  # Route 53 record per dominio API
  ApiGatewayDNSRecord:
    Type: AWS::Route53::RecordSet
    Properties:
      Name: !Sub "api.${DomainName}."
      Type: A
      AliasTarget:
        DNSName: !GetAtt ApiGatewayRegionalHostname.RegionalHostname
        HostedZoneId: !GetAtt ApiGatewayRegionalHostname.RegionalHostedZoneId
        EvaluateTargetHealth: false
      HostedZoneId: !Ref HostedZoneId

  # Lambda Function URL con AuthType AWS_IAM
  SecureLambdaUrl:
    Type: AWS::Lambda::Url
    Properties:
      AuthType: AWS_IAM
      TargetFunctionArn: !GetAtt SecureLambdaFunction.Arn
      Cors:
        AllowCredentials: true
        AllowHeaders:
          - Authorization
          - Content-Type
        AllowMethods:
          - GET
          - POST
        AllowOrigins:
          - !Ref AllowedOrigin
        MaxAge: 86400
      InvokeMode: BUFFERED
```

## Parameter Security Best Practices

### AWS-Specific Parameter Types with Validation

```yaml
Parameters:
  # AWS-specific types for automatic validation
  VPCId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID for deployment

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnet IDs for private subnets

  SecurityGroupIds:
    Type: List<AWS::EC2::SecurityGroup::Id>
    Description: Security group IDs

  DatabaseInstanceIdentifier:
    Type: AWS::RDS::DBInstance::Identifier
    Description: RDS instance identifier

  KMSKeyArn:
    Type: AWS::KMS::Key::Arn
    Description: KMS key ARN for encryption

  SecretArn:
    Type: AWS::SecretsManager::Secret::Arn
    Description: Secrets Manager secret ARN

  LambdaFunctionArn:
    Type: AWS::Lambda::Function::Arn
    Description: Lambda function ARN

  # SSM Parameter with secure string
  DatabasePassword:
    Type: AWS::SSM::Parameter::Value<SecureString>
    NoEcho: true
    Description: Database password from SSM

  # Custom parameters with constraints
  DBUsername:
    Type: String
    Description: Database username
    Default: appuser
    MinLength: 1
    MaxLength: 63
    AllowedPattern: "[a-zA-Z][a-zA-Z0-9_]*"
    ConstraintDescription: Must start with letter, alphanumeric and underscores only

  DBPort:
    Type: Number
    Description: Database port
    Default: 5432
    MinValue: 1024
    MaxValue: 65535

  MaxConnections:
    Type: Number
    Description: Maximum database connections
    Default: 100
    MinValue: 10
    MaxValue: 65535

  EnvironmentName:
    Type: String
    Description: Deployment environment
    Default: dev
    AllowedValues:
      - dev
      - staging
      - production
    ConstraintDescription: Must be dev, staging, or production
```

## Outputs and Secure Cross-Stack References

### Export with Naming Convention

```yaml
Outputs:
  # Export for cross-stack references
  VPCIdExport:
    Description: VPC ID for network stack
    Value: !Ref VPC
    Export:
      Name: !Sub "${AWS::StackName}-VPCId"

  ApplicationSecurityGroupIdExport:
    Description: Application security group ID
    Value: !Ref ApplicationSecurityGroup
    Export:
      Name: !Sub "${AWS::StackName}-AppSecurityGroupId"

  DatabaseSecurityGroupIdExport:
    Description: Database security group ID
    Value: !Ref DatabaseSecurityGroup
    Export:
      Name: !Sub "${AWS::StackName}-DBSecurityGroupId"

  KMSKeyArnExport:
    Description: KMS key ARN for encryption
    Value: !GetAtt ApplicationKmsKey.Arn
    Export:
      Name: !Sub "${AWS::StackName}-KMSKeyArn"

  DatabaseSecretArnExport:
    Description: Database secret ARN
    Value: !Ref DatabaseSecret
    Export:
      Name: !Sub "${AWS::StackName}-DatabaseSecretArn"

  SSLCertificateArnExport:
    Description: SSL certificate ARN
    Value: !Ref SSLCertificate
    Export:
      Name: !Sub "${AWS::StackName}-SSLCertificateArn"
```

### Import from Network Stack

```yaml
Parameters:
  NetworkStackName:
    Type: String
    Description: Name of the network stack

Resources:
  # Import values from network stack
  VPCId:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Select [0, !Split [",", !ImportValue !Sub "${NetworkStackName}-VPCcidrs"]]

  ApplicationSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}-app-sg"
      VpcId: !ImportValue !Sub "${NetworkStackName}-VPCId"
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !ImportValue !Sub "${NetworkStackName}-ALBSecurityGroupId"
```

## CloudWatch Logs Encryption

### Log Group with KMS Encryption

```yaml
Resources:
  # Encrypted CloudWatch Log Group
  EncryptedLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/lambda/${AWS::StackName}-function"
      RetentionInDays: 30
      KmsKeyId: !Ref ApplicationKmsKey

      # Data protection policy
      LogGroupClass: STANDARD

      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Encrypted
          Value: "true"

  # Metric Filter for security events
  SecurityEventMetricFilter:
    Type: AWS::Logs::MetricFilter
    Properties:
      LogGroupName: !Ref EncryptedLogGroup
      FilterPattern: '[ERROR, WARNING, "Access Denied", "Unauthorized"]'
      MetricTransformations:
        - MetricValue: "1"
          MetricNamespace: !Sub "${AWS::StackName}/Security"
          MetricName: SecurityEvents

  # Alarm for security errors
  SecurityAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-security-errors"
      AlarmDescription: Alert on security-related errors
      MetricName: SecurityEvents
      Namespace: !Sub "${AWS::StackName}/Security"
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref SecurityAlertTopic

  # SNS Topic for security alerts
  SecurityAlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-security-alerts"
```

## Defense in Depth

### Stack with Multiple Security Layers

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Defense in depth security architecture

Resources:
  # Layer 1: Network Security - Security Groups
  WebTierSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Web tier security group"
      VpcId: !Ref VPCId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: "HTTPS from internet"

  AppTierSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "App tier security group"
      VpcId: !Ref VPCId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref WebTierSecurityGroup

  # Layer 2: Encryption - KMS
  DataEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "Data encryption key"
      KeyPolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: "EnableIAMPoliciesForKeyManagement"
            Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:role/AdminRole"
            Action: kms:*
            Resource: "*"
          - Sid: "AllowEncryptionOperations"
            Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:role/AppRole"
            Action:
              - kms:Encrypt
              - kms:Decrypt
            Resource: "*"

  # Layer 3: Secrets Management
  ApplicationSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/application/credentials"
      SecretString: "{}"
      KmsKeyId: !Ref DataEncryptionKey

  # Layer 4: IAM Least Privilege
  ApplicationRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-app-role"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: MinimalSecretsAccess
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Ref ApplicationSecret

  # Layer 5: Logging and Monitoring
  AuditLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/${AWS::StackName}/audit"
      RetentionInDays: 365
      KmsKeyId: !Ref DataEncryptionKey

  # Layer 6: WAF for API protection
  WebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: !Sub "${AWS::StackName}-waf"
      Scope: REGIONAL
      DefaultAction:
        Allow:
          CustomRequestHandling:
            InsertHeaders:
              - Name: X-Frame-Options
                Value: DENY
      Rules:
        - Name: BlockSQLInjection
          Priority: 1
          Statement:
            SqliMatchStatement:
              FieldToMatch:
                Body:
                  OversizeHandling: CONTINUE
              SensitivityLevel: HIGH
          Action:
            Block:
              CustomResponse:
                ResponseCode: 403
                ResponseBody: "Request blocked due to SQL injection"
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: BlockSQLInjection

        - Name: BlockXSS
          Priority: 2
          Statement:
            XssMatchStatement:
              FieldToMatch:
                QueryString:
                  OversizeHandling: CONTINUE
          Action:
            Block:
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: BlockXSS

        - Name: RateLimit
          Priority: 3
          Statement:
            RateBasedStatement:
              Limit: 2000
              EvaluationWindowSec: 60
          Action:
            Block:
              CustomResponse:
                ResponseCode: 429
                ResponseBody: "Too many requests"
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: RateLimit

      VisibilityConfig:
        CloudWatchMetricsEnabled: true
        MetricName: !Sub "${AWS::StackName}-WebACL"
        SampledRequestsEnabled: true
```

## Best Practices

### Encryption
- Always use KMS with customer-managed keys for sensitive data
- Enable automatic key rotation (max 365 days)
- Use S3 bucket keys to reduce KMS costs
- Encrypt CloudWatch Logs with KMS
- Implement envelope encryption for large data

### Secrets Management
- Use Secrets Manager for automatic rotation
- Reference secrets via ARN, not hard-coded
- Use resource-based policies for granular access
- Implement encryption context for auditing
- Limit access with IAM conditions

### IAM Security
- Apply least privilege in all policies
- Use permissions boundaries to limit escalation
- Enable MFA for administrative roles
- Implement condition keys for region/endpoint
- Regular audit with IAM Access Analyzer

### Network Security
- Security groups with minimal rules
- Deny default outbound where possible
- Use VPC endpoints for AWS services
- Implement private subnets for backend tiers
- Use Network ACLs as additional layer

### TLS/SSL
- Use ACM for managed certificates
- Enforce HTTPS with resource policies
- Configure minimum TLS 1.2
- Use HSTS headers
- Renew certificates before expiration

### Monitoring
- Enable CloudTrail for audit trail
- Create metrics for security events
- Configure alarms for suspicious activity
- Appropriate log retention (min 90 days)
- Use GuardDuty for threat detection

## Related Resources

- [AWS KMS Documentation](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
- [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)

## Additional Files

For complete details on resources and their properties, see:
- [REFERENCE.md](reference.md) - Detailed reference guide for all CloudFormation security resources
- [EXAMPLES.md](examples.md) - Complete production-ready examples for security scenarios

## CloudFormation Stack Management Best Practices

### Stack Policies

Stack Policies prevent accidental updates to critical infrastructure resources. Use them to protect production resources from unintended modifications.

```yaml
Resources:
  ProductionStackPolicy:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/production-stack.yaml"
      StackPolicyBody:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Action: Update:*
            Principal: "*"
            Resource: "*"
          - Effect: Deny
            Action:
              - Update:Replace
              - Update:Delete
            Principal: "*"
            Resource:
              - LogicalResourceId/ProductionDatabase
              - LogicalResourceId/ProductionKmsKey
            Condition:
              StringEquals:
                aws:RequestedRegion:
                  - us-east-1
                  - us-west-2

  # Inline stack policy for sensitive resources
  SensitiveResourcesPolicy:
    Type: AWS::CloudFormation::StackPolicy
    Properties:
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Deny
            Action: Update:*
            Principal: "*"
            Resource: "*"
            Condition:
              StringEquals:
                aws:ResourceTag/Environment: production
              Not:
                StringEquals:
                  aws:username: security-admin
```

### Termination Protection

Enable termination protection to prevent accidental deletion of production stacks. This adds a safety layer for critical infrastructure.

```yaml
Resources:
  # Production stack with termination protection
  ProductionDatabaseStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/database.yaml"
      TerminationProtection: true
      Parameters:
        Environment: production
        InstanceClass: db.r6g.xlarge
        MultiAZ: true

  # Stack with conditional termination protection
  ApplicationStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/application.yaml"
      TerminationProtection: !If [IsProduction, true, false]
      Parameters:
        Environment: !Ref Environment
```

### Drift Detection

Detect configuration drift in your CloudFormation stacks to identify unauthorized or unexpected changes.

```yaml
Resources:
  # Custom resource for drift detection
  DriftDetectionFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${AWS::StackName}-drift-detector"
      Runtime: python3.11
      Handler: drift_detector.handler
      Role: !GetAtt DriftDetectionRole.Arn
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: lambda/drift-detector.zip
      Environment:
        Variables:
          STACK_NAME: !Ref StackName
          SNS_TOPIC_ARN: !Ref DriftAlertTopic
      Timeout: 300

  # Scheduled drift detection
  DriftDetectionSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub "${AWS::StackName}-drift-schedule"
      ScheduleExpression: rate(1 day)
      State: ENABLED
      Targets:
        - Arn: !GetAtt DriftDetectionFunction.Arn
          Id: DriftDetectionFunction

  # Permission for EventBridge to invoke Lambda
  DriftDetectionPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref DriftDetectionFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt DriftDetectionSchedule.Arn

  # SNS topic for drift alerts
  DriftAlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-drift-alerts"
```

### Drift Detection Python Handler

```python
import boto3
import json

def handler(event, context):
    cloudformation = boto3.client('cloudformation')
    sns = boto3.client('sns')

    stack_name = event.get('STACK_NAME', 'my-production-stack')
    topic_arn = event.get('SNS_TOPIC_ARN')

    # Detect drift
    response = cloudformation.detect_stack_drift(StackName=stack_name)

    # Wait for drift detection to complete
    import time
    time.sleep(60)

    # Get drift status
    drift_status = cloudformation.describe_stack-drift-detection-status(
        StackName=stack_name,
        DetectionId=response['StackDriftDetectionId']
    )

    # Get resources with drift
    resources = []
    paginator = cloudformation.get_paginator('list_stack_resources')
    for page in paginator.paginate(StackName=stack_name):
        for resource in page['StackResourceSummaries']:
            if resource['DriftStatus'] != 'IN_SYNC':
                resources.append({
                    'LogicalId': resource['LogicalResourceId'],
                    'PhysicalId': resource['PhysicalResourceId'],
                    'DriftStatus': resource['DriftStatus'],
                    'Expected': resource.get('ExpectedResourceType'),
                    'Actual': resource.get('ActualResourceType')
                })

    # Send alert if drift detected
    if resources:
        message = f"Drift detected on stack {stack_name}:\n"
        for r in resources:
            message += f"- {r['LogicalId']}: {r['DriftStatus']}\n"

        sns.publish(
            TopicArn=topic_arn,
            Subject=f"CloudFormation Drift Alert: {stack_name}",
            Message=message
        )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'drift_status': drift_status['StackDriftStatus'],
            'resources_with_drift': len(resources)
        })
    }
```

### Change Sets Usage

Use Change Sets to preview and review changes before applying them to production stacks.

```yaml
Resources:
  # Change set for stack update
  ChangeSet:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/updated-template.yaml"
      ChangeSetName: !Sub "${AWS::StackName}-update-changeset"
      ChangeSetType: UPDATE
      Parameters:
        Environment: !Ref Environment
        InstanceType: !Ref NewInstanceType
      Capabilities:
        - CAPABILITY_IAM
        - CAPABILITY_NAMED_IAM

  # Nested change set for review
  ReviewChangeSet:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/review-template.yaml"
      ChangeSetName: !Sub "${AWS::StackName}-review-changeset"
      ChangeSetType: UPDATE
      Parameters:
        Environment: !Ref Environment
      Tags:
        - Key: ChangeSetType
          Value: review
        - Key: CreatedBy
          Value: CloudFormation
```

### Change Set Generation Script

```bash
#!/bin/bash

# Create a change set for review
aws cloudformation create-change-set \
  --stack-name my-production-stack \
  --change-set-name production-update-changeset \
  --template-url https://my-bucket.s3.amazonaws.com/updated-template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=production \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

# Wait for change set creation
aws cloudformation wait change-set-create-complete \
  --stack-name my-production-stack \
  --change-set-name production-update-changeset

# Describe change set to see what will change
aws cloudformation describe-change-set \
  --stack-name my-production-stack \
  --change-set-name production-update-changeset

# Execute change set if changes look good
aws cloudformation execute-change-set \
  --stack-name my-production-stack \
  --change-set-name production-update-changeset
```

### Stack Update with Rollback Triggers

```yaml
Resources:
  # Production stack with rollback configuration
  ProductionStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: !Sub "https://${BucketName}.s3.amazonaws.com/production.yaml"
      TimeoutInMinutes: 60
      RollbackConfiguration:
        RollbackTriggers:
          - Arn: !Sub "arn:aws:cloudwatch:${AWS::Region}:${AWS::AccountId}:alarm:ProductionCPUHigh"
            Type: AWS::CloudWatch::Alarm
          - Arn: !Sub "arn:aws:cloudwatch:${AWS::Region}:${AWS::AccountId}:alarm:ProductionLatencyHigh"
            Type: AWS::CloudWatch::Alarm
        MonitoringTimeInMinutes: 15
      NotificationARNs:
        - !Ref UpdateNotificationTopic

  # CloudWatch alarms for rollback
  ProductionCPUHigh:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${AWS::StackName}-CPU-High"
      AlarmDescription: Trigger rollback if CPU exceeds 80%
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Statistic: Average
      Period: 60
      EvaluationPeriods: 5
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref UpdateNotificationTopic

  # SNS topic for notifications
  UpdateNotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub "${AWS::StackName}-update-notifications"
```

### Best Practices for Stack Management

1. **Enable Termination Protection**
   - Always enable for production stacks
   - Use as a safety mechanism against accidental deletion
   - Requires manual disabling before deletion

2. **Use Stack Policies**
   - Protect critical resources from unintended updates
   - Use Deny statements for production databases, KMS keys, and IAM roles
   - Apply conditions based on region, user, or tags

3. **Implement Drift Detection**
   - Run drift detection regularly (daily for production)
   - Alert on any drift detection
   - Investigate and remediate drift immediately

4. **Use Change Sets**
   - Always use Change Sets for production updates
   - Review changes before execution
   - Use descriptive change set names

5. **Configure Rollback Triggers**
   - Set up CloudWatch alarms for critical metrics
   - Configure monitoring time to allow stabilization
   - Test rollback triggers in non-production first

6. **Implement Change Management**
   - Require approval for production changes
   - Use CodePipeline with manual approval gates
   - Document all changes in change log

7. **Use Stack Sets for Multi-Account**
   - Deploy infrastructure consistently across accounts
   - Use StackSets for organization-wide policies
   - Implement drift detection at organization level
