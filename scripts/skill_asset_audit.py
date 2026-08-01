"""Shared helpers for auditing bundled-asset composition of archived skills.

The data archive stores only SKILL.md + metadata.json, so bundled assets are
inferred from relative-path references in the SKILL.md body, then verified
against the upstream repository tree.
"""
from __future__ import annotations

import json
import os
import re
import subprocess

EXEC_EXTENSIONS = {
    ".py", ".sh", ".bash", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".rb", ".go", ".rs", ".pl", ".ps1", ".lua", ".php",
}
DOC_EXTENSIONS = {".md", ".markdown", ".rst", ".txt", ".adoc"}

_EXEC_REF_RE = re.compile(
    r"(?<![\w/])(?:\./)?[A-Za-z0-9_\-]+(?:/[A-Za-z0-9_.\-]+)*\."
    r"(?:py|sh|bash|js|mjs|ts|tsx|rb|go|rs|pl|ps1|lua|php)\b"
)
_DOC_REF_RE = re.compile(
    r"(?<![\w/])(?:\./)?(?:references|reference|docs|assets|templates)/"
    r"[A-Za-z0-9_.\-/]+\.(?:md|txt|json|yaml|yml|csv|html)\b"
)
_URL_RE = re.compile(r"https?://\S+")


def classify_skill_text(text: str) -> str:
    """Bucket a SKILL.md body by the local files it references.

    Returns "EXEC" (references script/code files), "REF" (extra local docs
    only), or "BARE" (no local file references). URLs are stripped first so
    links to files on other hosts do not count as bundled references.
    """
    text = _URL_RE.sub("", text)
    if _EXEC_REF_RE.search(text):
        return "EXEC"
    if _DOC_REF_RE.search(text):
        return "REF"
    return "BARE"


def classify_files(paths: list[str]) -> dict[str, int]:
    """Count sibling files by kind, ignoring SKILL.md / metadata.json."""
    counts = {"exec": 0, "doc": 0, "asset": 0}
    for path in paths:
        base = os.path.basename(path)
        if base in ("SKILL.md", "metadata.json"):
            continue
        ext = os.path.splitext(base)[1].lower()
        if ext in EXEC_EXTENSIONS:
            counts["exec"] += 1
        elif ext in DOC_EXTENSIONS:
            counts["doc"] += 1
        else:
            counts["asset"] += 1
    return counts


def verdict_from_counts(counts: dict[str, int]) -> str:
    """Collapse sibling-file counts into a verified bucket."""
    if counts["exec"]:
        return "EXEC"
    if counts["doc"] or counts["asset"]:
        return "REF_ASSET"
    return "BARE"


def fetch_repo_tree(repo: str, timeout: int = 120) -> list[str]:
    """Return all blob paths of the repo's default branch via `gh api`.

    Raises RuntimeError with the gh stderr on failure so callers surface the
    error instead of silently treating the repo as empty.
    """
    result = subprocess.run(
        [
            "gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1",
            "--jq", '[.tree[] | select(.type=="blob") | .path]',
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh api tree failed for {repo}: {result.stderr.strip()[:200]}")
    return json.loads(result.stdout)


def iter_archived_skills(root: str):
    """Yield (dirpath, metadata dict or None) for each archived skill dir."""
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        if "SKILL.md" not in filenames:
            continue
        meta = None
        meta_path = os.path.join(dirpath, "metadata.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, encoding="utf-8") as fh:
                    meta = json.load(fh)
            except (OSError, json.JSONDecodeError):
                meta = None
        yield dirpath, meta
