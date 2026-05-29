---
name: docs-codebase
description: Technical writing patterns for README files, API documentation, architecture decision records (ADRs), changelogs, contributing guides, code comments, and docs-as-code workflows. Covers documentation structure, style guides, Markdown best practices, and documentation testing.
---

# Technical Documentation — Quick Reference

This skill provides execution-ready patterns for writing clear, maintainable technical documentation. Claude should apply these patterns when users need README files, API docs, ADRs, changelogs, or any technical writing.

**Modern Best Practices (2025)**: Docs-as-code workflows, Markdown standardization, automated changelog generation, ADRs, interactive API docs (OpenAPI 3.2+), documentation testing, accessibility standards (WCAG 2.2), and docs in version control with CI/CD.

---

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Writing README files for projects
- Documenting APIs (REST, GraphQL, gRPC)
- Creating architecture decision records (ADRs)
- Writing changelogs and release notes
- Creating contributing guidelines
- Documenting code with comments and docstrings
- Setting up docs-as-code workflows
- Creating user guides and tutorials
- Writing technical specifications
- Building documentation sites (MkDocs, Docusaurus)

---

## Quick Reference

| Documentation Type | Template | Key Sections | When to Use |
|-------------------|----------|--------------|-------------|
| **Project README** | [readme-template.md](templates/project-management/readme-template.md) | Name, Features, Installation, Usage, Config | New project, open source, onboarding |
| **Architecture Decision** | [adr-template.md](templates/architecture/adr-template.md) | Status, Context, Decision, Consequences | Technical decisions, trade-offs |
| **API Reference** | [api-docs-template.md](templates/api-reference/api-docs-template.md) | Auth, Endpoints, Schemas, Errors, Rate Limits | REST/GraphQL APIs, webhooks |
| **Changelog** | [changelog-template.md](templates/project-management/changelog-template.md) | Added, Changed, Deprecated, Removed, Fixed, Security | Releases, version history |
| **Contributing Guide** | [contributing-template.md](templates/project-management/contributing-template.md) | Setup, Commit Guidelines, PR Process, Code Style | Open source, team projects |
| **Code Comments** | JSDoc, Python docstrings | Params, Returns, Raises, Examples | Public APIs, complex functions |
| **User Guide** | MkDocs/Docusaurus | Getting Started, Tutorials, Troubleshooting | End-user documentation |

---

## Decision Tree: Choosing Documentation Type

```text
User needs: [Documentation Task]
    ├─ New project or repository?
    │   └─ **README.md** (project overview, installation, quick start)
    │
    ├─ Made important technical decision?
    │   ├─ Architecture or design choice? → **ADR** (adr-template.md)
    │   └─ Technology choice? → **ADR** with alternatives section
    │
    ├─ Building or documenting API?
    │   ├─ REST API? → **OpenAPI 3.1** spec + api-docs-template
    │   ├─ GraphQL API? → Schema-first + GraphQL Docs
    │   └─ gRPC API? → Protobuf + generated docs
    │
    ├─ Releasing new version?
    │   ├─ Manual changelog? → **CHANGELOG.md** (Keep a Changelog format)
    │   └─ Automated? → semantic-release + Conventional Commits
    │
    ├─ Open source or team collaboration?
    │   ├─ Contribution workflow? → **CONTRIBUTING.md**
    │   ├─ Code of conduct? → CODE_OF_CONDUCT.md
    │   └─ License? → LICENSE file
    │
    ├─ Documenting code?
    │   ├─ Public API/library? → **Docstrings** (JSDoc, Python, etc.)
    │   ├─ Complex logic? → **Comments** (explain WHY, not WHAT)
    │   └─ Architecture? → **README** in module/package + diagrams
    │
    ├─ Building documentation site?
    │   ├─ Python project? → **MkDocs** + Material theme
    │   ├─ JavaScript/React? → **Docusaurus** (versioning support)
    │   └─ Next.js? → **Nextra** (minimal setup)
    │
    └─ Troubleshooting guide?
        └─ Common issues → Solutions → Diagnostic commands → Logs location
```

---

## Navigation: README Documentation

**README Best Practices** - [`resources/readme-best-practices.md`](resources/readme-best-practices.md)

Comprehensive guide for creating effective README files with:

- Essential 13-section structure (Name, Features, Prerequisites, Installation, Configuration, Usage, etc.)
- Copy-paste ready installation commands
- Configuration table templates
- Troubleshooting patterns
- Badge recommendations
- Anti-patterns to avoid
- README quality checklist

**When to use**: Creating new project README or improving existing documentation.

---

## Navigation: Architecture Documentation

**ADR Writing Guide** - [`resources/adr-writing-guide.md`](resources/adr-writing-guide.md)

Complete guide for documenting architectural decisions with:

- 8-section ADR structure (Title, Status, Context, Decision, Consequences, Alternatives, Implementation, References)
- Status lifecycle (Proposed → Accepted → Deprecated → Superseded)
- How to document trade-offs and alternatives
- ADR naming conventions and indexing
- When to write vs skip ADRs
- Real-world examples with metrics

**When to use**: Documenting technical decisions like database choice, framework selection, or architecture patterns.

**Template**: [templates/architecture/adr-template.md](templates/architecture/adr-template.md)

---

## Navigation: Changelog Documentation

**Changelog Best Practices** - [`resources/changelog-best-practices.md`](resources/changelog-best-practices.md)

Guide for maintaining changelogs using Keep a Changelog format with:

- 6 change categories (Added, Changed, Deprecated, Removed, Fixed, Security)
- Semantic versioning rules (MAJOR.MINOR.PATCH)
- Unreleased section management
- Conventional Commits integration
- Automated changelog generation (semantic-release, standard-version)
- Breaking change communication
- Linking to Git commits

**When to use**: Creating release notes, maintaining version history, documenting breaking changes.

**Template**: [templates/project-management/changelog-template.md](templates/project-management/changelog-template.md)

---

## Navigation: API Documentation

**API Documentation Standards** - [`resources/api-documentation-standards.md`](resources/api-documentation-standards.md)

Modern API documentation standards covering:

- REST API documentation (OpenAPI 3.1/3.2, authentication, endpoints, errors)
- GraphQL API documentation (schema, queries, mutations)
- gRPC API documentation (Protocol Buffers, service definitions)
- Essential elements (base URL, auth, rate limiting, pagination, webhooks)
- Error response format (RFC 7807)
- Interactive documentation tools (Swagger UI, Redoc, Stoplight)
- Code examples in multiple languages

**When to use**: Documenting REST, GraphQL, or gRPC APIs for developers.

**Template**: [templates/api-reference/api-docs-template.md](templates/api-reference/api-docs-template.md)

---

## Navigation: Code Comments & Docstrings

**Code Commenting Guide** - [`resources/code-commenting-guide.md`](resources/code-commenting-guide.md)

Comprehensive guide for effective code documentation with:

- Core principles (Comment WHY not WHAT, avoid obvious comments, keep updated)
- Docstring formats (JSDoc, Python Google Style, TSDoc, Godoc)
- Inline comment best practices
- When to use documentation vs implementation comments
- Comment anti-patterns (commented-out code, redundant comments, changelog comments)
- TODO/FIXME/HACK comment standards
- Accessibility comments (ARIA labels)

**When to use**: Documenting code for maintainability, writing public API documentation.

---

## Navigation: Contributing Guidelines

**Contributing Guide Standards** - [`resources/contributing-guide-standards.md`](resources/contributing-guide-standards.md)

Guide for creating CONTRIBUTING.md files with:

- 9-section structure (Welcome, Ways to Contribute, Setup, Workflow, Code Style, Review, Issues, Community, Recognition)
- Development setup instructions
- Conventional Commits format
- Pull request workflow
- Code style guidelines (JavaScript, Python, testing)
- Code review expectations
- Bug reporting and feature request templates
- Security vulnerability reporting

**When to use**: Setting up contribution process for open-source or team projects.

**Template**: [templates/project-management/contributing-template.md](templates/project-management/contributing-template.md)

---

## Navigation: Docs-as-Code Workflows

**Docs-as-Code Setup** - [`resources/docs-as-code-setup.md`](resources/docs-as-code-setup.md)

Setting up documentation with version control and CI/CD:

- MkDocs configuration and Material theme
- Docusaurus setup for versioned docs
- GitBook integration
- GitHub Actions for automated deployment
- Documentation site structure
- Search and navigation patterns

**When to use**: Building documentation sites with automated deployment.

---

## Navigation: Writing & Testing

**Technical Writing Best Practices** - [`resources/writing-best-practices.md`](resources/writing-best-practices.md)

Clear communication principles:

- Active voice and conciseness
- Plain language guidelines
- Audience awareness
- Structure and formatting
- Writing style consistency

**Markdown Style Guide** - [`resources/markdown-style-guide.md`](resources/markdown-style-guide.md)

Markdown formatting standards:

- Syntax reference (headers, lists, code blocks, tables)
- Style consistency rules
- Link formatting
- Code block language tags
- Table formatting

**Documentation Testing** - [`resources/documentation-testing.md`](resources/documentation-testing.md)

Automated documentation quality checks:

- Linting with markdownlint and Vale
- Link validation with markdown-link-check
- Spell checking with cspell
- Code example testing
- CI/CD integration

**When to use**: Establishing documentation standards, automating quality checks.

---

## Templates

Complete copy-paste ready templates organized by domain:

### Architecture Documentation

- **ADR Template**: [templates/architecture/adr-template.md](templates/architecture/adr-template.md) - Architecture Decision Records for technical decisions

### API Reference

- **API Docs Template**: [templates/api-reference/api-docs-template.md](templates/api-reference/api-docs-template.md) - REST/GraphQL API documentation with authentication, endpoints, webhooks

### Project Management

- **README Template**: [templates/project-management/readme-template.md](templates/project-management/readme-template.md) - Project overview, installation, usage
- **Changelog Template**: [templates/project-management/changelog-template.md](templates/project-management/changelog-template.md) - Keep a Changelog format with semantic versioning
- **Contributing Guide**: [templates/project-management/contributing-template.md](templates/project-management/contributing-template.md) - Contribution workflow, code standards, commit guidelines

### Docs-as-Code

- **Docs Structure Template**: [templates/docs-as-code/docs-structure-template.md](templates/docs-as-code/docs-structure-template.md) - IA, folder structure, freshness metadata
- **Docs Ownership Model**: [templates/docs-as-code/ownership-model.md](templates/docs-as-code/ownership-model.md) - Owners, review cadence, enforcement

---

## Do / Avoid (Dec 2025)

### Do

- Assign owners and review cadences to docs that matter (runbooks, onboarding, APIs).
- Add CI checks for links, style, and stale docs where feasible.
- Prefer small, task-oriented docs over “big wiki pages”.

### Avoid

- Docs without owners (guaranteed to rot).
- Stale runbooks (dangerous during incidents).
- Copy/paste docs that drift from code and config.

## What Good Looks Like

- Ownership: every critical doc has an owner and review cadence (runbooks, onboarding, APIs).
- Structure: consistent information architecture (tutorial/how-to/reference/explanation) and clear navigation.
- Quality gates: CI runs link checks and linting; stale docs are flagged.
- Decision capture: ADRs exist for major choices and are referenced from code and runbooks.
- Onboarding: a new engineer can get to a first PR within a defined target time (tracked and improved).

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Draft and summarize docs changes; humans review before publishing.
- Generate doc diffs in PRs; do not auto-merge.

## External Resources

See [data/sources.json](data/sources.json) for:

- **Style Guides**: Google Developer Docs, Microsoft Writing Guide, Write the Docs
- **Documentation Tools**: MkDocs, Docusaurus, GitBook, Nextra, Mintlify
- **API Documentation**: OpenAPI, Swagger UI, Redoc, GraphQL Docs
- **Testing Tools**: Vale (prose linting), markdownlint, cspell (spell check), markdown-link-check
- **Patterns**: Keep a Changelog, Semantic Versioning, ADRs, Conventional Commits
- **Learning**: Google Technical Writing Courses, Docs for Developers (book)

---

## Related Skills

- **Documentation Audit**: [../qa-docs-coverage/SKILL.md](../qa-docs-coverage/SKILL.md) - Audit codebases for documentation gaps, generate coverage reports, identify what needs documenting
- **API Design**: [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) - REST API patterns, endpoint design, versioning strategies
- **Code Review**: [../software-code-review/SKILL.md](../software-code-review/SKILL.md) - Code review checklists including documentation standards
- **Testing**: [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) - Test documentation patterns, test plan templates
- **Git Workflow**: [../git-workflow/SKILL.md](../git-workflow/SKILL.md) - Commit message standards (Conventional Commits), changelog automation
- **PRD Development**: [../docs-ai-prd/SKILL.md](../docs-ai-prd/SKILL.md) - PRD templates, tech specs, story mapping for new features

---

## Navigation: Production Gotchas Documentation

**Purpose**: Document platform-specific issues, silent failures, and hard-to-debug problems to prevent repeated mistakes.

**When to Use**: After discovering a production issue that:
- Took significant time to debug
- Was caused by external service configuration (not your code)
- Could affect other developers on the team
- Has a non-obvious solution

### Gotcha Documentation Structure

```markdown
## Production Gotchas

### [Provider/Feature Name]

- **The Trap**: What looks correct but actually fails
- **Symptom**: How the issue manifests (error messages, behavior)
- **Root Cause**: Why it happens (the underlying reason)
- **Fix**: Step-by-step solution
- **Prevention**: How to avoid this in the future
```

### Example Gotchas (Real-World)

```markdown
## Production Gotchas

### Vercel Cron Jobs Require Pro Plan

- **The Trap**: Cron configuration in vercel.json looks valid, jobs never run
- **Symptom**: Scheduled tasks (notifications, data cleanup) never execute; no errors in logs
- **Root Cause**: Vercel Free tier doesn't support cron jobs; requires Pro plan ($20/month)
- **Fix**: Upgrade to Vercel Pro, verify cron jobs in Vercel dashboard under "Cron Jobs" tab
- **Prevention**: Check Vercel plan requirements before implementing scheduled features

### Supabase Site URL Misconfiguration

- **The Trap**: OAuth redirects users to localhost instead of production domain
- **Symptom**: Users click "Sign in with Google" → redirected to localhost:3000 → broken auth
- **Root Cause**: Site URL in Supabase Dashboard → Authentication → URL Configuration still set to localhost
- **Fix**: Set Site URL to `https://your-production-domain.com` (no trailing slash)
- **Prevention**: Add Site URL configuration to deployment checklist

### Apple OAuth Secret Expiration

- **The Trap**: Apple Sign-In stops working after 6 months with no warning
- **Symptom**: "Invalid client secret" error on Apple OAuth flow
- **Root Cause**: Apple's client secret JWT expires in 180 days (not documented clearly)
- **Fix**: Regenerate client secret using .p8 key: `npm run generate-apple-secret`
- **Prevention**: Set calendar reminder 7 days before expiration; consider automation

### Next.js API Route JSON Parsing

- **The Trap**: API returns 500 error when client sends malformed JSON
- **Symptom**: `SyntaxError: Unexpected token` in server logs; client sees generic 500
- **Root Cause**: `await request.json()` throws if body isn't valid JSON
- **Fix**: Wrap in try-catch, return 400 with helpful message
- **Prevention**: Create reusable `parseRequestBody` utility (see software-backend skill)
```

### Where to Document Gotchas

| Project Type | Location | Format |
|-------------|----------|--------|
| Claude Code projects | `CLAUDE.md` | Markdown section |
| Standard projects | `docs/gotchas.md` or `TROUBLESHOOTING.md` | Dedicated file |
| Wiki/Notion | Dedicated page | Searchable knowledge base |
| README | Bottom section | Brief summaries with links |

### Gotcha Documentation Checklist

```
[ ] Gotcha has clear, searchable title
[ ] Symptom describes what user sees (error messages, behavior)
[ ] Root cause explains WHY (not just WHAT)
[ ] Fix has step-by-step instructions
[ ] Prevention explains how to avoid in future
[ ] Added to project documentation
[ ] Shared with team (Slack, standup, PR comment)
```

### Anti-Patterns

- **Too vague**: "Sometimes auth breaks" → Add specific error messages and conditions
- **Missing root cause**: "Set Site URL to production" → Explain WHY this matters
- **No prevention**: Fix alone isn't enough → How to avoid this next time?
- **Buried in code comments**: Gotchas should be discoverable, not hidden in code

---

## Usage Notes

**For Claude**: When a user requests documentation:

1. **Identify documentation type** using the Decision Tree
2. **Reference appropriate template** from templates/ directory
3. **Follow best practices** from relevant resource file
4. **Provide copy-paste ready content** with user's specific context
5. **Include examples** from templates or resources
6. **Mention related skills** if user might need complementary guidance

**Common workflows**:

- **New project**: README template → Contributing guide → Changelog
- **API development**: API docs template → OpenAPI spec → Interactive docs
- **Technical decision**: ADR template → Document alternatives → Reference in README
- **Open source setup**: README → CONTRIBUTING.md → CODE_OF_CONDUCT.md → LICENSE

**Quality checks**:

- Verify all links work (use markdown-link-check)
- Run spell checker (cspell)
- Lint Markdown (markdownlint)
- Test code examples actually run
- Check accessibility (WCAG 2.2 for web docs)

---

> **Success Criteria:** Documentation is clear, accurate, up-to-date, discoverable, and enables users to be productive quickly with minimal support.
