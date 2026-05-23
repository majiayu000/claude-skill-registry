---
name: planning-research
description: Use when tackling complex features, architectural decisions, or problems requiring careful thought. Enforces research and planning BEFORE implementation to improve design quality.
---

# Planning & Research Workflow

## Core Principle
**"Research and plan first - code later."**

Claude tends to jump straight into coding. For complex problems requiring deeper thinking, force explicit research and planning phases BEFORE writing any code.

## Before You Start

Follow the standard development workflow from CLAUDE.md before beginning any feature work:

1. **Checkout and pull main:** `git checkout main && git pull`
2. **Create branch with issue number:** `git checkout -b <type>/<issue-number>-<description>`
3. **Update project board status** to "In Progress" (see CLAUDE.md "GitHub Project Board Updates" section)

Branch naming convention: `<type>/<issue-number>-<short-description>`
- Examples: `feat/42-add-folder-support`, `fix/15-login-token-refresh`

## When to Use

✅ **Always plan first for:**
- New feature implementation (3+ files affected)
- Architecture decisions or refactoring
- Integration with external services
- Security-sensitive code (authentication, encryption)
- Performance-critical paths
- Complex business logic
- Debugging non-trivial issues

⚠️ **Skip planning for:**
- Simple bug fixes (1-2 line changes)
- Typo corrections
- Adding obvious tests
- Documentation updates

## The Three-Phase Workflow

### Phase 1: RESEARCH
**Understand the problem deeply before proposing solutions.**

1. **Read existing code**
   - Find related implementations
   - Identify patterns already in use
   - Note libraries and frameworks in play
   - Understand current architecture

2. **Identify constraints**
   - Security requirements
   - Performance requirements
   - Backward compatibility needs
   - Platform/framework limitations

3. **Gather context**
   - Review documentation
   - Check for existing tests
   - Find similar solved problems
   - Note edge cases

**Output:** Summary of findings, constraints, and open questions.

### Phase 2: PLAN
**Design the solution with multiple approaches.**

1. **Propose 2-3 approaches**
   - Describe each option clearly
   - List pros and cons for each
   - Note trade-offs (complexity vs performance, etc.)
   - Identify risks

2. **Recommend one approach**
   - State which option you recommend
   - Explain why (aligns with constraints, simpler, etc.)
   - Show how it integrates with existing code

3. **Define implementation steps**
   - Break down into concrete tasks
   - Identify files to create/modify
   - Note testing strategy
   - Call out risky or complex parts

**Output:** Written plan with approach comparison and recommended implementation.

### Phase 3: EXECUTE
**Implement the plan with TDD.**

1. **Follow the plan** - Don't deviate without discussion
2. **Use TDD** - Tests first for all new code
3. **Verify each step** - Test after each change
4. **Update plan if needed** - Document discoveries

## Example: Adding User Authentication

### RESEARCH Output
```markdown
## Research: User Authentication

**Existing patterns found:**
- No authentication currently exists
- FastAPI app with SQLAlchemy models
- Pydantic schemas for validation
- PostgreSQL database

**Constraints:**
- Zero-knowledge architecture (server never sees master password)
- Must use authHash validation (not password)
- JWT tokens for session management
- Audit logging required

**Libraries in use:**
- FastAPI, SQLAlchemy 2.0, Pydantic V2
- Need to add: python-jose[cryptography], passlib[argon2]

**Open questions:**
- Token expiration time? (Recommend: 2 hours)
- Refresh token strategy? (Not in MVP)
```

### PLAN Output
```markdown
## Plan: User Authentication Implementation

**Approach 1: JWT with database token storage**
Pros: Can revoke tokens, audit trail
Cons: Database hit on every request, complexity
Risk: Performance impact

**Approach 2: Stateless JWT (RECOMMENDED)**
Pros: No database lookups, scalable, simple
Cons: Can't revoke until expiration
Risk: Compromise requires waiting for expiry

**Recommendation:** Approach 2 - Stateless JWT
- Aligns with zero-knowledge architecture
- Simpler for MVP
- Performance benefits
- Can add token blacklist later if needed

**Implementation steps:**
1. Add JWT dependencies to pyproject.toml
2. Create auth utilities (token generation/validation)
3. Create `/auth/login` endpoint (validates authHash, returns JWT)
4. Create auth dependency for protected routes
5. Update user model with authHash field
6. Add tests for each component
7. Update existing endpoints to require authentication

**Files to modify:**
- `app/models/user.py` - Add authHash field
- `app/schemas/auth.py` - Create LoginRequest/TokenResponse
- `app/routers/auth.py` - NEW - Login endpoint
- `app/dependencies.py` - Add get_current_user dependency
- `app/utils/security.py` - NEW - JWT functions
- `pyproject.toml` - Add python-jose, passlib to dependencies

**Testing strategy:**
- Unit tests for JWT generation/validation
- Integration tests for login endpoint
- Test invalid/expired tokens
- Test protected endpoint access
```

### EXECUTE
Now implement following TDD and the plan above.

## Common Planning Mistakes

**Jumping to code too quickly:**
```
# Bad: No research or planning
User: "Add user authentication"
Claude: "I'll create the auth module..."
[starts writing code immediately]

# Good: Research first
User: "Add user authentication"
Claude: "Let me research the existing codebase first..."
[reads code, identifies patterns, understands constraints]
Claude: "Here's what I found... [research summary]"
Claude: "I recommend approach X because... [plan with options]"
User: "Sounds good, proceed"
Claude: [implements with TDD]
```

**One-size-fits-all solutions:**
```
# Bad: Only one option
"I'll use JWT authentication"

# Good: Multiple approaches considered
"Option 1: JWT (stateless, scalable)
 Option 2: Session tokens (revocable)
 Option 3: OAuth (external provider)
 Recommendation: Option 1 because..."
```

**Vague implementation steps:**
```
# Bad: Too vague
"1. Add authentication
 2. Update endpoints
 3. Test"

# Good: Specific and actionable
"1. Add python-jose to pyproject.toml [dev] dependencies
 2. Create app/utils/security.py with create_token(), verify_token()
 3. Create app/schemas/auth.py with LoginRequest, TokenResponse
 4. Create app/routers/auth.py with POST /auth/login endpoint
 5. Add get_current_user dependency in app/dependencies.py
 6. Update app/routers/users.py to use Depends(get_current_user)
 7. Write tests for each component"
```

## Questions to Answer in Planning

1. **What patterns already exist?** (consistency)
2. **What are the constraints?** (security, performance, compatibility)
3. **What are 2-3 ways to solve this?** (don't commit to first idea)
4. **What are the trade-offs?** (help user make informed decision)
5. **What files need to change?** (scope understanding)
6. **How will we test this?** (quality assurance)
7. **What could go wrong?** (risk mitigation)

## Red Flags That You Skipped Planning

🚩 Starting to code within 30 seconds of request
🚩 Not reading existing related code first
🚩 Only proposing one solution
🚩 Not considering trade-offs
🚩 Vague "add feature X" steps
🚩 No testing strategy mentioned
🚩 Not asking clarifying questions for complex requests

## Key Principles

1. **Research first**: Understand before solving
2. **Multiple options**: Consider 2-3 approaches
3. **Explicit trade-offs**: Help user decide
4. **Detailed steps**: Clear, actionable tasks
5. **Testing strategy**: Plan verification
6. **Written plan**: Document for reference
7. **User approval**: Get buy-in before coding

**Planning takes 5-10 minutes. Fixing bad design takes hours.**
