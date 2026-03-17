---
name: mobile-forensics
description: |
  Analyze mobile device data for forensic investigation. Use when investigating
  incidents involving iOS or Android devices, mobile malware, data theft, or
  communications analysis. Supports logical and file system extractions.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: libimobiledevice, adb, plistlib
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Mobile Forensics

Comprehensive mobile forensics skill for analyzing iOS and Android device data. Enables extraction and analysis of communications, app data, location history, media files, and system artifacts from mobile device backups and extractions.

## Capabilities

- **iOS Analysis**: Parse iTunes/Finder backups, file system images
- **Android Analysis**: Parse ADB backups, file system extractions
- **Communications Analysis**: Extract SMS, MMS, calls, messaging apps
- **App Data Analysis**: Parse application databases and caches
- **Location Analysis**: Extract GPS data, location history, geofences
- **Media Analysis**: Catalog photos, videos with metadata
- **Contact Analysis**: Extract contacts from all sources
- **Browser History**: Mobile browser artifact analysis
- **Cloud Data**: Analyze synced cloud service data
- **Timeline Generation**: Create device activity timeline

## Quick Start

```python
from mobile_forensics import MobileAnalyzer, iOSParser, AndroidParser

# Analyze iOS backup
ios = iOSParser("/evidence/ios_backup/")
messages = ios.get_messages()
calls = ios.get_call_history()

# Analyze Android extraction
android = AndroidParser("/evidence/android_extraction/")
contacts = android.get_contacts()
```

## Usage

### Task 1: iOS Backup Analysis
**Input**: iTunes/Finder backup directory

**Process**:
1. Load and decrypt backup (if encrypted)
2. Parse Manifest database
3. Extract and analyze data
4. Parse application data
5. Generate device report

**Output**: Comprehensive iOS backup analysis

**Example**:
```python
from mobile_forensics import iOSParser

# Initialize parser
parser = iOSParser("/evidence/ios_backup/")

# Get backup info
info = parser.get_backup_info()
print(f"Device: {info.device_name}")
print(f"iOS Version: {info.ios_version}")
print(f"Serial: {info.serial_number}")
print(f"IMEI: {info.imei}")
print(f"Backup Date: {info.backup_date}")
print(f"Encrypted: {info.is_encrypted}")

# Decrypt if needed
if info.is_encrypted:
    parser.decrypt(password="backup_password")

# Get messages (SMS/iMessage)
messages = parser.get_messages()
for msg in messages:
    print(f"[{msg.date}] {msg.sender} -> {msg.recipient}")
    print(f"  Text: {msg.text}")
    print(f"  Type: {msg.message_type}")
    print(f"  Delivered: {msg.is_delivered}")
    print(f"  Read: {msg.is_read}")

# Get call history
calls = parser.get_call_history()
for call in calls:
    print(f"[{call.date}] {call.call_type}: {call.phone_number}")
    print(f"  Duration: {call.duration}s")
    print(f"  Location: {call.location}")

# Get contacts
contacts = parser.get_contacts()
for contact in contacts:
    print(f"Contact: {contact.name}")
    print(f"  Phone: {contact.phone_numbers}")
    print(f"  Email: {contact.emails}")

# Get Safari history
safari = parser.get_safari_history()
for entry in safari:
    print(f"[{entry.visit_date}] {entry.title}")
    print(f"  URL: {entry.url}")

# Get photos
photos = parser.get_photos()
for photo in photos:
    print(f"Photo: {photo.filename}")
    print(f"  Date: {photo.date_taken}")
    print(f"  Location: {photo.gps_location}")
    print(f"  Camera: {photo.camera_info}")

# Get location history
locations = parser.get_location_history()
for loc in locations:
    print(f"[{loc.timestamp}] {loc.latitude}, {loc.longitude}")
    print(f"  Accuracy: {loc.accuracy}m")
    print(f"  Source: {loc.source}")

# Export all data
parser.export_all("/evidence/ios_export/")
parser.generate_report("/evidence/ios_report.html")
```

### Task 2: Android Analysis
**Input**: Android backup or extraction

**Process**:
1. Load Android data
2. Parse databases
3. Extract communications
4. Analyze applications
5. Generate report

**Output**: Android device analysis

**Example**:
```python
from mobile_forensics import AndroidParser

# Initialize parser
parser = AndroidParser("/evidence/android_extraction/")

# Get device info
info = parser.get_device_info()
print(f"Device: {info.manufacturer} {info.model}")
print(f"Android: {info.android_version}")
print(f"Build: {info.build_number}")
print(f"Serial: {info.serial_number}")
print(f"IMEI: {info.imei}")

# Get SMS messages
sms = parser.get_sms()
for msg in sms:
    print(f"[{msg.date}] {msg.direction}: {msg.address}")
    print(f"  Body: {msg.body}")
    print(f"  Read: {msg.read}")

# Get call logs
calls = parser.get_call_logs()
for call in calls:
    print(f"[{call.date}] {call.type}: {call.number}")
    print(f"  Duration: {call.duration}s")
    print(f"  Name: {call.cached_name}")

# Get contacts
contacts = parser.get_contacts()
for contact in contacts:
    print(f"Contact: {contact.display_name}")
    print(f"  Numbers: {contact.phone_numbers}")
    print(f"  Account: {contact.account_type}")

# Get Chrome history
chrome = parser.get_chrome_history()
for entry in chrome:
    print(f"[{entry.visit_time}] {entry.title}")
    print(f"  URL: {entry.url}")

# Get WiFi networks
wifi = parser.get_wifi_networks()
for network in wifi:
    print(f"SSID: {network.ssid}")
    print(f"  Security: {network.security}")
    print(f"  First connected: {network.first_connected}")

# Get installed apps
apps = parser.get_installed_apps()
for app in apps:
    print(f"App: {app.name}")
    print(f"  Package: {app.package_name}")
    print(f"  Version: {app.version}")
    print(f"  Installed: {app.install_date}")

# Get location data
locations = parser.get_locations()

# Export and report
parser.export_all("/evidence/android_export/")
parser.generate_report("/evidence/android_report.html")
```

### Task 3: Messaging App Analysis
**Input**: Mobile device data

**Process**:
1. Identify installed messaging apps
2. Locate app databases
3. Parse message content
4. Extract media and attachments
5. Build conversation timeline

**Output**: Messaging app analysis

**Example**:
```python
from mobile_forensics import MessagingAnalyzer

# Initialize analyzer
analyzer = MessagingAnalyzer("/evidence/device_extraction/")

# Detect available messaging apps
apps = analyzer.detect_messaging_apps()
for app in apps:
    print(f"Found: {app.name}")
    print(f"  Data available: {app.has_data}")

# Parse WhatsApp
whatsapp = analyzer.parse_whatsapp()
print(f"WhatsApp messages: {len(whatsapp.messages)}")
print(f"WhatsApp contacts: {len(whatsapp.contacts)}")
print(f"WhatsApp groups: {len(whatsapp.groups)}")

for chat in whatsapp.chats:
    print(f"Chat with: {chat.contact_name}")
    print(f"  Messages: {chat.message_count}")
    print(f"  Last message: {chat.last_message_date}")

    for msg in chat.messages[-5:]:  # Last 5 messages
        print(f"    [{msg.timestamp}] {msg.sender}: {msg.content}")

# Parse Telegram
telegram = analyzer.parse_telegram()
for chat in telegram.chats:
    print(f"Telegram: {chat.title}")
    print(f"  Type: {chat.chat_type}")
    print(f"  Messages: {chat.message_count}")

# Parse Signal
signal = analyzer.parse_signal()
for conversation in signal.conversations:
    print(f"Signal: {conversation.recipient}")
    print(f"  Messages: {conversation.message_count}")

# Parse Facebook Messenger
messenger = analyzer.parse_messenger()

# Parse Instagram DMs
instagram = analyzer.parse_instagram()

# Export media
analyzer.export_media("/evidence/messaging_media/")

# Generate unified timeline
timeline = analyzer.create_timeline()
for event in timeline:
    print(f"[{event.timestamp}] {event.app}: {event.summary}")

# Generate report
analyzer.generate_report("/evidence/messaging_report.html")
```

### Task 4: Location Analysis
**Input**: Mobile device data

**Process**:
1. Extract GPS data from photos
2. Parse location databases
3. Analyze location history
4. Identify significant locations
5. Create location timeline

**Output**: Location analysis with maps

**Example**:
```python
from mobile_forensics import LocationAnalyzer

# Initialize analyzer
analyzer = LocationAnalyzer("/evidence/device_extraction/")

# Get all location data
locations = analyzer.get_all_locations()
print(f"Total location points: {len(locations)}")

for loc in locations[:10]:
    print(f"[{loc.timestamp}] {loc.latitude}, {loc.longitude}")
    print(f"  Source: {loc.source}")  # GPS, WiFi, Cell, Photo
    print(f"  Accuracy: {loc.accuracy}m")
    print(f"  Address: {loc.reverse_geocode}")

# Get significant locations (iOS)
significant = analyzer.get_significant_locations()
for loc in significant:
    print(f"Significant: {loc.label}")
    print(f"  Visits: {loc.visit_count}")
    print(f"  Average duration: {loc.avg_duration}")

# Get location history from Google
google_history = analyzer.get_google_location_history()

# Get photo locations
photo_locations = analyzer.get_photo_locations()
for photo in photo_locations:
    print(f"Photo: {photo.filename}")
    print(f"  Location: {photo.latitude}, {photo.longitude}")
    print(f"  Time: {photo.timestamp}")

# Find locations at specific time
time_locations = analyzer.get_locations_at_time(
    start="2024-01-15 09:00",
    end="2024-01-15 18:00"
)

# Find visits to location
visits = analyzer.find_visits_to_location(
    latitude=40.7128,
    longitude=-74.0060,
    radius_meters=100
)

# Create KML export
analyzer.export_kml("/evidence/locations.kml")

# Create timeline map
analyzer.create_map("/evidence/location_map.html")

# Generate location report
analyzer.generate_report("/evidence/location_report.html")
```

### Task 5: Application Data Analysis
**Input**: Mobile device extraction

**Process**:
1. Inventory installed applications
2. Locate app data directories
3. Parse app databases
4. Extract cached data
5. Analyze user activity

**Output**: Application analysis report

**Example**:
```python
from mobile_forensics import AppAnalyzer

# Initialize analyzer
analyzer = AppAnalyzer("/evidence/device_extraction/")

# Get installed apps
apps = analyzer.get_installed_apps()

for app in apps:
    print(f"App: {app.name}")
    print(f"  Package: {app.package_name}")
    print(f"  Version: {app.version}")
    print(f"  Install date: {app.install_date}")
    print(f"  Last used: {app.last_used}")
    print(f"  Data size: {app.data_size_mb}MB")

# Analyze specific app
app_data = analyzer.analyze_app("com.example.app")
print(f"Databases: {app_data.databases}")
print(f"Shared prefs: {app_data.shared_preferences}")
print(f"Cache files: {app_data.cache_files}")

# Parse SQLite databases in app
for db in app_data.databases:
    tables = analyzer.get_db_tables(db)
    print(f"Database: {db.name}")
    for table in tables:
        print(f"  Table: {table.name} ({table.row_count} rows)")

# Get app permissions
permissions = analyzer.get_app_permissions("com.example.app")
for perm in permissions:
    print(f"Permission: {perm.name}")
    print(f"  Granted: {perm.granted}")
    print(f"  Dangerous: {perm.is_dangerous}")

# Find apps with sensitive permissions
sensitive_apps = analyzer.find_apps_with_permissions([
    "READ_CONTACTS",
    "READ_SMS",
    "ACCESS_FINE_LOCATION",
    "CAMERA"
])

# Export app data
analyzer.export_app_data("com.example.app", "/evidence/app_export/")

# Generate app inventory report
analyzer.generate_report("/evidence/app_report.html")
```

### Task 6: Communications Timeline
**Input**: Mobile device data

**Process**:
1. Extract all communication types
2. Parse timestamps
3. Build unified timeline
4. Identify patterns
5. Detect anomalies

**Output**: Unified communications timeline

**Example**:
```python
from mobile_forensics import CommunicationsTimeline

# Initialize timeline
timeline = CommunicationsTimeline("/evidence/device_extraction/")

# Add all sources
timeline.add_sms()
timeline.add_calls()
timeline.add_imessage()
timeline.add_whatsapp()
timeline.add_telegram()
timeline.add_messenger()
timeline.add_email()

# Build unified timeline
events = timeline.build()

for event in events:
    print(f"[{event.timestamp}] {event.type} - {event.app}")
    print(f"  From: {event.sender}")
    print(f"  To: {event.recipient}")
    print(f"  Summary: {event.summary}")

# Filter by contact
contact_timeline = timeline.filter_by_contact("+1234567890")
print(f"Communications with contact: {len(contact_timeline)}")

# Filter by date range
date_timeline = timeline.filter_by_date(
    start="2024-01-01",
    end="2024-01-31"
)

# Get communication patterns
patterns = timeline.analyze_patterns()
print(f"Most contacted: {patterns.top_contacts}")
print(f"Peak hours: {patterns.peak_hours}")
print(f"App usage: {patterns.app_distribution}")

# Detect anomalies
anomalies = timeline.detect_anomalies()
for a in anomalies:
    print(f"ANOMALY: {a.description}")
    print(f"  Time: {a.timestamp}")
    print(f"  Significance: {a.significance}")

# Export timeline
timeline.export_csv("/evidence/communications_timeline.csv")
timeline.generate_report("/evidence/communications_report.html")
```

### Task 7: Media Analysis
**Input**: Mobile device photos and videos

**Process**:
1. Extract all media files
2. Parse EXIF metadata
3. Extract GPS coordinates
4. Identify faces/objects
5. Build media timeline

**Output**: Media analysis with metadata

**Example**:
```python
from mobile_forensics import MediaAnalyzer

# Initialize analyzer
analyzer = MediaAnalyzer("/evidence/device_extraction/")

# Get all media
media = analyzer.get_all_media()
print(f"Total photos: {media.photo_count}")
print(f"Total videos: {media.video_count}")
print(f"Total size: {media.total_size_gb}GB")

# Analyze photos
photos = analyzer.get_photos()
for photo in photos:
    print(f"Photo: {photo.filename}")
    print(f"  Date taken: {photo.date_taken}")
    print(f"  Camera: {photo.camera_make} {photo.camera_model}")
    print(f"  Location: {photo.latitude}, {photo.longitude}")
    print(f"  Size: {photo.width}x{photo.height}")

# Analyze videos
videos = analyzer.get_videos()
for video in videos:
    print(f"Video: {video.filename}")
    print(f"  Duration: {video.duration}s")
    print(f"  Date: {video.date_created}")
    print(f"  Location: {video.latitude}, {video.longitude}")

# Get media with locations
geotagged = analyzer.get_geotagged_media()
print(f"Media with GPS: {len(geotagged)}")

# Find media in date range
dated = analyzer.find_by_date(
    start="2024-01-01",
    end="2024-01-31"
)

# Find media by location
location_media = analyzer.find_by_location(
    latitude=40.7128,
    longitude=-74.0060,
    radius_km=1
)

# Export with metadata
analyzer.export_media("/evidence/media_export/")
analyzer.export_metadata("/evidence/media_metadata.csv")

# Generate media report
analyzer.generate_report("/evidence/media_report.html")
```

### Task 8: Cloud Data Analysis
**Input**: Mobile device cloud sync data

**Process**:
1. Identify synced services
2. Extract cloud tokens
3. Analyze synced data
4. Identify cloud accounts
5. Document cloud activity

**Output**: Cloud service analysis

**Example**:
```python
from mobile_forensics import CloudAnalyzer

# Initialize analyzer
analyzer = CloudAnalyzer("/evidence/device_extraction/")

# Detect cloud services
services = analyzer.detect_cloud_services()
for service in services:
    print(f"Cloud service: {service.name}")
    print(f"  Account: {service.account}")
    print(f"  Data available: {service.has_data}")

# Analyze iCloud data
icloud = analyzer.analyze_icloud()
print(f"iCloud account: {icloud.account_email}")
print(f"iCloud Drive files: {len(icloud.drive_files)}")
print(f"iCloud Photos: {icloud.photo_count}")
print(f"Synced contacts: {icloud.contact_count}")

# Analyze Google account data
google = analyzer.analyze_google()
print(f"Google account: {google.account_email}")
print(f"Drive files: {len(google.drive_files)}")
print(f"Photos: {google.photo_count}")

# Get cloud tokens (for authorized access)
tokens = analyzer.extract_cloud_tokens()
for token in tokens:
    print(f"Token for: {token.service}")
    print(f"  Type: {token.token_type}")
    print(f"  Expires: {token.expiry}")

# Analyze cloud backup data
backups = analyzer.get_cloud_backups()
for backup in backups:
    print(f"Backup: {backup.service}")
    print(f"  Date: {backup.backup_date}")
    print(f"  Size: {backup.size_mb}MB")

# Generate cloud report
analyzer.generate_report("/evidence/cloud_report.html")
```

### Task 9: Deleted Data Recovery
**Input**: Mobile device file system

**Process**:
1. Analyze free space
2. Recover deleted files
3. Parse deleted database records
4. Reconstruct deleted messages
5. Document recovery results

**Output**: Recovered deleted data

**Example**:
```python
from mobile_forensics import DeletedDataRecovery

# Initialize recovery
recovery = DeletedDataRecovery("/evidence/device_extraction/")

# Recover deleted SQLite records
messages = recovery.recover_deleted_messages()
for msg in messages:
    print(f"RECOVERED: [{msg.date}] {msg.sender}")
    print(f"  Content: {msg.content}")
    print(f"  Recovery confidence: {msg.confidence}")

# Recover deleted photos
photos = recovery.recover_deleted_photos(
    output_dir="/evidence/recovered_photos/"
)
for photo in photos:
    print(f"Recovered: {photo.filename}")
    print(f"  Original path: {photo.original_path}")
    print(f"  Confidence: {photo.confidence}")

# Recover deleted contacts
contacts = recovery.recover_deleted_contacts()

# Recover deleted call logs
calls = recovery.recover_deleted_calls()

# Recover from WhatsApp
whatsapp = recovery.recover_deleted_whatsapp()

# Analyze SQLite WAL files
wal_data = recovery.analyze_wal_files()
for entry in wal_data:
    print(f"WAL recovery: {entry.table}")
    print(f"  Records: {entry.record_count}")

# Generate recovery report
recovery.generate_report("/evidence/recovery_report.html")
```

### Task 10: Mobile Malware Analysis
**Input**: Mobile device data

**Process**:
1. Scan for known malware
2. Identify suspicious apps
3. Analyze permissions abuse
4. Check for rootkit indicators
5. Generate threat report

**Output**: Mobile threat analysis

**Example**:
```python
from mobile_forensics import MobileThreatAnalyzer

# Initialize analyzer
analyzer = MobileThreatAnalyzer("/evidence/device_extraction/")

# Scan for known malware
malware = analyzer.scan_for_malware()
for m in malware:
    print(f"MALWARE: {m.app_name}")
    print(f"  Package: {m.package_name}")
    print(f"  Family: {m.malware_family}")
    print(f"  Confidence: {m.confidence}")

# Check for suspicious apps
suspicious = analyzer.find_suspicious_apps()
for app in suspicious:
    print(f"SUSPICIOUS: {app.name}")
    print(f"  Reason: {app.reason}")
    print(f"  Permissions: {app.suspicious_permissions}")

# Check for root/jailbreak
root_status = analyzer.check_root_status()
print(f"Device rooted: {root_status.is_rooted}")
print(f"Indicators: {root_status.indicators}")

# Check for spyware indicators
spyware = analyzer.detect_spyware()
for s in spyware:
    print(f"SPYWARE INDICATOR: {s.indicator}")
    print(f"  Details: {s.details}")

# Analyze app network behavior
network = analyzer.analyze_app_network()
for app in network:
    print(f"App: {app.name}")
    print(f"  Domains contacted: {app.domains}")
    print(f"  Suspicious: {app.suspicious_connections}")

# Generate threat report
analyzer.generate_report("/evidence/threat_report.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ADB_PATH` | Path to ADB binary | No | System PATH |
| `BACKUP_PASSWORD` | iOS backup password | No | None |
| `MAPS_API_KEY` | API key for map generation | No | None |
| `MALWARE_HASHES` | Path to malware hash database | No | None |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `decrypt_backup` | boolean | Attempt backup decryption |
| `recover_deleted` | boolean | Attempt deleted data recovery |
| `extract_media` | boolean | Extract media files |
| `geocode_locations` | boolean | Reverse geocode coordinates |
| `parallel` | boolean | Enable parallel processing |

## Examples

### Example 1: Criminal Investigation
**Scenario**: Analyzing suspect's phone for evidence

```python
from mobile_forensics import MobileAnalyzer

# Load device extraction
analyzer = MobileAnalyzer("/evidence/suspect_phone/")

# Get all communications
timeline = analyzer.get_communications_timeline()

# Filter for relevant time period
incident_comms = timeline.filter_by_date(
    start="2024-01-14",
    end="2024-01-16"
)

# Get location during incident
locations = analyzer.get_locations_at_time(
    start="2024-01-15 22:00",
    end="2024-01-16 02:00"
)

# Find communications with specific number
suspect_contact = timeline.filter_by_contact("+1234567890")

# Export evidence
analyzer.export_evidence("/evidence/case_evidence/")
```

### Example 2: Corporate Investigation
**Scenario**: Investigating data theft via mobile device

```python
from mobile_forensics import MobileAnalyzer, CloudAnalyzer

# Analyze company phone
analyzer = MobileAnalyzer("/evidence/employee_phone/")

# Check for unauthorized cloud services
cloud = CloudAnalyzer("/evidence/employee_phone/")
services = cloud.detect_cloud_services()

# Find file sharing activity
file_activity = analyzer.search_for_files(
    extensions=[".pdf", ".xlsx", ".docx"]
)

# Check messaging for data sharing
messaging = analyzer.get_messaging_data()
attachments = messaging.find_attachments()
```

## Limitations

- Encrypted devices require passcode/credentials
- Some app data may be encrypted by app
- Cloud data access requires proper authorization
- Deleted data recovery success varies
- Some features require physical extraction
- App-specific parsing may have limited support
- Location data depends on user settings

## Troubleshooting

### Common Issue 1: Encrypted Backup
**Problem**: Cannot read encrypted iOS backup
**Solution**:
- Provide backup password
- Use backup password recovery tools
- Request password from device owner

### Common Issue 2: ADB Connection Issues
**Problem**: Cannot connect to Android device
**Solution**:
- Enable USB debugging
- Accept RSA fingerprint
- Try different USB cable/port

### Common Issue 3: Missing App Data
**Problem**: Expected app data not found
**Solution**:
- App may use cloud-only storage
- Data may be encrypted by app
- Check for app-specific backup location

## Related Skills

- [memory-forensics](../memory-forensics/): Device memory analysis
- [disk-forensics](../disk-forensics/): Device storage analysis
- [network-forensics](../network-forensics/): Mobile traffic analysis
- [cloud-forensics](../cloud-forensics/): Cloud-synced data analysis
- [timeline-forensics](../timeline-forensics/): Timeline integration

## References

- [Mobile Forensics Reference](references/REFERENCE.md)
- [iOS Artifact Guide](references/IOS_ARTIFACTS.md)
- [Android Artifact Guide](references/ANDROID_ARTIFACTS.md)
