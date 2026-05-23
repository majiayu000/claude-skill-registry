---
name: log-forensics
description: |
  Analyze system, application, and security logs for forensic investigation. Use when
  investigating security incidents, insider threats, system compromises, or any scenario
  requiring analysis of log data. Supports Windows Event Logs, Syslog, web server logs,
  and application-specific log formats.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: python-evtx, lxml, pandas
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Log Forensics

Comprehensive log forensics skill for analyzing various log sources to reconstruct events, detect anomalies, and identify indicators of compromise. Enables correlation across multiple log sources, timeline creation, and automated anomaly detection.

## Capabilities

- **Windows Event Log Analysis**: Parse and analyze EVTX files for security events
- **Syslog Analysis**: Parse Unix/Linux syslog and rsyslog formats
- **Web Server Log Analysis**: Analyze Apache, Nginx, IIS access and error logs
- **Application Log Analysis**: Parse application-specific log formats
- **Log Correlation**: Correlate events across multiple log sources
- **Timeline Generation**: Create chronological event timelines
- **Anomaly Detection**: Detect unusual patterns and outliers
- **Authentication Analysis**: Track login attempts, failures, and lateral movement
- **IOC Extraction**: Extract indicators of compromise from log entries
- **Statistical Analysis**: Perform statistical analysis on log patterns

## Quick Start

```python
from log_forensics import LogAnalyzer, EventLogParser, LogCorrelator

# Parse Windows Event Logs
parser = EventLogParser("/evidence/Security.evtx")
events = parser.parse_all()

# Analyze authentication events
auth_events = parser.get_authentication_events()

# Create log correlator
correlator = LogCorrelator()
correlator.add_source("windows", parser)
correlator.add_source("firewall", FirewallLogParser("/evidence/firewall.log"))
timeline = correlator.create_timeline()
```

## Usage

### Task 1: Windows Event Log Analysis
**Input**: Windows EVTX log files

**Process**:
1. Load and parse EVTX files
2. Filter by event IDs of interest
3. Extract relevant fields
4. Identify security-relevant events
5. Generate analysis report

**Output**: Parsed events with security analysis

**Example**:
```python
from log_forensics import EventLogParser

# Parse Security event log
parser = EventLogParser("/evidence/Security.evtx")

# Get all events
events = parser.parse_all()
print(f"Total events: {len(events)}")

# Filter by event ID (4624 = successful login)
logins = parser.filter_by_event_id([4624, 4625])
for login in logins:
    print(f"[{login.timestamp}] Event {login.event_id}")
    print(f"  User: {login.get_field('TargetUserName')}")
    print(f"  Domain: {login.get_field('TargetDomainName')}")
    print(f"  Logon Type: {login.get_field('LogonType')}")
    print(f"  Source IP: {login.get_field('IpAddress')}")

# Get authentication failures
failures = parser.get_failed_logins()
for f in failures:
    print(f"Failed login: {f.username} from {f.source_ip}")
    print(f"  Failure reason: {f.failure_reason}")

# Detect brute force attempts
brute_force = parser.detect_brute_force(
    threshold=10,
    time_window_minutes=5
)
for bf in brute_force:
    print(f"Brute force: {bf.target_account}")
    print(f"  Attempts: {bf.attempt_count}")
    print(f"  Source IPs: {bf.source_ips}")

# Get process creation events (4688)
processes = parser.get_process_creation_events()
for p in processes:
    print(f"Process: {p.process_name}")
    print(f"  Command line: {p.command_line}")
    print(f"  Parent: {p.parent_process}")

# Export to CSV
parser.export_csv("/evidence/security_events.csv")
```

### Task 2: Security Event Detection
**Input**: Windows Security Event Log

**Process**:
1. Identify security-relevant event IDs
2. Detect privilege escalation
3. Identify lateral movement
4. Detect persistence mechanisms
5. Flag suspicious activities

**Output**: Security findings with severity ratings

**Example**:
```python
from log_forensics import EventLogParser, SecurityDetector

parser = EventLogParser("/evidence/Security.evtx")
detector = SecurityDetector(parser)

# Detect privilege escalation
priv_esc = detector.detect_privilege_escalation()
for pe in priv_esc:
    print(f"PRIV ESC: {pe.technique}")
    print(f"  User: {pe.user}")
    print(f"  Timestamp: {pe.timestamp}")
    print(f"  Details: {pe.details}")

# Detect lateral movement
lateral = detector.detect_lateral_movement()
for lm in lateral:
    print(f"Lateral Movement: {lm.source} -> {lm.destination}")
    print(f"  Technique: {lm.technique}")
    print(f"  Account: {lm.account}")

# Detect account manipulation
account_changes = detector.detect_account_changes()
for ac in account_changes:
    print(f"Account Change: {ac.action}")
    print(f"  Target: {ac.target_account}")
    print(f"  By: {ac.actor}")

# Detect service installations
services = detector.detect_service_installations()
for s in services:
    print(f"Service Installed: {s.service_name}")
    print(f"  Path: {s.service_path}")
    print(f"  Account: {s.service_account}")

# Detect scheduled tasks
tasks = detector.detect_scheduled_tasks()

# Detect log clearing
cleared = detector.detect_log_clearing()
for c in cleared:
    print(f"LOG CLEARED: {c.log_name} at {c.timestamp}")
    print(f"  By: {c.actor}")

# Generate security report
detector.generate_report("/evidence/security_findings.html")
```

### Task 3: Syslog Analysis
**Input**: Unix/Linux syslog files

**Process**:
1. Parse syslog format
2. Categorize by facility and severity
3. Identify authentication events
4. Detect suspicious activities
5. Create timeline

**Output**: Parsed syslog with analysis

**Example**:
```python
from log_forensics import SyslogParser

# Parse syslog
parser = SyslogParser("/evidence/messages")

# Get all entries
entries = parser.parse_all()
print(f"Total entries: {len(entries)}")

# Filter by severity
errors = parser.filter_by_severity(["error", "crit", "alert", "emerg"])
for e in errors:
    print(f"[{e.timestamp}] {e.facility}.{e.severity}: {e.message}")

# Get authentication events
auth = parser.get_auth_events()
for a in auth:
    print(f"[{a.timestamp}] {a.event_type}: {a.user}")
    print(f"  Source: {a.source_ip}")
    print(f"  Success: {a.success}")

# Detect SSH brute force
ssh_attacks = parser.detect_ssh_brute_force()
for attack in ssh_attacks:
    print(f"SSH Attack from {attack.source_ip}")
    print(f"  Attempts: {attack.count}")
    print(f"  Users tried: {attack.users}")

# Analyze sudo usage
sudo = parser.get_sudo_events()
for s in sudo:
    print(f"Sudo: {s.user} -> {s.run_as}")
    print(f"  Command: {s.command}")
    print(f"  Allowed: {s.allowed}")

# Get cron job executions
cron = parser.get_cron_events()

# Export timeline
parser.export_timeline("/evidence/syslog_timeline.csv")
```

### Task 4: Web Server Log Analysis
**Input**: Apache/Nginx/IIS access logs

**Process**:
1. Parse access log format
2. Identify unique visitors
3. Detect attack patterns
4. Find suspicious requests
5. Generate access statistics

**Output**: Web access analysis with attack detection

**Example**:
```python
from log_forensics import WebLogParser

# Parse Apache access log
parser = WebLogParser(
    "/evidence/access.log",
    log_format="apache_combined"
)

# Get all requests
requests = parser.parse_all()
print(f"Total requests: {len(requests)}")

# Get unique visitors
visitors = parser.get_unique_visitors()
print(f"Unique IPs: {len(visitors)}")

# Find suspicious requests
suspicious = parser.find_suspicious_requests()
for s in suspicious:
    print(f"SUSPICIOUS: {s.request}")
    print(f"  IP: {s.client_ip}")
    print(f"  Reason: {s.detection_reason}")

# Detect SQL injection attempts
sqli = parser.detect_sql_injection()
for attack in sqli:
    print(f"SQLi: {attack.request}")
    print(f"  Parameter: {attack.parameter}")
    print(f"  IP: {attack.source_ip}")

# Detect path traversal
traversal = parser.detect_path_traversal()

# Detect web shells
webshells = parser.detect_webshell_access()
for ws in webshells:
    print(f"Webshell: {ws.path}")
    print(f"  IP: {ws.client_ip}")
    print(f"  Commands: {ws.detected_commands}")

# Get response code distribution
codes = parser.get_status_code_distribution()
print(f"200 OK: {codes.get(200, 0)}")
print(f"404 Not Found: {codes.get(404, 0)}")
print(f"500 Error: {codes.get(500, 0)}")

# Analyze by user agent
user_agents = parser.analyze_user_agents()
for ua in user_agents.suspicious:
    print(f"Suspicious UA: {ua.user_agent}")
    print(f"  Reason: {ua.reason}")

# Export to CSV
parser.export_csv("/evidence/web_access.csv")
```

### Task 5: Log Correlation
**Input**: Multiple log sources

**Process**:
1. Normalize log formats
2. Align timestamps
3. Correlate related events
4. Build unified timeline
5. Identify attack chains

**Output**: Correlated timeline with attack sequences

**Example**:
```python
from log_forensics import LogCorrelator, EventLogParser, SyslogParser, WebLogParser

# Initialize correlator
correlator = LogCorrelator()

# Add log sources
correlator.add_source(
    "windows",
    EventLogParser("/evidence/Security.evtx")
)
correlator.add_source(
    "linux",
    SyslogParser("/evidence/auth.log")
)
correlator.add_source(
    "webserver",
    WebLogParser("/evidence/access.log")
)

# Normalize timestamps to UTC
correlator.normalize_timestamps(timezone="UTC")

# Create unified timeline
timeline = correlator.create_timeline()
for event in timeline:
    print(f"[{event.timestamp}] {event.source}: {event.summary}")

# Correlate by IP address
ip_activity = correlator.correlate_by_ip("192.168.1.100")
print(f"Activity from 192.168.1.100:")
for event in ip_activity:
    print(f"  [{event.source}] {event.summary}")

# Correlate by username
user_activity = correlator.correlate_by_user("admin")

# Detect attack chains
chains = correlator.detect_attack_chains()
for chain in chains:
    print(f"Attack Chain: {chain.name}")
    print(f"  Confidence: {chain.confidence}")
    print(f"  Events: {len(chain.events)}")
    for event in chain.events:
        print(f"    - {event.timestamp}: {event.summary}")

# Find temporal correlations
correlations = correlator.find_temporal_correlations(
    time_window_seconds=60
)

# Export correlated timeline
correlator.export_timeline("/evidence/correlated_timeline.csv")
correlator.export_timeline_html("/evidence/timeline.html")
```

### Task 6: Authentication Analysis
**Input**: Log files containing authentication events

**Process**:
1. Extract all authentication events
2. Analyze login patterns
3. Detect anomalous logins
4. Identify credential attacks
5. Track session activity

**Output**: Authentication analysis report

**Example**:
```python
from log_forensics import AuthenticationAnalyzer

# Initialize with multiple sources
analyzer = AuthenticationAnalyzer()
analyzer.add_windows_logs("/evidence/Security.evtx")
analyzer.add_linux_logs("/evidence/auth.log")
analyzer.add_vpn_logs("/evidence/vpn.log")

# Get all authentication events
auth_events = analyzer.get_all_events()

# Analyze login patterns per user
patterns = analyzer.analyze_user_patterns("john.doe")
print(f"User: john.doe")
print(f"  Usual login times: {patterns.usual_hours}")
print(f"  Usual locations: {patterns.usual_locations}")
print(f"  Failed attempts: {patterns.failed_count}")

# Detect anomalous logins
anomalies = analyzer.detect_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.user} at {a.timestamp}")
    print(f"  Reason: {a.reason}")
    print(f"  Details: {a.details}")

# Detect impossible travel
travel = analyzer.detect_impossible_travel()
for t in travel:
    print(f"Impossible Travel: {t.user}")
    print(f"  Location 1: {t.location1} at {t.time1}")
    print(f"  Location 2: {t.location2} at {t.time2}")
    print(f"  Distance: {t.distance_km}km in {t.time_diff_minutes}min")

# Detect credential stuffing
stuffing = analyzer.detect_credential_stuffing()

# Get failed login summary
failed = analyzer.get_failed_login_summary()
print(f"Total failed logins: {failed.total}")
print(f"Top targeted accounts: {failed.top_accounts}")
print(f"Top source IPs: {failed.top_sources}")

# Generate authentication report
analyzer.generate_report("/evidence/auth_analysis.html")
```

### Task 7: PowerShell and Command Line Analysis
**Input**: Windows Event Logs with PowerShell/command logging

**Process**:
1. Extract PowerShell events (4103, 4104)
2. Decode encoded commands
3. Detect malicious patterns
4. Identify obfuscation techniques
5. Extract IOCs from commands

**Output**: Command analysis with threat indicators

**Example**:
```python
from log_forensics import PowerShellAnalyzer

# Parse PowerShell logs
analyzer = PowerShellAnalyzer()
analyzer.add_event_log("/evidence/Microsoft-Windows-PowerShell%4Operational.evtx")
analyzer.add_event_log("/evidence/Security.evtx")

# Get all PowerShell events
events = analyzer.get_all_events()

# Decode encoded commands
decoded = analyzer.decode_encoded_commands()
for d in decoded:
    print(f"Encoded command at {d.timestamp}:")
    print(f"  Original: {d.encoded[:50]}...")
    print(f"  Decoded: {d.decoded}")

# Detect malicious patterns
malicious = analyzer.detect_malicious_patterns()
for m in malicious:
    print(f"MALICIOUS: {m.pattern}")
    print(f"  Command: {m.command}")
    print(f"  Technique: {m.mitre_technique}")

# Detect download cradles
cradles = analyzer.detect_download_cradles()
for c in cradles:
    print(f"Download Cradle: {c.type}")
    print(f"  URL: {c.url}")
    print(f"  Command: {c.command}")

# Detect obfuscation
obfuscated = analyzer.detect_obfuscation()
for o in obfuscated:
    print(f"Obfuscation: {o.technique}")
    print(f"  Score: {o.obfuscation_score}")

# Extract IOCs from commands
iocs = analyzer.extract_iocs()
print(f"URLs found: {len(iocs.urls)}")
print(f"IPs found: {len(iocs.ips)}")
print(f"Domains found: {len(iocs.domains)}")
print(f"File paths: {len(iocs.file_paths)}")

# Generate report
analyzer.generate_report("/evidence/powershell_analysis.html")
```

### Task 8: Firewall and Network Log Analysis
**Input**: Firewall logs (various formats)

**Process**:
1. Parse firewall log format
2. Analyze allowed/denied traffic
3. Detect port scans
4. Identify suspicious patterns
5. Generate traffic statistics

**Output**: Firewall log analysis

**Example**:
```python
from log_forensics import FirewallLogParser

# Parse firewall logs
parser = FirewallLogParser(
    "/evidence/firewall.log",
    format="pfsense"  # or "iptables", "windows_firewall", "cisco_asa"
)

# Get all events
events = parser.parse_all()

# Get denied traffic
denied = parser.get_denied_traffic()
for d in denied:
    print(f"DENIED: {d.src_ip}:{d.src_port} -> {d.dst_ip}:{d.dst_port}")
    print(f"  Protocol: {d.protocol}")
    print(f"  Rule: {d.rule_name}")

# Detect port scans
scans = parser.detect_port_scans()
for s in scans:
    print(f"Port Scan: {s.source_ip}")
    print(f"  Target: {s.target_ip}")
    print(f"  Ports: {s.ports_scanned}")
    print(f"  Type: {s.scan_type}")

# Detect potential C2
c2_indicators = parser.detect_c2_indicators()
for c2 in c2_indicators:
    print(f"C2 Indicator: {c2.internal_ip} -> {c2.external_ip}")
    print(f"  Pattern: {c2.pattern}")

# Get traffic summary
summary = parser.get_traffic_summary()
print(f"Total connections: {summary.total}")
print(f"Allowed: {summary.allowed}")
print(f"Denied: {summary.denied}")
print(f"Top talkers: {summary.top_sources}")

# Analyze by destination port
port_analysis = parser.analyze_by_port()
for port, stats in port_analysis.items():
    print(f"Port {port}: {stats.connection_count} connections")

# Export analysis
parser.export_csv("/evidence/firewall_events.csv")
```

### Task 9: Cloud Service Log Analysis
**Input**: Cloud platform logs (AWS, Azure, GCP)

**Process**:
1. Parse cloud log format
2. Identify management events
3. Detect suspicious API calls
4. Analyze IAM activities
5. Check for data access

**Output**: Cloud activity analysis

**Example**:
```python
from log_forensics import CloudLogAnalyzer

# AWS CloudTrail analysis
aws_analyzer = CloudLogAnalyzer(
    "/evidence/cloudtrail/",
    platform="aws"
)

# Get all events
events = aws_analyzer.parse_all()

# Get IAM events
iam_events = aws_analyzer.get_iam_events()
for e in iam_events:
    print(f"[{e.timestamp}] {e.event_name}")
    print(f"  User: {e.user_identity}")
    print(f"  Source IP: {e.source_ip}")

# Detect suspicious activities
suspicious = aws_analyzer.detect_suspicious_activities()
for s in suspicious:
    print(f"SUSPICIOUS: {s.event_name}")
    print(f"  Reason: {s.reason}")
    print(f"  Risk: {s.risk_level}")

# Detect privilege escalation
priv_esc = aws_analyzer.detect_privilege_escalation()

# Detect data exfiltration indicators
exfil = aws_analyzer.detect_data_exfiltration()
for e in exfil:
    print(f"Potential Exfil: {e.resource}")
    print(f"  Action: {e.action}")
    print(f"  By: {e.user}")

# Analyze S3 access
s3_access = aws_analyzer.get_s3_access_events()
for access in s3_access:
    print(f"S3: {access.action} on {access.bucket}")
    print(f"  Object: {access.object_key}")
    print(f"  User: {access.user}")

# Generate cloud security report
aws_analyzer.generate_report("/evidence/cloud_analysis.html")
```

### Task 10: Log Anomaly Detection
**Input**: Any log source

**Process**:
1. Establish baseline patterns
2. Apply statistical analysis
3. Detect outliers
4. Identify unusual sequences
5. Flag anomalies

**Output**: Anomaly detection results

**Example**:
```python
from log_forensics import AnomalyDetector

# Initialize detector
detector = AnomalyDetector()

# Add log sources
detector.add_logs("/evidence/Security.evtx")
detector.add_logs("/evidence/access.log")
detector.add_logs("/evidence/auth.log")

# Build baseline (using first portion of logs)
detector.build_baseline(training_percentage=0.7)

# Detect volume anomalies
volume_anomalies = detector.detect_volume_anomalies()
for a in volume_anomalies:
    print(f"Volume Anomaly at {a.timestamp}")
    print(f"  Expected: {a.expected_count}")
    print(f"  Actual: {a.actual_count}")
    print(f"  Deviation: {a.deviation}x")

# Detect timing anomalies
timing_anomalies = detector.detect_timing_anomalies()
for a in timing_anomalies:
    print(f"Timing Anomaly: {a.description}")
    print(f"  Event: {a.event_type}")
    print(f"  Usual time: {a.usual_time}")
    print(f"  Occurred: {a.actual_time}")

# Detect sequence anomalies
sequence_anomalies = detector.detect_sequence_anomalies()
for a in sequence_anomalies:
    print(f"Unusual Sequence: {a.sequence}")
    print(f"  Probability: {a.probability}")

# Detect rare events
rare_events = detector.find_rare_events(threshold=0.01)
for e in rare_events:
    print(f"Rare Event: {e.event_type}")
    print(f"  Frequency: {e.frequency}")
    print(f"  Count: {e.count}")

# Generate anomaly report
detector.generate_report("/evidence/anomaly_report.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LOG_TIMEZONE` | Default timezone for log parsing | No | UTC |
| `EVTX_PARSER` | Path to EVTX parser binary | No | Built-in |
| `GEOIP_DB` | Path to GeoIP database | No | None |
| `YARA_RULES` | Path to YARA rules for log analysis | No | None |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `normalize_timestamps` | boolean | Normalize all timestamps to UTC |
| `parallel_parsing` | boolean | Enable parallel log parsing |
| `cache_parsed` | boolean | Cache parsed log entries |
| `max_memory_mb` | integer | Maximum memory for log processing |
| `chunk_size` | integer | Lines to process per chunk |

## Examples

### Example 1: Investigating Unauthorized Access
**Scenario**: Detecting and analyzing unauthorized system access

```python
from log_forensics import EventLogParser, AuthenticationAnalyzer

# Parse Security event log
parser = EventLogParser("/evidence/Security.evtx")

# Get failed login attempts
failed = parser.get_failed_logins()
print(f"Total failed logins: {len(failed)}")

# Group by target account
accounts = {}
for f in failed:
    if f.target_account not in accounts:
        accounts[f.target_account] = []
    accounts[f.target_account].append(f)

# Find accounts with many failures
for account, failures in accounts.items():
    if len(failures) > 10:
        print(f"Account: {account}")
        print(f"  Failures: {len(failures)}")
        unique_ips = set(f.source_ip for f in failures)
        print(f"  Source IPs: {unique_ips}")

# Check for successful logins after failures
auth_analyzer = AuthenticationAnalyzer()
auth_analyzer.add_parser(parser)
compromise_indicators = auth_analyzer.find_success_after_failure()
```

### Example 2: Insider Threat Investigation
**Scenario**: Analyzing logs for insider threat indicators

```python
from log_forensics import LogCorrelator, EventLogParser, FileAccessParser

# Combine multiple log sources
correlator = LogCorrelator()
correlator.add_source("security", EventLogParser("/evidence/Security.evtx"))
correlator.add_source("files", FileAccessParser("/evidence/file_audit.evtx"))

# Analyze specific user's activity
user = "john.smith"
user_timeline = correlator.get_user_activity(user)

# Look for data collection indicators
data_access = correlator.find_bulk_file_access(
    user=user,
    threshold=100,
    time_window_hours=1
)

# Check for off-hours activity
off_hours = correlator.find_off_hours_activity(
    user=user,
    business_hours=(9, 18),
    business_days=[0, 1, 2, 3, 4]  # Mon-Fri
)

# Generate insider threat report
correlator.generate_insider_report(user, "/evidence/insider_report.html")
```

## Limitations

- Large log files may require significant memory
- Some log formats may not be fully supported
- Timestamp parsing depends on consistent formats
- Anomaly detection requires sufficient baseline data
- Real-time analysis not supported
- Encrypted logs cannot be parsed
- Log rotation may cause gaps in analysis

## Troubleshooting

### Common Issue 1: EVTX Parsing Errors
**Problem**: Unable to parse Windows Event Log
**Solution**:
- Check file for corruption
- Ensure file is complete (not truncated)
- Try alternative parser

### Common Issue 2: Timestamp Misalignment
**Problem**: Events from different sources don't correlate
**Solution**:
- Verify source timezones
- Use normalize_timestamps option
- Check for clock skew

### Common Issue 3: Memory Exhaustion
**Problem**: Out of memory on large log files
**Solution**:
- Use streaming mode
- Process in chunks
- Increase max_memory_mb setting

## Related Skills

- [timeline-forensics](../timeline-forensics/): Super timeline creation
- [memory-forensics](../memory-forensics/): Correlate with memory analysis
- [network-forensics](../network-forensics/): Correlate with network captures
- [registry-forensics](../registry-forensics/): Windows registry analysis
- [incident-response](../../cybersecurity/incident-response/): IR workflow integration

## References

- [Log Forensics Reference](references/REFERENCE.md)
- [Windows Event ID Guide](references/WINDOWS_EVENT_IDS.md)
- [Log Format Specifications](references/LOG_FORMATS.md)
