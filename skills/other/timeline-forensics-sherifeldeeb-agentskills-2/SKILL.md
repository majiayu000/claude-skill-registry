---
name: timeline-forensics
description: |
  Create comprehensive forensic timelines from multiple data sources. Use when
  reconstructing event sequences, correlating activities across sources, or
  visualizing incident progression. Supports super timeline creation and analysis.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: plaso, pandas, plotly
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Timeline Forensics

Comprehensive timeline forensics skill for creating and analyzing forensic timelines from multiple data sources. Enables super timeline creation, event correlation, anomaly detection, and visualization of activities across disk, memory, network, and log sources.

## Capabilities

- **Super Timeline Creation**: Create comprehensive timelines from multiple sources
- **Multi-Source Correlation**: Correlate events across different artifact types
- **Event Filtering**: Filter timelines by time, source, or keyword
- **Anomaly Detection**: Identify unusual patterns and outliers
- **Timeline Visualization**: Create interactive timeline visualizations
- **Gap Analysis**: Identify missing time periods in evidence
- **Pivot Point Analysis**: Find key events and pivot around them
- **Export Formats**: Export to CSV, JSON, bodyfile, and other formats
- **Timeline Comparison**: Compare timelines from different systems
- **Activity Clustering**: Group related events into activities

## Quick Start

```python
from timeline_forensics import TimelineBuilder, SuperTimeline, TimelineAnalyzer

# Create super timeline
builder = TimelineBuilder()
builder.add_disk_image("/evidence/disk.E01")
builder.add_memory_dump("/evidence/memory.raw")
builder.add_logs("/evidence/logs/")

timeline = builder.build()

# Analyze timeline
analyzer = TimelineAnalyzer(timeline)
anomalies = analyzer.detect_anomalies()
```

## Usage

### Task 1: Super Timeline Creation
**Input**: Multiple forensic artifacts

**Process**:
1. Add all evidence sources
2. Parse timestamps from each source
3. Normalize to UTC
4. Merge into unified timeline
5. Generate output

**Output**: Comprehensive super timeline

**Example**:
```python
from timeline_forensics import TimelineBuilder

# Initialize timeline builder
builder = TimelineBuilder(
    case_id="CASE-2024-001",
    timezone="UTC"
)

# Add disk image (will parse MFT, registry, etc.)
builder.add_disk_image(
    image_path="/evidence/disk.E01",
    parsers=["mft", "registry", "prefetch", "evtx", "browser"]
)

# Add memory dump
builder.add_memory_dump("/evidence/memory.raw")

# Add log files
builder.add_logs("/evidence/logs/")

# Add PCAP
builder.add_pcap("/evidence/capture.pcap")

# Add custom events
builder.add_custom_event(
    timestamp="2024-01-15T10:30:00Z",
    source="analyst",
    description="Incident reported by user",
    event_type="incident_report"
)

# Build timeline
timeline = builder.build()

print(f"Total events: {timeline.event_count}")
print(f"Time range: {timeline.start_time} - {timeline.end_time}")
print(f"Sources: {timeline.sources}")

# Export timeline
timeline.export_csv("/evidence/timeline/supertimeline.csv")
timeline.export_json("/evidence/timeline/supertimeline.json")
timeline.export_bodyfile("/evidence/timeline/bodyfile.txt")

# Generate timeline report
builder.generate_report("/evidence/timeline/timeline_report.html")
```

### Task 2: File System Timeline
**Input**: Disk image or file system

**Process**:
1. Parse MFT/inode tables
2. Extract all timestamps
3. Handle MAC times
4. Detect timestomping
5. Build file timeline

**Output**: File system timeline

**Example**:
```python
from timeline_forensics import FileSystemTimeline

# Initialize file system timeline
fst = FileSystemTimeline("/evidence/disk.E01")

# Parse file system
fst.parse()

# Get all events
events = fst.get_events()
for event in events[:10]:
    print(f"[{event.timestamp}] {event.event_type}")
    print(f"  File: {event.filename}")
    print(f"  Path: {event.full_path}")
    print(f"  Source: {event.timestamp_source}")  # mtime, atime, ctime, crtime

# Get events for specific file
file_events = fst.get_file_events("/Users/suspect/malware.exe")
for event in file_events:
    print(f"[{event.timestamp}] {event.event_type}")
    print(f"  Timestamp type: {event.timestamp_source}")

# Detect timestomping
anomalies = fst.detect_timestamp_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.file_path}")
    print(f"  Type: {a.anomaly_type}")
    print(f"  Evidence: {a.evidence}")

# Get recently modified files
recent = fst.get_files_modified_after("2024-01-15T00:00:00Z")

# Get files created during incident window
incident_files = fst.get_files_in_range(
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T12:00:00Z",
    event_types=["created", "modified"]
)

# Export file system timeline
fst.export("/evidence/timeline/filesystem.csv")
```

### Task 3: Registry Timeline
**Input**: Registry hives

**Process**:
1. Parse registry key timestamps
2. Extract last-write times
3. Build key timeline
4. Identify rapid changes
5. Correlate with events

**Output**: Registry timeline

**Example**:
```python
from timeline_forensics import RegistryTimeline

# Initialize registry timeline
rt = RegistryTimeline()

# Add registry hives
rt.add_hive("/evidence/registry/SYSTEM")
rt.add_hive("/evidence/registry/SOFTWARE")
rt.add_hive("/evidence/registry/NTUSER.DAT")

# Build timeline
rt.build()

# Get all events
events = rt.get_events()
for event in events[:10]:
    print(f"[{event.timestamp}] Registry modification")
    print(f"  Hive: {event.hive}")
    print(f"  Key: {event.key_path}")

# Get events for specific key
run_events = rt.get_key_events("Software\\Microsoft\\Windows\\CurrentVersion\\Run")

# Find rapid modifications (potential automation)
rapid = rt.find_rapid_modifications(
    threshold_seconds=60,
    min_changes=10
)
for r in rapid:
    print(f"Rapid changes at {r.start_time}:")
    print(f"  Keys modified: {r.key_count}")
    print(f"  Duration: {r.duration_seconds}s")

# Get modifications in time range
incident_mods = rt.get_modifications_in_range(
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T12:00:00Z"
)

# Export registry timeline
rt.export("/evidence/timeline/registry.csv")
```

### Task 4: Event Log Timeline
**Input**: Windows Event Logs

**Process**:
1. Parse EVTX files
2. Extract timestamps
3. Categorize events
4. Build log timeline
5. Identify patterns

**Output**: Event log timeline

**Example**:
```python
from timeline_forensics import EventLogTimeline

# Initialize event log timeline
elt = EventLogTimeline()

# Add event logs
elt.add_log("/evidence/logs/Security.evtx")
elt.add_log("/evidence/logs/System.evtx")
elt.add_log("/evidence/logs/Application.evtx")
elt.add_directory("/evidence/logs/")

# Build timeline
elt.build()

# Get all events
events = elt.get_events()
for event in events[:10]:
    print(f"[{event.timestamp}] {event.log_name}")
    print(f"  Event ID: {event.event_id}")
    print(f"  Description: {event.description}")

# Get security events
security_events = elt.get_events_by_log("Security")

# Get specific event IDs
login_events = elt.get_events_by_id([4624, 4625])
for event in login_events:
    print(f"[{event.timestamp}] Login event {event.event_id}")
    print(f"  User: {event.user}")
    print(f"  Source IP: {event.source_ip}")

# Find event sequences
sequences = elt.find_event_sequences([
    {"event_id": 4624, "description": "Login"},
    {"event_id": 4688, "description": "Process creation"},
    {"event_id": 4689, "description": "Process exit"}
])

# Export event log timeline
elt.export("/evidence/timeline/eventlogs.csv")
```

### Task 5: Network Timeline
**Input**: Network captures

**Process**:
1. Parse PCAP files
2. Extract connection timestamps
3. Track sessions
4. Build network timeline
5. Correlate with activity

**Output**: Network activity timeline

**Example**:
```python
from timeline_forensics import NetworkTimeline

# Initialize network timeline
nt = NetworkTimeline()

# Add network captures
nt.add_pcap("/evidence/network/capture1.pcap")
nt.add_pcap("/evidence/network/capture2.pcap")

# Add flow data
nt.add_netflow("/evidence/network/flows/")

# Build timeline
nt.build()

# Get all events
events = nt.get_events()
for event in events[:10]:
    print(f"[{event.timestamp}] {event.event_type}")
    print(f"  Source: {event.src_ip}:{event.src_port}")
    print(f"  Destination: {event.dst_ip}:{event.dst_port}")
    print(f"  Protocol: {event.protocol}")

# Get connections to specific IP
c2_connections = nt.get_connections_to_ip("203.0.113.50")

# Get DNS queries
dns_events = nt.get_dns_events()
for event in dns_events:
    print(f"[{event.timestamp}] DNS: {event.query}")

# Get HTTP events
http_events = nt.get_http_events()
for event in http_events:
    print(f"[{event.timestamp}] HTTP: {event.method} {event.url}")

# Find data transfers
transfers = nt.find_large_transfers(min_bytes=1000000)

# Export network timeline
nt.export("/evidence/timeline/network.csv")
```

### Task 6: Timeline Correlation
**Input**: Multiple timelines or super timeline

**Process**:
1. Align timestamps
2. Find temporal correlations
3. Identify related events
4. Build event chains
5. Document relationships

**Output**: Correlated timeline analysis

**Example**:
```python
from timeline_forensics import TimelineCorrelator

# Initialize correlator with super timeline
correlator = TimelineCorrelator("/evidence/timeline/supertimeline.csv")

# Find events around pivot point
pivot = correlator.get_events_around(
    timestamp="2024-01-15T10:30:00Z",
    window_minutes=30
)
for event in pivot:
    print(f"[{event.timestamp}] {event.source}: {event.description}")

# Correlate by IP address
ip_activity = correlator.correlate_by_ip("192.168.1.100")
print(f"Events related to IP: {len(ip_activity)}")

# Correlate by filename
file_activity = correlator.correlate_by_filename("malware.exe")
print(f"Events related to file: {len(file_activity)}")

# Correlate by user
user_activity = correlator.correlate_by_user("DOMAIN\\suspect")

# Find event chains
chains = correlator.find_event_chains()
for chain in chains:
    print(f"Chain: {chain.name}")
    print(f"  Events: {len(chain.events)}")
    print(f"  Duration: {chain.duration}")
    for event in chain.events:
        print(f"    [{event.timestamp}] {event.description}")

# Detect temporal anomalies
anomalies = correlator.detect_temporal_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.description}")
    print(f"  Events: {a.events}")

# Generate correlation report
correlator.generate_report("/evidence/timeline/correlation.html")
```

### Task 7: Timeline Filtering
**Input**: Timeline data

**Process**:
1. Apply time filters
2. Apply source filters
3. Apply keyword filters
4. Reduce noise
5. Focus investigation

**Output**: Filtered timeline

**Example**:
```python
from timeline_forensics import TimelineFilter

# Initialize filter with timeline
filter = TimelineFilter("/evidence/timeline/supertimeline.csv")

# Filter by time range
time_filtered = filter.by_time_range(
    start="2024-01-15T10:00:00Z",
    end="2024-01-15T12:00:00Z"
)
print(f"Events in time range: {len(time_filtered)}")

# Filter by source
source_filtered = filter.by_source(["MFT", "Registry", "EventLog"])

# Filter by keyword
keyword_filtered = filter.by_keyword(
    keywords=["malware", "suspicious", "admin"],
    case_sensitive=False
)

# Filter by event type
type_filtered = filter.by_event_type(["file_created", "process_start"])

# Exclude noise
noise_excluded = filter.exclude_patterns([
    "*Windows\\Prefetch\\*.pf",
    "*$RECYCLE.BIN*",
    "*pagefile.sys*"
])

# Complex filter
complex_filtered = filter.complex_filter(
    time_start="2024-01-15T10:00:00Z",
    time_end="2024-01-15T12:00:00Z",
    sources=["MFT", "Registry"],
    keywords=["malware"],
    exclude_patterns=["*TEMP*"]
)

# Export filtered timeline
filter.export_filtered("/evidence/timeline/filtered.csv", complex_filtered)
```

### Task 8: Timeline Visualization
**Input**: Timeline data

**Process**:
1. Prepare visualization data
2. Create interactive charts
3. Generate heat maps
4. Build activity graphs
5. Export visualizations

**Output**: Timeline visualizations

**Example**:
```python
from timeline_forensics import TimelineVisualizer

# Initialize visualizer
viz = TimelineVisualizer("/evidence/timeline/supertimeline.csv")

# Create interactive timeline
viz.create_interactive_timeline(
    output_path="/evidence/timeline/interactive.html",
    title="Incident Timeline",
    highlight_events=["malware.exe", "suspicious"]
)

# Create activity heatmap
viz.create_heatmap(
    output_path="/evidence/timeline/heatmap.html",
    granularity="hour"
)

# Create source distribution chart
viz.create_source_chart(
    output_path="/evidence/timeline/sources.html"
)

# Create event type distribution
viz.create_event_type_chart(
    output_path="/evidence/timeline/event_types.html"
)

# Create activity sparkline
viz.create_activity_sparkline(
    output_path="/evidence/timeline/activity.png",
    window="day"
)

# Create network graph
viz.create_event_graph(
    output_path="/evidence/timeline/event_graph.html",
    relationship_type="temporal"
)

# Generate full visualization report
viz.generate_visualization_report(
    output_dir="/evidence/timeline/viz/",
    include_all=True
)
```

### Task 9: Gap Analysis
**Input**: Timeline data

**Process**:
1. Analyze event distribution
2. Identify time gaps
3. Detect missing periods
4. Assess evidence coverage
5. Document gaps

**Output**: Gap analysis report

**Example**:
```python
from timeline_forensics import GapAnalyzer

# Initialize gap analyzer
analyzer = GapAnalyzer("/evidence/timeline/supertimeline.csv")

# Find gaps in timeline
gaps = analyzer.find_gaps(min_gap_minutes=60)
for gap in gaps:
    print(f"GAP: {gap.start_time} - {gap.end_time}")
    print(f"  Duration: {gap.duration_minutes} minutes")
    print(f"  Events before: {gap.events_before}")
    print(f"  Events after: {gap.events_after}")

# Analyze coverage by source
coverage = analyzer.analyze_source_coverage()
for source, cov in coverage.items():
    print(f"Source: {source}")
    print(f"  First event: {cov.first_event}")
    print(f"  Last event: {cov.last_event}")
    print(f"  Coverage: {cov.coverage_percent}%")
    print(f"  Gaps: {cov.gap_count}")

# Find suspicious gaps
suspicious = analyzer.find_suspicious_gaps()
for gap in suspicious:
    print(f"SUSPICIOUS GAP: {gap.start_time} - {gap.end_time}")
    print(f"  Reason: {gap.reason}")

# Analyze activity distribution
distribution = analyzer.analyze_distribution()
print(f"Peak hours: {distribution.peak_hours}")
print(f"Quiet hours: {distribution.quiet_hours}")
print(f"Average events/hour: {distribution.avg_events_per_hour}")

# Generate gap report
analyzer.generate_report("/evidence/timeline/gap_analysis.html")
```

### Task 10: Timeline Analysis
**Input**: Timeline data

**Process**:
1. Statistical analysis
2. Pattern detection
3. Anomaly identification
4. Activity clustering
5. Investigation support

**Output**: Timeline analysis results

**Example**:
```python
from timeline_forensics import TimelineAnalyzer

# Initialize analyzer
analyzer = TimelineAnalyzer("/evidence/timeline/supertimeline.csv")

# Get timeline statistics
stats = analyzer.get_statistics()
print(f"Total events: {stats.total_events}")
print(f"Time span: {stats.time_span}")
print(f"Sources: {stats.source_count}")
print(f"Event types: {stats.event_type_count}")
print(f"Unique files: {stats.unique_files}")

# Detect anomalies
anomalies = analyzer.detect_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.type}")
    print(f"  Description: {a.description}")
    print(f"  Timestamp: {a.timestamp}")
    print(f"  Confidence: {a.confidence}")

# Find patterns
patterns = analyzer.find_patterns()
for p in patterns:
    print(f"Pattern: {p.name}")
    print(f"  Occurrences: {p.count}")
    print(f"  Description: {p.description}")

# Cluster related events
clusters = analyzer.cluster_events()
for cluster in clusters:
    print(f"Cluster: {cluster.label}")
    print(f"  Events: {cluster.event_count}")
    print(f"  Time range: {cluster.start_time} - {cluster.end_time}")

# Get investigation suggestions
suggestions = analyzer.get_investigation_suggestions()
for s in suggestions:
    print(f"SUGGESTION: {s.title}")
    print(f"  Priority: {s.priority}")
    print(f"  Description: {s.description}")
    print(f"  Related events: {s.event_count}")

# Generate analysis report
analyzer.generate_report("/evidence/timeline/analysis.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PLASO_PATH` | Path to Plaso tools | No | System PATH |
| `TIMELINE_TZ` | Default timezone | No | UTC |
| `MAX_EVENTS` | Maximum events to process | No | 10000000 |
| `CACHE_DIR` | Timeline cache directory | No | ./cache |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `normalize_timezone` | boolean | Normalize to UTC |
| `deduplicate` | boolean | Remove duplicate events |
| `parallel_parsing` | boolean | Parallel source parsing |
| `cache_results` | boolean | Cache parsed results |
| `include_hash` | boolean | Include file hashes |

## Examples

### Example 1: Incident Timeline Reconstruction
**Scenario**: Reconstructing attack timeline from evidence

```python
from timeline_forensics import TimelineBuilder, TimelineAnalyzer

# Build comprehensive timeline
builder = TimelineBuilder(case_id="INCIDENT-001")
builder.add_disk_image("/evidence/victim.E01")
builder.add_memory_dump("/evidence/memory.raw")
builder.add_logs("/evidence/logs/")
builder.add_pcap("/evidence/traffic.pcap")

timeline = builder.build()

# Analyze for attack indicators
analyzer = TimelineAnalyzer(timeline)

# Find initial compromise
initial = analyzer.find_events_with_keywords(["powershell", "cmd.exe"])
print(f"Potential initial access: {len(initial)}")

# Find lateral movement
lateral = analyzer.find_events_by_pattern("network_login")

# Build attack narrative
narrative = analyzer.build_narrative()
print(narrative)
```

### Example 2: Data Breach Timeline
**Scenario**: Creating timeline for data exfiltration investigation

```python
from timeline_forensics import TimelineBuilder, TimelineCorrelator

# Build timeline
builder = TimelineBuilder(case_id="BREACH-001")
builder.add_disk_image("/evidence/server.E01")
builder.add_logs("/evidence/access_logs/")

timeline = builder.build()

# Find data access
correlator = TimelineCorrelator(timeline)
data_access = correlator.correlate_by_path("*\\SensitiveData\\*")

# Find large file operations
large_ops = correlator.find_large_file_operations(min_size_mb=10)

# Generate breach timeline
correlator.generate_breach_report("/evidence/breach_timeline.html")
```

## Limitations

- Large timelines require significant memory
- Timezone handling requires accurate source metadata
- Some artifacts lack precise timestamps
- Correlation accuracy depends on time synchronization
- Visualization performance degrades with many events
- Gap analysis assumes continuous activity
- Pattern detection requires sufficient data

## Troubleshooting

### Common Issue 1: Memory Exhaustion
**Problem**: Out of memory processing large timeline
**Solution**:
- Process in time chunks
- Filter before loading
- Increase system memory

### Common Issue 2: Timezone Confusion
**Problem**: Events appear at wrong times
**Solution**:
- Verify source timezones
- Check DST handling
- Normalize all to UTC

### Common Issue 3: Missing Events
**Problem**: Expected events not in timeline
**Solution**:
- Verify parser support
- Check source integrity
- Review parser logs

## Related Skills

- [memory-forensics](../memory-forensics/): Add memory artifacts to timeline
- [disk-forensics](../disk-forensics/): Add disk artifacts to timeline
- [log-forensics](../log-forensics/): Add log events to timeline
- [network-forensics](../network-forensics/): Add network events to timeline
- [artifact-collection](../artifact-collection/): Collect artifacts for timeline

## References

- [Timeline Forensics Reference](references/REFERENCE.md)
- [Plaso Integration Guide](references/PLASO_GUIDE.md)
- [Timeline Analysis Techniques](references/ANALYSIS_TECHNIQUES.md)
