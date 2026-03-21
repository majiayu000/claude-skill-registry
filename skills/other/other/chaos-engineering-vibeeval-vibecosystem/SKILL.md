---
name: chaos-engineering
description: Failure injection patterns, blast radius control, steady state hypothesis, and gameday planning for resilience testing.
---

# Chaos Engineering

Systematic resilience testing to discover weaknesses before they cause outages.

## Steady State Hypothesis

```yaml
# Define BEFORE injecting chaos - what "normal" looks like
steady_state_hypothesis:
  title: "API serves traffic within SLO"
  probes:
    - name: "API response time p95 < 500ms"
      type: http
      url: "https://api.example.com/health"
      threshold: 500

    - name: "Error rate < 1%"
      type: prometheus
      query: "rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m])"
      threshold: 0.01

    - name: "Order processing queue depth < 100"
      type: cloudwatch
      metric: "ApproximateNumberOfMessagesVisible"
      threshold: 100

    - name: "Database connections < 80% capacity"
      type: prometheus
      query: "pg_stat_activity_count / pg_settings_max_connections"
      threshold: 0.8
```

## Failure Injection Patterns

```python
# Using Chaos Toolkit (chaostoolkit.org)
# experiment.json

{
  "title": "Database failover resilience",
  "description": "Verify app handles primary DB failover gracefully",

  "steady-state-hypothesis": {
    "title": "API responds normally",
    "probes": [
      {
        "name": "api-health",
        "type": "probe",
        "provider": {
          "type": "http",
          "url": "https://api.example.com/health",
          "timeout": 5
        },
        "tolerance": {"status": 200}
      }
    ]
  },

  "method": [
    {
      "name": "failover-primary-db",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "failover_db_cluster",
        "arguments": {
          "db_cluster_identifier": "prod-cluster"
        }
      },
      "pauses": {"after": 60}
    }
  ],

  "rollbacks": [
    {
      "name": "verify-db-recovered",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.probes",
        "func": "cluster_status",
        "arguments": {
          "db_cluster_identifier": "prod-cluster"
        }
      },
      "tolerance": "available"
    }
  ]
}
```

## Blast Radius Control

```python
# ALWAYS limit the impact of chaos experiments

class BlastRadiusController:
    """Control and limit chaos experiment impact."""

    def __init__(self, config: dict):
        self.max_affected_percentage = config.get('max_affected_pct', 5)
        self.max_duration_seconds = config.get('max_duration_s', 300)
        self.excluded_services = config.get('excluded', ['auth', 'payments'])
        self.kill_switch_url = config.get('kill_switch_url')

    def can_inject(self, target: str, scope: str) -> bool:
        # Never chaos-test critical services without explicit approval
        if target in self.excluded_services:
            return False

        # Never inject during peak hours
        hour = datetime.now().hour
        if 9 <= hour <= 17:  # Business hours (adjust per timezone)
            return False

        # Never affect more than N% of instances
        if self.get_affected_percentage(target, scope) > self.max_affected_percentage:
            return False

        return True

    def get_affected_percentage(self, target: str, scope: str) -> float:
        total = self.get_total_instances(target)
        affected = self.get_affected_instances(target, scope)
        return (affected / total) * 100 if total > 0 else 100

    async def emergency_stop(self) -> None:
        """Kill switch: immediately halt all chaos experiments."""
        await httpx.post(self.kill_switch_url, json={"action": "stop_all"})
```

## Common Chaos Experiments

```yaml
# Experiment catalog - start with these

level_1_basic:
  - name: "Kill a single pod"
    tool: "kubectl delete pod <name>"
    validates: "Pod auto-recovery, health checks"
    blast_radius: "1 pod"

  - name: "CPU stress on one node"
    tool: "stress-ng --cpu 4 --timeout 60"
    validates: "Autoscaling, request routing"
    blast_radius: "1 node"

  - name: "Inject 500ms network latency"
    tool: "tc qdisc add dev eth0 root netem delay 500ms"
    validates: "Timeout handling, circuit breakers"
    blast_radius: "1 container"

level_2_intermediate:
  - name: "Kill entire availability zone"
    tool: "Chaos Toolkit / AWS FIS"
    validates: "Multi-AZ failover, data replication"
    blast_radius: "1 AZ"

  - name: "DNS resolution failure"
    tool: "iptables -A OUTPUT -p udp --dport 53 -j DROP"
    validates: "DNS caching, fallback resolution"
    blast_radius: "1 service"

  - name: "Disk fill to 95%"
    tool: "fallocate -l 50G /tmp/disk_fill"
    validates: "Disk space alerts, log rotation"
    blast_radius: "1 node"

level_3_advanced:
  - name: "Split brain network partition"
    tool: "Toxiproxy / Linux iptables"
    validates: "Consensus protocols, data consistency"
    blast_radius: "Cluster segment"

  - name: "Clock skew injection"
    tool: "timedatectl set-time +5min"
    validates: "Certificate validation, token expiry"
    blast_radius: "1 node"
```

## Gameday Checklist

```markdown
## Pre-Gameday (1 week before)
- [ ] Define steady state hypothesis with measurable probes
- [ ] Identify blast radius and set hard limits
- [ ] Ensure kill switch is tested and accessible
- [ ] Notify on-call team and stakeholders
- [ ] Verify rollback procedures are documented and tested
- [ ] Set up monitoring dashboards for the experiment
- [ ] Run experiment in staging first

## During Gameday
- [ ] Verify steady state BEFORE injecting chaos
- [ ] Start with smallest blast radius, escalate gradually
- [ ] Monitor dashboards continuously during experiment
- [ ] Document observations in real-time (shared doc)
- [ ] If SLO violated: trigger kill switch immediately
- [ ] Time-box each experiment (max 5 minutes per injection)

## Post-Gameday
- [ ] Verify system returned to steady state
- [ ] Document findings: what broke, what recovered, what surprised
- [ ] Create action items for discovered weaknesses
- [ ] Update runbooks based on learnings
- [ ] Share results with broader engineering team
- [ ] Schedule fixes and re-test
```

## Checklist

- [ ] Define steady state hypothesis before every experiment
- [ ] Never run chaos in production without a tested kill switch
- [ ] Start in staging, graduate to production with reduced blast radius
- [ ] Exclude critical services (auth, payments) unless specifically targeting them
- [ ] Time-box experiments (max 5 minutes injection, 30 minutes observation)
- [ ] Run during low-traffic windows, never during peak
- [ ] Document every experiment: hypothesis, method, observations, findings
- [ ] Automate recurring experiments in CI/CD pipeline

## Anti-Patterns

- Chaos without hypothesis: random breaking is not engineering
- No kill switch: unable to stop experiment when things go wrong
- Running in production first: always validate in staging
- Affecting too many instances: never exceed 5% without explicit approval
- Chaos during incidents: only inject chaos on healthy systems
- Not fixing findings: experiments without follow-up action items are wasted
