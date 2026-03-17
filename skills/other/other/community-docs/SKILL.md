---
name: community-docs
description: >
  Community superstitions - unverified observations from pattern development.
  Use when encountering undocumented edge cases or framework quirks not in
  official docs. Verified knowledge should be upstreamed to labs docs.
---

# Community Docs (Superstitions)

**Location:** `community-docs/` in community-patterns repo

**CRITICAL:** These are NOT official framework documentation. Always check `~/Code/labs/docs/common/` first.

Community docs capture empirical observations discovered during pattern development - unverified things that seemed to work but may be coincidence or context-specific.

## Superstitions (⚠️ Treat With Skepticism)

**Location:** `superstitions/`

Single observations only. May be wrong, incomplete, or context-specific.

- **Treat with extreme skepticism**
- May be wrong, incomplete, or context-specific
- Each has prominent warning disclaimer
- Try if completely stuck, but verify thoroughly

## When to Consult Superstitions

**After checking official labs/docs/ first:**
- Encountering undocumented edge cases
- Framework behaving unexpectedly
- TypeScript errors not explained in official docs
- Before creating new superstition (check if already documented)

**Do NOT consult before official docs** - labs/docs/ is always more authoritative!

## Searching Superstitions

```bash
# Search superstitions
grep -r "Cell.*handler" community-docs/superstitions/

# List superstitions by topic
ls community-docs/superstitions/ | grep "types-"
ls community-docs/superstitions/ | grep "reactivity-"
```

## If a Superstition Works

**Upstream it to labs docs** instead of keeping it here:

1. Identify the appropriate doc in `~/Code/labs/docs/common/`
2. Add the information to that doc
3. Create a PR to labs
4. Once merged, delete the superstition

**The goal is for verified knowledge to live in official docs, not here.**

## Creating a New Superstition

**Only after solving something not in any docs:**

1. **Search first** - Check it's not already documented:
   ```bash
   grep -r "your topic" ~/Code/labs/docs/common/
   grep -r "your topic" community-docs/superstitions/
   ```

2. **Create file:** `community-docs/superstitions/YYYY-MM-DD-topic-brief-description.md`
   - Use topic prefixes: `types-`, `reactivity-`, `jsx-`, `handlers-`, `llm-`, `patterns-`, etc.

3. **Copy template** from `community-docs/superstitions/README.md`

4. **Include full ⚠️ disclaimer** at top

5. **Document:**
   - What problem you had
   - What you tried that didn't work
   - What solution seemed to work
   - Code examples (before/after)
   - Your context
   - Related official docs

6. **Commit:** `"Add superstition: [brief description]"`

**Remember:** You're creating a hypothesis, not stating fact! Be humble about uncertainty.

## Deprecated Tiers

The `blessed/` and `folk_wisdom/` directories are **deprecated**. Previously we had a three-tier promotion system. Now, verified knowledge should be upstreamed directly to labs docs.

## Important Notes

**Skepticism is critical:**
- Superstitions may be wrong or context-specific
- **Always prefer official labs/docs/ when they exist**

**Do NOT:**
- Trust superstitions blindly
- Skip checking official docs first
- Create superstition for things in official docs

**DO:**
- Read disclaimer on every superstition
- Verify against official docs
- Test thoroughly before relying on it
- Upstream verified knowledge to labs docs

**Superstitions are a safety net for edge cases, not a primary reference!**

## Related Skills

- **recovery-strategies** - Use superstitions as part of recovery escalation
- **pattern-dev** - Reference when stuck on implementation
