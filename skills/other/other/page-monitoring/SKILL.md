---
name: page-monitoring
description: Web page monitoring, change detection, and availability tracking. Use when tracking content changes, detecting when pages go down, monitoring for updates, preserving content before deletion, or generating feeds for pages without RSS. Covers Visualping, ChangeTower, Distill.io, and self-hosted monitoring solutions.
---

# Page monitoring methodology

Patterns for tracking web page changes, detecting content removal, and preserving important pages before they disappear.

## Monitoring service comparison

| Service | Free Tier | Best For | Storage | Alert Speed |
|---------|-----------|----------|---------|-------------|
| **Visualping** | 5 pages | Visual changes | Standard | Minutes |
| **ChangeTower** | Yes | Compliance, archiving | 12 years | Minutes |
| **Distill.io** | 25 pages | Element-level tracking | 12 months | Seconds |
| **Wachete** | Limited | Login-protected pages | 12 months | Minutes |
| **UptimeRobot** | 50 monitors | Uptime only | 2 months | Minutes |

## Quick-start: Monitor a page

### Distill.io element monitoring

```javascript
// Distill.io allows CSS/XPath selectors for precise monitoring
// Example selectors for common use cases:

// Monitor news article headlines
const newsSelector = '.article-headline, h1.title, .story-title';

// Monitor price changes
const priceSelector = '.price, .product-price, [data-price]';

// Monitor stock/availability
const availabilitySelector = '.in-stock, .availability, .stock-status';

// Monitor specific paragraph or section
const sectionSelector = '#main-content p:first-child';

// Monitor table data
const tableSelector = 'table.data-table tbody tr';
```

### Python monitoring script

```python
import requests
import hashlib
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup

class PageMonitor:
    """Simple page change monitor with local storage."""

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = storage_dir / 'monitor_state.json'
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {'pages': {}}

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def _get_page_hash(self, url: str, selector: str = None) -> tuple[str, str]:
        """Get content hash and content for a page or element."""

        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (PageMonitor/1.0)'
        })
        response.raise_for_status()

        if selector:
            soup = BeautifulSoup(response.text, 'html.parser')
            element = soup.select_one(selector)
            content = element.get_text(strip=True) if element else ''
        else:
            content = response.text

        content_hash = hashlib.sha256(content.encode()).hexdigest()
        return content_hash, content

    def add_page(self, url: str, name: str, selector: str = None):
        """Add a page to monitor."""

        content_hash, content = self._get_page_hash(url, selector)

        self.state['pages'][url] = {
            'name': name,
            'selector': selector,
            'last_hash': content_hash,
            'last_check': datetime.now().isoformat(),
            'last_content': content[:1000],  # Store preview
            'change_count': 0
        }

        self._save_state()
        print(f"Added: {name} ({url})")

    def check_page(self, url: str) -> Optional[dict]:
        """Check single page for changes."""

        if url not in self.state['pages']:
            return None

        page = self.state['pages'][url]
        selector = page.get('selector')

        try:
            new_hash, new_content = self._get_page_hash(url, selector)
        except Exception as e:
            return {
                'url': url,
                'name': page['name'],
                'status': 'error',
                'error': str(e)
            }

        changed = new_hash != page['last_hash']

        result = {
            'url': url,
            'name': page['name'],
            'status': 'changed' if changed else 'unchanged',
            'previous_content': page['last_content'],
            'new_content': new_content[:1000] if changed else None
        }

        if changed:
            page['last_hash'] = new_hash
            page['last_content'] = new_content[:1000]
            page['change_count'] += 1

            # Archive the change
            archive_file = self.storage_dir / f"{hashlib.md5(url.encode()).hexdigest()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            archive_file.write_text(new_content)

        page['last_check'] = datetime.now().isoformat()
        self._save_state()

        return result

    def check_all(self) -> list[dict]:
        """Check all monitored pages."""
        results = []
        for url in self.state['pages']:
            result = self.check_page(url)
            if result:
                results.append(result)
        return results

# Usage
monitor = PageMonitor(Path('./page_monitor_data'))

# Add pages to monitor
monitor.add_page(
    'https://example.com/important-page',
    'Important Page',
    selector='.main-content'  # Optional: monitor specific element
)

# Check for changes
results = monitor.check_all()
for result in results:
    if result['status'] == 'changed':
        print(f"CHANGED: {result['name']}")
        print(f"  Previous: {result['previous_content'][:100]}...")
        print(f"  New: {result['new_content'][:100]}...")
```

## Uptime monitoring

### UptimeRobot API integration

```python
import requests
from typing import List, Optional

class UptimeRobotClient:
    """UptimeRobot API client for monitoring page availability."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.uptimerobot.com/v2"

    def _request(self, endpoint: str, params: dict = None) -> dict:
        data = {'api_key': self.api_key}
        if params:
            data.update(params)

        response = requests.post(f"{self.base_url}/{endpoint}", data=data)
        return response.json()

    def get_monitors(self) -> List[dict]:
        """Get all monitors."""
        result = self._request('getMonitors')
        return result.get('monitors', [])

    def create_monitor(self, friendly_name: str, url: str,
                       monitor_type: int = 1) -> dict:
        """Create a new monitor.

        Types: 1=HTTP(s), 2=Keyword, 3=Ping, 4=Port
        """
        return self._request('newMonitor', {
            'friendly_name': friendly_name,
            'url': url,
            'type': monitor_type
        })

    def get_monitor_uptime(self, monitor_id: int,
                           custom_uptime_ratios: str = "7-30-90") -> dict:
        """Get uptime statistics for a monitor."""
        return self._request('getMonitors', {
            'monitors': monitor_id,
            'custom_uptime_ratios': custom_uptime_ratios
        })

    def pause_monitor(self, monitor_id: int) -> dict:
        """Pause a monitor."""
        return self._request('editMonitor', {
            'id': monitor_id,
            'status': 0
        })

    def resume_monitor(self, monitor_id: int) -> dict:
        """Resume a monitor."""
        return self._request('editMonitor', {
            'id': monitor_id,
            'status': 1
        })

# Usage
client = UptimeRobotClient('your-api-key')

# Create monitors for important pages
client.create_monitor('News Homepage', 'https://example-news.com')
client.create_monitor('API Status', 'https://api.example.com/health')

# Check all monitors
for monitor in client.get_monitors():
    status = 'UP' if monitor['status'] == 2 else 'DOWN'
    print(f"{monitor['friendly_name']}: {status}")
```

## RSS feed generation

### Generate RSS from pages without feeds

```python
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import hashlib

class RSSGenerator:
    """Generate RSS feeds from web pages."""

    def __init__(self, feed_id: str, title: str, link: str):
        self.fg = FeedGenerator()
        self.fg.id(feed_id)
        self.fg.title(title)
        self.fg.link(href=link)
        self.fg.description(f'Auto-generated feed for {title}')

    def add_from_page(self, url: str, item_selector: str,
                      title_selector: str, link_selector: str,
                      description_selector: str = None):
        """Parse a page and add items to feed.

        Args:
            url: Page URL to parse
            item_selector: CSS selector for each item container
            title_selector: CSS selector for title (relative to item)
            link_selector: CSS selector for link (relative to item)
            description_selector: Optional CSS selector for description
        """

        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select(item_selector)

        for item in items[:20]:  # Limit to 20 items
            title_elem = item.select_one(title_selector)
            link_elem = item.select_one(link_selector)

            if not title_elem or not link_elem:
                continue

            title = title_elem.get_text(strip=True)
            link = link_elem.get('href', '')

            # Make absolute URL if relative
            if link.startswith('/'):
                from urllib.parse import urljoin
                link = urljoin(url, link)

            fe = self.fg.add_entry()
            fe.id(hashlib.md5(link.encode()).hexdigest())
            fe.title(title)
            fe.link(href=link)

            if description_selector:
                desc_elem = item.select_one(description_selector)
                if desc_elem:
                    fe.description(desc_elem.get_text(strip=True))

            fe.published(datetime.now())

    def generate_rss(self) -> str:
        """Generate RSS XML string."""
        return self.fg.rss_str(pretty=True).decode()

    def save_rss(self, filepath: str):
        """Save RSS feed to file."""
        self.fg.rss_file(filepath)

# Example: Generate feed for a news site without RSS
rss = RSSGenerator(
    'https://example.com/news',
    'Example News Feed',
    'https://example.com/news'
)

rss.add_from_page(
    'https://example.com/news',
    item_selector='.news-item',
    title_selector='h2 a',
    link_selector='h2 a',
    description_selector='.summary'
)

# Save the feed
rss.save_rss('example_feed.xml')
```

### Using RSS-Bridge (self-hosted)

```bash
# RSS-Bridge generates feeds for sites without them
# Supports Twitter, Instagram, YouTube, and many others

# Docker installation
docker pull rssbridge/rss-bridge
docker run -d -p 3000:80 rssbridge/rss-bridge

# Access at http://localhost:3000
# Select a bridge, enter parameters, get RSS feed URL
```

## Social media monitoring

### Twitter/X archiving with Twarc

```python
# Twarc requires Twitter API credentials

# Installation
# pip install twarc

# Configure
# twarc2 configure

import subprocess
import json
from pathlib import Path

class TwitterArchiver:
    """Archive Twitter searches and timelines."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def search(self, query: str, max_results: int = 100) -> Path:
        """Search tweets and save to file."""

        output_file = self.output_dir / f"search_{query.replace(' ', '_')}.jsonl"

        subprocess.run([
            'twarc2', 'search',
            '--max-results', str(max_results),
            query,
            str(output_file)
        ], check=True)

        return output_file

    def get_timeline(self, username: str, max_results: int = 100) -> Path:
        """Get user timeline."""

        output_file = self.output_dir / f"timeline_{username}.jsonl"

        subprocess.run([
            'twarc2', 'timeline',
            '--max-results', str(max_results),
            username,
            str(output_file)
        ], check=True)

        return output_file

    def parse_archive(self, filepath: Path) -> list[dict]:
        """Parse archived tweets."""

        tweets = []
        with open(filepath) as f:
            for line in f:
                data = json.loads(line)
                if 'data' in data:
                    tweets.extend(data['data'])

        return tweets
```

## Webhook notifications

### Send alerts on changes

```python
import requests
from typing import Optional

class AlertManager:
    """Send alerts when monitored pages change."""

    def __init__(self, slack_webhook: str = None,
                 discord_webhook: str = None,
                 email_config: dict = None):
        self.slack_webhook = slack_webhook
        self.discord_webhook = discord_webhook
        self.email_config = email_config

    def send_slack(self, message: str, channel: str = None):
        """Send Slack notification."""
        if not self.slack_webhook:
            return

        payload = {'text': message}
        if channel:
            payload['channel'] = channel

        requests.post(self.slack_webhook, json=payload)

    def send_discord(self, message: str):
        """Send Discord notification."""
        if not self.discord_webhook:
            return

        requests.post(self.discord_webhook, json={'content': message})

    def send_email(self, subject: str, body: str, to: str):
        """Send email notification."""
        if not self.email_config:
            return

        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_config['from']
        msg['To'] = to

        with smtplib.SMTP(self.email_config['smtp_host'],
                         self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['username'],
                        self.email_config['password'])
            server.send_message(msg)

    def alert_change(self, page_name: str, url: str,
                     old_content: str, new_content: str):
        """Send change alert to all configured channels."""

        message = f"""
Page Changed: {page_name}
URL: {url}
Time: {datetime.now().isoformat()}

Previous content (preview):
{old_content[:200]}...

New content (preview):
{new_content[:200]}...
"""

        if self.slack_webhook:
            self.send_slack(message)

        if self.discord_webhook:
            self.send_discord(message)
```

## Scheduled monitoring with cron

### Cron setup for continuous monitoring

```bash
# Edit crontab
crontab -e

# Check pages every 15 minutes
*/15 * * * * /usr/bin/python3 /path/to/monitor_script.py >> /var/log/monitor.log 2>&1

# Check critical pages every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/critical_monitor.py >> /var/log/critical.log 2>&1

# Daily summary report at 8 AM
0 8 * * * /usr/bin/python3 /path/to/daily_report.py
```

### Monitoring script template

```python
#!/usr/bin/env python3
"""Page monitoring script for cron execution."""

import sys
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from monitor import PageMonitor
from alerts import AlertManager

def main():
    # Initialize
    monitor = PageMonitor(Path('./data'))
    alerts = AlertManager(
        slack_webhook='https://hooks.slack.com/services/...',
        discord_webhook='https://discord.com/api/webhooks/...'
    )

    # Check all pages
    results = monitor.check_all()

    # Process results
    changes = [r for r in results if r['status'] == 'changed']
    errors = [r for r in results if r['status'] == 'error']

    # Alert on changes
    for change in changes:
        alerts.alert_change(
            change['name'],
            change['url'],
            change['previous_content'],
            change['new_content']
        )
        print(f"[{datetime.now()}] CHANGE: {change['name']}")

    # Alert on errors
    for error in errors:
        alerts.send_slack(f"Monitor error for {error['name']}: {error['error']}")
        print(f"[{datetime.now()}] ERROR: {error['name']} - {error['error']}")

    # Summary
    print(f"[{datetime.now()}] Checked {len(results)} pages, "
          f"{len(changes)} changes, {len(errors)} errors")

if __name__ == '__main__':
    main()
```

## Archive on change

### Automatic archiving when changes detected

```python
from multiarchiver import MultiArchiver

class ArchivingMonitor(PageMonitor):
    """Page monitor that archives content when changes detected."""

    def __init__(self, storage_dir: Path):
        super().__init__(storage_dir)
        self.archiver = MultiArchiver()

    def check_page(self, url: str) -> dict:
        """Check page and archive if changed."""

        result = super().check_page(url)

        if result and result['status'] == 'changed':
            # Archive to multiple services
            archive_results = self.archiver.archive_url(url)

            successful_archives = [
                r.archived_url for r in archive_results
                if r.success
            ]

            result['archives'] = successful_archives

            # Log archive URLs
            print(f"Archived {url} to:")
            for archive_url in successful_archives:
                print(f"  - {archive_url}")

        return result
```

## Monitoring strategy by use case

### News monitoring

```markdown
## News/Current Events Monitoring

### Pages to monitor:
- Breaking news sections
- Press release pages
- Government announcement pages
- Company newsrooms

### Monitoring frequency:
- Breaking news: Every 5 minutes
- Press releases: Every 15-30 minutes
- General news: Every hour

### Archive strategy:
- Archive immediately on detection
- Use both Wayback Machine and Archive.today
- Save local copy with timestamp
```

### Research monitoring

```markdown
## Academic/Research Monitoring

### Pages to monitor:
- Preprint servers (arXiv, SSRN)
- Journal table of contents
- Conference proceedings
- Researcher profiles

### Monitoring frequency:
- Daily for active topics
- Weekly for general monitoring

### Tools recommended:
- Google Scholar alerts (free, built-in)
- Semantic Scholar alerts
- RSS feeds where available
- Custom monitors for specific pages
```

### Competitive intelligence

```markdown
## Competitor Monitoring

### Pages to monitor:
- Pricing pages
- Product pages
- Job postings
- Press releases
- Executive bios

### Monitoring frequency:
- Pricing: Daily
- Products: Daily
- Jobs: Weekly
- Press: Daily

### Legal considerations:
- Don't violate terms of service
- Don't circumvent access controls
- Public pages only
- Don't scrape at high frequency
```

## Best practices

### Monitoring checklist

```markdown
## Before monitoring a page:

- [ ] Is the page publicly accessible?
- [ ] Are you respecting robots.txt?
- [ ] Is monitoring frequency reasonable?
- [ ] Do you have a legitimate purpose?
- [ ] Are you storing data securely?
- [ ] Do you have alerts configured?
- [ ] Is archiving set up for important pages?

## Maintenance:

- [ ] Review monitors monthly
- [ ] Remove stale monitors
- [ ] Update selectors if pages change
- [ ] Check alert delivery
- [ ] Verify archives are working
```

### Rate limiting

```python
import time
from functools import wraps

def rate_limit(min_interval: float = 1.0):
    """Decorator to rate limit function calls."""
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@rate_limit(min_interval=2.0)  # Max once per 2 seconds
def check_page(url: str):
    return requests.get(url)
```
