---
name: openspec-daem0n-bridge
description: Bridges OpenSpec (spec-driven development) with Daem0n-MCP memory - auto-imports specs, informs proposals with past outcomes, converts archived changes to learnings
---

# OpenSpec-Daem0n Bridge

## Overview

This skill creates a bidirectional bridge between:
- **OpenSpec**: Spec-driven development with formal change proposals
- **Daem0n-MCP**: AI memory system with semantic search and outcome tracking

**The feedback loop:**
```
OpenSpec specs ──────► Daem0n patterns/rules
       ▲                        │
       │                        ▼
  Future specs ◄────── Past outcomes/failures
```

## Auto-Detection

**On session start, after `get_briefing()`:**

Check if `openspec/` directory exists in the project root:

```bash
ls openspec/specs/ 2>/dev/null
```

**If OpenSpec detected AND specs not yet imported:**
1. Announce: "OpenSpec detected. Syncing specs to Daem0n memory..."
2. Execute Workflow 1 (Import) automatically
3. Report summary of imported specs and rules

**How to check if already imported:**
```
recall(topic="openspec", tags=["spec"], limit=1)
```
If results exist with recent timestamps, skip import.

## Workflow 1: Import Specs to Memory

**Triggers:**
- Auto: OpenSpec directory detected on first session
- Manual: "sync specs to memory", "import openspec", "refresh openspec"

### Steps

1. **List all spec directories**
   ```bash
   ls openspec/specs/
   ```

2. **For each spec, read the spec.md file**
   ```bash
   cat openspec/specs/[name]/spec.md
   ```

3. **Parse requirements using these patterns:**

   | Pattern | Extract As |
   |---------|------------|
   | `MUST`, `SHALL`, `REQUIRED` | rule.must_do |
   | `MUST NOT`, `SHALL NOT`, `PROHIBITED` | rule.must_not |
   | `SHOULD`, `RECOMMENDED` | pattern |
   | `SHOULD NOT`, `NOT RECOMMENDED` | warning |
   | `## Purpose` section | pattern (overview) |

4. **Create memories via remember_batch**
   ```
   mcp__daem0nmcp__remember_batch(memories=[
       {
           "category": "pattern",
           "content": "[spec-name]: [overview/purpose summary]",
           "rationale": "OpenSpec specification - source of truth",
           "tags": ["openspec", "spec", "[spec-name]"],
           "file_path": "openspec/specs/[spec-name]/spec.md",
           "context": {
               "openspec_type": "spec",
               "imported_at": "[ISO timestamp]"
           }
       }
       // ... one per spec
   ])
   ```

5. **Create rules from MUST/MUST NOT**
   ```
   mcp__daem0nmcp__add_rule(
       trigger="implementing [spec-name] feature",
       must_do=["[extracted MUST items]"],
       must_not=["[extracted MUST NOT items]"],
       ask_first=["Does this align with the spec?"]
   )
   ```

6. **Report summary**
   ```
   Imported [N] specs as patterns
   Created [M] rules with [X] must_do and [Y] must_not constraints
   Use recall("openspec") to query
   ```

### Memory Mapping Reference

| OpenSpec Element | Daem0n Category | Tags |
|-----------------|-----------------|------|
| spec.md overview | pattern | openspec, spec, [name] |
| MUST requirements | rule.must_do | (in rule, not memory) |
| MUST NOT constraints | rule.must_not | (in rule, not memory) |
| Known limitations | warning | openspec, limitation, [name] |
| Design rationale | learning | openspec, rationale, [name] |

## Workflow 2: Inform Proposal Creation

**Triggers:**
- "prepare proposal for [feature]"
- "check before proposing [feature]"
- "what do I need to know before proposing [feature]"

### Steps

1. **Recall relevant memories**
   ```
   mcp__daem0nmcp__recall(
       topic="[feature description]",
       categories=["pattern", "warning", "decision"]
   )
   ```

2. **Check applicable rules**
   ```
   mcp__daem0nmcp__check_rules(
       action="proposing change for [feature]"
   )
   ```

3. **Recall OpenSpec-specific context**
   ```
   mcp__daem0nmcp__recall(
       topic="openspec [feature]",
       tags=["openspec"]
   )
   ```

4. **If specific files are affected, check them**
   ```
   mcp__daem0nmcp__recall_for_file(
       file_path="openspec/specs/[affected-spec]/spec.md"
   )
   ```

5. **Present findings to user in this format:**
   ```markdown
   # Memory Context for Proposal: [feature]

   ## Relevant Specs
   - [spec-name]: [summary]

   ## Patterns to Follow
   - [pattern 1]
   - [pattern 2]

   ## Warnings to Consider
   - [warning 1] (from past failure)

   ## Past Decisions That May Apply
   - [decision] - worked: [true/false]

   ## Rules to Follow
   When implementing this:
   - MUST: [list]
   - MUST NOT: [list]
   - ASK FIRST: [list]
   ```

6. **If user proceeds, record the intent**
   ```
   mcp__daem0nmcp__remember(
       category="decision",
       content="Creating OpenSpec proposal for [feature]: [brief description]",
       rationale="[user's stated rationale]",
       tags=["openspec", "proposal", "pending"],
       context={
           "openspec_type": "proposal",
           "feature": "[feature]",
           "change_id": "[generated-id or TBD]"
       }
   )
   ```
   **SAVE THE MEMORY ID** - needed for Workflow 3.

## Workflow 3: Archive to Learnings

**Triggers:**
- After `openspec archive [id]` completes
- "record outcome for [change-id]"
- "convert archived change [id] to learnings"

### Steps

1. **Read the archived change**
   ```bash
   cat openspec/changes/archive/[id]/proposal.md
   cat openspec/changes/archive/[id]/tasks.md
   ls openspec/changes/archive/[id]/specs/
   ```

2. **Find the original decision memory**
   ```
   mcp__daem0nmcp__search_memories(
       query="OpenSpec proposal [id]"
   )
   ```
   Or search by feature name if ID wasn't recorded.

3. **Record the outcome**
   ```
   mcp__daem0nmcp__record_outcome(
       memory_id=[found decision id],
       outcome="Completed and archived. [summary of what was implemented]",
       worked=true  // or false if there were issues
   )
   ```

4. **Create learnings from the completed work**
   ```
   mcp__daem0nmcp__remember_batch(memories=[
       {
           "category": "learning",
           "content": "[change-id]: [key lesson from implementation]",
           "rationale": "Extracted from completed OpenSpec change",
           "tags": ["openspec", "completed", "[feature-name]"],
           "context": {
               "openspec_type": "archived_change",
               "change_id": "[id]",
               "archived_at": "[timestamp]"
           }
       }
       // ... one learning per significant insight
   ])
   ```

5. **Link the memories to create causal chain**
   ```
   mcp__daem0nmcp__link_memories(
       source_id=[proposal decision id],
       target_id=[learning id],
       relationship="led_to",
       description="Proposal implementation led to these learnings"
   )
   ```

6. **If spec deltas were applied, update spec memories**

   For each delta in `openspec/changes/archive/[id]/specs/`:
   - ADDED requirements: Create new pattern memories
   - MODIFIED requirements: Update or supersede existing
   - REMOVED requirements: Create warning memories noting removal

## Tags Convention

| Tag | Meaning | When Used |
|-----|---------|-----------|
| `openspec` | Memory from OpenSpec integration | All OpenSpec memories |
| `spec` | From spec.md source of truth | Workflow 1 |
| `proposal` | From change proposal | Workflow 2 |
| `pending` | Proposal not yet archived | Workflow 2 |
| `completed` | From archived change | Workflow 3 |
| `limitation` | Known constraint | Workflow 1 |
| `rationale` | Design reasoning | Workflow 1 |

## Integration with Sacred Covenant

This skill respects the Daem0n's Sacred Covenant:

1. **COMMUNE** - `get_briefing()` must be called first (auto-detection happens after)
2. **SEEK COUNSEL** - Workflow 2 IS the counsel-seeking step for proposals
3. **INSCRIBE** - `remember()` records proposal decisions
4. **SEAL** - `record_outcome()` closes the loop when changes are archived

**Enforcement:**
- Workflow 1 (Import) requires communion (get_briefing called)
- Workflow 2 (Inform) calls context_check internally
- Workflow 3 (Archive) requires the original decision memory to exist

## Parsing OpenSpec Spec Files

### Spec Format Reference

```markdown
# [Spec Title]

## Purpose
[Description - extract as pattern overview]

## Requirements

### Requirement: [Name]
[Text containing MUST/MUST NOT/SHOULD]

#### Scenario: [Description]
- **GIVEN** [condition]
- **WHEN** [action]
- **THEN** [result]
```

### Extraction Regex Patterns

```
MUST requirements:     /(?:MUST|SHALL|REQUIRED):\s*(.+)/gi
MUST NOT constraints:  /(?:MUST NOT|SHALL NOT|PROHIBITED):\s*(.+)/gi
SHOULD patterns:       /(?:SHOULD|RECOMMENDED):\s*(.+)/gi
SHOULD NOT warnings:   /(?:SHOULD NOT|NOT RECOMMENDED):\s*(.+)/gi
```

### Spec Delta Format

```markdown
## ADDED
### Requirement: [New requirement]

## MODIFIED
### Requirement: [Changed requirement]

## REMOVED
- Requirement: [Removed name]

## RENAMED
FROM: ### Requirement: OldName
TO: ### Requirement: NewName
```

## Example Session

```
[Session starts]
User: Let's work on the authentication feature

Claude: [Calls get_briefing()]
        [Detects openspec/ directory]

        OpenSpec detected. Syncing specs to Daem0n memory...

        Imported 5 specs as patterns:
        - authentication (3 MUST, 2 MUST NOT)
        - api-endpoints (5 MUST, 1 MUST NOT)
        - error-handling (2 MUST)
        - ...

        Created 5 rules for spec enforcement.

User: I want to propose adding OAuth support

Claude: [Workflow 2: Inform]
        Querying memory before proposal...

        # Memory Context for Proposal: OAuth support

        ## Relevant Specs
        - authentication: "All auth must be stateless for scaling"

        ## Warnings
        - Previous session-based auth was rejected (worked=false)

        ## Rules
        MUST: Use JWT tokens, Support token refresh
        MUST NOT: Store sessions server-side

        Shall I proceed with recording this proposal intent?

User: Yes, proceed

Claude: [Records decision with openspec/proposal/pending tags]
        Recorded. Memory ID: 1847

        Now create your proposal at openspec/changes/add-oauth-support/

[Later, after implementation]

User: I've archived the OAuth change, record it

Claude: [Workflow 3: Archive]
        Reading openspec/changes/archive/add-oauth-support/...

        Recording outcome for decision #1847...
        - Outcome: Completed successfully with OAuth2 + PKCE
        - Worked: true

        Created 2 learnings:
        - OAuth2 PKCE flow works well for SPAs
        - Token refresh needs 5-minute buffer

        Linked proposal -> learnings via "led_to"

        The Daem0n will remember this for future auth work.
```

## Troubleshooting

### "No OpenSpec specs found"
Check that `openspec/specs/` directory exists and contains spec directories.

### "Already imported" but specs are stale
Use "refresh openspec" to force re-import. Old memories will be superseded.

### "Can't find proposal decision"
Search with broader terms:
```
mcp__daem0nmcp__search_memories(query="[feature keywords]", tags=["openspec"])
```

### Rules not matching
Check rule triggers match your action descriptions:
```
mcp__daem0nmcp__list_rules()
```
