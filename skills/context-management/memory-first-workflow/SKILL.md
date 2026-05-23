---
name: memory-first-workflow
description: Workflow for checking memory before code exploration. Auto-loaded when answering questions about code, architecture, or patterns.
user-invocable: false
---

# Memory-First Research Pattern

When answering questions about code, architecture, patterns, decisions, or technical choices, follow this workflow:

## Step 1: Query Memory First

Before reading files or exploring code, check if memory already has the answer:

```
memory.recall "<topic>"
```

**Example queries:**
- `memory.recall "authentication flow"`
- `memory.recall "database choice"`
- `memory.recall "error handling patterns"`

## Step 2: Use Specialized Shortcuts

For specific types of questions, use targeted memory tools:

### Before Implementing Features
```
memory.decisions
```
Returns architectural decisions and constraints that may affect implementation.

### Before Working with Frameworks/Databases
```
memory.architecture
```
Returns framework choices, database selection, and architectural patterns.

### Before Writing Code
```
memory.conventions
```
Returns coding style, naming conventions, and project standards.

### If Finding Contradictions
```
memory.conflicts
```
Returns open disputes that need resolution.

## Step 3: Evaluate Memory Results

**If memory has sufficient information:**
- Answer using recalled facts
- Cite fact IDs or sources: "From memory (fact #42): ..."
- Avoid unnecessary file reads

**If memory has partial information:**
- Share what memory knows
- Note what needs investigation: "Memory shows we use PostgreSQL, but I need to check the connection pooling setup..."
- Proceed to file exploration for missing details

**If memory has no information:**
- Note explicitly: "Memory has no prior knowledge about [topic]"
- Proceed to file exploration
- After learning, consider if this should be stored in memory

## Step 4: Explore Code (Only If Needed)

When memory is insufficient, use file exploration tools:
- `Read` for specific files
- `Grep` for searching content
- `Glob` for finding files by pattern
- `Task` (Explore agent) for broad investigations

## Step 5: Distinguish Sources

When presenting findings, clearly separate:
- **Recalled knowledge:** "From memory: We use RSpec for testing"
- **Discovered information:** "From code exploration: Found additional test helper in `spec/support/`"

## Why This Pattern Matters

### Saves Time
Memory provides instant access to distilled knowledge without re-reading hundreds of files.

### Provides Context
Past decisions, lessons learned, and rationale are preserved in memory.

### Reduces Tokens
Recalled facts are concise compared to reading entire files.

### Ensures Consistency
Prevents contradicting previous decisions or duplicating solved problems.

### Improves Quality
Understanding past context leads to better decisions aligned with project history.

## Anti-Patterns to Avoid

❌ **Don't skip memory checks:**
```
User: "What database do we use?"
Bad: *immediately reads config files*
Good: *checks memory.architecture first*
```

❌ **Don't assume memory is wrong:**
```
Bad: "Memory says PostgreSQL, let me verify by reading the config..."
Good: "Memory says PostgreSQL. Need any specific config details?"
```

❌ **Don't ignore memory conflicts:**
```
Bad: *finds conflict, picks one arbitrarily*
Good: "memory.conflicts shows authentication method disputed—let me investigate and resolve"
```

## Example Workflow

**User asks:** "How do we handle errors in API responses?"

**Step 1:** Check memory
```
memory.recall "error handling API"
memory.conventions
```

**Step 2:** Evaluate results
- Memory shows: "Convention: API errors return JSON with `error` and `message` keys"
- Memory shows: "Decision: 4xx for client errors, 5xx for server errors"

**Step 3:** Answer with citations
"From memory: We handle API errors by returning JSON with `error` and `message` keys. Client errors use 4xx status codes, server errors use 5xx. Is there a specific error case you're working with?"

**Step 4:** Only if needed, explore code
If user asks: "Show me the error middleware"
*Then* use Read/Grep to find the implementation.

---

This workflow is automatically loaded when you ask technical questions. You don't need to invoke it manually—it guides Claude's research process behind the scenes.
