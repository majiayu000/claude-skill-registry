---
name: filesystem-context
description: "Manage filesystem context for offloading large context to files, persisting state between sessions, and reducing token usage. Use when managing cross-session state or context persistence. Not for small temporary data or in-memory variables."
---

# Filesystem-Based Context Engineering

<mission_control>
<objective>Manage filesystem context for unlimited capacity through dynamic discovery, offloading large context to files and persisting state between sessions</objective>
<success_criteria>Context efficiently managed with write-once/read-selective patterns, reducing token usage while maintaining full data availability</success_criteria>
</mission_control>

<trigger>When offloading large context to files, persisting state between sessions, or reducing token usage. Not for: Small temporary data or in-memory variables.</trigger>

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

**Related Skills**:

- `context-fundamentals` - Progressive disclosure principles
- `evaluation` - Multi-dimensional quality assessment
- `iterative-retrieval` - Progressive refinement for targeted context discovery
- `filesystem-context` - Context management patterns (this skill)

**For Complex Discovery**:

When basic search is insufficient, use **iterative-retrieval** for targeted context discovery:

```
# Basic search (grep/glob)
grep("pattern", "**/*.ts")

# Iterative retrieval with progressive refinement
/search "authentication patterns in TypeScript"
```

**iterative-retrieval** enhances filesystem-context by:

- **4-phase loop**: DISPATCH → EVALUATE → REFINE → LOOP
- **Relevance scoring**: Identifies which files to read from filesystem
- **Progressive refinement**: Discovers relevant files systematically
- **Termination conditions**: Stops when sufficient high-relevance files found

**Integration**:

- Use iterative-retrieval to discover relevant files
- Use filesystem-context to persist discovered files for selective retrieval
- Combined: Discovery → Storage → Targeted retrieval

**Key Principle**: Filesystem provides unlimited context capacity through dynamic discovery. Write once, read selectively, discover on-demand.

---

<critical_constraint>
MANDATORY: Write large outputs to files, not to context
MANDATORY: Use descriptive, timestamped filenames for traceability
MANDATORY: Search before reading (find relevant sections first)
MANDATORY: Use structured formats (YAML/JSONL) for machine-readability
MANDATORY: Never return full large outputs to context (use references)
No exceptions. Filesystem context enables unlimited capacity.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
