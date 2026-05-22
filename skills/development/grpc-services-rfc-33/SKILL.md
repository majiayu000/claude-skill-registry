---
name: grpc-services-rfc-33
description: >
  RFC-33 compliant gRPC service standards for Java services. Covers protobuf contracts,
  service implementation, resilience patterns (retry, bulkhead, circuit breaker), and linting.
  Use when creating or maintaining gRPC services and clients.
compatibility: Java projects using gRPC with Spring Boot
metadata:
  version: "1.0.0"
  technology: java
  category: infrastructure
  tags:
    - java
    - grpc
    - rfc-33
    - protobuf
    - resilience
---

# gRPC Services (RFC-33)

RFC-33 compliant gRPC service standards for Java services.

## When to use this skill

- Creating new gRPC services or clients
- Implementing protobuf contracts
- Adding resilience patterns (retry, bulkhead, circuit breaker)
- Configuring deadline propagation
- Setting up protobuf linting with Buf
- Implementing gRPC error handling

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L24-L32)
- [Quick Start](#quick-start) (L54-L97)
- [Service Implementation](#service-implementation) (L98-L120)
- [Client Configuration](#client-configuration) (L121-L146)
- [References](#references) (L147-L154)
- [Related Rules](#related-rules) (L155-L159)
- [Related Skills](#related-skills) (L160-L165)

### Available Resources

**📚 references/** - Detailed documentation
- [contracts](references/contracts.md)
- [linting](references/linting.md)
- [resilience](references/resilience.md)

---

## Quick Start

### 1. Add Dependencies

```toml
# gradle/libs.versions.toml
[versions]
grpc = "1.78.0"
protobuf = "4.33.0"

[libraries]
grpc-protobuf = { module = "io.grpc:grpc-protobuf", version.ref = "grpc" }
grpc-stub = { module = "io.grpc:grpc-stub", version.ref = "grpc" }
grpc-api = { module = "io.grpc:grpc-api", version.ref = "grpc" }
protobuf-java = { module = "com.google.protobuf:protobuf-java", version.ref = "protobuf" }
grpc-resilience-starter = { module = "com.bitso.commons:grpc-resilience-starter", version = "LATEST" }

[plugins]
protobuf = { id = "com.google.protobuf", version = "0.9.6" }
```

### 2. Configure gRPC Server

```yaml
# application.yml
grpc:
  server:
    port: 8201
```

### 3. Implement Service Handler

```java
@GrpcService
public class MyServiceHandler extends MyServiceGrpc.MyServiceImplBase {
    @Override
    public void myMethod(MyRequest request, StreamObserver<MyResponse> responseObserver) {
        // Implementation
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}
```

## Service Implementation

### Error Handling

Use `FailureHelper` to send errors in metadata:

```java
public static StatusRuntimeException createStatusRuntimeException(
        Status.Code code, DataCommonsProto.Failure failure) {
    Metadata metadata = new Metadata();
    metadata.put(FAILURE_DETAILS_KEY, failure);
    return code.toStatus().withDescription(failure.getCode()).asRuntimeException(metadata);
}
```

### gRPC Error Codes

| Code | Usage |
|------|-------|
| `INTERNAL` | Infrastructure errors |
| `UNKNOWN` | Only used by gRPC core |
| `FAILED_PRECONDITION` | Business errors |

## Client Configuration

### With Resilience

```yaml
grpc:
  client:
    my-service:
      address: dns:/${MY_SERVICE_HOST:localhost}:${GRPC_PORT:8201}
      negotiation-type: PLAINTEXT
      service-config:
        method-config:
          - name: []
            timeout: PT5S
            retry-policy:
              max-attempts: 3
              initial-backoff: PT1S
              max-backoff: PT5S
              backoff-multiplier: 1.5
              retryable-status-codes:
                - UNAVAILABLE
      bulkhead:
        max-concurrent-calls: 10
        max-wait-duration: PT1S
```

## References

| Reference | Description |
|-----------|-------------|
| [references/contracts.md](references/contracts.md) | Protobuf contract guidelines, versioning, documentation |
| [references/resilience.md](references/resilience.md) | Deadline propagation, retry, bulkhead, circuit breaker |
| [references/linting.md](references/linting.md) | Buf linting setup and custom rules |

## Related Rules

- [java-grpc-services](.cursor/rules/java-grpc-services/java-grpc-services.mdc) - gRPC service standards
- [java-grpc-resilience](.cursor/rules/java-grpc-resilience/java-grpc-resilience.mdc) - Resilience configuration

## Related Skills

| Skill | Purpose |
|-------|---------|
| [gradle-standards](.claude/skills/gradle-standards/SKILL.md) | Dependency configuration |
| [java-testing](.claude/skills/java-testing/SKILL.md) | Testing gRPC services |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/grpc-services-rfc-33/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

