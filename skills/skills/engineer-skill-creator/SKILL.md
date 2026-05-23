---
name: engineer-skill-creator
description: Transform extracted engineer expertise into an actionable skill with progressive disclosure, allowing agents to find and apply relevant patterns for specific tasks.
---

# Engineer Skill Creator

Transform extracted engineer profiles into ready-to-use skills with progressive disclosure, enabling AI agents to efficiently find and apply the right expertise for any coding task.

## What This Skill Does

Takes the output from **engineer-expertise-extractor** and creates a structured, queryable skill that:
- **Organizes expertise by task type** - Find relevant patterns quickly
- **Uses progressive disclosure** - Show only what's needed for current task
- **Provides contextual examples** - Real code samples for specific scenarios
- **Guides agents intelligently** - Help find the right expertise at the right time
- **Enables task-specific queries** - "How would they handle authentication?"

## The Two-Step Process

### Step 1: Extract (engineer-expertise-extractor)
```bash
./extract_engineer.sh senior_dev
# Output: engineer_profiles/senior_dev/
```

### Step 2: Create Skill (THIS SKILL)
```bash
./create_expert_skill.sh senior_dev
# Output: expert-skills/senior-dev-mentor/
```

**Result:** A ready-to-use skill that agents can query for specific guidance.

## Why Progressive Disclosure Matters

**Without progressive disclosure:**
- Agent gets all expertise at once (overwhelming)
- Hard to find relevant information
- Context limits reached quickly
- Inefficient and slow

**With progressive disclosure:**
- Agent asks specific question
- Gets only relevant expertise
- Focused, actionable guidance
- Efficient use of context
- Faster, better results

## Output Structure

When you create a skill from an engineer profile, you get:

```
expert-skills/
└── [engineer-name]-mentor/
    ├── SKILL.md (skill documentation)
    ├── query_expertise.sh (interactive query tool)
    ├── expertise/
    │   ├── by_task/
    │   │   ├── authentication.md
    │   │   ├── api_design.md
    │   │   ├── database_design.md
    │   │   ├── error_handling.md
    │   │   └── testing.md
    │   ├── by_language/
    │   │   ├── typescript.md
    │   │   ├── python.md
    │   │   └── go.md
    │   ├── by_pattern/
    │   │   ├── dependency_injection.md
    │   │   ├── repository_pattern.md
    │   │   └── factory_pattern.md
    │   └── quick_reference/
    │       ├── coding_style.md
    │       ├── naming_conventions.md
    │       └── best_practices.md
    └── examples/
        ├── authentication_service.ts
        ├── api_controller.ts
        └── test_example.spec.ts
```

## Progressive Disclosure System

### Query by Task

**Agent asks:** "How would they implement user authentication?"

**Skill provides:**
1. Relevant patterns from `by_task/authentication.md`
2. Code examples from their auth PRs
3. Their testing approach for auth
4. Security considerations they use
5. Related best practices

**NOT provided (yet):**
- Unrelated patterns
- Database design details
- Payment processing approach
- Everything else

### Query by Language

**Agent asks:** "Show me their TypeScript coding style"

**Skill provides:**
1. TypeScript-specific conventions
2. Type usage patterns
3. Interface design approach
4. Error handling in TS
5. Real TS examples

### Query by Pattern

**Agent asks:** "How do they implement dependency injection?"

**Skill provides:**
1. DI pattern from their code
2. Constructor injection examples
3. IoC container setup
4. Testing with DI
5. When they use it vs when they don't

## Skill Usage by Agents

### Basic Query
```
"Using the skill expert-skills/senior-dev-mentor/, show me how to
implement authentication"
```

**Skill responds with:**
- Authentication patterns they use
- Real code examples
- Testing approach
- Security practices
- Step-by-step guidance

### Language-Specific Query
```
"Using expert-skills/senior-dev-mentor/, write a TypeScript service
following their style"
```

**Skill provides:**
- TypeScript coding conventions
- Class structure patterns
- Type definitions approach
- Import organization
- Testing patterns for services

### Pattern-Specific Query
```
"Using expert-skills/senior-dev-mentor/, implement the repository
pattern as they would"
```

**Skill provides:**
- Their repository pattern implementation
- Interface definitions
- Concrete implementation example
- Testing approach
- When to use this pattern

## Created Skill Features

### 1. Task-Based Navigation
Expertise organized by common development tasks:
- Authentication & Authorization
- API Design
- Database Design
- Error Handling
- Testing Strategies
- Performance Optimization
- Security Practices
- Code Review Guidelines

### 2. Language-Specific Guidance
Separate docs for each language they use:
- Naming conventions per language
- Language-specific patterns
- Idiomatic code examples
- Framework preferences

### 3. Pattern Library
Design patterns they commonly use:
- When to apply each pattern
- Implementation examples
- Testing approach
- Common pitfalls to avoid

### 4. Quick Reference
Fast access to essentials:
- Coding style at a glance
- Naming conventions cheat sheet
- Common commands/snippets
- Review checklist

### 5. Interactive Query Tool
Script that helps find expertise:
```bash
./query_expertise.sh

What are you working on?
1) Authentication
2) API Design
3) Database
4) Testing
5) Custom query

Select: 1

=== Authentication Expertise ===

[Shows relevant patterns, examples, best practices]
```

## How Skills Are Created

### Input
Engineer profile from extractor:
```
engineer_profiles/senior_dev/
├── coding_style/
├── patterns/
├── best_practices/
├── architecture/
├── code_review/
└── examples/
```

### Process
1. **Analyze profile structure**
2. **Categorize by task** - Group related expertise
3. **Extract examples** - Pull relevant code samples
4. **Create navigation** - Build progressive disclosure system
5. **Generate queries** - Create query tool
6. **Package skill** - Ready-to-use skill structure

### Output
Skill with progressive disclosure:
```
expert-skills/senior-dev-mentor/
├── SKILL.md
├── query_expertise.sh
├── expertise/
│   ├── by_task/
│   ├── by_language/
│   ├── by_pattern/
│   └── quick_reference/
└── examples/
```

## Example Created Skill

### Authentication Task Doc

**File:** `expertise/by_task/authentication.md`

```markdown
# Authentication - Senior Dev's Approach

## Overview
How senior_dev implements authentication based on 15 PRs analyzed.

## Preferred Approach
- JWT-based authentication
- Refresh token rotation
- HttpOnly cookies for web
- Token in headers for mobile/API

## Implementation Pattern

### Service Structure
[Code example from their PR #1234]

### Token Generation
[Code example from their PR #5678]

### Token Validation
[Code example from their PR #9012]

## Testing Approach
- Unit tests for token generation
- Integration tests for auth flow
- Security tests for token validation

[Test examples from their code]

## Security Considerations
From their code reviews:
- Always validate token signature
- Check expiration
- Implement rate limiting
- Use secure random for secrets

## Common Pitfalls They Avoid
- Storing tokens in localStorage (XSS risk)
- Not rotating refresh tokens
- Weak secret keys
- Missing token expiration

## Related Patterns
- Error handling for auth failures
- Middleware pattern for auth checks
- Repository pattern for user lookup

## Examples
See: examples/authentication_service.ts
```

## Use Cases

### 1. Consistent Code Generation

**Problem:** AI generates code that doesn't match team style

**Solution:**
```
"Using expert-skills/senior-dev-mentor/, write a user service"
```

**Result:** Code matching senior dev's exact style and patterns

### 2. Task-Specific Guidance

**Problem:** How would senior dev approach this specific problem?

**Solution:**
```
"Using expert-skills/tech-lead-mentor/, how do I handle rate limiting?"
```

**Result:** Their specific approach, examples, and reasoning

### 3. Code Review Training

**Problem:** Learn what experienced engineer looks for

**Solution:**
```
"Using expert-skills/architect-mentor/, review this code"
```

**Result:** Review following their standards and priorities

### 4. Onboarding

**Problem:** New engineer needs to learn team conventions

**Solution:** Give them access to expert-skills

**Result:** Learn from real examples, specific to their tasks

## Skill Query Examples

### Example 1: Authentication
```bash
./query_expertise.sh
> Working on: Authentication
> Language: TypeScript

Output:
=== Authentication in TypeScript ===

Preferred approach: JWT with refresh tokens

[Shows specific auth pattern]
[Provides TS code example]
[Testing strategy]
[Security checklist]

Related: error_handling.md, api_design.md
```

### Example 2: Database Design
```bash
./query_expertise.sh
> Working on: Database design
> Database: PostgreSQL

Output:
=== Database Design - PostgreSQL ===

Schema design approach:
- Normalized tables
- Foreign keys enforced
- Indexes on lookups
- Migrations for changes

[Shows migration example]
[Query optimization patterns]
[Testing approach]
```

### Example 3: Error Handling
```bash
./query_expertise.sh
> Working on: Error handling
> Language: Python

Output:
=== Error Handling in Python ===

Pattern: Custom exception classes + global handler

[Shows exception hierarchy]
[Handler implementation]
[Logging approach]
[User-facing messages]
```

## Creating a Skill

### Basic Usage
```bash
cd engineer-skill-creator
./scripts/create_expert_skill.sh [engineer-username]
```

### Advanced Usage
```bash
./scripts/create_expert_skill.sh [engineer-username] --focus api,testing
```

Limits skill to specific focus areas.

### What Gets Generated

**Automatic categorization:**
- Groups related patterns
- Organizes by common tasks
- Separates by language
- Highlights best practices

**Query system:**
- Interactive CLI tool
- Smart search
- Related content linking
- Example suggestions

**Documentation:**
- Task-specific guides
- Language references
- Pattern library
- Quick reference cards

## Integration with Development Workflow

### In Claude Code
```
"Load the expert-skills/senior-dev-mentor/ skill and help me
implement this feature following their approach"
```

### In Code Review
```
"Using expert-skills/tech-lead-mentor/, review this PR for:
- Code style compliance
- Pattern usage
- Best practices
- Security considerations"
```

### In Architecture Decisions
```
"Using expert-skills/architect-mentor/, how would they design
this microservice?"
```

## Skill Maintenance

### Updating Skills
When engineer profile is updated:
```bash
./scripts/update_expert_skill.sh senior-dev
```

Re-generates skill with new expertise.

### Version Control
Each skill generation includes:
- Source profile version
- Generation date
- Expertise count
- Last PR analyzed

## Best Practices

### When Creating Skills

**DO:**
- ✅ Create skills for different expertise areas
- ✅ Update skills regularly (quarterly)
- ✅ Test queries before deploying
- ✅ Document what the skill covers

**DON'T:**
- ❌ Create skills from insufficient data (< 20 PRs)
- ❌ Mix multiple engineers in one skill
- ❌ Ignore profile updates
- ❌ Over-categorize (keep it simple)

### When Using Skills

**DO:**
- ✅ Ask specific questions
- ✅ Provide context (language, task)
- ✅ Reference examples
- ✅ Combine with your judgment

**DON'T:**
- ❌ Blindly copy patterns
- ❌ Skip understanding reasoning
- ❌ Ignore project context
- ❌ Treat as inflexible rules

## Limitations

**What Skills Can Do:**
- ✅ Provide proven patterns
- ✅ Show real examples
- ✅ Guide implementation
- ✅ Explain reasoning
- ✅ Surface best practices

**What Skills Cannot Do:**
- ❌ Make decisions for you
- ❌ Understand your specific context
- ❌ Replace senior engineer judgment
- ❌ Guarantee correctness
- ❌ Adapt to new technologies automatically

## Summary

The Engineer Skill Creator transforms extracted expertise into actionable, queryable skills:

**Input:** Engineer profile (from extractor)
**Process:** Categorize, organize, create query system
**Output:** Progressive disclosure skill

**Benefits:**
- Find expertise fast
- Get task-specific guidance
- Learn from real examples
- Maintain consistency
- Scale knowledge

**Use with agents:**
```
"Using expert-skills/[engineer]-mentor/, [task description]"
```

**The complete workflow:**
1. Extract expertise: `extract_engineer.sh username`
2. Create skill: `create_expert_skill.sh username`
3. Use with agents: Reference skill in prompts
4. Get consistent, expert-level results

---

**"Progressive disclosure: Show only what's needed, when it's needed."**
