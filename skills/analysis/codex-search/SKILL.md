---
name: codex-search
description: Search the web using OpenAI Codex CLI to find current documentation, best practices, solutions, and technical information. Use when the user needs to research libraries, find API documentation, troubleshoot errors, or learn about new technologies. Requires Codex CLI installed.
allowed-tools: Bash, Read, Grep, Glob, WebFetch, WebSearch
---

# Codex Search Skill

Use OpenAI Codex CLI with web search capabilities to research current information, documentation, and solutions. This is a **read-only research** skill.

## When to Use

- User asks "what's the best library for X?"
- User needs current documentation or API references
- User wants to compare different libraries or approaches
- User has an error message and needs solutions
- User asks about best practices or security recommendations
- User wants to learn about a new technology or framework
- User needs to find tutorials or getting started guides

## Prerequisites

Verify Codex CLI is available:

```bash
codex --version  # Should display installed version
```

**Requirements:**

- Internet connectivity for web search
- Authenticated Codex access (ChatGPT Plus/Pro/Team/Enterprise or API key in `~/.codex/config.toml`)
- Web search enabled in `~/.codex/config.toml` as follows:
  ```toml
  [features]
  web_search_request = true
  ```

**Note:** The `--search` flag enables Codex's native web search tool. If web search is not available in your environment, the skill will provide information based on the model's training data.

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
```

### Step 3: Execute Codex Search

Run Codex with the `--search` flag for web research:

```bash
codex --sandbox=read-only --search exec "Research and provide comprehensive information about: [QUERY]

Include:
1. Direct answer to the question
2. Official documentation links
3. Best practices and recommended approaches
4. Code examples with explanations
5. Common pitfalls and how to avoid them
6. Alternative approaches if applicable
7. Source URLs for all information

Search context:
- Current year: 2026
- Looking for latest/current information
- Prefer official documentation over third-party sources
- Include security considerations if relevant

Do NOT make any changes - this is research only."
```

### Step 4: Present Results

Format the response with proper citations:

- **Summary**: Direct answer with key findings
- **Official Documentation**: Links to authoritative sources
- **Best Practices**: Recommendations with reasoning
- **Code Examples**: Working examples from official docs
- **Sources**: All URLs cited

## Example Queries

### Documentation Lookup

```bash
codex --sandbox=read-only --search exec "Find official documentation for React hooks in 2026:
- useState, useEffect, useContext documentation
- Best practices for custom hooks
- Performance optimization tips
- Official examples
Include only official React documentation."
```

### Library Comparison

```bash
codex --sandbox=read-only --search exec "Compare Prisma vs TypeORM vs Drizzle for TypeScript database ORMs in 2026:
- Feature comparison
- Performance benchmarks
- Community adoption
- Learning curve
- Use case recommendations
Include recent comparisons and official documentation."
```

### Error Resolution

```bash
codex --sandbox=read-only --search exec "Research solutions for error: 'ECONNREFUSED' in Node.js:
- Root causes
- Common solutions
- Prevention strategies
- Related issues
Include Stack Overflow discussions and official Node.js docs."
```

### Best Practices

```bash
codex --sandbox=read-only --search exec "Find current security best practices for JWT authentication in 2026:
- OWASP recommendations
- Token storage best practices
- Refresh token patterns
- Common vulnerabilities
- Security tools
Prioritize official sources and security organizations."
```

### Getting Started

```bash
codex --sandbox=read-only --search exec "Find getting started guide for Next.js 15 in 2026:
- Installation and setup
- Project structure
- Core concepts
- First app tutorial
- Best practices for beginners
Use official Next.js documentation."
```

## Output Format

Structure research findings like this:

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

### Sources

All information sourced from:

1. [Title](URL) - [Description]
2. [Title](URL) - [Description]
3. [Title](URL) - [Description]

Last verified: [Current date]
````

## Best Practices

✅ **DO:**

- Always use `--search` flag for web research
- Include URLs for all sources
- Prefer official documentation over blog posts
- Verify information is current (2025-2026)
- Cross-reference multiple sources
- Note when information is version-specific
- Include security considerations

❌ **DON'T:**

- Make or suggest code changes (use codex-exec for that)
- Trust outdated information (pre-2024 for fast-moving tech)
- Rely on single sources
- Present unverified information
- Skip source attribution
- Ignore official documentation

## Verification

After getting Codex's search results:

1. Verify URLs are accessible and relevant
2. Check dates on sources (prefer recent)
3. Confirm information matches official docs
4. Cross-reference conflicting information
5. Add context specific to user's project if applicable

## Source Evaluation

**Prioritize:**

- Official documentation and guides
- Official GitHub repositories
- CVE databases and security advisories
- MDN (for web standards)
- OWASP (for security)
- RFC specifications

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

**If Codex not found:**

```
Codex CLI is not available. Ensure it's installed and in your PATH.
Install: https://developers.openai.com/codex/cli/
```

**If authentication fails:**

```
Codex CLI needs authentication. Run:
codex

Then follow the prompts to sign in with ChatGPT or configure API key.
```

**If search returns no results:**

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

- **codex-ask**: For understanding existing code in your codebase
- **codex-exec**: For implementing solutions found through research
- **codex-review**: For validating code quality after implementation

## Tips for Better Results

1. **Be specific**: "What's the best React state management library for large apps?" vs "What's good for state?"
2. **Include context**: "For a Next.js 15 app with TypeScript..."
3. **Request sources**: "Include official documentation and recent comparisons"
4. **Specify timeframe**: "Current best practices in 2026"
5. **Define scope**: "Focus on security best practices"

## Use Cases

### Technology Evaluation

Research before choosing a library or framework:

```bash
codex --sandbox=read-only --search exec "Evaluate GraphQL vs REST vs tRPC for TypeScript API in 2026"
```

### Migration Planning

Find migration guides and breaking changes:

```bash
codex --sandbox=read-only --search exec "Find breaking changes migrating from Vue 2 to Vue 3"
```

### Security Research

Find vulnerabilities and best practices:

```bash
codex --sandbox=read-only --search exec "Search for security vulnerabilities in express@4.18 CVE advisories"
```

### Learning

Get tutorials and learning resources:

```bash
codex --sandbox=read-only --search exec "Find beginner-friendly TypeScript tutorial for 2026"
```

### Troubleshooting

Research error messages and solutions:

```bash
codex --sandbox=read-only --search exec "Solutions for 'Module not found' error in webpack 5"
```

## Limitations

- Requires internet connectivity
- Search quality depends on available online information
- May return outdated info if not explicitly filtered
- Cannot execute or test code
- Cannot make code modifications
- Limited to publicly available information

## Advanced Usage

### Multi-Query Research

For complex research, break into focused queries:

```bash
# Query 1: Current state
codex --sandbox=read-only --search exec "What is the current recommended approach for SSR in React 2026?"

# Query 2: Specific implementation
codex --sandbox=read-only --search exec "Find implementation examples for React Server Components"

# Query 3: Gotchas
codex --sandbox=read-only --search exec "Common problems with React Server Components and solutions"
```

### Version-Specific Research

```bash
codex --sandbox=read-only --search exec "Find features specific to TypeScript 5.5:
- New features in this version
- Breaking changes from 5.4
- Migration guide
Ensure results are version-specific."
```

### Comparison Research

```bash
codex --sandbox=read-only --search exec "Detailed comparison of Vite vs webpack vs Turbopack in 2026:
- Build performance benchmarks
- Developer experience
- Ecosystem and plugin support
- Production optimization
- Migration complexity from webpack
Include recent benchmarks and official documentation."
```

---

**Remember**: This skill is READ-ONLY research. For code modifications, use the `codex-exec` skill. Always cite sources and verify information is current.
