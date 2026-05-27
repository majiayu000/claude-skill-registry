---
name: grep-and-read
description: Find and read multiple files in one operation (50-70% faster for exploration)
allowed-tools: Grep, Read, Bash
---

# Grep and Read Skill

**Purpose**: Search for pattern and read all matching files in a single coordinated operation, eliminating sequential round-trips.

**Performance**: 50-70% time savings, 4000-8000 token savings compared to sequential Grep → Read → Read → Read pattern.

**When to Use**:
- Exploring codebase for specific functionality
- Finding all files containing a pattern
- Researching implementation approaches
- Investigating errors or bugs across multiple files

## Anti-Pattern This Skill Replaces

❌ **INEFFICIENT PATTERN** (4 messages, 9-12 seconds):
```
Message 1: Grep "FormattingRule" → returns 5 files
  [Wait for response ~2.5s]

Message 2: Read src/main/java/.../FormattingRule.java
  [Wait for response ~2.5s]

Message 3: Read src/test/java/.../FormattingRuleTest.java
  [Wait for response ~2.5s]

Message 4: Read docs/architecture.md
  [Wait for response ~2.5s]

→ Impact: 4 round-trips = ~10 seconds, ~12,000 tokens
→ Wasted: 3 avoidable round-trips
```

✅ **EFFICIENT PATTERN** (1 message, 3-4 seconds):
```
Message 1: Skill grep-and-read pattern="FormattingRule" max_files=5
  - Grep finds matches
  - Read all matching files in parallel
  - Return consolidated output
  [Wait for response ~3.5s]

→ Impact: 1 round-trip = ~3.5 seconds, ~4,000 tokens
→ Saved: 3 round-trips = 6.5 seconds (65% faster), 8,000 tokens
```

## Skill Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `pattern` | ✅ Yes | - | Grep pattern to search for (regex supported) |
| `path` | No | `.` | Directory to search in |
| `glob` | No | - | File type filter (e.g., "*.java", "*.md") |
| `max_files` | No | 5 | Maximum number of files to read |
| `context_lines` | No | 100 | Lines to read per file (0 = all) |
| `case_sensitive` | No | true | Case-sensitive search |

## Skill Workflow

### Phase 1: Search for Pattern

Use Grep tool to find all files containing the pattern:

```bash
# Search for pattern with optional filters
Grep: pattern="{pattern}"
  path="{path}"
  glob="{glob}"
  output_mode="files_with_matches"
  -i={!case_sensitive}
```

**Example**:
```
Grep: pattern="FormattingRule"
  path="/workspace/main"
  glob="*.java"
  output_mode="files_with_matches"
```

**Output**: List of file paths
```
src/main/java/io/github/cowwoc/styler/formatter/FormattingRule.java
src/main/java/io/github/cowwoc/styler/formatter/FormattingRuleImpl.java
src/test/java/io/github/cowwoc/styler/formatter/FormattingRuleTest.java
```

### Phase 2: Read All Matching Files (Parallel)

Read all found files in a single message using multiple Read tool calls:

```bash
# Parallel read invocations in one message
Read: /workspace/main/src/main/java/.../FormattingRule.java
Read: /workspace/main/src/main/java/.../FormattingRuleImpl.java
Read: /workspace/main/src/test/java/.../FormattingRuleTest.java
```

**If max_files exceeded**: Show first N files, report total found
**If context_lines limited**: Read first N lines of each file

### Phase 3: Consolidate and Report

Provide summary and consolidated output:

```
═══════════════════════════════════════════════════════════
GREP AND READ SUMMARY
═══════════════════════════════════════════════════════════
Pattern:        FormattingRule
Files Found:    3
Files Read:     3
Total Size:     ~15KB
Time Saved:     ~6.5 seconds (vs sequential)
Tokens Saved:   ~8,000 tokens
═══════════════════════════════════════════════════════════

FILES READ:

───────────────────────────────────────────────────────────
FILE 1: src/main/java/.../FormattingRule.java
───────────────────────────────────────────────────────────
[file contents...]

───────────────────────────────────────────────────────────
FILE 2: src/main/java/.../FormattingRuleImpl.java
───────────────────────────────────────────────────────────
[file contents...]

───────────────────────────────────────────────────────────
FILE 3: src/test/java/.../FormattingRuleTest.java
───────────────────────────────────────────────────────────
[file contents...]
```

## Usage Examples

### Example 1: Explore API Implementation

**Goal**: Understand how "FormattingRule" is implemented

**Command**:
```bash
Skill: grep-and-read
  pattern="FormattingRule"
  path="/workspace/main"
  glob="*.java"
  max_files=5
```

**Benefit**: Get complete picture of implementation in one round-trip

### Example 2: Research Error Handling

**Goal**: Find all files handling "ValidationException"

**Command**:
```bash
Skill: grep-and-read
  pattern="ValidationException"
  path="/workspace/main/src"
  max_files=10
  context_lines=50
```

**Benefit**: See all error handling patterns without multiple reads

### Example 3: Documentation Research

**Goal**: Find all documentation mentioning "task protocol"

**Command**:
```bash
Skill: grep-and-read
  pattern="task protocol"
  path="/workspace/main/docs"
  glob="*.md"
  case_sensitive=false
  context_lines=0
```

**Benefit**: Read all relevant docs in one operation

### Example 4: Test Coverage Analysis

**Goal**: Find all tests for "Formatter" classes

**Command**:
```bash
Skill: grep-and-read
  pattern="class.*Formatter.*Test"
  path="/workspace/main/src/test"
  glob="*Test.java"
  max_files=8
```

**Benefit**: See complete test coverage at once

## Edge Cases

### Too Many Matches

**Problem**: Pattern matches 50+ files

**Solution**:
1. Report total matches found
2. Read first `max_files` only
3. Suggest more specific pattern or glob filter

**Output**:
```
⚠️  Pattern matched 53 files
📊 Reading first 5 files (use max_files parameter to adjust)
💡 Suggestion: Refine pattern or add glob filter for more targeted search
```

### Large Files

**Problem**: Files exceed context window

**Solution**:
1. Use `context_lines` parameter to limit output
2. Read first N lines of each file
3. Report truncation with file statistics

**Output**:
```
📄 File: FormattingRule.java
   Total lines: 1500
   Read lines: 100 (first 100)
   [... file contents ...]
   [... truncated: showing 100 of 1500 lines ...]
```

### No Matches

**Problem**: Pattern doesn't match any files

**Solution**:
1. Report no matches found
2. Suggest alternative search strategies
3. Verify search path and pattern

**Output**:
```
❌ No files found matching pattern: "FooBar"
📂 Search path: /workspace/main
🔍 Suggestions:
   - Try case-insensitive search (case_sensitive=false)
   - Broaden pattern (use wildcards)
   - Check search path is correct
```

## Performance Comparison

### Scenario: Finding and reading 5 files

| Approach | Messages | Time | Tokens | Savings |
|----------|----------|------|--------|---------|
| **Sequential** (Grep + 5 Reads) | 6 | ~15s | ~18,000 | Baseline |
| **grep-and-read Skill** | 1 | ~4s | ~6,000 | 73% time, 67% tokens |

### Scenario: Finding and reading 3 files

| Approach | Messages | Time | Tokens | Savings |
|----------|----------|------|--------|---------|
| **Sequential** (Grep + 3 Reads) | 4 | ~10s | ~12,000 | Baseline |
| **grep-and-read Skill** | 1 | ~3s | ~4,000 | 70% time, 67% tokens |

## Implementation Notes

### Parallel Read Execution

When reading multiple files, use Claude Code's parallel tool execution feature:

```python
# In skill implementation
def execute_skill(pattern, max_files):
    # Step 1: Grep for matches
    matches = grep_tool(pattern, output_mode="files_with_matches")

    # Step 2: Limit to max_files
    files_to_read = matches[:max_files]

    # Step 3: Generate parallel Read tool calls
    # IMPORTANT: Return all Read tool calls in SAME message
    return [
        {"tool": "Read", "file_path": f}
        for f in files_to_read
    ]
```

### Memory Considerations

For very large result sets:
- Default `max_files=5` prevents context overflow
- `context_lines` parameter limits per-file output
- Total output capped at ~50KB to stay within token limits

### Error Handling

**Grep fails**: Report error, suggest pattern refinement
**Read fails**: Continue reading other files, report which failed
**Permission denied**: Skip inaccessible files, report count

## When NOT to Use This Skill

❌ **Don't use when**:
- You need only file paths (use Grep alone with `output_mode="files_with_matches"`)
- You need specific line context (use Grep with `output_mode="content"` and `-C` flag)
- Files are too large (> 1000 lines each) and you don't know which parts to read
- Pattern is exploratory and you need to see matches before reading

✅ **DO use when**:
- You know you'll read the matching files
- Files are reasonably sized (< 1000 lines each)
- You want comprehensive view of pattern usage
- Exploring codebase for implementation understanding

## Integration with Existing Tools

### Complements batch-read Skill

**batch-read**: Use when you KNOW which files to read
```bash
# You already know the files
batch-read: "task-protocol" --type md --max-files 5
```

**grep-and-read**: Use when you need to FIND files first
```bash
# You need to discover the files
grep-and-read: pattern="task protocol" glob="*.md"
```

### Complements Grep Tool

**Grep (content mode)**: Use for seeing match context
```bash
# See lines around matches
Grep: pattern="FormattingRule" output_mode="content" -C=3
```

**grep-and-read**: Use for reading entire matching files
```bash
# Read complete files
grep-and-read: pattern="FormattingRule" max_files=5
```

## Success Metrics

### Adoption
- **Usage Frequency**: Count of skill invocations per week
- **User Preference**: % of Grep operations followed by grep-and-read vs manual reads
- **Pattern Refinement**: % of skill calls that required pattern adjustment

### Performance
- **Time Savings**: Average seconds saved per invocation
- **Token Savings**: Average tokens saved per invocation
- **Throughput**: Files processed per minute

### Quality
- **Match Accuracy**: % of reads that were relevant to user's goal
- **Coverage**: % of relevant files captured in max_files limit
- **User Satisfaction**: Feedback on result quality

## Future Enhancements

### Smart File Prioritization

Instead of reading first N files:
- Prioritize by file type (source > test > docs)
- Prioritize by match density (files with most matches)
- Prioritize by recency (recently modified files first)

### Incremental Reading

For large result sets:
1. Read first batch (e.g., 5 files)
2. Ask user: "Continue reading next 5?"
3. Read next batch if user approves
4. Repeat until all read or user satisfied

### Result Summarization

Add LLM-powered summary:
- "Found 3 implementations of FormattingRule"
- "2 interface definitions, 1 test file"
- "Key patterns: [list common patterns across files]"

### Caching

Cache Grep results temporarily:
- Avoid re-grepping same pattern
- Update cache on file modifications
- Clear cache after 5 minutes

---

**Related Skills**:
- [batch-read](../batch-read/SKILL.md) - Read known files in batch
- [parse-conversation-timeline](../parse-conversation-timeline/SKILL.md) - Analyze session patterns

**Related Tools**:
- [Grep tool](https://docs.claude.com/tools/grep) - Pattern search
- [Read tool](https://docs.claude.com/tools/read) - File reading
- [batch-read.sh script](../../scripts/batch-read.sh) - Batch read script
