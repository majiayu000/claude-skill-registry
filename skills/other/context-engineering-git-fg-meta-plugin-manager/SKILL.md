---
name: context-engineering
description: "Manage filesystem context for large data offloading, cross-session state persistence, and token optimization. Use when managing persistent state, offloading large context, or reducing token usage across sessions. Includes write-once/read-selective patterns, dynamic file discovery, and context reconstruction. Not for small temporary data, in-memory variables, or simple caching."
---

# Filesystem-Based Context Engineering

<mission_control>
<objective>Manage filesystem context for unlimited capacity through dynamic discovery, offloading large context to files and persisting state between sessions</objective>
<success_criteria>Context efficiently managed with write-once/read-selective patterns, reducing token usage while maintaining full data availability</success_criteria>
</mission_control>

## The Path to High-Efficiency Context Management

<interaction_schema>
WRITE_ONCE → READ_SELECTIVELY → DISCOVER_DYNAMICALLY
</interaction_schema>

The filesystem provides unlimited context capacity through dynamic discovery. Instead of stuffing everything into the context window, agents write once and read selectively, pulling relevant context on demand.

## Core Concept

**Problem**: Context windows are limited but tasks often require more information than fits

**Solution**: Use filesystem as persistent layer where agents:

1. Write once (large outputs, state, plans)
2. Read selectively (targeted retrieval via search)
3. Discover dynamically (find relevant files on-demand)

**Benefit**: Unlimited context capacity with natural progressive disclosure

## Quick Start

**Write large outputs:** Store to files instead of returning to context

**Read selectively:** Use Grep/Glob to pull relevant portions on-demand

**Persist state:** Write-once pattern for cross-session continuity

**Why:** Filesystem provides unlimited context—write once, read selectively, reduces token usage.

## Navigation

| If you need...          | Read...                                            |
| :---------------------- | :------------------------------------------------- |
| Understand core concept | ## Core Concept                                    |
| Write large outputs     | ## Quick Start → Write large outputs               |
| Read selectively        | ## Quick Start → Read selectively                  |
| Persist state           | ## Quick Start → Persist state                     |
| Interaction pattern     | <interaction_schema> → WRITE_ONCE → READ_SELECTIVE |
| Context reconstruction  | See memory-persistence skill                       |

## Operational Patterns

- **Content Search**: Search file contents for context retrieval
- **Discovery**: Locate files matching patterns for context reconstruction
- **Tracking**: Maintain a visible task list for context operations
- **Execution**: Execute system commands for file operations

## Context Engineering Patterns

### Pattern 1: Filesystem as Scratch Pad

**Problem**: Tool calls return massive outputs (10k+ tokens for web search, hundreds of rows for database queries). If this enters message history, it remains for entire conversation, bloating tokens and degrading attention.

**Solution**: Write large tool outputs to files instead of returning to context. Agent uses targeted retrieval to extract only relevant portions.

**Implementation**:

```python
def handle_tool_output(output: str, threshold: int = 2000) -> str:
    if len(output) < threshold:
        return output  # Small output, return directly

    # Write to scratch pad
    file_path = f"scratch/{tool_name}_{timestamp}.txt"
    write_file(file_path, output)

    # Return reference with summary
    summary = extract_summary(output, max_tokens=200)
    return f"[Output written to {file_path}. Summary: {summary}]"
```

**Usage**:

- Web search results → `scratch/web_search_20260126_143022.txt`
- Database queries → `scratch/db_query_users_active.txt`
- API responses → `scratch/api_response_20260126_143045.json`

**Benefits**:

- Reduces token accumulation over long conversations
- Preserves full output for later reference
- Enables targeted retrieval instead of carrying everything
- Natural progressive disclosure

### Pattern 2: Plan Persistence

**Problem**: Long-horizon tasks require plans. But as conversations extend, plans fall out of attention or get lost to summarization. Agent loses track of objectives.

**Solution**: Write plans to filesystem. Agent can re-read plan anytime to re-orient.

**Implementation**:

```yaml
# scratch/current_plan.yaml
objective: "Refactor authentication module"
status: in_progress
steps:
  - id: 1
    description: "Audit current auth endpoints"
    status: completed
  - id: 2
    description: "Design new token validation flow"
    status: in_progress
  - id: 3
    description: "Implement and test changes"
    status: pending

progress:
  current_step: 2
  blockers: ["Waiting for security review"]
  next_action: "Complete token validation design"
```

**Usage**:

- Agent reads `scratch/current_plan.yaml` at start of each turn
- Updates progress as work completes
- Re-orients when context degrades

**Benefits**:

- Maintains objective visibility throughout long tasks
- Survives context compaction
- Enables "manipulating attention through recitation"

### Pattern 3: Sub-Agent Communication via Filesystem

**Problem**: In multi-agent systems, sub-agents report to coordinator through message passing. This creates "telephone game" where information degrades through summarization at each hop.

**Solution**: Sub-agents write findings directly to filesystem. Coordinator reads files directly, bypassing intermediate passing.

**Implementation**:

```
workspace/
  agents/
    research_agent/
      findings.md        # Research agent writes here
      sources.jsonl      # Source tracking
    code_agent/
      changes.md         # Code agent writes here
      test_results.txt   # Test output
  coordinator/
    synthesis.md         # Coordinator reads outputs, writes synthesis
```

**Usage**:

- Research agent: `workspace/agents/research_agent/findings.md`
- Code agent: `workspace/agents/code_agent/changes.md`
- Coordinator: reads both, writes synthesis

**Benefits**:

- Preserves fidelity (no telephone game)
- Reduces coordinator context accumulation
- Enables asynchronous collaboration
- Natural audit trail

### Pattern 4: Dynamic Skill Loading

**Problem**: Agents may have many skills/instructions, but most irrelevant to any given task. Stuffing all into system prompt wastes tokens and can confuse with contradictory guidance.

**Solution**: Store skills as files. Include only skill names/brief descriptions in static context. Load relevant skill content when task requires it.

**Implementation**:

```markdown
Available skills (load with read_file when relevant):

- database-optimization: Query tuning and indexing strategies
- api-design: REST/GraphQL best practices
- testing-strategies: Unit, integration, and e2e patterns
- security-review: OWASP Top 10, authentication patterns
```

**Usage**:

```python
# Agent working on database task
skill_content = read_file("skills/database-optimization/SKILL.md")

# Agent working on API task
skill_content = read_file("skills/api-design/SKILL.md")
```

**Benefits**:

- Minimal static context
- On-demand skill activation
- No contradictory guidance
- Scales to hundreds of skills

### Pattern 5: Terminal and Log Persistence

**Problem**: Terminal output from long-running processes accumulates rapidly. Copying/pasting into agent input is manual and inefficient.

**Solution**: Sync terminal output to files automatically. Agent greps for relevant sections without loading entire histories.

**Implementation**:

```bash
# Auto-sync terminal to file
script -c "npm run dev" scratch/terminal.log

# Agent searches for specific patterns
grep "ERROR" scratch/terminal.log
grep -A5 "failed" scratch/terminal.log
```

**Benefits**:

- Automatic log capture
- Targeted error finding
- No manual copy/paste
- Historical terminal access

## Filesystem Navigation

### Discovery Patterns

**Find files by name**:

```bash
Glob patterns:
- "**/*.yaml" - All YAML files
- "**/scratch/*" - Scratch pad directory
- "**/plans/*" - Plan files
- "**/logs/*" - Log files
```

**Search file contents**:

```bash
Grep patterns:
- "TODO|FIXME|BUG" - Find action items
- "ERROR|Exception" - Find errors
- "summary|conclusion" - Find summaries
- "^# .*" - Find headings
```

**Targeted reading**:

```bash
Read specific sections:
- First 50 lines: `read_file(path, limit=50)`
- Last 50 lines: `read_file(path, offset=-50)`
- Around pattern: `grep(pattern)`, then `read_file(path, offset=X, limit=Y)`
```

### File Metadata Hints

**File sizes suggest complexity**:

- Small (<1KB): summaries, metadata
- Medium (1-10KB): full outputs, reports
- Large (>10KB): raw data, logs

**Naming conventions**:

- `YYYYMMDD_HHMMSS_*` - Timestamped files
- `*_summary.*` - Summarized outputs
- `*_raw.*` - Raw data
- `current_*.*` - Current state

**Timestamps**:

- Newer files likely more relevant
- Timestamps show activity patterns
- Enable time-based filtering

## JSONL Append-Only Design

**Pattern**: All logs use JSONL (JSON Lines) format

**Benefits**:

- Agent-friendly parsing
- History preservation
- Pattern analysis capability
- Never-delete integrity

**Example**:

```jsonl
{"timestamp": "2026-01-26T14:30:00Z", "type": "post", "content": "...", "status": "published"}
{"timestamp": "2026-01-26T14:35:00Z", "type": "contact", "name": "Sarah", "updated": true}
{"timestamp": "2026-01-26T14:40:00Z", "type": "plan_update", "step": 2, "status": "completed"}
```

**Reading JSONL**:

```python
# Read as list of dicts
logs = [json.loads(line) for line in open('logs.jsonl')]

# Filter by type
posts = [log for log in logs if log['type'] == 'post']

# Query by timestamp
recent = [log for log in logs if log['timestamp'] > '2026-01-26']
```

## Progressive Disclosure in Filesystem

### Level 1: Metadata

```markdown
# Component Index

skills/my-skill/
├── overview.yaml # 200 tokens - auto-loaded
├── trigger_phrases.md # 100 tokens - auto-loaded
└── references/ # On-demand
├── examples/
└── patterns/
```

### Level 2: Instructions

```markdown
# Full Skill (1500 tokens)

- Load when skill activated
- Contains all instructions
- Progressive disclosure enabled
```

### Level 3: Data

```markdown
# References/ (As needed)

- examples/ - Usage examples
- patterns/ - Implementation patterns
- scripts/ - Automation scripts
- data/ - Sample data
```

## Best Practices

### File Organization

1. **Use descriptive names**: `auth_plan_20260126.yaml` not `plan1.yaml`
2. **Timestamp files**: `scratch/web_search_20260126_143022.txt`
3. **Group related files**: `evidence/`, `scratch/`, `context/`
4. **Use extensions**: `.yaml`, `.jsonl`, `.md`, `.txt`

### Content Guidelines

1. **Write summaries**: Extract key info for quick reference
2. **Preserve full data**: Keep raw outputs for later analysis
3. **Use structured formats**: YAML, JSONL for machine-readability
4. **Include metadata**: Timestamps, types, status

### Performance

1. **Write once, read many**: Optimize for read patterns
2. **Use targeted reads**: Line ranges, not full files
3. **Search before read**: Grep to find relevant sections
4. **Cache frequently accessed**: Keep metadata in memory

## Example Workflow

## Guidelines

1. **Write once, read selectively** - Don't return large outputs to context
2. **Use descriptive names** - Enable quick discovery
3. **Timestamp files** - Show temporal relationships
4. **Preserve full data** - Keep raw outputs for analysis
5. **Structure formats** - YAML/JSONL for machine-readability
6. **Search before read** - Grep to find relevant sections
7. **Progressive disclosure** - Load only what you need
8. **Append-only logs** - Preserve history for pattern analysis

## References

**Related Concepts**:

- Progressive disclosure principles for context loading
- Multi-dimensional quality assessment for context evaluation
- Progressive refinement for targeted context discovery
- Context management patterns (this skill's domain)

**For Complex Discovery**:

When basic search is insufficient, combine search strategies:

```
# Basic search (grep/glob)
grep("pattern", "**/*.ts")

# Multi-stage search for refinement
1. Broad grep for candidate files
2. Narrow with specific patterns
3. Read selected files for targeted content
```

**Multi-stage discovery enhances context-engineering by**:

- **Broad then narrow**: Start wide, progressively refine
- **Pattern evolution**: Adjust search based on findings
- **Selective reading**: Read only relevant sections from discovered files
- **Termination**: Stop when sufficient context gathered

**Integration**:

- Use broad search to discover relevant files
- Use context-engineering to cache discovered file metadata
- Combined: Discovery → Metadata caching → Targeted retrieval

**Key Principle**: Filesystem provides unlimited context capacity through dynamic discovery. Write once, read selectively, discover on-demand.

---

## Common Mistakes to Avoid

### Mistake 1: Returning Large Outputs to Context

❌ **Wrong:**
```python
result = perform_web_search(query)
return result  # 10k+ tokens added to context
```

✅ **Correct:**
```python
result = perform_web_search(query)
write_file("scratch/search_results.json", result)
return f"[Output written to scratch/search_results.json. Summary: {extract_summary(result)}]"
```

### Mistake 2: Reading Full Files Instead of Targeted Sections

❌ **Wrong:**
```python
data = read_file("large_log_file.txt")  # Full file into context
```

✅ **Correct:**
```python
errors = grep("ERROR", "large_log_file.txt")  # Find relevant lines
relevant_section = read_file("large_log_file.txt", offset=100, limit=50)  # Specific section
```

### Mistake 3: Not Using Timestamped Filenames

❌ **Wrong:**
```bash
write_file("output.json", data)  # Overwrites previous output
```

✅ **Correct:**
```bash
timestamp=$(date +%Y%m%d_%H%M%S)
write_file "output_${timestamp}.json" data
```

### Mistake 4: Storing Everything Instead of Summarizing

❌ **Wrong:**
```python
for tool_call in all_tool_calls:
    write_file("all_calls.txt", all_tool_calls)  # Dumps everything
```

✅ **Correct:**
```python
write_file("call_summary.yaml", summarize_tool_calls(all_tool_calls))
write_file("call_details/", individual_call_files)  # Only if truly needed
```

### Mistake 5: Using Non-Descriptive Filenames

❌ **Wrong:**
```bash
write_file("plan1.txt", plan)
write_file("data.json", results)
write_file("notes.txt", notes)
```

✅ **Correct:**
```bash
write_file("scratch/auth_refactor_plan_20260130.yaml", plan)
write_file("scratch/user_query_results_20260130.jsonl", results)
write_file("scratch/meeting_notes_20260130.md", notes)
```

---

## Validation Checklist

Before claiming filesystem context complete:

**Write Operations:**
- [ ] Large outputs written to files instead of returned to context
- [ ] Timestamped or descriptive filenames used
- [ ] Summaries extracted for quick reference

**Read Operations:**
- [ ] Targeted reads (line ranges) used instead of full files
- [ ] Grep/Glob to find relevant sections before reading
- [ ] Only necessary data loaded into context

**Organization:**
- [ ] Consistent directory structure (scratch/, context/, logs/)
- [ ] Descriptive filenames enable quick discovery
- [ ] Related files grouped together

**Persistence:**
- [ ] Plans and state persisted for cross-session continuity
- [ ] JSONL format used for append-only logs
- [ ] History preserved for pattern analysis

---

## Best Practices Summary

✅ **DO:**
- Write large outputs to files instead of returning to context
- Use timestamps in filenames for temporal ordering
- Read specific sections (line ranges, grep results) instead of full files
- Use descriptive filenames that indicate content
- Group related files in consistent directories
- Use JSONL format for append-only logs
- Extract summaries for quick reference

❌ **DON'T:**
- Return large tool outputs directly to context
- view_file full files when only specific sections are needed
- Use generic filenames like "output.txt" or "notes.txt"
- Dump everything without organization
- Delete log files (preserve history)
- Skip summaries when writing large outputs

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
**Portability Invariant**: All components MUST be self-contained with zero CLAUDE.md, CLAUDE.local.md, or .claude/rules/ dependencies to enable fork isolation. When referencing other skills, use: "invoke `skill-name`" or "invoke `skill-name` and read its file". Never cite absolute paths or reference .claude/rules/ from within skills.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

## Recognition Questions

| Question | Recognition |
| :------- | :---------- |
| Would Claude know this without being told? | Delete (zero delta) |
| Can this work standalone? | Fix if no (non-self-sufficient) |
| Did I read the actual file, or just see it in grep? | Verify before claiming |

---

## Validation Checklist

Before claiming filesystem context complete:

- [ ] Large context offloaded to files
- [ ] Write-once semantics enforced
- [ ] Cross-session state persisted
- [ ] Token optimization achieved

