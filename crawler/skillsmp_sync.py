"""
SkillsMP.com Sync
Sync skills from SkillsMP.com API which has already crawled 32,000+ skills
"""

import json
import time
import logging
import requests
from typing import Optional
from datetime import datetime

from .config import CATEGORY_KEYWORDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SKILLSMP_API = "https://skillsmp.com/api/skills"


class SkillsMPSync:
    """Sync skills from SkillsMP.com"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Claude-Skills-Registry/1.0'
        # Disable SSL verification for older Python versions with LibreSSL
        self.session.verify = False
        self.skills = []

        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _request(self, page: int = 1, limit: int = 100, retries: int = 3) -> Optional[dict]:
        """Make request to SkillsMP API with retry logic"""
        for attempt in range(retries):
            try:
                params = {
                    'page': page,
                    'limit': limit,
                    'sortBy': 'stars',  # Sort by stars to get best first
                }
                response = self.session.get(SKILLSMP_API, params=params, timeout=30)

                # Handle rate limiting
                if response.status_code == 429:
                    wait_time = 30 * (attempt + 1)  # Exponential backoff
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))

        return None

    def _detect_category(self, skill: dict) -> str:
        """Detect category from skill data"""
        name = skill.get('name', '').lower()
        description = skill.get('description', '').lower()
        text = f"{name} {description}"

        scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)
        return "development"

    def _transform_skill(self, skill: dict) -> dict:
        """Transform SkillsMP skill to our format"""
        # Get repo path
        github_url = skill.get('githubUrl', '')
        repo = ''
        if 'github.com/' in github_url:
            # Extract owner/repo from URL
            parts = github_url.replace('https://github.com/', '').split('/')
            if len(parts) >= 2:
                repo = f"{parts[0]}/{parts[1]}"

        # Get skill path
        path = skill.get('path', '')
        if path and path.endswith('/SKILL.md'):
            path = path.replace('/SKILL.md', '')
        elif path == 'SKILL.md':
            path = ''

        # Detect category
        category = self._detect_category(skill)

        # Extract tags from name
        name = skill.get('name', 'unknown')
        tags = [t for t in name.lower().replace('_', '-').split('-') if len(t) > 2][:5]

        return {
            'name': name,
            'repo': repo,
            'path': path,
            'description': skill.get('description', f"Skill from {repo}")[:200],
            'category': category,
            'tags': tags,
            'stars': skill.get('stars', 0),
            'featured': skill.get('stars', 0) >= 50,
        }

    def sync(self, max_skills: int = 50000, min_stars: int = 0) -> list:
        """Sync skills from SkillsMP"""
        logger.info("Starting SkillsMP sync...")

        page = 1
        total_pages = 1

        while page <= total_pages and len(self.skills) < max_skills:
            logger.info(f"Fetching page {page}/{total_pages}...")

            result = self._request(page=page, limit=100)
            if not result:
                break

            pagination = result.get('pagination', {})
            total_pages = pagination.get('totalPages', 1)
            total_count = pagination.get('total', 0)

            logger.info(f"Total available: {total_count} skills")

            for skill in result.get('skills', []):
                # Filter by stars
                if skill.get('stars', 0) < min_stars:
                    continue

                transformed = self._transform_skill(skill)
                if transformed['repo']:  # Only add if we have a valid repo
                    self.skills.append(transformed)

                if len(self.skills) >= max_skills:
                    break

            page += 1
            time.sleep(1.5)  # Be nice to their API - rate limit is strict

        # Remove duplicates by name
        seen = set()
        unique_skills = []
        for skill in self.skills:
            key = f"{skill['repo']}/{skill['path']}/{skill['name']}"
            if key not in seen:
                seen.add(key)
                unique_skills.append(skill)

        self.skills = unique_skills

        # Sort by stars
        self.skills.sort(key=lambda x: x.get('stars', 0), reverse=True)

        logger.info(f"Sync complete: {len(self.skills)} skills")
        return self.skills

    def save(self, output_path: str):
        """Save synced skills to JSON file"""
        output = {
            'name': 'SkillsMP Synced Skills',
            'description': 'Skills synced from SkillsMP.com - aggregated from GitHub',
            'synced_at': datetime.utcnow().isoformat() + 'Z',
            'total_count': len(self.skills),
            'skills': self.skills,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(self.skills)} skills to {output_path}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Sync skills from SkillsMP.com')
    parser.add_argument('--output', default='sources/skillsmp.json', help='Output file path')
    parser.add_argument('--max', type=int, default=50000, help='Maximum skills to sync')
    parser.add_argument('--min-stars', type=int, default=0, help='Minimum stars filter')

    args = parser.parse_args()

    syncer = SkillsMPSync()
    syncer.sync(max_skills=args.max, min_stars=args.min_stars)
    syncer.save(args.output)


if __name__ == '__main__':
    main()
