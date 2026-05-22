---
name: spring-boot-project-creator
description: Creates and scaffolds a new Spring Boot project (3.x or 4.x) by downloading from Spring Initializr, generating package structure (DDD or Layered architecture), configuring JPA, SpringDoc OpenAPI, and Docker Compose services (PostgreSQL, Redis, MongoDB). Use when creating a new Java Spring Boot project from scratch, bootstrapping a microservice, or initializing a backend application.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Spring Boot Project Creator

## Overview

Generates a fully configured Spring Boot project from scratch using the Spring Initializr API. The skill walks the user through selecting project parameters, choosing an architecture style (DDD or Layered), configuring data stores, and setting up Docker Compose for local development. The result is a build-ready project with standardized structure, dependency management, and configuration.

## When to Use

- Bootstrap a new Spring Boot 3.x or 4.x project with a standard structure.
- Initialize a backend microservice with JPA, SpringDoc OpenAPI, and Docker Compose.
- Scaffold a project following either DDD (Domain-Driven Design) or Layered (Controller/Service/Repository/Model) architecture.
- Set up local development infrastructure with PostgreSQL, Redis, and/or MongoDB via Docker Compose.
- Trigger phrases: **"create spring boot project"**, **"new spring boot app"**, **"bootstrap java project"**, **"scaffold spring boot microservice"**, **"initialize spring boot backend"**, **"generate spring boot project"**.

## Prerequisites

Before starting, ensure the following tools are installed:

- **Java Development Kit (JDK)**: Version 17+ (Java 21 recommended for Spring Boot 3.x/4.x)
- **Apache Maven**: Build tool (Spring Initializr generates Maven projects by default)
- **Docker** and **Docker Compose**: For running local infrastructure services
- **curl** and **unzip**: For downloading and extracting the project from Spring Initializr

## Instructions

Follow these steps to create a new Spring Boot project.

### 1. Gather Project Configuration

Ask the user for the following project parameters using **AskUserQuestion**. Provide sensible defaults:

| Parameter | Default | Options |
|-----------|---------|---------|
| **Group ID** | `com.example` | Any valid Java package name |
| **Artifact ID** | `demo` | Kebab-case identifier |
| **Package Name** | Same as Group ID | Valid Java package |
| **Spring Boot Version** | `3.4.5` | `3.4.x`, `4.0.x` (check start.spring.io for latest) |
| **Java Version** | `21` | `17`, `21` |
| **Architecture** | User choice | `DDD` or `Layered` |
| **Docker Services** | User choice | PostgreSQL, Redis, MongoDB (multi-select) |
| **Build Tool** | `maven` | `maven`, `gradle` |

### 2. Generate Project with Spring Initializr

Use `curl` to download the project scaffold from start.spring.io.

**Base dependencies** (always included):
- `web` — Spring Web MVC
- `validation` — Jakarta Bean Validation
- `data-jpa` — Spring Data JPA
- `testcontainers` — Testcontainers support

**Conditional dependencies** (based on Docker Services selection):
- PostgreSQL selected → add `postgresql`
- Redis selected → add `data-redis`
- MongoDB selected → add `data-mongodb`

```bash
# Example for Spring Boot 3.4.5 with PostgreSQL only
curl -s https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=3.4.5 \
  -d groupId=com.example \
  -d artifactId=demo \
  -d packageName=com.example \
  -d javaVersion=21 \
  -d packaging=jar \
  -d dependencies=web,data-jpa,postgresql,validation,testcontainers \
  -o starter.zip

unzip -o starter.zip -d ./demo
rm starter.zip
cd demo
```

### 3. Add Additional Dependencies

Edit `pom.xml` to add SpringDoc OpenAPI and ArchUnit for architectural testing.

```xml
<!-- SpringDoc OpenAPI -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.15</version>
</dependency>

<!-- ArchUnit for architecture tests -->
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.4.1</version>
    <scope>test</scope>
</dependency>
```

### 4. Create Architecture Structure

Based on the user's choice, create the package structure under `src/main/java/<packagePath>/`.

#### Option A: Layered Architecture

```
src/main/java/com/example/
├── controller/        # REST controllers (@RestController)
├── service/           # Business logic (@Service)
├── repository/        # Data access (@Repository, Spring Data interfaces)
├── model/             # JPA entities (@Entity)
│   └── dto/           # Request/Response DTOs (Java records)
├── config/            # Configuration classes (@Configuration)
└── exception/         # Custom exceptions and @ControllerAdvice
```

Create placeholder classes for each layer:

- **config/OpenApiConfig.java** — SpringDoc OpenAPI configuration bean
- **exception/GlobalExceptionHandler.java** — `@RestControllerAdvice` with standard error handling
- **model/dto/ErrorResponse.java** — Standard error response record

#### Option B: DDD (Domain-Driven Design) Architecture

```
src/main/java/com/example/
├── domain/                 # Core domain (framework-free)
│   ├── model/              # Entities, Value Objects, Aggregates
│   ├── repository/         # Repository interfaces (ports)
│   └── exception/          # Domain exceptions
├── application/            # Use cases / Application services
│   ├── service/            # @Service orchestration
│   └── dto/                # Input/Output DTOs (records)
├── infrastructure/         # External adapters
│   ├── persistence/        # JPA entities, Spring Data repos
│   └── config/             # Spring @Configuration
└── presentation/           # REST API layer
    ├── controller/         # @RestController
    └── exception/          # @RestControllerAdvice
```

Create placeholder classes for each layer:

- **infrastructure/config/OpenApiConfig.java** — SpringDoc OpenAPI configuration bean
- **presentation/exception/GlobalExceptionHandler.java** — `@RestControllerAdvice` with standard error handling
- **application/dto/ErrorResponse.java** — Standard error response record

### 5. Configure Application Properties

Create `src/main/resources/application.properties` with the selected services.

**Always include:**

```properties
# Application
spring.application.name=${artifactId}

# SpringDoc OpenAPI
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
```

**If PostgreSQL is selected:**

```properties
# PostgreSQL / JPA
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/${POSTGRES_DB:postgres}
spring.datasource.username=${POSTGRES_USER:postgres}
spring.datasource.password=${POSTGRES_PASSWORD:changeme}
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

**If Redis is selected:**

```properties
# Redis
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.password=${REDIS_PASSWORD:changeme}
```

**If MongoDB is selected:**

```properties
# MongoDB
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=${MONGO_USER:root}
spring.data.mongodb.password=${MONGO_PASSWORD:changeme}
spring.data.mongodb.database=${MONGO_DB:test}
```

### 6. Set Up Docker Compose

Create `docker-compose.yaml` at the project root with only the services the user selected.

```yaml
services:
  # Include if PostgreSQL selected
  postgresql:
    image: postgres:17
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
      POSTGRES_DB: ${POSTGRES_DB:-postgres}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data

  # Include if Redis selected
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    command: redis-server --requirepass ${REDIS_PASSWORD:-changeme}
    volumes:
      - ./redis_data:/data

  # Include if MongoDB selected
  mongodb:
    image: mongo:8
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-root}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-changeme}
    volumes:
      - ./mongo_data:/data/db
```

### 7. Create `.env` File for Docker Compose

Create a `.env` file at the project root with default credentials for local development:

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeme
POSTGRES_DB=postgres

# Redis
REDIS_PASSWORD=changeme

# MongoDB
MONGO_USER=root
MONGO_PASSWORD=changeme
MONGO_DB=test
```

Include only the variables for the services the user selected. Docker Compose automatically loads this file.

### 8. Update .gitignore

Append Docker Compose volume directories and the `.env` file to `.gitignore`:

```
# Docker Compose
.env
postgres_data/
redis_data/
mongo_data/
```

### 9. Verify the Build

Run the Maven build to confirm the project compiles and tests pass:

```bash
./mvnw clean verify
```

If the build succeeds, inform the user. If it fails, diagnose and fix the issue before proceeding.

### 10. Present Summary to User

Display a summary of the created project:

```
Project Created Successfully

  Artifact:      <artifactId>
  Spring Boot:   <version>
  Java:          <javaVersion>
  Architecture:  <DDD | Layered>
  Build Tool:    Maven
  Docker:        <services list>

  Directory:     ./<artifactId>/

  Next Steps:
    1. cd <artifactId>
    2. docker compose up -d
    3. ./mvnw spring-boot:run
    4. Open http://localhost:8080/swagger-ui.html
```

## Architecture Patterns

### Layered Architecture

Traditional three-tier architecture with clear separation of concerns:

| Layer | Package | Responsibility |
|-------|---------|---------------|
| **Presentation** | `controller/` | HTTP endpoints, request/response mapping |
| **Business** | `service/` | Business logic, transaction management |
| **Data Access** | `repository/` | Database operations via Spring Data |
| **Domain** | `model/` | JPA entities and DTOs |

**Best for:** Simple CRUD applications, small-to-medium services, teams new to Spring Boot.

### DDD Architecture

Domain-Driven Design with hexagonal boundaries:

| Layer | Package | Responsibility |
|-------|---------|---------------|
| **Domain** | `domain/` | Entities, value objects, domain services (framework-free) |
| **Application** | `application/` | Use cases, orchestration, DTO mapping |
| **Infrastructure** | `infrastructure/` | JPA adapters, external integrations, configuration |
| **Presentation** | `presentation/` | REST controllers, error handling |

**Best for:** Complex business domains, microservices with rich logic, long-lived projects.

## Examples

### Example 1: Simple REST API with PostgreSQL (Layered)

**User request:** "Create a Spring Boot project for a REST API with PostgreSQL"

```bash
curl -s https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d bootVersion=3.4.5 \
  -d groupId=com.example \
  -d artifactId=my-api \
  -d packageName=com.example.myapi \
  -d javaVersion=21 \
  -d dependencies=web,data-jpa,postgresql,validation,testcontainers \
  -o starter.zip
```

Result: Layered project with `controller/`, `service/`, `repository/`, `model/` packages, PostgreSQL Docker Compose, and SpringDoc OpenAPI.

### Example 2: Microservice with DDD and Multiple Stores

**User request:** "Bootstrap a Spring Boot 3 microservice with DDD, PostgreSQL and Redis"

```bash
curl -s https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d bootVersion=3.4.5 \
  -d groupId=com.acme \
  -d artifactId=order-service \
  -d packageName=com.acme.order \
  -d javaVersion=21 \
  -d dependencies=web,data-jpa,postgresql,data-redis,validation,testcontainers \
  -o starter.zip
```

Result: DDD project with `domain/`, `application/`, `infrastructure/`, `presentation/` packages, PostgreSQL + Redis Docker Compose, and SpringDoc OpenAPI.

## Best Practices

- **Always use Spring Initializr** for project generation to get the correct dependency management and parent POM.
- **Use Java records** for DTOs — they are immutable and concise.
- **Keep domain layer framework-free** in DDD architecture — no Spring annotations in `domain/`.
- **Use environment variables** for sensitive configuration in production (database passwords, etc.).
- **Pin Docker image versions** in `docker-compose.yaml` to avoid unexpected breaking changes.
- **Run `./mvnw clean verify`** after setup to ensure everything compiles and tests pass.
- **Add Testcontainers** for integration tests instead of relying on Docker Compose.

## Constraints and Warnings

- Spring Initializr requires internet access — this skill cannot work offline.
- Spring Boot 4.x availability depends on the current release cycle — check start.spring.io for latest versions.
- Docker Compose credentials are loaded from `.env` file (git-ignored) — never commit secrets to version control.
- The `spring.jpa.hibernate.ddl-auto=update` setting is for development only — use Flyway or Liquibase in production.
- ArchUnit version must be compatible with the JUnit 5 version bundled with Spring Boot.
