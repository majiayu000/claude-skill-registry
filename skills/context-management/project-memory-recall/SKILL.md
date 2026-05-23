---
name: Project Memory Recall
description: Retrieve project-specific insights from file-based memory. Use when working on features, encountering domain-specific questions, or user says "--project-recall" or "--recall" (you decide which scope, may use both). Skip for routine tasks or universal pattern questions (use coder-memory-recall). MUST be invoked using Task tool to avoid polluting main context.
---

# Project Memory Recall

**⚠️ EXECUTION CONTEXT**: This Skill MUST be executed using Task tool with subagent_type="general-purpose". Runs in separate context to avoid polluting main conversation.

**Purpose**: Retrieve **project-specific insights** from file-based memory at `.claude/skills/project-memory-store/`.

**Key Architecture**: SKILL.md + README.md files form a **tree guideline structure** - read overviews first, navigate to specific files as needed. Very effective for progressive disclosure.

**Keep SKILL.md lean**: Provide overview and reference other files. When this file becomes unwieldy, split content into separate files and reference them. Trust Claude to read detailed files only when needed.

**When to Use**:
- Before working on project-specific features or components
- When encountering domain-specific questions or patterns
- User explicitly says "--project-recall" or "--recall" (Claude decides if universal or project-specific, may use both)
- Need architecture decisions or integration patterns for THIS codebase

**REMEMBER**: Failures are as valuable as successes. Look for both #success and #failure tags when searching project memories.

**When NOT to Use**:
- Routine or trivial tasks
- Just recalled similar knowledge recently
- Universal pattern questions (use coder-memory-recall)

---

## PHASE 0: Understand Memory Structure

Read `.claude/skills/project-memory-store/SKILL.md` to understand current organization.

Memory types available:
- `episodic/` - Concrete events in this project
- `procedural/` - Project-specific workflows
- `semantic/` - Project patterns and architecture

---

## PHASE 1: Construct Search Strategy

**If user provided explicit query**: Use it to determine which memory type(s) to search

**If inferring from context**: Analyze task to choose:
- Need past experience in this project? → Search episodic
- Need project-specific process? → Search procedural
- Need architecture/domain pattern? → Search semantic
- Unclear? → Search all three

**Query keywords**: Extract 3-8 core concepts including project-specific terms

---

## PHASE 2: Search for Relevant Memories

### Step 0 (Optional): Try Vector Search First

**If Qdrant MCP server available**, try semantic search for file hints:

1. **Construct vector query** - Use full summary for better semantic matching:
   - If user provided query: Use their question/description as-is
   - If inferring from task: Write 2-3 sentence summary of what you're looking for
   - Include key concepts, technical terms, problem description, and project-specific context
   - Keep concise but descriptive (not just keywords, not entire context)

2. **Call search_memory** MCP tool:
   ```
   search_memory(
       query="<2-3 sentence summary of what you're looking for>",
       memory_level="project",
       limit=5
   )
   ```
3. **Extract file_path hints** from top results
4. **Evaluate sufficiency**:
   - If vector results provide enough relevant information to answer the query: You may skip to Phase 3 (present those results)
   - If results seem incomplete, outdated, or you need verification: Continue to file-based navigation below
   - If <3 results or tool unavailable: Continue to file-based navigation below

**IMPORTANT**: Vector results may be outdated (files could have moved/changed). You decide whether they're sufficient or if file verification is needed. Progressive disclosure is optional if vector search already provided good answers.

---

### File-Based Navigation (Primary Method)

For each target memory type:

1. **Read README.md** (if exists) in memory type directory
2. **Identify relevant subdirectories** based on query and project context (use file_path hints if available)
3. **Read targeted files**:
   - Use Grep to search for keywords (project-specific terms, module names, domain concepts) - prioritize hinted paths if available
   - Use Read to load promising files
   - Progressive disclosure: Read READMEs first, then specific files

**Do NOT read entire memory tree** - use filesystem tools intelligently.

---

## PHASE 3: Extract Relevant Memories

Collect top 3 most relevant memories matching query.

**Relevance criteria**:
- Keyword match quality (project-specific terms matter)
- Component/module relevance to current task
- Actionability for current project work

---

## PHASE 4: Check If Refactoring Needed

**Signs memory needs reorganization**:
- Took >5 file reads to find relevant memories
- Found duplicates in multiple files
- Unrelated content mixed in same file
- Difficult to navigate structure

**If reorganization needed**: Invoke general-purpose agent to refactor memory structure.

**Refactoring prompt**:
```
Refactor project-memory-store file structure at .claude/skills/project-memory-store/.

Current issues: [describe what made recall difficult]

Actions needed:
- Merge duplicate memories
- Reorganize files by project components/topics (max 2-level depth)
- Update README.md files as overviews
- Ensure episodic/procedural/semantic separation is clear

Maintain all existing memory content - only reorganize structure.
```

---

## PHASE 5: Present Results

**Format**:
```
🔍 Project Memory Recall Results

**Project**: <project name>
**Query**: <keywords or user question>
**Memory Types Searched**: <episodic/procedural/semantic>
**Results Found**: <number>

---

## Result 1: [Title]

**Type**: <Episodic/Procedural/Semantic>
**Source**: <file path>

<Full memory content>

**Relevance**: <1-2 sentences explaining why this matches query and applies to current work>

---

## Result 2: [Title]

[Same format]

---

## Application Guidance

<2-3 sentences synthesizing results and actionable next steps for current project task>

**Related Components**: <list specific files/modules mentioned in results>
```

**If no results found**:
```
🔍 Project Memory Recall Results

**Project**: <project name>
**Query**: <keywords>
**Results Found**: 0 relevant memories

No project-specific insights matched your query.

**Suggestions**:
- Try broader search terms
- Check if this is universal knowledge (use coder-memory-recall)
- This may be new area of codebase - proceed with exploration
- Store insights after completing this task
```

**If refactoring triggered**:
```
⚙️ Memory Refactoring Triggered

Project memory structure was reorganized during recall to improve future searches.
<report refactoring actions taken>
```

---

## Tool Usage

**CRITICAL**: Invoke via Task tool with general-purpose agent. Never execute directly in main context.
