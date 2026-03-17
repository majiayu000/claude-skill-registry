---
name: octocode
description: Semantic code research across GitHub repositories for finding implementations, patterns, and conducting PR/security reviews.
agents: [morgan, cleo, cipher, rex, nova, blaze, grizz, tap, spark, bolt, vex]
triggers: [code search, find implementation, how does X work, pattern, review PR, security audit, real code, production examples]
---

# OctoCode (Semantic Code Research)

Use OctoCode to search across GitHub repositories for real implementations, patterns, and to conduct code/security reviews. Unlike Context7 (documentation lookup), OctoCode finds **actual production code**.

## Tools

| Tool | Purpose |
|------|---------|
| `octocode_githubSearchCode` | Search code across repositories by content or path |
| `octocode_githubSearchRepositories` | Discover repositories by topics, keywords, stars |
| `octocode_githubViewRepoStructure` | Explore repository directory structure |
| `octocode_githubGetFileContent` | Read files with pattern matching and line ranges |
| `octocode_githubSearchPullRequests` | Search PRs with discussions, diffs, and metadata |
| `octocode_packageSearch` | Search npm and PyPI packages |

## When to Use OctoCode vs Context7

| Need | Tool | Why |
|------|------|-----|
| Library API documentation | **Context7** | Curated, version-specific docs |
| Find real implementations | **OctoCode** | Searches actual codebases |
| How does React do X? | **OctoCode** | Search React's source code |
| Axum middleware examples | **OctoCode** | Find production patterns |
| PR review with evidence | **OctoCode** | `/review_pull_request` command |
| Security vulnerability patterns | **OctoCode** | `/review_security` command |

## Common Workflows

### 1. Research Implementation Patterns

```
# Find OAuth implementations in Rust
octocode_githubSearchCode({
  query: "oauth axum",
  language: "rust",
  stars: ">100"
})

# Then explore the top result
octocode_githubViewRepoStructure({
  owner: "found-org",
  repo: "found-repo",
  path: "src/auth"
})

# Read the specific implementation
octocode_githubGetFileContent({
  owner: "found-org",
  repo: "found-repo",
  path: "src/auth/oauth.rs"
})
```

### 2. PR Review (Cleo)

For code quality reviews, use OctoCode to find canonical implementations for comparison:

```
# Find how top projects handle the same pattern
octocode_githubSearchCode({
  query: "error handling middleware",
  language: "typescript",
  stars: ">1000"
})
```

### 3. Security Analysis (Cipher)

For security reviews, search for vulnerability patterns and fixes:

```
# Find how security issues were fixed
octocode_githubSearchPullRequests({
  query: "CVE fix authentication",
  state: "merged",
  repo: "relevant/repo"
})
```

### 4. Research for Task Generation (Morgan)

Before generating implementation tasks, research existing patterns:

```
# How do multi-agent platforms handle task decomposition?
octocode_githubSearchCode({
  query: "task decomposition agent",
  language: "rust OR python",
  stars: ">500"
})
```

## OctoCode Commands (Prompts)

OctoCode provides specialized prompt commands for complex research:

| Command | Purpose | Use Case |
|---------|---------|----------|
| `/research` | Deep code discovery and pattern analysis | Finding implementations before coding |
| `/plan` | Research-backed implementation planning | Planning complex features |
| `/review_pull_request` | Defects-first PR analysis | Quality reviews with evidence |
| `/review_security` | Security audit with validation | Security analysis with citations |

### Using `/research`

```
/research How does React's useState hook work internally?
/research Compare state management: Redux vs Zustand vs Jotai
/research Find authentication patterns in axum Rust projects
```

### Using `/review_pull_request`

```
/review_pull_request prUrl: https://github.com/5dlabs/cto/pull/123
```

This provides:
- **Defects & Bugs**: Logic errors, edge cases, race conditions
- **Security Issues**: Injection vulnerabilities, auth bypasses
- **Performance**: N+1 queries, memory leaks
- **Code Quality**: Complexity, maintainability

### Using `/review_security`

```
/review_security repoUrl: https://github.com/5dlabs/cto
```

This provides:
- **Authentication & Authorization**: Auth flows, session management
- **Input Validation**: Injection points, sanitization
- **Secrets Management**: Hardcoded credentials, API keys
- **Dependencies**: Known vulnerabilities, supply chain risks

## Best Practices

1. **Use both tools together** - Context7 for docs, OctoCode for implementations
2. **Be specific with searches** - "axum middleware error handling" not "error handling"
3. **Filter by stars** - `stars:>100` for quality code
4. **Cite your sources** - Include GitHub links in research findings
5. **Check recent PRs** - For understanding how issues were solved

## Integration with Deep Research

OctoCode complements Firecrawl for comprehensive research:

| Research Type | Primary Tool | Secondary Tool |
|---------------|--------------|----------------|
| Competitive analysis | Firecrawl Agent | OctoCode (open source competitors) |
| Implementation patterns | OctoCode | Context7 (docs for libraries used) |
| Best practices | Firecrawl | OctoCode (real code examples) |
| Bug investigation | OctoCode | GitHub MCP (internal PRs) |

## Example: Research-Backed Task Generation

When Morgan processes a PRD mentioning "implement OAuth like Auth0":

```
1. Use OctoCode to search for OAuth implementations:
   octocode_githubSearchCode({ query: "oauth2 refresh token rotation rust" })

2. Analyze how top projects structure auth:
   octocode_githubViewRepoStructure({ owner: "top-project", repo: "auth" })

3. Extract patterns from implementations:
   octocode_githubGetFileContent({ 
     owner: "top-project", 
     repo: "auth", 
     path: "src/oauth.rs",
     matchString: "refresh_token"
   })

4. Embed findings in task details for implementation agents
```
