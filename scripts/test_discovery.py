#!/usr/bin/env python3
"""
Test the discovery mechanism with a small sample
"""

import os

import requests


def test_topic_search():
    """Test searching repos by topic"""
    print("=== Testing GitHub Topics API ===")

    url = 'https://api.github.com/search/repositories'
    params = {
        'q': 'topic:claude-code-skills',
        'sort': 'stars',
        'per_page': 5,
    }

    headers = {'Accept': 'application/vnd.github.v3+json'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'token {token}'

    resp = requests.get(url, headers=headers, params=params, timeout=30)

    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Found {data['total_count']} repos with claude-code-skills topic")
        print("\nTop 5 repos:")
        for repo in data['items']:
            print(f"  - {repo['full_name']} ({repo['stargazers_count']} stars)")
        return True
    else:
        print(f"✗ Failed: {resp.status_code}")
        print(resp.text[:200])
        return False

def test_skill_download():
    """Test downloading a known SKILL.md"""
    print("\n=== Testing SKILL.md Download ===")

    # Test with anthropics/skills - we know this exists
    url = "https://raw.githubusercontent.com/anthropics/skills/main/skills/pdf/SKILL.md"

    resp = requests.get(url, timeout=15)

    if resp.status_code == 200:
        content = resp.text
        has_frontmatter = '---' in content[:100]
        has_name = 'name:' in content[:500]

        print(f"✓ Downloaded SKILL.md ({len(content)} bytes)")
        print(f"  Has frontmatter: {has_frontmatter}")
        print(f"  Has name field: {has_name}")

        # Show first few lines
        lines = content.split('\n')[:10]
        print("\n  Preview:")
        for line in lines:
            print(f"    {line}")

        return has_frontmatter and has_name
    else:
        print(f"✗ Failed: {resp.status_code}")
        return False

if __name__ == '__main__':
    print("Testing GitHub Skills Discovery\n")

    test1 = test_topic_search()
    test2 = test_skill_download()

    print("\n=== Results ===")
    print(f"Topic Search: {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"Skill Download: {'✓ PASS' if test2 else '✗ FAIL'}")

    if test1 and test2:
        print("\n✓ All tests passed! The discovery mechanism works.")
    else:
        print("\n✗ Some tests failed. Check the output above.")
