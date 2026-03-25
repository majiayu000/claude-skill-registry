---
name: aws-cloudformation-s3
description: Provides AWS CloudFormation patterns for Amazon S3. Use when creating S3 buckets, policies, versioning, lifecycle rules, and implementing template structure with Parameters, Outputs, Mappings, Conditions, and cross-stack references.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation S3 Patterns

Provides S3 bucket configurations, policies, versioning, lifecycle rules, and CloudFormation template structure best practices for production-ready infrastructure.

## When to Use

- Creating S3 buckets with custom configurations
- Implementing bucket policies for access control
- Configuring S3 versioning for data protection
- Setting up lifecycle rules for data management
- Creating Outputs for cross-stack references
- Using Parameters with AWS-specific types
- Organizing templates with Mappings and Conditions

## Overview

S3 bucket configurations, policies, versioning, lifecycle rules, and CloudFormation template structure for production-ready infrastructure.

## Instructions

1. **Define Bucket Resources**: Create `AWS::S3::Bucket` with versioning, encryption, PublicAccessBlock
2. **Configure Bucket Policy**: Set up IAM policies for access control
3. **Set Up Lifecycle Rules**: Define transitions and expiration policies
4. **Configure CORS**: Allow cross-origin requests if needed
5. **Add Outputs**: Export bucket names/ARNs for cross-stack references

**Validate before deploy:**
```bash
aws cloudformation validate-template --template-body file://template.yaml
```

**Deploy with rollback on failure:**
```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-s3-stack \
  --capabilities CAPABILITY_IAM
```

If deployment fails, CloudFormation automatically rolls back. Check failures with:
```bash
aws cloudformation describe-stack-events --stack-name my-s3-stack
```

## Quick Reference

| Resource Type | Purpose |
|---------------|---------|
| `AWS::S3::Bucket` | Create S3 bucket |
| `AWS::S3::BucketPolicy` | Set bucket-level policies |
| `AWS::S3::BucketReplication` | Cross-region replication |
| Parameters | Input values for customization |
| Mappings | Static configuration tables |
| Conditions | Conditional resource creation |
| Outputs | Return values for cross-stack references |

## Examples

### Basic S3 Bucket

```yaml
Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket
```

### Bucket with Versioning and Encryption

```yaml
DataBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: !Sub "${AWS::StackName}-data"
    VersioningConfiguration:
      Status: Enabled
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: AES256
    PublicAccessBlockConfiguration:
      BlockPublicAcls: true
      BlockPublicPolicy: true
```

### Lifecycle Rule

```yaml
DataBucket:
  Type: AWS::S3::Bucket
  Properties:
    LifecycleConfiguration:
      Rules:
        - Id: ArchiveOldData
          Status: Enabled
          Transitions:
            - StorageClass: GLACIER
              TransitionInDays: 365
```

### Bucket Policy

```yaml
BucketPolicy:
  Type: AWS::S3::BucketPolicy
  Properties:
    Bucket: !Ref DataBucket
    PolicyDocument:
      Statement:
        - Effect: Allow
          Principal:
            AWS: !Ref RoleArn
          Action:
            - s3:GetObject
          Resource: !Sub "${DataBucket.Arn}/*"
```

See [references/complete-examples.md](references/complete-examples.md) for more complete examples including CORS, static websites, replication, and production-ready configurations.

## Template Structure

### Template Sections

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: Template description

Mappings: {}       # Static configuration tables
Metadata: {}       # Additional information
Parameters: {}     # Input values
Conditions: {}     # Conditional creation
Transform: {}      # Macro processing
Resources: {}      # AWS resources (REQUIRED)
Outputs: {}        # Return values
```

### Parameters

```yaml
Parameters:
  BucketName:
    Type: String
    Description: S3 bucket name
    Default: my-bucket
    MinLength: 3
    MaxLength: 63
    AllowedPattern: '^[a-z0-9-]+$'
```

### Conditions

```yaml
Conditions:
  IsProduction: !Equals [!Ref Environment, prod]
  ShouldEnableVersioning: !Equals [!Ref EnableVersioning, 'true']

Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration:
        Status: !If [ShouldEnableVersioning, Enabled, Suspended]
```

### Outputs

```yaml
Outputs:
  BucketName:
    Description: Name of the S3 bucket
    Value: !Ref DataBucket
    Export:
      Name: !Sub '${AWS::StackName}-BucketName'
```

See [references/advanced-configuration.md](references/advanced-configuration.md) for detailed Mappings, Conditions, Parameters, and cross-stack references.

## Best Practices

1. **Public Access Block**: Always enable for non-static website buckets
2. **Versioning**: Enable for critical data to prevent accidental deletion
3. **Bucket Policies**: Use instead of ACLs for access control
4. **Lifecycle Rules**: Implement cost optimization with tiering
5. **Encryption**: Enable default encryption (SSE-KMS or AES256)
6. **Tags**: Tag all resources for organization and cost allocation
7. **Outputs**: Export bucket names/ARNs for cross-stack references
8. **Parameters**: Use parameters for reusability across environments

## Common Troubleshooting

**Bucket already exists**: Use unique bucket names with CloudFormation stack name
**Access denied**: Verify bucket policy and IAM permissions
**Versioning conflicts**: Cannot suspend versioning once objects exist
**Lifecycle not working**: Check rule status and prefix filters
**Cross-stack references**: Ensure outputs are exported before importing

## Related Skills

- [aws-cloudformation-security](../aws-cloudformation-security/) - Security best practices for S3
- [aws-cloudformation-lambda](../aws-cloudformation-lambda/) - Lambda triggers for S3 events
- [aws-cloudformation-iam](../aws-cloudformation-iam/) - IAM roles for S3 access

## References

### Complete Examples
- **[references/complete-examples.md](references/complete-examples.md)** - Basic buckets, versioning, lifecycle, CORS, policies, production stacks, event notifications, static websites, replication

### Advanced Configuration
- **[references/advanced-configuration.md](references/advanced-configuration.md)** - Parameters, Mappings, Conditions, Outputs, Metadata, DeletionPolicy, DependsOn, Transform

## Constraints and Warnings

- **Bucket names**: Must be globally unique (across all AWS accounts)
- **Versioning**: Cannot be suspended once objects exist in bucket
- **Lifecycle rules**: Minimum 1 day for expiration, 0 days for transitions
- **Bucket policies**: Limited to 20 KB in size
- **Public access**: Blocked by default; requires explicit configuration
- **CORS**: Limited to 100 rules per bucket
- **Replication**: Versioning must be enabled on both source and destination
- **Encryption**: KMS keys must be in same region as bucket
- **Tags**: Maximum 50 tags per resource
- **Stack limits**: CloudFormation limits resources per stack (200 default)
