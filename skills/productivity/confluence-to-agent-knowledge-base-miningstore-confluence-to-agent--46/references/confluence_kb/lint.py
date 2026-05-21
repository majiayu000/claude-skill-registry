"""
Knowledge Base Linting & Health Checks.

Runs various quality checks over the compiled wiki:
- Finds orphaned pages (no backlinks)
- Detects stale content
- Checks for inconsistencies across pages
- Suggests missing content
- Validates cross-references
- Suggests new concepts to extract
"""

from __future__ import annotations

import os
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

import anthropic
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .config import KBConfig
from .utils import read_md_file, truncate_for_context, now_iso, write_md_file

console = Console()


@dataclass
class LintIssue:
    severity: str  # "info", "warning", "error"
    category: str
    message: str
    filepath: str = ""


HEALTH_CHECK_PROMPT = """You are auditing a company knowledge base for {company}. Review these page summaries and identify:

1. INCONSISTENCIES: Places where different pages contradict each other
2. GAPS: Important topics that seem to be missing or poorly covered
3. STALE CONTENT: Pages that reference outdated information
4. CONNECTIONS: Interesting connections between topics that should be linked
5. SUGGESTIONS: New articles or concepts that would improve the knowledge base

Page summaries:
{summaries}

Provide your findings as a structured report with sections for each category above.
Be specific - cite page titles and explain each finding."""


class KBLinter:
    """Runs health checks and quality audits on the knowledge base."""

    def __init__(self, config: KBConfig, base_dir: Path):
        self.config = config
        self.base_dir = base_dir
        self.wiki_dir = base_dir / config.wiki_dir
        self.output_dir = base_dir / config.output_dir
        api_key = config.effective_anthropic_key or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        self.client = anthropic.Anthropic(api_key=api_key)

    def lint(self, use_llm: bool = True) -> list[LintIssue]:
        """Run all lint checks."""
        issues: list[LintIssue] = []

        console.print(f"\n[bold blue]Running health checks on {self.config.company_name} KB[/bold blue]\n")

        # Structural checks (no LLM needed)
        issues.extend(self._check_empty_pages())
        issues.extend(self._check_orphaned_pages())
        issues.extend(self._check_broken_links())
        issues.extend(self._check_category_balance())

        # LLM-powered checks
        if use_llm:
            issues.extend(self._llm_health_check())

        # Display results
        self._display_issues(issues)

        # Save report
        self._save_report(issues)

        return issues

    def _check_empty_pages(self) -> list[LintIssue]:
        """Find pages with very little content."""
        issues = []
        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name.startswith("_"):
                continue
            meta, content = read_md_file(md_file)
            if len(content.strip()) < 100:
                issues.append(LintIssue(
                    severity="warning",
                    category="empty_pages",
                    message=f"Page has very little content ({len(content)} chars)",
                    filepath=str(md_file.relative_to(self.wiki_dir)),
                ))
        return issues

    def _check_orphaned_pages(self) -> list[LintIssue]:
        """Find pages that aren't referenced by any index or other page."""
        issues = []
        all_files = set()
        referenced_files = set()

        for md_file in self.wiki_dir.rglob("*.md"):
            rel = str(md_file.relative_to(self.wiki_dir))
            if not md_file.name.startswith("_"):
                all_files.add(rel)

            # Scan content for links
            _, content = read_md_file(md_file)
            import re
            links = re.findall(r'\[([^\]]*)\]\(([^)]+\.md)\)', content)
            for _, link_path in links:
                referenced_files.add(link_path)

        orphaned = all_files - referenced_files
        for filepath in sorted(orphaned):
            issues.append(LintIssue(
                severity="info",
                category="orphaned_pages",
                message="Page is not linked from any other page or index",
                filepath=filepath,
            ))
        return issues

    def _check_broken_links(self) -> list[LintIssue]:
        """Find internal links that point to non-existent files."""
        issues = []
        import re

        for md_file in self.wiki_dir.rglob("*.md"):
            _, content = read_md_file(md_file)
            links = re.findall(r'\[([^\]]*)\]\(([^)]+\.md)\)', content)

            for link_text, link_path in links:
                if link_path.startswith("http"):
                    continue
                # Resolve relative to the file's directory
                target = md_file.parent / link_path
                if not target.exists():
                    issues.append(LintIssue(
                        severity="warning",
                        category="broken_links",
                        message=f"Broken link to '{link_path}' (text: '{link_text}')",
                        filepath=str(md_file.relative_to(self.wiki_dir)),
                    ))
        return issues

    def _check_category_balance(self) -> list[LintIssue]:
        """Check if categories are reasonably balanced."""
        issues = []
        by_category: dict[str, int] = defaultdict(int)

        for md_file in self.wiki_dir.rglob("*.md"):
            if md_file.name.startswith("_"):
                continue
            meta, _ = read_md_file(md_file)
            cat = meta.get("category", "unknown")
            by_category[cat] += 1

        if not by_category:
            return issues

        avg = sum(by_category.values()) / len(by_category)
        for cat, count in by_category.items():
            if count > avg * 3:
                issues.append(LintIssue(
                    severity="info",
                    category="balance",
                    message=f"Category '{cat}' has {count} pages (avg is {avg:.0f}). Consider subcategories.",
                ))
            elif count == 1:
                issues.append(LintIssue(
                    severity="info",
                    category="balance",
                    message=f"Category '{cat}' has only 1 page. Consider merging with another category.",
                ))

        return issues

    def _llm_health_check(self) -> list[LintIssue]:
        """Use LLM to find deeper quality issues."""
        issues = []

        # Load summaries
        summaries_path = self.wiki_dir / "_summaries.md"
        _, summaries = read_md_file(summaries_path)

        if not summaries:
            return issues

        summaries = truncate_for_context(summaries, max_tokens=10000)

        try:
            prompt = HEALTH_CHECK_PROMPT.format(
                company=self.config.company_name,
                summaries=summaries,
            )
            response = self.client.messages.create(
                model=self.config.compile.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            report = response.content[0].text

            # Parse into issues (rough extraction)
            issues.append(LintIssue(
                severity="info",
                category="llm_audit",
                message=report,
            ))
        except Exception as e:
            console.print(f"  [yellow]LLM health check failed: {e}[/yellow]")

        return issues

    def _display_issues(self, issues: list[LintIssue]) -> None:
        """Display lint issues in a formatted table."""
        if not issues:
            console.print("[green]No issues found! Knowledge base is healthy.[/green]")
            return

        # Count by severity
        counts = defaultdict(int)
        for issue in issues:
            counts[issue.severity] += 1

        console.print(f"\n  Found {len(issues)} issues: "
                       f"[red]{counts.get('error', 0)} errors[/red], "
                       f"[yellow]{counts.get('warning', 0)} warnings[/yellow], "
                       f"[blue]{counts.get('info', 0)} info[/blue]\n")

        # Show structural issues in a table
        structural = [i for i in issues if i.category != "llm_audit"]
        if structural:
            table = Table(title="Structural Issues")
            table.add_column("Severity", width=8)
            table.add_column("Category", width=16)
            table.add_column("File", width=40)
            table.add_column("Issue", width=50)

            for issue in structural[:20]:  # Limit display
                style = {"error": "red", "warning": "yellow", "info": "blue"}.get(
                    issue.severity, "white"
                )
                table.add_row(
                    issue.severity,
                    issue.category,
                    issue.filepath[:40],
                    issue.message[:50],
                    style=style,
                )
            console.print(table)

        # Show LLM audit
        llm_issues = [i for i in issues if i.category == "llm_audit"]
        if llm_issues:
            console.print(Panel(
                llm_issues[0].message,
                title="LLM Audit Report",
                border_style="blue",
            ))

    def _save_report(self, issues: list[LintIssue]) -> None:
        """Save the lint report to output/."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        report_path = self.output_dir / f"lint-report-{now_iso()[:10]}.md"

        lines = [
            f"# Knowledge Base Health Report\n",
            f"*Generated: {now_iso()}*\n",
            f"*Company: {self.config.company_name}*\n",
            f"\nTotal issues: {len(issues)}\n",
        ]

        by_category: dict[str, list] = defaultdict(list)
        for issue in issues:
            by_category[issue.category].append(issue)

        for cat, cat_issues in sorted(by_category.items()):
            lines.append(f"\n## {cat.replace('_', ' ').title()}\n")
            for issue in cat_issues:
                prefix = {"error": "!!!", "warning": "!!", "info": "!"}.get(issue.severity, "")
                if issue.filepath:
                    lines.append(f"- {prefix} `{issue.filepath}`: {issue.message}")
                else:
                    lines.append(f"- {prefix} {issue.message}")

        write_md_file(report_path, "\n".join(lines))
        console.print(f"\n[dim]Report saved to {report_path}[/dim]")
