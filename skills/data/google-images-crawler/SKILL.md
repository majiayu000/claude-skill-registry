---
name: google-images-crawler
description: Crawl high-resolution original images from Google Images search. Use when user needs to (1) Search and download images from Google, (2) Get original/full-size images instead of thumbnails, (3) Batch download images by keyword, (4) Extract image URLs from Google Images search results. Supports specifying number of images, filtering by size, and downloading to local storage.
---

# Google Images Crawler

Crawl original (non-thumbnail) images from Google Images search results.

## Key Difference: Original vs Thumbnail

- **Thumbnail URLs** (low quality, avoid): `https://encrypted-tbn0.gstatic.com/images?q=tbn:...`
- **Original URLs** (high quality, target): External domain links like `https://example.com/photo.jpg`

This skill extracts the original high-resolution images, not the low-quality thumbnails.

## Quick Start

### 1. Search and Get Image URLs

```python
python3 scripts/crawl_google_images.py "search keyword" --count 10
```

### 2. Download Images

```python
python3 scripts/download_images.py urls.txt --output ./images
```

## Methods for Extracting Original Images

### Method 1: From href links (Recommended)

Google Images wraps original URLs in `imgurl` parameter:

```python
import re
# Extract from a[href*="imgurl="] links
match = re.search(r'imgurl=([^&]+)', href)
original_url = match.group(1)
```

### Method 2: From page scripts

Parse JSON embedded in page HTML containing image metadata.

### Method 3: From rg_meta divs (Legacy)

```python
# Google sometimes embeds metadata in div.rg_meta
data = json.loads(div.text_content)
original_url = data['ou']  # original URL
```

## Core Script

Use `scripts/crawl_google_images.py`:

```python
from playwright.sync_api import sync_playwright
import re

def crawl_google_images(keyword, count=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to Google Images
        page.goto(f"https://www.google.com/search?q={keyword}&tbm=isch")
        page.wait_for_timeout(3000)
        
        # Method 1: Extract from imgurl parameter
        links = page.eval_on_selector_all('a[href*="imgurl="]', 
            'els => els.map(e => e.href)')
        
        original_urls = []
        for link in links:
            match = re.search(r'imgurl=([^&]+)', link)
            if match:
                url = match.group(1)
                # URL decode
                url = url.replace('%3A', ':').replace('%2F', '/')
                if 'gstatic' not in url and 'google' not in url:
                    original_urls.append(url)
        
        browser.close()
        return original_urls[:count]
```

## Download Script

```python
import requests

def download_image(url, output_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(r.content)
        return len(r.content)
    return 0
```

## Common Issues

1. **Connection reset**: Some sites block scrapers, use retry with different headers
2. **Low resolution thumbnails**: Always filter URLs containing `gstatic` or `google`
3. **Rate limiting**: Add delays between requests

## References

- `references/advanced_filtering.md` - Size, type, and color filtering options
- `references/api_alternative.md` - Using Google Custom Search API as alternative
