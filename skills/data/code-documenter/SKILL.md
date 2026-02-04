---
name: code-documenter
description: Expert documentation generator for coding projects. Analyzes codebases to create thorough, comprehensive documentation for developers and users. Supports incremental updates, multi-audience documentation, architecture decision records, and documentation health tracking. Works with any project type (APIs, CLIs, web apps, libraries). Use when you need to document a new project, update docs after adding features, or create comprehensive documentation for open source releases.
---

# Code Documenter Skill

An intelligent documentation system that analyzes codebases and generates thorough, comprehensive documentation tailored to your project type and audience needs.

## Core Philosophy

**Documentation serves readers, not authors.** Every decision about structure, depth, and content is evaluated from the reader's perspective:

- Will this help them understand?
- Will this help them succeed?
- Will this answer their questions?
- Does this earn its place?

**Comprehensive without overwhelm.** Thorough coverage of what matters, ruthless cutting of what doesn't. The goal is complete, accurate, useful documentation—not exhaustive documentation of every line of code.

**Documentation as code artifact.** Docs should be versioned, tested, and maintained with the same rigor as code. They're not afterthoughts; they're essential.

## When to Use This Skill

**Primary use cases:**
- After completing significant new work (epic, major feature, new app)
- When shipping an open source project
- When documentation has fallen out of sync with code
- When onboarding requires better documentation
- When setting up a new project properly

**Not for:**
- In-progress features (wait until stable)
- Code comments or docstrings (this generates external docs)
- API reference generation from code (use language-specific tools for that)

## Session Flow

### Mode Selection

The skill operates in two modes:

| Mode | When to Use | Behavior |
|------|-------------|----------|
| **Quick Mode** | Incremental updates after new features | Autonomous, fast, focused on what changed |
| **Comprehensive Mode** | New projects, major overhauls, first-time setup | Collaborative, thorough, quality gates throughout |

**The skill will ask:** "Quick update or comprehensive documentation?"

### Phase 1: Multi-Agent Project Analysis

The skill deploys specialized analysis agents to understand your project:

```
Analysis Phase:
├─ Agent 1: Project Structure
│  └─ Scanning file tree, identifying project type, tech stack
├─ Agent 2: Code Surface Analysis  
│  └─ Finding APIs, components, commands, exports
├─ Agent 3: Dependency Analysis
│  └─ Reviewing packages, frameworks, key dependencies
├─ Agent 4: Git History Analysis
│  └─ Analyzing commits since last doc update
├─ Agent 5: Existing Documentation Review
│  └─ Reading current docs, assessing state
└─ Synthesis: Generating documentation plan...
```

**Quick Mode:** Focused analysis on what changed since last update  
**Comprehensive Mode:** Full analysis of entire project

Each agent reports findings in structured format. You see everything happening.

### Phase 2: Documentation State Assessment

The skill compares code state vs. documentation state:

**If manifest exists (`.doc-state.json`):**
- Loads documentation state from last run
- Compares current code vs. last documented state
- Identifies what's changed (added/modified/removed)
- Shows you the documentation debt

**If no manifest:**
- First time documenting this project
- Will create fresh manifest after completion

**Key metrics shown:**
- **Health Score:** Current documentation health (0-100)
- **Coverage:** What % of public surface is documented
- **Freshness:** How current are docs vs. code
- **Debt:** What needs attention (prioritized)

### Phase 3: Audience & Scope Discovery

The skill asks:

1. **"Who needs these docs?"**
   - Developers only
   - Users only  
   - Both developers and users

2. **"What depth of documentation?"**
   - **Standard:** Right-sized coverage (4,000-7,000 words)
   - **Deep:** Comprehensive with internals (8,000-12,000 words)

**Quick Mode:** Uses stored preferences from manifest  
**Comprehensive Mode:** Asks explicitly, shows examples

### Phase 4: Documentation Boundaries

The skill proposes what should be documented:

```
Based on my analysis of your Express + PostgreSQL API:

PUBLIC SURFACE (Always Document)
├─ 12 API endpoints in /routes
├─ Database schema (3 tables)
├─ 14 environment variables
└─ Authentication flow

INTERNAL IMPLEMENTATION (Recommended for Deep)
├─ 6 middleware functions
├─ Error handling patterns
└─ Database migration strategy

INFRASTRUCTURE (Essential for all levels)
├─ Docker setup
├─ CI/CD pipeline
└─ Deployment process

EXCLUDED (Recommend skip)
├─ Test files (obvious from names)
├─ Build scripts (standard tooling)
└─ Internal helpers (<10 lines each)

Adjust these boundaries? [approve/modify]
```

You approve or adjust before documentation generation begins.

### Phase 5: Documentation Plan Presentation

The skill presents a complete plan:

```
DOCUMENTATION PLAN

Structure:
└─ /docs
   ├─ developers/
   │  ├─ api.md (API endpoint reference)
   │  ├─ architecture.md (System design + diagrams)
   │  ├─ contributing.md (How to contribute)
   │  ├─ deployment.md (Deploy & operate)
   │  ├─ troubleshooting.md (Common issues)
   │  ├─ examples/ (12 runnable examples)
   │  └─ adr/ (4 architecture decisions)
   ├─ users/
   │  ├─ getting-started.md (Quick start guide)
   │  ├─ features.md (Feature overview)
   │  ├─ troubleshooting.md (User-facing issues)
   │  └─ examples/ (5 user examples)
   ├─ CHANGELOG.md (Documentation change log)
   └─ documentation-map.md (Navigation guide)

Files to update:
- README.md (complete rewrite, progressive disclosure)
- docs/developers/api.md (2 new endpoints, 1 modified)
- docs/CHANGELOG.md (new entry)

Files to create:
- docs/adr/004-caching-strategy.md (new decision)
- docs/developers/examples/pagination.js (new example)

Files to remove:
- docs/developers/legacy-auth.md (endpoint removed)

Estimated scope: ~5,200 words total
Target health score: 92/100

Proceed? [yes/adjust scope/abort]
```

**Comprehensive Mode:** Review and approve before generation  
**Quick Mode:** Brief preview, option to review or proceed

### Phase 6: Documentation Generation

#### Comprehensive Mode (with Quality Gates)

The skill works through documentation in phases, pausing for review:

**Gate 1: Core Documentation** (README + Getting Started)
- Generates README with progressive disclosure
- Creates getting started guides
- **Quality Check:** Does this hook and onboard effectively?
- **You review and approve or request changes**

**Gate 2: Reference Documentation** (API/Commands/Components)
- Generates reference documentation
- Creates working examples
- **Quality Check:** Is everything covered? Examples clear?
- **You review and approve or request changes**

**Gate 3: Architecture & Decisions**
- Documents architecture with Mermaid diagrams
- Creates ADRs for key decisions
- **Quality Check:** Does this explain the WHY?
- **You review and approve or request changes**

**Gate 4: Supporting Documentation**
- Generates troubleshooting guides
- Creates contributing guidelines
- Documentation map for navigation
- **Quality Check:** Complete and helpful?
- **You review and approve or request changes**

**Gate 5: Polish & Verification**
- Generates test scripts for examples
- Creates link validation script
- Runs accessibility check
- Final health score calculation
- **Final review**

#### Quick Mode (Autonomous)

The skill executes the plan efficiently:
- Updates only changed sections
- Preserves manual edits in unchanged areas
- Generates new content as needed
- Updates manifest and changelog
- Reports final results

### Phase 7: Session Completion

The skill produces:

**Files Created/Updated:**
- All documentation files as planned
- `.doc-state.json` (updated manifest)
- `docs/CHANGELOG.md` (new entry)
- Test and validation scripts

**Documentation Health Report:**
```
DOCUMENTATION HEALTH REPORT

Overall Health Score: 92/100 (↑ from 78)

Component Scores:
├─ Coverage Health: 95/100 (↑ from 82)
│  └─ 97% of public surface documented
├─ Freshness Health: 98/100 (↑ from 65)
│  └─ All docs current as of commit a3f2b1c
├─ Quality Health: 88/100 (↑ from 81)
│  └─ 12 examples, 4 ADRs, troubleshooting complete
└─ Consistency Health: 90/100 (↑ from 84)
   └─ Tone consistent, terminology standardized

Debt Status:
├─ Critical: 0 items (was 2)
├─ Important: 1 item (was 4)
└─ Minor: 3 items (unchanged)

Next session recommendations:
- Document the new webhook system (flagged as potential)
- Add performance troubleshooting section
- Consider hosting docs on GitHub Pages
```

**Session Notes:**
- Decisions made
- Scope adjustments
- What was included/excluded and why
- Next steps

## File Outputs

### Core Documentation Structure

**Developer-only projects:**
```
/docs
├── CHANGELOG.md
├── api.md / commands.md / components.md
├── architecture.md
├── contributing.md
├── deployment.md
├── troubleshooting.md
├── examples/
│   ├── example-1.js
│   ├── example-2.js
│   └── test-examples.sh
├── adr/
│   ├── 001-initial-decisions.md
│   ├── 002-database-choice.md
│   └── ...
└── scripts/
    ├── validate-links.sh
    └── accessibility-check.md
```

**Multi-audience projects:**
```
/docs
├── CHANGELOG.md
├── documentation-map.md
├── users/
│   ├── getting-started.md
│   ├── features.md
│   ├── troubleshooting.md
│   └── examples/
│       ├── basic-usage.js
│       └── advanced-usage.js
├── developers/
│   ├── api.md / architecture.md
│   ├── contributing.md
│   ├── deployment.md
│   ├── troubleshooting.md
│   ├── examples/
│   │   ├── integration.js
│   │   ├── extending.js
│   │   └── test-examples.sh
│   └── adr/
│       ├── 001-framework-choice.md
│       └── ...
└── scripts/
    ├── validate-links.sh
    └── accessibility-check.md
```

### Documentation Manifest (`.doc-state.json`)

Tracks complete documentation state:

```json
{
  "version": "1.0",
  "project": {
    "name": "my-api",
    "type": "express-api",
    "lastScanned": "2025-01-10T14:30:00Z",
    "gitCommit": "a3f2b1c"
  },
  "preferences": {
    "audiences": ["developers", "users"],
    "depthLevel": "standard",
    "tone": "professional"
  },
  "healthScore": {
    "overall": 92,
    "components": {
      "coverage": 95,
      "freshness": 98,
      "quality": 88,
      "consistency": 90
    },
    "trend": [78, 85, 92]
  },
  "coverage": {
    "endpoints": {"total": 12, "documented": 12, "changed": 0},
    "components": {"total": 8, "documented": 8, "changed": 0},
    "schemas": {"total": 3, "documented": 3, "changed": 0}
  },
  "debt": {
    "critical": [],
    "important": [
      {
        "item": "Document webhook system",
        "effort": "medium",
        "status": "to-fix"
      }
    ],
    "minor": [
      {
        "item": "Add performance troubleshooting",
        "effort": "low",
        "status": "accepted"
      }
    ]
  },
  "documentationMap": {
    "README.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["overview", "quickstart"],
      "wordCount": 850
    },
    "docs/developers/api.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["endpoints"],
      "wordCount": 2400
    }
  }
}
```

## Collaboration Behaviors

### In Comprehensive Mode

**Proactive contributions:**
- "I notice you're using Redis but there's no ADR explaining why—should I document that decision?"
- "Your error handling is sophisticated. This deserves explanation in architecture docs."
- "The authentication flow is non-standard. Users will have questions—let me address them."

**Challenge assumptions:**
- "You said 'standard depth' but you have 47 endpoints. That needs Deep documentation."
- "This 'getting started' guide assumes too much. Your users won't know X."
- "Three examples aren't enough here. The concept is complex."

**Surface insights:**
- "Your git history shows you refactored auth 3 times. That's an ADR waiting to be written."
- "These three files handle all business logic but aren't documented at all. Gap."
- "You have inline JSDoc but it contradicts what's in the markdown docs. Consistency issue."

### In Quick Mode

**Efficient execution:**
- "Updating 3 files based on changes in commit a3f2b1c..."
- "2 new endpoints detected, adding to api.md..."
- "Removed documentation for deleted legacy-auth endpoint..."

**Flag concerns:**
- "Warning: Manual changes detected in architecture.md, preserving your edits"
- "Note: Health score dropped from 92 to 85 due to new undocumented features"

## Quality Standards

The skill maintains high documentation quality through:

### Clarity
- Concepts explained before they're used
- Technical terms defined on first use
- Examples precede or immediately follow concepts
- Progressive disclosure (simple → complex)

### Completeness
- Every public-facing element documented
- Edge cases and gotchas addressed
- Troubleshooting for predictable failures
- Examples for common use cases

### Accuracy
- All facts verified against code
- Examples tested and working
- Links validated
- No outdated information

### Accessibility
- Diagrams include alt text
- Links have descriptive text
- Heading hierarchy is logical
- Code snippets have language labels

### Consistency
- Terminology used uniformly
- Tone maintained throughout
- Formatting standardized
- Structure predictable

## Special Features

### Architecture Decision Records (ADRs)

Captures WHY decisions were made:

The skill identifies decision points through:
- Major dependency additions (git history)
- Non-standard architectural patterns (code analysis)
- Framework/library choices
- Flagged commits with "decision" language
- Your explicit identification

Each ADR documents:
- Context (what was the situation?)
- Decision (what did we decide?)
- Rationale (why this choice?)
- Consequences (trade-offs accepted)
- Alternatives considered

### Living, Tested Examples

Examples are runnable code in `/examples`:
- Actually work (not pseudocode)
- Cover common use cases
- Include test script to verify they run
- Referenced from documentation
- Maintained as code evolves

### Troubleshooting Database

Two flavors:
- **User troubleshooting:** Common errors, how to fix them
- **Developer troubleshooting:** Debugging guides, edge cases, gotchas

The skill seeds initial content in Comprehensive Mode, grows it in Quick Mode as you add real troubleshooting content.

### Documentation Map

For large projects, a navigation guide:
- Different learning paths (beginner/advanced)
- How docs connect to each other
- What to read when
- Visual/textual navigation aid

### Mermaid Diagrams

The skill generates code-based diagrams:
- Architecture diagrams
- Sequence diagrams
- Entity-relationship diagrams
- State diagrams
- Flowcharts

All version-controllable, all render in GitHub.

### Documentation Hosting Integration

Detects if you're using:
- GitHub Pages
- ReadTheDocs
- GitBook
- MkDocs

Generates appropriate config files and optimizes structure for static site generation.

## Reference Documents

Load contextually when needed:

- **`references/project-types-guide.md`** — How to document different project types
- **`references/documentation-patterns.md`** — Common documentation patterns and structures
- **`references/quality-standards.md`** — Detailed quality criteria and examples
- **`references/manifest-spec.md`** — Technical specification for `.doc-state.json`
- **`references/depth-levels-guide.md`** — Standard vs. Deep explained with examples
- **`references/health-score-formula.md`** — How health score is calculated
- **`references/adr-guide.md`** — Writing effective Architecture Decision Records

## Templates

Available in `templates/`:

- **`README-template.md`** — Progressive disclosure README structure
- **`api-docs-template.md`** — API endpoint documentation
- **`component-docs-template.md`** — Component/module documentation
- **`troubleshooting-template.md`** — Troubleshooting guide structure
- **`contributing-template.md`** — Contributing guidelines
- **`documentation-map-template.md`** — Navigation guide template

## Success Criteria

Documentation is complete when:

✓ Health score ≥ 85  
✓ All critical and important debt resolved  
✓ Examples run without errors  
✓ Links validate successfully  
✓ Accessibility check passes  
✓ Tone is consistent throughout  
✓ You're confident someone could use your project from the docs alone

## Key Reminders

- **Reader-first always:** Every decision serves the reader
- **Git-aware:** Smart incremental updates, not regeneration
- **Transparency:** You see all analysis and decisions
- **Preserve quality:** Don't overwrite good manual edits
- **Test examples:** Generate test scripts for working code
- **Track health:** Health score trends over time
- **Prioritize debt:** Not all debt is equal
- **Comprehensive without exhaustive:** Document what matters
