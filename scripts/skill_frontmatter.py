"""Canonical SKILL.md frontmatter normalization helpers."""

from __future__ import annotations

import re
from typing import Any

import yaml
from utils import extract_description, normalize_name, split_frontmatter_content

TRAILING_HORIZONTAL_WHITESPACE_RE = re.compile(r"[ \t]+(?=\r?$)", re.MULTILINE)


def _strip_trailing_whitespace(content: str) -> str:
    return TRAILING_HORIZONTAL_WHITESPACE_RE.sub("", content)


def _source_text(source: dict[str, Any], key: str) -> str:
    value = source.get(key)
    return value.strip() if isinstance(value, str) else ""


def _frontmatter_and_body(content: str) -> tuple[dict[str, Any] | None, str]:
    raw_frontmatter, body = split_frontmatter_content(content)
    if raw_frontmatter is None:
        return None, content

    try:
        frontmatter = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError:
        return None, content
    if not isinstance(frontmatter, dict):
        return None, content
    return frontmatter, body


def _canonical_description(content: str, source: dict[str, Any], name: str) -> str:
    source_description = _source_text(source, "description")
    if 10 <= len(source_description) <= 500:
        return source_description

    derived = extract_description(content, max_length=500).strip()
    if len(derived) >= 10:
        return derived[:500]

    return f"Archived skill guidance for {name}."[:500]


def normalize_skill_frontmatter(
    content: str,
    source: dict[str, Any],
    *,
    fallback_name: str = "",
) -> str:
    """Repair absent/invalid frontmatter and bound an overlong description.

    Valid upstream mappings are preserved except for the existing overlong
    description repair. Invalid or absent mappings are replaced by the minimum
    registry schema fields, using archive metadata before body-derived text.
    """
    frontmatter, body = _frontmatter_and_body(content)
    if frontmatter is not None:
        upstream_description = frontmatter.get("description")
        if not isinstance(upstream_description, str) or len(upstream_description) <= 500:
            return content

        source_description = _source_text(source, "description")
        if not 10 <= len(source_description) <= 500:
            return content

        frontmatter["description"] = source_description
        rendered = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
        return _strip_trailing_whitespace(f"---\n{rendered}\n---{body}")

    name = normalize_name(_source_text(source, "name") or fallback_name)
    description = _canonical_description(body, source, name)
    rendered = yaml.safe_dump(
        {"name": name, "description": description},
        sort_keys=False,
        allow_unicode=True,
    ).strip()
    normalized_body = body.lstrip("\r\n")
    separator = "\n\n" if normalized_body else "\n"
    return _strip_trailing_whitespace(
        f"---\n{rendered}\n---{separator}{normalized_body}"
    )
