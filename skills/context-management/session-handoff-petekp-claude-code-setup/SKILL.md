---
name: session-handoff
description: >
  Generate a smart bootstrap prompt to continue the current conversation in a fresh session.
  Use when (1) approaching context limits, (2) user says "handoff", "bootstrap", "continue later",
  "save session", or similar, (3) before closing a session with unfinished work, (4) user wants
  to resume in a different environment. Outputs a clipboard-ready prompt capturing essential
  context while minimizing tokens.
---

# Session Handoff

Generate a bootstrap prompt that enables seamless conversation continuity in a new session.

## Process

### 1. Analyze Current Session

Identify and categorize:

- **Goal state**: What is the user trying to accomplish? What's the end state?
- **Current progress**: What's been done? What's working?
- **Blockers/open questions**: What's unresolved? What decisions are pending?
- **Key artifacts**: Files modified, commands run, errors encountered
- **Critical context**: Domain knowledge, constraints, or preferences established

### 2. Apply Token Efficiency Heuristics

**Include:**
- Specific file paths, function names, error messages (hard to rediscover)
- Decisions made and their rationale (prevents re-discussion)
- Current hypothesis or approach being tested
- Exact reproduction steps for bugs

**Exclude:**
- General knowledge Claude already has
- Verbose explanations of standard concepts
- Full file contents (use paths + line numbers instead)
- Conversation pleasantries or meta-discussion

**Compress:**
- Use bullet points over prose
- Reference files by path, not content
- Summarize long error traces to key lines
- Use "established: X" for agreed-upon decisions

### 3. Structure the Bootstrap Prompt

```markdown
## Context
[1-2 sentence goal statement]

## Progress
- [Completed item with outcome]
- [Completed item with outcome]

## Current State
[What's happening right now - the exact point to resume from]

## Key Files
- `path/to/file.ext` - [role/status]

## Open Items
- [ ] [Next immediate action]
- [ ] [Subsequent action]

## Constraints/Decisions
- [Established constraint or decision]
```

### 4. Output

Copy the bootstrap prompt to clipboard using:

```bash
echo "PROMPT_CONTENT" | pbcopy  # macOS
```

Confirm with: "Bootstrap prompt copied to clipboard. Paste it to start a new session."

## Adaptive Sizing

**Simple tasks** (bug fix, small feature): 100-200 tokens
- Goal, current file, error/behavior, next step

**Medium tasks** (feature implementation, refactor): 200-400 tokens
- Goal, progress list, current state, key files, next steps

**Complex tasks** (architecture, multi-system): 400-800 tokens
- Full structure above, plus constraints and decision rationale

## Example Output

```markdown
## Context
Adding OAuth login to the Express app, Google provider first.

## Progress
- Installed passport, passport-google-oauth20
- Created `src/auth/google.ts` with strategy config
- Added `/auth/google` and `/auth/google/callback` routes

## Current State
Callback route returns "Failed to serialize user into session" - need to implement serializeUser/deserializeUser in passport config.

## Key Files
- `src/auth/google.ts` - strategy setup (working)
- `src/routes/auth.ts:45` - callback handler (error here)
- `src/app.ts` - passport.initialize() added, missing session serialize

## Open Items
- [ ] Add serialize/deserialize to passport config
- [ ] Test full OAuth flow
- [ ] Add session persistence (currently memory store)

## Constraints
- Using express-session with default memory store for now
- Google OAuth credentials in .env (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
```
