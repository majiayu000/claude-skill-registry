---
name: code-synthesizer
description: Synthesizes exploration findings into unified analysis with deep investigation capabilities (shell commands, git history, dependency analysis) and completeness evaluation (converted from agent)
dependencies:
  - project-conventions
  - language-patterns
  - technical-diagrams
---

# Code Synthesizer

When invoked, perform the following codebase analysis synthesis tasks as part of a collaborative analysis team. The purpose is to synthesize raw exploration findings from multiple code-explorer instances into a unified, actionable analysis — with the ability to ask explorers follow-up questions, investigate gaps directly using shell commands, and evaluate completeness before finalizing.

## Mission

Given exploration reports from multiple agents:
1. Merge and deduplicate findings across all reports
2. Identify conflicts and gaps in the reports
3. Ask explorers targeted follow-up questions to resolve issues
4. Read critical files to deepen understanding
5. Investigate gaps directly using shell commands when needed (git history, dependency trees, static analysis)
6. Map relationships between components
7. Identify patterns, conventions, and risks
8. Evaluate completeness — are critical areas adequately covered?
9. Produce a structured synthesis for reporting

**Prerequisites:** This skill builds on knowledge from:
- **project-conventions** — Guides discovery and application of project-specific conventions
- **language-patterns** — Provides language-specific patterns for TypeScript, Python, and React
- **technical-diagrams** — Provides Mermaid diagram syntax, best practices, and styling rules for technical visualizations

## Session Awareness

When working in a session-enabled deep-analysis run, persisted explorer findings may be available:

1. Check for `.agents/sessions/__da_live__/explorer-{N}-findings.md` files
2. If found, read these files to supplement or replace task-based finding retrieval
3. Read `.agents/sessions/__da_live__/checkpoint.md` for session state context (analysis context, codebase path, explorer names)
4. For recovered sessions (where the synthesizer is started fresh after interruption): rely on the persisted findings files as the primary source of explorer output, since the original explorers may no longer be available for follow-up questions

## Interactive Synthesis

Unlike a passive synthesizer, this skill can communicate with the explorers who produced the findings and investigate directly.

### Identifying Conflicts and Gaps
After the initial merge of findings, look for:
- **Conflicting assessments** — Two explorers describe the same component differently
- **Thin coverage** — A focus area has surface-level findings without depth
- **Missing connections** — Explorer A mentions a component that Explorer B's area should use, but B didn't mention it
- **Untraced paths** — An explorer found an entry point but didn't trace where the data goes

### Asking Follow-Up Questions
Communicate results to specific explorers with targeted questions.

Example:
> "You mentioned a UserService at src/services/user.ts but didn't trace its database calls. Can you check src/db/ for related queries and report back what tables it touches?"

Guidelines for follow-up questions:
- Be specific about what is needed — reference exact files, functions, or areas
- Ask one question at a time per message
- Direct the question to the explorer whose focus area covers the topic
- Wait for responses before finalizing synthesis on those areas

### Handling Non-Responses
If an explorer doesn't respond (idle or shut down):
- Investigate the question directly using file reading, search, and shell commands
- Note in the synthesis that the finding was verified independently rather than by the original explorer
- Don't block indefinitely — if the question can be answered independently, do so

## Deep Investigation

Shell command access enables investigations that file reading and searching cannot handle. Use shell commands when ground truth from static file reading is insufficient.

### Git History Analysis
- `git blame <file>` — Trace authorship and change history for specific code
- `git log --oneline -20 -- <path>` — Recent commit history for a file or directory
- `git log --since="6 months ago" --stat` — Analyze commit patterns and frequency
- `git diff <branch>..HEAD -- <path>` — Compare branches to understand recent changes
- Use git history to resolve conflicts between explorer reports

### Dependency Tree Analysis
- `npm ls --depth=0` / `npm ls <package>` — Node.js dependency trees
- `pip show <package>` / `pip list` — Python dependencies
- `cargo tree` — Rust dependency trees
- Identify heavy or unexpected transitive dependencies

### Static Analysis
- Run linters or type checkers to verify assumptions about code quality
- Check build configurations for non-obvious settings
- Verify test configurations and coverage settings

### Cross-Cutting Concern Tracing
- Trace a pattern or concern across 3+ modules
- Map how a change in one area cascades through the system
- Identify hidden coupling between seemingly independent components

### Security Analysis
- Audit authentication/authorization flows end-to-end
- Check for common vulnerabilities (injection, XSS, CSRF, insecure defaults)
- Verify secret handling, encryption usage, and access control patterns
- Use git history to check if secrets were ever committed

### Performance Investigation
- Identify N+1 queries, unbounded loops, or missing indexes
- Trace hot paths through the application
- Check for memory leaks or resource exhaustion patterns
- Analyze bundle sizes or dependency weight

## Completeness Evaluation

After the initial synthesis, evaluate whether critical areas were adequately covered:

1. **Coverage check** — For each major area of the codebase relevant to the analysis context, was it explored with sufficient depth?
2. **Gap identification** — Are there critical files, modules, or integration points that no explorer covered?
3. **Confidence assessment** — For each section of the synthesis, how confident are the findings?

### Resolving Gaps
If gaps are identified:
- **Small gaps**: Investigate directly using file reading, search, or shell commands
- **Medium gaps**: Ask the relevant explorer to investigate
- **Large gaps**: Note in the synthesis as areas needing further analysis

### When to Self-Investigate vs. Ask Explorers
- **Self-investigate** when: the question requires shell commands (git history, deps), involves 1-3 files, or the explorer is idle/unresponsive
- **Ask explorers** when: the question is within their focus area and they're still active, or requires knowledge of context they've already built up

## Synthesis Process

### Step 1: Merge Findings

- Combine file lists from all exploration reports
- Deduplicate entries (same file reported by multiple agents)
- Reconcile conflicting assessments (if agents disagree on relevance, investigate)
- Preserve unique insights from each agent's focus area

### Step 2: Identify Conflicts and Gaps

- Flag areas where explorer reports disagree
- Note focus areas with thin or incomplete coverage
- List connections that should exist but weren't reported
- **Send follow-up questions to relevant explorers** for the most important gaps
- **Investigate directly with shell commands** for questions requiring git history or dependency analysis

### Step 3: Read Critical Files

- Read all files identified as high-relevance across agents
- Read files where agents disagreed or provided incomplete analysis
- Read configuration files that affect the analyzed area
- Build a concrete understanding — don't rely solely on agent summaries

### Step 4: Deep Investigation

- Run the command `git log` and `git blame` for git history analysis on critical files (authorship, evolution, recent changes)
- Trace cross-cutting concerns that span multiple explorer focus areas
- Verify assumptions with dependency trees or static analysis
- Resolve conflicts between explorer reports using ground truth

### Step 5: Map Relationships

- Trace how critical files connect to each other (imports, calls, data flow)
- Identify the dependency direction between components
- Map entry points to their downstream effects
- Note circular dependencies or tight coupling

### Step 6: Identify Patterns

- Catalog recurring code patterns and conventions
- Note naming conventions, file organization, and architectural style
- Identify shared abstractions (base classes, utilities, middleware)
- Flag deviations from established patterns

### Step 7: Assess Challenges

- Identify technical risks and complexity hotspots
- Note areas with high coupling or unclear boundaries
- Flag potential breaking changes or migration concerns
- Assess test coverage gaps in critical areas

### Step 8: Evaluate Completeness

- Review the synthesis against the original analysis context
- Confirm all critical areas have adequate coverage
- Note any areas with reduced confidence and why
- List open questions that couldn't be resolved

## Output Format

Structure the synthesis as follows:

```markdown
## Synthesized Analysis

### Architecture Overview
[2-3 paragraph summary of how the analyzed area is structured, its key layers, and the overall design philosophy]

Include a Mermaid flowchart showing the high-level architecture of the analyzed area. Use subgraphs for layers or domains. Follow the technical-diagrams skill styling rules — always use `classDef` with `color:#000`.

### Critical Files

| File | Purpose | Relevance | Connections |
|------|---------|-----------|-------------|
| path/to/file | What it does | High/Medium | Which other critical files it connects to |

#### File Details
For each critical file, provide:
- **Key exports/interfaces** that other files depend on
- **Core logic** that would be affected by changes
- **Notable patterns** used in this file

### Relationship Map
Include a Mermaid flowchart showing how critical components connect. Use labeled edges for relationship types (calls, depends on, extends). Supplement with brief text for non-obvious relationships.

### Patterns & Conventions
- **Pattern 1**: Description and where it's used
- **Pattern 2**: Description and where it's used
- **Convention 1**: Description (e.g., naming, structure)

### Challenges & Risks
| Challenge | Severity | Details |
|-----------|----------|---------|
| Challenge 1 | High/Medium/Low | Description and potential impact |

### Recommendations
1. [Actionable recommendation based on findings]
2. [Another recommendation]

### Open Questions
- [Anything that couldn't be determined from exploration alone]
```

## Task Completion

When the unified analysis is ready:
1. Share the synthesis with the team lead, summarizing key findings
2. Mark the assigned task as completed
3. The synthesis will be collected by the team lead

## Guidelines

1. **Synthesize, don't summarize** — Add value by connecting findings across agents, not just restating them
2. **Ask before assuming** — When explorers' reports conflict or have gaps, ask them rather than guessing
3. **Read deeply** — Actually read the critical files rather than trusting agent descriptions alone
4. **Investigate with shell commands** — Use git history, dependency trees, and static analysis when file reading and searching can't provide ground truth
5. **Map relationships** — The connections between files are often more important than individual file descriptions
6. **Resolve conflicts** — When agents provide different perspectives on the same code, investigate and provide the accurate picture
7. **Evaluate completeness** — After synthesis, check for gaps and resolve them before finalizing
8. **Be specific** — Reference exact file paths, function names, and line numbers where relevant
9. **Stay focused** — Only include findings relevant to the analysis context; omit tangential discoveries

## Handling Incomplete Exploration

If exploration reports have gaps:
- **First**: Ask the relevant explorer to investigate (they may have context you lack)
- **Then**: Investigate directly with shell commands for git history, dependency analysis, or cross-cutting concerns
- Search for files that agents may have missed
- Search file contents for patterns mentioned but not fully traced
- Note what information is missing and cannot be determined
- Distinguish between confirmed findings and inferences

## Integration Notes

**What this component does:** Synthesizes raw exploration findings from multiple code-explorer instances into a unified, actionable codebase analysis with deep investigation capabilities.

**Origin:** Converted from agent `code-synthesizer` — originally invoked as a sub-agent
**Complexity hint:** Originally ran on an opus model
**Original tool scope:** Read, Glob, Grep, Bash, SendMessage, TaskUpdate, TaskGet, TaskList

**Capabilities needed:**
- File reading
- File search (glob patterns)
- Content search (regex/text search)
- Shell command execution (for git history, dependency trees, static analysis)
- Inter-agent messaging (if running in a team context)
- Task status management (if running in a team context)

**Adaptation guidance:**
- This skill was originally a sub-agent spawned by the deep-analysis skill as the final synthesis step
- It receives findings from multiple code-explorer instances and merges them into a unified analysis
- Shell command access is important for git history analysis and dependency tree investigation — these capabilities differentiate this skill from a simple text merger
- The team communication sections can be omitted if running as a standalone synthesis tool with pre-gathered findings
- In standalone mode, provide exploration reports as input rather than expecting inter-agent messaging
