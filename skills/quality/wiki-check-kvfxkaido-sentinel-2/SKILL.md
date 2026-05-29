---
name: wiki-check
description: Validate wiki integrity using Kimi. Checks broken wikilinks, missing frontmatter, orphan pages, and structural issues in the Obsidian vault.
allowed-tools: Bash, Read, Glob, Grep
user-invocable: true
proactive: false
---

# Wiki Integrity Check

Use Kimi to validate the SENTINEL wiki structure and find broken links, missing pages, lore/wiki title mismatches, and other issues.

## When to Use

- After bulk wiki edits
- Before committing wiki changes
- When adding new canon pages
- After modifying lore files
- Periodic health checks

## How to Run

### Step 1: Read Agent Context

First, read the wiki agent instructions:
```
C:\dev\SENTINEL\wiki\AGENTS.md
```

This contains all the rules Kimi should check against.

### Step 2: Gather Wiki State

Collect the current wiki structure for Kimi to analyze:

```bash
# List all wiki pages
find C:/dev/SENTINEL/wiki -name "*.md" -type f | head -100

# Extract all wikilinks from canon
grep -roh "\[\[[^]]*\]\]" C:/dev/SENTINEL/wiki/canon/ | sort | uniq

# List frontmatter types
grep -rh "^type:" C:/dev/SENTINEL/wiki/canon/
```

### Step 3: Run Kimi Integrity Check

Invoke Kimi with the wiki structure and rules (using `--print` for non-interactive mode).

**Note:** Set UTF-8 encoding to handle em-dashes in filenames on Windows:

```bash
PYTHONIOENCODING=utf-8 kimi --print -w C:/dev/SENTINEL/wiki -c "You are a wiki integrity checker for the SENTINEL project.

<rules>
$(cat C:/dev/SENTINEL/wiki/AGENTS.md)
</rules>

<wiki_pages>
$(find C:/dev/SENTINEL/wiki -name '*.md' -type f)
</wiki_pages>

<wikilinks_found>
$(grep -roh '\[\[[^]]*\]\]' C:/dev/SENTINEL/wiki/canon/ | sort | uniq)
</wikilinks_found>

Perform these checks:
1. **Broken wikilinks**: For each [[link]], verify a matching page exists (by filename or alias)
2. **Missing factions**: Check all 11 factions have canon pages
3. **Missing regions**: Check all 11 regions have canon pages
4. **Orphan pages**: Find pages not linked from Home.md, Factions.md, Geography.md, or Timeline.md
5. **Lore title mismatches**: Compare wiki link text to lore filenames (after stripping chapter prefixes like '01 - ')
6. **Orphan lore**: Lore files not referenced anywhere in wiki

Output a structured report following the format in AGENTS.md.
Be thorough but concise. Focus on actionable issues."
```

### Step 4: Present Results

Format Kimi's findings as a checklist the user can act on:

```markdown
## Wiki Health Report

### Status: [HEALTHY | NEEDS ATTENTION | BROKEN]

### Issues Found
- [ ] Issue 1
- [ ] Issue 2

### Recommendations
- ...
```

## Alternative: Quick Check (No Kimi)

For a fast local check without Kimi, run the Python script:

```bash
python C:/dev/SENTINEL/wiki/check_links.py
```

This checks:
- Broken wikilinks (missing pages/aliases)
- All 11 factions and regions present
- Lore/wiki title mismatches (case differences, etc.)
- Orphan lore files not referenced in wiki

## Tips

- **Quick check first**: Run `check_links.py` for fast local validation
- **Kimi for deep analysis**: Use Kimi when you need semantic understanding (orphan pages, content consistency)
- Run before major lore updates to catch issues early
- The check is read-only — it never modifies wiki files
- **Lore is source of truth**: When titles mismatch, update wiki to match lore filename
