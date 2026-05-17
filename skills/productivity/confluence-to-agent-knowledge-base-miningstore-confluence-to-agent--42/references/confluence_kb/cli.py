"""
CLI for confluence-kb.

Commands:
  ckb init          Initialize a new knowledge base config
  ckb ingest        Pull Confluence pages into raw/
  ckb compile       LLM compiles raw/ into wiki/
  ckb query         Ask questions against the wiki
  ckb search        Full-text search the wiki
  ckb lint          Health check the wiki
  ckb status        Show sync status
  ckb interactive   Start an interactive Q&A session
"""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import load_config, save_config, KBConfig, ConfluenceConfig, DEFAULT_CONFIG_NAME

console = Console()


def find_config(ctx_dir: str = ".") -> Path:
    """Find the config file, searching current dir and parents."""
    current = Path(ctx_dir).resolve()
    while current != current.parent:
        config_path = current / DEFAULT_CONFIG_NAME
        if config_path.exists():
            return config_path
        current = current.parent
    return Path(ctx_dir).resolve() / DEFAULT_CONFIG_NAME


def load_or_fail(ctx_dir: str = ".") -> tuple[KBConfig, Path]:
    """Load config or exit with helpful error."""
    config_path = find_config(ctx_dir)
    if not config_path.exists():
        console.print("[red]No ckb-config.yaml found. Run 'ckb init' first.[/red]")
        sys.exit(1)
    config = load_config(config_path)
    base_dir = config_path.parent
    return config, base_dir


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """confluence-kb: Turn Confluence spaces into LLM-powered knowledge bases."""
    pass


@cli.command()
@click.option("--company", prompt="Company name", help="Your company name")
@click.option("--url", prompt="Confluence URL", help="e.g. https://yourcompany.atlassian.net")
@click.option("--email", prompt="Confluence email", help="Email for API authentication")
@click.option("--dir", "directory", default=".", help="Directory to create the KB in")
def init(company: str, url: str, email: str, directory: str):
    """Initialize a new knowledge base configuration."""
    base_dir = Path(directory).resolve()
    config_path = base_dir / DEFAULT_CONFIG_NAME

    if config_path.exists():
        if not click.confirm(f"Config already exists at {config_path}. Overwrite?"):
            return

    config = KBConfig(
        company_name=company,
        company_description=f"{company} company knowledge base",
        confluence=ConfluenceConfig(
            url=url.rstrip("/"),
            email=email,
            api_token="${CONFLUENCE_API_TOKEN}",
        ),
    )
    save_config(config, config_path)

    # Create directory structure
    (base_dir / "raw").mkdir(exist_ok=True)
    (base_dir / "wiki").mkdir(exist_ok=True)
    (base_dir / "output").mkdir(exist_ok=True)

    # Create .gitignore
    gitignore = base_dir / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(
            "# confluence-kb\n"
            ".ckb-sync-state.json\n"
            ".ckb-search-index.json\n"
            "*.pyc\n"
            "__pycache__/\n"
            ".env\n"
        )

    # Create .env template
    env_template = base_dir / ".env.template"
    env_template.write_text(
        "# Copy to .env and fill in your values\n"
        "CONFLUENCE_API_TOKEN=your_confluence_api_token_here\n"
        "ANTHROPIC_API_KEY=your_anthropic_api_key_here\n"
    )

    console.print(Panel(
        f"[bold green]Knowledge base initialized![/bold green]\n\n"
        f"Config: {config_path}\n"
        f"Company: {company}\n"
        f"Confluence: {url}\n\n"
        f"[bold]Next steps:[/bold]\n"
        f"1. Copy .env.template to .env and add your API tokens\n"
        f"2. Edit {config_path} to configure space filters\n"
        f"3. Run 'ckb ingest' to pull Confluence content\n"
        f"4. Run 'ckb compile' to build the knowledge base\n"
        f"5. Run 'ckb query \"your question\"' to start asking questions",
        title="Setup Complete",
    ))


@cli.command()
@click.option("--full", is_flag=True, help="Force full sync (ignore cache)")
@click.option("--dir", "directory", default=".", help="KB directory")
def ingest(full: bool, directory: str):
    """Pull Confluence pages into the raw/ directory."""
    config, base_dir = load_or_fail(directory)

    from .ingest_v2 import ConfluenceIngesterV2
    ingester = ConfluenceIngesterV2(config, base_dir)
    stats = ingester.ingest(full_sync=full)

    total = stats["pages_new"] + stats["pages_updated"]
    if total > 0:
        console.print(f"\n[green]Ingested {total} pages. Run 'ckb compile' to update the wiki.[/green]")
    else:
        console.print("\n[dim]No changes detected. Wiki is up to date.[/dim]")


@cli.command()
@click.option("--fast", is_flag=True, help="Fast mode: heuristic categorization, no LLM calls")
@click.option("--dir", "directory", default=".", help="KB directory")
def compile(fast: bool, directory: str):
    """Compile raw pages into a structured knowledge base wiki."""
    config, base_dir = load_or_fail(directory)

    from .compile_kb import KBCompiler
    compiler = KBCompiler(config, base_dir)

    if fast:
        stats = compiler.compile_fast()
    else:
        stats = compiler.compile()

    console.print(f"\n[bold green]Compiled {stats['pages_processed']} pages into wiki/[/bold green]")
    console.print(f"  Concepts extracted: {stats['concepts_extracted']}")
    console.print(f"  Articles generated: {stats['articles_generated']}")


@cli.command()
@click.argument("question")
@click.option("--no-save", is_flag=True, help="Don't save answer to output/")
@click.option("--dir", "directory", default=".", help="KB directory")
def query(question: str, no_save: bool, directory: str):
    """Ask a question against the knowledge base."""
    config, base_dir = load_or_fail(directory)

    from .query import KBQueryEngine
    engine = KBQueryEngine(config, base_dir)
    engine.query(question, save_output=not no_save)


@cli.command()
@click.argument("terms")
@click.option("--limit", default=10, help="Max results to show")
@click.option("--dir", "directory", default=".", help="KB directory")
def search(terms: str, limit: int, directory: str):
    """Full-text search the knowledge base."""
    config, base_dir = load_or_fail(directory)

    from .search import KBSearchEngine
    wiki_dir = base_dir / config.wiki_dir
    engine = KBSearchEngine(wiki_dir)

    # Try loading cached index
    index_path = base_dir / ".ckb-search-index.json"
    if not engine.load_index(index_path):
        console.print("[dim]Building search index...[/dim]")
        count = engine.build_index()
        engine.save_index(index_path)
        console.print(f"[dim]Indexed {count} documents[/dim]\n")

    results = engine.search(terms, limit=limit)

    if not results:
        console.print(f"[yellow]No results found for '{terms}'[/yellow]")
        return

    table = Table(title=f"Search Results: '{terms}'")
    table.add_column("#", width=3)
    table.add_column("Title", width=40)
    table.add_column("Category", width=12)
    table.add_column("Score", width=8, justify="right")
    table.add_column("Snippet", width=50)

    for i, r in enumerate(results, 1):
        table.add_row(
            str(i),
            r.title[:40],
            r.category,
            f"{r.score:.3f}",
            r.snippet[:50] + "...",
        )

    console.print(table)


@cli.command()
@click.option("--no-llm", is_flag=True, help="Skip LLM-powered checks")
@click.option("--dir", "directory", default=".", help="KB directory")
def lint(no_llm: bool, directory: str):
    """Run health checks on the knowledge base."""
    config, base_dir = load_or_fail(directory)

    from .lint import KBLinter
    linter = KBLinter(config, base_dir)
    linter.lint(use_llm=not no_llm)


@cli.command()
@click.option("--dir", "directory", default=".", help="KB directory")
def interactive(directory: str):
    """Start an interactive Q&A session."""
    config, base_dir = load_or_fail(directory)

    from .query import KBQueryEngine, InteractiveSession
    engine = KBQueryEngine(config, base_dir)
    session = InteractiveSession(engine)
    session.run()


@cli.command()
@click.option("--dir", "directory", default=".", help="KB directory")
def status(directory: str):
    """Show the current status of the knowledge base."""
    config, base_dir = load_or_fail(directory)

    from .utils import load_sync_state

    console.print(Panel(
        f"[bold]{config.company_name} Knowledge Base[/bold]",
        border_style="blue",
    ))

    # Sync state
    state_path = base_dir / ".ckb-sync-state.json"
    state = load_sync_state(state_path)

    table = Table(title="Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold")

    table.add_row("Company", config.company_name)
    table.add_row("Confluence URL", config.confluence.url)
    table.add_row("Last sync", state.get("last_sync", "never"))
    table.add_row("Raw pages", str(len(state.get("pages", {}))))

    # Count wiki files
    wiki_dir = base_dir / config.wiki_dir
    wiki_count = sum(1 for _ in wiki_dir.rglob("*.md")) if wiki_dir.exists() else 0
    table.add_row("Wiki articles", str(wiki_count))

    # Count output files
    output_dir = base_dir / config.output_dir
    output_count = sum(1 for _ in output_dir.rglob("*.md")) if output_dir.exists() else 0
    table.add_row("Q&A outputs", str(output_count))

    # Space breakdown
    spaces: dict[str, int] = {}
    for page_info in state.get("pages", {}).values():
        sk = page_info.get("space_key", "?")
        spaces[sk] = spaces.get(sk, 0) + 1

    table.add_row("Spaces synced", str(len(spaces)))

    console.print(table)

    if spaces:
        space_table = Table(title="Pages by Space")
        space_table.add_column("Space Key", width=20)
        space_table.add_column("Pages", justify="right", width=8)

        for sk in sorted(spaces, key=lambda k: spaces[k], reverse=True):
            space_table.add_row(sk, str(spaces[sk]))

        console.print(space_table)


if __name__ == "__main__":
    cli()
