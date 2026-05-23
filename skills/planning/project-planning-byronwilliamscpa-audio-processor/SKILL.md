---
name: project-planning
description: >
  Generate initial project planning documents (PVS, ADR, Tech Spec, Roadmap) from a project
  concept description. Use when starting a new project, when docs/planning/ contains placeholder
  files, or when user requests project planning document generation.
version: 1.0.0
---

# Project Planning Skill

Generate four essential planning documents to guide AI-assisted development. These documents
maintain context coherence across coding sessions and prevent architectural drift.

## When to Use This Skill

- User describes a project concept and asks for planning documents
- Files in `docs/planning/` show "Awaiting Generation" status
- User invokes `/plan` command with project description
- Starting development on a new feature requiring architectural decisions

## Output Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Project Vision & Scope | `docs/planning/project-vision.md` | What & Why - problem, solution, scope |
| Technical Spec | `docs/planning/tech-spec.md` | How - architecture, data model, APIs |
| Development Roadmap | `docs/planning/roadmap.md` | When - phased implementation plan |
| Architecture Decision Record | `docs/planning/adr/adr-001-*.md` | Key technical decisions with rationale |

## Generation Process

### Step 1: Gather Project Context

Before generating, collect:
1. **Project description** from user input
2. **Technical constraints** from `pyproject.toml` and existing code
3. **Cookiecutter choices** reflected in project structure

### Step 2: Generate Documents in Order

Generate documents sequentially, as later documents reference earlier ones:

1. **Project Vision & Scope** - Establishes what we're building and why
2. **Architecture Decision Record** - Key technical choices based on PVS
3. **Technical Implementation Spec** - Detailed how-to based on ADRs
4. **Development Roadmap** - Implementation plan based on all above

### Step 3: Expert Review via Consensus

After generating each document, use the zen-mcp-server consensus tool to get expert review:

```
Use mcp__zen__consensus with gemini-3-pro-preview to review:

"Review this [document type] for sufficiency to begin development.

Evaluate:
1. SPECIFICITY: Are requirements concrete enough to implement?
2. COMPLETENESS: Are all critical sections filled with project-specific content?
3. FEASIBILITY: Are timelines and technical choices realistic?
4. CLARITY: Can a developer understand what to build from this?
5. GAPS: What critical information is missing?

Respond with:
- READY: Document is sufficient to begin work
- NEEDS REVISION: [List specific improvements required]

Document content:
[paste document content]"
```

**Review each document in order**:
1. PVS → Must be READY before generating ADR
2. ADR → Must be READY before generating Tech Spec
3. Tech Spec → Must be READY before generating Roadmap
4. Roadmap → Must be READY before completing

If any document NEEDS REVISION, incorporate feedback and re-review before proceeding.

### Step 4: Validate and Cross-Reference

After all documents pass review:
- Ensure documents reference each other correctly
- Verify technical choices are consistent across documents
- Flag any assumptions needing user validation
- Run validation script if available

## Document Generation Guidelines

### All Documents

- **Be specific**: Use concrete technologies, versions, and measurable criteria
- **No boilerplate**: Every section must contain project-specific information
- **Under 1000 words**: Dense information, minimal prose
- **Markdown format**: Use headers, bullets, tables for structure
- **Include TL;DR**: 2-3 sentence summary at top of each document

### Project Vision & Scope (PVS)

Use template: `templates/pvs-template.md`

Focus on:
- Problem being solved and user impact
- Core capabilities (3-5 max for MVP)
- Explicit scope boundaries (in vs out)
- Measurable success metrics

### Architecture Decision Record (ADR)

Use template: `templates/adr-template.md`

Create ADR for:
- Database/storage choice
- Authentication strategy
- API design approach
- Key framework decisions
- Any choice expensive to reverse

Format: `adr-001-{decision-slug}.md`

### Technical Implementation Spec

Use template: `templates/tech-spec-template.md`

Include:
- Complete tech stack with versions
- Component architecture diagram (ASCII)
- Data model with schemas
- API endpoints specification
- Security requirements
- Error handling approach

### Development Roadmap

Use template: `templates/roadmap-template.md`

Structure as:
- Phase 0: Foundation (environment, CI/CD)
- Phase 1: MVP Core (essential features)
- Phase 2: Enhancement (additional features)
- Phase 3: Polish (testing, documentation)

Each phase needs:
- Clear deliverables
- Success criteria (testable)
- Estimated duration
- Dependencies

## Pre-Filling from Project Context

When generating, incorporate known information:

```python
# From pyproject.toml / cookiecutter context
python_version = "3.12"
project_name = "Audio Processor"
project_slug = "audio_processor"
cli_framework = "Click"
containerization = "Docker"
```

## Quality Checklist

Before completing generation:

- [ ] All four documents created in `docs/planning/`
- [ ] Each document has TL;DR section
- [ ] No "[TODO]" or "[TBD]" placeholders remain
- [ ] Documents cross-reference each other
- [ ] Technical choices are consistent
- [ ] Success criteria are measurable
- [ ] Scope boundaries are explicit
- [ ] At least one ADR created

## Templates Reference

Templates are in `templates/` directory:
- `pvs-template.md` - Project Vision & Scope structure
- `adr-template.md` - Architecture Decision Record structure
- `tech-spec-template.md` - Technical Spec structure
- `roadmap-template.md` - Development Roadmap structure

## Detailed Guidance

For comprehensive documentation on each document type, see `reference/` directory:
- `reference/document-guide.md` - Full guidance for all document types
- `reference/prompting-patterns.md` - How to use documents during development

## After Generation

Instruct user to:
1. Review each document for accuracy
2. Validate assumptions marked with `[ ]`
3. Adjust timelines in roadmap if needed
4. Commit documents to version control
5. Reference documents in future development sessions

## Example Usage

When user says: "I want to build a CLI tool for managing personal finances..."

### Generation Flow with Consensus Review

1. **Generate PVS**
   - Read `templates/pvs-template.md`
   - Generate `docs/planning/project-vision.md` with finance CLI specifics
   - **Review**: `mcp__zen__consensus` with gemini-3-pro-preview → READY or revise

2. **Generate ADR**
   - Read `templates/adr-template.md`
   - Generate `docs/planning/adr/adr-001-database-choice.md` for SQLite decision
   - **Review**: `mcp__zen__consensus` with gemini-3-pro-preview → READY or revise

3. **Generate Tech Spec**
   - Read `templates/tech-spec-template.md`
   - Generate `docs/planning/tech-spec.md` with Python/Click/SQLite stack
   - **Review**: `mcp__zen__consensus` with gemini-3-pro-preview → READY or revise

4. **Generate Roadmap**
   - Read `templates/roadmap-template.md`
   - Generate `docs/planning/roadmap.md` with phased implementation
   - **Review**: `mcp__zen__consensus` with gemini-3-pro-preview → READY or revise

5. **Final Validation**
   - Run `scripts/validate-planning-docs.py`
   - Summarize what was created and review outcomes
   - List next steps for beginning development

### Consensus Review Prompt Template

```
mcp__zen__consensus with gemini-3-pro-preview:

Review this Project Vision & Scope document for Audio Processor.

EVALUATION CRITERIA:
1. SPECIFICITY - Can a developer implement from these requirements?
2. COMPLETENESS - All sections filled with project-specific content?
3. FEASIBILITY - Realistic scope for the described constraints?
4. CLARITY - Unambiguous success criteria and scope boundaries?
5. GAPS - Any critical missing information?

RESPOND:
- READY: Sufficient to proceed to next document
- NEEDS REVISION: [Specific improvements with examples]

DOCUMENT:
[Full document content here]
```

### MCP Server Requirement

This skill requires the zen-mcp-server for consensus review.
If not available, skip Step 3 and proceed with manual review.

Configuration: Ensure `mcp__zen__consensus` tool is accessible.
