---
title: "PRD: Product Manager Skill for Morphir Ecosystem"
linkTitle: "Product Manager Skill"
weight: 20
description: "Product Requirements Document for an AI Product Manager skill with comprehensive Morphir ecosystem knowledge"
---

# Product Requirements Document: Product Manager Skill for Morphir Ecosystem

**Status**: 📋 Draft
**Created**: 2025-12-18
**Last Updated**: 2025-12-18
**Current Phase**: Phase 1 - Planning and Design
**Author**: Morphir .NET Team
**Related Issue**: [#228](https://github.com/finos/morphir-dotnet/issues/228)

## Overview

This PRD defines requirements for creating a specialized Product Manager skill for AI coding agents. This skill will provide comprehensive product management capabilities tailored to the Morphir ecosystem across all FINOS Morphir repositories, helping users create better PRDs, craft meaningful issues, understand the ecosystem, and make product decisions aligned with Morphir's philosophy.

## Problem Statement

Currently, contributors working across the Morphir ecosystem face several challenges:

1. **Fragmented Knowledge**: Morphir spans multiple repositories (morphir-elm, morphir-jvm, morphir-scala, morphir-dotnet, etc.) with varying maturity levels, features, and conventions
2. **Inconsistent Issue Quality**: Issues and PRs often lack context, proper categorization, or alignment with project goals
3. **PRD Gaps**: Not all features have comprehensive PRDs, and creating high-quality PRDs requires deep Morphir knowledge
4. **Cross-Repo Blind Spots**: Contributors may duplicate work or miss opportunities for cross-repository synergies
5. **UX/DX Debt**: User experience and developer experience improvements need dedicated advocacy
6. **Manual Ecosystem Tracking**: No automated way to track trends, backlogs, or health metrics across the ecosystem

### Current Pain Points

- **New contributors** struggle to understand where to contribute and how to write good issues
- **Maintainers** spend time triaging poorly-written issues and PRs
- **Product decisions** lack ecosystem-wide context and may not align with Morphir's functional modeling philosophy
- **Documentation gaps** make it hard to understand feature status across implementations
- **Backlog management** is manual and repository-siloed

## Goals

### Primary Goals

1. **Expert PRD Guidance**: Help users create comprehensive, well-structured PRDs aligned with Morphir principles
2. **Issue Quality Improvement**: Assist in crafting high-quality issues (bugs, features, enhancements) with proper context
3. **Ecosystem Intelligence**: Provide real-time awareness of backlogs, trends, and status across all Morphir repositories
4. **UX/DX Advocacy**: Champion user and developer experience improvements
5. **Intelligent Questioning**: Push back constructively on features that don't align with Morphir's ethos
6. **GitHub Automation**: Provide F# scripts for querying, analyzing, and reporting across the ecosystem

### Secondary Goals

7. **Cross-Skill Integration**: Coordinate effectively with qa-tester and release-manager skills
8. **Knowledge Management**: Maintain and share institutional knowledge about Morphir
9. **Template Library**: Provide reusable templates for common product management tasks
10. **Metrics & Analytics**: Track and report ecosystem health metrics

## Non-Goals

### Explicitly Out of Scope

- **Code Implementation**: Development agents handle implementation
- **Test Execution**: qa-tester skill handles testing
- **Release Management**: release-manager skill handles releases
- **Direct Repository Modifications**: Should create PRs/issues instead of direct changes
- **Automated Merging**: Requires human review and approval
- **External Product Management**: Focus is on Morphir ecosystem only

## User Stories

### Story 1: Create a Comprehensive PRD
**As a** feature owner
**I want to** create a comprehensive PRD with AI assistance
**So that** my feature is well-specified and aligns with Morphir principles

**Acceptance Criteria**:
- User requests help creating a PRD for a feature
- Product Manager asks clarifying questions about goals, scope, users
- Product Manager generates PRD using template with all sections filled
- PRD references existing Morphir patterns and architecture
- PRD includes feature tracking table and implementation phases
- Product Manager validates alignment with Morphir philosophy

### Story 2: Craft a High-Quality Issue
**As a** contributor
**I want to** create a well-structured issue
**So that** maintainers can quickly understand and prioritize it

**Acceptance Criteria**:
- User describes a bug, feature, or enhancement idea
- Product Manager asks clarifying questions
- Product Manager helps categorize and label appropriately
- Product Manager suggests related issues across repositories
- Product Manager generates issue description with proper formatting
- Issue includes references to relevant documentation and code

### Story 3: Ecosystem Trend Analysis
**As a** maintainer
**I want to** understand what's trending across the Morphir ecosystem
**So that** I can align my repository's priorities with ecosystem needs

**Acceptance Criteria**:
- User requests ecosystem analysis
- Product Manager runs trend-analysis.fsx script
- Product Manager reports most active labels, common themes
- Product Manager identifies cross-repository patterns
- Product Manager suggests areas needing attention
- Report includes links to relevant issues and discussions

### Story 4: Backlog Health Check
**As a** project lead
**I want to** assess the health of my backlog
**So that** I can prioritize triage and cleanup efforts

**Acceptance Criteria**:
- User requests backlog analysis
- Product Manager runs analyze-backlog.fsx script
- Product Manager reports backlog metrics (age, staleness, priority distribution)
- Product Manager identifies stale issues needing attention
- Product Manager suggests triage priorities
- Product Manager compares against ecosystem averages

### Story 5: Cross-Repository Issue Search
**As a** developer
**I want to** find related issues across all Morphir repositories
**So that** I don't duplicate work and can learn from other implementations

**Acceptance Criteria**:
- User describes a feature or issue
- Product Manager runs query-issues.fsx across all finos/morphir-* repos
- Product Manager presents related issues with context
- Product Manager highlights implementation differences
- Product Manager suggests collaboration opportunities
- Results link to original issues

### Story 6: Feature Alignment Validation
**As a** contributor
**I want to** validate that my feature idea aligns with Morphir's philosophy
**So that** I don't waste effort on something that won't be accepted

**Acceptance Criteria**:
- User proposes a feature idea
- Product Manager asks probing questions about motivation, alternatives
- Product Manager evaluates alignment with Morphir principles (functional, type-driven, domain modeling)
- Product Manager provides constructive feedback
- Product Manager suggests modifications or alternatives if misaligned
- Product Manager references similar features in other repos

## Detailed Requirements

### Functional Requirements

#### FR-1: PRD Creation and Guidance

**Capabilities**:
- Generate PRDs from template with all required sections
- Ask clarifying questions to fill in gaps
- Validate PRD completeness and quality
- Reference existing PRDs for consistency
- Ensure alignment with Morphir architecture
- Include feature status tracking tables
- Suggest implementation phases

**Templates**:
- Standard feature PRD
- Architecture change PRD
- Breaking change PRD
- Cross-repository PRD

**Validation Checklist**:
- [ ] Problem statement clearly defined
- [ ] Goals and non-goals explicit
- [ ] User stories with acceptance criteria
- [ ] Technical design outlined
- [ ] Testing strategy included
- [ ] Success criteria measurable
- [ ] References to Morphir docs/architecture
- [ ] Feature tracking table included

#### FR-2: Issue Creation and Enhancement

**Capabilities**:
- Help craft feature requests
- Help write bug reports
- Help create enhancement proposals
- Suggest appropriate labels and milestones
- Cross-reference related issues
- Validate issue completeness

**Issue Templates**:
- Feature request
- Bug report
- Enhancement proposal
- Documentation improvement
- Performance issue

**Quality Checklist**:
- [ ] Clear, descriptive title
- [ ] Problem/motivation explained
- [ ] Expected vs actual behavior (for bugs)
- [ ] Steps to reproduce (for bugs)
- [ ] Proposed solution or alternatives
- [ ] Impact assessment
- [ ] Links to related issues/docs
- [ ] Appropriate labels

#### FR-3: Ecosystem Intelligence

**Data Sources**:
- finos/morphir (core specs and schemas)
- finos/morphir-elm (reference implementation)
- finos/morphir-jvm (JVM implementation)
- finos/morphir-scala (Scala implementation)
- finos/morphir-dotnet (this repository)
- finos/morphir-examples (examples and docs)

**Intelligence Capabilities**:
- Query issues across all repositories
- Track trending topics and labels
- Identify common pain points
- Monitor release cadences
- Compare feature parity
- Detect cross-repository dependencies

**Metrics Tracked**:
- Issue velocity (opened, closed, avg time to close)
- Backlog health (age distribution, staleness)
- Label distribution and trends
- Contributor activity
- Documentation coverage
- Test coverage trends

#### FR-4: GitHub Automation Scripts (F#)

**Script: query-issues.fsx**
```fsharp
// Query issues across Morphir repositories
// Usage: dotnet fsi query-issues.fsx --label "enhancement" --state "open" --repos "all"
// Output: JSON, Markdown, or formatted table
```

**Features**:
- Multi-repository queries (all finos/morphir-* repos)
- Filter by label, state, milestone, assignee, author
- Sort by created, updated, comments, reactions
- Format output as JSON, Markdown, or table
- Cache results for performance

**Script: analyze-backlog.fsx**
```fsharp
// Analyze backlog health metrics
// Usage: dotnet fsi analyze-backlog.fsx --repo "finos/morphir-dotnet"
// Output: Health report with metrics and recommendations
```

**Features**:
- Calculate backlog age distribution
- Identify stale issues (no activity in 90+ days)
- Analyze priority distribution
- Compare against ecosystem averages
- Generate recommendations for triage

**Script: trend-analysis.fsx**
```fsharp
// Identify trending topics across ecosystem
// Usage: dotnet fsi trend-analysis.fsx --since "30 days ago"
// Output: Trend report with top labels, themes, activity
```

**Features**:
- Most active labels in time period
- Emerging themes from issue titles/descriptions
- Spike detection (unusual activity)
- Cross-repository correlation
- Sentiment analysis (positive/negative)

**Script: check-ecosystem.fsx**
```fsharp
// Check status across all Morphir repositories
// Usage: dotnet fsi check-ecosystem.fsx
// Output: Ecosystem health dashboard
```

**Features**:
- Latest release versions
- CI/CD status
- Open PR counts
- Recent activity summary
- Documentation status
- Test coverage (if available)

**Script: generate-prd.fsx**
```fsharp
// Generate PRD from template with interactive prompts
// Usage: dotnet fsi generate-prd.fsx --template "standard"
// Output: PRD markdown file
```

**Features**:
- Interactive questionnaire for PRD sections
- Pre-fill from existing issues or discussions
- Validate completeness
- Preview before saving
- Save to docs/content/contributing/design/prds/

#### FR-5: Integration with Other Skills

**With qa-tester**:
- Coordinate on acceptance criteria definition
- Align test plans with PRD requirements
- Validate feature completeness against PRD
- Review test coverage for PRD features

**With release-manager**:
- Align features with release roadmap
- Coordinate changelog entries
- Review "What's New" documentation
- Prioritize features for releases

**With development agents**:
- Provide clear requirements and context
- Answer questions during implementation
- Validate implementation against PRD
- Document design decisions in PRD

#### FR-6: Knowledge Management

**Morphir Core Concepts**:
- Functional modeling approach
- Type-driven development
- Business domain modeling
- Distribution and intermediate representation
- Cross-language support strategy

**Architecture Patterns**:
- Vertical Slice Architecture
- Railway-oriented programming
- ADT-first design
- Immutability and pure functions
- Effect management at boundaries

**Decision-Making Framework**:
- IR fidelity over convenience
- Minimize dependencies
- Performance requires benchmarks
- Keep effects at edges
- Prefer explicit ADTs

### Non-Functional Requirements

#### NFR-1: Response Time
- Script execution < 30 seconds for single-repo queries
- Script execution < 2 minutes for ecosystem-wide queries
- PRD generation interactive (responds to each question in < 5 seconds)

#### NFR-2: Accuracy
- Cross-repository queries return 100% accurate results
- Trend analysis validated against manual review (>95% agreement)
- Issue recommendations relevant (>80% user acceptance)

#### NFR-3: Maintainability
- Scripts use GitHub CLI (gh) for authentication
- Scripts use standard F# libraries (no exotic dependencies)
- Scripts include help text and examples
- Scripts handle rate limiting gracefully

#### NFR-4: Usability
- Clear, conversational interaction style
- Asks clarifying questions before making assumptions
- Provides rationale for recommendations
- Offers alternatives when pushing back
- Links to relevant documentation

#### NFR-5: Documentation
- Comprehensive skill.md with all capabilities
- README with quick start guide
- Script documentation with usage examples
- Template documentation with instructions
- Integration guide for other skills

## Technical Design

### Skill Structure

```
.claude/skills/product-manager/
├── skill.md                          # Main skill definition and playbooks
├── README.md                         # Quick start and overview
├── scripts/                          # F# automation scripts
│   ├── query-issues.fsx              # Multi-repo issue queries
│   ├── analyze-backlog.fsx           # Backlog health analysis
│   ├── trend-analysis.fsx            # Trend detection and reporting
│   ├── check-ecosystem.fsx           # Ecosystem status dashboard
│   ├── generate-prd.fsx              # Interactive PRD generation
│   ├── update-knowledge.fsx          # Update knowledgebase from live sources
│   └── common/                       # Shared utilities
│       ├── github-api.fsx            # GitHub API helpers
│       ├── formatting.fsx            # Output formatting
│       └── cache.fsx                 # Result caching
├── templates/                        # Document templates
│   ├── prd-standard.md               # Standard feature PRD
│   ├── prd-architecture.md           # Architecture change PRD
│   ├── prd-breaking.md               # Breaking change PRD
│   ├── issue-feature.md              # Feature request template
│   ├── issue-bug.md                  # Bug report template
│   └── issue-enhancement.md          # Enhancement proposal template
├── knowledge/                        # Curated knowledgebase (markdown)
│   ├── README.md                     # Knowledgebase overview and index
│   ├── morphir-principles.md         # Core Morphir philosophy and principles
│   ├── ecosystem-map.md              # Repository overview and relationships
│   ├── architecture/                 # Architecture patterns and decisions
│   │   ├── ir-design.md              # IR architecture and versioning
│   │   ├── vertical-slices.md        # Vertical Slice Architecture
│   │   ├── type-system.md            # Morphir type system
│   │   └── distribution-model.md     # Cross-language distribution
│   ├── repositories/                 # Per-repository knowledge
│   │   ├── morphir-core.md           # finos/morphir (specs)
│   │   ├── morphir-elm.md            # finos/morphir-elm (reference)
│   │   ├── morphir-jvm.md            # finos/morphir-jvm
│   │   ├── morphir-scala.md          # finos/morphir-scala
│   │   ├── morphir-dotnet.md         # finos/morphir-dotnet (this repo)
│   │   └── morphir-examples.md       # finos/morphir-examples
│   ├── features/                     # Feature status across repos
│   │   ├── cli-tools.md              # CLI feature parity
│   │   ├── ir-versions.md            # IR version support matrix
│   │   ├── backends.md               # Backend/codegen support
│   │   └── testing-tools.md          # Testing capabilities
│   ├── conventions/                  # Standards and conventions
│   │   ├── naming.md                 # Naming conventions
│   │   ├── code-style.md             # Code style per language
│   │   ├── commit-messages.md        # Commit message format
│   │   └── issue-labels.md           # Standard labels across repos
│   ├── workflows/                    # Common workflows and processes
│   │   ├── contributing.md           # Contribution workflow
│   │   ├── prd-process.md            # PRD creation and review
│   │   ├── release-process.md        # Release workflow
│   │   └── issue-triage.md           # Issue triage guidelines
│   └── faq/                          # Frequently asked questions
│       ├── product-decisions.md      # Common product decision rationales
│       ├── technical-choices.md      # Technical architecture FAQs
│       └── cross-repo-alignment.md   # How to align features across repos
└── docs/                             # Skill-specific documentation
    └── integration-guide.md          # Integration with other skills
```

### Morphir Ecosystem Model

**Repository Categories**:

1. **Core Specification** (finos/morphir)
   - Language specification
   - IR schema definitions (v1, v2, v3)
   - Authoritative documentation

2. **Reference Implementation** (finos/morphir-elm)
   - Elm frontend compiler
   - CLI tools
   - Example models
   - Most mature implementation

3. **Platform Implementations**:
   - **finos/morphir-jvm**: Java/Kotlin support
   - **finos/morphir-scala**: Scala support
   - **finos/morphir-dotnet**: C#/F# support

4. **Resources**:
   - **finos/morphir-examples**: Example models and documentation

**Cross-Repository Queries**:
```fsharp
// Example: Find all IR-related issues across ecosystem
let irIssues =
    MorphirRepos.All
    |> Seq.collect (fun repo -> GitHub.queryIssues repo "label:IR")
    |> Seq.sortByDescending (_.UpdatedAt)
```

### GitHub API Integration

**Authentication**:
- Use GitHub CLI (`gh`) for authenticated requests
- Leverage existing user credentials
- No API tokens to manage

**Rate Limiting**:
- Implement exponential backoff
- Cache results for 15 minutes
- Use GraphQL for complex queries (fewer requests)
- Batch queries when possible

**Query Patterns**:

**REST API** (simple queries):
```bash
gh api repos/finos/morphir-dotnet/issues \
  --field state=open \
  --field labels=enhancement \
  --jq '.[] | {title, number, url}'
```

**GraphQL API** (complex queries):
```graphql
query EcosystemIssues {
  search(query: "org:finos morphir in:name is:issue label:enhancement", type: ISSUE, first: 100) {
    nodes {
      ... on Issue {
        title
        number
        repository { name }
        labels(first: 10) { nodes { name } }
      }
    }
  }
}
```

### Knowledgebase Management

**Purpose**: The Product Manager skill maintains a curated knowledgebase of Morphir ecosystem knowledge as markdown files within the skill directory. This enables offline access, version control, and structured knowledge organization.

**Knowledge Categories**:

1. **Core Principles** (`knowledge/morphir-principles.md`)
   - Functional modeling philosophy
   - Type-driven development
   - Business domain modeling
   - Distribution strategy
   - Cross-language approach

2. **Ecosystem Map** (`knowledge/ecosystem-map.md`)
   - Repository overview and purposes
   - Maturity levels and feature parity
   - Release cadences
   - Maintainer information
   - Dependency relationships

3. **Architecture** (`knowledge/architecture/`)
   - IR design and versioning strategy
   - Vertical Slice Architecture patterns
   - Type system design
   - Distribution model
   - Backend architecture patterns

4. **Repository-Specific Knowledge** (`knowledge/repositories/`)
   - Per-repo feature status
   - Technology stacks
   - Conventions and patterns
   - Common issues and solutions
   - Roadmap highlights

5. **Feature Parity** (`knowledge/features/`)
   - CLI tools comparison matrix
   - IR version support across implementations
   - Backend/codegen capabilities
   - Testing tool availability
   - Documentation status

6. **Conventions** (`knowledge/conventions/`)
   - Naming conventions (modules, types, functions)
   - Code style guides per language
   - Commit message standards
   - Issue/PR label taxonomy
   - Documentation standards

7. **Workflows** (`knowledge/workflows/`)
   - Contribution process
   - PRD creation and review
   - Release management
   - Issue triage guidelines
   - Cross-repo coordination

8. **FAQs** (`knowledge/faq/`)
   - Common product decision rationales
   - Technical architecture questions
   - Cross-repo alignment strategies
   - Migration and compatibility

**Knowledge Update Workflow**:

```fsharp
// update-knowledge.fsx: Fetch latest info from live sources
// Usage: dotnet fsi update-knowledge.fsx --category repositories

// Fetch latest README from each repo
let updateRepositoryDocs repos =
    repos
    |> Seq.iter (fun repo ->
        let readme = GitHub.fetchFile repo "README.md"
        let repoDoc = Knowledge.parseRepositoryInfo readme
        Knowledge.save $"knowledge/repositories/{repo.name}.md" repoDoc
    )

// Fetch latest feature status
let updateFeatureMatrix () =
    let cliFeatures =
        MorphirRepos.All
        |> Seq.collect (fun repo ->
            GitHub.searchCode repo "CLI commands"
        )
    Knowledge.generateFeatureMatrix cliFeatures
    |> Knowledge.save "knowledge/features/cli-tools.md"

// Validate knowledgebase consistency
let validateKnowledge () =
    Knowledge.checkBrokenLinks ()
    Knowledge.validateMarkdown ()
    Knowledge.checkOutdatedInfo ()
```

**Knowledge Access Patterns**:

```markdown
When asked about Morphir principles:
1. Read knowledge/morphir-principles.md
2. Cite specific sections with links
3. Provide examples from knowledge/faq/

When comparing repos:
1. Read knowledge/ecosystem-map.md for overview
2. Read specific knowledge/repositories/{repo}.md
3. Consult knowledge/features/ for capability matrix

When validating feature alignment:
1. Reference knowledge/morphir-principles.md
2. Check knowledge/architecture/ for design patterns
3. Review knowledge/faq/product-decisions.md for precedents
```

**Knowledge Maintenance**:

- **Manual Curation**: Maintainers update knowledge files as authoritative sources
- **Periodic Updates**: Run update-knowledge.fsx quarterly to refresh from live sources
- **Version Control**: Knowledge evolves with the skill, tracked in git
- **Validation**: CI validates markdown formatting and internal links
- **Review Process**: Knowledge changes reviewed like code changes

**Knowledge vs. Live Data**:

- **Knowledgebase**: Stable, curated, architectural, and philosophical knowledge
- **Live Queries**: Real-time issue data, PR status, recent activity
- **Hybrid Approach**: Use knowledge for context, live queries for current state

### PRD Template Engine

**Interactive Generation**:
```fsharp
// Prompt user for each section
let prd = PRD.Interactive [
    Section.Overview [
        Question "What feature are you proposing?"
        Question "Why is this feature needed?"
    ]
    Section.Goals [
        Question "What are the primary goals? (one per line)"
        Question "What is explicitly out of scope?"
    ]
    // ... more sections
]

// Validate completeness
let validation = PRD.validate prd

// Save to file
PRD.save "docs/content/contributing/design/prds/my-feature.md" prd
```

### Skill Activation Triggers

**Keywords**:
- "PRD", "product requirements", "feature spec"
- "create issue", "file bug", "report enhancement"
- "ecosystem", "cross-repo", "morphir repos"
- "backlog", "triage", "issue health"
- "trend", "popular", "common issues"
- "align with morphir", "morphir philosophy"

**Scenarios**:
- User asks for help creating a PRD
- User wants to file an issue
- User asks "what should I work on?"
- User asks about feature status across repos
- User proposes a feature that may not align
- User asks about Morphir architecture or principles

## Feature Status Tracking

| Feature ID | Feature | Status | Priority | Assigned | Notes |
|-----------|---------|--------|----------|----------|-------|
| PM-01 | Skill definition (skill.md) | ⏳ Planned | P0 | - | Core skill description and playbooks |
| PM-02 | README and quick start | ⏳ Planned | P0 | - | User-facing documentation |
| PM-03 | Knowledgebase: morphir-principles.md | ⏳ Planned | P0 | - | Core Morphir philosophy and principles |
| PM-04 | Knowledgebase: ecosystem-map.md | ⏳ Planned | P0 | - | Repository overview and relationships |
| PM-05 | Knowledgebase: architecture/ (4 docs) | ⏳ Planned | P0 | - | IR, VSA, type system, distribution |
| PM-06 | Knowledgebase: repositories/ (6 docs) | ⏳ Planned | P1 | - | Per-repo knowledge |
| PM-07 | Knowledgebase: features/ (4 docs) | ⏳ Planned | P1 | - | Feature parity matrices |
| PM-08 | Knowledgebase: conventions/ (4 docs) | ⏳ Planned | P1 | - | Standards and conventions |
| PM-09 | Knowledgebase: workflows/ (4 docs) | ⏳ Planned | P1 | - | Process documentation |
| PM-10 | Knowledgebase: faq/ (3 docs) | ⏳ Planned | P2 | - | Frequently asked questions |
| PM-11 | PRD templates (standard, architecture, breaking) | ⏳ Planned | P0 | - | Reusable PRD templates |
| PM-12 | Issue templates (feature, bug, enhancement) | ⏳ Planned | P0 | - | Reusable issue templates |
| PM-13 | Script: query-issues.fsx | ⏳ Planned | P0 | - | Multi-repo issue querying |
| PM-14 | Script: analyze-backlog.fsx | ⏳ Planned | P1 | - | Backlog health metrics |
| PM-15 | Script: trend-analysis.fsx | ⏳ Planned | P1 | - | Ecosystem trend detection |
| PM-16 | Script: check-ecosystem.fsx | ⏳ Planned | P1 | - | Ecosystem status dashboard |
| PM-17 | Script: generate-prd.fsx | ⏳ Planned | P2 | - | Interactive PRD generation |
| PM-18 | Script: update-knowledge.fsx | ⏳ Planned | P2 | - | Update knowledgebase from live sources |
| PM-19 | Script utilities (GitHub API, formatting, cache) | ⏳ Planned | P0 | - | Shared script infrastructure |
| PM-20 | Integration guide (with qa-tester, release-manager) | ⏳ Planned | P1 | - | Cross-skill coordination |
| PM-21 | PRD creation playbook | ⏳ Planned | P0 | - | Step-by-step PRD creation guide |
| PM-22 | Issue crafting playbook | ⏳ Planned | P0 | - | Step-by-step issue creation guide |
| PM-23 | Ecosystem analysis playbook | ⏳ Planned | P1 | - | How to analyze cross-repo trends |
| PM-24 | Feature validation playbook | ⏳ Planned | P1 | - | Validate alignment with Morphir |
| PM-25 | Knowledge management playbook | ⏳ Planned | P2 | - | How to maintain knowledgebase |

**Status Legend**:
- ⏳ **Planned**: Specification complete, ready to implement
- 🚧 **In Progress**: Currently being implemented
- ✅ **Implemented**: Feature complete and tested
- 🔄 **Iterating**: Implemented but needs refinement
- ⏸️ **Deferred**: Postponed to later phase

**Priority Legend**:
- **P0**: Must-have for initial release
- **P1**: Should-have for initial release
- **P2**: Nice-to-have, can be added later

## Implementation Phases

### Phase 1: Core Infrastructure and Knowledgebase Foundation (Weeks 1-2)
**Goal**: Establish skill structure, foundational scripts, and core knowledgebase

**Deliverables**:
- [x] PRD created and reviewed (this document)
- [ ] skill.md with core playbooks
- [ ] README with quick start
- [ ] Knowledgebase structure and README
- [ ] knowledge/morphir-principles.md (P0)
- [ ] knowledge/ecosystem-map.md (P0)
- [ ] knowledge/architecture/ - 4 core docs (P0)
  - [ ] ir-design.md
  - [ ] vertical-slices.md
  - [ ] type-system.md
  - [ ] distribution-model.md
- [ ] Basic GitHub API utilities (scripts/common/)
- [ ] query-issues.fsx (basic functionality)

**Success Criteria**:
- Skill can be invoked and responds appropriately
- Knowledgebase has core Morphir principles documented
- query-issues.fsx can query issues from single repository
- Documentation explains skill purpose and capabilities
- Skill can reference knowledgebase when answering questions

### Phase 2: Templates, Playbooks, and Extended Knowledgebase (Weeks 2-3)
**Goal**: Provide templates, guided workflows, and expand knowledgebase

**Deliverables**:
- [ ] All PRD templates (standard, architecture, breaking)
- [ ] All issue templates (feature, bug, enhancement)
- [ ] PRD creation playbook
- [ ] Issue crafting playbook
- [ ] Enhanced query-issues.fsx (multi-repo, filtering)
- [ ] knowledge/repositories/ - 6 repo docs (P1)
- [ ] knowledge/conventions/ - 4 convention docs (P1)
- [ ] knowledge/workflows/ - 4 workflow docs (P1)

**Success Criteria**:
- User can generate PRD using template
- User can create well-structured issue with guidance
- Multi-repository queries work across all finos/morphir-* repos
- Knowledgebase covers all major Morphir repositories
- Skill can compare features across repositories using knowledgebase

### Phase 3: Analytics, Intelligence, and Feature Matrices (Weeks 3-4)
**Goal**: Add ecosystem intelligence capabilities and feature comparison matrices

**Deliverables**:
- [ ] analyze-backlog.fsx
- [ ] trend-analysis.fsx
- [ ] check-ecosystem.fsx
- [ ] Feature validation playbook
- [ ] Ecosystem analysis playbook
- [ ] Caching infrastructure
- [ ] knowledge/features/ - 4 feature matrices (P1)
- [ ] knowledge/faq/ - 3 FAQ docs (P2)

**Success Criteria**:
- Backlog health metrics accurate and actionable
- Trend analysis identifies real patterns (validated manually)
- Ecosystem dashboard provides useful overview
- Feature matrices enable cross-repo capability comparisons
- FAQs capture common product decision rationales

### Phase 4: Integration, Polish, and Knowledge Automation (Week 4-5)
**Goal**: Integrate with other skills, refine, and add knowledge automation

**Deliverables**:
- [ ] Integration guide (qa-tester, release-manager)
- [ ] generate-prd.fsx (interactive PRD generation)
- [ ] update-knowledge.fsx (knowledgebase automation)
- [ ] Knowledge management playbook
- [ ] Comprehensive testing
- [ ] Documentation review and updates
- [ ] Example walkthroughs
- [ ] Knowledgebase validation (CI integration)

**Success Criteria**:
- Skill integrates smoothly with qa-tester and release-manager
- generate-prd.fsx creates complete, high-quality PRDs
- update-knowledge.fsx can refresh knowledgebase from live sources
- Documentation is comprehensive and clear
- Examples demonstrate all major workflows
- Knowledgebase passes automated validation checks

## Testing Strategy

### Manual Testing

**PRD Creation**:
1. Request PRD for fictional feature
2. Validate all sections populated
3. Check alignment with existing PRDs
4. Verify feature tracking table included

**Issue Creation**:
1. Request help creating feature, bug, enhancement
2. Validate templates used correctly
3. Check cross-references to related issues
4. Verify appropriate labels suggested

**Ecosystem Queries**:
1. Run query-issues.fsx across all repos
2. Validate results accuracy (spot check 20 issues)
3. Test filtering, sorting, formatting
4. Verify performance < 2 minutes

**Backlog Analysis**:
1. Run analyze-backlog.fsx on known repo
2. Manually validate metrics (age, staleness)
3. Check recommendations are actionable
4. Compare against ecosystem averages

**Trend Analysis**:
1. Run trend-analysis.fsx for 30-day window
2. Manually review top trending labels
3. Validate emerging themes make sense
4. Check for false positives

### Integration Testing

**With qa-tester**:
1. Create PRD, then ask qa-tester for test plan
2. Verify test plan aligns with PRD acceptance criteria
3. Check cross-references work

**With release-manager**:
1. Ask about feature priority for release
2. Verify release-manager can access PRD context
3. Check coordination on changelog entries

### Acceptance Testing

**User Scenarios**:
- [ ] New contributor creates first issue with PM help
- [ ] Maintainer generates PRD for complex feature
- [ ] Developer checks ecosystem for related work
- [ ] Project lead analyzes backlog health
- [ ] Contributor validates feature alignment

**Quality Checks**:
- [ ] PRDs follow template structure
- [ ] Issues have appropriate labels
- [ ] Cross-repo queries are accurate
- [ ] Metrics are validated against manual checks
- [ ] Recommendations are helpful (user survey)

## Success Criteria

### Quantitative Metrics

- **Adoption**: 80% of PRDs created using Product Manager skill
- **Issue Quality**: 90% of issues created with PM help are well-structured (manual review)
- **Query Accuracy**: 95% precision on cross-repo issue searches
- **Performance**: All scripts complete within SLA (30s single-repo, 2min ecosystem)
- **Coverage**: All 6 Morphir repos covered by ecosystem queries

### Qualitative Metrics

- **User Satisfaction**: Positive feedback from 4+ contributors
- **Maintainer Impact**: Reduced time spent triaging issues
- **Knowledge Transfer**: New contributors feel confident creating issues/PRDs
- **Alignment**: Features better aligned with Morphir philosophy (maintainer assessment)
- **Integration**: Smooth coordination with qa-tester and release-manager

### Completion Criteria

- [ ] All P0 features implemented and tested
- [ ] All P1 features implemented and tested
- [ ] Documentation complete and reviewed
- [ ] Integration tested with other skills
- [ ] At least 3 real PRDs created using the skill
- [ ] At least 10 real issues created with PM assistance
- [ ] Ecosystem queries validated across all repos
- [ ] Maintainer sign-off

## Implementation Notes

### 2025-12-18: Initial PRD Creation
- **Decision**: Start with comprehensive PRD before implementation
- **Rationale**: Complex skill requiring careful design and alignment with existing patterns
- **Impact**: Clear roadmap for phased implementation
- **Files**: This PRD (product-manager-skill.md)

## Open Questions

### Q1: Should the Product Manager skill fetch live documentation from morphir.finos.org?
**Status**: Open
**Options**:
1. Fetch live docs via WebFetch tool
2. Maintain local cache of key documentation
3. Reference docs via links only

**Decision Needed By**: Phase 1 (Week 1)
**Impact**: Affects skill.md design and response accuracy

### Q2: How should the skill handle conflicting guidance across repos?
**Status**: Open
**Example**: morphir-elm uses one convention, morphir-dotnet uses another
**Options**:
1. Always favor reference implementation (morphir-elm)
2. Favor current repo context
3. Present both and explain tradeoffs

**Decision Needed By**: Phase 1 (Week 1)
**Impact**: Affects ecosystem map and playbook design

### Q3: Should F# scripts use GitHub CLI or direct API calls?
**Status**: Open
**Options**:
1. GitHub CLI (`gh`) for simplicity and auth
2. Direct API calls via HTTP client for flexibility
3. Hybrid approach

**Recommendation**: GitHub CLI for Phase 1, evaluate direct API if needed
**Decision Needed By**: Phase 1 (Week 1)
**Impact**: Affects script architecture and dependencies

### Q4: How deep should trend analysis go?
**Status**: Open
**Options**:
1. Label frequency and time-series only
2. Add NLP for theme extraction from titles/descriptions
3. Add sentiment analysis

**Recommendation**: Start with label frequency, add NLP in Phase 3 if valuable
**Decision Needed By**: Phase 3 (Week 3)
**Impact**: Affects trend-analysis.fsx complexity and dependencies

## References

### Project Documentation
- [AGENTS.md](../../../../AGENTS.md) - Primary agent guidance
- [CLAUDE.md](../../../../CLAUDE.md) - Claude Code-specific guidance
- [QA Tester Skill](../../../.claude/skills/qa-tester/skill.md)
- [Release Manager Skill](../../../.claude/skills/release-manager/skill.md)
- [Existing PRDs](./_index.md)

### Morphir Resources
- [Morphir Homepage](https://morphir.finos.org/)
- [morphir (core spec)](https://github.com/finos/morphir)
- [morphir-elm (reference)](https://github.com/finos/morphir-elm)
- [morphir-jvm](https://github.com/finos/morphir-jvm)
- [morphir-scala](https://github.com/finos/morphir-scala)
- [morphir-dotnet (this repo)](https://github.com/finos/morphir-dotnet)
- [morphir-examples](https://github.com/finos/morphir-examples)

### Related Standards
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Issues Best Practices](https://docs.github.com/en/issues/tracking-your-work-with-issues/quickstart)
- [Writing Good PRDs](https://www.atlassian.com/agile/product-management/requirements)

---

**Last Updated**: 2025-12-18
**Next Review**: After Phase 1 completion (Week 2)
