---
name: documentation
description: Maintain documentation for IntelliFill following Diátaxis framework. Use when creating or updating docs, API references, or guides.
---

# Documentation Maintenance Skill

This skill provides comprehensive guidance for maintaining IntelliFill documentation following the Diátaxis framework.

## Table of Contents

1. [Documentation Architecture](#documentation-architecture)
2. [Diátaxis Framework](#diataxis-framework)
3. [Frontmatter Standards](#frontmatter-standards)
4. [Writing Guidelines](#writing-guidelines)
5. [Update Triggers](#update-triggers)
6. [Code Examples](#code-examples)
7. [Cross-Referencing](#cross-referencing)
8. [ADR Pattern](#adr-pattern)

## Documentation Architecture

IntelliFill uses a structured, multi-location documentation system.

### Documentation Locations

```
IntelliFill/
├── docs/                          # Root-level Diátaxis docs
│   ├── README.md                  # Documentation hub
│   ├── MAINTENANCE.md             # This guide
│   ├── tutorials/                 # Learning-oriented
│   ├── how-to/                    # Problem-oriented
│   ├── reference/                 # Information-oriented
│   │   ├── api/
│   │   │   ├── endpoints.md
│   │   │   └── schemas.md
│   │   ├── configuration/
│   │   │   └── environment.md
│   │   └── database/
│   │       └── schema.md
│   └── explanation/               # Understanding-oriented
│       └── architecture.md
├── quikadmin/
│   ├── docs/                      # Backend-specific docs
│   └── CLAUDE.md                  # Backend AI context
├── quikadmin-web/
│   ├── docs/                      # Frontend-specific docs
│   └── CLAUDE.md                  # Frontend AI context
├── CLAUDE.local.md                # Local dev context
└── AGENTS.md                      # Task Master integration
```

### Documentation Hierarchy

```
1. CLAUDE.local.md        → Local dev overrides (not in git)
2. [subproject]/CLAUDE.md → Subproject-specific context
3. docs/                  → Unified Diátaxis documentation
4. README.md              → Project overview
5. AGENTS.md              → Agent integration guide
```

## Diátaxis Framework

IntelliFill documentation follows the Diátaxis framework with four quadrants.

### Four Quadrants

```
                Learning          Practical
              ┌─────────────┬─────────────┐
              │             │             │
    Practical │  Tutorials  │  How-To     │
              │             │             │
              ├─────────────┼─────────────┤
              │             │             │
 Theoretical  │ Explanation │  Reference  │
              │             │             │
              └─────────────┴─────────────┘
```

### 1. Tutorials (Learning-Oriented)

**Purpose**: Help newcomers learn by doing

**Characteristics**:
- Step-by-step instructions
- Beginner-friendly
- Repeatable and reliable
- Complete examples
- Focus on learning, not production

**Example Structure**:

```markdown
---
title: Building Your First PDF Form
description: Learn IntelliFill basics by creating and filling a simple form
category: tutorials
difficulty: beginner
duration: 30 minutes
---

# Building Your First PDF Form

In this tutorial, you'll learn the basics of IntelliFill by creating a simple
PDF form and automatically filling it with data.

## What You'll Learn

- Uploading documents
- Creating templates
- Mapping form fields
- Generating filled PDFs

## Prerequisites

- IntelliFill account
- Sample PDF form (provided)
- 30 minutes

## Step 1: Upload Your First Document

First, let's upload a sample invoice...

[Detailed step-by-step instructions]

## What You've Learned

Congratulations! You've successfully...

## Next Steps

- [Tutorial: Advanced Field Mapping](./advanced-mapping.md)
- [How-To: Batch Process Documents](../how-to/batch-processing.md)
```

### 2. How-To Guides (Problem-Oriented)

**Purpose**: Solve specific problems

**Characteristics**:
- Goal-oriented
- Assume knowledge
- Show one way to do something
- Practical and actionable
- Production-focused

**Example Structure**:

```markdown
---
title: How to Implement Rate Limiting
description: Add rate limiting to API endpoints
category: how-to
tags: [api, security, backend]
---

# How to Implement Rate Limiting

This guide shows you how to add rate limiting to protect your API endpoints.

## Problem

You need to prevent API abuse by limiting request rates per user.

## Solution

Use the built-in rate limiter middleware.

## Prerequisites

- Backend development environment
- Basic Express.js knowledge

## Steps

### 1. Import the Rate Limiter

```typescript
import { rateLimiter } from '@/middleware/rateLimiter';
```

### 2. Apply to Routes

[Detailed implementation steps]

## Verification

Test your rate limiting...

## Troubleshooting

If rate limiting isn't working...

## See Also

- [Reference: Rate Limiter API](../reference/api/rate-limiter.md)
- [Explanation: Rate Limiting Strategy](../explanation/rate-limiting.md)
```

### 3. Reference (Information-Oriented)

**Purpose**: Describe the system accurately

**Characteristics**:
- Dry and factual
- Consistent structure
- Complete and accurate
- Searchable
- No opinions or explanations

**Example Structure**:

```markdown
---
title: Document API Reference
description: Complete API reference for document endpoints
category: reference
tags: [api, documents]
---

# Document API Reference

Complete reference for all document-related API endpoints.

## Endpoints

### List Documents

```http
GET /api/documents
```

**Description**: Retrieve a paginated list of documents.

**Authentication**: Required

**Query Parameters**:

| Parameter | Type   | Required | Default | Description           |
|-----------|--------|----------|---------|----------------------|
| page      | number | No       | 1       | Page number          |
| limit     | number | No       | 20      | Items per page       |
| search    | string | No       | -       | Search query         |
| status    | string | No       | -       | Filter by status     |

**Response**:

```typescript
{
  success: boolean;
  data: {
    items: Document[];
    total: number;
    page: number;
    totalPages: number;
  };
}
```

**Example Request**:

```bash
curl -X GET "http://localhost:3002/api/documents?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response**:

```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 42,
    "page": 1,
    "totalPages": 3
  }
}
```

[Continue for all endpoints...]
```

### 4. Explanation (Understanding-Oriented)

**Purpose**: Deepen understanding

**Characteristics**:
- Discusses alternatives
- Provides context
- Explains design decisions
- Higher-level concepts
- No instructions

**Example Structure**:

```markdown
---
title: Authentication Architecture
description: Understanding IntelliFill's authentication system
category: explanation
tags: [architecture, security, auth]
---

# Authentication Architecture

This document explains the design decisions and architecture of IntelliFill's
authentication system.

## Overview

IntelliFill uses Supabase Auth for authentication, supplemented by backend
JWT validation and session management.

## Why Supabase Auth?

We chose Supabase Auth over custom JWT implementation for several reasons:

1. **Security**: Industry-standard OAuth2 flows
2. **Features**: Built-in email verification, password reset
3. **Scalability**: Handles user management at scale
4. **Developer Experience**: Simple API, good docs

## Authentication Flow

[Detailed explanation of the flow]

## Design Trade-offs

### Backend vs. Frontend Auth

We support two authentication modes...

**Backend Auth Mode**:
- Pros: No Supabase dependency in frontend
- Cons: Extra API calls

**Direct Supabase Mode**:
- Pros: Faster authentication
- Cons: Requires Supabase SDK

## Alternative Approaches Considered

We considered these alternatives:

1. **Custom JWT**: More control, but more maintenance
2. **Auth0**: Feature-rich, but expensive
3. **Passport.js**: Flexible, but requires setup

## Security Considerations

[Security implications and best practices]

## See Also

- [Tutorial: Setting Up Authentication](../tutorials/auth-setup.md)
- [Reference: Auth API](../reference/api/auth.md)
```

## Frontmatter Standards

All documentation files must include frontmatter.

### Frontmatter Template

```markdown
---
title: Short, Descriptive Title
description: One-line summary of the document
category: tutorials | how-to | reference | explanation
tags: [tag1, tag2, tag3]
difficulty: beginner | intermediate | advanced  # (tutorials only)
duration: 15 minutes | 1 hour                  # (tutorials only)
lastUpdated: 2024-01-15                        # (optional)
---
```

### Frontmatter Examples

**Tutorial**:
```yaml
---
title: Getting Started with IntelliFill
description: Learn the basics in 30 minutes
category: tutorials
difficulty: beginner
duration: 30 minutes
tags: [getting-started, basics]
---
```

**How-To**:
```yaml
---
title: How to Add Custom Validation
description: Implement custom validation for form fields
category: how-to
tags: [validation, backend, forms]
---
```

**Reference**:
```yaml
---
title: Environment Variables Reference
description: Complete list of environment variables
category: reference
tags: [configuration, environment]
---
```

**Explanation**:
```yaml
---
title: Document Processing Pipeline
description: Understanding how documents flow through the system
category: explanation
tags: [architecture, processing, ocr]
---
```

## Writing Guidelines

### Voice and Tone

- **Active voice**: "Click the button" not "The button should be clicked"
- **Present tense**: "The system validates" not "The system will validate"
- **Direct address**: "You can configure" not "One can configure"
- **Concise**: Remove unnecessary words
- **Clear**: Use simple language

### Formatting Standards

**Headings**:
```markdown
# H1: Document Title (only one per page)
## H2: Major Sections
### H3: Subsections
#### H4: Minor Subsections (avoid if possible)
```

**Lists**:
```markdown
- Unordered lists for items without sequence
1. Ordered lists for steps or sequences
- Use sentence case
- End with periods if complete sentences
- No periods for fragments
```

**Code**:
```markdown
`inline code` for variables, commands, filenames

```language
code blocks for examples
```

Supported languages: typescript, javascript, bash, json, yaml, prisma, sql
```

**Emphasis**:
```markdown
**Bold** for UI elements, important terms
*Italic* for emphasis (use sparingly)
`code` for technical terms
```

### File Naming

- Use kebab-case: `api-endpoints.md`, `getting-started.md`
- Be descriptive: `authentication-flow.md` not `auth.md`
- Avoid dates in names unless part of ADR

## Update Triggers

Documentation MUST be updated when:

### API Changes

**Trigger**: Adding, modifying, or removing API endpoints

**Update**:
- `docs/reference/api/endpoints.md`
- Relevant how-to guides
- CLAUDE.local.md if affects local dev

**Example**:
```markdown
# docs/reference/api/endpoints.md

### Upload Document

```http
POST /api/documents/upload
```

**Added**: v1.2.0 (2024-01-15)
**Updated**: v1.3.0 (2024-02-01) - Added multipart support

[Documentation...]
```

### Environment Variables

**Trigger**: Adding or changing environment variables

**Update**:
- `docs/reference/configuration/environment.md`
- `.env.example`
- CLAUDE.local.md (Environment Variables section)

### Database Schema

**Trigger**: Prisma migrations

**Update**:
- `docs/reference/database/schema.md`
- CLAUDE.local.md if affects common queries

### Known Issues

**Trigger**: Fixing or discovering bugs

**Update**:
- CLAUDE.local.md (Known Issues section)
- Mark as ✅ FIXED when resolved

### New Features

**Trigger**: Implementing new features

**Update**:
- Tutorial (if beginner-focused)
- How-to guide (if problem-solving)
- Reference docs (for API/config)
- Explanation (for architecture)

## Code Examples

### Code Example Standards

**Always include**:
1. Language identifier in code fence
2. Complete, runnable examples
3. Comments for clarity
4. Error handling
5. Type annotations (TypeScript)

**Good Example**:
```typescript
// quikadmin/src/services/document.service.ts
import { PrismaClient } from '@prisma/client';
import { AppError } from '@/utils/errors';

export class DocumentService {
  private prisma: PrismaClient;

  constructor(deps: { prisma: PrismaClient }) {
    this.prisma = deps.prisma;
  }

  /**
   * Retrieve a document by ID with ownership check
   */
  async getById(id: string, userId: string) {
    const document = await this.prisma.document.findFirst({
      where: { id, userId },
    });

    if (!document) {
      throw new AppError('Document not found', 404);
    }

    return document;
  }
}
```

**Bad Example**:
```typescript
// Don't do this - incomplete, no context, no types
async getById(id, userId) {
  return prisma.document.findFirst({ where: { id, userId } });
}
```

### Code Block Headers

Include file paths for context:

```typescript
// quikadmin/src/api/documents.routes.ts
import { Router } from 'express';

const router = Router();
// ...
```

### Placeholder Values

Use descriptive placeholders:

```bash
# Good
curl -X POST http://localhost:3002/api/documents \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -d '{"name": "Invoice.pdf"}'

# Bad
curl -X POST http://localhost:3002/api/documents \
  -H "Authorization: Bearer xxx" \
  -d '{"name": "abc"}'
```

## Cross-Referencing

### Internal Links

```markdown
- [Tutorial: Getting Started](../tutorials/getting-started.md)
- [Reference: API Endpoints](./api/endpoints.md)
- [How-To: Rate Limiting](../how-to/rate-limiting.md)
```

### Link Text Standards

```markdown
# Good
See [How to Add Validation](../how-to/validation.md) for details.

# Bad
See [here](../how-to/validation.md) for details.
Click [this link](../how-to/validation.md).
```

### See Also Sections

End documents with related links:

```markdown
## See Also

- [Tutorial: Setting Up IntelliFill](../tutorials/setup.md) - Get started
- [Reference: Configuration](../reference/configuration/environment.md) - All config options
- [Explanation: Architecture](../explanation/architecture.md) - System design
```

## ADR Pattern

Architecture Decision Records document significant decisions.

### ADR Location

```
docs/decisions/
├── 0001-use-supabase-auth.md
├── 0002-monorepo-with-docker.md
├── 0003-tailwindcss-4-migration.md
└── template.md
```

### ADR Template

```markdown
---
title: ADR-0001: Use Supabase for Authentication
description: Decision to use Supabase Auth over custom JWT
category: explanation
tags: [adr, architecture, auth]
status: accepted | rejected | superseded | deprecated
date: 2024-01-15
---

# ADR-0001: Use Supabase for Authentication

## Status

Accepted (2024-01-15)

## Context

We need a secure, scalable authentication system for IntelliFill. Key requirements:

- Email/password authentication
- OAuth providers (Google, GitHub)
- Email verification
- Password reset
- Session management
- Minimal maintenance overhead

## Decision

We will use Supabase Auth for user authentication.

## Consequences

### Positive

- Industry-standard security practices
- Built-in features (verification, reset, OAuth)
- Scales automatically
- Well-documented
- Active community

### Negative

- External dependency
- Vendor lock-in risk
- Requires Supabase account
- Additional cost at scale

### Neutral

- Team needs to learn Supabase Auth
- Migration path exists if needed

## Alternatives Considered

### 1. Custom JWT Implementation

**Pros**: Full control, no dependencies
**Cons**: Security burden, ongoing maintenance

### 2. Auth0

**Pros**: Feature-rich, enterprise-ready
**Cons**: Expensive, complex setup

### 3. Passport.js

**Pros**: Flexible, many strategies
**Cons**: DIY security, more setup

## References

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [OAuth2 Specification](https://oauth.net/2/)
```

## Best Practices

1. **Update documentation WITH code changes** - Not after
2. **Use examples from actual code** - Keep them in sync
3. **Test all code examples** - Ensure they work
4. **Link related documents** - Help readers navigate
5. **Use consistent terminology** - Don't vary terms
6. **Keep it current** - Remove outdated information
7. **Use version markers** - Note when things changed
8. **Include prerequisites** - Don't assume knowledge
9. **Provide context** - Explain why, not just how
10. **Review regularly** - Audit docs quarterly

## Maintenance Checklist

When making changes:

- [ ] Updated relevant Diátaxis documents
- [ ] Updated CLAUDE.local.md if affects local dev
- [ ] Updated .env.example if new env vars
- [ ] Added/updated code examples
- [ ] Tested all code examples
- [ ] Cross-referenced related docs
- [ ] Updated lastUpdated date
- [ ] Reviewed for clarity and completeness

## References

- [Diátaxis Framework](https://diataxis.fr/)
- [Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/)
- [Write the Docs](https://www.writethedocs.org/)
