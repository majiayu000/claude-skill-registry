---
name: rest-api
description: >
  REST API standards for Java Spring services. Covers Bitso API guidelines, authentication
  integration, OpenAPI documentation, and RFC-37 service documentation.
  Use when creating or maintaining REST endpoints.
compatibility: Java projects using Spring Boot with REST APIs
metadata:
  version: "1.0.0"
  technology: java
  category: infrastructure
  tags:
    - java
    - rest-api
    - rfc-37
    - openapi
    - authentication
---

# REST API

REST API standards for Java Spring services.

## When to use this skill

- Creating REST endpoints in Spring services
- Integrating Bitso authentication
- Documenting APIs with OpenAPI
- Setting up service documentation (RFC-37)
- Testing authenticated endpoints

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L31)
- [Quick Start](#quick-start) (L52-L91)
- [Authentication](#authentication) (L92-L123)
- [Documentation](#documentation) (L124-L144)
- [References](#references) (L145-L151)
- [Related Rules](#related-rules) (L152-L156)
- [Related Skills](#related-skills) (L157-L162)

### Available Resources

**📚 references/** - Detailed documentation
- [documentation](references/documentation.md)
- [guidelines](references/guidelines.md)

---

## Quick Start

### 1. Add Authentication Dependency

```groovy
implementation libs.bitso.api.base.spring.webapi
```

### 2. Configure gRPC Client

```yaml
grpc:
  client:
    user-security:
      address: dns:/${USER_SECURITY_HOST:localhost}:${GRPC_PORT:8201}
      negotiation-type: PLAINTEXT
```

### 3. Create Controller

```java
@RestController
@RequestMapping("/")
public class MyController {

    @Autowired
    SpringHttpResponseFactory responseFactory;

    @Autowired
    WebAuthenticationContext authenticationContext;

    @GetMapping("/private")
    @WebAPI(WebAPIType.PRIVATE)
    public ResponseEntity<?> privateEndpoint() {
        Long userId = authenticationContext.getPrincipalId();
        return responseFactory.ok(userId);
    }
}
```

## Authentication

### Configuration Bean

```java
@Configuration
public class UserSecurityContextConfiguration {
    @Bean
    @Primary
    public AuthenticationService authenticationService(
        @GrpcClient("user-security") AuthorizationServiceV1BlockingStub stub,
        @Qualifier("userSecurityResilienceConfig") ResilienceConfiguration config
    ) {
        return new ProtoShimAuthenticationService(config, stub);
    }
}
```

### Component Scan

Ensure your main application scans Bitso components:

```java
@SpringBootApplication
@ComponentScan("com.bitso.*")
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

## Documentation

### OpenAPI Specification

All endpoints should be documented under `./docs/api/rest/openapi.yaml`

### RFC-37 Documentation Structure

```text
docs/
├── api/
│   ├── async/
│   ├── grpc/
│   └── rest/
├── decisions/
├── <domain-name>/
├── runbooks/
└── how-tos/
    └── local-execution.md
```

## References

| Reference | Description |
|-----------|-------------|
| [references/guidelines.md](references/guidelines.md) | API guidelines, authentication, testing |
| [references/documentation.md](references/documentation.md) | RFC-37 documentation standards |

## Related Rules

- [java-rest-api-guidelines](.cursor/rules/java-rest-api-guidelines/java-rest-api-guidelines.mdc) - Full API guidelines
- [java-service-documentation](.cursor/rules/java-service-documentation/java-service-documentation.mdc) - RFC-37 documentation

## Related Skills

| Skill | Purpose |
|-------|---------|
| [grpc-services-rfc-33](.claude/skills/grpc-services-rfc-33/SKILL.md) | gRPC service standards |
| [java-testing](.claude/skills/java-testing/SKILL.md) | Testing REST endpoints |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/rest-api/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

