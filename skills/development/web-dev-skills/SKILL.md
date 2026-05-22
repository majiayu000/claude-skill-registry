---
name: web-dev-skills
description: Use when working on web development tasks involving NextJS, React, TypeScript, Tailwind CSS, testing, deployment, APIs, databases, authentication, cloud infrastructure, or any modern web development stack. Provides access to 22 specialized web development skills covering frontend, backend, DevOps, and best practices.
---

# Web Development Skills Collection

Access to 22 specialized web development skills covering the complete modern web stack. This skill helps you quickly find and load the right specialized knowledge for your task.

## When to Use This Skill

Use this when working with:
- Frontend development (NextJS, React, Tailwind)
- Backend & APIs (Server Actions, REST APIs)
- Database & ORM (Prisma, Neon, migrations)
- Authentication (NextAuth)
- Testing (Vitest, Playwright, E2E)
- Cloud Infrastructure (AWS, GCP, Vercel)
- DevOps (deployment, monitoring, logging)
- Code quality (TypeScript standards, code review, security)
- Performance & SEO optimization
- Accessibility & UX

## Available Skills

All skills are located at: `~/claude-prompt-engineering-guide/skills/examples/`

### 🎨 Frontend Development

**NextJS App Router** (`nextjs-app-router-skill.md`)
- Server Components vs Client Components
- App Router patterns and file-based routing
- Server Actions for mutations
- Data fetching and streaming
- Performance optimization

**Tailwind Design System** (`tailwind-design-system-skill.md`)
- Utility-first CSS patterns
- Custom design tokens and configuration
- shadcn/ui integration
- Responsive design (mobile-first)
- Dark mode support

**TypeScript Standards** (`typescript-standards.md`)
- Type safety best practices
- Interface vs Type usage
- Generics and utility types
- Strict mode configuration

**Accessibility & UX** (`accessibility-ux.md`)
- WCAG compliance
- Semantic HTML
- ARIA attributes
- Keyboard navigation
- Screen reader optimization

### 🔐 Authentication & Security

**NextAuth Authentication** (`nextauth-authentication-skill.md`)
- NextAuth.js v5 setup
- OAuth providers
- Session management
- Protected routes

**Security & Compliance** (`security-compliance.md`)
- Security best practices
- OWASP top 10 prevention
- Data protection
- Compliance requirements

### 🗄️ Database & Backend

**Prisma ORM** (`prisma-orm-skill.md`)
- Schema design
- Migrations
- Query optimization
- Relations and transactions

**Database Migrations** (`database-migrations.md`)
- Migration strategies
- Schema versioning
- Data migration patterns

**Neon Serverless** (`neon-serverless-skill.md`)
- Serverless PostgreSQL
- Connection pooling
- Branching and environments

**API Development** (`api-development-skill.md`)
- REST API design
- Route handlers
- Error handling
- API documentation

### 🧪 Testing

**Vitest Unit Testing** (`vitest-unit-testing-skill.md`)
- Unit test patterns
- Test organization
- Mocking strategies
- Coverage optimization

**Playwright E2E Testing** (`playwright-e2e-testing-skill.md`)
- End-to-end test patterns
- Page object model
- Test fixtures
- CI/CD integration

**Testing Skill** (`testing-skill.md`)
- General testing best practices
- Test pyramid
- Testing strategies

**Code Review** (`code-review.md`)
- Code review checklist
- Best practices
- Common issues to catch

### ☁️ Cloud & Infrastructure

**AWS Cloud Infrastructure** (`aws-cloud-infrastructure-skill.md`)
- AWS service selection
- Infrastructure as Code
- Security best practices
- Cost optimization

**Google Cloud Platform** (`google-cloud-platform-skill.md`)
- GCP service selection
- Cloud Run and App Engine
- Firestore and Cloud SQL

**Vercel Deployment** (`vercel-deployment-skill.md`)
- Deployment configuration
- Environment variables
- Preview deployments
- Edge functions

### 📊 DevOps & Monitoring

**Monitoring & Logging** (`monitoring-logging-skill.md`)
- Application monitoring
- Error tracking
- Performance monitoring
- Log aggregation

**Git Workflow** (`git-workflow-skill.md`)
- Branching strategies
- Commit conventions
- PR best practices
- Git commands reference

### ⚡ Optimization

**Performance Optimization** (`performance-optimization-skill.md`)
- Core Web Vitals
- Bundle optimization
- Image optimization
- Caching strategies

**SEO Optimization** (`seo-optimization-skill.md`)
- Meta tags and structured data
- OpenGraph and Twitter cards
- Sitemap and robots.txt
- Performance and SEO

### 📋 Other

**Feedback Analyzer** (`example-feedback-analyzer.md`)
- Customer feedback analysis
- Sentiment analysis
- Pattern identification

## How to Use These Skills

When I detect you're working on a web development task, I'll automatically reference the relevant skill(s) from this collection.

### Manual Usage

You can also explicitly request a specific skill:

```
"Using the NextJS App Router skill, help me build a dashboard page"
"Reference the Tailwind Design System skill to style this component"
"Apply the Vitest Unit Testing skill to write tests for this function"
```

### Loading Multiple Skills

For complex tasks, I can reference multiple skills:

```
"Using the NextJS, Prisma, and NextAuth skills, help me build a user profile page"
```

## Skill Loading Strategy

I will:
1. **Detect** what technology/task you're working on
2. **Identify** which skill(s) are relevant
3. **Read** the specific skill file(s) from `~/claude-prompt-engineering-guide/skills/examples/`
4. **Apply** the patterns and best practices from those skills
5. **Load on-demand** - Only read skills when needed to avoid context bloat

## Quick Reference by Task Type

**Building a new feature:**
→ NextJS + Tailwind + Prisma + Testing

**Adding authentication:**
→ NextAuth + Security + TypeScript

**Deploying an app:**
→ Vercel + Monitoring + Performance

**Writing tests:**
→ Vitest + Playwright + Testing

**API development:**
→ API Development + Prisma + TypeScript

**Styling components:**
→ Tailwind + Accessibility + TypeScript

**Infrastructure setup:**
→ AWS/GCP + Monitoring + Security

**Code quality:**
→ Code Review + TypeScript + Testing

## Best Practices

1. **Start with architecture** - Consider NextJS patterns first
2. **Type safety** - Apply TypeScript standards throughout
3. **Test as you build** - Reference testing skills early
4. **Accessibility first** - Check accessibility guidelines
5. **Security by default** - Apply security best practices
6. **Performance matters** - Optimize as you develop
7. **Review before deploy** - Use code review checklist

## Pro Tips

- These skills work **together** - combine them for complex tasks
- Skills contain **real code examples** - patterns you can copy
- Skills enforce **best practices** - follow their guidelines
- Skills are **framework-specific** - optimized for modern stack
- Skills include **decision trees** - when to use what approach

## Source

All skills sourced from: https://github.com/ThamJiaHe/claude-prompt-engineering-guide

Full skill files available at: `~/claude-prompt-engineering-guide/skills/examples/`
