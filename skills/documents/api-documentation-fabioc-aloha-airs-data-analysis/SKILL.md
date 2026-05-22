---
name: "API Documentation Skill"
description: "Technical documentation, API references, user guides, and docs-as-code workflows."
applyTo: "**/*doc*,**/*api*,**/*readme*,**/*guide*"
---

# API Documentation Skill

> Technical documentation, API references, user guides, and docs-as-code workflows.

---

## Documentation Project Scaffolding

### Recommended Folder Structure

```text
docs-project/
├── .github/
│   ├── copilot-instructions.md    # Docs-specific Alex context
│   └── prompts/
│       └── api-review.prompt.md
├── docs/
│   ├── index.md                   # Landing page / overview
│   ├── getting-started/
│   │   ├── installation.md
│   │   ├── quick-start.md
│   │   └── configuration.md
│   ├── guides/
│   │   ├── user-guide.md
│   │   └── admin-guide.md
│   ├── api/
│   │   ├── overview.md
│   │   ├── authentication.md
│   │   ├── endpoints/
│   │   │   └── [resource].md
│   │   └── errors.md
│   ├── reference/
│   │   ├── glossary.md
│   │   └── faq.md
│   └── contributing/
│       ├── style-guide.md
│       └── templates.md
├── examples/
│   ├── code-snippets/
│   └── sample-projects/
├── assets/
│   ├── images/
│   └── diagrams/
├── CHANGELOG.md
├── README.md
└── mkdocs.yml                     # Or docusaurus.config.js
```

### DOCS-PLAN.md Template

```markdown
# Documentation Plan: [Product/API Name]

## Scope
- **Product**: [What are we documenting?]
- **Audience**: [Developers / Admins / End Users]
- **Prerequisites**: [What readers should know]

## Documentation Types

| Type | Location | Status |
|------|----------|--------|
| Getting Started | docs/getting-started/ | ⬜ |
| User Guide | docs/guides/user-guide.md | ⬜ |
| API Reference | docs/api/ | ⬜ |
| Examples | examples/ | ⬜ |

## Style Guidelines
- **Tone**: [Technical but approachable]
- **Person**: [Second person - "you"]
- **Tense**: [Present tense]
- **Code style**: [Language-specific conventions]

## Quality Checklist
- [ ] All endpoints documented
- [ ] Code examples tested and working
- [ ] Screenshots current
- [ ] Links verified
- [ ] Spelling/grammar checked
```

### API-ENDPOINT.md Template

```markdown
# [Endpoint Name]

[One-line description of what this endpoint does]

## Request

\`\`\`http
[METHOD] /api/v1/[resource]
\`\`\`

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource identifier |

### Request Body

\`\`\`json
{
  "field": "value"
}
\`\`\`

## Response

### Success (200 OK)

\`\`\`json
{
  "data": {
    "id": "123",
    "field": "value"
  }
}
\`\`\`

### Errors

| Code | Description |
|------|-------------|
| 400 | Invalid request body |
| 401 | Unauthorized |
| 404 | Resource not found |

## Example

\`\`\`bash
curl -X GET "https://api.example.com/v1/resource/123" \
  -H "Authorization: Bearer $TOKEN"
\`\`\`
```

### copilot-instructions.md Template (Documentation Projects)

```markdown
# [Product Name] Documentation — Context

## Project Overview
[What product/API this documents, current status]

## Current Phase
- [x] Structure defined
- [ ] Getting started complete
- [ ] API reference complete
- [ ] Examples tested

## Key Files
- Docs plan: DOCS-PLAN.md
- Style guide: docs/contributing/style-guide.md
- API overview: docs/api/overview.md

## Alex Guidance
- **Audience**: [Developers with X experience level]
- **Tone**: Technical but approachable
- Use second person ("you") not third person
- Include working code examples for every endpoint
- Link to related endpoints/concepts

## Style Rules
- Headings: Sentence case
- Lists: No periods for fragments, periods for sentences
- Code: Include language identifier in fenced blocks
- Links: Use relative paths within docs/

## Don't
- Don't assume reader knows internal terminology
- Don't document deprecated features without clear warnings
- Don't include placeholder examples — all code must work
```

### Documentation Project Audit Checklist

```markdown
## Documentation Project Audit

### Structure Assessment
- [ ] Clear navigation hierarchy
- [ ] Getting started section exists
- [ ] API reference organized by resource
- [ ] Examples directory with working code

### Alex-Readiness Assessment
- [ ] copilot-instructions.md exists
- [ ] Audience clearly defined
- [ ] Style guide documented
- [ ] Key files linked

### Content Assessment
- [ ] All public endpoints documented
- [ ] Authentication explained
- [ ] Error codes listed
- [ ] Code examples in multiple languages (if applicable)

### Quality Assessment
- [ ] All links valid
- [ ] Code examples tested
- [ ] Screenshots current
- [ ] Consistent formatting
```

---

## Documentation Types

### API Reference Structure

| Section | Purpose |
|---------|---------|
| **Overview** | What the API does, base URL, versioning |
| **Authentication** | How to get and use credentials |
| **Rate Limits** | Throttling rules and headers |
| **Endpoints** | Per-endpoint details |
| **Errors** | Error format and common codes |
| **Changelog** | API version history |

### User Guide Structure

| Section | Purpose |
|---------|---------|
| **Introduction** | What, why, for whom |
| **Installation** | How to set up |
| **Quick Start** | First success in 5 minutes |
| **Core Concepts** | Key ideas to understand |
| **How-To Guides** | Task-oriented walkthroughs |
| **Troubleshooting** | Common issues and fixes |

### README Best Practices

| Section | Required? |
|---------|-----------|
| Project name + description | ✅ Yes |
| Badges (build, version) | Recommended |
| Quick start / Installation | ✅ Yes |
| Usage examples | ✅ Yes |
| Configuration | If applicable |
| Contributing | Recommended |
| License | ✅ Yes |

---

## Docs-as-Code Tools

### Static Site Generators

| Tool | Best For | Config File |
|------|----------|-------------|
| **MkDocs** | Python projects, simple setup | mkdocs.yml |
| **Docusaurus** | React, versioning, i18n | docusaurus.config.js |
| **Sphinx** | Python autodocs | conf.py |
| **GitBook** | Beautiful docs, non-technical | book.json |
| **VitePress** | Vue projects, fast | .vitepress/config.js |

### API Documentation Tools

| Tool | Format | Output |
|------|--------|--------|
| **OpenAPI/Swagger** | YAML/JSON spec | Interactive docs |
| **Redoc** | OpenAPI | Static HTML |
| **Stoplight** | Design-first | Portal |
| **Postman** | Collections | Shareable docs |

---

## Writing Patterns

### The 4 Cs of Technical Writing

| Principle | Meaning |
|-----------|---------|
| **Clear** | No ambiguity, simple words |
| **Concise** | No filler, respect reader's time |
| **Correct** | Accurate, tested, up-to-date |
| **Complete** | All needed info present |

### Code Example Guidelines

| Do | Don't |
|----|-------|
| Show complete, runnable examples | Partial snippets without context |
| Include error handling | Happy path only |
| Use realistic data | `foo`, `bar`, `test123` |
| Explain non-obvious parts | Assume reader knows everything |

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Outdated screenshots | Automate with Puppeteer/Playwright |
| Broken links | CI link checking |
| Stale examples | Tests for code samples |
| Jargon overload | Glossary + define on first use |

---

## Synapses

### High-Strength Connections

- [project-scaffolding] (High, Extends, Bidirectional) — "Documentation project structure"
- [code-quality] (High, Complements, Bidirectional) — "Documented code is quality code"

### Medium-Strength Connections

- [creative-writing] (Medium, Complements, Forward) — "Clear writing techniques"
- [git-workflow] (Medium, Uses, Forward) — "Docs-as-code versioning"

### Supporting Connections

- [markdown-mastery] (Medium, Uses, Forward) — "Core formatting"
- [appropriate-reliance] (Low, Applies, Forward) — "AI assistance in docs"
