---
name: web-scraping
description: Web scraping with anti-bot bypass, content extraction, undocumented APIs and poison pill detection. Use when extracting content from websites, handling paywalls, implementing scraping cascades or processing social media. Covers requests, trafilatura, Playwright with stealth mode, yt-dlp and instaloader patterns.
---

# Web scraping methodology

Patterns for reliable, ethical web scraping with fallback strategies and anti-bot handling.

## Scraping cascade architecture

Implement multiple extraction strategies with automatic fallback:

```python
from abc import ABC, abstractmethod
from typing import Optional
import requests
from bs4 import BeautifulSoup
import trafilatura

#for .py files
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

#for .ipynb files
import asyncio
from playwright.async_api import async_playwright

class ScrapingResult:
    def __init__(self, content: str, title: str, method: str):
        self.content = content
        self.title = title
        self.method = method  # Track which method succeeded

class Scraper(ABC):
    @abstractmethod
    def fetch(self, url: str) -> Optional[ScrapingResult]: ...

class TrafilaturaСscraper(Scraper):
    """Fast, lightweight extraction for standard articles."""

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None

            content = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=True,
                favor_recall=True
            )

            if not content or len(content) < 100:
                return None

            # Extract title separately
            soup = BeautifulSoup(downloaded, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text() if title else ''

            return ScrapingResult(content, title_text, 'trafilatura')
        except Exception:
            return None

class RequestsScraper(Scraper):
    """HTTP requests with rotating user agents."""

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ]

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        import random

        headers = {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script/style elements
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()

            # Find main content
            main = soup.find('main') or soup.find('article') or soup.find('body')
            content = main.get_text(separator='\n', strip=True) if main else ''

            title = soup.find('title')
            title_text = title.get_text() if title else ''

            if len(content) < 100:
                return None

            return ScrapingResult(content, title_text, 'requests')
        except Exception:
            return None

class PlaywrightScraper(Scraper):
    """Heavy JavaScript rendering with stealth mode for anti-bot bypass."""

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()

                # Apply stealth to avoid detection
                stealth_sync(page)

                page.goto(url, wait_until='networkidle', timeout=60000)

                # Wait for content to load
                page.wait_for_timeout(2000)

                # Extract content
                content = page.evaluate('''() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }''')

                title = page.title()

                browser.close()

                if len(content) < 100:
                    return None

                return ScrapingResult(content, title, 'playwright')
        except Exception:
            return None

class PlaywrightScraperAsync:
    """Async Playwright scraper for Jupyter notebooks (.ipynb files).
    
    Jupyter notebooks run their own event loop, so sync Playwright won't work.
    Use this async version with `await` in notebook cells.
    """

    async def fetch(self, url: str) -> Optional[ScrapingResult]:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()

                # Note: playwright-stealth async version
                # from playwright_stealth import stealth_async
                # await stealth_async(page)

                await page.goto(url, wait_until='networkidle', timeout=60000)

                # Wait for content to load
                await page.wait_for_timeout(2000)

                # Extract content
                content = await page.evaluate('''() => {
                    const article = document.querySelector('article, main, .content, #content');
                    return article ? article.innerText : document.body.innerText;
                }''')

                title = await page.title()

                await browser.close()

                if len(content) < 100:
                    return None

                return ScrapingResult(content, title, 'playwright_async')
        except Exception:
            return None

# Usage in Jupyter notebook cells:
# scraper = PlaywrightScraperAsync()
# result = await scraper.fetch('https://example.com')

class ScrapingCascade:
    """Try multiple scrapers in order until one succeeds."""

    def __init__(self):
        self.scrapers = [
            TrafilaturaСscraper(),
            RequestsScraper(),
            PlaywrightScraper(),
        ]

    def fetch(self, url: str) -> Optional[ScrapingResult]:
        for scraper in self.scrapers:
            result = scraper.fetch(url)
            if result:
                return result
        return None
```

## Undocumented APIs

### Finding undocumented APIs

Use browser developer tools to discover APIs:

1. **Open developer tools** (right-click → Inspect, or F12)
2. **Go to the Network tab** to monitor all requests
3. **Filter by Fetch/XHR** to show only API calls
4. **Trigger the action** you want to capture (search, scroll, click)
5. **Analyze the response** — usually JSON with key-value pairs
6. **Copy as cURL** (right-click the request)
7. **Convert to code** using [curlconverter.com](https://curlconverter.com/)

### Stripping down API requests

When you copy a cURL from dev tools, it includes many parameters. Strip it down by:

1. **Remove unnecessary cookies** — test without them first
2. **Keep authentication tokens** if required
3. **Identify the input parameters** you can modify (like `prefix` for search terms)
4. **Test parameter values** — some expire, so periodically verify

### Example: Reverse-engineering an autocomplete API

```python
import requests
import time

def search_suggestions(keyword: str) -> dict:
    """
    Get autocompleted search suggestions from an undocumented API.
    Stripped down from browser dev tools capture.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    params = {
        'prefix': keyword,
        'suggestion-type': ['WIDGET', 'KEYWORD'],
        'alias': 'aps',
        'plain-mid': '1',
    }

    response = requests.get(
        'https://completion.amazon.com/api/2017/suggestions',
        params=params,
        headers=headers
    )
    return response.json()

# Collect suggestions for multiple keywords
keywords = ['a', 'b', 'cookie', 'sock']
data = []

for keyword in keywords:
    suggestions = search_suggestions(keyword)
    suggestions['search_word'] = keyword  # track seed keyword
    time.sleep(1)  # rate limit yourself
    data.extend(suggestions.get('suggestions', []))
```
*Source: [Leon Yin, "Finding Undocumented APIs," Inspect Element](https://inspectelement.org/apis.html), 2023*

## Poison pill detection

Detect paywalls, anti-bot pages, and other failures:

```python
from dataclasses import dataclass
from enum import Enum
import re

class PoisonPillType(Enum):
    PAYWALL = 'paywall'
    CAPTCHA = 'captcha'
    RATE_LIMIT = 'rate_limit'
    CLOUDFLARE = 'cloudflare'
    LOGIN_REQUIRED = 'login_required'
    NOT_FOUND = 'not_found'
    NONE = 'none'

@dataclass
class PoisonPillResult:
    detected: bool
    type: PoisonPillType
    confidence: float
    details: str

class PoisonPillDetector:
    PATTERNS = {
        PoisonPillType.PAYWALL: [
            r'subscribe to continue',
            r'subscription required',
            r'become a member',
            r'sign up to read',
            r'you\'ve reached your limit',
            r'article limit reached',
        ],
        PoisonPillType.CAPTCHA: [
            r'verify you are human',
            r'captcha',
            r'robot verification',
            r'prove you\'re not a robot',
        ],
        PoisonPillType.RATE_LIMIT: [
            r'too many requests',
            r'rate limit exceeded',
            r'slow down',
            r'429',
        ],
        PoisonPillType.CLOUDFLARE: [
            r'checking your browser',
            r'cloudflare',
            r'ddos protection',
            r'please wait while we verify',
        ],
        PoisonPillType.LOGIN_REQUIRED: [
            r'sign in to continue',
            r'log in required',
            r'create an account',
        ],
    }

    PAYWALL_DOMAINS = {
        'nytimes.com': PoisonPillType.PAYWALL,
        'wsj.com': PoisonPillType.PAYWALL,
        'washingtonpost.com': PoisonPillType.PAYWALL,
        'ft.com': PoisonPillType.PAYWALL,
        'bloomberg.com': PoisonPillType.PAYWALL,
    }

    def detect(self, url: str, content: str, status_code: int = 200) -> PoisonPillResult:
        # Check status code
        if status_code == 429:
            return PoisonPillResult(True, PoisonPillType.RATE_LIMIT, 1.0, 'HTTP 429')
        if status_code == 403:
            return PoisonPillResult(True, PoisonPillType.CLOUDFLARE, 0.8, 'HTTP 403')
        if status_code == 404:
            return PoisonPillResult(True, PoisonPillType.NOT_FOUND, 1.0, 'HTTP 404')

        # Check known paywall domains
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace('www.', '')
        for paywall_domain, pill_type in self.PAYWALL_DOMAINS.items():
            if paywall_domain in domain:
                # Check if content is suspiciously short (paywall truncation)
                if len(content) < 500:
                    return PoisonPillResult(True, pill_type, 0.9, f'Short content from {domain}')

        # Pattern matching
        content_lower = content.lower()
        for pill_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    return PoisonPillResult(True, pill_type, 0.7, f'Pattern match: {pattern}')

        return PoisonPillResult(False, PoisonPillType.NONE, 0.0, '')
```

## Social media scraping

### YouTube with yt-dlp

```python
import yt_dlp
from pathlib import Path

def download_video_metadata(url: str) -> dict:
    """Extract metadata without downloading video."""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title'),
            'description': info.get('description'),
            'duration': info.get('duration'),
            'upload_date': info.get('upload_date'),
            'view_count': info.get('view_count'),
            'channel': info.get('channel'),
            'thumbnail': info.get('thumbnail'),
        }

def download_video(url: str, output_dir: Path, audio_only: bool = False) -> Path:
    """Download video or audio."""
    output_template = str(output_dir / '%(title)s.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
    }

    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if audio_only:
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return Path(filename)

def get_transcript(url: str) -> list[dict]:
    """Extract auto-generated or manual subtitles."""
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Check for subtitles
        subtitles = info.get('subtitles', {})
        auto_captions = info.get('automatic_captions', {})

        # Prefer manual subtitles over auto-generated
        subs = subtitles.get('en') or auto_captions.get('en')
        if not subs:
            return []

        # Get the vtt or json format
        for sub in subs:
            if sub['ext'] in ['vtt', 'json3']:
                # Download and parse subtitle file
                # ... implementation depends on format
                pass

        return []
```

### Instagram with instaloader

```python
import instaloader
from pathlib import Path

class InstagramScraper:
    def __init__(self, username: str = None, session_file: str = None):
        self.loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
        )

        if session_file and Path(session_file).exists():
            self.loader.load_session_from_file(username, session_file)

    def get_profile_posts(self, username: str, limit: int = 50) -> list[dict]:
        """Get recent posts from a profile."""
        profile = instaloader.Profile.from_username(self.loader.context, username)
        posts = []

        for i, post in enumerate(profile.get_posts()):
            if i >= limit:
                break

            posts.append({
                'shortcode': post.shortcode,
                'url': f'https://instagram.com/p/{post.shortcode}/',
                'caption': post.caption,
                'timestamp': post.date_utc.isoformat(),
                'likes': post.likes,
                'comments': post.comments,
                'is_video': post.is_video,
                'video_url': post.video_url if post.is_video else None,
            })

        return posts

    def download_post(self, shortcode: str, output_dir: Path):
        """Download a single post's media."""
        post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
        self.loader.download_post(post, target=str(output_dir))
```

### TikTok with yt-dlp

```python
def scrape_tiktok_profile(username: str, output_dir: Path, limit: int = 50) -> list[dict]:
    """Scrape TikTok profile videos."""
    profile_url = f'https://tiktok.com/@{username}'

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download, just get info
        'playlistend': limit,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(profile_url, download=False)
        videos = []

        for entry in info.get('entries', []):
            videos.append({
                'id': entry.get('id'),
                'title': entry.get('title'),
                'url': entry.get('url'),
                'timestamp': entry.get('timestamp'),
                'view_count': entry.get('view_count'),
            })

        return videos

def download_tiktok_video(url: str, output_dir: Path) -> Path:
    """Download a single TikTok video."""
    ydl_opts = {
        'outtmpl': str(output_dir / '%(id)s.%(ext)s'),
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return Path(ydl.prepare_filename(info))
```

## Request patterns

### Rotating user agents and headers

```python
import random
from fake_useragent import UserAgent

class RequestManager:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()

    def get_headers(self) -> dict:
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def fetch(self, url: str, retry_count: int = 3) -> requests.Response:
        for attempt in range(retry_count):
            try:
                response = self.session.get(
                    url,
                    headers=self.get_headers(),
                    timeout=30
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == retry_count - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
```

### Respectful scraping with delays

```python
import time
import random
from urllib.parse import urlparse

class PoliteRequester:
    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_per_domain = {}

    def wait_for_domain(self, url: str):
        domain = urlparse(url).netloc
        last_request = self.last_request_per_domain.get(domain, 0)

        elapsed = time.time() - last_request
        delay = random.uniform(self.min_delay, self.max_delay)

        if elapsed < delay:
            time.sleep(delay - elapsed)

        self.last_request_per_domain[domain] = time.time()
```

## Ethical considerations

- Always check `robots.txt` before scraping
- Respect rate limits and add delays between requests
- Don't scrape personal data without consent
- Cache responses to avoid redundant requests
- Identify yourself with a descriptive User-Agent when appropriate
- Stop if you receive explicit blocking signals
