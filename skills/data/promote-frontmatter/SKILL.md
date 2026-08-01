---
name: promote-frontmatter
description: 'Extract prose patterns like "Key: Value" or "Key: [[wikilink]]" and
  promote them to YAML frontmatter. Triggers on "promote to frontmatter", "extract
  frontmatter", "prose to yaml".'
---

---
name: promote-frontmatter
description: Extract prose patterns like "Key: Value" or "Key: [[wikilink]]" and promote them to YAML frontmatter. Triggers on "promote to frontmatter", "extract frontmatter", "prose to yaml".
auto_trigger: true
trigger_keywords:
  - "promote to frontmatter"
  - "extract frontmatter"
  - "prose to yaml"
  - "prose to frontmatter"
  - "add frontmatter"
  - "create frontmatter"
  - "extract metadata"
  - "move to frontmatter"
  - "convert prose to frontmatter"
  - "frontmatter from content"
allowed-tools: mcp__flywheel__detect_prose_patterns, mcp__flywheel__suggest_frontmatter_from_prose
---

# Promote to Frontmatter

Extract "Key: Value" and "Key: [[wikilink]]" patterns from note prose and promote them to YAML frontmatter.

## When to Use

Invoke when you want to:
- Convert inline metadata patterns to structured frontmatter
- Add YAML frontmatter based on existing prose patterns
- Structure unstructured notes for better querying
- Migrate from prose-based to schema-based organization

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| path | Yes | Path to the note (e.g., "meeting-notes/2024-01-15.md") |

## Process

### 1. Parse User Input

Recognize promotion requests:
- "promote the prose patterns to frontmatter in this note"
- "extract frontmatter from meeting-notes/standup.md"
- "move the metadata to yaml"

### 2. Call MCP Tools

```
# Step 1: Detect all prose patterns
mcp__flywheel__detect_prose_patterns(path)

# Step 2: Get frontmatter suggestions
mcp__flywheel__suggest_frontmatter_from_prose(path)
```

### 3. Format Results

```
Frontmatter Promotion: meeting-notes/2024-01-15.md
=================================================

Detected Patterns (4):
-------------------------------------------------
  Line 8:  Client: [[Acme Corp]]    (wikilink)
  Line 10: Date: 2024-01-15         (plain text)
  Line 12: Attendees: [[Ben Carter]] (wikilink)
  Line 12: Attendees: [[Sarah J]]   (wikilink)

Suggested Frontmatter:
-------------------------------------------------
---
client: [[Acme Corp]]         # High confidence (wikilink pattern)
date: 2024-01-15              # Medium confidence
attendees:                    # Array from multiple values
  - [[Ben Carter]]
  - [[Sarah J]]
---

Actions:
-------------------------------------------------
1. Add the suggested frontmatter to the file
2. Optionally remove the original prose patterns
3. Review for accuracy before committing

Would you like me to apply these changes?

=================================================
```

### 4. Apply Changes (with confirmation)

If user confirms:
1. Read current file content
2. Add/merge suggested frontmatter at top
3. Optionally remove or comment out the original prose patterns
4. Write updated file

## Pattern Detection

Patterns detected:
- `Key: [[wikilink]]` - Preserved as wikilinks in frontmatter
- `Key: Value` - Converted to plain frontmatter field
- `Key: "quoted value"` - Quotes stripped, value used as-is
- Multiple values for same key -> Array in frontmatter

## Use Cases

- **Meeting notes**: Extract client, date, attendees from prose
- **Project docs**: Convert inline metadata to queryable fields
- **Daily notes**: Structure recurring patterns (mood, weather, etc.)
- **Research notes**: Extract source, author, topic fields

## Integration

Part of the Bidirectional Bridge:
- **normalize-note**: Full analysis including this + wikilink suggestions
- **wikilinkify-frontmatter**: Convert plain values to wikilinks

---

**Version:** 1.0.0
