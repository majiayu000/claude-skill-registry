---
name: forensic-reporting
description: |
  Generate professional forensic reports and documentation. Use when creating
  investigation reports, expert witness documentation, executive summaries, or
  technical findings. Supports multiple report formats and compliance requirements.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: reportlab, docx, jinja2
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Forensic Reporting

Comprehensive forensic reporting skill for creating professional investigation reports and documentation. Enables generation of technical reports, executive summaries, expert witness documentation, and compliance-ready deliverables from forensic findings.

## Capabilities

- **Technical Reports**: Generate detailed technical forensic reports
- **Executive Summaries**: Create high-level summaries for management
- **Expert Witness Reports**: Prepare court-ready documentation
- **Incident Reports**: Generate incident response reports
- **Chain of Custody**: Create evidence handling documentation
- **Timeline Reports**: Generate timeline-focused reports
- **IOC Reports**: Create indicator of compromise reports
- **Compliance Reports**: Generate compliance-ready documentation
- **Multi-Format Export**: Export to PDF, DOCX, HTML, Markdown
- **Report Templates**: Use customizable report templates

## Quick Start

```python
from forensic_reporting import ReportGenerator, IncidentReport, TechnicalReport

# Initialize report generator
generator = ReportGenerator(case_id="CASE-2024-001")

# Add findings
generator.add_finding(title="Malware Detected", severity="high", details="...")

# Generate report
report = generator.generate_technical_report()
report.export_pdf("/evidence/reports/technical_report.pdf")
```

## Usage

### Task 1: Technical Forensic Report
**Input**: Forensic findings and analysis results

**Process**:
1. Structure findings
2. Add evidence references
3. Include technical details
4. Generate visualizations
5. Export report

**Output**: Comprehensive technical report

**Example**:
```python
from forensic_reporting import TechnicalReportGenerator

# Initialize report generator
report = TechnicalReportGenerator(
    case_id="CASE-2024-001",
    case_name="Corporate Network Intrusion",
    examiner="John Doe",
    organization="ACME Security"
)

# Set case details
report.set_case_details(
    date_received="2024-01-15",
    date_completed="2024-01-20",
    requesting_party="ACME Corporation",
    subject="Investigation of suspected network intrusion"
)

# Add evidence items
report.add_evidence(
    item_id="EVD-001",
    description="Memory dump from WORKSTATION01",
    hash_sha256="abc123...",
    acquisition_date="2024-01-15",
    acquisition_method="WinPMEM"
)

report.add_evidence(
    item_id="EVD-002",
    description="Disk image from WORKSTATION01",
    hash_sha256="def456...",
    acquisition_date="2024-01-15",
    acquisition_method="FTK Imager"
)

# Add findings
report.add_finding(
    title="Malware Infection Confirmed",
    severity="critical",
    category="malware",
    description="Analysis confirmed presence of Cobalt Strike beacon",
    evidence_refs=["EVD-001", "EVD-002"],
    artifacts=[
        "C:\\Windows\\Temp\\beacon.exe",
        "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Updater"
    ],
    iocs=["203.0.113.50", "evil-c2.example.com"],
    mitre_techniques=["T1059.001", "T1547.001"]
)

report.add_finding(
    title="Credential Access Detected",
    severity="high",
    category="credential_access",
    description="Evidence of Mimikatz execution found in memory",
    evidence_refs=["EVD-001"],
    artifacts=["Process: lsass.exe accessed by unknown process"],
    mitre_techniques=["T1003.001"]
)

# Add timeline
report.add_timeline_event("2024-01-10 10:30", "Initial phishing email received")
report.add_timeline_event("2024-01-10 10:35", "User opened malicious attachment")
report.add_timeline_event("2024-01-10 10:36", "Malware beacon established")
report.add_timeline_event("2024-01-10 14:00", "Credential dumping detected")

# Add analysis methodology
report.add_methodology(
    tools_used=["Volatility 3", "Autopsy", "YARA"],
    techniques=["Memory forensics", "Timeline analysis", "IOC extraction"]
)

# Add conclusions
report.add_conclusion(
    summary="The investigation confirmed a successful intrusion via phishing",
    impact="Critical - credential theft and potential data exfiltration",
    recommendations=[
        "Immediately reset all compromised credentials",
        "Block identified C2 infrastructure",
        "Conduct enterprise-wide threat hunting"
    ]
)

# Generate report
report.generate()

# Export to multiple formats
report.export_pdf("/evidence/reports/technical_report.pdf")
report.export_docx("/evidence/reports/technical_report.docx")
report.export_html("/evidence/reports/technical_report.html")
```

### Task 2: Executive Summary
**Input**: Investigation findings

**Process**:
1. Summarize key findings
2. Highlight business impact
3. Provide recommendations
4. Use non-technical language
5. Generate concise report

**Output**: Executive-level summary

**Example**:
```python
from forensic_reporting import ExecutiveSummaryGenerator

# Initialize executive summary
summary = ExecutiveSummaryGenerator(
    case_id="CASE-2024-001",
    case_name="Security Incident Investigation"
)

# Set header information
summary.set_header(
    prepared_for="Executive Leadership Team",
    prepared_by="Security Incident Response Team",
    date="January 20, 2024",
    classification="Confidential"
)

# Add executive overview
summary.add_overview("""
On January 10, 2024, the Security Operations Center detected suspicious
activity on WORKSTATION01. An investigation was immediately initiated,
confirming a successful cyber intrusion. The attacker gained initial
access via a phishing email and subsequently stole credentials.
""")

# Add key findings
summary.add_key_finding(
    title="Confirmed Security Breach",
    description="An attacker successfully compromised corporate systems",
    impact="High - credential theft confirmed"
)

summary.add_key_finding(
    title="Attack Duration",
    description="The attacker maintained access for approximately 4 hours",
    impact="Medium - limited time window reduced exposure"
)

# Add business impact
summary.add_business_impact(
    affected_systems=["WORKSTATION01", "Potentially others"],
    data_at_risk="Employee credentials, potentially sensitive documents",
    operational_impact="Minimal - contained before widespread damage",
    financial_impact="Estimated $50,000 for incident response and remediation",
    regulatory_impact="Possible notification requirements under GDPR"
)

# Add recommendations
summary.add_recommendation(
    priority="immediate",
    action="Reset all credentials for affected users",
    owner="IT Security",
    timeline="Within 24 hours"
)

summary.add_recommendation(
    priority="short_term",
    action="Implement additional phishing protections",
    owner="IT Security",
    timeline="Within 2 weeks"
)

summary.add_recommendation(
    priority="long_term",
    action="Deploy endpoint detection and response solution",
    owner="IT Infrastructure",
    timeline="Within 90 days"
)

# Add metrics/KPIs
summary.add_metrics(
    detection_time="30 minutes",
    containment_time="4 hours",
    investigation_duration="5 days"
)

# Generate and export
summary.generate()
summary.export_pdf("/evidence/reports/executive_summary.pdf")
summary.export_pptx("/evidence/reports/executive_presentation.pptx")
```

### Task 3: Expert Witness Report
**Input**: Forensic analysis for legal proceedings

**Process**:
1. Document qualifications
2. Describe methodology
3. Present findings objectively
4. Use precise language
5. Prepare for cross-examination

**Output**: Court-ready expert report

**Example**:
```python
from forensic_reporting import ExpertWitnessReport

# Initialize expert witness report
report = ExpertWitnessReport(
    case_number="CV-2024-12345",
    court="United States District Court",
    jurisdiction="Northern District"
)

# Add expert qualifications
report.add_expert_qualifications(
    name="Dr. Jane Smith",
    title="Senior Digital Forensics Examiner",
    organization="Forensic Experts Inc.",
    qualifications=[
        "Ph.D. in Computer Science, specializing in Digital Forensics",
        "20+ years experience in digital forensic investigations",
        "Certified: EnCE, GCFE, CFCE",
        "Published author of 15 peer-reviewed papers on digital forensics"
    ],
    prior_testimony=[
        "Qualified as expert in federal and state courts 50+ times",
        "Testified in matters involving computer intrusion, fraud, IP theft"
    ]
)

# Add scope of engagement
report.add_engagement_scope(
    retained_by="Plaintiff",
    engagement_date="January 15, 2024",
    scope="""
    I was retained to examine digital evidence and provide expert opinion on:
    1. Whether the defendant's computer systems were used to access
       plaintiff's proprietary information
    2. The timing and extent of any unauthorized access
    3. Actions taken to conceal such access
    """,
    materials_reviewed=[
        "Forensic image of defendant's laptop (Evidence Item A)",
        "Server access logs from plaintiff's systems (Evidence Item B)",
        "Network traffic captures (Evidence Item C)"
    ]
)

# Add methodology
report.add_methodology(
    standards="NIST SP 800-86, Scientific Working Group on Digital Evidence",
    tools=[
        "EnCase Forensic 8.11",
        "Volatility Framework 3.0",
        "Autopsy Digital Forensics Platform"
    ],
    procedures="""
    All analysis was conducted on forensically sound copies of the original
    evidence. Hash values were verified before and after analysis to ensure
    integrity. Industry-standard forensic procedures were followed throughout.
    """
)

# Add findings
report.add_finding(
    finding_number=1,
    title="Unauthorized Access Occurred",
    opinion="Certain",
    basis="""
    Based on my analysis of Evidence Items A and B, I determined with a
    reasonable degree of scientific certainty that the defendant's computer
    was used to access plaintiff's proprietary database on multiple occasions.
    """,
    supporting_evidence=[
        "Browser history showing access to plaintiff's internal URL",
        "Downloaded files matching plaintiff's proprietary documents",
        "Timestamps correlating with server access logs"
    ]
)

report.add_finding(
    finding_number=2,
    title="Evidence of Concealment",
    opinion="Highly Probable",
    basis="""
    My analysis revealed evidence of anti-forensic activity designed to
    conceal the unauthorized access, including deleted browser history
    and use of privacy tools.
    """,
    supporting_evidence=[
        "CCleaner execution artifacts found in prefetch",
        "Recovered deleted browser history entries",
        "Timestamps showing activity followed by cleanup"
    ]
)

# Add opinions
report.add_opinion("""
Based on my examination and analysis of the digital evidence, it is my
expert opinion that the defendant used their computer to access plaintiff's
proprietary information without authorization, and subsequently took steps
to conceal this activity.
""")

# Add appendices
report.add_appendix("Technical Analysis Details", "detailed_analysis.pdf")
report.add_appendix("Evidence Inventory", "evidence_list.xlsx")

# Generate report
report.generate()
report.export_pdf("/evidence/reports/expert_witness_report.pdf")
```

### Task 4: Incident Response Report
**Input**: IR findings and actions

**Process**:
1. Document incident details
2. Record response actions
3. Analyze root cause
4. Document lessons learned
5. Generate recommendations

**Output**: IR documentation

**Example**:
```python
from forensic_reporting import IncidentResponseReport

# Initialize IR report
report = IncidentResponseReport(
    incident_id="INC-2024-0042",
    incident_name="Ransomware Attack - ACME Corporation"
)

# Set incident details
report.set_incident_details(
    detection_time="2024-01-10 10:30 UTC",
    declaration_time="2024-01-10 11:00 UTC",
    resolution_time="2024-01-12 16:00 UTC",
    severity="Critical",
    classification="Ransomware",
    affected_systems=["FILE-SERVER-01", "DB-SERVER-02", "25 workstations"],
    affected_users="Approximately 500 users"
)

# Add detection information
report.add_detection(
    detection_source="EDR Alert",
    initial_indicators=[
        "Multiple encryption processes detected",
        "Ransom note file creation",
        "Unusual SMB traffic patterns"
    ],
    first_responder="Jane Doe (SOC Analyst)"
)

# Add response timeline
report.add_response_action(
    timestamp="2024-01-10 11:15",
    action="Network isolation initiated",
    performed_by="Network Team",
    result="Affected servers isolated from network"
)

report.add_response_action(
    timestamp="2024-01-10 12:00",
    action="Forensic evidence collection started",
    performed_by="DFIR Team",
    result="Memory and disk images acquired"
)

report.add_response_action(
    timestamp="2024-01-10 18:00",
    action="Threat actor IOCs blocked at perimeter",
    performed_by="Security Team",
    result="C2 communications blocked"
)

report.add_response_action(
    timestamp="2024-01-11 09:00",
    action="Restoration from backups initiated",
    performed_by="IT Operations",
    result="Clean backups identified and restoration started"
)

# Add root cause analysis
report.add_root_cause_analysis(
    initial_access="Phishing email with malicious attachment",
    attack_vector="Macro-enabled Word document",
    vulnerabilities_exploited=[
        "Lack of email attachment sandboxing",
        "Macros enabled by default",
        "Insufficient network segmentation"
    ],
    timeline_summary="""
    The attacker sent a targeted phishing email to an employee, who opened
    the malicious attachment. The document macro downloaded and executed
    ransomware, which then spread via SMB to accessible file shares.
    """
)

# Add impact assessment
report.add_impact_assessment(
    business_impact="48 hours of partial business disruption",
    data_impact="No confirmed data exfiltration; files encrypted but restored",
    financial_impact="Estimated $250,000 (response, restoration, lost productivity)",
    reputational_impact="Minimal - no public disclosure required"
)

# Add lessons learned
report.add_lesson_learned(
    category="detection",
    lesson="Email gateway did not detect the malicious attachment",
    improvement="Implement advanced email threat protection with sandboxing"
)

report.add_lesson_learned(
    category="response",
    lesson="Network isolation took 45 minutes due to manual process",
    improvement="Implement automated isolation capabilities"
)

# Add recommendations
report.add_recommendation(
    priority="critical",
    recommendation="Disable macros by default enterprise-wide",
    timeline="Immediate"
)

report.add_recommendation(
    priority="high",
    recommendation="Implement network segmentation",
    timeline="30 days"
)

# Generate report
report.generate()
report.export_pdf("/evidence/reports/incident_report.pdf")
```

### Task 5: IOC Report
**Input**: Extracted indicators of compromise

**Process**:
1. Organize IOCs by type
2. Add context and metadata
3. Format for sharing
4. Generate blocklists
5. Export in standard formats

**Output**: IOC documentation and feeds

**Example**:
```python
from forensic_reporting import IOCReportGenerator

# Initialize IOC report
report = IOCReportGenerator(
    case_id="CASE-2024-001",
    threat_name="Operation Shadow Strike",
    tlp="amber"
)

# Add network IOCs
report.add_network_ioc(
    type="ip",
    value="203.0.113.50",
    context="Command and control server",
    confidence="high",
    first_seen="2024-01-10",
    source="Memory forensics"
)

report.add_network_ioc(
    type="domain",
    value="evil-c2.example.com",
    context="C2 domain",
    confidence="high",
    first_seen="2024-01-10",
    source="DNS cache analysis"
)

report.add_network_ioc(
    type="url",
    value="https://evil-c2.example.com/beacon",
    context="Beacon download URL",
    confidence="high",
    first_seen="2024-01-10",
    source="Network forensics"
)

# Add file IOCs
report.add_file_ioc(
    type="hash_md5",
    value="d41d8cd98f00b204e9800998ecf8427e",
    filename="malware.exe",
    context="Primary malware sample",
    confidence="high",
    source="Disk forensics"
)

report.add_file_ioc(
    type="hash_sha256",
    value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    filename="malware.exe",
    context="Primary malware sample",
    confidence="high",
    source="Disk forensics"
)

# Add host IOCs
report.add_host_ioc(
    type="registry",
    value="HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Updater",
    context="Persistence mechanism",
    confidence="high",
    source="Registry forensics"
)

report.add_host_ioc(
    type="mutex",
    value="Global\\MalwareMutex123",
    context="Malware mutex",
    confidence="high",
    source="Memory forensics"
)

report.add_host_ioc(
    type="filepath",
    value="C:\\Windows\\Temp\\beacon.exe",
    context="Malware drop location",
    confidence="high",
    source="Disk forensics"
)

# Add MITRE ATT&CK mapping
report.add_mitre_mapping("T1566.001", "Spearphishing Attachment")
report.add_mitre_mapping("T1059.001", "PowerShell")
report.add_mitre_mapping("T1547.001", "Registry Run Keys")
report.add_mitre_mapping("T1003.001", "LSASS Memory")

# Generate report
report.generate()

# Export in multiple formats
report.export_pdf("/evidence/reports/ioc_report.pdf")
report.export_csv("/evidence/reports/iocs.csv")
report.export_json("/evidence/reports/iocs.json")
report.export_stix("/evidence/reports/iocs.stix.json")
report.export_misp("/evidence/reports/misp_event.json")

# Generate blocklists
report.export_ip_blocklist("/evidence/reports/block_ips.txt")
report.export_domain_blocklist("/evidence/reports/block_domains.txt")
report.export_hash_blocklist("/evidence/reports/block_hashes.txt")
```

### Task 6: Chain of Custody Report
**Input**: Evidence handling records

**Process**:
1. Document evidence items
2. Record all transfers
3. Track access events
4. Verify integrity
5. Generate legal documentation

**Output**: Chain of custody documentation

**Example**:
```python
from forensic_reporting import ChainOfCustodyReport

# Initialize chain of custody report
report = ChainOfCustodyReport(
    case_id="CASE-2024-001",
    case_name="Corporate Investigation"
)

# Add evidence items
report.add_evidence_item(
    item_number="EVD-001",
    description="Dell Latitude 5520 Laptop",
    serial_number="ABC123XYZ",
    collected_by="John Doe",
    collected_date="2024-01-15 10:00",
    collected_location="Employee desk, Building A, Floor 3",
    initial_condition="Powered on, user logged in",
    storage_location="Evidence locker, Room 101"
)

report.add_evidence_item(
    item_number="EVD-002",
    description="Forensic image of EVD-001",
    hash_md5="abc123...",
    hash_sha256="def456...",
    created_by="Jane Smith",
    created_date="2024-01-15 14:00",
    tool_used="FTK Imager 4.7",
    storage_location="Evidence server, /cases/2024-001/"
)

# Record custody transfers
report.add_custody_transfer(
    item_number="EVD-001",
    transfer_date="2024-01-15 11:00",
    from_person="John Doe",
    from_location="Building A, Floor 3",
    to_person="Jane Smith",
    to_location="Forensics Lab, Room 201",
    purpose="Forensic imaging",
    transport_method="Hand-carried in evidence bag"
)

report.add_custody_transfer(
    item_number="EVD-001",
    transfer_date="2024-01-15 16:00",
    from_person="Jane Smith",
    from_location="Forensics Lab, Room 201",
    to_person="Evidence Custodian",
    to_location="Evidence Locker, Room 101",
    purpose="Secure storage",
    transport_method="Hand-carried in evidence bag"
)

# Record evidence access
report.add_access_record(
    item_number="EVD-002",
    access_date="2024-01-16 09:00",
    accessed_by="Jane Smith",
    purpose="Forensic analysis",
    actions="Mounted read-only, analyzed with Autopsy",
    duration="4 hours"
)

# Add verification records
report.add_verification(
    item_number="EVD-002",
    verification_date="2024-01-20",
    verified_by="Jane Smith",
    hash_verified=True,
    notes="Hash matches original acquisition"
)

# Generate report
report.generate()
report.export_pdf("/evidence/reports/chain_of_custody.pdf")
```

### Task 7: Timeline Report
**Input**: Forensic timeline data

**Process**:
1. Import timeline events
2. Add narrative context
3. Highlight key events
4. Create visualizations
5. Generate report

**Output**: Timeline-focused report

**Example**:
```python
from forensic_reporting import TimelineReportGenerator

# Initialize timeline report
report = TimelineReportGenerator(
    case_id="CASE-2024-001",
    title="Attack Timeline Analysis"
)

# Import timeline data
report.import_timeline("/evidence/timeline/supertimeline.csv")

# Add narrative sections
report.add_narrative_section(
    title="Initial Access",
    time_range=("2024-01-10 10:30", "2024-01-10 10:35"),
    narrative="""
    The attack began when a user opened a malicious email attachment.
    The document contained a macro that executed PowerShell commands
    to download the primary payload.
    """,
    highlight_events=[
        "2024-01-10 10:31 - Document opened",
        "2024-01-10 10:32 - PowerShell executed",
        "2024-01-10 10:33 - Payload downloaded"
    ]
)

report.add_narrative_section(
    title="Lateral Movement",
    time_range=("2024-01-10 14:00", "2024-01-10 15:00"),
    narrative="""
    After establishing persistence, the attacker performed credential
    dumping and began moving laterally through the network.
    """,
    highlight_events=[
        "2024-01-10 14:15 - Mimikatz execution",
        "2024-01-10 14:30 - RDP to FILE-SERVER-01"
    ]
)

# Add key events
report.add_key_event(
    timestamp="2024-01-10 10:31",
    event="Initial Compromise",
    description="User opened malicious attachment",
    significance="Attack initiation point"
)

report.add_key_event(
    timestamp="2024-01-10 14:15",
    event="Credential Theft",
    description="Mimikatz executed to dump credentials",
    significance="Enabled lateral movement"
)

# Configure visualization
report.configure_visualization(
    show_gaps=True,
    highlight_anomalies=True,
    group_by="source"
)

# Generate report
report.generate()
report.export_pdf("/evidence/reports/timeline_report.pdf")
report.export_html("/evidence/reports/timeline_report.html")
```

### Task 8: Compliance Report
**Input**: Investigation findings for compliance

**Process**:
1. Map to compliance framework
2. Document required elements
3. Assess compliance impact
4. Generate notifications
5. Create audit trail

**Output**: Compliance-ready documentation

**Example**:
```python
from forensic_reporting import ComplianceReportGenerator

# Initialize compliance report
report = ComplianceReportGenerator(
    case_id="CASE-2024-001",
    frameworks=["GDPR", "PCI-DSS", "HIPAA"]
)

# Add incident details
report.set_incident_details(
    incident_type="data_breach",
    detection_date="2024-01-10",
    affected_records=1500,
    data_types=["PII", "Financial data"],
    geographic_scope=["EU", "US"]
)

# GDPR compliance
report.add_gdpr_assessment(
    personal_data_affected=True,
    data_subjects=["Employees", "Customers"],
    dpa_notification_required=True,
    dpa_notification_deadline="2024-01-13",
    subject_notification_required=True,
    risk_to_subjects="High - credential theft"
)

# PCI-DSS compliance
report.add_pci_assessment(
    cardholder_data_affected=False,
    requirement_violations=["Req 10 - Logging", "Req 11 - Testing"],
    forensic_investigation_required=True
)

# Generate compliance timeline
report.add_compliance_action(
    framework="GDPR",
    action="DPA Notification Sent",
    date="2024-01-12",
    details="Notification sent to ICO within 72 hours"
)

report.add_compliance_action(
    framework="GDPR",
    action="Data Subject Notification",
    date="2024-01-15",
    details="Email notification sent to affected individuals"
)

# Generate notifications
report.generate_dpa_notification(
    authority="ICO",
    output_path="/evidence/reports/ico_notification.pdf"
)

report.generate_subject_notification(
    template="breach_notification",
    output_path="/evidence/reports/subject_notification.pdf"
)

# Generate compliance report
report.generate()
report.export_pdf("/evidence/reports/compliance_report.pdf")
```

### Task 9: Report Templates
**Input**: Template requirements

**Process**:
1. Create template structure
2. Define placeholders
3. Add styling
4. Test generation
5. Export template

**Output**: Reusable report templates

**Example**:
```python
from forensic_reporting import ReportTemplateManager

# Initialize template manager
templates = ReportTemplateManager()

# Create custom template
template = templates.create_template(
    name="malware_analysis",
    title="Malware Analysis Report",
    sections=[
        {
            "name": "executive_summary",
            "title": "Executive Summary",
            "required": True
        },
        {
            "name": "sample_information",
            "title": "Sample Information",
            "fields": ["filename", "hash_md5", "hash_sha256", "file_size", "file_type"]
        },
        {
            "name": "static_analysis",
            "title": "Static Analysis",
            "subsections": ["pe_analysis", "strings", "imports", "resources"]
        },
        {
            "name": "dynamic_analysis",
            "title": "Dynamic Analysis",
            "subsections": ["behavior", "network", "file_system", "registry"]
        },
        {
            "name": "iocs",
            "title": "Indicators of Compromise",
            "fields": ["network_iocs", "file_iocs", "host_iocs"]
        },
        {
            "name": "mitre_mapping",
            "title": "MITRE ATT&CK Mapping"
        },
        {
            "name": "conclusions",
            "title": "Conclusions and Recommendations"
        }
    ]
)

# Set template styling
template.set_styling(
    font="Arial",
    header_color="#003366",
    table_style="professional"
)

# Save template
templates.save_template(template, "/templates/malware_analysis.json")

# List available templates
available = templates.list_templates()
for t in available:
    print(f"Template: {t.name}")
    print(f"  Sections: {len(t.sections)}")

# Generate report from template
report = templates.generate_from_template(
    template_name="malware_analysis",
    data={
        "filename": "malware.exe",
        "hash_sha256": "abc123...",
        "executive_summary": "Analysis of malware sample...",
        "iocs": {...}
    }
)
report.export_pdf("/evidence/reports/malware_report.pdf")
```

### Task 10: Multi-Format Export
**Input**: Report content

**Process**:
1. Prepare content for format
2. Apply formatting
3. Include attachments
4. Generate output
5. Verify output

**Output**: Reports in multiple formats

**Example**:
```python
from forensic_reporting import MultiFormatExporter

# Initialize exporter with report content
exporter = MultiFormatExporter(
    report_data="/evidence/reports/report_data.json"
)

# Export to PDF with options
exporter.export_pdf(
    output_path="/evidence/reports/report.pdf",
    options={
        "include_toc": True,
        "include_appendices": True,
        "watermark": "CONFIDENTIAL",
        "password_protect": True,
        "password": "SecurePassword123"
    }
)

# Export to Word
exporter.export_docx(
    output_path="/evidence/reports/report.docx",
    options={
        "template": "/templates/corporate.docx",
        "include_styles": True,
        "track_changes": False
    }
)

# Export to HTML
exporter.export_html(
    output_path="/evidence/reports/report.html",
    options={
        "include_navigation": True,
        "interactive_timeline": True,
        "responsive": True
    }
)

# Export to Markdown
exporter.export_markdown(
    output_path="/evidence/reports/report.md",
    options={
        "github_flavored": True,
        "include_toc": True
    }
)

# Export to PowerPoint
exporter.export_pptx(
    output_path="/evidence/reports/presentation.pptx",
    options={
        "template": "/templates/corporate.pptx",
        "include_speaker_notes": True
    }
)

# Batch export
exporter.batch_export(
    output_dir="/evidence/reports/",
    formats=["pdf", "docx", "html", "md"],
    naming_pattern="{case_id}_{date}_{format}"
)
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `REPORT_TEMPLATE_DIR` | Report templates directory | No | ./templates |
| `REPORT_OUTPUT_DIR` | Default output directory | No | ./reports |
| `ORGANIZATION_NAME` | Organization for headers | No | None |
| `LOGO_PATH` | Path to organization logo | No | None |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `include_toc` | boolean | Include table of contents |
| `include_appendices` | boolean | Include appendices |
| `watermark` | string | Add watermark text |
| `classification` | string | Document classification |
| `template` | string | Template to use |

## Examples

### Example 1: Complete Investigation Report
**Scenario**: Generating full report package

```python
from forensic_reporting import ReportPackageGenerator

# Create complete report package
package = ReportPackageGenerator(case_id="CASE-2024-001")

# Add all report types
package.add_technical_report(findings_data)
package.add_executive_summary(summary_data)
package.add_ioc_report(iocs)
package.add_timeline_report(timeline)
package.add_chain_of_custody(custody_records)

# Generate all reports
package.generate_all("/evidence/reports/")

# Create final package
package.create_package(
    output_path="/evidence/CASE-2024-001_Final_Report_Package.zip"
)
```

## Limitations

- Complex formatting may vary across export formats
- Large reports may take time to generate
- Some features require specific fonts installed
- Template customization has boundaries
- Interactive features only in HTML export
- Password protection varies by format
- Legal compliance not guaranteed

## Troubleshooting

### Common Issue 1: Font Not Found
**Problem**: Report generation fails due to missing fonts
**Solution**:
- Install required fonts
- Use fallback font option
- Use built-in fonts

### Common Issue 2: Large Report Timeout
**Problem**: Report generation takes too long
**Solution**:
- Generate sections separately
- Reduce image quality
- Use lighter templates

### Common Issue 3: Format Conversion Issues
**Problem**: Content looks different in different formats
**Solution**:
- Use format-appropriate styling
- Test in target format
- Simplify complex formatting

## Related Skills

- [artifact-collection](../artifact-collection/): Evidence documentation
- [timeline-forensics](../timeline-forensics/): Timeline generation
- [malware-forensics](../malware-forensics/): IOC extraction
- [memory-forensics](../memory-forensics/): Technical findings
- [disk-forensics](../disk-forensics/): Technical findings

## References

- [Forensic Reporting Reference](references/REFERENCE.md)
- [Report Templates Guide](references/TEMPLATES.md)
- [Legal Documentation Standards](references/LEGAL_STANDARDS.md)
