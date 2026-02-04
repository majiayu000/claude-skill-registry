---
name: feature-dev
description: Feature Development Workflow - 7-phase structured approach for building features. Based on Anthropic's official feature-dev plugin. Activates for build feature, implement feature, feature development, feature workflow, structured development.
argument-hint: "[FEATURE_DESCRIPTION]"
---

# Feature Development Command

**7-phase structured workflow for building features systematically, rather than jumping directly into coding.**

Based on Anthropic's official feature-dev plugin: "Building features requires more than just writing code."

## Philosophy

This workflow prioritizes:
1. **Understanding** your codebase first
2. **Asking** clarifying questions before design
3. **Designing** thoughtfully before implementation
4. **Reviewing** quality before declaring complete

## The 7 Phases

### Phase 1: Discovery
**Goal**: Clarify requirements and constraints

Questions to answer:
- What problem does this feature solve?
- Who are the users?
- What are the success criteria?
- What are the constraints (time, tech, resources)?
- What's out of scope?

**Output**: Clear feature definition with acceptance criteria

### Phase 2: Codebase Exploration
**Goal**: Understand existing patterns and architecture

Actions:
1. Identify similar features in the codebase
2. Understand the tech stack and conventions
3. Map relevant files and modules
4. Note architectural patterns in use

**Tools**: Use code-explorer agent for deep analysis

**Output**: Understanding of how to integrate with existing code

### Phase 3: Clarifying Questions
**Goal**: Resolve ambiguities before design

Ask about:
- Edge cases not covered in requirements
- Integration points with other systems
- Performance expectations
- Security considerations
- Migration/rollout strategy

**Output**: Clear answers to all open questions

### Phase 4: Architecture Design
**Goal**: Compare 2-3 implementation approaches

For each approach, document:
- High-level design
- Trade-offs (pros/cons)
- Estimated complexity
- Risk factors
- Integration impact

**Tools**: Use code-architect agent for detailed blueprints

**Output**: Chosen approach with rationale

### Phase 5: Implementation
**Goal**: Build following chosen architecture

Best practices:
- Follow TDD where appropriate
- Implement in small, testable increments
- Keep commits focused and atomic
- Update tests as you go

**Output**: Working feature code with tests

### Phase 6: Quality Review
**Goal**: Check for bugs, quality issues, and conventions

Review checklist:
- [ ] All tests pass
- [ ] Code coverage meets threshold
- [ ] No security vulnerabilities
- [ ] Error handling complete
- [ ] Logging appropriate
- [ ] Documentation updated
- [ ] Performance acceptable

**Tools**: Use pr-test-analyzer, silent-failure-hunter, code-reviewer agents

**Output**: Polished, production-ready code

### Phase 7: Summary
**Goal**: Document accomplishments and next steps

Create:
- Summary of what was built
- Key decisions made
- Known limitations
- Future improvements
- Handoff notes

**Output**: Complete feature documentation

## Usage

```bash
/sw:feature-dev "Add user authentication with JWT"
```

This will guide you through all 7 phases, asking questions at each stage.

## Integration with SpecWeave

This command integrates with SpecWeave workflow:

1. **Phase 1-3** → Creates/updates spec.md with requirements
2. **Phase 4** → Generates plan.md with architecture
3. **Phase 5** → Creates tasks.md and executes via /sw:do
4. **Phase 6** → Validates via /sw:validate
5. **Phase 7** → Closes via /sw:done

## When to Use Feature-Dev

**Good fit**:
- Complex features touching multiple files
- Features requiring architectural decisions
- New functionality in unfamiliar codebases
- Team features needing documentation

**Skip for**:
- Single-line fixes
- Trivial changes
- Urgent hotfixes
- Well-defined bug fixes

## Specialized Agents Used

| Phase | Agent | Purpose |
|-------|-------|---------|
| 2 | code-explorer | Deep codebase analysis |
| 4 | code-architect | Architecture blueprints |
| 6 | pr-test-analyzer | Test coverage analysis |
| 6 | silent-failure-hunter | Error handling audit |
| 6 | code-reviewer | Quality checks |

## Example Interaction

```
User: /sw:feature-dev "Add password reset flow"

Claude: Starting Feature Development Workflow

## Phase 1: Discovery

I need to understand the requirements for the password reset flow.

Questions:
1. How should users initiate password reset? (Email link, security questions, SMS?)
2. What's the token expiration time?
3. Should we notify users of password changes?
4. Are there any compliance requirements (GDPR, etc.)?

Please answer these questions to proceed to Phase 2.

---

User: Email link, 1 hour expiration, yes notify, GDPR compliant

Claude: ## Phase 2: Codebase Exploration

Let me analyze your existing auth system...

[Spawns code-explorer agent]

Found:
- Auth service at src/services/auth.ts
- User model at src/models/user.ts
- Email service at src/services/email.ts
- Existing token utilities at src/utils/tokens.ts

Your codebase uses:
- JWT for authentication
- Prisma for database
- Nodemailer for emails
- Express for API routes

Ready for Phase 3: Clarifying Questions?
```

## Best Practices

1. **Don't skip phases** - Each phase prevents future problems
2. **Document decisions** - Future you will thank present you
3. **Get stakeholder input** - Phase 3 questions often need product input
4. **Keep phases focused** - Don't bleed implementation into design
5. **Review before merging** - Phase 6 catches issues before production
