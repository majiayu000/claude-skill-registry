---
name: build
description: Build features with AI coding tools (Claude Code, Lovable, Replit, Cursor). Use when implementing specs, iterating on AI code, or choosing tools. Focuses on tool selection, effective prompting, and iteration workflows for non-technical founders.
---

# Build

## Tool Selection

**Starting from scratch?** → Lovable (fastest MVP)  
**Existing codebase?** → Claude Code (best context)  
**Learning to code?** → Replit (educational)  
**Already code?** → Cursor (power features)

See [TOOLS.md](TOOLS.md) for detailed comparison.

---

## Build Workflow

```
- [ ] Start with spec (use scope skill)
- [ ] Give spec to AI tool
- [ ] Test happy path + edge cases
- [ ] Give specific feedback on issues
- [ ] Iterate (expect 2-4 rounds)
- [ ] Deploy when working
```

---

## Giving AI Your Spec

### Claude Code
```
Build this feature: [paste spec]

Codebase: React + TypeScript + Tailwind
Reference: src/components/Button.tsx for button patterns
```

### Lovable
```
Build: [paste simplified spec focusing on outcome]
Make it look like Linear (minimal, clean)
```

### Replit
```
Create: [paste spec emphasizing what user sees]
Use React. Keep simple.
```

See [PROMPTS.md](PROMPTS.md) for patterns.

---

## Reviewing What AI Built

Test, don't just run:

```
- [ ] Looks right?
- [ ] Happy path works?
- [ ] Edge cases work?
- [ ] Works on mobile?
- [ ] Error messages clear?
```

---

## Giving Feedback

**Bad:** "This doesn't work"  
**Good:** "Clicking 'Save' does nothing. Expected: 'Saved!' message"

**Template:**
```
What I tried: [action]
Expected: [outcome]
Got: [what happened]
```

---

## Iteration Expectations

**Normal:** 2-4 rounds per feature  
**First build:** AI builds from spec, you find 3-5 issues  
**Second build:** Fixes those, you find 1-2 more  
**Third build:** Final polish

**Stop when:**
- Happy path works
- Edge cases handled
- Mobile works
- No obvious bugs

**Don't iterate for:**
- Perfection
- Features beyond spec
- Premature optimization

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No spec | Use scope skill first |
| "Build a dashboard" | Specify what's on it |
| Skip edge case testing | Try breaking it |
| Accept without review | Always test |
| Add features mid-build | Finish current feature first |
| Fix code yourself | Describe problem, let AI fix |

---

## Right-Sizing Work

**Too big:** "Build entire app"  
**Too small:** "Add one button"  
**Right:** "Build user auth flow" (1-3 hours)

**Good chunks:**
- User login/signup flow
- Dashboard with 4 metrics
- Settings page with profile editing

---

## When Stuck

**AI keeps breaking things:**
→ Break into smaller piece, start fresh session

**Can't figure out complex feature:**
→ Ask: "What's simplest way?" Accept simpler solution

**Each fix breaks something else:**
→ Stop. Ask: "Better approach?" Consider starting over

---

## Working with Existing Code

```
Add [feature] to existing project.

Stack: [React, Next.js, etc]
Patterns: Check src/components for examples
Style: Tailwind + custom design system
Follow existing code style
```

---

## Prompting Patterns

**Reference existing:**
```
Build Settings page.
Reference Dashboard page layout.
Use same Card/Button components.
```

**Provide examples:**
```
Pricing page with 3 tiers.
Like Linear's pricing - clean, minimal.
```

**Specify constraints:**
```
Build profile page.
Must work offline.
Load under 2 seconds.
WCAG AA accessible.
```

See [PROMPTS.md](PROMPTS.md) for more.

---

## Review for Non-Technical Founders

**Check:**
- Does it match spec?
- Buttons work?
- Forms validate?
- Looks like design reference?
- Works on mobile?
- Error messages clear?

**Don't check:**
- Code cleanliness
- Optimization
- "Best practices"

AI handles code quality. You handle requirements.

---

## Success Looks Like

✅ Features match specs  
✅ 2-4 iterations (not 10+)  
✅ Can explain what's wrong  
✅ Building faster each week
