---
description: Add a learned pattern (lesson) that Ralph will remember for future stories.
---

# Add Lesson

The user wants to add a lesson - a pattern or rule that Ralph should remember for all future work.

**Get the pattern from the user.** Ask:
1. What's the pattern or rule? (e.g., "Always use select_related for foreign keys")
2. What category? (frontend, backend, general, testing)

**Then run:**

```bash
npx agentic-loop lesson "THE PATTERN HERE" CATEGORY
```

**Examples:**
```bash
npx agentic-loop lesson "Never hardcode AI model names - use env vars" backend
npx agentic-loop lesson "Always add data-testid for Playwright tests" frontend
npx agentic-loop lesson "Use useCallback for event handlers passed to children" frontend
npx agentic-loop lesson "Always paginate list endpoints" backend
```

**After adding, confirm:** "Added lesson. Ralph will include this in every future story prompt."

**To see all lessons:**
```bash
npx agentic-loop lessons
```
