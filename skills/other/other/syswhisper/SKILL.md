---
name: syswhisper
description: "Server health monitoring with plain language Telegram alerts. Tracks CPU, memory, disk, uptime, and custom metrics. Use when: running servers/VPS instances, monitoring app health, or need simple alerting. NOT for: enterprise-scale monitoring, complex distributed systems, or regulatory compliance logging."
homepage: https://pawhub.ai/syswhisper
metadata:
  {
    "openpaw":
      {
        "emoji": "🔔",
        "requires": { "bins": ["ssh"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/syswhisper",
              "bins": ["syswhisper"],
              "label": "Install SysWhisper (npm)",
            },
          ],
      },
  }
---

# SysWhisper 🔔

Your servers text you when something's wrong. Plain English alerts, no cryptic error codes. Know about issues before your users do.

## When to Use

✅ **USE when:**

- Running VPS/cloud instances
- Monitoring web app health
- Tracking resource usage
- Getting alerts for outages
- Simple uptime monitoring
- Disk space warnings
- Process monitoring

## When NOT to Use

❌ **DON'T use when:**

- Enterprise monitoring → use Datadog, New Relic
- Kubernetes clusters → use Prometheus
- Compliance logging → use dedicated tools
- APM tracing → use dedicated APM

## Example Interactions

**You:** Monitor my server at 192.168.1.100

**Paw:** *connects via SSH*

✅ **Server added:** 192.168.1.100

**Current status:**
- CPU: 12% (idle)
- Memory: 2.1GB / 8GB (26%)
- Disk: 47GB / 100GB (47%)
- Uptime: 23 days

**What to monitor?**
1. High CPU (alert if >80%)
2. Low memory (alert if <500MB free)
3. Disk space (alert if <10GB free)
4. Uptime (alert if server restarts)

Or I can set smart defaults. Your call. 🎯

---

**You:** Smart defaults

**Paw:** ✅ **Monitoring active**

**Alerts configured:**
- 🔥 CPU >85% for 5 minutes
- 💾 Memory <500MB free
- 💿 Disk <10GB free
- 🔄 Server restart detected
- ⏰ No heartbeat for 10 minutes

I'll check every 60 seconds. You'll get Telegram pings if anything breaks.

Sleep well. 😴

---

**3 AM alert:**

**Paw:** 🚨 **Server Alert: 192.168.1.100**

**Issue:** High CPU usage
**Current:** 94% (sustained for 8 minutes)
**Status:** Critical

**Top processes:**
1. node (PID 1234) — 87% CPU
2. postgres (PID 5678) — 6% CPU

**Actions:**
- `/sys kill 1234` (kill node process)
- `/sys restart node-app` (restart service)
- `/sys ssh` (get SSH command)

What do you want to do? 🔧

---

**You:** `/sys restart node-app`

**Paw:** Restarting `node-app` on 192.168.1.100...

✅ **Service restarted**
- Old PID: 1234 (killed)
- New PID: 9876 (running)
- CPU: 12% (back to normal)

**Status:** Resolved ✅

I'll keep watching. Go back to sleep. 😴

## Commands

```bash
# Add server
syswhisper add 192.168.1.100 --name "web-server"

# Configure alerts
syswhisper alert cpu --threshold 85 --duration 5m

# Show server status
syswhisper status

# View alert history
syswhisper alerts history

# Test alert
syswhisper alerts test
```

## Telegram Integration

**Quick status:**

**You:** `/sys status`

**Paw:** **All servers:** 3 online

✅ web-server — healthy
✅ db-server — healthy
⚠️ worker-1 — high memory (85%)

React to worker-1 for details.

## Pricing

- **Free tier:** 1 server, basic alerts
- **Pro:** $8/month — 10 servers, custom alerts

Install: [pawhub.ai/syswhisper](https://pawhub.ai/syswhisper)

---

Sleep soundly. Paw's watching your servers. 🔔🐾
