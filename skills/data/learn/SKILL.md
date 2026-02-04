---
name: learn
description: Teach Claude a new pattern, preference, or convention explicitly. Use when you want to save a correction, preference, or coding pattern for future sessions. Triggers on keywords like "remember this", "always do", "never do", "learn this pattern", "/learn".
allowed-tools: Read, Write, Edit, Bash
infer: true
---

# Pattern Learning Skill

Explicitly teach Claude patterns, preferences, or conventions that should be remembered across sessions.

## Quick Usage

```
/learn always use PlatformValidationResult instead of throwing ValidationException
/learn [wrong] var x = 1 [right] const x = 1 - always prefer const
/learn prefer async/await over .then() chains in this codebase
```

## Teaching Formats

### Format 1: Natural Language

```
/learn always use IGrowthRootRepository instead of generic IPlatformRootRepository
```

Detected patterns: "always use X instead of Y", "prefer X over Y", "never do X"

### Format 2: Explicit Wrong/Right

```
/learn [wrong] throw new ValidationException("Invalid") [right] return PlatformValidationResult.Invalid("Invalid")
```

Best for code-level corrections with exact examples.

### Format 3: Code Block Comparison

```
/learn
Wrong:
```csharp
public void Process() {
    if (x == null) throw new ArgumentNullException();
}
```

Right:
```csharp
public PlatformValidationResult Process() {
    return x == null
        ? PlatformValidationResult.Invalid("X required")
        : PlatformValidationResult.Valid();
}
```
```

### Format 4: Category-Specific

```
/learn backend: always add [ComputedEntityProperty] attribute to computed properties with empty setter
/learn frontend: extend AppBaseComponent instead of using raw Component
/learn workflow: always use TodoWrite before starting multi-step tasks
```

## How It Works

1. **Detection**: The pattern-learner hook detects your teaching input
2. **Extraction**: Extracts wrong/right pair, keywords, and context
3. **Storage**: Saves to `.claude/learned-patterns/{category}/{slug}.yaml`
4. **Injection**: Future sessions automatically inject relevant patterns based on context

## Pattern Categories

| Category | Use For |
|----------|---------|
| `backend` | C#, .NET, API, Entity, Repository patterns |
| `frontend` | Angular, TypeScript, Component, Store patterns |
| `workflow` | Development process, git, planning patterns |
| `general` | Cross-cutting concerns |

## Confidence System

- Explicit teaching starts at **80% confidence**
- Implicit corrections (detected from "no, do X instead") start at **40% confidence**
- Confidence increases when pattern is:
  - Confirmed by user
  - Injected and followed
- Confidence decreases when:
  - Pattern conflicts with user action
  - 30 days pass without use (decay)
- Patterns below **20% confidence** are auto-archived

## Conflict Checking

Patterns that conflict with `docs/claude/*.md` documentation are blocked to prevent inconsistencies.

## Examples

### Backend Pattern
```
/learn backend: DTO mapping should be in the DTO class using MapToEntity(), not in command handlers
```

### Frontend Pattern
```
/learn frontend: always use .pipe(this.untilDestroyed()) for subscriptions in components
```

### Anti-Pattern
```
/learn never call external APIs directly in command handlers - use Entity Event Handlers for side effects
```

### Code Style
```
/learn [wrong] items.Select(x => new Dto(x)).ToList() [right] items.SelectList(x => new Dto(x))
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/learned-patterns` | List and manage learned patterns |
| `/learned-patterns view <id>` | View specific pattern details |
| `/learned-patterns archive <id>` | Archive a pattern |
| `/learned-patterns boost <id>` | Increase pattern confidence |

## Storage Location

Patterns are stored in:
```
.claude/learned-patterns/
  index.yaml              # Pattern lookup index
  backend/                # Backend patterns
  frontend/               # Frontend patterns
  workflow/               # Workflow patterns
  general/                # General patterns
  archive/                # Archived patterns
```

## Tips

1. **Be Specific**: Include context about when the pattern applies
2. **Use Examples**: Code blocks help clarify exact patterns
3. **Categorize**: Prefix with category for better organization
4. **Review Periodically**: Use `/learned-patterns` to review and prune

## Technical Details

- Storage: YAML files in `.claude/learned-patterns/`
- Detection: `pattern-learner.cjs` hook on UserPromptSubmit
- Injection: `pattern-injector.cjs` hook on SessionStart and PreToolUse
- Max injection: 5 patterns per context, ~400 tokens budget
