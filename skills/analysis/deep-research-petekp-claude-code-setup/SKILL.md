---
name: deep-research
description: |
  Conduct exhaustive, citation-rich research on any topic using all available tools: web search, browser automation, documentation APIs, and codebase exploration. Use when asked to "research X", "find out about Y", "investigate Z", "deep dive into...", "what's the current state of...", "compare options for...", "fact-check this...", or any request requiring comprehensive, accurate information from multiple sources. Prioritizes accuracy over speed, cross-references claims across sources, identifies conflicts, and provides full citations. Outputs structured findings with confidence levels and source quality assessments.
---

# Deep Research

Systematic methodology for conducting exhaustive, accurate research using all available tools. Prioritizes correctness over speed.

## Core Principles

1. **Multiple sources required** — Never rely on a single source for important claims
2. **Cross-reference everything** — Verify facts appear consistently across independent sources
3. **Citation mandatory** — Every claim must have a source; no unsourced assertions
4. **Acknowledge uncertainty** — When sources conflict or are weak, say so explicitly
5. **Prefer primary sources** — Official docs > blog posts > forum answers > AI-generated content

## Available Research Tools

Use these tools in combination based on the research topic:

| Tool | Best For | Limitations |
|------|----------|-------------|
| **WebSearch** | Current events, recent information, broad topic discovery | Results may be outdated, SEO-influenced |
| **WebFetch** | Reading specific URLs, extracting detailed content | Requires known URL |
| **Playwright browser** | Interactive sites, paywalled content (if logged in), complex navigation | Slower, requires more tokens |
| **Context7/MCP docs** | Library/framework documentation | Only indexed libraries |
| **OpenAI docs MCP** | OpenAI API specifics | OpenAI only |
| **Grep/Glob/Read** | Codebase research, finding implementations | Local files only |

## Research Workflow

### Phase 1: Scope Definition

Before researching, clarify:

1. **Core question** — What specific question(s) need answering?
2. **Required depth** — Surface overview or exhaustive deep-dive?
3. **Recency requirements** — Is timeliness critical? (API versions, current events, etc.)
4. **Authoritative sources** — What would count as a definitive answer?

Ask clarifying questions if scope is ambiguous. Use AskUserQuestion for structured choices when multiple research directions are possible.

### Phase 2: Source Discovery

Cast a wide net to find relevant sources:

```
1. WebSearch with multiple query variations
   - Try 3-5 different phrasings of the core question
   - Include technical terms AND plain language
   - Search for "[topic] official documentation"
   - Search for "[topic] research paper" or "[topic] study"

2. Identify authoritative sources from results
   - Official documentation sites
   - Academic papers / research institutions
   - Industry standards bodies
   - Recognized experts in the field

3. Check specialized tools
   - Context7 for library/framework docs
   - OpenAI docs MCP for OpenAI-specific topics
   - GitHub/codebase for implementation details
```

**Source discovery heuristics:**
- Government and academic domains (.gov, .edu, .ac.uk) tend toward accuracy
- Official project documentation is authoritative for that project
- Wikipedia is a starting point, not an endpoint — follow its citations
- Stack Overflow answers need verification; check votes and dates
- Be skeptical of content farms and SEO-optimized listicles

### Phase 3: Deep Reading

For each promising source:

1. **Fetch full content** — Use WebFetch or browser to get complete text
2. **Extract key claims** — Note specific facts, figures, dates, quotes
3. **Note source metadata** — Author, date, organization, potential biases
4. **Identify citations** — What sources does this source cite?
5. **Flag conflicts** — Does this contradict other sources?

**Reading strategy for different source types:**

| Source Type | Strategy |
|-------------|----------|
| Documentation | Read relevant sections fully; note version/date |
| Research paper | Abstract, conclusion, methodology in that order |
| News article | Check publication date, author credentials, cited sources |
| Blog post | Verify claims independently; note author's expertise |
| Forum/Q&A | Check answer date, votes, accepted status; verify independently |

### Phase 4: Cross-Verification

For each major claim:

1. **Find 2+ independent sources** — Sources that don't cite each other
2. **Check for conflicts** — Note any disagreements between sources
3. **Prefer newer sources** — For rapidly evolving topics
4. **Weight by authority** — Primary sources > secondary > tertiary

**Conflict resolution:**
- When sources disagree, report all positions with citations
- Investigate why they disagree (different contexts, outdated info, different definitions)
- If one source is clearly more authoritative, note that
- Never silently pick one version

### Phase 5: Synthesis & Output

Structure findings clearly:

```markdown
## Research Summary: [Topic]

### Key Findings

1. **[Finding 1]**
   - [Specific fact with citation]
   - [Supporting evidence]
   - Confidence: High/Medium/Low
   - Sources: [1], [2]

2. **[Finding 2]**
   ...

### Conflicts & Uncertainties

- [Area of disagreement]: Source A claims X [1], while Source B claims Y [2]. [Analysis of why they differ]

### Source Quality Assessment

| # | Source | Type | Authority | Recency | Notes |
|---|--------|------|-----------|---------|-------|
| 1 | [URL] | Official docs | High | 2024-01 | Primary source |
| 2 | [URL] | Research paper | High | 2023-06 | Peer-reviewed |
| 3 | [URL] | Blog | Medium | 2024-03 | Author is [expert] |

### Gaps & Limitations

- [What couldn't be verified]
- [Areas needing more research]

### Citations

[1] [Full citation with URL]
[2] [Full citation with URL]
...
```

## Confidence Levels

Assign confidence to each finding:

| Level | Criteria |
|-------|----------|
| **High** | 3+ independent authoritative sources agree; no conflicts |
| **Medium** | 2 sources agree, or 1 highly authoritative source; minor conflicts |
| **Low** | Single source, or significant conflicts between sources |
| **Uncertain** | Sources conflict significantly; unable to determine truth |

Always state confidence explicitly. "I'm not sure" is a valid research finding.

## Citation Format

Use inline citations with numbered references:

```markdown
The API rate limit is 60 requests per minute [1], though this can be increased
for enterprise accounts [2].

---
[1] OpenAI API Documentation, "Rate Limits", https://platform.openai.com/docs/guides/rate-limits, accessed 2024-01-15
[2] OpenAI Enterprise FAQ, https://openai.com/enterprise, accessed 2024-01-15
```

**Citation must include:**
- Source name/title
- URL (if web source)
- Access date (for web sources)
- Publication date (if available)

## Special Research Scenarios

### Rapidly Evolving Topics (AI, crypto, etc.)

- Prioritize sources from last 6 months
- Check official changelogs and release notes
- Note when information might be outdated
- Consider using browser to check current state directly

### Controversial Topics

- Present multiple perspectives with citations for each
- Identify the strongest arguments on each side
- Note which sources might have biases and why
- Don't pick sides unless evidence is overwhelming

### Technical Implementation Questions

- Check official documentation first (Context7, MCP servers)
- Look for example code in GitHub
- Verify against actual behavior if possible
- Note version-specific differences

### Comparative Research ("X vs Y")

- Use same evaluation criteria for all options
- Find sources that compare directly when possible
- Check for bias (vendor-sponsored comparisons)
- Note what each option is optimized for

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Instead |
|--------------|--------------|---------|
| Single source | No verification | Always find 2+ sources |
| Uncited claims | Unverifiable | Every fact needs a source |
| Assuming first result is best | SEO != accuracy | Evaluate source quality |
| Ignoring conflicts | Hides uncertainty | Report all positions |
| Outdated sources | Information decay | Check publication dates |
| Trusting AI summaries | May hallucinate | Go to primary sources |
| Stopping early | Incomplete picture | Research until diminishing returns |

## Completion Criteria

Research is complete when:

1. Core question(s) answered with citations
2. Key claims verified by 2+ independent sources
3. Conflicts and uncertainties explicitly noted
4. Source quality assessed for all citations
5. Confidence levels assigned to findings
6. Gaps and limitations documented

## Reference Files

For detailed guidance on specific scenarios:

- [Source Evaluation Criteria](references/source-evaluation.md) — How to assess source reliability
- [Search Strategies](references/search-strategies.md) — Advanced query techniques for different domains
