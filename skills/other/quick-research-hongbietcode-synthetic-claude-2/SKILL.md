---
name: quick-research
description: This skill should be used when users need comprehensive research on a topic requiring exploration of multiple sources, synthesis of findings, and a well-structured report with citations. Use for complex research queries like "Research the latest developments in X", "Compare A vs B vs C", "Find the top N candidates for Y", or any request requiring deep exploration beyond a simple web search.
---

# Quick Research

## Overview

Quick research enables comprehensive topic exploration using a multi-agent architecture. A lead researcher (Claude Code) orchestrates multiple parallel research sub-agents to explore different aspects of a topic simultaneously, then synthesizes findings into a well-cited report.

This approach mirrors Anthropic's production research system which found that multi-agent systems outperform single-agent by 90%+ on breadth-first queries.

## When to Use This Skill

- Complex research requiring multiple independent directions
- Comparative analyses (e.g., "Compare OpenAI vs Anthropic vs Google approaches to AI safety")
- List/ranking requests (e.g., "Find the top 20 AI companies in healthcare")
- Validation questions requiring deep domain exploration
- Any research exceeding what a single web search can accomplish

## Architecture

```pseudo
# PSEUDO-CODE - Conceptual workflow, not executable code

def deep_research(user_query):
    # Phase 1: Scope
    brief = clarify_and_create_research_brief(user_query)

    # Phase 2: Research Loop (max 3 iterations)
    all_findings = []
    for iteration in range(3):
        subtopics = identify_gaps_or_subtopics(brief, all_findings)
        if not subtopics:
            break  # sufficient findings

        # Spawn parallel sub-agents (in single message)
        findings = parallel([
            Task(subagent_type="research-assistant", prompt=topic)
            for topic in subtopics
        ])
        all_findings.extend(findings)

    # Phase 3: Synthesize
    synthesized = merge_and_deduplicate(all_findings)

    # Phase 4: Report
    return generate_report_with_citations(brief, synthesized)
```

## Quick Research Workflow

### Phase 1: Scope the Research

Before spawning sub-agents, clarify the research scope:

1. **Analyze the query** - What specific information does the user need?
2. **Ask clarifying questions if needed** - Use AskUserQuestion for ambiguous terms, acronyms, or missing context
3. **Create a research brief** - A focused statement capturing:
   - The core research question
   - Specific dimensions to explore
   - Any constraints or preferences from the user
   - Source quality preferences (academic, official, etc.)

### Phase 2: Delegate Research to Sub-Agents

Use the Task tool with `subagent_type: "research-assistant"` to spawn parallel research agents.

#### Scaling Rules

| Query Type | Sub-Agents | Tool Calls Each |
|------------|------------|-----------------|
| Simple fact-finding | 1 | 3-10 |
| Direct comparisons | 2-4 (one per element) | 10-15 |
| Complex/broad research | 5-10 | 15-20 |

#### Delegation Best Practices

1. **Provide complete, standalone instructions** - Sub-agents cannot see other agents' work
2. **Specify clear task boundaries** - Avoid overlapping responsibilities
3. **Define output format expectations** - What structure should findings take?
4. **Include source guidance** - What types of sources to prioritize?
5. **Avoid acronyms** - Be explicit and specific in task descriptions

#### Example: Spawning Parallel Sub-Agents

For a query like "Compare OpenAI vs Anthropic vs Google approaches to AI safety":

```
Use Task tool THREE times in parallel (single message, multiple tool uses):

Task 1:
  subagent_type: "research-assistant"
  prompt: |
    Research OpenAI's approach to AI safety and alignment.
    Focus on:
    - Their philosophical framework for AI safety
    - Key research priorities and publications
    - Their stance on the alignment problem
    - Notable safety initiatives and teams

    Return findings with inline citations in format [Source Title](URL).
    Prioritize official OpenAI sources, research papers, and executive statements.

Task 2:
  subagent_type: "research-assistant"
  prompt: |
    Research Anthropic's approach to AI safety and alignment.
    Focus on:
    - Their philosophical framework (Constitutional AI, etc.)
    - Key research priorities and publications
    - Their stance on the alignment problem
    - Notable safety initiatives and teams

    Return findings with inline citations in format [Source Title](URL).
    Prioritize official Anthropic sources and research papers.

Task 3:
  subagent_type: "research-assistant"
  prompt: |
    Research Google DeepMind's approach to AI safety and alignment.
    Focus on:
    - Their philosophical framework for AI safety
    - Key research priorities and publications
    - Their stance on the alignment problem
    - Notable safety initiatives and teams

    Return findings with inline citations in format [Source Title](URL).
    Prioritize official DeepMind sources and research papers.
```

**CRITICAL**: Launch all sub-agents in a SINGLE message with multiple Task tool calls to enable true parallelization.

### Phase 3: Synthesize Findings

After all sub-agents return:

1. **Collect all findings** - Gather results from each sub-agent
2. **Identify patterns and gaps** - What themes emerge? What's missing?
3. **Spawn additional sub-agents if needed** - Fill gaps with targeted follow-up research
4. **Deduplicate and organize** - Remove redundant information, structure by theme

### Phase 4: Generate Final Report

Create a comprehensive report that:

1. **Answers the research brief directly**
2. **Organizes by logical structure** (see Report Structures below)
3. **Includes all relevant findings** with inline citations
4. **Ends with Sources section** listing all referenced URLs

#### Report Structures

**For comparisons:**
```markdown
# [Topic] Comparison

## Overview
[Brief context]

## [Element A]
[Detailed findings]

## [Element B]
[Detailed findings]

## Comparative Analysis
[Cross-cutting comparison]

## Conclusion
[Key takeaways]

## Sources
[Numbered list of all sources]
```

**For lists/rankings:**
```markdown
# Top [N] [Category]

## 1. [Item]
[Details with citations]

## 2. [Item]
[Details with citations]

...

## Sources
[Numbered list]
```

**For topic exploration:**
```markdown
# [Topic] Research Report

## Overview
[Context and scope]

## [Aspect 1]
[Detailed findings]

## [Aspect 2]
[Detailed findings]

## Key Insights
[Synthesized conclusions]

## Sources
[Numbered list]
```

## Citation Rules

- Assign each unique URL a single citation number
- Use inline citations: `[1]` or `[Source Title](URL)`
- Number sources sequentially (1, 2, 3...) without gaps
- End with `## Sources` section listing all sources:
  ```
  ## Sources
  [1] Source Title: URL
  [2] Source Title: URL
  ```

## Hard Limits

To prevent excessive resource usage:

- **Maximum 10 parallel sub-agents** per research iteration
- **Maximum 3 research iterations** (initial + 2 follow-ups)
- **Stop when findings are sufficient** - Don't pursue perfection
- **Token awareness** - Multi-agent systems use ~15x more tokens than chat

## Key Insights from Anthropic's Research System

1. **Token usage explains 80% of performance variance** - Distribute work across agents with separate context windows
2. **Start wide, then narrow** - Broad queries first, progressively focus
3. **Context isolation prevents failures** - Each sub-agent handles one subtopic cleanly
4. **Sub-agent output compression** - Have sub-agents summarize their findings to avoid "game of telephone" information loss
5. **Parallel execution cuts time 90%** - Always spawn sub-agents in parallel when independent

## References

For detailed prompt templates and architecture details, see:
- `references/prompts.md` - Research agent prompt templates
- `references/architecture.md` - Multi-agent system architecture details
