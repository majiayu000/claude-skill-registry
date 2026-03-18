#!/usr/bin/env python3
"""
Discover skill collections — cohesive products with skills + commands + hooks.

A collection is NOT "a repo with lots of SKILL.md files". It is a packaged
product where multiple skills, slash commands, and hooks work together to
serve a specific use case (e.g. PM workflow, frontend dev toolkit).

Discovery sources:
  1. npm search — find published packages with claude/skills keywords
  2. GitHub repo tree inspection — verify skills + commands + hooks structure

Required signals (must have ALL):
  - Multiple SKILL.md files (≥2)
  - npx-installable (package.json with bin)

Bonus signals (boost score):
  - Has /commands/ directory
  - Has /hooks/ directory
  - Cohesive description (not just "awesome list")
"""

import base64
import json
import logging
import subprocess
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

NPM_QUERIES = [
    "claude skills",
    "claude code skills",
    "claude commands hooks",
    "claude agent skills",
]


def load_existing_collections(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return {c.get("repo", "") for c in json.load(f).get("collections", [])}


def npm_search(query: str) -> list[dict]:
    """Search npm registry, return package metadata list."""
    try:
        r = subprocess.run(
            ["npm", "search", query, "--json", "--long"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0:
            return json.loads(r.stdout)
    except Exception as e:
        logger.warning("npm search failed for %r: %s", query, e)
    return []


def npm_view(pkg_name: str) -> Optional[dict]:
    """Get detailed npm package info."""
    try:
        r = subprocess.run(
            ["npm", "view", pkg_name, "--json"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            return json.loads(r.stdout)
    except Exception:
        pass
    return None


def extract_repo_slug(npm_info: dict) -> str:
    """Extract owner/repo from npm package repository field."""
    repo = npm_info.get("repository", {})
    url = repo.get("url", "") if isinstance(repo, dict) else str(repo)
    url = url.replace("git+", "").replace(".git", "").replace("git://", "https://")
    for prefix in ("https://github.com/", "http://github.com/"):
        if url.startswith(prefix):
            slug = url[len(prefix):].strip("/")
            parts = slug.split("/")
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
    return ""


def gh_api(endpoint: str, jq: str = "") -> Optional[str]:
    """Call GitHub API via gh CLI."""
    cmd = ["gh", "api", endpoint]
    if jq:
        cmd += ["--jq", jq]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return None


def inspect_repo_structure(repo: str) -> dict:
    """Check a GitHub repo for skills/commands/hooks structure."""
    result = {
        "skills": [],
        "commands": [],
        "hooks": [],
        "has_package_json": False,
        "description": "",
        "stars": 0,
        "default_branch": "main",
    }

    # Repo metadata
    meta_raw = gh_api(f"repos/{repo}", "{description: .description, stargazers_count: .stargazers_count, default_branch: .default_branch}")
    if not meta_raw:
        return result
    try:
        meta = json.loads(meta_raw)
        result["description"] = meta.get("description") or ""
        result["stars"] = meta.get("stargazers_count", 0)
        result["default_branch"] = meta.get("default_branch", "main")
    except json.JSONDecodeError:
        return result

    branch = result["default_branch"]

    # Recursive tree
    tree_raw = gh_api(
        f"repos/{repo}/git/trees/{branch}?recursive=true",
        "[.tree[].path] | .[]",
    )
    if not tree_raw:
        return result

    paths = tree_raw.split("\n")

    for p in paths:
        lower = p.lower()
        if lower.endswith("skill.md"):
            result["skills"].append(p)
        elif "/commands/" in p and lower.endswith(".md"):
            result["commands"].append(p)
        elif "/hooks/" in p and (lower.endswith(".sh") or lower.endswith(".json") or lower.endswith(".js")):
            result["hooks"].append(p)
        elif p == "package.json":
            result["has_package_json"] = True

    return result


def get_install_command(repo: str, branch: str) -> str:
    """Read package.json from repo to get npx install command."""
    content_b64 = gh_api(f"repos/{repo}/contents/package.json", ".content")
    if not content_b64:
        return ""
    try:
        content = base64.b64decode(content_b64).decode("utf-8")
        pkg = json.loads(content)
        name = pkg.get("name", "")
        has_bin = bool(pkg.get("bin"))
        if has_bin and name:
            return f"npx {name}@latest"
        return name
    except Exception:
        return ""


def score_candidate(repo: str, structure: dict, npm_name: str = "") -> dict:
    """Score a repo as a collection candidate. Strict criteria."""
    score = 0
    reasons = []

    skill_count = len(structure["skills"])
    cmd_count = len(structure["commands"])
    hook_count = len(structure["hooks"])
    stars = structure["stars"]

    # Hard requirement: must have ≥2 skills
    if skill_count < 2:
        return {"repo": repo, "score": 0, "reasons": ["too_few_skills"]}

    # Core signals: skills + commands + hooks
    if skill_count >= 10:
        score += 3
        reasons.append(f"skills={skill_count}")
    elif skill_count >= 5:
        score += 2
        reasons.append(f"skills={skill_count}")
    else:
        score += 1
        reasons.append(f"skills={skill_count}")

    if cmd_count > 0:
        score += 3
        reasons.append(f"commands={cmd_count}")

    if hook_count > 0:
        score += 3
        reasons.append(f"hooks={hook_count}")

    # Installable
    install = ""
    if npm_name:
        install = f"npx {npm_name}@latest" if npm_name else ""
        score += 2
        reasons.append(f"npm={npm_name}")
    elif structure["has_package_json"]:
        install = get_install_command(repo, structure["default_branch"])
        if install:
            score += 2
            reasons.append(f"install={install}")

    # Stars
    if stars >= 1000:
        score += 1
        reasons.append(f"stars={stars}")

    return {
        "repo": repo,
        "score": score,
        "reasons": reasons,
        "description": structure["description"],
        "stars": stars,
        "install": install,
        "skill_count": skill_count,
        "command_count": cmd_count,
        "hook_count": hook_count,
        "sample_skills": [p.split("/")[-2] if "/" in p else p for p in structure["skills"][:10]],
        "sample_commands": [p.split("/")[-1].replace(".md", "") for p in structure["commands"][:10]],
        "sample_hooks": [p.split("/")[-1] for p in structure["hooks"][:10]],
    }


def discover_from_npm(existing: set[str]) -> list[dict]:
    """Discover collection candidates from npm packages."""
    seen_repos: set[str] = set()
    candidates = []

    # Step 1: npm search
    all_packages: dict[str, dict] = {}
    for query in NPM_QUERIES:
        logger.info(f"npm search: {query}")
        for pkg in npm_search(query):
            name = pkg.get("name", "")
            if name and name not in all_packages:
                all_packages[name] = pkg

    logger.info(f"Found {len(all_packages)} unique npm packages")
    logger.info("")

    # Step 2: inspect each
    for pkg_name, pkg_meta in all_packages.items():
        # Get detailed info for repo URL
        info = npm_view(pkg_name)
        if not info:
            continue

        has_bin = bool(info.get("bin"))
        repo_slug = extract_repo_slug(info)

        if not repo_slug:
            continue
        if repo_slug in seen_repos or repo_slug in existing:
            continue
        seen_repos.add(repo_slug)

        # Only check repos with bin (npx installable)
        if not has_bin:
            continue

        logger.info(f"Inspecting {repo_slug} ({pkg_name})...")
        structure = inspect_repo_structure(repo_slug)

        candidate = score_candidate(repo_slug, structure, npm_name=pkg_name)
        if candidate["score"] >= 4:
            candidates.append(candidate)
            logger.info(f"  ✓ score={candidate['score']} skills={candidate['skill_count']} "
                        f"cmds={candidate['command_count']} hooks={candidate['hook_count']}")
        else:
            logger.info(f"  ✗ score={candidate['score']} (skipped)")

    return candidates


def discover_from_registry(registry_path: Path, existing: set[str], checked_repos: set[str]) -> list[dict]:
    """Scan registry for repos that might be collections (have many skills)."""
    if not registry_path.exists():
        return []

    with open(registry_path, "r", encoding="utf-8") as f:
        skills = json.load(f).get("skills", [])

    # Group by repo, find those with ≥10 skills (higher bar for registry scan)
    from collections import Counter
    repo_counts = Counter(s.get("repo", "") for s in skills if s.get("repo"))

    candidates = []
    repos_to_check = [
        repo for repo, count in repo_counts.most_common()
        if count >= 10 and repo not in existing and repo not in checked_repos
        and "claude-skill-registry" not in repo
    ]

    # Only check top 30 to avoid API rate limits
    repos_to_check = repos_to_check[:30]
    logger.info(f"Registry scan: checking {len(repos_to_check)} repos with 10+ skills")

    for repo in repos_to_check:
        logger.info(f"Inspecting {repo}...")
        structure = inspect_repo_structure(repo)
        candidate = score_candidate(repo, structure)
        if candidate["score"] >= 4:
            candidates.append(candidate)
            logger.info(f"  ✓ score={candidate['score']} skills={candidate['skill_count']} "
                        f"cmds={candidate['command_count']} hooks={candidate['hook_count']}")
        else:
            logger.info(f"  ✗ score={candidate['score']} (skipped)")

    return candidates


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Discover skill collections (skills + commands + hooks products)",
    )
    parser.add_argument("--collections", default="sources/collections.json")
    parser.add_argument("--registry", default="registry.json", help="Scan registry for candidates too")
    parser.add_argument("--output", "-o", help="Output JSON for candidates")
    parser.add_argument("--npm-only", action="store_true", help="Only search npm, skip registry scan")

    args = parser.parse_args()
    existing = load_existing_collections(Path(args.collections))
    logger.info(f"Existing collections: {len(existing)}")
    logger.info("")

    # Phase 1: npm discovery
    logger.info("=" * 60)
    logger.info("Phase 1: npm package discovery")
    logger.info("=" * 60)
    npm_candidates = discover_from_npm(existing)
    npm_repos = {c["repo"] for c in npm_candidates}

    # Phase 2: registry scan
    registry_candidates = []
    if not args.npm_only:
        logger.info("")
        logger.info("=" * 60)
        logger.info("Phase 2: registry repo scan")
        logger.info("=" * 60)
        registry_candidates = discover_from_registry(
            Path(args.registry), existing, npm_repos,
        )

    # Merge and sort
    all_candidates = npm_candidates + registry_candidates
    all_candidates.sort(key=lambda x: (-x["score"], -x["stars"]))

    # Display
    logger.info("")
    logger.info("=" * 60)
    logger.info("RESULTS")
    logger.info("=" * 60)
    logger.info(f"Total candidates: {len(all_candidates)}")
    logger.info("")

    if not all_candidates:
        logger.info("No collection candidates found.")
        return

    for c in all_candidates:
        has_3piece = c["command_count"] > 0 and c["hook_count"] > 0
        marker = "★" if has_3piece else "○"
        logger.info(f"{marker} [{c['score']:>2d}] {c['repo']}")
        logger.info(f"       {c['description'][:80]}")
        logger.info(f"       skills={c['skill_count']}  commands={c['command_count']}  hooks={c['hook_count']}  stars={c['stars']}")
        if c.get("install"):
            logger.info(f"       install: {c['install']}")
        logger.info(f"       skills: {c['sample_skills'][:6]}")
        if c["sample_commands"]:
            logger.info(f"       commands: {c['sample_commands'][:6]}")
        if c["sample_hooks"]:
            logger.info(f"       hooks: {c['sample_hooks'][:6]}")
        logger.info("")

    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_candidates, f, indent=2, ensure_ascii=False)
        logger.info(f"Written {len(all_candidates)} candidates to {output_path}")


if __name__ == "__main__":
    main()
