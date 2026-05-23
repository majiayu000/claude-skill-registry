---
name: skill-activator
description: Guide for making skills discoverable and ensuring they get invoked at the right time. Use when creating new skills or troubleshooting why existing skills aren't being called.
---

# Skill Activator: Make Your Skills Work

## Purpose

Ensure skills are discovered and invoked at the right time by designing effective triggers and descriptions.

## Why Skills Don't Get Called

| Problem | Cause | Solution |
|---------|-------|----------|
| Never invoked | Description doesn't match user language | Add trigger phrases |
| Invoked at wrong time | Description too broad | Add "Use when" / "Don't use when" |
| Invoked but ignored | Low relevance signal | Make description more specific |

## The Skill Description Formula

```
[What it does] + [When to use] + [Trigger phrases]
```

### Bad Example
```yaml
description: Code review skill
```
- Too vague
- No trigger phrases
- Doesn't say when to use

### Good Example
```yaml
description: >
  Perform structured code review with security, performance, and
  maintainability checks. Use when reviewing PRs, before merging,
  or when user says "review", "check this code", or "find issues".
```
- Specific about what it does
- Clear when to use
- Multiple trigger phrases

## Trigger Phrase Design

### Match User Language

Think about how users actually ask for things:

| User Says | Skill Should Match |
|-----------|-------------------|
| "review this" | code-review |
| "check for bugs" | code-review, debug |
| "is this secure?" | security-review |
| "make it faster" | performance-optimization |
| "clean this up" | refactoring |

### Include Variations

```yaml
description: >
  ... Use when user says "review", "check", "look at",
  "find issues", "is this good", or "before merging".
```

## The Description Template

```markdown
---
name: {skill-name}
description: >
  {One sentence: what this skill does}.
  Use when {specific situations}.
  Trigger phrases: "{phrase1}", "{phrase2}", "{phrase3}".
  Don't use when {exclusions}.
---
```

### Complete Example

```markdown
---
name: api-design
description: >
  Design RESTful APIs following best practices for naming,
  versioning, and error handling. Use when creating new endpoints,
  reviewing API design, or planning API changes. Trigger phrases:
  "design API", "new endpoint", "REST structure", "API review".
  Don't use for GraphQL or internal service communication.
---
```

## Skill Audit Checklist

Review each skill against this checklist:

### Discoverability
- [ ] Description is under 200 characters (for readability)
- [ ] First sentence clearly states purpose
- [ ] Contains 3+ trigger phrases
- [ ] Trigger phrases match real user language

### Specificity
- [ ] "Use when" is specific, not generic
- [ ] "Don't use when" excludes wrong contexts
- [ ] Doesn't overlap significantly with other skills

### Invocation Testing
- [ ] Tested with natural language requests
- [ ] Verified it's called in expected scenarios
- [ ] Verified it's NOT called in wrong scenarios

## Skill Categories and Conventions

### By Invocation Style

| Style | `disable-model-invocation` | When to Use |
|-------|---------------------------|-------------|
| Auto-invoked | `false` or omitted | Should trigger automatically based on context |
| Manual only | `true` | User must explicitly call with `/skill-name` |

### When to Use Manual-Only

- Destructive operations (delete, reset)
- Long-running processes
- Operations with side effects
- User preference workflows

## Debugging Skill Invocation

### Skill Not Being Called?

1. **Check description** - Does it match how users ask?
2. **Check triggers** - Are trigger phrases natural?
3. **Check competition** - Is another skill taking priority?
4. **Test directly** - Call with `/skill-name` to verify it works

### Skill Called at Wrong Time?

1. **Add exclusions** - "Don't use when..."
2. **Narrow scope** - Make "Use when" more specific
3. **Split skill** - Maybe it's doing too many things

## Skill Discovery Commands

### List Available Skills
```
/help skills
```

### Test Skill Matching
Ask Claude: "Which skill would you use for [scenario]?"

### Force Skill Invocation
```
/skill-name [arguments]
```

## Integration with Other Skills

- Use **intent-first** to clarify what the user needs
- Use **delegation-triggers** to decide if a skill or agent is appropriate
- Then activate the right skill based on the clarified intent
