---
name: Knowledge Base Builder
slug: knowledge-base-builder
description: Build and maintain AI-accessible knowledge bases for projects
category: meta
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "build knowledge base"
  - "create knowledge base"
  - "knowledge base builder"
  - "organize knowledge"
  - "structure knowledge"
tags:
  - knowledge-management
  - documentation
  - memory
---

# Knowledge Base Builder

The Knowledge Base Builder skill helps you create, structure, and maintain knowledge bases that AI agents can effectively query and utilize. It transforms scattered information—from project documentation to tribal knowledge—into organized, accessible knowledge that improves AI performance and team productivity.

This skill guides you through knowledge extraction, organization, structuring, and maintenance. It understands different knowledge formats (documentation, code comments, decision logs, schemas), helps you choose appropriate storage (markdown files, knowledge graphs, databases), and ensures knowledge remains current and useful.

Use this skill when starting new projects, onboarding AI to complex systems, preserving institutional knowledge, or improving AI agent effectiveness through better context.

## Core Workflows

### Workflow 1: Build Knowledge Base from Scratch
1. **Define** knowledge base purpose:
   - Who will use it? (AI agents, developers, both)
   - What problems does it solve?
   - What scope/boundaries?
2. **Identify** knowledge sources:
   - Existing documentation
   - Code repositories
   - Team conversations
   - Decision records
   - Tribal knowledge
3. **Extract** relevant information:
   - Key concepts and relationships
   - Architectural decisions
   - Domain terminology
   - Common patterns
   - Troubleshooting knowledge
4. **Structure** the knowledge:
   - Choose organization (hierarchical, graph, hybrid)
   - Define categories/taxonomies
   - Establish relationships
   - Create metadata schema
5. **Format** for consumption:
   - Markdown for documentation
   - Knowledge graph for relationships
   - Schema files for structure
   - Code comments for implementation
6. **Populate** the knowledge base:
   - Create initial content
   - Link related concepts
   - Add examples
   - Include references
7. **Validate** accessibility:
   - Can AI find information?
   - Is context sufficient?
   - Are relationships clear?
8. **Establish** maintenance process

### Workflow 2: Extract Knowledge from Codebase
1. **Analyze** codebase structure:
   - Architecture patterns
   - Module organization
   - Key abstractions
   - Data flow
2. **Identify** extractable knowledge:
   - Design decisions
   - API contracts
   - Data models
   - Business logic
   - Edge cases
3. **Generate** documentation:
   - Architecture overview
   - Component descriptions
   - API reference
   - Data dictionary
   - Integration guides
4. **Create** knowledge graph:
   - Entities (modules, services, models)
   - Relationships (depends on, implements, extends)
   - Observations (purpose, constraints, patterns)
5. **Link** to code:
   - File paths for reference
   - Function signatures
   - Configuration locations
6. **Maintain** synchronization:
   - Update on code changes
   - Version knowledge with code
   - Automate where possible

### Workflow 3: Organize Project Knowledge
1. **Audit** existing knowledge:
   - What documentation exists?
   - What's missing?
   - What's outdated?
   - What's scattered?
2. **Define** structure:
   - Documentation hierarchy
   - File organization
   - Naming conventions
   - Cross-referencing approach
3. **Create** core documents:
   - README.md (overview, getting started)
   - ARCHITECTURE.md (system design)
   - DECISIONS.md (ADRs)
   - PIPELINE_STATUS.md (project state)
   - CONTRIBUTING.md (development guide)
4. **Establish** conventions:
   - Document templates
   - Metadata standards
   - Update procedures
   - Review processes
5. **Populate** with content:
   - Migrate existing docs
   - Fill gaps with new content
   - Link related documents
   - Add navigation
6. **Integrate** with AI:
   - Add to context
   - Create knowledge graph entries
   - Enable discovery
   - Test accessibility

### Workflow 4: Build Knowledge Graph
1. **Identify** entities:
   - What are the key concepts?
   - What needs to be remembered?
   - What has relationships?
2. **Define** entity types:
   - Project (repos, services, apps)
   - Component (modules, features, functions)
   - Person (team members, stakeholders)
   - Decision (architectural choices)
   - Process (workflows, procedures)
   - Resource (docs, tools, dependencies)
3. **Extract** observations:
   - Facts about each entity
   - Properties and attributes
   - Context and purpose
   - Status and state
4. **Map** relationships:
   - How entities connect
   - Relationship types
   - Directionality
   - Strength/importance
5. **Store** in knowledge graph:
   - Use Memory MCP
   - Create entities
   - Create relations
   - Add observations
6. **Query** to validate:
   - Can you find entities?
   - Do relationships make sense?
   - Is information complete?
7. **Maintain** over time:
   - Add new entities
   - Update observations
   - Add new relationships
   - Prune obsolete information

### Workflow 5: Maintain Knowledge Base
1. **Monitor** knowledge health:
   - Usage frequency
   - Outdated content
   - Gaps in coverage
   - User feedback
2. **Update** regularly:
   - Reflect code changes
   - Document new decisions
   - Add new patterns
   - Remove deprecated info
3. **Review** periodically:
   - Quarterly knowledge audit
   - Validate accuracy
   - Check completeness
   - Improve clarity
4. **Optimize** for consumption:
   - Improve searchability
   - Add missing links
   - Consolidate redundancy
   - Enhance examples
5. **Gather** feedback:
   - What's confusing?
   - What's missing?
   - What's most useful?
6. **Iterate** on structure:
   - Reorganize if needed
   - Add new categories
   - Improve navigation
   - Refine metadata

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Build new knowledge base | "Build knowledge base for [project]" |
| Extract from codebase | "Extract knowledge from codebase" |
| Organize project docs | "Organize project knowledge" |
| Create knowledge graph | "Create knowledge graph for [domain]" |
| Update knowledge base | "Update knowledge base with [new info]" |
| Audit knowledge | "Audit knowledge base health" |
| Structure documentation | "Structure documentation for [project]" |

## Best Practices

- **Start with Purpose**: Define what the knowledge base should accomplish
  - Enable AI to understand codebase
  - Help new developers onboard
  - Preserve architectural decisions
  - Document domain knowledge

- **Structure for Discovery**: Make information findable
  - Clear hierarchy
  - Consistent naming
  - Comprehensive indexing
  - Rich cross-linking
  - Metadata tagging

- **Write for AI and Humans**: Both will consume this
  - Clear, concise language
  - Structured formats (tables, lists)
  - Explicit relationships
  - Contextual information
  - Code examples

- **Keep It Current**: Stale knowledge is worse than no knowledge
  - Update with code changes
  - Review regularly
  - Remove obsolete info
  - Version alongside code

- **Make It Accessible**: Knowledge must be reachable
  - Link from README
  - Reference in code comments
  - Add to AI context
  - Create in knowledge graph

- **Use Multiple Formats**: Different knowledge needs different formats
  - Markdown for prose documentation
  - Knowledge graphs for relationships
  - Schema files for structure
  - Code comments for implementation details
  - Diagrams for architecture

- **Preserve Context**: Don't just document "what", document "why"
  - Why this architecture?
  - Why not alternative approaches?
  - What constraints influenced decisions?
  - What trade-offs were made?

- **Link Generously**: Connect related concepts
  - Cross-reference documents
  - Link code to docs
  - Connect related decisions
  - Reference external resources

## Knowledge Base Structure

### Recommended File Organization
```
/docs
  /README.md                 # Project overview
  /ARCHITECTURE.md           # System design
  /DECISIONS.md              # ADRs (Architecture Decision Records)
  /PIPELINE_STATUS.md        # Current project state
  /CONTRIBUTING.md           # Development guide
  /API.md                    # API reference
  /DATABASE.md               # Schema documentation
  /DEPLOYMENT.md             # Deployment guide
  /TROUBLESHOOTING.md        # Common issues
  /guides/                   # How-to guides
    /getting-started.md
    /development-workflow.md
    /testing.md
  /reference/                # Technical reference
    /components.md
    /utilities.md
    /configurations.md
  /decisions/                # Detailed ADRs
    /001-framework-choice.md
    /002-state-management.md
```

### Documentation Templates

#### ARCHITECTURE.md Template
```markdown
# Architecture

## Overview
[High-level system description]

## System Components
- **Component 1**: [Purpose and responsibility]
- **Component 2**: [Purpose and responsibility]

## Data Flow
[How data moves through the system]

## Key Design Decisions
1. **[Decision]**: [Rationale]
2. **[Decision]**: [Rationale]

## Technology Stack
- Frontend: [Technologies]
- Backend: [Technologies]
- Database: [Technologies]
- Infrastructure: [Technologies]

## Integration Points
- [External service 1]: [How we integrate]
- [External service 2]: [How we integrate]

## Security Considerations
[Security architecture and patterns]

## Scalability & Performance
[How system scales, performance characteristics]
```

#### DECISIONS.md Template (ADR Log)
```markdown
# Architecture Decision Records

## ADR-001: [Decision Title]
**Date**: YYYY-MM-DD
**Status**: Accepted | Proposed | Deprecated

**Context**:
[What is the issue we're trying to solve?]

**Decision**:
[What we decided to do]

**Consequences**:
- Positive: [Benefits]
- Negative: [Trade-offs]
- Neutral: [Other impacts]

**Alternatives Considered**:
1. [Alternative 1]: [Why rejected]
2. [Alternative 2]: [Why rejected]

---

## ADR-002: [Next Decision]
[...]
```

#### Component Documentation Template
```markdown
# [Component Name]

## Purpose
[What this component does and why it exists]

## Location
`/path/to/component`

## Dependencies
- [Dependency 1]: [Why needed]
- [Dependency 2]: [Why needed]

## API
### Functions
- `functionName(params)`: [Description]

### Types
\`\`\`typescript
interface ComponentProps {
  // ...
}
\`\`\`

## Usage
\`\`\`typescript
// Example usage
\`\`\`

## Related Components
- [Component A]: [Relationship]
- [Component B]: [Relationship]

## Known Issues
- [Issue 1]: [Workaround]
```

## Knowledge Graph Patterns

### Entity Types for Software Projects
```
Project
  - name
  - description
  - status (active, maintenance, deprecated)
  - tech_stack

Component
  - name
  - type (service, module, function)
  - location (file path)
  - purpose
  - status

Person
  - name
  - role
  - expertise_areas
  - current_focus

Decision
  - title
  - date
  - status
  - context
  - choice
  - rationale

Process
  - name
  - type (workflow, procedure, standard)
  - steps
  - triggers
  - outputs

Dependency
  - name
  - version
  - purpose
  - critical (boolean)
```

### Relationship Types
```
Project --depends_on--> Dependency
Project --contains--> Component
Component --uses--> Component
Component --implements--> Decision
Person --owns--> Component
Person --made--> Decision
Decision --supersedes--> Decision
Component --documented_in--> Document
Process --governs--> Component
```

### Example Knowledge Graph Creation
```typescript
// Create entities
await memory.create_entities({
  entities: [
    {
      name: "id8labs-app",
      entityType: "Project",
      observations: [
        "Next.js 14+ application",
        "Uses Supabase for backend",
        "Deployed on Vercel",
        "Monorepo structure"
      ]
    },
    {
      name: "authentication-module",
      entityType: "Component",
      observations: [
        "Located in /src/features/auth",
        "Handles user authentication via Supabase Auth",
        "Supports magic link and OAuth",
        "Implements RLS policies"
      ]
    }
  ]
});

// Create relationships
await memory.create_relations({
  relations: [
    {
      from: "id8labs-app",
      to: "authentication-module",
      relationType: "contains"
    },
    {
      from: "authentication-module",
      to: "Supabase Auth",
      relationType: "uses"
    }
  ]
});
```

## Knowledge Extraction Techniques

### From Code
- **Function/Class documentation**: Purpose, parameters, returns
- **Module organization**: Structure and relationships
- **Design patterns**: Implementation approaches
- **Error handling**: Known failure modes
- **Performance considerations**: Optimization notes

### From Conversations
- **Decisions made**: Choices and rationale
- **Problems solved**: Issues and solutions
- **Lessons learned**: What worked, what didn't
- **Open questions**: Unresolved issues
- **Action items**: Tasks and owners

### From External Sources
- **API documentation**: Integration guides
- **Research papers**: Technical approaches
- **Stack Overflow**: Common solutions
- **Blog posts**: Best practices
- **Conference talks**: Industry patterns

## Knowledge Quality Checklist

Good knowledge base entries should:

- [ ] Have clear, descriptive titles
- [ ] Explain the "why" not just the "what"
- [ ] Include concrete examples
- [ ] Link to related concepts
- [ ] Specify when created/updated
- [ ] Indicate status (current, deprecated)
- [ ] Use consistent formatting
- [ ] Be discoverable through search
- [ ] Provide sufficient context
- [ ] Reference original sources

## Maintenance Schedule

### Daily
- Document new decisions as they're made
- Update PIPELINE_STATUS.md with progress
- Add code comments for complex logic

### Weekly
- Review open questions and update
- Check for outdated information
- Update API docs if endpoints changed
- Sync knowledge graph with changes

### Monthly
- Audit knowledge base completeness
- Review and improve unclear docs
- Update architecture diagrams
- Clean up obsolete content

### Quarterly
- Major knowledge base review
- Reorganize structure if needed
- Gather user feedback
- Plan improvements

## Tools & Technologies

### Storage Options
| Tool | Best For | Format |
|------|----------|--------|
| **Markdown files** | Human-readable docs | .md files in repo |
| **Memory MCP** | AI-accessible relationships | Knowledge graph |
| **Code comments** | Implementation context | JSDoc, inline comments |
| **OpenAPI/GraphQL** | API contracts | YAML/JSON schemas |
| **Mermaid** | Visual diagrams | Diagram-as-code |
| **Notion** | Collaborative docs | Rich text, databases |

### Generation Tools
- **TypeDoc**: Generate docs from TypeScript
- **JSDoc**: Generate docs from JavaScript
- **Swagger/OpenAPI**: Generate API docs
- **Mermaid**: Generate diagrams
- **Supabase CLI**: Generate DB types

## Common Pitfalls

- **Over-documentation**: Don't document the obvious
- **Under-documentation**: Don't assume knowledge
- **Outdated docs**: Worse than no docs
- **Scattered information**: Consolidate related knowledge
- **Missing context**: Always explain the "why"
- **Poor organization**: Make it findable
- **No maintenance**: Knowledge bases decay
- **One format only**: Use appropriate formats for different needs
