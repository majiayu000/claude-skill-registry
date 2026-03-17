---
name: scraping-reddit
description: Scrapes top posts from specified subreddits using the Reddit JSON API. Use when the user needs to fetch post titles and links from Reddit without authentication.
---

# Reddit Scraping Skill

## When to use this skill
- When the user wants to list top posts from a specific subreddit (e.g., "Get top posts from r/n8n").
- When the user needs a quick, unauthenticated way to check Reddit content.
- When expanding this functionality to other scraping tasks.

## Workflow
1.  **Verify Dependencies**: Ensure `requests` is installed or create a virtual environment.
2.  **Execute Scraper**: Run the provided python script, passing the subreddit name as an argument.
3.  **Process Output**: The script prints to stdout; output can be piped or captured.

## Instructions

### 1. Setup Environment
To avoid system package conflicts, prefer running this in a virtual environment if one doesn't exist.

```bash
cd .agent/skills/scraping-reddit/scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Scraper
The script accepts one optional argument: the subreddit name.

**Syntax:**
```bash
python3 scraper.py [subreddit_name]
```

**Examples:**
```bash
# Default (r/n8n)
python3 scraper.py

# Custom subreddit (r/python)
python3 scraper.py python
```

### 3. Modifying the Logic
If you need to change the limit (default 3) or extraction logic, edit `scripts/scraper.py`.

## Resources
- [Scraper Script](scripts/scraper.py)
- [Requirements](scripts/requirements.txt)
