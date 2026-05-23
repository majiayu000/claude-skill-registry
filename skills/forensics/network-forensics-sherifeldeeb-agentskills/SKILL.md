---
name: network-forensics
description: |
  Analyze network traffic captures and artifacts for forensic investigation. Use when
  investigating data exfiltration, command and control communications, lateral movement,
  or network-based attacks. Supports PCAP, PCAPNG, and NetFlow analysis.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: pyshark, scapy, dpkt, zeek
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Network Forensics

Comprehensive network forensics skill for analyzing packet captures, network flows, and communication patterns. Enables reconstruction of network sessions, detection of malicious traffic, extraction of transferred files, and identification of command and control communications.

## Capabilities

- **PCAP Analysis**: Parse and analyze packet capture files (PCAP, PCAPNG)
- **Session Reconstruction**: Rebuild TCP sessions and application-layer conversations
- **Protocol Analysis**: Deep inspection of HTTP, DNS, SMTP, FTP, SMB, and other protocols
- **File Extraction**: Carve files transferred over network protocols
- **C2 Detection**: Identify command and control communication patterns
- **DNS Analysis**: Analyze DNS queries, detect tunneling and DGA domains
- **TLS/SSL Analysis**: Inspect encrypted traffic metadata, certificate analysis
- **NetFlow Analysis**: Analyze network flow data for traffic patterns
- **Lateral Movement Detection**: Identify internal reconnaissance and movement
- **Exfiltration Detection**: Detect data exfiltration attempts

## Quick Start

```python
from network_forensics import PcapAnalyzer, SessionReconstructor, ProtocolParser

# Load packet capture
analyzer = PcapAnalyzer("/evidence/capture.pcap")

# Get capture statistics
stats = analyzer.get_statistics()
print(f"Total packets: {stats.total_packets}")
print(f"Duration: {stats.duration_seconds}s")

# Reconstruct sessions
reconstructor = SessionReconstructor(analyzer)
sessions = reconstructor.get_tcp_sessions()

# Analyze specific protocol
parser = ProtocolParser(analyzer)
http_requests = parser.get_http_requests()
```

## Usage

### Task 1: Packet Capture Analysis
**Input**: PCAP or PCAPNG file

**Process**:
1. Load and validate capture file
2. Generate capture statistics
3. Identify protocols and endpoints
4. Create conversation matrix
5. Generate analysis summary

**Output**: Comprehensive capture analysis

**Example**:
```python
from network_forensics import PcapAnalyzer

# Load packet capture
analyzer = PcapAnalyzer("/evidence/incident_capture.pcap")

# Get overall statistics
stats = analyzer.get_statistics()
print(f"Capture file: {stats.filename}")
print(f"File size: {stats.file_size_mb}MB")
print(f"Total packets: {stats.total_packets}")
print(f"Start time: {stats.start_time}")
print(f"End time: {stats.end_time}")
print(f"Duration: {stats.duration_seconds}s")

# Get protocol distribution
protocols = analyzer.get_protocol_distribution()
for proto, count in protocols.items():
    print(f"  {proto}: {count} packets")

# Get top talkers
talkers = analyzer.get_top_talkers(limit=10)
for t in talkers:
    print(f"  {t.ip}: {t.bytes_sent}B sent, {t.bytes_recv}B received")

# Get unique endpoints
endpoints = analyzer.get_unique_endpoints()
print(f"Unique IPs: {len(endpoints.ips)}")
print(f"Unique ports: {len(endpoints.ports)}")

# Filter packets
filtered = analyzer.filter_packets(
    src_ip="192.168.1.100",
    dst_port=443,
    protocol="TCP"
)
```

### Task 2: TCP Session Reconstruction
**Input**: Packet capture with TCP traffic

**Process**:
1. Identify TCP connections
2. Reassemble packet streams
3. Handle out-of-order packets
4. Reconstruct payload data
5. Extract session metadata

**Output**: Reconstructed TCP sessions

**Example**:
```python
from network_forensics import PcapAnalyzer, SessionReconstructor

analyzer = PcapAnalyzer("/evidence/capture.pcap")
reconstructor = SessionReconstructor(analyzer)

# Get all TCP sessions
sessions = reconstructor.get_tcp_sessions()

for session in sessions:
    print(f"Session: {session.src_ip}:{session.src_port} -> "
          f"{session.dst_ip}:{session.dst_port}")
    print(f"  Start: {session.start_time}")
    print(f"  Duration: {session.duration_seconds}s")
    print(f"  Packets: {session.packet_count}")
    print(f"  Bytes: {session.total_bytes}")
    print(f"  State: {session.state}")

# Reconstruct specific session
session_data = reconstructor.reconstruct_session(
    src_ip="192.168.1.100",
    src_port=49152,
    dst_ip="203.0.113.50",
    dst_port=80
)

# Get client-side data
client_data = session_data.client_payload
print(f"Client sent: {len(client_data)} bytes")

# Get server-side data
server_data = session_data.server_payload
print(f"Server sent: {len(server_data)} bytes")

# Export session to file
reconstructor.export_session(session_data, "/evidence/session_dump.bin")

# Find sessions by criteria
suspicious = reconstructor.find_sessions(
    min_duration=3600,  # Long-lived connections
    min_bytes=10000000  # Large data transfer
)
```

### Task 3: HTTP Traffic Analysis
**Input**: Packet capture containing HTTP traffic

**Process**:
1. Extract HTTP requests and responses
2. Parse headers and body content
3. Identify file downloads
4. Detect suspicious requests
5. Extract transferred files

**Output**: HTTP traffic analysis with extracted files

**Example**:
```python
from network_forensics import PcapAnalyzer, HTTPAnalyzer

analyzer = PcapAnalyzer("/evidence/capture.pcap")
http_analyzer = HTTPAnalyzer(analyzer)

# Get all HTTP requests
requests = http_analyzer.get_requests()

for req in requests:
    print(f"[{req.timestamp}] {req.method} {req.url}")
    print(f"  Host: {req.host}")
    print(f"  User-Agent: {req.user_agent}")
    print(f"  Status: {req.response_code}")

# Find specific requests
downloads = http_analyzer.find_requests(
    methods=["GET"],
    content_types=["application/octet-stream", "application/x-executable"]
)

# Extract downloaded files
files = http_analyzer.extract_files(output_dir="/evidence/http_files/")
for f in files:
    print(f"Extracted: {f.filename}")
    print(f"  Size: {f.size}")
    print(f"  Type: {f.content_type}")
    print(f"  URL: {f.source_url}")
    print(f"  Hash: {f.sha256}")

# Analyze POST requests (potential exfiltration)
posts = http_analyzer.get_post_requests()
for post in posts:
    print(f"POST to {post.url}")
    print(f"  Content-Length: {post.content_length}")
    print(f"  Content-Type: {post.content_type}")

# Find suspicious user agents
suspicious_ua = http_analyzer.find_suspicious_user_agents()

# Export HTTP log
http_analyzer.export_log("/evidence/http_log.csv")
```

### Task 4: DNS Analysis
**Input**: Packet capture containing DNS traffic

**Process**:
1. Extract DNS queries and responses
2. Identify unique domains queried
3. Detect DNS tunneling
4. Identify DGA domains
5. Analyze DNS response codes

**Output**: DNS analysis with threat indicators

**Example**:
```python
from network_forensics import PcapAnalyzer, DNSAnalyzer

analyzer = PcapAnalyzer("/evidence/capture.pcap")
dns_analyzer = DNSAnalyzer(analyzer)

# Get all DNS queries
queries = dns_analyzer.get_queries()

for query in queries:
    print(f"[{query.timestamp}] {query.query_name}")
    print(f"  Type: {query.query_type}")
    print(f"  Client: {query.client_ip}")
    print(f"  Response: {query.response_ips}")

# Get unique domains
domains = dns_analyzer.get_unique_domains()
print(f"Unique domains queried: {len(domains)}")

# Detect DNS tunneling
tunneling = dns_analyzer.detect_tunneling()
for t in tunneling:
    print(f"TUNNELING DETECTED: {t.domain}")
    print(f"  Indicator: {t.indicator}")
    print(f"  Query count: {t.query_count}")
    print(f"  Avg query length: {t.avg_query_length}")

# Detect DGA (Domain Generation Algorithm) domains
dga_domains = dns_analyzer.detect_dga()
for dga in dga_domains:
    print(f"DGA: {dga.domain}")
    print(f"  Score: {dga.dga_score}")
    print(f"  Entropy: {dga.entropy}")

# Find NXDOMAIN responses
nxdomain = dns_analyzer.get_nxdomain_responses()

# Analyze query patterns
patterns = dns_analyzer.analyze_query_patterns()
print(f"Total queries: {patterns.total_queries}")
print(f"Unique domains: {patterns.unique_domains}")
print(f"Top queried: {patterns.top_domains[:5]}")

# Export DNS log
dns_analyzer.export_log("/evidence/dns_log.csv")
```

### Task 5: File Extraction from Network Traffic
**Input**: Packet capture with file transfers

**Process**:
1. Identify file transfer protocols
2. Reconstruct transferred files
3. Calculate file hashes
4. Identify file types
5. Save extracted files

**Output**: Extracted files with metadata

**Example**:
```python
from network_forensics import PcapAnalyzer, FileExtractor

analyzer = PcapAnalyzer("/evidence/capture.pcap")
extractor = FileExtractor(analyzer)

# Extract all transferable files
files = extractor.extract_all(output_dir="/evidence/extracted/")

for f in files:
    print(f"File: {f.filename}")
    print(f"  Protocol: {f.protocol}")
    print(f"  Size: {f.size}")
    print(f"  Source: {f.source_ip}")
    print(f"  Destination: {f.dest_ip}")
    print(f"  MD5: {f.md5}")
    print(f"  SHA256: {f.sha256}")
    print(f"  Type: {f.detected_type}")

# Extract from specific protocol
http_files = extractor.extract_http(output_dir="/evidence/http/")
smtp_files = extractor.extract_smtp(output_dir="/evidence/email/")
ftp_files = extractor.extract_ftp(output_dir="/evidence/ftp/")
smb_files = extractor.extract_smb(output_dir="/evidence/smb/")

# Extract with filtering
exe_files = extractor.extract_by_type(
    file_types=["executable", "archive", "document"],
    output_dir="/evidence/suspicious/"
)

# Check against malware hashes
malware_check = extractor.check_malware_hashes(
    hash_db="/hashsets/malware.txt"
)
for match in malware_check:
    print(f"MALWARE: {match.filename} - {match.malware_name}")
```

### Task 6: C2 Communication Detection
**Input**: Packet capture suspected of containing C2 traffic

**Process**:
1. Analyze traffic patterns
2. Detect beaconing behavior
3. Identify suspicious destinations
4. Analyze encrypted traffic metadata
5. Correlate with threat intelligence

**Output**: C2 detection results with IOCs

**Example**:
```python
from network_forensics import PcapAnalyzer, C2Detector

analyzer = PcapAnalyzer("/evidence/capture.pcap")
c2_detector = C2Detector(analyzer)

# Detect beaconing behavior
beacons = c2_detector.detect_beaconing()
for beacon in beacons:
    print(f"BEACON DETECTED:")
    print(f"  Source: {beacon.src_ip}")
    print(f"  Destination: {beacon.dst_ip}:{beacon.dst_port}")
    print(f"  Interval: {beacon.interval_seconds}s")
    print(f"  Jitter: {beacon.jitter_percent}%")
    print(f"  Connection count: {beacon.connection_count}")

# Detect known C2 patterns
patterns = c2_detector.detect_known_patterns()
for p in patterns:
    print(f"C2 Pattern: {p.pattern_name}")
    print(f"  Confidence: {p.confidence}")
    print(f"  Hosts: {p.affected_hosts}")

# Check against threat intelligence
ti_matches = c2_detector.check_threat_intel(
    feed_path="/feeds/c2_indicators.json"
)

# Analyze encrypted traffic (JA3/JA3S fingerprints)
ja3_analysis = c2_detector.analyze_ja3()
for ja3 in ja3_analysis:
    print(f"JA3: {ja3.fingerprint}")
    print(f"  Client: {ja3.client_ip}")
    print(f"  Known as: {ja3.known_application}")

# Detect suspicious port usage
suspicious_ports = c2_detector.detect_suspicious_ports()

# Generate C2 report
c2_detector.generate_report("/evidence/c2_analysis.html")
```

### Task 7: Data Exfiltration Analysis
**Input**: Packet capture for exfiltration investigation

**Process**:
1. Identify large outbound transfers
2. Detect encoding/encryption indicators
3. Analyze unusual protocols
4. Check for covert channels
5. Quantify data exposure

**Output**: Exfiltration analysis report

**Example**:
```python
from network_forensics import PcapAnalyzer, ExfiltrationAnalyzer

analyzer = PcapAnalyzer("/evidence/capture.pcap")
exfil_analyzer = ExfiltrationAnalyzer(analyzer)

# Find large outbound transfers
large_transfers = exfil_analyzer.find_large_transfers(
    threshold_mb=10,
    direction="outbound"
)
for t in large_transfers:
    print(f"Large Transfer: {t.src_ip} -> {t.dst_ip}")
    print(f"  Size: {t.size_mb}MB")
    print(f"  Protocol: {t.protocol}")
    print(f"  Duration: {t.duration}s")

# Detect DNS exfiltration
dns_exfil = exfil_analyzer.detect_dns_exfiltration()
for e in dns_exfil:
    print(f"DNS Exfil: {e.domain}")
    print(f"  Data volume: {e.data_bytes}B")
    print(f"  Query count: {e.query_count}")

# Detect ICMP tunneling
icmp_tunnel = exfil_analyzer.detect_icmp_tunneling()

# Analyze HTTP(S) exfiltration
http_exfil = exfil_analyzer.analyze_http_exfiltration()
for h in http_exfil:
    print(f"HTTP POST: {h.url}")
    print(f"  Size: {h.size}")
    print(f"  Encoded: {h.appears_encoded}")

# Detect steganography indicators
stego = exfil_analyzer.detect_steganography_indicators()

# Calculate total data exposure
exposure = exfil_analyzer.calculate_exposure()
print(f"Total outbound data: {exposure.total_mb}MB")
print(f"Suspicious destinations: {len(exposure.destinations)}")

# Generate exfiltration report
exfil_analyzer.generate_report("/evidence/exfil_report.pdf")
```

### Task 8: SMB/Windows Network Analysis
**Input**: Packet capture with SMB/Windows traffic

**Process**:
1. Extract SMB sessions
2. Identify file operations
3. Detect lateral movement
4. Analyze authentication attempts
5. Extract shared files

**Output**: Windows network activity analysis

**Example**:
```python
from network_forensics import PcapAnalyzer, SMBAnalyzer

analyzer = PcapAnalyzer("/evidence/capture.pcap")
smb_analyzer = SMBAnalyzer(analyzer)

# Get SMB sessions
sessions = smb_analyzer.get_sessions()
for s in sessions:
    print(f"SMB Session: {s.client} -> {s.server}")
    print(f"  User: {s.username}")
    print(f"  Domain: {s.domain}")
    print(f"  Dialect: {s.dialect}")

# Get file operations
operations = smb_analyzer.get_file_operations()
for op in operations:
    print(f"[{op.timestamp}] {op.operation}: {op.filename}")
    print(f"  Client: {op.client_ip}")
    print(f"  Share: {op.share_name}")
    print(f"  Result: {op.status}")

# Detect lateral movement
lateral = smb_analyzer.detect_lateral_movement()
for l in lateral:
    print(f"Lateral Movement: {l.source} -> {l.targets}")
    print(f"  Technique: {l.technique}")
    print(f"  Confidence: {l.confidence}")

# Extract transferred files
files = smb_analyzer.extract_files("/evidence/smb_files/")

# Analyze authentication
auth = smb_analyzer.get_authentication_attempts()
for a in auth:
    print(f"Auth: {a.username}@{a.domain}")
    print(f"  Client: {a.client_ip}")
    print(f"  Success: {a.success}")
    print(f"  Type: {a.auth_type}")

# Find administrative share access
admin_access = smb_analyzer.find_admin_share_access()
```

### Task 9: Email Traffic Analysis
**Input**: Packet capture with email traffic

**Process**:
1. Extract SMTP/POP3/IMAP sessions
2. Parse email headers and body
3. Extract attachments
4. Identify phishing indicators
5. Analyze email metadata

**Output**: Email analysis with extracted messages

**Example**:
```python
from network_forensics import PcapAnalyzer, EmailAnalyzer

analyzer = PcapAnalyzer("/evidence/capture.pcap")
email_analyzer = EmailAnalyzer(analyzer)

# Extract all emails
emails = email_analyzer.extract_emails()

for email in emails:
    print(f"Email: {email.subject}")
    print(f"  From: {email.from_address}")
    print(f"  To: {email.to_addresses}")
    print(f"  Date: {email.date}")
    print(f"  Protocol: {email.protocol}")
    print(f"  Has attachments: {email.has_attachments}")

# Extract attachments
attachments = email_analyzer.extract_attachments("/evidence/attachments/")
for att in attachments:
    print(f"Attachment: {att.filename}")
    print(f"  Size: {att.size}")
    print(f"  Type: {att.content_type}")
    print(f"  SHA256: {att.sha256}")

# Analyze for phishing
phishing = email_analyzer.detect_phishing()
for p in phishing:
    print(f"PHISHING: {p.subject}")
    print(f"  Indicators: {p.indicators}")
    print(f"  Risk score: {p.risk_score}")

# Get email headers analysis
headers = email_analyzer.analyze_headers(emails[0])
print(f"Original sender: {headers.original_sender}")
print(f"Relay path: {headers.relay_path}")
print(f"SPF result: {headers.spf_result}")

# Export emails to EML format
email_analyzer.export_eml("/evidence/emails/")
```

### Task 10: NetFlow Analysis
**Input**: NetFlow/sFlow/IPFIX data

**Process**:
1. Parse flow records
2. Analyze traffic volumes
3. Identify top conversations
4. Detect anomalous flows
5. Create traffic baseline

**Output**: Flow analysis with anomalies

**Example**:
```python
from network_forensics import NetFlowAnalyzer

# Load NetFlow data
flow_analyzer = NetFlowAnalyzer("/evidence/netflow_data/")

# Get flow statistics
stats = flow_analyzer.get_statistics()
print(f"Total flows: {stats.total_flows}")
print(f"Total bytes: {stats.total_bytes}")
print(f"Time range: {stats.start_time} - {stats.end_time}")

# Get top conversations
conversations = flow_analyzer.get_top_conversations(limit=10)
for c in conversations:
    print(f"{c.src_ip}:{c.src_port} <-> {c.dst_ip}:{c.dst_port}")
    print(f"  Bytes: {c.total_bytes}")
    print(f"  Packets: {c.total_packets}")
    print(f"  Duration: {c.duration}")

# Find long-duration flows
long_flows = flow_analyzer.find_long_flows(min_duration_hours=1)

# Find high-volume flows
high_volume = flow_analyzer.find_high_volume_flows(min_bytes_gb=1)

# Detect port scanning
scans = flow_analyzer.detect_port_scans()
for scan in scans:
    print(f"Scan: {scan.source_ip} -> {scan.target}")
    print(f"  Ports scanned: {scan.port_count}")
    print(f"  Duration: {scan.duration}")

# Detect data exfiltration
exfil = flow_analyzer.detect_exfiltration()

# Create traffic heatmap
flow_analyzer.create_heatmap("/evidence/traffic_heatmap.png")

# Export analysis
flow_analyzer.export_report("/evidence/netflow_analysis.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WIRESHARK_PATH` | Path to Wireshark/tshark | No | System PATH |
| `ZEEK_PATH` | Path to Zeek installation | No | System PATH |
| `MAXMIND_DB` | Path to MaxMind GeoIP database | No | None |
| `THREAT_INTEL_FEED` | Threat intelligence feed URL | No | None |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `reassemble_tcp` | boolean | Enable TCP reassembly |
| `decode_tls` | boolean | Attempt TLS decryption if keys available |
| `geoip_lookup` | boolean | Enable GeoIP lookups |
| `parallel_processing` | boolean | Enable multi-threaded analysis |
| `max_file_size` | integer | Maximum file extraction size (MB) |

## Examples

### Example 1: Investigating Data Breach
**Scenario**: Analyzing network traffic from a suspected data breach

```python
from network_forensics import (
    PcapAnalyzer, ExfiltrationAnalyzer, DNSAnalyzer, HTTPAnalyzer
)

# Load capture from breach timeframe
analyzer = PcapAnalyzer("/evidence/breach_capture.pcap")

# Step 1: Identify data leaving the network
exfil = ExfiltrationAnalyzer(analyzer)
outbound = exfil.find_large_transfers(threshold_mb=5, direction="outbound")
print(f"Found {len(outbound)} large outbound transfers")

# Step 2: Check DNS for C2 or tunneling
dns = DNSAnalyzer(analyzer)
tunneling = dns.detect_tunneling()
dga = dns.detect_dga()

# Step 3: Analyze HTTP for data exfiltration
http = HTTPAnalyzer(analyzer)
posts = http.get_post_requests()
suspicious_uploads = [p for p in posts if p.content_length > 1000000]

# Step 4: Extract transferred files
files = http.extract_files("/evidence/extracted/")

# Step 5: Generate comprehensive report
analyzer.generate_report(
    output_path="/evidence/breach_analysis.html",
    include_timeline=True,
    include_files=True
)
```

### Example 2: Malware C2 Analysis
**Scenario**: Analyzing captured malware command and control traffic

```python
from network_forensics import PcapAnalyzer, C2Detector, DNSAnalyzer

analyzer = PcapAnalyzer("/evidence/malware_traffic.pcap")

# Detect beaconing
c2 = C2Detector(analyzer)
beacons = c2.detect_beaconing()
for b in beacons:
    print(f"C2 Server: {b.dst_ip}:{b.dst_port}")
    print(f"  Beacon interval: {b.interval_seconds}s")

# Analyze DNS for DGA
dns = DNSAnalyzer(analyzer)
dga_domains = dns.detect_dga()

# Get JA3 fingerprints for attribution
ja3_hashes = c2.analyze_ja3()

# Check against known C2 infrastructure
ti_matches = c2.check_threat_intel("/feeds/c2_infrastructure.json")

# Export IOCs
iocs = c2.extract_iocs()
c2.export_iocs("/evidence/c2_iocs.json", format="stix")
```

## Limitations

- Large PCAP files may require significant memory
- TLS decryption requires session keys
- Some protocols may not be fully parsed
- Real-time analysis not supported
- File carving may miss fragmented transfers
- Tunneled traffic may evade detection
- Performance depends on capture size

## Troubleshooting

### Common Issue 1: Memory Errors on Large Captures
**Problem**: Out of memory when loading large PCAP
**Solution**:
- Use streaming mode for large files
- Filter packets during loading
- Split capture into smaller files

### Common Issue 2: TLS Traffic Not Decoded
**Problem**: Cannot inspect encrypted traffic
**Solution**:
- Provide TLS session keys if available
- Analyze metadata (JA3, certificate info)
- Use associated endpoint logs

### Common Issue 3: Missing File Extractions
**Problem**: Known transfers not extracted
**Solution**:
- Ensure full capture (no dropped packets)
- Check for chunked/compressed transfers
- Verify protocol support

## Related Skills

- [memory-forensics](../memory-forensics/): Correlate with memory artifacts
- [log-forensics](../log-forensics/): Correlate with system logs
- [malware-forensics](../malware-forensics/): Analyze extracted malware samples
- [timeline-forensics](../timeline-forensics/): Add network events to timeline
- [email-forensics](../email-forensics/): Detailed email analysis

## References

- [Network Forensics Reference](references/REFERENCE.md)
- [Protocol Analysis Guide](references/PROTOCOLS.md)
- [C2 Detection Patterns](references/C2_PATTERNS.md)
