---
name: artifact-collection
description: |
  Collect and preserve digital forensic artifacts from systems and devices. Use when
  responding to incidents, collecting evidence for investigation, or preserving
  volatile data. Supports Windows, Linux, macOS artifact collection with chain of custody.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: volatility3, psutil, wmi
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Artifact Collection

Comprehensive artifact collection skill for gathering and preserving digital forensic evidence. Enables systematic collection of volatile and non-volatile artifacts from endpoints, maintaining chain of custody, and ensuring forensic integrity throughout the collection process.

## Capabilities

- **Volatile Data Collection**: Capture RAM, running processes, network connections
- **Disk Artifact Collection**: Collect registry, event logs, browser data
- **Log Collection**: Gather system, application, and security logs
- **Configuration Collection**: Capture system configuration and state
- **Evidence Packaging**: Package artifacts with integrity verification
- **Chain of Custody**: Document and maintain evidence chain of custody
- **Remote Collection**: Collect artifacts from remote systems
- **Triage Collection**: Quick artifact collection for rapid response
- **Selective Collection**: Target specific artifact types
- **Collection Verification**: Verify collected artifact integrity

## Quick Start

```python
from artifact_collection import ArtifactCollector, WindowsCollector, ChainOfCustody

# Initialize collector
collector = WindowsCollector(output_dir="/evidence/case001/")

# Collect volatile artifacts
collector.collect_volatile()

# Collect disk artifacts
collector.collect_disk_artifacts()

# Generate chain of custody
coc = ChainOfCustody(collector)
coc.generate_report("/evidence/case001/chain_of_custody.pdf")
```

## Usage

### Task 1: Volatile Data Collection
**Input**: Target system (local or remote)

**Process**:
1. Document system state
2. Capture memory dump
3. Collect running processes
4. Capture network connections
5. Preserve volatile artifacts

**Output**: Volatile artifacts with documentation

**Example**:
```python
from artifact_collection import VolatileCollector

# Initialize collector
collector = VolatileCollector(
    output_dir="/evidence/case001/volatile/",
    case_id="CASE-2024-001",
    examiner="John Doe"
)

# Collect memory dump
memory = collector.collect_memory()
print(f"Memory dump: {memory.path}")
print(f"Size: {memory.size_gb}GB")
print(f"Hash: {memory.sha256}")
print(f"Tool: {memory.acquisition_tool}")

# Collect running processes
processes = collector.collect_processes()
for proc in processes:
    print(f"PID {proc.pid}: {proc.name}")
    print(f"  Path: {proc.exe_path}")
    print(f"  User: {proc.username}")
    print(f"  Command: {proc.command_line}")
    print(f"  Start: {proc.start_time}")

# Collect network connections
connections = collector.collect_network_connections()
for conn in connections:
    print(f"{conn.local_addr}:{conn.local_port} -> "
          f"{conn.remote_addr}:{conn.remote_port}")
    print(f"  PID: {conn.pid}")
    print(f"  State: {conn.state}")
    print(f"  Protocol: {conn.protocol}")

# Collect network interfaces
interfaces = collector.collect_network_interfaces()
for iface in interfaces:
    print(f"Interface: {iface.name}")
    print(f"  IP: {iface.ip_address}")
    print(f"  MAC: {iface.mac_address}")

# Collect DNS cache
dns_cache = collector.collect_dns_cache()

# Collect ARP cache
arp_cache = collector.collect_arp_cache()

# Collect clipboard
clipboard = collector.collect_clipboard()

# Collect environment variables
env_vars = collector.collect_environment_variables()

# Generate collection report
collector.generate_report("/evidence/case001/volatile_report.html")
```

### Task 2: Windows Artifact Collection
**Input**: Windows system

**Process**:
1. Collect registry hives
2. Collect event logs
3. Collect prefetch files
4. Collect browser artifacts
5. Package with hashes

**Output**: Windows artifacts with documentation

**Example**:
```python
from artifact_collection import WindowsCollector

# Initialize Windows collector
collector = WindowsCollector(
    output_dir="/evidence/case001/windows/",
    case_id="CASE-2024-001"
)

# Collect registry hives
registry = collector.collect_registry()
for hive in registry:
    print(f"Registry: {hive.name}")
    print(f"  Path: {hive.source_path}")
    print(f"  Hash: {hive.sha256}")

# Collect event logs
event_logs = collector.collect_event_logs()
for log in event_logs:
    print(f"Event Log: {log.name}")
    print(f"  Records: {log.record_count}")
    print(f"  Hash: {log.sha256}")

# Collect prefetch files
prefetch = collector.collect_prefetch()
print(f"Prefetch files: {len(prefetch)}")

# Collect Amcache
amcache = collector.collect_amcache()

# Collect SRUM database
srum = collector.collect_srum()

# Collect scheduled tasks
tasks = collector.collect_scheduled_tasks()

# Collect services
services = collector.collect_services()

# Collect startup items
startup = collector.collect_startup_items()

# Collect browser data
browsers = collector.collect_browser_artifacts()
for browser in browsers:
    print(f"Browser: {browser.name}")
    print(f"  History: {browser.history_count}")
    print(f"  Downloads: {browser.download_count}")

# Collect USB history
usb = collector.collect_usb_history()

# Collect recent files
recent = collector.collect_recent_files()

# Collect Jump Lists
jumplists = collector.collect_jumplists()

# Generate collection manifest
collector.generate_manifest("/evidence/case001/windows_manifest.json")
```

### Task 3: Linux Artifact Collection
**Input**: Linux system

**Process**:
1. Collect system logs
2. Collect user artifacts
3. Collect configuration files
4. Collect authentication data
5. Package artifacts

**Output**: Linux artifacts with documentation

**Example**:
```python
from artifact_collection import LinuxCollector

# Initialize Linux collector
collector = LinuxCollector(
    output_dir="/evidence/case001/linux/",
    case_id="CASE-2024-001"
)

# Collect system logs
logs = collector.collect_system_logs()
for log in logs:
    print(f"Log: {log.name}")
    print(f"  Path: {log.path}")
    print(f"  Size: {log.size}")

# Collect auth logs
auth = collector.collect_auth_logs()

# Collect user home directories
homes = collector.collect_user_homes()
for home in homes:
    print(f"User: {home.username}")
    print(f"  Bash history: {home.bash_history}")
    print(f"  SSH keys: {home.ssh_keys}")

# Collect cron jobs
cron = collector.collect_cron_jobs()
for job in cron:
    print(f"Cron: {job.user} - {job.schedule}")
    print(f"  Command: {job.command}")

# Collect systemd units
systemd = collector.collect_systemd_units()

# Collect network configuration
network = collector.collect_network_config()

# Collect installed packages
packages = collector.collect_installed_packages()

# Collect SSH configuration
ssh = collector.collect_ssh_config()

# Collect web server logs (if present)
web_logs = collector.collect_web_logs()

# Collect Docker artifacts (if present)
docker = collector.collect_docker_artifacts()

# Generate collection report
collector.generate_report("/evidence/case001/linux_report.html")
```

### Task 4: macOS Artifact Collection
**Input**: macOS system

**Process**:
1. Collect system logs
2. Collect user data
3. Collect application artifacts
4. Collect security data
5. Package artifacts

**Output**: macOS artifacts with documentation

**Example**:
```python
from artifact_collection import MacOSCollector

# Initialize macOS collector
collector = MacOSCollector(
    output_dir="/evidence/case001/macos/",
    case_id="CASE-2024-001"
)

# Collect unified logs
unified = collector.collect_unified_logs()

# Collect FSEvents
fsevents = collector.collect_fsevents()

# Collect user artifacts
users = collector.collect_user_artifacts()
for user in users:
    print(f"User: {user.username}")
    print(f"  Recent items: {len(user.recent_items)}")
    print(f"  Downloads: {len(user.downloads)}")

# Collect Spotlight data
spotlight = collector.collect_spotlight()

# Collect Keychain data (metadata only)
keychain = collector.collect_keychain_metadata()

# Collect LaunchAgents/Daemons
launch_items = collector.collect_launch_items()
for item in launch_items:
    print(f"Launch item: {item.name}")
    print(f"  Path: {item.path}")
    print(f"  Program: {item.program}")

# Collect quarantine events
quarantine = collector.collect_quarantine_events()
for q in quarantine:
    print(f"Quarantine: {q.filename}")
    print(f"  URL: {q.origin_url}")
    print(f"  Date: {q.quarantine_date}")

# Collect Safari data
safari = collector.collect_safari_artifacts()

# Collect Terminal history
terminal = collector.collect_terminal_history()

# Collect installed applications
apps = collector.collect_installed_apps()

# Generate report
collector.generate_report("/evidence/case001/macos_report.html")
```

### Task 5: Remote Artifact Collection
**Input**: Remote system credentials

**Process**:
1. Establish secure connection
2. Deploy collection agent
3. Collect artifacts remotely
4. Transfer with integrity check
5. Document collection

**Output**: Remote artifacts with verification

**Example**:
```python
from artifact_collection import RemoteCollector

# Initialize remote collector
collector = RemoteCollector(
    target="192.168.1.100",
    credentials={
        "username": "admin",
        "method": "key",
        "key_path": "/path/to/key"
    },
    output_dir="/evidence/case001/remote/"
)

# Connect to remote system
connection = collector.connect()
print(f"Connected: {connection.hostname}")
print(f"OS: {connection.os_type}")

# Collect volatile data first
volatile = collector.collect_volatile()
print(f"Memory collected: {volatile.memory_path}")
print(f"Processes: {len(volatile.processes)}")

# Collect disk artifacts
disk = collector.collect_disk_artifacts(
    artifact_types=["registry", "eventlogs", "browser"]
)

# Transfer artifacts securely
transfer = collector.transfer_artifacts()
for artifact in transfer:
    print(f"Transferred: {artifact.name}")
    print(f"  Size: {artifact.size}")
    print(f"  Local hash: {artifact.local_hash}")
    print(f"  Remote hash: {artifact.remote_hash}")
    print(f"  Verified: {artifact.verified}")

# Disconnect
collector.disconnect()

# Generate collection report
collector.generate_report("/evidence/case001/remote_report.html")
```

### Task 6: Triage Collection
**Input**: System requiring rapid assessment

**Process**:
1. Quick system inventory
2. Collect critical artifacts
3. Identify IOCs
4. Prioritize findings
5. Generate triage report

**Output**: Triage results with priorities

**Example**:
```python
from artifact_collection import TriageCollector

# Initialize triage collector
collector = TriageCollector(
    output_dir="/evidence/triage/",
    case_id="TRIAGE-001"
)

# Run quick triage
triage = collector.run_triage()

print(f"System: {triage.system_info.hostname}")
print(f"OS: {triage.system_info.os_version}")
print(f"Collection time: {triage.duration_seconds}s")

# Get alerts
for alert in triage.alerts:
    print(f"ALERT: {alert.severity} - {alert.description}")
    print(f"  Evidence: {alert.evidence}")

# Get quick IOCs
for ioc in triage.iocs:
    print(f"IOC: {ioc.type} - {ioc.value}")
    print(f"  Source: {ioc.source}")

# Get suspicious processes
for proc in triage.suspicious_processes:
    print(f"Suspicious: {proc.name} (PID {proc.pid})")
    print(f"  Reason: {proc.reason}")

# Get suspicious connections
for conn in triage.suspicious_connections:
    print(f"Connection: {conn.remote_addr}:{conn.remote_port}")
    print(f"  Process: {conn.process_name}")
    print(f"  Reason: {conn.reason}")

# Get persistence mechanisms
for persist in triage.persistence:
    print(f"Persistence: {persist.type}")
    print(f"  Path: {persist.path}")
    print(f"  Suspicious: {persist.is_suspicious}")

# Generate triage report
collector.generate_triage_report("/evidence/triage/triage_report.html")
```

### Task 7: Chain of Custody Management
**Input**: Collected artifacts

**Process**:
1. Document evidence items
2. Record handling events
3. Verify integrity
4. Generate custody log
5. Produce legal documentation

**Output**: Chain of custody documentation

**Example**:
```python
from artifact_collection import ChainOfCustody

# Initialize chain of custody
coc = ChainOfCustody(
    case_id="CASE-2024-001",
    case_name="Security Incident Investigation",
    custodian="John Doe"
)

# Add evidence items
item1 = coc.add_evidence(
    item_id="EVD-001",
    description="Memory dump from workstation",
    source_system="WORKSTATION01",
    acquisition_method="WinPMEM",
    acquisition_time="2024-01-15T10:30:00Z",
    original_location="Physical RAM",
    file_path="/evidence/case001/memory.raw",
    hash_sha256="abc123..."
)

item2 = coc.add_evidence(
    item_id="EVD-002",
    description="Windows Event Logs",
    source_system="WORKSTATION01",
    acquisition_method="Robocopy",
    acquisition_time="2024-01-15T10:45:00Z",
    original_location="C:\\Windows\\System32\\winevt\\Logs\\",
    file_path="/evidence/case001/eventlogs/",
    hash_sha256="def456..."
)

# Record custody transfer
coc.record_transfer(
    item_id="EVD-001",
    from_custodian="John Doe",
    to_custodian="Jane Smith",
    transfer_time="2024-01-15T14:00:00Z",
    reason="Transfer for analysis",
    location="Forensics Lab"
)

# Record evidence access
coc.record_access(
    item_id="EVD-001",
    accessor="Jane Smith",
    access_time="2024-01-15T14:30:00Z",
    purpose="Memory analysis",
    actions_performed="Parsed with Volatility"
)

# Verify evidence integrity
verification = coc.verify_all()
for item in verification:
    print(f"Item: {item.item_id}")
    print(f"  Current hash: {item.current_hash}")
    print(f"  Original hash: {item.original_hash}")
    print(f"  Verified: {item.verified}")

# Generate chain of custody report
coc.generate_report("/evidence/case001/chain_of_custody.pdf")

# Export custody log
coc.export_log("/evidence/case001/custody_log.json")
```

### Task 8: Evidence Packaging
**Input**: Collected artifacts

**Process**:
1. Organize artifacts
2. Calculate hashes
3. Create evidence container
4. Document contents
5. Seal package

**Output**: Sealed evidence package

**Example**:
```python
from artifact_collection import EvidencePackager

# Initialize packager
packager = EvidencePackager(
    case_id="CASE-2024-001",
    examiner="John Doe"
)

# Add artifacts to package
packager.add_directory("/evidence/case001/volatile/")
packager.add_directory("/evidence/case001/windows/")
packager.add_file("/evidence/case001/notes.txt")

# Set package metadata
packager.set_metadata(
    case_name="Security Incident",
    description="Forensic artifacts from WORKSTATION01",
    collection_start="2024-01-15T10:00:00Z",
    collection_end="2024-01-15T12:00:00Z",
    source_system="WORKSTATION01"
)

# Create evidence package
package = packager.create_package(
    output_path="/evidence/packages/CASE-2024-001.zip",
    compress=True,
    encrypt=True,
    encryption_password="secure_password"
)

print(f"Package: {package.path}")
print(f"Size: {package.size_mb}MB")
print(f"Files: {package.file_count}")
print(f"SHA256: {package.sha256}")

# Generate manifest
manifest = packager.generate_manifest()
for item in manifest.items:
    print(f"File: {item.relative_path}")
    print(f"  Size: {item.size}")
    print(f"  SHA256: {item.sha256}")

# Seal package (creates tamper-evident record)
seal = packager.seal_package()
print(f"Seal ID: {seal.seal_id}")
print(f"Seal time: {seal.timestamp}")
print(f"Seal hash: {seal.seal_hash}")
```

### Task 9: Selective Collection
**Input**: Target system and artifact specification

**Process**:
1. Parse collection specification
2. Identify target artifacts
3. Collect specified items
4. Verify collection
5. Document results

**Output**: Targeted artifact collection

**Example**:
```python
from artifact_collection import SelectiveCollector

# Initialize selective collector
collector = SelectiveCollector(
    output_dir="/evidence/selective/",
    case_id="CASE-2024-001"
)

# Define collection specification
spec = {
    "registry": ["HKLM\\SOFTWARE", "HKCU\\SOFTWARE"],
    "event_logs": ["Security", "System", "Application"],
    "directories": [
        "C:\\Users\\*\\Downloads",
        "C:\\Users\\*\\Documents"
    ],
    "files": [
        "C:\\Windows\\System32\\config\\SAM",
        "C:\\Windows\\System32\\config\\SYSTEM"
    ],
    "file_patterns": ["*.exe", "*.dll", "*.ps1"],
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-01-31"
    }
}

# Collect based on specification
results = collector.collect(spec)

print(f"Items collected: {results.total_items}")
print(f"Size: {results.total_size_mb}MB")
print(f"Duration: {results.duration_seconds}s")

# Get collection details
for item in results.items:
    print(f"Collected: {item.source_path}")
    print(f"  Destination: {item.dest_path}")
    print(f"  Size: {item.size}")
    print(f"  SHA256: {item.sha256}")

# Generate selective collection report
collector.generate_report("/evidence/selective/collection_report.html")
```

### Task 10: Collection Verification
**Input**: Evidence collection directory

**Process**:
1. Read collection manifest
2. Verify file integrity
3. Check for missing items
4. Validate metadata
5. Generate verification report

**Output**: Verification results

**Example**:
```python
from artifact_collection import CollectionVerifier

# Initialize verifier
verifier = CollectionVerifier(
    collection_path="/evidence/case001/",
    manifest_path="/evidence/case001/manifest.json"
)

# Run full verification
verification = verifier.verify()

print(f"Verification result: {verification.status}")
print(f"Items verified: {verification.verified_count}")
print(f"Items failed: {verification.failed_count}")
print(f"Items missing: {verification.missing_count}")

# Get verification details
for item in verification.items:
    print(f"Item: {item.path}")
    print(f"  Expected hash: {item.expected_hash}")
    print(f"  Actual hash: {item.actual_hash}")
    print(f"  Status: {item.status}")
    if item.status != "verified":
        print(f"  Error: {item.error}")

# Check for integrity issues
issues = verifier.get_integrity_issues()
for issue in issues:
    print(f"ISSUE: {issue.type}")
    print(f"  Item: {issue.item}")
    print(f"  Description: {issue.description}")

# Verify chain of custody
coc_verification = verifier.verify_chain_of_custody()
print(f"Chain of custody valid: {coc_verification.valid}")

# Generate verification report
verifier.generate_report("/evidence/case001/verification_report.pdf")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `EVIDENCE_OUTPUT` | Default output directory | No | ./evidence |
| `ACQUISITION_TOOL` | Memory acquisition tool | No | Auto-detect |
| `HASH_ALGORITHM` | Hash algorithm for integrity | No | SHA256 |
| `COMPRESS_ARTIFACTS` | Compress collected artifacts | No | true |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `include_memory` | boolean | Include memory dump |
| `compress` | boolean | Compress artifacts |
| `encrypt` | boolean | Encrypt evidence package |
| `verify_collection` | boolean | Verify after collection |
| `parallel_collection` | boolean | Parallel artifact collection |

## Examples

### Example 1: Incident Response Collection
**Scenario**: Rapid artifact collection during active incident

```python
from artifact_collection import IncidentResponseCollector

# Initialize IR collector
collector = IncidentResponseCollector(
    case_id="IR-2024-001",
    priority="high"
)

# Quick volatile collection
volatile = collector.collect_volatile()

# Critical artifacts only
critical = collector.collect_critical_artifacts()

# Generate IR report
collector.generate_ir_report("/evidence/ir_report.html")
```

### Example 2: Legal Hold Collection
**Scenario**: Collecting artifacts for legal proceedings

```python
from artifact_collection import LegalHoldCollector

# Initialize with legal requirements
collector = LegalHoldCollector(
    case_id="LEGAL-2024-001",
    legal_hold_id="LH-12345",
    custodian="John Doe"
)

# Collect with full chain of custody
artifacts = collector.collect_all()

# Generate court-ready documentation
collector.generate_legal_package("/evidence/legal/")
```

## Limitations

- Memory acquisition requires appropriate privileges
- Some artifacts may be locked by running processes
- Remote collection depends on network connectivity
- Encrypted files cannot be decrypted without keys
- Collection may impact system performance
- Storage space required for large collections
- Some artifacts may be volatile and change

## Troubleshooting

### Common Issue 1: Access Denied
**Problem**: Cannot access certain files
**Solution**:
- Run with elevated privileges
- Use forensic boot media
- Deploy signed collection agent

### Common Issue 2: Memory Acquisition Failure
**Problem**: Cannot capture memory
**Solution**:
- Use alternative acquisition tool
- Check security software interference
- Verify driver compatibility

### Common Issue 3: Incomplete Collection
**Problem**: Some artifacts missing
**Solution**:
- Check for file locks
- Verify permissions
- Review collection logs

## Related Skills

- [memory-forensics](../memory-forensics/): Analyze collected memory
- [disk-forensics](../disk-forensics/): Analyze collected disk artifacts
- [timeline-forensics](../timeline-forensics/): Build timeline from artifacts
- [log-forensics](../log-forensics/): Analyze collected logs
- [incident-response](../../cybersecurity/incident-response/): IR workflow

## References

- [Artifact Collection Reference](references/REFERENCE.md)
- [Windows Artifacts Guide](references/WINDOWS_ARTIFACTS.md)
- [Linux Artifacts Guide](references/LINUX_ARTIFACTS.md)
- [Chain of Custody Guide](references/CHAIN_OF_CUSTODY.md)
