---
name: Deep Research
description: Comprehensive web research with synthesis and actionable insights
triggers:
  - "research"
  - "deep research"
  - "investigate"
  - "find information about"
  - "best practices for"
---

# Deep Research Skill

Perform thorough research using web search, documentation, and intelligent synthesis to inform development decisions.

## Capabilities

- Web search via WebSearch tool
- Documentation analysis
- Technology trend research
- Competitive analysis
- Best practices discovery
- Academic/technical paper review

## Research Methodology

### Phase 1: Broad Search (10-15 sources)
- Query multiple search engines
- Scan for credibility (check date, author, domain)
- Filter by relevance score
- Prioritize official docs, established blogs, GitHub repos

### Phase 2: Deep Dive (Top 5 sources)
- Read thoroughly
- Extract key insights
- Identify patterns and trends
- Note contradictions or debates
- Look for code examples and real-world applications

### Phase 3: Synthesis
- Combine findings into cohesive narrative
- Create actionable recommendations
- Document all sources
- Generate summary report

## Output Format

Research saved to: `temp/research/{topic}-{timestamp}.md`

```markdown
# Research: {Topic}

## Executive Summary
[3-5 bullet points - key findings]

## Key Findings

### 1. {Finding Title}
- **Source**: [Link](url)
- **Insight**: What was learned
- **Actionable**: How to apply this
- **Code Example**: (if applicable)

### 2. {Finding Title}
...

## Recommendations
1. **Immediate Action**: What to do now
2. **Best Practice**: Pattern to follow
3. **Avoid**: What not to do

## Implementation Plan
- [ ] Step 1
- [ ] Step 2

## Sources
- [Title](URL) - Brief description
- [Title](URL) - Brief description
```

## Usage Examples

### Technology Research
```bash
"deep research on LangGraph supervisor pattern for production systems
 Focus on: state management, error handling, scalability
 Save to: temp/research/langgraph-supervisor.md"
```

### Competitive Analysis
```bash
"research competitors in AI code generation space
 Analyze: features, pricing, tech stack, user feedback
 Identify: gaps we can fill, unique angles
 Output: temp/research/competitive-analysis.md"
```

### Best Practices
```bash
"research React Server Components best practices for Next.js 14
 Include: when to use vs client components, data fetching patterns, common pitfalls
 Find: code examples from Vercel and community
 Save: temp/research/rsc-best-practices.md"
```

## Integration with Build Process

Research findings automatically:
1. **Update Learning**: Add insights to `directives/learning.json`
2. **Create Specs**: If features found → add to backlog
3. **Improve Docs**: Suggest updates to INSTRUCTIONS.md
4. **Inform Architecture**: Use findings in technical decisions

## Research Quality Checklist

Before completing research:
- [ ] At least 5 credible sources
- [ ] Checked for recency (prefer <1 year old info)
- [ ] Included official documentation
- [ ] Found real-world examples/code
- [ ] Synthesized conflicting information
- [ ] Created actionable recommendations
- [ ] Documented all sources with working links

## Advanced Research Patterns

### Comparative Research
```bash
"research and compare:
 Option A: Using Prisma ORM
 Option B: Using raw SQL with Postgres
 Option C: Using Drizzle ORM

 Compare: performance, DX, type safety, migrations, community support
 Recommend: Best option for Next.js 14 + Supabase stack"
```

### Trend Analysis
```bash
"research current trends in AI agent orchestration frameworks
 Analyze: LangGraph, CrewAI, AutoGPT, LangChain, Semantic Kernel
 Identify: Which is gaining traction, production-ready, best for SaaS
 Timeline: Last 6 months only"
```

---

**Remember**: Great research leads to better decisions. Invest time in deep research before implementation!
