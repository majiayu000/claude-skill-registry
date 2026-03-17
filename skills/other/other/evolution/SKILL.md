---
name: evolution
description: Self-improving skill system for Pi Agent development. Features self-evolution (accumulate knowledge), self-correction (fix errors automatically), self-validation (verify accuracy), usage feedback (track pattern health), and integration with workhub for documentation management.
---

# Evolution Skill

This skill enables Pi Agent to self-improve continuously during development by capturing learnings, correcting errors, and validating skills.

## Quick Navigation

| Topic | Description |
|-------|-------------|
| [Hooks Integration](#hooks-integration) | Auto-trigger evolution with Pi Agent hooks |
| [When to Evolve](#when-to-evolve) | Triggers and classification |
| [Evolution Process](#evolution-process) | Step-by-step guide |
| [Self-Correction](#self-correction) | Auto-fix skill errors |
| [Self-Validation](#self-validation) | Verify skill accuracy |
| [Workhub Integration](#workhub-integration) | Issue/PR management |

---

## Hooks Integration

Evolution uses Pi Agent's hooks system to automatically detect opportunities for improvement.

### Hook Installation

Create or edit `~/.pi/hooks/evolution.ts`:

```typescript
import type { HookAPI } from "@mariozechner/pi-coding-agent/hooks";

export default function (api: HookAPI) {
  // Monitor tool results for error detection
  api.on("tool_result", async (event, ctx) => {
    if (event.tool === "bash") {
      await detectErrorPatterns(event, ctx);
    }
  });

  // Monitor session end for learning capture
  api.on("session", async (event, ctx) => {
    if (event.reason === "shutdown") {
      await promptLearningCapture(ctx);
    }
  });

  // Monitor context for new patterns
  api.on("context", async (event, ctx) => {
    await detectNewPatterns(event, ctx);
  });
}
```

### What Hooks Do

| Hook Event | Trigger | Action |
|------------|---------|--------|
| `tool_result` | After bash command | Detect compilation errors, suggest fixes |
| `session` (shutdown) | Session ends | Prompt to capture learnings |
| `context` | Context transformation | Analyze for new patterns |

---

## When to Evolve

Trigger skill evolution when any of these occur during development:

| Trigger | Target Skill | Priority |
|---------|--------------|----------|
| New coding pattern discovered | Relevant skill | High |
| Error/debug solution found | troubleshooting skill | High |
| API usage pattern learned | core/reference skill | High |
| Build/packaging issue resolved | deployment skill | Medium |
| Project structure insight | getting-started skill | Low |
| Core concept clarified | core skill | Low |

---

## Evolution Process

### Step 1: Identify Knowledge Worth Capturing

Ask yourself:
- Is this a reusable pattern? (not project-specific)
- Did it take significant effort to figure out?
- Would it help other developers using Pi Agent?
- Is it not already documented in existing skills?

### Step 2: Classify the Knowledge

```
Coding Pattern           → relevant skill (e.g., typescript, patterns)
Error/Debug Solution     → troubleshooting skill
API Usage Pattern        → core/reference skill
Build/Deploy Issue       → deployment skill
Project Structure        → getting-started skill
Core Concept/API         → core skill
```

### Step 3: Use Workhub to Create Issue

```bash
# From project root directory
cd /path/to/project
bun ~/.pi/agent/skills/workhub/lib.ts create issue "evolution: add new pattern" [category]
```

### Step 4: Format the Contribution

**For Patterns**:
```markdown
## Pattern N: [Pattern Name]

Brief description of what this pattern solves.

### Implementation
\`\`\`typescript
// TypeScript code
\`\`\`

### Usage
\`\`\`typescript
// Example usage
\`\`\`
```

**For Troubleshooting**:
```markdown
### [Error Type/Message]

**Symptom**: What the developer sees

**Cause**: Why this happens

**Solution**:
\`\`\`typescript
// Fixed code
\`\`\`
```

### Step 5: Mark Evolution

Add an evolution marker above new content:

```markdown
<!-- Evolution: YYYY-MM-DD | source: project-name | author: @user -->
```

### Step 6: Submit via Workhub PR

```bash
# Create PR for your contribution
bun ~/.pi/agent/skills/workhub/lib.ts create pr "evolution: add new pattern" [category]
```

---

## Self-Correction

When skill content causes errors, automatically correct it.

### Trigger Conditions

```
User follows skill advice → Code fails to compile/run
                      ↓
                 Detect error
                      ↓
         Suggest correction to user
                      ↓
         Create workhub issue with fix
```

### Correction Flow

1. **Detect** - Skill advice led to an error
2. **Verify** - Confirm the skill content is wrong
3. **Suggest** - Propose fix to user
4. **Create Issue** - Document in workhub

### Correction Marker Format

```markdown
<!-- Correction: YYYY-MM-DD | was: [old advice] | reason: [why it was wrong] -->
```

---

## Self-Validation

Periodically verify skill content is still accurate.

### Validation Checklist

```markdown
## Validation Report

### Code Examples
- [ ] All TypeScript code compiles
- [ ] All patterns work as documented
- [ ] All examples are up-to-date

### API Accuracy
- [ ] API references are correct
- [ ] Method signatures are accurate
- [ ] Dependencies are current

### Documentation
- [ ] Instructions are clear
- [ ] Examples are complete
- [ ] Links are valid
```

### Validation Prompt

> "Please validate skills against current Pi Agent version and dependencies"

---

## Workhub Integration

Evolution skill extends workhub for documentation management.

### Creating Evolution Issues

```bash
# From project root
bun ~/.pi/agent/skills/workhub/lib.ts create issue "evolution: [description]" "evolution"
```

### Issue Template

```markdown
# Evolution: [Title]

## Type
- [ ] New pattern
- [ ] Error fix
- [ ] API update
- [ ] Documentation improvement

## Source
- Project: [project-name]
- File: [file-path]
- Context: [brief description]

## Content
[Detailed content to add]

## Target Skill
[Which skill should this be added to?]

## Validation
- [ ] Code tested
- [ ] Documentation updated
- [ ] Examples verified
```

### Creating Evolution PRs

```bash
# From project root
bun ~/.pi/agent/skills/workhub/lib.ts create pr "evolution: [description]" "evolution"
```

### PR Template

```markdown
# Evolution: [Title]

## Related Issue
#issue-number

## Changes
- [ ] Added new content
- [ ] Updated existing content
- [ ] Fixed errors
- [ ] Updated examples

## Files Changed
- [file1.md]
- [file2.md]

## Testing
- [ ] Tested locally
- [ ] Verified accuracy
- [ ] Checked for side effects
```

---

## Auto-Evolution Prompts

Use these prompts to trigger self-evolution:

### After Solving a Problem
> "This solution should be added to skills for future reference. Use workhub to create an evolution issue."

### After Creating a Pattern
> "This pattern is reusable. Let me create an evolution issue to document it."

### After Debugging
> "This error and its fix should be documented. Create an evolution issue in workhub."

### After Completing a Feature
> "Review what I learned and create evolution issues if applicable."

---

## Quality Guidelines

### DO Add
- Generic, reusable patterns
- Common errors with clear solutions
- Well-tested code examples
- Platform-specific gotchas
- Performance optimizations
- TypeScript/JavaScript best practices

### DON'T Add
- Project-specific code
- Unverified solutions
- Duplicate content
- Incomplete examples
- Personal preferences without rationale

---

## Continuous Improvement Checklist

After each development session, consider:

- [ ] Did I discover a new coding pattern?
- [ ] Did I solve a tricky error?
- [ ] Did I find a better way to structure code?
- [ ] Did I learn something about TypeScript/JavaScript?
- [ ] Did I encounter and fix a confusing issue?
- [ ] Would any of this help other developers?

If yes to any, use workhub to create an evolution issue!

---

## References

- [Workhub Skill](~/.pi/agent/skills/workhub/SKILL.md)
- [Pi Agent Hooks](https://github.com/badlogic/pi-mono/wiki/@mariozechner/pi-coding-agent#4.9-hooks-system)
- [Pi Agent Skills](https://github.com/badlogic/pi-mono/wiki/@mariozechner/pi-coding-agent#4.10-skills-system)