---
name: aws-cloudformation-dynamodb
description: Provides AWS CloudFormation patterns for DynamoDB tables, GSIs, LSIs, auto-scaling, and streams. Use when creating DynamoDB tables with CloudFormation, configuring primary keys, local/global secondary indexes, capacity modes (on-demand/provisioned), point-in-time recovery, encryption, TTL, and implementing template structure with Parameters, Outputs, Mappings, Conditions, cross-stack references.
allowed-tools: Read, Write, Bash
---

# AWS CloudFormation DynamoDB Patterns

Provides production-ready NoSQL database infrastructure patterns using AWS CloudFormation templates with DynamoDB tables, GSIs, LSIs, auto-scaling, encryption, TTL, and streams.

## Overview

Covers DynamoDB tables, primary keys, secondary indexes (GSI/LSI), capacity modes, auto-scaling, encryption, TTL, streams, and best practices for parameters, outputs, and cross-stack references.

## When to Use

Creating DynamoDB tables, configuring keys and indexes, setting capacity modes, implementing auto-scaling, enabling encryption/TTL/streams, and organizing CloudFormation templates.

## Instructions

Follow these steps to create DynamoDB tables with CloudFormation:

1. **Define Table Parameters**: Specify table name and billing mode
2. **Configure Primary Key**: Set partition key and optional sort key
3. **Add Secondary Indexes**: Create GSIs for alternative access patterns
4. **Configure Encryption**: Enable encryption using KMS keys
5. **Set Up TTL**: Define timestamp attribute for automatic deletion
6. **Enable Streams**: Configure stream for change data capture
7. **Add Auto Scaling**: Implement Application Auto Scaling for provisioned capacity
8. **Create Backup**: Enable point-in-time recovery
9. **Validate Template**: Run `aws cloudformation validate-template` before deployment
10. **Deploy Stack**: Use `aws cloudformation create-stack` or `update-stack`
11. **Monitor Events**: Check `aws cloudformation describe-stack-events` for failures or `ROLLBACK` status
12. **Handle Rollback**: On failure, review events for resource errors, fix the template, and re-deploy

## Quick Reference

| Resource Type | Purpose |
|---------------|---------|
| `AWS::DynamoDB::Table` | Create DynamoDB table |
| `AWS::ApplicationAutoScaling::ScalableTarget` | Auto scaling configuration |
| `AWS::ApplicationAutoScaling::ScalingPolicy` | Scaling policies |
| `AWS::KMS::Key` | KMS key for encryption |
| `AWS::IAM::Role` | IAM roles for auto scaling |
| BillingMode | `PAY_PER_REQUEST` or `PROVISIONED` |
| SSESpecification | Server-side encryption |

## Examples

### Basic Table with On-Demand Capacity

```yaml
DynamoDBTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: !Sub "${AWS::StackName}-table"
    BillingMode: PAY_PER_REQUEST
    AttributeDefinitions:
      - AttributeName: pk
        AttributeType: S
    KeySchema:
      - AttributeName: pk
        KeyType: HASH
```

### Table with Global Secondary Index

```yaml
DynamoDBTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: !Sub "${AWS::StackName}-table"
    BillingMode: PAY_PER_REQUEST
    AttributeDefinitions:
      - AttributeName: pk
        AttributeType: S
      - AttributeName: gsi-pk
        AttributeType: S
    KeySchema:
      - AttributeName: pk
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: gsi-index
        KeySchema:
          - AttributeName: gsi-pk
            KeyType: HASH
        Projection:
          ProjectionType: ALL
```

### Table with TTL

```yaml
SessionTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: !Sub "${AWS::StackName}-sessions"
    BillingMode: PAY_PER_REQUEST
    AttributeDefinitions:
      - AttributeName: sessionId
        AttributeType: S
    KeySchema:
      - AttributeName: sessionId
        KeyType: HASH
    TimeToLiveSpecification:
      AttributeName: expiresAt
      Enabled: true
```

### Table with Auto Scaling

```yaml
ScalableTarget:
  Type: AWS::ApplicationAutoScaling::ScalableTarget
  Properties:
    MaxCapacity: 100
    MinCapacity: 5
    ResourceId: !Sub "table/${DynamoDBTable}"
    RoleARN: !GetAtt AutoScalingRole.Arn
    ScalableDimension: dynamodb:table:ReadCapacityUnits
    ServiceNamespace: dynamodb
```

See [references/complete-examples.md](references/complete-examples.md) for more complete examples including encryption, streams, auto scaling, and production tables.

## Template Structure

### Base Template

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: DynamoDB table with GSI and auto-scaling

Parameters:
  TableName:
    Type: String
    Default: my-table
  BillingMode:
    Type: String
    Default: PAY_PER_REQUEST

Resources:
  DynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Ref TableName
      BillingMode: !Ref BillingMode

Outputs:
  TableName:
    Value: !Ref DynamoDBTable
  TableArn:
    Value: !GetAtt DynamoDBTable.Arn
```

See [references/advanced-configuration.md](references/advanced-configuration.md) for detailed Parameters, Mappings, Conditions, Outputs, IAM roles, and cross-stack references.

## Best Practices

1. **Use PAY_PER_REQUEST** for development/testing and unpredictable workloads
2. **Enable Point-In-Time Recovery** for production tables
3. **Use KMS encryption** for sensitive data (SSE-KMS)
4. **Configure auto-scaling** for provisioned capacity tables
5. **Design GSIs carefully** - each GSI consumes capacity
6. **Use TTL** for automatic data expiration (sessions, cache)
7. **Enable Streams** for change data capture and analytics
8. **Tag resources** for cost allocation and organization
9. **Export outputs** for cross-stack references
10. **Use Conditions** for environment-specific configurations

## Common Troubleshooting

**Table already exists**: Use unique table names or stack deletion policy
**GSI creation fails**: Verify attribute definitions include GSI attributes
**Auto-scaling not working**: Check IAM role permissions and service-linked role
**TTL not expiring**: Ensure TTL attribute is Number type, not String
**Streams not enabled**: Can only enable streams during table creation
**Encryption errors**: Verify KMS key exists in same region as table

## Related Skills

- [aws-cloudformation-security](../aws-cloudformation-security/) - Security best practices for DynamoDB
- [aws-cloudformation-lambda](../aws-cloudformation-lambda/) - Lambda triggers for DynamoDB Streams
- [aws-cloudformation-iam](../aws-cloudformation-iam/) - IAM roles for DynamoDB access

## References

### Complete Examples
- **[references/complete-examples.md](references/complete-examples.md)** - Basic tables, GSI, LSI, TTL, encryption, PITR, auto-scaling, production tables, global tables, streams

### Advanced Configuration
- **[references/advanced-configuration.md](references/advanced-configuration.md)** - Parameters, Mappings, Conditions, auto scaling policies, streams, TTL, global tables, outputs, IAM roles, deletion policies

## Constraints and Warnings

- **Table names**: Must be unique per region (globally unique for global tables)
- **GSI limits**: Maximum 5 GSIs per table (for single-region tables)
- **LSI limits**: Maximum 5 LSIs per table, same partition key as table
- **Capacity limits**: On-demand has default account limits (40,000 RCUs, 40,000 WCUs)
- **Auto-scaling**: Requires PROVISIONED billing mode (not PAY_PER_REQUEST)
- **Point-in-time recovery**: Can only be enabled during table creation
- **Streams**: Can only be enabled during table creation
- **Encryption**: KMS keys must be in same region as table
- **TTL**: Attribute must be Number type, measured in seconds
- **Throughput**: Each GSI shares provisioned throughput with table
- **Item size limit**: Maximum 400 KB per item
- **Hot partition**: Design keys to avoid hot partition issues
