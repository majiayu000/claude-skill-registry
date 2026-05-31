#!/usr/bin/env python3
"""
Shared utilities for skill registry scripts.
"""

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml
from category_taxonomy import category_keywords, resolve_category

logger = logging.getLogger(__name__)

_DIR_CACHE = {}

PERMISSIVE_LICENSES = {
    "0BSD",
    "Apache-2.0",
    "BlueOak-1.0.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC0-1.0",
    "ISC",
    "MIT",
    "MIT-0",
    "Unlicense",
    "WTFPL",
    "Zlib",
}

# License families that should not be merged into MIT-compatible distribution by default.
RESTRICTED_LICENSE_PATTERNS = (
    "AGPL",
    "GPL",
    "LGPL",
    "MPL",
    "EUPL",
    "CC-BY-NC",
    "CC-BY-ND",
    "NONCOMMERCIAL",
    "NOASSERTION",
    "PROPRIETARY",
    "UNLICENSED",
    "UNKNOWN",
)

PLACEHOLDER_AUTHOR_VALUES = {"", "n/a", "na", "none", "null", "tbd", "unknown"}


def normalize_license(license_name: str) -> str:
    """Normalize common license aliases to stable SPDX-like IDs where possible."""
    text = (license_name or "").strip()
    if not text:
        return "NOASSERTION"

    lowered = text.lower()
    hyphenated = re.sub(r"[\s_]+", "-", lowered).strip("-")
    hyphenated = re.sub(r"-+", "-", hyphenated)
    if lowered in {"mit", "mit license"}:
        return "MIT"
    if lowered in {"apache-2.0", "apache 2.0", "apache license 2.0", "apache license version 2.0"}:
        return "Apache-2.0"
    if lowered in {"bsd-2-clause", "bsd 2-clause", "bsd 2 clause"}:
        return "BSD-2-Clause"
    if lowered in {"bsd-3-clause", "bsd 3-clause", "bsd 3 clause"}:
        return "BSD-3-Clause"
    if hyphenated in {"cc-by-nc-sa-4.0", "cc-by-nc-sa"}:
        return "CC-BY-NC-SA-4.0"
    if hyphenated in {"cc-by-nc-4.0", "cc-by-nc"}:
        return "CC-BY-NC-4.0"
    if hyphenated in {"cc-by-sa-4.0", "cc-by-sa"}:
        return "CC-BY-SA-4.0"
    if hyphenated in {"cc-by-4.0", "cc-by"}:
        return "CC-BY-4.0"
    return text


def classify_license(license_name: str) -> str:
    """
    Classify license compatibility for main MIT-like artifact.
    Returns: compatible | restricted | unknown
    """
    normalized = normalize_license(license_name)

    if normalized in PERMISSIVE_LICENSES:
        return "compatible"

    upper = re.sub(r"[\s_]+", "-", normalized.upper())
    for marker in RESTRICTED_LICENSE_PATTERNS:
        if marker in upper:
            return "restricted"

    # SPDX-like Creative Commons variants that are not explicitly permissive.
    if normalized.startswith("CC-") and normalized not in {"CC0-1.0"}:
        return "restricted"

    return "unknown"


def build_source_url(repo: str = "", path: str = "", branch: str = "main") -> str:
    """Build a canonical GitHub source URL for a skill entry."""
    repo = normalize_repo(repo)
    path = (path or "").strip().strip("/")

    if path.startswith("http://") or path.startswith("https://"):
        return path

    if not repo:
        return ""

    if not path:
        return f"https://github.com/{repo}"

    # path may be a folder or a direct markdown file path
    if not path.lower().endswith(".md"):
        path = f"{path}/SKILL.md"
    return f"https://github.com/{repo}/blob/{branch}/{path}"


def infer_author(repo: str = "", fallback: str = "") -> str:
    """Infer author from repo owner when explicit author metadata is missing."""
    fallback = (fallback or "").strip()
    if fallback.lower() not in PLACEHOLDER_AUTHOR_VALUES:
        return fallback

    repo = normalize_repo(repo)
    if "/" in repo:
        owner = repo.split("/", 1)[0].strip()
        if owner:
            return owner
    return "unknown"


def build_legal_metadata(
    repo: str = "",
    path: str = "",
    branch: str = "main",
    source_url: str = "",
    author: str = "",
    license_name: str = "",
    copyright_text: str = "",
    permission_note: str = "",
    distribution: str = "",
) -> dict:
    """
    Build a normalized legal metadata block.

    distribution:
        compatible -> license is compatible with MIT-like redistribution
        restricted -> non-compatible/unknown license, requires explicit handling
    """
    normalized_license = normalize_license(license_name)
    license_class = classify_license(normalized_license)

    source_url = (source_url or "").strip() or build_source_url(repo=repo, path=path, branch=branch)
    author = infer_author(repo=repo, fallback=author)

    if not distribution:
        distribution = "compatible" if license_class == "compatible" else "restricted"

    if not permission_note:
        if distribution == "compatible":
            permission_note = (
                "Use according to upstream license terms and attribution requirements."
            )
        else:
            permission_note = "Restricted or unknown license. Do not treat as MIT; verify upstream permission before reuse."

    if not copyright_text:
        if source_url:
            copyright_text = f"Copyright belongs to upstream author(s); see {source_url}"
        else:
            copyright_text = "Copyright belongs to upstream author(s)."

    return {
        "author": author,
        "source_url": source_url,
        "license": normalized_license,
        "copyright": copyright_text,
        "permission_note": permission_note,
        "distribution": distribution,
        "license_class": license_class,
    }


def is_valid_https_url(url: str) -> bool:
    """Return True if URL is a valid https URL."""
    text = (url or "").strip()
    if not text:
        return False
    parsed = urlparse(text)
    return parsed.scheme == "https" and bool(parsed.netloc)


def normalize_name(name: str) -> str:
    """
    Normalize skill/category name: lowercase, hyphens, max 64 chars.

    This prevents case-sensitivity issues on macOS/Windows filesystems.
    All scripts MUST use this function when creating skill directories.

    Examples:
        "Architect" -> "architect"
        "LangChain" -> "langchain"
        "Go-to-Market-Planner" -> "go-to-market-planner"
        "My Skill Name" -> "my-skill-name"
    """
    if not name:
        return "unknown"
    # Convert to lowercase, replace non-alphanumeric with hyphens
    name = re.sub(r"[^a-z0-9]+", "-", name.lower())
    # Strip leading/trailing hyphens, collapse consecutive hyphens
    name = re.sub(r"-+", "-", name).strip("-")
    # Max 64 chars
    return name[:64] if name else "unknown"


def normalize_category(category: str) -> str:
    """
    Normalize category name for directory creation.
    Do not resolve legacy aliases here: source intake should either provide a
    canonical category slug or be routed into an explicit review queue.
    """
    if not category:
        return "other"
    name = resolve_category(category, allow_unknown=True)
    name = re.sub(r"-+", "-", name).strip("-")
    return name[:32] if name else "other"


def _skill_key_text(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _normalize_skill_key_path(path: str = "") -> str:
    normalized = _skill_key_text(path).strip().replace("\\", "/").strip("/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if normalized == "." or normalized.lower() == "skill.md":
        return ""
    return normalized


def build_skill_key(repo: str = "", path: str = "", name: str = "", category: str = "") -> str:
    """Build a stable key for a skill to detect duplicates."""
    repo = _skill_key_text(repo).strip()
    path = _normalize_skill_key_path(path)
    name = _skill_key_text(name).strip()
    category = _skill_key_text(category).strip()
    if repo and path:
        return f"{repo}:{path}"
    if repo and name:
        return f"{repo}:name:{name}"
    if repo and category:
        return f"{repo}:{category}"
    if repo:
        return repo
    if category or name:
        return f"{category}:{name}"
    return ""


def canonical_metadata_identity(metadata: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    """Build metadata identity while treating known source aliases as equivalent."""
    identity: dict[str, Any] = {}
    alias_groups = {
        "path": ("github_path", "path"),
        "branch": ("github_branch", "branch"),
    }
    handled_aliases = set()
    field_set = set(fields)
    for canonical_field, aliases in alias_groups.items():
        if not any(alias in field_set for alias in aliases):
            continue
        handled_aliases.update(aliases)
        for alias in aliases:
            value = metadata.get(alias)
            if value not in (None, ""):
                identity[canonical_field] = value
                break

    for field in fields:
        if field in handled_aliases:
            continue
        value = metadata.get(field)
        if value not in (None, ""):
            identity[field] = value
    return identity


def iter_source_skills(source: dict):
    """Yield source rows with any top-level repo applied to rows that omit it."""
    default_repo = source.get("repo") if isinstance(source.get("repo"), str) else ""
    for skill in source.get("skills", []):
        if not isinstance(skill, dict):
            raise TypeError("source skill entry must be an object")
        if default_repo and not skill.get("repo"):
            skill = {**skill, "repo": default_repo}
        yield skill


def _short_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:8]


def short_hash(value: str) -> str:
    """Public short hash helper."""
    return _short_hash(value)


def normalize_repo(repo: str) -> str:
    """Normalize GitHub repo to owner/repo format."""
    repo = (repo or "").strip()
    if repo.startswith("https://github.com/"):
        repo = repo[len("https://github.com/") :]
    return repo.strip("/")


def get_repo_suffix(repo: str) -> str:
    """Get a short suffix from repo: owner-repo."""
    repo = normalize_repo(repo)
    if not repo or "/" not in repo:
        return ""
    owner, repo_name = repo.split("/", 1)
    owner = normalize_name(owner)[:20]
    repo_name = normalize_name(repo_name)[:20]
    if not owner and not repo_name:
        return ""
    if not repo_name:
        return owner
    return f"{owner}-{repo_name}"


def build_dir_name(base_name: str, repo: str = "") -> str:
    """Build directory name using repo suffix when provided."""
    base = normalize_name(base_name)
    suffix = get_repo_suffix(repo)
    return f"{base}-{suffix}" if suffix else base


def _metadata_key(metadata_path: Path) -> str:
    if not metadata_path.exists():
        return ""
    try:
        meta = json.loads(metadata_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return build_skill_key(
        meta.get("repo", ""),
        meta.get("path") or meta.get("github_path") or "",
        meta.get("name", ""),
        meta.get("category", ""),
    )


def ensure_unique_dir(parent: Path, base_name: str, key: str = "", repo: str = "") -> Path:
    """
    Ensure directory name is unique on case-insensitive filesystems.
    If a conflict exists, prefer repo suffix (name-owner-repo).
    """
    parent = Path(parent)
    base = normalize_name(base_name)
    parent.mkdir(parents=True, exist_ok=True)

    cache_key = str(parent.resolve())
    state = _DIR_CACHE.get(cache_key)
    if state is None:
        existing = {}
        key_to_dir = {}
        for d in parent.iterdir():
            if not d.is_dir():
                continue
            existing.setdefault(d.name.lower(), []).append(d)
            meta_key = _metadata_key(d / "metadata.json")
            if meta_key and meta_key not in key_to_dir:
                key_to_dir[meta_key] = d
        state = {"existing": existing, "key_to_dir": key_to_dir}
        _DIR_CACHE[cache_key] = state

    existing = state["existing"]
    key_to_dir = state["key_to_dir"]

    # Always reuse existing dir if it resolves to the same metadata key.
    if key and key in key_to_dir:
        return key_to_dir[key]

    # No conflict
    if base.lower() not in existing:
        candidate = parent / base
        existing.setdefault(base.lower(), []).append(candidate)
        if key:
            key_to_dir.setdefault(key, candidate)
        return candidate

    # Create a unique suffixed directory name
    suffix = get_repo_suffix(repo)
    if suffix and not base.endswith(f"-{suffix}"):
        candidate_base = f"{base}-{suffix}"
    elif suffix:
        candidate_base = base
    else:
        candidate_base = f"{base}-{_short_hash(key or base)}"
    candidate = candidate_base
    counter = 2
    while candidate.lower() in existing:
        candidate = f"{candidate_base}-{counter}"
        counter += 1

    selected = parent / candidate
    existing.setdefault(candidate.lower(), []).append(selected)
    if key:
        key_to_dir.setdefault(key, selected)
    return selected


# ---------------------------------------------------------------------------
# Shared metadata / frontmatter helpers
# ---------------------------------------------------------------------------

# Category keywords used across multiple scripts for auto-detection.
CATEGORY_KEYWORDS = category_keywords()


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content using safe_load."""
    if not content.startswith("---"):
        return {}
    try:
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return {}
        frontmatter = content[3:end_idx].strip()
        data = yaml.safe_load(frontmatter)
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def extract_description(content: str, max_length: int = 200) -> str:
    """Extract description from SKILL.md content (frontmatter or first paragraph)."""
    fm = extract_frontmatter(content)
    if fm.get("description"):
        return str(fm["description"])[:max_length]

    lines = content.split("\n")
    in_frontmatter = False
    for line in lines:
        line = line.strip()
        if line == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith("#"):
            continue
        if line and not line.startswith("```") and len(line) > 20:
            line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
            line = re.sub(r"[*_`]", "", line)
            return line[:max_length]
    return ""


def _semantic_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _semantic_tags(value: Any) -> tuple[list[str], str]:
    if isinstance(value, list):
        tags = [str(item).strip() for item in value if str(item).strip()]
        return tags, "list" if tags else ""
    tag_text = _semantic_text(value)
    if tag_text:
        return [tag_text], "string"
    return [], ""


def skill_semantic_fields(
    skill_dir: Path,
    *,
    metadata: dict[str, Any],
    frontmatter: dict[str, Any],
    rel: Path | None = None,
    content: str = "",
    content_chars: int = 0,
) -> dict[str, Any]:
    """Build SKILL.md-first semantic fields for classification and audit text."""
    sources: dict[str, str] = {}

    name = _semantic_text(frontmatter.get("name"))
    if name:
        sources["name"] = "frontmatter"
    else:
        name = _semantic_text(metadata.get("name"))
        sources["name"] = "metadata" if name else "directory"
    if not name:
        name = skill_dir.name

    description = _semantic_text(frontmatter.get("description"))
    if description:
        sources["description"] = "frontmatter"
    else:
        description = _semantic_text(metadata.get("description"))
        if description:
            sources["description"] = "metadata"
        elif content_chars > 0 and content:
            description = extract_description(content)
            if description:
                sources["description"] = "body"

    tags, tag_shape = _semantic_tags(frontmatter.get("tags"))
    if tags:
        sources["tags"] = f"frontmatter:{tag_shape}"
    else:
        tags, tag_shape = _semantic_tags(metadata.get("tags"))
        if tags:
            sources["tags"] = f"metadata:{tag_shape}"

    tag_text = " ".join(tags)
    text_parts = [
        name,
        description,
        tag_text,
        str(rel) if rel else "",
        content[:content_chars] if content_chars > 0 else "",
    ]
    text = " ".join(part for part in text_parts if part)

    return {
        "name": name,
        "description": description,
        "tags": tags,
        "tag_text": tag_text,
        "text": text,
        "sources": sources,
    }


def _semantic_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _keyword_matches(tokens: list[str], keyword: str) -> bool:
    parts = [part for part in keyword.split("-") if part]
    if not parts:
        return False
    if len(parts) > 1:
        window = len(parts)
        return any(tokens[index : index + window] == parts for index in range(len(tokens)))

    part = parts[0]
    if len(part) <= 3:
        return part in tokens
    return any(token == part or token.startswith(part) for token in tokens)


def category_keyword_scores(
    text: str,
    keyword_map: dict[str, list[str]] | None = None,
) -> dict[str, dict[str, Any]]:
    """Score taxonomy categories against semantic text and retain matched signals."""
    tokens = _semantic_tokens(text)
    scores: dict[str, dict[str, Any]] = {}
    for category, keywords in (keyword_map or CATEGORY_KEYWORDS).items():
        signals = [
            keyword
            for keyword in keywords
            if _keyword_matches(tokens, str(keyword).strip().lower())
        ]
        if signals:
            scores[category] = {
                "score": len(signals),
                "signals": signals,
            }
    return scores


def classify_category_from_semantics(
    semantics: dict[str, Any],
    *,
    default_category: str = "other",
    min_score: int = 2,
    min_delta: int = 1,
    high_score: int = 4,
    high_delta: int = 2,
) -> dict[str, Any]:
    """Classify semantic fields with auditable taxonomy keyword evidence."""
    scores = category_keyword_scores(str(semantics.get("text") or ""))
    ranked = sorted(
        scores.items(),
        key=lambda item: (-int(item[1]["score"]), item[0]),
    )
    semantic_sources = dict(semantics.get("sources") or {})

    if not ranked:
        return {
            "category": default_category,
            "status": "unclassified",
            "method": "taxonomy_keyword_v1",
            "confidence": "low",
            "reason": "no taxonomy keywords matched SKILL.md semantic text",
            "score": 0,
            "runner_up": "",
            "runner_up_score": 0,
            "signals": [],
            "semantic_sources": semantic_sources,
        }

    top_category, top = ranked[0]
    top_score = int(top["score"])
    runner_category = ranked[1][0] if len(ranked) > 1 else ""
    runner_score = int(ranked[1][1]["score"]) if len(ranked) > 1 else 0
    delta = top_score - runner_score

    if top_score < min_score:
        return {
            "category": default_category,
            "status": "unclassified",
            "method": "taxonomy_keyword_v1",
            "confidence": "low",
            "reason": (
                f"top category {top_category} scored {top_score}, below "
                f"minimum score {min_score}"
            ),
            "score": top_score,
            "runner_up": runner_category,
            "runner_up_score": runner_score,
            "signals": list(top["signals"]),
            "semantic_sources": semantic_sources,
        }

    if delta < min_delta:
        return {
            "category": default_category,
            "status": "unclassified",
            "method": "taxonomy_keyword_v1",
            "confidence": "low",
            "reason": (
                f"ambiguous taxonomy keyword scores: {top_category}={top_score}, "
                f"{runner_category}={runner_score}"
            ),
            "score": top_score,
            "runner_up": runner_category,
            "runner_up_score": runner_score,
            "signals": list(top["signals"]),
            "semantic_sources": semantic_sources,
        }

    confidence = "high" if top_score >= high_score and delta >= high_delta else "medium"
    return {
        "category": top_category,
        "status": "classified",
        "method": "taxonomy_keyword_v1",
        "confidence": confidence,
        "reason": (
            f"matched taxonomy keywords for {top_category}: "
            f"{', '.join(top['signals'])}"
        ),
        "score": top_score,
        "runner_up": runner_category,
        "runner_up_score": runner_score,
        "signals": list(top["signals"]),
        "semantic_sources": semantic_sources,
    }


def load_metadata(skill_dir: Path) -> dict:
    """Safely load metadata.json from a skill directory."""
    meta_path = skill_dir / "metadata.json"
    if not meta_path.exists():
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to load %s: %s", meta_path, e)
        return {}


def write_metadata(skill_dir: Path, meta: dict) -> None:
    """Write metadata.json to a skill directory."""
    meta_path = skill_dir / "metadata.json"
    meta_path.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def guess_category(text: str) -> str:
    """Guess category from combined text (path + content snippet)."""
    scored = category_keyword_scores(text)
    scores = {category: int(result["score"]) for category, result in scored.items()}
    if scores:
        return max(scores, key=scores.get)
    return "other"
