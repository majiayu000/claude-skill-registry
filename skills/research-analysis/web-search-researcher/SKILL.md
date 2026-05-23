---
name: web-search-researcher
description: Research topics using web search and content fetching to find accurate, current information. Use when you need modern information, official documentation, best practices, technical solutions, or comparisons beyond your training data. Provides systematic web research with strategic searches, content analysis, and synthesized findings.
---

# Web Search Research

Expert web research specialist skill for finding accurate, relevant information from web sources using WebSearch and WebFetch tools.

## When to Use

Use this skill when you need to:
- Find modern information not in your training data
- Locate official documentation for APIs, libraries, or frameworks
- Research best practices and current recommendations
- Discover technical solutions to specific problems
- Compare technologies, approaches, or tools
- Verify version-specific information or recent changes
- Investigate emerging trends or recent developments

## Date Context Awareness

**CRITICAL**: Always check your environment context (`<env>`) for the current date before starting research.

**Why this matters**:
- Ensures searches use current year for recent information
- Helps evaluate source freshness and relevance
- Prevents relying on outdated best practices
- Improves search result quality

**How to use**:
1. Check `<env>` tag for "Today's date: YYYY-MM-DD"
2. Extract current year (e.g., 2025)
3. Include current year in searches for best practices, frameworks, or evolving technologies
4. Use current date to evaluate publication freshness (within 12-18 months = recent)

## Core Responsibilities

When conducting web research, you will:

### 1. Analyze the Query

Break down the user's request to identify:
- Key search terms and concepts
- Types of sources likely to have answers (documentation, blogs, forums, academic papers)
- Multiple search angles to ensure comprehensive coverage

### 2. Execute Strategic Searches

- Start with broad searches to understand the landscape
- Refine with specific technical terms and phrases
- Use multiple search variations to capture different perspectives
- Include site-specific searches when targeting known authoritative sources (e.g., "site:docs.stripe.com webhook signature")

### 3. Fetch and Analyze Content

- Use WebFetch to retrieve full content from promising search results
- Prioritize official documentation, reputable technical blogs, and authoritative sources
- Extract specific quotes and sections relevant to the query
- Note publication dates to ensure currency of information

### 4. Synthesize Findings

- Organize information by relevance and authority
- Include exact quotes with proper attribution
- Provide direct links to sources
- Highlight any conflicting information or version-specific details
- Note any gaps in available information

## Search Strategies

### For API/Library Documentation

- Search for official docs first: "[library name] official documentation [specific feature]"
- Look for changelog or release notes for version-specific information
- Find code examples in official repositories or trusted tutorials

**Example Search**:
```
"Stripe webhook signature verification" official documentation
site:stripe.com webhook signature validation
```

### For Best Practices

- Search for recent articles (**always include current year from environment context**)
- Look for content from recognized experts or organizations
- Cross-reference multiple sources to identify consensus
- Search for both "best practices" and "anti-patterns" to get full picture

**Example Search** (replace [CURRENT_YEAR] with year from environment):
```
"Rust async best practices" [CURRENT_YEAR]
"Tokio performance anti-patterns" [CURRENT_YEAR]
```

### For Technical Solutions

- Use specific error messages or technical terms in quotes
- Search Stack Overflow and technical forums for real-world solutions
- Look for GitHub issues and discussions in relevant repositories
- Find blog posts describing similar implementations

**Example Search**:
```
"tokio runtime panic" redb write transaction
site:github.com tokio blocking write transaction
```

### For Comparisons

- Search for "X vs Y" comparisons
- Look for migration guides between technologies
- Find benchmarks and performance comparisons
- Search for decision matrices or evaluation criteria

**Example Search**:
```
"redb vs sled" performance comparison
"SQLite vs Turso" migration guide
```

## Search Efficiency

### Progressive Search Strategy

Don't over-search initially. Use this progressive approach:

#### Round 1: Oriented Search (5 minutes)
**Goal**: Understand the landscape

- Run 1-2 broad searches
- Quickly scan result titles and snippets
- Identify: Is this well-documented? Common? Novel?
- **Decision**: If official docs found → Fetch and possibly stop. Otherwise → Round 2

#### Round 2: Targeted Search (10 minutes)
**Goal**: Find authoritative sources

- Run 2-3 specific searches with refined terms
- Use site-specific searches for known authorities
- Fetch 2-3 most promising sources
- **Decision**: If sufficient consensus → Synthesize and stop. Otherwise → Round 3

#### Round 3: Deep Dive (15 minutes)
**Goal**: Fill gaps and resolve conflicts

- Search for specific missing information
- Look for alternative perspectives
- Find production examples or case studies
- Fetch 2-4 additional sources
- **Decision**: Synthesize findings regardless of gaps. Note limitations.

#### Round 4: Extended Research (optional, 20+ minutes)
**Goal**: Only for critical decisions or persistent gaps

- Search academic sources, security advisories, archived discussions
- Look for expert interviews or conference presentations
- Find comparative analyses
- **Requirement**: Must justify why Rounds 1-3 were insufficient

**Efficiency Tip**: Most research should complete in Round 2. Only 20% of tasks justify Round 3, and <5% justify Round 4.

### Quick Result Evaluation

Before fetching content, rapidly triage search results using this priority matrix:

#### Priority 1 (Fetch First) ⭐⭐⭐
- Official documentation from library/framework maintainers
- GitHub issues/PRs from project maintainers
- Production case studies from reputable companies
- Recent posts (within current year or last 12 months) from recognized experts

**Indicators**: URLs contain official domains, author is maintainer/core contributor, recent date visible in snippet

#### Priority 2 (Fetch If Needed) ⭐⭐
- Technical blog posts from known experts
- Stack Overflow answers with high votes (>50) and recent activity
- Conference talks/presentations from domain experts
- Tutorial sites with technical depth

**Indicators**: Author credentials visible, multiple upvotes/endorsements, specific technical details in snippet

#### Priority 3 (Skip Unless Desperate) ⭐
- Generic tutorials without author credentials
- Old posts (>3 years) without recent updates
- Forum discussions without resolution
- Marketing/promotional content

**Indicators**: No author info, old dates, vague descriptions, commercial bias

#### Red Flags (Never Fetch) 🚫
- AI-generated content farms
- Duplicate content aggregators
- Paywalled content without abstracts
- Sources contradicting official docs without justification

**Triage Time Budget**: Spend 30-60 seconds per search result page reviewing titles, URLs, snippets, and dates before fetching.

### Search Operators

Use search operators effectively:
- **Quotes** for exact phrases: `"exact phrase"`
- **Minus** for exclusions: `rust -game`
- **site:** for specific domains: `site:docs.rs`
- **OR** for alternatives: `tokio OR async-std`

Consider searching in different forms: tutorials, documentation, Q&A sites, and discussion forums

## Output Format

Structure your findings as:

```markdown
## Summary
[Brief overview of key findings - 2-3 sentences]

## Detailed Findings

### [Topic/Source 1]
**Source**: [Name with link]
**Relevance**: [Why this source is authoritative/useful]
**Key Information**:
- Direct quote or finding (with link to specific section if possible)
- Another relevant point

### [Topic/Source 2]
**Source**: [Name with link]
**Relevance**: [Why this source is authoritative/useful]
**Key Information**:
- Finding 1
- Finding 2

## Additional Resources
- [Relevant link 1] - Brief description
- [Relevant link 2] - Brief description

## Gaps or Limitations
[Note any information that couldn't be found or requires further investigation]
```

## Quality Guidelines

### Accuracy
- Always quote sources accurately and provide direct links
- Include specific section links when possible
- Preserve technical terminology exactly as written

### Relevance
- Focus on information that directly addresses the user's query
- Filter out tangential or outdated information
- Prioritize actionable insights

### Currency
- **Always check environment context (`<env>`) for current date before evaluating freshness**
- Note publication dates and version information when relevant
- For fast-moving tech: prioritize sources from current year
- For stable tech: sources 2-3 years old may still be valid
- Indicate if information may be outdated relative to current date
- Look for recent updates or newer alternatives

### Authority
- Prioritize official sources, recognized experts, and peer-reviewed content
- Note the credibility of each source
- Be skeptical of unverified claims

### Completeness
- Search from multiple angles to ensure comprehensive coverage
- Don't stop at the first result - validate with multiple sources
- Identify consensus vs. outlier opinions

### Transparency
- Clearly indicate when information is outdated, conflicting, or uncertain
- Acknowledge gaps in available information
- Distinguish between official guidance and community opinions

## Research Depth Levels

Choose the appropriate research depth based on task criticality and time constraints:

### Quick Research (15-20 minutes)
**Use for**: Simple questions, checking current syntax, verifying basic facts

**Process**:
- 1-2 targeted searches
- Fetch 1-2 most authoritative sources (official docs preferred)
- Extract specific answer
- Skip deep synthesis

**Example**: "What's the signature for Stripe webhook verification?"

### Standard Research (30-45 minutes)
**Use for**: Technical decisions, best practices, understanding approaches

**Process**:
- 2-3 strategic searches (broad + specific)
- Fetch 3-5 high-quality sources
- Cross-reference for consensus
- Structured synthesis with template

**Example**: "Best practices for redb + Tokio integration"

### Deep Research (60-90 minutes)
**Use for**: Architecture decisions, comparing multiple solutions, critical systems

**Process**:
- 4-6 multi-angle searches
- Fetch 6-10 sources (mix of official docs, case studies, expert opinions)
- Compare trade-offs and alternatives
- Comprehensive synthesis with decision matrix
- Follow-up searches to fill gaps

**Example**: "Should we use redb vs sled vs SQLite for our memory system?"

### Exhaustive Research (2+ hours)
**Use for**: Mission-critical decisions, novel problem domains, security-sensitive choices

**Process**:
- Multiple search sessions over time
- 10+ authoritative sources
- Include academic papers, security advisories, production incident reports
- Build comprehensive knowledge base
- Validate with experts if possible

**Example**: "Design distributed consensus system for multi-region deployment"

**Rule**: Set a timer. When time expires, synthesize what you have and note gaps rather than continuing indefinitely.

## Research Workflow

### Step 0: Determine Research Depth

Before starting, decide which depth level (Quick/Standard/Deep/Exhaustive) is appropriate based on:
- Task criticality
- Decision impact
- Time constraints
- Information availability

### Step 1: Plan Searches
```markdown
Query: [User's question]
Key concepts: [List main terms]
Search variations:
1. [Broad search]
2. [Specific technical search]
3. [Site-specific search]
```

### Step 2: Execute Searches
- Run 2-3 initial searches
- Review search results for promising sources
- Identify authoritative and relevant URLs

### Step 3: Fetch Content
- Use WebFetch on 3-5 most promising URLs
- Extract relevant information
- Note publication dates and context

### Step 4: Synthesize
- Organize findings by theme/topic
- Identify consensus and conflicts
- Structure using output format template

### Step 4.5: Evaluate Stopping Criteria

Recognize these signals that you have sufficient information:

#### Positive Indicators (Stop Here) ✅
1. **Consensus Found**: 3+ authoritative sources agree on the approach
2. **Official Guidance Located**: Found maintainer recommendations or official docs
3. **Production Validation**: Found real-world implementations with similar constraints
4. **Actionable Path**: Have clear next steps and implementation guidance
5. **Trade-offs Understood**: Understand pros/cons of main approaches
6. **Time Limit Reached**: Hit your time-box limit with adequate information

#### Warning Signs (Keep Searching) ⚠️
1. **Conflicting Information**: Sources strongly disagree without version/context explanation
2. **Outdated Only**: All sources are >2 years old for fast-moving tech
3. **No Official Source**: Haven't found maintainer or official documentation
4. **Unclear Actionability**: Can't determine specific next steps
5. **Missing Context**: Don't understand why recommendations exist

#### Diminishing Returns (Stop Soon) 📉
- New sources repeat information already found
- Spending >10 minutes without finding new insights
- Found 8+ sources that all say roughly the same thing
- Searches returning increasingly tangential results

**Decision Rule**: If you've reached time-box limit AND have positive indicators, stop. If critical gaps remain, extend time-box by 50% maximum, then stop regardless.

### Step 5: Report
- Present findings clearly
- Provide actionable insights
- Note any limitations or gaps

## Examples

### Example 1: API Documentation Research

**Query**: "How do I verify webhook signatures in Stripe?"

**Search Strategy**:
1. `"Stripe webhook signature verification" official documentation`
2. `site:stripe.com webhook endpoints security`
3. `"Stripe webhook" signature example code`

**Expected Output**:
- Link to official Stripe webhook security docs
- Code examples for signature verification
- Common pitfalls and best practices
- Version-specific considerations

### Example 2: Best Practices Research

**Query**: "What are the best practices for async Rust error handling?"

**Pre-search**: Check environment context - current year is [CURRENT_YEAR]

**Search Strategy**:
1. `"Rust async error handling" best practices [CURRENT_YEAR]`
2. `"Tokio error handling" patterns [CURRENT_YEAR]`
3. `site:blog.rust-lang.org async errors`
4. `"anyhow vs thiserror" async context`

**Expected Output**:
- Official Rust async book recommendations
- Expert blog posts from recognized Rust developers
- Comparison of error handling libraries
- Real-world examples and patterns

### Example 3: Technical Problem Solving

**Query**: "Why is my Tokio runtime blocking on redb writes?"

**Search Strategy**:
1. `"tokio blocking" redb write transaction`
2. `site:github.com tokio spawn_blocking database`
3. `"redb" async tokio integration`
4. `"database write blocking async runtime"`

**Expected Output**:
- Explanation of blocking operations in async runtimes
- Solutions using spawn_blocking
- GitHub issues with similar problems
- Performance considerations

## Integration with Other Skills

- **episode-start**: Use web research to gather context before starting episodes
- **feature-implement**: Research API documentation and best practices before implementation
- **debug-troubleshoot**: Search for similar error patterns and solutions
- **architecture-validation**: Research architectural patterns and trade-offs

## Best Practices

### DO:
- ✓ Check environment context for current date before starting
- ✓ Use current year in searches for best practices and evolving tech
- ✓ Use specific, technical search terms
- ✓ Include version numbers when relevant
- ✓ Search official documentation first
- ✓ Cross-reference multiple sources
- ✓ Note publication dates relative to current date
- ✓ Provide direct links
- ✓ Quote sources accurately
- ✓ Indicate source authority

### DON'T:
- ✗ Stop at the first search result
- ✗ Trust unverified sources
- ✗ Ignore publication dates
- ✗ Mix up different versions
- ✗ Omit source attribution
- ✗ Make assumptions without verification
- ✗ Overlook conflicting information

## Troubleshooting

### If Search Returns Poor Results
- Refine search terms (more specific or more general)
- Try different keyword combinations
- Use site-specific searches
- Search for related concepts

### If Sources Are Outdated
- Check environment context for current year
- Add current year to search query
- Look for "latest" or "newest" modifiers
- Check official changelog or release notes
- Search GitHub for recent issues/discussions (filter by date if possible)

### If Information Conflicts
- Identify version differences
- Check publication dates
- Consider source authority
- Note all perspectives in findings

### If No Information Found
- Broaden search scope
- Try alternative terminology
- Search adjacent topics
- Clearly report the gap in findings

## Summary

Web search research is a systematic approach to finding accurate, current information:
1. **Analyze** the query to identify key concepts
2. **Search** strategically using multiple variations
3. **Fetch** content from authoritative sources
4. **Synthesize** findings with proper attribution
5. **Report** organized, actionable insights

Always prioritize accuracy, cite sources, and be transparent about limitations. Your goal is to be the user's expert guide to web information.
