---
name: update-docs
version: "1.0"
description: >-
  Use when implementing features, fixing bugs, or refactoring code that may
  invalidate existing docs. Detects stale documentation by matching the code
  diff against in-repo doc files and applies targeted updates. Relevant when
  code changes rename, remove, or add APIs, fields, config keys, or CLI flags.
  Also applies when the user says "update docs", "check docs", or "are the
  docs stale", or when reviewing a branch for documentation accuracy.
---

# Update Docs

Code changes can silently invalidate documentation. A renamed function,
a changed API signature, a removed configuration option, each can leave
docs describing behavior that no longer exists. This skill detects that
drift by matching the code diff against in-repo documentation and
updating docs whose descriptions contradict the new code.

## Process

Follow these steps in order. Do not skip steps.

### 1. Get the diff

```bash
DEFAULT_BRANCH=$(git rev-parse --abbrev-ref origin/HEAD | cut -d/ -f2)
git diff $(git merge-base HEAD "$DEFAULT_BRANCH")..HEAD --no-color
```

Record the list of files changed in the PR:

```bash
git diff --name-only $(git merge-base HEAD "$DEFAULT_BRANCH")..HEAD
```

If the diff is empty, output `NO_DOCS_UPDATED` and stop.

### 2. Discover documentation files

Explore the repository structure to identify where documentation lives.
Different repos organize docs differently — look for dedicated doc
directories, standalone files like README.md at any level, and any
other files whose primary purpose is documentation.

Search broadly — include diagram and config files that live alongside
docs:

```bash
find . -type f \( -name "*.md" -o -name "*.rst" -o -name "*.adoc" \
  -o -name "*.txt" -o -name "*.mmd" -o -name "*.puml" \
  -o -name "*.yaml" -o -name "*.yml" \) \
  ! -path "./.git/*" ! -path "./.forge/*" ! -path "./vendor/*" \
  ! -path "./node_modules/*" \
  | head -500
```

Then filter the results:

- **Exclude** files already modified in the PR (they are being actively
  updated — check against the changed file list from step 1)
- **Exclude** auto-generated files (lockfiles, generated API docs,
  swagger output)
- **Exclude** changelog and release note entries that describe past
  releases
- **Exclude** YAML/YML files that are not documentation. Only keep
  YAML files that live in doc directories or are clearly documentation
  examples.

If no documentation files exist in the repo, output `NO_DOCS_FOUND`
and stop.

### 3. Build the identifier checklist

Go through **every** changed file in the PR. For each file, extract
identifiers from the modified lines (lines starting with `+` or `-`)
and from diff hunk headers (`@@` lines). Write them down as a numbered
checklist — one entry per changed file, with all identifiers from that
file.

Use the most specific form of each identifier. CLI flag names,
configuration keys, full function names, and type names are good —
they match only relevant docs. Avoid generic short words that would
match hundreds of unrelated files. If a generic term is the only
identifier available for a change, include it, but prefer specific
forms when they exist.

Do not skip files. Do not prioritize some files over others. Every
changed file gets an entry in the checklist.

### 4. Search docs for every identifier

Write a shell script that takes the identifiers from step 3 and
greps for each one across the documentation files from step 2.
Run the script in a single Bash call:

```bash
for id in "identifier1" "identifier2" "identifier3"; do
  matches=$(grep -rlFi "$id" <doc_files> 2>/dev/null)
  if [ -n "$matches" ]; then
    echo "MATCH: $id -> $matches"
  fi
done
```

Include every identifier from every checklist entry in the `for`
loop. The script handles the searching mechanically — no identifiers
are skipped.

From the script output, collect all matched doc files into a
candidate list.

### 5. Evaluate candidates (two passes)

**Pass 1 — Quick scan.** For each candidate, view only the lines
that matched the grep (use `grep -n` to see them in context). Based
on the matching lines alone, give a quick verdict:

```
- path/to/doc.md -> possibly stale (describes behavior that changed)
- path/to/other.md -> not stale (mentions identifier in passing)
```

Every candidate must have a verdict. Do not skip candidates.

**Pass 2 — Deep read.** Only for candidates marked "possibly stale"
in pass 1. Read the full file alongside the relevant section of the
diff. Confirm whether the doc is actually stale. Check the file
header for auto-generation markers — if the file is generated from
source, skip it.

When evaluating:

- **Only flag docs whose content is now incorrect.** A doc that
  mentions an identifier is not stale if the described behavior is
  unchanged. It is stale only if the behavior, signature, or semantics
  changed in a way that makes the doc misleading.
- **Do not flag changelog entries or release notes that describe past
  releases.** Historical entries are not stale because the code evolved.

### 6. Review beyond grep results

This step catches stale references that grep cannot find because
documentation often uses prose names that differ from code identifiers,
and new code introduces identifiers that don't exist in any doc yet.

Always read the repository's README. Also read any main index or
overview files at the root of doc directories. Read each file fully
and compare it against the diff. Determine whether it describes any
behavior, flow, or feature that the code changes affected. If it
does, add it to the list of confirmed stale docs.

Also scan the discovered documentation files for any that may cover
the same area as the changed code, based on your understanding of
what the diff does. You don't need to read every file — use file
names and paths to decide which ones are worth checking.

### 7. Update confirmed stale docs

For each doc confirmed stale:

1. Read the full file
2. Update the documentation so it accurately reflects the new code
3. Preserve the file's existing format, style, and structure

### 8. Present changes for review

Do **not** commit automatically. Instead, present the user with a
summary of every file you updated and what changed in each one.
Let the user review the changes and decide whether to commit.

### 9. Output

If docs were updated:
```
DOCS_UPDATED

Updated:
- [path/to/doc.md] Brief description of what was updated and why
- [path/to/other.rst] Brief description
```

If no docs needed updating:
```
NO_DOCS_UPDATED
```

If no doc files found:
```
NO_DOCS_FOUND
```

## Constraints

- **Only change what the diff affects.** Fix stale content and add
  new information that the diff introduced to existing docs. Do not
  improve, restructure, or reformat documentation that is unrelated
  to the code change.
- **Do not update historical entries.** Changelog and release note
  entries for past releases are not stale — they describe what happened
  at that point in time.
- **Skip auto-generated files.** Do not edit files that are generated
  from source. They should be regenerated, not manually patched.
- **Update existing files only.** Do not create new doc files from
  scratch.
- **Preserve format.** Match the existing file's formatting conventions
  (heading style, list style, code block syntax, etc.).
