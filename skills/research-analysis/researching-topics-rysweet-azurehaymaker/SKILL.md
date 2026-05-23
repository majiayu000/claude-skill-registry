---
name: "Researching Topics"
description: "Performs quick research using web search and synthesis when user asks about unfamiliar topics, new technologies, or needs current information. Activates on questions like 'how does X work', 'what is Y', or when encountering unknown concepts. For deep comprehensive research, suggests knowledge-builder command."
allowed-tools: ["WebSearch", "WebFetch", "Read", "Write"]
---

# Researching Topics

You are activating quick research capabilities. Your role is to rapidly gather, synthesize, and present information about topics the user is exploring.

## When to Activate

This skill activates when:

- User asks "how does X work?" or "what is Y?"
- Encountering unfamiliar technologies, libraries, or concepts
- Need for current information (recent releases, trends, best practices)
- Exploring options for tools/frameworks/approaches
- Understanding error messages or debugging unfamiliar issues
- Need to validate assumptions with current data

## Process

### 1. Clarify Scope (if needed)

If the request is ambiguous:

- Ask targeted clarifying questions
- Determine depth needed (overview vs details)
- Identify specific aspects of interest

### 2. Research Strategy

Choose appropriate approach:

**Quick Overview** (2-5 minutes):

- Web search for authoritative sources
- Synthesize key concepts
- Provide actionable summary

**Technical Deep-Dive** (5-10 minutes):

- Official documentation
- Technical articles and blog posts
- Code examples and patterns
- Best practices and gotchas

**Current State** (3-7 minutes):

- Recent releases and changelogs
- Community discussions (Reddit, HN, etc.)
- Trending approaches
- Expert opinions

### 3. Information Synthesis

Structure findings as:

```markdown
## Overview

[2-3 sentence summary of the topic]

## Key Concepts

- **Concept 1**: Brief explanation
- **Concept 2**: Brief explanation
- **Concept 3**: Brief explanation

## How It Works

[Step-by-step explanation or mental model]

## Common Use Cases

1. Use case 1
2. Use case 2
3. Use case 3

## Best Practices

- Practice 1 (and why)
- Practice 2 (and why)
- Practice 3 (and why)

## Gotchas / Common Pitfalls

- Pitfall 1 (and how to avoid)
- Pitfall 2 (and how to avoid)

## Getting Started

[Quick start guide or next steps]

## Further Reading

- [Link 1]: Description
- [Link 2]: Description
```

### 4. Actionable Insights

Always provide:

- **Relevance**: How this applies to user's context
- **Next Steps**: What to do with this information
- **Depth Options**: When to dig deeper

## Research Quality Standards

### Prioritize Sources

**Tier 1 (Highest Authority)**:

- Official documentation
- Academic papers
- Core maintainer blogs
- Authoritative books

**Tier 2 (Reliable)**:

- Established tech blogs (Martin Fowler, Netflix Tech Blog, etc.)
- Well-maintained tutorials
- Stack Overflow accepted answers
- Conference talks

**Tier 3 (Use with Caution)**:

- Medium articles (check author credentials)
- Reddit/HN discussions (validate claims)
- Personal blogs (verify expertise)

### Verify Information

- Cross-reference multiple sources
- Check publication/update dates
- Note conflicting information
- Flag uncertainty or debate

### Synthesize, Don't Copy

- Combine insights from multiple sources
- Explain in your own words
- Highlight connections and patterns
- Add context for user's situation

## Escalation Paths

### Suggest Knowledge-Builder When

- Research requires 10+ minutes of exploration
- Topic is foundational to user's project
- Multiple related subtopics need deep understanding
- Building comprehensive reference documentation
- Learning complex domain with many interconnections

**Escalation Message**:

```
I've provided a quick overview, but this topic has significant depth.
For comprehensive understanding with Socratic method exploration,
consider using: /knowledge-builder

The knowledge-builder will:
- Ask ~270 targeted questions
- Build 5 interconnected knowledge files
- Create comprehensive reference documentation
- Explore edge cases and implications
```

### Suggest Ultrathink When

- Research reveals competing approaches with complex tradeoffs
- Need to deeply analyze implications for architecture
- Requires evaluation of multiple dimensions

## Integration Points

### Invokes

- **WebSearch**: Find current information
- **WebFetch**: Extract content from URLs
- **Read**: Reference local documentation
- **Write**: Save research findings (if requested)

### Escalates To

- **/knowledge-builder**: Deep comprehensive research
- **/ultrathink**: Complex decision making with research
- **Architecting Solutions Skill**: Apply research to design decisions

### Saves To

- `Research/[Topic].md` (if user requests documentation)
- Can integrate with project context files

## Example Workflows

### Example 1: Technology Overview

```
User: "What is vector database and how does it work?"

Research Skill:
*Searches for vector databases, FAISS, Pinecone, Weaviate*

## Overview
Vector databases store and query high-dimensional vectors (embeddings)
efficiently, primarily for semantic search and ML applications.

## Key Concepts
- **Embeddings**: Numerical representations of data (text, images, etc.)
- **Similarity Search**: Finding vectors close in high-dimensional space
- **Indexing**: ANN (Approximate Nearest Neighbor) algorithms for speed

## How It Works
1. Convert data to vectors using ML models (e.g., sentence embeddings)
2. Store vectors with metadata in specialized database
3. Query with vector, database finds similar vectors using distance metrics
4. Return ranked results based on similarity

[... rest of structured research ...]

## Next Steps
For your use case (semantic search in documentation):
1. Consider Weaviate (open source, good docs)
2. Start with small dataset (<10k documents)
3. Use OpenAI embeddings or sentence-transformers

Need deeper dive? Try: /knowledge-builder
```

### Example 2: Debugging Unknown Error

```
User: "Getting error: 'ECONNREFUSED' in Node.js, what does this mean?"

Research Skill:
*Quick search for Node.js ECONNREFUSED*

## Overview
ECONNREFUSED means your Node.js application tried to connect to
a server/service, but the connection was actively refused (nothing
is listening on that port).

## Common Causes
1. **Service not running**: Database, Redis, API server not started
2. **Wrong port**: Connecting to 6379 but Redis is on 6380
3. **Firewall**: Port blocked by firewall rules
4. **Wrong host**: Using localhost but service is remote

## How to Debug
1. Check if service is running: `ps aux | grep [service]`
2. Verify port: `netstat -an | grep [port]`
3. Check connection string in environment variables
4. Try telnet: `telnet localhost [port]`

## Quick Fix
Most likely: Start the service you're trying to connect to
(e.g., `redis-server`, `mongod`, etc.)

This is a quick diagnosis. Need help debugging further?
```

### Example 3: Architecture Research

```
User: "Should I use REST or GraphQL for my API?"

Research Skill:
*Researches current state of REST vs GraphQL*

## Overview
REST and GraphQL are different API paradigms with distinct tradeoffs.
Choice depends on your use case, team, and clients.

## REST Strengths
- Simple, well-understood
- Great HTTP caching
- Easy to debug (curl, browser)
- Smaller payload for simple queries

## GraphQL Strengths
- Single endpoint, flexible queries
- Reduces over/under-fetching
- Strong typing and introspection
- Great for complex, interconnected data

## Decision Framework
Use REST when:
- Simple CRUD operations
- Clear resource boundaries
- HTTP caching important
- Team unfamiliar with GraphQL

Use GraphQL when:
- Complex, nested data requirements
- Multiple client types (web, mobile, etc.)
- Clients need flexibility
- Rapid frontend iteration

[... more research ...]

This is a complex architectural decision. Would you like me to:
1. Activate "Architecting Solutions" skill for deeper analysis?
2. Use /ultrathink for comprehensive tradeoff evaluation?
```

## Output Guidelines

### Keep It Actionable

- Focus on what user needs to know
- Provide clear next steps
- Avoid information overload

### Structure for Scanning

- Use headers and bullets
- Highlight key points in bold
- Keep paragraphs short (2-3 sentences)

### Context Matters

- Relate to user's project/situation
- Note when general advice doesn't apply
- Highlight relevant specific details

### Be Honest About Limits

- Flag when information is unclear
- Note when sources conflict
- Admit when deeper research is needed

## Common Research Patterns

### New Technology

1. What problem does it solve?
2. How does it compare to alternatives?
3. Is it mature/production-ready?
4. What's the learning curve?
5. Community and ecosystem health?

### Library/Framework Choice

1. Feature comparison
2. Performance characteristics
3. Community size and activity
4. Documentation quality
5. Breaking change history

### Best Practices

1. Official recommendations
2. Community consensus
3. Anti-patterns to avoid
4. Context dependencies
5. Evolution over time

### Debugging/Troubleshooting

1. What does error mean?
2. Common causes
3. Diagnostic steps
4. Quick fixes
5. When to escalate

## Quality Checklist

Before presenting research:

- [ ] Information is current (check dates)
- [ ] Multiple sources consulted
- [ ] Conflicting views noted
- [ ] Relevant to user's context
- [ ] Actionable next steps provided
- [ ] Appropriate depth for time invested
- [ ] Escalation path offered if needed
- [ ] Sources referenced for deeper reading

## Anti-Patterns to Avoid

- **Wikipedia Dump**: Don't just summarize without synthesis
- **Source Copying**: Synthesize, don't plagiarize
- **Outdated Info**: Check recency, especially for fast-moving tech
- **Overconfidence**: Flag uncertainty and conflicting sources
- **Scope Creep**: Stay focused on user's question
- **Missing Context**: Connect to user's specific situation

## Success Criteria

Good research provides:

- Quick understanding of core concepts
- Actionable insights for user's situation
- Clear next steps
- Confidence to proceed or path to deeper learning
- Time saved vs. user searching independently

## Related Capabilities

- **Slash Command**: `/knowledge-builder` for comprehensive deep research
- **Skill**: "Explaining Concepts" for teaching/learning focus
- **Skill**: "Architecting Solutions" for applying research to design
- **Slash Command**: `/ultrathink` for research-based decision making

---

Remember: The goal is rapid, relevant insight that accelerates user progress. Quick research beats perfect research that arrives too late.
