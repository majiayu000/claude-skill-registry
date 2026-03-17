---
name: containment
description: |
  Security incident containment playbooks for isolating threats across network,
  endpoint, identity, cloud, and application layers. Use for active incident
  response to limit threat spread and impact.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - No external dependencies (standard library only)
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: cybersecurity
---

# Containment Playbooks Skill

Comprehensive containment procedures for isolating security threats during active incidents. Provides structured playbooks for network, endpoint, identity, cloud, and application containment.

## Capabilities

- **Network Containment**: Host isolation, firewall blocks, DNS sinkholing, network segmentation
- **Endpoint Containment**: EDR isolation, process termination, service disabling, memory preservation
- **Identity Containment**: Account disable, session termination, credential reset, MFA reset
- **Cloud Containment**: IAM revocation, resource isolation, API key rotation, security group lockdown
- **Application Containment**: WAF rules, rate limiting, service shutdown, database lockdown
- **Email Containment**: Message quarantine, sender blocking, rule removal
- **Playbook Execution**: Track and document containment actions

## Quick Start

```python
from containment_utils import (
    NetworkContainment, EndpointContainment, IdentityContainment,
    CloudContainment, ApplicationContainment, EmailContainment,
    ContainmentPlaybook, ContainmentAction
)

# Create playbook for incident
playbook = ContainmentPlaybook('INC-2024-001', 'Ransomware Containment')

# Network containment
network = NetworkContainment()
action = network.isolate_host('192.168.1.50', 'WORKSTATION-15', 'Ransomware infection')
playbook.add_action(action)

# Endpoint containment
endpoint = EndpointContainment()
action = endpoint.quarantine_endpoint('WORKSTATION-15', 'edr_api_key')
playbook.add_action(action)

# Identity containment
identity = IdentityContainment()
action = identity.disable_account('jdoe', 'Compromised credentials')
playbook.add_action(action)

# Generate containment report
print(playbook.generate_report())
```

## Usage

### Network Containment: Host Isolation

Isolate a compromised host from the network.

**Example**:
```python
from containment_utils import NetworkContainment, ContainmentPlaybook

playbook = ContainmentPlaybook('INC-2024-001', 'Host Isolation')
network = NetworkContainment()

# Full network isolation
action = network.isolate_host(
    ip_address='192.168.1.50',
    hostname='WORKSTATION-15',
    reason='Active malware infection',
    isolation_type='full',  # full, partial, or monitor
    allow_list=['192.168.1.10']  # Allow IR team access
)

playbook.add_action(action)
print(f"Status: {action.status}")
print(f"Commands: {action.commands}")
```

### Network Containment: Firewall Block

Block malicious IPs, domains, or ports.

**Example**:
```python
from containment_utils import NetworkContainment

network = NetworkContainment()

# Block malicious IP
action = network.firewall_block(
    target='198.51.100.1',
    target_type='ip',
    direction='both',  # inbound, outbound, both
    reason='C2 server',
    duration_hours=24
)

# Block malicious domain
action = network.firewall_block(
    target='evil-domain.com',
    target_type='domain',
    direction='outbound',
    reason='Malware distribution site'
)

# Block port range
action = network.firewall_block(
    target='4444-4450',
    target_type='port',
    direction='both',
    reason='Common backdoor ports'
)

print(action.generate_firewall_rules())
```

### Network Containment: DNS Sinkholing

Redirect malicious domains to a sinkhole.

**Example**:
```python
from containment_utils import NetworkContainment

network = NetworkContainment()

malicious_domains = [
    'malware-c2.com',
    'data-exfil.net',
    'phishing-site.org'
]

action = network.dns_sinkhole(
    domains=malicious_domains,
    sinkhole_ip='10.0.0.100',  # Internal sinkhole server
    reason='Active C2 domains',
    log_queries=True
)

print(f"Domains sinkholed: {len(action.targets)}")
print(f"DNS config: {action.dns_config}")
```

### Network Containment: Network Segmentation

Implement emergency network segmentation.

**Example**:
```python
from containment_utils import NetworkContainment

network = NetworkContainment()

action = network.segment_network(
    source_vlan=100,  # Compromised VLAN
    target_vlan=999,  # Quarantine VLAN
    affected_hosts=['192.168.1.50', '192.168.1.51', '192.168.1.52'],
    allow_ir_access=True,
    ir_subnet='10.0.100.0/24'
)

print(f"VLAN changes: {action.vlan_config}")
print(f"ACL rules: {action.acl_rules}")
```

### Endpoint Containment: EDR Quarantine

Quarantine endpoint using EDR platform.

**Example**:
```python
from containment_utils import EndpointContainment

endpoint = EndpointContainment()

action = endpoint.quarantine_endpoint(
    hostname='WORKSTATION-15',
    edr_platform='crowdstrike',  # crowdstrike, sentinelone, defender, carbon_black
    isolation_level='full',  # full, selective
    allow_list=['10.0.100.0/24'],  # IR team subnet
    preserve_evidence=True
)

print(f"EDR API call: {action.api_payload}")
print(f"Isolation status: {action.status}")
```

### Endpoint Containment: Process Termination

Terminate malicious processes.

**Example**:
```python
from containment_utils import EndpointContainment

endpoint = EndpointContainment()

action = endpoint.terminate_process(
    hostname='WORKSTATION-15',
    process_name='malware.exe',
    process_id=1234,
    kill_children=True,  # Also kill child processes
    create_memory_dump=True  # Preserve for forensics
)

print(f"Commands: {action.commands}")
print(f"Evidence preserved: {action.evidence_path}")
```

### Endpoint Containment: Service Disable

Disable malicious or compromised services.

**Example**:
```python
from containment_utils import EndpointContainment

endpoint = EndpointContainment()

action = endpoint.disable_service(
    hostname='SERVER-01',
    service_name='MaliciousService',
    stop_immediately=True,
    disable_autostart=True,
    backup_config=True
)

print(f"Service status: {action.status}")
print(f"Rollback info: {action.rollback_commands}")
```

### Endpoint Containment: Memory Preservation

Capture memory for forensic analysis before containment.

**Example**:
```python
from containment_utils import EndpointContainment

endpoint = EndpointContainment()

action = endpoint.preserve_memory(
    hostname='WORKSTATION-15',
    output_path='/evidence/INC-2024-001/',
    tool='winpmem',  # winpmem, dumpit, magnet_ram
    compress=True,
    hash_output=True
)

print(f"Memory dump: {action.output_file}")
print(f"Hash: {action.file_hash}")
print(f"Chain of custody: {action.custody_record}")
```

### Identity Containment: Account Disable

Disable compromised user accounts.

**Example**:
```python
from containment_utils import IdentityContainment

identity = IdentityContainment()

action = identity.disable_account(
    username='jdoe',
    reason='Account compromised in phishing attack',
    directory='active_directory',  # active_directory, azure_ad, okta, google
    preserve_data=True,
    notify_manager=True
)

print(f"Account status: {action.status}")
print(f"LDAP command: {action.commands}")
```

### Identity Containment: Session Termination

Terminate all active sessions for a user.

**Example**:
```python
from containment_utils import IdentityContainment

identity = IdentityContainment()

action = identity.terminate_sessions(
    username='jdoe',
    session_types=['all'],  # all, vpn, rdp, web, cloud
    force=True,
    invalidate_tokens=True
)

print(f"Sessions terminated: {action.session_count}")
print(f"Tokens invalidated: {action.tokens_invalidated}")
```

### Identity Containment: Password Reset

Force password reset for compromised accounts.

**Example**:
```python
from containment_utils import IdentityContainment

identity = IdentityContainment()

action = identity.force_password_reset(
    username='jdoe',
    require_mfa_reenroll=True,
    expire_immediately=True,
    notify_user=True,
    generate_temp_password=True
)

print(f"Temp password: {action.temp_password}")  # Securely transmitted
print(f"MFA status: {action.mfa_status}")
```

### Identity Containment: Service Account Rotation

Rotate compromised service account credentials.

**Example**:
```python
from containment_utils import IdentityContainment

identity = IdentityContainment()

action = identity.rotate_service_account(
    account_name='svc_backup',
    credential_type='password',  # password, api_key, certificate
    update_dependent_services=True,
    services=['BackupService', 'ScheduledTask1']
)

print(f"New credential generated: {action.credential_rotated}")
print(f"Services updated: {action.services_updated}")
```

### Cloud Containment: IAM Revocation

Revoke cloud IAM permissions.

**Example**:
```python
from containment_utils import CloudContainment

cloud = CloudContainment()

action = cloud.revoke_iam_permissions(
    principal='arn:aws:iam::123456789:user/compromised-user',
    cloud_provider='aws',  # aws, azure, gcp
    revocation_type='all',  # all, specific
    preserve_audit_logs=True
)

print(f"Policies detached: {action.policies_removed}")
print(f"Access keys disabled: {action.keys_disabled}")
```

### Cloud Containment: Resource Isolation

Isolate compromised cloud resources.

**Example**:
```python
from containment_utils import CloudContainment

cloud = CloudContainment()

action = cloud.isolate_resource(
    resource_id='i-0123456789abcdef0',
    resource_type='ec2_instance',
    cloud_provider='aws',
    isolation_method='security_group',  # security_group, nacl, vpc
    allow_forensic_access=True,
    forensic_ip='10.0.100.50'
)

print(f"Security group: {action.security_group_id}")
print(f"Isolation rules: {action.isolation_rules}")
```

### Cloud Containment: API Key Revocation

Revoke compromised API keys and tokens.

**Example**:
```python
from containment_utils import CloudContainment

cloud = CloudContainment()

action = cloud.revoke_api_keys(
    key_ids=['AKIA1234567890ABCDEF'],
    cloud_provider='aws',
    create_new_keys=False,  # Don't auto-create replacements
    notify_owner=True
)

print(f"Keys revoked: {action.keys_revoked}")
print(f"Affected services: {action.affected_services}")
```

### Cloud Containment: Security Group Lockdown

Emergency security group modifications.

**Example**:
```python
from containment_utils import CloudContainment

cloud = CloudContainment()

action = cloud.lockdown_security_group(
    security_group_id='sg-0123456789abcdef0',
    cloud_provider='aws',
    lockdown_type='deny_all',  # deny_all, allow_ir_only, block_egress
    ir_cidrs=['10.0.100.0/24'],
    preserve_logging=True
)

print(f"Rules removed: {action.rules_removed}")
print(f"New rules: {action.new_rules}")
```

### Application Containment: WAF Rules

Deploy emergency WAF rules.

**Example**:
```python
from containment_utils import ApplicationContainment

app = ApplicationContainment()

action = app.deploy_waf_rule(
    rule_name='Block_SQLi_Attack',
    rule_type='block',  # block, rate_limit, challenge
    conditions=[
        {'field': 'uri', 'operator': 'contains', 'value': '/api/search'},
        {'field': 'body', 'operator': 'regex', 'value': r'(union|select|insert)'}
    ],
    waf_provider='cloudflare',  # cloudflare, aws_waf, akamai
    priority=1
)

print(f"Rule ID: {action.rule_id}")
print(f"WAF config: {action.waf_config}")
```

### Application Containment: Rate Limiting

Implement emergency rate limiting.

**Example**:
```python
from containment_utils import ApplicationContainment

app = ApplicationContainment()

action = app.rate_limit(
    endpoint='/api/login',
    limit=10,  # Requests per window
    window_seconds=60,
    action='block',  # block, throttle, challenge
    scope='ip',  # ip, user, global
    whitelist=['10.0.0.0/8']
)

print(f"Rate limit config: {action.config}")
```

### Application Containment: Service Shutdown

Emergency application service shutdown.

**Example**:
```python
from containment_utils import ApplicationContainment

app = ApplicationContainment()

action = app.shutdown_service(
    service_name='payment-api',
    shutdown_type='graceful',  # graceful, immediate
    drain_connections=True,
    display_maintenance_page=True,
    notify_stakeholders=['security@company.com', 'oncall@company.com']
)

print(f"Service status: {action.status}")
print(f"Connections drained: {action.connections_drained}")
```

### Application Containment: Database Lockdown

Lock down database access.

**Example**:
```python
from containment_utils import ApplicationContainment

app = ApplicationContainment()

action = app.lockdown_database(
    database='production_db',
    db_type='postgresql',  # postgresql, mysql, mssql, mongodb
    lockdown_level='read_only',  # read_only, admin_only, full_lockdown
    revoke_users=['app_user', 'report_user'],
    preserve_admin=['dba_admin']
)

print(f"Users revoked: {action.users_revoked}")
print(f"Rollback script: {action.rollback_script}")
```

### Email Containment: Message Quarantine

Quarantine malicious emails.

**Example**:
```python
from containment_utils import EmailContainment

email = EmailContainment()

action = email.quarantine_messages(
    search_criteria={
        'sender': 'attacker@malicious.com',
        'subject_contains': 'Invoice',
        'date_range': ('2024-01-15', '2024-01-16')
    },
    email_platform='office365',  # office365, google, exchange
    delete_from_mailboxes=True,
    preserve_for_analysis=True
)

print(f"Messages quarantined: {action.message_count}")
print(f"Affected users: {action.affected_users}")
```

### Email Containment: Sender Block

Block malicious senders.

**Example**:
```python
from containment_utils import EmailContainment

email = EmailContainment()

action = email.block_sender(
    sender='attacker@malicious.com',
    block_type='domain',  # email, domain
    email_platform='office365',
    add_to_threat_list=True
)

print(f"Block rule: {action.block_rule}")
```

### Email Containment: Inbox Rule Removal

Remove malicious inbox rules.

**Example**:
```python
from containment_utils import EmailContainment

email = EmailContainment()

action = email.remove_inbox_rules(
    username='jdoe',
    rule_criteria={
        'forwards_externally': True,
        'deletes_messages': True
    },
    email_platform='office365'
)

print(f"Rules removed: {action.rules_removed}")
print(f"Rule details: {action.rule_details}")
```

### Playbook Management

Track and document containment actions.

**Example**:
```python
from containment_utils import ContainmentPlaybook, ContainmentAction

# Create playbook
playbook = ContainmentPlaybook(
    incident_id='INC-2024-001',
    name='Ransomware Containment',
    analyst='analyst1'
)

# Execute containment actions
# ... (use containment utilities as shown above)

# Mark action complete
playbook.complete_action(action.id, 'Successfully isolated host')

# Mark action failed with rollback
playbook.fail_action(action.id, 'Isolation failed', rollback=True)

# Generate reports
print(playbook.generate_report())
print(playbook.generate_executive_summary())

# Export to JSON for SOAR integration
print(playbook.to_json())
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CONTAINMENT_LOG_PATH` | Log file path | No | `./containment.log` |
| `EDR_API_KEY` | EDR platform API key | For EDR actions | - |
| `CLOUD_CREDENTIALS` | Cloud provider credentials | For cloud actions | - |

### Rollback Configuration

All containment actions support rollback:

```python
# Get rollback commands
rollback = action.get_rollback()
print(rollback.commands)

# Execute rollback
rollback.execute()
```

## Limitations

- **No Direct Execution**: Generates commands/configs, does not execute directly
- **API Integration**: Requires API credentials for platform-specific actions
- **Network Dependencies**: Some actions require network connectivity to targets
- **Permission Requirements**: Actions require appropriate administrative permissions

## Troubleshooting

### Action Failed to Execute

**Problem**: Containment action reports failure

**Solution**: Check permissions and connectivity:
```python
# Verify connectivity
action = network.verify_connectivity(target_ip)
print(action.reachable)

# Check required permissions
print(action.required_permissions)
```

### Rollback Not Available

**Problem**: Cannot rollback a containment action

**Solution**: Some destructive actions cannot be rolled back:
```python
if action.rollback_available:
    action.rollback()
else:
    print(f"Manual intervention required: {action.rollback_instructions}")
```

## Related Skills

- [detection](../detection/): Detect threats to contain
- [incident-response](../incident-response/): Full IR workflow
- [remediation](../remediation/): Post-containment cleanup
- [soc-operations](../soc-operations/): Alert triage

## References

- [Detailed API Reference](references/REFERENCE.md)
- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [SANS Incident Handler's Handbook](https://www.sans.org/white-papers/33901/)
