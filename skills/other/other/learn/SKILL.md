---
name: learn
description: Extract and persist insights from the current conversation to the knowledge base
user_invokable: true
---

# Learn

Extract insights from the current conversation and persist them to the project's knowledge base.

## What This Does

Analyzes the conversation context to identify:
- **Patterns**: Approaches that worked well in this project
- **Quirks**: Project-specific oddities or non-standard behaviors discovered
- **Decisions**: Architectural or implementation choices made with their rationale

These insights survive session boundaries and context compaction, building a persistent understanding of the project over time.

## Instructions

1. **Analyze the conversation** looking for:
   - Successful problem-solving approaches that could apply again
   - Unusual behaviors or gotchas discovered about the codebase
   - Decisions made and why (architectural choices, library selections, patterns chosen)

2. **Categorize each insight** as pattern, quirk, or decision

3. **Format and append** to the appropriate file in `knowledge/learnings/`:
   - `patterns.md` - What works well
   - `quirks.md` - Unexpected behaviors
   - `decisions.md` - Choices with rationale

4. **Update metadata** in each file's frontmatter (entry_count, last_updated)

5. **Update state** in `knowledge/state.json`:
   - Set `last_extraction` to current timestamp
   - Increment `extraction_count`
   - Reset `queries_since_extraction` to 0

6. **Report** what was learned to the user

## Entry Format

### Pattern Entry
```markdown
## Pattern: [Short descriptive title]
- **Discovered:** [ISO date]
- **Context:** [What task/problem led to this discovery]
- **Insight:** [What approach works well and why]
- **Confidence:** high|medium|low
```

### Quirk Entry
```markdown
## Quirk: [Short descriptive title]
- **Discovered:** [ISO date]
- **Location:** [File/module/area where this applies]
- **Behavior:** [What's unusual or unexpected]
- **Workaround:** [How to handle it]
- **Confidence:** high|medium|low
```

### Decision Entry
```markdown
## Decision: [Short descriptive title]
- **Made:** [ISO date]
- **Context:** [What prompted this decision]
- **Choice:** [What was decided]
- **Rationale:** [Why this choice over alternatives]
- **Confidence:** high|medium|low
```

## Confidence Levels

- **high**: Clear, verified insight with strong evidence
- **medium**: Reasonable inference, likely correct
- **low**: Tentative observation, needs validation

Only high and medium confidence insights influence routing decisions.

## Steps

1. Review the conversation for extractable insights
2. For each insight found:
   - Read the target file (patterns.md, quirks.md, or decisions.md)
   - Check for duplicates (skip if similar insight exists)
   - Append new entry in the format above
   - Update frontmatter (increment entry_count, set last_updated)
3. Read and update `knowledge/state.json`
4. Report summary to user:
   ```
   Knowledge Extraction Complete
   ─────────────────────────────
   Extracted:
     [Pattern] "Title of pattern learned"
     [Quirk] "Title of quirk discovered"
     [Decision] "Title of decision recorded"

   Knowledge base now contains:
     - X patterns
     - Y quirks
     - Z decisions
   ```

## Example Extraction

From a conversation where we debugged an auth issue:

**Quirk extracted:**
```markdown
## Quirk: Auth tokens require base64 padding
- **Discovered:** 2026-01-08
- **Location:** src/auth/tokenService.ts
- **Behavior:** JWT tokens in this codebase use non-standard base64 without padding, causing standard decoders to fail
- **Workaround:** Use the custom `decodeToken()` helper instead of atob()
- **Confidence:** high
```

## Notes

- This command extracts insights from the CURRENT conversation
- For continuous extraction, use `/learn-on` instead
- Insights should be project-specific, not generic programming knowledge
- Avoid extracting obvious or trivial information
- When in doubt about confidence, use "medium"
