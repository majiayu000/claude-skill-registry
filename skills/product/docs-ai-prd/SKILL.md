---
name: docs-ai-prd
description: Write PRDs, specs, and project context optimized for coding assistants (Claude Code, Cursor, Copilot, Custom GPTs). Includes CLAUDE.md generation, session planning, and templates for creating documentation that tools can execute effectively.
---

# PRDs & Project Context — Quick Reference

Create product requirements and project context that humans and coding assistants can execute effectively. This skill combines **PRD/spec templates** with **project context generation** so implementation work is faster and less ambiguous.

**Two complementary capabilities:**
1. **PRDs & Specs** - Requirements, specs, stories, and acceptance criteria for delivery
2. **Project Context** - Document architecture, conventions, and tribal knowledge for onboarding

---

**Modern Best Practices (Dec 2025)**:
- Decision-first: document the decision, owner, and due date (not just background).
- Testability: every requirement has acceptance criteria and explicit non-goals.
- Metrics: define formula + timeframe + data source; add guardrails for side effects.
- Change control: version docs and keep updates diff-friendly (small deltas, dated changes).
- Safety: privacy, security, and accessibility are requirements, not “later”.

## Do / Avoid (Dec 2025)

### Do

- Start with a short executive summary (decision, users, scope, success, risks).
- Define acceptance criteria in testable language (Gherkin or equivalent).
- Keep requirements unambiguous (“must/should/may”) and tie each to evidence.
- Link to supporting docs instead of pasting long appendices into the PRD.

### Avoid

- Vague requirements (“fast”, “easy”, “intuitive”) without measurable definitions.
- Mixing draft notes, open questions, and final requirements without labels.
- Metrics without a measurement plan (who measures, where, and when).
- Docs with no owner or review cadence (guaranteed staleness).

## What Good Looks Like

- Coverage: every requirement is testable and traceable to a user/job or risk.
- Clarity: scope, non-goals, and constraints are explicit and consistent across docs.
- Measurement: success metrics include baselines, targets, and guardrails.
- Execution: milestones, owners, and “how we verify” steps are written before build starts.
- Hygiene: links are valid, sources are dated, and the document is versioned.

## When to Use This Skill

Use this skill when a user requests:
- A PRD/spec/story map/acceptance criteria
- Defined metrics, constraints, risks, and non-goals for delivery
- Project context docs for onboarding (architecture, conventions, key files)
- A plan to execute a non-trivial change (>3 files)

---

## Quick Reference

### Core PRDs & Specs (Default)

| Task | Template | When to Use |
|------|----------|-------------|
| PRD creation | `templates/prd/prd-template.md` | Writing product requirements |
| Tech spec | `templates/spec/tech-spec-template.md` | Engineering design doc |
| Planning checklist | `templates/planning/planning-checklist.md` | Before complex feature |
| Story mapping | `templates/stories/story-mapping-template.md` | User journey visualization |
| Gherkin/BDD | `templates/stories/gherkin-example-template.md` | Acceptance criteria |

---

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

### Optional Quick Reference

| Task | Template | When to Use |
|------|----------|-------------|
| AI PRD | `templates/prd/ai-prd-template.md` | AI feature/system (eval + risk + monitoring) |
| Agentic session | `templates/planning/agentic-session-template.md` | AI coding session (>3 files) |
| Prompt playbook | `templates/prompting/prompt-playbook.md` | Repeatable prompts for complex work |
| Metrics tracking | `templates/metrics/agentic-coding-metrics-template.md` | AI coding effectiveness and ROI |

### Project Context (CLAUDE.md)

| Context Type | Template | Priority |
|--------------|----------|----------|
| **Architecture** | `templates/architecture-context.md` | Critical |
| **Conventions** | `templates/conventions-context.md` | High |
| **Tribal Knowledge** | `templates/tribal-knowledge-context.md` | High |
| **Key Files** | `templates/key-files-context.md` | Critical |
| **Dependencies** | `templates/dependencies-context.md` | Medium |
| **Web App** | `templates/web-app-context.md` | By project type |
| **CLI Tool** | `templates/cli-context.md` | By project type |
| **Library** | `templates/library-context.md` | By project type |
| **Minimal Quick Start** | `templates/minimal-claudemd.md` | 5-minute start |

### AI PRD Essentials (Dec 2025)

- Data: sources, rights, retention, PII classification, and access controls.
- Evaluation: baseline, offline/human/online eval plan, acceptance criteria, stop rules.
- Failure modes: user harm, injection/tool misuse, leakage, bias; mitigations and residual risk.
- Monitoring: drift, quality regression, incidents, rollback/kill switch.

## Decision Tree

```text
User needs: [Documentation Task]
     AI-Assisted Coding?
        Non-trivial feature (>3 files)?  Planning checklist + agentic session
        Prompt engineering?  Prompt playbook
        Measuring ROI?  Metrics tracking template
        Simple task (<3 files)?  Direct implementation
    
     Project Onboarding?
        New to codebase?  Generate CLAUDE.md (architecture + conventions)
        Team knowledge transfer?  Tribal knowledge template
        Quick context?  Minimal CLAUDE.md template
    
     Traditional PRD?
        Product requirements?  PRD template
        AI feature/system?  AI PRD template
        Technical design?  Tech spec template
        Acceptance criteria?  Gherkin/BDD template
    
     Cross-Domain Needs?
         API design?  Use dev-api-design skill
         Architecture?  Use software-architecture-design skill
         Codebase docs?  Use docs-codebase skill
```

---

## Context Extraction Workflow (CLAUDE.md)

```text
User needs: [CLAUDE.md for project]
    
     Step 1: Scan codebase structure
        Identify language/framework
        Map directory organization
        Find configuration files
    
     Step 2: Extract architecture
        Component relationships
        Data flow patterns
        Key abstractions
    
     Step 3: Identify conventions
        Naming patterns (files, functions, variables)
        Import/export patterns
        Testing conventions
    
     Step 4: Mine tribal knowledge
        Git history for "why" commits
        README/docs for context
        Comments explaining decisions
    
     Step 5: Document key files
        Entry points (main.*, index.*, app.*)
        Configuration (config.*, .env.example)
        Core business logic locations
    
     Step 6: Generate CLAUDE.md
         Assemble sections
         Verify accuracy
         Add usage guidance
```

---

## CLAUDE.md Structure

Optimal project memory file includes:

### 1. Project Overview (Required)

```markdown
# Project Name

Brief description of purpose.

## Tech Stack
- Language: [e.g., TypeScript 5.x]
- Framework: [e.g., Next.js 16]
- Database: [e.g., PostgreSQL 15]
```

### 2. Architecture (Required)

```markdown
## Architecture

### Key Components
- `src/api/` - REST API handlers
- `src/services/` - Business logic
- `src/models/` - Database models

### Data Flow
1. Request  API handler
2. Handler  Service  Database
3. Response  Service  Handler
```

### 3. Conventions (Required)

```markdown
## Conventions

### Naming
- Files: kebab-case (`user-service.ts`)
- Functions: camelCase (`getUserById`)
- Classes: PascalCase (`UserService`)

### Patterns
- Repository pattern for data access
- DTOs for API input/output
```

### 4. Key Files (Required)

```markdown
## Key Files

| Purpose | Location | Notes |
|---------|----------|-------|
| Entry point | `src/index.ts` | Server bootstrap |
| Config | `src/config/index.ts` | Environment loading |
| Auth | `src/middleware/auth.ts` | JWT validation |
```

### 5. Tribal Knowledge (Recommended)

```markdown
## Important Context

### Why PostgreSQL over MongoDB
Chose PostgreSQL for ACID requirements. Decision date: 2024-03.

### Known Gotchas
- `UserService.create()` triggers async email - don't await in tests
- Cache invalidation requires manual trigger after DB updates
```

### 6. AI-Specific Guidance (Optional)

```markdown
## For AI Assistants

### When modifying:
- Follow existing patterns in similar files
- Add tests for new functionality
- Run `npm run lint` before committing

### Avoid:
- Direct database queries (use repositories)
- Console.log in production (use logger)
```

---

## Navigation

### Resources - PRDs & Agentic Coding

- [resources/agentic-coding-best-practices.md](resources/agentic-coding-best-practices.md)
- [resources/vibe-coding-patterns.md](resources/vibe-coding-patterns.md)
- [resources/prompt-engineering-patterns.md](resources/prompt-engineering-patterns.md)
- [resources/requirements-checklists.md](resources/requirements-checklists.md)
- [resources/traditional-prd-writing.md](resources/traditional-prd-writing.md)
- [resources/pm-team-collaboration.md](resources/pm-team-collaboration.md)
- [resources/security-review-checklist.md](resources/security-review-checklist.md)
- [resources/tool-comparison-matrix.md](resources/tool-comparison-matrix.md)
- [resources/operational-guide.md](resources/operational-guide.md)

### Resources - Context Extraction

- [resources/architecture-extraction.md](resources/architecture-extraction.md)
- [resources/convention-mining.md](resources/convention-mining.md)
- [resources/tribal-knowledge-recovery.md](resources/tribal-knowledge-recovery.md)

### Templates - PRDs & Planning

- [templates/prd/prd-template.md](templates/prd/prd-template.md)
- [templates/prd/ai-prd-template.md](templates/prd/ai-prd-template.md)
- [templates/spec/tech-spec-template.md](templates/spec/tech-spec-template.md)
- [templates/planning/planning-checklist.md](templates/planning/planning-checklist.md)
- [templates/planning/agentic-session-template.md](templates/planning/agentic-session-template.md)
- [templates/prompting/prompt-playbook.md](templates/prompting/prompt-playbook.md)
- [templates/stories/story-mapping-template.md](templates/stories/story-mapping-template.md)
- [templates/stories/gherkin-example-template.md](templates/stories/gherkin-example-template.md)
- [templates/metrics/agentic-coding-metrics-template.md](templates/metrics/agentic-coding-metrics-template.md)

### Templates - Project Context

- [templates/architecture-context.md](templates/architecture-context.md)
- [templates/conventions-context.md](templates/conventions-context.md)
- [templates/tribal-knowledge-context.md](templates/tribal-knowledge-context.md)
- [templates/key-files-context.md](templates/key-files-context.md)
- [templates/dependencies-context.md](templates/dependencies-context.md)
- [templates/web-app-context.md](templates/web-app-context.md)
- [templates/cli-context.md](templates/cli-context.md)
- [templates/library-context.md](templates/library-context.md)
- [templates/minimal-claudemd.md](templates/minimal-claudemd.md)
- [templates/nodejs-context.md](templates/nodejs-context.md)
- [templates/python-context.md](templates/python-context.md)
- [templates/react-context.md](templates/react-context.md)
- [templates/go-context.md](templates/go-context.md)
- [templates/api-service-context.md](templates/api-service-context.md)

---

## Extraction Commands

Quick commands to gather project context:

```bash
# Directory structure
tree -L 3 -I 'node_modules|.git|dist|build' > structure.txt

# Package dependencies
cat package.json | jq '.dependencies, .devDependencies'

# Recent significant commits
git log --oneline --since="6 months ago" --grep="refactor\|migrate\|breaking\|major"

# Find entry points
find . -name "index.*" -o -name "main.*" -o -name "app.*" | head -20

# Mining "why" comments
grep -r "TODO\|FIXME\|HACK\|NOTE\|because\|workaround" --include="*.ts" --include="*.js"
```

---

## Quality Checklist

### PRD Quality

- [ ] Clear problem statement
- [ ] Measurable success criteria
- [ ] Unambiguous acceptance criteria
- [ ] Edge cases documented
- [ ] Dependencies identified
- [ ] AI can execute without clarification

### CLAUDE.md Quality

- [ ] Project overview is accurate and current
- [ ] Architecture reflects actual structure
- [ ] Key files exist and locations are correct
- [ ] Conventions match actual code patterns
- [ ] Commands actually work
- [ ] No sensitive information (secrets, internal URLs)

---

## External Resources

See [data/sources.json](data/sources.json) for curated links.

---

## Related Skills

- **Codebase Documentation**: [../docs-codebase/SKILL.md](../docs-codebase/SKILL.md) - README, API docs, ADRs, changelogs
- **Documentation Coverage**: [../qa-docs-coverage/SKILL.md](../qa-docs-coverage/SKILL.md) - Audit for documentation gaps
- **Product Management**: [../product-management/SKILL.md](../product-management/SKILL.md) - Product strategy, positioning
- **Architecture Design**: [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) - System design patterns
- **API Design**: [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) - REST/GraphQL patterns
- **Testing**: [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) - Test strategy for AI code
- **Git Workflow**: [../git-workflow/SKILL.md](../git-workflow/SKILL.md) - Git history analysis

---

## Usage Notes

**For Claude**: When user needs AI-friendly documentation:

1. **Identify need** - PRD/spec or project context (CLAUDE.md)?
2. **Reference template** - Use appropriate template from templates/
3. **Follow extraction** - For CLAUDE.md, run extraction commands
4. **Verify accuracy** - Check files exist, commands work
5. **Provide actionable output** - AI should execute without clarification

**Success criteria**:
- AI can navigate codebase without asking "where is X?"
- AI follows project conventions without being told
- PRDs have clear acceptance criteria AI can verify
- After reading docs, AI is productive in <5 minutes

---

> **Success Metric**: After reading CLAUDE.md + PRD, AI should produce production-quality code that matches team patterns on first attempt.
