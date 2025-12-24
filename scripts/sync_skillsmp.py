#!/usr/bin/env python3
"""
Sync skills from SkillsMP.com
SkillsMP has already crawled 32,000+ skills from GitHub
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.skillsmp_sync import SkillsMPSync


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Sync skills from SkillsMP.com')
    parser.add_argument('--output', default='sources/skillsmp.json', help='Output file path')
    parser.add_argument('--max', type=int, default=50000, help='Maximum skills to sync')
    parser.add_argument('--min-stars', type=int, default=0, help='Minimum stars filter')

    args = parser.parse_args()

    syncer = SkillsMPSync()
    skills = syncer.sync(max_skills=args.max, min_stars=args.min_stars)
    syncer.save(args.output)

    print(f"\nSync Summary:")
    print(f"  Total skills: {len(skills)}")

    # Category breakdown
    categories = {}
    for s in skills:
        cat = s.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print(f"  Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")

    # Top repos by skill count
    repos = {}
    for s in skills:
        repo = s.get('repo', 'unknown')
        repos[repo] = repos.get(repo, 0) + 1

    print(f"\n  Top repos by skill count:")
    for repo, count in sorted(repos.items(), key=lambda x: -x[1])[:10]:
        print(f"    {repo}: {count} skills")


if __name__ == '__main__':
    main()
