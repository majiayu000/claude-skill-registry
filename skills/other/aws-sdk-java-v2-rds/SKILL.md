---
name: aws-sdk-java-v2-rds
description: Provides AWS RDS (Relational Database Service) management patterns using AWS SDK for Java 2.x. Use when creating, modifying, monitoring, or managing Amazon RDS database instances, snapshots, parameter groups, and configurations.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java v2 - RDS Management

## Overview

This skill provides comprehensive guidance for working with Amazon RDS (Relational Database Service) using the AWS SDK for Java 2.x, covering database instance management, snapshots, parameter groups, and RDS operations.

## When to Use

- Creating, modifying, or deleting RDS database instances
- Managing DB snapshots, parameter groups, and configurations
- Setting up Multi-AZ deployments and automated backups
- Connecting Lambda functions to RDS databases
- Monitoring instance status and performance

## Instructions

Follow these steps to work with Amazon RDS:

1. **Add Dependencies** - Include AWS RDS SDK dependency and database drivers
2. **Create RDS Client** - Instantiate RdsClient with proper region and credentials
3. **Create DB Instance** - Use createDBInstance() with appropriate configuration
4. **Configure Security** - Set up VPC security groups and encryption
5. **Set Up Backups** - Configure automated backup windows and retention
6. **Monitor Status** - Use describeDBInstances() to check instance state
7. **Create Snapshots** - Take manual snapshots before major changes
8. **Handle Failover** - Configure Multi-AZ for high availability

## Getting Started

### RDS Client Setup

The `RdsClient` is the main entry point for interacting with Amazon RDS.

**Basic Client Creation:**
```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.rds.RdsClient;

RdsClient rdsClient = RdsClient.builder()
    .region(Region.US_EAST_1)
    .build();

// Use client
describeInstances(rdsClient);

// Always close the client
rdsClient.close();
```

**Client with Custom Configuration:**
```java
import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.http.apache.ApacheHttpClient;

RdsClient rdsClient = RdsClient.builder()
    .region(Region.US_WEST_2)
    .credentialsProvider(ProfileCredentialsProvider.create("myprofile"))
    .httpClient(ApacheHttpClient.builder()
        .connectionTimeout(Duration.ofSeconds(30))
        .socketTimeout(Duration.ofSeconds(60))
        .build())
    .build();
```

### Describing DB Instances

```java
DescribeDbInstancesResponse response = rdsClient.describeDBInstances();
for (DBInstance instance : response.dbInstances()) {
    System.out.println(instance.dbInstanceArn() + " - " + instance.dbInstanceStatus());
}
```

## Key Operations

### Creating DB Instances

```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .dbInstanceIdentifier(dbInstanceIdentifier)
    .dbName(dbName)
    .engine("postgres")
    .engineVersion("15.4")
    .dbInstanceClass("db.t3.micro")
    .allocatedStorage(20)
    .masterUsername(masterUsername)
    .masterUserPassword(masterPassword)
    .publiclyAccessible(false)
    .build();

CreateDbInstanceResponse response = rdsClient.createDBInstance(request);

// VALIDATION CHECKPOINT: Wait for instance to be available
rdsClient.waiter().waitUntilDBInstanceAvailable(
    DescribeDbInstancesRequest.builder().dbInstanceIdentifier(dbInstanceIdentifier).build()
);
System.out.println("Instance " + dbInstanceIdentifier + " is available!");
```

### Managing DB Parameter Groups

```java
CreateDbParameterGroupRequest request = CreateDbParameterGroupRequest.builder()
    .dbParameterGroupName(groupName)
    .dbParameterGroupFamily("postgres15")
    .description(description)
    .build();
rdsClient.createDBParameterGroup(request);
```

### Managing DB Snapshots

```java
CreateDbSnapshotRequest request = CreateDbSnapshotRequest.builder()
    .dbInstanceIdentifier(dbInstanceIdentifier)
    .dbSnapshotIdentifier(snapshotIdentifier)
    .build();
CreateDbSnapshotResponse response = rdsClient.createDBSnapshot(request);
```

## Integration Patterns

### Spring Boot Integration

Refer to [references/spring-boot-integration.md](references/spring-boot-integration.md) for complete Spring Boot integration examples including:

- Spring Boot configuration with application properties
- RDS client bean configuration
- Service layer implementation
- REST controller design
- Exception handling
- Testing strategies

### Lambda Integration

Refer to [references/lambda-integration.md](references/lambda-integration.md) for Lambda integration examples including:

- Traditional Lambda + RDS connections
- Lambda with connection pooling
- Using AWS Secrets Manager for credentials
- Lambda with AWS SDK for RDS management
- Security configuration and best practices

## Advanced Operations

### Modifying DB Instances

```java
ModifyDbInstanceRequest request = ModifyDbInstanceRequest.builder()
    .dbInstanceIdentifier(dbInstanceIdentifier)
    .dbInstanceClass(newInstanceClass)
    .applyImmediately(false)
    .build();
rdsClient.modifyDBInstance(request);
```

### Deleting DB Instances

```java
// VALIDATION CHECKPOINT: Verify instance exists and check status
DBInstance instance = rdsClient.describeDBInstances(
    DescribeDbInstancesRequest.builder().dbInstanceIdentifier(dbInstanceIdentifier).build()
).dbInstances().get(0);

if ("available".equals(instance.dbInstanceStatus())) {
    DeleteDbInstanceRequest request = DeleteDbInstanceRequest.builder()
        .dbInstanceIdentifier(dbInstanceIdentifier)
        .skipFinalSnapshot(false)
        .finalDBSnapshotIdentifier(snapshotId)
        .build();
    rdsClient.deleteDBInstance(request);
}
```

## Examples

### Complete RDS Instance Creation with Validation

```java
public String createSecurePostgreSQLInstance(RdsClient rdsClient,
                                            String instanceIdentifier,
                                            String dbName,
                                            String masterUsername,
                                            String masterPassword,
                                            String vpcSecurityGroupId) {
    // Create instance with security settings
    CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
        .dbInstanceIdentifier(instanceIdentifier)
        .dbName(dbName)
        .masterUsername(masterUsername)
        .masterUserPassword(masterPassword)
        .engine("postgres")
        .engineVersion("15.4")
        .dbInstanceClass("db.t3.micro")
        .allocatedStorage(20)
        .storageEncrypted(true)
        .vpcSecurityGroupIds(vpcSecurityGroupId)
        .publiclyAccessible(false)
        .multiAZ(true)
        .backupRetentionPeriod(7)
        .deletionProtection(true)
        .build();

    rdsClient.createDBInstance(request);

    // VALIDATION: Wait for instance availability
    rdsClient.waiter().waitUntilDBInstanceAvailable(
        DescribeDbInstancesRequest.builder().dbInstanceIdentifier(instanceIdentifier).build()
    );
    System.out.println("Instance " + instanceIdentifier + " is available!");
    return instanceIdentifier;
}
```

## Best Practices

**Security**: Enable encryption (`storageEncrypted=true`), use VPC security groups, disable public access.

**High Availability**: Enable Multi-AZ for production workloads.

**Backups**: Configure automated backups with 7+ day retention.

**Deletion Protection**: Enable `deletionProtection(true)` for production databases.

**Resource Management**: Always close clients with try-with-resources:
```java
try (RdsClient rdsClient = RdsClient.builder().region(Region.US_EAST_1).build()) {
    // Use client
}
```

## Dependencies

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>rds</artifactId>
    <version>2.20.0</version>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.6.0</version>
</dependency>
```

## Reference Documentation

For detailed API reference, see:
- [API Reference](references/api-reference.md) - Complete API documentation and data models
- [Spring Boot Integration](references/spring-boot-integration.md) - Spring Boot patterns and examples
- [Lambda Integration](references/lambda-integration.md) - Lambda function patterns and best practices

## Error Handling

See [API Reference](references/api-reference.md#error-handling) for comprehensive error handling patterns including common exceptions, error response structure, and pagination support.

## Constraints and Warnings

- **Instance Limits**: Account limits on DB instances per region
- **Multi-AZ Costs**: Approximately doubles compute costs
- **Snapshot Costs**: Manual snapshots billed per storage used
- **Deletion Protection**: Cannot delete instances with protection enabled
- **Maintenance Windows**: Instances may be unavailable during updates