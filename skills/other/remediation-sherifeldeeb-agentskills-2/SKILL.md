---
name: remediation
description: |
  Security incident remediation playbooks for removing threats, restoring systems,
  and recovering from incidents. Use for post-containment cleanup, system recovery,
  and returning to normal operations.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - No external dependencies (standard library only)
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: cybersecurity
---

# Remediation Playbooks Skill

Comprehensive remediation procedures for removing security threats, restoring systems, and recovering from incidents. Provides structured playbooks for malware removal, credential reset, system rebuild, and data recovery.

## Capabilities

- **Malware Remediation**: Malware removal, ransomware recovery, rootkit removal, web shell cleanup
- **Access Remediation**: Credential reset, backdoor removal, privilege cleanup, golden ticket remediation
- **System Remediation**: System rebuild, patch deployment, configuration hardening, log recovery
- **Data Remediation**: Data breach response, backup restoration, integrity verification, PII exposure handling
- **Cloud Remediation**: Cloud account recovery, IAM cleanup, S3 security fixes, container remediation
- **Business Remediation**: BEC recovery, vendor compromise cleanup, supply chain remediation
- **Playbook Execution**: Track and document remediation progress

## Quick Start

```python
from remediation_utils import (
    MalwareRemediation, AccessRemediation, SystemRemediation,
    DataRemediation, CloudRemediation, BusinessRemediation,
    RemediationPlaybook
)

# Create playbook for incident
playbook = RemediationPlaybook('INC-2024-001', 'Ransomware Recovery')

# Malware removal
malware = MalwareRemediation()
action = malware.remove_malware(
    hostname='WORKSTATION-15',
    malware_type='ransomware',
    malware_artifacts=['/temp/payload.exe', 'HKLM\\...\\Run\\malware']
)
playbook.add_action(action)

# System rebuild
system = SystemRemediation()
action = system.rebuild_system('WORKSTATION-15', 'windows_11', preserve_data=False)
playbook.add_action(action)

# Generate remediation report
print(playbook.generate_report())
```

## Usage

### Malware Remediation: Remove Malware

Remove malware from infected system.

**Example**:
```python
from remediation_utils import MalwareRemediation, RemediationPlaybook

playbook = RemediationPlaybook('INC-2024-001', 'Malware Removal')
malware = MalwareRemediation()

# Define malware artifacts discovered during investigation
artifacts = {
    'files': [
        'C:\\Users\\Public\\payload.exe',
        'C:\\Windows\\Temp\\dropper.dll',
        'C:\\ProgramData\\backdoor.exe'
    ],
    'registry': [
        'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\malware',
        'HKCU\\Software\\Classes\\CLSID\\{malicious-guid}'
    ],
    'scheduled_tasks': ['SystemUpdate', 'WindowsDefenderUpdate'],
    'services': ['MaliciousService'],
    'processes': ['payload.exe', 'backdoor.exe']
}

action = malware.remove_malware(
    hostname='WORKSTATION-15',
    malware_type='trojan',
    malware_artifacts=artifacts,
    quarantine_before_delete=True,
    scan_after_removal=True
)

playbook.add_action(action)
print(f"Removal commands: {action.commands}")
print(f"Verification steps: {action.verification_steps}")
```

### Malware Remediation: Ransomware Recovery

Recover from ransomware infection.

**Example**:
```python
from remediation_utils import MalwareRemediation

malware = MalwareRemediation()

action = malware.ransomware_recovery(
    hostname='FILESERVER-01',
    ransomware_family='lockbit',
    encrypted_extensions=['.lockbit', '.encrypted'],
    recovery_method='backup',  # backup, decryptor, shadow_copies
    backup_location='\\\\backup-server\\fileserver-01\\latest',
    verify_decryption=True
)

print(f"Recovery steps: {action.recovery_steps}")
print(f"Data validation: {action.validation_steps}")
```

### Malware Remediation: Rootkit Removal

Remove rootkits and bootkits.

**Example**:
```python
from remediation_utils import MalwareRemediation

malware = MalwareRemediation()

action = malware.rootkit_removal(
    hostname='SERVER-01',
    rootkit_type='kernel',  # kernel, bootkit, firmware
    detection_tool='gmer',
    offline_scan=True,
    rebuild_mbr=True
)

print(f"Removal procedure: {action.commands}")
print(f"Verification: {action.verification_steps}")
```

### Malware Remediation: Web Shell Removal

Remove web shells from compromised servers.

**Example**:
```python
from remediation_utils import MalwareRemediation

malware = MalwareRemediation()

webshells = [
    '/var/www/html/uploads/shell.php',
    '/var/www/html/images/cmd.php',
    '/var/www/html/includes/backdoor.php'
]

action = malware.webshell_removal(
    hostname='WEBSERVER-01',
    webshell_paths=webshells,
    web_root='/var/www/html',
    scan_for_additional=True,
    patch_upload_vulnerability=True,
    restore_from_clean=True
)

print(f"Files removed: {action.metadata['files_removed']}")
print(f"Integrity check: {action.verification_steps}")
```

### Access Remediation: Full Credential Reset

Perform comprehensive credential reset after breach.

**Example**:
```python
from remediation_utils import AccessRemediation

access = AccessRemediation()

action = access.full_credential_reset(
    scope='domain',  # domain, local, cloud, all
    users=['jdoe', 'admin', 'svc_backup'],
    reset_types=['password', 'kerberos', 'certificates'],
    force_mfa_reenroll=True,
    expire_all_sessions=True,
    notify_users=True
)

print(f"Reset commands: {action.commands}")
print(f"Users affected: {len(action.metadata['users'])}")
```

### Access Remediation: Backdoor Removal

Remove attacker persistence and backdoors.

**Example**:
```python
from remediation_utils import AccessRemediation

access = AccessRemediation()

backdoors = {
    'accounts': ['backdoor_admin', 'support_temp'],
    'ssh_keys': ['/root/.ssh/authorized_keys'],
    'scheduled_tasks': ['WindowsUpdate2', 'SystemMaintenance'],
    'services': ['RemoteSupport', 'WindowsDefenderUpdate'],
    'registry': ['HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\Update'],
    'web_shells': ['/var/www/html/admin.php'],
    'cron_jobs': ['/etc/cron.d/update']
}

action = access.backdoor_removal(
    hostname='SERVER-01',
    backdoors=backdoors,
    audit_all_persistence=True,
    compare_to_baseline=True
)

print(f"Backdoors removed: {action.metadata['removed_count']}")
print(f"Audit results: {action.audit_results}")
```

### Access Remediation: Privilege Escalation Cleanup

Clean up after privilege escalation attack.

**Example**:
```python
from remediation_utils import AccessRemediation

access = AccessRemediation()

action = access.privilege_cleanup(
    affected_accounts=['compromised_user'],
    unauthorized_groups=['Domain Admins', 'Enterprise Admins'],
    unauthorized_permissions=['SeDebugPrivilege', 'SeTcbPrivilege'],
    reset_to_baseline=True,
    audit_privileged_groups=True
)

print(f"Groups cleaned: {action.metadata['groups_cleaned']}")
print(f"Permissions revoked: {action.metadata['permissions_revoked']}")
```

### Access Remediation: Golden Ticket Remediation

Remediate Kerberos golden ticket attack.

**Example**:
```python
from remediation_utils import AccessRemediation

access = AccessRemediation()

action = access.golden_ticket_remediation(
    domain='corp.example.com',
    reset_krbtgt=True,  # Critical: Reset twice
    reset_interval_hours=10,
    force_all_ticket_renewal=True,
    audit_service_accounts=True
)

print(f"KRBTGT reset status: {action.metadata['krbtgt_reset']}")
print(f"Wait time before second reset: {action.metadata['wait_hours']} hours")
```

### System Remediation: System Rebuild

Rebuild compromised system from scratch.

**Example**:
```python
from remediation_utils import SystemRemediation

system = SystemRemediation()

action = system.rebuild_system(
    hostname='WORKSTATION-15',
    os_version='windows_11_enterprise',
    image_source='gold_image',
    preserve_data=False,  # Data already backed up
    join_domain=True,
    apply_security_baseline=True,
    install_edr=True
)

print(f"Rebuild steps: {action.commands}")
print(f"Post-rebuild checklist: {action.verification_steps}")
```

### System Remediation: Emergency Patching

Deploy emergency security patches.

**Example**:
```python
from remediation_utils import SystemRemediation

system = SystemRemediation()

action = system.emergency_patching(
    targets=['WEBSERVER-01', 'WEBSERVER-02', 'APPSERVER-01'],
    patches=['KB5012345', 'CVE-2024-1234'],
    patch_source='wsus',  # wsus, sccm, manual
    reboot_allowed=True,
    verify_after_patch=True,
    rollback_on_failure=True
)

print(f"Patching plan: {action.commands}")
print(f"Verification: {action.verification_steps}")
```

### System Remediation: Configuration Hardening

Apply security hardening after incident.

**Example**:
```python
from remediation_utils import SystemRemediation

system = SystemRemediation()

action = system.configuration_hardening(
    hostname='SERVER-01',
    baseline='cis_level_1',  # cis_level_1, cis_level_2, disa_stig, custom
    focus_areas=['authentication', 'network', 'logging', 'services'],
    disable_legacy_protocols=True,
    enable_advanced_audit=True
)

print(f"Hardening steps: {action.commands}")
print(f"Compliance score: {action.metadata['compliance_score']}")
```

### System Remediation: Log Recovery

Recover and restore audit logs.

**Example**:
```python
from remediation_utils import SystemRemediation

system = SystemRemediation()

action = system.log_recovery(
    hostname='SERVER-01',
    log_types=['security', 'system', 'application', 'powershell'],
    recovery_sources=['backup', 'siem', 'shadow_copy'],
    time_range=('2024-01-10', '2024-01-15'),
    verify_integrity=True
)

print(f"Logs recovered: {action.metadata['logs_recovered']}")
print(f"Integrity status: {action.metadata['integrity_verified']}")
```

### Data Remediation: Data Breach Response

Execute data breach response procedures.

**Example**:
```python
from remediation_utils import DataRemediation

data = DataRemediation()

action = data.breach_response(
    breach_type='pii_exposure',
    affected_data_types=['ssn', 'credit_card', 'medical_records'],
    affected_record_count=50000,
    notification_required=True,
    regulatory_requirements=['gdpr', 'hipaa', 'ccpa'],
    legal_hold=True
)

print(f"Response steps: {action.commands}")
print(f"Notification timeline: {action.metadata['notification_timeline']}")
print(f"Regulatory requirements: {action.metadata['regulatory_actions']}")
```

### Data Remediation: Backup Restoration

Restore data from backups.

**Example**:
```python
from remediation_utils import DataRemediation

data = DataRemediation()

action = data.backup_restoration(
    target_system='FILESERVER-01',
    backup_source='\\\\backup\\fileserver-01\\2024-01-14',
    restore_type='full',  # full, incremental, selective
    restore_paths=['/data/finance', '/data/hr'],
    verify_after_restore=True,
    scan_before_restore=True  # Scan backup for malware
)

print(f"Restoration steps: {action.commands}")
print(f"Verification: {action.verification_steps}")
```

### Data Remediation: Integrity Verification

Verify data integrity after incident.

**Example**:
```python
from remediation_utils import DataRemediation

data = DataRemediation()

action = data.integrity_verification(
    target_paths=['/data/critical', '/app/config'],
    baseline_hashes='/security/baselines/file_hashes.json',
    verification_method='sha256',
    report_modifications=True,
    quarantine_suspicious=True
)

print(f"Files verified: {action.metadata['files_checked']}")
print(f"Modifications found: {action.metadata['modifications']}")
```

### Cloud Remediation: Cloud Account Recovery

Recover compromised cloud account.

**Example**:
```python
from remediation_utils import CloudRemediation

cloud = CloudRemediation()

action = cloud.account_recovery(
    cloud_provider='aws',
    account_id='123456789012',
    compromised_resources=['iam_users', 'access_keys', 'roles'],
    reset_all_credentials=True,
    audit_cloudtrail=True,
    enable_guardduty=True
)

print(f"Recovery steps: {action.commands}")
print(f"Resources remediated: {action.metadata['resources_remediated']}")
```

### Cloud Remediation: IAM Policy Remediation

Fix IAM policy misconfigurations.

**Example**:
```python
from remediation_utils import CloudRemediation

cloud = CloudRemediation()

action = cloud.iam_remediation(
    cloud_provider='aws',
    issues=[
        {'type': 'overly_permissive', 'resource': 'arn:aws:iam::*:user/admin'},
        {'type': 'public_access', 'resource': 'arn:aws:s3:::public-bucket'},
        {'type': 'unused_credentials', 'resource': 'AKIA...'}
    ],
    apply_least_privilege=True,
    remove_unused_permissions=True
)

print(f"Policies fixed: {action.metadata['policies_fixed']}")
```

### Cloud Remediation: S3 Bucket Remediation

Fix S3 bucket security issues.

**Example**:
```python
from remediation_utils import CloudRemediation

cloud = CloudRemediation()

action = cloud.s3_remediation(
    bucket_name='sensitive-data-bucket',
    issues=['public_access', 'no_encryption', 'no_versioning', 'no_logging'],
    block_public_access=True,
    enable_encryption='aws:kms',
    enable_versioning=True,
    enable_access_logging=True
)

print(f"Remediation applied: {action.metadata['fixes_applied']}")
```

### Cloud Remediation: Container Image Remediation

Remediate compromised container images.

**Example**:
```python
from remediation_utils import CloudRemediation

cloud = CloudRemediation()

action = cloud.container_remediation(
    registry='ecr',
    images=['app-api:latest', 'app-web:latest'],
    issues=['vulnerability', 'malware', 'misconfig'],
    rebuild_from_source=True,
    scan_before_deploy=True,
    update_base_images=True
)

print(f"Images remediated: {action.metadata['images_fixed']}")
```

### Business Remediation: BEC Recovery

Recover from Business Email Compromise.

**Example**:
```python
from remediation_utils import BusinessRemediation

business = BusinessRemediation()

action = business.bec_recovery(
    incident_type='invoice_fraud',
    financial_impact=150000,
    compromised_accounts=['cfo@company.com', 'ap@company.com'],
    fraudulent_transactions=['TXN-12345', 'TXN-12346'],
    bank_notification=True,
    law_enforcement=True
)

print(f"Recovery steps: {action.commands}")
print(f"Financial recovery: {action.metadata['recovery_actions']}")
```

### Business Remediation: Vendor Compromise Response

Respond to compromised vendor/third-party.

**Example**:
```python
from remediation_utils import BusinessRemediation

business = BusinessRemediation()

action = business.vendor_compromise_response(
    vendor_name='Software Vendor Inc',
    compromise_type='supply_chain',
    affected_products=['vendor-sdk-1.2.3'],
    exposure_assessment=True,
    revoke_access=True,
    communication_plan=True
)

print(f"Response plan: {action.commands}")
print(f"Communication timeline: {action.metadata['communications']}")
```

### Playbook Management

Track and document remediation progress.

**Example**:
```python
from remediation_utils import RemediationPlaybook

# Create playbook
playbook = RemediationPlaybook(
    incident_id='INC-2024-001',
    name='Full System Recovery',
    analyst='senior_analyst'
)

# Add remediation actions
# ... (use remediation utilities as shown above)

# Track progress
playbook.complete_action(action.id, 'Successfully removed malware')
playbook.verify_action(action.id, 'Verified clean via EDR scan')

# Generate reports
print(playbook.generate_report())
print(playbook.generate_recovery_certification())

# Export for documentation
print(playbook.to_json())
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `REMEDIATION_LOG_PATH` | Log file path | No | `./remediation.log` |
| `BACKUP_PATH` | Default backup location | No | `./backups` |
| `BASELINE_PATH` | Security baseline location | No | `./baselines` |

### Verification Settings

All remediation actions include verification steps:

```python
# Get verification status
if action.verification_required:
    print(action.verification_steps)

# Mark verification complete
playbook.verify_action(action.id, 'Verified by EDR scan')
```

## Limitations

- **No Direct Execution**: Generates commands/procedures, does not execute directly
- **Requires Clean Media**: System rebuilds require verified clean installation media
- **Backup Dependencies**: Data restoration requires valid, clean backups
- **Time Requirements**: Full remediation may take hours to days

## Troubleshooting

### Remediation Verification Failed

**Problem**: Post-remediation verification shows issues

**Solution**: Re-run targeted remediation:
```python
# Identify remaining issues
remaining = action.get_verification_failures()
print(f"Remaining issues: {remaining}")

# Create follow-up action
follow_up = malware.remove_malware(hostname, remaining_artifacts)
```

### Backup Restoration Failed

**Problem**: Backup restoration incomplete or corrupt

**Solution**: Try alternative recovery sources:
```python
action = data.backup_restoration(
    target_system='SERVER-01',
    backup_source='alternative_backup',
    restore_type='incremental',
    verify_backup_integrity=True
)
```

## Related Skills

- [containment](../containment/): Contain threats before remediation
- [incident-response](../incident-response/): Full IR workflow
- [detection](../detection/): Detect remaining threats
- [grc](../grc/): Compliance documentation

## References

- [Detailed API Reference](references/REFERENCE.md)
- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [CIS Controls](https://www.cisecurity.org/controls)
