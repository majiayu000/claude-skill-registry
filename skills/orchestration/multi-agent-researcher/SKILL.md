---
name: multi-agent-researcher
description: Conduct comprehensive research on any topic by coordinating 2-4 specialized researcher agents in parallel, then synthesizing findings into a detailed report via mandatory report-writer agent delegation
allowed-tools: Task, Read, Glob, TodoWrite
version: 2.1.2
---

# Multi-Agent Research Coordinator

## Purpose

Transform complex research questions into comprehensive reports by:
1. Decomposing broad topics into 2-4 focused subtopics
2. Spawning specialized researcher agents in parallel
3. Synthesizing findings into cohesive final report
4. Saving structured outputs for reference

## When to Use

Auto-invoke when user asks:
- **Search/Discovery**: "Search what is [topic]", "Find information about [subject]", "Look up [technology]", "Discover [patterns]"
- **Investigation**: "Research [topic]", "Investigate [subject]", "Analyze [phenomenon]", "Study [field]", "Explore [domain]"
- **Collection**: "Gather information about [subject]", "Collect data on [topic]", "Compile resources for [area]"
- **Learning**: "Learn about [subject]", "Tell me about [topic]", "Dig into [technology]", "Delve into [concept]"
- **Contextual**: "What are the latest developments in [field]?", "Comprehensive analysis of [topic]", "Deep dive into [subject]", "State of the art in [domain]", "Best practices for [area]"

Do NOT invoke for:
- Simple factual questions ("What is the capital of France?")
- Decision evaluation ("Should I use X or Y?")
- Code-related tasks ("Debug this function", "Write a script")

## Orchestration Workflow

### Phase 1: Query Analysis & Decomposition

**Step 1.1: Understand the Research Question**
Analyze user's query to identify core topic, scope, and intent.

**Step 1.2: Decompose into Subtopics**
Break topic into 2-4 focused subtopics that are:
- Mutually exclusive (minimal overlap)
- Collectively exhaustive (cover whole topic)
- Independently researchable
- Together provide comprehensive coverage

**Decomposition Patterns:**

**Temporal**: Past → Current → Future
**Categorical**: Category 1, 2, 3
**Stakeholder**: Technical → Business → Policy → User
**Problem-Solution**: Problem → Solutions → Gaps → Future
**Geographic**: Region A → Region B → Comparison

**Step 1.3: Create Research Plan**
Use TodoWrite to track:
```
- [ ] Decompose query into subtopics
- [ ] Spawn researcher 1: [subtopic]
- [ ] Spawn researcher 2: [subtopic]
- [ ] Spawn researcher 3: [subtopic]
- [ ] Synthesize findings
- [ ] Save final report
```

---

### Phase 2: Parallel Research Execution

**Step 2.1: Spawn Researcher Agents in Parallel**

For each subtopic, create a Task tool call with:
```
subagent_type: "researcher"
description: "Research {subtopic name}"
prompt: "Research the following subtopic in depth:

**Subtopic**: {Subtopic name}
**Context**: Part of research on '{original topic}'
**Focus**: {Specific guidance}

Conduct thorough web research, gather authoritative sources, extract key findings, and save results to files/research_notes/{subtopic-slug}.md"
```

**Critical**: Spawn ALL researchers in parallel (multiple Task calls in same message), not sequentially.

**Step 2.2: Monitor Completion**
Update TodoWrite as researchers complete.

**Step 2.3: Verify All Complete**
Use Glob to confirm all files exist: `files/research_notes/*.md`

---

### Phase 3: Synthesis & Report Generation

**⚠️ CRITICAL: ARCHITECTURAL ENFORCEMENT ACTIVE ⚠️**

**YOU DO NOT HAVE WRITE TOOL ACCESS** when this skill is active. The `allowed-tools` frontmatter explicitly EXCLUDES the Write tool to enforce proper workflow delegation.

**YOU CANNOT**:
- ❌ Write synthesis reports yourself
- ❌ Create files in files/reports/ directory
- ❌ Bypass the report-writer agent

**YOU MUST**:
- ✅ Spawn report-writer agent via Task tool
- ✅ Delegate all synthesis and report writing to the agent
- ✅ Read the completed report and deliver to user

---

**Step 3.1: Verify Research Completion**

1. Use Glob to confirm all research notes exist: `files/research_notes/*.md`
2. Verify count matches number of spawned researchers
3. If any missing: investigate and complete before synthesis

**Step 3.2: Spawn Report-Writer Agent (MANDATORY)**

**This is the ONLY synthesis approach** - there is no "Option A" or "Option B". You MUST use the report-writer agent because you lack Write tool permissions.

```
Task:
subagent_type: "report-writer"
description: "Synthesize research findings into comprehensive report"
prompt: "Synthesize research into comprehensive report:

**Original Question**: {user query}
**Subtopics Researched**: {list all subtopics}
**Notes Location**: files/research_notes/

## Your Tasks:
1. Read ALL research notes from files/research_notes/
2. Identify themes, patterns, and contradictions across notes
3. Synthesize findings into cohesive narrative
4. Cite sources from research notes
5. Add cross-cutting insights beyond individual notes
6. Save comprehensive report to files/reports/{topic-slug}_{timestamp}.md

## Report Structure:
- Executive Summary
- Key Findings (with evidence from research notes)
- Detailed Analysis by subtopic
- Cross-Cutting Themes
- Contradictions and Debates
- Gaps and Limitations
- Source Bibliography

Use the timestamp format: $(date +\"%Y%m%d-%H%M%S\") for the filename."
```

**Step 3.3: Monitor Agent Completion**

After spawning report-writer agent, wait for completion. The agent will:
- Read all research notes
- Synthesize findings
- Write comprehensive report to files/reports/
- Return completion message with file path

---

### Phase 4: Deliver Results

**Step 4.1: Create User Summary**
```markdown
# Research Complete: {Topic}

Comprehensive research completed with {N} specialized researchers.

## Key Findings
1. {Finding 1}
2. {Finding 2}
3. {Finding 3}

## Research Scope
{N} subtopics investigated:
- {Subtopic 1}
- {Subtopic 2}
- {Subtopic 3}

## Files Generated
**Research Notes**: `files/research_notes/`
- {file1}.md
- {file2}.md
- {file3}.md

**Final Report**: `files/reports/{filename}.md`

## Next Steps
{Optional suggestions}
```

**Step 4.2: Update TodoWrite**
Mark all items complete.

---

## Best Practices

### Good Decomposition
✅ 2-4 subtopics (sweet spot: 3)
✅ Distinct but related
✅ Comprehensive coverage
✅ Independently researchable

❌ Too many (>5)
❌ Too few (1)
❌ Significant overlap
❌ Too narrow or too broad

### Parallel Execution
- Always spawn researchers simultaneously
- Never sequential unless dependent
- Provide context to each researcher
- Reasonable scope (10-15 min each)

### Synthesis Quality
- Read ALL notes
- Find connections across subtopics
- Note contradictions explicitly
- Cite sources
- Add insights beyond individual notes

---

## Error Handling

**Researcher Fails**: Try replacement, proceed with others, note gap
**No Results Found**: Accept partial, note limitation
**Contradictory Findings**: Document all perspectives explicitly
**Unclear Query**: Ask clarifying questions first

---

## Examples

**Query**: "Research quantum error correction"
**Decomposition**:
1. Theoretical foundations
2. Hardware implementations
3. Commercial viability
**Researchers**: 3 parallel
**Synthesis**: report-writer agent (MANDATORY)

**Query**: "Investigate cryptocurrency market 2025"
**Decomposition**:
1. Market metrics & players
2. Regulatory landscape
3. Technology evolution
4. Institutional trends
**Researchers**: 4 parallel
**Synthesis**: report-writer agent (MANDATORY)

---

**Remember**: Quality depends on good decomposition, thorough researchers, insightful synthesis, and clear user communication.
