#!/usr/bin/env python3
# /// script
# dependencies = ["networkx>=3.0"]
# requires-python = ">=3.10"
# ///
"""
Analyze Obsidian vault wikilink structure as a directed graph.

Parses all markdown files, extracts [[wikilinks]], builds a NetworkX
directed graph, and computes structural metrics.

Usage:
    uv run analyze_vault_graph.py <vault_root> [--output <path>] [--top N]

Output: JSON with graph metrics, top nodes, orphans, bridges, clusters.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

import networkx as nx


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+?)(?:\|[^\]]*?)?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
TYPE_PATTERN = re.compile(r"^type:\s*(.+)$", re.MULTILINE)
STATUS_PATTERN = re.compile(r"^processing_status:\s*(.+)$", re.MULTILINE)
TAG_LINE_PATTERN = re.compile(r"🏷️Tags.*?$", re.MULTILINE)
TAG_PATTERN = re.compile(r"#([\w-]+)")

# Directories to skip when scanning
SKIP_DIRS = {
    ".obsidian", ".claude", ".git", "templates", "node_modules",
    "claude-scientific-skills", ".book-work",
}


def resolve_note_name(raw_link: str) -> str:
    """Normalize a wikilink target to a canonical short name."""
    # Strip any path prefix — Obsidian resolves by short name
    name = raw_link.strip()
    if "/" in name:
        name = name.rsplit("/", 1)[-1]
    # Strip .md extension if present
    if name.lower().endswith(".md"):
        name = name[:-3]
    return name


def extract_short_name(filepath: str, vault_root: str) -> str:
    """Derive the short note name from a file path (filename without .md)."""
    basename = os.path.basename(filepath)
    if basename.lower().endswith(".md"):
        basename = basename[:-3]
    return basename


def parse_note(filepath: str):
    """Parse a single markdown note. Returns (short_name, metadata, links)."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError:
        return None

    # Extract frontmatter metadata
    note_type = ""
    processing_status = ""
    fm_match = FRONTMATTER_PATTERN.match(content)
    if fm_match:
        fm_text = fm_match.group(1)
        type_match = TYPE_PATTERN.search(fm_text)
        if type_match:
            note_type = type_match.group(1).strip()
        status_match = STATUS_PATTERN.search(fm_text)
        if status_match:
            processing_status = status_match.group(1).strip()

    # Extract inline tags
    tags = set()
    tag_line_match = TAG_LINE_PATTERN.search(content)
    if tag_line_match:
        tags = set(TAG_PATTERN.findall(tag_line_match.group()))

    # Extract wikilinks (skip frontmatter region)
    body = content
    if fm_match:
        body = content[fm_match.end():]
    links = [resolve_note_name(m) for m in WIKILINK_PATTERN.findall(body)]

    return {
        "type": note_type,
        "processing_status": processing_status,
        "tags": list(tags),
        "links": links,
    }


def scan_vault(vault_root: str):
    """Walk the vault and build a dict of {short_name: {path, metadata, links}}."""
    notes = {}
    name_conflicts = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(vault_root):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for fname in filenames:
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(filepath, vault_root)
            short_name = extract_short_name(filepath, vault_root)

            parsed = parse_note(filepath)
            if parsed is None:
                continue

            # Track name conflicts
            if short_name in notes:
                name_conflicts[short_name].append(rel_path)
                name_conflicts[short_name].append(notes[short_name]["path"])
                continue

            notes[short_name] = {
                "path": rel_path,
                **parsed,
            }

    return notes, dict(name_conflicts)


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_graph(notes: dict) -> nx.DiGraph:
    """Build a directed graph from vault notes and their wikilinks."""
    G = nx.DiGraph()

    # Add all notes as nodes
    for name, data in notes.items():
        G.add_node(name, **{
            "type": data["type"],
            "status": data["processing_status"],
            "path": data["path"],
        })

    # Add edges for wikilinks
    for name, data in notes.items():
        for target in data["links"]:
            # Only add edge if target exists as a note
            if target in notes:
                G.add_edge(name, target)
            # Track broken links as nodes without files
            elif not G.has_node(target):
                G.add_node(target, type="phantom", status="", path="")

    return G


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze_graph(G: nx.DiGraph, top_n: int = 20) -> dict:
    """Compute structural metrics on the vault graph."""
    # Separate real notes from phantom (referenced but don't exist)
    real_nodes = [n for n, d in G.nodes(data=True) if d.get("type") != "phantom"]
    phantom_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "phantom"]

    # --- Centrality metrics (on real nodes subgraph) ---
    G_real = G.subgraph(real_nodes).copy()
    undirected = G_real.to_undirected()

    # PageRank (most influential) — needs numpy/scipy
    try:
        pagerank = nx.pagerank(G_real) if len(G_real) > 0 else {}
    except (ImportError, nx.PowerIterationFailedConvergence):
        # Fallback: use in-degree as proxy for importance
        print("PageRank unavailable (numpy missing), using in-degree proxy", file=sys.stderr)
        total = max(G_real.number_of_nodes(), 1)
        pagerank = {n: G_real.in_degree(n) / total for n in G_real.nodes()}
    top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Betweenness centrality (bridge concepts) — can be slow on large graphs
    try:
        if len(G_real) > 3000:
            # Sample-based approximation for large graphs
            betweenness = nx.betweenness_centrality(G_real, k=min(500, len(G_real))) if len(G_real) > 0 else {}
        else:
            betweenness = nx.betweenness_centrality(G_real) if len(G_real) > 0 else {}
    except Exception as e:
        print(f"Betweenness centrality failed: {e}", file=sys.stderr)
        betweenness = {n: 0.0 for n in G_real.nodes()}
    top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # In-degree (most referenced)
    in_degree = dict(G_real.in_degree())
    top_in_degree = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Out-degree (most connecting)
    out_degree = dict(G_real.out_degree())
    top_out_degree = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # --- Orphans: notes with no incoming or outgoing links ---
    orphans = [n for n in real_nodes
               if G_real.in_degree(n) == 0 and G_real.out_degree(n) == 0]

    # --- Dead ends: notes that are linked TO but link to nothing ---
    dead_ends = [n for n in real_nodes
                 if G_real.in_degree(n) > 0 and G_real.out_degree(n) == 0]

    # --- Clusters (connected components in undirected view) ---
    components = list(nx.connected_components(undirected))
    clusters = []
    for comp in sorted(components, key=len, reverse=True)[:10]:
        # Get dominant types in this cluster
        types = defaultdict(int)
        for node in comp:
            ntype = G_real.nodes[node].get("type", "")
            if ntype:
                types[ntype] += 1
        clusters.append({
            "size": len(comp),
            "sample_nodes": sorted(list(comp))[:5],
            "dominant_types": dict(sorted(types.items(), key=lambda x: x[1], reverse=True)[:3]),
        })

    # --- Type distribution ---
    type_counts = defaultdict(int)
    status_counts = defaultdict(int)
    for n in real_nodes:
        ntype = G_real.nodes[n].get("type", "unknown")
        status = G_real.nodes[n].get("status", "unknown")
        type_counts[ntype] += 1
        if status:
            status_counts[status] += 1

    # --- Density and connectivity ---
    density = nx.density(G_real) if len(G_real) > 1 else 0
    avg_clustering = nx.average_clustering(undirected) if len(undirected) > 0 else 0

    # --- Missing links (phantom nodes = referenced but don't exist) ---
    # For each phantom, find who references it
    missing_links = {}
    for phantom in phantom_nodes[:50]:  # Cap at 50
        referrers = [pred for pred in G.predecessors(phantom) if pred in real_nodes]
        if referrers:
            missing_links[phantom] = referrers[:5]

    return {
        "summary": {
            "total_notes": len(real_nodes),
            "total_edges": G_real.number_of_edges(),
            "phantom_references": len(phantom_nodes),
            "orphan_notes": len(orphans),
            "dead_end_notes": len(dead_ends),
            "connected_components": len(components),
            "density": round(density, 6),
            "avg_clustering": round(avg_clustering, 4),
        },
        "type_distribution": dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True)),
        "status_distribution": dict(sorted(status_counts.items(), key=lambda x: x[1], reverse=True)),
        "top_pagerank": [{"name": n, "score": round(s, 6)} for n, s in top_pagerank],
        "top_betweenness": [{"name": n, "score": round(s, 6)} for n, s in top_betweenness],
        "top_in_degree": [{"name": n, "count": c} for n, c in top_in_degree],
        "top_out_degree": [{"name": n, "count": c} for n, c in top_out_degree],
        "orphans": sorted(orphans)[:50],
        "dead_ends": sorted(dead_ends)[:50],
        "clusters": clusters,
        "missing_links": missing_links,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Analyze Obsidian vault as a graph")
    parser.add_argument("vault_root", help="Path to vault root directory")
    parser.add_argument("--output", "-o", help="Output JSON path (default: stdout)")
    parser.add_argument("--top", type=int, default=20, help="Number of top nodes per metric")
    args = parser.parse_args()

    if not os.path.isdir(args.vault_root):
        print(f"Error: {args.vault_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Scan vault
    print("Scanning vault...", file=sys.stderr)
    notes, name_conflicts = scan_vault(args.vault_root)
    print(f"Found {len(notes)} notes", file=sys.stderr)

    # Build graph
    print("Building graph...", file=sys.stderr)
    G = build_graph(notes)
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges", file=sys.stderr)

    # Analyze
    print("Computing metrics...", file=sys.stderr)
    results = analyze_graph(G, top_n=args.top)

    # Add name conflicts if any
    if name_conflicts:
        results["name_conflicts"] = name_conflicts

    # Output
    output_json = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    print("Done.", file=sys.stderr)


if __name__ == "__main__":
    main()
