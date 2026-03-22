---
name: create-handoff
description: Create a structured handoff document to transfer context to another agent session. Captures task status, key learnings, critical files, and prioritized next steps.
---

# Create Handoff Document

Create a concise handoff document to transfer context to another agent session.
Compress and summarize the context without losing key details.

## Process

### Step 1: Gather Metadata

```bash
# Get current state
git branch --show-current
git rev-parse --short HEAD
date -Iseconds
pwd
```

### Step 2: Determine Filepath

Create file at `handoffs/YYYY-MM-DD_HH-MM-SS_description.md`

**Naming patterns:**
- With issue tracking: `handoffs/2026-01-12_14-30-00_issue-123_add-oauth.md`
- Without issues: `handoffs/2026-01-12_14-30-00_refactor-auth-system.md`

### Step 3: Write Handoff Document

**Template:**

```markdown
---
date: [ISO timestamp with timezone]
git_commit: [short hash]
branch: [branch name]
directory: [working directory]
issue: [issue-123 if applicable]
status: handoff
---

# Handoff: [brief description]

## Context

[1-2 paragraph overview of what we're working on and why]

## Current Status

### Completed
- [x] [Task 1 with file:line references]
- [x] [Task 2 with file:line references]

### In Progress
- [ ] [Task being worked on with current state]

### Planned
- [ ] [Next task]
- [ ] [Future task]

## Critical Files

> These are the MOST IMPORTANT files to understand for continuation

1. `path/to/critical/file.ext:123-156` - Core implementation of X
2. `path/to/config.ext:45` - Configuration for Y
3. `path/to/test.ext` - Existing tests that constrain changes

## Recent Changes

> Files modified in this session

- `src/auth/oauth.ts:34-89` - Added OAuth flow orchestration
- `src/auth/providers.ts:1-134` - Created provider abstraction (new file)
- `src/components/LoginForm.tsx:67-89` - Integrated OAuth UI
- `tests/oauth.test.ts:1-67` - Unit tests for OAuth (new file)

## Key Learnings

> Important discoveries that affect future work

1. **OAuth state must be stored in sessionStorage**
   - LocalStorage persists across tabs causing state confusion
   - See `src/auth/oauth.ts:45` for implementation

2. **Provider interface needs async initialization**
   - Some providers require config fetching before use
   - Current implementation in `src/auth/providers.ts:23`

3. **Existing auth system uses context pattern**
   - Must integrate OAuth without breaking existing email/password
   - See `src/contexts/AuthContext.tsx` for pattern

## Open Questions

> Unresolved decisions or uncertainties

- [ ] Should OAuth tokens be stored in httpOnly cookies or localStorage?
- [ ] Need to verify PKCE flow works with all providers
- [ ] How to handle provider-specific scopes?

## Next Steps

> Prioritized actions for next session

1. **Test OAuth flow end-to-end** [Priority: HIGH]
   - Test with real provider credentials
   - Verify token refresh works
   - Check error handling

2. **Add provider configuration UI** [Priority: MEDIUM]
   - Allow admin to enable/disable providers
   - Configure client IDs per environment

3. **Document OAuth setup** [Priority: MEDIUM]
   - Update README with provider setup instructions
   - Add environment variable documentation

## Artifacts

> Complete list of files created/modified

**New files:**
- `src/auth/oauth.ts`
- `src/auth/providers.ts`
- `tests/oauth.test.ts`

**Modified files:**
- `src/components/LoginForm.tsx`
- `src/types/auth.ts`

**Not committed:** [if applicable]
- `config/development.env` (local credentials)

## Related Links

> Links to relevant docs, discussions, or research

- [OAuth 2.0 spec](https://oauth.net/2/)
- Slack discussion: #auth-redesign (2026-01-10)
- Design doc: `docs/oauth-integration.md`

## Additional Context

> Any other useful context

- Testing locally requires registered OAuth apps for each provider
- Google OAuth has strict redirect URI validation
- GitHub provider works but needs organization scope review
```

### Step 4: Commit the Handoff

```bash
git add handoffs/YYYY-MM-DD_HH-MM-SS_description.md
git commit -m "docs(handoff): add handoff for [brief description]"
```

### Step 5: Inform User

```
Handoff created at: handoffs/2026-01-12_14-30-00_oauth-integration.md

To resume in a new session:
1. Start fresh AI session
2. Provide the prompt: "Resume work from handoffs/2026-01-12_14-30-00_oauth-integration.md"
3. Or use: /resume_handoff handoffs/2026-01-12_14-30-00_oauth-integration.md

The handoff captures:
- Current task status
- Key learnings and decisions
- Files to read first
- Prioritized next steps
```

## Guidelines

1. **Be specific, not vague** - Include file:line references for everything
2. **Capture the "why"** - Future sessions need to understand decisions
3. **Prioritize learnings** - Mistakes and discoveries are most valuable
4. **Reference, don't duplicate** - Link to files rather than copy code
5. **Update issue tracking** - If using issues, link the handoff
