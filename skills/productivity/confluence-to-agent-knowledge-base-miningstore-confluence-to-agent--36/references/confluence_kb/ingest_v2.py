"""
Confluence Ingest Engine v2 - Direct REST API with OAuth2 support.

Uses Confluence REST API v2 directly instead of atlassian-python-api,
supporting both API token auth and OAuth2 bearer tokens.

This is the preferred ingest method for Confluence Cloud.
"""

from __future__ import annotations

import time
import requests
from pathlib import Path
from typing import Optional, Generator
from dataclasses import dataclass

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

from .config import KBConfig
from .utils import (
    slugify,
    clean_confluence_markdown,
    content_hash,
    now_iso,
    write_md_file,
    load_sync_state,
    save_sync_state,
)

console = Console()


@dataclass
class PageInfo:
    """Metadata about a Confluence page."""
    id: str
    title: str
    space_key: str
    space_name: str
    status: str
    parent_id: Optional[str]
    author_id: Optional[str]
    created_at: str
    updated_at: str
    version: int
    body_markdown: str
    labels: list


class ConfluenceV2Client:
    """Direct REST API v2 client for Confluence Cloud."""

    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_base = f"{self.base_url}/wiki/api/v2"
        self.v1_base = f"{self.base_url}/wiki/rest/api"
        self.session = requests.Session()

        # Try Bearer token first, fall back to basic auth
        if api_token.startswith("ey"):
            # Looks like a JWT/OAuth token
            self.session.headers["Authorization"] = f"Bearer {api_token}"
        else:
            # Standard API token - use basic auth
            self.session.auth = (email, api_token)

        self.session.headers["Accept"] = "application/json"

    def get_spaces(self, limit: int = 50) -> Generator[dict, None, None]:
        """Get all spaces, handling pagination."""
        url = f"{self.api_base}/spaces"
        params = {"limit": limit}

        while url:
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            for space in data.get("results", []):
                yield space

            # Handle pagination
            next_link = data.get("_links", {}).get("next")
            if next_link:
                url = f"{self.base_url}/wiki{next_link}" if next_link.startswith("/") else next_link
                params = {}  # Params are in the URL already
            else:
                break

    def get_pages_in_space(self, space_id: str, limit: int = 50) -> Generator[dict, None, None]:
        """Get all pages in a space with body content."""
        url = f"{self.api_base}/spaces/{space_id}/pages"
        params = {
            "limit": limit,
            "body-format": "atlas_doc_format",
        }

        while url:
            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                console.print(f"  [yellow]Warning: Failed to get pages for space {space_id}: {resp.status_code}[/yellow]")
                break

            data = resp.json()
            for page in data.get("results", []):
                yield page

            next_link = data.get("_links", {}).get("next")
            if next_link:
                url = f"{self.base_url}/wiki{next_link}" if next_link.startswith("/api") else next_link
                params = {}
            else:
                break

            time.sleep(0.15)  # Rate limiting

    def get_page_labels(self, page_id: str) -> list:
        """Get labels for a page."""
        try:
            url = f"{self.api_base}/pages/{page_id}/labels"
            resp = self.session.get(url)
            if resp.status_code == 200:
                return [l.get("name", "") for l in resp.json().get("results", [])]
        except Exception:
            pass
        return []


class ConfluenceIngesterV2:
    """Ingest from Confluence using REST API v2."""

    def __init__(self, config: KBConfig, base_dir: Path):
        self.config = config
        self.base_dir = base_dir
        self.raw_dir = base_dir / config.raw_dir
        self.state_path = base_dir / ".ckb-sync-state.json"
        self.client = ConfluenceV2Client(
            config.confluence.url,
            config.confluence.email,
            config.confluence.api_token,
        )

    def get_filtered_spaces(self) -> list[dict]:
        """Get spaces filtered by config."""
        spaces = []
        for space in self.client.get_spaces():
            space_key = space.get("key", "")
            space_type = space.get("type", "global")
            space_status = space.get("status", "current")

            if self.config.spaces.include and space_key not in self.config.spaces.include:
                continue
            if space_key in self.config.spaces.exclude:
                continue
            if not self.config.spaces.include_archived and space_status == "archived":
                continue
            if not self.config.spaces.include_personal and space_type == "personal":
                continue

            spaces.append(space)

        return spaces

    def _page_to_filepath(self, space_key: str, title: str, page_id: str) -> Path:
        """Determine file path for a page."""
        space_slug = slugify(space_key)
        page_slug = slugify(title)
        filename = f"{page_slug}--{page_id}.md"
        return self.raw_dir / space_slug / filename

    def ingest(self, full_sync: bool = False) -> dict:
        """Run the ingest process."""
        state = load_sync_state(self.state_path)
        if full_sync:
            state = {"last_sync": None, "pages": {}}

        stats = {
            "spaces_processed": 0,
            "pages_new": 0,
            "pages_updated": 0,
            "pages_skipped": 0,
            "pages_total": 0,
            "errors": 0,
        }

        console.print(f"\n[bold blue]Ingesting Confluence for {self.config.company_name}[/bold blue]")
        console.print(f"  Source: {self.config.confluence.url}")
        console.print(f"  Target: {self.raw_dir}\n")

        spaces = self.get_filtered_spaces()
        console.print(f"  Found [bold]{len(spaces)}[/bold] matching spaces\n")

        if not spaces:
            console.print("[yellow]No spaces matched filters.[/yellow]")
            return stats

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            space_task = progress.add_task("Spaces", total=len(spaces))

            for space in spaces:
                space_key = space.get("key", "")
                space_name = space.get("name", space_key)
                space_id = space.get("id", "")
                progress.update(space_task, description=f"Space: {space_name}")

                page_count = 0
                for page in self.client.get_pages_in_space(space_id):
                    stats["pages_total"] += 1
                    page_count += 1

                    page_id = str(page.get("id", ""))
                    title = page.get("title", "Untitled")
                    body = page.get("body", "")
                    status = page.get("status", "current")
                    parent_id = page.get("parentId")
                    version_info = page.get("version", {})
                    version = version_info.get("number", 1)
                    created_at = page.get("createdAt", "")
                    updated_at = version_info.get("createdAt", created_at)

                    # Clean up body content
                    body_clean = clean_confluence_markdown(body) if body else ""

                    # Skip near-empty pages
                    if len(body_clean.strip()) < self.config.compile.min_content_length:
                        stats["pages_skipped"] += 1
                        continue

                    # Check for changes
                    new_hash = content_hash(body_clean)
                    existing = state.get("pages", {}).get(page_id, {})
                    if not full_sync and existing.get("content_hash") == new_hash:
                        stats["pages_skipped"] += 1
                        continue

                    # Write page
                    try:
                        filepath = self._page_to_filepath(space_key, title, page_id)
                        metadata = {
                            "confluence_id": page_id,
                            "title": title,
                            "space_key": space_key,
                            "space_name": space_name,
                            "parent_id": str(parent_id) if parent_id else None,
                            "status": status,
                            "created_at": created_at,
                            "updated_at": updated_at,
                            "version": version,
                            "labels": [],  # Will fetch if needed
                            "content_hash": new_hash,
                            "ingested_at": now_iso(),
                        }

                        content = f"# {title}\n\n{body_clean}"
                        write_md_file(filepath, content, metadata)

                        if page_id in state.get("pages", {}):
                            stats["pages_updated"] += 1
                        else:
                            stats["pages_new"] += 1

                        state.setdefault("pages", {})[page_id] = {
                            "title": title,
                            "space_key": space_key,
                            "content_hash": new_hash,
                            "version": version,
                            "filepath": str(filepath.relative_to(self.base_dir)),
                            "updated_at": updated_at,
                            "synced_at": now_iso(),
                        }
                    except Exception as e:
                        stats["errors"] += 1
                        console.print(f"  [red]Error: {title}: {e}[/red]")

                stats["spaces_processed"] += 1
                progress.update(space_task, advance=1)
                console.print(f"  [dim]{space_name}: {page_count} pages[/dim]")

        # Save state
        state["last_sync"] = now_iso()
        save_sync_state(self.state_path, state)

        # Build index
        self._write_space_index(spaces, state)

        # Summary
        self._print_summary(stats)
        return stats

    def _write_space_index(self, spaces: list, state: dict) -> None:
        """Write master index of ingested content."""
        index_path = self.raw_dir / "_index.md"
        lines = [
            f"# {self.config.company_name} - Confluence Knowledge Base\n",
            f"Last synced: {state.get('last_sync', 'never')}\n",
            f"Total pages: {len(state.get('pages', {}))}\n",
            "---\n",
            "## Spaces\n",
        ]

        for space in sorted(spaces, key=lambda s: s.get("name", "")):
            sk = space.get("key", "")
            sn = space.get("name", sk)
            count = sum(1 for p in state.get("pages", {}).values() if p.get("space_key") == sk)
            lines.append(f"- **{sn}** (`{sk}`) - {count} pages")

        write_md_file(index_path, "\n".join(lines))

    def _print_summary(self, stats: dict) -> None:
        """Print formatted summary."""
        table = Table(title="\nIngest Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", justify="right", style="bold")

        table.add_row("Spaces processed", str(stats["spaces_processed"]))
        table.add_row("New pages", str(stats["pages_new"]))
        table.add_row("Updated pages", str(stats["pages_updated"]))
        table.add_row("Skipped", str(stats["pages_skipped"]))
        table.add_row("Total seen", str(stats["pages_total"]))
        table.add_row("Errors", str(stats["errors"]))

        console.print(table)
