#!/usr/bin/env python3
"""
GitHub Skills Crawler Entry Point
Crawls GitHub for SKILL.md files and saves to sources/crawled.json
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.github_crawler import GitHubSkillsCrawler


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Crawl GitHub for SKILL.md files')
    parser.add_argument('--token', help='GitHub API token (or set GITHUB_TOKEN env var)')
    parser.add_argument('--output', default='sources/crawled.json', help='Output file path')
    parser.add_argument('--max', type=int, default=50000, help='Maximum skills to crawl')
    parser.add_argument('--min-stars', type=int, default=0, help='Minimum stars filter')

    args = parser.parse_args()

    # Get token
    token = args.token or os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Warning: No GitHub token provided. Rate limits will be very strict.")
        print("Set GITHUB_TOKEN environment variable or use --token flag")

    # Run crawler
    crawler = GitHubSkillsCrawler(token=token)
    skills = crawler.crawl(max_skills=args.max)

    # Filter by stars if specified
    if args.min_stars > 0:
        skills = [s for s in skills if s.get('stars', 0) >= args.min_stars]

    crawler.skills = skills
    crawler.save(args.output)

    print(f"\nCrawl Summary:")
    print(f"  Total skills: {len(skills)}")

    # Category breakdown
    categories = {}
    for s in skills:
        cat = s.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print(f"  Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")


if __name__ == '__main__':
    main()
