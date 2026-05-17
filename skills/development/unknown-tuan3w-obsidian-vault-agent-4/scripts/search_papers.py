#!/usr/bin/env python3
"""
Search academic papers via Semantic Scholar API (free, no auth needed).

Usage:
    python search_papers.py "query terms" [--limit N] [--year-from YYYY] [--year-to YYYY]
                                          [--min-citations N] [--fields extra,fields]

Output: JSON array of paper metadata to stdout.

API docs: https://api.semanticscholar.org/api-docs/graph
Rate limit: 100 requests/5min without API key.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.semanticscholar.org/graph/v1"

DEFAULT_FIELDS = ",".join([
    "title",
    "authors",
    "year",
    "abstract",
    "citationCount",
    "influentialCitationCount",
    "url",
    "externalIds",
    "publicationTypes",
    "journal",
    "fieldsOfStudy",
    "tldr",
])


def search_papers(query: str, limit: int = 20, year_range: str = None,
                  fields: str = DEFAULT_FIELDS, _retries: int = 0) -> list:
    """Search Semantic Scholar for papers matching query."""
    MAX_RETRIES = 2

    params = {
        "query": query,
        "limit": min(limit, 100),  # API max is 100
        "fields": fields,
    }
    if year_range:
        params["year"] = year_range

    url = f"{BASE_URL}/paper/search?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "ObsidianVaultBot/1.0 (knowledge-base-tool)",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 429 and _retries < MAX_RETRIES:
            wait = 30 * (_retries + 1)
            print(f"Rate limited. Waiting {wait}s... (retry {_retries + 1}/{MAX_RETRIES})", file=sys.stderr)
            time.sleep(wait)
            return search_papers(query, limit, year_range, fields, _retries + 1)
        elif e.code == 429:
            print(f"Rate limited after {MAX_RETRIES} retries. Try again later.", file=sys.stderr)
            return []
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    papers = data.get("data", [])
    return papers


def get_paper_by_id(paper_id: str, fields: str = DEFAULT_FIELDS) -> dict:
    """Get a single paper by Semantic Scholar ID, DOI, or arXiv ID."""
    url = f"{BASE_URL}/paper/{urllib.parse.quote(paper_id)}?fields={fields}"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "ObsidianVaultBot/1.0 (knowledge-base-tool)",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        return None


def get_recommendations(paper_id: str, limit: int = 10,
                        fields: str = DEFAULT_FIELDS) -> list:
    """Get recommended papers based on a seed paper."""
    params = {"fields": fields, "limit": min(limit, 100)}
    url = f"{BASE_URL}/recommendations/v1/papers/forpaper/{urllib.parse.quote(paper_id)}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "ObsidianVaultBot/1.0 (knowledge-base-tool)",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("recommendedPapers", [])
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Recommendation error: {e}", file=sys.stderr)
        return []


def format_paper(paper: dict) -> dict:
    """Clean up a paper result into a consistent format."""
    authors = paper.get("authors") or []
    author_names = [a.get("name", "") for a in authors if a.get("name")]

    external_ids = paper.get("externalIds") or {}
    doi = external_ids.get("DOI", "")
    arxiv_id = external_ids.get("ArXiv", "")

    tldr = paper.get("tldr")
    tldr_text = tldr.get("text", "") if isinstance(tldr, dict) else ""

    journal = paper.get("journal") or {}
    journal_name = journal.get("name", "") if isinstance(journal, dict) else ""

    return {
        "title": paper.get("title", "Untitled"),
        "authors": author_names,
        "year": paper.get("year"),
        "abstract": paper.get("abstract", ""),
        "tldr": tldr_text,
        "citation_count": paper.get("citationCount", 0),
        "influential_citations": paper.get("influentialCitationCount", 0),
        "url": paper.get("url", ""),
        "doi": doi,
        "arxiv_id": arxiv_id,
        "journal": journal_name,
        "fields_of_study": paper.get("fieldsOfStudy") or [],
        "publication_types": paper.get("publicationTypes") or [],
        "paper_id": paper.get("paperId", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Search academic papers via Semantic Scholar")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", "-n", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--year-from", type=int, help="Minimum publication year")
    parser.add_argument("--year-to", type=int, help="Maximum publication year")
    parser.add_argument("--min-citations", type=int, default=0, help="Minimum citation count filter")
    parser.add_argument("--recommend-from", help="Paper ID/DOI to get recommendations for (instead of search)")
    parser.add_argument("--paper-id", help="Get a specific paper by ID/DOI/arXiv ID")
    args = parser.parse_args()

    # Mode: get specific paper
    if args.paper_id:
        paper = get_paper_by_id(args.paper_id)
        if paper:
            print(json.dumps(format_paper(paper), indent=2, ensure_ascii=False))
        else:
            print("Paper not found", file=sys.stderr)
            sys.exit(1)
        return

    # Mode: get recommendations
    if args.recommend_from:
        print(f"Getting recommendations based on: {args.recommend_from}", file=sys.stderr)
        papers = get_recommendations(args.recommend_from, limit=args.limit)
        results = [format_paper(p) for p in papers if p]
        print(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"Found {len(results)} recommendations", file=sys.stderr)
        return

    # Mode: search
    year_range = None
    if args.year_from and args.year_to:
        year_range = f"{args.year_from}-{args.year_to}"
    elif args.year_from:
        year_range = f"{args.year_from}-"
    elif args.year_to:
        year_range = f"-{args.year_to}"

    print(f"Searching: '{args.query}'", file=sys.stderr)
    papers = search_papers(args.query, limit=args.limit, year_range=year_range)

    # Format and filter
    results = []
    for p in papers:
        formatted = format_paper(p)
        if formatted["citation_count"] >= args.min_citations:
            results.append(formatted)

    # Sort by citation count descending
    results.sort(key=lambda x: x["citation_count"], reverse=True)

    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Found {len(results)} papers (filtered from {len(papers)})", file=sys.stderr)


if __name__ == "__main__":
    main()
