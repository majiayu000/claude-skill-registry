"""
Q&A Interface for the Knowledge Base.

Uses the compiled wiki + search engine to answer questions.
The LLM reads relevant wiki articles and generates answers
grounded in the company's actual documentation.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

import anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .config import KBConfig
from .search import KBSearchEngine
from .utils import read_md_file, truncate_for_context, write_md_file, now_iso, slugify

console = Console()


RESEARCH_PROMPT = """You are a knowledge base assistant for {company}. {company_description}

You have access to a compiled knowledge base built from the company's Confluence documentation.
Answer the user's question using ONLY information from the provided knowledge base articles.

IMPORTANT RULES:
- Only use information present in the provided articles
- If the answer isn't in the articles, say so clearly
- Cite which articles/pages your information comes from
- Be specific - include names, dates, numbers when available
- If the question is ambiguous, note the different interpretations

Here is the master summary of the knowledge base:
{summaries}

Here are the most relevant articles for this question:
{relevant_articles}

User's question: {question}

Provide a thorough answer with citations to specific pages. Use markdown formatting."""


FOLLOWUP_PROMPT = """Based on the knowledge base for {company}, suggest 3-5 follow-up questions
the user might want to ask next, given their original question was:

"{question}"

And the answer covered:
{answer_summary}

List the follow-up questions, one per line, prefixed with "- "."""


class KBQueryEngine:
    """Handles Q&A against the compiled knowledge base."""

    def __init__(self, config: KBConfig, base_dir: Path):
        self.config = config
        self.base_dir = base_dir
        self.wiki_dir = base_dir / config.wiki_dir
        self.output_dir = base_dir / config.output_dir
        api_key = config.effective_anthropic_key or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.search = KBSearchEngine(self.wiki_dir)

        # Try to load cached index
        index_path = base_dir / ".ckb-search-index.json"
        if not self.search.load_index(index_path):
            console.print("  [dim]Building search index...[/dim]")
            count = self.search.build_index()
            self.search.save_index(index_path)
            console.print(f"  [dim]Indexed {count} documents[/dim]")

    def query(
        self,
        question: str,
        save_output: bool = True,
        show_sources: bool = True,
        max_context_articles: int = 8,
    ) -> str:
        """
        Answer a question using the knowledge base.

        Args:
            question: The user's question
            save_output: Whether to save the answer to output/
            show_sources: Whether to show which articles were used
            max_context_articles: Max number of articles to include in context

        Returns:
            The answer text
        """
        console.print(f"\n[bold blue]Researching:[/bold blue] {question}\n")

        # Step 1: Search for relevant articles
        results = self.search.search(question, limit=max_context_articles)

        if not results:
            msg = "No relevant articles found in the knowledge base for this question."
            console.print(f"[yellow]{msg}[/yellow]")
            return msg

        if show_sources:
            console.print("[dim]Relevant articles found:[/dim]")
            for r in results:
                console.print(f"  [dim]- {r.title} (score: {r.score})[/dim]")
            console.print()

        # Step 2: Load full content of relevant articles
        relevant_articles = []
        for result in results:
            full_path = self.wiki_dir / result.filepath
            _, content = read_md_file(full_path)
            if content:
                truncated = truncate_for_context(content, max_tokens=3000)
                relevant_articles.append(
                    f"### Article: {result.title}\n"
                    f"Category: {result.category} | Space: {result.space}\n\n"
                    f"{truncated}"
                )

        articles_text = "\n\n---\n\n".join(relevant_articles)

        # Step 3: Load the master summaries file for broader context
        summaries_path = self.wiki_dir / "_summaries.md"
        _, summaries = read_md_file(summaries_path)
        summaries = truncate_for_context(summaries, max_tokens=4000)

        # Step 4: Ask the LLM
        prompt = RESEARCH_PROMPT.format(
            company=self.config.company_name,
            company_description=self.config.company_description,
            summaries=summaries,
            relevant_articles=articles_text,
            question=question,
        )

        response = self.client.messages.create(
            model=self.config.compile.model,
            max_tokens=self.config.compile.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.content[0].text

        # Step 5: Display
        console.print(Panel(Markdown(answer), title="Answer", border_style="green"))

        # Step 6: Suggest follow-ups
        try:
            followup_prompt = FOLLOWUP_PROMPT.format(
                company=self.config.company_name,
                question=question,
                answer_summary=answer[:500],
            )
            followup_response = self.client.messages.create(
                model=self.config.compile.model,
                max_tokens=300,
                messages=[{"role": "user", "content": followup_prompt}],
            )
            followups = followup_response.content[0].text
            console.print(Panel(followups, title="Follow-up Questions", border_style="blue"))
        except Exception:
            pass

        # Step 7: Save output
        if save_output:
            self._save_output(question, answer, results)

        return answer

    def _save_output(self, question: str, answer: str, results: list) -> None:
        """Save the Q&A output to a markdown file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        slug = slugify(question[:60])
        filename = f"qa-{slug}.md"

        sources = "\n".join(
            f"- [{r.title}](../wiki/{r.filepath}) (relevance: {r.score})"
            for r in results
        )

        content = f"""# Q: {question}

*Asked on {now_iso()}*

## Answer

{answer}

## Sources

{sources}
"""
        write_md_file(self.output_dir / filename, content, {
            "type": "qa",
            "question": question,
            "created_at": now_iso(),
        })
        console.print(f"\n[dim]Answer saved to {self.output_dir / filename}[/dim]")


class InteractiveSession:
    """Interactive Q&A session with conversation history."""

    def __init__(self, query_engine: KBQueryEngine):
        self.engine = query_engine
        self.history: list[tuple[str, str]] = []

    def run(self) -> None:
        """Run an interactive Q&A session."""
        console.print(Panel(
            f"[bold]{self.engine.config.company_name} Knowledge Base Q&A[/bold]\n\n"
            "Ask questions about the company's documentation.\n"
            "Type 'quit' or 'exit' to end the session.\n"
            "Type 'history' to see previous Q&A.",
            title="Interactive Session",
            border_style="blue",
        ))

        while True:
            try:
                question = console.input("\n[bold cyan]Question:[/bold cyan] ").strip()

                if not question:
                    continue
                if question.lower() in ("quit", "exit", "q"):
                    console.print("[dim]Session ended.[/dim]")
                    break
                if question.lower() == "history":
                    self._show_history()
                    continue

                answer = self.engine.query(question)
                self.history.append((question, answer))

            except KeyboardInterrupt:
                console.print("\n[dim]Session ended.[/dim]")
                break
            except EOFError:
                break

    def _show_history(self) -> None:
        """Display conversation history."""
        if not self.history:
            console.print("[dim]No questions asked yet.[/dim]")
            return
        for i, (q, a) in enumerate(self.history, 1):
            console.print(f"\n[bold]Q{i}:[/bold] {q}")
            console.print(f"[dim]A: {a[:200]}...[/dim]")
