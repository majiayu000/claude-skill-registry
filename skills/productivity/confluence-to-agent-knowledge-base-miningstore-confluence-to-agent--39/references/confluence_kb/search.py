"""
Local search engine for the knowledge base.

Provides full-text search over the compiled wiki using a simple
inverted index. No external dependencies required - just pure Python
with TF-IDF scoring.

Can be used:
1. Directly by users via `ckb search "query"`
2. By the LLM as a tool for answering complex questions
3. By the lint system to find related content
"""

from __future__ import annotations

import re
import math
import json
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

from .utils import read_md_file


@dataclass
class SearchResult:
    """A single search result."""
    filepath: str
    title: str
    score: float
    snippet: str
    category: str
    space: str


class KBSearchEngine:
    """Simple TF-IDF search engine over the wiki."""

    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir
        self.index: dict[str, dict[str, float]] = {}  # term -> {filepath: tf-idf}
        self.documents: dict[str, dict] = {}  # filepath -> metadata
        self.doc_lengths: dict[str, int] = {}
        self._built = False

    def build_index(self) -> int:
        """Build the search index from all wiki markdown files."""
        self.index = defaultdict(dict)
        self.documents = {}
        self.doc_lengths = {}
        doc_count = 0

        # First pass: collect all documents and term frequencies
        term_doc_freq: dict[str, int] = defaultdict(int)  # term -> num docs containing it
        doc_terms: dict[str, dict[str, int]] = {}  # filepath -> {term: count}

        for md_file in sorted(self.wiki_dir.rglob("*.md")):
            if md_file.name.startswith("_"):
                continue

            meta, content = read_md_file(md_file)
            if not content.strip():
                continue

            rel_path = str(md_file.relative_to(self.wiki_dir))

            self.documents[rel_path] = {
                "title": meta.get("title", md_file.stem.replace("-", " ").title()),
                "category": meta.get("category", ""),
                "space": meta.get("source_space", ""),
                "content": content,
            }

            # Tokenize
            tokens = self._tokenize(f"{meta.get('title', '')} {content}")
            self.doc_lengths[rel_path] = len(tokens)

            # Count terms
            term_counts: dict[str, int] = defaultdict(int)
            for token in tokens:
                term_counts[token] += 1

            doc_terms[rel_path] = dict(term_counts)

            # Update document frequencies
            for term in term_counts:
                term_doc_freq[term] += 1

            doc_count += 1

        # Second pass: compute TF-IDF
        for filepath, terms in doc_terms.items():
            doc_len = self.doc_lengths[filepath]
            for term, count in terms.items():
                tf = count / max(doc_len, 1)
                idf = math.log(doc_count / max(term_doc_freq[term], 1))
                self.index[term][filepath] = tf * idf

        self._built = True
        return doc_count

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search the index and return ranked results."""
        if not self._built:
            self.build_index()

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Score each document
        scores: dict[str, float] = defaultdict(float)
        for token in query_tokens:
            if token in self.index:
                for filepath, tfidf in self.index[token].items():
                    scores[filepath] += tfidf

        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for filepath, score in ranked:
            doc = self.documents.get(filepath, {})
            snippet = self._extract_snippet(doc.get("content", ""), query_tokens)
            results.append(SearchResult(
                filepath=filepath,
                title=doc.get("title", ""),
                score=round(score, 4),
                snippet=snippet,
                category=doc.get("category", ""),
                space=doc.get("space", ""),
            ))

        return results

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into lowercase terms."""
        # Remove markdown formatting
        text = re.sub(r'[#*_`\[\](){}|>~]', ' ', text)
        text = re.sub(r'https?://\S+', '', text)
        # Split on non-alphanumeric, keep meaningful tokens
        tokens = re.findall(r'[a-zA-Z0-9]+', text.lower())
        # Filter stopwords and very short tokens
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'this', 'that', 'these', 'those', 'it', 'its', 'we', 'our', 'you',
            'your', 'they', 'their', 'he', 'she', 'him', 'her', 'who', 'what',
            'which', 'when', 'where', 'how', 'not', 'no', 'if', 'then', 'else',
            'so', 'up', 'out', 'about', 'into', 'can', 'all', 'each', 'every',
            'some', 'any', 'most', 'more', 'other', 'than', 'just', 'also',
            'very', 'as', 'only', 'such', 'here', 'there', 'own', 'same',
        }
        return [t for t in tokens if len(t) > 2 and t not in stopwords]

    def _extract_snippet(self, content: str, query_tokens: list[str], max_len: int = 200) -> str:
        """Extract a relevant snippet from content around query terms."""
        content_lower = content.lower()
        best_pos = 0
        best_score = 0

        # Find the region with most query term matches
        window = 300
        for i in range(0, len(content_lower) - window, 50):
            chunk = content_lower[i:i + window]
            score = sum(1 for t in query_tokens if t in chunk)
            if score > best_score:
                best_score = score
                best_pos = i

        snippet = content[best_pos:best_pos + max_len].strip()
        # Clean up
        snippet = re.sub(r'\s+', ' ', snippet)
        if best_pos > 0:
            snippet = "..." + snippet
        if best_pos + max_len < len(content):
            snippet = snippet + "..."

        return snippet

    def save_index(self, path: Path) -> None:
        """Save the index to disk for fast loading."""
        data = {
            "index": {k: dict(v) for k, v in self.index.items()},
            "documents": {
                k: {key: val for key, val in v.items() if key != "content"}
                for k, v in self.documents.items()
            },
            "doc_lengths": self.doc_lengths,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f)

    def load_index(self, path: Path) -> bool:
        """Load a previously saved index. Returns True if successful."""
        if not path.exists():
            return False
        try:
            with open(path) as f:
                data = json.load(f)
            self.index = defaultdict(dict, {
                k: dict(v) for k, v in data.get("index", {}).items()
            })
            self.documents = data.get("documents", {})
            self.doc_lengths = data.get("doc_lengths", {})
            # We still need to load content for snippets
            for md_file in self.wiki_dir.rglob("*.md"):
                if md_file.name.startswith("_"):
                    continue
                rel_path = str(md_file.relative_to(self.wiki_dir))
                if rel_path in self.documents:
                    _, content = read_md_file(md_file)
                    self.documents[rel_path]["content"] = content
            self._built = True
            return True
        except Exception:
            return False
