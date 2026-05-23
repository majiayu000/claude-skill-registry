---
name: python-micrometer-gcp-cloud-monitoring
description: |
  Exports Micrometer metrics to GCP Cloud Monitoring (Stackdriver) for GKE deployments. Use when setting up metrics export in Kubernetes environments, configuring Workload Identity, managing metric prefixes and resource labels, or correlating metrics with GCP services. Critical for GKE-based microservices with centralized observability in Google Cloud.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer GCP Cloud Monitoring Integration

## Quick Start

Export metrics to Cloud Monitoring in 3 steps:

**1. Add dependencies:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-stackdriver</artifactId>
</dependency>
<dependency>
    <groupId>com.google.cloud</groupId>
    <artifactId>spring-cloud-gcp-starter-metrics</artifactId>
</dependency>
```

**2. Configure export:**
```yaml
management:
  metrics:
    export:
      stackdriver:
        enabled: true
        project-id: ${GCP_PROJECT_ID}
        resource-type: k8s_container
        step: 1m
        resource-labels:
          cluster_name: ${GKE_CLUSTER_NAME}
          namespace_name: ${NAMESPACE}
          pod_name: ${POD_NAME}
```

**3. Grant IAM permission:**
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"
```

See [references/workload-identity-setup.md](references/workload-identity-setup.md) for complete Workload Identity setup.

## Table of Contents

1. [When to Use](#when-to-use)
2. [Configuration](#configuration)
3. [Testing](#testing)
4. [Supporting Files](#supporting-files)
5. [Requirements](#requirements)
6. [Anti-Patterns](#anti-patterns)

## When to Use

Use this skill when you need to:

- Export metrics to GCP Cloud Monitoring for GKE deployments
- Configure Workload Identity for secure pod authentication
- Set resource labels for filtering in Cloud Console
- Correlate metrics with GKE, Pub/Sub, Cloud SQL services
- Create dashboards and alerts in Cloud Monitoring

**When NOT to use:**
- Prometheus-only environments (use Prometheus registry)
- Before basic Micrometer setup (use `python-micrometer-metrics-setup`)
- Local development (use Prometheus locally)
- Without Workload Identity (requires GKE 1.12+)

## Configuration

### Basic Configuration

```yaml
# application.yml
management:
  metrics:
    export:
      stackdriver:
        enabled: ${STACKDRIVER_ENABLED:true}
        project-id: ${GCP_PROJECT_ID}
        step: 1m  # Export frequency
        resource-type: k8s_container  # GKE resource type

        # Resource labels (appear on every metric)
        resource-labels:
          cluster_name: ${GKE_CLUSTER_NAME}
          namespace_name: ${NAMESPACE}
          pod_name: ${POD_NAME}
          container_name: ${CONTAINER_NAME:app}
          environment: ${ENVIRONMENT:production}
          region: ${GCP_REGION:europe-west2}

    # Common tags (filterable in queries)
    tags:
      application: ${spring.application.name}
      version: ${BUILD_VERSION:unknown}

    # Histogram buckets for latency metrics
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 10ms,50ms,100ms,200ms,500ms,1s,2s,5s
```

### Kubernetes Deployment Environment Variables

```yaml
# deployment.yaml
env:
  - name: GCP_PROJECT_ID
    value: "my-project"
  - name: GKE_CLUSTER_NAME
    value: "my-cluster"
  - name: NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
  - name: CONTAINER_NAME
    value: "app"
```

### Custom Metric Configuration

```java
@Configuration
public class CloudMonitoringConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> commonTags() {
        return registry -> registry.config().commonTags(
            "service", "my-api",
            "component", "backend"
        );
    }
}
```

## Testing

### Verify Export in Logs

```bash
# Check pod logs for metric export success
kubectl logs -f deployment/my-api -n my-namespace

# Look for: "Successfully published X metrics to Stackdriver"
```

### Query Metrics via CLI

```bash
# List exported metrics
gcloud monitoring metrics-descriptors list \
  --filter="metric.type:custom.googleapis.com"
```

### View in Cloud Console

1. Open GCP Console → Cloud Monitoring → Metrics Explorer
2. Select resource: "Kubernetes Container"
3. Filter by cluster
4. View metric: custom.googleapis.com/...

## Supporting Files

| File | Purpose |
|------|---------|
| [references/workload-identity-setup.md](references/workload-identity-setup.md) | Complete Workload Identity configuration guide |
| [references/dashboards-and-alerting.md](references/dashboards-and-alerting.md) | Create dashboards and alert policies with Terraform |

## Requirements

- Spring Boot 2.1+ with Actuator
- `micrometer-registry-stackdriver` dependency
- GCP Project with Cloud Monitoring API enabled
- GKE cluster with Workload Identity enabled
- IAM role: `roles/monitoring.metricWriter`
- Java 11+

## Anti-Patterns

```yaml
# ❌ Missing resource labels (hard to filter)
resource-labels:
  environment: production

# ✅ Complete resource labels
resource-labels:
  cluster_name: my-cluster
  namespace_name: my-namespace
  pod_name: ${POD_NAME}

# ❌ High cardinality resource labels (memory issues)
resource-labels:
  pod_ip: ${POD_IP}       # Changes constantly
  user_id: ${USER_ID}     # Unbounded

# ✅ Stable, bounded labels
resource-labels:
  cluster_name: my-cluster
  environment: production
```

## See Also

- [python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md) - Manage metric cardinality
- [python-micrometer-business-metrics](../python-micrometer-business-metrics/SKILL.md) - Create business metrics
- [python-micrometer-metrics-setup](../python-micrometer-metrics-setup/SKILL.md) - Initial Micrometer setup
