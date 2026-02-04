---
name: archon-workflow
description: Task management with Archon MCP server. Manage projects, tasks, documents, and RAG knowledge base. Use for tracking work, organizing projects, searching documentation, and maintaining persistent context across sessions.
---

# Archon Workflow Skill

## Triggers

Use this skill when you see:
- archon, task, project, document
- rag, knowledge base, search docs
- task management, project tracking
- session context, persistent memory

## Instructions

### Core Concept

Archon is the PRIMARY task management system. It provides:
- **Projects**: Container for related work
- **Tasks**: Trackable work items with status
- **Documents**: Persistent knowledge storage
- **RAG**: Knowledge base search

**RULE**: Always use Archon over TodoWrite for task management.

### Project Management

#### Find Projects

```python
# List all projects
find_projects()

# Search projects
find_projects(query="authentication")

# Get specific project with full details
find_projects(project_id="proj-123")

# Get master projects only (no sub-projects)
find_projects(masters_only=True)

# Get sub-projects of a master
find_projects(parent_id="master-proj-123")
```

#### Create/Update Projects

```python
# Create standalone project
manage_project("create",
    title="User Authentication System",
    description="Implement OAuth2 and JWT authentication",
    github_repo="https://github.com/org/repo"
)

# Create sub-project under master
manage_project("create",
    title="Auth Backend",
    description="Backend authentication services",
    parent_id="master-proj-123"
)

# Update project
manage_project("update",
    project_id="proj-123",
    description="Updated scope and requirements"
)

# Delete project
manage_project("delete", project_id="proj-123")

# Move project (change parent)
manage_project("move",
    project_id="proj-123",
    new_parent_id="new-master-123"
)
```

### Task Management

#### Task Status Flow

```
todo -> doing -> review -> done
```

#### Find Tasks

```python
# All tasks
find_tasks()

# Search tasks
find_tasks(query="authentication")

# Get specific task
find_tasks(task_id="task-123")

# Filter by status
find_tasks(filter_by="status", filter_value="todo")
find_tasks(filter_by="status", filter_value="doing")

# Filter by project
find_tasks(filter_by="project", filter_value="proj-123")

# Filter by assignee
find_tasks(filter_by="assignee", filter_value="User")

# Include sub-project tasks
find_tasks(
    filter_by="project",
    filter_value="master-proj-123",
    include_sub_project_tasks=True
)

# Exclude completed
find_tasks(include_closed=False)
```

#### Create Tasks

```python
# Create task
manage_task("create",
    project_id="proj-123",
    title="Implement JWT token generation",
    description="""
    Create JWT token generation service.

    Requirements:
    - Support RS256 signing
    - Configurable expiration
    - Include user claims

    Acceptance Criteria:
    - [ ] Tokens validate correctly
    - [ ] Refresh tokens work
    - [ ] Tests passing
    """,
    assignee="User",
    feature="authentication"
)

# Create with priority (0-100, higher = more priority)
manage_task("create",
    project_id="proj-123",
    title="Critical security fix",
    description="Fix authentication bypass vulnerability",
    task_order=90
)
```

#### Update Tasks

```python
# Start working on task
manage_task("update",
    task_id="task-123",
    status="doing"
)

# Move to review
manage_task("update",
    task_id="task-123",
    status="review"
)

# Complete task
manage_task("update",
    task_id="task-123",
    status="done"
)

# Reassign task
manage_task("update",
    task_id="task-123",
    assignee="Claude"
)

# Update description
manage_task("update",
    task_id="task-123",
    description="Updated requirements..."
)

# Delete task
manage_task("delete", task_id="task-123")
```

### Document Management

Use documents for persistent knowledge that survives sessions.

#### Document Types
- `spec` - Technical specifications
- `design` - Design documents
- `note` - General notes
- `prp` - Product requirement prompts
- `api` - API documentation
- `guide` - How-to guides

#### Find Documents

```python
# All project documents
find_documents(project_id="proj-123")

# Search documents
find_documents(project_id="proj-123", query="authentication")

# Get specific document
find_documents(project_id="proj-123", document_id="doc-123")

# Filter by type
find_documents(project_id="proj-123", document_type="spec")
```

#### Create/Update Documents

```python
# Create document
manage_document("create",
    project_id="proj-123",
    title="Authentication Architecture",
    document_type="spec",
    content={
        "overview": "OAuth2 + JWT implementation",
        "components": ["auth-service", "token-service"],
        "decisions": [
            {"decision": "Use RS256", "reason": "Asymmetric for microservices"}
        ]
    },
    tags=["backend", "security"],
    author="Claude"
)

# Update document
manage_document("update",
    project_id="proj-123",
    document_id="doc-123",
    content={
        "overview": "Updated architecture...",
        "last_updated": "2024-01-15"
    }
)

# Delete document
manage_document("delete",
    project_id="proj-123",
    document_id="doc-123"
)
```

### RAG Knowledge Base

Search external documentation and code examples.

#### Get Available Sources

```python
# List all knowledge sources
rag_get_available_sources()
# Returns: sources with id, name, url
```

#### Search Knowledge Base

```python
# Search all sources (2-5 keywords work best)
rag_search_knowledge_base(
    query="React hooks useState",
    match_count=5
)

# Search specific source
rag_search_knowledge_base(
    query="authentication JWT",
    source_id="src_anthropic_docs",
    match_count=5
)

# Get raw chunks instead of pages
rag_search_knowledge_base(
    query="error handling",
    return_mode="chunks"
)
```

#### Search Code Examples

```python
# Find code examples
rag_search_code_examples(
    query="FastAPI middleware",
    match_count=5
)

# Filter by source
rag_search_code_examples(
    query="React context",
    source_id="src_react_docs"
)
```

#### Read Full Pages

```python
# After search, get full page content
rag_read_full_page(page_id="uuid-from-search")

# Or by URL
rag_read_full_page(url="https://docs.example.com/page")
```

#### List Pages for Source

```python
# Browse all pages in a source
rag_list_pages_for_source(source_id="src_123")

# Filter by section
rag_list_pages_for_source(
    source_id="src_123",
    section="# Getting Started"
)
```

### Session Workflow

#### Starting a Session

```python
# 1. Load project context
project = find_projects(project_id="proj-123")

# 2. Check current tasks
tasks = find_tasks(
    filter_by="project",
    filter_value="proj-123",
    include_closed=False
)

# 3. Load relevant documents
docs = find_documents(project_id="proj-123")

# 4. Start on a task
manage_task("update", task_id="task-123", status="doing")
```

#### During Work

```python
# Research using RAG
rag_search_knowledge_base(query="relevant topic")

# Update task as you progress
manage_task("update",
    task_id="task-123",
    description="Added: Implementation complete, testing needed"
)
```

#### Ending a Session

```python
# 1. Update task status
manage_task("update", task_id="task-123", status="review")

# 2. Save session context to document
manage_document("update",
    project_id="proj-123",
    document_id="session-context-doc",
    content={
        "last_session": "2024-01-15",
        "completed": ["Task A", "Task B"],
        "in_progress": ["Task C"],
        "blockers": ["Waiting on API access"],
        "next_steps": ["Complete Task C", "Start Task D"]
    }
)
```

### Best Practices

1. **Always Check Tasks First**: Start sessions by checking `find_tasks()`
2. **Update Status Promptly**: Move tasks through workflow as you work
3. **Use Documents for Context**: Persist important decisions and state
4. **RAG Before Implementing**: Search knowledge base before writing code
5. **Feature Labels**: Group related tasks with `feature` field
6. **Clear Descriptions**: Include acceptance criteria in task descriptions
7. **Save Before Clear**: Update documents before `/clear` or `/compact`
