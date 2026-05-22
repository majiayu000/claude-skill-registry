---
name: notion-management
description: Complete guide for working with Notion API in Node.js/JavaScript projects. Use when creating, updating, fetching, or managing Notion pages, databases, and properties. Includes proper handling of rich text, database schemas, multi-select fields, dates, and complex content structures. Triggers on tasks like "create a Notion page," "update database properties," "add content to Notion," or "manage Notion workflows."
license: MIT
---

# Notion Management Skill

Master working with the Notion API for Node.js/JavaScript development. This skill provides patterns, tools, and references for all common Notion operations.

## Quick Start

### Fetching Notion Resources

```typescript
// Fetch a page or database
const page = await notion_notion-fetch({
  id: "page-id-or-url"
});

// Pages return markdown content and properties
// Databases return schema, data sources, and views
```

### Creating Pages

```typescript
// Single page creation
const pages = await notion_notion-create-pages({
  pages: [{
    properties: {
      title: "My Page Title",
      // Other properties based on database schema
    },
    content: "# Markdown content here\n\nSupports rich markdown."
  }],
  parent: {
    data_source_id: "collection-id" // or page_id, or database_id
  }
});
```

### Updating Pages

```typescript
// Update properties
await notion_notion-update-page({
  page_id: "page-id",
  command: "update_properties",
  properties: {
    title: "Updated Title",
    status: "Done"
  }
});

// Replace all content
await notion_notion-update-page({
  page_id: "page-id",
  command: "replace_content",
  new_str: "# New content here"
});

// Replace specific section
await notion_notion-update-page({
  page_id: "page-id",
  command: "replace_content_range",
  selection_with_ellipsis: "# Old heading...last paragraph.",
  new_str: "# New heading\nNew content"
});

// Insert content after a section
await notion_notion-update-page({
  page_id: "page-id",
  command: "insert_content_after",
  selection_with_ellipsis: "## Section...end of section.",
  new_str: "\n## New Section\nNew content here"
});
```

## Common Property Types and Formats

### Simple Properties
- **title** (string): Page title, shown as large heading
- **rich_text** (string): Text field
- **url** (string): URL field
- **email** (string): Email field
- **phone_number** (string): Phone number
- **checkbox** (string): Use `"__YES__"` or `"__NO__"`
- **number** (number): Use JavaScript numbers, not strings

### Select Properties
```typescript
// single_select: Just use the option name
properties: {
  Status: "In Progress"  // Must match exact option name
}

// multi_select: Single string or comma-separated
// ❌ WRONG: ["option1", "option2"]  // Don't use arrays
// ❌ WRONG: "option1,option2"       // Don't use commas
// ✅ CORRECT: Need to use separate API calls or specific format
```

### Date Properties
```typescript
// Date properties use expanded format with three keys
properties: {
  "date:Due Date:start": "2025-01-30",
  "date:Due Date:end": null,  // Optional end date
  "date:Due Date:is_datetime": 0  // 0 for date, 1 for datetime
}
```

### Place Properties
```typescript
// Place/location properties use expanded format
properties: {
  "place:Office:name": "HQ",
  "place:Office:address": "123 Main St",
  "place:Office:latitude": 37.7749,
  "place:Office:longitude": -122.4194,
  "place:Office:google_place_id": "optional-id"
}
```

### Special Property Names
Properties named "id" or "url" (case-insensitive) must be prefixed with "userDefined:":
```typescript
properties: {
  "userDefined:id": "value",
  "userDefined:URL": "https://example.com"
}
```

## Multi-Select Fields - CRITICAL

**Common mistake**: Multi-select fields have strict validation. When creating or updating pages in a database with multi_select properties:

1. **Fetch the database first** to see available options:
   ```typescript
   const db = await notion_notion-fetch({ id: "database-id" });
   // Response shows: "Tags": {"options": [{"name": "Option1"}, {"name": "Option2"}]}
   ```

2. **Use only valid option names**:
   ```typescript
   properties: {
     Tags: "Option1"  // Single option as string
   }
   ```

3. **For multiple options**: Currently the API has limitations. Best practice:
   - Create the page with one tag
   - Update it with additional tags if needed
   - Or pass multiple tags separated by specific format (check database schema)

4. **Error handling**: If you get "Invalid multi_select value", check:
   - Is the option name spelled exactly as shown in database?
   - Are you passing a string, not an array?
   - Does the database schema allow this option?

## Database Operations

### Fetch Database Schema
```typescript
const db = await notion_notion-fetch({
  id: "database-id-or-url"
});

// Returns:
// - Database title and icon
// - Data sources (collections) within the database
// - Schema for each data source
// - Views available
```

### Creating Databases
```typescript
const db = await notion_notion-create-database({
  title: [{type: "text", text: {content: "My Database"}}],
  parent: {page_id: "parent-page-id"},
  properties: {
    "Task Name": {type: "title"},
    "Status": {
      type: "select",
      select: {
        options: [
          {name: "To Do", color: "red"},
          {name: "In Progress", color: "yellow"},
          {name: "Done", color: "green"}
        ]
      }
    },
    "Due Date": {type: "date"}
  }
});
```

### Updating Database Schema
```typescript
await notion_notion-update-database({
  database_id: "db-id",
  title: [{type: "text", text: {content: "New Title"}}],
  properties: {
    "New Property": {type: "rich_text"},
    "Property to Rename": {name: "Renamed Property"},
    "Property to Delete": null  // Set to null to remove
  }
});
```

## Content (Markdown) Guidelines

### Supported Markdown
- **Headings**: `# H1`, `## H2`, etc.
- **Lists**: Unordered `- item`, ordered `1. item`
- **Code**: Inline `` `code` `` and code blocks
- **Bold/Italic**: `**bold**`, `*italic*`
- **Links**: `[text](url)`
- **Tables**: Full markdown table support
- **Quotes**: `> quoted text`
- **Toggles/Collapsible**: `▶ Collapsed content\n\tHidden items` (Note: indentation with tabs)

### Toggle/Collapsible Sections
Toggles are created with the `▶` character followed by content that should be hidden:

```markdown
▶ Click to expand
	Hidden content line 1
	Hidden content line 2
	- Nested list item
```

**Important**: Content after `▶` must be indented with tabs or spaces.

### Rich Text Annotations
Content can include color and style annotations:

```markdown
# Heading {color="blue"}
Some text {color="red"} and {bold="true"}
```

## Search and Navigation

### Search Notion
```typescript
const results = await notion_notion-search({
  query: "search term",
  query_type: "internal"  // or "user" for user search
});

// Filter by creation date
const filtered = await notion_notion-search({
  query: "recent docs",
  filters: {
    created_date_range: {
      start_date: "2025-01-01",
      end_date: "2025-01-31"
    }
  }
});
```

### Fetch Teams and Users
```typescript
// List teams
const teams = await notion_notion-get-teams({
  query: "engineering"  // optional search
});

// List users
const users = await notion_notion-get-users({
  query: "john",  // optional search
  page_size: 100
});

// Get specific user
const user = await notion_notion-get-users({
  user_id: "user-id-or-self"
});
```

## Error Handling

### Common Errors and Solutions

#### "Invalid multi_select value"
**Cause**: Option name doesn't exist or format is wrong
**Solution**: 
1. Fetch database to see valid options
2. Use exact option names
3. Pass as string, not array

#### "Invalid input" / Validation error
**Cause**: Wrong property format or type
**Solution**:
1. Check property type in database schema
2. Use correct format (e.g., date properties need date:Property:start format)
3. Verify special names use userDefined: prefix

#### "Page not found"
**Cause**: Wrong ID or insufficient permissions
**Solution**:
1. Verify page/database ID is correct
2. Check you have access to the resource
3. Use full URL if ID doesn't work

#### "Unauthorized"
**Cause**: Notion integration doesn't have permission
**Solution**:
1. Verify integration is shared with the database/page
2. Check integration scopes in Notion settings
3. Re-authenticate if needed

## Best Practices

1. **Always fetch first**: Before creating content in a database, fetch the database to understand its schema
2. **Validate option names**: Multi-select options are strictly validated—check exact spellings
3. **Use data_source_id for databases**: When a database has multiple data sources, use `data_source_id` instead of `database_id` as parent
4. **Handle IDs flexibly**: Most tools accept page IDs with or without dashes
5. **Content indentation**: Toggle/collapsible content must use tabs or spaces for indentation
6. **Break up complex updates**: Large content updates are safer when split into smaller operations
7. **Test with simple cases first**: Before complex automation, test with a single page/field
8. **Document environment**: Store Notion integration tokens securely, never in git

## Advanced Patterns

See [references/advanced-patterns.md](references/advanced-patterns.md) for:
- Batch operations and performance optimization
- Syncing external data to Notion
- Creating dynamic databases and views
- Handling relationships and rollups
- Complex filtering and sorting
