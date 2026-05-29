---
name: aws-sdk-java-v2-rds
description: AWS RDS (Relational Database Service) management using AWS SDK for Java 2.x. Use when creating, modifying, monitoring, or managing Amazon RDS database instances, snapshots, parameter groups, and configurations.
category: aws
tags: [aws, rds, database, java, sdk, postgresql, mysql, aurora, spring-boot]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# AWS SDK for Java v2 - RDS Management

This skill provides comprehensive guidance for working with Amazon RDS (Relational Database Service) using the AWS SDK for Java 2.x, covering database instance management, snapshots, parameter groups, and RDS operations.

## When to Use This Skill

Use this skill when:
- Creating and managing RDS database instances (PostgreSQL, MySQL, Aurora, etc.)
- Taking and restoring database snapshots
- Managing DB parameter groups and configurations
- Querying RDS instance metadata and status
- Setting up Multi-AZ deployments
- Configuring automated backups
- Managing security groups for RDS
- Connecting Lambda functions to RDS databases
- Implementing RDS IAM authentication
- Monitoring RDS instances and metrics

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

Retrieve information about existing RDS instances.

**List All DB Instances:**
```java
public static void describeInstances(RdsClient rdsClient) {
    try {
        DescribeDbInstancesResponse response = rdsClient.describeDBInstances();
        List<DBInstance> instanceList = response.dbInstances();

        for (DBInstance instance : instanceList) {
            System.out.println("Instance ARN: " + instance.dbInstanceArn());
            System.out.println("Engine: " + instance.engine());
            System.out.println("Status: " + instance.dbInstanceStatus());
            System.out.println("Endpoint: " + instance.endpoint().address());
            System.out.println("Port: " + instance.endpoint().port());
            System.out.println("---");
        }
    } catch (RdsException e) {
        System.err.println(e.getMessage());
        System.exit(1);
    }
}
```

## Key Operations

### Creating DB Instances

Create new RDS database instances with various configurations.

**Create Basic DB Instance:**
```java
public static String createDBInstance(RdsClient rdsClient,
                                     String dbInstanceIdentifier,
                                     String dbName,
                                     String masterUsername,
                                     String masterPassword) {
    try {
        CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
            .dbInstanceIdentifier(dbInstanceIdentifier)
            .dbName(dbName)
            .engine("postgres")
            .engineVersion("14.7")
            .dbInstanceClass("db.t3.micro")
            .allocatedStorage(20)
            .masterUsername(masterUsername)
            .masterUserPassword(masterPassword)
            .publiclyAccessible(false)
            .build();

        CreateDbInstanceResponse response = rdsClient.createDBInstance(request);
        System.out.println("Creating DB instance: " + response.dbInstance().dbInstanceArn());

        return response.dbInstance().dbInstanceArn();
    } catch (RdsException e) {
        System.err.println("Error creating instance: " + e.getMessage());
        throw e;
    }
}
```

### Managing DB Parameter Groups

Create and manage custom parameter groups for database configuration.

**Create DB Parameter Group:**
```java
public static void createDBParameterGroup(RdsClient rdsClient,
                                         String groupName,
                                         String description) {
    try {
        CreateDbParameterGroupRequest request = CreateDbParameterGroupRequest.builder()
            .dbParameterGroupName(groupName)
            .dbParameterGroupFamily("postgres15")
            .description(description)
            .build();

        CreateDbParameterGroupResponse response = rdsClient.createDBParameterGroup(request);
        System.out.println("Created parameter group: " + response.dbParameterGroup().dbParameterGroupName());
    } catch (RdsException e) {
        System.err.println("Error creating parameter group: " + e.getMessage());
        throw e;
    }
}
```

### Managing DB Snapshots

Create, restore, and manage database snapshots.

**Create DB Snapshot:**
```java
public static String createDBSnapshot(RdsClient rdsClient,
                                     String dbInstanceIdentifier,
                                     String snapshotIdentifier) {
    try {
        CreateDbSnapshotRequest request = CreateDbSnapshotRequest.builder()
            .dbInstanceIdentifier(dbInstanceIdentifier)
            .dbSnapshotIdentifier(snapshotIdentifier)
            .build();

        CreateDbSnapshotResponse response = rdsClient.createDBSnapshot(request);
        System.out.println("Creating snapshot: " + response.dbSnapshot().dbSnapshotIdentifier());

        return response.dbSnapshot().dbSnapshotArn();
    } catch (RdsException e) {
        System.err.println("Error creating snapshot: " + e.getMessage());
        throw e;
    }
}
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

Update existing RDS instances.

```java
public static void modifyDBInstance(RdsClient rdsClient,
                                   String dbInstanceIdentifier,
                                   String newInstanceClass) {
    try {
        ModifyDbInstanceRequest request = ModifyDbInstanceRequest.builder()
            .dbInstanceIdentifier(dbInstanceIdentifier)
            .dbInstanceClass(newInstanceClass)
            .applyImmediately(false) // Apply during maintenance window
            .build();

        ModifyDbInstanceResponse response = rdsClient.modifyDBInstance(request);
        System.out.println("Modified instance: " + response.dbInstance().dbInstanceIdentifier());
        System.out.println("New class: " + response.dbInstance().dbInstanceClass());
    } catch (RdsException e) {
        System.err.println("Error modifying instance: " + e.getMessage());
        throw e;
    }
}
```

### Deleting DB Instances

Delete RDS instances with optional final snapshot.

```java
public static void deleteDBInstanceWithSnapshot(RdsClient rdsClient,
                                               String dbInstanceIdentifier,
                                               String finalSnapshotIdentifier) {
    try {
        DeleteDbInstanceRequest request = DeleteDbInstanceRequest.builder()
            .dbInstanceIdentifier(dbInstanceIdentifier)
            .skipFinalSnapshot(false)
            .finalDBSnapshotIdentifier(finalSnapshotIdentifier)
            .build();

        DeleteDbInstanceResponse response = rdsClient.deleteDBInstance(request);
        System.out.println("Deleting instance: " + response.dbInstance().dbInstanceIdentifier());
    } catch (RdsException e) {
        System.err.println("Error deleting instance: " + e.getMessage());
        throw e;
    }
}
```

## Best Practices

### Security

**Always use encryption:**
```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .storageEncrypted(true)
    .kmsKeyId("arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012")
    .build();
```

**Use VPC security groups:**
```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .vpcSecurityGroupIds("sg-12345678")
    .publiclyAccessible(false)
    .build();
```

### High Availability

**Enable Multi-AZ for production:**
```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .multiAZ(true)
    .build();
```

### Backups

**Configure automated backups:**
```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .backupRetentionPeriod(7)
    .preferredBackupWindow("03:00-04:00")
    .build();
```

### Monitoring

**Enable CloudWatch logs:**
```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .enableCloudwatchLogsExports("postgresql", "upgrade")
    .build();
```

### Cost Optimization

**Use appropriate instance class:**
```java
// Development
.dbInstanceClass("db.t3.micro")

// Production
.dbInstanceClass("db.r5.large")
```

### Deletion Protection

**Enable for production databases:**
```java
CreateDbInstanceRequest request = CreateDbInstanceRequest.builder()
    .deletionProtection(true)
    .build();
```

### Resource Management

**Always close clients:**
```java
try (RdsClient rdsClient = RdsClient.builder()
    .region(Region.US_EAST_1)
    .build()) {
    // Use client
} // Automatically closed
```

## Dependencies

### Maven Dependencies

```xml
<dependencies>
    <!-- AWS SDK for RDS -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>rds</artifactId>
        <version>2.20.0</version> // Use the latest version available
    </dependency>

    <!-- PostgreSQL Driver -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>42.6.0</version> // Use the correct version available
    </dependency>

    <!-- MySQL Driver -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>8.0.33</version>
    </dependency>
</dependencies>
```

### Gradle Dependencies

```gradle
dependencies {
    // AWS SDK for RDS
    implementation 'software.amazon.awssdk:rds:2.20.0'

    // PostgreSQL Driver
    implementation 'org.postgresql:postgresql:42.6.0'

    // MySQL Driver
    implementation 'mysql:mysql-connector-java:8.0.33'
}
```

## Reference Documentation

For detailed API reference, see:
- [API Reference](references/api-reference.md) - Complete API documentation and data models
- [Spring Boot Integration](references/spring-boot-integration.md) - Spring Boot patterns and examples
- [Lambda Integration](references/lambda-integration.md) - Lambda function patterns and best practices

## Error Handling

See [API Reference](references/api-reference.md#error-handling) for comprehensive error handling patterns including common exceptions, error response structure, and pagination support.

## Performance Considerations

- Use connection pooling for multiple database operations
- Implement retry logic for transient failures
- Monitor CloudWatch metrics for performance optimization
- Use appropriate instance types for workload requirements
- Enable Performance Insights for database optimization

## Support

For support with AWS RDS operations using AWS SDK for Java 2.x:
- AWS Documentation: [Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- AWS SDK Documentation: [AWS SDK for Java 2.x](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/home.html)
- AWS Support: [AWS Support Center](https://aws.amazon.com/premiumsupport/)