---
name: dual-pass-review
description: Use AFTER any code changes (feature implementation, bug fix, refactor) to enforce mandatory dual-pass review. First pass reviews unstaged changes for correctness and convention compliance. Second pass ONLY executes if first pass made any corrections. Ensures work follows project conventions, development rules, and best practices before task completion.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Dual-Pass Code Review Workflow

Mandatory review checkpoint that runs after any code changes to ensure quality and convention compliance.

## Core Principle

**Every code change requires verification before task completion.**

Two review passes:
1. **First Pass**: Review unstaged changes for correctness + convention compliance
2. **Second Pass**: Conditional - ONLY if first pass made changes, review again

## When to Use

Trigger AUTOMATICALLY after:
- Feature implementation (`/cook`, `/code`)
- Bug fixes (`/fix`, `/debug`)
- Refactoring (`/refactor`)
- Any edit/write operations that modify code

## Review Dimensions

### 1. Task Correctness
- [ ] Changes address the original task/requirement
- [ ] No missing pieces or incomplete logic
- [ ] Edge cases handled appropriately
- [ ] No unintended side effects

### 2. Project Conventions
- [ ] Follows Clean Architecture layers
- [ ] Uses correct repository pattern (service-specific, not generic)
- [ ] CQRS patterns: Command + Handler + Result in ONE file
- [ ] Entity patterns: static expressions, computed properties have empty `set { }`
- [ ] Frontend: correct base class hierarchy
- [ ] Frontend: BEM class naming on ALL elements

### 3. Development Rules Compliance
- [ ] YAGNI - No unnecessary features/abstractions
- [ ] KISS - Simplest solution that works
- [ ] DRY - No code duplication (search first, reuse existing)
- [ ] Logic in LOWEST layer (Entity > Service > Component)
- [ ] DTO mapping in DTO class, not handler
- [ ] Side effects in event handlers, not command handlers

### 4. Code Quality
- [ ] No syntax errors, code compiles
- [ ] Meaningful naming
- [ ] Single Responsibility Principle
- [ ] Proper error handling
- [ ] No security vulnerabilities

## Execution Protocol

### Step 1: Get Unstaged Changes

```bash
# Check for unstaged changes
git status --short

# Get full diff of unstaged changes
git diff

# Get diff of staged changes (if any)
git diff --staged
```

### Step 2: First Pass Review

For EACH changed file, verify:

```markdown
## First Pass Review Checklist

### File: [filename]

**Task Correctness:**
- [ ] Addresses original requirement
- [ ] Logic is complete and correct
- [ ] No missing edge cases

**Convention Compliance:**
- [ ] Follows platform patterns from CLAUDE.md
- [ ] Uses correct base classes
- [ ] Naming conventions followed
- [ ] BEM classes on all template elements (frontend)

**Development Rules:**
- [ ] YAGNI/KISS/DRY compliance
- [ ] Logic in correct layer
- [ ] No anti-patterns (side effects in handlers, generic repos, etc.)

**Quality:**
- [ ] Compiles without errors
- [ ] No security issues
- [ ] Proper error handling
```

### Step 3: First Pass Corrections

If issues found:
1. Document each issue clearly
2. Fix issues immediately
3. Track that corrections were made

```markdown
## First Pass Corrections Made

1. [File:Line] - [Issue] → [Fix Applied]
2. [File:Line] - [Issue] → [Fix Applied]
...
```

### Step 4: Conditional Second Pass

**CRITICAL DECISION POINT:**

```
IF first_pass_made_changes == true:
    EXECUTE full second pass review
ELSE:
    SKIP second pass, proceed to summary
```

### Step 5: Second Pass Review (If Needed)

Re-run complete review on current unstaged changes:

```bash
# Get fresh diff after corrections
git diff
```

Verify ALL checklist items again:
- Task correctness
- Convention compliance
- Development rules
- Code quality

### Step 6: Generate Summary

```markdown
## Dual-Pass Review Summary

**First Pass:**
- Files reviewed: [count]
- Issues found: [count]
- Corrections made: [yes/no]

**Second Pass:**
- Executed: [yes/no]
- Reason: [first pass made changes / first pass clean]
- Additional issues: [count if executed]

**Final Status:** [APPROVED / NEEDS ATTENTION]

**Remaining Concerns:**
- [List any minor items for future consideration]
```

## Common Issues to Check

### Backend Anti-Patterns

```csharp
// Side effect in handler (WRONG)
await notificationService.SendAsync(...);
// → Move to UseCaseEvents/ event handler

// Generic repository (WRONG)
IPlatformRootRepository<Entity>
// → Use service-specific: IMyServiceRootRepository<Entity>

// Mapping in handler (WRONG)
var entity = new Entity { Name = req.Name };
// → Use DTO.MapToEntity() or Command.MapToNewEntity()

// Missing eager loading (WRONG)
await repo.GetAllAsync(...)
// → Add: ct, e => e.Related
```

### Frontend Anti-Patterns

```typescript
// Missing BEM class (WRONG)
<div><span>{{ name }}</span></div>
// → <div class="user-card__content"><span class="user-card__name">{{ name }}</span></div>

// Missing untilDestroyed (WRONG)
this.data$.subscribe(...)
// → this.data$.pipe(this.untilDestroyed()).subscribe(...)

// Logic in component (WRONG)
readonly types = [{ value: 1, label: 'Type A' }];
// → Move to Entity: static readonly dropdownOptions = [...]

// Direct HttpClient (WRONG)
constructor(private http: HttpClient) {}
// → Extend PlatformApiService
```

## Integration with Workflows

This skill is the FINAL step before task completion in:

| Workflow | Sequence (Updated) |
|----------|-------------------|
| Feature | plan → cook → test → **dual-pass-review** → docs-update → watzup |
| Bug Fix | debug → plan → fix → test → **dual-pass-review** |
| Refactor | plan → code → test → **dual-pass-review** |

## Review Commands

```bash
# Quick convention check
grep -r "IPlatformRootRepository" --include="*.cs"  # Should be service-specific
grep -r "new Entity {" --include="*Handler.cs"  # Should be in DTO
grep -r "SendAsync\|NotifyAsync" --include="*CommandHandler.cs"  # Should be in event handler

# Frontend checks
grep -r "class=\"\"" --include="*.html"  # Empty class (suspicious)
grep -r "subscribe()" --include="*.ts" | grep -v "untilDestroyed"  # Missing cleanup
```

## Key Rules

1. **NEVER skip first pass** - Always review unstaged changes
2. **Second pass is CONDITIONAL** - Only if first pass made corrections
3. **Be honest and brutal** - Flag all issues, don't be lenient
4. **Evidence-based** - Cite specific files and lines
5. **Follow project conventions** - Check CLAUDE.md patterns

## Output Format

Always end with clear status:

```markdown
---
**Review Status:** [APPROVED / CORRECTIONS NEEDED]
**Passes Executed:** [1 / 2]
**Ready for Commit:** [Yes / No]
---
```
