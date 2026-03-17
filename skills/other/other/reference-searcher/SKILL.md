---
name: reference-searcher
description: Systematic external reference searching across documentation, open-source repositories, and web resources. Use when working with unfamiliar libraries, APIs, or when needing production-quality implementation examples.
---

# Reference Searcher

Structured methodology for searching external references — official docs, open-source implementations, and web resources — to inform development decisions.

## When to Use This Skill

- Working with unfamiliar libraries or frameworks
- Needing production-quality implementation examples
- Debugging unexpected behavior from external dependencies
- Finding best practices for specific patterns (auth, caching, etc.)
- Evaluating library choices with real-world usage data

## What This Skill Does

### Search Strategy: Three Layers

#### Layer 1: Official Documentation

Search official docs for the specific library using web search:

```bash
# Search official docs directly
# e.g., "next.js middleware authentication site:nextjs.org"
# Or use documentation MCP tools if available (e.g., Context7)
```

Best for: API signatures, configuration options, migration guides, official patterns.

#### Layer 2: Open-Source Implementation Examples (GitHub)

Search real codebases for production patterns:

```bash
# Search GitHub for code patterns via grep.app or GitHub search
# e.g., https://grep.app/search?q=getServerSession%28&filter[lang][0]=TypeScript
# Or use GitHub code search: gh search code "getServerSession(" --language=TypeScript
```

Best for: How established projects (1000+ stars) handle specific patterns, battle-tested error handling, real-world integration examples.

**Search tips:**
- Search for actual code patterns, not keywords
- Use `(?s)` prefix for multi-line regex patterns
- Filter by language and file path for precision
- Look for repos with 1000+ stars for production quality

#### Layer 3: Web Search (Current Information)

Search the web for recent articles, discussions, and guides:

```bash
# Web search for current information
# e.g., "OWASP JWT security best practices 2024"
```

Best for: Security advisories, recent breaking changes, community discussions, performance benchmarks, "why does X behave this way" questions.

### Search Workflow

1. **Start with official docs** — fastest, most authoritative
2. **If docs insufficient** — search GitHub for real implementations
3. **If pattern unclear** — web search for community knowledge
4. **Synthesize** — combine findings into actionable guidance

### Result Evaluation

For each source found, assess:

| Criterion | Check |
|-----------|-------|
| Recency | Is this from the current major version? |
| Authority | Official docs > popular repos > blog posts |
| Completeness | Does it cover error handling and edge cases? |
| Applicability | Does it match our tech stack and constraints? |

### Output Format

```markdown
## Research: [Topic]

### Official Documentation
- [Finding 1 with link]
- [Finding 2 with link]

### Production Examples
- [Repo/file]: [What pattern they use and why]
- [Repo/file]: [Alternative approach]

### Recommendation
Based on [sources], the recommended approach is [X] because [reasons].

### Caveats
- [Known limitation or gotcha]
```

## Anti-Patterns

- Searching for keywords instead of actual code patterns on GitHub
- Trusting blog posts over official documentation
- Using examples from outdated library versions
- Skipping error handling patterns in reference code
- Over-researching — stop when you have enough to proceed confidently

## Example

**User**: "How should I implement rate limiting in Express?"

**Output**:
1. Official docs: express-rate-limit documentation — configuration options, store adapters
2. GitHub: 3 production repos showing Redis-backed rate limiting with sliding window
3. Web: OWASP rate limiting guidelines, comparison of token bucket vs sliding window
4. Recommendation: Use `express-rate-limit` with Redis store, sliding window algorithm, with specific config example

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) Librarian agent
