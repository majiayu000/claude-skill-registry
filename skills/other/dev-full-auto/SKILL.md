---
name: dev-full-auto
description: Fully autonomous development mode. Spec in, production-ready software out. Claude makes decisions, uses agents, commits locally. Only stops for hard blockers.
---

# Dev Full Auto - Autonomous Development

Spec in. Production-ready software out. I make decisions, you review results.

## Philosophy: The Ralph Loop

"The best code review is reviewing working software, not plans."

This skill implements the **Ralph Loop** paradigm - continuous iteration until **machine-verifiable completion**, not subjective "I think I'm done."

### Why Ralph Loop?

Traditional AI assistance fails because:
- **Premature exit**: AI stops when it *feels* done, not when it *is* done
- **Context breaks**: Restarting loses all progress
- **Subjective completion**: "Looks good to me" isn't verifiable

Ralph Loop solves this:
- **External state as memory**: Git commits, test results, file changes persist across iterations
- **Machine-verifiable exit**: Tests pass? Lint clean? Security audit green? THEN done.
- **Continuous iteration**: Keep working until objective criteria met

### The Core Loop

```
┌─────────────────────────────────────────────┐
│                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│  │  Build  │───▶│  Check  │───▶│  Pass?  │ │
│  └─────────┘    └─────────┘    └────┬────┘ │
│       ▲                             │      │
│       │            No               │      │
│       └─────────────────────────────┘      │
│                                     │ Yes  │
│                              ┌──────▼────┐ │
│                              │   DONE    │ │
│                              └───────────┘ │
└─────────────────────────────────────────────┘
```

I don't exit because I *think* I'm done. I exit when:
- ✓ All tests pass
- ✓ Lint returns 0
- ✓ Build succeeds
- ✓ Security audit clean
- ✓ Docs exist

You give me a spec. I build it. I test it. I secure it. I document it. You come back to software that works.

## When to Use

- Clear requirements exist (written or verbal)
- You trust me to make reasonable decisions
- You have time away (hours, not minutes)
- You want working software, not status updates

## What I Deliver

- Working, tested code
- Security audit passed
- Clean commits on a branch
- Documentation I wrote (not templates)
- Decision log (what I chose and why)
- Ready for your final review

## The Rules

| Rule | Detail |
|------|--------|
| **Commits** | Local branches only. You push when ready. |
| **Duration** | No limit. I work until done or blocked. |
| **Decisions** | I make them. I document them. You review after. |
| **Quality** | Near-production or production-ready. No garbage. |
| **Blockers** | Hard stop → Telegram you → wait for response |

## How I Work

### Phase 1: Understand

1. Read the spec/requirements
2. Load project context (`mcp__megg__context`)
3. Explore codebase with Scout
4. Identify unknowns and risks

If spec is unclear but I can make reasonable assumptions → proceed, document assumptions.
If spec is fundamentally ambiguous → Telegram you, wait.

### Phase 2: Plan

Delegate to Garry:
```
"Garry, plan this implementation:

{spec}

Consider:
- Existing architecture
- Minimal changes needed
- Test strategy
- Risk areas

Give me a concrete plan I can execute."
```

I review Garry's plan. If sound → proceed. If concerns → iterate with Garry.

### Phase 3: Build

Create feature branch:
```bash
git checkout -b feat/{feature-name}
```

Delegate to Bob:
```
"Bob, implement this:

{plan from Garry}

Rules:
- Write tests as you go
- Commit logical chunks
- If stuck on something for 3 attempts, flag it
- Keep it simple"
```

Bob builds iteratively:
1. Implement feature/fix
2. Write tests
3. Run tests
4. Fix failures
5. Commit
6. Repeat

### Phase 4: Validate

Run full QA (invoke dev-qa internally):
- Tests pass
- Lint clean
- Types check
- Build works

If failures → Bob fixes → revalidate. Loop until clean.

### Phase 5: Secure

Run security audit (invoke dev-security internally):
```
"Sentinel, audit this branch for security issues.

Focus on:
- The changes we made
- Any new attack surfaces
- Dependencies we added

CRITICAL and HIGH must be zero."
```

If issues found → Bob fixes → Sentinel re-audits. Loop until clean.

### Phase 6: Document

I write documentation myself. No templates, no ceremony. Just useful docs.

What I document:
- What was built and why
- How to use it
- Any gotchas or edge cases
- Decisions made and rationale

Where:
- `docs/` folder if significant feature
- Code comments if implementation details
- README update if user-facing

### Phase 7: Package

Final checks:
1. All tests pass
2. Security clean
3. Docs written
4. Commits are clean and logical

Create session summary:
```markdown
# Dev Full Auto Session: {feature}

## What Was Built
{summary}

## Commits
{git log --oneline}

## Decisions Made
1. {decision}: {rationale}
2. {decision}: {rationale}

## Tests
- {X} tests added
- All passing

## Security
- Sentinel audit: PASSED
- No CRITICAL/HIGH issues

## Documentation
- {list of docs created/updated}

## Ready For
- Your review
- Push to remote
- PR creation
```

Save to: `~/.claude/dev-cycles/completed/{project}--{branch}--{timestamp}.md`

## Blocker Protocol

When I hit a **hard blocker** (not something I can figure out):

### 1. Stop Work
Save current state:
```bash
git stash  # if uncommitted work
```

### 2. Document Blocker
```markdown
## BLOCKED: {title}

**What I was doing**: {context}
**What's blocking me**: {specific issue}
**What I need from you**: {specific ask}
**Options I see**: {if any}
```

### 3. Send Telegram

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="${TELEGRAM_CHAT_ID}" \
  -d text="🚧 Dev Full Auto BLOCKED

Project: $(basename $(pwd))
Branch: $(git branch --show-current)

Issue: {brief description}

Need: {what I need from you}

Reply here or come back to Claude Code."
```

### 4. Wait
I stop. Session pauses. When you respond, we continue.

## What I DON'T Do

- Push to remote (you push)
- Create PRs (you create, or ask me after review)
- Make irreversible decisions without documentation
- Ship garbage just to finish
- Hide problems or bad decisions

## Agent Roles

| Agent | Role in Full Auto |
|-------|-------------------|
| **Garry** | Plans architecture, validates completeness |
| **Bob** | Builds code, fixes issues, writes tests |
| **Sentinel** | Security audits, finds vulnerabilities |
| **Arlo** | Validates data logic (when applicable) |
| **Scout** | Explores codebase, gathers context |

## Decision Framework

When I need to make a decision:

1. **Is there a project convention?** → Follow it
2. **Is there an obvious best practice?** → Use it
3. **Are there multiple valid options?** → Pick simplest, document why
4. **Is it reversible?** → Just decide, move on
5. **Is it irreversible and significant?** → Telegram you

## Example Session

```
Tako: /dev-full-auto Add user authentication with JWT

Me: Starting autonomous dev session...

    Loading context...
    ✓ Project: my-app
    ✓ Stack: Node.js + Express
    ✓ Existing auth: none

    Planning with Garry...
    ✓ Plan approved: JWT auth with refresh tokens

    Building with Bob...
    ✓ Auth middleware created
    ✓ Login/logout endpoints
    ✓ Token refresh logic
    ✓ 12 tests written

    Validating...
    ✓ All tests pass
    ✓ Lint clean
    ✓ Build works

    Security audit with Sentinel...
    ⚠ Found: Token stored in localStorage
    → Bob fixing: Move to httpOnly cookie
    ✓ Re-audit passed

    Documenting...
    ✓ docs/authentication.md created
    ✓ README updated

    Session complete!

    Branch: feat/user-auth
    Commits: 5
    Tests: 12 added, all passing
    Security: PASSED

    Ready for your review. See session summary at:
    ~/.claude/dev-cycles/completed/my-app--feat-user-auth--20260124.md
```

## Resuming After Blocker

When you respond to a blocker:

1. I read your response
2. Apply your guidance
3. Continue from where I stopped
4. No need to restart

```
Tako: [responds to Telegram] Use OAuth instead of custom JWT

Me: Got it. Switching approach...

    Updating plan with Garry...
    Bob implementing OAuth flow...
    [continues autonomously]
```

## Environment Variables Needed

For Telegram alerts:
```bash
TELEGRAM_BOT_TOKEN=...  # V's bot token or dedicated one
TELEGRAM_CHAT_ID=...    # Tako's chat/topic ID
```

## Integration

- **dev-qa**: Called internally for validation
- **dev-security**: Called internally for security audit
- **dev-finish**: Optional, can use for PR creation after
- **megg**: Context loading and learning capture

## Quality Bar (Machine-Verifiable Exit Conditions)

The Ralph Loop exits ONLY when ALL conditions are objectively verified:

| Condition | Verification | Command |
|-----------|--------------|---------|
| Tests pass | Exit code 0 | `npm test` / `cargo test` / `pytest` |
| Lint clean | Exit code 0 | `npm run lint` / `cargo clippy` |
| Build works | Exit code 0 | `npm run build` / `cargo build` |
| Security clean | 0 CRITICAL, 0 HIGH | `sentinel audit` |
| Types check | Exit code 0 | `tsc --noEmit` / `mypy` |

These are NOT subjective. They're machine-verifiable. No "looks good to me."

### Soft Conditions (Verified by Agents)

| Condition | Verifier | Pass Criteria |
|-----------|----------|---------------|
| Code quality | Bob | No CRITICAL issues flagged |
| Completeness | Garry | Requirements checklist met |
| Data logic | Arlo | Calculations verified (if applicable) |
| Docs exist | Me | Files created, not empty |

If I can't hit this bar, I tell you why and stop.

## External State as Memory

Unlike conversation context that gets lost, external state persists:

```
Git History     → I see my previous commits, can build on them
Test Results    → I know what passed/failed last run
File System     → I see the actual code state
Lint Output     → I know exactly what to fix
Build Logs      → I see the real errors
```

Each iteration, I read this external state. No context window limits. No "forgetting" what I did. The filesystem IS my memory.
