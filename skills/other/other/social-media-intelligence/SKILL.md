---
name: social-media-intelligence
description: Social media monitoring, narrative tracking, and open-source intelligence for journalists. Use when tracking viral content spread, analyzing coordinated campaigns, monitoring breaking news on social platforms, investigating accounts for authenticity, or detecting misinformation patterns. Essential for reporters covering online narratives and digital investigations.
---

# Social media intelligence

Systematic approaches for monitoring, analyzing, and investigating social media for journalism.

## When to activate

- Tracking how a story spreads across platforms
- Investigating potential coordinated inauthentic behavior
- Monitoring breaking news across social platforms
- Analyzing account networks and relationships
- Detecting bot activity or manipulation campaigns
- Building evidence trails for digital investigations
- Archiving social content before deletion

## Real-time monitoring

### Multi-platform tracker

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import hashlib

class Platform(Enum):
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    REDDIT = "reddit"
    THREADS = "threads"
    BLUESKY = "bluesky"
    MASTODON = "mastodon"

@dataclass
class SocialPost:
    platform: Platform
    post_id: str
    author: str
    content: str
    timestamp: datetime
    url: str
    engagement: Dict[str, int] = field(default_factory=dict)
    media_urls: List[str] = field(default_factory=list)
    archived_urls: List[str] = field(default_factory=list)
    content_hash: str = ""

    def __post_init__(self):
        # Hash content for duplicate detection
        self.content_hash = hashlib.md5(
            f"{self.platform.value}:{self.content}".encode()
        ).hexdigest()

@dataclass
class MonitoringQuery:
    keywords: List[str]
    platforms: List[Platform]
    accounts: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    exclude_terms: List[str] = field(default_factory=list)
    start_date: Optional[datetime] = None

    def to_search_string(self, platform: Platform) -> str:
        """Generate platform-specific search query."""
        parts = []

        # Keywords
        if self.keywords:
            parts.append(' OR '.join(f'"{k}"' for k in self.keywords))

        # Hashtags
        if self.hashtags:
            parts.append(' OR '.join(f'#{h}' for h in self.hashtags))

        # Exclusions
        if self.exclude_terms:
            parts.append(' '.join(f'-{t}' for t in self.exclude_terms))

        return ' '.join(parts)
```

### Breaking news monitor

```python
from collections import defaultdict
from datetime import datetime, timedelta

class BreakingNewsDetector:
    """Detect sudden spikes in keyword mentions."""

    def __init__(self, baseline_window_hours: int = 24):
        self.baseline_window = timedelta(hours=baseline_window_hours)
        self.mention_history = defaultdict(list)

    def add_mention(self, keyword: str, timestamp: datetime):
        """Record a mention of a keyword."""
        self.mention_history[keyword].append(timestamp)
        # Prune old data
        cutoff = datetime.now() - self.baseline_window * 2
        self.mention_history[keyword] = [
            t for t in self.mention_history[keyword] if t > cutoff
        ]

    def is_spiking(self, keyword: str, threshold_multiplier: float = 3.0) -> bool:
        """Check if keyword is spiking above baseline."""
        now = datetime.now()
        recent = sum(1 for t in self.mention_history[keyword]
                    if t > now - timedelta(hours=1))

        baseline_hourly = len([
            t for t in self.mention_history[keyword]
            if t > now - self.baseline_window
        ]) / self.baseline_window.total_seconds() * 3600

        if baseline_hourly == 0:
            return recent > 10  # Arbitrary threshold for new topics

        return recent > baseline_hourly * threshold_multiplier

    def get_trending(self, top_n: int = 10) -> List[tuple]:
        """Get keywords sorted by spike intensity."""
        spikes = []
        for keyword in self.mention_history:
            if self.is_spiking(keyword):
                recent = sum(1 for t in self.mention_history[keyword]
                           if t > datetime.now() - timedelta(hours=1))
                spikes.append((keyword, recent))

        return sorted(spikes, key=lambda x: x[1], reverse=True)[:top_n]
```

## Account analysis

### Authenticity indicators

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class AccountAnalysis:
    username: str
    platform: Platform
    created_date: Optional[datetime] = None
    follower_count: int = 0
    following_count: int = 0
    post_count: int = 0

    # Authenticity signals
    profile_photo_is_stock: Optional[bool] = None
    bio_contains_keywords: List[str] = field(default_factory=list)
    posts_primarily_reshares: Optional[bool] = None
    posting_pattern_irregular: Optional[bool] = None
    engagement_ratio_suspicious: Optional[bool] = None

    def calculate_red_flags(self) -> dict:
        """Score account authenticity."""
        flags = {}

        # Account age
        if self.created_date:
            age_days = (datetime.now() - self.created_date).days
            if age_days < 30:
                flags['new_account'] = f"Created {age_days} days ago"

        # Follower ratio
        if self.following_count > 0:
            ratio = self.follower_count / self.following_count
            if ratio < 0.1:
                flags['low_follower_ratio'] = f"Ratio: {ratio:.2f}"

        # Posting frequency
        if self.created_date and self.post_count > 0:
            age_days = max(1, (datetime.now() - self.created_date).days)
            posts_per_day = self.post_count / age_days
            if posts_per_day > 50:
                flags['excessive_posting'] = f"{posts_per_day:.0f} posts/day"

        # Stock photo check
        if self.profile_photo_is_stock:
            flags['stock_profile_photo'] = "Profile appears to be stock image"

        return flags

    def authenticity_score(self) -> int:
        """0-100 score, higher = more likely authentic."""
        score = 100
        flags = self.calculate_red_flags()

        penalty_per_flag = 20
        score -= len(flags) * penalty_per_flag

        return max(0, score)
```

### Network mapping

```python
from collections import defaultdict
from typing import Set, Dict

class AccountNetwork:
    """Map relationships between accounts."""

    def __init__(self):
        self.interactions = defaultdict(lambda: defaultdict(int))
        self.accounts = {}

    def add_interaction(self, from_account: str, to_account: str,
                       interaction_type: str = "mention"):
        """Record an interaction between accounts."""
        self.interactions[from_account][to_account] += 1

    def find_clusters(self, min_interactions: int = 3) -> List[Set[str]]:
        """Find groups of accounts that frequently interact."""
        # Build adjacency with minimum threshold
        adjacency = defaultdict(set)
        for from_acc, targets in self.interactions.items():
            for to_acc, count in targets.items():
                if count >= min_interactions:
                    adjacency[from_acc].add(to_acc)
                    adjacency[to_acc].add(from_acc)

        # Find connected components
        visited = set()
        clusters = []

        for account in adjacency:
            if account in visited:
                continue

            cluster = set()
            stack = [account]

            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                cluster.add(current)
                stack.extend(adjacency[current] - visited)

            if len(cluster) > 1:
                clusters.append(cluster)

        return sorted(clusters, key=len, reverse=True)

    def coordination_score(self, accounts: Set[str]) -> float:
        """Score how coordinated a group of accounts appears."""
        if len(accounts) < 2:
            return 0.0

        total_possible = len(accounts) * (len(accounts) - 1)
        actual_connections = 0

        for acc in accounts:
            for other in accounts:
                if acc != other and self.interactions[acc][other] > 0:
                    actual_connections += 1

        return actual_connections / total_possible if total_possible > 0 else 0
```

## Narrative tracking

### Claim propagation tracker

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class Claim:
    text: str
    first_seen: datetime
    first_seen_url: str
    variations: List[str] = field(default_factory=list)
    appearances: List[Dict] = field(default_factory=list)

    def add_appearance(self, url: str, platform: Platform,
                       timestamp: datetime, author: str):
        """Track where this claim has appeared."""
        self.appearances.append({
            'url': url,
            'platform': platform.value,
            'timestamp': timestamp,
            'author': author
        })

    def spread_timeline(self) -> List[Dict]:
        """Get chronological spread of the claim."""
        return sorted(self.appearances, key=lambda x: x['timestamp'])

    def platforms_reached(self) -> Dict[str, int]:
        """Count appearances by platform."""
        counts = defaultdict(int)
        for app in self.appearances:
            counts[app['platform']] += 1
        return dict(counts)

    def velocity(self, window_hours: int = 24) -> float:
        """Calculate spread rate in appearances per hour."""
        if not self.appearances:
            return 0.0

        recent = [
            a for a in self.appearances
            if a['timestamp'] > datetime.now() - timedelta(hours=window_hours)
        ]
        return len(recent) / window_hours
```

### Hashtag analysis

```python
from collections import Counter
from datetime import datetime, timedelta

class HashtagAnalyzer:
    """Analyze hashtag usage patterns."""

    def __init__(self):
        self.hashtag_posts = defaultdict(list)

    def add_post(self, hashtags: List[str], post: SocialPost):
        """Record a post's hashtags."""
        for tag in hashtags:
            self.hashtag_posts[tag.lower()].append(post)

    def co_occurrence(self, hashtag: str, top_n: int = 10) -> List[tuple]:
        """Find hashtags that commonly appear with this one."""
        co_tags = Counter()

        for post in self.hashtag_posts.get(hashtag.lower(), []):
            # Extract hashtags from post content
            tags = [
                word.lower() for word in post.content.split()
                if word.startswith('#')
            ]
            for tag in tags:
                if tag != f'#{hashtag.lower()}':
                    co_tags[tag] += 1

        return co_tags.most_common(top_n)

    def posting_pattern(self, hashtag: str) -> Dict:
        """Analyze when posts with this hashtag appear."""
        posts = self.hashtag_posts.get(hashtag.lower(), [])

        hour_counts = Counter(p.timestamp.hour for p in posts)
        day_counts = Counter(p.timestamp.strftime('%A') for p in posts)

        return {
            'by_hour': dict(hour_counts),
            'by_day': dict(day_counts),
            'total_posts': len(posts),
            'unique_authors': len(set(p.author for p in posts))
        }
```

## Evidence preservation

### Archive before it disappears

```python
import requests
from datetime import datetime
from typing import Optional

class SocialArchiver:
    """Archive social content before deletion."""

    def __init__(self):
        self.archived = {}

    def archive_to_wayback(self, url: str) -> Optional[str]:
        """Submit URL to Internet Archive."""
        try:
            save_url = f"https://web.archive.org/save/{url}"
            response = requests.get(save_url, timeout=30)

            if response.status_code == 200:
                archived_url = response.url
                self.archived[url] = {
                    'wayback': archived_url,
                    'archived_at': datetime.now().isoformat()
                }
                return archived_url
        except Exception as e:
            print(f"Archive failed: {e}")
        return None

    def archive_to_archive_today(self, url: str) -> Optional[str]:
        """Submit URL to archive.today."""
        try:
            response = requests.post(
                'https://archive.today/submit/',
                data={'url': url},
                timeout=60
            )
            if response.status_code == 200:
                return response.url
        except Exception as e:
            print(f"Archive.today failed: {e}")
        return None

    def full_archive(self, url: str) -> dict:
        """Archive to multiple services for redundancy."""
        results = {
            'original_url': url,
            'archived_at': datetime.now().isoformat(),
            'archives': {}
        }

        wayback = self.archive_to_wayback(url)
        if wayback:
            results['archives']['wayback'] = wayback

        archive_today = self.archive_to_archive_today(url)
        if archive_today:
            results['archives']['archive_today'] = archive_today

        return results
```

## Coordination detection

### Behavioral signals checklist

```markdown
## Coordinated inauthentic behavior indicators

### Timing patterns
- [ ] Multiple accounts posting same content within minutes
- [ ] Synchronized posting times across accounts
- [ ] Burst activity followed by dormancy
- [ ] Posts appear faster than human typing speed

### Content patterns
- [ ] Identical or near-identical text across accounts
- [ ] Same images/media shared by multiple accounts
- [ ] Identical typos or formatting errors
- [ ] Copy-paste artifacts visible

### Account patterns
- [ ] Accounts created around same time
- [ ] Similar naming conventions (name + numbers)
- [ ] Generic or stock profile photos
- [ ] Minimal personal content, mostly shares
- [ ] Follow the same accounts
- [ ] Engage with each other disproportionately

### Network patterns
- [ ] Form dense clusters in network analysis
- [ ] Amplify same external sources
- [ ] Target same accounts or hashtags
- [ ] Cross-platform coordination visible
```

### Automated coordination scoring

```python
def coordination_likelihood(posts: List[SocialPost]) -> dict:
    """Score how likely posts represent coordinated activity."""

    if len(posts) < 2:
        return {'score': 0, 'signals': []}

    signals = []
    score = 0

    # Check for identical content
    contents = [p.content for p in posts]
    unique_contents = set(contents)
    if len(unique_contents) < len(contents) * 0.5:
        signals.append("High content duplication")
        score += 30

    # Check timing clusters
    timestamps = sorted(p.timestamp for p in posts)
    rapid_posts = 0
    for i in range(1, len(timestamps)):
        if (timestamps[i] - timestamps[i-1]).seconds < 60:
            rapid_posts += 1

    if rapid_posts > len(posts) * 0.3:
        signals.append("Suspicious timing clusters")
        score += 25

    # Check unique authors
    authors = set(p.author for p in posts)
    if len(authors) > 5 and len(contents) / len(authors) > 2:
        signals.append("Few authors, many similar posts")
        score += 20

    return {
        'score': min(100, score),
        'signals': signals,
        'posts_analyzed': len(posts),
        'unique_authors': len(authors)
    }
```

## Platform-specific tools

| Platform | Monitoring Tool | Notes |
|----------|-----------------|-------|
| Twitter/X | TweetDeck, Brandwatch | API increasingly restricted |
| Facebook | CrowdTangle (limited) | Academic access only now |
| Instagram | Later, Brandwatch | No public API for search |
| TikTok | Exolyt, Pentos | Limited historical data |
| Reddit | Pushshift, Arctic Shift | Archive access varies |
| YouTube | YouTube Data API | Good metadata access |
| Bluesky | Firehose API | Open, real-time access |

## Ethical guidelines

- Archive public content only
- Don't create fake accounts for monitoring
- Respect platform terms of service
- Protect sources who share social content
- Verify before publishing claims about coordination
- Consider context before amplifying harmful content

## Related skills

- **source-verification** - Verify accounts and claims found on social
- **web-scraping** - Programmatic collection of public content
- **data-journalism** - Analyze social data for patterns

---

## Skill metadata

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Created | 2025-12-26 |
| Author | Claude Skills for Journalism |
| Domain | Journalism, OSINT |
| Complexity | Advanced |
