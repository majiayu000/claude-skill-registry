---
name: project-documentation
description: Comprehensive codebase documentation generator following a layered methodology. This skill should be used when scanning and documenting a codebase for the first time, when creating onboarding documentation for new developers, when generating architecture overviews, walkthroughs, and API references. Supports README generation, architecture diagrams, entry point documentation, pattern guides, and edge case documentation.
---

# Project Documentation

Comprehensive skill for scanning codebases and generating layered documentation to help developers get familiar quickly.

## Overview

This skill implements a 6-phase documentation methodology:
1. **Understand** - Explore codebase before documenting
2. **Structure** - Create layered documentation (high/mid/low level)
3. **Essential Docs** - Generate core documents
4. **Functions** - Document code with intent
5. **Onboarding** - Create self-paced learning materials
6. **Maintain** - Keep documentation versioned and searchable

## Documentation Workflow

### Phase 1: Understand Before Documenting

Before writing documentation, thoroughly explore the codebase:

1. **Explore Version Control History**
   ```bash
   git log --oneline -50           # Recent changes
   git log --all --oneline --graph # Visual branch history
   git shortlog -sn                # Top contributors
   ```

2. **Analyze Code Structure**
   - Run `tree -L 3 -I node_modules` for structure
   - Identify entry points (main.*, index.*, app.*)
   - Detect framework patterns (React, Express, FastAPI, etc.)

3. **Read Development Tests**
   - Tests reveal how code is intended to work
   - Failed test history shows fixed issues
   - Test structure mirrors code architecture

4. **Trace Execution Flows**
   - Follow imports from entry points
   - Map API routes to handlers
   - Document data flow patterns

### Phase 2: Create Layered Documentation

Generate three documentation layers:

| Layer | Purpose | Audience | Location |
|-------|---------|----------|----------|
| High-Level | Architecture, design principles | New devs, stakeholders | `docs/architecture/` |
| Walkthrough | Flows, patterns, interactions | Contributing devs | `docs/walkthroughs/` |
| Low-Level | Functions, parameters, returns | Active maintainers | Inline + `docs/api/` |

### Phase 3: Essential Documents

Generate using templates in `templates/`:

1. **README.md** - See [templates/readme-template.md](templates/readme-template.md)
2. **Architecture Overview** - See [templates/architecture-template.md](templates/architecture-template.md)
3. **Walkthrough Guide** - See [templates/walkthrough-template.md](templates/walkthrough-template.md)
4. **API/Function Reference** - See [templates/api-reference-template.md](templates/api-reference-template.md)
5. **Setup Guide** - See [templates/setup-guide-template.md](templates/setup-guide-template.md)

### Phase 4: Document Functions Effectively

When documenting individual functions:

- **Describe WHY, not just WHAT** - Business assumptions, algorithm steps
- **Use meaningful names** - Self-documenting code
- **Document intent** - Design choices, trade-offs
- **Include examples** - Expected usage patterns

Reference: [references/function-documentation.md](references/function-documentation.md)

### Phase 5: Onboarding-Focused Documentation

Create self-paced onboarding materials:

- **Clear language** - Avoid jargon without explanation
- **Code snippets** - Illustrate concepts with examples
- **Consistent naming** - Classes, functions, variables, files
- **Decision rationale** - Explain coding decisions

### Phase 6: Maintainability

- Version documentation with source code
- Make documentation searchable
- Link from team communication channels
- Incrementally improve as codebase evolves

## Documentation Priority Order

Generate documentation in this order:

1. **README** with setup instructions (get developers running)
2. **Architecture diagram** showing major components
3. **Entry points** documentation (where code starts)
4. **Core patterns** used throughout codebase
5. **Key functions/modules** with purpose and examples
6. **Edge cases and gotchas** that trip up newcomers

## Output Structure

```
docs/
├── README.md                    # Project overview
├── architecture/
│   ├── overview.md              # System architecture
│   ├── components.md            # Component descriptions
│   └── diagrams/                # Architecture diagrams
├── walkthroughs/
│   ├── entry-points.md          # Where code starts
│   ├── data-flow.md             # How data moves
│   └── patterns.md              # Recurring patterns
├── api/
│   ├── endpoints.md             # API endpoints
│   └── functions.md             # Key functions
├── setup/
│   ├── installation.md          # Installation guide
│   ├── configuration.md         # Configuration options
│   └── troubleshooting.md       # Common issues
└── onboarding/
    ├── quickstart.md            # 5-minute start
    ├── tutorials/               # Hands-on tutorials
    └── gotchas.md               # Edge cases & tips
```

## Scanning Checklist

- [ ] Version control history analyzed
- [ ] Project type and framework identified
- [ ] Entry points documented
- [ ] Directory structure mapped
- [ ] Dependencies catalogued
- [ ] Key patterns identified
- [ ] Configuration files documented
- [ ] README created/updated
- [ ] Architecture overview generated
- [ ] Walkthrough guides created
- [ ] API reference generated
- [ ] Setup guide complete
- [ ] Onboarding materials ready
