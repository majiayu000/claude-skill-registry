---
name: no_lazy_implementation
description: Prevents "lazy" coding habits by enforcing full implementation and banning placeholders.
allowed-tools: Read, Edit, Write
---

# No Lazy Implementation Protocol

## 1. Zero Placeholder Policy
**Strictly Prohibited:**
- `// ... rest of code`
- `// ... implement logic here`
- `// ... same as above`
- Leaving TODOs for critical business logic that was requested.

**Requirement:**
- You must generate **COMPLETE, WORKING CODE**.
- If a file is too large for one turn, explicitly state: "This is Part 1 of X. I will implement the rest in the next step." and **immediately** proceed to generate the rest.

## 2. Full Method Implementation
- When modifying a file, **never** replace existing working logic with a comment to save output space, unless you are absolutely certain that part of the file is untouched and you are using a diff-friendly tool.
- Even then, prefer context-aware editing that ensures the final file is complete and compilable.

## 3. "It Just Works" Standard
- The code you write must be ready to run.
- Imports must be real.
- Types must be defined (no `any` without strict justification).
- Variable names must be descriptive (no `data1`, `temp`).

## 4. Verification Checklist
Before calling `Edit` or `Write`:
- [ ] Did I simply comment out complex logic to save tokens? (If yes, STOP and write it out).
- [ ] Did I leave a "TODO" for something the user explicitly asked for? (If yes, implement it).
- [ ] Is the code compilable immediately after this edit?
