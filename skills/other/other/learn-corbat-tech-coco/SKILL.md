---
name: learn
description: Extract reusable patterns from the current session and save them as skills. Use after solving a non-trivial problem to capture the solution for future sessions. Saves to .claude/skills/learned/.
allowed-tools: Read, Write, Bash, Glob
---

# Learn — Extract Reusable Patterns

Capture valuable problem-solving approaches from this session and save them as reusable skills.

## When to Use

Use `/learn` after you've solved something non-trivial:
- Fixed a tricky TypeScript/ESM error that required research
- Discovered a non-obvious corbat-coco pattern or convention
- Worked around a library quirk or API constraint
- Found the right way to mock something in Vitest
- Figured out a complex git workflow
- Solved a provider-specific integration issue

**Don't capture**: typos, obvious syntax errors, one-time situations.

## Extraction Process

### 1. Reflect on the Session
Identify what was solved:
- What was the problem or question?
- What made it non-obvious?
- What was the solution?
- Will this pattern likely appear again?

### 2. Categorize the Pattern

| Category | Examples |
|----------|---------|
| **error-resolution** | TypeScript error fixes, ESM import issues |
| **debugging** | How to diagnose provider failures, tool errors |
| **workaround** | Library quirks, Node.js version specifics |
| **pattern** | corbat-coco conventions, architecture patterns |
| **workflow** | Git operations, pnpm commands, release steps |

### 3. Write the Skill File

Save to `.claude/skills/learned/<pattern-name>/SKILL.md`:

```markdown
---
name: [pattern-name]
description: [One-line description of when to use this pattern]
---

# [Pattern Title]

## Problem

[What situation triggers the need for this pattern?]

## Solution

[The approach that works]

## Example

[Concrete code example or command sequence]

\`\`\`typescript
// Context: corbat-coco TypeScript ESM
// Problem: [describe]
// Solution:
[code]
\`\`\`

## Why It Works

[Brief explanation of the underlying mechanism]

## Activation

Use this skill when you encounter:
- [trigger 1]
- [trigger 2]
```

### 4. Save the File

```bash
mkdir -p .claude/skills/learned/[pattern-name]
# Then write SKILL.md with Write tool
```

### 5. Confirm

Report what was saved:
```
✅ Learned: [pattern-name]
   Saved to: .claude/skills/learned/[pattern-name]/SKILL.md
   Trigger: [when this will be useful]
```

## Quality Standards

- **Focused**: One pattern per skill (not "everything I learned today")
- **Reusable**: Will this help in future sessions on this project?
- **Specific**: Include concrete code examples, not abstract descriptions
- **Actionable**: Someone reading it cold should know what to do

## Example: ESM Import Resolution Pattern

After solving a `Cannot find module './foo'` error:

```markdown
---
name: esm-import-js-extension
description: TypeScript ESM imports require .js extension even for .ts source files
---

# ESM Import .js Extension Requirement

## Problem
`Cannot find module './foo'` even though `./foo.ts` exists.

## Solution
TypeScript ESM requires `.js` extension in imports (resolved to `.ts` at compile time):

\`\`\`typescript
// ❌ Fails
import { bar } from "./foo";

// ✅ Works
import { bar } from "./foo.js";
\`\`\`

## Why It Works
Node.js ESM resolver looks for literal file extensions. TypeScript with `moduleResolution: NodeNext`
maps `.js` → `.ts` at compile time. This is intentional, not a bug.

## Activation
Whenever you see "Cannot find module" for a local import in corbat-coco.
```

## Usage

```
/learn                    # extract from this session
/learn the mock pattern   # extract specific thing learned
/learn esm import issue   # extract specific resolved issue
```
