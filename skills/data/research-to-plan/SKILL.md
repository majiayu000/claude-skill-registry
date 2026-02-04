---
name: research-to-plan
description: |
  Convert SOTA research into executable plans. Use when: (1) starting
  features with unknowns, (2) need current best practices, (3) converting
  notes to tasks. Searches web for 2026 SOTA, writes RESEARCH.md, generates
  PLAN.md tasks.
category: development
user-invocable: true
---

# Research to Plan

Converts state-of-the-art research into executable implementation plans.

## Trigger Conditions

Invoke when:
- Starting a feature with unknowns
- Need to validate approach against current best practices
- Converting research notes to actionable tasks
- User provides research text or topic

Also invoke explicitly with:
- `/research-to-plan [topic]`
- "research and plan"
- "find best practices for"

## Procedure

### Step 1: Accept Research Input

**Option A: Topic provided**
```
/research-to-plan OAuth authentication
```

**Option B: Research text provided**
```
/research-to-plan
[paste research notes or context]
```

**Option C: Existing RESEARCH.md**
```
/research-to-plan --from-file
```

### Step 2: Search for SOTA (2026)

Search the web for current best practices:

```
Search queries:
1. "{{topic}} best practices 2026"
2. "{{topic}} implementation guide 2026"
3. "{{topic}} security considerations 2026"
4. "{{topic}} common mistakes 2026"
```

**Important:** Use 2026 in search queries to get current information beyond knowledge cutoff.

### Step 3: Validate and Refine

Compare user's research with web findings:

| Aspect | User's Research | SOTA 2026 | Action |
|--------|-----------------|-----------|--------|
| Approach | ✓ Current | - | Keep |
| Library | Outdated | New version | Update |
| Pattern | Unknown | Best practice | Add |
| Security | Missing | Critical | Add |

### Step 4: Write RESEARCH.md

Structure findings:

```markdown
# Research

## Topic: OAuth Authentication

## Summary

OAuth 2.0 with PKCE is the current standard for web applications.
Google and GitHub are the most common providers.

## SOTA Findings (2026)

### Authentication Standards

OAuth 2.1 is now the recommended standard, consolidating
best practices from OAuth 2.0.

Source: [OAuth 2.1 RFC](https://oauth.net/2.1/)

### Library Recommendations

- **Node.js**: Use `@auth/core` (Auth.js v5)
- **Security**: Always use PKCE, even for confidential clients

Source: [Auth.js Documentation](https://authjs.dev)

## Key Decisions

- **Use OAuth 2.1**: More secure than 2.0, better defaults
- **Use Auth.js**: Well-maintained, supports multiple providers

## Open Questions

- Which OAuth providers to support initially?
- How to handle token refresh across tabs?

## Implementation Notes

1. Start with Google OAuth (widest user base)
2. Add GitHub OAuth for developer users
3. Implement token refresh with silent refresh

## References

- [OAuth 2.1 Specification](https://oauth.net/2.1/)
- [Auth.js Documentation](https://authjs.dev)
- [OWASP OAuth Security](https://owasp.org/oauth)

## Last Updated

2026-01-30
```

### Step 5: Convert to PLAN.md Tasks

Break research into actionable tasks:

```markdown
## Current Sprint

### OAuth Implementation
- [ ] Set up Auth.js v5 in project
- [ ] Configure Google OAuth provider
- [ ] Implement login/logout flow
- [ ] Add session management
- [ ] Implement token refresh
- [ ] Add CSRF protection
- [ ] Write authentication tests

### Security
- [ ] Enable PKCE for all flows
- [ ] Configure secure cookie settings
- [ ] Add rate limiting to auth endpoints
- [ ] Implement account lockout
```

### Step 6: Add Agent Assignments (Optional)

If using agent-orchestration:

```markdown
## Agent Assignments

| Task | Agent Type | Dependencies |
|------|------------|--------------|
| Set up Auth.js | Implement | None |
| Configure Google | Implement | Setup complete |
| Login flow | Implement | Provider configured |
| Tests | Review | Implementation complete |
```

### Step 7: Report Conversion

Output summary:

```
Research converted to plan:

RESEARCH.md updated:
  - Added SOTA findings from 5 sources
  - Documented 3 key decisions
  - Listed 2 open questions
  - Added 4 references

PLAN.md updated:
  - Added 11 tasks to Current Sprint
  - Organized into 2 categories: Implementation, Security

AGENTS.md (optional):
  - Created 4 agent assignments

Next steps:
1. Review open questions in RESEARCH.md
2. Prioritize tasks in PLAN.md
3. Start implementation with first task
```

## Research Categories

### Technical Research

Focus on:
- Current library versions and recommendations
- API changes and deprecations
- Performance considerations
- Security best practices

### Pattern Research

Focus on:
- Architecture patterns
- Code organization
- Error handling approaches
- Testing strategies

### Ecosystem Research

Focus on:
- Compatible tools and libraries
- Community standards
- Framework conventions
- Deployment patterns

## Skill Chaining

### With web search

Use WebSearch to find current information:
- Always include "2026" in queries
- Verify sources are recent
- Cross-reference multiple sources

### With agent-orchestration

Research agents feed into planning:
1. Multiple research agents gather information
2. research-to-plan synthesizes findings
3. Implementation agents execute plan

### With doc-maintenance

After implementation:
1. Mark PLAN.md tasks complete
2. Update RESEARCH.md with learnings

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "I know the research" | Knowledge cutoff may be stale | Web search for 2026 |
| "Research is done" | Needs to be actionable | Convert to tasks |
| "Tasks are obvious" | Implicit knowledge is lost | Document explicitly |
| "Plan is in my head" | Future sessions need context | Write to PLAN.md |

## Example Session

```
/research-to-plan "implement real-time notifications"

Searching for SOTA 2026...

Found 8 relevant sources:
1. Server-Sent Events vs WebSockets (2026)
2. Notification best practices
3. Push notification standards
4. Real-time architecture patterns

Key findings:
- SSE preferred for unidirectional (server→client)
- WebSocket for bidirectional communication
- Web Push API for background notifications

Writing RESEARCH.md...

Converting to plan...

Tasks generated:
1. [ ] Choose notification transport (SSE vs WS)
2. [ ] Set up SSE endpoint
3. [ ] Implement client listener
4. [ ] Add notification types
5. [ ] Handle reconnection
6. [ ] Add notification preferences
7. [ ] Write integration tests

Continue to implementation? [y/n]
```

## Notes

- Always search web for current SOTA
- Include 2026 in search queries
- Document sources with links
- Break large tasks into smaller ones
- Consider security implications
- Add open questions for unknowns
