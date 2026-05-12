#!/usr/bin/env python3
"""Inspect, filter, and query a typed node registry.

Usage:
    python3 registry.py [--registry dag-registry.json] [--filter "pattern"] [--show-schemas] [--stats]
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Inspect a typed node registry")
    parser.add_argument("--registry", "-r", default="dag-registry.json")
    parser.add_argument("--filter", "-f", default=None, help="Glob pattern to filter node names")
    parser.add_argument("--show-schemas", "-s", action="store_true", help="Show full input/output schemas")
    parser.add_argument("--stats", action="store_true", help="Show registry statistics")
    parser.add_argument("--kind", "-k", default=None, help="Filter by kind (function, method, class, endpoint)")
    parser.add_argument("--tag", "-t", default=None, help="Filter by tag")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text())
    nodes = registry.get("nodes", [])

    if args.filter:
        nodes = [n for n in nodes if fnmatch.fnmatch(n["name"], args.filter)]
    if args.kind:
        nodes = [n for n in nodes if n["kind"] == args.kind]
    if args.tag:
        nodes = [n for n in nodes if args.tag in n.get("tags", [])]

    if args.stats:
        all_nodes = registry.get("nodes", [])
        kinds = {}
        languages = {}
        tags = {}
        for n in all_nodes:
            kinds[n["kind"]] = kinds.get(n["kind"], 0) + 1
            languages[n["language"]] = languages.get(n["language"], 0) + 1
            for t in n.get("tags", []):
                tags[t] = tags.get(t, 0) + 1

        print(f"Registry: {registry['metadata']['node_count']} nodes")
        print(f"Extracted: {registry['metadata']['extracted_at']}")
        print(f"Source: {registry['metadata']['source_root']}")
        print(f"\nBy kind:")
        for k, v in sorted(kinds.items()):
            print(f"  {k}: {v}")
        print(f"\nBy language:")
        for k, v in sorted(languages.items()):
            print(f"  {k}: {v}")
        if tags:
            print(f"\nBy tag:")
            for k, v in sorted(tags.items(), key=lambda x: -x[1]):
                print(f"  {k}: {v}")
        return

    if args.json:
        print(json.dumps(nodes, indent=2))
        return

    if not nodes:
        print("No nodes found matching criteria.")
        return

    for node in nodes:
        print(f"{node['name']} ({node['kind']}, {node['language']})")
        if node.get("description"):
            print(f"  {node['description']}")
        if node.get("tags"):
            print(f"  tags: {', '.join(node['tags'])}")
        if node.get("side_effects"):
            print(f"  side_effects: true")
        if args.show_schemas:
            print(f"  input:  {json.dumps(node['input_schema'], separators=(',', ':'))}")
            print(f"  output: {json.dumps(node['output_schema'], separators=(',', ':'))}")
        print(f"  source: {node['source_ref']['file']}:{node['source_ref']['line']}")
        print()

    print(f"--- {len(nodes)} node(s) ---")


if __name__ == "__main__":
    main()
