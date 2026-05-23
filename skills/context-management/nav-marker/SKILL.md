---
name: nav-marker
description: Create context save points to preserve conversation state before breaks, risky changes, or compaction. Use when user says "save my progress", "create checkpoint", "mark this point", or before clearing context.
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Navigator Marker Skill

Create context markers - save points that preserve conversation state so you can resume work later without re-explaining everything.

## When to Invoke

Invoke this skill when the user:
- Says "save my progress", "create checkpoint", "mark this"
- Says "before I take a break", "save before lunch"
- Mentions "risky refactor ahead", "experiment with new approach"
- Says "end of day", "stopping for today"
- Before compacting context

**DO NOT invoke** if:
- User is asking about existing markers (use listing, not creation)
- Context is fresh (< 5 messages exchanged)

## Execution Steps

### Step 1: Check Navigator Structure

Verify `.agent/.context-markers/` directory exists:

```bash
mkdir -p .agent/.context-markers
```

### Step 2: Determine Marker Name

**If user provided name**:
- Use their name (sanitize: lowercase, hyphens for spaces)
- Example: "Before Big Refactor" → "before-big-refactor"

**If no name provided**:
- Auto-generate with timestamp: `marker-{YYYY-MM-DD}-{HHmm}`
- Example: `marker-2025-10-16-1430`

**Ask user for optional note**:
```
Creating marker: [name]

Add a note? (optional - helps remember context later)
Example: "OAuth working, need to add tests"

Note:
```

### Step 3: Generate Marker Content [EXECUTE]

**IMPORTANT**: You MUST actively capture ToM sections (User Intent, Corrections, Belief State).

Create marker document with this structure:

```markdown
# Context Marker: [name]

**Created**: [YYYY-MM-DD HH:MM]
**Note**: [user's note or "No note provided"]

---

## Conversation Summary

[Summarize last 10-15 messages:
- What user was working on
- Key decisions made
- Problems solved
- Current progress state
]

## Documentation Loaded

[List docs that were Read during session:
- Navigator: ✅ .agent/DEVELOPMENT-README.md
- Task: TASK-XX-feature.md
- System: project-architecture.md
- SOPs: [if any]
]

## Files Modified

[List files with Write/Edit calls:
- src/auth/login.ts (implemented OAuth)
- src/routes/auth.ts (added endpoints)
- tests/auth.test.ts (created tests)
]

## Current Focus

[What user is working on right now:
- Feature: Authentication with OAuth
- Phase: Integration complete, testing pending
- Blockers: [if any]
]

## Technical Decisions

[Key architectural choices:
- Using passport.js over next-auth (better control)
- JWT tokens in httpOnly cookies (XSS protection)
- Redis for session storage (scalability)
]

## Next Steps

[What to do after restore:
1. Finish writing tests for OAuth flow
2. Add error handling for failed logins
3. Document setup in README
]

## User Intent & Goals (ToM) [CAPTURE ACTIVELY]

[Theory of Mind section - captures user's mental state for better restoration]

**⚠️ CRITICAL: Analyze conversation to extract these - do not leave empty!**

**Primary goal this session**:
[What the user was ultimately trying to accomplish - not just the surface task]
- Review conversation for "I want to...", "The goal is...", "We need to..."
- Infer from task context if not explicitly stated

**Stated preferences**:
[Any preferences expressed during session:
- Communication style (concise/detailed)
- Code patterns preferred
- Confirmation behavior wanted
]
- Look for "I prefer...", "Don't do...", "Always use..."

**Corrections made**:
[Important corrections that should persist:
- "Should be /users not /user (plural convention)"
- "Prefer functional components over class"
- "Always use TypeScript strict mode"
]
- Look for "No, I meant...", "Actually...", "Not X, use Y"
- These MUST be captured to avoid repeating mistakes

## Belief State [CAPTURE ACTIVELY]

[Captures mutual understanding state for accurate restoration]

**⚠️ CRITICAL: Infer from conversation - do not leave empty!**

**What user knows**:
[User's demonstrated knowledge level:
- Familiar with Express, new to Passport
- Knows about JWT, unfamiliar with refresh tokens
- Senior developer, skip basics
]

**Assumptions I made**:
[Key assumptions during session:
- Using Redis for sessions (confirmed by user)
- Auth endpoints follow /api/auth/* pattern
- Testing with Jest + React Testing Library
]

**Uncertainty areas**:
[Questions that weren't fully resolved:
- Not sure if user wants social logins beyond Google
- Rate limiting requirements unclear
- Error message format preferences unknown
]

## Loop State (if in loop mode)

[Capture loop mode state for resumption - skip if not in loop mode]

**Iteration**: [N]/[MAX] (e.g., 3/5)
**Phase**: [INIT|RESEARCH|IMPL|VERIFY|COMPLETE]
**State Hash**: [6-char hash for continuity]
**Completion Indicators**:
- [ ] Code committed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Ticket closed
- [ ] Marker created

**EXIT_SIGNAL**: [true/false]
**Stagnation Count**: [N]/[THRESHOLD]

## Restore Instructions

To restore this marker:
\```bash
Read .agent/.context-markers/[filename]
\```

Or use: `/nav:markers` and select this marker
```

### Step 4: Save Marker File

Write marker to file:

```
Write(
  file_path: ".agent/.context-markers/[timestamp]_[name].md",
  content: [generated marker content]
)
```

Filename format: `{YYYY-MM-DD-HHmm}_{name}.md`
Example: `2025-10-16-1430_before-big-refactor.md`

### Step 4.5: Verify Marker Creation

After creating marker, verify it was written successfully:

```bash
# Verify file exists and is non-empty
if [ -f ".agent/.context-markers/[filename]" ] && [ -s ".agent/.context-markers/[filename]" ]; then
  # Calculate checksum for verification
  checksum=$(md5 -q ".agent/.context-markers/[filename]" 2>/dev/null || md5sum ".agent/.context-markers/[filename]" | cut -d' ' -f1)

  # Log to central marker log
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] ✅ Marker created: [filename] (checksum: $checksum)" >> .agent/.marker-log

  echo "✅ Marker verified successfully"
else
  echo "❌ Marker creation failed - file missing or empty"
  exit 1
fi
```

Marker verification ensures:
- File exists on disk
- File has content (non-empty)
- Checksum logged for integrity verification
- Creation event logged to central log

### Step 5: Confirm Creation

Show success message with verification details:

```
✅ Context marker created!

Marker: [name]
File: .agent/.context-markers/[filename]
Size: [X] KB (~[Y] tokens)
Checksum: [md5-hash]
Verified: ✅

This marker captures:
- Last [N] messages of conversation
- Files you were working on
- Technical decisions made
- Next steps to continue

To restore later:
- Start new session
- Say "load marker [name]"
- Or use /nav:markers to list all markers

Logged to: .agent/.marker-log
```

## Scripts

**create_marker.py**: Generates marker content from conversation analysis
- Input: Conversation history (from Claude)
- Output: Formatted markdown marker

## Common Use Cases

### Before Lunch Break
```
User: "Save my progress, taking lunch"
→ Creates marker: "lunch-break-2025-10-16"
→ Captures current state
→ User resumes after lunch: "Load my lunch marker"
```

### Before Risky Refactor
```
User: "Mark this before I refactor routing"
→ Creates marker: "before-routing-refactor"
→ If refactor fails, restore marker
→ If refactor succeeds, delete marker
```

### End of Day
```
User: "End of day checkpoint"
→ Creates marker: "eod-2025-10-16"
→ Note: "OAuth done, tests tomorrow"
→ Next morning: "Load yesterday's marker"
```

### Before Context Compact
```
Automatic (via nav-compact skill):
→ Creates marker: "before-compact-2025-10-16-1500"
→ Compact clears conversation
→ Marker preserves knowledge
→ Next session: Auto-offers to restore
```

## Marker Best Practices

**Good marker names**:
- `lunch-break` (clear when/why)
- `before-api-refactor` (indicates purpose)
- `feature-complete` (marks milestone)
- `eod-friday` (specific timing)

**Bad marker names**:
- `temp` (not descriptive)
- `marker1` (meaningless)
- `test` (confusing)

**When to create markers**:
- ✅ Before breaks (lunch, EOD)
- ✅ Before risky changes
- ✅ Before context compact
- ✅ At milestones (feature complete)
- ❌ After every single message (noise)
- ❌ When context is fresh (< 5 messages)

## Error Handling

**Marker directory missing**:
```
Creating .agent/.context-markers/ directory...
✅ Ready to save markers
```

**Duplicate marker name**:
```
⚠️  Marker "[name]" already exists

Options:
1. Overwrite (replace existing)
2. Append timestamp (create "[name]-v2")
3. Choose different name

Your choice [1-3]:
```

**Insufficient context**:
```
⚠️  Very little context to save (< 5 messages)

Markers work best when there's significant progress to preserve.
Continue anyway? [y/N]:
```

## Success Criteria

Marker creation is successful when:
- [ ] Marker file created in `.agent/.context-markers/`
- [ ] Filename is unique and descriptive
- [ ] Content includes: summary, loaded docs, files modified, next steps
- [ ] User knows how to restore marker later
- [ ] Marker is 2-5k tokens (comprehensive but efficient)

## Notes

- Markers are **git-ignored** (personal session save points)
- Team members don't see each other's markers
- Markers can be deleted anytime with `/nav:markers clean`
- Typical marker size: 2-5k tokens (97.7% compression from 130k conversation)

This skill provides same functionality as `/nav:marker` command but with natural language invocation.
