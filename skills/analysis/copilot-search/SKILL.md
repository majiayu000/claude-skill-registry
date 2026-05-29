---
name: copilot-search
description: Search the web using Claude Code's WebSearch/WebFetch tools combined with GitHub Copilot CLI to find current documentation, best practices, solutions, and technical information. Use when the user needs to research libraries, find API documentation, troubleshoot errors, or learn about new technologies. Requires Copilot CLI installed.
allowed-tools: Bash, Read, Grep, Glob, WebFetch, WebSearch
---

# Copilot Search Skill

Use Claude Code's web search capabilities combined with GitHub Copilot CLI to research current information, documentation, and solutions. This is a **read-only research** skill.

## When to Use

- User asks "what's the best library for X?"
- User needs current documentation or API references
- User wants to compare different libraries or approaches
- User has an error message and needs solutions
- User asks about best practices or security recommendations
- User wants to learn about a new technology or framework
- User needs to find tutorials or getting started guides

## Important Note

**GitHub Copilot CLI does not have built-in web search capabilities.** This skill uses:

- **WebSearch** and **WebFetch** tools for web research (primary)
- **Copilot CLI** for code analysis and contextualization (optional)

## Prerequisites

Verify Copilot CLI is available (optional for local context):

```bash
copilot --version  # Should display installed version
```

Ensure you have internet connectivity for web search.

## Basic Usage

### Step 1: Parse the Research Need

Extract what the user wants to know:

- Specific technology or library?
- What aspect (documentation, comparison, best practices)?
- Any version requirements?
- Context from current project?

### Step 2: Gather Local Context (Optional)

Check current project context if relevant:

```bash
# Check current dependencies
cat package.json  # or requirements.txt, go.mod, etc.

# Check versions in use
npm list --depth=0  # or pip list, go list, etc.

# Check git status
git status
git log --oneline -5
```

Use Read, Grep, Glob to understand existing patterns.

### Step 3: Execute Web Search

Use the **WebSearch** tool for broad research:

```
Query: "[TOPIC] latest documentation 2026"
Query: "best practices for [TECHNOLOGY] security 2026"
Query: "[ERROR_MESSAGE] solution [FRAMEWORK] [VERSION]"
```

**Search strategies:**

- Be specific about what you're looking for
- Include version numbers if known
- Specify "latest" or "2026" for current info
- Request official sources when possible
- Include framework/language context

**Example queries:**

```
"Next.js 15 authentication best practices 2026"
"React useEffect cleanup function official documentation"
"TypeScript generic constraints examples"
"Python async/await security vulnerabilities 2026"
```

### Step 4: Fetch and Verify Sources

Use **WebFetch** to retrieve specific documentation:

```
URL: https://nextjs.org/docs/app/building-your-application/authentication
Prompt: "Extract authentication best practices, code examples, and security recommendations"

URL: https://react.dev/reference/react/useEffect
Prompt: "Find cleanup function usage, common patterns, and gotchas"
```

**Verification steps:**

- Check publication dates (prefer recent sources)
- Verify information from official documentation
- Cross-reference multiple sources for controversial topics
- Look for version-specific information
- Check for deprecation warnings

### Step 5: Optional - Use Copilot CLI for Context

If needed, use Copilot CLI to understand how findings apply to the current codebase:

```bash
copilot
```

Then ask:

```
Based on the current codebase patterns, how would we implement [SOLUTION_FROM_SEARCH]?

Context from web search:
- [Key findings]
- [Recommended approach]
- [Code examples]

Analyze the current codebase and suggest how to integrate this approach.
Do NOT make changes - analysis only.
```

### Step 6: Present Results

Format the response with proper citations:

````markdown
## Research: [Topic]

### Summary

[Direct answer with key findings in 2-3 sentences]

### Official Documentation

- [Library Name - Topic](https://official-url) - Official reference
- [API Docs](https://api-url) - API documentation

### Key Findings

**Best Practices:**

1. [Practice] - [Explanation] ([Source URL])
2. [Practice] - [Explanation] ([Source URL])

**Common Pitfalls:**

- [Issue] - [How to avoid] ([Source URL])

**Recommendations:**

- [Recommendation with reasoning]

### Code Examples

```language
// Source: [URL]
// Example: [Description]
[Working code example]
```

### Alternative Approaches

| Approach   | Pros | Cons | Use When |
| ---------- | ---- | ---- | -------- |
| [Option 1] | ...  | ...  | ...      |
| [Option 2] | ...  | ...  | ...      |

### Integration Notes

[If Copilot CLI was used, include local context here]

- Current patterns: [What exists]
- Suggested approach: [How to integrate]
- Files to modify: [Specific paths]

### Sources

All information sourced from:

1. [Title](URL) - [Description]
2. [Title](URL) - [Description]
3. [Title](URL) - [Description]

Last verified: [Current date]
````

## Example Queries

### Documentation Lookup

```
WebSearch query: "React hooks official documentation 2026"
WebFetch URL: https://react.dev/reference/react
Prompt: "Extract useState, useEffect, useContext documentation with examples"
```

### Library Comparison

```
WebSearch query: "Prisma vs TypeORM vs Drizzle comparison TypeScript 2026"
WebFetch: Official docs for each library
Create comparison table from findings
```

### Error Resolution

```
WebSearch query: "ECONNREFUSED Node.js solution 2026"
WebSearch query: "ECONNREFUSED common causes troubleshooting"
Verify solutions from multiple sources
```

### Best Practices

```
WebSearch query: "JWT authentication security best practices OWASP 2026"
WebFetch: https://owasp.org (if applicable)
WebFetch: Official framework security docs
```

### Getting Started

```
WebSearch query: "Next.js 15 getting started tutorial 2026"
WebFetch: https://nextjs.org/learn
Extract setup, core concepts, first app tutorial
```

## Best Practices

✅ **DO:**

- Always use WebSearch for broad queries
- Use WebFetch to verify official sources
- Include URLs for all sources
- Prefer official documentation over blog posts
- Verify information is current (2025-2026)
- Cross-reference multiple sources
- Note when information is version-specific
- Include security considerations
- Use Copilot CLI for local codebase context (optional)

❌ **DON'T:**

- Make or suggest code changes (use copilot-exec for that)
- Trust outdated information (pre-2024 for fast-moving tech)
- Rely on single sources
- Present unverified information
- Skip source attribution
- Ignore official documentation
- Modify code (this is read-only research)

## Source Evaluation

**Prioritize:**

- Official documentation and guides
- Official GitHub repositories
- CVE databases and security advisories
- MDN (for web standards)
- OWASP (for security)
- RFC specifications
- Major framework official blogs

**Verify:**

- Stack Overflow (check dates, votes)
- Reputable tech blogs
- GitHub issues
- Conference talks

**Use with caution:**

- Personal blogs (unless from known experts)
- Old tutorials (pre-2024)
- Unverified forum posts

## Error Handling

**If WebSearch returns no results:**

- Simplify the query
- Try alternative keywords
- Search for related concepts
- Use broader terms

**If results are outdated:**

- Explicitly request "2026" or "latest" in query
- Use WebFetch to check official docs directly
- Ask for recent comparisons

**If results conflict:**

- Search for official stance
- Check version-specific differences
- Verify dates and determine which is current
- Prefer official documentation

**If Copilot not found (optional):**

```
Copilot CLI is not available. Continuing with web search only.
Install: https://github.com/github/copilot-cli
```

## Integration with Codebase

After gathering information:

1. **Assess applicability** to current project
2. **Check compatibility** with existing dependencies
3. **Plan implementation** steps if adopting findings
4. **Suggest testing** approach

Example:

```bash
# After researching a library, check compatibility
npm info [package]@latest peerDependencies
npm install [package]@latest --dry-run
```

## Related Skills

- **copilot-ask**: For understanding existing code in your codebase
- **copilot-exec**: For implementing solutions found through research
- **copilot-review**: For validating code quality after implementation

## Use Cases

### Technology Evaluation

Research before choosing a library or framework:

```
WebSearch query: "GraphQL vs REST vs tRPC TypeScript API comparison 2026"
```

### Migration Planning

Find migration guides and breaking changes:

```
WebSearch query: "Vue 2 to Vue 3 migration guide breaking changes"
WebFetch: Official Vue migration documentation
```

### Security Research

Find vulnerabilities and best practices:

```
WebSearch query: "express 4.18 security vulnerabilities CVE 2026"
WebFetch: GitHub Security Advisories
WebFetch: npm security advisories
```

### Learning

Get tutorials and learning resources:

```
WebSearch query: "TypeScript beginner tutorial 2026 official"
WebFetch: https://www.typescriptlang.org/docs/handbook/
```

### Troubleshooting

Research error messages and solutions:

```
WebSearch query: "Module not found webpack 5 solution"
Cross-reference Stack Overflow and official docs
```

## Advanced Usage

### Multi-Query Research

For complex research, break into focused queries:

```
# Query 1: Current state
WebSearch: "current best practice for SSR in React 2026"

# Query 2: Specific implementation
WebFetch: Official React Server Components documentation

# Query 3: Gotchas
WebSearch: "React Server Components common problems solutions"
```

### Version-Specific Research

```
WebSearch: "TypeScript 5.5 new features changelog"
WebFetch: Official TypeScript release notes
Compare with current project TypeScript version
```

### Comparison Research

```
WebSearch: "Vite vs webpack vs Turbopack 2026 benchmarks"
WebFetch: Official documentation for each tool
Create comparison table with pros/cons
```

### Local Context with Copilot CLI

```bash
# After web research, use Copilot for local context
copilot
```

```
I found these approaches for [TOPIC] from web research:
1. [Approach A] - [Description]
2. [Approach B] - [Description]

Analyze our current codebase:
- Which approach aligns with our patterns?
- What files would need modification?
- Are there any compatibility issues?

Provide file references and recommendations.
Do NOT make changes - analysis only.
```

## Limitations

- Requires internet connectivity for WebSearch/WebFetch
- Search quality depends on available online information
- May return outdated info if not explicitly filtered
- Cannot execute or test code
- Cannot make code modifications
- Limited to publicly available information
- Copilot CLI cannot perform web searches (only local code analysis)

## Tips for Better Results

1. **Be specific**: "What's the best React state management library for large apps?" vs "What's good for state?"
2. **Include context**: "For a Next.js 15 app with TypeScript..."
3. **Request sources**: "Include official documentation and recent comparisons"
4. **Specify timeframe**: "Current best practices in 2026"
5. **Define scope**: "Focus on security best practices"

---

**Remember**: This skill is READ-ONLY research using WebSearch and WebFetch as primary tools, with optional Copilot CLI for local codebase context. Always cite sources and verify information is current. For code modifications, use the `copilot-exec` skill.
