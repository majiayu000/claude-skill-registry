---
name: obsidian-internal-links
description: Follow and resolve Obsidian internal links ([[link]] syntax) to navigate interconnected notes within an Obsidian vault. Use when exploring note relationships, following references between documents, building knowledge graphs, or understanding how notes connect together. Supports recursive link traversal with configurable depth.
---

# Obsidian Internal Links

## Overview

This skill enables navigation and exploration of Obsidian's internal link structure by resolving `[[link]]` references to read connected notes. Use this skill when understanding relationships between notes, following references, or building a comprehensive view of interconnected ideas within an Obsidian vault.

## When to Use This Skill

Invoke this skill when:
- User asks to "follow links" in an Obsidian note
- User wants to "explore connected notes" or "see what this links to"
- User requests to "read linked pages" or "show me related notes"
- User wants to understand the "knowledge graph" or "note relationships"
- User asks to "trace references" or "find all related content"
- Working with Obsidian markdown files that contain `[[internal links]]`

## Core Workflow

### 1. Identify the Starting Note

Determine which Obsidian note to start from. This could be:
- A file path provided by the user
- The current file being discussed
- A note referenced by name or ID

### 2. Execute the Link Resolver

Use the `scripts/resolve_links.py` script to analyze the note and follow its links.

**Dependencies**: The script requires PyYAML. If using UV: `uv pip install PyYAML`. Otherwise: `pip install PyYAML` or `pip3 install --break-system-packages PyYAML` on systems with externally managed Python.

```bash
python scripts/resolve_links.py <file-path> --vault <vault-path> --depth <depth> --pretty
```

**Parameters:**
- `<file-path>` (required): Path to the markdown file to analyze
- `--vault` (optional): Path to the Obsidian vault (defaults to `/Users/tolga/src/tolgaio/brain`)
- `--depth` (optional): Maximum recursion depth for following links (default: 1)
  - `0` = Extract links but don't follow them
  - `1` = Follow direct links and identify their outgoing links
  - `2+` = Follow links recursively to the specified depth
- `--pretty` (optional): Format JSON output for readability

**Example:**
```bash
# Follow links one level deep from inbox.md
python scripts/resolve_links.py /Users/tolga/src/tolgaio/brain/0_inbox/inbox.md --depth 1 --pretty

# Just extract links without following them
python scripts/resolve_links.py /path/to/note.md --depth 0
```

### 3. Interpret the Results

The script returns a JSON structure containing:

```json
{
  "file": "/path/to/source.md",
  "links": [
    {
      "link_text": "digital-garden",
      "display_text": "Digital Garden",
      "resolved": true,
      "target_file": "/path/to/digital-garden.md",
      "content": "# Digital Garden\n\n...",
      "nested_links": [...]  // If depth > 0
    }
  ],
  "broken_links": ["nonexistent-note"]
}
```

**Key fields:**
- `links`: Array of resolved link objects
  - `link_text`: The target from `[[link_text]]` or `[[link_text|display]]`
  - `display_text`: What's shown to the user (after `|` or same as link_text)
  - `resolved`: Whether the link target was found
  - `target_file`: Absolute path to the linked file (if found)
  - `content`: Full text content of the linked file
  - `nested_links`: Recursively resolved links (if depth allows)
- `broken_links`: Array of link targets that couldn't be resolved

### 4. Present the Information

Structure the results for the user based on their request:

**For link exploration:**
- List all linked notes with their titles
- Show the hierarchy if depth > 0
- Highlight any broken links that need attention

**For content synthesis:**
- Read and summarize the linked notes
- Extract relevant sections
- Connect ideas across multiple notes

**For knowledge mapping:**
- Describe the relationship structure
- Identify central hub notes
- Show connection patterns

## Link Resolution Strategy

The script resolves links using this priority order:

1. **Frontmatter ID**: Checks if the link target matches any note's `id:` field in YAML frontmatter
2. **Filename**: Matches against the filename (without `.md` extension)
3. **Path-based**: For links like `[[folder/note]]`, tries path resolution

**Example:**
```yaml
---
id: digital-garden
aliases:
  - My Garden
  - Knowledge Base
---
```

A link `[[digital-garden]]` or `[[digital-garden|Digital Garden]]` will resolve to this note.

## Handling Different Link Types

### Basic Links
```markdown
[[note-name]]
```
Resolves to a note with `id: note-name` or filename `note-name.md`

### Links with Aliases
```markdown
[[note-id|Display Text]]
```
The script extracts `note-id` as the target and `Display Text` as what's shown

### Heading Links
```markdown
[[note-name#Heading]]
```
Currently resolves to the note itself (heading navigation is future enhancement)

### Path-Based Links
```markdown
[[folder/subfolder/note]]
```
Tries to resolve using the full path, or falls back to just the note name

### Embedded Files
```markdown
![[image.png]]
```
These are automatically skipped as they're not navigable note links

## Managing Recursion

**Depth 0** - Extract only:
- Lists all links in the starting document
- No content loading from linked files
- Fast, minimal context usage
- Use when you only need to know what's linked

**Depth 1** - One level deep (recommended default):
- Reads content of directly linked notes
- Identifies what those notes link to
- Balanced between context and insight
- Use for most exploration tasks

**Depth 2+** - Deep traversal:
- Follows links within linked notes
- Can quickly expand to many files
- Higher context usage
- Use when building comprehensive knowledge maps

**Cycle detection:** The script tracks visited files to prevent infinite loops when notes link to each other.

## Broken Link Handling

When links cannot be resolved:
- They're collected in the `broken_links` array
- Processing continues with other links
- Report broken links to the user so they can:
  - Fix the link
  - Create the missing note
  - Update references

## Example Usage Scenarios

### Scenario 1: Following References
User: "What does my inbox note link to?"

```bash
python scripts/resolve_links.py /Users/tolga/src/tolgaio/brain/0_inbox/inbox.md --depth 1 --pretty
```

Present: "Your inbox links to 5 notes: [list them]. Here's a summary of each linked note..."

### Scenario 2: Building a Knowledge Graph
User: "Show me how my digital garden notes are connected"

```bash
python scripts/resolve_links.py /Users/tolga/src/tolgaio/brain/2_Resources/digital-garden.md --depth 2 --pretty
```

Present: "Your digital garden connects to [X] notes. The main clusters are... [describe the network]"

### Scenario 3: Finding Broken Links
User: "Check if all my project notes have valid links"

```bash
python scripts/resolve_links.py /Users/tolga/src/tolgaio/brain/1_Projects/project-x.md --depth 0
```

Present: "Found 3 broken links: [list them]. These need to be fixed or the target notes created."

## Advanced Considerations

### Performance
- Large vaults (hundreds of files) may take a few seconds to index
- Deep recursion (depth 3+) can process many files
- Consider using `--depth 0` first to see link count before deep traversal

### Context Management
- Each linked file's content is included in the JSON output
- Deep traversal can generate large JSON responses
- Be mindful of context window limits when following many links

### Vault Configuration
- Default vault path: `/Users/tolga/src/tolgaio/brain`
- Override with `--vault` parameter for different vaults
- The script builds an index of all `.md` files in the vault

## Reference Documentation

For detailed information about Obsidian's internal link syntax, variants, and edge cases, refer to `references/obsidian-link-syntax.md`. This includes:
- Complete syntax reference for all link types
- Resolution behavior and priority rules
- Vault-specific naming conventions
- Regular expressions for link extraction
- Best practices for link creation

Load this reference when dealing with complex link patterns or unusual syntax.

## Resources

### scripts/resolve_links.py
Python script that handles link resolution. Capabilities:
- Indexes all markdown files in the vault by frontmatter ID and filename
- Extracts `[[...]]` links using regex parsing
- Resolves links following the priority order described above
- Recursively follows links up to specified depth
- Detects cycles to prevent infinite loops
- Returns structured JSON output with resolved links and content

### references/obsidian-link-syntax.md
Comprehensive documentation covering:
- All Obsidian link syntax variations
- Link resolution behavior and rules
- Vault-specific patterns from `/Users/tolga/src/tolgaio/brain`
- Best practices and common patterns
- Edge cases and special considerations
