---
name: repo-docs
description: This skill should be used when the user asks to "generate repository documentation", "create a README", "document API", "write architecture docs", "add CONTRIBUTING guide", "update repo docs", "document codebase", or mentions repository documentation, codebase analysis, or cross-repository integration documentation.
version: 1.0.0
---

# Repository Documentation

Generate comprehensive, self-contained documentation for code repositories with awareness of cross-repository integration points and dependencies.

## Purpose

Create and maintain repository documentation that includes README files, API documentation, contributing guides, and architecture documents. Each generated document is self-contained while explicitly documenting how the repository interacts with other repositories, services, and external dependencies.

## When to Use

Trigger this skill when:
- User asks to "generate documentation for this repo"
- User mentions "create/update README", "document API", "write architecture docs"
- User asks about "how this repo connects to other repos"
- User requests "CONTRIBUTING guide" or "setup documentation"
- User wants to document integration points with other repositories

## Documentation Workflow

### Phase 1: Repository Analysis

Before generating documentation, analyze the codebase to understand:

1. **Repository Structure**
   - Use `Glob` to discover key files: `README.md`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.
   - Identify main source directories (`src/`, `lib/`, `app/`, `internal/`, etc.)
   - Find configuration files (`.env.example`, `docker/`, `k8s/`, etc.)
   - Locate existing documentation (`docs/`, `*.md` files)

2. **Cross-Repository Integration Discovery**
   - Search for imports/requires referencing other repos (use `Grep` for common patterns)
   - Look for API client libraries pointing to internal services
   - Find shared dependencies or monorepo references
   - Identify external service integrations (databases, APIs, message queues)
   - Check for `.gitmodules`, `workspace` declarations, or subpackage references

3. **Technology Detection**
   - Identify primary programming language(s)
   - Find frameworks and major dependencies
   - Detect build systems and tooling
   - Note testing frameworks and CI/CD configuration

### Phase 2: Document Generation

For each document type, follow the structured templates in `examples/`. Templates contain:
- Section headers with placeholder content
- Specific placeholders for integration points
- Cross-repository dependency sections

**Key Principle:** Every generated document must include an "Integrations" or "Related Repositories" section that explicitly documents:
- Which other repositories this repo depends on
- How this repo is consumed by other repositories
- External services and dependencies
- Data flow between repositories

### Phase 3: Existing Document Updates

When updating existing documentation:
1. Read the current document using `Read`
2. Compare against current codebase state
3. Identify gaps (missing features, outdated integrations, stale dependencies)
4. Use `Edit` to update specific sections
5. Preserve existing voice and formatting where appropriate
6. Add newly discovered integration points

## Document Types

### README.md

The primary entry point for the repository. Use `examples/README-template.md` as a starting point.

Required sections:
- Project title and brief description
- Integration points with other repositories
- Quick start / Installation
- Usage examples
- API/CLI reference (link to detailed docs if separate)
- Contributing (link to CONTRIBUTING.md)
- License

### API Documentation

Document public APIs, functions, classes, and endpoints. Use `examples/API-template.md`.

Required sections:
- Overview
- Authentication/Authorization
- Endpoints/Functions with signatures
- Request/response examples
- Error handling
- Rate limits (if applicable)
- Integration points with other services

### CONTRIBUTING.md

Guide for contributors. Use `examples/CONTRIBUTING-template.md`.

Required sections:
- Prerequisites (other repos to clone, tools to install)
- Development setup
- Running tests
- Code style guidelines
- Pull request process
- Related repositories and their roles

### ARCHITECTURE.md

High-level design and integration documentation. Use `examples/ARCHITECTURE-template.md`.

Required sections:
- System overview
- Component diagram (describe verbally or use Mermaid)
- Cross-repository architecture
- Data flow between repositories
- Design decisions and rationale
- Scaling considerations

### INTEGRATIONS.md (Optional but Recommended)

Dedicated document for cross-repository relationships. Use `examples/INTEGRATIONS-template.md`.

Sections:
- Upstream dependencies (repos/services this depends on)
- Downstream consumers (repos/services that depend on this)
- Sibling repositories (related repos in the same ecosystem)
- External services
- Communication protocols between services

## Integration Discovery Guidelines

When scanning for integration points, search for:

| Pattern | Indicates |
|---------|-----------|
| `from @org/` | Internal package/repo imports (JS/TS) |
| `import.*internal` | Internal imports (Python/Java) |
| `github.com/org/` | Go module references to other repos |
| `client.*[Aa]pi` | API clients to other services |
| `restTemplate` | REST client usage (Java) |
| `fetch(` or `axios` | HTTP calls to external services |
| `messaging:` | Spring Cloud/Sidecar integrations |
| `pom.xml` `<artifactId>` | Maven dependencies |

Use `scripts/find-integration-points.py` to automate discovery.

## Writing Guidelines

### 1. Be Specific About Integrations
- Name the repositories explicitly: "Depends on `user-service` repo for authentication"
- Explain the relationship: "This repo consumes events from `event-bus` via Kafka"
- Link to the actual repositories when possible

### 2. Self-Contained Yet Connected
- Each document should stand alone
- Cross-reference other documents and repositories explicitly
- Include enough context for someone new to the broader ecosystem

### 3. Concise and Scannable
- **Use bullet points** over paragraphs for lists and procedures
- **Lead with the essential** - put most important information first
- **Use tables** for reference material (configs, commands, options)
- **Code over prose** - show examples instead of lengthy explanations
- **Collapse details** - use collapsible sections or "expand to read more" for depth
- **One concept per section** - avoid mixing multiple topics
- **Link, don't duplicate** - reference existing docs instead of repeating
- **Target reading time** - a README should take ~3-5 minutes to scan

### 4. Keep Examples Current
- Use actual code snippets from the repository
- Verify commands work before including them
- Update version numbers and dependency references
- Keep examples minimal - show only what's needed to understand

### 5. Progressive Detail
- Lead with high-level overview
- Link to detailed documentation
- Provide quick paths to "just make it work" and deep dives

## Tools and Utilities

### Scripts

Use scripts in `scripts/` for automation:

- **`find-integration-points.py`** - Scan codebase for references to other repositories
- **`analyze-repo-structure.py`** - Generate summary of repository structure and dependencies

Execute scripts without reading into context:
```bash
python skills/repo-docs/scripts/find-integration-points.py /path/to/repo
```

### References

Consult `references/` for detailed guidance:
- **`references/best-practices.md`** - Repository documentation standards
- **`references/integration-patterns.md`** - Common integration patterns and how to document them
- **`references/tech-detection.md`** - Technology detection patterns

## Additional Resources

### Reference Files

For detailed guidance beyond this core workflow:
- **`references/best-practices.md`** - Industry standards for repository documentation
- **`references/integration-patterns.md`** - Documenting microservices, monorepos, and distributed systems
- **`references/tech-detection.md`** - Patterns for identifying technologies and frameworks

### Example Templates

Templates in `examples/` provide starting points:
- **`examples/README-template.md`** - Standard README structure with integrations section
- **`examples/API-template.md`** - API documentation template
- **`examples/CONTRIBUTING-template.md`** - Contributor guide template
- **`examples/ARCHITECTURE-template.md`** - Architecture documentation template
- **`examples/INTEGRATIONS-template.md`** - Dedicated integrations document

### Scripts

Utilities in `scripts/`:
- **`scripts/find-integration-points.py`** - Automated integration discovery
- **`scripts/analyze-repo-structure.py`** - Repository structure analysis

## Quality Checklist

Before finalizing documentation, verify:

- [ ] All cross-repository dependencies are documented
- [ ] Integration points are explicitly named and described
- [ ] Quick start instructions actually work
- [ ] Code examples are from the actual codebase
- [ ] Links to other repos are included where applicable
- [ ] External service dependencies are listed
- [ ] Setup instructions include dependencies on other repos
- [ ] Document is readable without access to other repositories
