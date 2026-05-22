---
name: Rollout and Kill Switch
description: Comprehensive guide to safe agent deployment strategies including canary releases, feature flags, kill switches, and automated rollback mechanisms
---

# Rollout and Kill Switch

## Why Controlled Rollouts?

**Problem:** Deploying agent changes to all users at once is risky

### Risks
```
Bug affects all users
Performance issues at scale
Unexpected behavior
No easy rollback
```

### Solution: Gradual Rollout
```
1% → Monitor → 10% → Monitor → 50% → Monitor → 100%

Issues detected early → Affect fewer users → Easy rollback
```

---

## Rollout Strategies

### Canary Deployment
```
Deploy new version to small % of users
Monitor metrics
If good, increase %
If bad, rollback

Timeline:
Day 1: 1% of users
Day 2: 5% of users
Day 3: 10% of users
Day 4: 25% of users
Day 5: 50% of users
Day 6: 100% of users
```

### Blue-Green Deployment
```
Blue: Current version (100% traffic)
Green: New version (0% traffic)

Test green → Switch traffic → Green becomes blue

Instant rollback: Switch back to blue
```

### Feature Flags
```
Deploy code to all users
Feature disabled by default
Enable for specific users/% of traffic
Monitor
Enable for all
```

---

## Implementation

### Feature Flags
```python
class FeatureFlags:
    def __init__(self):
        self.flags = {}
    
    def is_enabled(self, flag_name, user_id=None, default=False):
        flag = self.flags.get(flag_name, {})
        
        # Check if globally enabled
        if flag.get("enabled", default):
            return True
        
        # Check rollout percentage
        rollout_pct = flag.get("rollout_percentage", 0)
        if rollout_pct > 0:
            # Consistent hashing (same user always gets same result)
            if (hash(user_id) % 100) < rollout_pct:
                return True
        
        # Check user whitelist
        if user_id in flag.get("whitelist", []):
            return True
        
        return False

# Usage
flags = FeatureFlags()
flags.flags = {
    "new_agent_version": {
        "enabled": False,
        "rollout_percentage": 10,  # 10% of users
        "whitelist": ["user_123", "user_456"]  # Always enabled for these users
    }
}

if flags.is_enabled("new_agent_version", user_id="user_789"):
    # Use new agent version
    agent = AgentV2()
else:
    # Use old agent version
    agent = AgentV1()
```

### Database-Backed Feature Flags
```sql
CREATE TABLE feature_flags (
    name VARCHAR(255) PRIMARY KEY,
    enabled BOOLEAN DEFAULT FALSE,
    rollout_percentage INT DEFAULT 0,
    whitelist JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

```python
def is_feature_enabled(flag_name, user_id):
    flag = db.query_one("""
        SELECT enabled, rollout_percentage, whitelist
        FROM feature_flags
        WHERE name = %s
    """, (flag_name,))
    
    if not flag:
        return False
    
    if flag["enabled"]:
        return True
    
    if (hash(user_id) % 100) < flag["rollout_percentage"]:
        return True
    
    if user_id in flag["whitelist"]:
        return True
    
    return False
```

---

## Kill Switch

### Emergency Stop
```python
class KillSwitch:
    def __init__(self):
        self.killed = False
    
    def activate(self, reason):
        self.killed = True
        log_event(f"Kill switch activated: {reason}")
        send_alert(f"🚨 Kill switch activated: {reason}")
    
    def deactivate(self):
        self.killed = False
        log_event("Kill switch deactivated")
    
    def is_active(self):
        return self.killed

# Global kill switch
kill_switch = KillSwitch()

# In agent code
def run_agent(user_input):
    if kill_switch.is_active():
        return "Service temporarily unavailable. Please try again later."
    
    # Normal agent logic
    return agent.run(user_input)

# Activate kill switch
kill_switch.activate("High error rate detected")
```

### Database-Backed Kill Switch
```sql
CREATE TABLE kill_switches (
    name VARCHAR(255) PRIMARY KEY,
    active BOOLEAN DEFAULT FALSE,
    reason TEXT,
    activated_by VARCHAR(100),
    activated_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

```python
def is_kill_switch_active(name):
    result = db.query_one("""
        SELECT active FROM kill_switches WHERE name = %s
    """, (name,))
    
    return result["active"] if result else False

def activate_kill_switch(name, reason, activated_by):
    db.execute("""
        INSERT INTO kill_switches (name, active, reason, activated_by, activated_at)
        VALUES (%s, TRUE, %s, %s, NOW())
        ON CONFLICT (name) DO UPDATE
        SET active = TRUE, reason = %s, activated_by = %s, activated_at = NOW()
    """, (name, reason, activated_by, reason, activated_by))
    
    send_alert(f"🚨 Kill switch '{name}' activated: {reason}")
```

---

## Monitoring and Auto-Rollback

### Monitor Metrics
```python
def monitor_agent_metrics(version):
    # Get metrics for last hour
    metrics = db.query_one("""
        SELECT
            COUNT(*) as total_requests,
            SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
            AVG(latency_ms) as avg_latency,
            SUM(CASE WHEN error THEN 1 ELSE 0 END) as errors
        FROM agent_logs
        WHERE version = %s
          AND timestamp > NOW() - INTERVAL '1 hour'
    """, (version,))
    
    success_rate = metrics["successes"] / metrics["total_requests"]
    error_rate = metrics["errors"] / metrics["total_requests"]
    
    return {
        "success_rate": success_rate,
        "error_rate": error_rate,
        "avg_latency": metrics["avg_latency"]
    }
```

### Auto-Rollback on Failures
```python
def auto_rollback_check(current_version, previous_version):
    metrics = monitor_agent_metrics(current_version)
    
    # Thresholds
    if metrics["success_rate"] < 0.95:  # < 95% success
        rollback(current_version, previous_version, "Low success rate")
    
    if metrics["error_rate"] > 0.05:  # > 5% errors
        rollback(current_version, previous_version, "High error rate")
    
    if metrics["avg_latency"] > 5000:  # > 5 seconds
        rollback(current_version, previous_version, "High latency")

def rollback(from_version, to_version, reason):
    # Deactivate current version
    db.execute("""
        UPDATE feature_flags
        SET enabled = FALSE
        WHERE name = %s
    """, (f"agent_{from_version}",))
    
    # Activate previous version
    db.execute("""
        UPDATE feature_flags
        SET enabled = TRUE
        WHERE name = %s
    """, (f"agent_{to_version}",))
    
    log_event(f"Auto-rolled back from {from_version} to {to_version}: {reason}")
    send_alert(f"🔄 Auto-rollback: {from_version} → {to_version} ({reason})")
```

---

## Gradual Rollout Automation

### Increase Rollout Percentage
```python
def gradual_rollout(flag_name, target_percentage=100, step=10, interval_hours=24):
    """
    Gradually increase rollout percentage
    
    Args:
        flag_name: Feature flag name
        target_percentage: Final percentage (default 100%)
        step: Increase by this % each interval (default 10%)
        interval_hours: Hours between increases (default 24)
    """
    current_pct = get_rollout_percentage(flag_name)
    
    while current_pct < target_percentage:
        # Check metrics before increasing
        metrics = monitor_agent_metrics(flag_name)
        
        if metrics["success_rate"] < 0.95:
            send_alert(f"⚠️ Rollout paused: Low success rate ({metrics['success_rate']:.2%})")
            break
        
        # Increase percentage
        new_pct = min(current_pct + step, target_percentage)
        set_rollout_percentage(flag_name, new_pct)
        
        log_event(f"Increased {flag_name} rollout to {new_pct}%")
        
        # Wait before next increase
        time.sleep(interval_hours * 3600)
        current_pct = new_pct

# Usage
gradual_rollout("new_agent_version", target_percentage=100, step=10, interval_hours=24)
```

---

## Feature Flag Services

### LaunchDarkly
```python
import ldclient
from ldclient.config import Config

ldclient.set_config(Config("sdk-key-123"))
client = ldclient.get()

# Check flag
user = {"key": "user_123"}
show_new_feature = client.variation("new-agent-version", user, False)

if show_new_feature:
    agent = AgentV2()
else:
    agent = AgentV1()
```

### Split.io
```python
from splitio import get_factory

factory = get_factory("api-key-123")
client = factory.client()

# Check flag
treatment = client.get_treatment("user_123", "new-agent-version")

if treatment == "on":
    agent = AgentV2()
else:
    agent = AgentV1()
```

### Unleash (Open Source)
```python
from UnleashClient import UnleashClient

client = UnleashClient(
    url="http://unleash.example.com/api",
    app_name="my-agent",
    custom_headers={"Authorization": "..."}
)

client.initialize_client()

# Check flag
if client.is_enabled("new-agent-version", {"userId": "user_123"}):
    agent = AgentV2()
else:
    agent = AgentV1()
```

---

## Best Practices

### 1. Start Small (1-5%)
```python
# Good
set_rollout_percentage("new_feature", 1)  # Start with 1%

# Bad
set_rollout_percentage("new_feature", 50)  # Too aggressive
```

### 2. Monitor Closely
```python
# Monitor every 5 minutes during rollout
while rollout_in_progress:
    metrics = monitor_agent_metrics("new_version")
    
    if metrics["error_rate"] > threshold:
        rollback()
    
    time.sleep(300)  # 5 minutes
```

### 3. Have Rollback Plan
```python
# Always know how to rollback
rollback_plan = {
    "method": "Feature flag toggle",
    "steps": [
        "1. Set feature_flag.enabled = False",
        "2. Verify traffic switched to old version",
        "3. Monitor for 1 hour"
    ],
    "contact": "oncall@example.com"
}
```

### 4. Test Rollback
```python
# Regularly test rollback procedure
def test_rollback():
    # Enable new version
    enable_feature("new_version")
    assert is_feature_enabled("new_version")
    
    # Rollback
    disable_feature("new_version")
    assert not is_feature_enabled("new_version")
    
    # Verify old version works
    response = agent_v1.run("test input")
    assert response is not None
```

### 5. Communicate Changes
```python
# Notify team before rollout
send_notification(
    channel="#agent-ops",
    message=f"Starting rollout of new agent version to 10% of users. Monitoring dashboard: {dashboard_url}"
)
```

---

## Rollout Checklist

### Pre-Rollout
```
☐ Code reviewed and approved
☐ Tests passing (unit, integration, e2e)
☐ Monitoring dashboard ready
☐ Rollback plan documented
☐ Team notified
☐ Oncall engineer assigned
```

### During Rollout
```
☐ Start at 1-5%
☐ Monitor metrics every 5-15 minutes
☐ Check error logs
☐ Verify user feedback
☐ Gradually increase % (10%, 25%, 50%, 100%)
☐ Wait 24 hours between increases
```

### Post-Rollout
```
☐ Verify 100% rollout successful
☐ Monitor for 48 hours
☐ Remove feature flag (if permanent)
☐ Document lessons learned
☐ Update runbooks
```

---

## Summary

**Rollout Strategies:**
- Canary (gradual % increase)
- Blue-green (instant switch)
- Feature flags (selective enable)

**Kill Switch:**
- Emergency stop
- Database-backed
- Alert on activation

**Auto-Rollback:**
- Monitor metrics
- Rollback on failures
- Alert team

**Feature Flag Services:**
- LaunchDarkly
- Split.io
- Unleash (open source)

**Best Practices:**
- Start small (1-5%)
- Monitor closely
- Have rollback plan
- Test rollback
- Communicate changes

**Rollout Timeline:**
- Day 1: 1%
- Day 2: 5%
- Day 3: 10%
- Day 4: 25%
- Day 5: 50%
- Day 6: 100%
