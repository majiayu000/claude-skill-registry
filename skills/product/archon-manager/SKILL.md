---
name: Archon Manager
description: Master Archon MCP for strategic project management, task tracking, and knowledge base operations. The strategic layer (WHAT/WHEN) that coordinates with Skills (HOW). Use when managing projects, tracking tasks, querying knowledge bases, or implementing the Archon+Skills two-layer architecture.
version: 1.0.0
category: project-management
tags:
  - project-management
  - knowledge-management
  - task-tracking
  - rag
  - strategic-planning
related_skills:
  - rag-implementer
  - knowledge-base-manager
  - mvp-builder
  - product-strategist
  - multi-agent-architect
triggers:
  - archon-manager
  - archon manager
  - archon
  - project management mcp
  - task tracking
supports_mcps:
  - archon-mcp
required_tools: []
required_integrations:
  - supabase
  - openai
---

# Archon Manager

**Master Archon MCP for strategic project management and knowledge operations.**

Archon is the command center for AI coding assistants, providing:

- **Strategic Layer**: Project management, task tracking, priority-based workflow (WHAT/WHEN)
- **Knowledge Layer**: RAG queries, web crawling, document processing, code examples
- **Integration Layer**: Connects Claude Code, Cursor, Windsurf with unified context

**The Two-Layer Architecture**:

- **Archon** (this skill) = Strategic (WHAT to build, WHEN)
- **Skills** = Tactical (HOW to build well)
- Together = Optimal outcomes

---

## When to Use This Skill

- **Project Setup**: Creating hierarchical projects with features and tasks
- **Task Management**: Priority-based workflow (P0/P1/P2), status tracking
- **Knowledge Queries**: RAG searches across documentation, code examples, PDFs
- **Strategic Planning**: Using Archon to decide WHAT to build next
- **Two-Layer Workflow**: Implementing Archon (strategic) + Skills (tactical) pattern
- **Context Preservation**: Maintaining project knowledge across sessions
- **AI Coordination**: Synchronizing multiple AI assistants on same project

---

## Core Concepts

### 1. The Two-Layer Architecture

```
┌──────────────────────────────────────────────────┐
│           ARCHON MCP SERVER                      │
│           (Strategic Layer)                      │
│                                                  │
│  • Project management & task tracking           │
│  • Priority-based workflow (P0/P1/P2)          │
│  • Knowledge queries (RAG)                      │
│  • Code example search                          │
│  • Progress tracking & metrics                  │
│  • Context preservation                         │
└─────────────────┬────────────────────────────────┘
                  │
                  │ invokes when needed
                  ↓
┌──────────────────────────────────────────────────┐
│      AI-DEV-STANDARDS SKILLS                     │
│      (Tactical Layer)                            │
│                                                  │
│  • Domain-specific expertise                    │
│  • Implementation patterns                      │
│  • Quality standards                            │
│  • Best practices                               │
└──────────────────────────────────────────────────┘
```

**Key Insight**: Archon manages WHAT to build and WHEN, Skills guide HOW to build it well.

### 2. Hierarchical Project Structure

```
Project
├── Feature 1
│   ├── Task 1.1 (P0)
│   ├── Task 1.2 (P1)
│   └── Task 1.3 (P2)
├── Feature 2
│   ├── Task 2.1 (P0)
│   └── Task 2.2 (P1)
└── Knowledge Base
    ├── Web pages
    ├── PDFs
    ├── Code examples
    └── Documentation
```

### 3. Priority-Based Workflow

- **P0 (Critical)**: Must have for core value prop, blocks everything
- **P1 (High Value)**: Important but can wait, high impact
- **P2 (Nice to Have)**: Enhancement, low priority

### 4. Knowledge Management

- **Web Crawling**: Automatic sitemap detection, intelligent scraping
- **Document Processing**: PDFs with intelligent chunking
- **Code Examples**: Extract from documentation
- **Semantic Search**: Vector-based RAG with embeddings
- **Source Organization**: Tags, categories, versions

---

## 6-Phase Archon Implementation

### Phase 1: Setup & Configuration

**Goal**: Install and configure Archon for your project

#### 1.1 Prerequisites

```bash
# Required
- Docker Desktop (running)
- Node.js 18+
- Supabase account (cloud: https://supabase.com or local)
- LLM API key (OpenAI, Gemini, or Ollama)
```

#### 1.2 Installation

```bash
# Clone Archon
git clone https://github.com/coleam00/Archon.git
cd Archon

# Create .env file
cp .env.example .env

# Edit .env with your credentials
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
OPENAI_API_KEY=your-openai-key  # or GEMINI_API_KEY, OLLAMA_URL

# Set up database (run SQL migrations in Supabase SQL Editor)
# See: database/migrations/

# Start Archon
docker compose up --build -d

# Verify running
# Frontend: http://localhost:3737
# API: http://localhost:8181
# MCP: http://localhost:8051
```

#### 1.3 Connect to AI Assistant

**For Claude Code** (.claude/mcp-settings.json):

```json
{
  "mcpServers": {
    "archon": {
      "command": "node",
      "args": ["/path/to/archon/mcp-server/dist/index.js"],
      "env": {
        "ARCHON_API_URL": "http://localhost:8181"
      }
    }
  }
}
```

**For Cursor/Windsurf**: Similar MCP configuration in settings

#### 1.4 Verify Connection

```typescript
// Test Archon connection
archon: list_projects()
// Should return empty list or existing projects
```

---

### Phase 2: Project Creation

**Goal**: Set up hierarchical project structure

#### 2.1 Create Project

```typescript
// Using Archon MCP tool
archon: create_project({
  name: 'My Application',
  description: 'Full-stack web application for task management',
  status: 'active',
  metadata: {
    tech_stack: ['Next.js', 'Supabase', 'TypeScript'],
    team_size: 1,
    target_launch: '2025-12-01'
  }
})

// Returns: { project_id: "uuid", name: "My Application", ... }
```

#### 2.2 Add Features

```typescript
// Create major features
archon: create_feature({
  project_id: 'uuid',
  name: 'User Authentication',
  description: 'Complete auth system with email/OAuth',
  priority: 'P0',
  estimated_effort: '2 days'
})

archon: create_feature({
  project_id: 'uuid',
  name: 'Task Management',
  description: 'CRUD operations for tasks',
  priority: 'P0',
  estimated_effort: '3 days'
})

archon: create_feature({
  project_id: 'uuid',
  name: 'Team Collaboration',
  description: 'Share tasks with team members',
  priority: 'P1',
  estimated_effort: '4 days'
})
```

#### 2.3 Break Down Features into Tasks

```typescript
// Use AI-assisted task generation
archon: generate_tasks({
  feature_id: 'auth-feature-uuid',
  instructions: 'Break down authentication into implementation tasks',
  use_ai: true
})

// Or create manually
archon: create_task({
  feature_id: 'auth-feature-uuid',
  title: 'Implement email/password signup',
  description: 'Create signup form, API endpoint, database schema',
  priority: 'P0',
  status: 'todo',
  estimated_hours: 4,
  skills_to_use: ['api-designer', 'security-engineer', 'frontend-builder']
})
```

---

### Phase 3: Knowledge Base Setup

**Goal**: Build comprehensive knowledge base for AI queries

#### 3.1 Add Web Documentation

```typescript
// Crawl entire documentation site
archon: crawl_website({
  url: 'https://nextjs.org/docs',
  max_depth: 3,
  follow_sitemap: true,
  tags: ['nextjs', 'documentation']
})

// Archon automatically:
// - Detects sitemap
// - Crawls pages
// - Extracts text
// - Chunks intelligently
// - Generates embeddings
// - Stores in vector database
```

#### 3.2 Add PDF Documents

```typescript
// Upload PDFs (design docs, specs, research papers)
archon: add_document({
  file_path: '/path/to/architecture-spec.pdf',
  type: 'pdf',
  tags: ['architecture', 'design'],
  project_id: 'uuid'
})

// Archon automatically:
// - Extracts text from PDF
// - Chunks by sections/pages
// - Generates embeddings
// - Indexes for search
```

#### 3.3 Add Code Examples

```typescript
// Extract code examples from repos or docs
archon: extract_code_examples({
  source_url: 'https://github.com/vercel/next.js/tree/canary/examples',
  tags: ['nextjs', 'examples'],
  language_filter: ['typescript', 'javascript']
})
```

#### 3.4 Organize Knowledge

```typescript
// Tag and categorize
archon: update_source({
  source_id: 'uuid',
  tags: ['authentication', 'security', 'best-practices'],
  category: 'implementation-guides',
  version: '1.0'
})
```

---

### Phase 4: The Archon+Skills Workflow

**Goal**: Use two-layer architecture for optimal development

#### 4.1 Phase 1: Strategic Planning (Archon)

**Goal**: Understand WHAT to build and WHY

```typescript
// 1. Get next priority task
const task = archon:get_next_task({
  project_id: "uuid",
  filter_by: "status",
  filter_value: "todo",
  sort_by: "priority"  // P0 first
})
// → { id: "P0-3", title: "Implement User Authentication", priority: "P0" }

// 2. Get task details
const details = archon:get_task({
  task_id: "P0-3"
})
// → Complete task info: description, requirements, dependencies

// 3. Research the domain (RAG query)
const research = archon:perform_rag_query({
  query: "JWT authentication Next.js best practices",
  project_id: "uuid",
  match_count: 5
})
// → Top 5 most relevant knowledge base entries with context

// 4. Find code examples
const examples = archon:search_code_examples({
  query: "auth middleware Next.js TypeScript",
  match_count: 3
})
// → Relevant code examples from knowledge base

// 5. Mark as doing
archon:update_task({
  task_id: "P0-3",
  updates: { status: "doing" }
})
```

#### 4.2 Phase 2: Tactical Execution (Skills)

**Goal**: Implement with domain expertise and best practices

```typescript
// 6. Identify required skills (from task.skills_to_use)
// → ["api-designer", "security-engineer", "frontend-builder"]

// 7. Invoke skills for guidance
// (AI assistant automatically invokes these skills based on context)

// 8. Implement following both:
//    - Archon research (RAG results + code examples)
//    - Skill guidance (best practices + patterns)

// 9. Build the feature
```

#### 4.3 Phase 3: Quality Validation

**Goal**: Ensure quality before marking complete

```typescript
// 10. Apply quality checks
// - Invoke testing-strategist skill
// - Invoke security-engineer skill
// - Run tests, validate security

// 11. Update task to review
archon:update_task({
  task_id: "P0-3",
  updates: { status: "review" }
})

// 12. After user validation → mark done
archon:update_task({
  task_id: "P0-3",
  updates: { status: "done" }
})

// 13. Get next task
const nextTask = archon:get_next_task({
  project_id: "uuid",
  filter_by: "status",
  filter_value: "todo"
})
// → Repeat cycle
```

---

### Phase 5: Advanced Knowledge Operations

**Goal**: Leverage Archon's RAG capabilities

#### 5.1 Semantic Search Patterns

```typescript
// Broad research query
archon: perform_rag_query({
  query: 'How to implement real-time features in Next.js',
  match_count: 10,
  similarity_threshold: 0.7
})

// Specific technical query
archon: perform_rag_query({
  query: 'Next.js middleware authentication example code',
  match_count: 3,
  filter_tags: ['nextjs', 'authentication', 'code-example']
})

// Architecture decision query
archon: perform_rag_query({
  query: 'PostgreSQL vs MongoDB for user data',
  match_count: 5,
  filter_tags: ['database', 'architecture']
})
```

#### 5.2 Context-Aware Queries

```typescript
// Query within project context
archon: perform_rag_query({
  query: 'How should we structure our authentication?',
  project_id: 'uuid', // Uses project's knowledge base
  match_count: 5
})

// Query specific feature context
archon: perform_rag_query({
  query: 'Best practices for this feature',
  feature_id: 'auth-feature-uuid',
  match_count: 3
})
```

#### 5.3 Knowledge Base Versioning

```typescript
// Version project documentation
archon: create_doc_version({
  project_id: 'uuid',
  document_name: 'Architecture Decision Record',
  content: '...',
  version: '1.0.0',
  tags: ['architecture', 'decisions']
})

// Query historical context
archon: get_doc_history({
  project_id: 'uuid',
  document_name: 'Architecture Decision Record'
})
```

---

### Phase 6: Progress Tracking & Metrics

**Goal**: Monitor project health and velocity

#### 6.1 Project Metrics

```typescript
// Get project overview
archon: get_project_metrics({
  project_id: 'uuid'
})
// Returns:
// {
//   total_features: 5,
//   total_tasks: 23,
//   p0_tasks: 8,
//   p1_tasks: 10,
//   p2_tasks: 5,
//   tasks_by_status: {
//     todo: 15,
//     doing: 3,
//     review: 2,
//     done: 3
//   },
//   completion_percentage: 13,
//   knowledge_base_entries: 147
// }
```

#### 6.2 Velocity Tracking

```typescript
// Tasks completed per week
archon: get_velocity({
  project_id: 'uuid',
  time_period: 'week'
})

// Burndown chart data
archon: get_burndown({
  project_id: 'uuid',
  sprint_id: 'sprint-1'
})
```

#### 6.3 Real-Time Updates

Archon uses Socket.IO for real-time progress updates:

- Task status changes
- Knowledge base additions
- Project metrics updates
- Team collaboration events

---

## Integration Patterns

### Pattern 1: Solo Developer Workflow

```typescript
// Morning routine
const nextTask = archon:get_next_task({ project_id: "uuid" })
const research = archon:perform_rag_query({
  query: nextTask.title + " implementation",
  match_count: 5
})

// Work on task (using Skills for implementation)
// ...

// End of day
archon:update_task({ task_id: nextTask.id, status: "review" })
```

### Pattern 2: Team Collaboration

```typescript
// Team lead creates project structure
archon: create_project({ name: 'Team Project' })
archon: create_feature({ name: 'Backend API', assigned_to: 'developer-1' })
archon: create_feature({ name: 'Frontend UI', assigned_to: 'developer-2' })

// Each team member queries same knowledge base
archon: perform_rag_query({ query: '...', project_id: 'uuid' })

// Real-time sync of task status across team
```

### Pattern 3: Multi-AI-Assistant Setup

```typescript
// Claude Code for implementation
// Cursor for refactoring
// Windsurf for testing

// All connected to same Archon instance
// Same project, same tasks, same knowledge base
// Coordinated through Archon's unified context
```

---

## Archon MCP Tools Reference

### Project Management

```typescript
// Projects
archon: create_project({ name, description, status, metadata })
archon: list_projects()
archon: get_project({ project_id })
archon: update_project({ project_id, updates })
archon: delete_project({ project_id })

// Features
archon: create_feature({ project_id, name, description, priority })
archon: list_features({ project_id })
archon: update_feature({ feature_id, updates })

// Tasks
archon: create_task({ feature_id, title, description, priority, status })
archon: get_next_task({ project_id, filter_by, sort_by })
archon: get_task({ task_id })
archon: update_task({ task_id, updates })
archon: list_tasks({ project_id, filter_by, filter_value })
archon: generate_tasks({ feature_id, instructions, use_ai })
```

### Knowledge Management

```typescript
// RAG Queries
archon:perform_rag_query({query, project_id?, match_count, similarity_threshold, filter_tags?})
archon:search_code_examples({query, match_count, language_filter?})

// Content Ingestion
archon:crawl_website({url, max_depth, follow_sitemap, tags})
archon:add_document({file_path, type, tags, project_id})
archon:extract_code_examples({source_url, tags, language_filter})

// Knowledge Base Management
archon:list_sources({project_id, filter_tags?})
archon:update_source({source_id, tags, category, version})
archon:delete_source({source_id})
```

### Metrics & Analytics

```typescript
archon: get_project_metrics({ project_id })
archon: get_velocity({ project_id, time_period })
archon: get_burndown({ project_id, sprint_id })
```

---

## Best Practices

### 1. Start with Clear Project Structure

```typescript
// Good: Hierarchical and organized
Project: "E-commerce Platform"
├── Feature: "User Authentication" (P0)
│   ├── Task: "Implement signup" (P0)
│   ├── Task: "Implement login" (P0)
│   └── Task: "Password reset" (P1)
├── Feature: "Product Catalog" (P0)
│   ├── Task: "Product CRUD API" (P0)
│   ├── Task: "Product listing UI" (P0)
│   └── Task: "Search functionality" (P1)

// Bad: Flat, disorganized
- Task: "Build everything"
- Task: "Make it work"
- Task: "Deploy"
```

### 2. Use Priority Effectively

**P0 (Critical)**: Must have for MVP, blocks everything

- Core value proposition features
- Critical bugs
- Security vulnerabilities

**P1 (High Value)**: Important, high impact

- Significant enhancements
- Important optimizations
- Major integrations

**P2 (Nice to Have)**: Can wait

- Polish and refinement
- Minor features
- Non-critical improvements

### 3. Build Comprehensive Knowledge Base

```typescript
// Add diverse sources
archon: crawl_website({ url: 'https://docs.framework.com' })
archon: add_document({ file_path: 'architecture-spec.pdf' })
archon: extract_code_examples({ source_url: 'https://github.com/...' })

// Tag consistently
tags: ['category', 'technology', 'type']
// e.g., ["authentication", "nextjs", "tutorial"]
```

### 4. Use RAG Queries Strategically

```typescript
// Before starting task
const research = archon:perform_rag_query({
  query: "How to implement " + task.title,
  match_count: 5
})

// During implementation (specific questions)
const answer = archon:perform_rag_query({
  query: "How to handle edge case X",
  match_count: 3
})

// Architecture decisions
const guidance = archon:perform_rag_query({
  query: "Should I use pattern A or pattern B for ...",
  match_count: 5
})
```

### 5. Maintain Task Status Discipline

```
todo → doing → review → done
```

- **todo**: Not started
- **doing**: Currently working on (limit to 1-3 tasks)
- **review**: Ready for validation
- **done**: Completed and validated

Update status immediately when changing.

---

## Troubleshooting

### Issue: Archon Not Connecting

**Symptoms**: MCP tools not available in AI assistant

**Solutions**:

1. Check Docker containers running: `docker ps`
2. Verify ports not blocked: 3737, 8181, 8051, 8052
3. Check MCP configuration in `.claude/mcp-settings.json`
4. Restart AI assistant after config changes
5. Check Archon logs: `docker logs archon-api`

### Issue: RAG Queries Return No Results

**Symptoms**: Empty results from `perform_rag_query`

**Solutions**:

1. Verify knowledge base has content: `archon:list_sources()`
2. Check embeddings generated (wait for processing)
3. Lower `similarity_threshold` (default 0.7, try 0.5)
4. Broader query terms
5. Check source tags match `filter_tags`

### Issue: Tasks Not Appearing

**Symptoms**: `get_next_task` returns empty

**Solutions**:

1. Verify project exists: `archon:list_projects()`
2. Check task status filters
3. Ensure tasks created for correct feature/project
4. Verify tasks not all marked "done"

### Issue: Slow Performance

**Symptoms**: RAG queries or task operations slow

**Solutions**:

1. Check Docker resource allocation
2. Optimize knowledge base (remove duplicates)
3. Use `match_count` appropriately (5-10, not 100)
4. Consider upgrading Supabase plan (if cloud)
5. Use local Ollama instead of API calls

---

## Integration with ai-dev-standards

### Using Archon + Skills Together

**Archon provides** (Strategic):

- WHAT to build (task from priority queue)
- WHEN to build it (P0/P1/P2 ordering)
- Context (RAG queries, project knowledge)

**Skills provide** (Tactical):

- HOW to build well (best practices, patterns)
- Domain expertise (security, performance, etc.)
- Quality standards (testing, validation)

**Example Workflow**:

```typescript
// 1. Strategic (Archon)
const task = archon:get_next_task({project_id: "uuid"})
const research = archon:perform_rag_query({query: task.title})
archon:update_task({task_id: task.id, status: "doing"})

// 2. Tactical (Skills)
// AI automatically invokes: api-designer, security-engineer, frontend-builder
// Based on task.skills_to_use

// 3. Implementation
// Build following: Archon research + Skill guidance

// 4. Quality (Skills)
// AI invokes: testing-strategist, security-engineer

// 5. Complete (Archon)
archon:update_task({task_id: task.id, status: "done"})
```

### Task-to-Skill Mapping

When creating tasks in Archon, specify `skills_to_use`:

```typescript
archon: create_task({
  title: 'Implement authentication API',
  skills_to_use: ['api-designer', 'security-engineer']
  // ...
})
```

This tells AI assistants which skills to invoke during implementation.

---

## Success Metrics

You're using Archon effectively when:

1. ✅ **Clear project structure**: Hierarchical, organized, prioritized
2. ✅ **Always know what's next**: `get_next_task` guides daily work
3. ✅ **Rich knowledge base**: RAG queries return relevant, useful results
4. ✅ **Visible progress**: Metrics show steady completion
5. ✅ **Status discipline**: Tasks flow smoothly through workflow
6. ✅ **Context preserved**: Can resume project after breaks without loss
7. ✅ **Quality maintained**: Two-layer workflow (Archon + Skills) produces excellent results

---

## Quick Reference

### Common Commands

```typescript
// Daily workflow
archon: get_next_task({ project_id })
archon: perform_rag_query({ query, match_count: 5 })
archon: update_task({ task_id, status: 'doing' })
// ... work ...
archon: update_task({ task_id, status: 'done' })

// Project setup
archon: create_project({ name, description })
archon: create_feature({ project_id, name, priority: 'P0' })
archon: create_task({ feature_id, title, priority: 'P0' })

// Knowledge building
archon: crawl_website({ url, tags })
archon: add_document({ file_path, tags })

// Progress tracking
archon: get_project_metrics({ project_id })
archon: list_tasks({ project_id, filter_by: 'status', filter_value: 'done' })
```

### Priority Guidelines

- **P0**: Core features, critical bugs, security issues
- **P1**: Important enhancements, optimizations, integrations
- **P2**: Polish, minor features, nice-to-haves

### Status Flow

```
todo → doing (working) → review (validate) → done (complete)
```

---

## Summary

Archon is the strategic command center that:

- Manages WHAT to build and WHEN (priority queue)
- Provides context through RAG (knowledge base)
- Tracks progress and metrics
- Coordinates AI assistants

Combined with Skills (HOW to build well), Archon enables:

- Strategic coherence (all work aligned with goals)
- Tactical excellence (domain expertise + best practices)
- Context preservation (no lost knowledge)
- Quality assurance (multi-layer validation)

**Key Takeaway**: Use Archon for strategic planning (WHAT/WHEN), invoke Skills for implementation guidance (HOW). Together they create optimal outcomes.

**For detailed integration patterns**: See `DOCS/ARCHON-INTEGRATION.md`
**For complete example**: See `EXAMPLES/archon-workflow-example.md`
