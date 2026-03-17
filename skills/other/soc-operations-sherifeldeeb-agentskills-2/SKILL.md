---
name: soc-operations
description: |
  Security Operations Center workflows, alert triage, shift handovers, and
  operational reporting. Automate SOC documentation and standardize processes.
  Use for SOC-related tasks, alert management, and operational metrics.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - No external dependencies (standard library only)
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: cybersecurity
---

# SOC Operations Skill

Streamline Security Operations Center workflows with standardized alert triage, shift handover reports, and operational metrics tracking.

## Capabilities

- **Alert Triage**: Document and categorize security alerts with standardized disposition
- **Shift Handovers**: Generate structured handover reports for seamless transitions
- **Metrics Tracking**: Track SOC KPIs including MTTD, MTTR, and false positive rates
- **Triage Templates**: Pre-built templates for common alert types
- **IOC Documentation**: Track indicators of compromise during investigations

## Quick Start

```python
from soc_utils import AlertTriage, ShiftHandover, SOCMetrics

# Triage an alert
alert = AlertTriage('ALT-2024-001', 'SIEM', 'High')
alert.add_note('Initial analysis shows suspicious PowerShell execution', 'analyst1')
alert.add_ioc('hash', 'abc123...', 'Malicious script hash')
alert.set_disposition('true_positive', 'analyst1', 'Confirmed malware execution')

# Generate shift handover
handover = ShiftHandover('2024-01-15', 'day', 'John Smith')
handover.add_open_alert('ALT-2024-002', 'Medium', 'EDR', 'investigating')
handover.set_metrics(total_alerts=45, closed=42, false_positives=8)
print(handover.generate_report())
```

## Usage

### Alert Triage

Document security alert investigations with standardized workflow.

**Example**:
```python
from soc_utils import AlertTriage

# Create triage record
alert = AlertTriage(
    alert_id='ALT-2024-001',
    source='CrowdStrike',
    severity='High'
)

# Document investigation
alert.add_note('Alert triggered by suspicious process execution', 'analyst1')
alert.add_note('Process tree shows lateral movement attempt', 'analyst1')

# Add indicators
alert.add_ioc('ip', '192.168.1.100', 'Source of attack')
alert.add_ioc('hash', 'a1b2c3d4e5...', 'Malicious executable')
alert.add_ioc('domain', 'malware.evil.com', 'C2 domain')

# Set disposition
alert.set_disposition('true_positive', 'analyst1', 'Confirmed malware infection')

# Or escalate
alert.escalate(
    reason='Active ransomware infection detected',
    target='IR Team',
    analyst='analyst1'
)

# Export
print(alert.to_json())
```

### Shift Handover Reports

Generate comprehensive shift handover documentation.

**Example**:
```python
from soc_utils import ShiftHandover

# Create handover
handover = ShiftHandover(
    shift_date='2024-01-15',
    shift_type='day',
    analyst='John Smith'
)

# Add open alerts
handover.add_open_alert(
    alert_id='ALT-2024-002',
    severity='High',
    source='SIEM',
    status='investigating',
    notes='Pending memory analysis'
)

handover.add_open_alert(
    alert_id='ALT-2024-003',
    severity='Medium',
    source='EDR',
    status='awaiting response',
    notes='Waiting for user confirmation'
)

# Add escalations
handover.add_escalation(
    incident_id='INC-2024-001',
    summary='Ransomware infection on WORKSTATION-15',
    team='IR Team'
)

# Add notable events
handover.add_notable_event('New phishing campaign targeting finance department')
handover.add_notable_event('Scheduled maintenance on SIEM at 22:00')

# Add pending tasks
handover.add_pending_task('Follow up on ticket #12345')
handover.add_pending_task('Review updated detection rules')

# Set metrics
handover.set_metrics(total_alerts=45, closed=42, false_positives=8)

# Generate report
report = handover.generate_report()
print(report)
```

### SOC Metrics

Track and analyze SOC operational metrics.

**Example**:
```python
from soc_utils import SOCMetrics
from datetime import datetime, timedelta

metrics = SOCMetrics()

# Add historical alert data
metrics.add_alert_record({
    'alert_id': 'ALT-001',
    'severity': 'High',
    'occurred_at': datetime.now() - timedelta(hours=2),
    'detected_at': datetime.now() - timedelta(hours=1, minutes=45),
    'responded_at': datetime.now() - timedelta(hours=1, minutes=30),
    'disposition': 'true_positive'
})

metrics.add_alert_record({
    'alert_id': 'ALT-002',
    'severity': 'Medium',
    'occurred_at': datetime.now() - timedelta(hours=1),
    'detected_at': datetime.now() - timedelta(minutes=50),
    'responded_at': datetime.now() - timedelta(minutes=40),
    'disposition': 'false_positive'
})

# Calculate metrics
print(f"MTTD: {metrics.calculate_mttd():.1f} minutes")
print(f"MTTR: {metrics.calculate_mttr():.1f} minutes")
print(f"False Positive Rate: {metrics.get_false_positive_rate():.1f}%")
print(f"Alert Volume: {metrics.get_alert_volume()}")

# Generate full report
print(metrics.generate_report())
```

### Triage Templates

Use pre-built templates for common alert types.

**Example**:
```python
from soc_utils import generate_triage_template

# Get malware triage template
malware_template = generate_triage_template('malware')
print(malware_template)

# Get network alert template
network_template = generate_triage_template('network')
print(network_template)

# Get authentication alert template
auth_template = generate_triage_template('authentication')
print(auth_template)
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SOC_ANALYST_NAME` | Default analyst name | No | None |
| `SOC_TEAM_NAME` | SOC team identifier | No | `SOC` |

## Valid Values

### Dispositions
- `true_positive` - Confirmed malicious activity
- `false_positive` - Alert triggered incorrectly
- `benign` - Suspicious but authorized behavior
- `inconclusive` - Unable to determine

### Severities
- `Critical` - Immediate response required
- `High` - Urgent attention needed
- `Medium` - Standard priority
- `Low` - Low priority
- `Info` - Informational only

## Limitations

- **No SIEM Integration**: Manual data entry required
- **No Ticket System**: Does not create tickets automatically
- **Local Storage**: Data stored in memory only

## Troubleshooting

### Invalid Disposition Error

Ensure you use one of the valid disposition values:
```python
# Valid dispositions
alert.set_disposition('true_positive', 'analyst1')  # OK
alert.set_disposition('True Positive', 'analyst1')  # Error!
```

### Missing Timestamps

Metrics calculations require proper datetime objects:
```python
from datetime import datetime

# Correct
metrics.add_alert_record({
    'detected_at': datetime.now(),  # datetime object
    ...
})

# Incorrect
metrics.add_alert_record({
    'detected_at': '2024-01-15',  # string - won't work
    ...
})
```

## Related Skills

- [incident-response](../incident-response/): For escalated incidents
- [threat-intelligence](../threat-intelligence/): CTI integration
- [docx](../../baseline/docx/): Report generation

## References

- [Detailed API Reference](references/REFERENCE.md)
