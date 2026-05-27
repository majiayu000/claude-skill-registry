---
name: build-jira-document-format
description: |
  Builds complex ADF (Atlassian Document Format) documents with advanced patterns, templates, and specialized builders. Use when creating sophisticated Jira descriptions, epics with structure, rich content documents, or implementing builder patterns for fluent APIs. Trigger keywords: "ADF template", "document builder", "complex description", "fluent API", "epic structure", "formatted issue", "rich content", "builder pattern", "EpicBuilder", "IssueBuilder", "document template", "nested content", "advanced formatting". Works with Python 3.10+, jira_tool.formatter module, and Jira REST API v3.
---

# Build Jira Document Format (Advanced)

## Purpose

Master advanced Atlassian Document Format patterns for creating sophisticated, reusable Jira documents. Learn the builder pattern for fluent APIs, create specialized templates (EpicBuilder, IssueBuilder), design complex nested structures, and build document templates that scale from individual issues to epic planning.

## When to Use This Skill

**Explicit Triggers:**
- "Create an ADF template for epics"
- "Build a document builder with fluent API"
- "Implement EpicBuilder for structured epics"
- "Design complex nested Jira document"
- "Create reusable Jira document templates"

**Implicit Triggers:**
- Repeatedly creating similar Jira documents manually
- Need consistent formatting across multiple issues/epics
- Building tools that generate Jira content programmatically
- Creating complex documents with code blocks, panels, and nested sections

**Debugging Scenarios:**
- "Why is my ADF document structure incorrect?"
- "How do I create nested panels with formatted content?"
- "Builder pattern not chaining correctly"

## Quick Start

Create a formatted epic with problem statement, technical details, and acceptance criteria:

```python
from jira_tool.formatter import EpicBuilder

# Create epic with builder
epic = EpicBuilder("Authentication Overhaul", "P0")
epic.add_problem_statement("Current auth is vulnerable to timing attacks")
epic.add_description("Implement OAuth2 with PKCE and secure session management")
epic.add_technical_details(
    requirements=[
        "PKCE flow support",
        "Session token encryption",
        "Rate limiting"
    ],
    code_example="""
    # OAuth2 flow
    token = oauth_client.get_token(code, pkce_verifier)
    session.set_secure_cookie(token)
    """
)
epic.add_acceptance_criteria([
    "All authentication tests pass",
    "Security audit complete",
    "Rate limiting works per RFC 6749"
])

# Get ADF for Jira API
adf = epic.build()
```

Or build step-by-step with the general-purpose builder:

```python
from jira_tool.formatter import JiraDocumentBuilder

doc = JiraDocumentBuilder()
doc.add_heading("Epic: Authentication System", 1)
doc.add_heading("Problem", 2)
doc.add_panel("warning",
    {"type": "paragraph", "content": [
        doc.add_text("Current authentication has security vulnerabilities")
    ]}
)
doc.add_heading("Approach", 2)
doc.add_bullet_list([
    "Implement OAuth2 with PKCE",
    "Use session token encryption",
    "Add rate limiting"
])

adf = doc.build()
```

## Instructions

### Step 1: Understand the Builder Pattern

The builder pattern solves the problem of constructing complex objects through method chaining.

**Without builder** (verbose and error-prone):
```python
doc = {
    "version": 1,
    "type": "doc",
    "content": [
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [{"type": "text", "text": "Title"}]
        }
    ]
}
```

**With builder** (readable and safe):
```python
doc = JiraDocumentBuilder()
doc.add_heading("Title", 1)
doc.add_paragraph(doc.add_text("Start: "), doc.bold("Bold"))
adf = doc.build()
```

**Builder Benefits:**
- **Fluent API** - Chain methods for readability
- **Safety** - Builders handle nesting automatically
- **Reusability** - Extend builders for custom layouts
- **Validation** - Catch errors early

### Step 2: Master JiraDocumentBuilder

**Method Chaining:**
```python
doc = JiraDocumentBuilder()
doc.add_heading("Title", 1) \
    .add_paragraph(doc.add_text("Introduction")) \
    .add_rule() \
    .add_heading("Section", 2) \
    .add_bullet_list(["Point 1", "Point 2"])

adf = doc.build()
```

**Key Methods:**

1. **Structural Elements:**
   ```python
   doc.add_heading("Text", level=1)      # Level 1-6
   doc.add_paragraph(content_nodes)       # Mixed content
   doc.add_rule()                         # Horizontal line
   ```

2. **Lists:**
   ```python
   doc.add_bullet_list(["Item 1", "Item 2"])
   doc.add_ordered_list(["First", "Second"], start=1)
   ```

3. **Code Blocks:**
   ```python
   doc.add_code_block("def hello(): pass", language="python")
   ```

4. **Panels** (colored boxes):
   ```python
   doc.add_panel("info", {"type": "paragraph", "content": [doc.add_text("Info")]})
   # Types: info, note, warning, success, error
   ```

5. **Text Formatting:**
   ```python
   doc.bold("Bold text")
   doc.italic("Italic text")
   doc.code("inline_code")
   doc.strikethrough("Deleted")
   doc.link("Click here", "https://...")
   doc.add_text("Plain text")
   ```

**Combining Formatting:**
```python
doc.add_paragraph(
    doc.bold("Important: "),
    doc.add_text("This is a "),
    doc.italic("complex"),
    doc.add_text(" message")
)
```

### Step 3: Create Specialized Builders

For repeated structures, create helper functions or specialized builders:

**Helper Function Pattern:**
```python
def add_titled_panel(builder, title, panel_type, content):
    """Add a heading followed by a panel."""
    builder.add_heading(title, 2)
    builder.add_panel(panel_type, {
        "type": "paragraph",
        "content": [builder.add_text(content)]
    })

# Usage
doc = JiraDocumentBuilder()
add_titled_panel(doc, "⚠️ Risks", "warning", "Performance impact on v1 API")
```

**EpicBuilder Pattern:**
```python
class EpicBuilder:
    """Pre-formatted epic template."""

    def __init__(self, title: str, priority: str = "P1"):
        self.builder = JiraDocumentBuilder()
        self.builder.add_heading(f"🎯 {title}", 1)
        self.builder.add_paragraph(
            self.builder.bold("Priority: "),
            self.builder.add_text(priority)
        )

    def add_problem_statement(self, statement: str):
        self.builder.add_heading("Problem Statement", 2)
        self.builder.add_panel("warning", {
            "type": "paragraph",
            "content": [self.builder.add_text(statement)]
        })
        return self

    def add_acceptance_criteria(self, criteria: list[str]):
        self.builder.add_heading("Acceptance Criteria", 2)
        self.builder.add_ordered_list(criteria)
        return self

    def build(self):
        return self.builder.build()
```

See **references/advanced-patterns.md** for full EpicBuilder and BugReportBuilder implementations with inheritance patterns, composition, and testing strategies.

### Step 4: Implement Builder Best Practices

**Return self for Chaining:**
```python
class CustomBuilder:
    def add_something(self) -> "CustomBuilder":
        # ... implementation
        return self  # Allow chaining
```

**Validate Before Building:**
```python
def build(self) -> dict:
    """Build and validate before returning."""
    if not self.title:
        raise ValueError("Title is required")
    if not self.builder.content:
        raise ValueError("Content is empty")
    return self.builder.build()
```

**Document Structure:**
```python
class DocumentTemplate:
    """
    Template for standard epic documentation.

    Structure:
    - Header (title, priority, timeline)
    - Problem statement (warning panel)
    - Solution approach (bullet list)
    - Technical requirements (ordered list)
    - Acceptance criteria (ordered list)
    """
    def __init__(self, title: str):
        pass
```

## Supporting Files

### References
- **references/advanced-patterns.md** - Builder inheritance, composition patterns, template methods, complex nested structures, performance considerations, testing strategies, full implementation examples for EpicBuilder and BugReportBuilder

### Examples
- **examples/epic-examples.md** - Database migration epic, two-factor authentication feature, bug report builder, authentication system epic, method chaining examples, complex nested structures with 6 complete working examples

## Expected Outcomes

**Successful Document Building:**
- ADF validates correctly with Jira API
- Documents render properly in Jira UI
- Builders return valid JSON structure
- Method chaining works smoothly

**Builder Template Creation:**
- Consistent structure across similar documents
- Reusable code reduces duplication
- Custom builders extend base functionality
- Validation catches errors early

## Requirements

### Core Requirements
- **Python 3.10+** (for type hints and dataclass improvements)
- **jira_tool.formatter module** containing:
  - `JiraDocumentBuilder` - General-purpose builder
  - `EpicBuilder` - Epic-specific template
  - `IssueBuilder` - Issue-specific template

### For Testing Builders
- **Jira REST API v3 access** (to submit built documents)
- **Environment variables**: `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`
- **Test project** where you can create issues

### Recommended Tools
- **jira_adf_validator**: `npm install -g jira-adf-validator`
- **Python json**: Built-in (for validating ADF structure)
- **curl**: For testing API submissions

## Red Flags to Avoid

- **Manual ADF Construction** - Use builders instead of raw dicts
- **No Validation** - Always validate before submitting to Jira
- **Builder Reuse** - Create new builder instance for each document
- **Missing Return self** - Breaks method chaining
- **Hardcoded Structure** - Use builders for flexibility
- **No Type Hints** - Type hints improve IDE support and catch errors
- **Verbose Paragraph Construction** - Use text helper methods
- **No Error Handling** - Catch validation errors in build()
- **Inconsistent Templates** - Use specialized builders for consistency

## See Also

- **work-with-adf** - Basic ADF concepts and structure
- **jira-api** - API endpoints for creating/updating documents
- **export-and-analyze-jira-data** - Generating report documents
- **src/jira_tool/formatter.py** - Full builder implementation reference

## Notes

- EpicBuilder and IssueBuilder are provided by jira_tool.formatter module
- ADF structure must have version:1, type:"doc", and content array
- Panels must contain content nodes (paragraphs, headings, etc.)
- Code blocks support language parameter for syntax highlighting
- Method chaining requires returning self from all builder methods
- Test builders with jira-adf-validator before submitting to Jira
- See references/advanced-patterns.md for builder inheritance, composition patterns, and full EpicBuilder/BugReportBuilder implementations
- See examples/epic-examples.md for 6 complete working examples including database migration, two-factor authentication, and complex nested structures
