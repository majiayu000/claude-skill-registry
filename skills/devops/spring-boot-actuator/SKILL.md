---
name: spring-boot-actuator
description: Configure Spring Boot Actuator for production-grade monitoring, health probes, secured management endpoints, and Micrometer metrics across JVM services.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, actuator, monitoring, health-checks, metrics, production]
version: 1.1.0
context7_library: /websites/spring_io_spring-boot_3_5
context7_trust_score: 7.5
---

# Spring Boot Actuator Skill

## Overview
- Deliver production-ready observability for Spring Boot services using Actuator endpoints, probes, and Micrometer integration.
- Standardize health, metrics, and diagnostics configuration while delegating deep reference material to `references/`.
- Support platform requirements for secure operations, SLO reporting, and incident diagnostics.

## When to Use
- Trigger: "enable actuator endpoints" – Bootstrap Actuator for a new or existing Spring Boot service.
- Trigger: "secure management port" – Apply Spring Security policies to protect management traffic.
- Trigger: "configure health probes" – Define readiness and liveness groups for orchestrators.
- Trigger: "export metrics to prometheus" – Wire Micrometer registries and tune metric exposure.
- Trigger: "debug actuator startup" – Inspect condition evaluations and startup metrics when endpoints are missing or slow.

## Quick Start
1. Add the starter dependency.
   ```xml
   <!-- Maven -->
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-actuator</artifactId>
   </dependency>
   ```
   ```gradle
   // Gradle
   dependencies {
       implementation "org.springframework.boot:spring-boot-starter-actuator"
   }
   ```
2. Restart the service and verify `/actuator/health` and `/actuator/info` respond with `200 OK`.

## Implementation Workflow

### 1. Expose the required endpoints
- Set `management.endpoints.web.exposure.include` to the precise list or `"*"` for internal deployments.
- Adjust `management.endpoints.web.base-path` (e.g., `/management`) when the default `/actuator` conflicts with routing.
- Review detailed endpoint semantics in `references/endpoint-reference.md`.

### 2. Secure management traffic
- Apply an isolated `SecurityFilterChain` using `EndpointRequest.toAnyEndpoint()` with role-based rules.
- Combine `management.server.port` with firewall controls or service mesh policies for operator-only access.
- Keep `/actuator/health/**` publicly accessible only when required; otherwise enforce authentication.

### 3. Configure health probes
- Enable `management.endpoint.health.probes.enabled=true` for `/health/liveness` and `/health/readiness`.
- Group indicators via `management.endpoint.health.group.*` to match platform expectations.
- Implement custom indicators by extending `HealthIndicator` or `ReactiveHealthContributor`; sample implementations live in `references/examples.md#custom-health-indicator`.

### 4. Publish metrics and traces
- Activate Micrometer exporters (Prometheus, OTLP, Wavefront, StatsD) via `management.metrics.export.*`.
- Apply `MeterRegistryCustomizer` beans to add `application`, `environment`, and business tags for observability correlation.
- Surface HTTP request metrics with `server.observation.*` configuration when using Spring Boot 3.2+.

### 5. Enable diagnostics tooling
- Turn on `/actuator/startup` (Spring Boot 3.5+) and `/actuator/conditions` during incident response to inspect auto-configuration decisions.
- Register an `HttpExchangeRepository` (e.g., `InMemoryHttpExchangeRepository`) before enabling `/actuator/httpexchanges` for request auditing.
- Consult `references/official-actuator-docs.md` for endpoint behaviors and limits.

## Examples

### Basic – Expose health and info safely
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "health,info"
  endpoint:
    health:
      show-details: never
```

### Intermediate – Readiness group with custom indicator
```java
@Component
public class PaymentsGatewayHealth implements HealthIndicator {

    private final PaymentsClient client;

    public PaymentsGatewayHealth(PaymentsClient client) {
        this.client = client;
    }

    @Override
    public Health health() {
        boolean reachable = client.ping();
        return reachable ? Health.up().withDetail("latencyMs", client.latency()).build()
                         : Health.down().withDetail("error", "Gateway timeout").build();
    }
}
```
```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
      group:
        readiness:
          include: "readinessState,db,paymentsGateway"
          show-details: always
```

### Advanced – Dedicated management port with Prometheus export
```yaml
management:
  server:
    port: 9091
    ssl:
      enabled: true
  endpoints:
    web:
      exposure:
        include: "health,info,metrics,prometheus"
      base-path: "/management"
  metrics:
    export:
      prometheus:
        descriptions: true
        step: 30s
  endpoint:
    health:
      show-details: when-authorized
      roles: "ENDPOINT_ADMIN"
```
```java
@Configuration
public class ActuatorSecurityConfig {

    @Bean
    SecurityFilterChain actuatorChain(HttpSecurity http) throws Exception {
        http.securityMatcher(EndpointRequest.toAnyEndpoint())
            .authorizeHttpRequests(c -> c
                .requestMatchers(EndpointRequest.to("health")).permitAll()
                .anyRequest().hasRole("ENDPOINT_ADMIN"))
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }
}
```

More end-to-end samples are available in `references/examples.md`.

## Best Practices
- Keep SKILL.md concise and rely on `references/` for verbose documentation to conserve context.
- Apply the principle of least privilege: expose only required endpoints and restrict sensitive ones.
- Use immutable configuration via profile-specific YAML to align environments.
- Monitor actuator traffic separately to detect scraping abuse or brute-force attempts.
- Automate regression checks by scripting `curl` probes in CI/CD pipelines.

## Constraints
- Avoid exposing `/actuator/env`, `/actuator/configprops`, `/actuator/logfile`, and `/actuator/heapdump` on public networks.
- Do not ship custom health indicators that block event loop threads or exceed 250 ms unless absolutely necessary.
- Ensure Actuator metrics exporters run on supported Micrometer registries; unsupported exporters require custom registry beans.
- Maintain compatibility with Spring Boot 3.5.x conventions; older versions may lack probes and observation features.

## Reference Materials
- [Endpoint quick reference](references/endpoint-reference.md)
- [Implementation examples](references/examples.md)
- [Official documentation extract](references/official-actuator-docs.md)
- [Auditing with Actuator](references/auditing.md)
- [Cloud Foundry integration](references/cloud-foundry.md)
- [Enabling Actuator features](references/enabling.md)
- [HTTP exchange recording](references/http-exchanges.md)
- [JMX exposure](references/jmx.md)
- [Monitoring and metrics](references/monitoring.md)
- [Logging configuration](references/loggers.md)
- [Metrics exporters](references/metrics.md)
- [Observability with Micrometer](references/observability.md)
- [Process and Monitoring](references/process-monitoring.md)
- [Tracing](references/tracing.md)
- Scripts directory (`scripts/`) reserved for future automation; no runtime dependencies today.

## Validation Checklist
- Confirm `mvn spring-boot:run` or `./gradlew bootRun` exposes expected endpoints under `/actuator` (or custom base path).
- Verify `/actuator/health/readiness` returns `UP` with all mandatory components before promoting to production.
- Scrape `/actuator/metrics` or `/actuator/prometheus` to ensure required meters (`http.server.requests`, `jvm.memory.used`) are present.
- Run security scans to validate only intended ports and endpoints are reachable from outside the trusted network.

