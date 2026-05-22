---
name: aws-cloudformation-s3
description: AWS CloudFormation patterns for Amazon S3. Use when creating S3 buckets, policies, versioning, lifecycle rules, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references.
category: aws
tags: [aws, cloudformation, s3, storage, infrastructure, iaac]
version: 1.0.0
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation S3 Patterns

Create production-ready Amazon S3 infrastructure using AWS CloudFormation templates. This skill covers S3 bucket configurations, bucket policies, versioning, lifecycle rules, and template structure best practices.

## When to Use

Use this skill when:
- Creating S3 buckets with custom configurations
- Implementing bucket policies for access control
- Configuring S3 versioning for data protection
- Setting up lifecycle rules for data management
- Creating Outputs for cross-stack references
- Using Parameters with AWS-specific types
- Organizing templates with Mappings and Conditions
- Building reusable CloudFormation templates for S3

## Quick Start

### Basic S3 Bucket

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Simple S3 bucket with default settings

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket
      Tags:
        - Key: Environment
          Value: production
        - Key: Project
          Value: my-project
```

### S3 Bucket with Versioning and Logging

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: S3 bucket with versioning and access logging

Parameters:
  BucketName:
    Type: String
    Description: Name of the S3 bucket

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
      VersioningConfiguration:
        Status: Enabled
      LoggingConfiguration:
        DestinationBucketName: !Ref AccessLogBucket
        LogFilePrefix: logs/
      Tags:
        - Key: Name
          Value: !Ref BucketName

  AccessLogBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${BucketName}-logs
      AccessControl: LogDeliveryWrite

Outputs:
  BucketName:
    Description: Name of the S3 bucket
    Value: !Ref DataBucket

  BucketArn:
    Description: ARN of the S3 bucket
    Value: !GetAtt DataBucket.Arn
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
Description: My S3 CloudFormation Template
```

### Description

Add a description to document the template's purpose. Must appear after the format version.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >
  This template creates an S3 bucket with versioning enabled
  for data protection. It includes:
  - Bucket with versioning configuration
  - Lifecycle rules for data retention
  - Server access logging
```

### Metadata

Use `Metadata` for additional information about resources or parameters.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Bucket Configuration
        Parameters:
          - BucketName
          - EnableVersioning
      - Label:
          default: Lifecycle Rules
        Parameters:
          - RetentionDays
    ParameterLabels:
      BucketName:
        default: Bucket Name
      EnableVersioning:
        default: Enable Versioning
```

### Resources Section

The `Resources` section is the only required section. It defines AWS resources to provision.

```yaml
Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
```

## Parameters

### Parameter Types

Use AWS-specific parameter types for validation and easier selection in the console.

```yaml
Parameters:
  ExistingBucketName:
    Type: AWS::S3::Bucket::Name
    Description: Select an existing S3 bucket

  BucketNamePrefix:
    Type: String
    Description: Prefix for new bucket names
```

### SSM Parameter Types

Reference Systems Manager parameters for dynamic values.

```yaml
Parameters:
  LatestBucketPolicy:
    Type: AWS::SSM::Parameter::Value<String>
    Description: Latest bucket policy from SSM
    Default: /s3/bucket-policy/latest
```

### Parameter Constraints

Add constraints to validate parameter values.

```yaml
Parameters:
  BucketName:
    Type: String
    Description: Name of the S3 bucket
    Default: my-bucket
    AllowedPattern: ^[a-z0-9][a-z0-9-]*[a-z0-9]$
    ConstraintDescription: Bucket names must be lowercase, numbers, or hyphens

  RetentionDays:
    Type: Number
    Description: Number of days to retain objects
    Default: 30
    MinValue: 1
    MaxValue: 365
    ConstraintDescription: Must be between 1 and 365 days

  Environment:
    Type: String
    Description: Deployment environment
    Default: development
    AllowedValues:
      - development
      - staging
      - production
    ConstraintDescription: Must be development, staging, or production
```

## Mappings

Use `Mappings` for static configuration data based on regions or other factors.

```yaml
Mappings:
  RegionConfig:
    us-east-1:
      BucketPrefix: us-east-1
    us-west-2:
      BucketPrefix: us-west-2
    eu-west-1:
      BucketPrefix: eu-west-1

  EnvironmentSettings:
    development:
      VersioningStatus: Suspended
      RetentionDays: 7
    staging:
      VersioningStatus: Enabled
      RetentionDays: 30
    production:
      VersioningStatus: Enabled
      RetentionDays: 90

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${BucketPrefix}-${Environment}-data
      VersioningConfiguration:
        Status: !FindInMap [EnvironmentSettings, !Ref Environment, VersioningStatus]
```

## Conditions

Use `Conditions` to conditionally create resources based on parameters.

```yaml
Parameters:
  EnableVersioning:
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

  CreateLifecycleRule:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

Conditions:
  ShouldEnableVersioning: !Equals [!Ref EnableVersioning, true]
  IsProduction: !Equals [!Ref Environment, production]
  ShouldCreateLifecycle: !Equals [!Ref CreateLifecycleRule, true]

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${Environment}-data-bucket
      VersioningConfiguration:
        Status: !If [ShouldEnableVersioning, Enabled, Suspended]

  LifecycleRule:
    Type: AWS::S3::Bucket
    Condition: ShouldCreateLifecycle
    Properties:
      BucketName: !Sub ${Environment}-lifecycle-bucket
      LifecycleConfiguration:
        Rules:
          - Status: Enabled
            ExpirationInDays: !If
              - IsProduction
              - 90
              - 30
            NoncurrentVersionExpirationInDays: 30
```

## Transform

Use `Transform` for macros like AWS::Serverless for SAM templates.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: SAM template with S3 bucket trigger

Resources:
  ThumbnailFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: python3.9
      CodeUri: function/
      Events:
        ImageUpload:
          Type: S3
          Properties:
            Bucket: !Ref ImageBucket
            Events: s3:ObjectCreated:*

  ImageBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-images
```

## Outputs and Cross-Stack References

### Basic Outputs

```yaml
Outputs:
  BucketName:
    Description: Name of the S3 bucket
    Value: !Ref DataBucket

  BucketArn:
    Description: ARN of the S3 bucket
    Value: !GetAtt DataBucket.Arn

  BucketDomainName:
    Description: Domain name of the S3 bucket
    Value: !GetAtt DataBucket.DomainName

  BucketWebsiteURL:
    Description: Website URL for the S3 bucket
    Value: !GetAtt DataBucket.WebsiteURL
```

### Exporting Values for Cross-Stack References

Export values so other stacks can import them.

```yaml
Outputs:
  BucketName:
    Description: Bucket name for other stacks
    Value: !Ref DataBucket
    Export:
      Name: !Sub ${AWS::StackName}-BucketName

  BucketArn:
    Description: Bucket ARN for other stacks
    Value: !GetAtt DataBucket.Arn
    Export:
      Name: !Sub ${AWS::StackName}-BucketArn

  BucketRegion:
    Description: Bucket region
    Value: !Ref AWS::Region
    Export:
      Name: !Sub ${AWS::StackName}-BucketRegion
```

### Importing Values in Another Stack

```yaml
Parameters:
  DataBucketName:
    Type: AWS::S3::Bucket::Name
    Description: Data bucket name from data stack
    # User selects from exported values in console

  # Or use Fn::ImportValue for programmatic access
Resources:
  BucketAccessRole:
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
        - PolicyName: S3Access
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: !Sub
                  - ${BucketArn}/*
                  - BucketArn: !ImportValue data-stack-BucketArn
```

### Cross-Stack Reference Pattern

Create a dedicated data storage stack that exports values:

```yaml
# storage-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: S3 storage infrastructure stack

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-data
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  LogBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-logs
      AccessControl: LogDeliveryWrite

Outputs:
  DataBucketName:
    Value: !Ref DataBucket
    Export:
      Name: !Sub ${AWS::StackName}-DataBucketName

  DataBucketArn:
    Value: !GetAtt DataBucket.Arn
    Export:
      Name: !Sub ${AWS::StackName}-DataBucketArn

  LogBucketName:
    Value: !Ref LogBucket
    Export:
      Name: !Sub ${AWS::StackName}-LogBucketName
```

Application stack imports these values:

```yaml
# application-stack.yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Application stack that imports from storage

Parameters:
  StorageStackName:
    Type: String
    Description: Name of the storage stack
    Default: storage-stack

Resources:
  ApplicationBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${AWS::StackName}-application
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders:
              - "*"
            AllowedMethods:
              - GET
              - PUT
              - POST
            AllowedOrigins:
              - !Ref ApplicationDomain
            MaxAge: 3600
```

## S3 Bucket Configuration

### Bucket with Public Access Block

```yaml
Resources:
  SecureBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-secure-bucket
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
```

### Bucket with Versioning

```yaml
Resources:
  VersionedBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-versioned-bucket
      VersioningConfiguration:
        Status: Enabled
        # Use MFADelete to require MFA for version deletion
        # MFADelete: Enabled  # Optional, requires MFA
```

### Bucket with Lifecycle Rules

```yaml
Resources:
  LifecycleBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-lifecycle-bucket
      LifecycleConfiguration:
        Rules:
          # Expire objects after 30 days
          - Id: ExpireOldObjects
            Status: Enabled
            ExpirationInDays: 30
            NoncurrentVersionExpirationInDays: 7
          # Archive to Glacier after 90 days
          - Id: ArchiveToGlacier
            Status: Enabled
            Transitions:
              - Days: 90
                StorageClass: GLACIER
              - Days: 365
                StorageClass: DEEP_ARCHIVE
            NoncurrentVersionTransitions:
              - NoncurrentDays: 30
                StorageClass: GLACIER
```

### Bucket with Cross-Region Replication

```yaml
Resources:
  SourceBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-source-bucket
      VersioningConfiguration:
        Status: Enabled
      ReplicationConfiguration:
        Role: !GetAtt ReplicationRole.Arn
        Rules:
          - Id: ReplicateToDestRegion
            Status: Enabled
            Destination:
              Bucket: !Sub arn:aws:s3:::my-dest-bucket-${AWS::Region}
              StorageClass: STANDARD_IA
              EncryptionConfiguration:
                ReplicaKmsKeyID: !Ref DestKMSKey

  ReplicationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action: sts:AssumeRole
```

## Bucket Policies

### Bucket Policy for Private Access

```yaml
Resources:
  PrivateBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-private-bucket
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref PrivateBucket
      PolicyDocument:
        Statement:
          - Sid: DenyPublicRead
            Effect: Deny
            Principal: "*"
            Action:
              - s3:GetObject
            Resource: !Sub ${PrivateBucket.Arn}/*
            Condition:
              Bool:
                aws:SecureTransport: false
```

### Bucket Policy for CloudFront OAI

```yaml
Resources:
  StaticWebsiteBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-static-website
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: error.html

  BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref StaticWebsiteBucket
      PolicyDocument:
        Statement:
          - Sid: CloudFrontReadAccess
            Effect: Allow
            Principal:
              CanonicalUser: !GetAtt CloudFrontOAI.S3CanonicalUserId
            Action: s3:GetObject
            Resource: !Sub ${StaticWebsiteBucket.Arn}/*

  CloudFrontOAI:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: !Sub ${AWS::StackName}-oai
```

### Bucket Policy for VPC Endpoint

```yaml
Resources:
  PrivateBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-private-bucket

  BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref PrivateBucket
      PolicyDocument:
        Statement:
          - Sid: AllowVPCEndpoint
            Effect: Allow
            Principal: "*"
            Action: s3:GetObject
            Resource: !Sub ${PrivateBucket.Arn}/*
            Condition:
              StringEquals:
                aws:sourceVpce: !Ref VPCEndpointId
```

## Complete S3 Bucket Example

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Production-ready S3 bucket with versioning, logging, and lifecycle

Parameters:
  BucketName:
    Type: String
    Description: Name of the S3 bucket

  Environment:
    Type: String
    Default: production
    AllowedValues:
      - development
      - staging
      - production

  EnableVersioning:
    Type: String
    Default: true
    AllowedValues:
      - true
      - false

  RetentionDays:
    Type: Number
    Default: 90
    Description: Days to retain objects

Conditions:
  ShouldEnableVersioning: !Equals [!Ref EnableVersioning, true]
  IsProduction: !Equals [!Ref Environment, production]

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
      VersioningConfiguration:
        Status: !If [ShouldEnableVersioning, Enabled, Suspended]
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LoggingConfiguration:
        DestinationBucketName: !Ref AccessLogBucket
        LogFilePrefix: !Sub ${BucketName}/logs/
      LifecycleConfiguration:
        Rules:
          - Id: StandardLifecycle
            Status: Enabled
            ExpirationInDays: !Ref RetentionDays
            NoncurrentVersionExpirationInDays: 30
            Transitions:
              - Days: 30
                StorageClass: STANDARD_IA
              - Days: 90
                StorageClass: GLACIER
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Name
          Value: !Ref BucketName

  AccessLogBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub ${BucketName}-logs
      AccessControl: LogDeliveryWrite
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: DeleteLogsAfter30Days
            Status: Enabled
            ExpirationInDays: 30

Outputs:
  BucketName:
    Description: Name of the S3 bucket
    Value: !Ref DataBucket

  BucketArn:
    Description: ARN of the S3 bucket
    Value: !GetAtt DataBucket.Arn

  BucketDomainName:
    Description: Domain name of the S3 bucket
    Value: !GetAtt DataBucket.DomainName

  BucketWebsiteURL:
    Description: Website URL for the S3 bucket
    Value: !GetAtt DataBucket.WebsiteURL

  LogBucketName:
    Description: Name of the access log bucket
    Value: !Ref AccessLogBucket
```

## CloudFormation Best Practices

### Stack Policies

Stack Policies protect stack resources from unintentional updates that could cause disruption or data loss. Use them to prevent accidental modifications to critical resources.

#### Setting a Stack Policy

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
      "Resource": "LogicalResourceId/DataBucket"
    },
    {
      "Effect": "Deny",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "LogicalResourceId/AccessLogBucket",
      "Condition": {
        "StringEquals": {
          "ResourceType": ["AWS::S3::Bucket"]
        }
      }
    }
  ]
}
```

#### Applying Stack Policy via AWS CLI

```bash
aws cloudformation set-stack-policy \
  --stack-name my-s3-stack \
  --stack-policy-body file://stack-policy.json
```

#### Stack Policy for Production Environment

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["Update:Modify", "Update:Replace", "Update:Delete"],
      "Principal": "*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "ResourceType": ["AWS::S3::Bucket"]
        }
      }
    },
    {
      "Effect": "Deny",
      "Action": "Update:Delete",
      "Principal": "*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "AWS": ["arn:aws:iam::123456789012:role/AdminRole"],
      "Resource": "*"
    }
  ]
}
```

### Termination Protection

Termination Protection prevents accidental deletion of CloudFormation stacks. Always enable it for production stacks.

#### Enabling Termination Protection

```bash
# Enable termination protection when creating a stack
aws cloudformation create-stack \
  --stack-name my-s3-stack \
  --template-body file://template.yaml \
  --enable-termination-protection

# Enable termination protection on existing stack
aws cloudformation update-termination-protection \
  --stack-name my-s3-stack \
  --enable-termination-protection

# Disable termination protection
aws cloudformation update-termination-protection \
  --stack-name my-s3-stack \
  --no-enable-termination-protection
```

#### Termination Protection in SDK (Python)

```python
import boto3

def enable_termination_protection(stack_name):
    cfn = boto3.client('cloudformation')
    try:
        cfn.update_termination_protection(
            StackName=stack_name,
            EnableTerminationProtection=True
        )
        print(f"Termination protection enabled for stack: {stack_name}")
    except cfn.exceptions.TerminationProtectionError as e:
        if "already" in str(e).lower():
            print(f"Termination protection already enabled for stack: {stack_name}")
        else:
            raise
```

#### Verification Script

```bash
#!/bin/bash
# verify-termination-protection.sh

STACK_NAME=$1

if [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <stack-name>"
    exit 1
fi

STATUS=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].TerminationProtection' \
  --output text)

if [ "$STATUS" = "True" ]; then
    echo "Termination protection is ENABLED for $STACK_NAME"
    exit 0
else
    echo "WARNING: Termination protection is DISABLED for $STACK_NAME"
    exit 1
fi
```

### Drift Detection

Drift Detection identifies differences between the actual infrastructure and the CloudFormation template. Run it regularly to ensure compliance.

#### Detecting Drift

```bash
# Detect drift on a single stack
aws cloudformation detect-drift \
  --stack-name my-s3-stack

# Detect drift and get detailed results
STACK_NAME="my-s3-stack"

# Start drift detection
aws cloudformation detect-drift \
  --stack-name $STACK_NAME

# Wait for drift detection to complete
aws cloudformation wait stack-drift-detection-complete \
  --stack-name $STACK_NAME

# Get drift detection status
STATUS=$(aws cloudformation describe-stack-drift-detection-status \
  --stack-name $STACK_NAME \
  --query 'StackDriftStatus' \
  --output text)

echo "Stack drift status: $STATUS"

# Get detailed drift information
if [ "$STATUS" = "DRIFTED" ]; then
  aws cloudformation describe-stack-resource-drifts \
    --stack-name $STACK_NAME \
    --query 'StackResourceDrifts[*].[LogicalResourceId,ResourceType,DriftStatus,PropertyDifferences]' \
    --output table
fi
```

#### Drift Detection Script with Reporting

```bash
#!/bin/bash
# detect-drift.sh

STACK_NAME=$1
REPORT_FILE="drift-report-${STACK_NAME}-$(date +%Y%m%d).json"

if [ -z "$STACK_NAME" ]; then
    echo "Usage: $0 <stack-name> [report-file]"
    exit 1
fi

if [ -n "$2" ]; then
    REPORT_FILE=$2
fi

echo "Starting drift detection for stack: $STACK_NAME"

# Start drift detection
DETECTION_ID=$(aws cloudformation detect-drift \
  --stack-name $STACK_NAME \
  --query 'Id' \
  --output text)

echo "Drift detection initiated. Detection ID: $DETECTION_ID"

# Wait for completion
echo "Waiting for drift detection to complete..."
aws cloudformation wait stack-drift-detection-complete \
  --stack-name $STACK_NAME 2>/dev/null || true

# Get detection status
DRIFT_STATUS=$(aws cloudformation describe-stack-drift-detection-status \
  --stack-name $STACK_NAME \
  --query 'StackDriftStatus' \
  --output text 2>/dev/null)

echo "Drift status: $DRIFT_STATUS"

# Get detailed results
if [ "$DRIFT_STATUS" = "DRIFTED" ]; then
    echo "Resources with drift detected:"
    aws cloudformation describe-stack-resource-drifts \
      --stack-name $STACK_NAME \
      --output json > "$REPORT_FILE"

    echo "Drift report saved to: $REPORT_FILE"

    # Display summary
    aws cloudformation describe-stack-resource-drifts \
      --stack-name $STACK_NAME \
      --query 'StackResourceDrifts[?DriftStatus==`MODIFIED`].[LogicalResourceId,ResourceType,PropertyDifferences[].PropertyName]' \
      --output table
else
    echo "No drift detected. Stack is in sync with template."
    echo "{}" > "$REPORT_FILE"
fi
```

#### Drift Detection for Multiple Stacks

```python
import boto3
from datetime import datetime

def detect_drift_all_stacks(prefix="prod-"):
    cfn = boto3.client('cloudformation')
    s3 = boto3.client('s3')

    # List all stacks with prefix
    stacks = cfn.list_stacks(
        StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE']
    )['StackSummaries']

    target_stacks = [s for s in stacks if s['StackName'].startswith(prefix)]

    drift_results = []

    for stack in target_stacks:
        stack_name = stack['StackName']
        print(f"Checking drift for: {stack_name}")

        # Start drift detection
        response = cfn.detect_drift(StackName=stack_name)
        detection_id = response['Id']

        # Wait for completion (simplified - in production use waiter)
        waiter = cfn.get_waiter('stack_drift_detection_complete')
        waiter.wait(StackName=stack_name)

        # Get status
        status = cfn.describe_stack_drift_detection_status(
            StackName=stack_name
        )

        drift_results.append({
            'stack_name': stack_name,
            'drift_status': status['StackDriftStatus'],
            'detection_time': datetime.utcnow().isoformat()
        })

        if status['StackDriftStatus'] == 'DRIFTED':
            # Get detailed drift info
            resources = cfn.describe_stack_resource_drifts(
                StackName=stack_name
            )['StackResourceDrifts']
            drift_results[-1]['drifted_resources'] = [
                {
                    'logical_id': r['LogicalResourceId'],
                    'type': r['ResourceType'],
                    'status': r['DriftStatus']
                } for r in resources
            ]

    return drift_results
```

### Change Sets

Change Sets preview changes before applying them. Always use them for production deployments to review impact.

#### Creating and Executing a Change Set

```bash
#!/bin/bash
# deploy-with-changeset.sh

STACK_NAME=$1
TEMPLATE_FILE=$2
CHANGESET_NAME="${STACK_NAME}-changeset-$(date +%Y%m%d%H%M%S)"

if [ -z "$STACK_NAME" ] || [ -z "$TEMPLATE_FILE" ]; then
    echo "Usage: $0 <stack-name> <template-file>"
    exit 1
fi

echo "Creating change set for stack: $STACK_NAME"

# Create change set
aws cloudformation create-change-set \
  --stack-name $STACK_NAME \
  --template-body file://$TEMPLATE_FILE \
  --change-set-name $CHANGESET_NAME \
  --capabilities CAPABILITY_IAM \
  --change-set-type UPDATE

echo "Change set created: $CHANGESET_NAME"

# Wait for change set creation
aws cloudformation wait change-set-create-complete \
  --stack-name $STACK_NAME \
  --change-set-name $CHANGESET_NAME

# Display changes
echo ""
echo "=== Change Set Summary ==="
aws cloudformation describe-change-set \
  --stack-name $STACK_NAME \
  --change-set-name $CHANGESET_NAME \
  --query '[ChangeSetName,Status,ChangeSetStatus,StatusReason]' \
  --output table

echo ""
echo "=== Detailed Changes ==="
aws cloudformation list-change-sets \
  --stack-name $STACK_NAME \
  --query "Summaries[?ChangeSetName=='$CHANGESET_NAME'].[Changes]" \
  --output text | python3 -m json.tool 2>/dev/null || \
aws cloudformation describe-change-set \
  --stack-name $STACK_NAME \
  --change-set-name $CHANGESET_NAME \
  --query 'Changes[*].ResourceChange' \
  --output table

# Prompt for execution
echo ""
read -p "Execute this change set? (yes/no): " CONFIRM

if [ "$CONFIRM" = "yes" ]; then
    echo "Executing change set..."
    aws cloudformation execute-change-set \
      --stack-name $STACK_NAME \
      --change-set-name $CHANGESET_NAME

    echo "Waiting for stack update to complete..."
    aws cloudformation wait stack-update-complete \
      --stack-name $STACK_NAME

    echo "Stack update complete!"
else
    echo "Change set execution cancelled."
    echo "To execute later, run:"
    echo "aws cloudformation execute-change-set --stack-name $STACK_NAME --change-set-name $CHANGESET_NAME"
fi
```

#### Change Set with Parameter Overrides

```bash
# Create change set with parameters
aws cloudformation create-change-set \
  --stack-name my-s3-stack \
  --template-body file://template.yaml \
  --change-set-name my-changeset \
  --parameters \
    ParameterKey=BucketName,ParameterValue=my-new-bucket \
    ParameterKey=Environment,ParameterValue=production \
  --capabilities CAPABILITY_IAM

# Generate change set from existing stack
aws cloudformation create-change-set \
  --stack-name my-s3-stack \
  --template-body file://new-template.yaml \
  --change-set-name migrate-to-new-template \
  --change-set-type IMPORT \
  --resources-to-import "[\"DataBucket\", \"AccessLogBucket\"]"
```

#### Change Set Preview Script

```python
import boto3

def preview_changes(stack_name, template_body, parameters=None):
    cfn = boto3.client('cloudformation')
    changeset_name = f"{stack_name}-preview-{int(__import__('time').time())}"

    try:
        # Create change set
        kwargs = {
            'StackName': stack_name,
            'TemplateBody': template_body,
            'ChangeSetName': changeset_name,
            'ChangeSetType': 'UPDATE'
        }

        if parameters:
            kwargs['Parameters'] = parameters

        response = cfn.create_change_set(**kwargs)

        # Wait for creation
        waiter = cfn.get_waiter('change_set_create_complete')
        waiter.wait(StackName=stack_name, ChangeSetName=changeset_name)

        # Get change set description
        changeset = cfn.describe_change_set(
            StackName=stack_name,
            ChangeSetName=changeset_name
        )

        print(f"Change Set: {changeset['ChangeSetName']}")
        print(f"Status: {changeset['Status']}")
        print(f"Number of changes: {len(changeset.get('Changes', []))}")

        # Display each change
        for change in changeset.get('Changes', []):
            resource = change['ResourceChange']
            print(f"\n{resource['Action']} {resource['LogicalResourceId']} ({resource['ResourceType']})")

            if resource.get('Replacement') == 'True':
                print(f"  - This resource will be REPLACED (potential downtime)")

            for detail in resource.get('Details', []):
                print(f"  - {detail['Attribute']}: {detail['Name']}")

        return changeset

    except cfn.exceptions.AlreadyExistsException:
        print(f"Change set already exists")
        return None
    finally:
        # Clean up change set
        try:
            cfn.delete_change_set(
                StackName=stack_name,
                ChangeSetName=changeset_name
            )
        except Exception:
            pass
```

#### Change Set Best Practices

```bash
# Best practices for change sets

# 1. Always use descriptive change set names
CHANGESET_NAME="update-bucket-config-$(date +%Y%m%d)"

# 2. Use appropriate change set type
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-type UPDATE \
  --template-body file://template.yaml

# 3. Review changes before execution
aws cloudformation describe-change-set \
  --stack-name my-stack \
  --change-set-name $CHANGESET_NAME \
  --query 'Changes[].ResourceChange'

# 4. Use capabilities flag when needed
aws cloudformation create-change-set \
  --stack-name my-stack \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --template-body file://template.yaml

# 5. Set execution role for controlled deployments
aws cloudformation create-change-set \
  --stack-name my-stack \
  --execution-role-name arn:aws:iam::123456789012:role/CloudFormationExecutionRole \
  --template-body file://template.yaml
```

## Related Files

For detailed resource reference information, see:
- [reference.md](reference.md) - Complete AWS::S3::Bucket and AWS::S3::BucketPolicy properties

For comprehensive examples, see:
- [examples.md](examples.md) - Real-world S3 patterns and use cases
