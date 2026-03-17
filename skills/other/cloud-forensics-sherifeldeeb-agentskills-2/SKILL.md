---
name: cloud-forensics
description: |
  Investigate cloud platform environments for forensic analysis. Use when investigating
  incidents in AWS, Azure, GCP, or M365 environments. Supports log analysis, resource
  inventory, configuration review, and evidence preservation in cloud environments.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: boto3, azure-mgmt, google-cloud-*
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Cloud Forensics

Comprehensive cloud forensics skill for investigating incidents in cloud platform environments. Enables analysis of cloud audit logs, resource configurations, data access patterns, and identity activities across AWS, Azure, GCP, and Microsoft 365 environments.

## Capabilities

- **AWS Forensics**: Analyze CloudTrail, VPC Flow Logs, S3 access, IAM activity
- **Azure Forensics**: Analyze Azure Activity Logs, Sign-in logs, resource changes
- **GCP Forensics**: Analyze Cloud Audit Logs, VPC Flow Logs, IAM activity
- **M365 Forensics**: Analyze Unified Audit Log, mailbox audit, SharePoint activity
- **Identity Analysis**: Track user activities, permission changes, suspicious access
- **Resource Inventory**: Document cloud resources and configurations
- **Data Access Analysis**: Track access to cloud storage and databases
- **Timeline Generation**: Create cloud activity timeline
- **Evidence Preservation**: Snapshot and preserve cloud evidence
- **Configuration Analysis**: Detect misconfigurations and security gaps

## Quick Start

```python
from cloud_forensics import AWSForensics, AzureForensics, CloudTimeline

# Initialize AWS forensics
aws = AWSForensics(profile="forensics", region="us-east-1")

# Get CloudTrail events
events = aws.get_cloudtrail_events(days=30)

# Analyze suspicious activity
suspicious = aws.detect_suspicious_activity()

# Create timeline
timeline = CloudTimeline()
timeline.add_aws(aws)
```

## Usage

### Task 1: AWS CloudTrail Analysis
**Input**: AWS credentials with CloudTrail access

**Process**:
1. Query CloudTrail events
2. Parse management events
3. Analyze data events
4. Detect anomalies
5. Generate timeline

**Output**: CloudTrail analysis report

**Example**:
```python
from cloud_forensics import AWSForensics

# Initialize with profile
aws = AWSForensics(profile="forensics", region="us-east-1")

# Get CloudTrail events
events = aws.get_cloudtrail_events(
    start_time="2024-01-01",
    end_time="2024-01-31",
    lookup_attributes=[
        {"AttributeKey": "EventSource", "AttributeValue": "iam.amazonaws.com"}
    ]
)

for event in events:
    print(f"[{event.event_time}] {event.event_name}")
    print(f"  User: {event.user_identity}")
    print(f"  Source IP: {event.source_ip}")
    print(f"  User Agent: {event.user_agent}")
    print(f"  Resources: {event.resources}")

# Get events by user
user_events = aws.get_events_by_user("arn:aws:iam::123456789012:user/suspect")

# Get events by IP
ip_events = aws.get_events_by_ip("203.0.113.50")

# Analyze IAM changes
iam_changes = aws.get_iam_changes()
for change in iam_changes:
    print(f"IAM Change: {change.event_name}")
    print(f"  Actor: {change.user}")
    print(f"  Target: {change.affected_entity}")
    print(f"  Details: {change.details}")

# Detect privilege escalation
priv_esc = aws.detect_privilege_escalation()
for pe in priv_esc:
    print(f"PRIV ESC: {pe.technique}")
    print(f"  User: {pe.user}")
    print(f"  Evidence: {pe.events}")

# Detect credential abuse
cred_abuse = aws.detect_credential_abuse()

# Export to CSV
aws.export_events("/evidence/cloudtrail.csv")

# Generate report
aws.generate_report("/evidence/aws_forensics.html")
```

### Task 2: AWS S3 Access Analysis
**Input**: S3 access logs or CloudTrail data events

**Process**:
1. Retrieve S3 access events
2. Analyze access patterns
3. Detect data exfiltration
4. Identify unauthorized access
5. Document findings

**Output**: S3 access analysis

**Example**:
```python
from cloud_forensics import AWSS3Forensics

# Initialize S3 forensics
s3_forensics = AWSS3Forensics(profile="forensics")

# Get bucket access events
access = s3_forensics.get_bucket_access("sensitive-data-bucket")

for event in access:
    print(f"[{event.time}] {event.operation}")
    print(f"  Key: {event.key}")
    print(f"  Requester: {event.requester}")
    print(f"  Source IP: {event.source_ip}")
    print(f"  Bytes: {event.bytes_sent}")

# Detect large downloads (potential exfiltration)
large_downloads = s3_forensics.detect_large_downloads(
    threshold_gb=1,
    time_window_hours=24
)
for dl in large_downloads:
    print(f"LARGE DOWNLOAD: {dl.bucket}/{dl.key}")
    print(f"  Size: {dl.size_gb}GB")
    print(f"  Requester: {dl.requester}")

# Detect unusual access patterns
unusual = s3_forensics.detect_unusual_access()
for u in unusual:
    print(f"UNUSUAL: {u.description}")
    print(f"  Bucket: {u.bucket}")
    print(f"  Evidence: {u.evidence}")

# Get public access events
public = s3_forensics.get_public_access_events()

# Analyze bucket policy changes
policy_changes = s3_forensics.get_policy_changes()

# Export S3 access report
s3_forensics.generate_report("/evidence/s3_access.html")
```

### Task 3: Azure Activity Log Analysis
**Input**: Azure credentials with Log Analytics access

**Process**:
1. Query Activity Logs
2. Analyze sign-in events
3. Track resource changes
4. Detect anomalies
5. Generate timeline

**Output**: Azure activity analysis

**Example**:
```python
from cloud_forensics import AzureForensics

# Initialize Azure forensics
azure = AzureForensics(
    tenant_id="tenant-id",
    subscription_id="subscription-id"
)

# Get activity logs
activities = azure.get_activity_logs(
    start_time="2024-01-01",
    end_time="2024-01-31"
)

for activity in activities:
    print(f"[{activity.event_timestamp}] {activity.operation_name}")
    print(f"  Caller: {activity.caller}")
    print(f"  Resource: {activity.resource_id}")
    print(f"  Status: {activity.status}")

# Get sign-in logs
signins = azure.get_signin_logs()
for signin in signins:
    print(f"Sign-in: {signin.user_principal_name}")
    print(f"  Time: {signin.created_datetime}")
    print(f"  IP: {signin.ip_address}")
    print(f"  Location: {signin.location}")
    print(f"  App: {signin.app_display_name}")
    print(f"  Status: {signin.status}")
    print(f"  Risk: {signin.risk_level}")

# Detect risky sign-ins
risky = azure.get_risky_signins()
for r in risky:
    print(f"RISKY: {r.user_principal_name}")
    print(f"  Risk level: {r.risk_level}")
    print(f"  Risk detail: {r.risk_detail}")

# Get directory audit logs
audit = azure.get_directory_audit()
for entry in audit:
    print(f"Audit: {entry.activity_display_name}")
    print(f"  Actor: {entry.initiated_by}")
    print(f"  Target: {entry.target_resources}")

# Detect suspicious activities
suspicious = azure.detect_suspicious_activities()

# Export report
azure.generate_report("/evidence/azure_forensics.html")
```

### Task 4: Microsoft 365 Investigation
**Input**: M365 admin credentials

**Process**:
1. Query Unified Audit Log
2. Analyze mailbox activity
3. Track SharePoint/OneDrive access
4. Detect data exfiltration
5. Generate report

**Output**: M365 investigation results

**Example**:
```python
from cloud_forensics import M365Forensics

# Initialize M365 forensics
m365 = M365Forensics(tenant_id="tenant-id")

# Search Unified Audit Log
events = m365.search_unified_audit_log(
    start_date="2024-01-01",
    end_date="2024-01-31",
    record_type="ExchangeItem",
    operations=["Send", "MailboxLogin"]
)

for event in events:
    print(f"[{event.creation_date}] {event.operation}")
    print(f"  User: {event.user_id}")
    print(f"  Client IP: {event.client_ip}")
    print(f"  Workload: {event.workload}")

# Get mailbox audit logs
mailbox = m365.get_mailbox_audit(user="user@company.com")
for entry in mailbox:
    print(f"[{entry.timestamp}] {entry.operation}")
    print(f"  Folders: {entry.folders}")
    print(f"  Client: {entry.client_info}")

# Get SharePoint activity
sharepoint = m365.get_sharepoint_activity(site="https://company.sharepoint.com/sites/sensitive")
for activity in sharepoint:
    print(f"[{activity.time}] {activity.operation}")
    print(f"  User: {activity.user}")
    print(f"  File: {activity.file_name}")
    print(f"  Site: {activity.site_url}")

# Detect data exfiltration
exfil = m365.detect_data_exfiltration()
for e in exfil:
    print(f"EXFIL: {e.indicator}")
    print(f"  User: {e.user}")
    print(f"  Data: {e.data_volume}")

# Get email forwarding rules
forwarding = m365.get_forwarding_rules()
for rule in forwarding:
    print(f"Forward: {rule.mailbox} -> {rule.forward_to}")
    print(f"  Created: {rule.created}")

# Get eDiscovery searches
ediscovery = m365.get_ediscovery_activity()

# Export report
m365.generate_report("/evidence/m365_forensics.html")
```

### Task 5: GCP Cloud Audit Analysis
**Input**: GCP credentials with logging access

**Process**:
1. Query Cloud Audit Logs
2. Analyze admin activity
3. Track data access
4. Detect anomalies
5. Generate timeline

**Output**: GCP audit analysis

**Example**:
```python
from cloud_forensics import GCPForensics

# Initialize GCP forensics
gcp = GCPForensics(project_id="my-project")

# Get admin activity logs
admin_logs = gcp.get_admin_activity_logs(
    start_time="2024-01-01",
    end_time="2024-01-31"
)

for log in admin_logs:
    print(f"[{log.timestamp}] {log.method_name}")
    print(f"  Principal: {log.principal_email}")
    print(f"  Resource: {log.resource_name}")
    print(f"  Service: {log.service_name}")

# Get data access logs
data_logs = gcp.get_data_access_logs()
for log in data_logs:
    print(f"[{log.timestamp}] {log.method_name}")
    print(f"  Principal: {log.principal_email}")
    print(f"  Resource: {log.resource_name}")

# Analyze IAM changes
iam_changes = gcp.get_iam_changes()
for change in iam_changes:
    print(f"IAM: {change.action}")
    print(f"  Member: {change.member}")
    print(f"  Role: {change.role}")
    print(f"  Resource: {change.resource}")

# Get Cloud Storage access
storage = gcp.get_storage_access_logs(bucket="sensitive-bucket")

# Detect suspicious activities
suspicious = gcp.detect_suspicious_activities()
for s in suspicious:
    print(f"SUSPICIOUS: {s.description}")
    print(f"  Evidence: {s.evidence}")

# Export VPC Flow Logs
flow_logs = gcp.get_vpc_flow_logs()

# Generate report
gcp.generate_report("/evidence/gcp_forensics.html")
```

### Task 6: Cloud Identity Investigation
**Input**: Cloud platform credentials

**Process**:
1. Enumerate identities
2. Analyze permission changes
3. Track authentication events
4. Detect credential compromise
5. Document findings

**Output**: Identity investigation results

**Example**:
```python
from cloud_forensics import CloudIdentityAnalyzer

# Initialize identity analyzer
analyzer = CloudIdentityAnalyzer()

# Add cloud sources
analyzer.add_aws(profile="forensics")
analyzer.add_azure(tenant_id="tenant-id")
analyzer.add_gcp(project_id="project-id")

# Get identity timeline
timeline = analyzer.get_identity_timeline(
    identity="user@company.com"
)
for event in timeline:
    print(f"[{event.timestamp}] {event.cloud} - {event.action}")
    print(f"  Details: {event.details}")

# Detect impossible travel
impossible = analyzer.detect_impossible_travel()
for i in impossible:
    print(f"IMPOSSIBLE TRAVEL: {i.identity}")
    print(f"  Location 1: {i.location1} at {i.time1}")
    print(f"  Location 2: {i.location2} at {i.time2}")

# Detect credential sharing
sharing = analyzer.detect_credential_sharing()
for s in sharing:
    print(f"SHARING: {s.identity}")
    print(f"  Evidence: {s.evidence}")

# Get permission changes
perms = analyzer.get_permission_changes()
for p in perms:
    print(f"Permission: {p.identity}")
    print(f"  Cloud: {p.cloud}")
    print(f"  Change: {p.change_type}")
    print(f"  Details: {p.details}")

# Detect privilege escalation
priv_esc = analyzer.detect_privilege_escalation()

# Generate identity report
analyzer.generate_report("/evidence/identity_investigation.html")
```

### Task 7: Cloud Resource Inventory
**Input**: Cloud platform credentials

**Process**:
1. Enumerate all resources
2. Document configurations
3. Identify exposed resources
4. Check security settings
5. Generate inventory

**Output**: Complete resource inventory

**Example**:
```python
from cloud_forensics import CloudInventory

# Initialize inventory
inventory = CloudInventory()

# Add cloud accounts
inventory.add_aws(profile="forensics", regions=["us-east-1", "us-west-2"])
inventory.add_azure(tenant_id="tenant-id", subscription_id="sub-id")
inventory.add_gcp(project_id="project-id")

# Collect inventory
resources = inventory.collect_all()

print(f"Total resources: {resources.total_count}")
print(f"AWS resources: {resources.aws_count}")
print(f"Azure resources: {resources.azure_count}")
print(f"GCP resources: {resources.gcp_count}")

# Get resources by type
ec2_instances = inventory.get_by_type("aws:ec2:instance")
for instance in ec2_instances:
    print(f"EC2: {instance.id}")
    print(f"  State: {instance.state}")
    print(f"  Type: {instance.instance_type}")
    print(f"  VPC: {instance.vpc_id}")
    print(f"  Public IP: {instance.public_ip}")

# Find exposed resources
exposed = inventory.find_exposed_resources()
for e in exposed:
    print(f"EXPOSED: {e.resource_type} - {e.resource_id}")
    print(f"  Reason: {e.exposure_reason}")

# Get security groups
security_groups = inventory.get_security_groups()
for sg in security_groups:
    print(f"SG: {sg.id}")
    print(f"  Open ports: {sg.open_ports}")
    print(f"  Public access: {sg.allows_public}")

# Export inventory
inventory.export_json("/evidence/cloud_inventory.json")
inventory.export_csv("/evidence/cloud_inventory.csv")

# Generate inventory report
inventory.generate_report("/evidence/inventory_report.html")
```

### Task 8: Evidence Preservation
**Input**: Cloud resources to preserve

**Process**:
1. Identify resources to preserve
2. Create snapshots
3. Export logs
4. Document chain of custody
5. Verify preservation

**Output**: Preserved evidence with documentation

**Example**:
```python
from cloud_forensics import CloudEvidencePreserver

# Initialize preserver
preserver = CloudEvidencePreserver(
    output_bucket="forensics-evidence-bucket",
    case_id="CASE-2024-001"
)

# AWS evidence preservation
aws_evidence = preserver.preserve_aws_instance(
    instance_id="i-1234567890abcdef0",
    region="us-east-1"
)
print(f"Instance snapshot: {aws_evidence.snapshot_id}")
print(f"Memory dump: {aws_evidence.memory_dump}")
print(f"Disk images: {aws_evidence.disk_images}")

# Preserve S3 bucket
s3_evidence = preserver.preserve_s3_bucket(
    bucket_name="compromised-bucket",
    include_versions=True
)

# Preserve CloudTrail logs
trail_evidence = preserver.preserve_cloudtrail(
    trail_name="main-trail",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Azure evidence preservation
azure_evidence = preserver.preserve_azure_vm(
    resource_group="my-rg",
    vm_name="compromised-vm"
)

# Preserve Azure storage
storage_evidence = preserver.preserve_azure_storage(
    storage_account="mystorageaccount",
    container="sensitive-data"
)

# Generate chain of custody
preserver.generate_chain_of_custody("/evidence/chain_of_custody.pdf")

# Verify evidence integrity
verification = preserver.verify_evidence()
for item in verification:
    print(f"Evidence: {item.id}")
    print(f"  Hash: {item.hash}")
    print(f"  Verified: {item.verified}")
```

### Task 9: Cloud Network Analysis
**Input**: VPC Flow Logs or network logs

**Process**:
1. Parse flow logs
2. Analyze traffic patterns
3. Identify C2 communications
4. Detect lateral movement
5. Document network activity

**Output**: Cloud network analysis

**Example**:
```python
from cloud_forensics import CloudNetworkAnalyzer

# Initialize network analyzer
analyzer = CloudNetworkAnalyzer()

# Load AWS VPC Flow Logs
analyzer.load_aws_flow_logs(
    log_group="/aws/vpc/flow-logs",
    start_time="2024-01-01",
    end_time="2024-01-31"
)

# Get flow statistics
stats = analyzer.get_statistics()
print(f"Total flows: {stats.total_flows}")
print(f"Accepted: {stats.accepted}")
print(f"Rejected: {stats.rejected}")

# Find top talkers
talkers = analyzer.get_top_talkers(limit=10)
for t in talkers:
    print(f"{t.source_ip} -> {t.dest_ip}:{t.dest_port}")
    print(f"  Bytes: {t.bytes}")
    print(f"  Packets: {t.packets}")

# Detect suspicious traffic
suspicious = analyzer.detect_suspicious_traffic()
for s in suspicious:
    print(f"SUSPICIOUS: {s.description}")
    print(f"  Source: {s.source}")
    print(f"  Destination: {s.destination}")
    print(f"  Reason: {s.reason}")

# Detect C2 beaconing
beacons = analyzer.detect_beaconing()
for b in beacons:
    print(f"BEACON: {b.source} -> {b.destination}")
    print(f"  Interval: {b.interval_seconds}s")

# Detect data exfiltration
exfil = analyzer.detect_exfiltration()

# Analyze security group violations
violations = analyzer.analyze_sg_violations()

# Generate network report
analyzer.generate_report("/evidence/cloud_network.html")
```

### Task 10: Cloud Timeline Generation
**Input**: Multiple cloud log sources

**Process**:
1. Collect events from all sources
2. Normalize timestamps
3. Correlate events
4. Build unified timeline
5. Identify attack sequence

**Output**: Unified cloud timeline

**Example**:
```python
from cloud_forensics import CloudTimeline

# Initialize timeline
timeline = CloudTimeline()

# Add AWS sources
timeline.add_cloudtrail(profile="forensics", region="us-east-1")
timeline.add_vpc_flow_logs(log_group="/aws/vpc/flow-logs")
timeline.add_s3_access_logs(bucket="access-logs-bucket")

# Add Azure sources
timeline.add_azure_activity_logs(subscription_id="sub-id")
timeline.add_azure_signin_logs(tenant_id="tenant-id")

# Add GCP sources
timeline.add_gcp_audit_logs(project_id="project-id")

# Build timeline
events = timeline.build(
    start_time="2024-01-01",
    end_time="2024-01-31"
)

for event in events:
    print(f"[{event.timestamp}] {event.cloud} - {event.event_type}")
    print(f"  Actor: {event.actor}")
    print(f"  Action: {event.action}")
    print(f"  Target: {event.target}")
    print(f"  Source IP: {event.source_ip}")

# Correlate events
correlated = timeline.correlate_by_ip("203.0.113.50")

# Identify attack chain
attack = timeline.identify_attack_sequence()
for stage in attack.stages:
    print(f"Stage: {stage.name}")
    print(f"  Technique: {stage.mitre_technique}")
    print(f"  Events: {len(stage.events)}")

# Export timeline
timeline.export_csv("/evidence/cloud_timeline.csv")
timeline.export_json("/evidence/cloud_timeline.json")

# Generate interactive timeline
timeline.generate_html("/evidence/cloud_timeline.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AWS_PROFILE` | AWS CLI profile name | No | default |
| `AZURE_TENANT_ID` | Azure tenant ID | No | None |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | No | None |
| `GCP_PROJECT_ID` | GCP project ID | No | None |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `include_data_events` | boolean | Include CloudTrail data events |
| `preserve_evidence` | boolean | Auto-preserve relevant evidence |
| `parallel_collection` | boolean | Parallel log collection |
| `normalize_timestamps` | boolean | Normalize to UTC |
| `enrich_geolocation` | boolean | Add geolocation data |

## Examples

### Example 1: Cloud Breach Investigation
**Scenario**: Investigating unauthorized access to cloud resources

```python
from cloud_forensics import AWSForensics, CloudTimeline

# Initialize AWS forensics
aws = AWSForensics(profile="forensics")

# Find initial compromise
suspicious = aws.detect_suspicious_activities()

# Get attacker's activities
attacker_events = aws.get_events_by_ip("203.0.113.50")

# Build attack timeline
timeline = CloudTimeline()
timeline.add_cloudtrail(profile="forensics")

# Identify all affected resources
affected = aws.get_affected_resources(ip="203.0.113.50")
for resource in affected:
    print(f"Affected: {resource.type} - {resource.id}")

# Preserve evidence
aws.preserve_evidence(affected, output_bucket="forensics-bucket")
```

### Example 2: Data Exfiltration Analysis
**Scenario**: Investigating data theft from cloud storage

```python
from cloud_forensics import AWSS3Forensics, AzureStorageForensics

# Analyze S3 access
s3 = AWSS3Forensics(profile="forensics")

# Find large downloads
downloads = s3.detect_large_downloads(threshold_gb=1)

# Analyze access patterns
patterns = s3.analyze_access_patterns("sensitive-bucket")

# Get unique requesters
requesters = s3.get_unique_requesters("sensitive-bucket")
for r in requesters:
    print(f"Requester: {r.identity}")
    print(f"  Downloads: {r.download_count}")
    print(f"  Volume: {r.total_bytes}")
```

## Limitations

- Requires appropriate cloud permissions
- Log retention affects available data
- Some logs may not be enabled
- Cross-account investigation requires access
- Real-time analysis not supported
- API rate limits may affect collection
- Cost implications for large-scale queries

## Troubleshooting

### Common Issue 1: Permission Denied
**Problem**: Cannot access cloud logs
**Solution**:
- Verify IAM permissions
- Check role trust relationships
- Ensure correct credentials

### Common Issue 2: Missing Logs
**Problem**: Expected logs not found
**Solution**:
- Verify logging is enabled
- Check log retention settings
- Confirm correct time range

### Common Issue 3: API Throttling
**Problem**: Rate limit errors
**Solution**:
- Use parallel collection carefully
- Implement exponential backoff
- Request limit increases

## Related Skills

- [log-forensics](../log-forensics/): General log analysis
- [network-forensics](../network-forensics/): Network traffic analysis
- [timeline-forensics](../timeline-forensics/): Timeline integration
- [email-forensics](../email-forensics/): M365 email investigation
- [artifact-collection](../artifact-collection/): Evidence preservation

## References

- [Cloud Forensics Reference](references/REFERENCE.md)
- [AWS Forensics Guide](references/AWS_FORENSICS.md)
- [Azure Forensics Guide](references/AZURE_FORENSICS.md)
- [GCP Forensics Guide](references/GCP_FORENSICS.md)
