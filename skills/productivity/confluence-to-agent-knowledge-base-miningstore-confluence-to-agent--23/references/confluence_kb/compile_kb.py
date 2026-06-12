"""
LLM Compilation Pipeline.

Takes raw Confluence markdown pages and compiles them into a structured
knowledge base wiki. The LLM:

1. Reads raw pages and their metadata
2. Categorizes content into topics
3. Generates summaries at multiple granularities
4. Extracts concepts and creates concept articles
5. Builds cross-references and backlinks
6. Maintains an index structure for efficient LLM navigation

The wiki/ directory is the "compiled" output - maintained entirely by LLMs.
"""

from __future__ import annotations

import os
import json
import time
from pathlib import Path
from typing import Optional

import anthropic
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import KBConfig
from .utils import (
    read_md_file,
    write_md_file,
    truncate_for_context,
    count_tokens,
    now_iso,
    slugify,
)

console = Console()


CATEGORIZE_PROMPT = """You are organizing a company knowledge base. Given the following page from {company}'s Confluence, categorize it into exactly ONE of these categories:

Categories: {categories}

Page title: {title}
Space: {space_name} ({space_key})
Labels: {labels}

Content (first 2000 chars):
{content_preview}

Respond with ONLY the category name, nothing else."""


SUMMARIZE_PROMPT = """You are building a knowledge base for {company}. Write a concise summary of this Confluence page.

Rules:
- 2-4 sentences maximum
- Capture the key information, decisions, or procedures
- Include specific names, numbers, and dates when present
- If it's a meeting note, focus on decisions and action items
- If it's a process doc, focus on the key steps
- Write in present tense

Page title: {title}
Space: {space_name}

Content:
{content}

Summary:"""


CONCEPT_EXTRACTION_PROMPT = """You are building a knowledge base for {company}. Analyze these page summaries and extract the KEY CONCEPTS that appear across multiple pages.

A concept is a recurring topic, system, process, team, project, tool, location, or entity that is referenced in multiple places and would benefit from having its own dedicated article.

Page summaries:
{summaries}

Return a JSON array of concepts, each with:
- "name": concept name (e.g. "Iowa Mining Site", "Foreman Monitoring", "Customer Onboarding")
- "description": one sentence explaining what this concept is
- "related_pages": list of page titles that reference this concept
- "category": which category it best fits in

Return ONLY valid JSON, no other text. Limit to the top 20 most important concepts."""


CONCEPT_ARTICLE_PROMPT = """You are writing a knowledge base article for {company} about: {concept_name}

Description: {concept_description}

Here are the relevant source pages that mention this concept:

{source_content}

Write a comprehensive knowledge base article that:
1. Starts with a clear definition/overview
2. Synthesizes information from all the source pages
3. Includes specific details (names, dates, numbers)
4. Notes any processes or procedures related to this concept
5. Ends with a "Related Topics" section listing other concepts it connects to

Write in a factual, encyclopedic tone. Use markdown formatting with headers.
Do not make up information - only use what's in the source pages.

Article:"""


SPACE_SUMMARY_PROMPT = """You are building a knowledge base for {company}. Write a summary of the "{space_name}" space based on these page summaries:

{summaries}

Write a 3-5 sentence overview of what this space covers, its key topics, and how it fits into the company. Then list the top 5-10 most important pages with one-line descriptions.

Format as markdown."""


class KBCompiler:
    """Compiles raw Confluence pages into a structured knowledge base."""

    def __init__(self, config: KBConfig, base_dir: Path):
        self.config = config
        self.base_dir = base_dir
        self.raw_dir = base_dir / config.raw_dir
        self.wiki_dir = base_dir / config.wiki_dir

        # Resolve API key: explicit config > ANTHROPIC_API_KEY > OAuth token
        api_key = config.effective_anthropic_key
        if not api_key:
            api_key = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        self.client = anthropic.Anthropic(api_key=api_key)

    def _llm(self, prompt: str, max_tokens: int = 2048, retries: int = 3) -> str:
        """Call the LLM with a prompt and retry on rate limits."""
        for attempt in range(retries):
            try:
                response = self.client.messages.create(
                    model=self.config.compile.model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text
            except anthropic.RateLimitError:
                wait = (attempt + 1) * 5
                console.print(f"  [dim]Rate limited, waiting {wait}s...[/dim]")
                time.sleep(wait)
            except Exception as e:
                if attempt == retries - 1:
                    raise
                time.sleep(2)
        raise RuntimeError("Max retries exceeded")

    def _load_raw_pages(self) -> list[tuple[dict, str]]:
        """Load all raw pages from disk. Returns list of (metadata, content)."""
        pages = []
        for md_file in sorted(self.raw_dir.rglob("*.md")):
            if md_file.name.startswith("_"):
                continue  # Skip index files
            meta, content = read_md_file(md_file)
            if meta and content.strip():
                meta["_filepath"] = str(md_file.relative_to(self.base_dir))
                pages.append((meta, content))
        return pages

    def compile(self) -> dict:
        """
        Run the full compilation pipeline.

        Steps:
        1. Load all raw pages
        2. Categorize each page
        3. Generate summaries
        4. Extract concepts
        5. Generate concept articles
        6. Build space summaries
        7. Build master index

        Returns:
            Summary stats dict.
        """
        stats = {
            "pages_processed": 0,
            "summaries_generated": 0,
            "concepts_extracted": 0,
            "articles_generated": 0,
        }

        console.print(f"\n[bold blue]Compiling knowledge base for {self.config.company_name}[/bold blue]")

        # Step 1: Load raw pages
        pages = self._load_raw_pages()
        console.print(f"  Loaded [bold]{len(pages)}[/bold] raw pages\n")

        if not pages:
            console.print("[yellow]No raw pages found. Run 'ckb ingest' first.[/yellow]")
            return stats

        # Step 2 & 3: Categorize and summarize each page
        page_data = []  # Will hold enriched page info
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Categorizing & summarizing pages...", total=len(pages))

            for meta, content in pages:
                title = meta.get("title", "Untitled")
                progress.update(task, description=f"Processing: {title[:50]}...")

                # Categorize
                category = self._categorize_page(meta, content)

                # Summarize
                summary = self._summarize_page(meta, content)

                page_data.append({
                    "meta": meta,
                    "content": content,
                    "category": category,
                    "summary": summary,
                })

                stats["pages_processed"] += 1
                stats["summaries_generated"] += 1
                progress.advance(task)

        # Write categorized summaries to wiki
        self._write_categorized_pages(page_data)

        # Step 4: Extract concepts (if enabled)
        concepts = []
        if self.config.compile.generate_concepts:
            console.print("\n  [bold]Extracting cross-cutting concepts...[/bold]")
            concepts = self._extract_concepts(page_data)
            stats["concepts_extracted"] = len(concepts)
            console.print(f"  Found [bold]{len(concepts)}[/bold] concepts\n")

            # Step 5: Generate concept articles
            if concepts:
                self._generate_concept_articles(concepts, page_data)
                stats["articles_generated"] = len(concepts)

        # Step 6: Build space summaries
        self._build_space_summaries(page_data)

        # Step 7: Build master index
        self._build_master_index(page_data, concepts)

        console.print(f"\n[bold green]Compilation complete![/bold green]")
        console.print(f"  Wiki directory: {self.wiki_dir}")
        return stats

    def _categorize_page(self, meta: dict, content: str) -> str:
        """Use LLM to categorize a page."""
        try:
            prompt = CATEGORIZE_PROMPT.format(
                company=self.config.company_name,
                categories=", ".join(self.config.compile.categories),
                title=meta.get("title", "Untitled"),
                space_name=meta.get("space_name", ""),
                space_key=meta.get("space_key", ""),
                labels=", ".join(meta.get("labels", [])),
                content_preview=content[:2000],
            )
            category = self._llm(prompt, max_tokens=50).strip().lower()

            # Validate against known categories
            valid = [c.lower() for c in self.config.compile.categories]
            if category not in valid:
                category = "general"
            return category
        except Exception as e:
            console.print(f"  [yellow]Categorization failed for '{meta.get('title')}': {e}[/yellow]")
            return "general"

    def _summarize_page(self, meta: dict, content: str) -> str:
        """Use LLM to generate a page summary."""
        try:
            truncated = truncate_for_context(content, max_tokens=6000)
            prompt = SUMMARIZE_PROMPT.format(
                company=self.config.company_name,
                title=meta.get("title", "Untitled"),
                space_name=meta.get("space_name", ""),
                content=truncated,
            )
            return self._llm(prompt, max_tokens=300).strip()
        except Exception as e:
            console.print(f"  [yellow]Summary failed for '{meta.get('title')}': {e}[/yellow]")
            return f"Page about: {meta.get('title', 'unknown topic')}"

    def _write_categorized_pages(self, page_data: list[dict]) -> None:
        """Write page summaries organized by category."""
        by_category: dict[str, list] = {}
        for pd in page_data:
            cat = pd["category"]
            by_category.setdefault(cat, []).append(pd)

        for category, items in by_category.items():
            cat_dir = self.wiki_dir / category
            cat_dir.mkdir(parents=True, exist_ok=True)

            # Write category index
            lines = [f"# {category.title()}\n"]
            lines.append(f"*{len(items)} pages in this category*\n")

            for item in sorted(items, key=lambda x: x["meta"].get("title", "")):
                title = item["meta"].get("title", "Untitled")
                slug = slugify(title)
                space = item["meta"].get("space_name", "")
                lines.append(f"## [{title}]({slug}.md)")
                lines.append(f"*Space: {space}*\n")
                lines.append(f"{item['summary']}\n")

            write_md_file(cat_dir / "_index.md", "\n".join(lines))

            # Write individual page summaries with backlinks
            for item in items:
                title = item["meta"].get("title", "Untitled")
                slug = slugify(title)
                page_meta = {
                    "title": title,
                    "category": category,
                    "source_space": item["meta"].get("space_key", ""),
                    "source_page_id": item["meta"].get("confluence_id", ""),
                    "compiled_at": now_iso(),
                }
                page_content = f"# {title}\n\n"
                page_content += f"**Category:** {category} | "
                page_content += f"**Space:** {item['meta'].get('space_name', '')} | "
                page_content += f"**Status:** {item['meta'].get('status', 'current')}\n\n"
                page_content += f"## Summary\n\n{item['summary']}\n\n"
                page_content += f"## Source Content\n\n{item['content']}\n"

                write_md_file(cat_dir / f"{slug}.md", page_content, page_meta)

    def _extract_concepts(self, page_data: list[dict]) -> list[dict]:
        """Extract cross-cutting concepts from all page summaries."""
        # Build a summary block for the LLM
        summary_lines = []
        for pd in page_data:
            title = pd["meta"].get("title", "Untitled")
            summary_lines.append(f"- **{title}** ({pd['category']}): {pd['summary']}")

        summaries_text = "\n".join(summary_lines)
        # Truncate if too long
        summaries_text = truncate_for_context(summaries_text, max_tokens=12000)

        prompt = CONCEPT_EXTRACTION_PROMPT.format(
            company=self.config.company_name,
            summaries=summaries_text,
        )

        try:
            result = self._llm(prompt, max_tokens=4096)
            # Parse JSON from response
            # Handle potential markdown code blocks
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                result = result.split("```")[1].split("```")[0]

            concepts = json.loads(result.strip())
            return concepts if isinstance(concepts, list) else []
        except Exception as e:
            console.print(f"  [yellow]Concept extraction failed: {e}[/yellow]")
            return []

    def _generate_concept_articles(self, concepts: list[dict], page_data: list[dict]) -> None:
        """Generate wiki articles for each extracted concept."""
        concepts_dir = self.wiki_dir / "concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating concept articles...", total=len(concepts))

            for concept in concepts:
                name = concept.get("name", "Unknown")
                progress.update(task, description=f"Writing: {name[:40]}...")

                # Find related source pages
                related_titles = concept.get("related_pages", [])
                source_content = []
                for pd in page_data:
                    title = pd["meta"].get("title", "")
                    if title in related_titles or any(
                        kw.lower() in title.lower()
                        for kw in name.split()
                        if len(kw) > 3
                    ):
                        source_content.append(
                            f"### From: {title}\n{truncate_for_context(pd['content'], 3000)}"
                        )

                if not source_content:
                    progress.advance(task)
                    continue

                source_text = "\n\n---\n\n".join(source_content[:5])  # Limit to 5 sources

                try:
                    prompt = CONCEPT_ARTICLE_PROMPT.format(
                        company=self.config.company_name,
                        concept_name=name,
                        concept_description=concept.get("description", ""),
                        source_content=truncate_for_context(source_text, 10000),
                    )
                    article = self._llm(prompt, max_tokens=self.config.compile.max_tokens)

                    slug = slugify(name)
                    article_meta = {
                        "title": name,
                        "type": "concept",
                        "category": concept.get("category", "general"),
                        "related_pages": related_titles,
                        "compiled_at": now_iso(),
                    }
                    write_md_file(
                        concepts_dir / f"{slug}.md",
                        article,
                        article_meta,
                    )
                except Exception as e:
                    console.print(f"  [yellow]Failed to generate article for '{name}': {e}[/yellow]")

                progress.advance(task)

        # Write concepts index
        lines = ["# Concepts Index\n"]
        lines.append(f"*{len(concepts)} concepts extracted from the knowledge base*\n")
        for concept in sorted(concepts, key=lambda c: c.get("name", "")):
            name = concept.get("name", "")
            desc = concept.get("description", "")
            slug = slugify(name)
            lines.append(f"- **[{name}]({slug}.md)**: {desc}")

        write_md_file(concepts_dir / "_index.md", "\n".join(lines))

    def _build_space_summaries(self, page_data: list[dict]) -> None:
        """Generate a summary for each Confluence space."""
        spaces_dir = self.wiki_dir / "spaces"
        spaces_dir.mkdir(parents=True, exist_ok=True)

        by_space: dict[str, list] = {}
        for pd in page_data:
            sk = pd["meta"].get("space_key", "unknown")
            by_space.setdefault(sk, []).append(pd)

        for space_key, items in by_space.items():
            space_name = items[0]["meta"].get("space_name", space_key)
            summaries = "\n".join(
                f"- **{pd['meta'].get('title', '?')}**: {pd['summary']}"
                for pd in items
            )
            summaries = truncate_for_context(summaries, 8000)

            try:
                prompt = SPACE_SUMMARY_PROMPT.format(
                    company=self.config.company_name,
                    space_name=space_name,
                    summaries=summaries,
                )
                summary = self._llm(prompt, max_tokens=1024)
            except Exception:
                summary = f"# {space_name}\n\n{len(items)} pages in this space."

            slug = slugify(space_key)
            write_md_file(
                spaces_dir / f"{slug}.md",
                summary,
                {"space_key": space_key, "space_name": space_name, "page_count": len(items)},
            )

    def _build_master_index(self, page_data: list[dict], concepts: list[dict]) -> None:
        """Build the master index file for the wiki."""
        lines = [
            f"# {self.config.company_name} Knowledge Base\n",
            f"*Auto-compiled from Confluence on {now_iso()}*\n",
            f"*{len(page_data)} pages across {len(set(pd['meta'].get('space_key', '') for pd in page_data))} spaces*\n",
            "---\n",
        ]

        # Categories overview
        by_cat: dict[str, int] = {}
        for pd in page_data:
            cat = pd["category"]
            by_cat[cat] = by_cat.get(cat, 0) + 1

        lines.append("## Browse by Category\n")
        for cat in sorted(by_cat):
            lines.append(f"- [{cat.title()}]({cat}/_index.md) ({by_cat[cat]} pages)")

        # Spaces overview
        by_space: dict[str, str] = {}
        for pd in page_data:
            sk = pd["meta"].get("space_key", "")
            sn = pd["meta"].get("space_name", sk)
            by_space[sk] = sn

        lines.append("\n## Browse by Space\n")
        for sk in sorted(by_space):
            slug = slugify(sk)
            lines.append(f"- [{by_space[sk]}](spaces/{slug}.md)")

        # Concepts
        if concepts:
            lines.append(f"\n## Key Concepts ({len(concepts)})\n")
            for c in sorted(concepts, key=lambda x: x.get("name", "")):
                name = c.get("name", "")
                slug = slugify(name)
                lines.append(f"- [{name}](concepts/{slug}.md): {c.get('description', '')}")

        # All pages alphabetical
        lines.append("\n## All Pages (A-Z)\n")
        sorted_pages = sorted(page_data, key=lambda pd: pd["meta"].get("title", "").lower())
        for pd in sorted_pages:
            title = pd["meta"].get("title", "Untitled")
            cat = pd["category"]
            slug = slugify(title)
            lines.append(f"- [{title}]({cat}/{slug}.md) *({pd['meta'].get('space_name', '')})*")

        write_md_file(self.wiki_dir / "_index.md", "\n".join(lines))

        # Also write a compact summaries file for LLM context loading
        summary_lines = [
            f"# {self.config.company_name} - Page Summaries\n",
            "Use this file to quickly understand what's in the knowledge base.\n",
        ]
        for pd in sorted_pages:
            title = pd["meta"].get("title", "Untitled")
            cat = pd["category"]
            summary_lines.append(f"**{title}** [{cat}]: {pd['summary']}")

        write_md_file(self.wiki_dir / "_summaries.md", "\n".join(summary_lines))

    # ---- Fast compile mode (no LLM calls) ----

    def compile_fast(self) -> dict:
        """
        Fast compilation without LLM calls.

        Uses heuristic categorization (based on space key mapping)
        and extracts first-paragraph summaries instead of LLM summaries.
        Good for initial setup and testing. Run `ckb compile` with API key
        for the full LLM-enhanced compilation.
        """
        stats = {
            "pages_processed": 0,
            "summaries_generated": 0,
            "concepts_extracted": 0,
            "articles_generated": 0,
        }

        console.print(f"\n[bold blue]Fast-compiling KB for {self.config.company_name}[/bold blue]")
        console.print("[dim](heuristic mode - no LLM calls)[/dim]\n")

        pages = self._load_raw_pages()
        console.print(f"  Loaded [bold]{len(pages)}[/bold] raw pages\n")

        if not pages:
            console.print("[yellow]No raw pages found. Run 'ckb ingest' first.[/yellow]")
            return stats

        # Space-to-category mapping for MiningStore (and sensible defaults)
        # Populated dynamically during skill setup based on the user's Confluence spaces.
        # Claude fills this dict mapping space keys to categories during Phase 4.
        space_category_map = {
        }

        page_data = []
        for meta, content in pages:
            title = meta.get("title", "Untitled")
            space_key = meta.get("space_key", "")

            # Heuristic categorization
            category = space_category_map.get(space_key, "general")
            # Title-based overrides
            title_lower = title.lower()
            if any(w in title_lower for w in ["meeting", "standup", "stand-up", "stand up", "weekly", "daily"]):
                category = "meetings"
            elif any(w in title_lower for w in ["onboard", "training", "new hire", "orientation"]):
                category = "onboarding"

            # Extract first-paragraph summary
            summary = self._extract_summary_heuristic(content, title)

            page_data.append({
                "meta": meta,
                "content": content,
                "category": category,
                "summary": summary,
            })
            stats["pages_processed"] += 1
            stats["summaries_generated"] += 1

        console.print(f"  Categorized {len(page_data)} pages")

        # Write categorized pages
        self._write_categorized_pages(page_data)

        # Build space summaries (heuristic)
        self._build_space_summaries_fast(page_data)

        # Build master index
        self._build_master_index(page_data, [])

        console.print(f"\n[bold green]Fast compilation complete![/bold green]")
        console.print(f"  Wiki directory: {self.wiki_dir}")
        console.print(f"  Run 'ckb compile' with ANTHROPIC_API_KEY for LLM-enhanced compilation")
        return stats

    def _extract_summary_heuristic(self, content: str, title: str) -> str:
        """Extract a summary from content without LLM."""
        import re
        # Remove the H1 title line
        lines = content.strip().split("\n")
        body_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# ") and title.lower() in stripped.lower():
                continue
            if stripped.startswith("---"):
                continue
            if stripped:
                body_lines.append(stripped)

        if not body_lines:
            return f"Page about: {title}"

        # Get first meaningful paragraph (skip headers, tables, images)
        paragraph = []
        for line in body_lines[:10]:
            if line.startswith("#") or line.startswith("|") or line.startswith("!"):
                if paragraph:
                    break
                continue
            # Strip markdown formatting
            clean = re.sub(r'[*_`\[\]()]', '', line).strip()
            if clean and len(clean) > 10:
                paragraph.append(clean)
                if len(" ".join(paragraph)) > 200:
                    break

        if paragraph:
            summary = " ".join(paragraph)[:300]
            if len(summary) == 300:
                summary = summary.rsplit(" ", 1)[0] + "..."
            return summary

        return f"Documentation page about: {title}"

    def _build_space_summaries_fast(self, page_data: list[dict]) -> None:
        """Build space summaries without LLM."""
        spaces_dir = self.wiki_dir / "spaces"
        spaces_dir.mkdir(parents=True, exist_ok=True)

        by_space: dict[str, list] = {}
        for pd in page_data:
            sk = pd["meta"].get("space_key", "unknown")
            by_space.setdefault(sk, []).append(pd)

        for space_key, items in by_space.items():
            space_name = items[0]["meta"].get("space_name", space_key)
            lines = [f"# {space_name}\n"]
            lines.append(f"*{len(items)} pages | Space key: {space_key}*\n")
            lines.append("## Pages\n")

            for pd in sorted(items, key=lambda x: x["meta"].get("title", "")):
                title = pd["meta"].get("title", "Untitled")
                lines.append(f"- **{title}**: {pd['summary'][:100]}")

            slug = slugify(space_key)
            write_md_file(
                spaces_dir / f"{slug}.md",
                "\n".join(lines),
                {"space_key": space_key, "space_name": space_name, "page_count": len(items)},
            )
