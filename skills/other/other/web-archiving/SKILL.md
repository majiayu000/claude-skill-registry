---
name: web-archiving
description: Web page archiving and retrieval from cached/deleted sources. Use when accessing unavailable pages, preserving web content, creating legal evidence archives, or building redundant archival workflows. Covers Wayback Machine, Archive.today, ArchiveBox, and evidence preservation tools.
---

# Web archiving methodology

Patterns for accessing inaccessible web pages and preserving web content for journalism, research, and legal purposes.

## Archive service hierarchy

Try services in this order for maximum coverage:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHIVE RETRIEVAL CASCADE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Wayback Machine (archive.org)                               │
│     └─ 916B+ pages, historical depth, API access                │
│                         ↓ not found                              │
│  2. Archive.today (archive.is/archive.ph)                       │
│     └─ On-demand snapshots, paywall bypass                      │
│                         ↓ not found                              │
│  3. Google Cache (limited availability)                         │
│     └─ Recent pages, search: cache:url                          │
│                         ↓ not found                              │
│  4. Bing Cache                                                  │
│     └─ Click dropdown arrow in search results                   │
│                         ↓ not found                              │
│  5. Memento Time Travel (aggregator)                            │
│     └─ Searches multiple archives simultaneously                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Wayback Machine API

### Check if URL is archived

```python
import requests
from typing import Optional
from datetime import datetime

def check_wayback_availability(url: str) -> Optional[dict]:
    """Check if URL exists in Wayback Machine."""
    api_url = f"http://archive.org/wayback/available?url={url}"

    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()

        if data.get('archived_snapshots', {}).get('closest'):
            snapshot = data['archived_snapshots']['closest']
            return {
                'available': snapshot.get('available', False),
                'url': snapshot.get('url'),
                'timestamp': snapshot.get('timestamp'),
                'status': snapshot.get('status')
            }
        return None
    except Exception as e:
        return None

def get_wayback_url(url: str, timestamp: str = None) -> str:
    """Generate Wayback Machine URL for a page.

    Args:
        url: Original URL to retrieve
        timestamp: Optional YYYYMMDDHHMMSS format, or None for latest
    """
    if timestamp:
        return f"https://web.archive.org/web/{timestamp}/{url}"
    return f"https://web.archive.org/web/{url}"
```

### Save page to Wayback Machine

```python
def save_to_wayback(url: str) -> Optional[str]:
    """Request Wayback Machine to archive a URL.

    Returns the archived URL if successful.
    """
    save_url = f"https://web.archive.org/save/{url}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (research-archiver)'
    }

    try:
        response = requests.get(save_url, headers=headers, timeout=60)

        # Check for successful archive
        if response.status_code == 200:
            # The archived URL is in the Content-Location header
            archived_url = response.headers.get('Content-Location')
            if archived_url:
                return f"https://web.archive.org{archived_url}"
            return response.url
        return None
    except Exception:
        return None
```

### CDX API for historical snapshots

```python
def get_all_snapshots(url: str, limit: int = 100) -> list[dict]:
    """Get all archived snapshots of a URL using CDX API.

    Returns list of snapshots with timestamps and status codes.
    """
    cdx_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        'url': url,
        'output': 'json',
        'limit': limit,
        'fl': 'timestamp,original,statuscode,digest,length'
    }

    try:
        response = requests.get(cdx_url, params=params, timeout=30)
        data = response.json()

        if len(data) < 2:  # First row is headers
            return []

        headers = data[0]
        snapshots = []

        for row in data[1:]:
            snapshot = dict(zip(headers, row))
            snapshot['wayback_url'] = (
                f"https://web.archive.org/web/{snapshot['timestamp']}/{snapshot['original']}"
            )
            snapshots.append(snapshot)

        return snapshots
    except Exception:
        return []
```

## Archive.today integration

### Save to Archive.today

```python
import requests
from urllib.parse import quote

def save_to_archive_today(url: str) -> Optional[str]:
    """Submit URL to Archive.today for archiving.

    Note: Archive.today has rate limiting and CAPTCHA requirements.
    This function works for basic archiving but may require
    manual intervention for high-volume use.
    """
    submit_url = "https://archive.today/submit/"

    data = {
        'url': url,
        'anyway': '1'  # Archive even if recent snapshot exists
    }

    try:
        response = requests.post(submit_url, data=data, timeout=60)
        # Archive.today returns the archived URL in the response
        if response.status_code == 200:
            return response.url
        return None
    except Exception:
        return None

def search_archive_today(url: str) -> Optional[str]:
    """Search for existing Archive.today snapshot."""
    search_url = f"https://archive.today/{quote(url, safe='')}"

    try:
        response = requests.get(search_url, timeout=30, allow_redirects=True)
        if response.status_code == 200 and 'archive.today' in response.url:
            return response.url
        return None
    except Exception:
        return None
```

## Multi-archive redundancy

### Archive cascade for maximum preservation

```python
from dataclasses import dataclass
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ArchiveResult:
    service: str
    url: str
    archived_url: Optional[str]
    success: bool
    error: Optional[str] = None

class MultiArchiver:
    """Archive URLs to multiple services for redundancy."""

    def __init__(self):
        self.services = [
            ('wayback', self._save_wayback),
            ('archive_today', self._save_archive_today),
            ('perma_cc', self._save_perma),  # Requires API key
        ]

    def archive_url(self, url: str, parallel: bool = True) -> List[ArchiveResult]:
        """Archive URL to all services.

        Args:
            url: URL to archive
            parallel: If True, archive to all services simultaneously
        """
        results = []

        if parallel:
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(save_func, url): name
                    for name, save_func in self.services
                }

                for future in as_completed(futures):
                    service = futures[future]
                    try:
                        archived_url = future.result()
                        results.append(ArchiveResult(
                            service=service,
                            url=url,
                            archived_url=archived_url,
                            success=archived_url is not None
                        ))
                    except Exception as e:
                        results.append(ArchiveResult(
                            service=service,
                            url=url,
                            archived_url=None,
                            success=False,
                            error=str(e)
                        ))
        else:
            for name, save_func in self.services:
                try:
                    archived_url = save_func(url)
                    results.append(ArchiveResult(
                        service=name,
                        url=url,
                        archived_url=archived_url,
                        success=archived_url is not None
                    ))
                except Exception as e:
                    results.append(ArchiveResult(
                        service=name,
                        url=url,
                        archived_url=None,
                        success=False,
                        error=str(e)
                    ))

        return results

    def _save_wayback(self, url: str) -> Optional[str]:
        return save_to_wayback(url)

    def _save_archive_today(self, url: str) -> Optional[str]:
        return save_to_archive_today(url)

    def _save_perma(self, url: str) -> Optional[str]:
        # Requires Perma.cc API key
        # Implementation depends on having API credentials
        return None
```

## Self-hosted archiving with ArchiveBox

### ArchiveBox setup

```bash
# Install ArchiveBox
pip install archivebox

# Or with Docker
docker pull archivebox/archivebox

# Initialize archive directory
mkdir ~/web-archives && cd ~/web-archives
archivebox init

# Add URLs to archive
archivebox add "https://example.com/article"

# Add multiple URLs from file
archivebox add --depth=0 < urls.txt

# Schedule regular archiving
archivebox schedule --every=day --depth=1 "https://example.com/feed.rss"
```

### ArchiveBox Python integration

```python
import subprocess
from pathlib import Path
from typing import List, Optional

class ArchiveBoxManager:
    """Manage local ArchiveBox instance."""

    def __init__(self, archive_dir: Path):
        self.archive_dir = archive_dir
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Initialize ArchiveBox if needed."""
        if not (self.archive_dir / 'index.sqlite3').exists():
            subprocess.run(
                ['archivebox', 'init'],
                cwd=self.archive_dir,
                check=True
            )

    def add_url(self, url: str, depth: int = 0) -> bool:
        """Archive a single URL.

        Args:
            url: URL to archive
            depth: 0 for single page, 1 to follow links one level deep
        """
        result = subprocess.run(
            ['archivebox', 'add', f'--depth={depth}', url],
            cwd=self.archive_dir,
            capture_output=True,
            text=True
        )
        return result.returncode == 0

    def add_urls_from_file(self, filepath: Path) -> bool:
        """Archive URLs from a text file (one per line)."""
        with open(filepath) as f:
            result = subprocess.run(
                ['archivebox', 'add', '--depth=0'],
                cwd=self.archive_dir,
                stdin=f,
                capture_output=True
            )
        return result.returncode == 0

    def search(self, query: str) -> List[dict]:
        """Search archived content."""
        result = subprocess.run(
            ['archivebox', 'list', '--filter-type=search', query],
            cwd=self.archive_dir,
            capture_output=True,
            text=True
        )
        # Parse output...
        return []
```

## Legal evidence preservation

### Chain of custody documentation

```python
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
import json

@dataclass
class EvidenceRecord:
    """Legally defensible evidence record."""

    # Content identification
    original_url: str
    archived_urls: List[str]  # Multiple archive copies
    content_hash_sha256: str

    # Timestamps
    capture_time_utc: str
    first_observed: str

    # Metadata
    page_title: str
    captured_by: str
    capture_method: str
    tool_versions: dict

    # Chain of custody
    custody_log: List[dict]  # Who accessed when

    def add_custody_entry(self, accessor: str, action: str, notes: str = ""):
        """Log access to evidence."""
        self.custody_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'accessor': accessor,
            'action': action,
            'notes': notes
        })

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_capture(cls, url: str, content: bytes, captured_by: str):
        """Create evidence record from captured content."""
        return cls(
            original_url=url,
            archived_urls=[],
            content_hash_sha256=hashlib.sha256(content).hexdigest(),
            capture_time_utc=datetime.utcnow().isoformat(),
            first_observed=datetime.utcnow().isoformat(),
            page_title="",
            captured_by=captured_by,
            capture_method="automated_capture",
            tool_versions={
                'archiver': '1.0.0',
                'python': '3.11'
            },
            custody_log=[]
        )

def capture_as_evidence(url: str, captured_by: str) -> EvidenceRecord:
    """Capture URL with full evidence chain documentation."""

    # Capture content
    response = requests.get(url)
    content = response.content

    # Create evidence record
    record = EvidenceRecord.from_capture(url, content, captured_by)
    record.page_title = extract_title(content)

    # Archive to multiple services
    archiver = MultiArchiver()
    results = archiver.archive_url(url)

    for result in results:
        if result.success:
            record.archived_urls.append(result.archived_url)

    # Log initial capture
    record.add_custody_entry(
        captured_by,
        'initial_capture',
        f'Captured from {url}, archived to {len(record.archived_urls)} services'
    )

    return record
```

### Perma.cc for legal citations

```python
import requests
from typing import Optional

class PermaCC:
    """Perma.cc API client for legal-grade archiving.

    Requires API key from perma.cc (free for limited use).
    Used by US courts and legal professionals.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perma.cc/v1"
        self.headers = {
            'Authorization': f'ApiKey {api_key}',
            'Content-Type': 'application/json'
        }

    def create_archive(self, url: str, folder_id: int = None) -> Optional[dict]:
        """Create a new Perma.cc archive.

        Returns dict with guid, creation_timestamp, and captures.
        """
        data = {'url': url}
        if folder_id:
            data['folder'] = folder_id

        try:
            response = requests.post(
                f"{self.base_url}/archives/",
                json=data,
                headers=self.headers,
                timeout=60
            )

            if response.status_code == 201:
                result = response.json()
                return {
                    'guid': result['guid'],
                    'url': f"https://perma.cc/{result['guid']}",
                    'creation_timestamp': result['creation_timestamp'],
                    'title': result.get('title', '')
                }
            return None
        except Exception:
            return None

    def get_archive(self, guid: str) -> Optional[dict]:
        """Retrieve archive metadata by GUID."""
        try:
            response = requests.get(
                f"{self.base_url}/archives/{guid}/",
                headers=self.headers,
                timeout=30
            )
            return response.json() if response.status_code == 200 else None
        except Exception:
            return None
```

## Browser extensions and bookmarklets

### Quick archive bookmarklet

```javascript
// Save to Wayback Machine - add as bookmark
javascript:(function(){
    var url = location.href;
    window.open('https://web.archive.org/save/' + url, '_blank');
})();

// Save to Archive.today
javascript:(function(){
    var url = location.href;
    window.open('https://archive.today/?run=1&url=' + encodeURIComponent(url), '_blank');
})();

// Check all archives (Memento)
javascript:(function(){
    var url = location.href;
    window.open('http://timetravel.mementoweb.org/list/0/' + url, '_blank');
})();
```

### Resurrect dead pages bookmarklet

```javascript
// Try multiple archives for dead pages
javascript:(function(){
    var url = location.href;
    var archives = [
        'https://web.archive.org/web/*/' + url,
        'https://archive.today/' + encodeURIComponent(url),
        'https://webcache.googleusercontent.com/search?q=cache:' + url,
        'http://timetravel.mementoweb.org/list/0/' + url
    ];
    archives.forEach(function(a){ window.open(a, '_blank'); });
})();
```

## Archive service comparison

| Service | Best For | API | Deletions | Max Size |
|---------|----------|-----|-----------|----------|
| **Wayback Machine** | Historical research | Yes (free) | On request | Unlimited |
| **Archive.today** | Paywall bypass, quick saves | No | Never | 50MB |
| **Perma.cc** | Legal citations | Yes (free tier) | By creator | Standard pages |
| **ArchiveBox** | Self-hosted, privacy | Local | Never | Disk space |
| **Conifer** | Interactive content | Yes | By creator | 5GB free |

## Error handling and fallbacks

```python
from enum import Enum
from typing import Optional

class ArchiveError(Enum):
    NOT_FOUND = "No archive found"
    RATE_LIMITED = "Rate limited by service"
    BLOCKED = "URL blocked from archiving"
    TIMEOUT = "Request timed out"
    SERVICE_DOWN = "Archive service unavailable"

def get_archived_page(url: str) -> tuple[Optional[str], Optional[ArchiveError]]:
    """Try all archive services with proper error handling."""

    # 1. Try Wayback Machine first
    try:
        result = check_wayback_availability(url)
        if result and result.get('available'):
            return result['url'], None
    except requests.Timeout:
        pass  # Try next service
    except Exception:
        pass

    # 2. Try Archive.today
    try:
        result = search_archive_today(url)
        if result:
            return result, None
    except Exception:
        pass

    # 3. Try Memento aggregator
    try:
        memento_url = f"http://timetravel.mementoweb.org/api/json/0/{url}"
        response = requests.get(memento_url, timeout=30)
        data = response.json()

        if data.get('mementos', {}).get('closest'):
            return data['mementos']['closest']['uri'][0], None
    except Exception:
        pass

    return None, ArchiveError.NOT_FOUND
```

## Best practices

### When to archive

- **Before publishing**: Archive all sources cited in your work
- **Breaking news**: Archive immediately, content may change or disappear
- **Legal matters**: Create timestamped evidence with multiple archives
- **Research**: Archive primary sources for reproducibility
- **Social media**: Archive posts before they can be deleted

### Archive redundancy

Always archive to at least two services:

```python
def ensure_archived(url: str) -> bool:
    """Ensure URL is archived in at least 2 services."""
    archiver = MultiArchiver()
    results = archiver.archive_url(url)

    successful = [r for r in results if r.success]
    return len(successful) >= 2
```

### Rate limiting and ethics

- Respect `robots.txt` for bulk archiving
- Add delays between requests (1-3 seconds minimum)
- Don't archive personal/private pages without consent
- Use API keys when available for better rate limits
- Cache results to avoid redundant requests
