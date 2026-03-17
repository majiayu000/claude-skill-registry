---
name: reflect
version: 1.0.0
model: claude-sonnet-4-5
description: CRITICAL learning capture. Extracts HIGH/MED/LOW confidence patterns from conversations to prevent repeating mistakes and preserve what works. Use PROACTIVELY after user corrections ("no", "wrong"), after praise ("perfect", "exactly"), when discovering edge cases, or when skills are heavily used. Without reflection, valuable learnings are LOST forever. Acts as continuous improvement engine for all skills. Invoke EARLY and OFTEN - every correction is a learning opportunity.
license: MIT
metadata:
  timelessness: 8/10
  adr: ADR-007, ADR-017
---

# Reflect Skill

**Critical learning capture system** that prevents repeating mistakes and preserves successful patterns across sessions.

Analyze the current conversation and propose improvements to skill-based memories based on what worked, what didn't, and edge cases discovered. **Every correction is a learning opportunity** - invoke proactively to build institutional knowledge.

---

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `reflect on this session` | Extract learnings from conversation |
| `learn from this mistake` | Capture correction patterns |
| `capture what we learned` | Document session insights |
| `improve skill {name}` | Target specific skill memory |
| `what did we learn` | Review and store patterns |

Also monitor user phrasing such as "what if...", "ensure", or "don't forget". These phrases should immediately route into the MEDIUM trigger tables below.

### 🔴 HIGH Priority Triggers (Invoke Immediately)

| Trigger | Example | Why Critical |
|---------|---------|--------------|
| User correction | "no", "wrong", "not like that", "never do" | Captures mistakes to prevent repetition |
| Chesterton's Fence | "you removed that without understanding" | Documents architectural decisions |
| Immediate fixes | "debug", "root cause", "fix all" | Learns from errors in real-time |

### 🟡 MEDIUM Priority Triggers (Invoke After Multiple)

| Trigger | Example | Why Important |
|---------|---------|---------------|
| User praise | "perfect", "exactly", "great" | Reinforces successful patterns |
| Tool preferences | "use X instead of Y", "prefer", "rather than" | Builds workflow preferences |
| Edge cases | "what if X happens?", "don't forget", "ensure" | Captures scenarios to handle |
| Questions | Short questions after output | May indicate confusion or gaps |

### 🟢 LOW Priority Triggers (Invoke at Session End)

| Trigger | Example | Why Useful |
|---------|---------|------------|
| Repeated patterns | Frequent use of specific commands/tools | Identifies workflow preferences |
| Session end | After skill-heavy work | Consolidates all session learnings |

---

## Original Triggers (Still Supported)

| Phrase | Action |
|--------|--------|
| "reflect" | Full analysis of current session |
| "improve skill" | Target specific skill for improvement |
| "learn from this" | Extract learnings from recent interaction |
| "what did we learn" | Summarize accumulated learnings |

---

## When to Use

Use this skill when:

- User corrects your output ("no", "wrong", "not like that")
- User praises specific output ("perfect", "exactly")
- Edge cases are discovered during work
- Session end after skill-heavy work
- Want to capture learnings before they are lost

Use [retrospective](../retrospective/SKILL.md) instead when:

- Conducting a full session retrospective (broader scope)
- Analyzing multi-session patterns across the project

## Proactive Invocation Reminder

**Don't wait for users to ask!** Invoke reflect immediately when you detect:

1. **User says "no"** → Invoke reflect NOW (captures correction)
2. **User says "perfect"** → Invoke reflect NOW (captures success pattern)
3. **User asks "what if"** → Invoke reflect NOW (captures edge case)
4. **You used multiple skills** → Invoke reflect at END (captures all learnings)
5. **User corrected your output** → Invoke reflect IMMEDIATELY (critical learning)

**Why this matters**: Without proactive reflection, learnings are LOST. The Stop hook captures some patterns, but **manual reflection is MORE ACCURATE** because you have full conversation context.

**Cost**: ~30 seconds of analysis. **Benefit**: Prevents repeating mistakes forever.

---

## Process

### Phase 1: Identify the Target Skill

Locate the skill-based memory to update:

1. **Check Serena memories**: Look for files ending with `-observations.md` in `.serena/memories/`
2. **Infer from context**: Identify which skill(s) were used in the conversation
3. **Create if needed**: If missing, propose `{skill-name}-observations.md` (skill observations pattern)

**Storage Locations**:

- **Serena MCP (canonical)**: `.serena/memories/{skill-name}-observations.md` via `mcp__serena__write_memory`
- **Contingency (Serena unavailable)**: Manually edit the same file in Git and note the manual update in the session log for later Serena sync

### Phase 2: Analyze the Conversation

Scan the conversation for learning signals with confidence levels:

#### HIGH Confidence: Corrections

User actively steered or corrected output. These are the most valuable signals.

**Detection patterns**:

- Explicit rejection: "no", "not like that", "that's wrong", "I meant"
- Strong directives: "never do", "always do", "don't ever"
- Immediate requests for changes after generation
- User provided alternative implementation
- User explicitly corrected output format/structure

**Example**:

```text
User: "No, use the PowerShell skill script instead of raw gh commands"
→ [HIGH] + Add constraint: "Use PowerShell skill scripts, never raw gh commands"
```

#### MEDIUM Confidence: Success Patterns

Output was accepted or praised. Good signals but may be context-specific.

**Detection patterns**:

- Explicit praise: "perfect", "great", "yes", "exactly", "that's it"
- Implicit acceptance: User built on top of output without modification
- User proceeded to next step without corrections
- Output was committed/merged without changes

**Example**:

```text
User: "Perfect, that's exactly what I needed"
→ [MED] + Add preference: "Include example usage in script headers"
```

#### MEDIUM Confidence: Edge Cases

Scenarios the skill didn't anticipate. Opportunities for improvement.

**Detection patterns**:

- Questions skill didn't answer
- Workarounds user had to apply
- Features user asked for that weren't covered
- Error handling gaps discovered

**Example**:

```text
User: "What if the file doesn't exist?"
→ [MED] ~ Add edge case: "Handle missing file scenario"
```

#### LOW Confidence: Preferences

Accumulated patterns over time. Need more evidence before formalizing.

**Detection patterns**:

- Repeated choices in similar situations
- Style preferences shown implicitly (formatting, naming)
- Tool/framework preferences
- Workflow preferences

**Example**:

```text
User consistently uses `-Force` flag
→ [LOW] ~ Note for review: "User prefers -Force flag for overwrites"
```

#### Confidence Threshold

Only propose changes when sufficient evidence exists:

| Threshold | Action |
|-----------|--------|
| ≥1 HIGH signal | Always propose (user explicitly corrected) |
| ≥2 MED signals | Propose (sufficient pattern) |
| ≥3 LOW signals | Propose (accumulated evidence) |
| 1-2 LOW only | Skip (insufficient evidence), note for next session |

### Phase 3: Propose Learnings

Present findings using WCAG AA accessible colors (4.5:1 contrast ratio):

```text
┌─────────────────────────────────────────────────────────────┐
│ SKILL REFLECTION: {skill-name}                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ [HIGH] + Add constraint: "{specific constraint}"            │
│   Source: "{quoted user correction}"                        │
│                                                             │
│ [MED]  + Add preference: "{specific preference}"            │
│   Source: "{evidence from conversation}"                    │
│                                                             │
│ [MED]  + Add edge case: "{scenario}"                        │
│   Source: "{question or workaround}"                        │
│                                                             │
│ [LOW]  ~ Note for review: "{observation}"                   │
│   Source: "{pattern observed}"                              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Apply changes? [Y/n/edit]                                   │
└─────────────────────────────────────────────────────────────┘
```

**Color Key** (accessible):

- `[HIGH]` - Red/bold: Mandatory corrections (user explicitly said "no")
- `[MED]` - Yellow/amber: Recommended additions
- `[LOW]` - Blue/dim: Notes for later review

**User Response Handling**:

| Response | Action |
|----------|--------|
| **Y** (yes) | Proceed to Step 4 (update memory) |
| **n** (no) | Abort update, ask "What would you like to change or was this not useful?" |
| **edit** | Present each finding individually, allow user to modify/reject each one |

**On rejection (n)**:

1. Log that reflection was declined (for future pattern analysis)
2. Ask user if they want to revise the analysis or skip entirely
3. If skip, end workflow without memory update

**On edit**:

1. Present first finding with options: [keep/modify/remove]
2. If modify, accept user's revised text
3. Repeat for each finding
4. Confirm final list before applying

### Phase 4: Persist Learnings to Memory

**ALWAYS show changes before applying.**

After user approval:

1. **Read existing memory** (if exists)
2. **Append new learnings** with timestamp and session reference
3. **Preserve existing content** - never remove without explicit request
4. **Extract code citations** (Phase 4 Enhancement - see below)
5. **Write to file**: `.serena/memories/{skill-name}-observations.md`

**Storage Strategy**:

1. **Serena MCP (canonical)**:

   ```text
   mcp__serena__write_memory(memory_file_name="{name}-observations", memory_content="...")
   ```

2. **If Serena unavailable** (contingency):

   ```powershell
   $path = ".serena/memories/{name}-observations.md"
   $existingContent = Get-Content $path -ErrorAction SilentlyContinue
   $newContent = $existingContent + "`n" + $newLearnings
   Set-Content $path -Value $newContent
   git add $path
   git commit -m "chore(memory): update {name} skill sidecar learnings"
   ```

   Record the manual edit in the session log so Serena MCP can replay the update when the service is available again.

**Memory Format**:

```markdown
# Skill Sidecar Learnings: {Skill Name}

**Last Updated**: {ISO date}
**Sessions Analyzed**: {count}

## Constraints (HIGH confidence)

- {constraint 1} (Session {N}, {date})
- {constraint 2} (Session {N}, {date})

## Preferences (MED confidence)

- {preference 1} (Session {N}, {date})
- {preference 2} (Session {N}, {date})

## Edge Cases (MED confidence)

- {edge case 1} (Session {N}, {date})
- {edge case 2} (Session {N}, {date})

## Notes for Review (LOW confidence)

- {note 1} (Session {N}, {date})
- {note 2} (Session {N}, {date})
```

#### Phase 4 Enhancement: Auto-Citation Capture

When persisting learnings that reference specific code locations, automatically capture citations:

1. **Detect code references** in learning text:
   - Inline code references: `` `path/to/file.ext` line N ``
   - Function references: `` `functionName()` in `file.ext` ``
   - Explicit citations: "See: file.ext:42"

2. **Extract citation metadata**: file path, line number, snippet (if available)

3. **Add citations to memory frontmatter**:

   ```bash
   python -m memory_enhancement add-citation <memory-id> --file <path> --line <num> --snippet <text>
   ```

4. **Update confidence score** based on initial verification

**Detection Patterns**:

| Pattern | Example | Extraction |
|---------|---------|------------|
| Inline code + line | In `` `src/client/constants.ts` line 42 `` | file=src/client/constants.ts, line=42 |
| Function in file | `` `handleError()` in `src/utils.ts` `` | file=src/utils.ts (file-level) |
| Explicit citation | See: src/api.py:100 | file=src/api.py, line=100 |

**Integration Point**:

After user approves learnings (step 4 above), before writing to Serena:

1. Parse learning text for code references using patterns above
2. For each reference found:
   - Extract file path, line number, and snippet
   - Call `python -m memory_enhancement add-citation <memory-id> --file <path> --line <num> --snippet <text>`
3. If citation extraction fails, proceed without citations (non-blocking)
4. Proceed with normal Serena MCP write

**Example**:

Learning text: "The bug was in `scripts/health.py` line 45, where we forgot to handle None"

1. Extract: file=scripts/health.py, line=45, snippet="handle None"
2. Add citation: `python -m memory_enhancement add-citation memory-observations --file scripts/health.py --line 45 --snippet "handle None"`
3. Write learning to Serena with citation attached

---

## Decision Tree

```text
User says "reflect" or similar?
│
├─► YES
│   │
│   ├─► Identify skill(s) used in conversation
│   │   │
│   │   └─► Skill identified?
│   │       │
│   │       ├─► YES → Analyze conversation for signals
│   │       │   │
│   │       │   └─► Meets confidence threshold?
│   │       │       │
│   │       │       ├─► YES → Present findings, await approval
│   │       │       │   │
│   │       │       │   ├─► User says Y → Update memory file
│   │       │       │   │   │
│   │       │       │   │   ├─► Serena available? → Use MCP write
│   │       │       │   │   └─► Serena unavailable? → Use Git fallback
│   │       │       │   │
│   │       │       │   ├─► User says n → Ask for feedback
│   │       │       │   │   │
│   │       │       │   │   ├─► User wants revision → Re-analyze
│   │       │       │   │   └─► User skips → End workflow
│   │       │       │   │
│   │       │       │   └─► User says edit → Interactive review
│   │       │       │       │
│   │       │       │       └─► Per-finding [keep/modify/remove]
│   │       │       │
│   │       │       └─► NO → Report "Insufficient evidence. Note for next session."
│   │       │
│   │       └─► NO → Ask user which skill to reflect on
│   │           │
│   │           ├─► User specifies skill → Continue with that skill
│   │           └─► User says "none" → End workflow
│   │
│   └─► Multiple skills?
│       │
│       └─► Analyze each, group findings by skill, present together
│
└─► NO → This skill not invoked
```

---

## Examples

### Example 1: Correction Detected

```text
Conversation:
User: "Create a PR for this change"
Agent: [runs gh pr create directly]
User: "No, use the github skill script!"

Analysis:
[HIGH] + Add constraint: "Always use .claude/skills/github/ scripts for PR operations"
  Source: User correction - "No, use the github skill script!"
```

### Example 2: Success Pattern

```text
Conversation:
User: "Add error handling"
Agent: [adds try/catch with specific error types]
User: "Perfect! That's exactly what I wanted"

Analysis:
[MED] + Add preference: "Use specific error types in catch blocks, not generic [Exception]"
  Source: User approval after seeing specific error types
```

### Example 3: Edge Case Discovery

```text
Conversation:
User: "Run the build"
Agent: [runs build command]
User: "Wait, what if the node_modules folder doesn't exist?"

Analysis:
[MED] + Add edge case: "Check for node_modules existence before build"
  Source: User question about missing dependencies
```

---

## Use Cases

### 1. Code Review Skills

Capture learnings about code review patterns:

- **Style guide rules**: User corrections on formatting, naming, structure
- **Security patterns**: Security vulnerabilities caught, OWASP patterns enforced
- **Severity levels**: When issues are P0 vs P1 vs P2
- **False positives**: Patterns that look like issues but aren't

**Example memory**: `.serena/memories/code-review-observations.md`

### 2. API Design Skills

Track API design decisions:

- **Naming conventions**: REST endpoint patterns, verb choices
- **Error formats**: HTTP status codes, error response structure
- **Auth patterns**: OAuth, JWT, API key patterns
- **Versioning style**: URL versioning, header versioning

**Example memory**: `.serena/memories/api-design-observations.md`

### 3. Testing Skills

Remember testing preferences:

- **Coverage targets**: Minimum % required, critical paths
- **Mocking patterns**: When to mock vs integration test
- **Assertion styles**: Preferred assertion libraries, patterns
- **Test naming**: Convention for test method names

**Example memory**: `.serena/memories/testing-observations.md`

### 4. Documentation Skills

Learn documentation patterns:

- **Structure/format**: Section order, heading levels
- **Code examples**: Real vs pseudo-code, language choice
- **Tone preferences**: Formal vs casual, active vs passive voice
- **Diagram styles**: Mermaid vs ASCII, detail level

**Example memory**: `.serena/memories/documentation-observations.md`

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Applying without showing | User loses visibility | Always preview changes |
| Overwriting existing learnings | Loses history | Append with timestamps |
| Generic observations | Not actionable | Be specific and contextual |
| Ignoring LOW confidence | Lose valuable patterns | Track for future validation |
| Creating memory for one-off | Noise | Wait for repeated patterns |

---

## Integration

### With Session Protocol

Run reflection at session end as part of retrospective:

```text
## Session End Checklist
- [ ] Complete session log
- [ ] Run skill reflection (if skills were used)
- [ ] Update Serena memory
- [ ] Commit changes
```

### With Memory Skill

Skill memories integrate with the memory system:

```powershell
# Search skill sidecar learnings
pwsh .claude/skills/memory/scripts/Search-Memory.ps1 -Query "github-observations constraints"

# Read specific skill sidecar
Read .serena/memories/github-observations.md
```

### With Serena

If Serena MCP is available:

```text
mcp__serena__read_memory(memory_file_name="github-observations")
mcp__serena__write_memory(memory_file_name="github-observations", memory_content="...")
```

---

## Verification

| Action | Verification |
|--------|--------------|
| Analysis complete | Signals categorized by confidence |
| User approved | Explicit Y or approval statement |
| Memory updated | File written to `.serena/memories/` |
| Changes preserved | Existing content not lost |
| Commit ready | Changes staged, message drafted |

---

## Design Decisions

### Agent Sidecar Naming: `{skill-name}-observations.md`

**Decision**: Skill memories follow the ADR-007 sidecar pattern (e.g., `github-observations.md`).

**Rationale**:

- **ADR-007 Alignment**: Reuses the agent sidecar convention instead of inventing a parallel structure
- **ADR-017 Compliance**: Keeps `{domain}-{description}` format while making "skill-sidecar" explicit
- **Discovery**: Sidecars are now referenced in `memory-index.md`, preventing orphaned learnings
- **Single Canonical Store**: Serena MCP and Git both write to the same file path, eliminating dual-governance ambiguity

**Migration**: Rename `{skill}-observations.md` (or legacy `skill-{name}.md`) to `{skill}-observations.md` and update index references.

### Serena vs Forgetful Roles

- **Serena MCP** remains the canonical record. Every learning is persisted to the `{skill}-observations.md` file.
- **Forgetful** is optional and used for semantic lookup only. When storing supporting context, tag the entry with `skill-{name}` and reference the Serena sidecar instead of duplicating the content.

### Relationship to `curating-memories`

- `curating-memories` = general-purpose maintenance of any memory artifact (linking, pruning, marking obsolete).
- `reflect` = targeted retrospective that feeds those artifacts with new learnings.
- When a sidecar accumulates conflicting guidance, route the file to `curating-memories` for cleanup.

### Session Protocol Integration

- Add "Run skill reflection if ≥3 distinct skills used" to the Session End checklist.
- Document any manual sidecar edits (when Serena MCP is unavailable) in the session log before completion.
- Invoke reflect immediately after the Stop hook highlights high-confidence learnings so the session log and sidecar stay in sync.

---

## Extension Points

1. **Curating memories** – route conflicting or stale learnings to `curating-memories` for consolidation.
2. **Memory skill** – use `memory` skill for search/recall before proposing redundant learnings.
3. **Forgetful** – optionally mirror high-confidence learnings into Forgetful with `skill-{name}` tags for semantic recall.
4. **Session log fixer** – after reflection, ensure the session log captures the learning summary via `session-log-fixer`.

## Related

| Skill | Relationship |
|-------|--------------|
| `memory` | Skill memories are part of Tier 1 |
| `using-forgetful-memory` | Alternative storage for skill learnings |
| `curating-memories` | For maintaining/pruning skill memories |
| `retrospective` | Full session retrospective (this is mini version) |

---

## Commit Convention

When committing skill observation updates:

```text
chore(memory): update {skill-name} skill sidecar learnings (session {N})

- Added {count} constraints (HIGH confidence)
- Added {count} preferences (MED confidence)
- Added {count} edge cases (MED confidence)
- Added {count} notes (LOW confidence)

Session: {session-id}
```
