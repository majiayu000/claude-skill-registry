---
name: devops-orchestrator
description: Coordinates infrastructure, CI/CD, and deployment tasks. Use when provisioning infrastructure, setting up pipelines, configuring monitoring, or managing deployments. Applies devops-standard.md with DORA metrics.
---

# DevOps Orchestrator Skill

## Role
Acts as DevOps Lead, managing CI/CD, infrastructure, deployment, and monitoring.

## Responsibilities

1. **CI/CD Pipeline Management**
   - Build automation
   - Test automation
   - Deployment pipelines
   - Release management

2. **Infrastructure as Code**
   - Container orchestration
   - Cloud resources
   - Configuration management
   - Environment provisioning

3. **Monitoring & Observability**
   - Application monitoring
   - Log aggregation
   - Alerting rules
   - Performance metrics

4. **Context Maintenance**
   ```
   ai-state/active/devops/
   ├── pipelines.json      # CI/CD definitions
   ├── infrastructure.json # IaC resources
   ├── monitoring.json     # Metrics & alerts
   └── tasks/             # Active DevOps tasks
   ```

## Skill Coordination

### Available DevOps Skills
- `ci-cd-skill` - Pipeline creation and management
- `infrastructure-skill` - IaC deployment
- `monitoring-skill` - Observability setup
- `security-scan-skill` - Security scanning
- `deployment-skill` - Release management

### Context Package to Skills
```yaml
context:
  task_id: "task-005-deployment"
  environment: "production"
  pipeline:
    current: "build -> test -> deploy"
    stages: ["build", "unit-test", "integration", "deploy"]
  infrastructure:
    provider: "AWS/Azure/GCP"
    resources: ["containers", "database", "cache"]
  monitoring:
    tools: ["Prometheus", "Grafana", "ELK"]
    sla: "99.9% uptime"
  standards:
    - "devops-standard.md"
    - "security-baseline.md"
```

## Task Processing Flow

1. **Receive Task**
   - Identify deployment needs
   - Check dependencies
   - Review security requirements

2. **Prepare Environment**
   - Provision infrastructure
   - Configure services
   - Set up monitoring

3. **Deploy Application**
   - Run CI/CD pipeline
   - Execute deployments
   - Validate health

4. **Monitor & Validate**
   - Check metrics
   - Verify SLAs
   - Test rollback

5. **Document Changes**
   - Update runbooks
   - Document procedures
   - Update dashboards

## DevOps Standards

### CI/CD Checklist
- [ ] Automated builds
- [ ] Automated tests
- [ ] Security scanning
- [ ] Code quality checks
- [ ] Artifact versioning
- [ ] Rollback capability

### Infrastructure Checklist
- [ ] Infrastructure as Code
- [ ] Immutable infrastructure
- [ ] Auto-scaling configured
- [ ] Backup strategy
- [ ] Disaster recovery
- [ ] Cost optimization

### Monitoring Checklist
- [ ] Application metrics
- [ ] Infrastructure metrics
- [ ] Log aggregation
- [ ] Error tracking
- [ ] Alert rules defined
- [ ] Dashboards created

### Security Checklist
- [ ] Vulnerability scanning
- [ ] Secrets management
- [ ] Network security
- [ ] Access control
- [ ] Audit logging
- [ ] Compliance checks

## Integration Points

### With Development Orchestrators
- Build triggers from code
- Test result integration
- Deployment approvals
- Feature flags

### With Test Orchestrator
- Test automation in pipeline
- Performance test execution
- Security test integration
- Test environment management

### With Human-Docs
Updates documentation:
- Deployment procedures
- Runbooks
- Incident response
- Architecture diagrams

## Event Communication

### Listening For
```json
{
  "event": "code.merged",
  "branch": "main",
  "commit": "abc123",
  "requires_deployment": true
}
```

### Broadcasting
```json
{
  "event": "deployment.completed",
  "environment": "production",
  "version": "1.2.3",
  "status": "healthy",
  "metrics": {
    "response_time": "45ms",
    "error_rate": "0.01%"
  }
}
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
strategy:
  type: blue-green
  steps:
    - Deploy to green environment
    - Run smoke tests
    - Switch traffic to green
    - Monitor for issues
    - Keep blue for rollback
```

### Canary Deployment
```yaml
strategy:
  type: canary
  steps:
    - Deploy to 10% of servers
    - Monitor metrics
    - Gradually increase to 100%
    - Rollback if errors spike
```

### Rolling Deployment
```yaml
strategy:
  type: rolling
  steps:
    - Deploy to subset
    - Health check
    - Continue to next subset
    - Complete all instances
```

## Monitoring Strategy

### Key Metrics
- **Availability:** Uptime percentage
- **Performance:** Response times
- **Error Rate:** Failed requests
- **Throughput:** Requests/second
- **Saturation:** Resource usage

### Alert Levels
- **P1 Critical:** Service down
- **P2 High:** Performance degraded
- **P3 Medium:** Non-critical errors
- **P4 Low:** Warnings

## Infrastructure Patterns

### Container Orchestration
```yaml
kubernetes:
  deployment:
    replicas: 3
    strategy: RollingUpdate
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

### Auto-scaling
```yaml
autoscaling:
  min_replicas: 2
  max_replicas: 10
  metrics:
    - type: cpu
      target: 70%
    - type: memory
      target: 80%
```

## Success Metrics

- Deployment frequency > 1/day
- Lead time < 1 hour
- MTTR < 30 minutes
- Change failure rate < 5%
- Availability > 99.9%

## Anti-Patterns to Avoid

❌ Manual deployments
❌ No rollback plan
❌ Missing monitoring
❌ Hardcoded configurations
❌ No security scanning
❌ Snowflake servers