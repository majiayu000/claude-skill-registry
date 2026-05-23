---
name: registry-forensics
description: |
  Analyze Windows Registry hives for forensic investigation. Use when investigating
  malware persistence, user activity, system configuration changes, or evidence of
  program execution. Supports offline registry analysis from disk images or extracted hives.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: python-registry, regipy, yarp
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Registry Forensics

Comprehensive Windows Registry forensics skill for analyzing registry hives to uncover user activity, malware persistence, system configuration, and evidence of program execution. Enables extraction of forensically valuable artifacts from SAM, SYSTEM, SOFTWARE, NTUSER.DAT, and other registry hives.

## Capabilities

- **Registry Hive Parsing**: Parse all Windows registry hive types (SAM, SYSTEM, SOFTWARE, NTUSER.DAT, USRCLASS.DAT)
- **Persistence Analysis**: Identify autorun entries, services, and scheduled tasks
- **User Activity Tracking**: Extract recent documents, typed URLs, search history
- **Program Execution**: Analyze UserAssist, Shimcache, Amcache, BAM/DAM
- **USB Device History**: Extract connected USB device information
- **Network History**: Analyze network connection history and profiles
- **System Configuration**: Extract OS version, timezone, computer name
- **Malware Indicators**: Detect known malicious registry patterns
- **Timeline Generation**: Create registry-based activity timeline
- **Registry Comparison**: Compare registry states for change detection

## Quick Start

```python
from registry_forensics import RegistryAnalyzer, HiveParser, PersistenceScanner

# Parse registry hive
parser = HiveParser("/evidence/NTUSER.DAT")

# Get all keys
keys = parser.get_all_keys()

# Scan for persistence
scanner = PersistenceScanner("/evidence/")
persistence = scanner.scan_all_hives()

# Analyze user activity
analyzer = RegistryAnalyzer("/evidence/")
activity = analyzer.get_user_activity()
```

## Usage

### Task 1: Registry Hive Parsing
**Input**: Registry hive file

**Process**:
1. Load and validate hive file
2. Parse hive structure
3. Enumerate keys and values
4. Extract metadata
5. Generate hive summary

**Output**: Parsed registry structure

**Example**:
```python
from registry_forensics import HiveParser

# Parse NTUSER.DAT hive
parser = HiveParser("/evidence/NTUSER.DAT")

# Get hive metadata
info = parser.get_hive_info()
print(f"Hive type: {info.hive_type}")
print(f"Last written: {info.last_written}")
print(f"Root key: {info.root_key}")

# Get all subkeys of a key
subkeys = parser.get_subkeys("Software\\Microsoft\\Windows\\CurrentVersion")
for key in subkeys:
    print(f"Key: {key.name}")
    print(f"  Last modified: {key.last_modified}")
    print(f"  Values: {key.value_count}")

# Get specific value
value = parser.get_value(
    "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer",
    "Shell Folders"
)
print(f"Value: {value.name} = {value.data}")

# Search for keys/values
results = parser.search("password", include_values=True)
for r in results:
    print(f"Found: {r.path}")

# Export key to REG file
parser.export_key(
    "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
    "/evidence/run_key.reg"
)

# Get all values recursively
all_values = parser.get_all_values(recursive=True)
```

### Task 2: Persistence Mechanism Analysis
**Input**: Registry hives (SOFTWARE, NTUSER.DAT, SYSTEM)

**Process**:
1. Load relevant hives
2. Check common persistence locations
3. Analyze autorun entries
4. Identify suspicious entries
5. Correlate with known malware

**Output**: Persistence mechanism inventory

**Example**:
```python
from registry_forensics import PersistenceScanner

# Initialize scanner with evidence directory
scanner = PersistenceScanner("/evidence/registry/")

# Scan all persistence locations
persistence = scanner.scan_all()

for p in persistence:
    print(f"Persistence: {p.location}")
    print(f"  Name: {p.name}")
    print(f"  Value: {p.value}")
    print(f"  Type: {p.persistence_type}")
    print(f"  Risk: {p.risk_level}")

# Get Run key entries
run_entries = scanner.get_run_keys()
for entry in run_entries:
    print(f"Run: {entry.name} = {entry.command}")
    print(f"  Hive: {entry.hive}")
    print(f"  User: {entry.user}")

# Get services
services = scanner.get_services()
for svc in services:
    print(f"Service: {svc.name}")
    print(f"  Display: {svc.display_name}")
    print(f"  Path: {svc.image_path}")
    print(f"  Start type: {svc.start_type}")
    print(f"  Account: {svc.service_account}")

# Get scheduled tasks (from registry)
tasks = scanner.get_scheduled_tasks()

# Get shell extensions
extensions = scanner.get_shell_extensions()

# Get browser helper objects
bhos = scanner.get_browser_helpers()

# Detect suspicious persistence
suspicious = scanner.find_suspicious()
for s in suspicious:
    print(f"SUSPICIOUS: {s.location}")
    print(f"  Reason: {s.reason}")

# Export report
scanner.generate_report("/evidence/persistence_report.html")
```

### Task 3: User Activity Analysis
**Input**: NTUSER.DAT and USRCLASS.DAT hives

**Process**:
1. Parse user registry hives
2. Extract recent documents
3. Get typed paths and URLs
4. Analyze search history
5. Extract user preferences

**Output**: User activity summary

**Example**:
```python
from registry_forensics import UserActivityAnalyzer

# Analyze user's registry
analyzer = UserActivityAnalyzer(
    ntuser_path="/evidence/NTUSER.DAT",
    usrclass_path="/evidence/USRCLASS.DAT"
)

# Get recent documents (MRU lists)
recent_docs = analyzer.get_recent_documents()
for doc in recent_docs:
    print(f"Recent: {doc.filename}")
    print(f"  Path: {doc.path}")
    print(f"  Last access: {doc.last_access}")
    print(f"  MRU source: {doc.source}")

# Get typed paths (Explorer address bar)
typed_paths = analyzer.get_typed_paths()
for path in typed_paths:
    print(f"Typed path: {path.value}")
    print(f"  Timestamp: {path.timestamp}")

# Get typed URLs (IE/Edge)
typed_urls = analyzer.get_typed_urls()
for url in typed_urls:
    print(f"URL: {url.value}")

# Get search history (WordWheelQuery)
searches = analyzer.get_search_history()
for search in searches:
    print(f"Search: {search.query}")
    print(f"  Timestamp: {search.timestamp}")

# Get recently opened/saved dialogs
dialogs = analyzer.get_dialog_history()
for d in dialogs:
    print(f"Dialog: {d.application}")
    print(f"  Path: {d.last_path}")

# Get mapped network drives
network_drives = analyzer.get_network_drives()

# Get user's shell bags
shellbags = analyzer.get_shellbags()
for bag in shellbags:
    print(f"ShellBag: {bag.path}")
    print(f"  First access: {bag.first_accessed}")
    print(f"  Last access: {bag.last_accessed}")
    print(f"  Access count: {bag.access_count}")

# Generate user activity report
analyzer.generate_report("/evidence/user_activity.html")
```

### Task 4: Program Execution Analysis
**Input**: Multiple registry hives

**Process**:
1. Parse UserAssist entries
2. Analyze Shimcache
3. Parse Amcache
4. Check BAM/DAM
5. Correlate execution evidence

**Output**: Program execution history

**Example**:
```python
from registry_forensics import ExecutionAnalyzer

# Initialize execution analyzer
analyzer = ExecutionAnalyzer(
    ntuser_path="/evidence/NTUSER.DAT",
    system_path="/evidence/SYSTEM",
    amcache_path="/evidence/Amcache.hve"
)

# Get UserAssist data
userassist = analyzer.get_userassist()
for entry in userassist:
    print(f"Program: {entry.name}")
    print(f"  Run count: {entry.run_count}")
    print(f"  Last run: {entry.last_run}")
    print(f"  Focus time: {entry.focus_time}")

# Get Shimcache entries
shimcache = analyzer.get_shimcache()
for entry in shimcache:
    print(f"Shimcache: {entry.path}")
    print(f"  Last modified: {entry.last_modified}")
    print(f"  Executed: {entry.executed}")

# Get Amcache entries
amcache = analyzer.get_amcache()
for entry in amcache:
    print(f"Amcache: {entry.filename}")
    print(f"  Path: {entry.full_path}")
    print(f"  SHA1: {entry.sha1}")
    print(f"  First run: {entry.first_run}")
    print(f"  Publisher: {entry.publisher}")

# Get BAM/DAM data (Background Activity Monitor)
bam = analyzer.get_bam_dam()
for entry in bam:
    print(f"BAM: {entry.executable}")
    print(f"  User: {entry.user_sid}")
    print(f"  Last execution: {entry.last_execution}")

# Get AppCompatFlags
appcompat = analyzer.get_appcompat_flags()

# Get MUICache (executed programs with GUIs)
muicache = analyzer.get_muicache()

# Correlate all execution evidence
correlated = analyzer.correlate_execution()
for prog in correlated:
    print(f"Execution: {prog.name}")
    print(f"  Evidence sources: {prog.sources}")
    print(f"  First seen: {prog.first_seen}")
    print(f"  Last seen: {prog.last_seen}")
    print(f"  Run count: {prog.estimated_runs}")

# Export execution timeline
analyzer.export_timeline("/evidence/execution_timeline.csv")
```

### Task 5: USB Device History
**Input**: SYSTEM and SOFTWARE hives

**Process**:
1. Parse USB device entries
2. Extract device details
3. Determine first/last connection
4. Map to volume information
5. Identify device owners

**Output**: USB device connection history

**Example**:
```python
from registry_forensics import USBAnalyzer

# Initialize USB analyzer
analyzer = USBAnalyzer(
    system_path="/evidence/SYSTEM",
    software_path="/evidence/SOFTWARE"
)

# Get all USB devices
devices = analyzer.get_all_devices()

for device in devices:
    print(f"USB Device: {device.friendly_name}")
    print(f"  Vendor ID: {device.vendor_id}")
    print(f"  Product ID: {device.product_id}")
    print(f"  Serial Number: {device.serial_number}")
    print(f"  First connected: {device.first_connected}")
    print(f"  Last connected: {device.last_connected}")
    print(f"  Volume GUID: {device.volume_guid}")
    print(f"  Drive letter: {device.drive_letter}")
    print(f"  User: {device.user_account}")

# Get USB storage devices specifically
storage = analyzer.get_usb_storage()
for s in storage:
    print(f"Storage: {s.friendly_name}")
    print(f"  Capacity: {s.capacity_bytes}")

# Get mounted devices
mounted = analyzer.get_mounted_devices()

# Get device setup classes
setup = analyzer.get_device_setup()

# Correlate with NTUSER for user mapping
analyzer.add_ntuser("/evidence/NTUSER.DAT")
user_devices = analyzer.get_user_device_history()

# Generate USB history report
analyzer.generate_report("/evidence/usb_history.html")
```

### Task 6: Network Configuration Analysis
**Input**: SYSTEM and SOFTWARE hives

**Process**:
1. Parse network profiles
2. Extract connection history
3. Get interface configuration
4. Analyze wireless networks
5. Check VPN configurations

**Output**: Network configuration and history

**Example**:
```python
from registry_forensics import NetworkAnalyzer

# Initialize network analyzer
analyzer = NetworkAnalyzer(
    system_path="/evidence/SYSTEM",
    software_path="/evidence/SOFTWARE"
)

# Get network interfaces
interfaces = analyzer.get_interfaces()
for iface in interfaces:
    print(f"Interface: {iface.name}")
    print(f"  Type: {iface.type}")
    print(f"  MAC: {iface.mac_address}")
    print(f"  DHCP: {iface.dhcp_enabled}")
    print(f"  IP: {iface.ip_address}")

# Get network profiles
profiles = analyzer.get_network_profiles()
for p in profiles:
    print(f"Profile: {p.name}")
    print(f"  First connected: {p.first_connected}")
    print(f"  Last connected: {p.last_connected}")
    print(f"  Type: {p.network_type}")
    print(f"  Category: {p.category}")

# Get wireless network history
wireless = analyzer.get_wireless_networks()
for w in wireless:
    print(f"SSID: {w.ssid}")
    print(f"  Authentication: {w.authentication}")
    print(f"  First seen: {w.first_connected}")

# Get VPN configurations
vpns = analyzer.get_vpn_connections()
for vpn in vpns:
    print(f"VPN: {vpn.name}")
    print(f"  Server: {vpn.server_address}")
    print(f"  Type: {vpn.type}")

# Get DNS cache information
dns_cache = analyzer.get_dns_cache_info()

# Get proxy settings
proxy = analyzer.get_proxy_settings()
if proxy.enabled:
    print(f"Proxy: {proxy.server}")

# Generate network report
analyzer.generate_report("/evidence/network_history.html")
```

### Task 7: System Information Extraction
**Input**: SYSTEM and SOFTWARE hives

**Process**:
1. Extract OS information
2. Get computer name/domain
3. Extract timezone
4. Get installed software
5. Determine system configuration

**Output**: System configuration details

**Example**:
```python
from registry_forensics import SystemInfoAnalyzer

# Initialize system info analyzer
analyzer = SystemInfoAnalyzer(
    system_path="/evidence/SYSTEM",
    software_path="/evidence/SOFTWARE"
)

# Get OS information
os_info = analyzer.get_os_info()
print(f"Product: {os_info.product_name}")
print(f"Version: {os_info.version}")
print(f"Build: {os_info.build_number}")
print(f"Install date: {os_info.install_date}")
print(f"Registered owner: {os_info.registered_owner}")
print(f"Product ID: {os_info.product_id}")

# Get computer information
computer = analyzer.get_computer_info()
print(f"Computer name: {computer.name}")
print(f"Domain/Workgroup: {computer.domain}")
print(f"Last shutdown: {computer.last_shutdown}")

# Get timezone
tz = analyzer.get_timezone()
print(f"Timezone: {tz.standard_name}")
print(f"UTC offset: {tz.utc_offset}")
print(f"DST: {tz.daylight_saving}")

# Get installed software
software = analyzer.get_installed_software()
for sw in software:
    print(f"Software: {sw.display_name}")
    print(f"  Version: {sw.version}")
    print(f"  Publisher: {sw.publisher}")
    print(f"  Install date: {sw.install_date}")
    print(f"  Install location: {sw.install_location}")

# Get environment variables
env_vars = analyzer.get_environment_variables()

# Get current control set
control_set = analyzer.get_current_control_set()
print(f"Current control set: {control_set}")

# Export system info report
analyzer.generate_report("/evidence/system_info.html")
```

### Task 8: SAM Analysis (User Accounts)
**Input**: SAM hive

**Process**:
1. Parse SAM hive
2. Extract user accounts
3. Get account metadata
4. Analyze login information
5. Extract password hints

**Output**: User account analysis

**Example**:
```python
from registry_forensics import SAMAnalyzer

# Initialize SAM analyzer
analyzer = SAMAnalyzer("/evidence/SAM")

# Get all user accounts
users = analyzer.get_users()

for user in users:
    print(f"User: {user.username}")
    print(f"  RID: {user.rid}")
    print(f"  Full name: {user.full_name}")
    print(f"  Comment: {user.comment}")
    print(f"  Account type: {user.account_type}")
    print(f"  Created: {user.created_date}")
    print(f"  Last login: {user.last_login}")
    print(f"  Login count: {user.login_count}")
    print(f"  Password last set: {user.password_last_set}")
    print(f"  Account expires: {user.account_expires}")
    print(f"  Disabled: {user.disabled}")
    print(f"  Password required: {user.password_required}")
    print(f"  Password hint: {user.password_hint}")

# Get groups
groups = analyzer.get_groups()
for group in groups:
    print(f"Group: {group.name}")
    print(f"  Members: {group.members}")

# Get administrator accounts
admins = analyzer.get_administrators()

# Get recently created accounts
recent = analyzer.get_recent_accounts(days=30)

# Export SAM report
analyzer.generate_report("/evidence/sam_analysis.html")
```

### Task 9: Malware Detection in Registry
**Input**: All registry hives

**Process**:
1. Scan for known malware indicators
2. Check suspicious key patterns
3. Analyze encoded values
4. Detect obfuscation
5. Generate IOCs

**Output**: Malware indicator findings

**Example**:
```python
from registry_forensics import MalwareScanner

# Initialize malware scanner
scanner = MalwareScanner("/evidence/registry/")

# Scan all hives
findings = scanner.scan_all()

for finding in findings:
    print(f"MALWARE INDICATOR: {finding.indicator_type}")
    print(f"  Location: {finding.key_path}")
    print(f"  Value: {finding.value_name}")
    print(f"  Data: {finding.value_data}")
    print(f"  Confidence: {finding.confidence}")
    print(f"  Description: {finding.description}")

# Check for known malware patterns
known = scanner.check_known_patterns()
for k in known:
    print(f"Known Malware: {k.malware_family}")
    print(f"  Match: {k.matched_pattern}")

# Find encoded/obfuscated values
encoded = scanner.find_encoded_values()
for e in encoded:
    print(f"Encoded: {e.path}")
    print(f"  Encoding: {e.encoding_type}")
    print(f"  Decoded: {e.decoded_value}")

# Find suspicious executables in autorun
suspicious_exe = scanner.find_suspicious_autoruns()

# Check for fileless malware indicators
fileless = scanner.detect_fileless_indicators()
for f in fileless:
    print(f"Fileless: {f.technique}")
    print(f"  Evidence: {f.evidence}")

# YARA scan registry values
yara_matches = scanner.yara_scan("/rules/malware.yar")

# Export findings
scanner.export_iocs("/evidence/registry_iocs.json")
scanner.generate_report("/evidence/malware_scan.html")
```

### Task 10: Registry Timeline Generation
**Input**: Registry hives with timestamps

**Process**:
1. Extract key last-write times
2. Correlate temporal data
3. Build activity timeline
4. Identify suspicious timing
5. Export timeline

**Output**: Registry-based timeline

**Example**:
```python
from registry_forensics import RegistryTimeline

# Initialize timeline builder
timeline = RegistryTimeline("/evidence/registry/")

# Build timeline from all hives
events = timeline.build_timeline()

for event in events:
    print(f"[{event.timestamp}] {event.event_type}")
    print(f"  Hive: {event.hive}")
    print(f"  Key: {event.key_path}")
    print(f"  Details: {event.details}")

# Filter timeline by date range
filtered = timeline.filter_by_date(
    start="2024-01-01",
    end="2024-01-31"
)

# Get events around specific time
window = timeline.get_events_around(
    timestamp="2024-01-15T10:30:00",
    window_minutes=60
)

# Find rapid changes (potential automation)
rapid = timeline.find_rapid_changes(
    threshold=10,
    window_seconds=60
)

# Get activity by hour
hourly = timeline.get_hourly_distribution()

# Export timeline
timeline.export_csv("/evidence/registry_timeline.csv")
timeline.export_json("/evidence/registry_timeline.json")
timeline.generate_html_report("/evidence/registry_timeline.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `REGISTRY_PARSER` | Path to registry parsing library | No | Built-in |
| `YARA_RULES` | Path to YARA rules for scanning | No | None |
| `MALWARE_HASHES` | Path to malware hash database | No | None |
| `TIMELINE_TZ` | Timezone for timeline display | No | UTC |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `parse_deleted` | boolean | Attempt to recover deleted entries |
| `decode_values` | boolean | Auto-decode encoded values |
| `include_slack` | boolean | Analyze registry slack space |
| `parallel` | boolean | Enable parallel processing |
| `cache_parsed` | boolean | Cache parsed results |

## Examples

### Example 1: Malware Persistence Investigation
**Scenario**: Finding malware persistence mechanisms

```python
from registry_forensics import RegistryAnalyzer, PersistenceScanner

# Load registry hives
scanner = PersistenceScanner("/evidence/registry/")

# Get all persistence mechanisms
persistence = scanner.scan_all()

# Filter suspicious entries
suspicious = [p for p in persistence if p.risk_level >= "medium"]

for s in suspicious:
    print(f"SUSPICIOUS: {s.name}")
    print(f"  Location: {s.location}")
    print(f"  Command: {s.value}")
    print(f"  Risk: {s.risk_level}")
    print(f"  Reason: {s.risk_reason}")

# Check against known malware
known = scanner.check_against_known_malware("/hashsets/malware_commands.txt")

# Generate remediation script
scanner.generate_remediation_script("/evidence/cleanup.reg")
```

### Example 2: User Activity Reconstruction
**Scenario**: Reconstructing user's actions for investigation

```python
from registry_forensics import UserActivityAnalyzer, ExecutionAnalyzer, RegistryTimeline

# Analyze user activity
activity = UserActivityAnalyzer("/evidence/NTUSER.DAT")

# Get comprehensive activity
timeline = activity.get_full_timeline()

# Add execution evidence
execution = ExecutionAnalyzer("/evidence/")
exec_timeline = execution.correlate_execution()

# Combine with registry timeline
reg_timeline = RegistryTimeline("/evidence/registry/")

# Merge all timelines
combined = reg_timeline.merge_timelines([
    activity.get_timeline(),
    execution.get_timeline()
])

# Export comprehensive report
combined.generate_report(
    "/evidence/user_investigation.html",
    include_charts=True
)
```

## Limitations

- Deleted registry entries may not be recoverable
- Some hives may be locked on live systems
- Timestamp precision limited to 100-nanosecond intervals
- Transaction logs required for full recovery
- Anti-forensics may hide registry artifacts
- Large hives may require significant memory
- Some encoding may not be automatically detected

## Troubleshooting

### Common Issue 1: Hive Parsing Failure
**Problem**: Unable to parse registry hive
**Solution**:
- Check hive file integrity
- Ensure complete extraction
- Try alternative parser

### Common Issue 2: Missing Timestamps
**Problem**: Key timestamps not available
**Solution**:
- Timestamps only on keys, not values
- Check for dirty hive (unsaved changes)
- Analyze transaction logs

### Common Issue 3: Encoded Values Not Decoded
**Problem**: Values appear as binary/encoded
**Solution**:
- Enable decode_values option
- Check for ROT13, Base64, XOR encoding
- Manually inspect suspicious values

## Related Skills

- [disk-forensics](../disk-forensics/): Extract registry hives from disk
- [memory-forensics](../memory-forensics/): Extract registry from memory
- [timeline-forensics](../timeline-forensics/): Integrate registry timeline
- [malware-forensics](../malware-forensics/): Analyze malware samples
- [log-forensics](../log-forensics/): Correlate with event logs

## References

- [Registry Forensics Reference](references/REFERENCE.md)
- [Windows Registry Keys Guide](references/REGISTRY_KEYS.md)
- [Persistence Locations](references/PERSISTENCE.md)
