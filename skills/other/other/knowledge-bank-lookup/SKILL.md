---
name: knowledge-bank-lookup
description: Delegates knowledge bank lookups to Explore subagents with reflections-first strategy that learns from past mistakes. Checks /reflections/ directory before documentation to extract documented failures to avoid and proven approaches to apply. Automatically triggers when user mentions services ([project-a], [project-b], [project-c], Claude Code), requests investigations, or queries past lessons. Returns structured, actionable insights achieving 69-94% context reduction. (project, gitignored)
user-invocable: true
context: fork
agent: Explore
---

# Knowledge Bank Lookup

## What's New

Latest: v2.4.0 - Structure refactoring with improved clarity and terminology. See [CHANGELOG.md](CHANGELOG.md) for details.

---

## Invocation

### Automatic (Recommended)
This skill triggers automatically when Claude detects patterns listed in [Trigger Detection](#trigger-detection). No manual invocation needed.

### Manual Invocation
- **Slash command**: `/second-brain:knowledge-bank-lookup`
- **Skill tool**: `Skill({ skill: "second-brain:knowledge-bank-lookup" })`

### Visibility Settings

| Setting | Value | Effect |
|---------|-------|--------|
| `user-invocable` | `true` | Visible in slash menu, Skill tool allowed |
| `context` | `fork` | Runs in isolated subagent (Explore agent) |
| `agent` | `Explore` | Uses Explore agent optimized for codebase research |

See [references/examples.md](references/examples.md) for detailed integration examples.

---

## Overview

This skill enables efficient lookup of service documentation, architectural patterns, best practices, and reflections from the knowledge bank by delegating research to specialized subagents. Rather than consuming main agent context with large documentation reads, subagents perform deep analysis and return only distilled, actionable insights.

**Key Benefits:**
- **Context Efficiency**: 69-94% context reduction per lookup
- **Reflections-First**: Learn from past mistakes before consulting documentation
- **WikiLink Following**: DFS traversal of interconnected docs for complete coverage
- **Frontmatter Filtering**: Property-based document discovery
- **Structured Insights**: JSON responses with reflection_insights, patterns, linked_concepts, gotchas
- **Automatic Activation**: Triggers on service mentions and investigation keywords

## Configuration

Knowledge bank path is dynamically resolved via common utilities.

**Setup**: `skills/common/setup_kb_path.sh --configure`

**Verify**: `skills/common/setup_kb_path.sh --show`

**Usage in Scripts**: `source skills/common/get_kb_path.sh && KB_PATH=$(get_kb_path)`

See `skills/common/README.md` for details.

## Trigger Detection

### Automatic Triggers

Automatically invoke knowledge bank lookup when detecting:

1. **Service Mentions**: [project-a], [project-b-server], [project-b], [project-c], Claude Code, CC, ClaudeCode, Migration
2. **Investigation Requests**: "investigate:", "analyze:", "create investigation plan:", "understand X"
3. **Component References**: filter, cache, LiveConfig, plugin, EnrichmentGraph, creative, DLQ, hook, subagent, build-interceptor, build-executor
4. **Best Practice Queries**: "how should I", "what's the pattern for", "best practice"
5. **Implementation Planning**: "implement", "refactor", "migrate"
6. **Documentation Requests**: "recap the session", "document this"
7. **Process Learning**: "how did we handle X before", "past lessons on", "what went wrong with"

### Lookup Type Selection

Choose lookup type based on trigger context:

| Type | When to Use | Context Budget | Model |
|------|-------------|----------------|-------|
| **Quick** | Service mention, component reference | ~900 lines → 300 returned | haiku |
| **Standard** | Investigation, implementation planning | ~1950 lines → 600 returned | sonnet |
| **Deep** | Architectural decisions, cross-service | ~7300 lines → 1500 returned | sonnet |

## Knowledge Bank Overview

**Base Path**: Dynamically resolved via common utilities (see [Configuration](#configuration))

**Total**: 172 markdown files across 4 projects ([project-a], [project-b], CC, [project-c])

**Key Directories**:
- `projects/{service}/` - Service-specific documentation (concepts, components, best-practices)
- `_index/` - Maps of Content (MOCs) for efficient navigation
- `reflections/` - Process reflections (⚠️ CHECK FIRST before technical docs)
- `manual/` - Documentation and integration manuals
- `rules/` - Cross-project process rules

See [references/knowledge-bank-structure.md](references/knowledge-bank-structure.md) for detailed structure.

## Lookup Workflows

All workflows follow this pattern:
1. **Step 0**: Check reflections first (learn from past mistakes)
2. **Step 1**: Read service MOC (Map of Content)
3. **Steps 2-3**: Identify and read relevant documents
4. **Step 4**: Follow WikiLinks for connected knowledge
5. **Step 5**: Synthesize with reflection insights and linked concepts

### Quick Lookup

**When**: Service mention, simple component reference

**Workflow**: Check 3-5 recent reflections → Read MOC → 2-3 docs → 1-hop WikiLinks (2-3 additional docs)

**Invocation**: See [Quick Lookup Template](references/templates.md#quick-lookup-template)

### Standard Lookup

**When**: Investigation mode, implementation planning, best practice queries

**Workflow**: Search reflections for topic → Read MOC → 5-7 docs → 1-2 hop WikiLinks (5-7 additional docs)

**Invocation**: See [Standard Lookup Template](references/templates.md#standard-lookup-template)

### Deep Lookup

**When**: Major refactoring, architectural decisions, cross-service analysis

**Workflow**: Comprehensive reflection analysis → All MOCs → 10+ docs → Full DFS (up to 20 docs, 3 hops)

**Invocation**: See [Deep Lookup Template](references/templates.md#deep-lookup-template)

### CC (Claude Code) Lookup

**When**: User mentions Claude Code, CC, hooks, subagents, AI agent patterns

**Note**: No CC MOC exists yet; navigate directly to `/knowledge-bank/projects/cc/`

**Workflow**: Check CC-related reflections → Navigate to project files → Synthesize meta-pattern insights

## Navigation Strategy

**MOC-First**: Always start with Map of Content for the relevant service
- Achieves 94% context reduction vs reading all documents
- Only [project-a] and [project-b] have MOCs currently
- CC and [project-c]: Navigate directly to project files

**Reflections-First**: Check `/reflections/` BEFORE technical documentation
- Learn from documented failures
- Apply proven approaches
- Understand workflow friction points

## Advanced Features

### WikiLink Following (v2.2.0+)

Documents are interconnected using Obsidian WikiLinks (`[[Document Name]]`). The skill uses Depth-First Search (DFS) to traverse these connections, ensuring comprehensive coverage of related knowledge.

**Key Concepts:**
- **Hop count**: Distance from primary documents (1-3 hops depending on lookup type)
- **Link prioritization**: Scored by keyword relevance (+10 exact match, +5 pattern/principle)
- **Cycle prevention**: Each document visited once per traversal

See [references/wikilink-traversal.md](references/wikilink-traversal.md) for complete details.

### Frontmatter-Based Retrieval (v2.3.0+)

Documents use LLM-optimized frontmatter properties (`type`, `status`, `complexity`, `relevance-to`) for efficient filtering without reading full content.

**Key Concepts:**
- **Property filtering**: Filter by type, status, complexity before reading
- **Graph traversal**: Follow `related-concepts`, `related-components` properties
- **Version awareness**: Track `superseded-by` chains to find current docs

See [references/frontmatter-retrieval.md](references/frontmatter-retrieval.md) for complete details.

### Progressive Refinement

For follow-up queries, reference previous lookup context so subagent can reuse cached data:
- Subagent preserves its own context
- No need to re-read MOC
- Main agent context stays clean

See [references/optimization-techniques.md](references/optimization-techniques.md) for details.

## Subagent Communication

### Request Structure (Main → Subagent)

Include in subagent prompts:
1. **Role**: "You are a knowledge bank exploration agent"
2. **Task**: Specific lookup objective
3. **Knowledge Bank Location**: Full base path
4. **Workflow**: Step-by-step instructions (reflections-first, then MOC-first)
5. **Output Format**: JSON structure specification
6. **Context**: User intent, focus areas, current working files

### Response Format (Subagent → Main)

Subagents return JSON with:

| Field | Description |
|-------|-------------|
| `executive_summary` | Key findings and recommended action |
| `reflection_insights` | Past mistakes, proven approaches, workflow gotchas |
| `relevant_patterns` | Technical patterns with gotchas |
| `related_concepts` | Prerequisites and alternatives |
| `linked_concepts` | Concepts discovered through WikiLink traversal |
| `best_practices` | Reusable methodologies |
| `cross_references` | Follow-up topics |
| `link_traversal` | WikiLink traversal statistics |
| `metadata` | Analysis depth, document counts, limitations |

See [references/json-schemas.md](references/json-schemas.md) for complete schema.

## Best Practices

| Practice | Rationale |
|----------|-----------|
| Always check reflections first | Learn from past mistakes before technical docs |
| Use MOC-first navigation | 94% context reduction vs reading all documents |
| Specify JSON output format | Ensures structured, parseable responses |
| Include user context | Improves relevance of findings |
| Choose appropriate lookup type | Don't use Deep for simple queries |
| Integrate insights naturally | Present as main agent knowledge, not "I looked this up" |

## Reference Documentation

- **[Prompt Templates](references/templates.md)** - Complete subagent prompts for Quick/Standard/Deep lookups
- **[Integration Examples](references/examples.md)** - Usage scenarios and response construction
- **[JSON Schemas](references/json-schemas.md)** - Response format specifications
- **[Knowledge Bank Structure](references/knowledge-bank-structure.md)** - Directory organization and document counts
- **[WikiLink Traversal](references/wikilink-traversal.md)** - DFS traversal details and utilities
- **[Frontmatter Retrieval](references/frontmatter-retrieval.md)** - Property-based filtering and search
- **[Optimization Techniques](references/optimization-techniques.md)** - Context efficiency methods
- **[Session Documentation](references/session-documentation.md)** - Documentation process guidelines
