---
name: writing-to-logseq
version: 1.0.0
description: >
  Expert in writing data to Logseq DB graphs via HTTP API.
  Auto-invokes when users want to create pages, add blocks, update content,
  set properties, or sync conversation notes to their Logseq graph.
  Provides CRUD operations with safety guidelines.
allowed-tools: Read, Bash, Grep, Glob
---

# Writing to Logseq

## When to Use This Skill

This skill auto-invokes when:
- User wants to create new pages or blocks in Logseq
- Updating existing content in the graph
- Setting or modifying properties on entities
- Adding tags/classes to blocks
- Syncing conversation notes to Logseq
- User mentions "add to logseq", "create page", "update block"

**Write Operations**: See `{baseDir}/scripts/write-operations.py` for the API.

## Available Operations

| Operation | Description |
|-----------|-------------|
| `create_page(title, content)` | Create new page |
| `create_block(parent, content)` | Add block under parent |
| `update_block(uuid, content)` | Modify block content |
| `delete_block(uuid)` | Remove block |
| `set_property(uuid, key, value)` | Set property value |
| `add_tag(uuid, tag)` | Add tag/class to block |
| `append_to_page(title, content)` | Add content to existing page |

## Quick Examples

### Create a Page

```python
from write_operations import LogseqWriter

writer = LogseqWriter()

# Create simple page
page = writer.create_page("Meeting Notes 2024-01-15")

# Create page with initial content
page = writer.create_page(
    "Project Alpha",
    content="Project overview and tasks",
    properties={"status": "Active", "priority": "High"}
)
```

### Add Blocks

```python
# Add block to a page
block = writer.create_block(
    parent="page-uuid-or-title",
    content="New task item"
)

# Add nested block
child = writer.create_block(
    parent=block["uuid"],
    content="Sub-task details"
)
```

### Update Content

```python
# Update block content
writer.update_block(
    uuid="block-uuid",
    content="Updated content here"
)

# Append to existing page
writer.append_to_page(
    title="Daily Notes",
    content="- New item added via API"
)
```

### Set Properties

```python
# Set single property
writer.set_property(
    uuid="block-uuid",
    key="status",
    value="Complete"
)

# Set typed property
writer.set_property(
    uuid="block-uuid",
    key="rating",
    value=5,
    type="number"
)

# Set multiple properties
writer.set_properties(
    uuid="block-uuid",
    properties={
        "author": "John Doe",
        "rating": 5,
        "published": "2024-01-15"
    }
)
```

### Add Tags

```python
# Add tag to block
writer.add_tag(uuid="block-uuid", tag="Book")

# Add multiple tags
writer.add_tags(uuid="block-uuid", tags=["Important", "Review"])
```

## HTTP API Methods

### Create Page

```json
{
  "method": "logseq.Editor.createPage",
  "args": ["PageTitle", {"property": "value"}, {"createFirstBlock": true}]
}
```

### Insert Block

```json
{
  "method": "logseq.Editor.insertBlock",
  "args": ["parent-uuid", "Block content", {"sibling": false}]
}
```

### Update Block

```json
{
  "method": "logseq.Editor.updateBlock",
  "args": ["block-uuid", "New content"]
}
```

### Set Property

```json
{
  "method": "logseq.Editor.upsertBlockProperty",
  "args": ["block-uuid", "property-name", "value"]
}
```

### Delete Block

```json
{
  "method": "logseq.Editor.removeBlock",
  "args": ["block-uuid"]
}
```

## Safety Guidelines

### Best Practices

1. **Verify before delete** - Always confirm block exists before removal
2. **Use unique titles** - Avoid creating duplicate pages
3. **Validate properties** - Ensure property types match schema
4. **Handle errors** - Catch and handle API failures gracefully

### Common Pitfalls

- **Duplicate pages**: Check if page exists before creating
- **Invalid UUIDs**: Verify UUID format before operations
- **Property types**: Number properties need numeric values
- **Rate limiting**: Don't spam API with rapid requests

## Content Formatting

### Markdown Support

```python
# Logseq supports markdown in blocks
writer.create_block(
    parent=page_uuid,
    content="""
## Section Header

- Bullet point
- Another point
  - Nested item

**Bold** and *italic* work too.

[[Link to Page]] and #tags
"""
)
```

### Property Syntax

```python
# Properties can be set in content
writer.create_block(
    parent=page_uuid,
    content="""
- Task item
  status:: In Progress
  priority:: High
  due:: [[2024-01-20]]
"""
)

# Or via API (preferred for typed values)
writer.set_property(uuid, "rating", 5)  # number
writer.set_property(uuid, "done", True)  # checkbox
```

## Sync Conversation to Logseq

### Pattern for Saving Notes

```python
def sync_conversation_to_logseq(title, notes):
    """Sync conversation notes to Logseq page."""
    writer = LogseqWriter()

    # Create or get page
    page = writer.get_or_create_page(f"Claude Notes/{title}")

    # Add timestamp header
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    writer.append_to_page(
        title=f"Claude Notes/{title}",
        content=f"""
## {timestamp}

{notes}

---
"""
    )

    return page
```

## Error Handling

```python
try:
    page = writer.create_page("My Page")
except writer.ConnectionError:
    print("Cannot connect to Logseq")
except writer.DuplicateError:
    print("Page already exists")
except writer.ValidationError as e:
    print(f"Invalid data: {e}")
```

## Reference Materials

- See `{baseDir}/references/write-operations.md` for all operations
- See `{baseDir}/references/safety-guidelines.md` for safety practices
- See `{baseDir}/templates/page-template.md` for page templates
