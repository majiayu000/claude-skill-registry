#!/usr/bin/env python3
"""
Extract EPUB to structured markdown chapters with metadata.

Usage:
    python extract_epub.py <input.epub> <output_dir>

Requires pandoc to be installed and available on PATH.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata


def check_pandoc():
    """Verify pandoc is installed and accessible."""
    if not shutil.which("pandoc"):
        print("Error: pandoc is not installed or not found on PATH.", file=sys.stderr)
        sys.exit(1)


def run_pandoc(args):
    """Run a pandoc command and return stdout. Exit on failure."""
    cmd = ["pandoc"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError as e:
        print(f"Error running pandoc: {e}", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(f"pandoc failed (exit {result.returncode}):", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    return result.stdout


def extract_metadata(epub_path):
    """Extract title and author from EPUB via pandoc template or YAML parsing."""
    title = ""
    author = ""

    # Approach 1: Use a pandoc template string to extract title and author directly.
    try:
        tpl = r"${if(title)}${title}${endif}" + "\n" + r"${if(author)}${for(author)}${it}${sep}, ${endfor}${endif}"
        result = subprocess.run(
            ["pandoc", epub_path, "-f", "epub", "-t", "plain", "--standalone", "--template", tpl],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 1:
                title = lines[0].strip()
            if len(lines) >= 2:
                author = lines[1].strip()
    except OSError:
        pass

    # Approach 2: Parse YAML from the markdown YAML block in pandoc --standalone output.
    if not title:
        try:
            result = subprocess.run(
                ["pandoc", epub_path, "-f", "epub", "-t", "markdown", "--standalone"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if result.returncode == 0:
                # Extract YAML frontmatter block between --- markers.
                yaml_match = re.search(r"^---\n(.*?)\n---", result.stdout, re.DOTALL)
                if yaml_match:
                    yaml_text = yaml_match.group(1)
                    title_match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", yaml_text, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
                    author_match = re.search(r"^author:\s*['\"]?(.+?)['\"]?\s*$", yaml_text, re.MULTILINE)
                    if author_match:
                        author = author_match.group(1).strip()
                    # Handle author as list.
                    if not author:
                        author_section = re.search(r"^author:\s*\n((?:\s*-\s*.+\n?)+)", yaml_text, re.MULTILINE)
                        if author_section:
                            author_lines = re.findall(r"-\s*['\"]?(.+?)['\"]?\s*$", author_section.group(1), re.MULTILINE)
                            author = ", ".join(author_lines)
        except OSError:
            pass

    # Approach 3: Fall back to filename.
    if not title:
        title = os.path.splitext(os.path.basename(epub_path))[0]

    return {
        "title": title or "Unknown Title",
        "author": author or "Unknown Author",
    }


def slugify(text):
    """Convert heading text to a filesystem-safe slug."""
    # Normalize unicode characters.
    text = unicodedata.normalize("NFKD", text)
    # Lowercase.
    text = text.lower()
    # Replace spaces and hyphens with underscores.
    text = re.sub(r"[\s\-]+", "_", text)
    # Strip everything that isn't alphanumeric or underscore.
    text = re.sub(r"[^a-z0-9_]", "", text)
    # Collapse multiple underscores.
    text = re.sub(r"_+", "_", text)
    # Strip leading/trailing underscores.
    text = text.strip("_")
    return text or "untitled"


def split_by_headings(markdown_text, level):
    """
    Split markdown text by headings of the given level (1 or 2).

    Returns a list of (title, body) tuples. Content before the first
    heading is included as a chapter with title "Front Matter" if
    non-trivial.
    """
    if level == 1:
        pattern = re.compile(r"^(# .+)$", re.MULTILINE)
    else:
        pattern = re.compile(r"^(## .+)$", re.MULTILINE)

    splits = pattern.split(markdown_text)

    chapters = []

    # splits[0] is text before the first heading.
    preamble = splits[0].strip()
    if preamble and len(preamble) > 50:
        chapters.append(("Front Matter", preamble))

    # After that, headings and bodies alternate: heading, body, heading, body...
    i = 1
    while i < len(splits):
        heading_line = splits[i].strip()
        # Remove the markdown heading prefix.
        title = re.sub(r"^#{1,6}\s+", "", heading_line).strip()
        body = splits[i + 1].strip() if i + 1 < len(splits) else ""
        if title:
            chapters.append((title, heading_line + "\n\n" + body))
        i += 2

    return chapters


def split_into_chapters(markdown_text):
    """
    Split markdown into chapters. Tries H1 first, falls back to H2,
    then returns the whole text as a single chapter.
    """
    # Count H1 headings.
    h1_count = len(re.findall(r"^# .+$", markdown_text, re.MULTILINE))

    if h1_count >= 2:
        chapters = split_by_headings(markdown_text, level=1)
        if len(chapters) >= 2:
            return chapters

    # Fall back to H2.
    h2_count = len(re.findall(r"^## .+$", markdown_text, re.MULTILINE))

    if h2_count >= 2:
        chapters = split_by_headings(markdown_text, level=2)
        if len(chapters) >= 2:
            return chapters

    # No usable heading structure; return entire text as one chapter.
    return [("Full Text", markdown_text)]


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.epub> <output_dir>", file=sys.stderr)
        sys.exit(1)

    epub_path = sys.argv[1]
    output_dir = sys.argv[2]

    # Validate input.
    if not os.path.isfile(epub_path):
        print(f"Error: input file not found: {epub_path}", file=sys.stderr)
        sys.exit(1)

    check_pandoc()

    # Convert EPUB to markdown.
    print(f"Converting {epub_path} to markdown...")
    markdown_text = run_pandoc([epub_path, "-t", "markdown", "--wrap=none"])

    # Extract metadata.
    print("Extracting metadata...")
    meta = extract_metadata(epub_path)

    # Create output directories.
    chapters_dir = os.path.join(output_dir, "chapters")
    os.makedirs(chapters_dir, exist_ok=True)

    # Write full text.
    full_text_path = os.path.join(output_dir, "full_text.md")
    with open(full_text_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"Wrote {full_text_path}")

    # Split into chapters.
    print("Splitting into chapters...")
    chapters = split_into_chapters(markdown_text)

    chapter_list = []
    for idx, (title, body) in enumerate(chapters, start=1):
        slug = slugify(title)
        filename = f"ch{idx:02d}_{slug}.md"
        filepath = os.path.join(chapters_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(body)

        chapter_list.append({
            "number": idx,
            "title": title,
            "file": f"chapters/{filename}",
        })
        print(f"  Chapter {idx:02d}: {title} -> {filename}")

    # Build and write metadata.json.
    metadata = {
        "title": meta["title"],
        "author": meta["author"],
        "total_chapters": len(chapter_list),
        "chapter_list": chapter_list,
        "format": "epub",
    }

    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Wrote {metadata_path}")

    print(f"\nDone. {len(chapter_list)} chapter(s) extracted to {output_dir}")


if __name__ == "__main__":
    main()
