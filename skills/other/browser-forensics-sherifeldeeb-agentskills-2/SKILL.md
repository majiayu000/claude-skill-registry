---
name: browser-forensics
description: |
  Analyze web browser artifacts for forensic investigation. Use when investigating
  user browsing activity, downloaded files, cached content, or web-based attacks.
  Supports Chrome, Firefox, Edge, Safari, and Internet Explorer artifacts.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Optional: sqlite3, pycryptodome, ccl_chrome_indexeddb
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: forensics
---

# Browser Forensics

Comprehensive browser forensics skill for analyzing web browser artifacts including history, downloads, cookies, cache, autofill data, and stored credentials. Enables reconstruction of user browsing activity, identification of malicious sites visited, and extraction of forensically valuable data from major browsers.

## Capabilities

- **Browsing History Analysis**: Extract and analyze browsing history from all major browsers
- **Download Analysis**: Track downloaded files with sources and timestamps
- **Cookie Analysis**: Extract and decode cookies, including encrypted values
- **Cache Extraction**: Recover cached web content and media
- **Form Data/Autofill**: Extract autofill data, saved forms, and search terms
- **Credential Extraction**: Recover saved passwords (where legally permitted)
- **Session Analysis**: Analyze active sessions and session restoration data
- **Extension Analysis**: Inventory and analyze installed browser extensions
- **Bookmark Analysis**: Extract and analyze bookmarks and reading lists
- **Cross-Browser Correlation**: Correlate activity across multiple browsers

## Quick Start

```python
from browser_forensics import BrowserAnalyzer, ChromeParser, FirefoxParser

# Initialize browser analyzer with profile path
analyzer = BrowserAnalyzer("/evidence/user_profile/")

# Auto-detect and parse all browsers
browsers = analyzer.detect_browsers()

# Get combined browsing history
history = analyzer.get_combined_history()

# Get downloads across browsers
downloads = analyzer.get_all_downloads()
```

## Usage

### Task 1: Chrome/Chromium Analysis
**Input**: Chrome user profile directory

**Process**:
1. Locate Chrome profile data
2. Parse SQLite databases
3. Decrypt protected data
4. Extract artifacts
5. Generate analysis report

**Output**: Comprehensive Chrome artifact analysis

**Example**:
```python
from browser_forensics import ChromeParser

# Initialize Chrome parser
parser = ChromeParser("/evidence/Chrome/Default/")

# Get browsing history
history = parser.get_history()
for entry in history:
    print(f"[{entry.visit_time}] {entry.title}")
    print(f"  URL: {entry.url}")
    print(f"  Visit count: {entry.visit_count}")
    print(f"  Typed count: {entry.typed_count}")
    print(f"  Transition: {entry.transition_type}")

# Get downloads
downloads = parser.get_downloads()
for dl in downloads:
    print(f"Download: {dl.filename}")
    print(f"  URL: {dl.url}")
    print(f"  Size: {dl.total_bytes}")
    print(f"  Start time: {dl.start_time}")
    print(f"  End time: {dl.end_time}")
    print(f"  State: {dl.state}")
    print(f"  Danger type: {dl.danger_type}")

# Get cookies
cookies = parser.get_cookies()
for cookie in cookies:
    print(f"Cookie: {cookie.name}")
    print(f"  Domain: {cookie.host}")
    print(f"  Value: {cookie.value}")
    print(f"  Expires: {cookie.expires}")
    print(f"  Secure: {cookie.is_secure}")
    print(f"  HTTPOnly: {cookie.is_httponly}")

# Get autofill data
autofill = parser.get_autofill()
for entry in autofill:
    print(f"Autofill: {entry.name} = {entry.value}")
    print(f"  Use count: {entry.count}")
    print(f"  Last used: {entry.last_used}")

# Get saved credentials (requires decryption key)
credentials = parser.get_credentials(decrypt_key=decrypt_key)
for cred in credentials:
    print(f"Login: {cred.origin_url}")
    print(f"  Username: {cred.username}")
    print(f"  Created: {cred.date_created}")

# Get extensions
extensions = parser.get_extensions()
for ext in extensions:
    print(f"Extension: {ext.name}")
    print(f"  ID: {ext.id}")
    print(f"  Version: {ext.version}")
    print(f"  Enabled: {ext.enabled}")
    print(f"  Permissions: {ext.permissions}")

# Export report
parser.generate_report("/evidence/chrome_analysis.html")
```

### Task 2: Firefox Analysis
**Input**: Firefox profile directory

**Process**:
1. Locate Firefox profile
2. Parse places.sqlite and other databases
3. Decrypt protected data
4. Extract artifacts
5. Generate report

**Output**: Firefox artifact analysis

**Example**:
```python
from browser_forensics import FirefoxParser

# Initialize Firefox parser
parser = FirefoxParser("/evidence/Firefox/Profiles/xxxxxxxx.default/")

# Get browsing history
history = parser.get_history()
for entry in history:
    print(f"[{entry.visit_date}] {entry.title}")
    print(f"  URL: {entry.url}")
    print(f"  Visit type: {entry.visit_type}")
    print(f"  From visit: {entry.from_visit}")

# Get downloads
downloads = parser.get_downloads()
for dl in downloads:
    print(f"Download: {dl.name}")
    print(f"  Source: {dl.source}")
    print(f"  Target: {dl.target}")
    print(f"  Start: {dl.start_time}")
    print(f"  End: {dl.end_time}")
    print(f"  State: {dl.state}")

# Get bookmarks
bookmarks = parser.get_bookmarks()
for bm in bookmarks:
    print(f"Bookmark: {bm.title}")
    print(f"  URL: {bm.url}")
    print(f"  Added: {bm.date_added}")
    print(f"  Folder: {bm.folder}")

# Get form history
forms = parser.get_form_history()
for form in forms:
    print(f"Form: {form.field_name} = {form.value}")
    print(f"  Times used: {form.times_used}")
    print(f"  Last used: {form.last_used}")

# Get session data
sessions = parser.get_sessions()
for session in sessions:
    print(f"Session window: {session.window_id}")
    for tab in session.tabs:
        print(f"  Tab: {tab.title} - {tab.url}")

# Get cookies
cookies = parser.get_cookies()

# Get credentials
credentials = parser.get_credentials()

# Export report
parser.generate_report("/evidence/firefox_analysis.html")
```

### Task 3: Edge Analysis
**Input**: Microsoft Edge profile directory

**Process**:
1. Locate Edge profile data
2. Parse Chromium-based databases
3. Extract Edge-specific artifacts
4. Analyze reading list and collections
5. Generate report

**Output**: Edge artifact analysis

**Example**:
```python
from browser_forensics import EdgeParser

# Initialize Edge parser
parser = EdgeParser("/evidence/Edge/Default/")

# Get browsing history
history = parser.get_history()

# Get downloads
downloads = parser.get_downloads()

# Get collections (Edge-specific)
collections = parser.get_collections()
for collection in collections:
    print(f"Collection: {collection.name}")
    print(f"  Created: {collection.created}")
    print(f"  Items: {len(collection.items)}")
    for item in collection.items:
        print(f"    - {item.title}: {item.url}")

# Get reading list
reading_list = parser.get_reading_list()
for item in reading_list:
    print(f"Reading: {item.title}")
    print(f"  URL: {item.url}")
    print(f"  Added: {item.added_date}")

# Get favorites (bookmarks)
favorites = parser.get_favorites()

# Get IE mode data
ie_mode = parser.get_ie_mode_history()

# Export report
parser.generate_report("/evidence/edge_analysis.html")
```

### Task 4: Safari Analysis
**Input**: Safari data directory (macOS)

**Process**:
1. Locate Safari data files
2. Parse History.db and other databases
3. Extract browser state
4. Analyze reading list
5. Generate report

**Output**: Safari artifact analysis

**Example**:
```python
from browser_forensics import SafariParser

# Initialize Safari parser
parser = SafariParser("/evidence/Safari/")

# Get browsing history
history = parser.get_history()
for entry in history:
    print(f"[{entry.visit_time}] {entry.title}")
    print(f"  URL: {entry.url}")
    print(f"  Redirect source: {entry.redirect_source}")

# Get downloads
downloads = parser.get_downloads()
for dl in downloads:
    print(f"Download: {dl.filename}")
    print(f"  URL: {dl.url}")
    print(f"  Download date: {dl.download_date}")
    print(f"  Remove when done: {dl.remove_when_done}")

# Get bookmarks
bookmarks = parser.get_bookmarks()

# Get reading list
reading_list = parser.get_reading_list()
for item in reading_list:
    print(f"Reading: {item.title}")
    print(f"  URL: {item.url}")
    print(f"  Added: {item.date_added}")
    print(f"  Preview text: {item.preview_text[:100]}")

# Get top sites
top_sites = parser.get_top_sites()

# Get last session
session = parser.get_last_session()

# Export report
parser.generate_report("/evidence/safari_analysis.html")
```

### Task 5: Browser Cache Analysis
**Input**: Browser cache directory

**Process**:
1. Locate cache files
2. Parse cache index
3. Extract cached content
4. Identify file types
5. Recover deleted cache

**Output**: Extracted cache contents

**Example**:
```python
from browser_forensics import CacheAnalyzer

# Initialize cache analyzer
analyzer = CacheAnalyzer("/evidence/Chrome/Default/Cache/")

# Get cache index
index = analyzer.parse_index()
print(f"Total cached items: {len(index)}")
print(f"Cache size: {analyzer.total_size_mb}MB")

# Get cached items by type
by_type = analyzer.group_by_type()
for mime_type, items in by_type.items():
    print(f"{mime_type}: {len(items)} items")

# Extract specific content types
images = analyzer.extract_by_type(
    ["image/jpeg", "image/png", "image/gif"],
    output_dir="/evidence/cache/images/"
)

# Extract all cached files
all_files = analyzer.extract_all(output_dir="/evidence/cache/all/")
for f in all_files:
    print(f"Cached: {f.url}")
    print(f"  Type: {f.content_type}")
    print(f"  Size: {f.size}")
    print(f"  Cached: {f.cached_time}")
    print(f"  Extracted to: {f.output_path}")

# Search cache for patterns
matches = analyzer.search_content(
    patterns=["password", "api_key", "token"],
    search_type="text"
)
for m in matches:
    print(f"Found '{m.pattern}' in {m.url}")
    print(f"  Context: {m.context}")

# Recover deleted cache entries
recovered = analyzer.recover_deleted()

# Export cache inventory
analyzer.export_inventory("/evidence/cache_inventory.csv")
```

### Task 6: Cross-Browser Timeline
**Input**: Multiple browser profiles

**Process**:
1. Parse all browser artifacts
2. Normalize timestamps
3. Merge activity timelines
4. Identify patterns
5. Generate unified timeline

**Output**: Cross-browser activity timeline

**Example**:
```python
from browser_forensics import BrowserTimeline

# Initialize timeline builder
timeline = BrowserTimeline()

# Add browser profiles
timeline.add_chrome("/evidence/Chrome/Default/")
timeline.add_firefox("/evidence/Firefox/Profiles/default/")
timeline.add_edge("/evidence/Edge/Default/")
timeline.add_safari("/evidence/Safari/")

# Build unified timeline
events = timeline.build()

for event in events:
    print(f"[{event.timestamp}] {event.browser} - {event.event_type}")
    print(f"  URL: {event.url}")
    print(f"  Title: {event.title}")

# Filter by date range
filtered = timeline.filter_by_date(
    start="2024-01-01",
    end="2024-01-31"
)

# Filter by domain
domain_activity = timeline.filter_by_domain("example.com")

# Get activity frequency
frequency = timeline.get_activity_frequency()
for hour, count in frequency.hourly.items():
    print(f"Hour {hour}: {count} events")

# Detect unusual patterns
patterns = timeline.detect_unusual_patterns()
for p in patterns:
    print(f"Pattern: {p.description}")
    print(f"  Significance: {p.significance}")

# Export timeline
timeline.export_csv("/evidence/browser_timeline.csv")
timeline.export_html("/evidence/browser_timeline.html")
```

### Task 7: Download Analysis
**Input**: Browser download histories

**Process**:
1. Extract download records
2. Verify file existence
3. Calculate file hashes
4. Check against threat intel
5. Correlate with browsing history

**Output**: Download analysis with risk assessment

**Example**:
```python
from browser_forensics import DownloadAnalyzer

# Initialize download analyzer
analyzer = DownloadAnalyzer()

# Add browser profiles
analyzer.add_browser("chrome", "/evidence/Chrome/Default/")
analyzer.add_browser("firefox", "/evidence/Firefox/default/")

# Get all downloads
downloads = analyzer.get_all_downloads()

for dl in downloads:
    print(f"Download: {dl.filename}")
    print(f"  Browser: {dl.browser}")
    print(f"  URL: {dl.source_url}")
    print(f"  Referrer: {dl.referrer}")
    print(f"  Time: {dl.download_time}")
    print(f"  Size: {dl.size}")
    print(f"  Exists: {dl.file_exists}")
    if dl.file_exists:
        print(f"  SHA256: {dl.sha256}")

# Find executable downloads
executables = analyzer.find_executables()
for exe in executables:
    print(f"EXE: {exe.filename}")
    print(f"  Risk score: {exe.risk_score}")

# Check against VirusTotal (requires API key)
vt_results = analyzer.check_virustotal(api_key=VT_API_KEY)
for result in vt_results:
    print(f"VT: {result.filename}")
    print(f"  Detections: {result.detections}/{result.total}")

# Find downloads from suspicious domains
suspicious = analyzer.find_suspicious_downloads()

# Get downloads by source domain
by_domain = analyzer.group_by_domain()

# Export download report
analyzer.generate_report("/evidence/downloads_report.html")
```

### Task 8: Cookie Analysis
**Input**: Browser cookie databases

**Process**:
1. Extract all cookies
2. Decrypt protected values
3. Analyze tracking cookies
4. Identify session cookies
5. Check for sensitive data

**Output**: Cookie analysis report

**Example**:
```python
from browser_forensics import CookieAnalyzer

# Initialize cookie analyzer
analyzer = CookieAnalyzer()
analyzer.add_browser("chrome", "/evidence/Chrome/Default/")
analyzer.add_browser("firefox", "/evidence/Firefox/default/")

# Get all cookies
cookies = analyzer.get_all_cookies()
print(f"Total cookies: {len(cookies)}")

# Group by domain
by_domain = analyzer.group_by_domain()
for domain, domain_cookies in by_domain.items():
    print(f"{domain}: {len(domain_cookies)} cookies")

# Find tracking cookies
tracking = analyzer.find_tracking_cookies()
for t in tracking:
    print(f"Tracker: {t.domain}")
    print(f"  Type: {t.tracker_type}")
    print(f"  Cookies: {len(t.cookies)}")

# Find session cookies
sessions = analyzer.find_session_cookies()
for s in sessions:
    print(f"Session: {s.domain}")
    print(f"  Cookie: {s.name}")
    print(f"  Expires: {s.expires}")

# Find authentication cookies
auth_cookies = analyzer.find_auth_cookies()
for auth in auth_cookies:
    print(f"Auth cookie: {auth.domain}")
    print(f"  Name: {auth.name}")

# Analyze cookie expiration
expiration = analyzer.analyze_expiration()
print(f"Expired: {expiration.expired}")
print(f"Persistent: {expiration.persistent}")
print(f"Session: {expiration.session}")

# Export cookie report
analyzer.generate_report("/evidence/cookies_report.html")
```

### Task 9: Extension/Add-on Analysis
**Input**: Browser extension directories

**Process**:
1. Inventory installed extensions
2. Analyze permissions
3. Identify suspicious extensions
4. Check against known malicious
5. Extract extension data

**Output**: Extension security analysis

**Example**:
```python
from browser_forensics import ExtensionAnalyzer

# Initialize extension analyzer
analyzer = ExtensionAnalyzer()
analyzer.add_chrome("/evidence/Chrome/Default/")
analyzer.add_firefox("/evidence/Firefox/default/")
analyzer.add_edge("/evidence/Edge/Default/")

# Get all extensions
extensions = analyzer.get_all_extensions()

for ext in extensions:
    print(f"Extension: {ext.name}")
    print(f"  Browser: {ext.browser}")
    print(f"  ID: {ext.id}")
    print(f"  Version: {ext.version}")
    print(f"  Enabled: {ext.enabled}")
    print(f"  Permissions: {ext.permissions}")
    print(f"  Web store URL: {ext.web_store_url}")

# Analyze permissions
risky = analyzer.find_risky_permissions()
for r in risky:
    print(f"RISKY: {r.name}")
    print(f"  Permissions: {r.risky_permissions}")
    print(f"  Risk level: {r.risk_level}")

# Check against known malicious
malicious = analyzer.check_known_malicious()
for m in malicious:
    print(f"MALICIOUS: {m.name}")
    print(f"  Reason: {m.reason}")

# Find extensions with content scripts
content_scripts = analyzer.find_content_scripts()
for cs in content_scripts:
    print(f"Content script: {cs.extension_name}")
    print(f"  Matches: {cs.matches}")

# Export extension inventory
analyzer.generate_report("/evidence/extensions_report.html")
```

### Task 10: Form and Search Analysis
**Input**: Browser autofill and search data

**Process**:
1. Extract form autofill data
2. Parse search history
3. Analyze search patterns
4. Extract credit card data
5. Find sensitive information

**Output**: Form and search analysis

**Example**:
```python
from browser_forensics import FormAnalyzer

# Initialize form analyzer
analyzer = FormAnalyzer()
analyzer.add_browser("chrome", "/evidence/Chrome/Default/")
analyzer.add_browser("firefox", "/evidence/Firefox/default/")

# Get autofill entries
autofill = analyzer.get_autofill()
for entry in autofill:
    print(f"Field: {entry.field_name}")
    print(f"  Value: {entry.value}")
    print(f"  Use count: {entry.count}")
    print(f"  Last used: {entry.last_used}")

# Get search history
searches = analyzer.get_search_history()
for search in searches:
    print(f"Search: {search.query}")
    print(f"  Engine: {search.search_engine}")
    print(f"  Time: {search.timestamp}")

# Find sensitive data in forms
sensitive = analyzer.find_sensitive_data()
for s in sensitive:
    print(f"SENSITIVE: {s.data_type}")
    print(f"  Field: {s.field_name}")
    print(f"  Masked value: {s.masked_value}")

# Get addresses
addresses = analyzer.get_addresses()
for addr in addresses:
    print(f"Address: {addr.name}")
    print(f"  Street: {addr.street}")
    print(f"  City: {addr.city}")

# Get credit cards (last 4 digits only)
cards = analyzer.get_credit_cards()
for card in cards:
    print(f"Card: **** **** **** {card.last_four}")
    print(f"  Name: {card.cardholder_name}")
    print(f"  Expiry: {card.expiry}")

# Analyze search patterns
patterns = analyzer.analyze_search_patterns()
print(f"Top searches: {patterns.top_queries}")
print(f"Search engines used: {patterns.engines}")

# Export form analysis
analyzer.generate_report("/evidence/forms_report.html")
```

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BROWSER_DECRYPT_KEY` | Key for credential decryption | No | None |
| `VT_API_KEY` | VirusTotal API key | No | None |
| `CACHE_EXTRACT_PATH` | Default cache extraction path | No | ./cache |
| `TIMEZONE` | Timezone for timestamp display | No | UTC |

### Options
| Option | Type | Description |
|--------|------|-------------|
| `decrypt_passwords` | boolean | Attempt password decryption |
| `extract_cache` | boolean | Extract cache contents |
| `include_deleted` | boolean | Attempt to recover deleted data |
| `parallel` | boolean | Enable parallel processing |
| `hash_files` | boolean | Calculate hashes for downloads |

## Examples

### Example 1: Investigating Web-Based Attack
**Scenario**: User clicked malicious link, investigating browser activity

```python
from browser_forensics import BrowserAnalyzer, DownloadAnalyzer

# Load user's browser profile
analyzer = BrowserAnalyzer("/evidence/user_profile/")

# Get browsing history around incident time
history = analyzer.get_combined_history()
incident_window = [h for h in history
    if "2024-01-15 10:00" <= str(h.visit_time) <= "2024-01-15 11:00"]

for entry in incident_window:
    print(f"[{entry.visit_time}] {entry.url}")
    if "redirect" in entry.transition_type.lower():
        print(f"  ** REDIRECT **")

# Check downloads
downloads = DownloadAnalyzer()
downloads.add_browser("all", "/evidence/user_profile/")
recent_downloads = downloads.get_downloads_in_range(
    start="2024-01-15 10:00",
    end="2024-01-15 11:00"
)

for dl in recent_downloads:
    print(f"DOWNLOAD: {dl.filename}")
    print(f"  Source: {dl.source_url}")
    print(f"  Danger type: {dl.danger_type}")
```

### Example 2: Data Exfiltration Investigation
**Scenario**: Investigating potential data leak via browser

```python
from browser_forensics import BrowserAnalyzer, CookieAnalyzer

analyzer = BrowserAnalyzer("/evidence/suspect_profile/")

# Find cloud storage/file sharing uploads
upload_urls = analyzer.search_history(
    patterns=["upload", "drive.google", "dropbox", "wetransfer", "pastebin"]
)

for url in upload_urls:
    print(f"Upload activity: {url.url}")
    print(f"  Time: {url.visit_time}")

# Check for webmail usage
webmail = analyzer.search_history(
    patterns=["mail.google", "outlook.live", "mail.yahoo"]
)

# Analyze cookies for session data
cookies = CookieAnalyzer()
cookies.add_browser("all", "/evidence/suspect_profile/")
cloud_sessions = cookies.find_cookies_for_domains([
    "google.com", "dropbox.com", "onedrive.live.com"
])
```

## Limitations

- Encrypted databases require decryption keys
- Some artifacts may be overwritten by browser
- Private/incognito browsing leaves minimal traces
- Cloud-synced browsers may have incomplete local data
- Cache extraction may recover partial files
- Extension analysis limited to manifest data
- Password recovery requires appropriate keys/permissions

## Troubleshooting

### Common Issue 1: Database Locked
**Problem**: Cannot read browser database
**Solution**:
- Close the browser before analysis
- Copy database files for offline analysis
- Use journal files for recovery

### Common Issue 2: Decryption Failure
**Problem**: Cannot decrypt protected data
**Solution**:
- Obtain appropriate decryption key
- Use DPAPI tools for Windows
- Check keychain for macOS

### Common Issue 3: Missing History
**Problem**: History appears incomplete
**Solution**:
- Check for history limits
- Analyze all profile folders
- Check cloud sync status

## Related Skills

- [disk-forensics](../disk-forensics/): Recover deleted browser data
- [memory-forensics](../memory-forensics/): Extract browser data from RAM
- [timeline-forensics](../timeline-forensics/): Integrate browser timeline
- [email-forensics](../email-forensics/): Webmail analysis
- [network-forensics](../network-forensics/): Correlate with traffic

## References

- [Browser Forensics Reference](references/REFERENCE.md)
- [Browser Database Schemas](references/DB_SCHEMAS.md)
- [Cookie Decryption Guide](references/COOKIE_DECRYPT.md)
