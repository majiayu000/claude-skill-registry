---
name: aws-cloudformation-security
description: Provides AWS CloudFormation patterns for security infrastructure including KMS encryption, Secrets Manager, IAM security, VPC security, ACM certificates, parameter security, outputs, and secure cross-stack references. Use when implementing security best practices, encrypting data, managing secrets, applying least privilege IAM policies, securing VPC configurations, managing TLS/SSL certificates, and implementing defense in depth strategies.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation Security Infrastructure

## Overview

Create production-ready security infrastructure using AWS CloudFormation templates. This skill covers KMS encryption, Secrets Manager, IAM security with least privilege, VPC security configurations, ACM certificates, parameter security, secure outputs, cross-stack references, CloudWatch Logs encryption, defense in depth strategies, and security best practices.

## When to Use

- Implementing KMS encryption at rest and in transit
- Managing secrets with Secrets Manager and automatic rotation
- Applying IAM least privilege policies and permission boundaries
- Securing VPC with security groups, NACLs, and VPC endpoints
- Managing TLS/SSL certificates with ACM
- Encrypting CloudWatch Logs and S3 buckets
- Creating secure cross-stack references and outputs

## Instructions

Follow these steps to create security infrastructure with CloudFormation:

### 1. Define KMS Encryption Keys

Create customer-managed keys for encryption:

```yaml
Resources:
  EncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: Customer-managed key for data encryption
      KeyPolicy:
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action:
              - kms:Decrypt
              - kms:GenerateDataKey
            Resource: "*"
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:root"
            Action:
              - kms:*
            Resource: "*"

  KeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: !Sub "${AWS::StackName}/encryption-key"
      TargetKeyId: !Ref EncryptionKey
```

**Validate:** `aws kms get-key-policy --key-id <key-id> --output text`

### 2. Manage Secrets with Secrets Manager

Store and retrieve sensitive data securely:

```yaml
Resources:
  DatabaseSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub "${AWS::StackName}/database"
      Description: Database credentials
      SecretString: !Sub |
        {
          "username": "admin",
          "password": "${DatabasePassword}",
          "engine": "mysql",
          "host": "${DatabaseEndpoint}",
          "port": 3306
        }
      KmsKeyId: !Ref EncryptionKey

  SecretRotationSchedule:
    Type: AWS::SecretsManager::RotationSchedule
    Properties:
      SecretId: !Ref DatabaseSecret
      RotationLambdaARN: !Ref RotationLambda.Arn
      RotationRules:
        AutomaticallyAfterDays: 30
```

**Validate:** `aws secretsmanager describe-secret --secret-id <secret-name>`

### 3. Apply IAM Least Privilege

Create roles and policies with minimal required permissions:

```yaml
Resources:
  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
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
        - PolicyName: SpecificPermissions
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource: !Sub "${DataBucket.Arn}/*"
```

**Validate:** `aws iam simulate-principal-policy --policy-source-arn <role-arn> --action-names s3:GetObject --resource-arns <bucket-arn>`

### 4. Secure VPC Configuration

Implement network security with security groups and NACLs:

```yaml
Resources:
  ApplicationSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Application security group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref LoadBalancerSecurityGroup
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0

  ApplicationNACL:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC

  NACLEntry:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref ApplicationNACL
      RuleNumber: 100
      Protocol: "6"
      RuleAction: allow
      Egress: false
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 443
        To: 443
```

**Validate:** `aws ec2 describe-security-groups --group-ids <sg-id> --query 'SecurityGroups[0].IpPermissions'`

### 5. Request ACM Certificates

Manage TLS/SSL certificates for secure communication:

```yaml
Resources:
  Certificate:
    Type: AWS::ACM::Certificate
    Properties:
      DomainName: !Ref DomainName
      SubjectAlternativeNames:
        - !Sub "www.${DomainName}"
        - !Sub "api.${DomainName}"
      DomainValidationOptions:
        - DomainName: !Ref DomainName
          ValidationDomain: !Ref DomainName
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # DNS validation record
  DnsValidationRecord:
    Type: AWS::Route53::RecordSet
    Properties:
      HostedZoneName: !Ref HostedZone
      Name: !Sub "_${DomainName}."
      Type: CNAME
      TTL: 300
      ResourceRecords:
        - !Ref Certificate
```

**Validate:** `aws acm describe-certificate --certificate-arn <arn> --query 'Certificate.Status'`

### 6. Implement Secure Parameters

Use SecureString for sensitive parameter values:

```yaml
Resources:
  DatabasePasswordParameter:
    Type: AWS::SSM::Parameter
    Properties:
      Name: !Sub "/${AWS::StackName}/database/password"
      Type: SecureString
      Value: !Ref DatabasePassword
      Description: Database master password
      KmsKeyId: !Ref EncryptionKey

  # Reference in other resources
  DatabaseInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      MasterUsername: admin
      MasterUserPassword: !Ref DatabasePasswordParameter
```

**Validate:** `aws ssm get-parameter --name <param-name> --with-decryption --query 'Parameter.Type'`

### 7. Create Secure Outputs

Export only non-sensitive values from stacks:

```yaml
Outputs:
  # Safe to export
  KMSKeyArn:
    Description: KMS Key ARN for encryption
    Value: !GetAtt EncryptionKey.Arn
    Export:
      Name: !Sub "${AWS::StackName}-KMSKeyArn"

  SecretArn:
    Description: Secret ARN (not the secret value)
    Value: !Ref DatabaseSecret
    Export:
      Name: !Sub "${AWS::StackName}-SecretArn"

  # DO NOT export sensitive data
  # Incorrect:
  # SecretValue:
  #   Value: !GetAtt DatabaseSecret.SecretString
```

**Validate:** `aws cloudformation list-exports --query "Exports[?Name=='<stack-name>-KMSKeyArn']"`

### 8. Encrypt CloudWatch Logs

Enable encryption for log groups:

```yaml
Resources:
  EncryptedLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/applications/${ApplicationName}"
      RetentionInDays: 30
      KmsKeyId: !Ref EncryptionKey
```

**Validate:** `aws logs describe-log-groups --log-group-name-prefix <prefix> --query 'logGroups[0].kmsKeyId'`

## Best Practices

- **KMS**: Use separate keys per data classification; enable annual key rotation; use customer-managed keys for compliance
- **Secrets**: Rotate automatically (30 days for databases); never store secrets in plain text; use IAM policies for access control
- **IAM**: Apply least privilege; use roles not access keys; enable MFA; implement permission boundaries
- **Network**: Prefer security groups over NACLs; use VPC endpoints; restrict by specific CIDR ranges
- **Certificates**: Use ACM for automatic renewal; DNS validation is faster than email
- **Encryption**: Encrypt at rest and in transit; TLS 1.2+ required; use SSE-KMS for S3

## Examples

### Complete KMS and Secrets Stack

```yaml
Resources:
  # KMS Key with proper policy
  AppKey:
    Type: AWS::KMS::Key
    Properties:
      KeyPolicy:
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:root"
            Action: kms:*
            Resource: "*"
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action:
              - kms:Decrypt
              - kms:GenerateDataKey
            Resource: "*"

  # Secrets Manager with rotation
  DbSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      SecretString: !Sub '{"password":"${DbPassword}"}'
      KmsKeyId: !Ref AppKey
      RotationRules:
        AutomaticallyAfterDays: 30
```

### IAM Least Privilege Role

```yaml
Resources:
  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: AccessPolicy
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action: s3:GetObject
                Resource: !Sub "${Bucket.Arn}/*"
```

For comprehensive examples with VPC security groups, ACM certificates, and complete encrypted infrastructure stacks, see [examples.md](references/examples.md).

## Constraints and Warnings

### Resource Limits
- Security groups: max 60 inbound + 60 outbound rules
- NACLs: max 20 inbound + 20 outbound rules per subnet
- VPCs: max 5 per region (soft limit)
- Key rotation: annual for KMS customer-managed keys

### Security Constraints
- NACLs are **stateless**: return traffic must be explicitly allowed
- Default security groups cannot be deleted
- Security group references cannot span VPC peering (use CIDR)
- Cross-account access requires both IAM and resource policies

### Operational Warnings
- Secrets rotation requires Lambda function with proper IAM permissions
- KMS key deletion requires pending window (7-30 days)
- ACM certificates need DNS validation before issuance
- VPC CIDR blocks cannot overlap with peered VPCs

For detailed constraints including cost considerations and quota management, see [constraints.md](references/constraints.md).

## References

For detailed implementation guidance, see:

- **[examples.md](references/examples.md)** - Complete KMS stacks, Secrets Manager with rotation, IAM least privilege roles, VPC security groups, ACM certificates, and encrypted infrastructure
- **[constraints.md](references/constraints.md)** - Resource limits, security constraints, operational constraints, network constraints, cost considerations, and access control constraints
