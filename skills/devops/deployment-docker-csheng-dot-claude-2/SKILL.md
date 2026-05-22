---
name: deployment-docker
description: Docker and containerization guidelines. Use when deployment docker guidance is required.
---
# Container Optimization Patterns

## Base Image Selection and Management

### Minimal Base Image Requirements

Execute lightweight, secure base image selection:
- Prefer alpine-based images for minimal footprint
- Use distroless images for maximum security
- Select official images with active maintenance
- Apply semantic versioning for image tags

Image versioning enforcement:
- Pin specific versions, avoid `latest` tags
- Use SHA digests for reproducible builds
- Implement automated base image updates
- Document version upgrade procedures

### Multi-Stage Build Implementation

Execute optimized build process with multi-stage builds:
- Separate build and runtime environments
- Copy only necessary artifacts to final stage
- Use build caches for faster incremental builds
- Minimize layer count and size

Layer optimization strategies:
- Group related operations into single layers
- Order instructions by frequency of change
- Use `.dockerignore` to exclude unnecessary files
- Leverage build cache effectively

## Security Hardening Standards

### Container Runtime Security

Execute non-root user implementation:
- Create and use dedicated service users
- Set appropriate file permissions
- Use `USER` directive in Dockerfile
- Apply capability dropping for minimal privileges

Security scanning and validation:
- Integrate vulnerability scanning in CI/CD
- Apply security policies with tools like Trivy
- Fix critical vulnerabilities before deployment
- Implement image signing with Notary or Cosign

### Secret Management Implementation

Execute external secret management:
- Use environment variables for configuration
- Implement secret management services (HashiCorp Vault, AWS Secrets Manager)
- Never bake secrets in container images
- Apply secret injection at runtime

Credential handling best practices:
- Rotate secrets regularly
- Use temporary credentials where possible
- Implement audit logging for secret access
- Apply principle of least privilege

# Resource Management and Orchestration

## Performance Optimization

### Resource Limits Configuration

Set appropriate resource constraints:
- Define memory limits and reservations
- Configure CPU quotas and shares
- Set appropriate request/limit ratios
- Monitor resource utilization metrics

Health check implementation:
- Configure comprehensive health checks
- Use appropriate check intervals and timeouts
- Implement graceful degradation strategies
- Monitor application responsiveness

### Container Orchestration Patterns

Execute Kubernetes deployment configuration:
- Use proper resource requests and limits
- Implement liveness and readiness probes
- Configure appropriate replica sets
- Apply pod disruption budgets

Service mesh integration:
- Implement service discovery mechanisms
- Use load balancing for high availability
- Apply circuit breakers for resilience
- Configure proper network policies

## Deployment Pipeline Integration

### CI/CD Container Build Pipeline

Execute automated build process:
- Integrate Docker builds in CI pipelines
- Implement automated testing in containers
- Use multi-environment deployment strategies
- Apply blue-green or canary deployments

Image registry management:
- Use private registries for sensitive images
- Implement proper access controls
- Configure image replication across regions
- Apply automated image cleanup policies

### Environment Configuration

Execute configuration management:
- Use ConfigMaps for application configuration
- Implement environment-specific overrides
- Apply configuration validation
- Document configuration requirements

Data persistence strategies:
- Use persistent volumes for stateful applications
- Implement backup and restore procedures
- Configure proper volume mounting
- Apply data lifecycle management

# Monitoring and Observability

## Container Monitoring Implementation

### Application Performance Monitoring

Execute container application instrumentation:
- Export application metrics via Prometheus
- Implement distributed tracing with Jaeger or Zipkin
- Configure log aggregation with ELK or Loki
- Set up alerting for critical metrics

Infrastructure monitoring:
- Monitor container resource usage
- Track container lifecycle events
- Implement cluster-level monitoring
- Use tools like cAdvisor and kube-state-metrics

### Security Monitoring

Execute container security monitoring:
- Implement runtime security monitoring
- Monitor for unusual container behavior
- Apply security policies and controls
- Use Falco or similar tools for threat detection

Compliance and audit logging:
- Log all container access and modifications
- Implement audit trail for container operations
- Monitor compliance with security policies
- Generate regular security reports
