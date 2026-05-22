---
name: aws-rds-spring-boot-integration
description: Configure AWS RDS (Aurora, MySQL, PostgreSQL) with Spring Boot applications. Use when setting up datasources, connection pooling, security, and production-ready database configuration.
category: aws
tags: [aws, rds, aurora, spring-boot, spring-data-jpa, datasource, configuration, hikari, mysql, postgresql]
version: 1.1.0
allowed-tools: Read, Write, Bash, Glob
---

# AWS RDS Spring Boot Integration

Configure AWS RDS databases (Aurora, MySQL, PostgreSQL) with Spring Boot applications for production-ready connectivity.

## When to Use This Skill

Use this skill when:
- Setting up AWS RDS Aurora with Spring Data JPA
- Configuring datasource properties for Aurora, MySQL, or PostgreSQL endpoints
- Implementing HikariCP connection pooling for RDS
- Setting up environment-specific configurations (dev/prod)
- Configuring SSL connections to AWS RDS
- Troubleshooting RDS connection issues
- Setting up database migrations with Flyway
- Integrating with AWS Secrets Manager for credential management
- Optimizing connection pool settings for RDS workloads
- Implementing read/write split with Aurora

## Prerequisites

Before starting AWS RDS Spring Boot integration:
1. AWS account with RDS access
2. Spring Boot project (3.x)
3. RDS instance created and running (Aurora/MySQL/PostgreSQL)
4. Security group configured for database access
5. Database endpoint information available
6. Database credentials secured (environment variables or Secrets Manager)

## Quick Start

### Step 1: Add Dependencies

**Maven (pom.xml):**
```xml
<dependencies>
    <!-- Spring Data JPA -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <!-- Aurora MySQL Driver -->
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <version>8.2.0</version>
        <scope>runtime</scope>
    </dependency>

    <!-- Aurora PostgreSQL Driver (alternative) -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- Flyway for database migrations -->
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
    </dependency>

    <!-- Validation -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
</dependencies>
```

**Gradle (build.gradle):**
```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-validation'

    // Aurora MySQL
    runtimeOnly 'com.mysql:mysql-connector-j:8.2.0'

    // Aurora PostgreSQL (alternative)
    runtimeOnly 'org.postgresql:postgresql'

    // Flyway
    implementation 'org.flywaydb:flyway-core'
}
```

### Step 2: Basic Datasource Configuration

**application.properties (Aurora MySQL):**
```properties
# Aurora MySQL Datasource - Cluster Endpoint
spring.datasource.url=jdbc:mysql://myapp-aurora-cluster.cluster-abc123xyz.us-east-1.rds.amazonaws.com:3306/devops
spring.datasource.username=admin
spring.datasource.password=${DB_PASSWORD}
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA/Hibernate Configuration
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.open-in-view=false

# HikariCP Connection Pool
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=20000
spring.datasource.hikari.idle-timeout=300000
spring.datasource.hikari.max-lifetime=1200000

# Flyway Configuration
spring.flyway.enabled=true
spring.flyway.baseline-on-migrate=true
spring.flyway.locations=classpath:db/migration
```

**application.properties (Aurora PostgreSQL):**
```properties
# Aurora PostgreSQL Datasource
spring.datasource.url=jdbc:postgresql://myapp-aurora-pg-cluster.cluster-abc123xyz.us-east-1.rds.amazonaws.com:5432/devops
spring.datasource.username=admin
spring.datasource.password=${DB_PASSWORD}
spring.datasource.driver-class-name=org.postgresql.Driver

# JPA/Hibernate Configuration
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.properties.hibernate.jdbc.lob.non_contextual_creation=true
spring.jpa.open-in-view=false
```

### Step 3: Set Up Environment Variables

```bash
# Production environment variables
export DB_PASSWORD=YourStrongPassword123!
export SPRING_PROFILES_ACTIVE=prod

# For development
export SPRING_PROFILES_ACTIVE=dev
```

## Configuration Examples

### Simple Aurora Cluster (MySQL)

**application.yml:**
```yaml
spring:
  application:
    name: DevOps

  datasource:
    url: jdbc:mysql://myapp-aurora-cluster.cluster-abc123xyz.us-east-1.rds.amazonaws.com:3306/devops
    username: admin
    password: ${DB_PASSWORD}
    driver-class-name: com.mysql.cj.jdbc.Driver

    hikari:
      pool-name: AuroraHikariPool
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 20000
      idle-timeout: 300000
      max-lifetime: 1200000
      leak-detection-threshold: 60000
      connection-test-query: SELECT 1

  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    open-in-view: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true
        jdbc:
          batch_size: 20
        order_inserts: true
        order_updates: true

  flyway:
    enabled: true
    baseline-on-migrate: true
    locations: classpath:db/migration
    validate-on-migrate: true

logging:
  level:
    org.hibernate.SQL: WARN
    com.zaxxer.hikari: INFO
```

### Read/Write Split Configuration

For read-heavy workloads, use separate writer and reader datasources:

**application.properties:**
```properties
# Aurora MySQL - Writer Endpoint
spring.datasource.writer.jdbc-url=jdbc:mysql://myapp-aurora-cluster.cluster-abc123xyz.us-east-1.rds.amazonaws.com:3306/devops
spring.datasource.writer.username=admin
spring.datasource.writer.password=${DB_PASSWORD}
spring.datasource.writer.driver-class-name=com.mysql.cj.jdbc.Driver

# Aurora MySQL - Reader Endpoint (Read Replicas)
spring.datasource.reader.jdbc-url=jdbc:mysql://myapp-aurora-cluster.cluster-ro-abc123xyz.us-east-1.rds.amazonaws.com:3306/devops
spring.datasource.reader.username=admin
spring.datasource.reader.password=${DB_PASSWORD}
spring.datasource.reader.driver-class-name=com.mysql.cj.jdbc.Driver

# HikariCP for Writer
spring.datasource.writer.hikari.maximum-pool-size=15
spring.datasource.writer.hikari.minimum-idle=5

# HikariCP for Reader
spring.datasource.reader.hikari.maximum-pool-size=25
spring.datasource.reader.hikari.minimum-idle=10
```

### SSL Configuration

**Aurora MySQL with SSL:**
```properties
spring.datasource.url=jdbc:mysql://myapp-aurora-cluster.cluster-abc123xyz.us-east-1.rds.amazonaws.com:3306/devops?useSSL=true&requireSSL=true&verifyServerCertificate=true
```

**Aurora PostgreSQL with SSL:**
```properties
spring.datasource.url=jdbc:postgresql://myapp-aurora-pg-cluster.cluster-abc123xyz.us-east-1.rds.amazonaws.com:5432/devops?ssl=true&sslmode=require
```

## Environment-Specific Configuration

### Development Profile

**application-dev.properties:**
```properties
# Local MySQL for development
spring.datasource.url=jdbc:mysql://localhost:3306/devops_dev
spring.datasource.username=root
spring.datasource.password=root

# Enable DDL auto-update in development
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

# Smaller connection pool for local dev
spring.datasource.hikari.maximum-pool-size=5
spring.datasource.hikari.minimum-idle=2
```

### Production Profile

**application-prod.properties:**
```properties
# Aurora Cluster Endpoint (Production)
spring.datasource.url=jdbc:mysql://${AURORA_ENDPOINT}:3306/${DB_NAME}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}

# Validate schema only in production
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.open-in-view=false

# Production-optimized connection pool
spring.datasource.hikari.maximum-pool-size=30
spring.datasource.hikari.minimum-idle=10
spring.datasource.hikari.connection-timeout=20000
spring.datasource.hikari.idle-timeout=300000
spring.datasource.hikari.max-lifetime=1200000

# Enable Flyway migrations
spring.flyway.enabled=true
spring.flyway.validate-on-migrate=true
```

## Database Migration Setup

Create migration files for Flyway:

```
src/main/resources/db/migration/
├── V1__create_users_table.sql
├── V2__add_phone_column.sql
└── V3__create_orders_table.sql
```

**V1__create_users_table.sql:**
```sql
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Advanced Features

For advanced configuration, see the reference documents:

- [Multi-datasource, SSL, Secrets Manager integration](references/advanced-configuration.md)
- [Common issues and solutions](references/troubleshooting.md)

## Best Practices

### Connection Pool Optimization

- Use HikariCP with Aurora-optimized settings
- Set appropriate pool sizes based on Aurora instance capacity
- Configure connection timeouts for failover handling
- Enable leak detection

### Security Best Practices

- Never hardcode credentials in configuration files
- Use environment variables or AWS Secrets Manager
- Enable SSL/TLS connections
- Configure proper security group rules
- Use IAM Database Authentication when possible

### Performance Optimization

- Enable batch operations for bulk data operations
- Disable open-in-view pattern to prevent lazy loading issues
- Use appropriate indexing for Aurora queries
- Configure connection pooling for high availability

### Monitoring

- Enable Spring Boot Actuator for database metrics
- Monitor connection pool metrics
- Set up proper logging for debugging
- Configure health checks for database connectivity

## Testing

Create a health check endpoint to test database connectivity:

```java
@RestController
@RequestMapping("/api/health")
public class DatabaseHealthController {

    @Autowired
    private DataSource dataSource;

    @GetMapping("/db-connection")
    public ResponseEntity<Map<String, Object>> testDatabaseConnection() {
        Map<String, Object> response = new HashMap<>();

        try (Connection connection = dataSource.getConnection()) {
            response.put("status", "success");
            response.put("database", connection.getCatalog());
            response.put("url", connection.getMetaData().getURL());
            response.put("connected", true);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            response.put("status", "failed");
            response.put("error", e.getMessage());
            response.put("connected", false);
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
        }
    }
}
```

**Test with cURL:**
```bash
curl http://localhost:8080/api/health/db-connection
```

## Support

For detailed troubleshooting and advanced configuration, refer to:

- [AWS RDS Aurora Advanced Configuration](references/advanced-configuration.md)
- [AWS RDS Aurora Troubleshooting Guide](references/troubleshooting.md)
- [AWS RDS Aurora documentation](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/java_aurora_code_examples.html)
- [Spring Boot Data RDS Aurora documentation](https://www.baeldung.com/aws-aurora-rds-java)