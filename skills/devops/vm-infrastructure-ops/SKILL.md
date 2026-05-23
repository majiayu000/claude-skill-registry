---
name: vm-infrastructure-ops
description: Troubleshoot and manage GCP e2-micro VM running eth-realtime-collector. Use when VM service is down, systemd failures occur, real-time data stream stops, or VM network issues arise. Keywords systemd, journalctl, eth-collector, gcloud compute.
---

# VM Infrastructure Operations

**Version**: 1.0.0
**Last Updated**: 2025-11-13
**Purpose**: Troubleshoot and manage GCP e2-micro VM running eth-realtime-collector

## When to Use

Use this skill when:

- VM service down, "eth-collector" systemd failures
- Real-time data stream stopped (ClickHouse not receiving blocks)
- VM network issues, DNS resolution failures
- Need to check service status, view logs, or restart services
- Keywords: systemd, journalctl, eth-collector, gcloud compute

## Prerequisites

- GCP project access: `eonlabs-ethereum-bq`
- VM instance: `eth-realtime-collector` in zone `us-east1-b`
- gcloud CLI configured with appropriate credentials

## Workflows

### 1. Check Service Status

Check if eth-collector systemd service is running:

```bash
gcloud compute ssh eth-realtime-collector --zone=us-east1-b \
  --command='sudo systemctl status eth-collector'
```

**Expected Output** (healthy):
```
● eth-collector.service - Ethereum Real-Time Collector
   Loaded: loaded (/etc/systemd/system/eth-collector.service; enabled)
   Active: active (running) since ...
```

**Alternative** (use provided script):
```bash
.claude/skills/vm-infrastructure-ops/scripts/check_vm_status.sh
```

### 2. View Logs (Live Tail)

Stream real-time logs from the collector service:

```bash
gcloud compute ssh eth-realtime-collector --zone=us-east1-b \
  --command='sudo journalctl -u eth-collector -f'
```

**What to Look For**:
- "Block inserted" messages every ~12 seconds (healthy)
- gRPC errors, DNS resolution failures (unhealthy)
- "Connection refused" or "Metadata server unreachable" (network issues)

### 3. View Recent Logs (Last 100 Lines)

```bash
gcloud compute ssh eth-realtime-collector --zone=us-east1-b \
  --command='sudo journalctl -u eth-collector -n 100'
```

### 4. Restart Service

Restart the collector service after configuration changes or to recover from errors:

```bash
gcloud compute ssh eth-realtime-collector --zone=us-east1-b \
  --command='sudo systemctl restart eth-collector'
```

**Alternative** (use provided script with pre-checks):
```bash
.claude/skills/vm-infrastructure-ops/scripts/restart_collector.sh
```

**When to Use**:
- After deploying code updates
- Recovering from gRPC metadata validation errors
- After Secret Manager credential updates

### 5. VM Hard Reset

Hard reset the VM instance (use as last resort):

```bash
gcloud compute instances reset eth-realtime-collector --zone=us-east1-b
```

**When to Use**:
- VM network connectivity completely lost
- DNS resolution failures
- Metadata server unreachable
- Service restart doesn't resolve issues

**Warning**: This forcefully restarts the VM. All in-memory state is lost.

### 6. Verify Data Flow

After restarting services, verify data is flowing to ClickHouse:

```bash
cd 
doppler run --project aws-credentials --config prd -- python3 -c "
import clickhouse_connect
import os
client = clickhouse_connect.get_client(
    host=os.environ['CLICKHOUSE_HOST'],
    port=8443,
    username='default',
    password=os.environ['CLICKHOUSE_PASSWORD'],
    secure=True
)
result = client.query('SELECT MAX(timestamp), MAX(number) FROM ethereum_mainnet.blocks FINAL')
print(f'Latest block: {result.result_rows[0][1]:,} at {result.result_rows[0][0]}')
"
```

**Expected Output** (healthy):
```
Latest block: 23,800,000+ at <within last 60 seconds>
```

## Common Failure Modes

See [VM Failure Modes](/.claude/skills/vm-infrastructure-ops/references/vm-failure-modes.md) for detailed troubleshooting guide.

**Quick Reference**:

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Service status: `failed` | gRPC metadata error | Check logs, restart with `.strip()` fix |
| No blocks for >5 minutes | Network connectivity | Check network, reset VM if needed |
| DNS resolution errors | Metadata server unreachable | VM hard reset |
| "Connection refused" | Service not running | Restart service |

## Systemd Commands

See [Systemd Commands Reference](/.claude/skills/vm-infrastructure-ops/references/systemd-commands.md) for complete systemd operations.

**Quick Reference**:

```bash
# Status
sudo systemctl status eth-collector

# Start
sudo systemctl start eth-collector

# Stop
sudo systemctl stop eth-collector

# Restart
sudo systemctl restart eth-collector

# Enable (start on boot)
sudo systemctl enable eth-collector

# Disable (don't start on boot)
sudo systemctl disable eth-collector

# View service logs
sudo journalctl -u eth-collector

# Follow logs live
sudo journalctl -u eth-collector -f
```

## Operational History

**Infrastructure Recovery** (2025-11-10 07:00 UTC):
- VM network failure detected (DNS resolution failed, metadata server unreachable)
- Recovery: VM reset restored network connectivity
- eth-collector service restarted with `.strip()` fix (gRPC metadata validation resolved)
- Real-time data flow confirmed: blocks streaming every ~12 seconds
- Database verified: 23.8M blocks (2015-2025), latest block within seconds

**Maintainability SLO Achievement**: Critical infrastructure failure (VM network down) resolved in <30 minutes (VM reset + service restart + verification).

## Related Documentation

- [ClickHouse Migration ADR](/docs/architecture/decisions/2025-11-25-motherduck-clickhouse-migration.md) - Production database migration
- [Real-Time Collector Deployment Guide](/docs/deployment/realtime-collector.md) - VM deployment
- [Gap Monitor README](/deployment/gcp-functions/gap-monitor/README.md) - Automated gap detection
- [Data Pipeline Monitoring Skill](/.claude/skills/data-pipeline-monitoring/SKILL.md) - Cloud Run Jobs monitoring

## Scripts

- [`check_vm_status.sh`](/.claude/skills/vm-infrastructure-ops/scripts/check_vm_status.sh) - Automated status check via gcloud
- [`restart_collector.sh`](/.claude/skills/vm-infrastructure-ops/scripts/restart_collector.sh) - Safe restart with pre-checks

## References

- [`vm-failure-modes.md`](/.claude/skills/vm-infrastructure-ops/references/vm-failure-modes.md) - Common failure scenarios and solutions
- [`systemd-commands.md`](/.claude/skills/vm-infrastructure-ops/references/systemd-commands.md) - Complete systemd operations reference
