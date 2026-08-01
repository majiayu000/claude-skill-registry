---
name: ai-memory
description: 'Purpose: Manage persistent memory files (STATUS.md, ROADMAP.md, DECISIONS.md,
  JOURNAL.md) for AI-assisted development across sessions.'
---

# AI Memory System Skill

**Purpose:** Manage persistent memory files (STATUS.md, ROADMAP.md, DECISIONS.md, JOURNAL.md) for AI-assisted development across sessions.

**Use this skill when:**
- Starting a new AI Friday session
- Ending a session and need to capture progress
- Making significant architectural decisions
- Discovering important learnings
- Initializing memory system for a new project or team

## Available Commands

### `/memory-init` - Initialize Memory System
Creates the core memory files from templates.

**When to use:** First time setting up the memory system for a project or team branch.

**What it does:**
1. Creates STATUS.md (current state tracking)
2. Creates ROADMAP.md (milestone checklists)
3. Creates DECISIONS.md (decision log)
4. Creates JOURNAL.md (learning documentation)
5. Ensures CLAUDE.md exists (or creates from template)

**Usage:**
```
User: /memory-init
```

### `/memory-start` - Start Session
Reads all memory files and provides situational awareness.

**When to use:** At the beginning of every AI Friday session.

**What it does:**
1. Reads CLAUDE.md (project context)
2. Reads STATUS.md (current state)
3. Reads ROADMAP.md (what's next)
4. Reads DECISIONS.md (decision history)
5. Summarizes current state and next steps

**Usage:**
```
User: /memory-start
```

### `/memory-update` - Update Status
Updates STATUS.md with current progress and next steps.

**When to use:** At the end of a session, or when switching tasks.

**What it does:**
1. Reads current STATUS.md
2. Asks what was completed
3. Asks what's in progress
4. Asks about blockers
5. Asks about next steps
6. Updates STATUS.md with new information

**Usage:**
```
User: /memory-update
```

### `/memory-decision` - Log Decision
Adds a decision entry to DECISIONS.md.

**When to use:** After making a significant architectural, technical, or process decision.

**What it does:**
1. Asks for decision details
2. Prompts for alternatives considered
3. Prompts for rationale
4. Prompts for tradeoffs
5. Formats and appends to DECISIONS.md

**Usage:**
```
User: /memory-decision
```

### `/memory-learn` - Capture Learning
Adds a learning entry to JOURNAL.md.

**When to use:** When you discover something non-obvious or worth remembering.

**What it does:**
1. Asks what was discovered
2. Asks for context/why it matters
3. Asks for solution/pattern
4. Requests code examples (if applicable)
5. Formats and appends to JOURNAL.md

**Usage:**
```
User: /memory-learn
```

### `/memory-roadmap` - Update Roadmap
Marks tasks complete or adds new tasks to ROADMAP.md.

**When to use:** When completing milestones or tasks.

**What it does:**
1. Shows current ROADMAP.md
2. Asks which tasks to mark complete
3. Asks if new tasks should be added
4. Updates ROADMAP.md accordingly

**Usage:**
```
User: /memory-roadmap
```

### `/memory-summary` - Session Summary
Generates a summary of the session for STATUS.md.

**When to use:** End of session, before committing.

**What it does:**
1. Reviews git diff to see what changed
2. Summarizes work completed
3. Identifies what's in progress
4. Suggests next steps
5. Outputs formatted summary for STATUS.md

**Usage:**
```
User: /memory-summary
```

## Workflow Examples

### Starting AI Friday Session
```
User: /memory-start

Claude: Reading memory files...

📍 Current State (from STATUS.md):
- Phase: Milestone 1 - Core Referral Tracking
- Task: Implementing referral hash generation (80% complete)
- Last updated: 2025-01-13 16:30

🎯 Next Steps (from ROADMAP.md):
- [ ] Complete hash generation
- [ ] Add cookie tracking
- [ ] Implement conversion detection

📋 Recent Decisions:
- Decision 001: Using SHA-256 for referral hashes

Ready to continue! Let's complete the hash generation.
```

### Ending Session
```
User: /memory-update

Claude: What did you complete this session?
User: Finished hash generation and started cookie tracking

Claude: What's currently in progress? (with %)
User: Cookie tracking is about 40% done

Claude: Any blockers?
User: None

Claude: What should we do next session?
User: Complete cookie tracking and test with MemberPress

Claude: ✅ Updated STATUS.md:

**Last Updated:** 2025-01-20 11:00
**Current Task:** Implementing cookie tracking (40% complete)

## Recent Progress
- ✅ Completed referral hash generation
- ⏳ Started cookie tracking (40%)

## Next Steps
1. Complete cookie tracking implementation
2. Test integration with MemberPress hooks
3. Begin conversion detection
```

### Logging a Decision
```
User: /memory-decision

Claude: What decision was made?
User: Use SHA-256 hashing for referral links instead of sequential IDs

Claude: What alternatives did you consider?
User: 1. Sequential IDs - simple but predictable
      2. UUID - unique but too long for URLs
      3. SHA-256 hash - chosen

Claude: Why did you choose SHA-256?
User: Non-reversible, secure, consistent length, no database lookup needed

Claude: What are the tradeoffs?
User: Pros: Security, no PII in URL
      Cons: Can't reverse-lookup referrer without DB query

Claude: ✅ Added Decision 002 to DECISIONS.md
```

## Best Practices

### DO:
- ✅ Run `/memory-start` at the beginning of every session
- ✅ Run `/memory-update` at the end of every session
- ✅ Use `/memory-decision` for significant choices (architecture, tech stack)
- ✅ Use `/memory-learn` for non-obvious discoveries
- ✅ Keep STATUS.md focused on current state only

### DON'T:
- ❌ Skip updating STATUS.md (next session will be confused)
- ❌ Log trivial decisions (variable names, formatting)
- ❌ Copy entire codebase into JOURNAL.md (keep entries concise)
- ❌ Let STATUS.md get stale (update it!)

## Integration with AI Friday Workflow

**Weekly Cycle:**
```
Friday 9:00am  - /memory-start (catch up from last week)
Friday 9:05am  - Start development
Friday 10:45am - /memory-decision (if made architectural choice)
Friday 10:50am - /memory-learn (if discovered something)
Friday 11:00am - /memory-update (capture progress)
Friday 11:05am - Commit changes (including memory files)
```

**Git Workflow:**
```bash
# At end of session
git add .
git status  # Verify memory files are included

git commit -m "feat: implement cookie tracking

Updated STATUS.md with progress and next steps.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Team Adoption

**For multi-team projects:**
- Each team branch has own STATUS.md, ROADMAP.md, DECISIONS.md, JOURNAL.md
- Share DECISIONS.md across teams in presentation
- Compare ROADMAP.md to see relative progress
- Learn from each team's JOURNAL.md discoveries

**Example:**
```
memberpress-referral-program/
├── yellow-team-01/
│   ├── STATUS.md     # Yellow team's current state
│   ├── ROADMAP.md    # Yellow team's tasks
│   └── ...
├── purple-team-01/
│   ├── STATUS.md     # Purple team's current state
│   ├── ROADMAP.md    # Purple team's tasks
│   └── ...
```

## Technical Notes

**File Locations:**
- Root level: STATUS.md, ROADMAP.md, DECISIONS.md, JOURNAL.md, CLAUDE.md
- Domain-specific: `[directory]/CLAUDE.md` (optional)

**Formats:**
- All files are GitHub-flavored markdown
- Use consistent checkbox syntax: `- [x]`, `- ⏳`, `- [ ]`
- Use ISO date format: YYYY-MM-DD HH:MM
- Use semantic status indicators: ✅ ⏳ ❌ ⚠️

**Git:**
- Memory files SHOULD be committed with code changes
- Include in .gitignore: Nothing (all memory files should be versioned)
- Merge conflicts: Most recent wins (timestamps help resolve)

## Resources

- Full documentation: `/docs/AI-AGENT-MEMORY-SYSTEM.md`
- Templates: `/.claude/skills/ai-memory/templates/`
- Training guide: `/.claude/skills/ai-memory/TRAINING.md`

---

**Version:** 1.0
**Last Updated:** 2025-01-21
**Compatible with:** Claude Code, Claude (web/API), ChatGPT, any AI assistant
