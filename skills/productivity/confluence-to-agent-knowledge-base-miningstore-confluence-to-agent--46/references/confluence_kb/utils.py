"""
Shared utilities for confluence-kb.
"""

from __future__ import annotations

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import frontmatter
import tiktoken


def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:120]


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Count tokens in text using tiktoken."""
    try:
        enc = tiktoken.get_encoding(model)
        return len(enc.encode(text))
    except Exception:
        # Rough fallback: ~4 chars per token
        return len(text) // 4


def read_md_file(path: Path) -> tuple[dict, str]:
    """Read a markdown file with YAML frontmatter. Returns (metadata, content)."""
    if not path.exists():
        return {}, ""
    post = frontmatter.load(str(path))
    return dict(post.metadata), post.content


def write_md_file(path: Path, content: str, metadata: Optional[dict] = None) -> None:
    """Write a markdown file with optional YAML frontmatter."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if metadata:
        post = frontmatter.Post(content, **metadata)
        path.write_text(frontmatter.dumps(post))
    else:
        path.write_text(content)


def content_hash(text: str) -> str:
    """Generate a short content hash for change detection."""
    return hashlib.md5(text.encode()).hexdigest()[:12]


def now_iso() -> str:
    """Current time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def clean_confluence_markdown(md: str) -> str:
    """
    Clean up Confluence-exported markdown.
    Removes Confluence-specific artifacts, blob URLs, custom tags, etc.
    """
    # Remove blob image URLs (media attachments that won't resolve locally)
    md = re.sub(
        r'!\[.*?\]\(blob:https://media\.staging\.atl-paas\.net/\?[^)]+\)',
        '[image]',
        md
    )

    # Remove custom data tags (Confluence macros)
    md = re.sub(
        r'<custom[^>]*>.*?</custom>',
        '',
        md,
        flags=re.DOTALL
    )

    # Clean up excessive blank lines
    md = re.sub(r'\n{4,}', '\n\n\n', md)

    # Remove zero-width spaces and other Unicode artifacts
    md = md.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')

    # Clean up empty table cells
    md = re.sub(r'\|\s*\|\s*\|', '| | |', md)

    return md.strip()


def truncate_for_context(text: str, max_tokens: int = 8000) -> str:
    """Truncate text to fit within a token budget."""
    tokens = count_tokens(text)
    if tokens <= max_tokens:
        return text
    # Rough truncation by character count
    ratio = max_tokens / tokens
    cut_point = int(len(text) * ratio * 0.95)  # 5% safety margin
    return text[:cut_point] + "\n\n[... content truncated ...]"


def load_sync_state(state_path: Path) -> dict:
    """Load the sync state file tracking last ingest timestamps."""
    if not state_path.exists():
        return {"last_sync": None, "pages": {}}
    with open(state_path) as f:
        return json.load(f)


def save_sync_state(state_path: Path, state: dict) -> None:
    """Save sync state to disk."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
