---
name: spring-boot-configuration
description: Guide for managing Spring Boot configuration including profiles, externalized configuration, and environment-specific settings. Use this when setting up configuration for different environments.
---

# Spring Boot Configuration Management

Follow these practices for managing application configuration.

## Configuration File Structure

```
src/main/resources/
├── application.yml           # Default/shared configuration
├── application-dev.yml       # Development overrides
├── application-test.yml      # Test environment
├── application-h2.yml        # H2 database for local dev
├── application-prod.yml      # Production settings
└── db/migration/             # Flyway migrations
```

## Profile-Based Configuration

### Default Configuration (application.yml)

```yaml
spring:
  application:
    name: salon-hub-api
  
  jpa:
    open-in-view: false
    show-sql: false
    properties:
      hibernate:
        format_sql: true

server:
  port: 8082
  shutdown: graceful

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when-authorized

# Application-specific settings
app:
  jwt:
    secret: ${JWT_SECRET:default-dev-secret-key-change-in-production}
    expiration: 86400000
```

### Development Profile (application-dev.yml)

```yaml
spring:
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: validate

logging:
  level:
    root: INFO
    com.salonhub.api: DEBUG
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG
```

### Test Profile (application-test.yml)

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true

  flyway:
    enabled: false
```

### Production Profile (application-prod.yml)

```yaml
spring:
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5

  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false

logging:
  level:
    root: WARN
    com.salonhub.api: INFO
```

## Typed Configuration Properties

```java
@Configuration
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {

    @NestedConfigurationProperty
    private final Jwt jwt = new Jwt();
    
    @NestedConfigurationProperty
    private final Queue queue = new Queue();

    public static class Jwt {
        @NotBlank
        private String secret;
        
        @Min(60000)
        private long expiration = 86400000;
        
        // Getters and setters
    }

    public static class Queue {
        @Min(1)
        @Max(100)
        private int maxSize = 50;
        
        @Min(1)
        private int estimatedWaitMinutes = 15;
        
        // Getters and setters
    }
    
    // Getters
}

// Usage
@Service
public class JwtService {
    private final AppProperties appProperties;
    
    public JwtService(AppProperties appProperties) {
        this.appProperties = appProperties;
    }
    
    public String generateToken() {
        return Jwts.builder()
            .setExpiration(new Date(System.currentTimeMillis() + 
                appProperties.getJwt().getExpiration()))
            .signWith(Keys.hmacShaKeyFor(
                appProperties.getJwt().getSecret().getBytes()))
            .compact();
    }
}
```

## Environment Variables

**Never hardcode sensitive values:**

```yaml
# application.yml - Use environment variables with defaults
spring:
  datasource:
    url: ${DATABASE_URL:jdbc:h2:mem:devdb}
    username: ${DATABASE_USERNAME:sa}
    password: ${DATABASE_PASSWORD:}

app:
  jwt:
    secret: ${JWT_SECRET}  # Required, no default for production
```

```powershell
# Set environment variables (PowerShell)
$env:DATABASE_URL = "jdbc:postgresql://localhost:5432/salonhub"
$env:JWT_SECRET = "your-secure-secret-key"

# Or in .env file (for Docker)
DATABASE_URL=jdbc:postgresql://db:5432/salonhub
JWT_SECRET=your-secure-secret-key
```

## Profile Activation

```powershell
# Command line
java -jar app.jar --spring.profiles.active=prod

# Gradle
.\gradlew.bat bootRun --args='--spring.profiles.active=dev'

# Environment variable
$env:SPRING_PROFILES_ACTIVE = "prod"

# Docker Compose
environment:
  - SPRING_PROFILES_ACTIVE=prod
```

## Logging Configuration

```yaml
logging:
  level:
    root: INFO
    com.salonhub.api: DEBUG
    org.springframework.web: WARN
    org.springframework.security: DEBUG
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE  # Log SQL parameters
  
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"
  
  file:
    name: logs/salon-hub.log
    max-size: 10MB
    max-history: 10
```

## Actuator Configuration

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
      base-path: /actuator
  
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  
  health:
    db:
      enabled: true
    diskspace:
      enabled: true
  
  info:
    env:
      enabled: true
```

## Graceful Shutdown

```yaml
server:
  shutdown: graceful

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

## CORS Configuration

```yaml
# For simple cases
app:
  cors:
    allowed-origins: 
      - http://localhost:3000
      - https://salon-hub-ui.vercel.app
    allowed-methods:
      - GET
      - POST
      - PUT
      - DELETE
```

```java
@Configuration
public class CorsConfig {
    
    @Value("${app.cors.allowed-origins}")
    private List<String> allowedOrigins;

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(allowedOrigins);
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", configuration);
        return source;
    }
}
```

## Configuration Validation

```java
@Configuration
@Validated
@ConfigurationProperties(prefix = "app.service")
public class ServiceConfig {

    @NotNull(message = "API URL is required")
    @URL(message = "Invalid API URL format")
    private String apiUrl;

    @Min(value = 1, message = "Timeout must be at least 1 second")
    @Max(value = 60, message = "Timeout cannot exceed 60 seconds")
    private int timeout = 30;

    @Min(value = 1, message = "Max retries must be at least 1")
    private int maxRetries = 3;
    
    // Getters and setters
}
```

## Configuration Checklist

- [ ] Use profiles for environment-specific settings
- [ ] Never hardcode secrets - use environment variables
- [ ] Create typed configuration classes with validation
- [ ] Set appropriate logging levels per environment
- [ ] Configure actuator endpoints securely
- [ ] Implement graceful shutdown
- [ ] Configure CORS for frontend integration
- [ ] Document all configuration properties
