---
name: spring-boot
description: Spring Boot CLI for project initialization and Actuator endpoints for monitoring and management.
---

# Spring Boot

## Project Initialization

**Setup with SDKMAN**

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 17.0.10-zulu
sdk install springboot
```

**Create New Project**

```bash
spring init my-app --build=maven --java-version=17 --group-id org.jyasu \
--boot-version=3.2.2 --packaging jar --extract --force \
--dependencies=web,lombok,docker-compose
```

**Common Dependencies**

```
web                    # Web (Spring MVC + Embedded Tomcat)
lombok                # Boilerplate reduction
docker-compose        # Docker Compose support
spring-ai-openai      # OpenAI integration
spring-ai-vectordb-elasticsearch  # Elasticsearch vector store
spring-ai-vectordb-redis          # Redis vector store
spring-ai-vectordb-mongodb-atlas  # MongoDB vector store
postgresql            # PostgreSQL JDBC driver
data-jpa              # Spring Data JPA
actuator              # Production monitoring
distributed-tracing   # Tracing support
data-cassandra        # Cassandra support
data-mongodb          # MongoDB support
graphql               # GraphQL support
data-elasticsearch    # Elasticsearch support
data-redis            # Redis support
kafka                 # Kafka messaging
amqp                  # RabbitMQ support
cloud-starter-vault-config  # Vault configuration
native                # Native image support
spring-shell          # Spring Shell
```

---

## Spring Boot Actuator Endpoints

🔗 [Official Documentation](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html)

| Endpoint | Description |
|----------|-------------|
| `/actuator/health` | Application health status (UP/DOWN) with optional details |
| `/actuator/info` | Arbitrary application info from `application.properties` |
| `/actuator/metrics` | JVM memory, CPU, HTTP requests, and custom metrics |
| `/actuator/env` | Complete environment properties and configuration |
| `/actuator/beans` | All Spring beans in the application context |
| `/actuator/mappings` | All `@RequestMapping` paths and handlers |
| `/actuator/threaddump` | Thread dump with stack traces |
| `/actuator/loggers` | Runtime log level viewing and modification |
| `/actuator/httptrace` | HTTP request/response trace (last 100 by default) |
| `/actuator/auditevents` | Audit events for security and changes |
| `/actuator/scheduledtasks` | Scheduled task information |
| `/actuator/heapdump` | JVM heap dump download (if enabled) |
| `/actuator/shutdown` | Graceful application shutdown (must be explicitly enabled) |

**Enable/Configure Endpoints**

```properties
# application.properties
management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=always
management.endpoint.shutdown.enabled=true
```

**Health Indicators**

```bash
# Check health
curl http://localhost:8080/actuator/health

# Health with details
curl http://localhost:8080/actuator/health/details

# View all endpoints
curl http://localhost:8080/actuator
```