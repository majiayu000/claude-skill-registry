---
name: email-forensics
description: |
  Analyze email messages and mailbox data for forensic investigation. Use when investigating
  phishing attacks, business email compromise, insider threats, or any scenario requiring
  email evidence analysis. Supports PST, OST, MBOX, EML, and MSG formats.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: libpst, python-msg, mailbox
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Email Forensics

Comprehensive email forensics skill for analyzing email messages, mailbox archives, and email metadata. Enables investigation of phishing attacks, business email compromise (BEC), email spoofing, and extraction of forensically valuable artifacts from email data.

## Capabilities

- **Mailbox Parsing**: Parse PST, OST, MBOX, EML, and MSG files
- **Header Analysis**: Deep analysis of email headers and routing
- **Attachment Extraction**: Extract and analyze email attachments
- **Phishing Detection**: Identify phishing indicators and techniques
- **Spoofing Detection**: Detect email spoofing and impersonation
- **Link Analysis**: Extract and analyze URLs in email content
- **Timeline Generation**: Create email-based communication timeline
- **Thread Reconstruction**: Rebuild email conversation threads
- **Metadata Extraction**: Extract sender, recipient, and routing metadata
- **Authentication Analysis**: Analyze SPF, DKIM, and DMARC results

## Quick Start

```python
from email_forensics import EmailAnalyzer, MailboxParser, PhishingDetector

# Parse mailbox file
parser = MailboxParser("/evidence/mailbox.pst")
emails = parser.get_all_messages()

# Analyze single email
analyzer = EmailAnalyzer()
analysis = analyzer.analyze_file("/evidence/suspicious.eml")

# Detect phishing
detector = PhishingDetector()
results = detector.scan_email(analysis)
```

## Usage

### Task 1: Mailbox Parsing
**Input**: Mailbox file (PST, OST, MBOX)

**Process**:
1. Load and validate mailbox file
2. Parse folder structure
3. Extract messages
4. Index metadata
5. Generate mailbox summary

**Output**: Parsed mailbox with message inventory

**Example**:
```python
from email_forensics import MailboxParser

# Parse Outlook PST file
parser = MailboxParser("/evidence/user_mailbox.pst")

# Get mailbox info
info = parser.get_mailbox_info()
print(f"Mailbox type: {info.format}")
print(f"Total messages: {info.message_count}")
print(f"Total folders: {info.folder_count}")
print(f"Date range: {info.oldest_date} - {info.newest_date}")

# List folders
folders = parser.get_folders()
for folder in folders:
    print(f"Folder: {folder.name}")
    print(f"  Path: {folder.path}")
    print(f"  Messages: {folder.message_count}")
    print(f"  Unread: {folder.unread_count}")

# Get messages from folder
inbox = parser.get_messages(folder_path="Inbox")
for msg in inbox:
    print(f"[{msg.date}] From: {msg.sender}")
    print(f"  Subject: {msg.subject}")
    print(f"  To: {msg.recipients}")
    print(f"  Has attachments: {msg.has_attachments}")

# Search messages
results = parser.search(
    query="confidential",
    search_body=True,
    search_subject=True
)
for r in results:
    print(f"Match: {r.subject}")
    print(f"  Folder: {r.folder}")
    print(f"  Match context: {r.context}")

# Export messages
parser.export_messages(
    folder_path="Inbox",
    output_dir="/evidence/exported/",
    format="eml"
)

# Generate mailbox report
parser.generate_report("/evidence/mailbox_report.html")
```

### Task 2: Email Header Analysis
**Input**: Email message (EML, MSG, or raw headers)

**Process**:
1. Parse all header fields
2. Analyze routing path
3. Verify authentication
4. Detect anomalies
5. Generate header analysis

**Output**: Comprehensive header analysis

**Example**:
```python
from email_forensics import HeaderAnalyzer

# Analyze email headers
analyzer = HeaderAnalyzer()
analysis = analyzer.analyze_file("/evidence/suspicious.eml")

# Get basic headers
print(f"From: {analysis.from_address}")
print(f"To: {analysis.to_addresses}")
print(f"Subject: {analysis.subject}")
print(f"Date: {analysis.date}")
print(f"Message-ID: {analysis.message_id}")

# Analyze routing path
routing = analysis.get_routing_path()
for hop in routing:
    print(f"Hop {hop.number}:")
    print(f"  From: {hop.from_server}")
    print(f"  By: {hop.by_server}")
    print(f"  Time: {hop.timestamp}")
    print(f"  Delay: {hop.delay_seconds}s")

# Get authentication results
auth = analysis.get_authentication()
print(f"SPF: {auth.spf_result}")
print(f"  SPF domain: {auth.spf_domain}")
print(f"DKIM: {auth.dkim_result}")
print(f"  DKIM domain: {auth.dkim_domain}")
print(f"DMARC: {auth.dmarc_result}")

# Detect anomalies
anomalies = analysis.detect_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.type}")
    print(f"  Description: {a.description}")
    print(f"  Severity: {a.severity}")

# Get original sender (envelope)
envelope = analysis.get_envelope_info()
print(f"Envelope From: {envelope.mail_from}")
print(f"Envelope To: {envelope.rcpt_to}")

# Get X-headers
x_headers = analysis.get_x_headers()
for header, value in x_headers.items():
    print(f"{header}: {value}")

# Export analysis
analysis.export_report("/evidence/header_analysis.html")
```

### Task 3: Phishing Detection
**Input**: Email message

**Process**:
1. Analyze sender authenticity
2. Check URLs for malicious indicators
3. Analyze attachment risks
4. Detect social engineering
5. Calculate risk score

**Output**: Phishing analysis with risk assessment

**Example**:
```python
from email_forensics import PhishingDetector, EmailAnalyzer

# Initialize detector
detector = PhishingDetector()

# Analyze email
analyzer = EmailAnalyzer()
email = analyzer.parse_file("/evidence/suspicious.eml")

# Run phishing detection
result = detector.analyze(email)

print(f"Risk Score: {result.risk_score}/100")
print(f"Classification: {result.classification}")
print(f"Confidence: {result.confidence}")

# Get indicators
for indicator in result.indicators:
    print(f"INDICATOR: {indicator.type}")
    print(f"  Description: {indicator.description}")
    print(f"  Weight: {indicator.weight}")
    print(f"  Evidence: {indicator.evidence}")

# Check sender authenticity
sender = result.sender_analysis
print(f"Sender: {sender.display_name} <{sender.address}>")
print(f"  Display name mismatch: {sender.display_name_mismatch}")
print(f"  Domain reputation: {sender.domain_reputation}")
print(f"  First-time sender: {sender.first_time_sender}")

# Analyze URLs
for url in result.url_analysis:
    print(f"URL: {url.url}")
    print(f"  Domain: {url.domain}")
    print(f"  Display text: {url.display_text}")
    print(f"  Mismatch: {url.text_url_mismatch}")
    print(f"  Shortened: {url.is_shortened}")
    print(f"  Risk: {url.risk_level}")

# Check attachments
for att in result.attachment_analysis:
    print(f"Attachment: {att.filename}")
    print(f"  Type: {att.content_type}")
    print(f"  Risk: {att.risk_level}")
    print(f"  Double extension: {att.has_double_extension}")

# Export report
detector.generate_report(result, "/evidence/phishing_report.html")
```

### Task 4: Attachment Analysis
**Input**: Email with attachments

**Process**:
1. Extract all attachments
2. Identify file types
3. Calculate hashes
4. Check for malware indicators
5. Extract metadata

**Output**: Attachment analysis with extracted files

**Example**:
```python
from email_forensics import AttachmentAnalyzer

# Initialize analyzer
analyzer = AttachmentAnalyzer()

# Extract from single email
attachments = analyzer.extract_from_email(
    email_path="/evidence/email.eml",
    output_dir="/evidence/attachments/"
)

for att in attachments:
    print(f"Attachment: {att.filename}")
    print(f"  Content-Type: {att.content_type}")
    print(f"  Size: {att.size}")
    print(f"  MD5: {att.md5}")
    print(f"  SHA256: {att.sha256}")
    print(f"  Detected type: {att.detected_type}")
    print(f"  Type mismatch: {att.type_mismatch}")
    print(f"  Extracted to: {att.output_path}")

# Analyze specific attachment
detailed = analyzer.analyze_file("/evidence/attachments/document.pdf")
print(f"Metadata: {detailed.metadata}")
print(f"Embedded objects: {detailed.embedded_objects}")
print(f"Scripts: {detailed.contains_scripts}")
print(f"Macros: {detailed.contains_macros}")

# Extract from mailbox
mailbox_attachments = analyzer.extract_from_mailbox(
    mailbox_path="/evidence/mailbox.pst",
    output_dir="/evidence/all_attachments/",
    filter_types=["application/pdf", "application/msword"]
)

# Find suspicious attachments
suspicious = analyzer.find_suspicious(attachments)
for s in suspicious:
    print(f"SUSPICIOUS: {s.filename}")
    print(f"  Reason: {s.reason}")

# Check against malware hashes
malware = analyzer.check_malware_hashes("/hashsets/malware.txt")

# Generate attachment report
analyzer.generate_report("/evidence/attachment_report.html")
```

### Task 5: Email Timeline Creation
**Input**: Mailbox or collection of emails

**Process**:
1. Parse all messages
2. Extract timestamps
3. Build chronological timeline
4. Identify communication patterns
5. Visualize activity

**Output**: Email communication timeline

**Example**:
```python
from email_forensics import EmailTimeline

# Initialize timeline
timeline = EmailTimeline()

# Add email sources
timeline.add_mailbox("/evidence/user1.pst")
timeline.add_mailbox("/evidence/user2.pst")
timeline.add_folder("/evidence/exported_emails/")

# Build timeline
events = timeline.build()

for event in events:
    print(f"[{event.timestamp}] {event.direction}")
    print(f"  From: {event.sender}")
    print(f"  To: {event.recipients}")
    print(f"  Subject: {event.subject}")

# Filter by date range
filtered = timeline.filter_by_date(
    start="2024-01-01",
    end="2024-01-31"
)

# Filter by participants
participant_emails = timeline.filter_by_participant("suspect@example.com")

# Get communication patterns
patterns = timeline.analyze_patterns()
print(f"Total messages: {patterns.total_messages}")
print(f"Unique senders: {patterns.unique_senders}")
print(f"Unique recipients: {patterns.unique_recipients}")
print(f"Peak hours: {patterns.peak_hours}")
print(f"Top correspondents: {patterns.top_correspondents}")

# Detect anomalies
anomalies = timeline.detect_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.description}")
    print(f"  Time: {a.timestamp}")

# Export timeline
timeline.export_csv("/evidence/email_timeline.csv")
timeline.generate_visualization("/evidence/email_timeline.html")
```

### Task 6: Email Thread Reconstruction
**Input**: Email messages

**Process**:
1. Group by conversation
2. Analyze In-Reply-To headers
3. Build thread hierarchy
4. Identify missing messages
5. Reconstruct full threads

**Output**: Reconstructed email threads

**Example**:
```python
from email_forensics import ThreadReconstructor

# Initialize reconstructor
reconstructor = ThreadReconstructor()

# Load emails
reconstructor.load_mailbox("/evidence/mailbox.pst")

# Reconstruct all threads
threads = reconstructor.reconstruct_all()

for thread in threads:
    print(f"Thread: {thread.subject}")
    print(f"  Messages: {thread.message_count}")
    print(f"  Participants: {thread.participants}")
    print(f"  Duration: {thread.start_date} - {thread.end_date}")
    print(f"  Complete: {thread.is_complete}")

    # Print thread hierarchy
    for msg in thread.messages:
        indent = "  " * msg.depth
        print(f"{indent}[{msg.date}] {msg.sender}: {msg.subject}")

# Find specific thread
thread = reconstructor.find_thread(subject_contains="Project Alpha")

# Find threads with missing messages
incomplete = reconstructor.find_incomplete_threads()
for t in incomplete:
    print(f"Incomplete: {t.subject}")
    print(f"  Missing IDs: {t.missing_message_ids}")

# Export threads
reconstructor.export_threads(
    output_dir="/evidence/threads/",
    format="mbox"
)

# Generate thread report
reconstructor.generate_report("/evidence/threads_report.html")
```

### Task 7: Spoofing Detection
**Input**: Email message

**Process**:
1. Verify sender headers
2. Check authentication records
3. Analyze display name tricks
4. Compare envelope vs header
5. Detect impersonation

**Output**: Spoofing analysis results

**Example**:
```python
from email_forensics import SpoofingDetector

# Initialize detector
detector = SpoofingDetector()

# Analyze email
result = detector.analyze_file("/evidence/suspicious.eml")

print(f"Spoofing detected: {result.is_spoofed}")
print(f"Confidence: {result.confidence}")

# Header vs Envelope analysis
print(f"Header From: {result.header_from}")
print(f"Envelope From: {result.envelope_from}")
print(f"Mismatch: {result.from_mismatch}")

# Display name analysis
display = result.display_name_analysis
print(f"Display Name: {display.name}")
print(f"Homograph attack: {display.homograph_detected}")
print(f"Executive impersonation: {display.executive_impersonation}")
print(f"Brand impersonation: {display.brand_impersonation}")

# Authentication analysis
auth = result.authentication_analysis
print(f"SPF Pass: {auth.spf_pass}")
print(f"DKIM Pass: {auth.dkim_pass}")
print(f"DMARC Pass: {auth.dmarc_pass}")

# Reply-To analysis
reply_to = result.reply_to_analysis
print(f"Reply-To: {reply_to.address}")
print(f"Reply-To differs from From: {reply_to.differs_from_sender}")

# Get all indicators
for indicator in result.indicators:
    print(f"INDICATOR: {indicator.name}")
    print(f"  Evidence: {indicator.evidence}")
    print(f"  Severity: {indicator.severity}")

# Export report
detector.generate_report(result, "/evidence/spoofing_analysis.html")
```

### Task 8: Link Analysis
**Input**: Email content

**Process**:
1. Extract all URLs
2. Analyze URL components
3. Check against threat intel
4. Detect URL obfuscation
5. Identify redirect chains

**Output**: URL analysis results

**Example**:
```python
from email_forensics import LinkAnalyzer

# Initialize analyzer
analyzer = LinkAnalyzer()

# Extract links from email
links = analyzer.extract_from_email("/evidence/email.eml")

for link in links:
    print(f"URL: {link.url}")
    print(f"  Display text: {link.display_text}")
    print(f"  Domain: {link.domain}")
    print(f"  TLD: {link.tld}")
    print(f"  Text matches URL: {link.text_matches_url}")
    print(f"  Is shortened: {link.is_shortened}")
    print(f"  Is IP-based: {link.is_ip_based}")
    print(f"  Risk score: {link.risk_score}")

# Unshorten URLs
unshortened = analyzer.unshorten_urls(links)
for u in unshortened:
    print(f"Short: {u.short_url}")
    print(f"Final: {u.final_url}")
    print(f"Redirects: {u.redirect_count}")

# Check against threat intelligence
threats = analyzer.check_threat_intel(
    links,
    feed_path="/feeds/malicious_urls.txt"
)
for t in threats:
    print(f"THREAT: {t.url}")
    print(f"  Category: {t.category}")
    print(f"  Source: {t.intel_source}")

# Detect URL obfuscation
obfuscated = analyzer.detect_obfuscation(links)
for o in obfuscated:
    print(f"OBFUSCATED: {o.url}")
    print(f"  Technique: {o.obfuscation_type}")
    print(f"  Decoded: {o.decoded_url}")

# Analyze link destinations (safe fetch)
destinations = analyzer.analyze_destinations(links, safe_mode=True)

# Export link analysis
analyzer.generate_report("/evidence/link_analysis.html")
```

### Task 9: Business Email Compromise Analysis
**Input**: Email or mailbox

**Process**:
1. Identify BEC indicators
2. Detect urgency language
3. Analyze financial requests
4. Check sender legitimacy
5. Score BEC probability

**Output**: BEC analysis results

**Example**:
```python
from email_forensics import BECDetector

# Initialize BEC detector
detector = BECDetector()

# Analyze single email
result = detector.analyze_email("/evidence/wire_request.eml")

print(f"BEC Score: {result.bec_score}/100")
print(f"Classification: {result.classification}")

# Check BEC indicators
for indicator in result.indicators:
    print(f"INDICATOR: {indicator.type}")
    print(f"  Description: {indicator.description}")
    print(f"  Evidence: {indicator.evidence}")
    print(f"  Weight: {indicator.weight}")

# Language analysis
language = result.language_analysis
print(f"Urgency detected: {language.urgency_score}")
print(f"Authority claims: {language.authority_score}")
print(f"Financial keywords: {language.financial_keywords}")
print(f"Secrecy requests: {language.secrecy_score}")

# Sender analysis
sender = result.sender_analysis
print(f"Claimed identity: {sender.claimed_identity}")
print(f"Actual sender: {sender.actual_address}")
print(f"Executive impersonation: {sender.executive_impersonation}")

# Request analysis
request = result.request_analysis
print(f"Action requested: {request.action}")
print(f"Amount mentioned: {request.amount}")
print(f"Account details: {request.has_account_details}")
print(f"Wire transfer request: {request.wire_transfer}")

# Scan mailbox for BEC
mailbox_results = detector.scan_mailbox("/evidence/mailbox.pst")
for r in mailbox_results.high_risk:
    print(f"HIGH RISK: {r.subject}")
    print(f"  BEC Score: {r.bec_score}")

# Generate BEC report
detector.generate_report("/evidence/bec_analysis.html")
```

### Task 10: Email Search and Export
**Input**: Mailbox file or email collection

**Process**:
1. Index email content
2. Execute search queries
3. Filter results
4. Export matches
5. Generate search report

**Output**: Search results with exported emails

**Example**:
```python
from email_forensics import EmailSearcher

# Initialize searcher
searcher = EmailSearcher("/evidence/mailbox.pst")

# Build search index
searcher.build_index()

# Search by keywords
results = searcher.search(
    query="confidential project",
    search_body=True,
    search_subject=True,
    search_attachments=True
)

for r in results:
    print(f"Match: {r.subject}")
    print(f"  From: {r.sender}")
    print(f"  Date: {r.date}")
    print(f"  Score: {r.relevance_score}")
    print(f"  Snippet: {r.snippet}")

# Search by sender
sender_emails = searcher.search_by_sender("suspicious@example.com")

# Search by date range
date_range = searcher.search_by_date(
    start="2024-01-01",
    end="2024-01-31"
)

# Search by attachment name
with_attachments = searcher.search_by_attachment(
    filename_pattern="*.pdf"
)

# Complex query
complex_results = searcher.advanced_search(
    sender_contains="@example.com",
    subject_contains="wire transfer",
    date_after="2024-01-01",
    has_attachments=True
)

# Export search results
searcher.export_results(
    results,
    output_dir="/evidence/search_results/",
    format="eml",
    include_attachments=True
)

# Generate search report
searcher.generate_report("/evidence/search_report.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `EMAIL_PARSER` | Path to email parsing library | No | Built-in |
| `THREAT_INTEL_FEED` | URL threat intelligence feed | No | None |
| `VT_API_KEY` | VirusTotal API key | No | None |
| `SAFE_BROWSE_KEY` | Google Safe Browsing API key | No | None |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `extract_attachments` | boolean | Auto-extract attachments |
| `decode_mime` | boolean | Decode MIME-encoded content |
| `parse_html` | boolean | Parse HTML email bodies |
| `safe_url_check` | boolean | Safe URL verification |
| `parallel` | boolean | Enable parallel processing |

## Examples

### Example 1: Phishing Campaign Investigation
**Scenario**: Investigating a phishing campaign targeting the organization

```python
from email_forensics import MailboxParser, PhishingDetector

# Parse quarantined emails
parser = MailboxParser("/evidence/quarantine.pst")
emails = parser.get_all_messages()

# Initialize phishing detector
detector = PhishingDetector()

# Analyze all emails
phishing_emails = []
for email in emails:
    result = detector.analyze(email)
    if result.risk_score > 70:
        phishing_emails.append(result)
        print(f"PHISHING: {email.subject}")
        print(f"  Risk: {result.risk_score}")
        print(f"  Indicators: {len(result.indicators)}")

# Extract IOCs from phishing emails
iocs = detector.extract_iocs(phishing_emails)
print(f"Malicious URLs: {len(iocs.urls)}")
print(f"Sender addresses: {len(iocs.senders)}")

# Generate campaign report
detector.generate_campaign_report(phishing_emails, "/evidence/phishing_campaign.html")
```

### Example 2: BEC Incident Investigation
**Scenario**: Investigating potential business email compromise

```python
from email_forensics import BECDetector, EmailTimeline, SpoofingDetector

# Analyze the suspicious request email
bec = BECDetector()
result = bec.analyze_email("/evidence/wire_request.eml")

print(f"BEC Score: {result.bec_score}")
print(f"Financial request: {result.request_analysis.wire_transfer}")

# Check for spoofing
spoof = SpoofingDetector()
spoof_result = spoof.analyze_file("/evidence/wire_request.eml")
print(f"Spoofed: {spoof_result.is_spoofed}")

# Build communication timeline
timeline = EmailTimeline()
timeline.add_mailbox("/evidence/cfo_mailbox.pst")
timeline.add_mailbox("/evidence/finance_mailbox.pst")

# Find related emails
related = timeline.filter_by_participant(result.sender_analysis.actual_address)
print(f"Related emails from sender: {len(related)}")
```

## Limitations

- Large mailboxes may require significant processing time
- Encrypted emails require decryption keys
- Some proprietary formats may have limited support
- URL analysis requires network access for verification
- Attachment analysis depends on file type support
- BEC detection may have false positives
- Header analysis accuracy depends on email preservation

## Troubleshooting

### Common Issue 1: PST File Corruption
**Problem**: Unable to parse PST file
**Solution**:
- Use PST repair tools before analysis
- Try different parsing libraries
- Extract individual messages if possible

### Common Issue 2: Encoded Content Not Decoded
**Problem**: Email body appears as encoded text
**Solution**:
- Enable MIME decoding
- Check for unusual character encodings
- Try different decoding methods

### Common Issue 3: Missing Attachments
**Problem**: Attachments not extracted
**Solution**:
- Check attachment size limits
- Verify attachment format support
- Look for inline attachments

## Related Skills

- [network-forensics](../network-forensics/): Analyze email network traffic
- [browser-forensics](../browser-forensics/): Webmail investigation
- [malware-forensics](../malware-forensics/): Analyze malicious attachments
- [timeline-forensics](../timeline-forensics/): Integrate email timeline
- [log-forensics](../log-forensics/): Correlate with mail server logs

## References

- [Email Forensics Reference](references/REFERENCE.md)
- [Email Header Analysis Guide](references/HEADER_ANALYSIS.md)
- [Phishing Detection Patterns](references/PHISHING_PATTERNS.md)
