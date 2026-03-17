---
description: Add a learned pattern (sign) that Ralph will remember for future stories.
---

# Add Sign

The user wants to add a sign - a pattern or rule that Ralph should remember for all future work.

**Get the pattern from the user.** Ask:
1. What's the pattern or rule? (e.g., "Always use select_related for foreign keys")
2. What category? (frontend, backend, general, testing)

**Then run:**

```bash
npx ralph sign "THE PATTERN HERE" CATEGORY
```

**Examples:**
```bash
npx ralph sign "Never hardcode AI model names - use env vars" backend
npx ralph sign "Always add data-testid for Playwright tests" frontend
npx ralph sign "Use useCallback for event handlers passed to children" frontend
npx ralph sign "Always paginate list endpoints" backend
```

**After adding, confirm:** "Added sign. Ralph will include this in every future story prompt."

**To see all signs:**
```bash
npx ralph signs
```
