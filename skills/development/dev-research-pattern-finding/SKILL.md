---
name: dev-research-pattern-finding
description: Find existing code patterns before implementing new features
category: research
---

# Pattern Finding

Find existing implementations in the codebase before writing new code.

## Process

1. **Identify key terms** from the task description
2. **Search for similar code** using Glob/Grep
3. **Analyze the patterns** used in existing implementations
4. **Document findings** for implementation

## Search Strategies

### By Feature Name
```bash
# Find files related to player movement
Glob("**/*movement*")
Glob("**/*player*")

# Search for specific patterns
Grep("function.*movement", "src/")
```

### By File Type
```bash
# Find React components
Glob("src/components/**/*.tsx")

# Find hooks
Glob("**/hooks/*.ts")
```

### By Pattern
```bash
# Find useState patterns
Grep("useState.*THREE", "src/")

# Find useEffect cleanup
Grep("useEffect.*return.*cleanup", "src/")
```

## What to Look For

- **Import patterns** - How are modules imported?
- **Component structure** - Functional vs class, hooks used
- **State management** - Zustand stores, contexts
- **API patterns** - How are API calls made?
- **Error handling** - Try/catch patterns
- **File organization** - Where does code belong?

## Output Format

Document findings as:
```
## Pattern: {pattern name}

Found in: {file paths}

Usage: {how it's used}

Key elements:
- {element 1}
- {element 2}
```

## Anti-Patterns

❌ **DON'T:**

- Search too broadly - `Grep("function")` returns too many results
- Skip reading context - Copying code without understanding causes bugs
- Assume patterns are correct - Existing code may have technical debt
- Ignore test files - Tests often show how code is meant to be used
- Search only one way - Combine Glob + Grep for best results

✅ **DO:**

- Use specific search terms - `Grep("function.*movement", "src/components/")`
- Read multiple examples - Find the common pattern across implementations
- Check test files - Tests reveal intended usage patterns
- Verify patterns work - Don't copy broken or outdated code
- Document findings - Write down patterns for reference during implementation
