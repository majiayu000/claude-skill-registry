#!/usr/bin/env python3
"""
Update star counts and validate skills from GitHub.
"""

import json
import os
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError

REGISTRY_DIR = Path(__file__).parent.parent
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def get_repo_info(owner, repo):
    """Fetch repository info from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "skill-registry-updater",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read())
    except HTTPError as e:
        if e.code == 404:
            return None
        raise


def check_skill_exists(owner, repo, path):
    """Check if SKILL.md exists at the given path."""
    if path:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}/SKILL.md"
    else:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/SKILL.md"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "skill-registry-updater",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=10) as response:
            return True
    except HTTPError:
        return False


def update_registry():
    """Update the registry with latest GitHub data."""
    registry_file = REGISTRY_DIR / "registry.json"

    with open(registry_file) as f:
        registry = json.load(f)

    updated = 0
    removed = 0
    skills_to_keep = []

    print(f"Checking {len(registry['skills'])} skills...")

    for skill in registry["skills"]:
        repo = skill.get("repo", "")
        if not repo:
            skills_to_keep.append(skill)
            continue

        parts = repo.split("/")
        if len(parts) < 2:
            skills_to_keep.append(skill)
            continue

        owner, repo_name = parts[0], parts[1]
        path = skill.get("path", "")

        # Get repo info
        info = get_repo_info(owner, repo_name)
        if not info:
            print(f"  ✗ {skill['name']}: repo not found, removing")
            removed += 1
            continue

        # Check SKILL.md exists
        if not check_skill_exists(owner, repo_name, path):
            print(f"  ✗ {skill['name']}: SKILL.md not found, removing")
            removed += 1
            continue

        # Update stars
        old_stars = skill.get("stars", 0)
        new_stars = info.get("stargazers_count", 0)
        if new_stars != old_stars:
            skill["stars"] = new_stars
            updated += 1
            print(f"  ✓ {skill['name']}: {old_stars} → {new_stars} stars")

        # Update description if empty
        if not skill.get("description") and info.get("description"):
            skill["description"] = info["description"]

        skills_to_keep.append(skill)

    registry["skills"] = skills_to_keep
    registry["total_count"] = len(skills_to_keep)

    # Write updated registry
    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=2)

    print()
    print(f"Updated: {updated}, Removed: {removed}")


if __name__ == "__main__":
    update_registry()
