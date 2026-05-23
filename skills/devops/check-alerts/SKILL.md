---
name: check-alerts
description: Check currently firing Grafana alerts, analyze alert status, and investigate alert issues in the Kagenti platform
---

# Check Alerts Skill

This skill helps you check and analyze Grafana alerts in the Kagenti platform.

## When to Use

- User asks "what alerts are firing?"
- User wants to check alert status
- After platform changes or deployments
- During incident investigation
- When troubleshooting platform issues

## What This Skill Does

1. **List Firing Alerts**: Show all currently active alerts
2. **Alert Details**: Display alert severity, component, and description
3. **Alert History**: Check recent alert state changes
4. **Query Alert Rules**: Verify alert configuration
5. **Test Alert Queries**: Validate PromQL queries

## Examples

### Check Firing Alerts

```bash
# Get all currently firing alerts from Grafana
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/alertmanager/grafana/api/v2/alerts' \
  -u admin:admin123 | python3 -c "
import sys, json
alerts = json.load(sys.stdin)
firing = [a for a in alerts if a.get('status', {}).get('state') == 'active']
print(f'Firing alerts: {len(firing)}')
for alert in firing:
    labels = alert.get('labels', {})
    annotations = alert.get('annotations', {})
    print(f\"\\n• {labels.get('alertname')} ({labels.get('severity')})\")
    print(f\"  Component: {labels.get('component')}\")
    print(f\"  Description: {annotations.get('description', 'N/A')[:100]}...\")
"
```

### List All Alert Rules

```bash
# Get all configured alert rules
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/v1/provisioning/alert-rules' \
  -u admin:admin123 | python3 -c "
import sys, json
rules = json.load(sys.stdin)
print(f'Total alert rules: {len(rules)}')
for rule in rules:
    print(f\"  • {rule.get('title')} ({rule.get('labels', {}).get('severity')})\")
"
```

### Check Specific Alert Configuration

```bash
# Get configuration for a specific alert
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/v1/provisioning/alert-rules' \
  -u admin:admin123 | python3 -c "
import sys, json
rules = json.load(sys.stdin)
alert_uid = 'prometheus-down'  # Change this to the alert UID
rule = next((r for r in rules if r.get('uid') == alert_uid), None)
if rule:
    print(f\"Alert: {rule.get('title')}\")
    print(f\"Query: {rule.get('data', [{}])[0].get('model', {}).get('expr')}\")
    print(f\"noDataState: {rule.get('noDataState')}\")
    print(f\"execErrState: {rule.get('execErrState')}\")
"
```

### Test Alert Query Against Prometheus

```bash
# Test an alert's PromQL query
QUERY='up{job="kubernetes-pods",app="prometheus"} == 0'

kubectl exec -n observability deployment/grafana -- \
  curl -s -G 'http://prometheus.observability.svc:9090/api/v1/query' \
  --data-urlencode "query=${QUERY}" | python3 -m json.tool
```

### Check Alert Evaluation State

```bash
# Check why an alert is firing or not firing
kubectl exec -n observability deployment/grafana -- \
  curl -s 'http://localhost:3000/api/v1/eval/rules' \
  -u admin:admin123 | python3 -m json.tool
```

## Alert Locations in Grafana UI

**Access Grafana**: https://grafana.localtest.me:9443
**Credentials**: admin / admin123

**Navigation**:
1. **Alerting** → **Alert rules** - View all configured alerts
2. **Alerting** → **Alert list** - See firing/pending alerts
3. **Alerting** → **Silences** - Manage alert silences
4. **Alerting** → **Contact points** - Check notification settings
5. **Alerting** → **Notification policies** - View routing rules

## Common Alert Issues

### False Positives
- Check `noDataState` configuration (should be `OK` for most alerts)
- Verify query matches actual resource type (Deployment vs StatefulSet)
- Test query returns correct results

### Alert Not Firing When It Should
- Verify metric exists in Prometheus
- Check alert threshold is appropriate
- Verify `for` duration isn't too long
- Check `noDataState` isn't masking the issue

### Alert Configuration Not Loading
- Restart Grafana: `kubectl rollout restart deployment/grafana -n observability`
- Check ConfigMap applied: `kubectl get configmap grafana-alerting -n observability`
- Verify no YAML syntax errors

## Related Documentation

- [Alert Runbooks](../../../docs/runbooks/alerts/)
- [Alert Testing Guide](../../../docs/04-observability/ALERT_TESTING_GUIDE.md)
- [CLAUDE.md Alert Monitoring](../../../CLAUDE.md#alert-monitoring)
- [TODO_INCIDENTS.md](../../../TODO_INCIDENTS.md) - Current incident tracking

## Runbooks by Alert

When an alert fires, consult its runbook:
- `docs/runbooks/alerts/<alert-uid>.md`

Example: If "Prometheus Down" alert fires → `docs/runbooks/alerts/prometheus-down.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
