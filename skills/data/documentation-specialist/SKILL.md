---
name: "documentation-specialist"
description: |
  This skill should be used when creating professional software documentation (SRS, PRD, OpenAPI,
  user manuals, tutorials, runbooks) from templates (greenfield) or reverse-engineering documentation
  from existing code like Spring Boot or FastAPI (brownfield). Also handles documentation audits/reviews,
  format conversion (Markdown, DOCX, PDF), and diagram generation (C4, Mermaid, PlantUML, ER, sequence).
  Use when asked to "create documentation", "document my code", "write SRS", "generate PRD", or "documentation specialist".
version: "3.0-PDA"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill"]
---

# Documentation Specialist Skill

## Quick Start

Software documentation creation, extraction, conversion, and diagramming capabilities.

**Capabilities:**
1. **Greenfield** - Create documentation from templates (SRS, PRD, OpenAPI, User Manuals, Tutorials, Runbooks)
2. **Brownfield** - Reverse-engineer documentation from code (Spring Boot, FastAPI)
3. **Audit** - Review and improve existing documentation
4. **Convert** - Transform formats (MD → DOCX → PDF)
5. **Diagram** - Generate visuals (Mermaid C4, PlantUML UML)

**Example Requests:**
```
Create an SRS for a billing system with PCI-DSS compliance
Document my Spring Boot application at ~/projects/customer-api
Create a user manual for my SaaS product
Write a database failover runbook
Audit my API documentation at docs/api/openapi.yaml
Convert docs/srs.md to Word format
Create a C4 container diagram for my microservices
```

**Execution Flow:**
1. Classify intent → 2. Load workflow → 3. Execute steps → 4. Generate documentation → 5. Present post-processing options

---

## Intent Classification

| Intent | Keywords | Workflow |
|--------|----------|----------|
| **CREATE_NEW** | "create", "generate", "write" + doc type | [greenfield-workflow.md](references/workflows/greenfield-workflow.md) |
| **CODE_TO_DOCS** | "document", "extract", path reference | [brownfield-workflow.md](references/workflows/brownfield-workflow.md) |
| **AUDIT** | "audit", "review", "check", "improve" | [audit-workflow.md](references/workflows/audit-workflow.md) |
| **CONVERT** | "convert", "to Word", "to PDF" | [convert-workflow.md](references/workflows/convert-workflow.md) |
| **DIAGRAM** | "diagram", "C4", "sequence", "ER" | [diagram-workflow.md](references/workflows/diagram-workflow.md) |
| **USER_DOCS** | "user manual", "how-to", "getting started" | [user-docs-workflow.md](references/workflows/user-docs-workflow.md) |
| **TUTORIAL** | "tutorial", "API guide", "CLI docs" | [tutorial-workflow.md](references/workflows/tutorial-workflow.md) |
| **RUNBOOK** | "runbook", "procedure", "incident" | [runbook-workflow.md](references/workflows/runbook-workflow.md) |

**CRITICAL**: Load only the workflow needed for the current intent. Avoid loading multiple workflows.

---

## Document Type → Template

**Requirements & Design:**
| Type | Template |
|------|----------|
| SRS | [requirements-srs.md](references/templates/markdown/requirements-srs.md) |
| PRD | [requirements-prd.md](references/templates/markdown/requirements-prd.md) |
| OpenAPI | [api-openapi.yaml](references/templates/markdown/api-openapi.yaml) |

**User Documentation:**
| Type | Template |
|------|----------|
| User Manual | [user-manual.md](references/templates/markdown/user-manual.md) |
| How-To Guide | [howto-guide.md](references/templates/markdown/howto-guide.md) |
| Getting Started | [getting-started.md](references/templates/markdown/getting-started.md) |

**Developer & Operations:**
| Type | Template |
|------|----------|
| Developer Tutorial | [developer-tutorial.md](references/templates/markdown/developer-tutorial.md) |
| Runbook | [runbook.md](references/templates/markdown/runbook.md) |

---

## Framework Detection (Brownfield)

| Framework | Detection | Mapping |
|-----------|-----------|---------|
| **Spring Boot** | `pom.xml`, `@SpringBootApplication` | [spring-boot-mapping.yaml](references/mappings/backend/spring-boot-mapping.yaml) |
| **FastAPI** | `requirements.txt`, `from fastapi import` | [fastapi-mapping.yaml](references/mappings/backend/fastapi-mapping.yaml) |

**Process**: Glob for detection files → Grep for patterns → Load mapping → Follow brownfield workflow

---

## On-Demand Resources

Load only what is needed for the current task.

### Workflows
- [Workflow TOC](references/workflows/TOC.md) - Navigation index
- [greenfield-workflow.md](references/workflows/greenfield-workflow.md)
- [brownfield-workflow.md](references/workflows/brownfield-workflow.md)
- [audit-workflow.md](references/workflows/audit-workflow.md)
- [convert-workflow.md](references/workflows/convert-workflow.md)
- [diagram-workflow.md](references/workflows/diagram-workflow.md)
- [user-docs-workflow.md](references/workflows/user-docs-workflow.md)
- [tutorial-workflow.md](references/workflows/tutorial-workflow.md)
- [runbook-workflow.md](references/workflows/runbook-workflow.md)

### Reference Guides
- [comprehensive-guide.md](references/reference/comprehensive-guide.md) - Navigation to all 27 reference guides

### Examples
- [Examples TOC](references/examples/TOC.md) - Navigation to all examples

---

## Skill Integration

| Skill | Invocation Trigger |
|-------|-------------------|
| **docx** | Request includes Word format |
| **pdf** | Request includes PDF format |
| **plantuml** | UML diagrams (ER, sequence, component) |
| **mermaid-architect** | C4 diagrams, flowcharts |

---

## Error Handling

| Error | Response |
|-------|----------|
| Cannot detect framework | Ask: "Is this Spring Boot, FastAPI, or another framework?" |
| Missing template | Use closest match, inform user |
| Skill not available | Offer markdown-only alternative |
| Ambiguous request | Ask: "Would you prefer SRS (formal) or PRD (agile)?" |

---

**End of SKILL.md (v3.0-PDA)**
