---
name: investigate-incident
description: Investigate platform incidents, perform RCA, create incident documentation, and follow alert runbooks in the Kagenti platform
---

# Investigate Incident Skill

This skill helps you investigate incidents, perform root cause analysis (RCA), and create comprehensive incident documentation.

## When to Use

- After alerts fire (check runbooks first)
- When tests fail unexpectedly
- User reports service unavailable
- Pods in CrashLoopBackOff or ImagePullBackOff
- Services showing degraded performance
- After deployment issues

## What This Skill Does

1. **Follow Runbooks**: Execute alert-specific investigation steps
2. **Gather Evidence**: Collect logs, metrics, events, pod status
3. **Root Cause Analysis**: Identify underlying issues
4. **Document Incidents**: Create structured RCA in TODO_INCIDENTS.md
5. **Track Fixes**: Plan and validate remediation

## Investigation Workflow

### 1. Check If Alert Has Runbook

```bash
# List all available runbooks
ls -1 docs/runbooks/alerts/*.md

# For specific alert, check annotation
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/v1/provisioning/alert-rules' \
  -u admin:admin123 | python3 -c "
import sys, json
rules = json.load(sys.stdin)
alert_uid = 'prometheus-down'  # Change this
rule = next((r for r in rules if r.get('uid') == alert_uid), None)
if rule:
    print('Runbook URL:', rule['annotations'].get('runbook_url', 'N/A'))
"
```

### 2. Follow Runbook Steps

**Runbooks are located at**: `docs/runbooks/alerts/<alert-uid>.md`

**Standard runbook sections**:
1. **Meaning** - What this alert indicates
2. **Impact** - Business/platform impact
3. **Diagnosis** - Investigation commands
4. **Mitigation** - How to fix

**Example: Follow Prometheus Down runbook**:

```bash
# From docs/runbooks/alerts/prometheus-down.md

# 1. Check pod status
kubectl get pods -n observability -l app=prometheus

# 2. Check pod logs
kubectl logs -n observability deployment/prometheus --tail=100

# 3. Check events
kubectl get events -n observability --field-selector involvedObject.name=prometheus --sort-by='.lastTimestamp'

# 4. Test Prometheus endpoint
kubectl exec -n observability deployment/grafana -- \
  curl -s http://prometheus.observability.svc:9090/-/ready
```

### 3. Gather Comprehensive Evidence

**Pod Status & Events**:
```bash
# Get pod status in namespace
kubectl get pods -n <namespace>

# Detailed pod description
kubectl describe pod <pod-name> -n <namespace>

# Recent events sorted by time
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# All failing pods across platform
kubectl get pods -A | grep -E "Error|CrashLoop|ImagePull|Pending"
```

**Logs**:
```bash
# Current container logs
kubectl logs -n <namespace> <pod-name> --tail=100

# Previous container (if crashed)
kubectl logs -n <namespace> <pod-name> --previous

# Specific container in pod
kubectl logs -n <namespace> <pod-name> -c <container-name>

# All containers in pod
kubectl logs -n <namespace> <pod-name> --all-containers=true

# Query Loki for errors (last 5 minutes)
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://loki.observability.svc:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={kubernetes_namespace_name="<namespace>"} |= "error"' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$(date -u -v-5M +%s)000000000" \
  --data-urlencode "end=$(date -u +%s)000000000" | python3 -m json.tool
```

**Metrics**:
```bash
# Check if service is up
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode 'query=up{job="<job-name>"}' | python3 -m json.tool

# Check replica availability
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode 'query=kube_deployment_status_replicas_available{deployment="<name>"}' \
  | python3 -m json.tool

# Check pod restarts
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode 'query=kube_pod_container_status_restarts_total{pod=~"<pod-pattern>"}' \
  | python3 -m json.tool
```

**ArgoCD Application Status**:
```bash
# Check application health
argocd app get <app-name> --port-forward --port-forward-namespace argocd --grpc-web

# Check sync status
argocd app list --port-forward --port-forward-namespace argocd --grpc-web | grep -E "Degraded|OutOfSync"

# View recent sync history
argocd app history <app-name> --port-forward --port-forward-namespace argocd --grpc-web
```

### 4. Identify Root Cause

**Common Root Causes**:

1. **Configuration Error**
   - Check recent Git commits: `git log --oneline -10`
   - Check ArgoCD diff: `argocd app diff <app-name> --port-forward ...`
   - Validate YAML: `kustomize build components/...`

2. **Image Issues**
   - Check image availability: `docker exec kagenti-demo-control-plane crictl images | grep <image>`
   - Check ImagePullBackOff: `kubectl describe pod <pod-name> | grep -A10 "Events"`

3. **Resource Constraints**
   - Check pod resources: `kubectl top pods -n <namespace>`
   - Check node resources: `kubectl top nodes`
   - Check OOM kills: `kubectl get events -A | grep OOM`

4. **Dependency Failure**
   - Check if dependent service is healthy
   - Check service endpoints: `kubectl get endpoints -n <namespace>`
   - Test connectivity: `kubectl run debug-curl -n <namespace> --image=curlimages/curl --rm -it -- curl http://service-name`

5. **mTLS/Network Issues**
   - Check Istio sidecar: `kubectl get pods -n <namespace>` (should show 2/2)
   - Check PeerAuthentication: `kubectl get peerauthentication -A`
   - Check sidecar logs: `kubectl logs -n <namespace> <pod-name> -c istio-proxy`

6. **Certificate Issues**
   - Check certificate status: `kubectl get certificate -A`
   - Check cert-manager logs: `kubectl logs -n cert-manager deployment/cert-manager`

### 5. Create Incident Documentation

**Create entry in TODO_INCIDENTS.md**:

```markdown
## Incident #X: [Alert Name] - [Brief Description]

**Status**: 🔴 Active / 🟡 Investigating / 🟢 Resolved

**Detected**: 2025-11-17 08:31:40 UTC

**Severity**: Critical / Warning / Info

**Components Affected**:
- Component 1
- Component 2

### Summary

Brief description of what happened.

### Investigation

**Timeline**:
- 08:31 - Alert fired
- 08:35 - Checked pod status, found CrashLoopBackOff
- 08:40 - Reviewed logs, identified error message
- 08:45 - Identified root cause

**Evidence Collected**:

1. **Pod Status**:
   ```
   NAME                 READY   STATUS             RESTARTS
   component-xxx        0/2     CrashLoopBackOff   5
   ```

2. **Error Logs**:
   ```
   ERROR: Failed to connect to database: connection refused
   ```

3. **Events**:
   ```
   Back-off restarting failed container
   ```

### Root Cause Analysis

**Root Cause**: [Specific technical reason]

**Why it happened**:
- Contributing factor 1
- Contributing factor 2

**Why alert fired**:
- PromQL query: `query_here`
- Query returned: `value`
- Threshold: `> threshold`

### Resolution

**Fix Applied**:
```bash
# Commands to fix the issue
kubectl apply -f ...
```

**Verification**:
```bash
# Commands to verify fix
kubectl get pods -n <namespace>
# Output showing healthy state
```

**Time to Resolution**: XX minutes

### Lessons Learned

1. **What went well**: Early detection via alerting
2. **What could improve**: Need better validation before deploy
3. **Action items**:
   - [ ] Add pre-deployment validation
   - [ ] Update runbook with this scenario
   - [ ] Add integration test for this case

### Related

- Alert: `alert-uid`
- Runbook: docs/runbooks/alerts/alert-uid.md
- Git commits: abc1234, def5678
```

### 6. Validate Fix

**After applying fix**:

```bash
# 1. Verify pods are healthy
kubectl get pods -n <namespace>

# 2. Check alert stopped firing
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/alertmanager/grafana/api/v2/alerts' \
  -u admin:admin123 | python3 -c "
import sys, json
alerts = json.load(sys.stdin)
firing = [a for a in alerts if a.get('status', {}).get('state') == 'active']
for a in firing:
    print(f\"{a['labels']['alertname']}: {a['labels']['severity']}\")
"

# 3. Run integration tests
pytest tests/integration/test_<component>.py -v

# 4. Check platform status
./scripts/platform-status.sh

# 5. Verify in Grafana UI
open https://grafana.localtest.me:9443/alerting/list
```

## Common Investigation Patterns

### Pattern 1: Pod Won't Start

```bash
# Investigation flow
kubectl get pods -n <namespace>  # Get pod status
kubectl describe pod <pod-name> -n <namespace>  # Check events
kubectl logs <pod-name> -n <namespace>  # Check logs (if available)

# Common causes:
# - ImagePullBackOff: Image not found or not loaded
# - CrashLoopBackOff: Application exits on startup
# - Pending: Resource constraints or scheduling issues
# - Init:Error: Init container failed
```

### Pattern 2: Service Unavailable

```bash
# Investigation flow
kubectl get pods -n <namespace> -l app=<service>  # Check pods
kubectl get svc -n <namespace> <service-name>  # Check service
kubectl get endpoints -n <namespace> <service-name>  # Check endpoints
kubectl get httproute -n <namespace>  # Check routes (if using Gateway API)

# Test connectivity
kubectl run debug-curl -n <namespace> --image=curlimages/curl --rm -it \
  -- curl -v http://<service-name>.<namespace>.svc:PORT
```

### Pattern 3: High Resource Usage

```bash
# Investigation flow
kubectl top pods -n <namespace> --sort-by=memory  # Memory usage
kubectl top pods -n <namespace> --sort-by=cpu  # CPU usage

# Check limits
kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources}{"\n"}{end}'

# Check for OOM kills
kubectl get events -n <namespace> | grep OOM
```

### Pattern 4: Frequent Restarts

```bash
# Investigation flow
kubectl get pods -n <namespace>  # Check RESTARTS column
kubectl describe pod <pod-name> -n <namespace>  # Check restart reason
kubectl logs <pod-name> -n <namespace> --previous  # Logs before crash

# Check restart metrics
kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode 'query=increase(kube_pod_container_status_restarts_total{pod="<pod-name>"}[1h])'
```

### Pattern 5: ArgoCD App OutOfSync

```bash
# Investigation flow
argocd app get <app-name> --port-forward ...  # Get status
argocd app diff <app-name> --port-forward ...  # See differences

# Check last sync
argocd app history <app-name> --port-forward ...

# Force sync if needed
argocd app sync <app-name> --force --prune --port-forward ...
```

## Integration with Other Skills

**Use check-alerts skill** to find which alerts are firing:
```bash
# This automatically invokes check-alerts skill
"What alerts are currently firing?"
```

**Use check-logs skill** to query specific error patterns:
```bash
# This automatically invokes check-logs skill
"Show me error logs from keycloak namespace in the last 10 minutes"
```

**Use check-metrics skill** to verify service health:
```bash
# This automatically invokes check-metrics skill
"What's the CPU usage of pods in observability namespace?"
```

## Incident Priority Guidelines

**Critical (P0)**:
- Platform-wide outage
- All users affected
- Data loss risk
- Security breach

**High (P1)**:
- Major feature unavailable
- Multiple users affected
- Performance severely degraded

**Medium (P2)**:
- Minor feature unavailable
- Some users affected
- Workaround available

**Low (P3)**:
- Cosmetic issue
- Minimal impact
- Can be fixed in next release

## Related Documentation

- [TODO_INCIDENTS.md](../../../TODO_INCIDENTS.md) - Active incident tracking
- [docs/runbooks/alerts/](../../../docs/runbooks/alerts/) - Alert-specific runbooks
- [CLAUDE.md Alert Monitoring](../../../CLAUDE.md#alert-monitoring) - Alert workflow
- [docs/04-observability/ALERT_TESTING_GUIDE.md](../../../docs/04-observability/ALERT_TESTING_GUIDE.md) - Alert testing

## Pro Tips

1. **Always check runbook first**: Save time by following proven steps
2. **Capture evidence early**: Logs/events may be lost if pod restarts
3. **Use --previous logs**: For crashed pods, previous container logs are critical
4. **Check Git history**: Recent commits often reveal configuration changes
5. **Document as you go**: Don't wait until end to write RCA
6. **Verify fix completely**: Check pods, alerts, tests, and platform status
7. **Update runbook**: Add new scenarios discovered during investigation

🤖 Generated with [Claude Code](https://claude.com/claude-code)
