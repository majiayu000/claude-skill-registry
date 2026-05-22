---
name: spring-boot-deployment
description: Guide for deploying Spring Boot applications including Docker, health checks, and production configurations. Use this when preparing applications for deployment or setting up CI/CD.
---

# Spring Boot Deployment Best Practices

Follow these practices for production-ready deployments.

## Dockerfile Best Practices

```dockerfile
# Multi-stage build for smaller image
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY gradle gradle
COPY gradlew build.gradle settings.gradle ./
COPY src src

# Build the application
RUN ./gradlew bootJar --no-daemon

# Runtime stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copy the built jar
COPY --from=builder /app/build/libs/*.jar app.jar

# JVM tuning for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8082/actuator/health || exit 1

EXPOSE 8082

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

## Docker Compose Configuration

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8082:8082"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DATABASE_URL=jdbc:postgresql://db:5432/salonhub
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=${DB_PASSWORD}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8082/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=salonhub
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  postgres_data:
```

## Health Checks and Probes

```yaml
# application-prod.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
    db:
      enabled: true
```

```java
// Custom health indicator
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    private final DataSource dataSource;

    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement ps = conn.prepareStatement("SELECT 1");
            ps.executeQuery();
            return Health.up()
                .withDetail("database", conn.getMetaData().getDatabaseProductName())
                .withDetail("version", conn.getMetaData().getDatabaseProductVersion())
                .build();
        } catch (SQLException e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

## Production Configuration

```yaml
# application-prod.yml
spring:
  datasource:
    url: ${DATABASE_URL}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 20000
      idle-timeout: 300000
      max-lifetime: 1200000

  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    open-in-view: false

server:
  port: 8082
  shutdown: graceful
  tomcat:
    connection-timeout: 20000
    max-connections: 10000
    accept-count: 100
    threads:
      max: 200
      min-spare: 10

logging:
  level:
    root: WARN
    com.salonhub.api: INFO
  pattern:
    console: '{"time":"%d","level":"%p","logger":"%logger","message":"%m"}%n'
```

## Graceful Shutdown

```yaml
server:
  shutdown: graceful

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

```java
// Handle cleanup on shutdown
@Component
public class GracefulShutdown {

    private static final Logger logger = LoggerFactory.getLogger(GracefulShutdown.class);

    @PreDestroy
    public void onShutdown() {
        logger.info("Application shutting down...");
        // Cleanup resources, finish pending operations
    }
}
```

## Environment Variables

```bash
# Required production environment variables
DATABASE_URL=jdbc:postgresql://localhost:5432/salonhub
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=<secure-password>
JWT_SECRET=<secure-random-string-min-256-bits>
SPRING_PROFILES_ACTIVE=prod
```

## Render.yaml (Cloud Deployment)

```yaml
services:
  - type: web
    name: salon-hub-api
    env: docker
    dockerfilePath: ./Dockerfile
    plan: starter
    healthCheckPath: /actuator/health
    envVars:
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: DATABASE_URL
        fromDatabase:
          name: salon-hub-db
          property: connectionString
      - key: JWT_SECRET
        generateValue: true

databases:
  - name: salon-hub-db
    databaseName: salonhub
    user: postgres
    plan: starter
```

## CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up JDK 21
        uses: actions/setup-java@v3
        with:
          java-version: '21'
          distribution: 'temurin'
      
      - name: Run tests
        run: ./gradlew check
      
      - name: Build JAR
        run: ./gradlew bootJar

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            https://api.render.com/deploy/srv-xxx
```

## Logging for Production

```yaml
logging:
  level:
    root: WARN
    com.salonhub.api: INFO
  
  # JSON format for log aggregation
  pattern:
    console: '{"timestamp":"%d{ISO8601}","level":"%p","thread":"%t","logger":"%logger{36}","message":"%m","exception":"%ex"}%n'
```

## Security Hardening

```yaml
# Disable sensitive actuator endpoints in production
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    env:
      enabled: false
    beans:
      enabled: false
    configprops:
      enabled: false
```

## Deployment Checklist

### Before Deployment
- [ ] All tests passing: `./gradlew check`
- [ ] Security scan passed
- [ ] Configuration validated for target environment
- [ ] Database migrations tested
- [ ] Environment variables documented

### Deployment
- [ ] Build Docker image
- [ ] Push to container registry
- [ ] Deploy with health checks enabled
- [ ] Verify health endpoints responding

### After Deployment
- [ ] Monitor application logs
- [ ] Check health endpoints
- [ ] Verify database connectivity
- [ ] Test critical endpoints
- [ ] Monitor metrics and alerts
