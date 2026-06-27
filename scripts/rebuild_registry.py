#!/usr/bin/env python3
"""
Rebuild registry.json from downloaded skills.

Scans archived SKILL.md files recursively and rebuilds the registry index.
"""

import gzip
import hashlib
import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from utils import (
    extract_description,
    is_declared_bundled_skill_file,
    load_metadata,
    normalize_category,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def utc_now_isoformat() -> str:
    """Return a stable UTC timestamp with trailing Z."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_write_registry(registry_path: Path, registry: dict) -> bool:
    """Safely write registry.json with atomic operation"""
    temp_path = registry_path.with_suffix(".json.tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, separators=(",", ":"))

        temp_path.rename(registry_path)
        return True
    except Exception:
        logger.exception("Failed to write registry")
        try:
            if temp_path.exists():
                temp_path.unlink()
        except Exception as cleanup_error:
            logger.error(
                "Failed to remove temporary registry file %s: %s",
                temp_path,
                cleanup_error,
            )
        raise


def safe_write_json(output_path: Path, payload: dict) -> None:
    """Write compact JSON atomically."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    temp_path.replace(output_path)


def safe_write_gzip_json(output_path: Path, payload: dict) -> None:
    """Write compact gzipped JSON atomically."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    with gzip.open(temp_path, "wt", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    temp_path.replace(output_path)


def skill_install_key(skill: dict) -> str:
    """Build the stable install key used for registry sharding."""
    repo = skill.get("repo", "")
    path = skill.get("path", "")
    name = skill.get("name", "unknown")
    category = skill.get("category", "other")

    if repo and path:
        return f"{repo}/{path}"
    if repo:
        return repo
    if path:
        return f"local/{path}"
    return f"local/{category}/{name}"


def registry_shard_id(skill: dict) -> str:
    """Return the two-character shard id for a skill."""
    branch = skill.get("branch", "main") or "main"
    key = f"{skill_install_key(skill)}|{branch}".encode("utf-8")
    return hashlib.sha256(key).hexdigest()[:2]


def remove_stale_shards(shards_dir: Path) -> int:
    """Remove old shard JSON files before writing a fresh shard set."""
    if not shards_dir.exists():
        return 0

    removed = 0
    for pattern in ("*.json", "*.json.gz"):
        for path in shards_dir.glob(pattern):
            path.unlink()
            removed += 1
    return removed


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_reference(path: Path, base_dir: Path) -> str:
    """Return a portable artifact reference relative to base_dir when possible."""
    resolved_path = path.resolve()
    resolved_base = base_dir.resolve()
    try:
        return resolved_path.relative_to(resolved_base).as_posix()
    except ValueError:
        return resolved_path.as_posix()


def write_registry_shards(
    skills: list[dict],
    shards_dir: Path,
    generated_at: str,
    reference_base: Path | None = None,
) -> list[dict]:
    """Write 256 registry shards and return manifest entries."""
    remove_stale_shards(shards_dir)
    reference_base = reference_base or shards_dir.parent
    shards: dict[str, list[dict]] = {f"{idx:02x}": [] for idx in range(256)}

    for skill in skills:
        shards[registry_shard_id(skill)].append(skill)

    manifest_entries: list[dict] = []
    for shard_id, shard_skills in sorted(shards.items()):
        shard_payload = {
            "schema_version": 1,
            "shard": shard_id,
            "generated_at": generated_at,
            "count": len(shard_skills),
            "skills": shard_skills,
        }
        shard_path = shards_dir / f"{shard_id}.json"
        gzip_path = shards_dir / f"{shard_id}.json.gz"
        safe_write_json(shard_path, shard_payload)
        safe_write_gzip_json(gzip_path, shard_payload)
        manifest_entries.append(
            {
                "id": shard_id,
                "path": artifact_reference(shard_path, reference_base),
                "gzip_path": artifact_reference(gzip_path, reference_base),
                "count": len(shard_skills),
                "bytes": shard_path.stat().st_size,
                "gzip_bytes": gzip_path.stat().st_size,
                "sha256": file_sha256(shard_path),
            }
        )

    return manifest_entries


def build_registry_manifest(
    *,
    generated_at: str,
    total_count: int,
    plugin_count: int,
    shards: list[dict],
    summary_path: str,
    plugins_path: str,
    provenance: dict | None = None,
) -> dict:
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "total_count": total_count,
        "plugin_count": plugin_count,
        "shard_strategy": "sha256-install-branch-prefix",
        "shard_count": len(shards),
        "record_key": "install|branch",
        "provenance": provenance or {},
        "summary": summary_path,
        "shards": shards,
        "plugins": {
            "path": plugins_path,
            "count": plugin_count,
        },
    }


def build_compatibility_registry(
    *,
    generated_at: str,
    total_count: int,
    plugin_count: int,
    archive_skill_md_count_raw: int,
    archive_metadata_count_raw: int,
    manifest_path: str | None = None,
) -> dict:
    message = "Full registry payload moved to registry-shards/*.json"
    if not manifest_path:
        message = "Full registry payload is published in the merged claude-skill-registry artifact"

    registry = {
        "version": "2.2.0",
        "updated_at": generated_at,
        "total_count": total_count,
        "plugin_count": plugin_count,
        "archive_skill_md_count_raw": archive_skill_md_count_raw,
        "archive_metadata_count_raw": archive_metadata_count_raw,
        "registry_skill_count_dedup": total_count,
        "deprecated_full_payload": True,
        "message": message,
    }
    if manifest_path:
        registry["manifest"] = manifest_path
    return registry


def scan_skills(skills_dir: Path) -> list:
    """
    Scan archived skills and build index.

    Supports archive layout:
    - <archive-root>/**/SKILL.md

    Metadata is optional for indexing. If metadata.json exists, it augments fields;
    otherwise fallback values are derived from path/content.
    """
    skills: list[dict] = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

    for skill_md in skills_dir.rglob("SKILL.md"):
        if is_declared_bundled_skill_file(skill_md, skills_dir):
            continue
        skill_dir = skill_md.parent
        rel_dir = skill_dir.relative_to(skills_dir)
        rel_parts = rel_dir.parts

        metadata = load_metadata(skill_dir)

        # Determine name
        name = metadata.get("name") or (rel_parts[-1] if rel_parts else skill_dir.name)

        # Determine category (prefer explicit metadata, then infer from path)
        inferred_category = rel_parts[0] if rel_parts else "other"
        category = metadata.get("category") or inferred_category

        # Read SKILL.md for description
        try:
            content = skill_md.read_text(encoding="utf-8")
            description = metadata.get("description") or extract_description(content)
        except UnicodeDecodeError as e:
            logger.warning(f"Encoding error reading {skill_md}: {e}")
            description = ""
        except Exception as e:
            logger.warning(f"Error reading {skill_md}: {e}")
            description = ""

        # Repo/path/branch normalization across different metadata formats
        repo = metadata.get("repo", "")
        github_path = metadata.get("github_path") or metadata.get("path") or "/".join(rel_parts)
        github_branch = metadata.get("github_branch") or metadata.get("branch") or "main"

        skill_entry = {
            "name": name,
            "description": description[:200] if description else f"Skill: {name}",
            "repo": repo,
            "path": github_path,
            "branch": github_branch,
            "category": category,
            "tags": metadata.get("tags", []),
            "stars": metadata.get("stars", 0),
            "source": metadata.get("source", "local"),
        }

        for key in ("author", "source_url", "license", "distribution", "permission_note"):
            value = metadata.get(key, "")
            if value not in ("", None):
                skill_entry[key] = value

        skills.append(skill_entry)

    return skills


def cleanup_orphan_metadata(skills_dir: Path) -> int:
    """
    Remove metadata.json files whose directories do not contain SKILL.md.

    This keeps archive parity clean without enforcing strict metadata schema checks.
    """
    skill_dirs = {p.parent for p in skills_dir.rglob("SKILL.md")}
    removed = 0

    for metadata_path in skills_dir.rglob("metadata.json"):
        if metadata_path.parent in skill_dirs:
            continue
        try:
            metadata_path.unlink()
            removed += 1
        except Exception as e:
            logger.warning(f"Failed to remove orphan metadata {metadata_path}: {e}")

    return removed


def sanitize_category(category: str) -> str:
    """Sanitize category name for use as filename."""
    return normalize_category(category or "other")


def build_category_indexes(skills: list, output_dir: Path):
    """Build category-based indexes."""
    categories = defaultdict(list)

    for skill in skills:
        cat = skill.get("category", "other")
        # Sanitize category for filename safety
        safe_cat = sanitize_category(cat)
        categories[safe_cat].append(skill)

    output_dir.mkdir(exist_ok=True)

    for cat, cat_skills in categories.items():
        cat_file = output_dir / f"{cat}.json"
        cat_data = {
            "category": cat,
            "count": len(cat_skills),
            "updated_at": utc_now_isoformat(),
            "skills": sorted(cat_skills, key=lambda x: (-x.get("stars", 0), x["name"])),
        }
        with open(cat_file, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)
        print(f"  {cat}: {len(cat_skills)} skills")

    # Index file
    index = {
        "updated_at": utc_now_isoformat(),
        "categories": [
            {"name": cat, "count": len(skills)} for cat, skills in sorted(categories.items())
        ],
    }
    with open(output_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def load_plugins(sources_dir: Path) -> list:
    """Load plugins from sources/plugins.json."""
    plugins_path = sources_dir / "plugins.json"
    if not plugins_path.exists():
        return []
    try:
        with open(plugins_path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("plugins", [])
    except Exception as e:
        logger.warning(f"Failed to load plugins: {e}")
        return []


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rebuild registry.json from downloaded skills")
    parser.add_argument("--skills-dir", default="skills", help="Skills directory to scan")
    parser.add_argument("--registry", default="registry.json", help="Output registry.json path")
    parser.add_argument(
        "--manifest", default="registry-manifest.json", help="Output shard manifest path"
    )
    parser.add_argument(
        "--shards-dir", default="registry-shards", help="Output registry shards directory"
    )
    parser.add_argument(
        "--categories-dir", default="categories", help="Output categories directory"
    )
    parser.add_argument(
        "--skip-categories", action="store_true", help="Do not write category index files"
    )
    parser.add_argument(
        "--compat-manifest-pointer",
        action="store_true",
        help="Include the shard manifest path in registry.json when manifest/shards are published with it",
    )

    args = parser.parse_args()

    def _main_from_args() -> None:
        script_dir = Path(__file__).parent
        registry_dir = script_dir.parent

        skills_dir = (registry_dir / args.skills_dir).resolve()
        registry_path = (registry_dir / args.registry).resolve()
        manifest_path = (registry_dir / args.manifest).resolve()
        shards_dir = (registry_dir / args.shards_dir).resolve()
        categories_dir = (registry_dir / args.categories_dir).resolve()
        sources_dir = (registry_dir / "sources").resolve()

        print("=" * 60)
        print("REBUILDING REGISTRY FROM DOWNLOADED SKILLS")
        print("=" * 60)
        print()

        print("Cleaning orphan metadata.json files...")
        orphan_removed = cleanup_orphan_metadata(skills_dir)
        print(f"Removed {orphan_removed} orphan metadata files")
        print()

        print(f"Scanning skills directory: {skills_dir}")
        skills = scan_skills(skills_dir)
        print(f"Found {len(skills)} skills")
        print()

        # Remove duplicates by repo:path (more accurate than name-only)
        # This prevents losing skills with same name but different sources
        seen = set()
        unique_skills = []
        duplicates_removed = 0

        for s in skills:
            # Use repo:path as unique key (most accurate)
            repo = s.get("repo", "")
            path = s.get("path", "")

            if repo and path:
                key = f"{repo}:{path}"
            elif repo:
                key = repo
            else:
                # Fallback to category:name for local skills without repo
                key = f"{s.get('category', 'other')}:{s['name']}"

            if key not in seen:
                seen.add(key)
                unique_skills.append(s)
            else:
                duplicates_removed += 1

        print(f"Duplicates removed: {duplicates_removed}")
        print(f"Unique skills: {len(unique_skills)}")
        print()

        # Sort by stars then name
        unique_skills.sort(key=lambda x: (-x.get("stars", 0), x["name"].lower()))

        # Load plugins
        plugins = load_plugins(sources_dir)
        print(f"Plugins loaded: {len(plugins)}")
        print()

        archive_skill_md_count_raw = sum(1 for _ in skills_dir.rglob("SKILL.md"))
        archive_metadata_count_raw = sum(1 for _ in skills_dir.rglob("metadata.json"))

        generated_at = utc_now_isoformat()
        manifest_ref = artifact_reference(manifest_path, registry_path.parent)

        print(f"Writing registry shards: {shards_dir}")
        shard_entries = write_registry_shards(
            unique_skills,
            shards_dir,
            generated_at,
            reference_base=manifest_path.parent,
        )
        print(f"Written {len(shard_entries)} registry shards")
        print()

        manifest = build_registry_manifest(
            generated_at=generated_at,
            total_count=len(unique_skills),
            plugin_count=len(plugins),
            shards=shard_entries,
            summary_path="registry_summary.json",
            plugins_path="sources/plugins.json",
        )
        safe_write_json(manifest_path, manifest)
        print(f"Written {manifest_path}")
        print()

        registry = build_compatibility_registry(
            generated_at=generated_at,
            total_count=len(unique_skills),
            plugin_count=len(plugins),
            archive_skill_md_count_raw=archive_skill_md_count_raw,
            archive_metadata_count_raw=archive_metadata_count_raw,
            manifest_path=manifest_ref if args.compat_manifest_pointer else None,
        )

        safe_write_registry(registry_path, registry)
        print(
            f"Written compatibility {registry_path} "
            f"with {len(unique_skills)} skills, {len(plugins)} plugins"
        )
        print()

        if not args.skip_categories:
            print(f"Building category indexes: {categories_dir}")
            build_category_indexes(unique_skills, categories_dir)
            print()

            # Stats
            print("=" * 60)
            print("CATEGORY DISTRIBUTION")
            print("=" * 60)
            cat_counts = defaultdict(int)
            for s in unique_skills:
                cat_counts[s.get("category", "other")] += 1

            for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
                pct = count / len(unique_skills) * 100 if unique_skills else 0
                bar = "█" * int(pct / 2)
                print(f"  {cat:15} {count:6} ({pct:5.1f}%) {bar}")

            print()

        print("=" * 60)
        print("DONE!")
        print("=" * 60)

    _main_from_args()
