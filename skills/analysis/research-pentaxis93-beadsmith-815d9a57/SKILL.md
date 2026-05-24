# Research Skill

> Version: 1.0.0
> Compiler: manual (bootstrap)
> Last Updated: 2026-01-22

Systematic methodology for conducting comprehensive, multi-source research with citations and synthesis.

## When to Activate

Use this skill when:
- User asks to "research", "investigate", "find out about", or "analyze" a topic
- Task requires gathering information from multiple sources
- Output needs citations or evidence-based conclusions
- Comprehensive analysis across perspectives is required
- Fact-checking or verification is needed

## Core Principles

### 1. Start Simple, Add Complexity When Needed
Begin with focused searches before expanding scope. Complex multi-agent research is only warranted when simpler approaches fail to produce adequate results.

### 2. Context Engineering is Critical
The quality of research depends on providing the right information, in the right format, at the right time. Structure queries precisely and validate sources systematically.

### 3. Three-Source Rule
Never trust a single source. Cross-reference with at least two independent sources before treating information as reliable.

### 4. Version Everything
Most source conflicts dissolve when versions/dates are explicit. Always anchor findings to specific versions and timestamps.

### 5. Empirical Verification Over Authority
When stakes are high, test claims directly rather than trusting even authoritative sources. Code behavior beats documentation.

---

## Research Workflow

### Phase 1: Clarification

Before researching, clarify the query:

1. **Identify the core question**: What specifically needs to be answered?
2. **Determine scope**: Breadth vs depth? Historical context needed?
3. **Specify output format**: Report, comparison table, decision recommendation?
4. **Note constraints**: Time period, specific technologies, geographic scope?

If the query is vague, ask clarifying questions before proceeding.

### Phase 2: Query Decomposition

Break the research question into 3-5 specific sub-questions that together form a complete picture:

```
Main: "Should we use PostgreSQL or MongoDB for this project?"

Sub-questions:
1. What are the data modeling requirements? (structured vs flexible)
2. What are the scaling requirements? (read-heavy, write-heavy, both)
3. What's the team's existing expertise?
4. What are the operational complexity tradeoffs?
5. What do production users of similar scale report?
```

### Phase 3: Source Gathering

Consult sources in this priority order, adapting to the domain:

| Source Type | Strengths | Best For |
|-------------|-----------|----------|
| **Official Docs** | Authoritative, maintained | API signatures, core concepts |
| **GitHub Issues/PRs** | Real problems, maintainer input | Edge cases, bugs, workarounds |
| **Stack Overflow** | Curated answers, voting signal | Common problems, quick fixes |
| **Source Code** | Ground truth | When docs are unclear |
| **Blog Posts** | Deep dives, tutorials | Learning workflows, context |
| **Discord/Forums** | Cutting-edge, insider knowledge | Latest changes, community consensus |

**For each source, record:**
- URL and access date
- Version/date of the information
- Author credibility indicators
- Key claims with direct quotes when significant

### Phase 4: Source Evaluation

Score each source (mentally or explicitly) on:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Relevance** | Does it directly address the question? | High |
| **Credibility** | Author expertise? Peer review? Maintainer? | High |
| **Currency** | How recent? Still applicable? | Medium-High |
| **Specificity** | Contains concrete data, examples, code? | Medium |
| **Consensus** | Does it align with other sources? | Medium |

**Trust hierarchy (highest to lowest):**
1. Source code behavior (empirical test)
2. Official docs with version tags
3. Maintainer statements in issues/PRs
4. Highly upvoted + recently active Stack Overflow
5. Blog posts with working code examples
6. Unverified forum posts

**Red flags:**
- No version/date mentioned
- Code examples without imports
- "This worked for me" with no context
- Confidently stated but lacks detail
- Circular references between sources

### Phase 5: Conflict Resolution

When sources disagree:

1. **Check versions**: Conflict often means different versions, not factual disagreement
2. **Find the maintainer**: Their comment trumps community answers
3. **Test empirically**: Run the code if possible
4. **Apply consensus weighting**: 5 sources saying X vs 1 saying Y → lean X, but investigate Y
5. **Note the disagreement**: If unresolved, report both positions with evidence

### Phase 6: Synthesis

Structure your synthesis:

1. **Executive Summary**: 1-2 paragraphs answering the core question directly
2. **Evidence Review**: Key findings organized by sub-question
3. **Conflicting Perspectives**: Where sources disagree and why
4. **Concrete Conclusion**: Clear, evidence-based recommendation (avoid hedge words)
5. **Caveats and Limitations**: What wasn't covered, what might change
6. **References**: All sources with URLs and access dates

**Quality standards:**
- Every factual claim has a citation
- Quantitative data preferred over qualitative assertions
- Multiple perspectives on controversial topics
- Conclusions are specific, not vague generalizations

---

## Capturing Practical Wisdom

Official docs miss the "clever hacks" and "power user moves." Find them by:

### Search Patterns

```
# GitHub issue archaeology
"workaround" OR "hack" OR "trick" site:github.com/[repo]/issues
"finally figured out" site:github.com
"for anyone else" [technology]

# Stack Overflow comment mining
[technology] [problem] "note that" OR "also need to"

# Dotfile diving
[tool] dotfiles github
awesome-[tool]

# Conference talk wisdom
[technology] conference talk transcript
```

### Emotional Language Signals

Hard-won knowledge often comes with emotional markers:
- "Finally!"
- "After hours of debugging..."
- "The trick is..."
- "What the docs don't tell you..."
- "I wish I knew this earlier..."

When you find such knowledge, preserve context:
```
## [Problem]
**Source**: [URL] ([date])
**Version**: [when this worked]
**The trick**: [solution]
**Why**: [explanation if known]
**Caveats**: [when this might break]
```

---

## Prompt Templates

### For Query Decomposition

```
Break down this research question into 3-5 specific sub-questions 
that together provide a complete answer:

Question: [QUESTION]

Requirements:
- Sub-questions should be independently answerable
- Cover different aspects (technical, practical, tradeoffs)
- Be specific enough to search for directly
```

### For Source Summarization

```
Summarize this content for the research question: "[QUESTION]"

Include:
- Key facts and statistics (with direct quotes for significant claims)
- Author/source credibility indicators
- Version/date applicability
- Relevance assessment (high/medium/low)

If content doesn't address the question, state that briefly and note 
any tangentially useful information.
```

### For Synthesis

```
Using the gathered information, synthesize a response to: "[QUESTION]"

Structure:
1. Direct answer (1-2 sentences)
2. Key evidence supporting the answer
3. Important caveats or exceptions
4. Confidence level (high/medium/low) with reasoning

Requirements:
- Cite sources inline: ([Source](url))
- Prefer concrete data over generalizations
- Acknowledge uncertainty explicitly
- State your conclusion clearly—don't hedge
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Single-source answers** | No verification | Cross-reference 3+ sources |
| **Skipping clarification** | Vague query → poor results | Ask questions first |
| **Trusting first results** | Confirmation bias | Seek disconfirming evidence |
| **Copy-paste without understanding** | Cargo culting | Understand the "why" |
| **Ignoring version/date** | Outdated info applied incorrectly | Always note versions |
| **Vague conclusions** | "It depends" helps no one | Make a specific recommendation |
| **Hiding uncertainty** | Overconfidence misleads | State confidence levels |

---

## Quality Checklist

Before concluding research:

- [ ] Core question answered directly and specifically
- [ ] 3+ diverse sources consulted
- [ ] All factual claims have citations
- [ ] Version/date noted for time-sensitive information
- [ ] Conflicting sources investigated and explained
- [ ] Quantitative data included where available
- [ ] Practical wisdom captured (not just official docs)
- [ ] Conclusion is concrete, not hedged
- [ ] Limitations and caveats acknowledged

---

## Example Application

**Query**: "How should we handle authentication in our new FastAPI application?"

**Phase 1 - Clarification**:
- Scope: REST API, not WebSocket
- Users: Internal service-to-service initially, public API later
- Constraints: Must integrate with existing OAuth2 provider

**Phase 2 - Decomposition**:
1. What authentication methods does FastAPI natively support?
2. What's the recommended approach for OAuth2 integration?
3. What are common pitfalls in FastAPI auth implementations?
4. How do production FastAPI apps handle this at scale?

**Phase 3-4 - Research**:
- Official FastAPI security docs (v0.109): OAuth2 with JWT, multiple security schemes
- GitHub issue #1234: Common mistake with dependency injection order
- Blog: "FastAPI Auth in Production at Company X" - Token refresh patterns
- Stack Overflow (maintainer answer): Security best practices

**Phase 5 - Synthesis**:
"Use FastAPI's built-in `OAuth2PasswordBearer` with JWT tokens. Implement token refresh following the pattern in [FastAPI docs](url). Key pitfall: dependency injection order matters—security dependencies must be defined before routes that use them ([GitHub #1234](url)). At scale, consider Redis for token blacklisting ([Company X blog](url))."

---

## References

This skill synthesizes research methodology from:
- Anthropic: "Building Effective Agents" (2024)
- OpenAI: Agents Guide, Deep Research documentation
- LangChain: RAG and Context Engineering docs
- GPT-Researcher: Research agent implementation patterns
- Academic: Plan-and-Solve (arXiv:2305.04091), RAG (arXiv:2005.11401)
