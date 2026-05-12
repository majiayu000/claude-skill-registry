"""
Confluence Ingest Engine.

Pulls pages from Confluence spaces via REST API and stores them
as clean markdown files with YAML frontmatter in the raw/ directory.

Supports:
- Incremental sync (only pull changed pages since last sync)
- Space filtering (include/exclude lists)
- Parent-child hierarchy preservation
- Content cleaning (remove Confluence artifacts)
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional, Generator
from dataclasses import dataclass

from atlassian import Confluence
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
    labels: list[str]


class ConfluenceIngester:
    """Handles pulling data from Confluence and writing to raw/ directory."""

    def __init__(self, config: KBConfig, base_dir: Path):
        self.config = config
        self.base_dir = base_dir
        self.raw_dir = base_dir / config.raw_dir
        self.state_path = base_dir / ".ckb-sync-state.json"

        # Initialize Confluence client
        self.client = Confluence(
            url=config.confluence.url,
            username=config.confluence.email,
            password=config.confluence.api_token,
            cloud=True,
        )

    def get_spaces(self) -> list[dict]:
        """Get list of Confluence spaces based on config filters."""
        spaces = []
        start = 0
        limit = 50

        while True:
            result = self.client.get_all_spaces(
                start=start,
                limit=limit,
                expand="description.plain",
            )

            batch = result.get("results", [])
            if not batch:
                break

            for space in batch:
                space_key = space["key"]
                space_type = space.get("type", "global")
                space_status = space.get("status", "current")

                # Apply filters
                if self.config.spaces.include and space_key not in self.config.spaces.include:
                    continue
                if space_key in self.config.spaces.exclude:
                    continue
                if not self.config.spaces.include_archived and space_status == "archived":
                    continue
                if not self.config.spaces.include_personal and space_type == "personal":
                    continue

                spaces.append(space)

            start += limit
            if len(batch) < limit:
                break

        return spaces

    def get_pages_for_space(
        self, space_key: str, space_name: str
    ) -> Generator[PageInfo, None, None]:
        """Yield all pages from a space."""
        start = 0
        limit = 50

        while True:
            try:
                result = self.client.get_all_pages_from_space(
                    space=space_key,
                    start=start,
                    limit=limit,
                    status=None,
                    expand="body.storage,version,ancestors,metadata.labels",
                    content_type="page",
                )
            except Exception as e:
                console.print(f"  [yellow]Warning: Error fetching pages from {space_key}: {e}[/yellow]")
                break

            if not result:
                break

            for page in result:
                try:
                    # Extract body content
                    body_storage = page.get("body", {}).get("storage", {}).get("value", "")

                    # Convert HTML storage format to markdown
                    body_md = self._html_to_markdown(body_storage)

                    # Extract labels
                    labels_data = (
                        page.get("metadata", {})
                        .get("labels", {})
                        .get("results", [])
                    )
                    labels = [l.get("name", "") for l in labels_data if l.get("name")]

                    # Get parent info
                    ancestors = page.get("ancestors", [])
                    parent_id = ancestors[-1]["id"] if ancestors else None

                    version_info = page.get("version", {})

                    yield PageInfo(
                        id=page["id"],
                        title=page.get("title", "Untitled"),
                        space_key=space_key,
                        space_name=space_name,
                        status=page.get("status", "current"),
                        parent_id=parent_id,
                        author_id=version_info.get("by", {}).get("accountId"),
                        created_at=page.get("history", {}).get(
                            "createdDate",
                            version_info.get("when", ""),
                        ),
                        updated_at=version_info.get("when", ""),
                        version=version_info.get("number", 1),
                        body_markdown=body_md,
                        labels=labels,
                    )
                except Exception as e:
                    console.print(
                        f"  [yellow]Warning: Error processing page {page.get('id', '?')}: {e}[/yellow]"
                    )

            start += limit
            if len(result) < limit:
                break

            # Rate limiting courtesy
            time.sleep(0.2)

    def _html_to_markdown(self, html: str) -> str:
        """Convert Confluence storage format HTML to clean markdown."""
        if not html.strip():
            return ""

        try:
            from markdownify import markdownify
            md = markdownify(html, heading_style="ATX", strip=["script", "style"])
        except Exception:
            # Fallback: strip HTML tags crudely
            import re
            md = re.sub(r'<[^>]+>', '', html)

        return clean_confluence_markdown(md)

    def _page_to_filepath(self, page: PageInfo) -> Path:
        """Determine the file path for a page in raw/."""
        space_slug = slugify(page.space_key)
        page_slug = slugify(page.title)

        # Use page ID suffix to avoid collisions
        filename = f"{page_slug}--{page.id}.md"
        return self.raw_dir / space_slug / filename

    def _write_page(self, page: PageInfo) -> Path:
        """Write a page to the raw/ directory with frontmatter."""
        filepath = self._page_to_filepath(page)

        metadata = {
            "confluence_id": page.id,
            "title": page.title,
            "space_key": page.space_key,
            "space_name": page.space_name,
            "parent_id": page.parent_id,
            "status": page.status,
            "created_at": page.created_at,
            "updated_at": page.updated_at,
            "version": page.version,
            "labels": page.labels,
            "content_hash": content_hash(page.body_markdown),
            "ingested_at": now_iso(),
        }

        # Build the page content with title as H1
        content = f"# {page.title}\n\n{page.body_markdown}"

        write_md_file(filepath, content, metadata)
        return filepath

    def ingest(self, full_sync: bool = False) -> dict:
        """
        Run the ingest process.

        Args:
            full_sync: If True, re-download all pages. If False, only changed pages.

        Returns:
            Summary dict with counts of pages processed.
        """
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

        console.print(f"\n[bold blue]Ingesting Confluence spaces for {self.config.company_name}[/bold blue]")
        console.print(f"  Source: {self.config.confluence.url}")
        console.print(f"  Target: {self.raw_dir}\n")

        # Get spaces
        spaces = self.get_spaces()
        console.print(f"  Found [bold]{len(spaces)}[/bold] spaces to ingest\n")

        if not spaces:
            console.print("[yellow]No spaces matched the configured filters.[/yellow]")
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
                space_key = space["key"]
                space_name = space.get("name", space_key)
                progress.update(space_task, description=f"Space: {space_name}")

                page_count = 0
                for page in self.get_pages_for_space(space_key, space_name):
                    stats["pages_total"] += 1
                    page_count += 1

                    # Skip pages below content threshold
                    if len(page.body_markdown.strip()) < self.config.compile.min_content_length:
                        stats["pages_skipped"] += 1
                        continue

                    # Check if page has changed since last sync
                    existing = state["pages"].get(page.id, {})
                    new_hash = content_hash(page.body_markdown)

                    if not full_sync and existing.get("content_hash") == new_hash:
                        stats["pages_skipped"] += 1
                        continue

                    # Write the page
                    try:
                        filepath = self._write_page(page)

                        if page.id in state["pages"]:
                            stats["pages_updated"] += 1
                        else:
                            stats["pages_new"] += 1

                        state["pages"][page.id] = {
                            "title": page.title,
                            "space_key": space_key,
                            "content_hash": new_hash,
                            "version": page.version,
                            "filepath": str(filepath.relative_to(self.base_dir)),
                            "updated_at": page.updated_at,
                            "synced_at": now_iso(),
                        }
                    except Exception as e:
                        stats["errors"] += 1
                        console.print(f"  [red]Error writing page '{page.title}': {e}[/red]")

                stats["spaces_processed"] += 1
                progress.update(space_task, advance=1)
                console.print(f"  [dim]{space_name}: {page_count} pages[/dim]")

        # Save sync state
        state["last_sync"] = now_iso()
        save_sync_state(self.state_path, state)

        # Write space index file
        self._write_space_index(spaces, state)

        # Print summary
        self._print_summary(stats)

        return stats

    def _write_space_index(self, spaces: list[dict], state: dict) -> None:
        """Write a master index of all ingested spaces and pages."""
        index_path = self.raw_dir / "_index.md"
        lines = [
            f"# {self.config.company_name} - Confluence Knowledge Base\n",
            f"Last synced: {state.get('last_sync', 'never')}\n",
            f"Total pages: {len(state.get('pages', {}))}\n",
            "---\n",
            "## Spaces\n",
        ]

        for space in sorted(spaces, key=lambda s: s.get("name", "")):
            space_key = space["key"]
            space_name = space.get("name", space_key)
            page_count = sum(
                1 for p in state.get("pages", {}).values()
                if p.get("space_key") == space_key
            )
            lines.append(f"- **{space_name}** (`{space_key}`) - {page_count} pages")

        lines.append("\n## Pages by Space\n")
        pages_by_space: dict[str, list] = {}
        for page_id, info in state.get("pages", {}).items():
            sk = info.get("space_key", "unknown")
            pages_by_space.setdefault(sk, []).append(info)

        for sk in sorted(pages_by_space):
            pages = sorted(pages_by_space[sk], key=lambda p: p.get("title", ""))
            lines.append(f"\n### {sk}\n")
            for p in pages:
                rel_path = p.get("filepath", "")
                lines.append(f"- [{p.get('title', 'Untitled')}]({rel_path})")

        write_md_file(index_path, "\n".join(lines))

    def _print_summary(self, stats: dict) -> None:
        """Print a formatted summary table."""
        table = Table(title="\nIngest Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", justify="right", style="bold")

        table.add_row("Spaces processed", str(stats["spaces_processed"]))
        table.add_row("New pages", str(stats["pages_new"]))
        table.add_row("Updated pages", str(stats["pages_updated"]))
        table.add_row("Skipped (unchanged)", str(stats["pages_skipped"]))
        table.add_row("Total pages seen", str(stats["pages_total"]))
        table.add_row("Errors", str(stats["errors"]))

        console.print(table)
