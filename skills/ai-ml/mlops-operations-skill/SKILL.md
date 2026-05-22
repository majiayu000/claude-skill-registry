---
skill: 'mlops-operations'
version: '2.0.0'
updated: '2025-12-31'
category: 'operations'
complexity: 'advanced'
prerequisite_skills:
  - 'local-ai-deployment'
  - 'hardware-sizing'
composable_with:
  - 'production-readiness'
  - 'metrics-analytics'
  - 'data-sovereignty'
---

# MLOps Operations Skill

## Overview
Expertise in operating and maintaining production AI/ML systems, including deployment pipelines, monitoring, incident response, capacity management, and continuous improvement for local LLM infrastructure.

## Key Capabilities
- Production deployment and operations
- Monitoring and observability
- Incident management and response
- Capacity planning and scaling
- Model lifecycle management
- Cost optimization

## Operational Framework

### MLOps Maturity Model

```markdown
## MLOps Maturity Levels for Local AI

### Level 0: Manual
- Manual deployment via scripts
- Ad-hoc monitoring
- No formal processes
- Suitable for: POC, small pilots

### Level 1: Repeatable
- Documented deployment procedures
- Basic monitoring (health checks)
- Manual scaling
- Suitable for: Small production deployments

### Level 2: Defined
- Infrastructure as Code (IaC)
- Comprehensive monitoring and alerting
- Runbooks for common operations
- Suitable for: Production deployments

### Level 3: Managed
- Automated deployment pipelines
- Predictive scaling
- SLO-based alerting
- Suitable for: Enterprise production

### Level 4: Optimizing
- Continuous optimization
- Automated incident response
- Cost optimization automation
- Suitable for: Large-scale enterprise
```

### Service Level Objectives (SLOs)

```markdown
## SLO Framework for Local LLM

### Availability SLO
| Tier | Target | Monthly Downtime | Error Budget |
|------|--------|------------------|--------------|
| Standard | 99.5% | 3.6 hours | 216 minutes |
| Enhanced | 99.9% | 43 minutes | 43 minutes |
| Premium | 99.95% | 22 minutes | 22 minutes |

### Latency SLO
| Metric | Standard | Enhanced | Premium |
|--------|----------|----------|---------|
| TTFT P50 | <500ms | <300ms | <200ms |
| TTFT P95 | <2s | <1s | <500ms |
| Total P50 | <5s | <3s | <2s |
| Total P95 | <15s | <10s | <5s |

### Throughput SLO
| Metric | Standard | Enhanced | Premium |
|--------|----------|----------|---------|
| Tokens/sec (P50) | >50 | >100 | >200 |
| Requests/min | >10 | >30 | >100 |
| Queue depth max | <20 | <10 | <5 |

### Error Rate SLO
| Metric | Standard | Enhanced | Premium |
|--------|----------|----------|---------|
| Error rate | <2% | <1% | <0.5% |
| Timeout rate | <5% | <2% | <1% |
```

## Monitoring and Observability

### Metrics Collection

```yaml
# prometheus.yml - LLM monitoring configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # LLM inference server
  - job_name: 'vllm'
    static_configs:
      - targets: ['vllm:8000']
    metrics_path: /metrics
    scrape_interval: 10s

  # GPU metrics
  - job_name: 'dcgm'
    static_configs:
      - targets: ['dcgm-exporter:9400']
    scrape_interval: 5s

  # System metrics
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # Custom application metrics
  - job_name: 'ai-gateway'
    static_configs:
      - targets: ['gateway:9090']
```

### Key Metrics Reference

```markdown
## Essential Metrics for LLM Operations

### Infrastructure Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| gpu_utilization | GPU compute % | <20% (idle), >95% (saturated) |
| gpu_memory_used_bytes | VRAM usage | >90% capacity |
| gpu_temperature_celsius | GPU temp | >80°C |
| node_cpu_seconds_total | CPU usage | >90% sustained |
| node_memory_used_bytes | RAM usage | >85% |
| node_disk_io_utilization | Disk I/O | >80% |

### Application Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| llm_requests_total | Total requests | Trend analysis |
| llm_requests_in_flight | Active requests | >80% max |
| llm_request_duration_seconds | Latency histogram | P95 >SLO |
| llm_tokens_generated_total | Output tokens | Trend analysis |
| llm_time_to_first_token_seconds | TTFT | P95 >SLO |
| llm_queue_depth | Pending requests | >10 sustained |
| llm_errors_total | Error count | >1% rate |

### Business Metrics
| Metric | Description | Purpose |
|--------|-------------|---------|
| requests_by_user | Per-user count | Cost allocation |
| tokens_by_model | Per-model usage | Capacity planning |
| daily_active_users | Unique users | Adoption tracking |
| requests_by_type | Task breakdown | Usage patterns |
```

### Alerting Rules

```yaml
# alerts/llm-operations.yml
groups:
  - name: llm-availability
    rules:
      - alert: LLMServiceDown
        expr: up{job="vllm"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "LLM service is down"
          runbook: "https://runbooks/llm-down"

      - alert: LLMHighLatency
        expr: histogram_quantile(0.95, rate(llm_request_duration_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency exceeds 10 seconds"

      - alert: LLMHighErrorRate
        expr: rate(llm_errors_total[5m]) / rate(llm_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error rate exceeds 1%"

  - name: llm-infrastructure
    rules:
      - alert: GPUMemoryPressure
        expr: dcgm_fb_used / dcgm_fb_total > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "GPU memory above 90%"

      - alert: GPUHighTemperature
        expr: dcgm_gpu_temp > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "GPU temperature high"

  - name: llm-capacity
    rules:
      - alert: QueueBacklog
        expr: llm_queue_depth > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Request queue building up"

      - alert: CapacityNearLimit
        expr: avg_over_time(gpu_utilization[1h]) > 0.8
        for: 1h
        labels:
          severity: info
        annotations:
          summary: "Consider capacity expansion"
```

## Operational Runbooks

### Service Start/Stop

```markdown
## LLM Service Start Runbook

### Pre-Start Checklist
```bash
# 1. Verify GPU availability
nvidia-smi --query-gpu=name,memory.total --format=csv

# 2. Check disk space
df -h /mnt/models /var/log

# 3. Verify model files
ls -la /mnt/models/$(cat /opt/llm/config/model-name)

# 4. Check dependencies
docker compose -f /opt/llm/docker-compose.yml config --quiet
```

### Start Sequence
```bash
# 1. Start infrastructure services
docker compose up -d prometheus grafana

# 2. Start LLM server
docker compose up -d vllm

# 3. Wait for model loading
timeout 600 bash -c 'until curl -s http://localhost:8000/health | grep -q "ok"; do sleep 5; done'

# 4. Start API gateway
docker compose up -d nginx

# 5. Run smoke test
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"glm-4.6","messages":[{"role":"user","content":"test"}]}'
```

### Verification
```bash
# Check all services running
docker compose ps

# Verify metrics collection
curl -s http://localhost:9090/api/v1/query?query=up | jq '.data.result'

# Check for errors in logs
docker compose logs --tail=50 vllm | grep -i error
```

### Rollback
If startup fails:
```bash
docker compose down
docker compose -f docker-compose.backup.yml up -d
```
```

### Incident Response

```markdown
## Incident Response Runbook

### Severity Levels
| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| SEV1 | Service down | 15 minutes | Complete outage |
| SEV2 | Major degradation | 30 minutes | >50% errors |
| SEV3 | Minor degradation | 2 hours | Elevated latency |
| SEV4 | No impact | 1 business day | Warning alerts |

### Initial Response (SEV1/SEV2)
```
1. Acknowledge alert
2. Start incident channel (#incident-YYYYMMDD)
3. Assess impact scope
4. Notify stakeholders
5. Begin diagnosis
```

### Diagnosis Checklist
```bash
# 1. Service health
curl http://localhost:8000/health

# 2. Recent changes
git -C /opt/llm log --oneline -5

# 3. Resource utilization
nvidia-smi
docker stats --no-stream

# 4. Error logs
docker logs vllm --since 10m 2>&1 | grep -i error

# 5. Network connectivity
curl -v http://localhost:8000/health

# 6. System resources
free -h
df -h
```

### Common Issues and Fixes

#### Issue: OOM (Out of Memory)
**Symptoms:** Container restarts, CUDA out of memory errors
**Fix:**
```bash
# Reduce batch size
docker compose down
# Edit config: --max-num-seqs 64
docker compose up -d
```

#### Issue: High Latency
**Symptoms:** Slow responses, queue buildup
**Fix:**
```bash
# Check GPU utilization
nvidia-smi
# If saturated, reduce load or add capacity
# Temporary: enable request shedding
```

#### Issue: Connection Refused
**Symptoms:** 502/503 errors
**Fix:**
```bash
# Check if service is running
docker ps | grep vllm
# Restart if needed
docker compose restart vllm
```

### Post-Incident
1. Document timeline and resolution
2. Update runbooks if new issue
3. Schedule post-mortem for SEV1/SEV2
4. Track action items
```

## Capacity Management

### Capacity Planning

```markdown
## Capacity Planning Framework

### Current State Assessment
```bash
# Collect metrics for planning
promtool query range \
  --start="-30d" \
  --end="now" \
  --step="1h" \
  'avg_over_time(gpu_utilization[1h])'
```

### Growth Projection
```
Current utilization: 60%
Growth rate: 10% monthly
Capacity threshold: 80%

Months until threshold:
(80 - 60) / (60 * 0.1) = 3.3 months

Action: Plan capacity expansion within 3 months
```

### Scaling Decision Matrix
| Utilization | Queue Depth | Latency | Action |
|-------------|-------------|---------|--------|
| <50% | <5 | <SLO | Monitor |
| 50-70% | <10 | <SLO | Plan expansion |
| 70-80% | <15 | Near SLO | Execute expansion |
| >80% | >15 | >SLO | Emergency expansion |

### Scaling Options
1. **Vertical:** Larger GPU (4090 → A6000 → A100)
2. **Horizontal:** More replicas with load balancing
3. **Model optimization:** Quantization, smaller model
4. **Request shaping:** Rate limiting, prioritization
```

### Load Testing

```markdown
## Load Testing Procedures

### Pre-Production Load Test
```bash
# Using locust or custom script
python load_test.py \
  --target http://localhost:8000 \
  --users 50 \
  --spawn-rate 5 \
  --duration 10m \
  --output results.json
```

### Test Scenarios
| Scenario | Users | Duration | Purpose |
|----------|-------|----------|---------|
| Baseline | 10 | 5m | Establish normal metrics |
| Peak load | 50 | 10m | Validate capacity |
| Sustained | 30 | 1h | Check stability |
| Spike | 10→100→10 | 15m | Test elasticity |
| Soak | 30 | 8h | Memory leaks, degradation |

### Success Criteria
- [ ] P95 latency within SLO under peak load
- [ ] Error rate <1% under peak load
- [ ] No memory leaks over soak test
- [ ] Graceful degradation under overload
- [ ] Recovery time <5 minutes after spike
```

## Model Lifecycle Management

### Model Updates

```markdown
## Model Update Procedure

### Pre-Update
```bash
# 1. Download new model in staging
huggingface-cli download <provider>/<model> \
  --revision <REVISION_OR_TAG> \
  --local-dir /mnt/models/staging/<MODEL_DIR>-v2

# 2. Validate model
python validate_model.py /mnt/models/staging/<MODEL_DIR>-v2

# 3. Test in staging
docker run --gpus all -p 8001:8000 vllm/vllm-openai \
  --model /mnt/models/staging/<MODEL_DIR>-v2
pytest tests/model_acceptance.py --endpoint http://localhost:8001
```

### Blue-Green Deployment
```bash
# 1. Start new version
docker compose -f docker-compose-v2.yml up -d vllm-v2

# 2. Wait for ready
until curl -s http://localhost:8001/health; do sleep 5; done

# 3. Shift traffic gradually
# Update nginx upstream weights: v1=90%, v2=10%
# Monitor for errors
# Update weights: v1=50%, v2=50%
# Monitor
# Update weights: v1=0%, v2=100%

# 4. Decommission old version (after 24h)
docker compose down vllm-v1
```

### Rollback
```bash
# If issues detected:
# Revert nginx weights to v1=100%, v2=0%
# Document issue
# Stop v2
docker compose -f docker-compose-v2.yml down
```
```

### Model Versioning

```markdown
## Model Version Management

### Version Tracking
```yaml
# model-inventory.yml
models:
  - name: <MODEL_NAME>
    versions:
      - version: v1.0
        deployed: 2024-06-01
        status: deprecated
        path: /mnt/models/archive/<MODEL_DIR>-v1
      - version: v1.1
        deployed: 2024-09-01
        status: active
        path: /mnt/models/<MODEL_DIR>
      - version: v2.0
        deployed: null
        status: staging
        path: /mnt/models/staging/<MODEL_DIR>-v2
```

### Retention Policy
- **Active:** Currently serving production traffic
- **Standby:** Ready for quick rollback (keep 1 version)
- **Archive:** Compressed storage (keep 2 versions)
- **Delete:** Remove after 90 days in archive
```

## Cost Optimization

### Cost Tracking

```markdown
## Cost Allocation Framework

### Infrastructure Costs
| Component | Monthly Cost | Allocation Method |
|-----------|--------------|-------------------|
| Hardware amortization | $5,000 | Fixed |
| Power | $400 | Metered |
| Cooling | $100 | Estimated |
| Network | $200 | Fixed |
| Maintenance | $500 | Fixed |
| **Total** | **$6,200** | |

### Per-Request Cost
```
Monthly requests: 500,000
Cost per request: $6,200 / 500,000 = $0.0124

Compare to cloud:
- GPT-4o: ~$0.03/request (3,000 tokens)
- Local: $0.0124/request
- Savings: 59%
```

### Cost Optimization Levers
1. **Increase utilization:** Process more with same hardware
2. **Right-size models:** Use smallest model that meets quality needs
3. **Quantization:** Reduce resource requirements
4. **Batch processing:** Higher efficiency for async workloads
5. **Off-peak scheduling:** Run intensive tasks during low usage
```

### Efficiency Metrics

```markdown
## Operational Efficiency Metrics

### Utilization Targets
| Resource | Target Range | Below Target | Above Target |
|----------|--------------|--------------|--------------|
| GPU | 60-80% | Overprovisioned | Underprovisioned |
| Memory | 70-85% | Normal | Add capacity |
| CPU | 50-70% | Normal | Check bottleneck |

### Efficiency Calculations
```
GPU Efficiency = Useful Work / Total Capacity
             = (Tokens Generated × Quality Factor) / (Max Theoretical Tokens)

Cost Efficiency = Value Delivered / Total Cost
              = (Requests Processed × Value per Request) / Monthly Cost
```

### Optimization Actions
| Efficiency | Utilization | Action |
|------------|-------------|--------|
| Low | Low | Reduce capacity or increase workload |
| Low | High | Optimize configuration |
| High | Low | Good - headroom available |
| High | High | Good - consider expansion |
```

## Automation

### CI/CD for Model Updates

```yaml
# .github/workflows/model-update.yml
name: Model Update Pipeline

on:
  workflow_dispatch:
    inputs:
      model_name:
        description: 'Model to update'
        required: true
      model_version:
        description: 'Target version'
        required: true

jobs:
  validate:
    runs-on: self-hosted
    steps:
      - name: Download model
        run: |
          huggingface-cli download ${{ inputs.model_name }} \
            --revision ${{ inputs.model_version }} \
            --local-dir /tmp/model-staging

      - name: Validate model
        run: python scripts/validate_model.py /tmp/model-staging

      - name: Run acceptance tests
        run: |
          docker run -d --gpus all -p 8001:8000 \
            -v /tmp/model-staging:/model \
            vllm/vllm-openai --model /model
          sleep 120
          pytest tests/model_acceptance.py --endpoint http://localhost:8001

  deploy:
    needs: validate
    runs-on: self-hosted
    steps:
      - name: Deploy to staging
        run: |
          mv /tmp/model-staging /mnt/models/staging/
          ./scripts/deploy-staging.sh

      - name: Run smoke tests
        run: pytest tests/smoke.py --endpoint https://staging.llm.internal

      - name: Deploy to production
        run: ./scripts/deploy-production.sh
        if: success()
```

### Automated Remediation

```yaml
# Auto-remediation rules
rules:
  - name: restart-on-oom
    condition: container_restart_count > 3 in 10m
    action: |
      docker compose down
      docker system prune -f
      docker compose up -d
    cooldown: 30m

  - name: scale-on-queue
    condition: queue_depth > 20 for 5m
    action: |
      kubectl scale deployment vllm --replicas=+1
    cooldown: 15m
    max_replicas: 4

  - name: alert-on-degradation
    condition: error_rate > 0.05
    action: |
      slack-notify --channel ops --severity high \
        --message "LLM error rate elevated"
```

## Best Practices

### Operational Excellence
1. **Document everything:** Runbooks, procedures, decisions
2. **Automate repetitive tasks:** Deployments, backups, scaling
3. **Monitor proactively:** Catch issues before users notice
4. **Practice incident response:** Regular drills
5. **Continuous improvement:** Regular retrospectives

### Reliability
1. **Design for failure:** Graceful degradation
2. **Test recovery:** Regular DR tests
3. **Maintain headroom:** 20-30% capacity buffer
4. **Version everything:** IaC, configs, models
5. **Backup aggressively:** Configs, models, data

### Efficiency
1. **Right-size resources:** Match capacity to demand
2. **Optimize configurations:** Regular tuning
3. **Track costs:** Understand unit economics
4. **Eliminate waste:** Unused resources, inefficient processes
5. **Automate optimization:** Continuous improvement

This skill ensures reliable, efficient operation of local AI infrastructure with enterprise-grade operational practices.
