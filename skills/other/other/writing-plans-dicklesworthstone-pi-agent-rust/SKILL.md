---
name: writing-plans
description: Create detailed implementation plans with bite-sized tasks
version: 1.0.0
author: Ariff
when_to_use: After design is complete, before implementation
---

# Writing Implementation Plans

## Purpose
Create comprehensive plans assuming the implementer has zero context.

> "I'm using the Writing Plans skill to create the implementation plan."

**Save to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Plan Header Template

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]
**Estimated Tasks:** [count]

---
```

## Task Granularity

Each step = ONE action (2-5 minutes):
- "Write the failing test" ← step
- "Run it to confirm failure" ← step
- "Implement minimal code" ← step
- "Run tests, confirm pass" ← step
- "Commit" ← step

**NOT:** "Write tests and implement feature" ← too big

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:lines`
- Test: `tests/path/to/test.ts`

**Step 1: Write failing test**
\`\`\`typescript
test('should do X', () => {
  expect(thing()).toBe(expected);
});
\`\`\`

**Step 2: Verify failure**
Run: `npm test -- --grep "should do X"`
Expected: FAIL - "thing is not defined"

**Step 3: Implement**
\`\`\`typescript
export function thing() {
  return expected;
}
\`\`\`

**Step 4: Verify pass**
Run: `npm test -- --grep "should do X"`
Expected: PASS

**Step 5: Commit**
\`\`\`bash
git add -A && git commit -m "feat: add thing"
\`\`\`
```

## Plan Principles

| Principle | Meaning |
|-----------|---------|
| **DRY** | Don't repeat yourself |
| **YAGNI** | Don't build what's not needed |
| **TDD** | Test first, always |
| **Small commits** | One logical change per commit |

## What to Include

- ✅ Exact file paths
- ✅ Complete code snippets (not "add validation")
- ✅ Exact commands with expected output
- ✅ Dependencies to install
- ✅ Environment setup needed

## Handoff

After saving plan:

```markdown
**Plan saved to `docs/plans/[filename].md`**

Ready to execute. Options:
1. **Execute now** - I'll work through tasks with you
2. **Subagent execution** - Fresh agent per task with review gates
3. **Later** - Plan saved for future session
```

If executing → Use `executing-plans` skill
