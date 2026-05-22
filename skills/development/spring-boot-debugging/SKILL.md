---
name: spring-boot-debugging
description: Debug Spring Boot applications — diagnose startup failures, bean wiring issues, configuration problems, and runtime errors.
---

# Spring Boot Debugging

## Overview
You are a Spring Boot debugging expert. Use these procedures to diagnose and fix common Spring Boot application issues.

## When to Use
Use this skill when the user reports issues with Spring Boot application startup, bean wiring, configuration, or runtime behavior.

## Diagnostic Procedures

### Application Won't Start
1. Check the full stack trace — the root cause is usually near the bottom
2. Look for `BeanCreationException` — indicates a wiring problem
3. Look for `BindException` — port already in use
4. Check `application.yml` / `application.properties` syntax

### Common Startup Failures
- **Port in use**: `lsof -i :8080` then kill the process or change `server.port`
- **Missing bean**: Check `@Component`, `@Service`, `@Repository` annotations and component scan paths
- **Circular dependency**: Refactor to use `@Lazy` or restructure the dependency graph
- **Database connection failed**: Verify JDBC URL, credentials, and that the DB is running

### Configuration Issues
1. Check active profiles: Look for `The following profiles are active:` in startup logs
2. Verify property sources: Enable `logging.level.org.springframework.boot.context.config=DEBUG`
3. Check property precedence: env vars > command line > application-{profile}.yml > application.yml

### Runtime Debugging
- Enable debug logging: `logging.level.com.yourpackage=DEBUG`
- Check actuator health: `curl http://localhost:8080/actuator/health`
- View loaded beans: `curl http://localhost:8080/actuator/beans`
- Check environment: `curl http://localhost:8080/actuator/env`

## Best Practices
- Read the full stack trace before searching for solutions
- Check the active Spring profile first — many issues come from wrong profile
- Use actuator endpoints to inspect runtime state
