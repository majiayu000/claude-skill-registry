---
name: spring-boot-skill
description: >
  Build Spring Boot 4.x applications following the best practices. 
  Use this skill:
    * When developing Spring Boot applications using Spring MVC, Spring Data JPA, Spring Modulith, Spring Security
    * To create recommended Spring Boot package structure
    * To implement REST APIs, entities/repositories, service layer, modular monoliths
    * To use Thymeleaf view templates for building web applications
    * To write tests for REST APIs and Web applications
    * To write ArchUnit tests for testing architecture
    * To configure the recommended plugins and configurations to improve code quality, and testing while using Maven.
    * To use Spring Boot's Docker Compose support for local development
    * To create Taskfile for easier execution of common tasks while working with a Spring Boot application
---

# Spring Boot Skill

Apply the practices below when developing Spring Boot applications. Read the linked reference only when working on that area.

## Maven pom.xml Configuration

Read [references/spring-boot-maven-config.md](references/spring-boot-maven-config.md) for Maven `pom.xml` configuration with supporting plugins and configurations to improve code quality, and testing.

## Package structure

Read [references/code-organization.md](references/code-organization.md) for domain-driven, module-based package layout and naming conventions.

## Spring Data JPA

Implement the repository and entity layer using [references/spring-data-jpa.md](references/spring-data-jpa.md).

## Service layer

Implement business logic in the service layer using [references/spring-service-layer.md](references/spring-service-layer.md).

## Spring MVC REST APIs

Implement REST APIs with Spring MVC using [references/spring-webmvc-rest-api.md](references/spring-webmvc-rest-api.md).

## Spring Modulith

Build a modular monolith with Spring Modulith using [references/spring-modulith.md](references/spring-modulith.md).

## Thymeleaf

If Thymeleaf is used for view templates, refer [references/thymeleaf.md](references/thymeleaf.md)

## REST API Testing

If building a REST API using Spring WebMVC, test Spring Boot REST APIs using [references/spring-boot-rest-api-testing.md](references/spring-boot-rest-api-testing.md).

### Web App Controller Testing
If building a web application using view rendering controllers, test the controller layer using [references/spring-boot-webapp-testing-with-mockmvctester.md](references/spring-boot-webapp-testing-with-mockmvctester.md).

### Write ArchUnit Tests
To write tests for testing the architecture using ArchUnit, refer [references/archunit.md](references/archunit.md)

### Spring Boot Docker Compose Support
To use Docker Compose support for local development, refer [references/spring-boot-docker-compose.md](references/spring-boot-docker-compose.md).

## Taskfile

Use [references/taskfile.md](references/taskfile.md) for easier commands execution.
