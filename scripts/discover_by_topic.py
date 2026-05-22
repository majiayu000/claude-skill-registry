#!/usr/bin/env python3
"""
Discover skills by GitHub Topics
Uses GitHub Search API to find repositories with claude-code-skills or claude-skills topics
"""

import os
import json
import time
import logging
import shutil
import tempfile
from collections import defaultdict
import requests
from datetime import datetime
from pathlib import Path

from security_blocklist import blocked_metadata_source, load_security_blocklist
from security_scanner import SecurityScanner
from utils import normalize_name, ensure_unique_dir, build_skill_key, build_legal_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
GITHUB_RAW = "https://raw.githubusercontent.com"

# Topics to search for
SKILL_TOPICS = [
    "claude-code-skills",
    "claude-skills",
    "agent-skills",
    "codex-skills",
]

# Search queries for finding SKILL.md files
CODE_SEARCH_QUERIES = [
    "filename:SKILL.md",
    "filename:SKILL.md path:.claude/skills",
    "filename:SKILL.md path:skills",
]


class GitHubTopicDiscovery:
    """Discover skills using GitHub Topics and Code Search"""

    def __init__(
        self,
        token=None,
        max_repos=0,
        max_topic_pages=10,
        max_code_pages=10,
        skip_code_search=False,
        request_delay=2.0,
    ):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/vnd.github.v3+json'
        if self.token:
            self.session.headers['Authorization'] = f'token {self.token}'
            logger.info("Using authenticated GitHub API")
        else:
            logger.warning("No token - rate limits will be strict (10 req/min)")

        self.max_repos = max(0, int(max_repos or 0))
        self.max_topic_pages = max(1, int(max_topic_pages or 1))
        self.max_code_pages = max(1, int(max_code_pages or 1))
        self.skip_code_search = bool(skip_code_search)
        self.request_delay = max(0.0, float(request_delay or 0.0))

        self.discovered_repos = set()
        self.skills = []
        self.security_blocklist = load_security_blocklist()
        self.security_scanner = SecurityScanner()
        self.repo_candidates = {}
        self.path_candidates = {}
        self.topic_stats = defaultdict(
            lambda: {"repo_hits": 0, "repo_selected": 0, "downloaded_skills": 0}
        )
        self.code_query_stats = defaultdict(
            lambda: {"repo_hits": 0, "path_hits": 0, "downloaded_skills": 0}
        )

    def _ensure_repo_candidate(self, repo: str) -> dict:
        candidate = self.repo_candidates.get(repo)
        if candidate is None:
            candidate = {
                "candidate_level": "repo",
                "repo": repo,
                "topics": [],
                "code_queries": [],
                "topic_hits": 0,
                "code_hits": 0,
                "max_stars": 0,
                "selected_for_scan": False,
                "downloaded_skills": 0,
            }
            self.repo_candidates[repo] = candidate
        return candidate

    def _ensure_path_candidate(self, repo: str, path: str) -> dict:
        key = f"{repo}:{path}"
        candidate = self.path_candidates.get(key)
        if candidate is None:
            candidate = {
                "candidate_level": "path",
                "repo": repo,
                "path": path,
                "code_queries": [],
                "discovered_via_code_search": False,
                "discovered_via_repo_scan": False,
                "downloaded": False,
            }
            self.path_candidates[key] = candidate
        return candidate

    @staticmethod
    def _append_unique(items: list[str], value: str) -> bool:
        if value in items:
            return False
        items.append(value)
        return True

    @staticmethod
    def _is_skill_md_path(path: str) -> bool:
        """Only accept real SKILL.md files, not backups like SKILL.md.bak."""
        norm = (path or "").strip().replace("\\", "/")
        if not norm:
            return False
        lower = norm.lower()
        return lower == "skill.md" or lower.endswith("/skill.md")

    def _request(self, url, params=None):
        """Make rate-limited request"""
        if self.request_delay > 0:
            time.sleep(self.request_delay)
        try:
            resp = self.session.get(url, params=params, timeout=30)

            # Handle rate limiting
            if resp.status_code == 403:
                reset = int(resp.headers.get('X-RateLimit-Reset', 0))
                if reset:
                    wait = max(0, reset - time.time() + 1)
                    if wait < 3600:
                        logger.warning(f"Rate limited, waiting {wait:.0f}s")
                        time.sleep(wait)
                        return self._request(url, params)
                return None

            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    def discover_by_topics(self, topics=None):
        """Discover repositories by GitHub topics"""
        topics = topics or SKILL_TOPICS

        for topic in topics:
            logger.info(f"Searching topic: {topic}")

            page = 1
            while page <= self.max_topic_pages:
                url = f"{GITHUB_API}/search/repositories"
                params = {
                    'q': f'topic:{topic}',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 100,
                    'page': page,
                }

                result = self._request(url, params)
                if not result:
                    break

                items = result.get('items', [])
                if not items:
                    break

                for repo in items:
                    full_name = repo['full_name']
                    stars = int(repo.get('stargazers_count') or 0)
                    candidate = self._ensure_repo_candidate(full_name)
                    candidate["topic_hits"] += 1
                    candidate["max_stars"] = max(candidate["max_stars"], stars)
                    if self._append_unique(candidate["topics"], topic):
                        self.topic_stats[topic]["repo_hits"] += 1
                    if full_name not in self.discovered_repos:
                        self.discovered_repos.add(full_name)
                        logger.info(f"  Found: {full_name} ({stars} stars)")
                        if self.max_repos and len(self.discovered_repos) >= self.max_repos:
                            logger.info(
                                f"Reached max repos limit ({self.max_repos}) during topic discovery"
                            )
                            return list(self.discovered_repos)

                total = result.get('total_count', 0)
                if page * 100 >= total:
                    break
                page += 1

        logger.info(f"Discovered {len(self.discovered_repos)} repositories from topics")
        return list(self.discovered_repos)

    def discover_by_code_search(self, queries=None):
        """Discover SKILL.md files using GitHub Code Search"""
        if self.skip_code_search:
            logger.info("Skipping code search phase (--skip-code-search)")
            return list(self.discovered_repos)

        queries = queries or CODE_SEARCH_QUERIES

        for query in queries:
            logger.info(f"Code search: {query}")

            page = 1
            while page <= self.max_code_pages:
                url = f"{GITHUB_API}/search/code"
                params = {
                    'q': query,
                    'per_page': 100,
                    'page': page,
                }

                result = self._request(url, params)
                if not result:
                    break

                items = result.get('items', [])
                if not items:
                    break

                for item in items:
                    repo = item['repository']['full_name']
                    path = item['path']
                    if not self._is_skill_md_path(path):
                        continue

                    candidate = self._ensure_repo_candidate(repo)
                    candidate["code_hits"] += 1
                    if self._append_unique(candidate["code_queries"], query):
                        self.code_query_stats[query]["repo_hits"] += 1
                    path_candidate = self._ensure_path_candidate(repo, path)
                    path_candidate["discovered_via_code_search"] = True
                    if self._append_unique(path_candidate["code_queries"], query):
                        self.code_query_stats[query]["path_hits"] += 1

                    if repo not in self.discovered_repos:
                        self.discovered_repos.add(repo)
                        logger.info(f"  Found: {repo} - {path}")
                        if self.max_repos and len(self.discovered_repos) >= self.max_repos:
                            logger.info(
                                f"Reached max repos limit ({self.max_repos}) during code search"
                            )
                            return list(self.discovered_repos)

                total = result.get('total_count', 0)
                if page * 100 >= total:
                    break
                page += 1

        logger.info(f"Total discovered: {len(self.discovered_repos)} repositories")
        return list(self.discovered_repos)

    def get_skill_files_from_repo(self, repo):
        """Find all SKILL.md files in a repository"""
        skills = []

        # Common skill locations
        paths_to_check = [
            '',
            'skills',
            '.claude/skills',
            '.codex/skills',
        ]

        # First try to search the repo for SKILL.md files
        url = f"{GITHUB_API}/search/code"
        params = {
            'q': f'filename:SKILL.md repo:{repo}',
            'per_page': 100,
        }

        result = self._request(url, params)
        if result and result.get('items'):
            for item in result['items']:
                if not self._is_skill_md_path(item.get('path', '')):
                    continue
                skills.append({
                    'repo': repo,
                    'path': item['path'],
                    'html_url': item['html_url'],
                })

        return skills

    def download_skill(self, repo, path, output_dir):
        """Download a SKILL.md file"""
        blocked_source = blocked_metadata_source(
            {"repo": repo, "path": path},
            self.security_blocklist,
        )
        if blocked_source:
            blocked_entry, source_field = blocked_source
            logger.warning(
                "Blocked security-listed discovered source: %s via %s (%s)",
                blocked_entry["repo"],
                source_field,
                path,
            )
            return False

        # Extract skill name from path
        parts = path.rsplit('/', 1)
        if len(parts) == 2:
            skill_dir = parts[0].split('/')[-1] if '/' in parts[0] else parts[0]
        else:
            skill_dir = repo.split('/')[-1]

        # Normalize to lowercase to prevent case conflicts on macOS/Windows
        skill_dir = normalize_name(skill_dir)

        # Try to fetch content
        for branch in ['main', 'master']:
            url = f"{GITHUB_RAW}/{repo}/{branch}/{path}"
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    content = resp.text

                    # Validate it's a skill file
                    if '---' not in content[:100] and 'name:' not in content[:500]:
                        continue

                    # Save skill (case-safe)
                    category = "other"
                    key = build_skill_key(repo, path, name=skill_dir, category=category)

                    # Save metadata
                    legal_meta = build_legal_metadata(
                        repo=repo,
                        path=path,
                        branch=branch,
                    )
                    metadata = {
                        'name': skill_dir,
                        'repo': repo,
                        'path': path,
                        'github_branch': branch,
                        'category': category,
                        'source': f'github.com/{repo}',
                        'dir_name': skill_dir,
                        'downloaded_at': datetime.utcnow().isoformat() + 'Z',
                        **legal_meta,
                    }

                    output_dir.mkdir(parents=True, exist_ok=True)
                    with tempfile.TemporaryDirectory(
                        prefix=".discover-scan-",
                        dir=output_dir,
                    ) as temp_dir:
                        temp_skill_path = Path(temp_dir) / skill_dir
                        temp_skill_path.mkdir(parents=True, exist_ok=True)
                        (temp_skill_path / 'SKILL.md').write_text(content, encoding='utf-8')
                        (temp_skill_path / 'metadata.json').write_text(
                            json.dumps(metadata, indent=2), encoding='utf-8'
                        )
                        is_safe, issues = self.security_scanner.scan_file(
                            temp_skill_path / 'SKILL.md'
                        )

                    if not is_safe:
                        issue_types = sorted(
                            {str(issue.get("type") or "unknown") for issue in issues}
                        )
                        logger.warning(
                            "Rejected discovered skill after security scan: %s/%s (%s)",
                            repo,
                            path,
                            ", ".join(issue_types[:8]),
                        )
                        return False

                    skill_path = ensure_unique_dir(output_dir / category, skill_dir, key, repo=repo)
                    metadata['dir_name'] = skill_path.name

                    with tempfile.TemporaryDirectory(
                        prefix=".discover-final-scan-",
                        dir=output_dir,
                    ) as temp_dir:
                        staged_skill_path = Path(temp_dir) / skill_path.name
                        if skill_path.exists():
                            shutil.copytree(skill_path, staged_skill_path)
                        else:
                            staged_skill_path.mkdir(parents=True, exist_ok=True)
                        (staged_skill_path / 'SKILL.md').write_text(content, encoding='utf-8')
                        (staged_skill_path / 'metadata.json').write_text(
                            json.dumps(metadata, indent=2), encoding='utf-8'
                        )
                        is_safe, issues = self.security_scanner.scan_file(
                            staged_skill_path / 'SKILL.md'
                        )

                    if not is_safe:
                        issue_types = sorted(
                            {str(issue.get("type") or "unknown") for issue in issues}
                        )
                        logger.warning(
                            "Rejected discovered skill after final archive scan: %s/%s (%s)",
                            repo,
                            path,
                            ", ".join(issue_types[:8]),
                        )
                        return False

                    skill_path.mkdir(parents=True, exist_ok=True)
                    (skill_path / 'SKILL.md').write_text(content, encoding='utf-8')
                    (skill_path / 'metadata.json').write_text(
                        json.dumps(metadata, indent=2), encoding='utf-8'
                    )

                    return True
            except Exception as e:
                logger.debug(f"Failed to fetch {url}: {e}")

        return False

    def _write_candidates_jsonl(self, output_path: str, discovered_at: str, repos_to_scan: list[str]) -> int:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        selected = set(repos_to_scan)
        written = 0
        with path.open("w", encoding="utf-8") as handle:
            for repo in sorted(self.repo_candidates):
                item = dict(self.repo_candidates[repo])
                item["discovered_at"] = discovered_at
                item["candidate_key"] = f"repo:{repo}"
                item["selected_for_scan"] = repo in selected
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
                written += 1
            for key in sorted(self.path_candidates):
                item = dict(self.path_candidates[key])
                item["discovered_at"] = discovered_at
                item["candidate_key"] = f"path:{item['repo']}:{item['path']}"
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
                written += 1
        return written

    def _update_priors(self, priors_path: str, discovered_at: str, repos_to_scan: list[str]) -> None:
        path = Path(priors_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            try:
                priors = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                priors = {}
        else:
            priors = {}

        repo_priors = priors.setdefault("repo_priors", {})
        topic_yield = priors.setdefault("topic_yield", {})
        query_yield = priors.setdefault("query_yield", {})
        priors["version"] = 1
        priors["runs"] = int(priors.get("runs", 0)) + 1
        priors["updated_at"] = discovered_at

        selected = set(repos_to_scan)
        for repo, record in self.repo_candidates.items():
            repo_state = repo_priors.setdefault(
                repo,
                {
                    "seen_runs": 0,
                    "selected_runs": 0,
                    "downloaded_skills": 0,
                    "topic_hits": 0,
                    "code_hits": 0,
                    "max_stars": 0,
                    "last_seen_at": "",
                },
            )
            repo_state["seen_runs"] += 1
            if repo in selected:
                repo_state["selected_runs"] += 1
            repo_state["downloaded_skills"] += int(record.get("downloaded_skills") or 0)
            repo_state["topic_hits"] += int(record.get("topic_hits") or 0)
            repo_state["code_hits"] += int(record.get("code_hits") or 0)
            repo_state["max_stars"] = max(repo_state["max_stars"], int(record.get("max_stars") or 0))
            repo_state["last_seen_at"] = discovered_at

        for topic, stats in self.topic_stats.items():
            topic_state = topic_yield.setdefault(
                topic,
                {"repo_hits": 0, "repo_selected": 0, "downloaded_skills": 0},
            )
            topic_state["repo_hits"] += int(stats.get("repo_hits") or 0)
            topic_state["repo_selected"] += int(stats.get("repo_selected") or 0)
            topic_state["downloaded_skills"] += int(stats.get("downloaded_skills") or 0)

        for query, stats in self.code_query_stats.items():
            query_state = query_yield.setdefault(
                query,
                {"repo_hits": 0, "path_hits": 0, "downloaded_skills": 0},
            )
            query_state["repo_hits"] += int(stats.get("repo_hits") or 0)
            query_state["path_hits"] += int(stats.get("path_hits") or 0)
            query_state["downloaded_skills"] += int(stats.get("downloaded_skills") or 0)

        path.write_text(json.dumps(priors, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def run(
        self,
        output_dir='skills',
        output_json='sources/discovered.json',
        candidates_output='sources/learning/discovery_candidates.jsonl',
        priors_output='sources/learning/discovery_priors.json',
    ):
        """Run full discovery pipeline"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Phase 1: Discover by topics
        logger.info("=== Phase 1: Topic Discovery ===")
        self.discover_by_topics()

        # Phase 2: Discover by code search
        logger.info("\n=== Phase 2: Code Search ===")
        self.discover_by_code_search()

        # Phase 3: Download skills from discovered repos
        logger.info("\n=== Phase 3: Download Skills ===")
        downloaded = 0

        repos_to_scan = sorted(self.discovered_repos)
        if self.max_repos:
            repos_to_scan = repos_to_scan[:self.max_repos]

        logger.info(f"Scanning {len(repos_to_scan)} repositories for SKILL.md files")

        for repo in repos_to_scan:
            repo_candidate = self._ensure_repo_candidate(repo)
            repo_candidate["selected_for_scan"] = True
            for topic in repo_candidate["topics"]:
                self.topic_stats[topic]["repo_selected"] += 1
            logger.info(f"Scanning {repo}...")
            skill_files = self.get_skill_files_from_repo(repo)

            for skill in skill_files:
                path_candidate = self._ensure_path_candidate(repo, skill["path"])
                path_candidate["discovered_via_repo_scan"] = True
                if self.download_skill(repo, skill['path'], output_dir):
                    downloaded += 1
                    self.skills.append({
                        'repo': repo,
                        'path': skill['path'],
                    })
                    repo_candidate["downloaded_skills"] += 1
                    path_candidate["downloaded"] = True
                    for topic in repo_candidate["topics"]:
                        self.topic_stats[topic]["downloaded_skills"] += 1
                    for query in repo_candidate["code_queries"]:
                        self.code_query_stats[query]["downloaded_skills"] += 1
                    logger.info(f"  ✓ Downloaded: {skill['path']}")

        # Save discovery results
        discovered_at = datetime.utcnow().isoformat() + 'Z'
        Path(output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump({
                'discovered_at': discovered_at,
                'total_repos': len(self.discovered_repos),
                'total_skills': len(self.skills),
                'scanned_repos': len(repos_to_scan),
                'limits': {
                    'max_repos': self.max_repos,
                    'max_topic_pages': self.max_topic_pages,
                    'max_code_pages': self.max_code_pages,
                    'skip_code_search': self.skip_code_search,
                    'request_delay': self.request_delay,
                },
                'repos': repos_to_scan,
                'skills': self.skills,
            }, f, indent=2, ensure_ascii=False)

        candidates_written = self._write_candidates_jsonl(
            candidates_output,
            discovered_at,
            repos_to_scan,
        )
        self._update_priors(priors_output, discovered_at, repos_to_scan)

        logger.info(f"\n=== Summary ===")
        logger.info(f"Repositories discovered: {len(self.discovered_repos)}")
        logger.info(f"Skills downloaded: {downloaded}")
        logger.info(f"Candidate records written: {candidates_written}")
        logger.info(f"Results saved to: {output_json}")
        logger.info(f"Priors saved to: {priors_output}")

        return self.skills


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Discover skills from GitHub')
    parser.add_argument('--token', help='GitHub token (or set GITHUB_TOKEN env)')
    parser.add_argument('--output', default='skills', help='Output directory')
    parser.add_argument('--json', default='sources/discovered.json', help='JSON output')
    parser.add_argument(
        '--max-repos',
        type=int,
        default=0,
        help='Maximum repositories to scan in download phase (0 = no limit)',
    )
    parser.add_argument(
        '--max-topic-pages',
        type=int,
        default=10,
        help='Maximum pages per topic query (default: 10)',
    )
    parser.add_argument(
        '--max-code-pages',
        type=int,
        default=10,
        help='Maximum pages per code search query (default: 10)',
    )
    parser.add_argument(
        '--skip-code-search',
        action='store_true',
        help='Skip the global code search phase for faster runs',
    )
    parser.add_argument(
        '--request-delay',
        type=float,
        default=2.0,
        help='Delay (seconds) between GitHub API requests (default: 2.0)',
    )
    parser.add_argument(
        '--candidates-output',
        default='sources/learning/discovery_candidates.jsonl',
        help='JSONL output path for candidate-level discovery events',
    )
    parser.add_argument(
        '--priors-output',
        default='sources/learning/discovery_priors.json',
        help='JSON output path for aggregated discovery priors',
    )

    args = parser.parse_args()

    discoverer = GitHubTopicDiscovery(
        token=args.token,
        max_repos=args.max_repos,
        max_topic_pages=args.max_topic_pages,
        max_code_pages=args.max_code_pages,
        skip_code_search=args.skip_code_search,
        request_delay=args.request_delay,
    )
    discoverer.run(
        output_dir=args.output,
        output_json=args.json,
        candidates_output=args.candidates_output,
        priors_output=args.priors_output,
    )


if __name__ == '__main__':
    main()
