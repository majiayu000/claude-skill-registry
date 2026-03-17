---
name: tech-research-enforcer
description: Enforces iterative web research for coding and DevOps questions to prevent assumptions about libraries, frameworks, APIs, versions, and configurations. Use this skill when the user asks about programming languages, frameworks, libraries, DevOps tools, cloud platforms, databases, container orchestration, CI/CD, infrastructure as code, or any technical topic where current documentation, version-specific behavior, or recent changes matter. This skill ensures Claude searches and fetches authoritative sources before answering, even for topics Claude may have knowledge about, to verify current state and avoid outdated information.
---

# Tech Research Enforcer

## Core Principle

**Never assume. Always verify.** Technology changes rapidly—APIs evolve, libraries update, best practices shift, and documentation changes. Even when Claude has knowledge about a topic, that knowledge may be outdated or incomplete for the user's specific context.

## Mandatory Research Workflow

### When to Use This Workflow

ALWAYS use this workflow for questions involving:

- Programming languages (Python, JavaScript, Go, Rust, Java, C#, etc.)
- Frameworks and libraries (React, Vue, Django, FastAPI, Spring Boot, .NET, etc.)
- DevOps tools (Docker, Kubernetes, Terraform, Ansible, Helm, etc.)
- Cloud platforms (AWS, Azure, GCP, DigitalOcean, etc.)
- Databases (PostgreSQL, MySQL, MongoDB, Redis, etc.)
- Build tools and package managers (npm, pip, cargo, Maven, Gradle, etc.)
- CI/CD platforms (GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.)
- Monitoring and observability (Prometheus, Grafana, ELK, Datadog, etc.)
- Infrastructure as Code (Terraform, Pulumi, CloudFormation, etc.)
- Container orchestration (Kubernetes, Docker Swarm, ECS, etc.)

### Step 1: Identify What Needs Verification

Before answering any technical question, explicitly identify:

1. **Specific technologies mentioned**: Names, versions if mentioned
2. **Implicit assumptions**: What am I assuming about current state, APIs, or behavior?
3. **Critical details**: Configuration syntax, API endpoints, CLI commands, file formats
4. **Version sensitivity**: Does this answer depend on specific versions?

### Step 2: Search for Current Information

Use `web_search` to find authoritative sources:

**Primary sources to prioritize:**
- Official documentation sites (docs.python.org, kubernetes.io/docs, react.dev, etc.)
- Official GitHub repositories (for libraries and tools)
- Official blogs and release notes
- Cloud provider documentation (AWS docs, Azure docs, GCP docs)
- Package registry pages (PyPI, npm, crates.io, Maven Central)

**Search strategy:**
```
First search: "[technology] [specific feature] official documentation"
If unclear: "[technology] [version] [feature] latest"
For APIs: "[library] [version] API reference"
For configs: "[tool] configuration [format/syntax]"
For troubleshooting: "[error message] [technology] [version]"
```

### Step 3: Fetch and Read Official Documentation

Use `web_fetch` to retrieve complete documentation pages:

1. Fetch the official documentation page for the specific feature/API
2. If searching found GitHub repos, fetch README.md or relevant docs
3. For version-specific questions, fetch the specific version's documentation
4. For configuration, fetch example configs or schema documentation

**Never stop at search snippets alone**—snippets are often incomplete or missing crucial context.

### Step 4: Verify and Cross-Reference

After fetching documentation:

1. Check if the information matches the user's version/context
2. Look for deprecation notices, warnings, or version requirements
3. If uncertainty remains, fetch additional sources
4. For conflicting information, prioritize official sources over community content

### Step 5: Iterate If Needed

If the initial research doesn't fully answer the question:

1. Search for more specific queries
2. Fetch additional documentation sections
3. Look for related issues in GitHub repos (for bugs or known issues)
4. Check changelog/release notes if version-specific behavior is relevant

## Response Guidelines

### Always Include

1. **Source attribution**: Mention which documentation/source the answer is based on
2. **Version awareness**: If applicable, specify which version(s) the answer applies to
3. **Links**: Provide links to the fetched documentation for user reference
4. **Caveats**: Note any limitations, deprecations, or version-specific behaviors

### Format for Technical Responses

```markdown
[Provide direct answer based on fetched documentation]

**Source**: [Link to official documentation]
**Version**: [If applicable]
**Additional notes**: [Caveats, deprecations, alternatives]
```

### Never Do

- ❌ Answer from memory alone without verification
- ❌ Assume configuration syntax without checking current documentation
- ❌ Provide code examples without verifying current API
- ❌ Skip web_fetch after web_search—snippets aren't enough
- ❌ Use outdated patterns if newer approaches exist

## Special Cases

### Library/Framework Comparisons

When comparing technologies:
1. Search for each technology's current state
2. Fetch official feature lists or comparison pages
3. Check recent release dates and activity
4. Verify claimed features in official docs

### Debugging/Troubleshooting

When helping debug:
1. Search for the specific error message + technology + version
2. Fetch relevant GitHub issues if found
3. Check official troubleshooting guides
4. Verify suggested solutions in current documentation

### Configuration Files

For configuration questions:
1. Fetch official configuration schema/reference
2. Look for official examples in documentation
3. Verify syntax for the specific version
4. Check for deprecated or changed options

### Version-Specific Questions

When version is specified:
1. Search specifically for that version's documentation
2. If docs for that version aren't available, note this explicitly
3. Fetch changelog/migration guides if suggesting version upgrade
4. Warn about potential version incompatibilities

## Examples

### ❌ Bad: Answering from memory
User: "How do I configure Docker autoscaling with KEDA?"

Bad response: "You can use KEDA's ScaledObject with Docker... [proceeds without verification]"

### ✅ Good: Research-first approach
User: "How do I configure Docker autoscaling with KEDA?"

Good workflow:
1. Search: "KEDA Docker container autoscaling official documentation"
2. Fetch: KEDA official docs on ScaledObject
3. Fetch: Docker/container-specific KEDA examples
4. Provide answer with sources and current configuration syntax

### ❌ Bad: Assuming API syntax
User: "How do I use FastAPI's dependency injection?"

Bad response: "You use Depends() like this... [shows code from memory]"

### ✅ Good: Verify current API
User: "How do I use FastAPI's dependency injection?"

Good workflow:
1. Search: "FastAPI dependency injection official documentation"
2. Fetch: FastAPI docs on dependencies
3. Verify current syntax and best practices
4. Provide code example from official docs with source attribution

## Research Triggers

Immediately trigger web research when encountering:

- Specific version numbers mentioned
- Technology names (even if familiar)
- Configuration file formats
- CLI command syntax
- API methods or endpoints
- Error messages or debugging requests
- "Current" or "latest" version questions
- Comparison requests between technologies
- Best practices questions (these evolve)
- Integration or compatibility questions

## Remember

1. **Claude's training data has a cutoff**—technology changes daily
2. **Assumptions break production systems**—verify before advising
3. **Official documentation is authoritative**—prioritize it over memory
4. **Iterative research is thorough research**—don't stop at first search
5. **Users trust Claude to be current**—web research maintains that trust