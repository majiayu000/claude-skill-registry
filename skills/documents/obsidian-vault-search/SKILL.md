---
name: obsidian-vault-search
description: |
  Searches an Obsidian vault intelligently — combines CLI search, frontmatter
  filtering, content grep, and wikilink traversal. Goes beyond keyword search
  to find notes by property, by link, by folder, and by content. Activates on
  "find in vault", "search vault", "which note has", "where did I write about",
  or when looking for specific notes in Obsidian.
allowed-tools: |
  bash: grep, find, ls, cat, obsidian-cli, obsidian, python3
  file: read
---

# Obsidian Vault Search

<purpose>
Raw grep on a vault is noisy. You search "API" and get 200 hits across daily
notes, templates, meeting notes, and the actual design doc you wanted. Obsidian
vaults are structured — frontmatter, wikilinks, folders, tags — and search
should use that structure. This skill searches smart: by property, by link graph,
by folder scope, not just by keyword.
</purpose>

## When To Activate

<triggers>
- User says "find in vault", "search vault", "search obsidian"
- User says "which note has...", "where did I write about..."
- User says "find all meetings about...", "show notes tagged..."
- User needs to locate a specific note or set of notes
- Before creating a note (to check if it exists)
- Any vault-level search that isn't just opening a known file
</triggers>

Do NOT trigger for:
- Searching code repositories (use zero-in)
- Web search (different skill entirely)
- Single file content search (just read the file)

## Instructions

### Step 1: Classify the Search

<classify>
Determine what kind of search before running anything:

| Request | Search Type | Method |
|---------|------------|--------|
| "Find note about X" | Content search | grep + frontmatter |
| "All meetings with Sarah" | Property search | frontmatter scan |
| "Notes tagged #project" | Tag search | frontmatter scan |
| "What links to [[Note]]" | Backlink search | wikilink grep |
| "Notes in Projects/ folder" | Folder search | find |
| "Recent notes about X" | Combined | content + date sort |
| "Everything related to X" | Graph search | links + content |

Match the search method to the request. Don't grep the whole vault for a
property-based question.
</classify>

### Step 2: Run the Appropriate Search

<search_methods>

**Content search** — find notes mentioning a term:
```bash
# Basic content search
grep -rl "search term" "$VAULT_PATH" --include="*.md" | head -20

# With context (shows surrounding lines)
grep -rn "search term" "$VAULT_PATH" --include="*.md" -C 2 | head -50

# Case insensitive
grep -ril "search term" "$VAULT_PATH" --include="*.md"
```

**Property search** — find notes with specific frontmatter:
```bash
# Find by type
grep -rl "^type: meeting" "$VAULT_PATH" --include="*.md"

# Find by status
grep -rl "^status: active" "$VAULT_PATH" --include="*.md"

# Find by tag in frontmatter
grep -rl "tags:" "$VAULT_PATH" --include="*.md" | \
  xargs grep -l "project-name"

# Find by attendee
grep -rl "attendees:" "$VAULT_PATH" --include="*.md" | \
  xargs grep -l "Sarah"

# Combined: active meetings
grep -rl "^type: meeting" "$VAULT_PATH" --include="*.md" | \
  xargs grep -l "^status: active"
```

**Tag search** — find notes with specific tags:
```bash
# Inline tags
grep -rl "#tag-name" "$VAULT_PATH" --include="*.md"

# Frontmatter tags
grep -rl "  - tag-name" "$VAULT_PATH" --include="*.md"

# Both
grep -rl "#tag-name\|  - tag-name" "$VAULT_PATH" --include="*.md"
```

**Backlink search** — find notes that link to a specific note:
```bash
# Find all notes linking to [[Note Name]]
grep -rl "\[\[Note Name" "$VAULT_PATH" --include="*.md"

# Find links with aliases
grep -rl "\[\[Note Name|" "$VAULT_PATH" --include="*.md"
```

**Folder search** — find notes in a specific location:
```bash
find "$VAULT_PATH/Projects/project-name" -name "*.md" | sort
```

**Date-range search** — find notes by date:
```bash
# Notes modified in last 7 days
find "$VAULT_PATH" -name "*.md" -mtime -7 | sort

# Notes with date property in range
grep -rl "^date: 2026-02" "$VAULT_PATH" --include="*.md"
```

**CLI search** (if available):
```bash
# Official CLI
obsidian search query="search term" limit=20

# Yakitrak CLI
obsidian-cli search-content "search term"
```
</search_methods>

### Step 3: Rank and Present Results

<results>
Don't dump raw grep output. Process the results:

1. **Deduplicate** — same note from multiple matches
2. **Sort by relevance:**
   - Title match > heading match > body match
   - Recent notes > older notes
   - Exact match > partial match
3. **Extract context** — show WHY each result matched
4. **Show frontmatter** — type, status, date for each result

```bash
# For each result, extract useful metadata
for file in $RESULTS; do
  echo "---"
  echo "File: $file"
  # Get frontmatter type and status
  head -10 "$file" | grep "^type:\|^status:\|^date:"
  # Get the match context
  grep -n "search term" "$file" | head -3
done
```
</results>

### Step 4: Offer Follow-Up Actions

<followup>
After presenting results, offer relevant next steps:

- "Open [[Note Name]] to read it?"
- "Want to see notes that link to this one?"
- "Should I create a base view for this query?"
- "Want to add this to today's daily note?"
</followup>

## Output Format

```markdown
## Vault Search: "query"

**Found:** X notes

### Results

1. **[[Note Title]]** — Notes/note-title.md
   Type: note | Status: active | Date: 2026-02-10
   > ...matching context...

2. **[[Another Note]]** — Projects/project/another-note.md
   Type: meeting | Status: active | Date: 2026-02-08
   > ...matching context...

### Related
- [[Linked Note 1]] (linked from result #1)
- [[Linked Note 2]] (linked from result #2)

Want to open any of these, or refine the search?
```

## NEVER

- Dump raw grep output without processing
- Search the entire vault without narrowing scope first
- Return more than 20 results without asking to narrow
- Search without indicating what was searched and how
- Open or modify notes during a search (search is read-only)

## ALWAYS

- Classify the search type before running commands
- Use the most targeted search method for the request
- Show frontmatter metadata alongside results
- Deduplicate results
- Offer follow-up actions
- Suggest narrowing if too many results (>20)

## Example

**User:** "Find all my meeting notes about the API project"

```
Vault Search: "meeting notes about API project"

Search: type == meeting AND (content contains "API" OR project == "api")

Found: 4 notes

1. [[2026-02-10 API Design Review]] — Projects/api/meetings/2026-02-10-api-design-review.md
   Type: meeting | Status: active | Date: 2026-02-10
   > Discussed rate limiting approach and endpoint contracts

2. [[2026-02-05 API Sprint Planning]] — Projects/api/meetings/2026-02-05-api-sprint-planning.md
   Type: meeting | Status: active | Date: 2026-02-05
   > Sprint goals: auth middleware, rate limiting, documentation

3. [[2026-01-28 API Kickoff]] — Projects/api/meetings/2026-01-28-api-kickoff.md
   Type: meeting | Status: completed | Date: 2026-01-28
   > Initial scope: REST API for mobile app

4. [[2026-01-20 API Requirements]] — Projects/api/meetings/2026-01-20-api-requirements.md
   Type: meeting | Status: completed | Date: 2026-01-20
   > Requirements gathering with product team

Related notes:
- [[api-design]] (linked from 3 meetings)
- [[api-rate-limiting]] (linked from #1, #2)

Want to open any of these?
```

<failed-attempts>
What DOESN'T work:
- Grepping "meeting" across the whole vault — matches templates, daily notes, random mentions
- Searching by filename only — misses notes where the content matches but the filename doesn't
- Not checking frontmatter — you find notes that MENTION meetings but aren't meeting notes
- Returning 50+ results — user can't process that, narrow the search
</failed-attempts>
