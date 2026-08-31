#!/usr/bin/env python3
"""Generate a bounded set of crawlable skill pages from featured records."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

PUBLIC_SITE = "https://majiayu000.github.io/claude-skill-registry/"
STATIC_PAGE_LIMIT = 20
FEATURED_START = "<!-- static-featured:start -->"
FEATURED_END = "<!-- static-featured:end -->"
GENERATED_MARKER = ".generated-static-skill-pages"


def select_featured_skills(
    records: Iterable[dict[str, Any]], limit: int = STATIC_PAGE_LIMIT
) -> list[dict[str, Any]]:
    """Return the highest-starred safe records that have a known install path."""
    eligible = [
        record
        for record in records
        if record.get("security_status") == "passed"
        and record.get("install_status") == "known_good"
        and "/" in str(record.get("repo") or "")
        and record.get("name")
    ]
    return sorted(
        eligible,
        key=lambda record: (
            int(record.get("stars", 0) or 0),
            int(record.get("quality_score", 0) or 0),
            str(record.get("name") or "").casefold(),
        ),
        reverse=True,
    )[:limit]


def skill_page_slug(record: dict[str, Any]) -> str:
    """Build a readable slug with a stable identity suffix."""
    base = re.sub(
        r"[^a-z0-9]+", "-", str(record.get("name") or "").casefold()
    ).strip("-")
    if not base:
        base = "skill"
    stable_id = str(record.get("id") or "").strip().casefold()
    if not stable_id:
        identity = f"{record.get('install', '')}|{record.get('branch', 'main')}"
        stable_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    suffix = re.sub(r"[^a-z0-9]+", "-", stable_id).strip("-")[:8]
    return f"{base}-{suffix or 'unknown'}"


def _source_url(record: dict[str, Any]) -> str:
    repo = quote(str(record.get("repo") or ""), safe="/")
    branch = quote(str(record.get("branch") or "main"), safe="/")
    path = quote(str(record.get("path") or "").strip("/"), safe="/")
    base = f"https://github.com/{repo}/tree/{branch}"
    return f"{base}/{path}" if path else base


def _render_detail_page(record: dict[str, Any], slug: str) -> str:
    name = html.escape(str(record.get("name") or "Unnamed skill"))
    description = html.escape(
        str(record.get("description") or "No description provided.")
    )
    repo = html.escape(str(record.get("repo") or ""))
    category = html.escape(str(record.get("category") or "other"))
    quality = html.escape(str(record.get("quality_grade") or "unknown"))
    security = html.escape(str(record.get("security_status") or "unknown"))
    install_status = html.escape(str(record.get("install_status") or "unknown"))
    tags = [html.escape(str(tag)) for tag in (record.get("tags") or [])]
    tag_text = ", ".join(tags) if tags else "No tags"
    canonical = f"{PUBLIC_SITE}skills/{slug}/"
    install_command = html.escape(
        f"npx skills add {record.get('repo', '')} --skill {record.get('name', '')}"
    )
    source_url = html.escape(_source_url(record), quote=True)
    raw_meta_description = " ".join(
        str(record.get("description") or "").split()
    )[:160]
    meta_description = html.escape(raw_meta_description, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} — Claude Skills Registry</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{name} — Claude Skills Registry">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:url" content="{canonical}">
  <meta name="twitter:card" content="summary">
  <style>body{{font:16px/1.6 system-ui,sans-serif;max-width:760px;margin:3rem auto;padding:0 1rem;color:#202124}}code{{display:block;overflow:auto;padding:1rem;background:#f4f4f4;border-radius:.5rem}}dt{{font-weight:700}}dd{{margin:0 0 .75rem}}</style>
</head>
<body>
  <p><a href="{PUBLIC_SITE}">← Claude Skills Registry</a></p>
  <main>
    <h1>{name}</h1>
    <p>{description}</p>
    <dl>
      <dt>Source</dt><dd><a href="{source_url}">{repo}</a></dd>
      <dt>Category</dt><dd>{category}</dd>
      <dt>Tags</dt><dd>{tag_text}</dd>
      <dt>Quality</dt><dd>{quality}</dd>
      <dt>Security scan</dt><dd>{security}</dd>
      <dt>Install status</dt><dd>{install_status}</dd>
    </dl>
    <h2>Install</h2>
    <code>{install_command}</code>
    <p><small>Review third-party skill content before installation. A passed registry scan is not a guarantee of safety or quality.</small></p>
  </main>
</body>
</html>
"""


def _render_homepage_links(records: list[dict[str, Any]]) -> str:
    items = "\n".join(
        f'      <li><a href="skills/{skill_page_slug(record)}/">'
        f'{html.escape(str(record["name"]))}</a></li>'
        for record in records
    )
    return f"""{FEATURED_START}
<section class="featured-static" aria-labelledby="featured-static-heading">
  <h2 id="featured-static-heading">Featured skill guides</h2>
  <p>Browse crawlable details for a bounded set of high-signal, security-scanned skills.</p>
  <ul>
{items}
  </ul>
</section>
{FEATURED_END}"""


def _update_homepage(output_dir: Path, records: list[dict[str, Any]]) -> None:
    homepage_path = output_dir / "index.html"
    if not homepage_path.exists():
        return
    homepage = homepage_path.read_text(encoding="utf-8")
    start = homepage.find(FEATURED_START)
    end = homepage.find(FEATURED_END)
    if start < 0 or end < 0 or end < start:
        raise ValueError("docs/index.html is missing a valid static featured block")
    end += len(FEATURED_END)
    homepage_path.write_text(
        homepage[:start] + _render_homepage_links(records) + homepage[end:],
        encoding="utf-8",
    )


def _write_sitemap(output_dir: Path, slugs: list[str]) -> None:
    urls = [PUBLIC_SITE, *(f"{PUBLIC_SITE}skills/{slug}/" for slug in slugs)]
    rows = "\n".join(f"  <url><loc>{html.escape(url)}</loc></url>" for url in urls)
    (output_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{rows}\n"
        "</urlset>\n",
        encoding="utf-8",
    )


def _prepare_generated_root(output_dir: Path) -> Path:
    generated_root = output_dir / "skills"
    if generated_root.exists():
        marker = generated_root / GENERATED_MARKER
        if any(generated_root.iterdir()) and not marker.is_file():
            raise ValueError(
                f"Refusing to replace {generated_root}: directory is not marked as generated"
            )
        shutil.rmtree(generated_root)
    generated_root.mkdir()
    (generated_root / GENERATED_MARKER).write_text("generated\n", encoding="utf-8")
    return generated_root


def build_static_skill_pages(
    featured_records: Iterable[dict[str, Any]], output_dir: Path
) -> dict[str, Any]:
    """Write bounded detail pages, homepage links, and their sitemap entries."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = select_featured_skills(featured_records)
    generated_root = _prepare_generated_root(output_dir)

    slugs: list[str] = []
    for record in records:
        slug = skill_page_slug(record)
        if slug in slugs:
            raise ValueError(f"Duplicate generated skill page slug: {slug}")
        detail_dir = generated_root / slug
        detail_dir.mkdir(parents=True)
        (detail_dir / "index.html").write_text(
            _render_detail_page(record, slug), encoding="utf-8"
        )
        slugs.append(slug)

    _update_homepage(output_dir, records)
    _write_sitemap(output_dir, slugs)
    return {"generated_count": len(records), "slugs": slugs}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--featured", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.featured.read_text(encoding="utf-8"))
    records = payload.get("skills") if isinstance(payload, dict) else None
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise ValueError(f"Featured artifact has no valid skills list: {args.featured}")
    summary = build_static_skill_pages(records, args.output)
    print(f"Generated {summary['generated_count']} static skill pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
