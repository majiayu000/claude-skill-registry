---
name: threat-intelligence
description: |
  Cyber Threat Intelligence gathering, IOC extraction, threat analysis, and
  intelligence reporting. Process threat data and produce actionable intelligence.
  Use for CTI work, threat research, and intelligence dissemination.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: requests for feed fetching
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: cybersecurity
---

# Threat Intelligence Skill

Gather, analyze, and disseminate cyber threat intelligence with IOC extraction, threat actor profiling, and MITRE ATT&CK mapping.

## Capabilities

- **IOC Extraction**: Extract indicators from text, logs, and reports
- **IOC Management**: Deduplicate, validate, and enrich indicators
- **Threat Profiling**: Document threat actors and campaigns
- **ATT&CK Mapping**: Map threats to MITRE ATT&CK framework
- **Intelligence Reports**: Generate threat bulletins and assessments
- **Feed Processing**: Parse and normalize threat feeds

## Quick Start

```python
from cti_utils import IOCExtractor, ThreatActor, IntelReport

# Extract IOCs from text
extractor = IOCExtractor()
iocs = extractor.extract_from_text('''
Malware connects to 192.168.1.100 and evil.com.
Hash: d41d8cd98f00b204e9800998ecf8427e
''')
print(iocs)

# Document threat actor
actor = ThreatActor('APT29', aliases=['Cozy Bear', 'The Dukes'])
actor.add_ttp('T1566', 'Phishing')
actor.set_motivation('espionage')

# Generate intel report
report = IntelReport('Emerging Ransomware Campaign')
report.add_ioc('ip', '10.0.0.1', 'C2 server')
print(report.generate())
```

## Usage

### IOC Extraction

Extract indicators of compromise from various text sources.

**Example**:
```python
from cti_utils import IOCExtractor

extractor = IOCExtractor()

# Extract from text
text = '''
The malware was downloaded from hxxp://malware[.]evil[.]com/payload.exe
It connects to C2 server at 192.168.100.50 on port 443.
The file hash is: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4
Email originated from attacker@phishing.com
'''

iocs = extractor.extract_from_text(text)

print(f"IPs: {iocs['ip']}")
print(f"Domains: {iocs['domain']}")
print(f"URLs: {iocs['url']}")
print(f"Hashes: {iocs['hash']}")
print(f"Emails: {iocs['email']}")

# Defang/refang IOCs
defanged = extractor.defang('http://evil.com')  # hxxp://evil[.]com
refanged = extractor.refang('hxxp://evil[.]com')  # http://evil.com

# Validate IOCs
valid = extractor.validate_ioc('ip', '192.168.1.1')  # True
invalid = extractor.validate_ioc('ip', '999.999.999.999')  # False
```

### IOC Management

Manage collections of indicators with context.

**Example**:
```python
from cti_utils import IOCCollection

collection = IOCCollection('Campaign-2024-001')

# Add IOCs with context
collection.add_ioc(
    ioc_type='ip',
    value='192.168.1.100',
    context='C2 server',
    confidence='high',
    source='Sandbox analysis'
)

collection.add_ioc(
    ioc_type='domain',
    value='malware.evil.com',
    context='Payload delivery',
    confidence='medium',
    source='Network logs'
)

collection.add_ioc(
    ioc_type='hash',
    value='a1b2c3d4e5f6...',
    context='Ransomware executable',
    confidence='high',
    source='EDR'
)

# Deduplicate
collection.deduplicate()

# Export formats
print(collection.to_csv())
print(collection.to_json())
print(collection.to_stix())  # STIX 2.1 format
```

### Threat Actor Profiling

Document threat actors and their characteristics.

**Example**:
```python
from cti_utils import ThreatActor

actor = ThreatActor(
    name='APT29',
    aliases=['Cozy Bear', 'The Dukes', 'YTTRIUM']
)

# Set attributes
actor.set_motivation('espionage')
actor.set_sophistication('advanced')
actor.set_origin('Russia')

# Add TTPs (MITRE ATT&CK)
actor.add_ttp('T1566.001', 'Spearphishing Attachment')
actor.add_ttp('T1059.001', 'PowerShell')
actor.add_ttp('T1071.001', 'Web Protocols')
actor.add_ttp('T1486', 'Data Encrypted for Impact')

# Add targeting
actor.add_target_sector('Government')
actor.add_target_sector('Healthcare')
actor.add_target_region('North America')
actor.add_target_region('Europe')

# Add tools
actor.add_tool('Cobalt Strike')
actor.add_tool('Mimikatz')

# Add infrastructure
actor.add_infrastructure('ip', '192.168.1.100', 'C2 server')
actor.add_infrastructure('domain', 'actor-c2.com', 'Primary C2')

# Generate profile
print(actor.generate_profile())
```

### Campaign Tracking

Track threat campaigns over time.

**Example**:
```python
from cti_utils import Campaign

campaign = Campaign(
    name='Operation DarkSide',
    first_seen='2024-01-01',
    threat_actor='APT29'
)

# Add campaign details
campaign.set_description('''
Targeted campaign against financial institutions using
spearphishing emails with malicious Excel attachments.
''')

campaign.set_objective('Financial theft and espionage')

# Add IOCs
campaign.add_ioc('domain', 'campaign-c2.evil.com')
campaign.add_ioc('hash', 'abc123...', 'Excel dropper')

# Add TTPs
campaign.add_ttp('T1566.001', 'Initial access via phishing')
campaign.add_ttp('T1059.005', 'VBA macro execution')

# Add targets
campaign.add_target('Financial Services', 'North America')

# Timeline events
campaign.add_event('2024-01-01', 'First phishing emails observed')
campaign.add_event('2024-01-05', 'New C2 infrastructure identified')
campaign.add_event('2024-01-10', 'Malware variant updated')

# Generate report
print(campaign.generate_report())
```

### MITRE ATT&CK Mapping

Map threats to the ATT&CK framework.

**Example**:
```python
from cti_utils import ATTACKMapper

mapper = ATTACKMapper()

# Map techniques
mapper.add_technique('T1566.001', 'Spearphishing used for initial access')
mapper.add_technique('T1059.001', 'PowerShell scripts executed')
mapper.add_technique('T1055', 'Process injection observed')
mapper.add_technique('T1486', 'Files encrypted with ransomware')

# Generate matrix view
print(mapper.generate_matrix())

# Get technique details
print(mapper.get_technique_info('T1566.001'))

# Export for ATT&CK Navigator
mapper.export_navigator('attack_layer.json')
```

### Intelligence Reports

Generate threat intelligence reports.

**Example**:
```python
from cti_utils import IntelReport

report = IntelReport(
    title='Emerging Ransomware Campaign Targeting Healthcare',
    classification='TLP:AMBER'
)

# Executive summary
report.set_summary('''
A new ransomware campaign has been identified targeting healthcare
organizations in North America. The campaign uses phishing emails
with malicious attachments to gain initial access.
''')

# Key findings
report.add_finding('New ransomware variant identified: "MedLocker"')
report.add_finding('Campaign active since January 2024')
report.add_finding('At least 5 healthcare organizations targeted')

# Add IOCs
report.add_ioc('hash', 'abc123...', 'Ransomware executable')
report.add_ioc('domain', 'medlocker-payment.onion', 'Payment portal')
report.add_ioc('ip', '192.168.1.100', 'C2 server')

# Add TTPs
report.add_ttp('T1566.001', 'Phishing with malicious attachments')
report.add_ttp('T1486', 'Data encryption')

# Recommendations
report.add_recommendation('Block IOCs at perimeter')
report.add_recommendation('Update endpoint detection signatures')
report.add_recommendation('Conduct phishing awareness training')

# Generate outputs
print(report.generate())
print(report.generate_executive_brief())
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CTI_FEED_API_KEY` | API key for threat feeds | No | None |
| `CTI_OUTPUT_DIR` | Output directory for reports | No | `./output` |

## Supported IOC Types

- **ip** - IPv4 and IPv6 addresses
- **domain** - Domain names
- **url** - Full URLs
- **hash** - MD5, SHA1, SHA256 hashes
- **email** - Email addresses
- **cve** - CVE identifiers

## Limitations

- **No Live Feeds**: Feed fetching requires manual configuration
- **Offline ATT&CK**: Uses embedded technique data
- **No Enrichment APIs**: External enrichment not included

## Troubleshooting

### Invalid IOC Format

IOC validation uses standard regex patterns:
```python
# Valid
extractor.validate_ioc('ip', '192.168.1.1')  # True

# Invalid
extractor.validate_ioc('ip', '192.168.1.256')  # False
```

### Defanging Issues

Use consistent defanging format:
```python
# Standard defanging
extractor.defang('http://evil.com')
# Returns: hxxp://evil[.]com
```

## Related Skills

- [incident-response](../incident-response/): Apply CTI during incidents
- [soc-operations](../soc-operations/): CTI-informed detection
- [research](../../baseline/research/): General research capabilities

## References

- [Detailed API Reference](references/REFERENCE.md)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [STIX 2.1 Specification](https://oasis-open.github.io/cti-documentation/)
