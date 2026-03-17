---
name: updating-knowledge
description: Systematic research methodology for building comprehensive, current knowledge on any topic. Requires web_search tool. Use when questions require thorough investigation, recent developments post-cutoff, synthesis across multiple sources, or when Claude's knowledge may be outdated or incomplete. Triggered by "Research", "Investigate", "What's current on", "Latest info on", complex queries needing validation, or technical topics with recent changes.
metadata:
  version: 1.0.3
---

# Updating Knowledge

## Core Principles

- **Systematic > ad-hoc** - Follow research methodology, don't scatter searches randomly
- **Cross-validate** - Verify claims across multiple independent sources
- **Confidence tracking** - Explicitly flag single-source claims and gaps
- **Concise output** - Present findings efficiently, introspection in thinking blocks

## Preflight Check

**CRITICAL: This skill requires web_search tool access.**

Before proceeding:
1. Verify web_search tool is available in tool set
2. If NOT available:
   - Immediately inform user: "I need web search enabled for research tasks. Please toggle on 'Web search' in the feature menu."
   - DO NOT attempt research without web_search
   - DO NOT proceed with workflow

If web_search is unavailable, fail fast—don't waste context attempting workarounds.

## Imperative Triggers

Use this skill when:
- User says "Research", "Investigate", "What's current on", "Latest info on", "Find out about"
- Query requires synthesizing multiple authoritative sources
- Topic likely changed since training cutoff
- Technical/product questions where documentation is essential
- Contradictory information needs resolution
- Building comprehensive understanding for ongoing work

**Note:** Avoid triggering on generic action verbs like "update" (which could mean file/code changes). Focus on explicit knowledge-gathering requests.

## Research Workflow

### 1. Scope Definition (internal)

Identify in thinking block:
- What specifically needs investigation
- Current knowledge baseline
- Known gaps
- Required depth (overview vs comprehensive)

### 2. Source Gathering (2-10 tool calls)

**Source priority:**
1. Official documentation, project repos, company announcements
2. Academic papers, technical blogs with clear expertise
3. Community discussions (for ecosystem context only)

**Tool selection:**
- `web_search` - Find authoritative sources
- `web_fetch` - Extract complete content from any URL (no prior search required)
- Internal tools (GitHub, Drive, etc.) - Company/personal context
- Multiple tool types as needed

**Gather 3-5 diverse sources minimum** for cross-validation.

### 3. Synthesis (internal)

In thinking block:
- Cross-validate major claims across sources
- Note contradictions explicitly
- Track publication dates
- Assess source credibility
- Identify remaining gaps

### 4. Output (concise)

Present findings concisely:

```markdown
## [Topic]

**Key findings:**
[2-3 sentence summary with most important updates]

**Current state:**
[Concise description of what's true now]

**Changes since cutoff:**
[Only if relevant - what's different]

**Gaps:**
[Only if user needs to know - what wasn't found]

Sources: [URLs]
```

**Confidence indicators:**
- State explicitly when claims are single-source
- Note contradictions between sources
- Flag unverified information
- Quantify confidence (high/medium/low) when uncertain

## Quality Standards

**Minimum requirements:**
- 3+ independent sources consulted
- Major claims cross-validated
- Explicit confidence assessment
- Remaining gaps identified when relevant

**Avoid:**
- Single-source claims presented as definitive
- Ignoring publication dates
- Marketing language as fact
- Verbose deliberation in final output (use thinking blocks)
- Over-explaining research process to user

## Tool Usage Notes

**web_fetch capabilities:**
- Can fetch ANY URL directly - doesn't require prior search results
- Use for complete documentation pages, technical articles
- Effective for deep content extraction after search identifies sources

**web_search patterns:**
- Start specific, broaden if needed
- Never repeat similar queries - make each unique
- Use current date context when relevant (November 2025)

**Internal tools:**
- Prioritize for company/personal data
- Combine with web tools for comparative analysis

## Output Efficiency

**DO:**
- Present findings concisely
- Use thinking blocks for deliberation
- Lead with key takeaways
- State confidence explicitly when low
- Cite sources inline

**DON'T:**
- Narrate research process unless asked
- Include verbose phase descriptions
- Over-explain methodology
- Repeat information across sections
- Document internal reasoning in output

## Example Outputs

**Technical documentation inquiry:**
```
TypeScript 5.3 (Nov 2023) added import attributes for JSON modules. The syntax uses `with` instead of deprecated `assert`. Runtime performance unchanged—validation happens at parse time.

Gap: No official benchmarks comparing validation overhead across bundlers.

Sources: [TS release notes, GitHub issue #54242, esbuild docs]
```

**Conflicting information:**
```
React Server Components ship in Next.js 13.4+ (stable) and Remix 2.0 (experimental). 

Contradiction: Meta's blog claims "production-ready" while Remix docs flag "breaking changes expected." Cross-validation shows Meta refers to Next.js implementation only.

Confidence: High on Next.js status, medium on Remix timeline.

Sources: [Next.js changelog, Remix docs, React.dev]
```

**Avoid narrating process:**
```
❌ "After conducting extensive research and cross-validating multiple authoritative sources..."
✓ Just present findings with source attribution
```
