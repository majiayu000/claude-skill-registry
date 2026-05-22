---
name: notion-api
version: 1.0.0
description: Notion API for workspace automation including databases, pages, blocks, query/filter syntax, and integration patterns
author: workspace-hub
category: productivity
type: skill
capabilities:
  - database_operations
  - page_management
  - block_manipulation
  - query_filtering
  - property_types
  - relation_rollups
  - search_api
  - integration_patterns
tools:
  - notion-api
  - notion-client
  - curl
  - jq
tags: [notion, api, databases, pages, blocks, automation, productivity, workspace, integration]
platforms: [rest-api, python, javascript, web]
related_skills:
  - api-integration
  - todoist-api
  - obsidian
  - webhook-automation
---

# Notion API Integration Skill

Master the Notion API for workspace automation, including databases, pages, blocks, query/filter syntax, and integration patterns. This skill covers the official REST API and Python SDK for building powerful Notion integrations.

## When to Use This Skill

### USE Notion API when:
- Automating database entries and updates
- Building custom dashboards from Notion data
- Syncing data between Notion and external systems
- Creating pages programmatically from templates
- Querying databases with complex filters
- Building integrations with other productivity tools
- Generating reports from Notion databases
- Implementing workflow automations

### DON'T USE Notion API when:
- Need real-time sync (API has rate limits)
- Building chat/messaging features (use Slack API)
- Need file storage solution (use dedicated storage)
- Simple task management only (use Todoist API)
- Need offline-first solution (use Obsidian)
- Require sub-second response times

## Prerequisites

### Create Integration

```markdown
1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name: "My Integration"
4. Select workspace
5. Set capabilities (Read/Write content, etc.)
6. Copy the "Internal Integration Token"
```

### Connect Integration to Pages

```markdown
1. Open the Notion page/database you want to access
2. Click "..." menu (top right)
3. Click "Connections" > "Connect to" > Your integration
4. Integration can now access this page and children
```

### Environment Setup

```bash
# Set environment variable
export NOTION_API_KEY="secret_xxxxxxxxxxxxxxxxxxxxx"

# Verify connection
curl -s "https://api.notion.com/v1/users/me" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" | jq
```

### Python SDK Installation

```bash
# Install official Python client
pip install notion-client

# Or with uv
uv pip install notion-client

# Additional dependencies
pip install python-dotenv requests
```

### Verify Setup

```python
from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])

# Test connection
me = notion.users.me()
print(f"Connected as: {me['name']}")

# List accessible databases
databases = notion.search(filter={"property": "object", "value": "database"})
print(f"Found {len(databases['results'])} databases")
```

## Core Capabilities

### 1. Database Operations

**List and Search Databases:**
```bash
# Search for databases
curl -s -X POST "https://api.notion.com/v1/search" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{
        "filter": {
            "property": "object",
            "value": "database"
        }
    }' | jq '.results[] | {id: .id, title: .title[0].plain_text}'

# Get database schema
curl -s "https://api.notion.com/v1/databases/DATABASE_ID" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" | jq '.properties'
```

**Python - Database Operations:**
```python
from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])

# Search for databases
results = notion.search(
    filter={"property": "object", "value": "database"}
)

for db in results["results"]:
    title = db["title"][0]["plain_text"] if db["title"] else "Untitled"
    print(f"Database: {title} (ID: {db['id']})")

# Get database details
database = notion.databases.retrieve(database_id="your-database-id")
print(f"Properties: {list(database['properties'].keys())}")

# Create database
new_db = notion.databases.create(
    parent={"type": "page_id", "page_id": "parent-page-id"},
    title=[{"type": "text", "text": {"content": "Tasks Database"}}],
    properties={
        "Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "To Do", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Done", "color": "green"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "gray"}
                ]
            }
        },
        "Due Date": {"date": {}},
        "Assignee": {"people": {}},
        "Tags": {"multi_select": {"options": []}},
        "Completed": {"checkbox": {}},
        "Notes": {"rich_text": {}}
    }
)
print(f"Created database: {new_db['id']}")

# Update database
notion.databases.update(
    database_id="your-database-id",
    title=[{"type": "text", "text": {"content": "Updated Title"}}],
    properties={
        "New Property": {"rich_text": {}}
    }
)
```

### 2. Query Databases

**Basic Query:**
```bash
# Query all items
curl -s -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{}' | jq '.results'

# Query with filter
curl -s -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{
        "filter": {
            "property": "Status",
            "select": {
                "equals": "In Progress"
            }
        }
    }' | jq '.results'

# Query with sort
curl -s -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{
        "sorts": [
            {
                "property": "Due Date",
                "direction": "ascending"
            }
        ]
    }' | jq '.results'
```

**Python - Query Operations:**
```python
# Simple query
results = notion.databases.query(database_id="your-database-id")
for page in results["results"]:
    props = page["properties"]
    name = props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else "Untitled"
    print(f"- {name}")

# Query with filter
results = notion.databases.query(
    database_id="your-database-id",
    filter={
        "property": "Status",
        "select": {
            "equals": "In Progress"
        }
    }
)

# Query with multiple filters (AND)
results = notion.databases.query(
    database_id="your-database-id",
    filter={
        "and": [
            {
                "property": "Status",
                "select": {"equals": "In Progress"}
            },
            {
                "property": "Priority",
                "select": {"equals": "High"}
            }
        ]
    }
)

# Query with OR filter
results = notion.databases.query(
    database_id="your-database-id",
    filter={
        "or": [
            {"property": "Status", "select": {"equals": "To Do"}},
            {"property": "Status", "select": {"equals": "In Progress"}}
        ]
    }
)

# Query with sorting
results = notion.databases.query(
    database_id="your-database-id",
    sorts=[
        {"property": "Priority", "direction": "ascending"},
        {"property": "Due Date", "direction": "ascending"}
    ]
)

# Paginated query
def query_all_pages(database_id, filter=None):
    """Query all pages with pagination"""
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.databases.query(
            database_id=database_id,
            filter=filter,
            start_cursor=start_cursor,
            page_size=100
        )
        all_results.extend(response["results"])
        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")

    return all_results

all_items = query_all_pages("your-database-id")
print(f"Total items: {len(all_items)}")
```

### 3. Filter Syntax Reference

**Text Filters:**
```python
# Text property filters
{"property": "Name", "title": {"equals": "Exact Match"}}
{"property": "Name", "title": {"does_not_equal": "Not This"}}
{"property": "Name", "title": {"contains": "partial"}}
{"property": "Name", "title": {"does_not_contain": "exclude"}}
{"property": "Name", "title": {"starts_with": "Prefix"}}
{"property": "Name", "title": {"ends_with": "suffix"}}
{"property": "Name", "title": {"is_empty": True}}
{"property": "Name", "title": {"is_not_empty": True}}

# Rich text property
{"property": "Notes", "rich_text": {"contains": "keyword"}}
```

**Number Filters:**
```python
{"property": "Amount", "number": {"equals": 100}}
{"property": "Amount", "number": {"does_not_equal": 0}}
{"property": "Amount", "number": {"greater_than": 50}}
{"property": "Amount", "number": {"less_than": 100}}
{"property": "Amount", "number": {"greater_than_or_equal_to": 10}}
{"property": "Amount", "number": {"less_than_or_equal_to": 99}}
{"property": "Amount", "number": {"is_empty": True}}
{"property": "Amount", "number": {"is_not_empty": True}}
```

**Date Filters:**
```python
{"property": "Due Date", "date": {"equals": "2025-01-17"}}
{"property": "Due Date", "date": {"before": "2025-01-20"}}
{"property": "Due Date", "date": {"after": "2025-01-10"}}
{"property": "Due Date", "date": {"on_or_before": "2025-01-17"}}
{"property": "Due Date", "date": {"on_or_after": "2025-01-01"}}
{"property": "Due Date", "date": {"is_empty": True}}
{"property": "Due Date", "date": {"is_not_empty": True}}

# Relative date filters
{"property": "Due Date", "date": {"past_week": {}}}
{"property": "Due Date", "date": {"past_month": {}}}
{"property": "Due Date", "date": {"past_year": {}}}
{"property": "Due Date", "date": {"next_week": {}}}
{"property": "Due Date", "date": {"next_month": {}}}
{"property": "Due Date", "date": {"next_year": {}}}
{"property": "Due Date", "date": {"this_week": {}}}
```

**Select/Multi-Select Filters:**
```python
# Select
{"property": "Status", "select": {"equals": "Done"}}
{"property": "Status", "select": {"does_not_equal": "Done"}}
{"property": "Status", "select": {"is_empty": True}}
{"property": "Status", "select": {"is_not_empty": True}}

# Multi-select
{"property": "Tags", "multi_select": {"contains": "urgent"}}
{"property": "Tags", "multi_select": {"does_not_contain": "archived"}}
{"property": "Tags", "multi_select": {"is_empty": True}}
{"property": "Tags", "multi_select": {"is_not_empty": True}}
```

**Checkbox Filters:**
```python
{"property": "Completed", "checkbox": {"equals": True}}
{"property": "Completed", "checkbox": {"equals": False}}
```

**Relation and Rollup Filters:**
```python
# Relation
{"property": "Project", "relation": {"contains": "page-id"}}
{"property": "Project", "relation": {"does_not_contain": "page-id"}}
{"property": "Project", "relation": {"is_empty": True}}
{"property": "Project", "relation": {"is_not_empty": True}}

# Rollup (depends on rollup type)
{"property": "Total Tasks", "rollup": {"number": {"greater_than": 5}}}
{"property": "Completion", "rollup": {"number": {"equals": 100}}}
```

**Compound Filters:**
```python
# AND
{
    "and": [
        {"property": "Status", "select": {"equals": "In Progress"}},
        {"property": "Priority", "select": {"equals": "High"}},
        {"property": "Due Date", "date": {"before": "2025-02-01"}}
    ]
}

# OR
{
    "or": [
        {"property": "Status", "select": {"equals": "To Do"}},
        {"property": "Status", "select": {"equals": "In Progress"}}
    ]
}

# Nested (AND with OR)
{
    "and": [
        {
            "or": [
                {"property": "Priority", "select": {"equals": "High"}},
                {"property": "Priority", "select": {"equals": "Medium"}}
            ]
        },
        {"property": "Status", "select": {"does_not_equal": "Done"}}
    ]
}
```

### 4. Page Operations

**Create Pages:**
```bash
# Create page in database
curl -s -X POST "https://api.notion.com/v1/pages" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d '{
        "parent": {"database_id": "DATABASE_ID"},
        "properties": {
            "Name": {
                "title": [{"text": {"content": "New Task"}}]
            },
            "Status": {
                "select": {"name": "To Do"}
            },
            "Priority": {
                "select": {"name": "High"}
            },
            "Due Date": {
                "date": {"start": "2025-01-20"}
            }
        }
    }' | jq
```

**Python - Page Operations:**
```python
# Create page in database
new_page = notion.pages.create(
    parent={"database_id": "your-database-id"},
    properties={
        "Name": {
            "title": [{"text": {"content": "New Task"}}]
        },
        "Status": {
            "select": {"name": "To Do"}
        },
        "Priority": {
            "select": {"name": "High"}
        },
        "Due Date": {
            "date": {"start": "2025-01-20", "end": "2025-01-25"}
        },
        "Tags": {
            "multi_select": [
                {"name": "development"},
                {"name": "urgent"}
            ]
        },
        "Assignee": {
            "people": [{"id": "user-id"}]
        },
        "Notes": {
            "rich_text": [{"text": {"content": "Task description here"}}]
        },
        "Completed": {
            "checkbox": False
        },
        "Amount": {
            "number": 100
        },
        "URL": {
            "url": "https://example.com"
        },
        "Email": {
            "email": "user@example.com"
        }
    }
)
print(f"Created page: {new_page['id']}")

# Create page with content (blocks)
new_page = notion.pages.create(
    parent={"database_id": "your-database-id"},
    properties={
        "Name": {"title": [{"text": {"content": "Page with Content"}}]}
    },
    children=[
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Overview"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "This is the content."}}]
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Task item"}}],
                "checked": False
            }
        }
    ]
)

# Retrieve page
page = notion.pages.retrieve(page_id="page-id")
print(f"Page: {page['properties']['Name']['title'][0]['plain_text']}")

# Update page properties
notion.pages.update(
    page_id="page-id",
    properties={
        "Status": {"select": {"name": "Done"}},
        "Completed": {"checkbox": True}
    }
)

# Archive page (soft delete)
notion.pages.update(
    page_id="page-id",
    archived=True
)

# Restore page
notion.pages.update(
    page_id="page-id",
    archived=False
)
```

### 5. Block Operations

**Block Types:**
```python
# Paragraph
{
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Text content"}}]
    }
}

# Headings
{
    "type": "heading_1",
    "heading_1": {
        "rich_text": [{"type": "text", "text": {"content": "Heading 1"}}]
    }
}
# Also: heading_2, heading_3

# Bulleted list
{
    "type": "bulleted_list_item",
    "bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "List item"}}]
    }
}

# Numbered list
{
    "type": "numbered_list_item",
    "numbered_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "Item 1"}}]
    }
}

# To-do
{
    "type": "to_do",
    "to_do": {
        "rich_text": [{"type": "text", "text": {"content": "Task"}}],
        "checked": False
    }
}

# Toggle
{
    "type": "toggle",
    "toggle": {
        "rich_text": [{"type": "text", "text": {"content": "Toggle header"}}],
        "children": []  # Nested blocks
    }
}

# Code block
{
    "type": "code",
    "code": {
        "rich_text": [{"type": "text", "text": {"content": "print('hello')"}}],
        "language": "python"
    }
}

# Quote
{
    "type": "quote",
    "quote": {
        "rich_text": [{"type": "text", "text": {"content": "Quote text"}}]
    }
}

# Callout
{
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "Important note"}}],
        "icon": {"emoji": "💡"}
    }
}

# Divider
{
    "type": "divider",
    "divider": {}
}

# Table of contents
{
    "type": "table_of_contents",
    "table_of_contents": {}
}
```

**Python - Block Operations:**
```python
# Get page blocks (children)
blocks = notion.blocks.children.list(block_id="page-id")
for block in blocks["results"]:
    print(f"Block type: {block['type']}")

# Append blocks to page
notion.blocks.children.append(
    block_id="page-id",
    children=[
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "New Section"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Some "}},
                    {"type": "text", "text": {"content": "bold"}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": " text."}}
                ]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "First item"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Second item"}}]
            }
        }
    ]
)

# Update block
notion.blocks.update(
    block_id="block-id",
    paragraph={
        "rich_text": [{"type": "text", "text": {"content": "Updated content"}}]
    }
)

# Delete block
notion.blocks.delete(block_id="block-id")

# Get all blocks recursively
def get_all_blocks(block_id):
    """Recursively get all blocks"""
    all_blocks = []
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.blocks.children.list(
            block_id=block_id,
            start_cursor=start_cursor,
            page_size=100
        )
        for block in response["results"]:
            all_blocks.append(block)
            if block.get("has_children"):
                children = get_all_blocks(block["id"])
                all_blocks.extend(children)
        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")

    return all_blocks

all_blocks = get_all_blocks("page-id")
print(f"Total blocks: {len(all_blocks)}")
```

### 6. Rich Text Formatting

**Rich Text Structure:**
```python
# Basic text
{"type": "text", "text": {"content": "Plain text"}}

# Styled text
{
    "type": "text",
    "text": {"content": "Styled text"},
    "annotations": {
        "bold": True,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "red"  # default, gray, brown, orange, yellow, green, blue, purple, pink, red
    }
}

# Link
{
    "type": "text",
    "text": {
        "content": "Click here",
        "link": {"url": "https://example.com"}
    }
}

# Mention user
{
    "type": "mention",
    "mention": {
        "type": "user",
        "user": {"id": "user-id"}
    }
}

# Mention page
{
    "type": "mention",
    "mention": {
        "type": "page",
        "page": {"id": "page-id"}
    }
}

# Mention date
{
    "type": "mention",
    "mention": {
        "type": "date",
        "date": {"start": "2025-01-17"}
    }
}

# Equation
{
    "type": "equation",
    "equation": {"expression": "E = mc^2"}
}
```

**Python - Rich Text Helper:**
```python
def create_rich_text(text, bold=False, italic=False, code=False, color="default", link=None):
    """Helper to create rich text objects"""
    rt = {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "strikethrough": False,
            "underline": False,
            "code": code,
            "color": color
        }
    }
    if link:
        rt["text"]["link"] = {"url": link}
    return rt

# Usage
paragraph_content = [
    create_rich_text("This is "),
    create_rich_text("bold", bold=True),
    create_rich_text(" and "),
    create_rich_text("italic", italic=True),
    create_rich_text(" text with a "),
    create_rich_text("link", link="https://example.com"),
    create_rich_text(".")
]

notion.blocks.children.append(
    block_id="page-id",
    children=[{
        "type": "paragraph",
        "paragraph": {"rich_text": paragraph_content}
    }]
)
```

### 7. Relations and Rollups

**Create Related Databases:**
```python
# Create Projects database
projects_db = notion.databases.create(
    parent={"type": "page_id", "page_id": "parent-page-id"},
    title=[{"type": "text", "text": {"content": "Projects"}}],
    properties={
        "Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Active", "color": "green"},
                    {"name": "Completed", "color": "gray"}
                ]
            }
        }
    }
)

# Create Tasks database with relation to Projects
tasks_db = notion.databases.create(
    parent={"type": "page_id", "page_id": "parent-page-id"},
    title=[{"type": "text", "text": {"content": "Tasks"}}],
    properties={
        "Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "To Do", "color": "gray"},
                    {"name": "Done", "color": "green"}
                ]
            }
        },
        "Project": {
            "relation": {
                "database_id": projects_db["id"],
                "single_property": {}
            }
        }
    }
)

# Add rollup to Projects for task count
notion.databases.update(
    database_id=projects_db["id"],
    properties={
        "Task Count": {
            "rollup": {
                "relation_property_name": "Tasks",  # This is auto-created
                "rollup_property_name": "Name",
                "function": "count"
            }
        }
    }
)

# Create task linked to project
notion.pages.create(
    parent={"database_id": tasks_db["id"]},
    properties={
        "Name": {"title": [{"text": {"content": "Task 1"}}]},
        "Status": {"select": {"name": "To Do"}},
        "Project": {"relation": [{"id": "project-page-id"}]}
    }
)
```

### 8. Search API

**Search Operations:**
```python
# Search all
results = notion.search()
print(f"Total accessible items: {len(results['results'])}")

# Search with query
results = notion.search(query="project plan")
for item in results["results"]:
    obj_type = item["object"]
    if obj_type == "page":
        title = item["properties"].get("title", {}).get("title", [{}])[0].get("plain_text", "Untitled")
    elif obj_type == "database":
        title = item["title"][0]["plain_text"] if item["title"] else "Untitled"
    print(f"{obj_type}: {title}")

# Search only pages
results = notion.search(
    query="meeting",
    filter={"property": "object", "value": "page"}
)

# Search only databases
results = notion.search(
    filter={"property": "object", "value": "database"}
)

# Search with sorting
results = notion.search(
    query="report",
    sort={
        "direction": "descending",
        "timestamp": "last_edited_time"
    }
)

# Paginated search
def search_all(query=None, filter=None):
    """Search with pagination"""
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.search(
            query=query,
            filter=filter,
            start_cursor=start_cursor,
            page_size=100
        )
        all_results.extend(response["results"])
        has_more = response["has_more"]
        start_cursor = response.get("next_cursor")

    return all_results
```

## Complete Examples

### Example 1: Task Management System

```python
#!/usr/bin/env python3
"""notion_tasks.py - Complete task management with Notion"""

from notion_client import Client
from datetime import datetime, timedelta
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])

class NotionTaskManager:
    def __init__(self, database_id):
        self.database_id = database_id

    def create_task(self, name, status="To Do", priority="Medium",
                    due_date=None, tags=None, notes=None):
        """Create a new task"""
        properties = {
            "Name": {"title": [{"text": {"content": name}}]},
            "Status": {"select": {"name": status}},
            "Priority": {"select": {"name": priority}}
        }

        if due_date:
            properties["Due Date"] = {"date": {"start": due_date}}

        if tags:
            properties["Tags"] = {
                "multi_select": [{"name": tag} for tag in tags]
            }

        if notes:
            properties["Notes"] = {
                "rich_text": [{"text": {"content": notes}}]
            }

        return notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

    def get_tasks_by_status(self, status):
        """Get all tasks with given status"""
        return notion.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Status",
                "select": {"equals": status}
            }
        )

    def get_overdue_tasks(self):
        """Get all overdue tasks"""
        today = datetime.now().strftime("%Y-%m-%d")
        return notion.databases.query(
            database_id=self.database_id,
            filter={
                "and": [
                    {"property": "Due Date", "date": {"before": today}},
                    {"property": "Status", "select": {"does_not_equal": "Done"}}
                ]
            }
        )

    def get_high_priority_tasks(self):
        """Get high priority incomplete tasks"""
        return notion.databases.query(
            database_id=self.database_id,
            filter={
                "and": [
                    {"property": "Priority", "select": {"equals": "High"}},
                    {"property": "Status", "select": {"does_not_equal": "Done"}}
                ]
            },
            sorts=[
                {"property": "Due Date", "direction": "ascending"}
            ]
        )

    def complete_task(self, page_id):
        """Mark task as done"""
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"select": {"name": "Done"}},
                "Completed": {"checkbox": True}
            }
        )

    def update_task_status(self, page_id, status):
        """Update task status"""
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"select": {"name": status}}
            }
        )

    def get_weekly_summary(self):
        """Get summary for the week"""
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # Completed this week
        completed = notion.databases.query(
            database_id=self.database_id,
            filter={
                "and": [
                    {"property": "Status", "select": {"equals": "Done"}},
                    {"property": "Last edited time", "date": {"after": week_ago}}
                ]
            }
        )

        # Due this week
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        upcoming = notion.databases.query(
            database_id=self.database_id,
            filter={
                "and": [
                    {"property": "Due Date", "date": {"on_or_before": next_week}},
                    {"property": "Status", "select": {"does_not_equal": "Done"}}
                ]
            }
        )

        return {
            "completed_count": len(completed["results"]),
            "upcoming_count": len(upcoming["results"]),
            "completed": completed["results"],
            "upcoming": upcoming["results"]
        }

# Usage
if __name__ == "__main__":
    tm = NotionTaskManager("your-database-id")

    # Create task
    task = tm.create_task(
        name="Review Q1 report",
        priority="High",
        due_date="2025-01-20",
        tags=["work", "quarterly"],
        notes="Review and provide feedback"
    )
    print(f"Created task: {task['id']}")

    # Get overdue tasks
    overdue = tm.get_overdue_tasks()
    print(f"\nOverdue tasks: {len(overdue['results'])}")
    for t in overdue["results"]:
        name = t["properties"]["Name"]["title"][0]["plain_text"]
        print(f"  - {name}")

    # Weekly summary
    summary = tm.get_weekly_summary()
    print(f"\nWeekly Summary:")
    print(f"  Completed: {summary['completed_count']}")
    print(f"  Upcoming: {summary['upcoming_count']}")
```

### Example 2: Content Management System

```python
#!/usr/bin/env python3
"""notion_cms.py - Content management with Notion"""

from notion_client import Client
from datetime import datetime
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])

class NotionCMS:
    def __init__(self, content_db_id, categories_db_id=None):
        self.content_db_id = content_db_id
        self.categories_db_id = categories_db_id

    def create_article(self, title, content_blocks, status="Draft",
                       category=None, tags=None, author=None):
        """Create a new article"""
        properties = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Status": {"select": {"name": status}},
            "Created": {"date": {"start": datetime.now().isoformat()}}
        }

        if category:
            properties["Category"] = {"select": {"name": category}}

        if tags:
            properties["Tags"] = {
                "multi_select": [{"name": tag} for tag in tags]
            }

        if author:
            properties["Author"] = {
                "rich_text": [{"text": {"content": author}}]
            }

        return notion.pages.create(
            parent={"database_id": self.content_db_id},
            properties=properties,
            children=content_blocks
        )

    def create_article_with_template(self, title, template="blog"):
        """Create article from template"""
        templates = {
            "blog": [
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Introduction"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Main Content"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Conclusion"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
            ],
            "tutorial": [
                {"type": "callout", "callout": {
                    "rich_text": [{"text": {"content": "Prerequisites: "}}],
                    "icon": {"emoji": "📋"}
                }},
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Overview"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Step 1"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
                {"type": "code", "code": {"rich_text": [{"text": {"content": "# code here"}}], "language": "python"}},
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Step 2"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
                {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Summary"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ""}}]}},
            ]
        }

        return self.create_article(
            title=title,
            content_blocks=templates.get(template, templates["blog"]),
            status="Draft"
        )

    def get_published_articles(self, category=None, limit=10):
        """Get published articles"""
        filter_conditions = [
            {"property": "Status", "select": {"equals": "Published"}}
        ]

        if category:
            filter_conditions.append(
                {"property": "Category", "select": {"equals": category}}
            )

        return notion.databases.query(
            database_id=self.content_db_id,
            filter={"and": filter_conditions} if len(filter_conditions) > 1 else filter_conditions[0],
            sorts=[{"property": "Created", "direction": "descending"}],
            page_size=limit
        )

    def publish_article(self, page_id):
        """Publish an article"""
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Status": {"select": {"name": "Published"}},
                "Published Date": {"date": {"start": datetime.now().isoformat()}}
            }
        )

    def export_article_to_markdown(self, page_id):
        """Export article content to markdown"""
        page = notion.pages.retrieve(page_id)
        blocks = notion.blocks.children.list(block_id=page_id)

        title = page["properties"]["Title"]["title"][0]["plain_text"]
        markdown = f"# {title}\n\n"

        for block in blocks["results"]:
            markdown += self._block_to_markdown(block)

        return markdown

    def _block_to_markdown(self, block):
        """Convert block to markdown"""
        block_type = block["type"]

        if block_type == "paragraph":
            text = self._rich_text_to_markdown(block["paragraph"]["rich_text"])
            return f"{text}\n\n"
        elif block_type == "heading_1":
            text = self._rich_text_to_markdown(block["heading_1"]["rich_text"])
            return f"# {text}\n\n"
        elif block_type == "heading_2":
            text = self._rich_text_to_markdown(block["heading_2"]["rich_text"])
            return f"## {text}\n\n"
        elif block_type == "heading_3":
            text = self._rich_text_to_markdown(block["heading_3"]["rich_text"])
            return f"### {text}\n\n"
        elif block_type == "bulleted_list_item":
            text = self._rich_text_to_markdown(block["bulleted_list_item"]["rich_text"])
            return f"- {text}\n"
        elif block_type == "numbered_list_item":
            text = self._rich_text_to_markdown(block["numbered_list_item"]["rich_text"])
            return f"1. {text}\n"
        elif block_type == "code":
            text = self._rich_text_to_markdown(block["code"]["rich_text"])
            lang = block["code"]["language"]
            return f"```{lang}\n{text}\n```\n\n"
        elif block_type == "quote":
            text = self._rich_text_to_markdown(block["quote"]["rich_text"])
            return f"> {text}\n\n"
        elif block_type == "divider":
            return "---\n\n"

        return ""

    def _rich_text_to_markdown(self, rich_text):
        """Convert rich text array to markdown"""
        result = ""
        for rt in rich_text:
            text = rt.get("text", {}).get("content", "")
            annotations = rt.get("annotations", {})

            if annotations.get("bold"):
                text = f"**{text}**"
            if annotations.get("italic"):
                text = f"*{text}*"
            if annotations.get("code"):
                text = f"`{text}`"
            if annotations.get("strikethrough"):
                text = f"~~{text}~~"

            link = rt.get("text", {}).get("link")
            if link:
                text = f"[{text}]({link['url']})"

            result += text
        return result

# Usage
if __name__ == "__main__":
    cms = NotionCMS("your-content-database-id")

    # Create article from template
    article = cms.create_article_with_template(
        title="Getting Started with Python",
        template="tutorial"
    )
    print(f"Created article: {article['id']}")

    # Get published articles
    published = cms.get_published_articles(limit=5)
    print(f"\nPublished articles: {len(published['results'])}")

    # Export to markdown
    md = cms.export_article_to_markdown("article-page-id")
    print(md)
```

### Example 3: Project Dashboard

```python
#!/usr/bin/env python3
"""notion_dashboard.py - Project dashboard with Notion"""

from notion_client import Client
from datetime import datetime, timedelta
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])

def generate_project_dashboard(projects_db_id, tasks_db_id):
    """Generate project dashboard data"""

    # Get all active projects
    projects = notion.databases.query(
        database_id=projects_db_id,
        filter={
            "property": "Status",
            "select": {"equals": "Active"}
        }
    )

    dashboard_data = []

    for project in projects["results"]:
        project_id = project["id"]
        project_name = project["properties"]["Name"]["title"][0]["plain_text"]

        # Get tasks for this project
        tasks = notion.databases.query(
            database_id=tasks_db_id,
            filter={
                "property": "Project",
                "relation": {"contains": project_id}
            }
        )

        # Calculate metrics
        total_tasks = len(tasks["results"])
        completed = sum(1 for t in tasks["results"]
                       if t["properties"]["Status"]["select"]["name"] == "Done")
        in_progress = sum(1 for t in tasks["results"]
                        if t["properties"]["Status"]["select"]["name"] == "In Progress")

        # Get overdue tasks
        today = datetime.now().strftime("%Y-%m-%d")
        overdue = sum(1 for t in tasks["results"]
                     if t["properties"].get("Due Date", {}).get("date", {}).get("start", "9999-99-99") < today
                     and t["properties"]["Status"]["select"]["name"] != "Done")

        dashboard_data.append({
            "project_id": project_id,
            "project_name": project_name,
            "total_tasks": total_tasks,
            "completed": completed,
            "in_progress": in_progress,
            "pending": total_tasks - completed - in_progress,
            "overdue": overdue,
            "completion_rate": round(completed / total_tasks * 100, 1) if total_tasks > 0 else 0
        })

    return dashboard_data

def create_dashboard_page(parent_page_id, dashboard_data):
    """Create a dashboard page with metrics"""

    # Build blocks for dashboard
    blocks = [
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"text": {"content": f"Project Dashboard - {datetime.now().strftime('%Y-%m-%d')}"}}]
            }
        },
        {
            "type": "divider",
            "divider": {}
        }
    ]

    for project in dashboard_data:
        blocks.extend([
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": project["project_name"]}}]
                }
            },
            {
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "text": {
                            "content": f"Completion: {project['completion_rate']}% | "
                                      f"Tasks: {project['completed']}/{project['total_tasks']} | "
                                      f"In Progress: {project['in_progress']} | "
                                      f"Overdue: {project['overdue']}"
                        }
                    }],
                    "icon": {"emoji": "📊"}
                }
            }
        ])

        # Add progress bar representation
        progress = int(project['completion_rate'] / 10)
        progress_bar = "🟩" * progress + "⬜" * (10 - progress)
        blocks.append({
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": f"Progress: {progress_bar}"}}]
            }
        })

    # Create the page
    return notion.pages.create(
        parent={"page_id": parent_page_id},
        properties={
            "title": {"title": [{"text": {"content": "Project Dashboard"}}]}
        },
        children=blocks
    )

# Usage
if __name__ == "__main__":
    data = generate_project_dashboard(
        projects_db_id="projects-database-id",
        tasks_db_id="tasks-database-id"
    )

    print("Project Dashboard")
    print("=" * 50)
    for project in data:
        print(f"\n{project['project_name']}")
        print(f"  Completion: {project['completion_rate']}%")
        print(f"  Tasks: {project['completed']}/{project['total_tasks']}")
        print(f"  In Progress: {project['in_progress']}")
        print(f"  Overdue: {project['overdue']}")
```

## Integration Examples

### Integration with Slack

```python
#!/usr/bin/env python3
"""slack_notion.py - Sync Slack messages to Notion"""

import os
import requests
from notion_client import Client

notion = Client(auth=os.environ["NOTION_API_KEY"])
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK_URL"]

def notify_slack_on_page_update(page_id, message):
    """Send Slack notification when Notion page is updated"""
    page = notion.pages.retrieve(page_id)
    title = page["properties"]["Name"]["title"][0]["plain_text"]

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Notion Update*: {title}\n{message}"
                }
            },
            {
                "type": "actions",
                "elements": [{
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View in Notion"},
                    "url": page["url"]
                }]
            }
        ]
    }

    requests.post(SLACK_WEBHOOK, json=payload)

def create_notion_page_from_slack(database_id, title, content, channel):
    """Create Notion page from Slack message"""
    return notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Source": {"select": {"name": "Slack"}},
            "Channel": {"rich_text": [{"text": {"content": channel}}]}
        },
        children=[{
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": content}}]
            }
        }]
    )
```

### Integration with GitHub

```python
#!/usr/bin/env python3
"""github_notion.py - Sync GitHub issues to Notion"""

import os
import requests
from notion_client import Client

notion = Client(auth=os.environ["NOTION_API_KEY"])
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

def sync_github_issues_to_notion(repo, database_id):
    """Sync GitHub issues to Notion database"""
    # Fetch issues from GitHub
    response = requests.get(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    issues = response.json()

    for issue in issues:
        # Check if issue already exists in Notion
        existing = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "GitHub ID",
                "number": {"equals": issue["number"]}
            }
        )

        properties = {
            "Name": {"title": [{"text": {"content": issue["title"]}}]},
            "GitHub ID": {"number": issue["number"]},
            "Status": {
                "select": {"name": "Open" if issue["state"] == "open" else "Closed"}
            },
            "URL": {"url": issue["html_url"]},
            "Labels": {
                "multi_select": [{"name": l["name"]} for l in issue["labels"]]
            }
        }

        if existing["results"]:
            # Update existing
            notion.pages.update(
                page_id=existing["results"][0]["id"],
                properties=properties
            )
        else:
            # Create new
            notion.pages.create(
                parent={"database_id": database_id},
                properties=properties,
                children=[{
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": issue.get("body", "") or ""}}]
                    }
                }]
            )

    print(f"Synced {len(issues)} issues from {repo}")
```

## Best Practices

### 1. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_second=3):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

# Usage
@rate_limit(calls_per_second=3)
def api_call(func, *args, **kwargs):
    return func(*args, **kwargs)
```

### 2. Error Handling

```python
from notion_client import APIResponseError

def safe_notion_call(func, *args, max_retries=3, **kwargs):
    """Execute Notion API call with retry logic"""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except APIResponseError as e:
            if e.status == 429:
                # Rate limited
                wait_time = int(e.headers.get("Retry-After", 60))
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            elif e.status >= 500:
                # Server error, retry
                time.sleep(2 ** attempt)
            else:
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise

    raise Exception(f"Failed after {max_retries} retries")
```

### 3. Batch Operations

```python
def batch_create_pages(database_id, pages_data, batch_size=10):
    """Create pages in batches to avoid rate limits"""
    results = []
    for i in range(0, len(pages_data), batch_size):
        batch = pages_data[i:i + batch_size]
        for page_data in batch:
            result = notion.pages.create(
                parent={"database_id": database_id},
                properties=page_data["properties"],
                children=page_data.get("children", [])
            )
            results.append(result)
        if i + batch_size < len(pages_data):
            time.sleep(1)  # Brief pause between batches
    return results
```

### 4. Caching

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path.home() / ".cache" / "notion"
CACHE_TTL = timedelta(minutes=5)

def get_cached_or_fetch(key, fetch_func, ttl=CACHE_TTL):
    """Get from cache or fetch fresh data"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{key}.json"

    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at < ttl:
            return data["value"]

    value = fetch_func()
    cache_data = {
        "cached_at": datetime.now().isoformat(),
        "value": value
    }
    cache_file.write_text(json.dumps(cache_data, default=str))
    return value
```

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
```python
# Verify API key
curl -s "https://api.notion.com/v1/users/me" \
    -H "Authorization: Bearer $NOTION_API_KEY" \
    -H "Notion-Version: 2022-06-28"

# Check if integration is connected to the page/database
# Go to page > ... menu > Connections > Your integration
```

**Issue: 404 Not Found**
```python
# Ensure integration has access to the page
# The integration must be explicitly connected to each page

# For databases, check the database ID is correct
# Database ID format: 32 hex characters (with or without hyphens)
```

**Issue: 400 Bad Request**
```python
# Check property names match exactly (case-sensitive)
# Verify property types match the database schema

# Common mistakes:
# - Using "title" instead of actual title property name
# - Wrong select/multi_select option names
# - Invalid date format (use ISO 8601: "2025-01-17")
```

**Issue: Rate limiting (429)**
```python
# Notion allows ~3 requests/second
# Implement exponential backoff
# Check Retry-After header for wait time
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-17 | Initial release with comprehensive Notion API coverage |

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [API Reference](https://developers.notion.com/reference/intro)
- [Python SDK](https://github.com/ramnes/notion-sdk-py)
- [JavaScript SDK](https://github.com/makenotion/notion-sdk-js)
- [Integration Gallery](https://www.notion.so/integrations)
- [API Changelog](https://developers.notion.com/changelog)

---

*This skill enables powerful workspace automation through Notion's comprehensive API, supporting databases, pages, blocks, queries, and integration patterns.*
