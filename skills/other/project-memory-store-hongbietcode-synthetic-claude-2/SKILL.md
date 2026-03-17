---
name: Project Memory Store
description: Store project-specific insights and context into file-based memory. Use after completing tasks that reveal important details about THIS codebase. Use when user says "--project-store" or "--learn" (you decide which scope, may use both) or after discovering project-specific patterns. ALSO invoke when user expresses strong frustration using trigger words like "fuck", "fucking", "shit", "moron", "idiot", "stupid", "garbage", "useless", "terrible", "wtf", "this is ridiculous", "you're not listening" - these are CRITICAL learning signals for storing project-specific failure patterns. Skip for universal patterns (use coder-memory-store) or routine work. MUST be invoked using Task tool to avoid polluting main context.
---

# Project Memory Store

**⚠️ EXECUTION CONTEXT**: This Skill MUST be executed using Task tool with subagent_type="general-purpose". Runs in separate context to avoid polluting main conversation.

**Purpose**: Extract and store **project-specific insights** (episodic/procedural/semantic) into file-based memory at `.claude/skills/project-memory-store/`.

**Key Architecture**: This SKILL.md + subdirectory README.md files form a **tree guideline structure** for progressive disclosure - overview at top, details deeper. This is very effective for information retrieval.

**Keep SKILL.md lean**: Provide overview and reference other files. When this file becomes unwieldy, split content into separate files and reference them. Trust Claude to read detailed files only when needed.

**When to Use**:
- After making significant architecture decisions for THIS project
- When discovering project-specific patterns or configurations
- User explicitly says "--project-store" or "--learn" (Claude decides if universal or project-specific, may use both)
- Completed tasks revealing important domain logic or codebase structure

**CRITICAL**: Store BOTH successful AND failed trajectories. Failures are equally important - often MORE valuable than successes. Failed approaches in this project teach what NOT to do and why.

**When NOT to Use**:
- Universal patterns applicable to any project (use coder-memory-store)
- Routine tasks or obvious conventions
- Standard debugging without project-specific learnings

**Selection Criteria**: Most conversations yield 0-1 project-specific insights. Focus on details future work on THIS codebase would benefit from.

---

## PHASE 0: Initialize Memory Structure

Check if memory directories exist at `.claude/skills/project-memory-store/`:
- `episodic/` - Concrete events in this project
- `procedural/` - Project-specific workflows
- `semantic/` - Project patterns and principles

If missing, create directories and initialize each with single file:
- `episodic/episodic.md`
- `procedural/procedural.md`
- `semantic/semantic.md`

Update `SKILL.md` (this file) as needed when structure changes - modify ANY part to keep it accurate and useful.

---

## PHASE 1: Extract Project-Specific Insights

Analyze conversation and extract **0-3 insights** (most yield 0-1).

**Classify each as**:
- **Episodic**: Concrete events in THIS project (debugging specific module, implementing feature)
- **Procedural**: Project-specific workflow (how we deploy, how we test this codebase)
- **Semantic**: Project patterns (architecture decisions, domain-specific approaches)

**Extraction Criteria** (ALL must be true):
1. **Project-specific**: Applies to THIS particular codebase/domain
2. **Non-obvious**: Not already in documentation or README
3. **Actionable**: Provides concrete guidance for future work on this project
4. **Important**: Worth remembering for long-term maintenance

**Reject**:
- Universal patterns (use coder-memory-store)
- Routine work
- Obvious conventions already documented

---

## PHASE 2: Search for Similar Memories

For each extracted insight:

**Step 1: Determine target memory type** (episodic/procedural/semantic)

**Step 2 (Optional): Try Vector Search First**

**If Qdrant MCP server available**, try semantic search for similar memories:

1. **Construct query** from new memory - Use full formatted memory for better matching:
   - Use: Title + Description + Content (the complete formatted memory text)
   - This gives embedding model sufficient context for semantic similarity (including project-specific details)

2. **Call search_memory** MCP tool:
   ```
   search_memory(
       query="<full formatted memory text>",
       memory_level="project",
       limit=5
   )
   ```
3. **Extract file_path hints** and similarity scores
4. **If <3 results or tool unavailable**: Continue to file-based search below

**IMPORTANT**: Vector results may be outdated. Use as hints to guide file search, not as absolute truth.

---

**Step 3: File-Based Search (Primary Method)**
- Use Grep to search for keywords across project memory files (prioritize hinted paths if available)
- Search in target memory type directory (e.g., `.claude/skills/project-memory-store/episodic/`)
- Look for similar titles, tags, project components, or core concepts
- Read files with potential matches

**Step 4: Check similarity**
- If found similar content: Read full context
- Determine if: Duplicate, Related, or Different

---

## PHASE 3: Consolidation Decision

**Decision Matrix** (file-based consolidation):

| Similarity | Action | Rationale |
|-----------|--------|-----------|
| **Duplicate/Very Similar** | **MERGE** | Combine into single stronger entry |
| **Related (same topic)** | **UPDATER** | Update existing memory with new information |
| **Pattern Emerges** | **GENERALIZE** | Extract pattern → promote episodic to semantic |
| **Different** | **CREATE** | New file or separate section |

**Actions**:

**MERGE** (duplicate or very similar):
- Combine both memories into single, stronger entry
- Eliminate redundancy, keep unique project-specific details from both
- If contradictory: Add "**Previous Approach:**" and tag #reconsolidated
- Update in existing file

**UPDATER** (related, same topic):
- Update existing memory with new information
- If extends existing: Add new details inline with note "**Updated [date]:**"
- If alternative approach: Add separate entry in same file with cross-reference
- If contradicts: Add "**Previous approach:**" to show evolution of understanding

**GENERALIZE** (pattern emerges from multiple episodic memories):
- Extract common pattern from 2+ similar episodic entries in THIS project
- Create/update semantic memory with the generalized project-specific pattern
- Reference episodic examples in semantic entry
- Tag episodic entries with reference to semantic pattern
- This is how learning happens: specific experiences → general principles
- **Check universality**: If pattern applies beyond this project, also invoke coder-memory-store

**CREATE** (different topic):
- Store in new location (new file or different section)
- Update README.md to reference new content

---

## PHASE 4: Store Memory

**CRITICAL: Use COMPACT format to prevent memory bloat. Each memory = 3-5 sentences MAX.**

**Universal Format** (works for ALL memory types):
```
**Title:** <concise title>
**Description:** <one sentence summary>

**Content:** <3-5 sentences covering: what happened in this project, what was tried (including failures), what worked/failed, key lesson, relevant files/components>

**Tags:** #tag1 #tag2 #success OR #failure
```

**Formatting Rules**:
- NO blank line between Title and Description
- ONE blank line before Content
- ONE blank line before Tags
- Content MUST be 3-5 sentences (not paragraphs, not lists, not verbose sections)
- Include project-specific file paths and components in Content
- Include both failures and successes if relevant
- Tag episodic memories with #episodic, procedural with #procedural, semantic with #semantic

**Determine storage location**:
1. **Read README.md** (if exists) in target memory type directory
2. **Decide based on consolidation action**:
   - MERGE/UPDATER: Modify existing file
   - GENERALIZE: Update semantic/ or create new semantic file
   - CREATE: New file or new section
3. **Max depth**: 2 levels (e.g., `episodic/authentication/` is deepest)

**Execute storage**:
1. **Write to file (Source of Truth)**:
   - Write formatted memory to file (merge, update, generalize, or create)
   - File write is PRIMARY - must succeed

2. **Optional: Dual-Write to Qdrant**:

   **If Qdrant MCP server available**, also store to vector database:

   ```
   store_memory(
       document="<full formatted memory text>",
       metadata={
           "memory_level": "project",
           "memory_type": "<episodic|procedural|semantic>",
           "file_path": "<relative path from project-memory-store/>",
           "skill_root": "project-memory-store",
           "tags": ["<tag1>", "<tag2>"],
           "title": "<memory title>",
           "created_at": "<ISO timestamp>",
           "last_synced": "<ISO timestamp>"
       },
       memory_level="project"
   )
   ```

   - If dual-write fails: Log warning but continue (file write already succeeded)
   - If tool unavailable: Skip silently

3. **Cross-promotion check**: If generalized pattern is universal (not project-specific):
   - Invoke coder-memory-store skill to store universal version
   - Keep project-specific version in project-memory with note: "**See also:** coder-memory for universal pattern"

4. If file becomes "too long" with unrelated info:
   - Create subdirectory with topic name
   - Move related memories to new file in subdirectory
   - Create README.md in subdirectory as overview

5. Update parent README.md to reference new structure

---

## PHASE 5: Update Skill Metadata

If directory structure changed (new subdirectories created):
- Update this SKILL.md frontmatter `description` if needed
- Ensure future recalls can discover new structure

---

## Final Report

**Format**:
```
✅ Project Memory Storage Complete

**Project**: <project name>
**Insights Extracted**: <number> project-specific details
  - Episodic: <number>
  - Procedural: <number>
  - Semantic: <number>

**Storage Actions**:
  - Merged: <number>
  - Updated: <number>
  - Generalized: <number>
  - Created: <number>

**Cross-Promotion**:
  - Promoted to coder-memory (universal patterns): <number>

**Quality Check**:
  - ✓ All insights are project-specific
  - ✓ All insights are non-obvious
  - ✓ File organization maintained (max 2-level depth)
  - ✓ Universal patterns promoted to coder-memory
```

**If 0 insights extracted**:
```
✅ Project Memory Storage Complete

**Insights Extracted**: 0 (conversation contained universal patterns or routine work)

Consider using coder-memory-store for universal patterns.
```

---

## Self-Maintenance Note

This skill's memory files can be refactored by project-memory-recall when organization becomes unclear. The recall skill will invoke general-purpose agent to reorganize structure if needed.

---

## Tool Usage

**CRITICAL**: Invoke via Task tool with general-purpose agent. Never execute directly in main context.
