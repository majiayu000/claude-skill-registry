---
name: python-micrometer-metrics-setup
description: |
  Sets up Micrometer metrics in a Spring Boot service from scratch, including dependencies, Actuator configuration, and registry customization. Use when starting a new microservice, configuring metrics export backends, enabling Prometheus scraping, or auto-configured JVM metrics. Foundational skill for metrics instrumentation in Java/Spring Boot applications.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer Metrics Setup

## Table of Contents

1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [Quick Start](#quick-start)
4. [Instructions](#instructions)
5. [Examples](#examples)
6. [Requirements](#requirements)
7. [Auto-Configured Metrics Reference](#auto-configured-metrics-reference)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
9. [See Also](#see-also)

---

## Purpose

Micrometer is Spring Boot's metrics framework. This skill covers the initial setup required before implementing custom metrics: adding dependencies, configuring Actuator endpoints, choosing backends, and understanding auto-configured metrics like JVM, HTTP, and database metrics.

## When to Use

Use this skill when you need to:

- **Start a new microservice** - Set up metrics infrastructure from scratch
- **Add Micrometer to existing service** - Retrofit metrics into Spring Boot application
- **Configure metrics export backends** - Choose between Prometheus, GCP Cloud Monitoring, Datadog, etc.
- **Enable Actuator endpoints** - Expose /actuator/metrics and /actuator/prometheus
- **Configure auto-metrics** - Enable JVM, HTTP, database, and system metrics
- **Set up Kubernetes scraping** - Add Prometheus annotations for pod discovery
- **Customize MeterRegistry** - Add common tags, filters, or histogram configuration
- **Understand baseline metrics** - Learn what's automatically collected by Spring Boot

**When NOT to use:**
- For implementing custom business metrics (use `python-python-micrometer-business-metrics` instead)
- For managing metric cardinality (use `python-python-micrometer-cardinality-control` instead)
- For GCP-specific export setup (use `python-python-micrometer-gcp-cloud-monitoring` instead)
- When Micrometer is already configured (skip to specific skill for your need)

---

## Quick Start

Add dependency to `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>

<!-- Choose your backend(s) -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

Enable endpoints in `application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus

  metrics:
    enable:
      jvm: true
      process: true
      http: true
```

Access metrics:
- `/actuator/metrics` - List all metrics
- `/actuator/metrics/{name}` - View specific metric
- `/actuator/prometheus` - Prometheus scrape endpoint

## Instructions

### Step 1: Add Dependencies

**Maven (pom.xml):**

```xml
<dependencies>
    <!-- Spring Boot Actuator (includes Micrometer) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>

    <!-- Backend: Prometheus (most common for Kubernetes) -->
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-registry-prometheus</artifactId>
    </dependency>

    <!-- Backend: GCP Cloud Monitoring (for GKE) -->
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-registry-stackdriver</artifactId>
    </dependency>

    <!-- Optional: Spring Cloud GCP helpers -->
    <dependency>
        <groupId>com.google.cloud</groupId>
        <artifactId>spring-cloud-gcp-starter-metrics</artifactId>
    </dependency>

    <!-- Optional: OpenTelemetry integration (for distributed tracing) -->
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-tracing-bridge-otel</artifactId>
    </dependency>

    <!-- Optional: Resilience4j integration -->
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-micrometer</artifactId>
    </dependency>
</dependencies>
```

**Gradle (build.gradle):**

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    implementation 'io.micrometer:micrometer-registry-prometheus'
    implementation 'io.micrometer:micrometer-registry-stackdriver'
    implementation 'com.google.cloud:spring-cloud-gcp-starter-metrics'
    implementation 'io.micrometer:micrometer-tracing-bridge-otel'
}
```

### Step 2: Configure Actuator Endpoints

Create `application.yml` with Actuator configuration:

```yaml
# Spring Boot configuration
spring:
  application:
    name: supplier-charges-api  # Used in metric tags
  jpa:
    properties:
      hibernate:
        generate_statistics: true  # Enable Hibernate metrics

# Actuator and Metrics configuration
management:
  # Endpoint exposure
  endpoints:
    web:
      exposure:
        # Expose these endpoints over HTTP
        include: health,info,metrics,prometheus
      base-path: /actuator

  # Individual endpoint configuration
  endpoint:
    health:
      show-details: when-authorized  # Hide details from unauthorized users
      probes:
        enabled: true  # Kubernetes liveness/readiness probes

    metrics:
      enabled: true

    prometheus:
      enabled: true

  # Health indicators
  health:
    circuitbreakers:
      enabled: true
    ratelimiters:
      enabled: true
    livenessState:
      enabled: true
    readinessState:
      enabled: true

  # Metrics configuration
  metrics:
    # Enable/disable meter types
    enable:
      jvm: true             # JVM memory, garbage collection, threads
      process: true         # Process CPU, uptime, file descriptors
      system: true          # System CPU, load average
      tomcat: true          # Tomcat threads, sessions
      logback: true         # Log events by level
      hikaricp: true        # Database connection pool
      jdbc: true            # JDBC operations (if using spring-data-jdbc)
      http: true            # HTTP server/client metrics

    # Common tags applied to ALL metrics
    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:local}
      region: ${GCP_REGION:local}
      version: ${BUILD_VERSION:unknown}

    # Distribution configuration (histograms)
    distribution:
      # Percentiles to calculate in-application (expensive!)
      percentiles:
        http.server.requests: 0.5,0.95,0.99

      # Histogram buckets (for Prometheus/Stackdriver)
      percentiles-histogram:
        http.server.requests: true
        http.client.requests: true

      # SLO-aligned buckets (Service Level Objectives)
      slo:
        http.server.requests: 10ms,50ms,100ms,200ms,500ms,1s,2s,5s
        http.client.requests: 100ms,500ms,1s,5s

    # HTTP request customization
    web:
      server:
        request:
          autotime:
            enabled: true
            percentiles: 0.95,0.99
            percentiles-histogram: true

      client:
        request:
          autotime:
            enabled: true

    # Prometheus export
    export:
      prometheus:
        enabled: true
        step: 1m  # Scrape interval
        descriptions: true  # Include metric descriptions

      # GCP Cloud Monitoring
      stackdriver:
        enabled: ${STACKDRIVER_ENABLED:false}
        project-id: ${GCP_PROJECT_ID}
        resource-type: k8s_container
        step: 1m
        resource-labels:
          cluster_name: ${GKE_CLUSTER_NAME}
          namespace_name: ${NAMESPACE}
          pod_name: ${POD_NAME}

  # Observations (Spring Boot 3.x only)
  observations:
    annotations:
      enabled: true  # Enable @Timed, @Counted aspects

# Resilience4j (optional)
resilience4j:
  metrics:
    enabled: true
```

### Step 3: Choose Backend(s)

Micrometer supports multiple backends. Choose based on your infrastructure:

**For Kubernetes/Prometheus:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

**For GCP/GKE:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-stackdriver</artifactId>
</dependency>
```

**For Datadog:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-datadog</artifactId>
</dependency>
```

**For multiple backends simultaneously:**
```xml
<!-- Prometheus (local Kubernetes scraping) -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>

<!-- Stackdriver (central GCP monitoring) -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-stackdriver</artifactId>
</dependency>
```

### Step 4: Inject MeterRegistry

Make `MeterRegistry` available application-wide:

```java
// Spring Boot auto-configures this bean
@Component
public class MetricsInitializer {

    private final MeterRegistry registry;

    public MetricsInitializer(MeterRegistry registry) {
        this.registry = registry;

        // Customize registry if needed
        registry.config().commonTags(
            "service.name", "supplier-charges-api"
        );
    }
}

// Inject into services
@Service
public class ChargeService {

    private final MeterRegistry registry;

    public ChargeService(MeterRegistry registry) {
        this.registry = registry;
    }

    public void processCharge(Charge charge) {
        Counter.builder("charge.processed")
            .register(registry)
            .increment();
    }
}
```

### Step 5: Verify Auto-Configured Metrics

Test that metrics are working:

```bash
# Start application
mvn spring-boot:run

# List available metrics
curl http://localhost:8080/actuator/metrics

# View specific metric
curl http://localhost:8080/actuator/metrics/jvm.memory.used

# Get Prometheus format
curl http://localhost:8080/actuator/prometheus
```

**Expected JVM metrics:**
- `jvm.memory.used`
- `jvm.gc.pause`
- `jvm.threads.live`
- `system.cpu.usage`
- `process.uptime`

**Expected HTTP metrics (after requests):**
- `http.server.requests`
- `http.client.requests` (if using RestTemplate/WebClient)

**Expected database metrics (with HikariCP):**
- `hikaricp.connections.active`
- `hikaricp.connections.idle`
- `hikaricp.connections.max`

### Step 6: Configure Kubernetes Prometheus Scraping

For Kubernetes, add annotations to enable Prometheus scraping:

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplier-charges-api
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"

    spec:
      containers:
      - name: app
        image: gcr.io/my-project/supplier-charges-api:latest
        ports:
        - containerPort: 8080
          name: http

        env:
        - name: ENVIRONMENT
          value: "production"
        - name: GCP_PROJECT_ID
          value: "my-project"
        - name: STACKDRIVER_ENABLED
          value: "true"

        # Kubernetes probe endpoints
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Step 7: Create Metrics Config Bean

Customize MeterRegistry behavior:

```java
@Configuration
public class MetricsConfig {

    /**
     * Add common tags to all metrics
     */
    @Bean
    public MeterRegistryCustomizer<MeterRegistry> commonTags(
            @Value("${spring.application.name}") String appName,
            @Value("${ENVIRONMENT:local}") String environment) {

        return registry -> registry.config().commonTags(
            "application", appName,
            "environment", environment,
            "region", System.getenv("GCP_REGION"),
            "version", System.getenv("BUILD_VERSION")
        );
    }

    /**
     * Configure HTTP server metrics
     */
    @Bean
    public MeterRegistryCustomizer<MeterRegistry> httpMetrics() {
        return registry -> {
            registry.config().meterFilter(
                new MeterFilter() {
                    @Override
                    public DistributionStatisticConfig configure(
                            Meter.Id id,
                            DistributionStatisticConfig config) {

                        if (id.getName().equals("http.server.requests")) {
                            return DistributionStatisticConfig.builder()
                                .percentilesHistogram(true)
                                .serviceLevelObjectives(
                                    Duration.ofMillis(50).toNanos(),
                                    Duration.ofMillis(100).toNanos(),
                                    Duration.ofMillis(200).toNanos(),
                                    Duration.ofMillis(500).toNanos(),
                                    Duration.ofSeconds(1).toNanos()
                                )
                                .build()
                                .merge(config);
                        }

                        return config;
                    }
                }
            );
        };
    }

    /**
     * Enable @Timed aspect (Spring Boot 3.0+)
     */
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
}
```

### Step 8: Test Metrics Endpoint

Verify metrics collection is working:

```java
@SpringBootTest
@AutoConfigureMockMvc
class MetricsEndpointTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private MeterRegistry registry;

    @Test
    void testMetricsEndpointAvailable() throws Exception {
        mockMvc.perform(get("/actuator/metrics"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.names").isArray())
            .andExpect(jsonPath("$.names[*]").exists());
    }

    @Test
    void testPrometheusEndpointAvailable() throws Exception {
        mockMvc.perform(get("/actuator/prometheus"))
            .andExpect(status().isOk())
            .andExpect(content().contentType("text/plain;charset=UTF-8"));
    }

    @Test
    void testJVMMetricsAutoConfigured() throws Exception {
        mockMvc.perform(get("/actuator/metrics/jvm.memory.used"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("jvm.memory.used"));
    }

    @Test
    void testHTTPMetricsRecorded() throws Exception {
        // Make a request
        mockMvc.perform(get("/health"))
            .andExpect(status().isOk());

        // Verify metrics recorded
        mockMvc.perform(get("/actuator/metrics/http.server.requests"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.measurements[0].statistic").exists());
    }
}
```

## Examples

### Example 1: Minimal Production Configuration

```yaml
# application-production.yml
management:
  endpoints:
    web:
      exposure:
        include: health,prometheus
      base-path: /actuator

  metrics:
    export:
      prometheus:
        enabled: true
        step: 1m

  endpoint:
    health:
      show-details: never

spring:
  application:
    name: supplier-charges-api
```

### Example 2: Complete Configuration with All Features

See Step 2 in Instructions above for comprehensive example.

### Example 3: Testing Metrics Configuration

```java
@SpringBootTest(
    properties = {
        "management.endpoints.web.exposure.include=metrics,prometheus",
        "management.metrics.enable.jvm=true",
        "management.metrics.enable.http=true"
    }
)
class MetricsConfigurationTest {

    @Autowired
    private MeterRegistry registry;

    @Test
    void testMeterRegistryConfigured() {
        assertThat(registry).isNotNull();
        assertThat(registry.getMeters()).isNotEmpty();
    }

    @Test
    void testCommonTagsApplied() {
        Counter counter = Counter.builder("test")
            .register(registry);

        assertThat(counter.getId().getTags())
            .extracting(Tag::getKey)
            .contains("application", "environment");
    }
}
```

## Requirements

- Spring Boot 2.1+ (2.7+ recommended)
- Maven 3.6+ or Gradle 6.0+
- Java 11+
- `spring-boot-starter-actuator` dependency
- One or more backend registries (Prometheus, Stackdriver, etc.)

## Auto-Configured Metrics Reference

When you add `spring-boot-starter-actuator`, these metrics are automatically enabled:

| Category | Metrics | Requires |
|----------|---------|----------|
| JVM | memory, GC, threads, classes | `jvm: true` |
| Process | CPU, uptime, file descriptors | `process: true` |
| System | CPU, load average | `system: true` |
| HTTP Server | request latency, count, status | `http: true` |
| HTTP Client | (same as server) | RestTemplate/WebClient |
| Database | HikariCP connections | `hikaricp: true` |
| Tomcat | threads, sessions (embedded) | `tomcat: true` |
| Logback | log events by level | `logback: true` |
| Hibernate | sessions, queries, cache | JPA enabled |

## Anti-Patterns to Avoid

```yaml
# ❌ Wrong: exposing sensitive endpoints
endpoints:
  web:
    exposure:
      include: "*"  # Exposes all endpoints!

# ✅ Right: whitelist only needed endpoints
endpoints:
  web:
    exposure:
      include: health,info,metrics,prometheus

# ❌ Wrong: all percentiles calculated client-side
percentiles:
  http.server.requests: 0.1,0.25,0.5,0.75,0.9,0.95,0.99,0.999

# ✅ Right: histogram buckets let backend calculate
percentiles-histogram:
  http.server.requests: true

# ❌ Wrong: no common tags
tags: {}

# ✅ Right: apply common tags consistently
tags:
  application: ${spring.application.name}
  environment: ${ENVIRONMENT}
  version: ${BUILD_VERSION}

# ❌ Wrong: custom metrics without registry injection
@Service
public class Service {
    public void doWork() {
        // registry is null!
        Counter.builder("work").register(registry);
    }
}

# ✅ Right: inject registry in constructor
@Service
public class Service {
    private final MeterRegistry registry;

    public Service(MeterRegistry registry) {
        this.registry = registry;
    }

    public void doWork() {
        Counter.builder("work").register(registry).increment();
    }
}
```

## See Also

- [python-micrometer-business-metrics](../python-micrometer-business-metrics/SKILL.md) - Create custom business metrics
- [python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md) - Prevent metric explosion
- [python-test-micrometer-testing-metrics](../python-test-micrometer-testing-metrics/SKILL.md) - Test metrics
- [python-micrometer-gcp-cloud-monitoring](../python-micrometer-gcp-cloud-monitoring/SKILL.md) - Export to GCP
