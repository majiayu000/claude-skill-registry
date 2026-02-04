---
name: knowledge-base-system
version: "1.0.0"
category: coordination
description: "Knowledge Base System"
---

# Knowledge Base System

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Category:** workspace-hub
> **Related Skills:** repo-sync, workspace-cli, compliance-check

## Overview

The Knowledge Base System serves as the central intelligence layer for all 26+ repositories, AI agents, and human developers in workspace-hub. It provides unified access to documentation, standards, patterns, and learnings across the entire workspace ecosystem.

## Purpose

Create a searchable, AI-accessible knowledge base that:
- **Centralizes documentation** from all repositories
- **Captures patterns** and best practices
- **Enables AI agents** to learn from past work
- **Helps humans** find answers quickly
- **Continuously improves** through feedback loops

## When to Use

**Trigger this skill when:**
- Starting work on any repository
- Looking for patterns or examples
- Implementing standards or workflows
- Creating documentation
- Onboarding new team members or AI agents
- Resolving cross-repository questions

**Examples:**
- "How do I implement HTML reporting in this repo?"
- "What's the standard way to organize Python modules?"
- "Show me examples of YAML configuration patterns"
- "What AI agents should I use for this task?"
- "How was [feature] implemented in [other-repo]?"

## How It Works

### 1. Knowledge Base Structure

```
knowledge-base/
├── index/
│   ├── by-topic/           # Organized by subject matter
│   │   ├── ai-workflows/
│   │   ├── standards/
│   │   ├── patterns/
│   │   └── examples/
│   ├── by-repository/      # Organized by repository
│   │   ├── digitalmodel/
│   │   ├── worldenergydata/
│   │   └── ...
│   └── by-skill/           # Organized by skill type
│       ├── development/
│       ├── testing/
│       └── deployment/
├── patterns/
│   ├── workflow-patterns.md
│   ├── code-patterns.md
│   └── integration-patterns.md
├── standards/
│   ├── file-organization.md
│   ├── logging.md
│   ├── testing.md
│   └── html-reporting.md
├── examples/
│   ├── yaml-configs/
│   ├── pseudocode/
│   └── implementations/
└── learnings/
    ├── what-works.md
    ├── what-to-avoid.md
    └── optimization-tips.md
```

### 2. Data Sources

**Primary Sources:**
- `/mnt/github/workspace-hub/docs/` - All workspace documentation
- Each repository's `/docs/` directory
- `.agent-os/product/` - Product documentation
- `.agent-os/specs/` - Feature specifications
- `CLAUDE.md` files across all repos
- `README.md` files across all repos

**Metadata Sources:**
- Git history and commit messages
- PR descriptions and comments
- Issue discussions
- Test files and coverage reports
- CI/CD logs and metrics

### 3. Indexing Strategy

**Document Indexing:**
```python
# Index structure
{
    "document_id": "docs/modules/ai/AI_AGENT_GUIDELINES.md",
    "repository": "workspace-hub",
    "category": "standards",
    "tags": ["ai", "agents", "workflow", "mandatory"],
    "priority": "critical",
    "related_docs": [...],
    "last_updated": "2025-10-24",
    "usage_count": 147,
    "effectiveness_score": 0.95
}
```

**Pattern Indexing:**
```python
# Pattern structure
{
    "pattern_id": "development-workflow-yaml-to-code",
    "name": "YAML → Pseudocode → TDD → Code",
    "category": "workflow",
    "repositories_using": ["worldenergydata", "digitalmodel"],
    "effectiveness": 0.92,
    "examples": [...],
    "template_path": "templates/workflow/",
    "related_skills": ["development-workflow-orchestrator"]
}
```

### 4. Search Interface

**For AI Agents:**
```bash
# Search by topic
kb search --topic "html-reporting" --format structured

# Search by repository
kb search --repo digitalmodel --category standards

# Find examples
kb examples --pattern "YAML configuration" --language python

# Get related documents
kb related --doc "AI_AGENT_GUIDELINES.md" --depth 2
```

**For Humans:**
```bash
# Interactive search
kb search

# Quick lookup
kb lookup "how to create interactive plots"

# Show examples
kb examples "testing standards"

# Browse by category
kb browse --category standards
```

### 5. AI Agent Integration

**Automatic Context Loading:**
```python
# When AI agent starts task
def load_kb_context(task_description):
    """Load relevant KB context for task."""
    # Extract keywords from task
    keywords = extract_keywords(task_description)

    # Search KB for relevant docs
    docs = kb.search(keywords, limit=10)

    # Load related patterns
    patterns = kb.patterns.find_relevant(keywords)

    # Find similar examples
    examples = kb.examples.find_similar(task_description)

    return {
        "documentation": docs,
        "patterns": patterns,
        "examples": examples,
        "best_practices": kb.best_practices.for_keywords(keywords)
    }
```

**Feedback Loop:**
```python
# After task completion
def update_kb(task_result):
    """Update KB with learnings."""
    if task_result.success:
        kb.patterns.record_success(
            pattern=task_result.pattern_used,
            effectiveness=task_result.effectiveness_score
        )
        kb.examples.add(task_result.implementation)
    else:
        kb.learnings.record_failure(
            approach=task_result.approach,
            issue=task_result.error,
            resolution=task_result.fix
        )
```

## Implementation Steps

### Phase 1: Index Existing Documentation

1. **Scan all repositories:**
   ```bash
   # Scan workspace-hub
   kb init --scan /mnt/github/workspace-hub/docs/

   # Scan all repositories
   for repo in $(cat config/repos.conf); do
       kb index --repo "$repo" --scan docs/
   done
   ```

2. **Extract metadata:**
   - Document structure and headers
   - Cross-references between docs
   - Usage patterns from git history
   - Related code files

3. **Build search index:**
   - Full-text search
   - Tag-based search
   - Semantic search (embeddings)
   - Pattern matching

### Phase 2: Create Pattern Library

1. **Extract patterns from code:**
   ```python
   # Identify recurring patterns
   patterns = PatternExtractor().analyze(
       repos=all_repositories,
       types=["workflow", "code", "configuration", "integration"]
   )
   ```

2. **Document patterns:**
   - Pattern name and description
   - When to use / when not to use
   - Implementation template
   - Examples from repositories
   - Effectiveness metrics

3. **Link to implementations:**
   - Map patterns to actual code
   - Show variations across repos
   - Track success rates

### Phase 3: Build Search Interface

1. **CLI tool:**
   ```bash
   # Install KB CLI
   kb install

   # Interactive search
   kb search

   # Direct query
   kb query "YAML configuration patterns"
   ```

2. **AI Agent API:**
   ```python
   from workspace_kb import KnowledgeBase

   kb = KnowledgeBase()
   results = kb.search(
       query="HTML reporting standards",
       context="implementing new report",
       repository="digitalmodel"
   )
   ```

3. **Web Interface (future):**
   - Visual search and browse
   - Interactive pattern explorer
   - Real-time updates

### Phase 4: Continuous Learning

1. **Automatic updates:**
   ```bash
   # Git hook: after successful commit
   kb update --analyze-commit HEAD

   # CI/CD hook: after successful build
   kb update --analyze-build $BUILD_ID
   ```

2. **Effectiveness tracking:**
   - Pattern success rates
   - Document usefulness scores
   - AI agent performance correlation

3. **Feedback collection:**
   - User ratings on helpfulness
   - AI agent success with KB context
   - Gap identification

## Usage Examples

### Example 1: AI Agent Starting Task

```python
# AI agent receives task
task = "Implement interactive HTML report for analysis results"

# Load KB context
context = kb.load_context(task)

# AI discovers:
# 1. HTML_REPORTING_STANDARDS.md (MANDATORY: interactive only)
# 2. Pattern: "plotly-interactive-report"
# 3. Example: worldenergydata/reports/lower_tertiary_report.py
# 4. Best practice: CSV data with relative paths

# AI implements following discovered patterns
# Result: Compliant implementation on first try
```

### Example 2: Human Developer Onboarding

```bash
# New developer joins team
$ kb onboard

# KB provides:
# 1. Essential reading list (prioritized)
# 2. Common workflows and patterns
# 3. Repository structure overview
# 4. Quick-start guides
# 5. Who to ask for specific topics

$ kb quickstart --topic "python development"
# Shows: UV setup, testing standards, SPARC workflow
```

### Example 3: Cross-Repository Learning

```bash
# Find how feature was implemented elsewhere
$ kb examples --feature "authentication" --repos all

# Results:
# - aceengineer-admin: JWT-based auth with refresh tokens
# - digitalmodel: OAuth2 with Google integration
# - Pattern: session-based-auth (effectiveness: 0.87)
# - Related docs: security-standards.md, api-design.md
```

### Example 4: Standards Validation

```python
# Before implementing feature
validator = kb.validate_approach(
    approach="Generate matplotlib PNG for report",
    repository="worldenergydata",
    category="reporting"
)

# Returns:
# VIOLATION: HTML_REPORTING_STANDARDS.md
#   "All plots MUST be interactive (Plotly, Bokeh, Altair, D3.js)"
#   "NOT ALLOWED: Static matplotlib PNG/SVG exports"
# Suggestion: Use plotly.express for interactive plots
# Examples: [links to compliant implementations]
```

## Knowledge Categories

### 1. Standards (MANDATORY)

**Critical Standards:**
- AI_AGENT_GUIDELINES.md (ALL AI agents MUST read)
- AI_USAGE_GUIDELINES.md (Effectiveness patterns)
- DEVELOPMENT_WORKFLOW.md (user_prompt → YAML → pseudocode → TDD)
- HTML_REPORTING_STANDARDS.md (Interactive plots ONLY)
- FILE_ORGANIZATION_STANDARDS.md (AI folder organization)
- LOGGING_STANDARDS.md (Consistent logging)
- TESTING_FRAMEWORK_STANDARDS.md (80%+ coverage)

**Access Pattern:**
```python
# AI agent checks standards before implementing
standards = kb.standards.get_mandatory_for_task(task)
for standard in standards:
    context.add_requirement(standard)
```

### 2. Workflows

**Development Workflows:**
- SPARC methodology (Specification → Pseudocode → Architecture → Refinement → Completion)
- TDD cycle (Red → Green → Refactor)
- Git workflows (branching, committing, PR creation)
- CI/CD pipelines

**AI Workflows:**
- Interactive questioning (MANDATORY before implementation)
- Context gathering
- Implementation planning
- Review and iteration

### 3. Patterns

**Code Patterns:**
- Module organization
- Configuration management
- Error handling
- Logging integration

**Integration Patterns:**
- API design
- Database interactions
- External service integration
- Cross-repository communication

**Workflow Patterns:**
- YAML-driven configuration
- Pseudocode-first development
- Test-driven implementation
- Documentation generation

### 4. Examples

**Complete Implementations:**
- HTML reports with interactive Plotly charts
- YAML configuration files
- Test suites with 80%+ coverage
- CI/CD pipeline configurations

**Code Snippets:**
- Common functions and utilities
- Configuration templates
- Test fixtures
- Documentation templates

### 5. Learnings

**What Works:**
- Patterns with high success rates
- Effective AI agent strategies
- Productivity optimizations
- Quality improvements

**What to Avoid:**
- Anti-patterns and pitfalls
- Common mistakes
- Ineffective approaches
- Performance issues

## Metrics and Analytics

### Effectiveness Metrics

**Document Metrics:**
- Access frequency
- Implementation success rate
- Time saved (estimated)
- User satisfaction score

**Pattern Metrics:**
- Usage count across repositories
- Success rate when applied
- Time to implement
- Defect rate

**AI Agent Metrics:**
- Context utilization rate
- First-try success rate
- Rework reduction
- Compliance improvement

### Dashboard

```
Knowledge Base Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Documents: 88
Total Patterns: 47
Total Examples: 156
Repositories Indexed: 26

Most Accessed Documents (Last 30 Days):
1. AI_AGENT_GUIDELINES.md         (247 accesses, 98% success)
2. HTML_REPORTING_STANDARDS.md    (189 accesses, 95% success)
3. DEVELOPMENT_WORKFLOW.md        (156 accesses, 92% success)

Top Patterns:
1. yaml-to-code-workflow          (87% effectiveness, 34 uses)
2. plotly-interactive-report      (94% effectiveness, 28 uses)
3. sparc-tdd-cycle               (89% effectiveness, 41 uses)

Recent Learnings:
- AI questioning reduces rework by 40%
- Interactive plots improve user satisfaction by 65%
- YAML-first workflow speeds development by 50%
```

## Integration Points

### With Existing Skills

- **session-start-routine**: Load KB updates at session start
- **sparc-workflow**: Use KB patterns for each SPARC phase
- **compliance-check**: Validate against KB standards
- **repo-sync**: Update KB after sync operations
- **workspace-cli**: Integrate KB search into CLI

### With AI Agents

**All agents should:**
1. Query KB at task start
2. Follow KB standards (MANDATORY)
3. Use KB patterns when available
4. Record success/failure for KB learning

### With Documentation

- Auto-index new documentation
- Cross-link related documents
- Track documentation gaps
- Generate documentation from code

## Maintenance

### Automatic Updates

**Git Hooks:**
```bash
# .git/hooks/post-commit
kb update --incremental --source "$REPO_PATH"
```

**CI/CD Hooks:**
```yaml
# .github/workflows/kb-update.yml
on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'src/**'
      - 'tests/**'

jobs:
  update-kb:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update Knowledge Base
        run: kb update --analyze-changes
```

### Manual Curation

**Weekly Reviews:**
- Review high-access documents
- Update patterns based on feedback
- Add new examples
- Archive outdated information

**Monthly Analysis:**
- Effectiveness metrics review
- Gap identification
- Pattern optimization
- Documentation improvements

## Best Practices

1. **Always search KB before implementing** - Save time and ensure compliance
2. **Contribute learnings back** - Help future work and AI agents
3. **Rate documents and patterns** - Improve KB effectiveness
4. **Report gaps** - Help identify missing knowledge
5. **Keep examples up to date** - Ensure accuracy and relevance

## Troubleshooting

**Problem: KB search returns too many results**
```bash
# Use filters
kb search --topic "reporting" --repo digitalmodel --format yaml
```

**Problem: Pattern not working as expected**
```bash
# Check pattern details and variations
kb pattern --id "yaml-to-code-workflow" --show-variations
```

**Problem: Can't find relevant documentation**
```bash
# Browse by category
kb browse --category standards
# Or ask for help
kb suggest --task "implement authentication"
```

## Future Enhancements

### Phase 2 Features
- **Semantic search** using embeddings
- **AI-powered summarization** of long documents
- **Automatic pattern extraction** from code
- **Visual knowledge graph** showing relationships

### Phase 3 Features
- **Collaborative editing** of KB content
- **Version control** for KB entries
- **API for external tools** integration
- **Mobile app** for quick reference

---

## Version History

- **1.0.0** (2026-01-05): Initial knowledge base system skill created

---

**This skill creates the foundation for continuous learning and improvement across all repositories and AI agents!** 🧠
