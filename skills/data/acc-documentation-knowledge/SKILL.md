---
name: acc-documentation-knowledge
description: Documentation knowledge base. Provides documentation types, audiences, best practices, and antipatterns for technical documentation creation.
---

# Documentation Knowledge Base

Quick reference for technical documentation types, audiences, and best practices.

## Documentation Types

### By Purpose

| Type | Audience | Goal | Examples |
|------|----------|------|----------|
| **README** | New users | Quick start | badges, install, basic usage |
| **Architecture** | Developers | System understanding | layers, components, decisions |
| **API** | Integrators | Integration | endpoints, params, responses |
| **ADR** | Team | Decision history | context, decision, consequences |
| **Getting Started** | Beginners | First success | step-by-step tutorial |
| **Reference** | All | Quick lookup | methods, options, configs |
| **Troubleshooting** | Users | Problem solving | FAQ, error messages, solutions |
| **CHANGELOG** | All | Version history | features, fixes, breaking |

### Documentation Pyramid

```
        /\
       /  \
      / ADR \          ← Why (decisions)
     /________\
    /   Arch    \      ← How (structure)
   /______________\
  /    API Ref     \   ← What (details)
 /____________________\
/        README        \← Quick start
```

## Audience Analysis

### Developer Personas

| Persona | Needs | Tone |
|---------|-------|------|
| **Evaluator** | Quick value assessment | Benefits, features |
| **Beginner** | Step-by-step guidance | Simple, encouraging |
| **Intermediate** | Best practices, patterns | Technical, practical |
| **Expert** | Advanced configs, internals | Concise, complete |
| **Contributor** | Setup, conventions | Technical, detailed |

### Content Mapping

```
Evaluator → README (badges, features, comparison)
Beginner → Getting Started, Examples
Intermediate → API Reference, Guides
Expert → Architecture, Internals
Contributor → CONTRIBUTING, ADRs
```

## Structure Principles

### README Structure (Recommended)

```markdown
# Project Name

Brief description (1-2 sentences)

## Badges
[Build][Coverage][Version][License]

## Features
- Feature 1
- Feature 2

## Installation
```bash
composer require ...
```

## Quick Start
```php
// minimal working example
```

## Documentation
Links to detailed docs

## Contributing
Link to CONTRIBUTING.md

## License
MIT / Apache / etc.
```

### Architecture Doc Structure

```markdown
# Architecture

## Overview
High-level description

## System Context
C4 Context diagram

## Components
C4 Component diagram

## Data Flow
Sequence diagrams

## Technology Stack
| Layer | Technology |
|-------|------------|

## Decisions
Link to ADRs

## Deployment
Infrastructure diagram
```

## Best Practices

### Writing Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Scannable** | Headers, bullets, tables | Use `##` for sections |
| **Task-oriented** | Focus on goals, not features | "How to X" not "X feature" |
| **Example-driven** | Code before explanation | ```php example``` then text |
| **Layered** | Quick start → details | README → Guide → Reference |
| **Up-to-date** | Doc near code | Update together |

### Code Examples Principles

```markdown
✅ Good:
- Minimal complete example
- Copy-paste ready
- Shows expected output
- Uses realistic data

❌ Bad:
- Snippets that don't run
- Foo/Bar/Baz naming
- Missing imports
- Outdated syntax
```

### Example Quality Checklist

```php
// ✅ Good example
use App\Service\PaymentService;

$payment = new PaymentService($gateway);
$result = $payment->charge(
    amount: 99.99,
    currency: 'USD',
    customerId: 'cus_123'
);

echo $result->transactionId; // "txn_abc123"
```

```php
// ❌ Bad example
$foo = new Foo();
$bar = $foo->doSomething($baz);
// returns something
```

## Common Antipatterns

### Documentation Smell Checklist

| Smell | Detection | Fix |
|-------|-----------|-----|
| **Stale** | Code changed, docs not | Review on PR |
| **Wall of text** | No headers, no examples | Structure + code |
| **Jargon soup** | Undefined terms | Glossary, links |
| **Dead links** | 404 errors | Link checker CI |
| **No examples** | Pure prose | Add code blocks |
| **Copy-paste broken** | Missing imports | Run examples |
| **Version mismatch** | Wrong versions | Automate sync |

### README Antipatterns

```markdown
❌ No installation instructions
❌ No usage examples
❌ Badges only (no content)
❌ Generated API docs only
❌ Outdated screenshots
❌ Broken links
❌ No clear project description
```

### Architecture Doc Antipatterns

```markdown
❌ Box-and-arrow without explanation
❌ Outdated diagrams
❌ Missing "why" context
❌ No technology justification
❌ Inconsistent terminology
❌ Too much detail (implementation in arch doc)
```

## Documentation as Code

### Principles

1. **Version control** — docs in git with code
2. **Review** — PRs include doc updates
3. **Test** — validate links, examples
4. **Automate** — generate where possible
5. **CI/CD** — build and deploy docs

### File Organization

```
project/
├── README.md           # Quick start
├── docs/
│   ├── architecture/
│   │   ├── README.md
│   │   ├── diagrams/
│   │   └── decisions/ (ADRs)
│   ├── api/
│   │   └── README.md
│   ├── guides/
│   │   ├── getting-started.md
│   │   └── deployment.md
│   └── reference/
│       └── configuration.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## Markdown Best Practices

### Formatting Guidelines

| Element | Usage |
|---------|-------|
| `#` H1 | Document title only |
| `##` H2 | Main sections |
| `###` H3 | Subsections |
| `-` | Unordered lists |
| `1.` | Ordered steps |
| `>` | Warnings, notes |
| `\`\`\`` | Code blocks |
| `\|` | Data tables |

### Code Block Languages

```markdown
```php      # PHP code
```bash     # Shell commands
```yaml     # Configuration
```json     # API responses
```mermaid  # Diagrams
```sql      # Database
```

## References

For detailed information, load these reference files:

- `references/readme-patterns.md` — README structure and examples
- `references/api-documentation.md` — API documentation guidelines
- `references/architecture-docs.md` — Architecture documentation patterns
- `references/adr-format.md` — ADR structure and examples
- `references/diagramming.md` — Diagram types and tools
