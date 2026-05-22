---
name: kaizen
description: Continuous improvement methodology for SignalRoom. Use after incidents, when reviewing processes, or when looking for ways to prevent repeat problems. Implements structured retrospectives and improvement cycles.
---

# Kaizen — Continuous Improvement

## Philosophy

**Kaizen** (改善) means "change for better." Small, continuous improvements compound over time.

After every incident or friction point:
1. Understand what happened
2. Identify the root cause
3. Implement a prevention measure
4. Document the learning

## The 5 Whys

Drill down to root cause by asking "Why?" five times:

```
Problem: Deployment flooded Slack with errors

Why? → Worker kept failing with auth errors
Why? → Database password was wrong
Why? → Credentials weren't loading from .env
Why? → env_file setting was removed from config
Why? → Engineer conflated unrelated errors and made unnecessary changes

Root Cause: Panic-driven debugging without understanding the problem
Prevention: Pre-deployment checklist, local testing requirement
```

## Post-Incident Template

After any incident, create a record:

```markdown
# Incident: [Brief Title]
**Date:** YYYY-MM-DD
**Duration:** X minutes
**Impact:** What was affected

## Timeline
- HH:MM - What happened
- HH:MM - What was tried
- HH:MM - What fixed it

## Root Cause
Single sentence explaining the actual cause.

## What Should Have Happened
The correct sequence of actions.

## Prevention Measures
- [ ] Specific action item 1
- [ ] Specific action item 2

## Learnings
What we now know that we didn't before.
```

## PDCA Cycle

**Plan → Do → Check → Act**

| Phase | Action | SignalRoom Example |
|-------|--------|-------------------|
| **Plan** | Identify improvement | "Add pre-deploy checklist" |
| **Do** | Implement small change | Add checklist to CLAUDE.md |
| **Check** | Verify it works | Next deploy follows checklist |
| **Act** | Standardize or adjust | Update checklist based on feedback |

## Improvement Categories

### Process Improvements

- Pre-deployment checklists
- Local testing requirements
- Code review standards
- Documentation updates

### Tooling Improvements

- Better error messages
- Automated checks
- Monitoring and alerts
- Skills and shortcuts

### Knowledge Improvements

- Document tribal knowledge
- Create runbooks
- Update CLAUDE.md
- Add skills for common patterns

## SignalRoom Improvements Log

Track improvements over time:

| Date | Trigger | Improvement | Location |
|------|---------|-------------|----------|
| 2025-12-19 | Fly.io incident | Deployment discipline section | CLAUDE.md |
| 2025-12-19 | Fly.io incident | Deploy skill with checklist | .claude/skills/deploy |
| 2025-12-19 | Fly.io incident | Root-cause-tracing skill | .claude/skills/root-cause-tracing |

## Questions to Ask

After any friction:

1. **What took longer than expected?**
2. **What caused confusion?**
3. **What would have helped to know beforehand?**
4. **What will we do differently next time?**
5. **How do we prevent this class of problem?**

## Anti-Patterns to Avoid

### Blame Culture
Focus on process failures, not people. "The process allowed this to happen" not "X made a mistake."

### Improvement Theater
Creating documentation nobody reads. Make improvements actionable and discoverable.

### Over-Engineering
Don't build a framework when a checklist will do. Start simple, iterate.

### Forgetting
Improvements only work if they're discoverable. Put them where they'll be seen (CLAUDE.md, skills, pre-commit hooks).

## Integrating with Skills

Skills are a kaizen mechanism:
- After learning something, encode it in a skill
- Next time the situation arises, Claude uses the skill automatically
- Knowledge persists across sessions

Example: Today's deployment incident → deploy skill → future deployments follow the checklist automatically.

## The Compound Effect

```
Day 1: Add pre-deploy checklist
Day 7: Add root-cause-tracing skill
Day 14: Add automated local test before deploy
Day 30: Deployments that used to take 45 minutes now take 5
```

Small improvements. Consistent application. Compounding results.
