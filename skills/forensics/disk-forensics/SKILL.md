---
name: disk-forensics
description: |
  Analyze disk images and file systems for forensic investigation. Use when investigating
  data theft, insider threats, malware persistence, deleted file recovery, or any incident
  requiring analysis of storage media. Supports NTFS, FAT, EXT, HFS+, and APFS file systems.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: pytsk3, pyewf, The Sleuth Kit, libewf
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Disk Forensics

Comprehensive disk forensics skill for analyzing storage media, file systems, and persistent artifacts. Enables recovery of deleted files, analysis of file system metadata, detection of hidden data, and extraction of forensic artifacts from disk images.

## Capabilities

- **Disk Image Acquisition**: Create forensically sound disk images with integrity verification
- **File System Analysis**: Parse and analyze NTFS, FAT, EXT, HFS+, APFS file systems
- **Deleted File Recovery**: Recover deleted files using file carving and file system analysis
- **MFT Analysis**: Parse NTFS Master File Table for file metadata and timestamps
- **Slack Space Analysis**: Examine slack space for hidden or residual data
- **Alternate Data Streams**: Detect and extract NTFS alternate data streams
- **File Signature Analysis**: Verify file signatures and detect mismatched extensions
- **Hash Analysis**: Calculate and verify file hashes for integrity and known file detection
- **Volume Shadow Copy Analysis**: Extract and analyze Windows Volume Shadow Copies
- **Partition Analysis**: Detect hidden partitions, analyze partition tables

## Quick Start

```python
from disk_forensics import DiskAnalyzer, FileRecovery, MFTParser

# Initialize analyzer with disk image
analyzer = DiskAnalyzer("/evidence/disk_image.E01")

# Get volume information
volumes = analyzer.list_volumes()
for vol in volumes:
    print(f"Volume: {vol.description} - {vol.size_gb}GB")

# Recover deleted files
recovery = FileRecovery(analyzer)
deleted = recovery.find_deleted_files()

# Parse MFT
mft_parser = MFTParser(analyzer)
entries = mft_parser.parse_all()
```

## Usage

### Task 1: Disk Image Acquisition
**Input**: Physical disk or logical volume to acquire

**Process**:
1. Document source media details
2. Calculate source hash before acquisition
3. Create forensic image (E01/Ex01/raw)
4. Verify image integrity with hash comparison
5. Generate acquisition report

**Output**: Forensically sound disk image with documentation

**Example**:
```python
from disk_forensics import DiskAcquisition

# Initialize acquisition
acquisition = DiskAcquisition()

# Document source
source_info = acquisition.document_source(
    device_path="/dev/sdb",
    make="Samsung",
    model="SSD 870 EVO",
    serial_number="S5XXXXXXXXXXXX",
    capacity_gb=500
)

# Create forensic image
result = acquisition.create_image(
    source="/dev/sdb",
    destination="/evidence/suspect_disk.E01",
    format="ewf",  # Expert Witness Format
    compression="best",
    segment_size_gb=2,
    hash_algorithms=["md5", "sha256"]
)

print(f"Acquisition complete")
print(f"Source Hash: {result.source_hash}")
print(f"Image Hash: {result.image_hash}")
print(f"Verified: {result.verified}")

# Generate acquisition report
acquisition.generate_report(
    output_path="/evidence/acquisition_report.pdf",
    case_id="CASE-2024-001",
    examiner="Jane Smith"
)
```

### Task 2: File System Analysis
**Input**: Disk image file path

**Process**:
1. Mount disk image read-only
2. Identify file system type
3. Parse file system structures
4. Extract file metadata
5. Build file system timeline

**Output**: File system analysis with metadata

**Example**:
```python
from disk_forensics import DiskAnalyzer, FileSystemParser

analyzer = DiskAnalyzer("/evidence/disk_image.E01")

# List all volumes
volumes = analyzer.list_volumes()
for vol in volumes:
    print(f"Volume {vol.index}: {vol.file_system}")
    print(f"  Start: {vol.start_offset}")
    print(f"  Size: {vol.size_bytes} bytes")

# Parse specific volume
parser = FileSystemParser(analyzer, volume_index=2)

# Get volume statistics
stats = parser.get_statistics()
print(f"Total files: {stats.total_files}")
print(f"Total directories: {stats.total_directories}")
print(f"Deleted entries: {stats.deleted_entries}")

# List directory contents
files = parser.list_directory("/Users/suspect/Documents")
for f in files:
    print(f"{f.name} - {f.size} bytes - {f.modified_time}")

# Find files by extension
docs = parser.find_files_by_extension([".docx", ".xlsx", ".pdf"])

# Find files by date range
recent = parser.find_files_by_date(
    start_date="2024-01-01",
    end_date="2024-01-31",
    date_type="modified"
)
```

### Task 3: Deleted File Recovery
**Input**: Disk image with potential deleted files

**Process**:
1. Scan file system for deleted entries
2. Analyze unallocated space
3. Perform file carving by signatures
4. Verify recovered file integrity
5. Document recovery results

**Output**: Recovered files with recovery metadata

**Example**:
```python
from disk_forensics import DiskAnalyzer, FileRecovery

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
recovery = FileRecovery(analyzer)

# Find deleted files via file system
deleted = recovery.find_deleted_files()
for f in deleted:
    print(f"Deleted: {f.name}")
    print(f"  Original path: {f.original_path}")
    print(f"  Size: {f.size}")
    print(f"  Recoverable: {f.recoverable_percent}%")

# Recover specific file
recovery.recover_file(
    file_entry=deleted[0],
    output_path="/evidence/recovered/"
)

# File carving from unallocated space
carved = recovery.carve_files(
    file_types=["jpg", "png", "pdf", "docx"],
    output_dir="/evidence/carved/"
)

for f in carved:
    print(f"Carved: {f.filename}")
    print(f"  Type: {f.file_type}")
    print(f"  Size: {f.size}")
    print(f"  Offset: {f.disk_offset}")

# Recovery statistics
stats = recovery.get_statistics()
print(f"Files recovered: {stats.files_recovered}")
print(f"Data recovered: {stats.bytes_recovered} bytes")
```

### Task 4: MFT Analysis (NTFS)
**Input**: NTFS disk image or extracted MFT file

**Process**:
1. Locate and extract MFT
2. Parse MFT entries
3. Extract standard information attributes
4. Analyze file names and timestamps
5. Detect timestamp manipulation

**Output**: MFT analysis with timeline anomalies

**Example**:
```python
from disk_forensics import DiskAnalyzer, MFTParser

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
mft_parser = MFTParser(analyzer, volume_index=2)

# Parse entire MFT
entries = mft_parser.parse_all()
print(f"Total MFT entries: {len(entries)}")

# Get specific file entry
entry = mft_parser.get_entry_by_path("/Users/suspect/malware.exe")
if entry:
    print(f"File: {entry.filename}")
    print(f"Created: {entry.created_time}")
    print(f"Modified: {entry.modified_time}")
    print(f"Accessed: {entry.accessed_time}")
    print(f"MFT Modified: {entry.mft_modified_time}")

# Detect timestamp anomalies (timestomping)
anomalies = mft_parser.detect_timestamp_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.filename}")
    print(f"  Type: {a.anomaly_type}")
    print(f"  Details: {a.description}")

# Find files by MFT entry number
entry = mft_parser.get_entry_by_number(12345)

# Extract MFT to file
mft_parser.extract_mft("/evidence/extracted_mft.bin")

# Generate MFT timeline
mft_parser.export_timeline("/evidence/mft_timeline.csv")
```

### Task 5: Alternate Data Streams Analysis
**Input**: NTFS disk image

**Process**:
1. Scan for files with alternate data streams
2. Extract ADS content
3. Analyze ADS for malicious content
4. Check Zone.Identifier streams
5. Document ADS findings

**Output**: ADS inventory with extracted content

**Example**:
```python
from disk_forensics import DiskAnalyzer, ADSScanner

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
ads_scanner = ADSScanner(analyzer, volume_index=2)

# Find all alternate data streams
streams = ads_scanner.find_all_streams()

for stream in streams:
    print(f"File: {stream.parent_file}")
    print(f"  Stream: {stream.stream_name}")
    print(f"  Size: {stream.size} bytes")

# Extract specific stream
ads_scanner.extract_stream(
    file_path="/Users/suspect/document.docx",
    stream_name="Zone.Identifier",
    output_path="/evidence/zone_id.txt"
)

# Analyze Zone.Identifier streams (download origins)
zone_info = ads_scanner.analyze_zone_identifiers()
for zi in zone_info:
    print(f"File: {zi.filename}")
    print(f"  Download URL: {zi.referrer_url}")
    print(f"  Host URL: {zi.host_url}")
    print(f"  Zone: {zi.security_zone}")

# Find executable content in ADS
suspicious = ads_scanner.find_executable_ads()
for s in suspicious:
    print(f"SUSPICIOUS: {s.parent_file}:{s.stream_name}")
```

### Task 6: Volume Shadow Copy Analysis
**Input**: Windows disk image with VSS

**Process**:
1. Enumerate Volume Shadow Copies
2. Mount shadow copy for analysis
3. Compare files across shadow copies
4. Extract previous file versions
5. Timeline shadow copy changes

**Output**: VSS analysis with file version history

**Example**:
```python
from disk_forensics import DiskAnalyzer, VSSAnalyzer

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
vss_analyzer = VSSAnalyzer(analyzer, volume_index=2)

# List all shadow copies
shadows = vss_analyzer.list_shadow_copies()
for sc in shadows:
    print(f"Shadow Copy: {sc.id}")
    print(f"  Created: {sc.creation_time}")
    print(f"  Volume: {sc.volume_path}")

# Get file from specific shadow copy
file_content = vss_analyzer.extract_file(
    shadow_id=shadows[0].id,
    file_path="/Users/suspect/deleted_evidence.xlsx",
    output_path="/evidence/recovered_from_vss.xlsx"
)

# Compare file across shadow copies
diff = vss_analyzer.compare_file_versions(
    file_path="/Users/suspect/important.docx"
)
for version in diff:
    print(f"Version from {version.shadow_date}:")
    print(f"  Size: {version.size}")
    print(f"  Hash: {version.hash}")

# Find deleted files recoverable from VSS
recoverable = vss_analyzer.find_deleted_in_shadows()

# Export VSS timeline
vss_analyzer.export_timeline("/evidence/vss_timeline.csv")
```

### Task 7: File Signature Analysis
**Input**: Disk image or directory of files

**Process**:
1. Extract file headers/signatures
2. Compare to known file signatures
3. Identify mismatched extensions
4. Detect embedded files
5. Report signature anomalies

**Output**: File signature analysis with mismatches

**Example**:
```python
from disk_forensics import DiskAnalyzer, SignatureAnalyzer

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
sig_analyzer = SignatureAnalyzer(analyzer, volume_index=2)

# Analyze all files
results = sig_analyzer.analyze_all()

# Find extension mismatches
mismatches = sig_analyzer.find_mismatches()
for m in mismatches:
    print(f"MISMATCH: {m.file_path}")
    print(f"  Extension: {m.extension}")
    print(f"  Actual Type: {m.detected_type}")
    print(f"  Signature: {m.signature_hex}")

# Analyze specific file
file_info = sig_analyzer.analyze_file("/Users/suspect/image.jpg")
print(f"File: {file_info.path}")
print(f"Detected Type: {file_info.detected_type}")
print(f"MIME Type: {file_info.mime_type}")
print(f"Extension Valid: {file_info.extension_valid}")

# Find renamed executables
renamed_exe = sig_analyzer.find_renamed_executables()
for exe in renamed_exe:
    print(f"Hidden EXE: {exe.path} (disguised as {exe.extension})")

# Detect polyglot files (multiple valid signatures)
polyglots = sig_analyzer.find_polyglots()

# Export analysis report
sig_analyzer.export_report("/evidence/signature_analysis.csv")
```

### Task 8: Slack Space Analysis
**Input**: Disk image file

**Process**:
1. Identify file slack space locations
2. Extract slack space content
3. Search for readable data
4. Identify potential evidence
5. Document findings

**Output**: Slack space analysis with extracted data

**Example**:
```python
from disk_forensics import DiskAnalyzer, SlackSpaceAnalyzer

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
slack_analyzer = SlackSpaceAnalyzer(analyzer, volume_index=2)

# Analyze all slack space
results = slack_analyzer.analyze_all()
print(f"Total slack space: {results.total_bytes} bytes")
print(f"Slack with data: {results.data_bytes} bytes")

# Extract slack space from specific file
slack_data = slack_analyzer.get_file_slack("/Users/suspect/document.docx")
print(f"Slack content: {slack_data.content[:100]}")

# Search slack space for patterns
matches = slack_analyzer.search_slack(
    patterns=["password", "secret", "confidential"],
    case_sensitive=False
)
for m in matches:
    print(f"Found '{m.pattern}' in slack of {m.file_path}")
    print(f"  Context: {m.context}")

# Extract all readable strings from slack
strings = slack_analyzer.extract_strings(min_length=4)

# Export slack space content
slack_analyzer.export_slack_data("/evidence/slack_space/")
```

### Task 9: Partition Analysis
**Input**: Raw disk image or physical device

**Process**:
1. Read partition table (MBR/GPT)
2. Identify all partitions
3. Detect hidden partitions
4. Analyze unallocated space
5. Document partition layout

**Output**: Complete partition analysis

**Example**:
```python
from disk_forensics import DiskAnalyzer, PartitionAnalyzer

analyzer = DiskAnalyzer("/evidence/full_disk.dd")
partition_analyzer = PartitionAnalyzer(analyzer)

# Get partition table type
pt_type = partition_analyzer.get_partition_table_type()
print(f"Partition Table: {pt_type}")

# List all partitions
partitions = partition_analyzer.list_partitions()
for p in partitions:
    print(f"Partition {p.index}:")
    print(f"  Type: {p.type_name}")
    print(f"  Start: {p.start_sector}")
    print(f"  Size: {p.size_bytes} bytes")
    print(f"  File System: {p.file_system}")
    print(f"  Bootable: {p.bootable}")

# Detect hidden partitions
hidden = partition_analyzer.find_hidden_partitions()
for h in hidden:
    print(f"HIDDEN: Found at sector {h.start_sector}")

# Analyze gaps between partitions
gaps = partition_analyzer.find_unallocated_space()
for gap in gaps:
    print(f"Unallocated: {gap.start_sector} - {gap.end_sector}")
    print(f"  Size: {gap.size_bytes} bytes")

# Analyze deleted partitions
deleted = partition_analyzer.find_deleted_partitions()

# Export partition map
partition_analyzer.export_map("/evidence/partition_map.json")
```

### Task 10: Hash Analysis and Known File Detection
**Input**: Disk image or file collection

**Process**:
1. Calculate hashes for all files
2. Compare against known file databases
3. Identify known good files (NSRL)
4. Flag known malicious files
5. Generate hash report

**Output**: Hash analysis with categorization

**Example**:
```python
from disk_forensics import DiskAnalyzer, HashAnalyzer

analyzer = DiskAnalyzer("/evidence/disk_image.E01")
hash_analyzer = HashAnalyzer(analyzer, volume_index=2)

# Calculate hashes for all files
hashes = hash_analyzer.hash_all_files(
    algorithms=["md5", "sha1", "sha256"]
)

# Compare against NSRL (known good files)
nsrl_results = hash_analyzer.check_nsrl(
    nsrl_path="/hashsets/NSRLFile.txt"
)
print(f"Known good files: {nsrl_results.known_count}")
print(f"Unknown files: {nsrl_results.unknown_count}")

# Check against malware hash database
malware_check = hash_analyzer.check_malware_hashes(
    hash_db="/hashsets/malware_hashes.txt"
)
for match in malware_check.matches:
    print(f"MALWARE: {match.file_path}")
    print(f"  Hash: {match.hash}")
    print(f"  Malware Name: {match.malware_name}")

# Find duplicate files
duplicates = hash_analyzer.find_duplicates()
for dup_group in duplicates:
    print(f"Duplicate files (hash: {dup_group.hash}):")
    for f in dup_group.files:
        print(f"  - {f}")

# Export hash report
hash_analyzer.export_report(
    output_path="/evidence/hash_report.csv",
    format="csv"
)
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SLEUTHKIT_PATH` | Path to The Sleuth Kit binaries | No | System PATH |
| `NSRL_PATH` | Path to NSRL hash database | No | None |
| `YARA_RULES` | Path to YARA rules for file analysis | No | None |
| `CARVING_SIGNATURES` | Custom file carving signatures | No | Built-in |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `verify_image` | boolean | Verify image integrity on load |
| `cache_metadata` | boolean | Cache parsed metadata |
| `parallel_hash` | boolean | Parallel hash calculation |
| `carving_depth` | integer | Maximum carving depth in bytes |
| `timezone` | string | Timezone for timestamp display |

## Examples

### Example 1: Data Theft Investigation
**Scenario**: Investigating potential intellectual property theft

```python
from disk_forensics import DiskAnalyzer, FileSystemParser, MFTParser

# Load suspect's disk image
analyzer = DiskAnalyzer("/evidence/suspect_laptop.E01")
parser = FileSystemParser(analyzer, volume_index=2)

# Find recently accessed sensitive documents
recent_docs = parser.find_files_by_date(
    start_date="2024-01-01",
    end_date="2024-01-31",
    date_type="accessed",
    extensions=[".docx", ".xlsx", ".pdf", ".pptx"]
)

# Check USB device history
usb_artifacts = analyzer.get_usb_history()
for device in usb_artifacts:
    print(f"USB: {device.device_name}")
    print(f"  First connected: {device.first_connected}")
    print(f"  Last connected: {device.last_connected}")

# Analyze MFT for deleted documents
mft = MFTParser(analyzer, volume_index=2)
deleted = mft.find_deleted_entries(extensions=[".docx", ".xlsx"])

# Check cloud sync folders
cloud_folders = [
    "/Users/suspect/Dropbox",
    "/Users/suspect/OneDrive",
    "/Users/suspect/Google Drive"
]
for folder in cloud_folders:
    files = parser.list_directory(folder, recursive=True)
    print(f"Found {len(files)} files in {folder}")
```

### Example 2: Malware Persistence Analysis
**Scenario**: Finding malware persistence mechanisms on disk

```python
from disk_forensics import DiskAnalyzer, FileSystemParser, SignatureAnalyzer

analyzer = DiskAnalyzer("/evidence/infected_system.E01")
parser = FileSystemParser(analyzer, volume_index=2)
sig_analyzer = SignatureAnalyzer(analyzer, volume_index=2)

# Check common persistence locations
persistence_paths = [
    "/Windows/System32/Tasks",
    "/Users/*/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup",
    "/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup"
]

for path in persistence_paths:
    files = parser.list_directory(path)
    for f in files:
        print(f"Persistence: {f.name} - Created: {f.created_time}")

# Find hidden executables
hidden_exe = sig_analyzer.find_renamed_executables()

# Analyze Windows prefetch
prefetch_files = parser.find_files_by_extension([".pf"],
    path="/Windows/Prefetch")

# Check for suspicious services
services = parser.get_file("/Windows/System32/config/SYSTEM")
```

### Example 3: Deleted File Recovery Operation
**Scenario**: Recovering deleted evidence

```python
from disk_forensics import DiskAnalyzer, FileRecovery, VSSAnalyzer

analyzer = DiskAnalyzer("/evidence/suspect_disk.E01")

# Method 1: File system recovery
recovery = FileRecovery(analyzer)
fs_deleted = recovery.find_deleted_files()
print(f"Found {len(fs_deleted)} deleted files in file system")

# Method 2: File carving
carved = recovery.carve_files(
    file_types=["jpg", "png", "pdf", "docx", "xlsx"],
    output_dir="/evidence/carved_files/"
)
print(f"Carved {len(carved)} files from unallocated space")

# Method 3: Volume Shadow Copy recovery
vss = VSSAnalyzer(analyzer, volume_index=2)
shadows = vss.list_shadow_copies()

for shadow in shadows:
    vss_files = vss.list_deleted_in_shadow(shadow.id)
    for f in vss_files:
        vss.extract_file(shadow.id, f.path,
            f"/evidence/vss_recovery/{shadow.id}/{f.name}")
```

## Limitations

- Maximum supported disk image size depends on system resources
- EWF compression may slow analysis on large images
- File carving cannot recover fragmented files completely
- Encrypted volumes require decryption keys
- Some file systems may have limited support
- VSS analysis requires Windows images
- Hash database comparison requires external databases

## Troubleshooting

### Common Issue 1: Image Mount Failure
**Problem**: Unable to mount or read disk image
**Solution**:
- Verify image integrity with hash verification
- Check for supported image format (raw, E01, AFF)
- Ensure adequate disk space for cache

### Common Issue 2: File System Not Recognized
**Problem**: Unknown file system type
**Solution**:
- Check partition offset alignment
- Try manual file system specification
- Verify image is not encrypted

### Common Issue 3: Carving Produces Corrupt Files
**Problem**: Carved files are damaged or incomplete
**Solution**:
- Files may be fragmented
- Increase carving validation settings
- Use multiple carving tools for verification

### Common Issue 4: Slow Hash Calculation
**Problem**: Hashing takes too long
**Solution**:
- Enable parallel processing
- Use faster hash algorithm (MD5 vs SHA-256)
- Exclude known good files

## Related Skills

- [memory-forensics](../memory-forensics/): Volatile memory analysis
- [timeline-forensics](../timeline-forensics/): Super timeline creation
- [artifact-collection](../artifact-collection/): Evidence collection procedures
- [registry-forensics](../registry-forensics/): Windows registry analysis
- [malware-forensics](../malware-forensics/): Malware sample analysis

## References

- [Disk Forensics Reference](references/REFERENCE.md)
- [File System Analysis Guide](references/FILE_SYSTEMS.md)
- [File Carving Signatures](references/CARVING_SIGNATURES.md)
