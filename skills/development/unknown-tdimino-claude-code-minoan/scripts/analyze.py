#!/usr/bin/env python3
"""Analyze a repository and generate a typed node registry.

Usage:
    python3 analyze.py [--language python|typescript|auto] [--output dag-registry.json] [repo_root]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from extractors.base import BaseExtractor
from extractors.python_extractor import PythonExtractor
from extractors.typescript_extractor import TypeScriptExtractor


def detect_languages(root: Path) -> list[str]:
    languages = []
    py_files = list(root.rglob("*.py"))
    ts_files = list(root.rglob("*.ts")) + list(root.rglob("*.tsx"))

    skip = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"}
    py_files = [f for f in py_files if not any(p in skip for p in f.parts)]
    ts_files = [f for f in ts_files if not any(p in skip for p in f.parts)]

    if py_files:
        languages.append("python")
    if ts_files:
        languages.append("typescript")
    return languages


def get_extractor(language: str) -> BaseExtractor:
    if language == "python":
        return PythonExtractor()
    elif language == "typescript":
        return TypeScriptExtractor()
    else:
        raise ValueError(f"Unsupported language: {language}")


def merge_registries(registries: list[dict]) -> dict:
    if len(registries) == 1:
        return registries[0]

    merged = registries[0].copy()
    all_languages = set()
    all_nodes = []

    for reg in registries:
        all_languages.update(reg["metadata"]["languages"])
        all_nodes.extend(reg["nodes"])

    merged["metadata"]["languages"] = sorted(all_languages)
    merged["metadata"]["node_count"] = len(all_nodes)
    merged["nodes"] = all_nodes
    return merged


def main():
    parser = argparse.ArgumentParser(description="Extract typed node registry from a repository")
    parser.add_argument("repo_root", nargs="?", default=".", help="Repository root (default: cwd)")
    parser.add_argument("--language", "-l", choices=["python", "typescript", "auto"], default="auto")
    parser.add_argument("--output", "-o", default="dag-registry.json", help="Output file path")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    if args.language == "auto":
        languages = detect_languages(root)
        if not languages:
            print("No Python or TypeScript files found", file=sys.stderr)
            sys.exit(1)
        print(f"Detected languages: {', '.join(languages)}")
    else:
        languages = [args.language]

    registries = []
    for lang in languages:
        print(f"Extracting {lang} types...")
        extractor = get_extractor(lang)
        registry = extractor.build_registry(root)
        print(f"  Found {registry['metadata']['node_count']} nodes")
        registries.append(registry)

    merged = merge_registries(registries)
    output = Path(args.output)
    output.write_text(json.dumps(merged, indent=2))
    print(f"\nRegistry written to {output} ({merged['metadata']['node_count']} nodes)")


if __name__ == "__main__":
    main()
