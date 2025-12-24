"""
GitHub Skills Crawler
Crawls GitHub for SKILL.md files and aggregates them into a registry
"""

import os
import json
import time
import logging
import requests
from datetime import datetime, timedelta
from typing import Optional, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import (
    GITHUB_API_BASE,
    GITHUB_RAW_BASE,
    SEARCH_QUERIES,
    REQUEST_DELAY,
    MIN_STARS,
    MIN_RECENT_DAYS,
)
from .skill_parser import SkillParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubSkillsCrawler:
    """Crawl GitHub for SKILL.md files"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.session = requests.Session()
        self.parser = SkillParser()

        if self.token:
            self.session.headers['Authorization'] = f'token {self.token}'
            self.session.headers['Accept'] = 'application/vnd.github.v3+json'
            logger.info("Using authenticated GitHub API")
        else:
            logger.warning("No GitHub token provided, rate limits will be strict")

        # Track seen repos to avoid duplicates
        self.seen_repos = set()
        self.skills = []

    def _request(self, url: str, params: dict = None) -> Optional[dict]:
        """Make a rate-limited request to GitHub API"""
        try:
            time.sleep(REQUEST_DELAY)
            response = self.session.get(url, params=params, timeout=30)

            # Handle rate limiting
            if response.status_code == 403:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                if reset_time:
                    wait_time = reset_time - time.time() + 1
                    if wait_time > 0 and wait_time < 3600:
                        logger.warning(f"Rate limited, waiting {wait_time:.0f}s")
                        time.sleep(wait_time)
                        return self._request(url, params)
                logger.error("Rate limited, no reset time available")
                return None

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def _get_raw_content(self, repo: str, path: str, branch: str = 'main') -> Optional[str]:
        """Get raw file content from GitHub"""
        # Try main, then master
        for b in [branch, 'main', 'master']:
            url = f"{GITHUB_RAW_BASE}/{repo}/{b}/{path}"
            try:
                time.sleep(0.5)
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    return response.text
            except requests.RequestException:
                continue
        return None

    def search_code(self, query: str, page: int = 1) -> Generator[dict, None, None]:
        """Search GitHub code for SKILL.md files"""
        url = f"{GITHUB_API_BASE}/search/code"
        params = {
            'q': query,
            'per_page': 100,
            'page': page,
        }

        result = self._request(url, params)
        if not result:
            return

        for item in result.get('items', []):
            yield {
                'repo': item['repository']['full_name'],
                'path': item['path'],
                'html_url': item['html_url'],
                'repo_url': item['repository']['html_url'],
            }

        # Check if there are more pages
        total_count = result.get('total_count', 0)
        if page * 100 < total_count and page < 10:  # GitHub limits to 1000 results
            yield from self.search_code(query, page + 1)

    def get_repo_info(self, repo: str) -> Optional[dict]:
        """Get repository metadata"""
        url = f"{GITHUB_API_BASE}/repos/{repo}"
        return self._request(url)

    def process_skill(self, item: dict) -> Optional[dict]:
        """Process a single SKILL.md file"""
        repo = item['repo']
        path = item['path']

        # Skip if we've seen this repo+path combo
        key = f"{repo}/{path}"
        if key in self.seen_repos:
            return None
        self.seen_repos.add(key)

        # Get SKILL.md content
        content = self._get_raw_content(repo, path)
        if not content:
            logger.debug(f"Could not fetch content for {key}")
            return None

        # Get repo info for stars and metadata
        repo_info = self.get_repo_info(repo)
        if not repo_info:
            return None

        # Apply filters
        stars = repo_info.get('stargazers_count', 0)
        if stars < MIN_STARS:
            return None

        # Check if recently updated
        updated_at = repo_info.get('pushed_at')
        if updated_at:
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            cutoff = datetime.now(updated_date.tzinfo) - timedelta(days=MIN_RECENT_DAYS)
            if updated_date < cutoff:
                logger.debug(f"Skipping stale repo {repo}")
                return None

        # Parse SKILL.md
        try:
            skill = self.parser.parse(content, repo, path)
            skill['stars'] = stars
            skill['updated_at'] = updated_at
            skill['html_url'] = item['html_url']

            # Mark as featured if high stars
            if stars >= 50:
                skill['featured'] = True

            logger.info(f"Found skill: {skill['name']} from {repo} ({stars} stars)")
            return skill

        except Exception as e:
            logger.error(f"Error parsing {key}: {e}")
            return None

    def crawl(self, max_skills: int = 50000) -> list:
        """Crawl GitHub for skills"""
        logger.info("Starting GitHub skills crawl...")

        all_items = []

        # Search using multiple queries
        for query in SEARCH_QUERIES:
            logger.info(f"Searching: {query}")
            for item in self.search_code(query):
                if item['repo'] not in [i['repo'] for i in all_items if i['path'] == item['path']]:
                    all_items.append(item)

                if len(all_items) >= max_skills:
                    break

            if len(all_items) >= max_skills:
                break

        logger.info(f"Found {len(all_items)} potential skills to process")

        # Process skills (can parallelize with care for rate limits)
        for item in all_items:
            skill = self.process_skill(item)
            if skill:
                self.skills.append(skill)

            if len(self.skills) >= max_skills:
                break

        # Sort by stars
        self.skills.sort(key=lambda x: x.get('stars', 0), reverse=True)

        logger.info(f"Crawl complete: {len(self.skills)} skills found")
        return self.skills

    def save(self, output_path: str):
        """Save crawled skills to JSON file"""
        output = {
            'name': 'GitHub Crawled Skills',
            'description': 'Skills automatically crawled from GitHub SKILL.md files',
            'crawled_at': datetime.utcnow().isoformat() + 'Z',
            'total_count': len(self.skills),
            'skills': self.skills,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(self.skills)} skills to {output_path}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Crawl GitHub for SKILL.md files')
    parser.add_argument('--token', help='GitHub API token')
    parser.add_argument('--output', default='sources/crawled.json', help='Output file path')
    parser.add_argument('--max', type=int, default=50000, help='Maximum skills to crawl')

    args = parser.parse_args()

    crawler = GitHubSkillsCrawler(token=args.token)
    crawler.crawl(max_skills=args.max)
    crawler.save(args.output)


if __name__ == '__main__':
    main()
